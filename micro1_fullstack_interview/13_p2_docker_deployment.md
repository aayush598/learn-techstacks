# Priority 2 — Docker / Deployment (Q374–Q385)

**Why these matter for micro1:** production FastAPI + Next.js deployment on AWS. Expect image vs container, Dockerfile optimization, Compose, volumes, multi-stage builds, and debugging a crashing container.

---

## Q374: What is Docker?

A platform for **packaging applications with their dependencies** into portable containers and running them consistently anywhere (dev → CI → prod).

- **Images** — immutable, buildable packages (code + runtime + deps + config).
- **Containers** — running instances of images; isolated processes with their own filesystem/network/pid namespaces.
- **Key benefits:** consistency ("works on my machine" gone), isolation, reproducibility, lightweight vs VMs (shares the host kernel), easy scaling/CI.
- Components: Docker Engine (daemon), Dockerfile, images/registries (Docker Hub, ECR), Docker Compose, volumes/networks.

---

## Q375: What is the difference between an image and a container?

| | **Image** | **Container** |
|---|---|---|
| What | Immutable blueprint/template | Running instance of an image |
| State | Static (read-only layers) | Mutable (writable layer, runtime state) |
| Analogy | Class / installer / snapshot | Object / running process |
| Creation | Built (`docker build`) | Run (`docker run`) |
| Lifecycle | Persistent until removed | Start, run, stop, remove |

- Same image → many containers.
- `docker run image` creates a fresh container each time; container state is lost unless volumes are used (Q381).

---

## Q376: What is a Dockerfile?

A **text file of build instructions** that defines how to assemble an image: base OS, dependencies, code, startup command.

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- Each instruction creates a **layer** (cached); order matters for cache hits (install deps before copying code).
- Best practices: minimal base, `.dockerignore`, non-root user, multi-stage builds (Q382–383).

---

## Q377: How do you Dockerize a FastAPI application?

```dockerfile
# --- build stage ---
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# --- runtime stage ---
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir /wheels/*
COPY ./app ./app
RUN adduser --disabled-password appuser && chown -R appuser /app
USER appuser
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Key points to mention:**
- Multi-stage → tiny final image (deps only, no build toolchain).
- `.dockerignore` (`__pycache__`, `.git`, `.venv`, tests) to keep context small.
- Non-root user for security.
- Healthcheck: `HEALTHCHECK CMD curl -f http://localhost:8000/healthz`.
- For production use **Gunicorn + Uvicorn workers** (`gunicorn app.main:app -k uvicorn.workers.UvicornWorker`) (Q652).

---

## Q378: What is Docker Compose?

A tool to **define and run multi-container applications** with one YAML file.

```yaml
services:
  api:
    build: .
    ports: ["8000:8000"]
    environment:
      DATABASE_URL: postgresql://postgres:pass@db:5432/app
    depends_on: [db]
    volumes: ["./app:/app"]        # dev hot-reload
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: pass
    volumes: ["pgdata:/var/lib/postgresql/data"]

volumes:
  pgdata:
```

- One command: `docker compose up`.
- Great for **local dev** (API + DB + Redis + worker together) and simple prod deployments.
- Not a full orchestrator — for prod scale use ECS/EKS/k8s (Q360, Q384).

---

## Q379: How do containers communicate?

Via **Docker networks**:

1. **User-defined bridge networks** — containers on the same network resolve each other by **service/container name** (`http://db:5432`).
2. **Host network** — share host network stack (ports directly; Linux only).
3. **Port mapping (`-p host:container`)** — expose container ports to the host/external.
4. **`depends_on`** — ordering only (doesn't guarantee readiness — use healthchecks + wait loops).

```yaml
# compose: api can reach db at host "db"
DATABASE_URL: postgresql://postgres:pass@db:5432/app
```

- Compose automatically creates a default network for the project; containers reference each other by name.
- Cross-host communication = real networking (load balancer / service discovery) — that's what orchestrators add.

---

## Q380: How do you pass environment variables to Docker?

1. **Inline:** `docker run -e API_KEY=xyz image`.
2. **Env file:** `docker run --env-file .env image` (gitignore it!).
3. **Compose `environment:`** or `env_file:`.
4. **Secrets (production):** inject from the orchestrator/secrets manager — **never bake into the image** or commit to git (Q70, Q367).

```yaml
# compose
environment:
  DATABASE_URL: ${DATABASE_URL}     # from host env / .env
secrets:
  - llm_api_key
```

- The app reads env vars (pydantic-settings, Q69).
- Keep secrets out of image layers (they persist in history).

---

## Q381: What are Docker volumes?

**Persistent storage** managed by Docker, outliving containers.

```yaml
services:
  db:
    image: postgres:16
    volumes:
      - pgdata:/var/lib/postgresql/data   # named volume — persists across restarts
```

- **Named volumes** — Docker-managed, survive container removal.
- **Bind mounts** — host directory → container (`./app:/app`); used for dev hot-reload; path-dependent.
- **tmpfs** — in-memory (ephemeral) for cache.
- Why: containers are **ephemeral** — any data written to the container layer is lost on remove. DB data, uploads, caches must live in volumes.
- For prod object storage (S3), use it instead of container filesystems (Q357).

---

## Q382: What are multi-stage builds?

A Dockerfile with **multiple `FROM` stages** — build tools/deps in one stage, copy only the needed artifacts into a **small final stage**.

```dockerfile
FROM node:20 AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build          # produces .next/ (or dist/)

FROM node:20-slim AS runner
WORKDIR /app
COPY --from=build /app/.next ./next
COPY --from=build /app/package*.json ./
RUN npm ci --omit=dev
CMD ["npm", "start"]
```

**Benefits:** the final image excludes build toolchains (node_modules for build, compilers, dev deps) → smaller, fewer attack surfaces, faster pulls. Layers are cached per-stage.

---

## Q383: How would you reduce Docker image size?

1. **Small base image** — `python:3.12-slim` instead of full; `alpine` (careful: musl wheels), `distroless`.
2. **Multi-stage builds** (Q382) — don't ship build toolchain.
3. **Only production deps** — `pip install --no-cache-dir`, `npm ci --omit=dev`.
4. **`.dockerignore`** — exclude `.git`, tests, `__pycache__`, `.venv`, caches.
5. **Clean caches** in the same RUN layer (`apt-get clean`, remove pip cache) — keep layers small.
6. **Layer ordering** for cache reuse (deps before code).
7. **Compress/combine** — `RUN` fewer, chained commands; avoid duplicate `COPY`s.
8. **Don't copy what you don't run** (docs, sample data).
9. **Tools:** `docker buildx` + `--squash`, `dive` to analyze layers, `SlimToolkit`.

**Result to brag about:** "cut the image from ~900MB to ~150MB with multi-stage + slim base."

---

## Q384: How would you deploy Docker containers to AWS?

**Path: ECR → ECS/Fargate → ALB (or EKS for k8s).**

1. **Build + push** image to **ECR** (private registry).
2. **Task definition** — image, CPU/memory, env, secrets (Q367), healthcheck, ports.
3. **Service** — desired count, ALB target group, autoscaling, rolling deploys.
4. **ALB** — route HTTPS → service; path routing if sharing with Next.js.
5. **Networking** — Fargate tasks in private subnets; DB in private subnet; secrets via Secrets Manager (Q364).
6. **CI/CD** — GitHub Actions: test → build → push ECR → `ecs update-service` (force new deployment) (Q621).
7. **EKS** (Q616) when you need Kubernetes (advanced scheduling, service mesh) — more ops; ECS is simpler for most teams.

```yaml
# GitHub Actions (sketch)
- uses: docker/build-push-action@v5
  with: { push: true, tags: "ecr.../zara:latest" }
- run: aws ecs update-service --cluster zara --service api --force-new-deployment
```

---

## Q385: How would you debug a container that keeps crashing?

**Systematic:**
1. **See the logs first:** `docker logs <container>` (and `--follow` for live). The crash reason is usually here (import error, missing env, port bind, command typo).
2. **Inspect state:** `docker ps -a` (exit code), `docker inspect <id>` (ExitCode, RestartCount, OOMKilled flag, last state).
   - Exit 137 → OOM or killed; Exit 1 → app error.
3. **Run interactively to reproduce:** `docker run --rm -it --entrypoint sh <image>` — test the start command manually, check env (`env`), paths, `python -c "import app"`.
4. **Check health checks** — failing healthcheck → task restarted (not a crash).
5. **Resource limits** — memory limit vs usage (`docker stats`); OOMKilled.
6. **Environment/secrets** — missing env var that the app requires (pydantic-settings fails fast, Q69); mis-named secret.
7. **Network** — can't reach DB/dependency (`depends_on` isn't readiness); test connectivity from inside.
8. **Config drift** — code builds locally but fails in image (deps not installed, wrong working dir, `.dockerignore` removed something).
9. **Fix + iterate:** change code/Dockerfile → rebuild → redeploy. Add a startup `--preload` check or explicit error messages.
10. **In ECS/prod:** check task definitions, stop reasons in ECS console/`aws ecs describe-tasks`, CloudWatch logs, and use a `HEALTHCHECK` that fails with useful detail.
