from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]  # backend/
UPLOADS_DIR = PROJECT_ROOT / "uploads"

# Simple limits for v1
MAX_UPLOAD_MB = 200
ALLOWED_CONTENT_TYPES = {"video/mp4", "video/quicktime", "video/x-matroska"}  # mp4, mov, mkv
