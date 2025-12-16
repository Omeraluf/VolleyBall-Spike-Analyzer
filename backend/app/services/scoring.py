# backend/app/services/scoring.py
from app.models.schemas import AnalysisResponse, AnalysisSection, AnalysisMetrics


def mock_score_spike() -> AnalysisResponse:
    """
    Temporary fake scoring – later this will receive real features.
    """
    metrics = AnalysisMetrics(
        max_jump_cm=40.0,
        approach_speed_m_s=3.0,
        arm_angle_deg=135.0,
    )

    sections = [
        AnalysisSection(
            name="jump_height",
            score=70.0,
            comment="Try to jump a bit higher – aim for ~45–50cm.",
        ),
        AnalysisSection(
            name="approach_speed",
            score=80.0,
            comment="Nice approach speed – keep a smooth, controlled run-up.",
        ),
        AnalysisSection(
            name="arm_angle",
            score=85.0,
            comment="Good arm extension at contact – you're close to ideal.",
        ),
    ]

    overall_score = sum(s.score for s in sections) / len(sections)

    return AnalysisResponse(
        overall_score=overall_score,
        sections=sections,
        metrics=metrics,
    )
