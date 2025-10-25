# **e2e-RFM-based Customer Segmentation**

An end-to-end machine learning system to cluster e-commerce customers using RFM analysis and deploy the model as a real-time, containerized FastAPI application.

## **1\. Introduction**

This project moves beyond a simple analysis notebook to a production-ready, MLOps-focused system. It takes raw e-commerce transaction data, engineers RFM (Recency, Frequency, Monetary) features, trains a K-Means clustering model, and deploys this model as a high-performance API.

The entire workflow is automated with a Makefile, the API is containerized with Docker, and the project is fully documented with MkDocs.

## **2\. The Four Customer Segments**

The model groups customers into four distinct segments, allowing for targeted and effective marketing strategies:

* **Champions:** Your best and most loyal customers. They buy recently, frequently, and spend the most.  
  * **Strategy:** Reward them with loyalty programs, early access, and personalized engagement. Avoid discounts.  
* **At-Risk:** High-value customers who *used* to buy frequently but haven't purchased in a while.  
  * **Strategy:** High-priority. Win them back with personalized re-engagement emails and special discounts.  
* **New Customers:** First-time or recent buyers with low frequency.  
  * **Strategy:** Nurture them. Send a welcome series and offer incentives for a second purchase to build frequency.  
* **Lost Customers:** Customers with high recency (long time since last purchase) and low frequency/monetary value.  
  * **Strategy:** Low-priority. Include in a low-cost win-back newsletter, but do not spend significant marketing budget.

## **3\. Technologies Used**

| Category | Technology | Purpose |
| :---- | :---- | :---- |
| **Data Science** | Pandas, NumPy | Data manipulation and feature engineering. |
| **ML** | Scikit-learn | K-Means clustering and data scaling. |
| **API** | FastAPI | Building the high-performance, real-time API. |
| **Data Validation** | Pydantic | Validating API input/output schemas. |
| **Web Server** | Uvicorn | Running the FastAPI application. |
| **Containerization** | Docker | Creating a portable, isolated production environment. |
| **Automation** | Makefile | Automating the entire ML pipeline (make all). |
| **Documentation** | MkDocs | Generating a static documentation website. |
| **Testing** | Pytest | Running automated tests on the source code. |
| **Linting** | Ruff | Code formatting and linting. |

## **4\. Project Architecture**

```
├── LICENSE            <- MIT licence 
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         src and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── src   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes src a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```
--------

## **5\. Getting Started**

### **Prerequisites**

* Python (3.12+)  
* uv (or pip)  
* make (On Windows, install with winget install Gnu.Make)  
* Docker Desktop (Optional, for running the container)

### **Setup & Installation**

1. **Clone the repository:**
    ```
   git clone https://github.com/ahmudmuhamad/e2e-customer-segmentation-rfm.git
   cd e2e-customer-segmentation-rfm
   ```


2. **Create and activate the environment:**
   ``` 
   \# Create the .venv  
   make create\_environment

   \# Activate (Windows)  
   .venv\\Scripts\\activate

   \# Activate (macOS / Linux)  
   source .venv/bin/activate
   ```

3. **Install dependencies:**  
    ```
   make requirements
    ```

## **6\. How to Use**

You can run this project as an automated pipeline, a live API server, or a Docker container.

### **Option 1: Run the Automated Pipeline**

This is the simplest way to run the project. It will process all data and train the models from scratch.

\# This command runs data, train, and predict steps in order:
      ```
     make all
      ```

This will:

1. **data:** Run src/features.py to create data/processed/rfm\_features.csv.  
2. **train:** Run src/modeling/train.py to create models/scaler.pkl and models/kmeans\_model.pkl.  
3. **predict:** Run src/modeling/predict.py to create the final data/processed/customer\_segments.csv.

To clean up all generated files, run make clean.

### **Option 2: Run the Real-Time API**

After running make all (which creates the model files), you can start the API server.

1. **Start the server:**
   ```
   uvicorn app:app \--reload
   ```

3. Access the Docs:  
   Open your browser to
    ```
   http://127.0.0.1:8000/docs.
    ``` 
5. Send a Request:  
   Use the interactive docs or curl to send a POST request:  
    ```
     curl -X POST "http://127.0.0.1:8000/api/v1/segment" \
   -H "Content-Type: application/json" \
   -d '{
         "recency": 15,
         "frequency": 2,
         "monetary": 350.75
       }'
    ```
    ```
   **Response:**  
   {  
     "segment\_name": "New Customers",  
     "cluster\_label": 2  
   }
    ```
### **Option 3: Run with Docker**

This is the recommended way to run the API in a production-like environment.

1. **Build the image:**
   ```
   docker build \-t rfm-api .
   ```

3. **Run the container:**
   ```
   docker run \-p 8000:8000 \--name rfm-service rfm-api
   ```

   The API is now running and accessible at
    ```
   http://127.0.0.1:8000/docs.
    ```

## **6\. Project Documentation**

This project includes a full documentation website. To view it locally:

1. **Install MkDocs:**
   ```
   uv pip install mkdocs mkdocs-readthedocs-theme
   ```

2. **Serve the docs:**  
    ```
   mkdocs serve
    ```

3. View in browser:  
   Open http://127.0.0.1:8001 to see the full site.



## 7. Deployment Architecture (AWS)

This project is not just a local script; it is a fully **deployment-ready** application. The system has been successfully containerized with Docker and deployed on **Amazon Web Services (AWS)**.

The architecture is designed to be scalable, secure, and automated, using a modern CI/CD approach.

### Key Deployment Features:
* **Containerized:** The `Dockerfile` creates a minimal, secure, and fast-starting image for the FastAPI application.
* **Container Registry:** The image is designed to be pushed to **Amazon ECR (Elastic Container Registry)**, providing a secure, private registry for the production image.

* **CI/CD Ready:** The project structure is built to plug directly into an **AWS CodePipeline** workflow. A push to the `main` branch can be configured to automatically test, build, and deploy the new version of the API.

### Note on Free Tier & Availability

This deployment was successfully tested and validated using the AWS Free Tier.

To demonstrate a cost-conscious *and* production-ready architecture, the public endpoint is not kept active 24/7. The infrastructure is fully defined and can be **spun up on demand** to serve the API, proving the deployment pipeline is functional without incurring unnecessary costs.
