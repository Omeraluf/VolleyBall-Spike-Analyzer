# RUN IT BY
cd D:\Projects\volleyball-spike-analyzer

.venv\Scripts\activate

uvicorn app.main:app --reload --port 8000 --app-dir backend

http://127.0.0.1:8000/docs



# Volleyball Spike Analyzer – Current Pipeline (v0.1)

## What works right now (end-to-end)
1) Client uploads a video via API (Swagger UI now, React later)
2) Backend saves the video to disk: `backend/uploads/<uuid>.<ext>`
3) Backend probes the saved video with OpenCV:
   - fps
   - frame_count
   - width / height
4) Backend returns a JSON response (still mock scoring) that includes:
   - overall_score (mock)
   - tips/sections (mock)
   - metrics (real video info + mock spike metrics)

---

## Request → Response flow
### Request
- **POST** `/api/analyze-spike`
- Body: `multipart/form-data`
  - `file`: video file

### Response (JSON)
- `overall_score`: number (mock for now)
- `sections`: list of feedback sections (mock for now)
- `metrics`:
  - spike metrics: `max_jump_cm`, `approach_speed_m_s`, `arm_angle_deg` (mock for now)
  - video metrics: `fps`, `frame_count`, `width`, `height` (REAL)

---

## Code path (what calls what)
### Entry point
- `backend/app/main.py`
  - Creates the FastAPI app
  - Includes the analyze router under `/api`

### Endpoint
- `backend/app/api/endpoints/analyze.py`
  - Receives the upload (`UploadFile`)
  - Calls saving + probing services
  - Returns response

### Services
- `backend/app/services/video_ingest.py`
  - `save_upload_to_disk(file)`:
    - validates content type
    - streams file to `backend/uploads/`
    - returns saved path

- `backend/app/services/video_probe.py`
  - `probe_video(path)`:
    - OpenCV reads fps/frame_count/width/height

- `backend/app/services/scoring.py`
  - `mock_score_spike()`:
    - returns placeholder score + tips (temporary)

### Schemas (API contract)
- `backend/app/models/schemas.py`
  - Defines the response shape returned to clients

---

## Current pipeline diagram
Upload video
  → save to disk (video_ingest)
    → probe video (video_probe)
      → mock scoring (scoring)
        → return JSON (schemas)

---

## Next planned steps
1) Frame extraction / sampling (read frames from saved video)
2) Pose estimation per frame (MediaPipe Pose)
3) Feature engineering (jump height, arm angle, approach speed)
4) Replace mock scoring with rule-based scoring based on features
5) Add React UI to upload + display results
