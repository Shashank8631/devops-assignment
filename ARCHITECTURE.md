# Architecture notes & diagram

- App: Flask (stateless HTTP app) — exposes CRUD endpoints
- DB: SQLite file (`items.db`) for simple demo
- Container: Docker image with app and DB file (or host-mounted DB file in docker-compose)
- CI: GitHub Actions builds image on `main`
- K8s: Deployment with 2 replicas; Service NodePort to expose app

## Diagram (Mermaid)
```mermaid
flowchart LR
  Developer -->|push to main| GitHubActions
  GitHubActions -->|build image| DockerHub
  DockerHub -->|image pull| Kubernetes
  subgraph K8sCluster
    direction TB
    Service[NodePort Service] --> Deployment[flask-app Deployment (2 replicas)]
    Deployment --> Pod1[Pod A (items.db)]
    Deployment --> Pod2[Pod B (items.db)]
  end
```

## Talking points
- Each pod has its own DB file in this demo (not shared).
- For production you'd use a proper DB with persistent storage and internal-only networking.
