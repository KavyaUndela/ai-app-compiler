# Deployment Guide

Complete guide for deploying AI Application Compiler to production.

## Table of Contents

- [Docker Deployment](#docker-deployment)
- [AWS Deployment](#aws-deployment)
- [Vercel (Frontend) + Heroku (Backend)](#vercel--heroku)
- [Google Cloud](#google-cloud)
- [DigitalOcean](#digitalocean)
- [Local Production](#local-production-setup)

---

## Docker Deployment

### Build Images

```bash
# Build backend
docker build -t ai-compiler-backend:latest ./backend

# Build frontend
docker build -t ai-compiler-frontend:latest ./frontend

# Tag for registry
docker tag ai-compiler-backend:latest myregistry/ai-compiler-backend:latest
docker tag ai-compiler-frontend:latest myregistry/ai-compiler-frontend:latest
```

### Production Docker Compose

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  backend:
    image: myregistry/ai-compiler-backend:latest
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
      - LOG_LEVEL=warning
      - DATABASE_URL=postgresql://user:pass@postgres:5432/compiler
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis
    restart: always
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '0.5'
          memory: 512M

  frontend:
    image: myregistry/ai-compiler-frontend:latest
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=https://api.compiler.com
    depends_on:
      - backend
    restart: always
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '0.25'
          memory: 256M

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=compiler
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=compiler_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

  redis:
    image: redis:7-alpine
    restart: always
    volumes:
      - redis_data:/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - backend
      - frontend
    restart: always

volumes:
  postgres_data:
  redis_data:
```

### Run Production Stack

```bash
docker compose -f docker-compose.prod.yml up -d

# Check status
docker compose -f docker-compose.prod.yml ps

# View logs
docker compose -f docker-compose.prod.yml logs -f backend
```

---

## AWS Deployment

### Option 1: ECS (Elastic Container Service)

```bash
# Configure AWS CLI
aws configure

# Create ECR repositories
aws ecr create-repository --repository-name ai-compiler-backend
aws ecr create-repository --repository-name ai-compiler-frontend

# Get login token
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

# Tag and push images
docker tag ai-compiler-backend:latest \
  123456789.dkr.ecr.us-east-1.amazonaws.com/ai-compiler-backend:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/ai-compiler-backend:latest

# Similar for frontend...
```

### Option 2: Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p docker ai-compiler

# Create environment
eb create prod-environment

# Deploy
eb deploy

# View logs
eb logs
```

### Option 3: EKS (Kubernetes)

```bash
# Create cluster
eksctl create cluster --name ai-compiler --region us-east-1

# Create namespace
kubectl create namespace ai-compiler

# Apply manifests
kubectl apply -f k8s/backend.yaml
kubectl apply -f k8s/frontend.yaml

# Check deployment
kubectl get pods -n ai-compiler
```

**Sample k8s/backend.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: ai-compiler
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: 123456789.dkr.ecr.us-east-1.amazonaws.com/ai-compiler-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        resources:
          limits:
            cpu: "500m"
            memory: "512Mi"
---
apiVersion: v1
kind: Service
metadata:
  name: backend-service
  namespace: ai-compiler
spec:
  selector:
    app: backend
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

---

## Vercel + Heroku

### Deploy Frontend to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
cd frontend
vercel

# Set environment variables
vercel env add NEXT_PUBLIC_API_URL https://your-backend.herokuapp.com/api
```

### Deploy Backend to Heroku

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create ai-compiler-backend

# Set environment variables
heroku config:set DATABASE_URL=postgresql://...
heroku config:set LOG_LEVEL=warning

# Create Procfile in backend/:
# Procfile
echo "web: uvicorn app.main:app --host 0.0.0.0 --port $PORT" > backend/Procfile

# Deploy
cd backend
git push heroku main

# View logs
heroku logs --tail
```

### Configure Vercel Backend URL

```bash
cd frontend
vercel env add NEXT_PUBLIC_API_URL https://ai-compiler-backend.herokuapp.com/api
vercel deploy --prod
```

---

## Google Cloud

### Deploy with Cloud Run

```bash
# Authenticate
gcloud auth login
gcloud config set project PROJECT_ID

# Build and push backend
gcloud builds submit ./backend \
  --tag gcr.io/PROJECT_ID/ai-compiler-backend

# Deploy backend
gcloud run deploy ai-compiler-backend \
  --image gcr.io/PROJECT_ID/ai-compiler-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# Deploy frontend similarly
gcloud builds submit ./frontend \
  --tag gcr.io/PROJECT_ID/ai-compiler-frontend

gcloud run deploy ai-compiler-frontend \
  --image gcr.io/PROJECT_ID/ai-compiler-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Cloud Firestore (Database)

```python
# backend/app/services/firestore_service.py

from google.cloud import firestore

db = firestore.Client()

def store_compilation(compilation_id: str, data: dict):
    db.collection('compilations').document(compilation_id).set(data)

def get_compilation(compilation_id: str):
    return db.collection('compilations').document(compilation_id).get().to_dict()
```

---

## DigitalOcean

### Deploy with App Platform

```bash
# Create app.yaml in project root:
cat > app.yaml << EOF
name: ai-compiler
services:
- name: backend
  github:
    repo: your-org/ai-compiler
    branch: main
  build_command: pip install -r requirements.txt
  run_command: uvicorn app.main:app --host 0.0.0.0 --port 8080
  source_dir: backend/
  http_port: 8080
  
- name: frontend
  github:
    repo: your-org/ai-compiler
    branch: main
  build_command: npm install && npm run build
  run_command: npm start
  source_dir: frontend/
  http_port: 3000

databases:
- name: postgres
  engine: PG
  version: "15"
EOF

# Deploy using doctl
doctl apps create --spec app.yaml
```

---

## Local Production Setup

For running on your own server:

### Prerequisites

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y docker.io docker-compose postgresql redis-server nginx

# Start services
sudo systemctl start docker
sudo systemctl start postgresql
sudo systemctl start redis-server
sudo systemctl start nginx
```

### Setup SSL

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Create certificate
sudo certbot certonly --standalone -d yourdomain.com

# Configure nginx
sudo nano /etc/nginx/sites-available/default
```

### Nginx Configuration

```nginx
upstream backend {
    server localhost:8000;
}

upstream frontend {
    server localhost:3000;
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API
    location /api {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Reload Nginx

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

## Environment Configuration

### Backend (.env)

```
# Production
ENVIRONMENT=production
LOG_LEVEL=warning
DEBUG=false

# Database
DATABASE_URL=postgresql://user:pass@host:5432/compiler_db
REDIS_URL=redis://host:6379/0

# API
API_TITLE=AI Application Compiler
API_VERSION=1.0.0

# Security
SECRET_KEY=your-secret-key-here
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Optional
SENTRY_DSN=https://...@sentry.io/...
```

### Frontend (.env.production)

```
NEXT_PUBLIC_API_URL=https://yourdomain.com/api
NEXT_PUBLIC_ANALYTICS=true
```

---

## Monitoring & Logging

### Backend Logging

```python
# backend/app/main.py

import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)
```

### Error Tracking (Sentry)

```bash
# Install Sentry
pip install sentry-sdk

# Configure in backend
import sentry_sdk

sentry_sdk.init(
    dsn="https://your-sentry-dsn@sentry.io/...",
    traces_sample_rate=0.1
)
```

### Monitoring Tools

- **Datadog:** Docker integration
- **New Relic:** APM monitoring
- **Prometheus:** Metrics collection
- **CloudWatch:** AWS native monitoring

---

## Scaling Recommendations

### Horizontal Scaling

- Backend: Scale replicas (3-5 initially)
- Frontend: Scale replicas (2-3 initially)
- Database: Use managed service (RDS, Cloud SQL)

### Caching

```python
# Add Redis caching
from redis import Redis

redis_client = Redis(host='localhost', port=6379)

def get_compilation(compilation_id: str):
    # Check cache
    cached = redis_client.get(f"compilation:{compilation_id}")
    if cached:
        return json.loads(cached)
    
    # Fetch and cache
    result = db.get_compilation(compilation_id)
    redis_client.setex(f"compilation:{compilation_id}", 3600, json.dumps(result))
    return result
```

---

## Post-Deployment Checklist

- [ ] HTTPS enabled
- [ ] Environment variables configured
- [ ] Database backed up
- [ ] Error logging configured
- [ ] Monitoring set up
- [ ] Rate limiting enabled
- [ ] CORS configured properly
- [ ] Database indexes created
- [ ] Health checks passing
- [ ] Performance benchmarks met

---

## Rollback Procedure

```bash
# Docker
docker compose -f docker-compose.prod.yml down
docker pull myregistry/ai-compiler-backend:previous
docker compose -f docker-compose.prod.yml up -d

# Kubernetes
kubectl rollout undo deployment/backend -n ai-compiler
kubectl rollout history deployment/backend -n ai-compiler

# Heroku
heroku releases
heroku rollback v123
```

---

## Support

For deployment issues:
1. Check application logs
2. Review deployment documentation
3. Verify environment variables
4. Test health endpoint

---

**Last Updated:** 2024
**Version:** 1.0.0
