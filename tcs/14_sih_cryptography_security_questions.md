# SIH Cryptography & Security Core Defense

Since you were a Smart India Hackathon (SIH) finalist for building a "security-focused encryption system," expect aggressive questioning on Cryptography and Cybersecurity. TCS values security highly.

## Cryptography Core Concepts
1. **Q:** What is the difference between Hashing and Encryption? **A:** Encryption is a two-way process; data is encrypted with a key and can be decrypted with the right key. Hashing is a one-way mathematical function mapping data to a fixed-size string; it cannot be reversed.
2. **Q:** Symmetric vs Asymmetric Encryption? **A:** Symmetric uses the same key for both encryption and decryption (fast, used for bulk data like AES). Asymmetric uses a pair of keys—a public key for encryption and a private key for decryption (slower, used for secure key exchange/signatures like RSA).
3. **Q:** What is AES? **A:** Advanced Encryption Standard. The industry-standard symmetric block cipher operating on 128-bit data blocks with key sizes of 128, 192, or 256 bits.
4. **Q:** What is RSA? **A:** Rivest–Shamir–Adleman. An asymmetric algorithm based on the practical difficulty of factoring the product of two large prime numbers.
5. **Q:** How does a digital signature work? **A:** A user hashes a message and encrypts the hash with their private key. The receiver decrypts the hash using the sender's public key and compares it to a locally generated hash of the message to verify integrity and non-repudiation.

## Secure Hash Algorithms
6. **Q:** Why not use MD5 or SHA-1 anymore? **A:** Both are considered cryptographically broken because they are vulnerable to collision attacks (where two different inputs produce the same hash output).
7. **Q:** Which hash algorithm should be used for passwords? **A:** Bcrypt or Argon2. They are deliberately slow and computationally expensive (incorporating "cost factors"), rendering brute-force and hardware acceleration attacks unfeasible.
8. **Q:** What is a Salt in cryptography? **A:** A unique, randomly generated string appended to a password before hashing. It ensures identical passwords have totally different hashes, defeating pre-computed Rainbow Table attacks.

## Web & Application Security
9. **Q:** Explain the SSL/TLS Handshake. **A:** 1. Client sends "Client Hello" with supported cipher suites. 2. Server responds with "Server Hello" and its SSL certificate (containing public key). 3. Client verifies certificate. 4. Client generates a symmetric session key, encrypts it with server's public key, and sends it. 5. Server decrypts using its private key. 6. Both uses the symmetric key for fast, secure communication.
10. **Q:** How do you secure a REST API? **A:** Implement HTTPS (SSL/TLS), use Token-Based Authentication (JWT or OAuth2), validate/sanitize all inputs to prevent SQL Injection, and implement rate-limiting and CORS policies.
11. **Q:** What are JWTs vulnerable to? **A:** If the secret signing key is weak or leaked, attackers can forge valid tokens. If algorithms aren't explicitly verified (the `alg: none` vulnerability), arbitrary unsigned tokens might be accepted.
12. **Q:** How did you handle large payloads in your SIH encryption system? **A:** Since RSA cannot encrypt data larger than its key size, a hybrid approach is used: a fast symmetric key (AES) encrypts the large file, and the slow asymmetric key (RSA) encrypts the tiny AES key to safely share it.
13. **Q:** What is the Principle of Least Privilege? **A:** A security concept where users, programs, or processes are given only the bare minimum access permissions necessary to perform their function.
14. **Q:** What is Penetration Testing? **A:** A simulated cyber attack against your computer system to check for exploitable vulnerabilities.
15. **Q:** How do you obscure sensitive keys (like Gemini/OpenAI API keys) in code? **A:** Using `.env` environment variables never committed to Git (via `.gitignore`), and injecting them securely via secrets managers (like GitHub Secrets or AWS Secrets Manager) in CI/CD environments.
