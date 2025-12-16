from pathlib import Path
import cv2


def extract_frames_stats(
    path: Path,
    sample_every_n: int = 4,
    max_frames: int = 300,
) -> dict:
    """
    Reads the video and samples frames.
    Returns stats only (for now) to prove the pipeline works.
    """
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise ValueError("Could not open video")

    fps = cap.get(cv2.CAP_PROP_FPS) or 0.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)

    processed = 0
    read_index = 0

    while processed < max_frames:
        ok, frame = cap.read()
        if not ok:
            break

        # sample: take every Nth frame
        if read_index % sample_every_n == 0:
            # later we will run pose detection on `frame`
            processed += 1

        read_index += 1

    cap.release()

    duration_sec = (total_frames / fps) if fps and total_frames else None

    return {
        "processed_frames": processed,
        "sample_every_n": sample_every_n,
        "duration_sec": duration_sec,
    }
