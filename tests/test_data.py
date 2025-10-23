import pandas as pd
import numpy as np

def get_mock_raw_data() -> pd.DataFrame:
    """
    Returns a small, in-memory DataFrame that mimics
    the structure of 'online_retail.xlsx' and includes
    all the edge cases we need to test.
    
    Snapshot date for this data (for manual RFM calc) is '2024-01-01'.
    """
    data = [
        # Customer 123: Good customer, 2 purchases, 1 return
        {'CustomerID': 123, 'InvoiceNo': 'A001', 'InvoiceDate': '2023-12-15 08:00:00', 'Quantity': 10, 'UnitPrice': 1.5, 'Country': 'UK'},
        {'CustomerID': 123, 'InvoiceNo': 'A002', 'InvoiceDate': '2023-10-01 12:00:00', 'Quantity': 5, 'UnitPrice': 2.0, 'Country': 'UK'},
        {'CustomerID': 123, 'InvoiceNo': 'C001', 'InvoiceDate': '2023-10-02 09:00:00', 'Quantity': -1, 'UnitPrice': 2.0, 'Country': 'UK'}, # Return
        
        # Customer 456: Lost customer, 1 old purchase
        {'CustomerID': 456, 'InvoiceNo': 'A003', 'InvoiceDate': '2022-01-01 14:00:00', 'Quantity': 2, 'UnitPrice': 5.0, 'Country': 'France'},
        
        # Customer 789: New customer, 1 recent purchase
        {'CustomerID': 789, 'InvoiceNo': 'A004', 'InvoiceDate': '2023-12-20 10:00:00', 'Quantity': 1, 'UnitPrice': 20.0, 'Country': 'Germany'},
        
        # --- Edge Cases for Cleaning ---
        # 1. Missing CustomerID
        {'CustomerID': np.nan, 'InvoiceNo': 'A005', 'InvoiceDate': '2023-01-01 00:00:00', 'Quantity': 1, 'UnitPrice': 1.0, 'Country': 'UK'},
        
        # 2. Duplicate Row
        {'CustomerID': 999, 'InvoiceNo': 'A006', 'InvoiceDate': '2023-01-01 00:00:00', 'Quantity': 1, 'UnitPrice': 1.0, 'Country': 'UK'},
        {'CustomerID': 999, 'InvoiceNo': 'A006', 'InvoiceDate': '2023-01-01 00:00:00', 'Quantity': 1, 'UnitPrice': 1.0, 'Country': 'UK'},
    ]
    
    df = pd.DataFrame(data)
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    # Add other columns if your script uses them
    df['StockCode'] = 'TEST'
    df['Description'] = 'TEST'
    
    return df

def get_mock_rfm_features() -> pd.DataFrame:
    """
    Returns a mock DataFrame that mimics 'rfm_features.csv'.
    This is what we expect after processing 'get_mock_raw_data()'.
    
    Snapshot date: '2024-01-01'
    - C_123: Recency=17 (2024-01-01 - 2023-12-15), Freq=2 (A001, A002), Monetary= (10*1.5) + (5*2.0) = 25.0
    - C_456: Recency=730 (2024-01-01 - 2022-01-01), Freq=1 (A003), Monetary= (2*5.0) = 10.0
    - C_789: Recency=12 (2024-01-01 - 2023-12-20), Freq=1 (A004), Monetary= (1*20.0) = 20.0
    - C_999: Recency=365 (2024-01-01 - 2023-01-01), Freq=1 (A006), Monetary= (1*1.0) = 1.0
    """
    data = {
        'CustomerID': [123, 456, 789, 999],
        'recency': [17, 730, 12, 365],
        'frequency': [2, 1, 1, 1],
        'monetary': [25.0, 10.0, 20.0, 1.0]
    }
    rfm = pd.DataFrame(data)
    
    # Add the log columns that the training script expects
    rfm['recency_log'] = np.log1p(rfm['recency'])
    rfm['frequency_log'] = np.log1p(rfm['frequency'])
    rfm['monetary_log'] = np.log1p(rfm['monetary'])
    
    return rfm

# --- API Test Payloads ---

VALID_API_PAYLOAD = {
    "recency": 15,
    "frequency": 2,
    "monetary": 350.75
}

INVALID_API_PAYLOAD_BAD_TYPE = {
    "recency": "fifteen",  # Should be int
    "frequency": 2,
    "monetary": 350.75
}

INVALID_API_PAYLOAD_MISSING_FIELD = {
    "recency": 15,
    "monetary": 350.75
    # 'frequency' is missing
}
