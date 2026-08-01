# Chapter: Email, DHCP & Other Protocols

## What you'll learn
- The email delivery chain: SMTP (send/relay), POP3/IMAP (retrieve), and the store-and-forward mail model with headers/MIME.
- DHCP in depth: the DORA exchange (Discover, Offer, Request, Acknowledge), lease lifecycle, and how hosts get an IP automatically.
- The classic application protocols: FTP, SFTP, Telnet, SSH, plus file transfer security (FTP vs SFTP vs FTPS vs SCP).
- Modern real-time and event-delivery options: WebSockets (full-duplex), Server-Sent Events (SSE, one-way push), and Webhooks (server-to-server callbacks).

## Prerequisites (linked)
- [Chapter 01: HTTP](../chapter-01-http/README.md) — WebSockets/SSE are HTTP-upgrade or HTTP-companion protocols.
- [Chapter 02: DNS](../chapter-02-dns/README.md) — MX records route email; DHCP runs *before* DNS matters.

## Sections (linked table)
- [section-01-smtp-pop3-and-imap](section-01-smtp-pop3-and-imap.md)
- [section-02-dhcp-in-depth](section-02-dhcp-in-depth.md)
- [section-03-ftp-sftp-telnet-ssh-and-other-services](section-03-ftp-sftp-telnet-ssh-and-other-services.md)
- [section-04-websockets-webhooks-and-sse](section-04-websockets-webhooks-and-sse.md)

## One-paragraph narrative connecting all sections
Section 01 covers email's push-pull split: SMTP *pushes* between mail servers (store-and-forward), while POP3/IMAP *pull* into the client — a division that explains how mail survives hours of offline servers. Section 02 covers DHCP, the protocol that configures every host's IP/mask/gateway/DNS before anything else works — the DORA handshake and lease lifecycle. Section 03 covers the file/terminal protocols: FTP (data + control channels, insecure) and SSH (encrypted replacement for Telnet and file transfer via SFTP/SCP). Section 04 covers the real-time push ecosystem: WebSockets, SSE, and Webhooks — the three ways servers talk to clients/apps asynchronously. Together: how the Internet handles mail, configuration, files, and real-time delivery.

## Common interview trap in this chapter
Trap: "Email uses IMAP to send mail." — **Wrong.** Sending/relaying is always SMTP; IMAP/POP3 only retrieve. Also a trap: "DHCP assigns IPs forever" — leases expire and renew (and DHCP can hand out static reservations). And: "FTP is secure because SFTP" — FTPS is FTP over TLS, SFTP is SSH-based file transfer — different mechanisms entirely.

## Checklist before moving on
- [ ] I can draw the SMTP push + POP3/IMAP pull mail model with ports (25/587/110/143/993/995).
- [ ] I can walk the DORA DHCP exchange with ports 67/68 and lease timeline.
- [ ] I can compare FTP vs FTPS vs SFTP vs SCP and Telnet vs SSH.
- [ ] I can compare WebSockets vs SSE vs Webhooks with use cases (chat, feed, callbacks).
- [ ] I know why SMTP uses port 587 and why DHCP is UDP.
