# Chapter 01: Docker Containerization Strategy

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Multi-Stage Build Architecture](sec-01-multi-stage-build-architecture.md) | Build stages, dependency caching, output minimization, layer optimization |
| 02 | [Image Optimization](sec-02-image-optimization.md) | Base image selection (Alpine/Distro-less), size reduction, dependency pruning, SBOM generation |
| 03 | [Docker Compose for Local Dev](sec-03-docker-compose-local-dev.md) | Service definitions, volume mounts, hot reload, service dependencies, network configuration |
| 04 | [Production Image Strategy](sec-04-production-image-strategy.md) | Minimal runtime images, non-root user, security scanning, image signing, registry management |
| 05 | [Base Image Selection](sec-05-base-image-selection.md) | Node.js base images, Python base images, language runtime optimization, distroless vs alpine |
| 06 | [Docker Networking](sec-06-docker-networking.md) | Bridge networks, host networking, overlay networks, DNS resolution, port mapping |
| 07 | [CI/CD Docker Integration](sec-07-cicd-docker-integration.md) | Docker layer caching in CI, parallel image builds, image tagging strategy, registry push |
| 08 | [Container Security](sec-08-container-security.md) | Image scanning (Trivy), secret management, read-only filesystem, security context, seccomp profiles |
