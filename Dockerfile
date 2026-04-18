FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=7860 \
    API_PORT=5000

WORKDIR /app

COPY requirement.txt /app/requirement.txt
RUN pip install --upgrade pip && pip install -r /app/requirement.txt

COPY . /app

EXPOSE 7860

# Run API on 5000 (internal) and frontend on 7860 (public for Hugging Face)
CMD ["bash", "-lc", "gunicorn --workers 1 --threads 4 --timeout 120 --bind 0.0.0.0:${API_PORT} api.app:app & exec gunicorn --workers 1 --threads 8 --timeout 120 --bind 0.0.0.0:${PORT} frontend.app:app"]
