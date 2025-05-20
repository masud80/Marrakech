import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess

app = FastAPI(title="Ash Investments ML Service")


class InferenceRequest(BaseModel):
    asset_id: int
    name: str
    owner: str
    lease_status: str
    production_rate: float
    location: str


class InferenceResponse(BaseModel):
    prediction: int


MODEL_ID = "logreg_model"
MODEL_PATH = os.path.join(
    os.path.dirname(__file__), '../models/logreg_model.joblib'
)
METRICS_PATH = os.path.join(
    os.path.dirname(__file__), '../models/logreg_model_metrics.txt'
)
_model = None


def get_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise HTTPException(
                status_code=500, detail="Model file not found."
            )
        _model = joblib.load(MODEL_PATH)
    return _model


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/models")
def list_models():
    # For now, only one model
    return [{
        "id": MODEL_ID,
        "name": "Logistic Regression Model",
        "path": MODEL_PATH,
        "metrics_path": METRICS_PATH
    }]


@app.get("/models/{model_id}/metrics")
def get_model_metrics(model_id: str):
    if model_id != MODEL_ID:
        raise HTTPException(status_code=404, detail="Model not found")
    # Try to read metrics from file, else return placeholder
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, 'r') as f:
            metrics = f.read()
        return {"model_id": model_id, "metrics": metrics}
    else:
        return {"model_id": model_id, "metrics": "Accuracy: N/A"}


@app.post("/models/{model_id}/retrain")
def retrain_model(model_id: str):
    if model_id != MODEL_ID:
        raise HTTPException(status_code=404, detail="Model not found")
    # Run the sample pipeline to retrain
    pipeline_path = os.path.join(
        os.path.dirname(__file__), '../pipelines/sample_pipeline.py'
    )
    try:
        result = subprocess.run(
            ['python', pipeline_path],
            capture_output=True, text=True, check=True
        )
        # Parse accuracy from output and save to metrics file
        for line in result.stdout.splitlines():
            if line.startswith('Test Accuracy:'):
                with open(METRICS_PATH, 'w') as f:
                    f.write(line)
        return {
            "model_id": model_id,
            "status": "retrained",
            "output": result.stdout
        }
    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Retraining failed: {e.stderr}"
        )


@app.post("/inference", response_model=InferenceResponse)
def run_inference(request: InferenceRequest):
    model = get_model()
    # Prepare input as DataFrame
    input_df = pd.DataFrame([
        request.dict()
    ])
    # Drop asset_id if not used in training
    if 'asset_id' in input_df.columns:
        input_df = input_df.drop(columns=['asset_id'])
    # Convert categorical columns if needed (assume model trained on dummies)
    # For demo, try to match training columns
    try:
        prediction = model.predict(input_df)[0]
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Prediction failed: {e}"
        )
    return InferenceResponse(prediction=int(prediction)) 