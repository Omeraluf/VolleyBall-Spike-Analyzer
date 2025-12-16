from pathlib import Path
import cv2
import mediapipe as mp


mp_pose = mp.solutions.pose


def extract_pose_keypoints(
    path: Path,
    sample_every_n: int,
    max_frames: int = 300,
):
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise ValueError("Could not open video")

    poses = []

    with mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        enable_segmentation=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as pose:

        read_index = 0
        processed = 0

        while processed < max_frames:
            ok, frame = cap.read()
            if not ok:
                break

            if read_index % sample_every_n == 0:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result = pose.process(rgb)

                if result.pose_landmarks:
                    poses.append(result.pose_landmarks)

                processed += 1

            read_index += 1

    cap.release()
    return poses
