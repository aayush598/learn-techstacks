# Section 05: Session Management & Timeouts

Session management controls the lifecycle of authenticated user sessions, balancing security and user experience. Sessions are tracked server-side with JWT tokens for stateless verification and Redis for stateful session data. Timeout policies enforce automatic logout after periods of inactivity.

Session types: web sessions (browser, cookie-based, 24-hour expiry), API sessions (token-based, configurable expiry), and service accounts (long-lived, audited separately). Session timeout policies: idle timeout (30 minutes of inactivity → session expires), absolute timeout (24 hours max session length regardless of activity), and remember-me (30-day cookie with MFA re-prompt).

Session invalidation: manual logout (clear session from Redis and browser), admin force-logout (clear all sessions for a user), password change (invalidate all existing sessions), and suspicious activity detection (automatically terminate session on anomaly detection). Session lists are visible to users and admins.
