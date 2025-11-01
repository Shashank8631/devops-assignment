# DevOps Assignment — Flask + SQLite (Simple demo)

## What is included
- Flask REST API (`app.py`) using **SQLite** (file `items.db`)
- Dockerfile and `.dockerignore`
- `docker-compose.yml` for local run
- GitHub Actions workflow to build & push Docker image on `main` (uses Docker Hub)
- Kubernetes manifests (namespace, Deployment with 2 replicas, Service NodePort)
- `INTERVIEW.md` — short script and explanations to help you present this in interview
- `ARCHITECTURE.md` — architecture notes and diagram

## Why SQLite?
SQLite is a lightweight relational database stored as a single file. It's ideal for demos and easy to explain:
- No separate DB server to configure
- ACID compliant for single-writer scenarios
- File `items.db` lives inside container (or host when using docker-compose)
- **Important**: When you scale to multiple replicas in Kubernetes each pod gets its own copy of the DB file (data won't be shared). This is intentional for the assignment to keep the demo simple. In production you'd use PostgreSQL/MySQL with PersistentVolumes and StatefulSets.

## Quick local run (recommended for demo)
1. Build:
   ```bash
   docker build -t flask-sqlite-demo:local .
   ```
2. Run with docker-compose (this mounts `items.db` on host so data persists):
   ```bash
   docker compose up --build
   ```
   Then open `http://localhost:5000/health`

## Kubernetes (demo)
- Apply namespace:
  ```bash
  kubectl apply -f k8s/namespace.yaml
  ```
- Edit `k8s/app-deployment.yaml` to set correct image (replace `yourdockerhubuser/...`)
- Apply manifests:
  ```bash
  kubectl apply -f k8s/app-deployment.yaml -n devops-challenge
  kubectl apply -f k8s/app-service.yaml -n devops-challenge
  ```
- Access via NodePort at `<NODE_IP>:30080` (or `kubectl port-forward svc/flask-app 5000:5000 -n devops-challenge`)

## Notes to explain in interview
- Explain why SQLite is chosen and its limitations when scaling.
- Show how CI builds and publishes image on `main` branch.
- Explain how you'd change to Postgres for production: use PVC, DB Service ClusterIP, and StatefulSet or managed DB.

