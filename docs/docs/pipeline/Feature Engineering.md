```markdown
# 1. Feature Engineering

The `src/features.py` script is responsible for loading the raw data and transforming it into a clean set of RFM features.

---

## Logic

### 1. Load Data
- Loads the `data/raw/online_retail.xlsx` file.

### 2. Clean Data
- Drops all rows where `CustomerID` is missing.  
- Removes duplicate transactions.  
- Converts `InvoiceDate` to a `datetime` object.

### 3. Engineer TotalPrice
- Creates the `TotalPrice` column as: TotalPrice = Quantity * UnitPrice


### 4. Filter Returns
- Filters out all transactions where `TotalPrice` is **zero or negative**.  
- This prevents `NaN` errors during the logarithmic transformation.

### 5. Calculate RFM Metrics
- **Recency:** Calculates the number of days since each customer’s last purchase.  
- **Frequency:** Counts the number of unique invoices per customer.  
- **Monetary:** Sums the total `TotalPrice` per customer.

### 6. Log Transformation
- Applies a `np.log1p()` transformation to the Recency, Frequency, and Monetary values to reduce skewness.

### 7. Save Output
- Saves the final DataFrame (including the log-transformed columns) to:
  data/processed/rfm_features.csv
  
