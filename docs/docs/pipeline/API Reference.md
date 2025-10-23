# API Reference

The project includes a real-time **FastAPI** server for on-demand predictions.

---

## 1. Running the API

To run the server locally, use:

```bash
uvicorn app:app --reload
```

✅ The API will be available at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 2. Interactive Documentation

FastAPI automatically generates interactive documentation.  
You can access it at:

📘 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 3. Endpoint: `POST /api/v1/segment`

This is the main endpoint for predicting a customer segment.

---

### Request Body

The endpoint expects a JSON payload with raw **RFM values**, defined in `customer_schema.py` as `CustomerData`:

```json
{
  "recency": int,
  "frequency": int,
  "monetary": float
}
```

#### Example Payload

```json
{
  "recency": 15,
  "frequency": 2,
  "monetary": 350.75
}
```

---

### Response Body

The API returns a JSON object with the predicted segment name and cluster label, defined in `customer_schema.py` as `SegmentResponse`:

```json
{
  "segment_name": str,
  "cluster_label": int
}
```

#### Example Response

```json
{
  "segment_name": "New Customers",
  "cluster_label": 2
}
```

---

## 4. Outlier Handling (Clipping)

The API is protected against **extreme outliers** to ensure robust predictions.

At startup, it loads the `rfm_features.csv` file to learn the **minimum and maximum values** from the training data.

When a new request comes in:

1. The raw `R`, `F`, and `M` values are **log-transformed**.  
2. The log-transformed values are **clipped** using `np.clip()` to stay within the learned min/max bounds.  
3. The clipped data is passed to the **scaler** and **model** for prediction.

This ensures that an extreme request such as:

```json
{
  "monetary": 200000000000
}
```

is treated as a **very high-value customer** and classified appropriately (e.g., as a “Champion”) rather than breaking the model.

