# Section 02: Encryption in Transit (TLS 1.3)

Encryption in transit protects data as it travels between clients, services, and external integrations. The platform enforces TLS 1.3 for all external connections and mTLS for internal service-to-service communication. Certificates are managed automatically with Let's Encrypt for public endpoints and an internal CA for private services.

TLS configuration: minimum TLS 1.2 (TLS 1.3 preferred), cipher suites (ECDHE + AES-GCM + SHA384 for forward secrecy), HSTS enabled (max-age=31536000, includeSubDomains, preload), OCSP stapling for certificate status, and certificate pinning (HPKP) for API clients. All HTTP traffic redirects to HTTPS at the load balancer level.

Internal communication: services use mTLS with certificates issued by the internal certificate authority. Each service has a unique certificate identifying it. Connections are verified at both ends. Service mesh (Istio/Linkerd) enforces mTLS between all pods automatically. API gateway terminates external TLS and re-encrypts for internal traffic.
