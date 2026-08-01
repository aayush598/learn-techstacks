# Zero Trust Architecture and Best Practices

> **TL;DR**: Zero Trust (ZTNA) abandons the "trusted internal network" model — every request is authenticated, authorized, and encrypted regardless of source; identity and device posture replace the firewall perimeter as the enforcement point (NIST SP 800-207).

## 1. Why Does This Exist?
The traditional **castle-and-moat / perimeter security** model assumes everything *inside* the corporate network is trusted and everything outside is not. That assumption collapsed: cloud apps live outside the perimeter, employees work from anywhere, and attackers routinely *get inside* (phishing, compromised endpoints, insider risk). Once inside, lateral movement is trivial — internal traffic is unauthenticated and unencrypted, so one breach spreads everywhere. **Zero Trust** exists to treat every request as hostile: authenticate and authorize each request against *identity + device + context*, encrypt everything, and deny by default — so "being on the network" grants nothing. This is the BeyondCorp model and is now codified in NIST SP 800-207.

## 2. How Does It Work?
Core model — **never trust, always verify**: 
1. **Every request** is evaluated by a policy decision point (PDP) against: who (identity/SSO/MFA), what (device posture: patched, managed, EDR), where (location/IP), what data/app, and when (context/risk).
2. **Default deny**: access is granted per-request, per-resource (micro-segmentation), not per-network.
3. **Enforcement**: a policy enforcement point (PEP) — an application gateway, service mesh sidecar, or network micro-segmentation — blocks or forwards based on policy.
4. **Everything encrypted** (mTLS, TLS) and **continuously verified** (session revalidation, risk scoring), with full logging.
The *architecture*: an identity-aware proxy in front of apps (Cloudflare Access, Google IAP), service meshes (Istio mTLS) inside, and micro-segmentation at the network (NSX) or L7 (app-aware) level.

## 3. When Is It Used?
- **Remote workforce**: employees access SaaS/corp apps via identity + MFA from any device — no VPN needed (ZTNA replaces VPN).
- **Cloud**: access to cloud console, APIs, and databases is identity-scoped with short-lived credentials (IAM, workload identity).
- **Service-to-service**: mTLS in service meshes (Istio, Linkerd) and pod identity in Kubernetes.
- **Third-party/contractors**: granular, time-boxed access to specific apps only.
- **Data exfiltration protection**: DLP + policy on sensitive data flows.
- **Compliance**: many frameworks (SOC2, FedRAMP, NIST) now expect ZTA principles for cloud and remote access.

## 4. Why Wasn't Another Approach Chosen?
- *Alternative: just harden the firewall perimeter.* Doesn't help when insiders/attackers are already inside (phishing, leaked creds); cloud and remote access make the perimeter meaningless. Zero Trust moves the "perimeter" to *every resource*.
- *Alternative: trust the network, secure the app.* App-only security ignores the blast radius — an app compromise gives the attacker the whole network. ZT adds per-request authz and segmentation so one app compromise doesn't mean everything is reachable.
- *Alternative: everything through a big VPN.* Classic VPN gives blanket network access (the opposite of least privilege) and creates a single choke point. ZTNA gives per-app, per-identity access.
- *Alternative: only encryption.* Encryption protects in transit but doesn't say *who* gets access — ZT combines encryption (mTLS) with authentication *and authorization* per request.
- *Alternative: MFA only.* MFA stops credential theft but not compromised/rogue devices or insider misuse; ZT adds device posture + continuous risk evaluation.

## 5. Intuition
The old model: the network is a **gated community** — show a badge at the front gate (firewall/VPN), then you can wander into any house (host). Zero Trust: every house has its own locked door, a security guard who checks your ID + your guest pass *for that specific house* each visit, and the street between houses has security cameras and locked gates (mTLS everywhere). Being inside the walls grants nothing — the trust is per-door, per-visit, continuously rechecked. If a guest turns out to be a thief (compromised account), they can only open doors they have a pass for, and their movement is logged.

## 6. Real-World Analogy
A **high-security office floor**. Badge readers (PDP) at *every* office door, not just the front entrance. To enter the server room (DB), you need: valid ID (identity), active clearance (authorization), a phone that's not jailbroken (device posture), and a reason at this hour (context). The lobby is no longer "safe" — the cafeteria (shared network) is untrusted too. A visitor (contractor) gets a badge that only opens the conference room (per-app access) for today (time-boxed), and every door opening is logged. If a badge is cloned (compromised account), it opens only what that badge could open, and the anomaly (swipe at 3am from another city) triggers an alert. This is Zero Trust's physical form: the perimeter is gone; trust is per-door, per-person, per-request.

## 7. Formal Definition
NIST SP 800-207 defines the **Zero Trust Architecture (ZTA)**:
- **Core concepts**: no implicit trust based on network location; access determined by dynamic policy (identity, device, resource, environment); monitoring all assets, all traffic (encrypted); policy is comprehensive (least privilege); risk-based, continuously evaluated.
- **Components**: **Policy Decision Point (PDP)** — decides; **Policy Engine (PE)** + **Policy Administrator (PA)** — make and enforce the decision; **Policy Enforcement Point (PEP)** — executes (gateway/sidecar/agent). 
- **Control plane** (PDP, PA, policy metadata) vs **data plane** (PEP, app, data flows).
- **ZT principles (pillars)**: verify explicitly (every request), use least privilege (per-request), assume breach (segment, encrypt, monitor).
- **Identity**: SSO, MFA, short-lived credentials; **device**: posture, compliance, EDR; **network**: micro-segmentation, mTLS, encryption in transit (and at rest).
- Related: **SDP (Software-Defined Perimeter)** — "dark cloud"/black cloud: apps are invisible until identity is verified; **ZTNA** = ZT applied to network access, typically via an identity-aware proxy in front of apps.

## 8. Example
**A ZTNA request flow (BeyondCorp / Cloudflare Access-style):**
```
Employee (laptop, corp-managed)  →  requests app.internal.corp
  1. No VPN. The request hits the ZTNA proxy (PEP).
  2. Proxy redirects to IdP: SSO login + MFA (time-based one-time pass).
  3. PDP evaluates: identity ✓ (corp employee), device ✓ (managed, EDR healthy,
     OS patched, not rooted), context ✓ (country matches, time normal),
     resource ✓ (this user's role permits this app), risk low.
  4. Decision: ALLOW, issue short-lived (e.g., 5-min) signed session/JWT to the proxy.
  5. PEP forwards the request to the app over mTLS/TLS; response flows back.
  6. Every request revalidated (short session TTL); all events logged to SIEM.
  If any signal degrades (device flips unhealthy, MFA expires): DENY on next check.
```

## 9. Internal Working
1. **Identity establishment**: SSO (OIDC/SAML) + MFA establishes who; a short-lived session token (JWT with expiry) is the basis for each PDP decision.
2. **Device trust**: the device agent reports posture (OS, patch level, EDR status, disk encryption, jailbreak/root); policies require healthy posture for sensitive access.
3. **Dynamic policy evaluation**: PDP combines identity, device, resource sensitivity, location, time, and real-time risk (anomaly detection, threat intel) to decide; decisions are *per-request*, re-evaluated continuously (short TTLs).
4. **Enforcement**: PEP (reverse proxy/gateway, service-mesh sidecar, or endpoint agent) blocks/forwards; with SDP, unreachable unless authenticated (apps are "black cloud").
5. **Encryption everywhere**: mTLS between services (service mesh), TLS to apps, TLS to endpoints — traffic is encrypted even inside the datacenter (assume breach).
6. **Micro-segmentation**: network (VLAN/NSX, policy per workload) or L7 (policy per app/API) — limits blast radius and lateral movement.
7. **Continuous verification & logging**: revalidate sessions/device, score risk, log every access for detection and forensics.

## 10. Time Complexity / Performance
- **Latency**: each request goes through a PDP check + proxy hop — a few ms to tens of ms; mitigated by local policy caching and short-lived sessions. Not a correctness issue but a real design constraint (per-request authz must be fast).
- **Scale**: ZTNA gateways and PDPs must handle SSO bursts and high request rates (stateless decisions, cached policy); service meshes add per-pod mTLS overhead (small, AES-NI).
- **mTLS cost**: key distribution at scale (SPIFFE/SPIRE), rotation, and cert lifecycle — automation is essential; handshake overhead on new connections.
- **Operational cost**: identity orchestration, device management (MDM), posture agents, and SIEM/log pipelines are significant; the payoff is breach containment.

## 11. Advantages
- **Breach containment**: compromised identity/endpoint only reaches the resources it's authorized for — lateral movement is blocked.
- **Remote-first ready**: works from anywhere (no VPN dependency); consistent access to cloud and on-prem.
- **Least privilege enforced per request** — not "member of network = full trust."
- **Visibility**: every request authenticated, authorized, logged — detection and forensics vastly better.
- **Adaptive/risk-based**: suspicious context (new device, foreign IP) triggers step-up auth or denial.
- **Encryption everywhere**: assume-breach mindset protects internal flows too (mTLS).

## 12. Disadvantages
- **Migration cost & complexity**: legacy apps, protocols (non-HTTP), and on-prem systems are hard to wrap in identity proxies.
- **Performance**: added proxy/PDP hop latency; mTLS and posture checks add overhead and friction.
- **Endpoint dependency**: ZT trusts device signals heavily — a compromised *agent* or unmanaged device weakens the model (though risk scoring helps).
- **Identity is the new perimeter**: SSO compromise or MFA fatigue attacks become the critical target — a single identity breach is now the top concern.
- **Operational burden**: cert rotation (mTLS), device management, policy sprawl, and SIEM tuning.
- **Not a silver bullet**: still needs DLP, patching, and endpoint detection; ZT assumes the host is healthy but doesn't by itself stop malware on an allowed device.

## 13. Interview Questions
1. **Q: What is Zero Trust?** A: The security model of "never trust, always verify": no implicit trust based on network location; every request is authenticated, authorized, and encrypted against identity + device + context, with default-deny and least privilege. Codified in NIST SP 800-207.

2. **Q: Why does the perimeter model fail?** A: Cloud apps and remote work put trusted resources outside the network; attackers get inside via phishing/compromised endpoints; internal traffic is then unauthenticated, so lateral movement spreads one breach everywhere. ZT makes "being on the network" grant nothing.

3. **Q: What are the pillars of Zero Trust?** A: (1) Verify explicitly — every request; (2) Use least privilege — per-request, per-resource; (3) Assume breach — segment, encrypt (mTLS), and monitor everywhere. Plus: continuous evaluation and full visibility.

4. **Q: What are PDP and PEP?** A: PDP = Policy Decision Point (decides — the policy engine/administrator); PEP = Policy Enforcement Point (executes — gateway, sidecar, agent). Control plane (PDP/policy) vs data plane (PEP/traffic) separation is a key ZTA design.

5. **Q: How is ZTNA different from a VPN?** A: VPN grants blanket network access (least privilege violated) and a single choke point. ZTNA grants per-app, per-identity, per-request access via an identity-aware proxy — no network membership granted, works from any location, denies by default.

6. **Q: What is micro-segmentation?** A: Splitting the network into fine-grained zones with per-workload/per-app policy so a compromise in one segment can't reach others — implemented at L2/L3 (VLANs, NSX) or L7 (service mesh/app-aware policies). Limits blast radius and lateral movement.

7. **Q: TRICKY — What role does mTLS play in Zero Trust?** A: mTLS provides *mutual* authentication and encryption between every service — proving both ends are who they claim and encrypting internal flows. This operationalizes "assume breach": even inside the network, traffic is authenticated and encrypted. In service meshes (Istio), mTLS + per-request policy = ZT for service-to-service.

8. **Q: How does device posture factor into ZT?** A: Before (and while) granting access, the PEP checks the device agent's report: OS patched, disk encrypted, EDR present, not rooted/jailbroken. Unhealthy device → restricted/denied access. This is how ZT mitigates compromised/rogue endpoints.

9. **Q: What is a "risk score"/adaptive access?** A: The PDP continuously evaluates context (IP, location, time, device, behavior anomalies, threat intel) into a risk score; risky access triggers step-up auth (MFA), reduced scope, or denial — access is dynamic, not a static grant.

10. **Q: PRODUCTION — Migrating 200 legacy apps to Zero Trust. What breaks and how do you proceed?** A: (1) Non-HTTP protocols (database, SSH, RDP, proprietary) need special handling (agents, proxies, or gateway support); (2) apps with embedded credentials/static IP whitelists conflict with identity-based access; (3) service accounts and machine identity (SPIFFE/SPIRE); (4) performance expectations (proxy hop). Strategy: classify apps by sensitivity, use an identity-aware proxy + connector for web, mTLS mesh for services, agents for SSH/DB, and roll out incrementally with policy monitoring; set per-app, deny-by-default rules.

11. **Q: What is BeyondCorp?** A: Google's original ZT implementation (2011 paper): employees access internal apps over the public internet via the BeyondCorp proxy, with access decisions based on device inventory + user identity, and zero network-level trust. It's the canonical reference deployment of ZTA.

12. **Q: TRICKY — "Identity is the new perimeter." What are the implications?** A: Since ZT removes network trust, the credential/SSO becomes the critical attack surface: MFA fatigue attacks, token theft (pass-the-cookie), and IdP compromise become the highest-impact attacks. Mitigations: phishing-resistant MFA (WebAuthn/FIDO2), short-lived tokens, device binding of sessions, anomaly detection, and strong IdP controls.

13. **Q: What is a Software-Defined Perimeter (SDP)?** A: An overlay that keeps apps invisible ("black cloud") until a request is authenticated and authorized; the PEP then establishes a connection. Combines identity-based access with obscuring attack surface — a core ZTNA mechanism (e.g., Cloudflare Access, AppGate).

14. **Q: What is the difference between ZT for humans vs machine identities?** A: Humans: SSO/MFA/device posture via agents. Machines (services, workloads, IoT): mTLS certs, workload identity (SPIFFE/SPIRE, cloud IAM roles, Kubernetes service accounts), short-lived credentials, and rotation. Both follow the same "verify every request" principle but with different identity stores.

15. **Q: SCENARIO — An employee's account is compromised. Why does ZT limit the damage?** A: The attacker can only reach the specific apps the account is authorized for (per-request default-deny), can't move laterally to other segments, faces step-up MFA if context looks anomalous, and every action is logged (rapid detection/revocation). With short-lived sessions/tokens, revocation takes effect quickly. Contrast: a VPN gives the attacker the whole network.

16. **Q: What is "just-in-time" (JIT) access?** A: Privileged/administrative access is granted on demand for a short window (e.g., 15 minutes) after approval/justification, then automatically revoked — rather than permanent standing privileges. Reduces the attack surface of always-on admin accounts. A core ZT access pattern for ops.

17. **Q: PRODUCTION — Design ZTA for a multi-cloud SaaS company.** A: (1) Identity: OIDC SSO + FIDO2 MFA, short-lived tokens; (2) ZTNA proxy in front of all web apps (cloud + on-prem connectors); (3) service mesh (Istio) with mTLS + per-service policies in K8s; (4) workload identity via SPIFFE/IAM roles — no static keys; (5) micro-segmentation + egress filtering per environment; (6) continuous risk scoring, SIEM + SOAR, DLP; (7) automated cert/secret rotation and posture agents on endpoints; (8) fail-closed policy, audit everything. Emphasize: identity-first, least privilege, assume breach.

## 14. Follow-Up Questions
1. **Q: What does NIST SP 800-207 actually require?** A: It defines ZTA as an architecture (not a product) with seven tenets (e.g., all data sources/computing considered resources; all communication secured; access granted per-session; policies based on the full resource; monitor all assets/traffic; dynamic policy; collect telemetry). It maps to the PDP/PEP model and describes deployment patterns (SDP, enhanced IAM, micro-segmentation).

2. **Q: What is the difference between a "policy engine" and a "policy administrator"?** A: The Policy Engine (PE) computes the decision from policies + signals; the Policy Administrator (PA) communicates that decision to the PEP and manages the session's crypto/material. Both are part of the PDP. The PEP just executes.

3. **Q: How do you handle OT/IoT or devices that can't run an agent?** A: Network micro-segmentation + device fingerprinting/NAC + dedicated VLANs with deny-by-default egress + hardware identity (certificates via TPM) where possible; such devices are a recognized ZTA gap — compensate with strict segmentation and monitoring.

4. **Q: What is "MAC" (network access control) vs ZT?** A: NAC authenticates devices *at network entry* (802.1X) but then grants network membership — still network-level trust. ZT grants per-request access and keeps evaluating; NAC is a component, not the full model.

## 15. Coding Example
```bash
# Typical ZTNA-adjacent operational checks on the enforcement path
# 1. Enforce TLS + view the proxy's handshake (ZTNA gateway logs equivalent)
curl -sSI https://app.internal.corp | grep -iE "HTTP/|server|set-cookie"   # session = short-lived

# 2. mTLS / service mesh: test that the sidecar requires a client cert
curl -s -o /dev/null -w "%{http_code}\n" https://svc.internal:8443          # -> 401/403 (no client cert)
curl -s -o /dev/null -w "%{http_code}\n" \
     --cert client.crt --key client.key https://svc.internal:8443           # -> 200 (mTLS identity ok)

# 3. Rotate short-lived workload identity (K8s service account token — JIT-like)
kubectl create token mysa --duration=15m        # short-lived token (no standing secret)

# 4. Micro-segmentation verification — show that cross-namespace is denied by default
kubectl get networkpolicy --all-namespaces      # list policies; default-deny = none for internal
kubectl auth can-i --as=system:serviceaccount:team-a:svc create pods --all-namespaces  # check permission
```
```python
# Minimal PDP-style decision (per-request allow/deny, deny by default)
def evaluate(identity, device, resource, risk_score):
    if not identity.authenticated or not identity.mfa:     # verify explicitly
        return "DENY"
    if device.patched is False or device.edr is None:      # device posture
        return "DENY"
    if resource not in identity.allowed_resources:          # least privilege
        return "DENY"
    if risk_score > 70:                                      # adaptive access
        return "DENY_OR_STEP_UP"
    return "ALLOW"
```
```bash
# Audit trail wiring (log everything — assume breach)
# proxy logs → SIEM; mTLS SPIFFE identity shown per request:
journalctl -u ztna-proxy | jq 'select(.user!="") | {user, app, device, risk, decision}'
```

## 16. Industry Usage
- **Google BeyondCorp** (2011 → GA 2020): the canonical ZTA.
- **Cloudflare Zero Trust / Access / WARP**: ZTNA in front of apps, mTLS, device posture, network-level filtering.
- **Microsoft Entra (Azure AD)**: Conditional Access, Identity Protection, ZTNA for M365/Entra apps.
- **Google Cloud IAP / Cloud Armor**: identity-aware access to GCP apps and workloads.
- **Service meshes**: Istio/Linkerd mTLS + AuthorizationPolicy — ZT for service-to-service.
- **AWS**: IAM roles, workload identity (IRSA), VPC Lattice (mTLS + policies), and NACL/security-group micro-segmentation.
- **Tailscale/Zero Trust overlays**: mesh VPNs with SSO + device posture.
- **Compliance**: NIST SP 800-207, CISA ZT Maturity Model, zero-trust requirements in FedRAMP/DISA.

## 17. References
- NIST SP 800-207, *Zero Trust Architecture* — https://csrc.nist.gov/pubs/sp/800/207/final
- NIST SP 800-207A (Zero Trust for Cloud) — https://csrc.nist.gov/pubs/sp/800/207a/final
- Google BeyondCorp paper — https://research.google/pubs/pub43231/
- CISA Zero Trust Maturity Model — https://www.cisa.gov/zero-trust-maturity-model
- Cloudflare Zero Trust docs — https://developers.cloudflare.com/cloudflare-one/
- Istio security/mTLS docs — https://istio.io/latest/docs/concepts/security/

## 18. Cheat Sheet
- Zero Trust = "never trust, always verify": no implicit network trust; every request authenticated + authorized + encrypted.
- Pillars: verify explicitly, least privilege (per-request), assume breach (segment + encrypt + monitor).
- NIST SP 800-207 model: PDP (PE + PA decides) vs PEP (executes); control plane vs data plane.
- ZTNA (identity-aware proxy) replaces VPN: per-app, per-identity, deny-by-default; SDP = "black cloud" until verified.
- Pillars of enforcement: SSO + MFA + short-lived tokens; device posture agents; mTLS everywhere; micro-segmentation (L2/L7).
- Adaptive/risk-based access: context anomalies → step-up MFA or deny.
- "Identity is the new perimeter" — MFA fatigue/pass-the-cookie are top threats; use FIDO2.
- Just-in-time (JIT) privileged access: grant on demand, auto-revoke.
- Migrate legacy: classify apps, proxy web apps, mTLS mesh for services, agents for SSH/DB, incremental rollout.

## 19. Quiz
1. Zero Trust's core assumption: a) network is trusted b) every request is hostile c) VPN is enough d) MFA replaces everything → **b**
2. Which NIST doc defines ZTA? a) 800-53 b) 800-207 c) 800-171 d) 800-190 → **b**
3. The component that *executes* the decision: a) PDP b) PEP c) PE d) PA → **b**
4. ZTNA grants access to: a) the network b) specific apps c) the whole subnet d) IP ranges → **b**
5. "Assume breach" means: a) always deny b) segment, encrypt, monitor everywhere c) use MFA d) block external IPs → **b**
6. mTLS provides: a) only encryption b) mutual auth + encryption c) only auth d) compression → **b**
7. JIT access means: a) always-on admin b) on-demand short-lived privilege c) just-in-time VPN d) 24/7 access → **b**
8. The new critical attack surface: a) firewall b) identity c) VLANs d) DNS → **b**

**Answers**: 1-b, 2-b, 3-b, 4-b, 5-b, 6-b, 7-b, 8-b.

## 20. Flashcards
- **Q: Define Zero Trust** → **A:** Never trust, always verify — every request authenticated, authorized, encrypted; deny by default.
- **Q: Pillars?** → **A:** Verify explicitly; least privilege; assume breach (segment, encrypt, monitor).
- **Q: PDP vs PEP** → **A:** PDP decides (policy engine/administrator); PEP executes (gateway/sidecar/agent).
- **Q: ZTNA vs VPN** → **A:** Per-app/per-identity access vs blanket network membership.
- **Q: What is micro-segmentation?** → **A:** Fine-grained per-workload policy limiting lateral movement.
- **Q: Role of mTLS in ZT** → **A:** Mutual auth + encryption for all service traffic (assume breach).
- **Q: Why is identity the new perimeter?** → **A:** No network trust → credential/SSO compromise is the top risk; need FIDO2 + short-lived tokens.

## 21. Revision
Zero Trust (NIST SP 800-207) replaces perimeter trust with per-request verification: PDP (policy engine + administrator) decides against identity, device posture, resource sensitivity, and context; PEP (proxy/sidecar/agent) enforces; default-deny, least privilege. ZTNA applies this to access via identity-aware proxies (per-app, no VPN membership); SDP hides apps until verified. Enforcement stack: SSO + MFA (FIDO2) + short-lived tokens, device posture agents, mTLS everywhere (service mesh), micro-segmentation (L2/L7), continuous risk scoring, JIT privileged access, full logging. The trade-off is the new attack surface: identity itself (MFA fatigue, pass-the-cookie). Migration: classify apps, proxy web apps, mTLS for services, agents for SSH/DB, incremental deny-by-default rollout. Anchors: *never trust always verify; PDP decides / PEP enforces; verify + least privilege + assume breach; ZTNA = per-app access without network membership; mTLS everywhere operationalizes assume breach.*

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is Zero Trust?" | 13-Q1 |
| "Why does the perimeter fail?" | 13-Q2 |
| "Pillars of ZT" | 13-Q3 |
| "PDP vs PEP" | 13-Q4 |
| "ZTNA vs VPN" | 13-Q5 |
| "What is micro-segmentation?" | 13-Q6 |
| "Role of mTLS" | 13-Q7 |
| "Device posture" | 13-Q8 |
| "Adaptive/risk-based access" | 13-Q9 |
| "Legacy app migration to ZT" | 13-Q10 |
| "What is BeyondCorp?" | 13-Q11 |
| "Identity as the new perimeter" | 13-Q12 |
| "What is an SDP?" | 13-Q13 |
| "JIT access" | 13-Q16 |
| "Design ZTA for multi-cloud SaaS" | 13-Q17 |
