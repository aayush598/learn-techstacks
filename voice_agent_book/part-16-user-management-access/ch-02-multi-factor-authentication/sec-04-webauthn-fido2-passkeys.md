# WebAuthn / FIDO2 Passkeys

## Overview

WebAuthn (Web Authentication) is a W3C standard for passwordless authentication using public-key cryptography. FIDO2 passkeys replace passwords with device-bound or cloud-synced cryptographic credentials, supporting biometric verification (fingerprint, face ID), PIN, or security keys.

## WebAuthn Authentication Flow

```
[User] → "Register Passkey"
    ↓
[Browser] → navigator.credentials.create({ publicKey })
    ↓
[Platform Authenticator] → Biometric/PIN verification
    ↓
[Authenticator] → Generate key pair (sk, pk)
    ↓
[Browser] → Return publicKey + credentialId
    ↓
[Server] → Store publicKey, credentialId, signCount
    ↓
[User] → "Login with Passkey"
    ↓
[Browser] → navigator.credentials.get({ publicKey })
    ↓
[Authenticator] → Biometric/PIN verification
    ↓
[Authenticator] → Sign challenge with private key
    ↓
[Server] → Verify signature with stored publicKey
    ↓
[Server] → Issue session token
```

## Registration Implementation

```typescript
import {
  generateRegistrationOptions,
  verifyRegistrationResponse,
  generateAuthenticationOptions,
  verifyAuthenticationResponse,
} from '@simplewebauthn/server';

import type {
  RegistrationResponseJSON,
  AuthenticationResponseJSON,
} from '@simplewebauthn/server';

interface WebAuthnCredential {
  id: string;
  publicKey: Uint8Array;
  counter: number;
  deviceType: 'singleDevice' | 'multiDevice';
  backedUp: boolean;
  transports?: AuthenticatorTransport[];
  userId: string;
  label: string;
  createdAt: Date;
  lastUsedAt?: Date;
}

class WebAuthnService {
  private rpName = 'VoiceAgent';
  private rpId = 'voiceagent.com';
  private origin = 'https://app.voiceagent.com';

  async generateRegistrationOptions(userId: string, userName: string): Promise<any> {
    const existingCredentials = await this.getUserCredentials(userId);

    const options = generateRegistrationOptions({
      rpName: this.rpName,
      rpID: this.rpId,
      userName,
      userDisplayName: userName,
      timeout: 60000,
      attestationType: 'none',
      excludeCredentials: existingCredentials.map(cred => ({
        id: Buffer.from(cred.publicKey).toString('base64url'),
        type: 'public-key' as const,
        transports: cred.transports,
      })),
      authenticatorSelection: {
        residentKey: 'preferred',
        userVerification: 'preferred',
      },
    });

    // Store challenge temporarily for verification
    await this.challengeStore.set(userId, options.challenge, 120);
    return options;
  }

  async verifyRegistration(
    userId: string,
    response: RegistrationResponseJSON
  ): Promise<WebAuthnCredential> {
    const expectedChallenge = await this.challengeStore.get(userId);
    if (!expectedChallenge) throw new Error('Challenge expired');

    const verification = await verifyRegistrationResponse({
      response,
      expectedChallenge,
      expectedOrigin: this.origin,
      expectedRPID: this.rpId,
    });

    if (!verification.verified || !verification.registrationInfo) {
      throw new Error('Registration verification failed');
    }

    const { credential, credentialDeviceType, credentialBackedUp } = verification.registrationInfo;

    const credentialRecord: WebAuthnCredential = {
      id: credential.id,
      publicKey: credential.publicKey,
      counter: credential.counter,
      deviceType: credentialDeviceType,
      backedUp: credentialBackedUp,
      transports: response.response.transports,
      userId,
      label: this.generateCredentialLabel(credentialDeviceType),
      createdAt: new Date(),
    };

    await this.credentialStore.save(credentialRecord);
    await this.challengeStore.del(userId);
    return credentialRecord;
  }
}
```

## Authentication Implementation

```typescript
class WebAuthnService {
  async generateAuthenticationOptions(userId: string): Promise<any> {
    const credentials = await this.getUserCredentials(userId);

    const options = generateAuthenticationOptions({
      rpID: this.rpId,
      timeout: 60000,
      allowCredentials: credentials.map(cred => ({
        id: Buffer.from(cred.publicKey).toString('base64url'),
        type: 'public-key' as const,
        transports: cred.transports,
      })),
      userVerification: 'preferred',
    });

    await this.challengeStore.set(`auth:${userId}`, options.challenge, 120);
    return options;
  }

  async verifyAuthentication(
    userId: string,
    response: AuthenticationResponseJSON
  ): Promise<boolean> {
    const expectedChallenge = await this.challengeStore.get(`auth:${userId}`);
    if (!expectedChallenge) throw new Error('Challenge expired');

    const credential = await this.credentialStore.findById(response.id);
    if (!credential) throw new Error('Credential not found');

    const verification = await verifyAuthenticationResponse({
      response,
      expectedChallenge,
      expectedOrigin: this.origin,
      expectedRPID: this.rpId,
      credential: {
        id: credential.id,
        publicKey: credential.publicKey,
        counter: credential.counter,
        transports: credential.transports,
      },
    });

    if (verification.verified && verification.authenticationInfo) {
      // Update credential counter for cloned key detection
      await this.credentialStore.updateCounter(
        credential.id,
        verification.authenticationInfo.newCounter
      );
      await this.credentialStore.updateLastUsed(credential.id);
    }

    await this.challengeStore.del(`auth:${userId}`);
    return verification.verified;
  }
}
```

## Passkey Management UI

```typescript
interface PasskeyManagementAPI {
  // List user's registered passkeys
  listCredentials(userId: string): Promise<WebAuthnCredential[]>;

  // Remove a passkey
  removeCredential(credentialId: string): Promise<void>;

  // Rename a passkey label
  renameCredential(credentialId: string, label: string): Promise<void>;

  // Get credential details for display
  getCredentialDetails(credentialId: string): Promise<{
    label: string;
    deviceType: 'platform' | 'cross-platform';
    backedUp: boolean;
    createdAt: Date;
    lastUsedAt: Date | null;
  }>;
}
```

## Open-Source Tools

- **@simplewebauthn/server** (MIT) — Server-side WebAuthn library
- **@simplewebauthn/browser** (MIT) — Browser WebAuthn helpers
- **@passwordless-id/webauthn** (MIT) — Alternative WebAuthn implementation

## Production Considerations

- Support both platform authenticators (fingerprint, Face ID) and roaming authenticators (YubiKey, Titan Key)
- Store challenge values in Redis with automatic expiry (2 minutes)
- Track credential counter to detect cloned authenticator keys
- Allow users to register multiple passkeys across different devices
- Provide fallback to TOTP/OTP when WebAuthn is unavailable (e.g., incognito mode, older browsers)
- Browser compatibility: Chrome 67+, Firefox 60+, Safari 13.1+, Edge 18+
- For mobile apps, use platform-specific APIs (Android Credential Manager, iOS ASCredentialManager)
