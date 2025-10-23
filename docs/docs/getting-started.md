# Getting Started

This guide covers how to set up the project locally for development and how to run the full pipeline.

---

## 1. Prerequisites

Before you begin, ensure you have the following tools installed:

- Python 3.12+
- `uv` (or `pip`)
- Git
- `make`  
  *(On Windows, install via: `winget install Gnu.Make`)*
- Docker Desktop *(Optional, for containerizing)*

---

## 2. Clone the Repository

Clone the project to your local machine:

```bash
git clone https://github.com/ahmudmuhamad/e2e-customer-segmentation-rfm.git
cd e2e-customer-segmentation-rfm
```

---

## 3. Set Up the Environment

This project uses **uv** for package and environment management.

### 3.1 Create the virtual environment

```bash
make create_environment
```

### 3.2 Activate the environment

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

---

## 4. Install Dependencies

Install all development dependencies (including Jupyter, matplotlib, etc.) using the `requirements.txt` file:

```bash
make requirements
```

This is equivalent to running:

```bash
uv pip install -r requirements.txt
```

---

## 5. Run the End-to-End Pipeline

The `Makefile` automates the entire data processing and model training pipeline.

Run the following command to execute all steps in the correct order:

```bash
make all
```

This command will:

- Run `src/features.py` → creates `data/processed/rfm_features.csv`
- Run `src/modeling/train.py` → creates `models/scaler.pkl` and `models/kmeans_model.pkl`
- Run `src/modeling/predict.py` → creates `data/processed/customer_segments.csv`

💡 To start fresh, run:

```bash
make clean
```

*(Deletes all generated files.)*

---

## 6. Run the API Server

After the pipeline has been run (which creates the models), you can start the FastAPI server:

```bash
uvicorn app:app --reload
```

✅ The server will be running at: [http://127.0.0.1:8000](http://127.0.0.1:8000)  
📘 Access the interactive API documentation at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)



