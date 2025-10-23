# Model Training

The `src/modeling/train.py` script is responsible for training the segmentation model.

## Logic

### 1. Load Features
- Loads the `data/processed/rfm_features.csv` file.

### 2. Select Features
- Selects only the **log-transformed columns**:  
  `recency_log`, `frequency_log`, and `monetary_log`.  
- These features are already normalized and ready for scaling.

### 3. Fit Scaler
- Initializes a `StandardScaler`.  
- Fits the scaler to the log-transformed RFM data.  
- Saves the fitted scaler to:
  models/scaler.pkl

### 4. Train K-Means
- Initializes a `KMeans` model with:
  n_clusters = 4
  random_state = 42
- Fits the K-Means model to the scaled data.  
- Saves the trained model to:
  models/kmeans_model.pkl

