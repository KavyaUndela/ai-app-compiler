FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

WORKDIR /app

# Install runtime Python dependencies only. Avoid installing build tools in the image
# so builds are smaller and compatible with Railway. If you need to build packages
# with C extensions, add appropriate system packages (gcc) back.
COPY requirements.txt ./

RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt \
    && python -m pip cache purge || true

# Copy application code (expecting repository structure: backend/*)
COPY . .

EXPOSE 8000

# Use PORT env provided by Railway; default to 8000 when not set.
CMD ["sh", "-c", "gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 120"]
