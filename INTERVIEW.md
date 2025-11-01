# Interview script — how to explain your solution

1. Overview
   - "I created a simple Flask REST API that performs CRUD operations on an 'items' table."
   - "To keep the demo simple and focus on CI/CD + Kubernetes, I used SQLite as the database."

2. Why SQLite?
   - "SQLite is a file-based relational DB. It's easy to set up and explain."
   - "No separate DB process needed — good for demos and coding tests."

3. Architecture and trade-offs
   - "Local/demo: Docker Compose mounts the DB file so data persists across restarts."
   - "Kubernetes demo: I deploy 2 replicas. Each replica gets its own ephemeral DB file (emptyDir). This means data is not shared between pods — I will explicitly mention this during interview and explain the production alternative."
   - Production alternative:
     - Use PostgreSQL (managed or deployed), a PersistentVolumeClaim for data, and a Deployment/StatefulSet.
     - Keep DB Service `ClusterIP` so it's internal to the cluster.

4. CI/CD
   - "I added a GitHub Actions workflow to build the Docker image and push to Docker Hub on pushes to `main`."
   - "In production pipeline you'd add image scanning, a staging environment, and gated deploys."

5. Security & networking
   - "DB is not exposed externally (in production). Secrets should be stored in Kubernetes Secrets or a secret manager."
   - "Use NetworkPolicies to restrict traffic to DB from app only."

6. Demo steps to run during interview
   - `docker compose up --build`
   - `curl -X POST http://localhost:5000/items -H 'Content-Type: application/json' -d '{"name":"demo"}'`
   - `curl http://localhost:5000/items`
   - Show code for `app.py` to explain endpoints and SQLAlchemy use.

7. Questions to expect
   - "How would you persist data in K8s?" -> PVC + StatefulSet or managed DB
   - "How would you secure credentials?" -> K8s Secrets or external secret manager
