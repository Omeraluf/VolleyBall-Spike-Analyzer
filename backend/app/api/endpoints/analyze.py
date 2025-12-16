# backend/app/api/endpoints/analyze.py
from fastapi import APIRouter, UploadFile, File

from app.models.schemas import AnalysisResponse
from app.services.scoring import mock_score_spike

router = APIRouter(tags=["analysis"])


@router.post("/analyze-spike", response_model=AnalysisResponse)
async def analyze_spike(file: UploadFile = File(...)):
    """
    For now: just accept the file and return a mock analysis.
    Later: we'll:
      - save video
      - extract frames
      - run pose detection
      - compute features
      - score based on rules
    """
    # you can inspect file.filename, file.content_type, etc. here if needed
    return mock_score_spike()
