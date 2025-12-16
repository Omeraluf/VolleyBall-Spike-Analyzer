import uuid
from pathlib import Path

from fastapi import UploadFile, HTTPException

from app.core.config import UPLOADS_DIR, MAX_UPLOAD_MB, ALLOWED_CONTENT_TYPES


def _safe_suffix(filename: str) -> str:
    # Keep extension if it exists, default to ".mp4"
    suffix = Path(filename).suffix.lower()
    return suffix if suffix else ".mp4"


async def save_upload_to_disk(file: UploadFile) -> Path:
    # Basic type check (not perfect, but good for v1)
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported content type: {file.content_type}",
        )

    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

    suffix = _safe_suffix(file.filename or "")
    out_path = UPLOADS_DIR / f"{uuid.uuid4().hex}{suffix}"

    max_bytes = MAX_UPLOAD_MB * 1024 * 1024
    written = 0

    # Stream to disk in chunks (best practice: don’t read entire file into memory)
    with out_path.open("wb") as f:
        while True:
            chunk = await file.read(1024 * 1024)  # 1MB
            if not chunk:
                break
            written += len(chunk)
            if written > max_bytes:
                out_path.unlink(missing_ok=True)
                raise HTTPException(status_code=413, detail="File too large.")
            f.write(chunk)

    await file.close()
    return out_path
