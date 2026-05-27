# SSO Session Mapping

## Overview

SSO session mapping aligns IdP session lifetimes with application sessions. This involves session timeout alignment, forced re-authentication, single logout, and handling IdP session expiry.

## Session Mapping

```typescript
interface SsoSessionMapping {
  id: string;
  userId: string;
  tenantId: string;
  idpSessionId: string;       // IdP session identifier
  idpSessionExpiry: Date;     // When IdP session expires
  appSessionId: string;
  appSessionExpiry: Date;
  lastIdpAuthnAt: Date;
  forceReauth: boolean;       // Force re-auth on next request
}

class SsoSessionService {
  async createMappedSession(userId: string, tenantId: string, idpSession: IdpSession): Promise<SessionInfo> {
    const appSession = await this.sessionService.createSession(userId, tenantId);

    // Align app session expiration with IdP session (whichever is sooner)
    const appSessionExpiry = new Date(Math.min(
      appSession.expiresAt.getTime(),
      idpSession.expiresAt.getTime()
    ));

    const mapping: SsoSessionMapping = {
      id: generateId('sso_map'),
      userId,
      tenantId,
      idpSessionId: idpSession.id,
      idpSessionExpiry: idpSession.expiresAt,
      appSessionId: appSession.id,
      appSessionExpiry,
      lastIdpAuthnAt: new Date(),
      forceReauth: false,
    };

    await this.db.insert('sso_session_mappings', mapping);
    return { ...appSession, expiresAt: appSessionExpiry };
  }

  async handleIdpSessionExpiry(idpSessionId: string): Promise<void> {
    const mapping = await this.db.findOne('sso_session_mappings', { idpSessionId });
    if (!mapping) return;

    // Force re-authentication or expire app session
    if (mapping.appSessionExpiry > new Date()) {
      // App session still valid, but IdP session expired
      await this.db.update('sso_session_mappings', { id: mapping.id }, {
        forceReauth: true,
      });
    } else {
      // Both expired, clean up
      await this.sessionService.revokeSession(mapping.appSessionId);
      await this.db.delete('sso_session_mappings', { id: mapping.id });
    }
  }

  async validateMappedSession(sessionId: string): Promise<boolean> {
    const mapping = await this.db.findOne('sso_session_mappings', { appSessionId: sessionId });
    if (!mapping) return true; // Not an SSO session, use normal validation

    if (mapping.forceReauth) {
      return false; // Needs re-authentication
    }

    // Check IdP session is still valid
    if (mapping.idpSessionExpiry < new Date()) {
      await this.handleIdpSessionExpiry(mapping.idpSessionId);
      return false;
    }

    return true; // Session valid
  }
}
```

## Single Logout (SLO)

```typescript
class SingleLogoutService {
  async initiateSlo(userId: string): Promise<void> {
    const mappings = await this.db.find('sso_session_mappings', { userId });
    const idpSessionIds = mappings.map(m => m.idpSessionId);

    // Clear app sessions
    await this.sessionService.revokeAllUserSessions(userId);

    // Build SLO request for each IdP
    for (const mapping of mappings) {
      const config = await this.getSsoConfig(mapping.tenantId);
      if (config?.provider === 'saml') {
        await this.sendSamlLogoutRequest(mapping, config);
      } else if (config?.provider === 'oidc') {
        await this.sendOidcLogoutRequest(mapping, config);
      }
    }

    await this.db.delete('sso_session_mappings', { userId });
  }

  async handleIdpInitiatedLogout(samlLogoutRequest: any): Promise<void> {
    const config = await this.getSsoConfigForIssuer(samlLogoutRequest.issuer);
    const sessionIndex = samlLogoutRequest.sessionIndex;

    const mapping = await this.db.findOne('sso_session_mappings', { idpSessionId: sessionIndex });
    if (mapping) {
      await this.sessionService.revokeSession(mapping.appSessionId);
      await this.db.delete('sso_session_mappings', { id: mapping.id });
    }

    // Respond with SAML logout response
    return this.buildSamlLogoutResponse(config, samlLogoutRequest);
  }
}
```

## Open-Source Tools

- **samlify** (MIT) — SLO request/response handling
- **openid-client** (MIT) — OIDC RP-initiated logout

## Production Considerations

- Align session timeouts: app session should not exceed IdP session time
- Support IdP session timeout notification via SAML `SessionNotOnOrAfter`
- Handle IdP-initiated SLO for compliance (HIPAA requires session termination)
- Provide fallback to app-level logout if IdP SLO fails
- Log all SSO session events for audit trail
- Support session refresh without full re-auth using IdP session cookies
