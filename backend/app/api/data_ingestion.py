from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
import uuid

router = APIRouter()

UPLOAD_DIR = os.path.join(
    os.path.dirname(__file__), '../../../data/raw'
)
JOBS = []  # In-memory job store for demo

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post('/ingestion/upload')
def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=400, detail='Only CSV files are supported.'
        )
    file_id = str(uuid.uuid4())
    file_path = os.path.join(
        UPLOAD_DIR, f'{file_id}_{file.filename}'
    )
    with open(file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    # Add a job entry for demonstration
    job = {
        'id': file_id,
        'filename': file.filename,
        'status': 'uploaded',
        'path': file_path
    }
    JOBS.append(job)
    return {'job_id': file_id, 'filename': file.filename}


@router.post('/ingestion/trigger')
def trigger_ingestion(job_id: str):
    for job in JOBS:
        if job['id'] == job_id:
            job['status'] = 'processing'  # Simulate processing
            # Here you would trigger actual ingestion logic
            job['status'] = 'completed'   # Simulate completion
            return {'job_id': job_id, 'status': job['status']}
    raise HTTPException(status_code=404, detail='Job not found')


@router.get('/ingestion/jobs')
def list_jobs():
    return JOBS 