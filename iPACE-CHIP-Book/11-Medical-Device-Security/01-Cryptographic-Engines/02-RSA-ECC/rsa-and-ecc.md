# RSA and Elliptic Curve Cryptography for iPACE-CHIP

## Overview

Asymmetric cryptographic algorithms — RSA and Elliptic Curve Cryptography (ECC) —
play a critical role in the iPACE-CHIP implantable pacemaker ecosystem by enabling
secure key exchange, digital signatures, and certificate-based authentication. While
symmetric algorithms like AES handle bulk data encryption, RSA and ECC provide the
trust infrastructure that makes secure communication between implant and programmer
possible.

## 1. RSA in the iPACE-CHIP Context

### 1.1 RSA Mathematical Foundation

RSA security rests on the computational difficulty of factoring the product of two
large primes. Key generation involves:

1. Select two distinct large primes p and q
2. Compute n = p × q (modulus)
3. Compute φ(n) = (p-1)(q-1) (Euler's totient)
4. Select e such that 1 < e < φ(n) and gcd(e, φ(n)) = 1 (public exponent)
5. Compute d ≡ e^(-1) mod φ(n) (private exponent)

The public key is (n, e) and the private key is (d, or equivalently p, q, d).

**RSA Parameter Choices for iPACE-CHIP:**

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Modulus size | 2048 bits | Minimum for 112-bit security |
| Public exponent | 65537 (0x10001) | Efficient verification, standard choice |
| Private exponent | CRT form (dP, dQ, qInv) | 4× faster private key operations |
| Prime generation | Miller-Rabin with 4 rounds | 2^-80 false positive probability |

### 1.2 RSA Operations Used in iPACE-CHIP

**RSA-OAEP Encryption (Key Encapsulation):**

RSA-OAEP (Optimal Asymmetric Encryption Padding) is used during the initial
key exchange between the external programmer and the iPACE-CHIP implant. The
programmer encrypts a random AES session key using the implant's RSA public key.

```
OAEP Encoding:
  1. Generate random seed r (20 bytes)
  2. Compute lHash = Hash(label)
  3. Compute maskedDB = DB ⊕ MGF1(r, dbLen)
  4. Compute maskedSeed = r ⊕ MGF1(maskedDB, seedLen)
  5. Encoded message = 0x00 || maskedSeed || maskedDB
  6. Ciphertext = EncodedMessage^d mod n (for decryption)
```

OAEP provides provable security in the random oracle model and eliminates the
padding vulnerabilities that plagued PKCS#1 v1.5.

**RSA-PSS Digital Signatures:**

RSA-PSS (Probabilistic Signature Scheme) is used for firmware image authentication
and device identity attestation. The iPACE-CHIP signs critical data with its
device-specific private key, and the programmer or cloud verifier validates the
signature using the corresponding public key from the device certificate.

```
PSS Signature Generation:
  1. Compute mHash = Hash(message)
  2. Generate random salt s (32 bytes)
  3. Compute H' = 0x0000000000000000 || mHash || s
  4. Compute MGF1 hash for padding
  5. Construct encoded message with DB and maskedDB
  6. Signature = EncodedMessage^d mod n
```

### 1.3 RSA CRT Optimization

The Chinese Remainder Theorem (CRT) accelerates RSA private key operations by
4× by splitting the computation into two smaller modular exponentiations:

```
m1 = c^(dP) mod p
m2 = c^(dQ) mod q
h = (m1 - m2) × qInv mod p
m = m2 + h × q
```

where dP = d mod (p-1), dQ = d mod (q-1), and qInv = q^(-1) mod p.

**Blinding Countermeasure:**

Before each RSA private key operation, a random blinding factor r is applied:

```
c' = c × r^e mod n
m' = (c')^d mod n
m = m' × r^(-1) mod n
```

This prevents timing and power analysis attacks by randomizing the relationship
between the input ciphertext and the internal computation.

### 1.4 RSA Performance Constraints

RSA-2048 operations are computationally expensive on microcontrollers. The
iPACE-CHIP mitigates this through:

**Precomputation:** During idle periods, the implant precomputes CRT components
and stores them in SRAM for immediate use during key exchange.

**Batch Verification:** Multiple RSA-PSS signatures (e.g., firmware segments)
are batched and verified together, amortizing the cost of modular exponentiation.

**Hybrid Approach:** RSA is used only for key encapsulation and signatures; bulk
data encryption uses AES as described in the AES chapter.

| Operation | Time (ARM Cortex-M4, 24 MHz) | Energy (3V) |
|-----------|------------------------------|-------------|
| RSA-2048 Sign | 180 ms | 32 μJ |
| RSA-2048 Verify | 12 ms | 2.1 μJ |
| RSA-2048 KeyGen | 3.2 s | 576 μJ |

## 2. Elliptic Curve Cryptography (ECC)

### 2.1 Why ECC for iPACE-CHIP

ECC provides equivalent security to RSA with significantly smaller key sizes,
making it ideal for resource-constrained implantable devices:

| Security Level | RSA Key Size | ECC Key Size | Ratio |
|----------------|--------------|--------------|-------|
| 80-bit | 1024 | 160 | 6.4× |
| 112-bit | 2048 | 224 | 9.1× |
| 128-bit | 3072 | 256 | 12× |
| 192-bit | 7680 | 384 | 20× |
| 256-bit | 15360 | 521 | 29.3× |

Smaller keys mean smaller certificates, less storage, lower bandwidth requirements,
and faster computation — all critical for an implant with limited flash and RF
throughput.

### 2.2 Curve Selection: NIST P-256

The iPACE-CHIP uses the NIST P-256 (secp256r1) elliptic curve, defined over
the finite field F_p where:

```
p = 2^256 - 2^224 + 2^192 + 2^96 - 1
y^2 = x^3 - 3x + b (mod p)
```

P-256 provides 128-bit security against classical attacks and 64-bit security
against quantum attacks (via Pollard's rho on a quantum computer).

**Curve Parameters:**

| Parameter | Value |
|-----------|-------|
| Field prime p | FFFFFFFF 00000001 00000000 00000000 00000000 FFFFFFFF FFFFFFFF FFFFFFFF |
| Generator G.x | 6B17D1F2 E12C4247 F8BCE6E5 63A440F2 77037D81 2DEB33A0 F4A13945 D898C296 |
| Generator G.y | 4FE342E2 FE1A7F9B 8EE7EB4A 7C0F9E16 2BCE3357 6B315ECE CBB64068 37BF51F5 |
| Order n | FFFFFFFF 00000000 FFFFFFFF FFFFFFFF BCE6FAAD 7159456A 490AAA60 2D391745 |
| Cofactor h | 1 |

### 2.3 ECDH Key Agreement

Elliptic Curve Diffie-Hellman (ECDH) enables the iPACE-CHIP and programmer to
establish a shared secret over an insecure channel:

```
Programmer:
  1. Generate ephemeral key pair (d_P, Q_P = d_P × G)
  2. Transmit Q_P to implant

Implant:
  1. Generate ephemeral key pair (d_I, Q_I = d_I × G)
  2. Transmit Q_I to programmer
  3. Compute shared_secret = d_I × Q_P

Programmer:
  1. Compute shared_secret = d_P × Q_I
```

Both parties derive the same shared secret, which is then fed into HKDF to
produce symmetric encryption keys.

**Ephemeral Keys:** ECDH operations on the iPACE-CHIP use ephemeral keys that are
generated fresh for each session and discarded immediately after key derivation.
This provides forward secrecy — compromise of the device's long-term signature key
does not expose past session keys.

### 2.4 ECDSA Digital Signatures

Elliptic Curve Digital Signature Algorithm (ECDSA) is used for:

- **Firmware authentication:** Each firmware image is signed by the manufacturer's
  ECDSA key pair (P-384 curve for enhanced security margin)
- **Device attestation:** The implant signs a challenge with its device-specific
  ECDSA key (P-256) to prove authenticity during pairing
- **Telemetry integrity:** Critical telemetry summaries are signed to ensure
  non-repudiation in medical records

```
ECDSA Signature Generation (P-256):
  1. Hash message: e = SHA-256(message)
  2. Generate random k ∈ [1, n-1]
  3. Compute (x1, y1) = k × G
  4. r = x1 mod n (if r = 0, go to step 2)
  5. s = k^(-1) × (e + r × d) mod n (if s = 0, go to step 2)
  6. Signature = (r, s)
```

**RFC 6979 Deterministic ECDSA:**

To eliminate the critical vulnerability of poor random number generation in
signature creation, the iPACE-CHIP uses deterministic ECDSA (RFC 6979), where
the nonce k is derived deterministically from the private key and message hash:

```
k = HMAC-SHA256(d || Hash(message), random_seed)
```

This eliminates the category of attacks where weak randomness leads to private
key recovery (as occurred in PlayStation 3 ECDSA signing).

### 2.5 ECDSA Verification Performance

| Operation | Time (ARM Cortex-M4, 24 MHz) | Code Size |
|-----------|------------------------------|-----------|
| ECDSA Sign (P-256) | 48 ms | 8.2 KB |
| ECDSA Verify (P-256) | 62 ms | 7.8 KB |
| ECDH Shared Secret | 52 ms | 6.1 KB |
| Point Multiply (single) | 38 ms | — |

## 3. Hybrid RSA+ECC Protocol Design

### 3.1 Protocol Overview

The iPACE-CHIP uses a hybrid approach combining RSA and ECC:

- **RSA-2048** for certificate chain verification (compatibility with existing
  PKI infrastructure used by medical device manufacturers)
- **ECC P-256** for real-time operations (key exchange, telemetry signing)
- **ECC P-384** for long-term firmware signing (higher security margin)

### 3.2 Certificate Chain

```
Root CA (RSA-4096, offline)
  └── Intermediate CA (RSA-2048, manufacturer)
       └── Device Certificate (ECDSA P-256, per-implant)
            ├── Subject: iPACE-CHIP S/N: xxxxx
            ├── Public Key: ECDSA P-256
            ├── Extensions: Key Usage = digitalSignature, keyAgreement
            ├── Extensions: Extended Key Usage = id-kp-serverAuth
            └── Extensions: Medical Device Identifier (UDI)
```

### 3.3 Initial Pairing Protocol

The secure pairing between programmer and implant follows this sequence:

```
Phase 1: Device Discovery
  Programmer → Implant: Hello(Nonce_P, Timestamp_P)
  Implant → Programmer: Hello(Nonce_I, Timestamp_I, DeviceCert_I)

Phase 2: Certificate Verification
  Programmer verifies DeviceCert_I chain to Root CA
  Programmer validates certificate freshness (timestamp within 24 hours)
  Programmer checks certificate revocation list (if available)

Phase 3: Ephemeral Key Exchange
  Programmer generates (d_P, Q_P) for P-256
  Programmer → Implant: KeyExchange(Q_P, Sign_ECDSA(d_P_prog, Hash(Q_P || Nonce_I)))

Phase 4: Shared Secret Computation
  Implant verifies programmer signature on Q_P
  Implant generates (d_I, Q_I) for P-256
  Implant computes: shared_secret = d_I × Q_P
  Implant → Programmer: KeyExchange(Q_I, Sign_ECDSA(d_I, Hash(Q_I || Nonce_P)))
  Programmer computes: shared_secret = d_P × Q_I

Phase 5: Key Derivation
  session_key = HKDF-SHA256(shared_secret, salt=Nonce_I||Nonce_P, info="iPACE session")
```

### 3.4 Certificate Pinning

To prevent man-in-the-middle attacks through compromised CA certificates, the
iPACE-CHIP implements certificate pinning:

- The implant stores the SHA-256 hash of the programmer's certificate during
  initial pairing
- Subsequent connections verify the programmer certificate against the pinned hash
- Pin rotation requires physical presence (programmer within NFC range) and
  explicit patient consent via the patient controller

## 4. Hardware Acceleration for ECC

### 4.1 Crypto Co-Processor

The iPACE-CHIP includes a dedicated ECC co-processor with the following
capabilities:

- **Point multiplication:** Hardware-accelerated modular arithmetic over P-256
  and P-384 fields
- **Montgomery ladder:** Constant-time point multiplication using the Montgomery
  ladder algorithm, resistant to timing and simple power analysis attacks
- **Projective coordinates:** Internal use of Jacobian projective coordinates to
  avoid costly field inversions during point multiplication
- **Secure key storage:** Private keys loaded into the co-processor via a
  write-only interface; the CPU never has direct access to key material

### 4.2 Modular Arithmetic Unit

The hardware modular arithmetic unit provides:

| Operation | Latency | Area (gate equivalent) |
|-----------|---------|----------------------|
| 256-bit modular add/sub | 2 cycles | 1.2K GE |
| 256-bit modular multiply | 16 cycles | 8.4K GE |
| 256-bit modular inverse | 480 cycles | 4.2K GE |
| Point multiply (256-bit) | 12,000 cycles | — (combined) |

### 4.3 Side-Channel Countermeasures

**Scalar Randomization:** Before each point multiplication, the scalar is
randomized: k' = k + r×n (mod n), where r is random. Since (k' mod n) × G
equals (k mod n) × G, the result is unchanged but the intermediate computations
are randomized.

**Point Blinding:** The base point is blinded by adding a random point:
P' = P + R, where R is a precomputed random point. The result is corrected
after multiplication.

**Projective Coordinate Randomization:** The projective representation is
randomized by multiplying (X:Y:Z) by (r^2:r^3:1), preventing simple power
analysis from extracting affine coordinates.

## 5. Post-Quantum Transition Planning

### 5.1 Quantum Threat Timeline

Current estimates suggest that a cryptographically relevant quantum computer capable
of breaking ECC-256 (via Shor's algorithm) is 15-25 years away. However, the
iPACE-CHIP is designed with a 10-15 year implant lifetime, making post-quantum
readiness relevant.

### 5.2 Cryptographic Agility Framework

The iPACE-CHIP firmware includes a cryptographic agility framework that supports:

- Algorithm negotiation during pairing (current: RSA-2048 + ECDSA P-256)
- Runtime detection of post-quantum algorithm support in programmers
- Seamless transition path to NIST PQC standards (CRYSTALS-Dilithium for
  signatures, CRYSTALS-Kyber for key encapsulation)

### 5.3 Hybrid Classical+PQ Mode

The planned firmware update will support:

```
Key Exchange = ECDH_P256(shared_secret_1) || Kyber768(shared_secret_2)
Final Key = HKDF-SHA256(shared_secret_1 || shared_secret_2, salt, info)
```

This hybrid mode provides security even if one of the two algorithms is broken.

## 6. Key Sizes and Storage Requirements

### 6.1 Implant Key Storage Budget

| Key/Material | Size | Storage |
|-------------|------|---------|
| Device Root Key | 256 bits | OTP NVM |
| ECDSA P-256 private key | 256 bits | KMU register |
| ECDSA P-256 public key | 512 bits | Flash (read-only) |
| Device certificate | ~512 bytes | Flash (read-only) |
| Pinned programmer cert hash | 256 bits | Flash (write-once) |
| Ephemeral ECDH keys | 256 bits each | KMU register (volatile) |
| Session key | 128 bits | KMU register (volatile) |
| **Total non-volatile** | **~1.2 KB** | — |

### 6.2 Programmer Key Storage

| Material | Size | Storage |
|----------|------|---------|
| Programmer CA certificate | ~1 KB | Secure enclave |
| Programmer private key (RSA-2048) | 2048 bits | HSM-backed |
| Programmer private key (ECDSA P-256) | 256 bits | HSM-backed |
| Pinned implant cert hashes | 256 bits per device | Database |

## 7. Security Considerations

### 7.1 Side-Channel Attacks on RSA/ECC

| Attack | Target | Countermeasure |
|--------|--------|----------------|
| Timing analysis | Modular exponentiation | Constant-time Montgomery multiplication |
| Simple Power Analysis | Point multiplication | Montgomery ladder + scalar randomization |
| Differential Power Analysis | Key recovery | Point blinding + projective randomization |
| Electromagnetic emanation | Field operations | Shielded packaging + balanced logic |
| Fault injection | Signature computation | Verify-and-retry with comparison |

### 7.2 Implementation Pitfalls Avoided

- **No custom cryptography:** All algorithms use standardized, peer-reviewed
  implementations
- **No secret-dependent branching:** All conditional operations use arithmetic
  masking rather than branch instructions
- **No secret-dependent memory access:** Key material stored in registers, not
  indexed arrays
- **No reuse of nonces:** Deterministic ECDSA (RFC 6979) prevents nonce reuse

### 7.3 Certification Path

The RSA/ECC implementation targets:

- FIPS 140-3 Level 2 (cryptographic module validation)
- Common Criteria EAL4+ (evaluation assurance level)
- IEC 62443-4-2 SL2 (component security requirements)

## 8. Summary

The iPACE-CHIP leverages RSA-2048 for certificate infrastructure compatibility
and ECC P-256/P-384 for efficient real-time cryptographic operations. The hybrid
approach balances the practical requirements of a resource-constrained implantable
device with the security demands of a life-critical medical system. Hardware
acceleration with comprehensive side-channel countermeasures ensures that
asymmetric operations are both fast and secure, while the cryptographic agility
framework prepares the device for the post-quantum era.
