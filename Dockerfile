FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
ENV PYTHONUNBUFFERED=1
RUN python -m pip install --upgrade pip && python -m pip install --no-cache-dir -r requirements.txt
COPY . .
# install curl for HEALTHCHECK (cleanup apt lists to keep image small)
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
# create a non-root user and give ownership of the app directory
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD curl -f http://127.0.0.1:8080/ || exit 1
CMD ["python", "app.py"]
