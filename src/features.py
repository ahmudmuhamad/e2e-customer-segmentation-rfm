import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add src to the Python path
sys.path.append(str(Path(__file__).resolve().parent))

# Define file paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "online_retail.xlsx"
PROCESSED_DATA_PATH = BASE_DIR / "data" / "processed" / "rfm_features.csv"

def create_rfm_features(data_path, save_path):
    """
    Loads raw data, performs cleaning and feature engineering
    to create RFM features, and saves them to a file.
    """
    print(f"Loading raw data from {data_path}...")
    try:
        df = pd.read_excel(data_path) 
    except FileNotFoundError:
        print(f"Error: Raw data file not found at {data_path}")
        return
    except ImportError:
        print("Error: 'openpyxl' library not found.")
        print("Please install it by running: pip install openpyxl")
        return

    # --- 1. Data Cleaning ---
    print("Cleaning data...")
    df = df.dropna(subset=['CustomerID'])
    df = df.drop_duplicates()
    
    # Convert InvoiceDate to datetime
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    # --- 2. Feature Engineering ---
    print("Engineering RFM features...")
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    
    # --- *** NEW LINE: FIX FOR NAN *** ---
    # Only keep transactions with positive TotalPrice for RFM calculation
    # This removes returns/cancellations from the monetary sum.
    df = df[df['TotalPrice'] > 0]
    # --- *** END OF FIX *** ---

    # Set a snapshot date (one day after the last transaction)
    snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
    
    # Group by customer
    rfm = df.groupby('CustomerID').agg(
        recency=('InvoiceDate', lambda x: (snapshot_date - x.max()).days),
        frequency=('InvoiceNo', 'nunique'),
        monetary=('TotalPrice', 'sum')
    )
    
    # --- 3. Log Transformations ---
    print("Applying log transformations...")
    # Now, 'monetary' should not be negative, so log1p will work.
    rfm['recency_log'] = np.log1p(rfm['recency'])
    rfm['frequency_log'] = np.log1p(rfm['frequency'])
    rfm['monetary_log'] = np.log1p(rfm['monetary'])
    
    # Reset index to get CustomerID as a column
    rfm = rfm.reset_index().astype(int)

    # --- 4. Save Processed Data ---
    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    rfm.to_csv(save_path, index=False)
    print(f"Successfully created RFM features at {save_path}")

def main():
    """Main function to run the script."""
    create_rfm_features(RAW_DATA_PATH, PROCESSED_DATA_PATH)

if __name__ == "__main__":
    main()