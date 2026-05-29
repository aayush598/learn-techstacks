# Section 03: Dependency Vulnerability Scanning

Dependency vulnerability scanning automatically detects known vulnerabilities in third-party libraries and frameworks. The scan runs on every code commit and pull request, preventing vulnerable dependencies from reaching production. The system monitors the dependency graph: direct dependencies and their transitive dependencies.

Scanning tools: npm audit / yarn audit (JavaScript), pip-audit / safety (Python), cargo audit (Rust), go vulnerability check (Go), Trivy (containers), and Snyk / GitHub Dependabot (cross-language). Each tool is integrated into the CI/CD pipeline. The scan checks against the National Vulnerability Database (NVD), GitHub Advisory Database, and other vulnerability feeds.

Scan results: each dependency is reported with name, version, CVE ID, CVSS score, fixed version (if available), and affected path (direct or transitive). Blocking policy: critical vulnerabilities block the build; high vulnerabilities require manual review before merge; medium and low are reported as warnings. The dependency dashboard shows the health of each repository and tracks remediation velocity.
