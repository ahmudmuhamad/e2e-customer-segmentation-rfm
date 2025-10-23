import pandas as pd
import joblib
from pathlib import Path

# Define file paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROCESSED_DATA_PATH = BASE_DIR / "data" / "processed" / "rfm_features.csv"
MODELS_DIR = BASE_DIR / "models"
SCALER_PATH = MODELS_DIR / "scaler.pkl"
MODEL_PATH = MODELS_DIR / "kmeans_model.pkl"
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "customer_segments.csv"

# The segment map you defined
SEGMENT_NAME_MAP = {
    0: 'Champions',
    1: 'Lost Customers',
    2: 'New Customers',
    3: 'At-Risk' 
}

def predict_segments(data_path, scaler_path, model_path, output_path):
    """
    Loads features, scaler, and model, then predicts
    segments and saves the final dataframe.
    """
    print("Loading data and models for prediction...")
    try:
        rfm_df = pd.read_csv(data_path)
        scaler = joblib.load(scaler_path)
        model = joblib.load(model_path)
    except FileNotFoundError as e:
        print(f"Error: Missing file. {e}")
        print("Ensure src/features.py and src/modeling/train.py have been run.")
        return

    # --- 1. Apply Scaler ---
    print("Scaling features...")
    features_to_scale = ['recency_log', 'frequency_log', 'monetary_log']
    rfm_scaled = rfm_df[features_to_scale]
    
    # Use scaler.transform() - NOT fit_transform()
    rfm_scaled = scaler.transform(rfm_scaled)

    # --- 2. Predict Clusters ---
    print("Predicting segments...")
    clusters = model.predict(rfm_scaled)
    
    # Add clusters and segment names to the original dataframe
    rfm_df['cluster'] = clusters
    rfm_df['segment_name'] = rfm_df['cluster'].map(SEGMENT_NAME_MAP)
    
    # --- 3. Save Final Output ---
    # Select only the columns we care about for the final report
    final_df = rfm_df[[
        'CustomerID', 'recency', 'frequency', 'monetary', 'segment_name'
    ]]
    
    final_df.to_csv(output_path, index=False)
    print(f"Successfully saved segmented customer data to {output_path}")

def main():
    """Main function to run the script."""
    predict_segments(PROCESSED_DATA_PATH, SCALER_PATH, MODEL_PATH, OUTPUT_PATH)

if __name__ == "__main__":
    main()