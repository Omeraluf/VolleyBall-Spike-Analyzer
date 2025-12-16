from fastapi import APIRouter, UploadFile, File

from app.models.schemas import AnalysisResponse
from app.services.scoring import mock_score_spike
from app.services.video_ingest import save_upload_to_disk
from app.services.video_probe import probe_video
from app.services.frame_extraction import extract_frames_stats
from app.services.sampling import choose_sample_every_n
from app.services.pose_extraction import extract_pose_keypoints



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



    return resp