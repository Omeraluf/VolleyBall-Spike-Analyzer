from fastapi import APIRouter, UploadFile, File

from app.models.schemas import AnalysisResponse
from app.services.scoring import mock_score_spike
from app.services.video_ingest import save_upload_to_disk
from app.services.video_probe import probe_video
from app.services.frame_extraction import extract_frames_stats
from app.services.sampling import choose_sample_every_n
from app.services.pose_extraction import extract_pose_keypoints
from app.services.features import estimate_jump_height_cm_from_poses
from pathlib import Path
from app.services.debug_plots import save_series_plot
from app.services.features import extract_hip_y_series
from app.services.debug_frames import save_landmark_frames





router = APIRouter(tags=["analysis"])


@router.post("/analyze-spike", response_model=AnalysisResponse)
async def analyze_spike(file: UploadFile = File(...)):
    saved_path = await save_upload_to_disk(file)

    resp = mock_score_spike()
    info = probe_video(saved_path)

    # inject video info into metrics
    resp.metrics.fps = info["fps"]
    resp.metrics.frame_count = info["frame_count"]
    resp.metrics.width = info["width"]
    resp.metrics.height = info["height"]

    n = choose_sample_every_n(info["fps"])
    frame_stats = extract_frames_stats(saved_path, sample_every_n=n, max_frames=300)

    resp.metrics.sample_every_n = n
    resp.metrics.processed_frames = frame_stats["processed_frames"]
    resp.metrics.duration_sec = frame_stats["duration_sec"]

    poses = extract_pose_keypoints(
    saved_path,
    sample_every_n=resp.metrics.sample_every_n or 1,
    max_frames=300,
    )

    # TEMP: expose how many frames had a detected pose
    resp.metrics.detected_pose_frames = len(poses)

    jump_cm = estimate_jump_height_cm_from_poses(poses, assumed_height_cm=190.0)            # assume 190cm tall for now
    if jump_cm is not None:
        resp.metrics.max_jump_cm = round(jump_cm, 1)

    hip_y = extract_hip_y_series(poses)
    save_series_plot(
        hip_y,
        out_path=Path("backend/debug/hip_y.png"),
        title="Hip Y over time (lower = higher jump)"
    )

    save_landmark_frames(saved_path, Path("backend/debug/frames"), every_n=5, max_saved=20)


    return resp