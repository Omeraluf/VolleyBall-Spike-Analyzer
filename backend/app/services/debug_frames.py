from pathlib import Path
import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

def save_landmark_frames(video_path: Path, out_dir: Path, every_n: int = 30, max_saved: int = 5):
    out_dir.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise ValueError("Could not open video")

    saved = 0
    idx = 0

    with mp_pose.Pose(model_complexity=1) as pose:
        while saved < max_saved:
            ok, frame = cap.read()
            if not ok:
                break

            if idx % every_n == 0:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                res = pose.process(rgb)

                if res.pose_landmarks:
                    mp_draw.draw_landmarks(frame, res.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                cv2.imwrite(str(out_dir / f"frame_{idx:05d}.jpg"), frame)
                saved += 1

            idx += 1

    cap.release()
