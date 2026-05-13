# CI/CD Interview Questions and Answers

## Q1: What is CI/CD?
**A:** CI/CD stands for Continuous Integration and Continuous Delivery/Deployment. CI is the practice of automatically building and testing code changes frequently (often multiple times per day). CD automates deploying code to staging/production environments after passing CI checks.

## Q2: What is the difference between Continuous Delivery and Continuous Deployment?
**A:** Continuous Delivery means every change that passes CI is ready to be deployed to production but requires manual approval to trigger the deployment. Continuous Deployment automates the entire pipeline — every change that passes CI is automatically deployed to production without manual intervention.

## Q3: What are the key benefits of CI/CD?
**A:** Faster time to market, reduced manual errors, immediate feedback on code changes, consistent build and deployment processes, improved developer productivity, easier rollbacks, increased deployment frequency, and better code quality through automated testing.

## Q4: What is a CI/CD pipeline?
**A:** A CI/CD pipeline is an automated sequence of stages that code changes go through from commit to production. Typical stages include: source control checkout, build, unit tests, code quality analysis, integration tests, security scanning, artifact creation, staging deployment, acceptance tests, and production deployment.

## Q5: What is a build stage in CI/CD?
**A:** The build stage compiles source code into executable artifacts (binaries, packages, container images). It runs dependency installation, compilation, and produces deployable artifacts. A failed build stops the pipeline.

## Q6: What is the difference between unit tests and integration tests in CI/CD?
**A:** Unit tests test individual components in isolation (fast, no external dependencies). Integration tests verify that components work together correctly (may require databases, APIs, external services). Unit tests typically run first; integration tests run after a successful build.

## Q7: What is a test stage in a CI/CD pipeline?
**A:** The test stage executes automated tests against the built artifacts. It may include unit tests, integration tests, end-to-end tests, performance tests, and security tests. If tests fail, the pipeline stops and the team is notified.

## Q8: What is a deployment stage in CI/CD?
**A:** The deployment stage takes the tested artifacts and deploys them to a target environment (development, staging, production). It may involve updating servers, restarting services, running database migrations, configuring load balancers, or updating Kubernetes deployments.

## Q9: What is a "gate" in a CI/CD pipeline?
**A:** A gate is a checkpoint that must pass before the pipeline proceeds. Examples: manual approval, test coverage threshold, security scan pass, performance benchmark minimum, or compliance check. Gates prevent problematic code from reaching production.

## Q10: What is a "rollback" strategy in CI/CD?
**A:** Rollback reverts a deployment to a previous stable version. Strategies include: redeploying the previous artifact, using blue/green deployment (switch traffic back), using canary releases (gradually revert), database snapshot restore, or feature flags to disable problematic features.

## Q11: What is the difference between a CI server and a CI/CD tool?
**A:** A CI server (like Jenkins) is a self-hosted platform that runs builds and pipelines. A CI/CD tool (like GitHub Actions, GitLab CI) is often cloud-hosted and integrated with the source control platform. Modern tools blur this distinction.

## Q12: What is Jenkins?
**A:** Jenkins is an open-source automation server for building, testing, and deploying software. It supports hundreds of plugins, pipeline-as-code (Jenkinsfile), master/agent architecture, and integration with virtually every tool in the DevOps ecosystem.

## Q13: What is a Jenkinsfile?
**A:** A Jenkinsfile is a text file that defines a Jenkins pipeline as code. It can be written in Declarative (structured, easier) or Scripted (Groovy-based, more flexible) syntax. It is stored in the source repository alongside the application code.

## Q14: What is the difference between Declarative and Scripted Pipeline in Jenkins?
**A:** Declarative Pipeline uses a simpler, predefined structure with stages, steps, and agents. Scripted Pipeline uses Groovy for full flexibility but is more complex. Declarative is preferred for most use cases; Scripted is used when advanced logic is needed.

## Q15: What is a Jenkins agent?
**A:** A Jenkins agent (formerly slave) is a remote machine that executes pipeline jobs. The master (controller) schedules jobs on agents. Agents can have specific labels (e.g., "linux", "docker", "gpu") for targeting particular workloads.

## Q16: What is GitHub Actions?
**A:** GitHub Actions is GitHub's built-in CI/CD platform. Workflows are defined as YAML files in the `.github/workflows/` directory. It supports event-driven triggers, matrix builds, reusable workflows, self-hosted runners, and integration with the GitHub ecosystem.

## Q17: What is a GitHub Actions workflow?
**A:** A workflow is an automated process defined in YAML that runs on GitHub's runners. It is triggered by events (push, pull_request, schedule, workflow_dispatch). Workflows consist of jobs (run on runners) and steps (individual commands or actions).

## Q18: What is a GitHub Actions job vs step?
**A:** A job is a set of steps that execute on the same runner. Jobs run in parallel by default but can be sequenced with `needs`. A step is an individual task (run a command or use an action) within a job.

## Q19: What is a GitHub Actions runner?
**A:** A runner is a server that executes GitHub Actions workflows. GitHub-hosted runners (Ubuntu, Windows, macOS) are maintained by GitHub. Self-hosted runners are machines you manage, useful for custom hardware or internal network access.

## Q20: What is GitLab CI/CD?
**A:** GitLab CI/CD is GitLab's integrated CI/CD platform. Pipelines are defined in `.gitlab-ci.yml` files. It offers auto DevOps, container registry, artifact management, environments, and review apps. It is deeply integrated with GitLab repositories.

## Q21: What is a `.gitlab-ci.yml` file?
**A:** `.gitlab-ci.yml` is the YAML configuration file for GitLab CI/CD pipelines. It defines stages, jobs, scripts, dependencies, and rules. It is stored in the root of the repository and is automatically detected by GitLab.

## Q22: What is a GitLab runner?
**A:** A GitLab runner is an agent that executes GitLab CI/CD jobs. Runners can be shared (across projects), group-specific, or project-specific. They execute on various executors: shell, Docker, Kubernetes, SSH, VirtualBox, etc.

## Q23: What are GitLab CI/CD environments?
**A:** Environments in GitLab CI/CD represent deployment targets (staging, production). They track deployments, provide history, and enable rollbacks. Review apps create temporary environments for each merge request, enabling preview of changes.

## Q24: What is CircleCI?
**A:** CircleCI is a cloud-based CI/CD platform known for its speed and simplicity. It uses `.circleci/config.yml` for pipeline configuration, supports Docker, machine, and macOS executors, caching, workspaces, orbs (reusable config packages), and parallel job execution.

## Q25: What is a CircleCI orb?
**A:** An orb is a reusable package of CircleCI configuration — jobs, commands, and executors. Orbs simplify CI/CD setup by providing pre-built integrations with AWS, Docker, Slack, testing frameworks, and more. They are versioned and shared in the CircleCI registry.

## Q26: What is Travis CI?
**A:** Travis CI was one of the first cloud CI services, closely integrated with GitHub. It uses `.travis.yml` for configuration, supports matrix builds, multiple languages, and deployment to various cloud providers. It has largely been superseded by GitHub Actions.

## Q27: What is a build artifact?
**A:** A build artifact is a file or directory produced by a build stage that is needed in later stages or for deployment. Examples: compiled binaries, JAR files, Docker images, Python wheels, npm packages, or ZIP archives. Artifacts are passed between stages or stored for release.

## Q28: What is artifact caching in CI/CD?
**A:** Caching stores frequently used files (dependency directories, compiled libraries) between pipeline runs to speed up builds. Unlike artifacts (which are outputs), caches are not guaranteed to exist. Common caches: `.m2/repository` (Maven), `node_modules/`, `vendor/bundle` (Ruby), `~/.cache/pip`.

## Q29: What is the difference between artifacts and cache in CI/CD?
**A:** Artifacts are outputs of a job that are passed to subsequent jobs or stored for download. They are essential for the pipeline. Caches are optional performance optimizations that store dependencies to speed up future runs. Caches can be deleted or invalidated without breaking the pipeline.

## Q30: What is pipeline-as-code?
**A:** Pipeline-as-code treats CI/CD pipeline configuration as source code stored in the repository (e.g., `Jenkinsfile`, `.gitlab-ci.yml`, `.github/workflows/`). Benefits include version control, code review, reproducibility, and standardization across teams.

## Q31: What is a merge request/pull request pipeline?
**A:** A merge request (GitLab) or pull request (GitHub) pipeline automatically runs when a merge/pull request is opened or updated. It builds and tests the proposed changes before merging. Status checks can block merging if the pipeline fails.

## Q32: What is a trunk-based development?
**A:** Trunk-based development is a branching model where developers integrate small, frequent changes directly into a shared main branch (trunk). Feature branches are short-lived (hours to days). It enables CI by keeping the main branch always deployable.

## Q33: What is GitFlow?
**A:** GitFlow is a branching model with `main`, `develop`, `feature`, `release`, and `hotfix` branches. It is suited for projects with scheduled releases. It can conflict with CI/CD goals because feature branches may live for weeks before merging.

## Q34: How do you handle database migrations in CI/CD?
**A:** Database migrations are executed as part of the deployment stage. Strategies include: (1) run migrations before new code starts, (2) backward-compatible changes only (add columns before removing), (3) use expansion/contraction pattern, (4) migrate in a separate job before deployment, (5) test migrations against a copy of production data.

## Q35: What is blue/green deployment?
**A:** Blue/green deployment runs two identical environments (blue = current, green = new). Traffic is switched from blue to green once green is verified. This enables zero-downtime deployments and instant rollbacks (just switch traffic back).

## Q36: What is a canary deployment?
**A:** Canary deployment routes a small percentage of traffic to the new version while serving most users with the old version. If the canary is healthy, traffic is gradually increased to 100%. This minimizes risk by detecting issues early with minimal user impact.

## Q37: What is a rolling deployment?
**A:** Rolling deployment gradually replaces instances of the old version with the new version one by one (or batch by batch). A load balancer directs traffic away from instances being updated. It provides zero-downtime updates with limited resource overhead.

## Q38: What is the difference between blue/green and rolling deployment?
**A:** Blue/green requires double the infrastructure (two full environments) but provides instant rollback. Rolling uses existing capacity (no extra infrastructure) but rollback takes time and may be slower to complete. Blue/green is simpler for stateful applications.

## Q39: What is a feature flag (feature toggle)?
**A:** A feature flag is a conditional statement in code that enables or disables functionality at runtime without deploying new code. Flags enable trunk-based development, canary releases, A/B testing, and quick rollback of features without redeployment.

## Q40: How do feature flags relate to CI/CD?
**A:** Feature flags decouple deployment from release. Code can be deployed to production behind a disabled flag and activated later without a new deployment. This reduces deployment risk and enables faster deployment cycles.

## Q41: What is a webhook in CI/CD?
**A:** A webhook is an HTTP callback triggered by an event (e.g., push to repository, pull request opened). The CI/CD tool listens for webhooks to automatically trigger pipeline runs. Webhooks enable event-driven automation between tools.

## Q42: What is a CI/CD trigger?
**A:** A trigger starts a pipeline or job. Triggers can be automatic (webhook on push, schedule) or manual (button click, API call). Multi-branch pipelines trigger on branch creation. Pipeline triggers can also be invoked by other pipelines.

## Q43: What is environment promotion in CI/CD?
**A:** Environment promotion moves a build artifact through successive environments (dev -> staging -> production) with gates at each stage. Each promotion runs environment-specific tests (e.g., smoke tests in staging, load tests before production).

## Q44: How do you handle secrets in CI/CD pipelines?
**A:** Secrets (API keys, passwords, tokens) should never be hardcoded in pipeline config. Use the CI/CD tool's secret management (GitHub secrets, GitLab CI variables, Jenkins credentials). Secrets are injected as environment variables or mounted files, masked in logs.

## Q45: What is a service container in CI/CD?
**A:** A service container is a dependent service (database, Redis, message queue) that runs alongside the build container for integration tests. Example: in GitHub Actions, you can define a `services:` block with `postgres:latest` for testing database interactions.

## Q46: What is matrix testing in CI/CD?
**A:** Matrix (or parallel) testing runs the same tests across multiple configurations (e.g., different OS versions, language versions, dependency versions) simultaneously. Example: test on Ubuntu 20.04, 22.04 with Python 3.9, 3.10, 3.11.

## Q47: What is a self-hosted runner?
**A:** A self-hosted runner is a CI/CD agent that you install and manage on your own infrastructure. Benefits: control over hardware, access to internal networks, no usage limits, custom configurations. Drawbacks: maintenance overhead, security responsibility.

## Q48: What is the difference between a shared and a specific runner (GitLab)?
**A:** Shared runners are available to all projects in a GitLab instance (managed by administrators). Specific runners are assigned to a particular project or group. Shared runners are convenient; specific runners offer isolation and dedicated resources.

## Q49: What is a pipeline schedule?
**A:** A pipeline schedule runs a CI/CD pipeline at specified intervals (cron-like). Common uses: nightly builds, regular security scans, database maintenance, report generation, or testing against external dependencies.

## Q50: How do you handle monorepos in CI/CD?
**A:** Monorepo strategies: (1) use path filters to only build/test changed projects, (2) use dependency graph analysis to determine affected projects, (3) use build tools like Nx, Turborepo, Bazel for incremental builds, (4) split pipelines per project within the monorepo.

## Q51: What is a Docker-based CI/CD pipeline?
**A:** A Docker-based pipeline runs each step or stage in a Docker container. Benefits: consistent environment, isolated dependencies, easy tooling management, reproducible builds. Each job specifies a Docker image (e.g., `node:18`, `python:3.11`, `custom:latest`).

## Q52: What is a Kubernetes-based CI/CD pipeline?
**A:** A Kubernetes-based pipeline runs CI/CD jobs as pods on a Kubernetes cluster. Tools like Jenkins X, Tekton, Argo Workflows, and GitLab CI with Kubernetes executor leverage Kubernetes for dynamic resource allocation, scaling, and isolation.

## Q53: What is Tekton?
**A:** Tekton is a Kubernetes-native CI/CD framework. It defines pipelines, tasks, and their steps as Kubernetes CRDs (Custom Resource Definitions). It is cloud-native, portable across Kubernetes clusters, and integrates with the wider Kubernetes ecosystem.

## Q54: What is Argo CD?
**A:** Argo CD is a declarative, GitOps continuous delivery tool for Kubernetes. It synchronizes the cluster state with the desired state defined in a Git repository. It provides automated deployment, drift detection, rollback, and visibility into cluster state.

## Q55: What is GitOps?
**A:** GitOps is a deployment pattern where Git is the single source of truth for declarative infrastructure and application configurations. A GitOps operator (like Argo CD or Flux) continuously reconciles the actual environment state with the Git-defined desired state.

## Q56: What is the difference between GitOps and traditional CI/CD?
**A:** Traditional CI/CD pushes artifacts to environments (push model). GitOps pulls desired state from Git (pull model). GitOps provides better audit trails, easier rollbacks (revert Git commit), and automatic drift detection.

## Q57: What is a pipeline failure, and how do you handle it?
**A:** A pipeline failure occurs when any stage (build, test, deploy) fails. Handling: (1) notify the team (Slack, email), (2) analyze logs to identify the cause, (3) fix the code or configuration, (4) retry the pipeline (or specific stage), (5) implement retry logic for flaky tests.

## Q58: What is a flaky test, and how should it be handled in CI/CD?
**A:** A flaky test passes or fails non-deterministically (due to timing, ordering, race conditions). It should be quarantined (not blocking the pipeline) and tracked for resolution. Never ignore flaky tests — they erode trust in the CI pipeline.

## Q59: How do you measure CI/CD pipeline effectiveness?
**A:** Key metrics: deployment frequency, lead time for changes, mean time to recovery (MTTR), change failure rate (DORA metrics). Additional metrics: build time, test coverage, pipeline pass rate, time from commit to production, and developer satisfaction.

## Q60: What are DORA metrics?
**A:** DORA (DevOps Research and Assessment) metrics are four key DevOps performance indicators: Deployment Frequency (how often deployments happen), Lead Time for Changes (time from commit to production), Change Failure Rate (percentage of failed deployments), and Mean Time to Recovery (time to recover from failures).

## Q61: What is the difference between `git push` triggering a CI build vs a scheduled build?
**A:** A push-triggered build runs immediately when code is pushed, providing fast feedback to developers. A scheduled build (e.g., daily) runs regardless of code changes, useful for dependency updates, long-running tests, or compliance checks.

## Q62: How do you handle multiple environments (dev, staging, prod) in CI/CD?
**A:** Define separate deployment jobs/stages for each environment. Use environment-specific variables or variable groups. Promote artifacts through environments with gates (manual approval for production). Use branch-based triggers (e.g., `main` -> staging, tag `v*` -> production).

## Q63: What is a conditional stage in a pipeline?
**A:** A conditional stage only runs when certain conditions are met. Examples: run deployment only on `main` branch, run security scan only on pull requests, run performance tests only for release tags, run cleanup only on failure.

## Q64: How do you secure a CI/CD pipeline?
**A:** (1) Never hardcode secrets, (2) Limit who can modify pipeline configuration, (3) Restrict runner permissions, (4) Scan third-party actions/orbs before use, (5) Sign commits and artifacts, (6) Use immutable build tags, (7) Implement approval gates for production, (8) Audit pipeline access.

## Q65: What is supply chain security in CI/CD?
**A:** Supply chain security ensures the integrity of dependencies and tools used in the pipeline. Practices: (1) pin dependency versions, (2) verify checksums, (3) scan for vulnerabilities (Snyk, Dependabot), (4) sign artifacts (Sigstore, cosign), (5) use SBOMs (Software Bill of Materials).

## Q66: What is a Software Bill of Materials (SBOM)?
**A:** An SBOM is a formal record of all components, libraries, and dependencies in a software artifact. It includes versions, licenses, and vulnerability information. CI/CD pipelines can generate SBOMs (e.g., with Syft, Trivy) and integrate with security scanning.

## Q67: What is SLSA (Supply-chain Levels for Software Artifacts)?
**A:** SLSA is a security framework for ensuring software supply chain integrity. It defines levels (SLSA 1-4) based on build integrity, provenance, and reproducibility. CI/CD pipelines can be hardened to achieve higher SLSA levels.

## Q68: What is Cosign?
**A:** Cosign is a tool for signing and verifying container images and blobs. It integrates with CI/CD pipelines to sign artifacts at build time and verify them at deployment time. It supports keyless signing via Sigstore, using OIDC identity.

## Q69: What is the difference between `git tag` and `git branch` in the context of CI/CD?
**A:** Git tags (e.g., `v1.2.3`) are typically used for releases — CI/CD pipelines triggered by tags often deploy to production. Git branches are for ongoing development — different branches map to different environments (feature -> dev, main -> staging).

## Q70: How do you implement approval gates in CI/CD?
**A:** Approval gates require manual sign-off before proceeding. In GitHub Actions, use `environment` with required reviewers. In GitLab, use `manual` jobs with `when: manual`. In Jenkins, use `input` step in Declarative Pipeline. In Azure DevOps, use release approvals.

## Q71: What is a time-based deployment gate?
**A:** A time-based gate restricts deployment to specific windows (e.g., only deploy on weekdays 9 AM - 5 PM, not on holidays, not during blackout periods). This reduces risk by avoiding deployments during peak traffic or when fewer team members are available.

## Q72: What is infrastructure-as-code (IaC) and its role in CI/CD?
**A:** IaC manages infrastructure (servers, networks, databases) through configuration files (Terraform, CloudFormation, Ansible). In CI/CD: (1) validate IaC in pipelines, (2) provision environments automatically, (3) test infrastructure changes, (4) achieve reproducible deployments.

## Q73: What is Terraform in CI/CD?
**A:** Terraform is an IaC tool for provisioning infrastructure. In CI/CD: run `terraform plan` in pull requests (review changes), `terraform apply` in deployment pipelines. Use state locking (S3, DynamoDB) and remote state storage for team collaboration.

## Q74: What is Ansible in CI/CD?
**A:** Ansible is an IT automation tool for configuration management and application deployment. In CI/CD: Ansible playbooks can be triggered from pipelines to configure servers, deploy applications, and orchestrate multi-tier deployments.

## Q75: How do you handle zero-downtime deployments?
**A:** Strategies: (1) blue/green deployment, (2) rolling deployment, (3) canary deployment, (4) feature flags to disable problematic features. All require load balancers, health checks, and graceful shutdown handling.

## Q76: What is health check in the context of deployments?
**A:** A health check verifies that an application instance is running and ready to serve traffic. Types: startup probe (has the app started?), liveness probe (is it running?), readiness probe (can it accept traffic?). CI/CD waits for health checks before routing traffic.

## Q77: What is a smoke test?
**A:** A smoke test is a minimal set of tests run after deployment to verify that the application starts correctly and critical functionality works. It catches obvious failures (wrong config, missing dependencies) quickly before running a full test suite.

## Q78: What is a regression test in CI/CD?
**A:** Regression tests verify that new changes do not break existing functionality. They are typically automated and run as part of the test stage. High regression test coverage is essential for frequent deployments.

## Q79: What is the difference between a smoke test and a sanity test?
**A:** Smoke tests verify that the build is stable enough for further testing (checking critical paths). Sanity tests verify that specific functionality works after minor changes. The terms are often used interchangeably.

## Q80: What is a performance test in CI/CD?
**A:** Performance tests verify that the application meets performance requirements (response time, throughput, resource usage). Examples: load tests, stress tests, endurance tests, spike tests. They are often run in staging environments before production deployment.

## Q81: What is a security scan in CI/CD?
**A:** Security scans detect vulnerabilities in code, dependencies, and configurations. Types: SAST (Static Application Security Testing) analyzes source code, DAST (Dynamic Application Security Testing) tests running applications, dependency scanning checks libraries, container scanning checks images.

## Q82: What is SAST vs DAST?
**A:** SAST (Static Analysis Security Testing) scans source code for vulnerabilities without executing it (white-box, early in pipeline). DAST (Dynamic Analysis Security Testing) tests running applications for vulnerabilities (black-box, later in pipeline). Both are complementary.

## Q83: What is container scanning in CI/CD?
**A:** Container scanning (e.g., Trivy, Clair, Snyk) checks Docker images for vulnerabilities in the base OS packages and application dependencies. It should run after the image is built and before it is pushed or deployed. Failing scans should block deployment.

## Q84: What is Dependency Check in CI/CD?
**A:** Dependency checking (OWASP Dependency-Check, Dependabot, Renovate) identifies known vulnerabilities in project dependencies. It compares dependency versions against CVE (Common Vulnerabilities and Exposures) databases and reports or fails the pipeline.

## Q85: How do you handle concurrency in CI/CD pipelines?
**A:** Concurrency control prevents multiple runs of the same pipeline from interfering. Strategies: (1) cancel in-progress runs when a new commit is pushed, (2) group deployments to prevent simultaneous deploys, (3) use resource locks for shared infrastructure.

## Q86: What is a `concurrency` group in GitHub Actions?
**A:** `concurrency` ensures that only one workflow run per group runs at a time. If a new run is triggered, any in-progress run in the same group is cancelled or waits. Example: `concurrency: deploy-production` prevents simultaneous production deployments.

## Q87: How do you set up a CI/CD pipeline for a mobile app?
**A:** Mobile CI/CD includes: (1) build for multiple platforms (iOS, Android), (2) run unit/integration tests on emulators/simulators, (3) code signing, (4) distribute to beta testers (TestFlight, Firebase App Distribution), (5) submit to App Store/Google Play.

## Q88: How do you set up a CI/CD pipeline for a microservices architecture?
**A:** Each microservice has its own CI/CD pipeline. Strategies: (1) independently deployable services, (2) API contract testing between services, (3) integration test suite for service interactions, (4) shared CI/CD templates, (5) orchestration service for multi-service deployments.

## Q89: What is a release pipeline vs a build pipeline?
**A:** A build pipeline creates and tests artifacts. A release pipeline takes those artifacts and deploys them to environments with approval gates and environment-specific configurations. They are often combined in modern CI/CD (single pipeline with stages).

## Q90: How do you manage configuration for different environments in CI/CD?
**A:** (1) Environment-specific variables (stored in the CI/CD tool), (2) Configuration files per environment selected during deployment, (3) External config services (Consul, Vault), (4) Kubernetes ConfigMaps/Secrets, (5) Environment variable substitution in deployment scripts.

## Q91: What is a canary release vs A/B testing?
**A:** Canary release tests a new version for stability with a subset of users (gradual rollout). A/B testing compares two versions to measure business metrics (conversion, engagement). Canary is about risk reduction; A/B is about feature validation. They can be combined.

## Q92: What is immutable infrastructure, and how does it relate to CI/CD?
**A:** Immutable infrastructure means servers/containers are never modified after deployment — they are replaced entirely for updates. CI/CD builds new images/AMIs for every deployment and replaces instances. This eliminates configuration drift and simplifies rollbacks.

## Q93: What is the "shift left" principle in CI/CD?
**A:** Shift left means moving testing and quality checks earlier in the development lifecycle. In CI/CD: run linting, unit tests, and security scans early (during commit/PR) rather than later (during deployment). Catching issues earlier reduces cost and effort.

## Q94: How do you implement versioning in CI/CD?
**A:** Versioning strategies: (1) semantic versioning (major.minor.patch) from git tags, (2) commit hash-based (automatic, unique), (3) datetime-based, (4) build number. Use CI/CD variables to generate and propagate versions throughout the pipeline.

## Q95: How do you create a release in CI/CD?
**A:** Release process: (1) create a git tag with version, (2) CI pipeline builds and tests the tagged commit, (3) create release artifact (binary, Docker image, package), (4) publish to registry (Docker Hub, npm, PyPI), (5) create GitHub/GitLab release with changelog, (6) deploy to production.

## Q96: What is a changelog, and how do you automate it?
**A:** A changelog documents notable changes per release. Automated generation tools (git-cliff, semantic-release, conventional-changelog) parse commit messages following Conventional Commits format. CI/CD can generate and publish changelogs during the release process.

## Q97: What are Conventional Commits?
**A:** Conventional Commits is a specification for structured commit messages: `type(scope): description` where type is `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, etc. It enables automated changelog generation, semantic versioning, and CI/CD triggers based on commit types.

## Q98: What is the difference between `git tag` and `git describe` in CI/CD?
**A:** `git tag` marks a specific commit with a human-readable name (e.g., `v1.0.0`). `git describe` generates a human-readable name from the nearest tag (e.g., `v1.0.0-3-gabc123`), useful for versioning pre-release builds.

## Q99: How do you debug a failed CI/CD pipeline?
**A:** (1) Check pipeline logs for error messages, (2) Re-run with debug mode (e.g., `ACTIONS_STEP_DEBUG=true`), (3) SSH into runner for live debugging, (4) Compare successful vs failed runs, (5) Check environment differences, (6) Run the same steps locally.

## Q100: What is the future of CI/CD?
**A:** Trends: (1) AI/ML for intelligent pipeline optimization and failure prediction, (2) GitOps for unified deployment, (3) Service mesh integration for safe deployments, (4) Supply chain security (SBOM, SLSA), (5) Environment as a Service (ephemeral environments), (6) Low-code pipeline builders for non-dev teams.
