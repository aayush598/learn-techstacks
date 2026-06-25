# Encryption

## Symmetric Encryption
- Same key for **encryption and decryption**
- Fast, suitable for bulk data
- **AES** (Advanced Encryption Standard): block cipher, 128/192/256-bit keys
  - Modes: ECB (unsafe), CBC, GCM (authenticated), CTR
- **DES/3DES**: obsolete (56-bit key cracked)
- **ChaCha20**: stream cipher, fast on mobile (used in TLS)

## Asymmetric Encryption
- **Key pair**: public key (share), private key (keep secret)
- Slower than symmetric, used for key exchange/signatures
- **RSA**: based on integer factorization (1024/2048/4096-bit)
- **ECC** (Elliptic Curve Cryptography): smaller keys, same security
  - ECDH for key exchange, **ECDSA** for signatures
  - Ed25519: modern, fast, side-channel resistant

## TLS/SSL
- **TLS Handshake** (asymmetric): authenticate server, exchange session key
  1. ClientHello → ServerHello + Certificate
  2. Key exchange (Diffie-Hellman or RSA)
  3. ChangeCipherSpec → Finished
- **Session** (symmetric): AES-GCM or ChaCha20-Poly1305
- Perfect Forward Secrecy (PFS): ephemeral Diffie-Hellman

## Digital Signatures
- **Sign**: hash message → encrypt hash with **private key**
- **Verify**: decrypt hash with **public key** → compare to message hash
- Provides: authentication, integrity, non-repudiation

## Certificates & PKI
- **X.509** certificate: binds public key to identity
  - Fields: Subject, Issuer (CA), Validity, Public Key, Signature
- **CA** (Certificate Authority): trusted third party
- **Chain of trust**: root CA → intermediate CA → server cert
- **Certificate Revocation**: CRL (list) or OCSP (online check)

## Full-Disk Encryption
- **LUKS** (Linux): dm-crypt + LUKS header, multiple passphrases
- **BitLocker** (Windows): TPM + PIN/USB, AES-128/256
- **FileVault** (macOS): XTS-AES-128, hardware acceleration
