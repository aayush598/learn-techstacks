# Self-Service Security Testing for Solo Founders

## Penetration Testing on a Solo Budget

Professional penetration testing costs $5,000-50,000 per engagement. As a solo founder, you can't afford that. But you can run much of the same testing yourself using automated tools, following the same methodology professional testers use.

This guide covers how to perform security testing on your own SaaS product using free and low-cost tools, following a structured pentest methodology.

## The Solo Pentest Methodology

### What You're Testing For

```markdown
The OWASP Top 10 (2021):
1. Broken Access Control
2. Cryptographic Failures
3. Injection (SQL, XSS, Command)
4. Insecure Design
5. Security Misconfiguration
6. Vulnerable and Outdated Components
7. Identification and Authentication Failures
8. Software and Data Integrity Failures
9. Security Logging and Monitoring Failures
10. Server-Side Request Forgery (SSRF)

Your focus as a solo founder:
  - #1, #3, #5, #7 are the most common in SaaS apps
  - #2, #6 are easy to check with automated tools
  - #8, #10 are less common but important
```

### The Testing Process

```
1. Reconnaissance
   - Map attack surface
   - Identify all endpoints
   - Discover subdomains

2. Automated Scanning
   - Run vulnerability scanners
   - Check for common misconfigurations
   - Audit dependencies

3. Manual Testing
   - Test authentication
   - Test authorization (IDOR)
   - Test input validation (XSS, SQLi)
   - Test business logic flaws

4. Reporting
   - Document findings
   - Prioritize by severity
   - Plan remediation
```

## Automated Security Tools

### Tool Stack for Solo Founders

```markdown
Tool                    | Cost        | Purpose                    | Effort
------------------------|-------------|----------------------------|--------
OWASP ZAP              | Free        | Web app vulnerability scan | Medium
Burp Suite (Community)  | Free        | Web app security testing   | High
Nuclei                 | Free        | Template-based scanning    | Low
SQLmap                 | Free        | SQL injection detection    | Medium
Nikto                  | Free        | Web server scanner         | Low
WPScan                 | Free        | WordPress scanner          | Low
Trivy                  | Free        | Container vulnerability    | Low
Snyk                   | Free tier   | Dependency vulnerability   | Low
sslscan               | Free        | SSL/TLS configuration     | Low
Subfinder              | Free        | Subdomain discovery       | Low
httpx                  | Free        | Web probe                 | Low
```

### Running OWASP ZAP (Most Comprehensive Free Scanner)

```bash
#!/bin/bash
# scripts/security-scan.sh
# Run OWASP ZAP automated scan

set -euo pipefail

TARGET_URL=${1:-"https://mysaas.com"}
ZAP_DIR="./security-reports"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_DIR="${ZAP_DIR}/zap_${TIMESTAMP}"

mkdir -p $REPORT_DIR

echo "Starting OWASP ZAP scan against $TARGET_URL"

# Pull and run ZAP in headless mode
docker run --rm -v ${PWD}/${REPORT_DIR}:/zap/wrk:rw \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-full-scan.py \
  -t $TARGET_URL \
  -r zap_report.html \
  -w zap_report.md \
  -J zap_report.json \
  -x zap_report.xml \
  -I \
  -d

echo "ZAP scan complete! Reports in $REPORT_DIR"

# Check for high/critical findings
HIGH_COUNT=$(cat ${REPORT_DIR}/zap_report.json | jq '.site[0].alerts[] | select(.riskcode == "2" or .riskcode == "3") | .count' | paste -s -d+ | bc)

echo "High/Critical findings: $HIGH_COUNT"

if [ "$HIGH_COUNT" -gt "0" ]; then
  echo "⚠️  Found $HIGH_COUNT high/critical issues!"
  echo "Review reports in $REPORT_DIR"
fi
```

### Running Nuclei (Fast, Template-Based Scanning)

```bash
#!/bin/bash
# scripts/nuclei-scan.sh

TARGET_URL=${1:-"https://mysaas.com"}

echo "Running Nuclei scan against $TARGET_URL"

# Install nuclei if not present
if ! command -v nuclei &> /dev/null; then
  go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
fi

# Update templates
nuclei -update-templates

# Run scan
nuclei -u $TARGET_URL \
  -severity critical,high,medium \
  -o nuclei_results.txt \
  -json -o nuclei_results.json \
  -rate-limit 50 \
  -concurrency 10

echo "Nuclei scan complete! Results in nuclei_results.txt"

# Display findings
if [ -f nuclei_results.txt ]; then
  echo "Findings:"
  cat nuclei_results.txt
fi
```

## Automated Scanning Pipeline

### CI/CD Security Scanning

```yaml
# .github/workflows/security-scan.yml
name: Security Scan

on:
  schedule:
    - cron: '0 6 * * 1'  # Every Monday at 6 AM
  workflow_dispatch: # Manual trigger

jobs:
  dependency-scan:
    name: Dependency Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Run npm audit
        run: npm audit --audit-level=high
        continue-on-error: true

      - name: Run Snyk scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high
        continue-on-error: true

  secret-scan:
    name: Secret Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  container-scan:
    name: Container Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build Docker image
        run: docker build -t app:latest .

      - name: Run Trivy scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'app:latest'
          format: 'table'
          exit-code: '1'
          severity: 'CRITICAL,HIGH'
```

## Manual Security Testing

### Testing Authentication

```markdown
## Authentication Test Cases

### 1. Password Security
[ ] Minimum password length enforced (8+ chars)
[ ] Common passwords rejected
[ ] Password complexity enforced
[ ] Passwords stored as bcrypt/argon2 hash
[ ] Password change requires old password
[ ] Password reset requires token (not just email)
[ ] Reset tokens expire (15-60 minutes)

### 2. Login Security
[ ] Rate limiting on login endpoint
[ ] Account lockout after failed attempts
[ ] "Remember me" tokens expire properly
[ ] Session token is random and unpredictable
[ ] Session expires after inactivity
[ ] Logout invalidates session
[ ] Concurrent sessions limited

### 3. MFA/2FA
[ ] MFA can be enabled
[ ] MFA is required for admin actions
[ ] Backup codes provided for MFA recovery
[ ] SMS/email OTPs expire quickly

### 4. Token Security
[ ] JWT tokens signed with strong algorithm
[ ] JWT expiry time is reasonable (15 min for access)
[ ] Refresh tokens are long-lived but revocable
[ ] Tokens are stored in HTTP-only cookies (not localStorage)
[ ] CSRF tokens for state-changing requests
```

#### Manual Auth Testing Script

```bash
#!/bin/bash
# scripts/test-auth.sh
# Manually test authentication endpoints

BASE_URL=${1:-"https://mysaas.com"}

echo "=== Auth Security Tests ==="

# Test 1: Rate limiting
echo "Test 1: Rate limiting..."
for i in {1..10}; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST "$BASE_URL/api/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"email":"test@test.com","password":"wrong"}')
  echo "Attempt $i: $STATUS"
done

# Test 2: Password requirements
echo -e "\nTest 2: Weak password..."
RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"123"}')
echo "Short password: $RESPONSE"

# Test 3: SQL injection attempt
echo -e "\nTest 3: SQL injection..."
RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"\" OR 1=1 --"}')
echo "SQL injection: $RESPONSE"

# Test 4: XSS attempt
echo -e "\nTest 4: XSS in input..."
RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{"email":"<script>alert(1)</script>@test.com","password":"Test1234!"}')
echo "XSS attempt: $RESPONSE"
```

### Testing Authorization (IDOR)

```markdown
## Authorization Test Cases

### Insecure Direct Object Reference (IDOR) Tests
[ ] Can user A access user B's data by changing IDs?
[ ] Can user A modify user B's data?
[ ] Can user A delete user B's data?
[ ] Can user A access admin endpoints?
[ ] Can user A access other tenant's data?
[ ] Can unauthenticated user access authenticated endpoints?

### Role-Based Access Control Tests
[ ] Can regular user access admin API?
[ ] Can regular user access admin UI?
[ ] Can regular user perform admin actions?
[ ] Are permissions checked server-side (not just UI)?
[ ] Is tenant isolation enforced?
```

#### IDOR Testing Script

```bash
#!/bin/bash
# scripts/test-idor.sh
# Test for Insecure Direct Object Reference

BASE_URL=${1:-"https://mysaas.com"}
AUTH_TOKEN=${2:-"user-jwt-token-here"}

echo "=== IDOR Tests ==="

# Test 1: Access other user's profile
echo "Test 1: Access other user's data..."
for USER_ID in "00000000-0000-0000-0000-000000000001" \
               "00000000-0000-0000-0000-000000000002" \
               "admin"; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: Bearer $AUTH_TOKEN" \
    "$BASE_URL/api/users/$USER_ID")
  echo "  User $USER_ID: $STATUS (expect 403 or 404)"
done

# Test 2: Access admin endpoints
echo -e "\nTest 2: Admin endpoints..."
for ENDPOINT in "/api/admin/users" \
                "/api/admin/settings" \
                "/admin/dashboard" \
                "/api/admin/logs"; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: Bearer $AUTH_TOKEN" \
    "$BASE_URL$ENDPOINT")
  echo "  $ENDPOINT: $STATUS (expect 403)"
done

# Test 3: Access other tenant's projects
echo -e "\nTest 3: Tenant isolation..."
for TENANT_ID in "tenant-001" "tenant-002" "tenant-003"; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: Bearer $AUTH_TOKEN" \
    -H "X-Tenant-ID: $TENANT_ID" \
    "$BASE_URL/api/projects")
  echo "  Tenant $TENANT_ID: $STATUS (expect 403 if not your tenant)"
done
```

### Testing Input Validation

```bash
#!/bin/bash
# scripts/test-input-validation.sh

BASE_URL=${1:-"https://mysaas.com"}

echo "=== Input Validation Tests ==="

# XSS Payloads
echo "Test 1: XSS payloads..."
XSS_PAYLOADS=(
  "<script>alert(1)</script>"
  "<img src=x onerror=alert(1)>"
  "<svg onload=alert(1)>"
  "javascript:alert(1)"
  "\"><script>alert(1)</script>"
  "';alert(1)//"
)

for payload in "${XSS_PAYLOADS[@]}"; do
  RESPONSE=$(curl -s "$BASE_URL/api/v1/search?q=$payload" \
    -H "Authorization: Bearer $AUTH_TOKEN")
  if echo "$RESPONSE" | grep -qi "script\|alert\|<\|>"; then
    echo "  ⚠️  XSS might be possible with: $payload"
  fi
done

# SQL Injection Payloads
echo -e "\nTest 2: SQL injection..."
SQLI_PAYLOADS=(
  "' OR '1'='1"
  "' UNION SELECT * FROM users--"
  "'; DROP TABLE users--"
  "1; SELECT * FROM users"
  "' OR 1=1--"
)

for payload in "${SQLI_PAYLOADS[@]}"; do
  RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
    "$BASE_URL/api/users?search=$payload" \
    -H "Authorization: Bearer $AUTH_TOKEN")
  # If it returns 200 instead of 400/500, SQLi might be possible
  if [ "$RESPONSE" == "200" ]; then
    echo "  ⚠️  SQLi might be possible with: $payload (got 200)"
  fi
done

# Path Traversal
echo -e "\nTest 3: Path traversal..."
TRAVERSAL_PAYLOADS=(
  "../../../etc/passwd"
  "..\..\..\windows\win.ini"
  "%2e%2e%2f%2e%2e%2fetc/passwd"
  "....//....//....//etc/passwd"
)

for payload in "${TRAVERSAL_PAYLOADS[@]}"; do
  RESPONSE=$(curl -s "$BASE_URL/api/files/download?path=$payload" \
    -H "Authorization: Bearer $AUTH_TOKEN")
  if echo "$RESPONSE" | grep -qi "root:\|\[extensions\]"; then
    echo "  ⚠️  Path traversal possible with: $payload"
  fi
done
```

## Web Security Headers Check

```bash
#!/bin/bash
# scripts/check-headers.sh

TARGET_URL=${1:-"https://mysaas.com"}

echo "=== Security Headers Check ==="

# Get headers
HEADERS=$(curl -sI $TARGET_URL)

declare -A REQUIRED_HEADERS=(
  ["Strict-Transport-Security"]="HSTS not set"
  ["X-Content-Type-Options"]="Prevents MIME sniffing"
  ["X-Frame-Options"]="Prevents clickjacking"
  ["Content-Security-Policy"]="CSP not set"
  ["X-XSS-Protection"]="XSS filter not enabled"
  ["Referrer-Policy"]="Referrer policy not set"
  ["Permissions-Policy"]="Permissions policy not set"
)

for header in "${!REQUIRED_HEADERS[@]}"; do
  if echo "$HEADERS" | grep -qi "^$header:"; then
    VALUE=$(echo "$HEADERS" | grep -i "^$header:" | head -1)
    echo "✅ $header: $VALUE"
  else
    echo "❌ $header — ${REQUIRED_HEADERS[$header]}"
  fi
done

# Check HTTPS
echo -e "\nTLS Check:"
TLS_VERSION=$(echo | openssl s_client -connect $(echo $TARGET_URL | sed 's|https://||'):443 \
  -servername $(echo $TARGET_URL | sed 's|https://||') 2>/dev/null | \
  grep "Protocol" | head -1)
echo "$TLS_VERSION"

# Check for information disclosure
echo -e "\nInformation Disclosure:"
X_POWERED_BY=$(echo "$HEADERS" | grep -i "^X-Powered-By" || echo "Not disclosed ✅")
echo "X-Powered-By: $X_POWERED_BY"

SERVER=$(echo "$HEADERS" | grep -i "^Server" || echo "Not disclosed ✅")
echo "Server: $SERVER"
```

## SSL/TLS Configuration Check

```bash
#!/bin/bash
# scripts/check-ssl.sh

TARGET_URL=${1:-"mysaas.com"}

echo "=== SSL/TLS Check ==="

# Test with sslscan
if command -v sslscan &> /dev/null; then
  sslscan $TARGET_URL:443 | grep -E "Accepted|TLS|SSL"
fi

# OR use openssl
echo "Certificate expiry:"
echo | openssl s_client -servername $TARGET_URL \
  -connect $TARGET_URL:443 2>/dev/null | \
  openssl x509 -noout -dates | grep -E "notAfter|notBefore"

echo -e "\nProtocol support:"
for version in "tls1_2" "tls1_3"; do
  if echo | openssl s_client -$version \
    -connect $TARGET_URL:443 2>&1 | grep -q "CONNECTED"; then
    echo "  ✅ $version supported"
  else
    echo "  ❌ $version not supported"
  fi
done

echo -e "\nCipher strength:"
echo | openssl s_client -connect $TARGET_URL:443 \
  -cipher "HIGH:!aNULL:!eNULL:!EXPORT:!DES:!3DES:!MD5:!PSK:!RC4" \
  2>/dev/null | grep "Cipher" | head -1
```

## Vulnerability Reporting Template

```markdown
# Security Assessment Report

## Executive Summary
**Date:** [Date]
**Target:** [Target URL]
**Tester:** [Your Name]
**Scope:** [What was tested]
**Overall Risk:** [Low/Medium/High/Critical]

### Summary of Findings
| Severity | Count |
|----------|-------|
| Critical | [N] |
| High     | [N] |
| Medium   | [N] |
| Low      | [N] |
| Info     | [N] |

## Detailed Findings

### Finding 1: [Title]
**Severity:** [Critical/High/Medium/Low/Info]
**Location:** [URL/Endpoint]
**Type:** [OWASP Category]

**Description:**
[Detailed description of the vulnerability]

**Impact:**
[What an attacker could do with this]

**Reproduction Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Proof of Concept:**
```
[Request/response or command used]
```

**Remediation:**
[How to fix this]

**References:**
- [OWASP Link]
- [CVE Link]

---

### Finding 2: [Title]
...

## Positive Findings
Things that are done well:
- Proper HTTPS configuration
- CSRF tokens implemented
- Input validation on [specific endpoint]

## Recommendations
Priority order:
1. Fix critical/high findings immediately
2. Address medium findings within 30 days
3. Review low findings and plan remediation
4. Implement missing security headers
5. Add additional monitoring

## Appendix
- Tools used
- Scan results
- Additional notes
```

## Automated Security Score

```typescript
// scripts/security-score.ts
// Calculate an overall security score

interface SecurityCheck {
  name: string;
  passed: boolean;
  weight: number; // 1-10 importance
}

class SecurityScoreCalculator {
  private checks: SecurityCheck[] = [];

  addCheck(name: string, passed: boolean, weight: number) {
    this.checks.push({ name, passed, weight });
  }

  calculate(): {
    score: number;
    totalWeight: number;
    passedWeight: number;
    checks: SecurityCheck[];
    grade: string;
  } {
    const totalWeight = this.checks.reduce((s, c) => s + c.weight, 0);
    const passedWeight = this.checks
      .filter(c => c.passed)
      .reduce((s, c) => s + c.weight, 0);
    const score = totalWeight > 0
      ? Math.round((passedWeight / totalWeight) * 100)
      : 0;

    let grade: string;
    if (score >= 90) grade = 'A';
    else if (score >= 80) grade = 'B';
    else if (score >= 70) grade = 'C';
    else if (score >= 60) grade = 'D';
    else grade = 'F';

    return {
      score,
      totalWeight,
      passedWeight,
      checks: this.checks,
      grade,
    };
  }

  generateReport() {
    const result = this.calculate();
    let report = '=== Security Score Report ===\n\n';

    for (const check of result.checks) {
      const icon = check.passed ? '✅' : '❌';
      report += `${icon} ${check.name} (weight: ${check.weight})\n`;
    }

    report += `\nScore: ${result.score}/100 (Grade: ${result.grade})`;
    report += `\nPassed: ${result.passedWeight}/${result.totalWeight} weighted checks\n`;

    if (result.score < 70) {
      report += '\n⚠️  Security score below 70. Immediate action required.';
    } else if (result.score < 85) {
      report += '\nImprovements recommended to reach A grade.';
    } else {
      report += '\n✅ Good security posture. Continue monitoring.';
    }

    return report;
  }
}
```

## Monthly Self-Pentest Routine

```markdown
## Monthly Security Testing Schedule

### Week 1: Automated Scanning
[ ] Run OWASP ZAP full scan (30 min)
[ ] Run Nuclei scan (10 min)
[ ] Run dependency audit (5 min)
[ ] Run secret scan (5 min)
[ ] Review results and prioritize

### Week 2: Manual Testing
[ ] Test authentication flow (30 min)
[ ] Test authorization (IDOR check) (30 min)
[ ] Test input validation (20 min)
[ ] Test business logic (20 min)
[ ] Test file upload (if applicable) (15 min)

### Week 3: Infrastructure Check
[ ] Check SSL/TLS configuration (10 min)
[ ] Check security headers (5 min)
[ ] Review server hardening (15 min)
[ ] Check firewall rules (10 min)
[ ] Review access logs for anomalies (15 min)

### Week 4: Review & Plan
[ ] Review all findings (30 min)
[ ] Fix critical/high issues (time varies)
[ ] Plan remediation for medium issues (30 min)
[ ] Update security runbook (15 min)
[ ] Schedule next month's tests (5 min)

Total time: ~5 hours/month
```

## Summary

Self-service penetration testing as a solo founder is about consistency, not sophistication. You don't need to find every vulnerability — you need to find the common ones that attackers actually exploit.

Key practices:
1. **Run automated scans monthly** — ZAP + Nuclei catch 70% of common issues
2. **Test authentication manually** — This is where most SaaS vulnerabilities live
3. **Check for IDOR** — The most common SaaS-specific vulnerability
4. **Scan dependencies** — Most breaches exploit known vulnerabilities
5. **Review security headers** — Easy to check, easy to fix
6. **Document everything** — Track findings and remediation over time
7. **Improve continuously** — Each month, add one new test or process
8. **Get a professional audit when you can afford it** — $2-5k for a focused pentest is worth it at scale

Remember: The goal is not to be perfectly secure — it's to eliminate the common vulnerabilities that attackers exploit. A consistently tested product is more secure than one that's never been tested, even without a professional pentester.
