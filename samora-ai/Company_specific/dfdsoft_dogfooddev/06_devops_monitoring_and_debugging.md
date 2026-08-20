# DFDSOFT / DogFoodDev — DevOps, Monitoring & Debugging (100 Q&A)
> Role: AI Coding & Agent Development Specialist  > Candidate: Aayush Gid (Docker/GitHub Actions/CI-CD/Linux/Git/debugging background)

---

## Docker (Q1–Q15)

**Q1: What is the difference between a container and a virtual machine?**
A: A container shares the host OS kernel and isolates processes using namespaces and cgroups, making it lightweight and fast to start. A VM runs a full guest OS on a hypervisor, providing stronger isolation but consuming more resources and taking longer to boot.

**Q2: What is a Dockerfile and what does each common instruction do?**
A: A Dockerfile is a text file with instructions to build a Docker image layer by layer. Key instructions include `FROM` (base image), `RUN` (execute commands), `COPY`/`ADD` (copy files), `WORKDIR` (set working directory), `ENV` (set environment variables), `EXPOSE` (document ports), and `CMD`/`ENTRYPOINT` (default command).

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

**Q3: What is a multi-stage build and why should you use it?**
A: A multi-stage build uses multiple `FROM` statements so that build-time dependencies (compilers, SDKs) are discarded in the final image. This drastically reduces image size and attack surface.

```dockerfile
FROM node:20 AS builder
WORKDIR /app
COPY . .
RUN npm ci && npm run build

FROM node:20-slim
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json .
RUN npm ci --omit=dev
CMD ["node", "dist/index.js"]
```

**Q4: What does `.dockerignore` do and why is it important?**
A: `.dockerignore` excludes files and directories from the Docker build context, preventing them from being sent to the daemon. This speeds up builds and avoids leaking secrets or unnecessary files into the image (e.g., `.git`, `node_modules`, `.env`).

**Q5: What are Docker volumes and how do they differ from bind mounts?**
A: Volumes are managed by Docker and stored in `/var/lib/docker/volumes/`, making them portable and backed up easily. Bind mounts map a host directory directly into the container, useful for development but host-dependent and less secure.

```bash
# Named volume
docker run -v mydata:/app/data myimage

# Bind mount
docker run -v /home/user/project:/app myimage
```

**Q6: How does Docker networking work? What are bridge, host, and overlay networks?**
A: `bridge` (default) creates an isolated network for containers on a single host. `host` removes network isolation and shares the host's network stack. `overlay` enables container-to-container communication across multiple Docker Swarm nodes.

**Q7: What is `docker-compose` and when should you use it?**
A: `docker-compose` (now `docker compose`) defines and runs multi-container applications using a YAML file. It is ideal for local development, testing, and orchestrating services like a web app + database + Redis with a single `docker compose up`.

```yaml
services:
  web:
    build: .
    ports: ["3000:3000"]
    depends_on: [db]
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: secret
    volumes: ["pgdata:/var/lib/postgresql/data"]
volumes:
  pgdata:
```

**Q8: What is the difference between `CMD` and `ENTRYPOINT`?**
A: `CMD` provides default arguments that can be overridden at runtime (`docker run myimage arg1`). `ENTRYPOINT` sets a fixed executable; `CMD` then supplies default arguments. Together they create a configurable default command.

```dockerfile
ENTRYPOINT ["python"]
CMD ["main.py"]
# docker run myimage            → python main.py
# docker run myimage script.py  → python script.py
```

**Q9: How do you reduce Docker image size?**
A: Use slim/distroless base images (`python:3.11-slim`, `gcr.io/distroless`), multi-stage builds, combine `RUN` commands to reduce layers, clean caches in the same layer (`pip install --no-cache-dir`), and use `.dockerignore` to exclude unnecessary files.

**Q10: What is a Docker health check and how do you define one?**
A: A health check periodically runs a command inside the container to determine if it is functioning. Docker marks the container as `healthy`, `unhealthy`, or `starting`.

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1
```

**Q11: How do you debug a running Docker container?**
A: Use `docker exec -it <container> bash` to get an interactive shell, `docker logs <container>` to view stdout/stderr, `docker inspect <container>` for metadata, `docker stats` for resource usage, and `docker cp` to copy files in/out.

**Q12: What are Docker image tags and why do they matter for CI/CD?**
A: Tags label image versions (e.g., `myapp:1.2.3`, `myapp:latest`). In CI/CD, use immutable tags like the git SHA (`myapp:a1b2c3d`) or semantic version for reproducibility. Avoid relying solely on `latest` as it changes unpredictably.

**Q13: What is Docker layer caching and how does it affect build speed?**
A: Docker caches each instruction as a layer. If an instruction and its inputs haven't changed, Docker reuses the cached layer. Put rarely-changing steps (like `COPY requirements.txt` and `RUN pip install`) before frequently-changing steps (like `COPY . .`) to maximize cache hits.

**Q14: How do you handle secrets in Docker containers securely?**
A: Never bake secrets into images via `COPY` or `ENV` in Dockerfiles. Use Docker secrets in Swarm, mount secrets as files at runtime (`docker run --secret`), use environment variables injected at deploy time, or integrate with Vault/AWS Secrets Manager.

**Q15: What is the difference between `docker compose up --build` and `docker compose up` without it?**
A: `--build` forces a rebuild of images before starting containers, picking up any Dockerfile or context changes. Without it, Compose reuses existing images even if the Dockerfile has changed, which can lead to running stale code.

---

## GitHub Actions (Q16–Q28)

**Q16: What is GitHub Actions and how does a workflow file work?**
A: GitHub Actions is a CI/CD platform built into GitHub that runs automation in response to repository events. A workflow is a YAML file in `.github/workflows/` containing jobs, which contain steps that run commands or use shared actions.

```yaml
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm test
```

**Q17: What are the common trigger events in GitHub Actions?**
A: Common triggers include `push` (code pushed to a branch), `pull_request` (PR opened/synchronized), `schedule` (cron-based), `workflow_dispatch` (manual trigger), `release` (tag published), and `workflow_call` (called by another workflow).

```yaml
on:
  push:
    branches: [main]
  schedule:
    - cron: '0 2 * * 1'  # Every Monday at 2 AM
  workflow_dispatch:
```

**Q18: How do you use secrets in GitHub Actions?**
A: Store secrets in the repository settings under Settings → Secrets → Actions. Reference them as `${{ secrets.MY_SECRET }}` in workflow files. They are masked in logs and not available to pull request workflows from forks by default.

**Q19: What are matrix builds and when should you use them?**
A: Matrix builds run the same job across multiple combinations of parameters (OS, language version, etc.). Use them to test cross-platform compatibility or multiple dependency versions in parallel.

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    node-version: [18, 20, 22]
```

**Q20: How do you cache dependencies in GitHub Actions?**
A: Use the built-in `actions/cache` action or framework-specific caches (`actions/setup-node` has built-in npm caching). Cache key on lock file hash for deterministic restores.

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: npm-${{ hashFiles('package-lock.json') }}
```

**Q21: What are reusable workflows and how do you call them?**
A: Reusable workflows are workflow files that can be invoked from other workflows using `workflow_call`. They reduce duplication across repos or jobs. The caller uses the `uses` key at the job level.

```yaml
# .github/workflows/reusable-build.yml (callee)
on:
  workflow_call:
    inputs:
      node-version:
        type: string

# Caller workflow
jobs:
  build:
    uses: ./.github/workflows/reusable-build.yml
    with:
      node-version: '20'
```

**Q22: What are self-hosted runners and when would you use them?**
A: Self-hosted runners are machines you manage that execute GitHub Actions jobs. Use them for access to private network resources, GPU workloads, custom hardware, or to avoid per-minute costs on GitHub-hosted runners.

**Q23: How do you handle conditional steps in GitHub Actions?**
A: Use the `if` key on steps with expressions. Common conditions check the event type, branch name, or previous step outcomes.

```yaml
- name: Deploy
  if: github.ref == 'refs/heads/main' && github.event_name == 'push'
  run: ./deploy.sh
```

**Q24: What is an artifact in GitHub Actions and how do you use them?**
A: Artifacts are files produced during a workflow run (build outputs, test reports) that can be uploaded, downloaded, or passed between jobs. Use `actions/upload-artifact` and `actions/download-artifact`.

```yaml
- uses: actions/upload-artifact@v4
  with:
    name: build-output
    path: dist/
```

**Q25: How do you prevent a workflow from running on certain file changes?**
A: Use the `paths` or `paths-ignore` filter on triggers. This avoids unnecessary runs when only documentation or config files change.

```yaml
on:
  push:
    paths:
      - 'src/**'
      - 'package.json'
    paths-ignore:
      - '*.md'
```

**Q26: What are GitHub Actions environments and why use them?**
A: Environments (e.g., `staging`, `production`) let you configure protection rules like required reviewers, branch restrictions, and deployment gates. They also scope environment-specific secrets.

**Q27: How do you debug a failing GitHub Actions workflow?**
A: Enable step debug logging by setting the secret `ACTIONS_STEP_DEBUG` to `true`. Use `act` to run workflows locally, add `run: cat file` or `run: env` for inspection, and check the raw logs for error context.

**Q28: How do you create a custom GitHub Action?**
A: Package reusable logic as a JavaScript (`index.js` + `action.yml`), composite (`action.yml` with `runs.using: composite`), or Docker action. Publish to the marketplace or use via relative path in your repo.

---

## CI/CD (Q29–Q40)

**Q29: What is the difference between continuous integration, continuous delivery, and continuous deployment?**
A: CI automates building and testing code on every commit. CD (delivery) extends CI by automating release artifact creation and staging deployment with manual production approval. Continuous deployment goes further by automatically deploying every passing change to production.

**Q30: What does a well-designed CI/CD pipeline look like?**
A: A typical pipeline: lint → unit tests → build → integration tests → security scan → artifact publish → deploy to staging → smoke tests → deploy to production. Each stage gates the next, failing fast on issues.

**Q31: How should you structure testing in a CI pipeline?**
A: Run fast tests (unit, lint) first for quick feedback, then slower tests (integration, e2e) in parallel if possible. Use test result reporting, fail the pipeline on test failures, and gate deployments on minimum coverage thresholds.

**Q32: What is SAST and DAST and how do you integrate them into CI/CD?**
A: SAST (Static Application Security Testing) scans source code for vulnerabilities without running it (e.g., CodeQL, Bandit). DAST (Dynamic Application Security Testing) probes a running application for vulnerabilities (e.g., OWASP ZAP). Run SAST on every PR, DAST against staging before production deploys.

```yaml
- name: SAST with CodeQL
  uses: github/codeql-action/analyze@v3
```

**Q33: What are deployment strategies and when would you use each?**
A: **Blue-green**: two identical environments, traffic switches atomically — zero downtime, easy rollback. **Canary**: gradually route a percentage of traffic to the new version — catches issues with minimal impact. **Rolling**: incrementally replace instances — resource efficient but slower rollback.

**Q34: How do you handle database migrations in a CI/CD pipeline?**
A: Run migrations as a separate step before application deployment. Test migrations against a copy of production data in staging. Always make migrations backward-compatible (expand-then-contract pattern) to avoid downtime during deploys.

**Q35: What is artifact management and why is it important?**
A: Artifact management stores build outputs (Docker images, binaries, packages) in a versioned registry (Docker Hub, GitHub Packages, Artifactory). It ensures reproducibility, enables rollbacks, and provides audit trails for deployments.

**Q36: How do you implement rollback in a CI/CD pipeline?**
A: Keep previous version artifacts tagged and deployable. For Docker, pull the previous image tag. For Kubernetes, use `kubectl rollout undo`. For infrastructure-as-code, maintain versioned state. Automate rollback triggers on health-check failures.

**Q37: What is infrastructure as code (IaC) and how does it relate to CI/CD?**
A: IaC defines infrastructure (servers, networks, policies) in version-controlled code (Terraform, Pulumi, CloudFormation). CI/CD pipelines apply IaC changes through the same review/test/deploy workflow as application code, ensuring reproducibility and auditability.

**Q38: How do you manage environment variables across dev, staging, and production?**
A: Use CI/CD platform environment variables scoped per environment, secrets managers (Vault, AWS SSM), or `.env` files excluded from version control. Load variables at runtime, never hard-code them. Use tools like `dotenvx` for local development parity.

**Q39: What is a pipeline as code anti-pattern?**
A: Common anti-patterns include: putting all logic in one massive step instead of modular jobs, not caching dependencies, running slow tests before fast ones, ignoring flaky tests, storing secrets in workflow files, and not using `needs` for proper job dependency ordering.

**Q40: How do you handle monorepo CI/CD efficiently?**
A: Use path-based triggers to only run pipelines for changed packages. Employ tools like `nx`, `turbo`, or `lerna` for affected-based builds. Split into separate workflows per package and use shared reusable workflows to reduce duplication.

---

## Linux (Q41–Q55)

**Q41: What is the Linux filesystem hierarchy?**
A: Key directories: `/` (root), `/home` (user dirs), `/etc` (config), `/var` (variable data, logs), `/tmp` (temporary), `/usr` (user programs), `/opt` (optional software), `/proc` (process info), `/sys` (kernel/sysfs), `/bin` & `/sbin` (essential binaries).

**Q42: How do you manage processes in Linux?**
A: `ps aux` lists all processes, `top`/`htop` shows real-time resource usage, `kill <pid>` sends signals (default SIGTERM), `kill -9` forces termination, `bg`/`fg` manage background/foreground jobs, and `nohup` runs processes immune to hangup signals.

**Q43: Explain Linux file permissions.**
A: Each file has owner, group, and others permissions for read (4), write (2), execute (1). `chmod 755 file` sets rwxr-xr-x. `chown user:group file` changes ownership. `umask` sets default permissions for new files. Special bits: `setuid` (4), `setgid` (2), `sticky` (1).

```bash
ls -la
# -rwxr-xr-x 1 user group 4096 Jan 1 00:00 script.sh

chmod +x script.sh      # add execute for all
chmod 600 secret.key     # owner read/write only
```

**Q44: What is `systemd` and how do you manage services?**
A: `systemd` is the init system and service manager on most Linux distributions. Use `systemctl start|stop|restart|enable|disable|status <service>` to manage services. Unit files in `/etc/systemd/system/` define custom services.

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/myapp/main.py
Restart=always
User=myapp

[Install]
WantedBy=multi-user.target
```

**Q45: How do you set up cron jobs?**
A: Cron executes commands on a schedule defined by a crontab. Edit with `crontab -e`. Format: `minute hour day-of-month month day-of-week command`.

```bash
# Run backup every day at 2 AM
0 2 * * * /opt/scripts/backup.sh >> /var/log/backup.log 2>&1

# Run every 5 minutes
*/5 * * * * /opt/scripts/health-check.sh
```

**Q46: How do you manage logs in Linux?**
A: Application logs are typically in `/var/log/`. `journalctl` queries systemd journal logs. Use `tail -f /var/log/syslog` for real-time monitoring. Configure log rotation with `/etc/logrotate.conf`. For structured logging, output JSON and ship to a central system (ELK, Loki).

**Q47: What are common networking commands in Linux?**
A: `ss -tlnp` or `netstat -tlnp` show listening ports, `curl` and `wget` make HTTP requests, `dig`/`nslookup` resolve DNS, `ip addr` shows interfaces, `ping` tests connectivity, `traceroute` traces packet paths, and `iptables`/`nftables` manages firewall rules.

```bash
ss -tlnp | grep 8080
curl -s http://localhost:8080/health
dig example.com +short
```

**Q48: How do you check disk space and manage storage?**
A: `df -h` shows filesystem disk usage, `du -sh /path` shows directory sizes, `lsblk` lists block devices. Use `find / -type f -size +100M` to find large files. Clean with `journalctl --vacuum-size=500M` or `docker system prune`.

**Q49: How do you find files and search content in Linux?**
A: `find /path -name "*.log" -mtime -7` finds files by name/date. `grep -r "error" /var/log/` searches content recursively. `which python` locates executables. `locate` uses a pre-built index for fast lookups (update with `updatedb`).

**Q50: What is the purpose of `/proc` and `/sys`?**
A: `/proc` is a virtual filesystem exposing process and kernel info as files (e.g., `/proc/<pid>/status`, `/proc/cpuinfo`). `/sys` exposes kernel objects like devices, drivers, and filesystems. Both are used for diagnostics without system calls.

**Q51: How do you check system resource usage and performance?**
A: `top`/`htop` for CPU/memory per process, `free -h` for memory, `vmstat 1` for CPU/IO stats, `iostat` for disk I/O, `sar` for historical data, `uptime` for load averages, and `dmesg` for kernel messages including OOM kills.

**Q52: How do you manage users and groups in Linux?**
A: `useradd -m -s /bin/bash newuser` creates a user, `passwd newuser` sets the password, `usermod -aG sudo newuser` adds to a group, `userdel -r olduser` removes a user. `groups newuser` shows group membership.

**Q53: What are environment variables and how do you manage them?**
A: `export VAR=value` sets a variable for the current session. `/etc/environment` or `~/.bashrc` persist variables. `env` shows all variables, `printenv VAR` shows one. In scripts, use `"$VAR"` (quoted) to prevent word splitting.

```bash
export DATABASE_URL="postgres://localhost/mydb"
echo "$DATABASE_URL"  # Always quote to handle spaces/special chars
```

**Q54: How do you set up SSH key-based authentication?**
A: Generate a key pair with `ssh-keygen -t ed25519`, copy the public key to the server with `ssh-copy-id user@host`, and ensure `~/.ssh/authorized_keys` has correct permissions (`600`). Disable password auth in `/etc/ssh/sshd_config` for security.

**Q55: How do you diagnose and handle an out-of-memory (OOM) situation?**
A: Check `dmesg | grep -i oom` for OOM killer events. Use `free -h` and `top` to identify memory-hungry processes. Increase swap temporarily with `fallocate` + `mkswap`. Long-term, optimize application memory usage, set container memory limits, and configure cgroup limits.

---

## Git (Q56–Q68)

**Q56: What is Git Flow and when should you use it?**
A: Git Flow uses `main` (production), `develop` (integration), `feature/*`, `release/*`, and `hotfix/*` branches. Use it for projects with scheduled releases and versioned software. For fast-moving web apps, consider trunk-based development instead.

**Q57: What is trunk-based development?**
A: All developers commit to a single `main` branch (or short-lived feature branches merged within a day). Features are hidden behind feature flags. It enables continuous delivery, reduces merge conflicts, and requires robust CI/CD and testing.

**Q58: What is the difference between `git rebase` and `git merge`?**
A: `git merge` creates a merge commit combining two branches, preserving full history. `git rebase` replays commits on top of another branch, creating a linear history. Rebase is cleaner but rewrites history — never rebase shared/public branches.

```bash
git checkout feature
git rebase main        # Replay feature commits on top of main
git checkout main
git merge feature      # Fast-forward merge
```

**Q59: What is `git cherry-pick` and when would you use it?**
A: `git cherry-pick <commit>` applies a specific commit from one branch to another. Use it to backport a bug fix from `main` to a release branch, or to move a single commit that was accidentally made on the wrong branch.

**Q60: What is `git bisect` and how does it help?**
A: `git bisect` uses binary search through commit history to find the exact commit that introduced a bug. Mark a known-bad and known-good commit, and Git checks out the midpoint for you to test.

```bash
git bisect start
git bisect bad          # current commit is broken
git bisect good v1.0.0  # this tag was working
# Git checks out a middle commit — test it
git bisect good  # or git bisect bad
# Repeat until the offending commit is found
git bisect reset
```

**Q61: What are git worktrees and why are they useful?**
A: `git worktree add ../hotfix-branch hotfix` creates a separate working directory for a branch without stashing or switching. This lets you work on a hotfix while keeping your feature branch work in progress, avoiding context switches.

**Q62: What are git hooks and how do you use them?**
A: Git hooks are scripts that run automatically on events (pre-commit, commit-msg, pre-push). They live in `.git/hooks/` or can be shared via tools like `husky`. Use them for linting, formatting, and enforcing commit message conventions.

```bash
# .husky/pre-commit
npx lint-staged
npx prettier --check .
```

**Q63: What are conventional commits?**
A: Conventional commits use a structured format: `type(scope): description` (e.g., `feat(auth): add OAuth2 login`, `fix(api): handle null response`). This enables automated changelogs, semantic versioning, and clear project history.

**Q64: How do you undo a commit that has already been pushed?**
A: Create a new commit that reverses the changes with `git revert <commit>`. Never use `git reset --hard` on pushed commits as it rewrites shared history. If you must remove a commit, coordinate with your team and use `git push --force-with-lease` carefully.

**Q65: What is `git stash` and when should you use it?**
A: `git stash` temporarily shelves uncommitted changes. Use it when you need to switch branches quickly without committing work-in-progress. `git stash pop` restores the most recent stash, `git stash list` shows all stashes.

**Q66: How do you clean up local branches that have been deleted from the remote?**
A: `git fetch --prune` removes local references to deleted remote branches. `git remote prune origin` does the same. Add this to your CI or as a post-fetch hook to keep your repository tidy.

**Q67: What is the difference between `git pull` and `git fetch` + `git merge`?**
A: `git fetch` downloads remote changes without modifying your working tree. `git pull` is shorthand for `git fetch` followed by `git merge` (or `git rebase` with `--rebase`). Use `fetch` + `merge` when you want to review changes before merging.

**Q68: How do you handle merge conflicts?**
A: After `git merge` reports conflicts, open the conflicted files and resolve the markers (`<<<<<<<`, `=======`, `>>>>>>>`). Use `git mergetool` for a visual helper. After resolving, `git add` the files and `git commit`. Prevent conflicts with smaller, frequent merges and clear team ownership of areas.

---

## Debugging Techniques (Q69–Q78)

**Q69: What is print debugging and when is it still useful?**
A: Print debugging involves adding `print()`/`console.log()` statements to inspect variable values and execution flow. It is still useful for quick investigation in scripts, log output analysis, and environments where attaching a debugger is impractical.

**Q70: How do you use Python's `logging` module effectively?**
A: Use structured logging with appropriate levels (DEBUG, INFO, WARNING, ERROR, CRITICAL). Configure format with timestamp, module, and level. Use `getLogger(__name__)` per module. For production, use JSON-formatted logs for easy parsing by tools like ELK or Loki.

```python
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='{"time":"%(asctime)s","level":"%(levelname)s","module":"%(module)s","msg":"%(message)s"}'
)
logger.info("Processing started", extra={"user_id": 123})
```

**Q71: How do you use the Python debugger (`pdb`/`breakpoint`)?**
A: Insert `breakpoint()` (Python 3.7+) in your code to drop into the debugger at that line. Use `n` (next), `s` (step into), `c` (continue), `p <expr>` (print), and `q` (quit). For remote debugging, use `debugpy` to attach VS Code or PyCharm to a running process.

**Q72: What is profiling and when should you use it?**
A: Profiling measures where time is spent in your code. Use `cProfile` for function-level profiling, `line_profiler` for line-by-line timing, and `py-spy` for sampling profiler that works on running processes without code modification.

```bash
python -m cProfile -s cumtime my_script.py
kernprof -l -v my_script.py  # line_profiler
py-spy top --pid 12345        # live profiling
```

**Q73: How do you diagnose memory leaks in Python?**
A: Use `tracemalloc` to track memory allocations, `objgraph` to find objects accumulating over time, `memory_profiler` for per-line memory usage, and `gc.get_objects()` to inspect the garbage collector. Compare snapshots to identify growth patterns.

```python
import tracemalloc
tracemalloc.start()
# ... run code ...
snapshot = tracemalloc.take_snapshot()
for stat in snapshot.statistics('lineno')[:10]:
    print(stat)
```

**Q74: How do you debug asynchronous code (asyncio, async/await)?**
A: Use `asyncio` debug mode (`asyncio.run(main(), debug=True)`), add logging to coroutines, use `asyncio.all_tasks()` to inspect running tasks, and check for unawaited coroutines. `aiodebug` and `trio`'s testing tools help catch concurrency bugs.

**Q75: What is structured logging and why is it important for debugging?**
A: Structured logging outputs machine-parseable formats (JSON) with consistent fields (timestamp, level, request_id, user_id, trace_id). It enables powerful querying in log aggregation systems and correlates logs across distributed services.

**Q76: How do you debug issues in a Docker container?**
A: Use `docker exec -it <container> bash` for interactive debugging, `docker logs <container> --tail 100` for recent output, `docker inspect <container>` for configuration, and `docker cp` to extract files. For production, attach a remote debugger or use `nsenter` to enter the container's namespace.

**Q77: How do you debug CI/CD pipeline failures?**
A: Reproduce the failure locally with the same environment (use `act` for GitHub Actions). Add diagnostic steps (`env`, `cat file`, `which command`). Check dependency versions, permissions, network access, and environment variables. Enable debug logging (`ACTIONS_STEP_DEBUG=true`).

**Q78: What is `strace` and when would you use it on Linux?**
A: `strace` traces system calls made by a process, showing file access, network connections, and signals. Use it to diagnose permission errors, missing files, unexpected network behavior, or understanding how a binary interacts with the OS.

```bash
strace -e trace=network -p 12345    # trace network calls
strace -e trace=file my_program      # trace file operations
```

---

## Monitoring and Observability (Q79–Q88)

**Q79: What are the three pillars of observability?**
A: **Metrics** (numeric time-series data like request count, latency), **Logs** (discrete event records with context), and **Traces** (distributed request paths across services). Together they provide a complete picture of system behavior.

**Q80: How does Prometheus collect and query metrics?**
A: Prometheus scrapes HTTP endpoints (e.g., `/metrics`) at configured intervals, storing time-series data. Use PromQL to query: `rate(http_requests_total[5m])` for request rate, `histogram_quantile(0.99, ...)` for p99 latency. Exporters expose metrics from third-party systems.

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'myapp'
    static_configs:
      - targets: ['localhost:8080']
```

**Q81: How do you use Grafana with Prometheus for dashboards?**
A: Add Prometheus as a Grafana data source, then create dashboards with panels querying Prometheus via PromQL. Use variables for dynamic dashboards (e.g., per-service, per-environment). Set up annotations for deployments to correlate metrics with changes.

**Q82: What is the ELK stack and when should you use it?**
A: ELK is Elasticsearch (storage/search), Logstash (processing/ingestion), and Kibana (visualization). Use it for full-text log search, complex aggregations, and audit trails. For lighter-weight log aggregation, consider Grafana Loki which stores only labels and references to object storage.

**Q83: What is distributed tracing and how does OpenTelemetry work?**
A: Distributed tracing tracks requests across service boundaries using unique trace IDs. OpenTelemetry provides SDKs to instrument code and export traces to backends like Jaeger or Tempo. Each service creates spans with timing, status, and metadata.

```python
from opentelemetry import trace
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("process_request") as span:
    span.set_attribute("user.id", user_id)
    result = do_work()
```

**Q84: What are SLAs, SLOs, and SLIs?**
A: **SLI** (Service Level Indicator) is a measurable metric like uptime percentage or latency. **SLO** (Service Level Objective) is the internal target for SLIs (e.g., 99.9% uptime). **SLA** (Service Level Agreement) is the external contract with consequences for missing targets.

**Q85: How do you set up meaningful alerts?**
A: Alert on symptoms that affect users (high error rate, elevated latency), not causes. Use multi-window multi-burn-rate alerting for SLOs. Avoid alert fatigue by tuning thresholds, using escalation policies, and ensuring every alert is actionable.

```yaml
# Prometheus alerting rule
groups:
  - name: http
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05
        for: 10m
        labels:
          severity: critical
```

**Q86: What is uptime monitoring and what tools are available?**
A: Uptime monitoring periodically checks if a service is reachable and响应s correctly. Tools include UptimeRobot, Checkly, BetterStack, and Prometheus Blackbox Exporter. Configure checks for HTTP status, response time, SSL certificate expiry, and content validation.

**Q87: How do you monitor containerized applications?**
A: Use `docker stats` for quick checks, cAdvisor for container metrics, Prometheus for scraping, and Grafana dashboards. In Kubernetes, use metrics-server, kube-state-metrics, and container-specific exporters. Monitor resource limits, OOM kills, restart counts, and network usage.

**Q88: What is the difference between monitoring and observability?**
A: Monitoring tells you *what* is broken (predefined dashboards, known metrics). Observability lets you ask *why* it's broken by providing rich, high-cardinality data (structured logs, traces, dimensions) that supports ad-hoc investigation of unknown issues.

---

## Application Maintenance (Q89–Q94)

**Q89: How does Sentry help with error tracking and debugging?**
A: Sentry captures exceptions with full stack traces, breadcrumbs (user actions before the error), environment context, and user info. It groups similar errors, tracks regression, and alerts on new issues. Integrate via SDK and configure source maps for minified code.

```python
import sentry_sdk
sentry_sdk.init(
    dsn="https://examplePublicKey@o0.ingest.sentry.io/0",
    traces_sample_rate=0.1,
)
```

**Q90: What are feature flags and how do you use them for safe deployments?**
A: Feature flags conditionally enable functionality without deploying new code. Use them to progressively roll out features, A/B test, and quickly disable broken features. Tools: LaunchDarkly, Unleash, Flagsmith, or custom config-based flags.

```python
if feature_flags.is_enabled("new_checkout_flow", user_id=user.id):
    return new_checkout(order)
else:
    return legacy_checkout(order)
```

**Q91: What is the expand-then-contract pattern for database migrations?**
A: Instead of modifying a column in place, use two migrations: **expand** (add new column, backfill data, update app to write to both) then **contract** (remove old column after all instances use the new one). This prevents downtime during rolling deployments.

**Q92: How do you maintain backward compatibility in APIs?**
A: Use versioning (`/v1/`, `/v2/`), deprecate fields gradually (return both old and new for a transition period), document changes, and never remove fields without a migration path. Use contract testing to catch breaking changes early.

**Q93: What is performance monitoring and how do you approach it?**
A: Track key metrics: response time (p50, p95, p99), throughput (requests/sec), error rate, CPU/memory usage, and database query times. Use APM tools (New Relic, Datadog, OpenTelemetry) to identify bottlenecks. Set performance budgets and regressions alerts.

**Q94: How do you handle application rollbacks in production?**
A: Fastest rollback: redeploy the previous Docker image tag or Kubernetes revision (`kubectl rollout undo`). Database rollbacks require backward-compatible migrations. For feature flags, disable the flag. Maintain runbooks for rollback procedures and test them regularly.

---

## Cloud Basics (Q95–Q98)

**Q95: What are the core AWS services and when would you use each?**
A: **EC2** — virtual machines for full control; **Lambda** — serverless functions for event-driven workloads; **S3** — object storage for files/assets; **ECS/Fargate** — container orchestration without managing servers; **RDS** — managed relational databases. Choose based on control vs. managed trade-offs.

**Q96: How do you deploy a web application to Vercel or Render?**
A: Both platforms offer Git-integrated deployment: push to `main` and they build/deploy automatically. Vercel is optimized for Next.js/frontend (edge functions, ISR). Render supports Docker, static sites, and databases. Configure environment variables, health checks, and custom domains through their dashboards or YAML config.

```yaml
# render.yaml
services:
  - type: web
    name: myapp
    runtime: docker
    dockerfilePath: Dockerfile
    envVars:
      - key: DATABASE_URL
        sync: false
```

**Q97: What are the key concepts of serverless computing?**
A: Serverless abstracts infrastructure management — you deploy functions/services and the platform handles scaling, patching, and provisioning. Key concepts: pay-per-invocation, auto-scaling (including to zero), event-driven triggers, cold starts, and statelessness (use external storage for state).

**Q98: How do you optimize cloud costs?**
A: Right-size instances (monitor actual usage), use reserved/spot instances for predictable workloads, auto-scale based on demand, delete unused resources (EBS volumes, idle load balancers), use S3 lifecycle policies, and set billing alerts. Review costs weekly using AWS Cost Explorer or equivalent.

---

## Software Reliability (Q99–Q100)

**Q99: What is blameless post-mortem and why does it matter?**
A: A blameless post-mortem focuses on systemic causes of incidents rather than individual blame. It documents timeline, impact, root cause, and actionable follow-ups (fixes, monitoring, process changes). This builds a learning culture, encourages reporting, and prevents repeated failures. Key principle: "How did the system allow this to happen?" not "Who caused this?"

**Q100: What is chaos engineering and how do you practice it?**
A: Chaos engineering deliberately injects failures (killed processes, network latency, resource exhaustion) into systems to verify they handle gracefully. Start with a hypothesis ("the system should survive X failure"), run the experiment in a controlled environment, observe, and fix weaknesses. Tools: Chaos Monkey (AWS), Litmus (Kubernetes), ToxiProxy (network). Begin in staging, never in production without safety guardrails.

```bash
# Example: inject CPU stress with stress-ng
stress-ng --cpu 4 --timeout 60s  # simulate CPU load
# Example: block traffic with tc
tc qdisc add dev eth0 root netem delay 200ms 50ms  # add latency
```
