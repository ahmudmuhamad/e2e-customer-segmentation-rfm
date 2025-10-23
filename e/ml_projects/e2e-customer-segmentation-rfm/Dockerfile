FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install uv (fast Python package manager)
RUN pip install uv

COPY api_requirements.txt .
RUN uv pip install --system -r api_requirements.txt

COPY app.py .
COPY src/ ./src/
COPY models/ ./models/
# If you have a data/processed directory, copy it as well:
# COPY data/processed/ ./data/processed/

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]