from __future__ import annotations

import statistics
import mediapipe as mp

mp_pose = mp.solutions.pose


def estimate_jump_height_cm_from_poses(poses, assumed_height_cm: float = 175.0) -> float | None:
    """
    Estimate jump height from pose landmarks.
    Uses normalized coordinates:
      - baseline hip Y (standing) vs minimum hip Y (highest point)
      - scales by estimated body height in the frame (ankle_y - shoulder_y)
      - converts to cm using an assumed real height (rough estimate)
    """
    if not poses:
        return None

    hip_y = []
    body_h = []

    for pl in poses:
        lm = pl.landmark

        lh = lm[mp_pose.PoseLandmark.LEFT_HIP].y
        rh = lm[mp_pose.PoseLandmark.RIGHT_HIP].y
        hip_y.append((lh + rh) / 2.0)

        ls = lm[mp_pose.PoseLandmark.LEFT_SHOULDER].y
        rs = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].y
        la = lm[mp_pose.PoseLandmark.LEFT_ANKLE].y
        ra = lm[mp_pose.PoseLandmark.RIGHT_ANKLE].y

        shoulder_y = (ls + rs) / 2.0
        ankle_y = (la + ra) / 2.0
        body_h.append(max(ankle_y - shoulder_y, 1e-6))

    # baseline = typical hip position early in clip (first ~20 frames)
    early = hip_y[: min(20, len(hip_y))]
    baseline = statistics.median(early)
    peak = min(hip_y)  # smaller y = higher in image coords

    jump_norm = baseline - peak
    body_h_med = statistics.median(body_h)

    # Convert normalized jump to cm using assumed real height (estimate)
    jump_cm = (jump_norm / body_h_med) * assumed_height_cm
    return max(0.0, float(jump_cm))


def extract_hip_y_series(poses) -> list[float]:
    hip_y = []
    for pl in poses:
        lm = pl.landmark
        lh = lm[mp_pose.PoseLandmark.LEFT_HIP].y
        rh = lm[mp_pose.PoseLandmark.RIGHT_HIP].y
        hip_y.append((lh + rh) / 2.0)
    return hip_y
