# Authentication Protocols for iPACE-CHIP

## Overview

Authentication in the iPACE-CHIP implantable pacemaker ecosystem ensures that
every communication partner is verified before any sensitive operation occurs.
A failed authentication could allow an attacker to assume control of the
pacemaker, while a missing authentication check could allow unauthorized access
to patient data. This chapter covers mutual authentication, device attestation,
and the multi-factor authentication framework that protects the implant.

## 1. Authentication Architecture

### 1.1 Trust Model

The iPACE-CHIP operates in a zero-trust environment where no communication
channel is inherently trusted. Authentication is required before:

- Establishing any communication session
- Executing therapy parameter changes
- Accessing stored telemetry data
- Performing firmware updates
- Rotating cryptographic keys
- Modifying device configuration

### 1.2 Authentication Factors

The iPACE-CHIP implements three authentication factors:

| Factor | Implementation | Strength |
|--------|---------------|----------|
| Something you have | Programmer certificate + private key | X.509 certificate chain |
| Something you know | Patient PIN (6-12 digits) | 20-40 bit entropy |
| Something you are | Patient biometric (fingerprint) | 1:50,000 FAR |

### 1.3 Authentication Levels

| Level | Factors Required | Operations Allowed |
|-------|-----------------|-------------------|
| AL1 (Basic) | Certificate only | Read telemetry, view status |
| AL2 (Standard) | Certificate + PIN | Adjust monitoring parameters |
| AL3 (Elevated) | Certificate + PIN + Biometric | Modify therapy, firmware update |
| AL4 (Emergency) | Certificate + Emergency Code | Emergency override, clinician access |

## 2. Device Authentication Protocols

### 2.1 Programmer-to-Implant Mutual Authentication

The iPACE-CHIP implements a custom mutual authentication protocol based on
ECDSA and ECDH, providing both identity verification and key establishment
in a single round-trip:

```
Protocol: iPACE-MAP (Mutual Authentication Protocol)

Message 1: Programmer → Implant
  [Certificate_P (DER encoded)]
  [Nonce_P (32 bytes, random)]
  [Timestamp_P (8 bytes, UTC)]

Message 2: Implant → Programmer
  [Certificate_I (DER encoded)]
  [Nonce_I (32 bytes, random)]
  [Timestamp_I (8 bytes, UTC)]
  [Sign_ECDSA(d_I, Hash(Cert_P || Nonce_P || Nonce_I || Timestamp_P || Timestamp_I))]

Message 3: Programmer → Implant
  [Sign_ECDSA(d_P, Hash(Cert_I || Nonce_P || Nonce_I || Timestamp_P || Timestamp_I))]
  [ECDH_Public_P (uncompressed point, 64 bytes)]

Message 4: Implant → Programmer
  [ECDH_Public_I (uncompressed point, 64 bytes)]
  [Sign_ECDSA(d_I, Hash(ECDH_Public_P || ECDH_Public_I || Nonce_P || Nonce_I))]
```

**Security Properties:**

- **Mutual authentication:** Both parties verify each other's certificate chain
- **Freshness:** Nonces prevent replay attacks
- **Key establishment:** ECDH provides forward-secret shared secret
- **Binding:** Signatures bind the key exchange to the authentication

### 2.2 Certificate Chain Verification

Each device certificate is verified against the manufacturer's certificate chain:

```
Verification Steps:
  1. Parse certificate DER encoding
  2. Verify signature: Issuer_Cert.verify(Cert.SignedCert)
  3. Check validity period (NotBefore ≤ now ≤ NotAfter)
  4. Verify Key Usage extension (digitalSignature for ECDSA)
  5. Check certificate policy OID matches iPACE-CHIP policy
  6. Verify Subject Alternative Name contains device serial number
  7. Check against revocation list (if available)
  8. Verify certificate pinning (if previously paired)
```

**Certificate Validation Time:**

| Step | Time (ARM Cortex-M4) |
|------|---------------------|
| Parse DER | 0.8 ms |
| ECDSA verify (P-256) | 62 ms |
| Policy checks | 0.2 ms |
| **Total per certificate** | **63 ms** |
| **Full chain (3 certs)** | **189 ms** |

### 2.3 Device Attestation

The iPACE-CHIP provides a hardware-backed attestation capability that proves
the device's identity and integrity to a remote verifier:

```
Attestation Protocol:

Verifier → Implant: Challenge(nonce_V, nonce_I)
Implant → Verifier: Attestation_Report {
    Device_ID: 32 bits
    Firmware_Version: 32 bits
    Security_Security_Security_Security_Security_Security_Security_Security_Security_Security_Security
    Boot_Counter: 32 bits
    Tamper_Status: 8 bits
    Certificate_I: DER encoded
    Sign_ECDSA(d_attest, Hash(device_state || nonce_V || nonce_I))
    ECDH_Public_attest: 64 bytes
}
```

The attestation key is derived from the device root key and a fixed context
string, ensuring only the genuine device can produce valid attestation reports.

## 3. Patient Authentication

### 3.1 Patient Identification Protocol

Patient authentication for the iPACE-CHIP uses a multi-step process mediated
through the patient controller (smartphone application):

```
Step 1: Patient initiates session on controller app
  - App verifies patient biometric (fingerprint/face)
  - App unlocks stored patient credentials

Step 2: Controller authenticates to implant via BLE
  - LE Secure Connections pairing
  - Certificate-based mutual authentication (AL1)

Step 3: Patient PIN entry (for AL2+)
  - PIN entered on controller
  - PIN verified using OPAQUE (PAKE protocol)
  - No PIN transmitted over wireless channel

Step 4: Biometric verification (for AL3)
  - Fingerprint sensor on patient controller
  - Biometric template stored locally, never transmitted
  - Verification result sent as signed assertion
```

### 3.2 PIN-Based Authentication (OPAQUE)

The iPACE-CHIP uses OPAQUE (Oblivious Pseudo-Random Function Asymmetric PAKE)
for PIN-based authentication. This protocol ensures that the PIN never leaves
the patient controller and is never transmitted over the wireless channel:

```
OPAQUE Registration (one-time):
  Client: r, u = Hash(PIN || salt), OPRF_output = u^r
  Server: stores (u^r, salt) — never sees PIN

OPAQUE Authentication:
  1. Client sends: alpha = a^r (random blinded value)
  2. Server responds: beta = alpha * OPRF_output = (a*u)^r
  3. Client computes: OPRF_result = beta^(1/r) = a*u
  4. Client derives: session_key = KDF(OPRF_result)
  5. Client sends: Auth = MAC(session_key, "client_auth")
  6. Server verifies: Auth against expected MAC
```

**Security Properties:**

- The server (implant) never learns the PIN
- The PIN has no mathematical relationship to the transmitted values
- Offline dictionary attacks are prevented by the OPRF structure
- Compromise of the server's stored value does not enable PIN recovery

### 3.3 Biometric Authentication

The patient controller's biometric sensor (fingerprint) provides a third
authentication factor:

```
Biometric Flow:
  1. Patient places finger on sensor
  2. Sensor extracts minutiae template (FAR < 1:50,000)
  3. Template matched against enrolled template (stored in secure enclave)
  4. On match: controller signs assertion with biometric_verified flag
  5. Assertion sent to implant: Sign_SK_controller(Hash(biometric_assertion))
  6. Implant verifies assertion signature and biometric_verified flag
```

**Privacy Protection:**

- Biometric data never leaves the patient controller
- Only a signed boolean assertion is transmitted
- Biometric template encrypted with controller's secure enclave key
- Template deletion on controller compromise detection

## 4. Emergency Authentication

### 4.1 Emergency Access Protocol

When normal authentication channels are unavailable (e.g., patient unconscious,
controller battery depleted), emergency access is possible through a clinician
override:

```
Emergency Protocol:

Clinician → Implant: Emergency_Request {
    Clinician_Certificate (hospital-issued)
    Emergency_Code (8-digit code, printed on implant card)
    Nonce_C
}

Implant:
  1. Verify Clinician_Certificate chain (hospital CA)
  2. Verify Emergency_Code against stored hash
  3. Compute emergency_key = KDF(emergency_code, nonce_C, "emergency")
  4. Respond: Emergency_Auth_Response {
      Implant_Certificate
      Nonce_I
      Sign(d_I, Hash(emergency_code_hash || nonce_C || nonce_I))
    }

Clinician → Implant: Emergency_Auth_Confirm {
    Sign(d_C, Hash(Nonce_I || emergency_scope))
    Emergency_Scope: {
      Duration: 30 minutes
      Allowed_Operations: [read_status, adjust_pacing, disable_pacing]
      Logging: mandatory
    }
}
```

### 4.2 Emergency Access Restrictions

| Restriction | Value | Rationale |
|------------|-------|-----------|
| Maximum duration | 30 minutes | Limit exposure window |
| Allowed operations | Read, adjust, disable | Not: firmware update, key rotation |
| Audit logging | Mandatory, signed | Non-repudiable record |
| Automatic lockout | After 3 emergency accesses | Prevent abuse |
| Cooldown period | 24 hours after 3rd emergency | Force secure re-pairing |

### 4.3 Lost/Stolen Controller Protocol

If the patient controller is lost or compromised:

```
Revocation Protocol:
  1. Patient (or clinician) contacts iPACE-CHIP support
  2. Support verifies patient identity (out-of-band)
  3. Revocation command signed by support key
  4. Implant receives revocation via MICS (if in range) or
     at next NFC programming session
  5. Implant:
     a. Invalidates all session keys for the revoked controller
     b. Clears paired device entry
     c. Enters "unpaired" mode
     d. Logs revocation event
  6. New pairing requires physical proximity (NFC)
```

## 5. Session Authentication

### 5.1 Session Establishment

Each communication session begins with a session establishment phase:

```
Session Setup:
  1. Physical proximity verification (NFC tap or BLE within 1m)
  2. Device mutual authentication (Section 2.1)
  3. Session key derivation (HKDF-SHA256)
  4. Session parameter negotiation:
     - Encryption algorithm (AES-128-GCM or ASCON-128)
     - Authentication level required
     - Session timeout
     - Maximum message size
  5. Session initialization complete
```

### 5.2 Session Resumption

To reduce authentication overhead for frequent connections, the iPACE-CHIP
supports session resumption:

```
Session Resumption Protocol:
  1. Client sends: session_ticket (encrypted with server key)
  2. Server decrypts ticket, extracts session parameters
  3. Server sends: NewNonce_S || Sign(d_S, Hash(session_ticket || NewNonce_S))
  4. Client verifies signature
  5. New session key = KDF(old_session_key, NewNonce_S || NewNonce_C)
```

**Resumption Security:**

- Session tickets expire after 24 hours
- Maximum 10 resumptions per original session
- Forward secrecy maintained through fresh ECDH
- Compromised ticket does not expose original session

### 5.3 Session Timeout and Re-authentication

| Parameter | Value |
|-----------|-------|
| Session idle timeout | 5 minutes |
| Session absolute timeout | 1 hour |
| Maximum messages per session | 2^20 |
| Re-authentication trigger | Policy change request |
| Emergency override timeout | 30 minutes |

## 6. Multi-Party Authentication

### 6.1 Clinician-Patient-Implant Three-Way Auth

For therapy modifications, the iPACE-CHIP requires authentication from both
the clinician and the patient:

```
Three-Way Authentication:
  1. Clinician authenticates (AL3: certificate + hospital credentials)
  2. Patient authenticates (AL2: PIN via OPAQUE)
  3. Both parties sign the therapy modification request:
     Request = {
       New_Parameters: {pacing_rate, voltage, pulse_width}
       Clinician_Signature: Sign(d_C, Hash(params))
       Patient_Signature: Sign(d_P, Hash(params))
     }
  4. Implant verifies both signatures
  5. Implant signs acceptance: Sign(d_I, Hash(request))
  6. All three signatures stored in audit log
```

### 6.2 Remote Programming Authentication

For remote programming (telehealth), additional authentication measures apply:

- VPN tunnel to hospital network (IPsec/IKEv2)
- Certificate pinning to hospital infrastructure
- Real-time video verification of clinician identity
- Patient consent confirmation via controller
- Two-person rule for critical parameter changes

## 7. Authentication Failure Handling

### 7.1 Failure Response Matrix

| Failure Type | Response | Duration | Recovery |
|-------------|----------|----------|----------|
| Certificate invalid | Reject, log | Immediate | Re-pair |
| Signature invalid | Reject, log | Immediate | Retry |
| PIN wrong (1-2 times) | Reject, log | Immediate | Retry |
| PIN wrong (3 times) | Lockout | 15 minutes | Timeout |
| PIN wrong (5 times) | Permanent lockout | Until clinician reset | Physical visit |
| Biometric mismatch | Reject | Immediate | Retry |
| Session ticket invalid | Full auth required | Immediate | New session |
| Emergency code wrong | Reject, log alert | Immediate | Contact support |

### 7.2 Brute Force Protection

**Rate Limiting:**

- Maximum 3 authentication attempts per 5-minute window
- Progressive delay: 1s, 2s, 4s between attempts
- Lockout after 5 failed attempts in 1 hour

**Account Lockout:**

```
Lockout escalation:
  3 failures → 15-minute lockout
  5 failures → 24-hour lockout
  7 failures → permanent lockout (requires clinician reset)
  Emergency code failures → alert to support center
```

### 7.3 Anomaly Detection

The iPACE-CHIP monitors authentication patterns for anomalies:

```
Anomaly Indicators:
  - Authentication at unusual time of day
  - Authentication from unusual geographic location
  - Rapid successive authentication attempts
  - Authentication following failed attempts from different device
  - Emergency access outside hospital hours
```

## 8. Implementation Details

### 8.1 Cryptographic Primitives for Authentication

| Primitive | Usage | Implementation |
|-----------|-------|---------------|
| ECDSA P-256 | Digital signatures | Hardware-accelerated |
| ECDH P-256 | Key agreement | Hardware-accelerated |
| HMAC-SHA256 | MAC operations | Software (optimized) |
| HKDF-SHA256 | Key derivation | Software |
| OPAQUE | PIN authentication | Software (constant-time) |
| AES-128-CMAC | Fast MAC | Hardware-accelerated |
| SHA-256 | Hashing | Hardware-accelerated |

### 8.2 Authentication State Machine

```
States:
  IDLE → DISCOVERY → CERT_EXCHANGE → MUTUAL_AUTH → KEY_ESTABLISH →
  SESSION_ACTIVE → (timeout) → IDLE

  SESSION_ACTIVE → POLICY_CHANGE → MULTI_PARTY_AUTH → SESSION_ACTIVE

  Any state → FAILURE → LOCKOUT → (timeout) → IDLE
  Any state → EMERGENCY → EMERGENCY_ACTIVE → (30min timeout) → IDLE
```

### 8.3 Timing Requirements

| Operation | Maximum Time | Actual Time |
|-----------|-------------|-------------|
| Certificate verify | 200 ms | 189 ms |
| ECDH key exchange | 150 ms | 104 ms |
| OPAQUE verification | 500 ms | 320 ms |
| Biometric assertion verify | 100 ms | 45 ms |
| Full AL3 authentication | 2 seconds | 1.2 seconds |
| Session resumption | 500 ms | 380 ms |

### 8.4 Security Token Format

```
iPACE Authentication Token:
  Header:
    Version: 1 (1 byte)
    Token_Type: 0x01=auth_request, 0x02=auth_response (1 byte)
    Auth_Level: AL1-AL4 (1 byte)
    Timestamp: UTC 8 bytes
  Body:
    Device_Certificate: variable length
    Nonce: 32 bytes
    Signature: 64 bytes (ECDSA)
  Trailer:
    ECDH_Public_Key: 64 bytes (optional)
    HMAC: 32 bytes (over Header+Body)
```

## 9. Formal Verification

### 9.1 Protocol Security Proofs

The iPACE-MAP protocol has been analyzed using the Tamarin prover with the
following verified properties:

```
Verified Properties:
  ✅ Mutual authentication (both parties authenticated)
  ✅ Key secrecy (established key not derivable by adversary)
  ✅ Forward secrecy (session key secure after session ends)
  ✅ Replay protection (fresh nonces in all messages)
  ✅ Certificate binding (signatures bound to correct certificates)
  ✅ No unknown key-share (adversary cannot impersonate either party)
```

### 9.2 Implementation Verification

- Constant-time execution verified through timing analysis
- Memory safety verified through static analysis (Polyspace)
- Fuzzing with 10^7 random inputs found no authentication bypasses
- Side-channel evaluation confirms no key leakage through power analysis

## 10. Compliance

| Standard | Requirement | Status |
|----------|-------------|--------|
| IEC 62304 | Auth during software updates | Compliant |
| IEC 81001-5-1 | Authentication mechanisms | Compliant |
| FDA Cybersecurity Guidance | Multi-factor authentication | Compliant |
| UL 2900-1 | Authentication strength | Level 3 |

## 11. Summary

The iPACE-CHIP authentication framework provides four levels of assurance,
from basic certificate-based device verification to multi-factor
clinician-patient-implant three-way authentication. The OPAQUE-based PIN
protocol ensures that patient credentials are never exposed over the wireless
channel. Emergency access provides a safety net with strict time and scope
limitations. Formal verification confirms the protocol's security properties,
while comprehensive failure handling protects against brute force and anomaly
attacks.
