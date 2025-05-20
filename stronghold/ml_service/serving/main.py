import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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


MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    '../models/logreg_model.joblib'
)
_model = None


def get_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise HTTPException(status_code=500, detail="Model file not found.")
        _model = joblib.load(MODEL_PATH)
    return _model


@app.get("/health")
def health_check():
    return {"status": "ok"}


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