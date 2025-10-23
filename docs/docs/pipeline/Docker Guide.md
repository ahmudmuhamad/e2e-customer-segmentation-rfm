# Docker Guide

This project is configured to be built and run as a lightweight **Docker** container.

---

## 1. Production vs. Development

To create a small and secure image, the project uses two separate requirements files:

- **`requirements.txt`** → Used for development.  
  Contains all libraries (including Jupyter, Matplotlib, etc.).
- **`api_requirements.txt`** → Used only for the Docker image.  
  Contains the **bare minimum** packages required to run the FastAPI application.

---

## 2. `.dockerignore`

A `.dockerignore` file is included to prevent unnecessary files from being copied into the Docker image.  
It typically excludes the following:

- `.venv/` directory  
- `notebooks/` and `reports/` folders  
- Raw data files  
- `.git/` and `.vscode/` directories  

This helps keep the Docker image lightweight and clean.

---

## 3. Build the Image

To build the Docker image, navigate to the project’s root directory and run:

```bash
docker build -t rfm-api .
```

**Explanation:**
- `-t rfm-api` → Tags the image with the name **rfm-api**.  
- `.` → Tells Docker to use the **Dockerfile** in the current directory.

---

## 4. Run the Container

Once built, run the image as a container:

```bash
docker run -p 8000:8000 --name rfm-service rfm-api
```

**Explanation:**
- `-p 8000:8000` → Maps port **8000** on your local machine to port **8000** inside the container.  
- `--name rfm-service` → Assigns the container a descriptive name (**rfm-service**).

✅ Your API will now be accessible at:  
[http://127.0.0.1:8000](http://127.0.0.1:8000)

---
```
