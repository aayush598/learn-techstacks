# Security Goals and the CIA Triad

> **TL;DR**: Security is defined by goals — Confidentiality (only authorized readers), Integrity (no unauthorized modification), Availability (accessible when needed), plus Authentication, Authorization, Accounting, and Non-repudiation — and every control, protocol, and attack in networking exists to defend (or breach) one of these pillars.

## 1. Why Does This Exist?
"Secure" is meaningless without a definition. The CIA triad exists because security professionals and engineers need a shared, testable vocabulary: what exactly are we protecting, and against whom? Every attack and every defense maps to a pillar — a data breach violates confidentiality, a transaction altered in transit violates integrity, a DDoS violates availability — and knowing *which* pillar a control protects tells you whether it's the right control at all. Beyond the triad, real systems need Authentication (who are you?), Authorization (what may you do?), Accounting (what did you do?), and Non-repudiation (you can't deny doing it). These goals are the *requirements* document for TLS, IPsec, SSH, firewalls, and every other technology in this part — and the first thing interviewers test when they ask "what does security mean here?"

## 2. How Does It Work?
Each goal maps to mechanisms:
- **Confidentiality** → encryption (symmetric AES, asymmetric RSA/ECC), access control, data-at-rest/in-transit protections.
- **Integrity** → hashes (SHA-256), MACs/HMACs, digital signatures, checksums at every layer (CRC at L2, TLS record MAC).
- **Availability** → redundancy, load balancing, DDoS mitigation, backups, rate limiting, failover.
- **Authentication** → passwords, MFA, certificates, tokens (OAuth), 802.1X.
- **Authorization** → RBAC/ABAC, ACLs, IAM policies, capability tokens.
- **Accounting/auditability** → logs, SIEM, tracing, non-repudiation via signatures.
In practice, a protocol (e.g., TLS) bundles several: it provides confidentiality (encryption), integrity (MAC), authentication (certificates), and even non-repudiation support (server signatures). A threat model (e.g., STRIDE) enumerates what could go wrong; the CIA goals say what "right" looks like.

## 3. When Is It Used?
- **Every design decision**: "should I encrypt this in transit? at rest? Who can call this API? Do I need an audit log?" — answered by CIA/AAA.
- **Compliance**: PCI-DSS (cardholder data confidentiality), HIPAA, GDPR (confidentiality + integrity + availability obligations) — regulators literally codify CIA.
- **Incident response**: classifying an incident ("data leak" = confidentiality; "defaced page" = integrity; "service down" = availability) directs the response.
- **Threat modeling**: STRIDE (Spoofing, Tampering, Repudiation, Info disclosure, DoS, Elevation of privilege) — each item is a CIA/AAA violation.
- **Architecture review**: zero trust, defense-in-depth, and least privilege are all operationalizations of these goals.

## 4. Why Wasn't Another Approach Chosen?
- *Alternative: single "security = encryption."* Encryption provides confidentiality but *nothing* else — a tampered encrypted blob (no MAC) corrupts silently, and encryption says nothing about who may read (authz) or whether the service is up (availability). Splitting goals forces a complete design; conflating them leaves glaring holes (the classic "encrypted but unauthenticated" vulnerability, e.g., CBC without MAC).
- *Alternative: one catch-all "privacy."* Privacy (GDPR sense) overlaps confidentiality but also includes data minimization, consent, and user control — a different, complementary frame. CIA is about protecting *data and service*; privacy is about *people and policy*. Both are needed.
- *Alternative: focus only on attacks (list every threat).* Attack taxonomies (OWASP Top 10) are useful but unbounded — new attacks appear constantly. Goals give you a *stable* frame: any new attack is still "a confidentiality violation" or "an availability attack," so you can reason about defenses without enumerating everything. This is why interviewers ask "which pillar does X violate?" — it's the transferable skill.

## 5. Intuition
CIA is the **health checklist of a system**: Confidentiality = "only the right people can read it" (a sealed letter), Integrity = "it hasn't been changed" (a tamper-evident seal), Availability = "I can use it when I need it" (the post office is open). Authentication is "prove it's really you" (show ID), Authorization is "here's what you're allowed to do" (your boarding pass), Accounting is "we recorded what you did" (the airline's manifest). A system is "secure" only when *all* of these hold — sealing a letter (confidentiality) but sending it through a mailbag full of razor blades (integrity/availability risk) isn't security.

## 6. Real-World Analogy
A **bank vault with a sign-in book**. Confidentiality = the vault and who can see inside (encryption, access control). Integrity = the ledger can't be edited without detection (signed checks, hash chains). Availability = the vault opens during business hours and can't be jammed (DDoS mitigation, redundancy). Authentication = you show ID at the door (password/MFA). Authorization = your account can withdraw but not open other accounts (RBAC). Accounting = the sign-in book records every visit (audit logs, non-repudiation). Rob a bank = breaching one or more pillars; the defense is keeping *each* pillar enforced independently so one failure doesn't sink the whole bank.

## 7. Formal Definition
- **Confidentiality**: information is not disclosed to unauthorized entities; implemented with encryption and access control.
- **Integrity**: information (and system state) is not modified or destroyed by unauthorized parties; implemented with cryptographic hashes/MACs/signatures; includes *authenticity* (the data came from the claimed source).
- **Availability**: authorized entities can access data/services when needed; implemented with redundancy, fault tolerance, and DDoS protection; the "availability zone" concept in clouds.
- **Non-repudiation**: a party cannot deny an action (sending a message, signing a document); implemented with digital signatures and logs.
- **AAA**: Authentication (verify identity), Authorization (grant allowed actions), Accounting (record actions for audit).
- **Threat modeling**: structured identification of threats (STRIDE) and the assets/trust boundaries they cross; a **risk** = likelihood × impact, and controls reduce risk.

## 8. Example
A **bank transfer over HTTPS** and which goal each piece serves:
1. TLS handshake authenticates the bank (server certificate — *authentication* + *non-repudiation* of the server).
2. The transfer payload is AES-encrypted (*confidentiality*).
3. TLS record MACs detect any tampering in transit (*integrity* + *authenticity*).
4. The bank's API checks your token/role before the transfer (*authorization*).
5. The request is logged with your ID, amount, timestamp (*accounting*).
6. If an attacker DDoSes the bank's login page, the transfer is *unavailable* — the availability pillar, fixed by load balancers + DDoS scrubbing.
One transaction, six goals — and removing any one creates an attack.

## 9. Internal Working
1. **Define assets** (data, keys, credentials, services) and their *value*.
2. **Define trust boundaries** (who/what is trusted vs untrusted — LAN vs Internet, process vs process).
3. **Model threats (STRIDE)**: for each interaction across a boundary, ask which CIA/AAA pillar each STRIDE category attacks.
4. **Select controls** per goal (encryption for confidentiality; MAC/signature for integrity; redundancy for availability; MFA/IAM for authentication/authorization; logging for accounting).
5. **Residual risk**: controls reduce but rarely eliminate risk; accept/mitigate/transfer/avoid the remainder.
6. **Continuously re-evaluate**: new assets, new threats, new weaknesses (threat modeling is a loop, not a one-shot).

## 10. Time Complexity / Overheads
- **Crypto overhead (per pillar)**: confidentiality via AES ≈ fast hardware (~1-10 Gbps with AES-NI); integrity via HMAC-SHA256 ≈ similar; availability via redundancy = 2-3× infrastructure cost.
- **Latency cost**: TLS handshake ~1-2 RTT (1.3), IPsec IKE ~3-6 messages — the "security costs a round trip or two" reality.
- **Operational overhead**: logging/accounting = storage + SIEM cost; IAM/RBAC = management overhead; key management (rotation, HSM) is its own discipline.
- The "cost" of security is measured in latency, CPU, and ops — balanced against the risk reduction.

## 11. Advantages
- **Shared vocabulary**: engineers, auditors, and executives agree on what "secure" means.
- **Drives correct architecture**: knowing a goal exists forces a mechanism (you can't hand-wave "confidential" without encryption).
- **Attack-independent**: new attacks are classified against stable goals, keeping defenses principled.
- **Regulatory alignment**: CIA maps directly to PCI/HIPAA/GDPR obligations.
- **Testable**: each pillar has measurable controls (encryption audit, hash verification, uptime SLO).

## 12. Disadvantages
- **Overlaps/conflicts**: availability vs confidentiality (e.g., too much encryption can slow service); a control can serve multiple pillars and misattribution leads to gaps.
- **Not sufficient alone**: goals without implementation = paperwork; "we have TLS" doesn't mean "secure."
- **Vague priorities**: without ranking assets and risks, everything looks equal and nothing gets protected.
- **Human factor**: goals are technical but most breaches (phishing, leaked keys) target the *people* layer — CIA doesn't cover social engineering directly.
- **Static**: a one-time "we meet CIA" assessment rots as the system changes.

## 13. Interview Questions
1. **Q: What is the CIA triad?** A: Confidentiality (only authorized parties can read), Integrity (data can't be modified without detection), Availability (services usable when needed). Every security control maps to one or more of these.

2. **Q: Which pillar does a data leak violate? Which does a defaced website violate? Which does a DDoS violate?** A: Data leak = confidentiality; defaced site = integrity; DDoS = availability. Being able to classify attacks instantly is the interview's core ask.

3. **Q: What is AAA?** A: Authentication (verify identity), Authorization (grant permitted actions), Accounting (record and audit actions). Also A=Availability sometimes grouped in — but AAA is the identity/audit trio.

4. **Q: How is integrity implemented differently from confidentiality?** A: Integrity = hashes/MACs/signatures (detect modification); confidentiality = encryption (prevent reading). They are orthogonal: you can encrypt without integrity (vulnerable to tampering) or authenticate without encrypting (public data signed).

5. **Q: What is non-repudiation and how is it achieved?** A: A party can't deny having sent a message or made an action. Achieved with *digital signatures* (private-key-signed, publicly verifiable) and audited logs — HMAC alone doesn't give non-repudiation because the shared key isn't uniquely attributable.

6. **Q: TRICKY — You encrypt a message but don't add a MAC. Which attacks are you exposed to?** A: Bit-flipping/tampering: an attacker (who can't read) can modify ciphertext blocks, and the receiver decrypts garbage or altered-but-valid plaintext (e.g., CBC bit-flip attacks). Confidentiality without integrity is a classic vulnerability — "encrypt-then-MAC" is the fix.

7. **Q: What is STRIDE and how does it relate to CIA?** A: STRIDE = Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege — Microsoft's threat-modeling categories. Spoofing↔authentication, Tampering↔integrity, Info disclosure↔confidentiality, DoS↔availability, Elevation↔authorization. It's CIA/AAA made enumerable for design review.

8. **Q: SCENARIO — A startup says "we're secure, we use TLS." What do you ask next?** A: Where's the data at rest? (confidentiality of storage), can an admin modify logs? (integrity of audit), is there MFA? (authentication), RBAC? (authorization), redundancy? (availability), and how do you rotate keys? (key management). TLS protects *one* part of one pillar — the conversation should expose the rest.

9. **Q: Why can't encryption alone make a system "secure"?** A: Encryption provides confidentiality only. It doesn't authenticate users (need authn), authorize actions (authz), detect tampering (need MAC), guarantee uptime (availability), or record activity (accounting). A system with strong crypto but no access control or monitoring is still insecure.

10. **Q: PRODUCTION — Your team must pick controls on a budget. What's the priority order?** A: (1) Authentication (MFA) + least-privilege authorization — most breaches start with stolen/lazy creds; (2) integrity (patching, code signing, immutable logs) — attack persistence; (3) encryption in transit and at rest — confidentiality of the crown jewels; (4) availability (backups, redundancy, rate limits); (5) accounting (logging/SIEM) to detect what slipped through. Defense-in-depth: don't skip any, but fund in this rough order.

11. **Q: What is the difference between authentication and authorization?** A: Authentication = "who are you?" (prove identity: password/MFA/cert). Authorization = "what are you allowed to do?" (roles/permissions/ACLs). Authn is the identity claim; authz is the capability grant — a system can authenticate everyone but authorize very little.

12. **Q: TRICKY — Is "authenticity" the same as "integrity"?** A: Related but distinct: integrity = data wasn't modified; authenticity = the data came from the claimed *source*. A MAC/signature provides both (if it verifies, data is unchanged *and* originated from the keyholder). Plain hash gives integrity only (anyone could have recomputed it) — which is why HMAC/signatures matter.

13. **Q: What does "defense in depth" mean?** A: Layering independent controls so one failure doesn't compromise the system: perimeter (firewall) + host (hardening) + app (input validation) + data (encryption) + detection (IDS/logs) + human (MFA/training). Each layer enforces a CIA/AAA pillar independently.

14. **Q: SCENARIO — An insider (a sysadmin) can read every customer record. Which pillar failed and what's the fix?** A: Confidentiality *and* authorization (and possibly accounting). Fixes: least-privilege/role separation (admins manage systems, not data), data at rest encrypted with keys the admin doesn't hold, and audited access logs with alerting — the principle that no single person should hold full capability.

15. **Q: What is the "principle of least privilege"?** A: Give every subject/process only the minimum permissions required for its function — a service account that reads one table, not all tables; an admin that manages infra, not data. It reduces the blast radius of any compromise (a direct consequence of authorization + integrity goals).

16. **Q: What is the difference between risk, threat, and vulnerability?** A: Threat = the actor/event that could cause harm (attacker, DDoS). Vulnerability = the weakness that lets a threat succeed (unpatched bug, open port). Risk = likelihood × impact of a threat exploiting a vulnerability. Security *reduces risk* by removing vulnerabilities and reducing impact.

17. **Q: PRODUCTION — Your monitoring shows data flowing out to an unknown IP. Which goal and which controls kick in?** A: Confidentiality is being violated (data exfiltration). Controls: DLP (data-loss prevention) flagging the egress, SIEM alerting on unexpected egress, TLS inspection/decryption policies, and — preventively — least privilege so the compromised account couldn't reach that data at all. Detection (accounting) caught what confidentiality didn't stop.

18. **Q: TRICKY — Why do regulators care about availability?** A: Because losing access to your own health records or bank data is as harmful as someone reading them. PCI/HIPAA/GDPR all require availability controls (redundancy, backups, RPO/RTO) because "secure" includes "usable when legitimately needed" — the A in CIA is a legal obligation, not just an ops concern.

## 14. Follow-Up Questions
1. **Q: What is the difference between integrity and authenticity again, with an example?** A: Integrity: a file hash unchanged. Authenticity: the file came from your vendor. A malicious vendor could send a file with a correct (unmodified) content but forged origin — only a signature (not a hash) catches that.

2. **Q: What is a trust boundary and why does threat modeling need it?** A: The line between trusted and untrusted contexts (Internet vs LAN, app vs DB, kernel vs userspace). Every STRIDE analysis happens *across* boundaries; misidentifying a boundary (e.g., treating a LAN as trusted) is how attacks hide.

3. **Q: What is the CIA conflict with availability vs confidentiality?** A: The same control can fight both — e.g., aggressive encryption/AES overhead can slow a service (availability), and too-permissive access (for availability) leaks data. Security design is a *balance* across all pillars, not a max of any one.

4. **Q: How does the CIA triad apply to a password database specifically?** A: Confidentiality: hashes not plaintext. Integrity: hash comparison detects tampering/corruption. Availability: the auth service must be up (and hashing must be fast enough to serve). Authentication uses the stored hashes; authorization decides which hashes/sessions grant what.

## 15. Coding Example
```python
# Mapping attacks to CIA/AAA pillars — a small reference table
ATTACK_PILLAR = {
    "data breach": "Confidentiality",
    "man-in-the-middle reading traffic": "Confidentiality",
    "bit-flip / tampered message": "Integrity",
    "defaced website": "Integrity",
    "DDoS": "Availability",
    "phishing for password": "Authentication (identity)",
    "privilege escalation": "Authorization",
    "logging disabled by attacker": "Accounting / Integrity",
    "sender denies sending": "Non-repudiation",
}
print("CIA classification:",
      {k: v for k, v in list(ATTACK_PILLAR.items())[:5]})

def risk(threat, vulnerability, likelihood=0.5, impact=10):
    """Risk = likelihood x impact (a qualitative scoring sketch)."""
    return {"threat": threat, "vuln": vulnerability,
            "risk_score": likelihood * impact}

print(risk("attacker", "open unpatched port 445", 0.7, 8))

def controls_for(goal):
    return {
        "confidentiality": ["AES-256 in transit/at rest", "IAM/least privilege"],
        "integrity": ["HMAC-SHA256", "digital signatures", "immutable logs"],
        "availability": ["redundancy", "DDoS scrubbing", "backups"],
        "authentication": ["MFA", "certificates", "OAuth"],
        "authorization": ["RBAC/ABAC", "ACLs"],
        "accounting": ["structured logging", "SIEM"],
    }.get(goal.lower(), [])

print("integrity controls:", controls_for("integrity"))
```
```bash
# Observe CIA/AAA-relevant behavior on a real system
journalctl -u sshd | grep -E "Failed password|Accepted" | tail    # accounting of auth attempts
ss -tnp | head -10                                               # who's connected (confidentiality surface)
sudo auditctl -l | head -5                                       # Linux audit rules (accounting)
loginctl list-sessions                                            # active authn sessions
# Availability-style checks:
systemctl status nginx --no-pager | head -3
ip -s link show eth0 | grep -E "dropped|overruns"                # loss = availability signal
```

## 16. Industry Usage
- **Every compliance framework**: PCI-DSS, HIPAA, SOC 2, GDPR all operationalize CIA/AAA; security teams map controls to pillars.
- **Cloud IAM**: AWS/GCP/Azure IAM is pure authentication (STS, MFA) + authorization (policies/RBAC/ABAC) + accounting (CloudTrail) — AAA in production at planet scale.
- **Product security**: Stripe/Square/Adyen map every data flow to CIA to drive crypto/access decisions; SOC 2 readiness is the same mapping.
- **Threat modeling**: Microsoft STRIDE, MITRE ATT&CK (attack taxonomy), OWASP ASVS — used in every mature SDLC.
- **Blue/red teams**: incident classification by pillar drives runbooks (availability incident → DDoS/redundancy; confidentiality incident → credential rotation, notification).

## 17. References
- Whitman & Mattord, *Principles of Information Security* — the CIA/AAA canonical text.
- Microsoft STRIDE — https://learn.microsoft.com/en-us/security/engineering/thread-modeling
- OWASP Threat Modeling — https://owasp.org/www-community/Threat_Modeling
- NIST SP 800-12 (Introduction to Information Security), NIST SP 800-30 (Risk Assessment) — https://csrc.nist.gov/pubs/sp/800/12/r1/upd1/final
- MITRE ATT&CK — https://attack.mitre.org/
- Kurose & Ross, *Computer Networking*, 8th ed., §8.1 (What Is Network Security?).

## 18. Cheat Sheet
- CIA: Confidentiality (encryption), Integrity (hash/MAC/signature), Availability (redundancy/DDoS).
- AAA: Authentication, Authorization, Accounting.
- Non-repudiation = digital signatures (private-key signing, public verification).
- STRIDE: Spoofing, Tampering, Repudiation, Info disclosure, DoS, Elevation — the CIA/AAA checklist.
- Encrypt without MAC → bit-flip/tampering; always encrypt-then-MAC.
- Hash = integrity; MAC = integrity + authenticity (shared key); signature = + non-repudiation.
- Least privilege = minimize blast radius (authorization).
- Defense in depth = independent layers, one failure ≠ breach.
- Risk = likelihood × impact; threats exploit vulnerabilities.
- Authenticity ≠ integrity: hash catches changes; signature catches changes *and* origin.

## 19. Quiz
1. A DDoS violates: a) confidentiality b) integrity c) availability d) non-repudiation → **c**
2. A tampered message violates: a) confidentiality b) integrity c) availability d) authentication → **b**
3. Encryption primarily provides: a) integrity b) confidentiality c) non-repudiation d) availability → **b**
4. Non-repudiation is achieved with: a) HMAC b) digital signatures c) AES d) TLS only → **b**
5. AAA does NOT include: a) authentication b) authorization c) accounting d) availability → **d**
6. HMAC provides: a) integrity + authenticity b) confidentiality c) non-repudiation d) availability → **a**
7. Which pairs with integrity? a) Spoofing b) Tampering c) DoS d) Info disclosure → **b**
8. "Only minimum permissions needed" is: a) MFA b) least privilege c) defense in depth d) risk → **b**

**Answers**: 1-c, 2-b, 3-b, 4-b, 5-d, 6-a, 7-b, 8-b.

## 20. Flashcards
- **Q: What are the three CIA pillars and their tools?** → **A:** Confidentiality (encryption), Integrity (hash/MAC/signature), Availability (redundancy/DDoS mitigation).
- **Q: What is AAA?** → **A:** Authentication, Authorization, Accounting.
- **Q: How do you get non-repudiation?** → **A:** Digital signatures (signed with private key, verified with public).
- **Q: Encrypt without MAC — what risk?** → **A:** Tampering/bit-flipping (CBC malleability); use encrypt-then-MAC.
- **Q: What is STRIDE?** → **A:** Spoofing, Tampering, Repudiation, Info disclosure, DoS, Elevation — threat-modeling categories.
- **Q: Integrity vs authenticity?** → **A:** Hash = unchanged; MAC/signature = unchanged + from the right source.
- **Q: What is least privilege?** → **A:** Grant only minimum needed permissions; shrink blast radius.

## 21. Revision
Security = protecting CIA + AAA + non-repudiation. Confidentiality = encryption; Integrity = hash/MAC/signature (and authenticity via keyed MAC); Availability = redundancy + DDoS defense; Authentication/Authorization/Accounting = the identity and audit trio; Non-repudiation = signatures. STRIDE enumerates threats across trust boundaries; risk = likelihood × impact. The classic traps: encrypt-without-MAC (tamperable), hash-without-key (no authenticity), HMAC-without-signature (no non-repudiation). Every protocol question ("how is TLS secure?") is really "which pillars does it enforce?" — TLS gives confidentiality + integrity + server authentication; IPsec the same at L3; SSH adds host auth. Anchor: *a system is secure only when every pillar is enforced independently — one pillar's failure must not breach the others.*

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is the CIA triad?" | 7 / 13-Q1 |
| "Which pillar does X attack violate?" | 13-Q2 |
| "What is AAA?" | 13-Q3 / 7 |
| "Integrity vs confidentiality mechanisms" | 13-Q4 |
| "What is non-repudiation?" | 13-Q5 |
| "Encrypt without MAC — what breaks?" | 13-Q6 / 9 |
| "What is STRIDE?" | 13-Q7 |
| "Authentication vs authorization" | 13-Q11 |
| "How do you prioritize security controls?" | 13-Q10 |
| "Least privilege / defense in depth" | 13-Q15,13 |
