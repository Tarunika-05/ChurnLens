"""Prediction endpoints."""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from api.schemas import PredictionRequest, PredictionResponse
from api.dependencies import get_model
import pandas as pd
from src.features import add_engineered_features, get_model_features
import io

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
async def predict_single(
    request: PredictionRequest, 
    model = Depends(get_model),
    explain: bool = False
) -> PredictionResponse:
    from api.dependencies import get_explainer
    from src.explainability import explain_prediction
    try:
        # Convert request to DataFrame
        input_data = pd.DataFrame([request.model_dump()])
        
        # Add engineered features
        enriched_data = add_engineered_features(input_data)
        features = get_model_features()
        
        # Ensure all required features are present
        missing = [f for f in features if f not in enriched_data.columns]
        if missing:
            raise HTTPException(status_code=422, detail=f"Missing required features after engineering: {missing}")
            
        # Predict
        prob = model.predict_proba(enriched_data[features])[0, 1]
        
        risk_tier = "High" if prob >= 0.7 else "Medium" if prob >= 0.4 else "Low"
        predicted_churn = 1 if prob >= 0.5 else 0
        
        top_drivers = []
        if explain:
            explainer, preprocessor = get_explainer()
            if explainer is not None:
                drivers_dict = explain_prediction(explainer, preprocessor, enriched_data[features], features)
                # Just return the top 3 drivers formatted nicely
                for i, (feat, val) in enumerate(drivers_dict.items()):
                    if i >= 3: break
                    direction = "Increased" if val > 0 else "Decreased"
                    top_drivers.append(f"{feat} ({direction} risk by {abs(val)*100:.1f}%)")
        
        return PredictionResponse(
            customer_id=request.customerID,
            churn_probability=float(prob),
            risk_tier=risk_tier,
            predicted_churn=predicted_churn,
            top_drivers=top_drivers if top_drivers else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict/batch", response_model=list[PredictionResponse])
async def predict_batch(file: UploadFile = File(...), model = Depends(get_model)) -> list[PredictionResponse]:
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
        
    try:
        content = await file.read()
        df = pd.read_csv(io.StringIO(content.decode('utf-8')))
        
        if "customerID" not in df.columns:
            # Add a dummy customerID if missing
            df["customerID"] = [f"BATCH_{i}" for i in range(len(df))]
            
        enriched_data = add_engineered_features(df)
        features = get_model_features()
        
        probs = model.predict_proba(enriched_data[features])[:, 1]
        
        results = []
        for i, prob in enumerate(probs):
            risk_tier = "High" if prob >= 0.7 else "Medium" if prob >= 0.4 else "Low"
            results.append(PredictionResponse(
                customer_id=str(df.iloc[i]["customerID"]),
                churn_probability=float(prob),
                risk_tier=risk_tier,
                predicted_churn=1 if prob >= 0.5 else 0,
                top_drivers=[]
            ))
            
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing batch: {str(e)}")
