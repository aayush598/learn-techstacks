# SaaS Security Checklist for Solo Founders

## Security Without a Security Team

As a solo founder, you don't have a security team, a CISO, or a penetration testing budget. But your customers expect you to protect their data. The key is to focus on the highest-impact security measures that prevent the most common and dangerous attacks.

This guide provides a comprehensive security checklist for solo SaaS founders, with specific implementation guidance for each control.

## The Solo Founder's Security Philosophy

### The Pareto Principle of Security

80% of security risk comes from 20% of vulnerabilities. Focus on:

```markdown
1. Authentication & Authorization (OWASP #1)
2. Data Encryption (in transit and at rest)
3. Input Validation (prevent injection attacks)
4. Dependency Management (known vulnerabilities)
5. Secrets Management (don't leak credentials)
6. Logging & Monitoring (detect breaches)
7. Backup & Recovery (survive ransomware)
```

If you do these seven things well, you've eliminated 80% of your risk.

### What NOT to Do (As a Solo Founder)

```markdown
DON'T waste time on:
  - Building your own authentication system (use Clerk/Auth0)
  - Custom encryption algorithms (use standard libraries)
  - Hardware security modules (too expensive, unnecessary)
  - Formal penetration testing (too expensive for MVP)
  - SOC2 certification (too expensive for early stage)
  - Bug bounty programs (too expensive for early stage)
  - Custom WAF rules (Cloudflare handles this)
```

## The Complete Security Checklist

### 1. Authentication & Authorization

```markdown
[ ] Password hashing: bcrypt or argon2 (NOT SHA1, MD5)
[ ] Session management: HTTP-only, Secure, SameSite cookies
[ ] JWT tokens: short expiry (15 min for access, 7 days for refresh)
[ ] MFA support: optional but available
[ ] Rate limiting on login: 5 attempts per minute per IP
[ ] Account lockout: after 10 failed attempts
[ ] Password policy: minimum 8 characters
[ ] Session invalidation: on password change
[ ] API authentication: API keys with least privilege
[ ] RBAC: role-based access control enforced server-side
[ ] Row-level security: users can only access their own data
[ ] CORS: restrict to your domain only
```

#### Authentication Implementation

```typescript
// lib/auth/password.ts
import { hash, compare } from 'bcryptjs';

const SALT_ROUNDS = 12;

export async function hashPassword(password: string): Promise<string> {
  return hash(password, SALT_ROUNDS);
}

export async function verifyPassword(
  password: string,
  hash: string
): Promise<boolean> {
  return compare(password, hash);
}
```

```typescript
// lib/auth/jwt.ts
import { SignJWT, jwtVerify } from 'jose';

const SECRET = new TextEncoder().encode(process.env.JWT_SECRET!);

export async function createToken(payload: {
  userId: string;
  role: string;
}): Promise<string> {
  return new SignJWT(payload)
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime('15m')
    .sign(SECRET);
}

export async function createRefreshToken(
  payload: { userId: string; sessionId: string }
): Promise<string> {
  return new SignJWT(payload)
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime('7d')
    .sign(SECRET);
}

export async function verifyToken<T>(token: string): Promise<T> {
  const { payload } = await jwtVerify(token, SECRET);
  return payload as T;
}
```

```typescript
// middleware/auth.ts
// Server-side authorization middleware

export function requireAuth() {
  return async (req: Request, res: Response, next: NextFunction) => {
    const token = req.headers.authorization?.replace('Bearer ', '');

    if (!token) {
      return res.status(401).json({
        error: { code: 'UNAUTHORIZED', message: 'Authentication required' },
      });
    }

    try {
      const payload = await verifyToken(token);
      req.userId = payload.userId;
      req.userRole = payload.role;
      next();
    } catch (error) {
      return res.status(401).json({
        error: { code: 'TOKEN_EXPIRED', message: 'Token is invalid or expired' },
      });
    }
  };
}

export function requireRole(...roles: string[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!roles.includes(req.userRole)) {
      return res.status(403).json({
        error: { code: 'FORBIDDEN', message: 'Insufficient permissions' },
      });
    }
    next();
  };
}
```

### 2. Data Encryption

```markdown
[ ] TLS/SSL: HTTPS only, HSTS enabled
[ ] TLS version: minimum 1.2 (prefer 1.3)
[ ] Database encryption: encrypted at rest (RDS/Supabase handles this)
[ ] Sensitive fields: encrypt PII in database
[ ] API keys: never store plaintext, always hash
[ ] Secrets: never hardcode in code, use environment variables
[ ] File uploads: encrypt at rest in storage (S3/R2 server-side encryption)
[ ] Backups: encrypted backups
[ ] Encryption keys: managed via cloud KMS or environment variables
```

#### Data Encryption Helpers

```typescript
// lib/security/encryption.ts
import { createCipheriv, createDecipheriv, randomBytes, scrypt } from 'crypto';
import { promisify } from 'util';

const ALGORITHM = 'aes-256-gcm';

export class FieldEncryption {
  private key: Buffer;

  constructor(secret: string) {
    // Derive a 32-byte key from the secret
    this.key = Buffer.from(secret.padEnd(32).slice(0, 32));
  }

  encrypt(text: string): string {
    const iv = randomBytes(16);
    const cipher = createCipheriv(ALGORITHM, this.key, iv);

    let encrypted = cipher.update(text, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    const authTag = cipher.getAuthTag().toString('hex');

    // Store: iv:authTag:encrypted
    return `${iv.toString('hex')}:${authTag}:${encrypted}`;
  }

  decrypt(encryptedText: string): string {
    const [ivHex, authTagHex, encrypted] = encryptedText.split(':');

    const decipher = createDecipheriv(
      ALGORITHM,
      this.key,
      Buffer.from(ivHex, 'hex')
    );
    decipher.setAuthTag(Buffer.from(authTagHex, 'hex'));

    let decrypted = decipher.update(encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');

    return decrypted;
  }
}

// Usage: encrypt sensitive fields before storing
const encryption = new FieldEncryption(process.env.ENCRYPTION_KEY!);

// Store encrypted
await db.query(
  'INSERT INTO users (id, email, ssn_encrypted) VALUES ($1, $2, $3)',
  [userId, email, encryption.encrypt(ssn)]
);

// Read and decrypt
const result = await db.query('SELECT ssn_encrypted FROM users WHERE id = $1', [userId]);
const ssn = encryption.decrypt(result.rows[0].ssn_encrypted);
```

### 3. Input Validation & Injection Prevention

```markdown
[ ] SQL injection: use parameterized queries (NEVER string concatenation)
[ ] XSS: sanitize user input, use Content-Security-Policy header
[ ] CSRF: use anti-CSRF tokens for state-changing requests
[ ] Command injection: never pass user input to shell commands
[ ] File upload: validate type, size, scan for malware
[ ] SSRF: validate URLs, restrict outbound traffic
[ ] Rate limiting: apply to all endpoints
[ ] Request size limits: prevent large payload attacks
[ ] HTTP methods: restrict to needed methods only
[ ] Content-Type: validate Content-Type headers
```

#### Input Validation

```typescript
// lib/security/validation.ts
import { z } from 'zod';

// Strict validation schemas
export const SafeString = z.string().min(1).max(1000).trim();
export const SafeEmail = z.string().email().max(255).toLowerCase().trim();
export const SafeUUID = z.string().uuid();
export const SafeURL = z.string().url().max(2048);
export const SafeHTML = z.string().max(10000); // Use sanitizer before rendering

// Sanitize HTML (prevent XSS)
export function sanitizeHTML(input: string): string {
  return input
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;')
    .replace(/\//g, '&#x2F;');
}

// Always parameterized queries - NO string interpolation
// BAD: await pool.query(`SELECT * FROM users WHERE id = ${userId}`)
// GOOD: await pool.query('SELECT * FROM users WHERE id = $1', [userId])

// File upload validation
export function validateFileUpload(file: {
  mimetype: string;
  size: number;
  buffer: Buffer;
}): boolean {
  const ALLOWED_TYPES = [
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/webp',
    'application/pdf',
    'text/csv',
  ];

  const MAX_SIZE = 10 * 1024 * 1024; // 10MB

  if (!ALLOWED_TYPES.includes(file.mimetype)) {
    throw new Error('File type not allowed');
  }

  if (file.size > MAX_SIZE) {
    throw new Error('File too large');
  }

  return true;
}
```

### 4. Dependency Management

```markdown
[ ] Regular updates: npm audit / dependabot weekly
[ ] Known vulnerabilities: use Snyk or GitHub Dependabot
[ ] Lock files: commit package-lock.json / yarn.lock
[ ] Minimal dependencies: avoid unnecessary packages
[ ] Version pinning: specify exact versions in production
[ ] Deprecation checks: use npm-check or similar
[ ] Supply chain: avoid suspicious packages (typosquatting)
[ ] Node.js: stay on LTS versions
[ ] Docker images: use minimal base images (alpine)
```

#### Dependency Audit Script

```bash
#!/bin/bash
# scripts/security-audit.sh
# Run weekly to check for vulnerabilities

set -euo pipefail

echo "=== Security Audit ==="

# Check npm dependencies
echo "Checking npm dependencies..."
npm audit --audit-level=high || true

# Check for outdated packages
echo "Checking for outdated packages..."
npm outdated || true

# Check for known malicious packages
echo "Checking for malicious packages..."
npx @socketsecurity/cli audit || true

# Check for hardcoded secrets
echo "Checking for hardcoded secrets..."
npx secretlint "**/*" || true

echo "=== Audit Complete ==="
```

#### Dependabot Configuration

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "09:00"
      timezone: "America/New_York"
    open-pull-requests-limit: 10
    labels:
      - "dependencies"
      - "security"
    reviewers:
      - "you"  # Your GitHub username
    ignore:
      # Only receive security updates for these
      - dependency-name: "*"
        update-types: ["version-update:semver-patch"]

  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

### 5. Secrets Management

```markdown
[ ] Environment variables: ALL secrets via env vars, never hardcoded
[ ] .env files: in .gitignore, never committed
[ ] Secrets storage: use platform secrets (Railway, Vercel) or GitHub Secrets
[ ] API keys: rotate regularly
[ ] Database credentials: use different credentials per environment
[ ] Encryption keys: separate key per environment
[ ] Logging: never log secrets, tokens, or passwords
[ ] Error messages: never expose stack traces to users
[ ] Git history: scan for accidentally committed secrets (git-secrets, trufflehog)
```

#### Secret Scanning

```bash
#!/bin/bash
# scripts/scan-secrets.sh
# Scan for accidentally committed secrets

# Install: brew install git-secrets
# Or: npm install -g secretlint

echo "Scanning for secrets in git history..."

# Option 1: git-secrets
if command -v git-secrets &> /dev/null; then
  git secrets --scan-history
fi

# Option 2: trufflehog (more thorough)
if command -v trufflehog &> /dev/null; then
  trufflehog git file://. --since-commit HEAD --results=verified,unknown
fi

# Option 3: grep for common patterns
echo "Checking for common secret patterns..."
git grep -n -i "api_key\|api_key\|api_secret\|password\|secret\|token\|credential" \
  -- ':!*.md' ':!*.yml' ':!*.yaml' ':!package-lock.json' ':!*.lock' || true

echo "Scan complete!"
```

### 6. Security Headers

```typescript
// middleware/security-headers.ts
// Set security headers on all responses

export function securityHeaders() {
  return (req: Request, res: Response, next: NextFunction) => {
    // Prevent MIME type sniffing
    res.setHeader('X-Content-Type-Options', 'nosniff');

    // Prevent clickjacking
    res.setHeader('X-Frame-Options', 'DENY');

    // Enable XSS filter in older browsers
    res.setHeader('X-XSS-Protection', '1; mode=block');

    // HSTS: force HTTPS
    if (process.env.NODE_ENV === 'production') {
      res.setHeader(
        'Strict-Transport-Security',
        'max-age=31536000; includeSubDomains; preload'
      );
    }

    // Content Security Policy
    res.setHeader(
      'Content-Security-Policy',
      [
        "default-src 'self'",
        "script-src 'self' 'unsafe-inline' 'unsafe-eval'",
        "style-src 'self' 'unsafe-inline'",
        "img-src 'self' data: https:",
        "font-src 'self'",
        "connect-src 'self' https://api.stripe.com https://*.clerk.com",
        "frame-src 'self' https://checkout.stripe.com",
        "base-uri 'self'",
        "form-action 'self'",
      ].join('; ')
    );

    // Referrer Policy
    res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');

    // Permissions Policy
    res.setHeader(
      'Permissions-Policy',
      'camera=(), microphone=(), geolocation=(), interest-cohort=()'
    );

    // Cache control for sensitive pages
    if (req.path.startsWith('/dashboard') || req.path.startsWith('/api')) {
      res.setHeader('Cache-Control', 'no-store');
    }

    next();
  };
}
```

### 7. Rate Limiting

```typescript
// middleware/rate-limit.ts
// Prevent brute force and DoS attacks

import { RateLimiter } from 'limiter';

interface RateLimitConfig {
  windowMs: number;
  max: number;
  message?: string;
}

const limits = new Map<string, { count: number; resetAt: number }>();

export function rateLimit(config: RateLimitConfig) {
  return (req: Request, res: Response, next: NextFunction) => {
    const key = req.ip || req.headers['x-forwarded-for'] as string || 'unknown';
    const now = Date.now();
    const record = limits.get(key);

    if (!record || now > record.resetAt) {
      limits.set(key, { count: 1, resetAt: now + config.windowMs });
      setRateLimitHeaders(res, config.max, config.max - 1);
      return next();
    }

    if (record.count >= config.max) {
      setRateLimitHeaders(res, config.max, 0);
      const retryAfter = Math.ceil((record.resetAt - now) / 1000);
      return res.status(429).json({
        error: {
          code: 'RATE_LIMITED',
          message: config.message || 'Too many requests',
          retryAfter,
        },
      });
    }

    record.count++;
    setRateLimitHeaders(res, config.max, config.max - record.count);
    next();
  };
}

function setRateLimitHeaders(
  res: Response,
  limit: number,
  remaining: number
) {
  res.setHeader('X-RateLimit-Limit', limit);
  res.setHeader('X-RateLimit-Remaining', remaining);
}

// Specific rate limits for different endpoints
export const strictRateLimit = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 10, // 10 requests per minute
  message: 'Too many requests, please slow down',
});

export const authRateLimit = rateLimit({
  windowMs: 60 * 1000,
  max: 5, // 5 login attempts per minute
  message: 'Too many login attempts',
});

export const apiRateLimit = rateLimit({
  windowMs: 60 * 1000,
  max: 60, // 60 API calls per minute
});

export const webhookRateLimit = rateLimit({
  windowMs: 60 * 1000,
  max: 100, // Webhooks can be more frequent
});
```

### 8. Logging & Monitoring

```typescript
// lib/security/audit.ts
// Security event logging

interface SecurityEvent {
  type: 'login' | 'logout' | 'failed_login' | 'password_change'
       | 'permission_change' | 'api_key_created' | 'api_key_deleted'
       | 'data_export' | 'data_delete' | 'settings_change'
       | 'suspicious_activity' | 'admin_action';
  userId: string;
  ip: string;
  userAgent?: string;
  details?: Record<string, any>;
  severity: 'info' | 'warning' | 'critical';
}

class SecurityAudit {
  async log(event: SecurityEvent) {
    // Always log to database
    await db.query(
      `INSERT INTO security_audit_log
       (type, user_id, ip, user_agent, details, severity)
       VALUES ($1, $2, $3, $4, $5, $6)`,
      [event.type, event.userId, event.ip,
       event.userAgent, JSON.stringify(event.details || {}), event.severity]
    );

    // Critical events trigger immediate alert
    if (event.severity === 'critical') {
      await this.alertCritical(event);
    }

    // Suspicious patterns trigger investigation
    if (this.isSuspicious(event)) {
      await this.alertSuspicious(event);
    }
  }

  private isSuspicious(event: SecurityEvent): boolean {
    // Multiple failed logins
    // Login from unusual IP/location
    // Access to sensitive data outside normal patterns
    return event.type === 'failed_login' && (event.details?.count || 0) > 5;
  }

  private async alertCritical(event: SecurityEvent) {
    // Send immediate notification (SMS, phone call)
    await notifyService.send({
      channel: 'sms',
      message: `CRITICAL: ${event.type} for user ${event.userId}`,
    });
  }

  private async alertSuspicious(event: SecurityEvent) {
    // Send email notification
    await sendEmail({
      to: process.env.ADMIN_EMAIL!,
      subject: `Suspicious activity detected: ${event.type}`,
      body: JSON.stringify(event, null, 2),
    });
  }
}

export const securityAudit = new SecurityAudit();
```

### 9. Database Security

```sql
-- Database-level security controls

-- Least privilege role
CREATE ROLE app_user WITH LOGIN PASSWORD 'strong-password';
GRANT CONNECT ON DATABASE app TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;

-- Grant only necessary permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO app_user;

-- Revoke unnecessary permissions
REVOKE CREATE ON SCHEMA public FROM app_user;
REVOKE DROP ON ALL TABLES IN SCHEMA public FROM app_user;

-- Row-Level Security (already covered in schema design)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

-- Connection limits
ALTER ROLE app_user CONNECTION LIMIT 20;

-- Idle session timeout
ALTER SYSTEM SET idle_in_transaction_session_timeout = '60000'; -- 1 minute
```

### 10. Infrastructure Security

```markdown
[ ] SSH: key-based authentication only, disable password login
[ ] Firewall: restrict ports (22, 80, 443 only)
[ ] WAF: Cloudflare WAF rules (free tier)
[ ] DDoS: Cloudflare DDoS protection (free)
[ ] Bot protection: Cloudflare bot fight mode
[ ] IP whitelisting: admin tools accessible only from your IP
[ ] Server updates: automated security patches (unattended-upgrades)
[ ] Docker: run containers as non-root user
[ ] File permissions: strict file system permissions
[ ] Monitoring: intrusion detection (fail2ban, OSSEC)
```

#### Server Hardening Script

```bash
#!/bin/bash
# scripts/harden-server.sh

set -euo pipefail

echo "Hardening server..."

# 1. SSH hardening
cat >> /etc/ssh/sshd_config << 'EOF'
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
AllowUsers deploy
EOF
systemctl restart sshd

# 2. Firewall (UFW)
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

# 3. Fail2Ban (prevent brute force)
apt-get install -y fail2ban
cat > /etc/fail2ban/jail.local << 'EOF'
[sshd]
enabled = true
maxretry = 3
bantime = 3600

[nginx-http-auth]
enabled = true
maxretry = 5
bantime = 3600
EOF
systemctl restart fail2ban

# 4. Automatic security updates
apt-get install -y unattended-upgrades
cat > /etc/apt/apt.conf.d/20auto-upgrades << 'EOF'
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Download-Upgradeable-Packages "1";
APT::Periodic::AutocleanInterval "7";
APT::Periodic::Unattended-Upgrade "1";
EOF

# 5. Docker security (if using Docker)
cat > /etc/docker/daemon.json << 'EOF'
{
  "userns-remap": "default",
  "no-new-privileges": true,
  "live-restore": true
}
EOF

echo "Server hardened!"
```

## Security Incident Response

### Incident Response Plan

```markdown
## Security Incident Response Plan

### 1. Detect
How you'll know there's a security incident:
  - Automated alerts (Sentry, monitoring)
  - User reports (support email)
  - Anomalous patterns (unusual traffic, error spikes)
  - Third-party notification (cloud provider, security researcher)

### 2. Assess
Determine severity:
  - CRITICAL: Data breach, unauthorized access, payment compromise
  - HIGH: Active exploit, account takeover wave
  - MEDIUM: Vulnerability discovered (no active exploit)
  - LOW: Security scan finding (theoretical risk)

### 3. Contain
Immediate actions to stop the bleeding:
  [ ] Revoke compromised credentials
  [ ] Block malicious IPs (Cloudflare WAF)
  [ ] Disable compromised user accounts
  [ ] Rotate API keys and secrets
  [ ] Scale down/disconnect affected services

### 4. Investigate
Determine scope and cause:
  [ ] Check security audit logs
  [ ] Review application logs for unusual activity
  [ ] Identify affected users and data
  [ ] Determine root cause
  [ ] Preserve evidence (logs, snapshots)

### 5. Remediate
Fix the vulnerability:
  [ ] Deploy security patch
  [ ] Update security controls
  [ ] Add additional monitoring
  [ ] Rotate ALL secrets (even potentially affected ones)

### 6. Communicate
Notify affected parties:
  [ ] Notify affected users (data breach notification)
  [ ] Notify cloud provider (if applicable)
  [ ] Update status page
  [ ] File necessary reports (regulatory compliance)

### 7. Learn
Improve for next time:
  [ ] Conduct post-mortem
  [ ] Update incident response plan
  [ ] Implement preventative measures
  [ ] Add security tests
```

### Security Contact Information

```markdown
Keep this information accessible (but secure):

Emergency Contacts:
  - Your phone: [number]
  - Backup contact: [friend/co-founder]
  - Cloud provider support: [phone/chat]
  - Stripe security: security@stripe.com
  - Cloudflare security: security@cloudflare.com

Important URLs:
  - Cloudflare dashboard: https://dash.cloudflare.com
  - Sentry dashboard: https://sentry.io
  - GitHub security: https://github.com/settings/security
  - Domain registrar: [URL]
  - DNS provider: [URL]

Runbook Locations:
  - Server access: [stored in password manager]
  - Database access: [stored in password manager]
  - Emergency scripts: /opt/scripts/
  - Backup locations: [S3 bucket / R2 bucket]
```

## Security Automation

### Weekly Security Tasks

```bash
#!/bin/bash
# scripts/weekly-security.sh
# Run every Monday

echo "=== Weekly Security Check ==="

# 1. Check for vulnerabilities
npm audit --audit-level=high

# 2. Scan for secrets
git secrets --scan

# 3. Check SSL certificate expiry
echo | openssl s_client -servername mysaas.com \
  -connect mysaas.com:443 2>/dev/null | \
  openssl x509 -noout -dates

# 4. Review recent failed logins
grep "Failed password" /var/log/auth.log | tail -20

# 5. Check firewall status
ufw status verbose

# 6. Check disk space (prevent data loss)
df -h / | awk 'NR==2 {print $5}'

echo "=== Weekly Check Complete ==="
```

## Security Budget for Solo Founders

```markdown
Security investments that matter (in order):

Free (0-50/mo):
  [ ] Clerk/Auth0 (free tier) - Authentication
  [ ] Cloudflare (free) - WAF, DDoS, SSL
  [ ] GitHub Dependabot (free) - Dependency scanning
  [ ] HTTPS (free via Cloudflare/LetsEncrypt) - Encryption in transit
  [ ] HSTS headers - Force HTTPS
  [ ] CORS configuration - Prevent cross-origin attacks
  [ ] Rate limiting middleware - Prevent brute force
  [ ] Security headers - CSP, X-Frame-Options, etc.

Low Cost ($10-50/mo):
  [ ] Sentry (free/tier) - Error monitoring (detect anomalies)
  [ ] Better Uptime ($20/mo) - Availability monitoring
  [ ] Password manager ($3/mo) - Secure credential storage

When You Have Revenue ($50-500/mo):
  [ ] Penetration testing ($500-2000/engagement)
  [ ] Snyk ($25/mo) - Advanced vulnerability scanning
  [ ] Security training ($200/year)
  [ ] Bug bounty (HackerOne, $500/mo+)

Don't Invest In (Yet):
  [ ] SOC2 certification ($10k+)
  [ ] SIEM ($1000/mo+)
  [ ] Dedicated security tools
```

## Monthly Security Review

```markdown
## Monthly Security Review

### Access Review
[ ] Review admin accounts - still needed?
[ ] Review API keys - rotate any that are old
[ ] Review team member access (when you have team)
[ ] Check for inactive sessions

### Vulnerability Management
[ ] Run dependency audit (npm audit)
[ ] Check for known vulnerabilities in critical libraries
[ ] Review security advisories for your stack
[ ] Apply security patches

### Monitoring Review
[ ] Review security audit logs for anomalies
[ ] Check failed login rates
[ ] Review error rates in Sentry
[ ] Check for suspicious API patterns

### Backup Verification
[ ] Test database restoration from backup
[ ] Verify backup integrity
[ ] Check backup retention meets requirements

### Compliance Check
[ ] Review privacy policy - still accurate?
[ ] Check data retention - delete old data
[ ] Review user data deletion process
[ ] Update terms of service if needed
```

## Summary

Security for solo founders is about focus. You can't do everything, so you must do the things that matter most:

1. **Authentication is your #1 priority** — Use a managed auth service, never build your own
2. **Encrypt everything** — HTTPS, database at rest, sensitive fields
3. **Validate all inputs** — Prevent injection attacks at every entry point
4. **Keep dependencies updated** — Most breaches come from known vulnerabilities
5. **Never hardcode secrets** — Environment variables always
6. **Set security headers** — CSP, HSTS, and others prevent common attacks
7. **Rate limit aggressively** — Prevent brute force and abuse
8. **Log security events** — You can't respond to what you can't see
9. **Backup regularly** — Ransomware is real, backups are your last line of defense
10. **Have an incident plan** — You'll panic less if you have a plan

The goal is not to be unhackable (impossible) — it's to be a harder target than the next SaaS. Most attacks are opportunistic. Make your system not worth the effort.
