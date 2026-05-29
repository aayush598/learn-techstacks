# Section 05: End-to-End Encryption for Media

End-to-end encryption (E2EE) ensures that voice call media (audio streams) is encrypted between the caller's device and the AI agent's processing pipeline, with no intermediate party able to decrypt the content. While full E2EE (where the platform cannot decrypt) is technically challenging for AI processing, the platform offers encrypted media pipelines as an enterprise feature.

Encrypted media flow: caller → encrypted SRTP stream → media server decrypts → processes (STT, AI, TTS) → re-encrypts → streamed to recipient. For compliance recording, the platform can store the decrypted stream in an encrypted recording store. Enterprise tenants can bring their own encryption keys (BYOK) for recording encryption.

Implementation: SRTP with AES-256 for RTP streams, DTLS-SRTP for key exchange, and TLS for SIP signaling. WebRTC uses built-in encryption (DTLS + SRTP). For the enterprise E2EE tier, media is encrypted end-to-end with tenant-provided keys, and the platform performs AI processing on encrypted data using confidential computing (SGX/AMD SEV enclaves).
