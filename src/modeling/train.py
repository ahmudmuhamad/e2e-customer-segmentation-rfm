import pandas as pd
import joblib
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Define file paths
# Go up two levels from src/modeling to the project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROCESSED_DATA_PATH = BASE_DIR / "data" / "processed" / "rfm_features.csv"
MODELS_DIR = BASE_DIR / "models"
SCALER_PATH = MODELS_DIR / "scaler.pkl"
MODEL_PATH = MODELS_DIR / "kmeans_model.pkl"

# Ensure the models directory exists
MODELS_DIR.mkdir(parents=True, exist_ok=True)

def train_model(data_path, scaler_path, model_path):
    """
    Loads processed features, scales them, trains KMeans,
    and saves the scaler and model.
    """
    print(f"Loading processed data from {data_path}...")
    try:
        rfm_df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"Error: Processed data file not found at {data_path}")
        print("Run src/features.py first.")
        return

    # Select features for clustering (the log-transformed ones)
    features_to_scale = ['recency_log', 'frequency_log', 'monetary_log']
    rfm_scaled = rfm_df[features_to_scale]

    # --- 1. Fit and Save Scaler ---
    print("Fitting and saving scaler...")
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm_scaled)
    
    # Save the fitted scaler
    joblib.dump(scaler, scaler_path)
    print(f"Scaler saved to {scaler_path}")

    # --- 2. Train and Save Model ---
    print("Training KMeans model (k=4)...")
    # Using the parameters from your notebook (assumed k=4)
    kmeans = KMeans(n_clusters=4, init='k-means++', random_state=42)
    kmeans.fit(rfm_scaled)
    
    # Save the trained model
    joblib.dump(kmeans, model_path)
    print(f"KMeans model saved to {model_path}")
    print("--- Training complete ---")

def main():
    """Main function to run the script."""
    train_model(PROCESSED_DATA_PATH, SCALER_PATH, MODEL_PATH)

if __name__ == "__main__":
    main()