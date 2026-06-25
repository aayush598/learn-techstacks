# Authentication

## Authentication Factors
| Factor | Examples |
|--------|----------|
| **Something you know** | Password, PIN, security question |
| **Something you have** | Token, smart card, phone (TOTP) |
| **Something you are** | Fingerprint, face, iris, voice |

## Password Security
- **Hashing**: never store plaintext passwords
- **Salt**: unique random value per user, stored alongside hash
- **Key Derivation Functions**: bcrypt, PBKDF2, **Argon2** (memory-hard)
  - bcrypt: adaptive cost factor, resistant to GPU/ASIC
  - PBKDF2: iterates HMAC many times (configurable rounds)
  - Argon2: winner of Password Hashing Competition, resistant to side-channel
- **Hash algorithms**: SHA-256 (fast, not ideal alone), bcrypt (slow, intended)

## Multi-Factor Authentication (MFA)
- Combines 2+ factors (e.g., password + TOTP)
- **TOTP** (Time-based One-Time Password): RFC 6238, 30-second window
- **U2F/FIDO2**: hardware security keys, phishing-resistant

## Single Sign-On (SSO)
- **Kerberos**: trusted third-party auth protocol
  - **KDC** (Key Distribution Center): AS + TGS
  - **TGT** (Ticket-Granting Ticket): obtained after initial auth
  - Service tickets: used to access specific services
  - Realm: administrative domain

## Federation Protocols
- **OAuth 2.0**: delegated authorization (access tokens, scopes)
  - Flows: Authorization Code, Implicit, Client Credentials
- **OpenID Connect (OIDC)**: identity layer on top of OAuth 2.0
  - **ID Token** (JWT): proves user identity
- **SAML**: XML-based, enterprise SSO
