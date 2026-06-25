# Docker Basics

## Architecture

```
┌───────────────┐
│  Docker Client │  (CLI: docker build, run, push)
└───────┬───────┘
        │ REST API (HTTP)
┌───────▼───────┐
│  Docker Daemon │  (dockerd — manages images, containers, networks)
└───────┬───────┘
        │
┌───────▼───────┐
│  containerd   │  (OCI runtime manager — lifecycle)
└───────┬───────┘
        │
┌───────▼───────┐
│   runc        │  (OCI runtime spec — create/run container)
└───────────────┘
```

## Images vs Containers
- **Image:** read-only template (layers), defined by **Dockerfile**
- **Container:** running instance of an image (adds writable layer)
- **Layer caching:** each Dockerfile instruction = layer; cached if unchanged

## Dockerfile Instructions

```dockerfile
FROM ubuntu:22.04          # Base image (starting point)
LABEL maintainer="dev@x"   # Metadata
RUN apt update && apt install -y python3  # Build-time command (creates layer)
COPY . /app                # Copy files from context
WORKDIR /app               # Set working directory
EXPOSE 8080                # Document port (just metadata)
ENV MY_VAR=value           # Environment variable
CMD ["python3", "app.py"]  # Default command (entrypoint args)
ENTRYPOINT ["python3"]     # Container entry point (overrides CMD when passed args)
```

## Build Cache & Layer Optimization
- Each `RUN`, `COPY`, `ADD` creates a **new layer**
- Cached if the instruction + context unchanged (hash-based)
- **Optimization:** order FROM → RUN (deps) → COPY (code) → CMD
  - Change code often; change deps rarely
- **Multi-stage builds:** `FROM ... AS builder`, `COPY --from=builder`
  - Final image tiny (only runtime, not build tools)

## Networking Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| **bridge** (default) | Private network per host, NAT port mapping | Single-host containers |
| **host** | Container uses host network stack (no isolation) | Performance-critical |
| **overlay** | Multi-host networking (Swarm/K8s) | Distributed apps |
| **macvlan** | Container gets MAC address on physical net | Legacy apps, IP-per-container |
| **none** | No networking (loopback only) | Secure isolated tasks |

## Docker Compose
```yaml
services:
  web:
    build: .
    ports: ["8080:8080"]
    depends_on: [db]
  db:
    image: postgres:15
    volumes: ["pgdata:/var/lib/postgresql/data"]
volumes:
  pgdata:
```

## Key Commands
- `docker build -t myapp .` — build image from Dockerfile
- `docker run -p 8080:80 myapp` — run container with port mapping
- `docker exec -it <id> bash` — shell into running container
- `docker ps` / `docker images` / `docker logs`
- `docker push myuser/myapp:tag` — push to registry
- `docker system prune` — clean unused resources

## Registry
- **Docker Hub:** public registry (rate-limited 2023+)
- **ECR (AWS), GCR (GCP), ACR (Azure):** cloud registries
- **Private registry:** `docker run registry:2` — self-hosted

## Interview Tips
- *"Containers are processes with namespaces + cgroups + layered filesystem"*
- *"Each line in Dockerfile is a layer; caching depends on hash of instruction + context"*
- *"Multi-stage builds produce smaller images (build deps in first stage, runtime in final)"*
- *"Docker networking: bridge (default), host (no isolation), overlay (multi-host)"*
