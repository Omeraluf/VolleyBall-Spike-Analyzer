# backend/app/models/schemas.py
from pydantic import BaseModel


class AnalysisSection(BaseModel):
    name: str
    score: float
    comment: str

class AnalysisMetrics(BaseModel):
    max_jump_cm: float | None = None
    approach_speed_m_s: float | None = None
    arm_angle_deg: float | None = None

    fps: float | None = None
    frame_count: int | None = None
    width: int | None = None
    height: int | None = None

    processed_frames: int | None = None
    sample_every_n: int | None = None
    duration_sec: float | None = None


class AnalysisResponse(BaseModel):
    overall_score: float
    sections: list[AnalysisSection]
    metrics: AnalysisMetrics

    