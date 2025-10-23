import joblib
import numpy as np
import uvicorn
from fastapi import FastAPI, APIRouter
from pathlib import Path

# --- NEW: Import schemas from your file ---
from src.schemas.customers_schema import CustomerData, SegmentResponse

# --- 1. Initialize the FastAPI App ---
app = FastAPI(
    title="RFM Customer Segmentation API",
    description="An API to segment customers in real-time based on RFM values.",
    version="1.0.0"
)

# --- 2. Define File Paths and Load Models ---

# Build paths relative to this file
BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"
SCALER_PATH = MODELS_DIR / "scaler.pkl"
MODEL_PATH = MODELS_DIR / "kmeans_model.pkl"

# Load the scaler and model at startup
try:
    SCALER = joblib.load(SCALER_PATH)
    MODEL = joblib.load(MODEL_PATH)
    print("Models and scaler loaded successfully.")
except FileNotFoundError:
    print("Error: Model or scaler file not found. Run 'make all' first.")
    SCALER, MODEL = None, None

# Define the segment map from your project
SEGMENT_NAME_MAP = {
    0: 'Champions',
    1: 'Lost Customers',
    2: 'New Customers',
    3: 'At-Risk' 
}

# --- 3. Define the API Endpoints ---

# --- NEW: Create a v1 Router ---
# All v1 endpoints will be added to this router
v1_router = APIRouter(
    prefix="/api/v1",  # This adds /api/v1 to all routes in this router
    tags=["v1 - Customer Segmentation"]  # This groups them nicely in the docs
)

@app.get("/")
def read_root():
    """
    Root endpoint to check if the API is running.
    """
    return {"message": "Welcome to the RFM Segmentation API. Go to /docs for API v1."}


@v1_router.get("/")
def read_v1_root():
    """
    Root endpoint for the v1 API.
    """
    return {"message": "API v1 is running"}


# --- NEW: Endpoint uses the router, input schema, and response schema ---
@v1_router.post("/segment", response_model=SegmentResponse)
def segment_customer(data: CustomerData):
    """
    Predicts the customer segment from raw RFM values.
    
    - **recency**: Days since last purchase
    - **frequency**: Total number of purchases
    - **monetary**: Total monetary value of purchases
    """
    if MODEL is None or SCALER is None:
        return {"error": "Models not loaded. Check server logs."}

    # 1. Get data from the request
    recency = data.recency
    frequency = data.frequency
    monetary = data.monetary

    # 2. Apply log transformations (same as in features.py)
    recency_log = np.log1p(recency)
    frequency_log = np.log1p(frequency)
    monetary_log = np.log1p(monetary)

    # 3. Put features into a 2D array for the scaler
    features_log = np.array([[recency_log, frequency_log, monetary_log]])

    # 4. Scale the features
    features_scaled = SCALER.transform(features_log)

    # 5. Predict the cluster
    cluster_label = MODEL.predict(features_scaled)[0]

    # 6. Map cluster label to segment name
    segment_name = SEGMENT_NAME_MAP.get(int(cluster_label), "Unknown Segment")

    # 7. Return the response (FastAPI will validate it against SegmentResponse)
    return SegmentResponse(
        segment_name=segment_name,
        cluster_label=int(cluster_label)
    )

# --- NEW: Include the router in the main app ---
app.include_router(v1_router)


# --- 5. Run the API (if this file is run directly) ---
if __name__ == "__main__":
    # This block allows you to run the app with 'python app.py'
    # --reload is great for development
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

