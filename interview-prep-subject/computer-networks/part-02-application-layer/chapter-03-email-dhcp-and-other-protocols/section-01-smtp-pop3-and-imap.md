# SMTP, POP3, and IMAP

> **TL;DR**: Email is a store-and-forward system with two halves — **SMTP** (RFC 5321, ports 25/587) *pushes* mail from client to server and between servers, while **POP3** (port 110) *downloads-and-deletes* and **IMAP** (port 143) *syncs a server-side mailbox* — the split exists because delivery must tolerate servers being offline and users need access from many devices.

## 1. Why Does This Exist?
Email's founding problem: **the sender and receiver are rarely online at the same time** and there was no global directory. SMTP exists to implement *store-and-forward*: mail is accepted by a server, relayed hop-by-hop, and stored until the recipient's server can deliver it — like postal mail, not a phone call. POP3/IMAP exist for the *retrieval* half: once mail arrives at your server, you need a way to read it from your device. POP3 (1984-era) was designed for a single device that downloads and removes mail; IMAP (1986+) was designed for the multi-device, server-authoritative model we actually use today. The push/pull split is the fundamental architectural answer to "how do two unreliable parties exchange durable messages?"

## 2. How Does It Work?
- **SMTP (Simple Mail Transfer Protocol)**: ASCII, text-based, command/response (HELO/EHLO, MAIL FROM, RCPT TO, DATA, QUIT). Two roles:
  - *Mail Submission* (client → own server, **port 587**, requires auth — STARTTLS or implicit TLS).
  - *Mail Transfer* (server → server, **port 25**, no end-user auth; uses MX records from DNS).
  - The **envelope** (MAIL FROM/RCPT TO — used for routing) is separate from the **message** (headers + body). Bounces use the envelope, not From.
- **POP3 (Post Office Protocol 3)**: download mailbox → client (typically delete from server; POP3 in "keep" mode exists). Port **110** (POP3S: **995**).
- **IMAP (Internet Message Access Protocol)**: keeps mail *on the server*, syncs folders, flags, and state between clients; supports partial fetch, search, server-side flags. Port **143** (IMAPS: **993**).
- **Message format**: RFC 5322 headers (From, To, Subject, Date, Message-ID, References) + body. **MIME** (RFC 2045-2049) extends it: multipart (text + attachments), encodings (base64/quoted-printable), character sets.
- **Deliverability chain**: SPF/DKIM/DMARC (from DNS section) authenticate; **MX lookup** routes to the recipient's server.

## 3. When Is It Used?
- **SMTP**: every email sent anywhere — webmail (Gmail submits via SMTP), apps (SendGrid/Postmark/SES), internal relays, mailing lists.
- **POP3**: legacy/single-device setups, offline clients, minimal storage scenarios (rare now; mostly POP3s for compatibility).
- **IMAP**: the modern default — Gmail/Outlook/Apple Mail sync via IMAP; mobile + desktop + web all read the same server mailbox.
- **Email pipelines**: inbound parsing (SendGrid Inbound Parse), automated emails (transactional — SMTP APIs), newsletters (bulk via SMTP relays with DKIM/SPF).

## 4. Why Wasn't Another Approach Chosen?
- **Why store-and-forward instead of direct delivery (end-to-end like X.400)?** X.400 (the OSI mail standard) was end-to-end: no intermediate storage, huge headers, heavyweight. SMTP's simple hop-by-hop store-and-forward tolerates offline servers (a relay queues mail for hours/days), scales without global presence, and is easy to implement. It won on simplicity + robustness, accepting *no delivery guarantees* (SMTP has no "was it read" semantics).
- **Why separate submission (587) from transfer (25)?** Port 25 relays open → spam abuse. Splitting: authenticated submission on 587 for users, locked-down port 25 for server relay. This was the anti-spam architecture fix.
- **Why SMTP and not an API/queue?** SMTP predates APIs; it's the universal wire language. Modern systems (SES/SendGrid) wrap SMTP *and* expose HTTP APIs — but the mail path is still SMTP between MTAs.
- **Why IMAP over POP3?** POP3 = download-and-delete → mail exists in one place (your device); multi-device sync impossible, and you lose mail if the device dies. IMAP keeps the server authoritative → any client sees the same mailbox; it also supports partial fetch (progressive loading) and server-side search. The only reason to prefer POP3: privacy/offline single-device or tiny server storage.

## 5. Intuition
Email is **two postal systems joined at the door**:
- **SMTP** = the postal trucks. A letter (message) is handed to your local post office (submission, 587), the post office routes it through other post offices (relay, 25) using the address on the *envelope* (MX/envelope), and drops it at the destination post office — *even if the recipient is asleep* (store-and-forward).
- **POP3** = you walk to the post office and *take your mail home* (download + delete) — good if you have one mailbox at home (one device).
- **IMAP** = the post office *keeps your mail in a PO box*; you open it from home, your phone, or your office, and they all see the same letters, read/unread state, and folders. The mailbox lives at the post office, not in your pocket.

## 6. Real-World Analogy
**The university mailroom**: You send a package (SMTP) by handing it to your department mailroom (submission) which stamps it and forwards it through central campus mail (relay) to the recipient's department box (MX routing → store-and-forward). If the recipient is on vacation, the package waits in their box (server storage) — delivery doesn't require them to be present. POP3 = you come to the mailroom, take the package home, and the mailroom discards its copy. IMAP = the mailroom keeps your package and its "read" status; you inspect it from your laptop, then your phone shows the same "opened" state. The mailroom never gives up its copy — it's the source of truth.

## 7. Formal Definition
- **SMTP** (RFC 5321): a text-based protocol for the *submission and transfer* of email messages; uses commands `EHLO`, `MAIL FROM:`, `RCPT TO:`, `DATA`, `QUIT`; delivery via **store-and-forward** between MTAs; mail routing uses DNS **MX** records. Submission (RFC 6409) uses port 587 with SMTP AUTH; transfer uses port 25.
- **POP3** (RFC 1939): a protocol to *download* messages from a server to a client, typically deleting them from the server afterward; state transitions AUTHORIZATION → TRANSACTION → UPDATE; ports 110 (995 with TLS).
- **IMAP** (RFC 3501): a protocol to *manipulate and synchronize* a server-side mailbox; supports multiple clients, folders, flags, partial fetch, search, IDLE (push-ish notification); ports 143 (993 with TLS).
- **MIME** (RFC 2045-2049): extends the message format with structured multipart bodies, non-ASCII content, and attachments.

## 8. Example
Alice (alice@corp.com) sends to bob@example.org:
```
[Alice's client] --SMTP(587, auth, TLS)--> corp.com MTA
  EHLO corp.com
  AUTH LOGIN ...
  MAIL FROM: <alice@corp.com>
  RCPT TO: <bob@example.org>
  DATA
  From: Alice <alice@corp.com>
  To: Bob <bob@example.org>
  Subject: Hello
  Message-ID: <abc123@corp.com>

  Hi Bob, meeting at 3pm.
  .
  QUIT
corp.com MTA: MX lookup for example.org -> mail.example.org (10)
  --SMTP(25)--> mail.example.org   (relay/store)
  ...if mail.example.org is down: queue + retry (store-and-forward)...
Bob's client --IMAP(993, TLS)--> mail.example.org  -> sees "Hello, unread"
Bob replies --SMTP(587)--> ... -> alice@corp.com's mailbox -> Alice sees it via IMAP
```
A bounce: if `bob@example.org` doesn't exist, the final MTA replies `550` → the *originating* MTA generates a **Delivery Status Notification (DSN)** addressed to alice@corp.com using the **envelope** sender.

## 9. Internal Working
1. **Envelope vs message**: `MAIL FROM`/`RCPT TO` define the routing envelope (used for bounces, DSNs); the headers `From`/`To` are part of the *message* and are what users see. Forging From is trivial without SPF/DKIM — hence authentication.
2. **Command/response**: SMTP is ASCII line-based; each command gets a 3-digit reply (220 ready, 250 OK, 550 failure). DATA ends with a line containing only `.` (dot-stuffing: a real `.` at line start is doubled).
3. **MX routing**: sender's MTA queries DNS `MX example.org` → `mail.example.org (10)`; picks lowest-priority MX; falls back on failure; if no MX, falls back to the domain's A record (historical).
4. **Store-and-forward**: if the receiving MTA is unavailable, the sending MTA **queues** the message and retries with backoff (typically 5 min → hours → days), then bounces after the expiry (RFC 5321, usually 2+ days).
5. **Authentication & anti-abuse**: submission requires SMTP AUTH; receivers check SPF (sender IP), DKIM (signature), DMARC (policy). Missing/  failing → reject/quarantine. Relay control: MTAs only relay for authenticated users or their own domains (open relays = spam source).
6. **IMAP internals**: commands like `LOGIN`, `SELECT INBOX`, `FETCH 1:10 BODY[]`, `STORE +FLAGS \Seen`, `SEARCH`, `IDLE` (server pushes changes). UID stability lets clients sync incrementally; state (folders, flags) is server-side.
7. **POP3 internals**: `USER`/`PASS` (or APOP), `LIST`, `RETR n`, `DELE n`, `QUIT` → server marks deleted and removes at UPDATE. No folders, no partial fetch.
8. **MIME structure**: `Content-Type: multipart/mixed; boundary=...` with parts (plain text, HTML, attachments base64). `Content-Transfer-Encoding` per part.

## 10. Time Complexity
- **Mail delivery latency**: SMTP is *not* bounded like HTTP — a message can take seconds (direct) to hours (queued relay, retry backoff). Expect no SLA; that's why transactional services retry/alert.
- **IMAP sync**: incremental (UID + flags) → O(changed messages); full mailbox on first sync O(N). IDLE gives near-real-time push (no polling).
- **POP3**: O(N) download each connect (all mail) — fine for single device, wasteful for multi-device.
- **Store-and-forward queue**: memory/disk O(messages) with bounded retry windows — the "reliability queue" of the mail system.

## 11. Advantages
- **SMTP**: universally interoperable, store-and-forward (tolerant of offline servers), simple text protocol, MX-based routing, DSN for delivery status, secure submission (STARTTLS/587 + auth).
- **IMAP**: server-authoritative (multi-device), flags/folders/search server-side, partial fetch (mobile-friendly), IDLE push, no data loss on device death.
- **POP3**: simple, minimal server storage, good for offline single-device, easy to implement.
- **MIME**: attachments, rich text, internationalization — all backward-compatible.

## 12. Disadvantages
- **No delivery guarantee / no end-to-end encryption by default**: SMTP relays are plaintext (use STARTTLS opportunistically); content visible to MTAs (hence PGP/S-MIME, rare).
- **Spam abuse surface**: without SPF/DKIM/DMARC, forgery is trivial; open relays were a disaster; spam filters are an arms race.
- **Store-and-forward latency**: email can be delayed arbitrarily (queues, greylisting).
- **POP3 limitations**: single device, download-delete semantics, no server sync.
- **IMAP complexity**: heavy protocol, server storage cost, sync conflicts, IDLE/connection management.

## 13. Interview Questions
1. **Q: What's the difference between SMTP and IMAP/POP3?** A: SMTP *sends/relays* mail (push, server-to-server and submission); POP3/IMAP *retrieve* mail (pull, server-to-client). You can't "receive" with SMTP and can't "send" with IMAP.
2. **Q: Why do we need both send and retrieve protocols?** A: Delivery must be *asynchronous* (sender/receiver rarely online together) → push with store-and-forward (SMTP). Reading is *your* action → pull (POP3/IMAP). The asymmetry reflects the postal model.
3. **Q: What ports does each use?** A: SMTP submission 587 (auth), SMTP relay 25, SMTPS/STARTTLS 465/587. POP3 110, POP3S 995. IMAP 143, IMAPS 993.
4. **Q (tricky): What is the difference between the envelope and the message headers?** A: The envelope (`MAIL FROM`/`RCPT TO`) is *routing metadata* — who it's from/to for delivery, used for bounces (DSNs). The headers (`From`, `To`, `Subject`) are part of the delivered *message* and can be forged. Bounces go to the envelope sender, not the From header.
5. **Q: How does SMTP find the recipient's server?** A: Via DNS **MX records** — `example.org MX 10 mail.example.org`; the sender's MTA connects to that host on port 25. No MX → fallback to the domain A record. MX priority handles redundancy.
6. **Q: What is store-and-forward and why does email need it?** A: Messages are queued at each MTA until the next hop is reachable, with retries and backoff. Because the recipient's server may be down for hours, email must survive async outages — SMTP's defining reliability property (unlike a phone call).
7. **Q (production): Your transactional email is landing in spam. What do you check?** A: SPF (TXT), DKIM (signed, `_domainkey`), DMARC (policy + alignment), PTR/reverse DNS matching, sending reputation, bounces/rate limits, and content signals. Deliverability is a DNS + reputation game.
8. **Q: What is a bounce / DSN?** A: When a final MTA rejects a message (550 user unknown, etc.), it returns a Delivery Status Notification to the *envelope* sender. Address validation (bounce handling) must be robust — bounces going to a real user are a classic design bug.
9. **Q: IMAP vs POP3 — when would you choose each?** A: IMAP: multiple devices, server sync, folders/flags/search, partial fetch → the modern default. POP3: single-device offline, minimal server storage, simple clients → legacy/niche. IMAP won because people have phones + laptops + web.
10. **Q (scenario): A user has "lost" mail after upgrading from POP3 to IMAP. Why?** A: POP3 download-and-delete removed mail from the server; IMAP's mailbox is server-side — so the POP3-era mail vanished from the server (it's only on the old device). Recovery: import from the old client, or keep-mode POP3.
11. **Q: What is MIME and why was it needed?** A: The original message format was ASCII-text-only. MIME (RFC 2045+) adds multipart structure (text + HTML + attachments), base64/quoted-printable encoding, and character sets — making non-ASCII and binary email possible.
12. **Q: Why is port 25 not used for user submission?** A: Port 25 is the server-relay channel; ISPs/firewalls block it for end users to stop spam relays and require authenticated submission on 587 (RFC 6409). Port 25 should be locked to authenticated/known relays only.
13. **Q (tricky): Does SMTP guarantee delivery?** A: No. It guarantees *attempted* store-and-forward delivery with retries, then a bounce. There is no end-to-end acknowledgment of receipt (that's a higher-level feature — read receipts are app-level, not SMTP).
14. **Q: What is STARTTLS?** A: SMTP upgrades an existing plaintext connection to TLS (on the same port, e.g., 587). Opportunistic STARTTLS (unauthenticated) is vulnerable to downgrade; STRICT-TLS (RFC 8461) uses MTA-STS policies to require it.
15. **Q: How does IMAP notify a client of new mail (IDLE)?** A: `IDLE` keeps the connection open; the server pushes unsolicited updates (`* 5 EXISTS`) as mail arrives — the client avoids polling. This is email's "push" on top of IMAP's pull model.
16. **Q (production): Design a reliable outgoing email service (e.g., SendGrid-like).** A: Submission endpoint (587/SES API) → queue (SQS/Kafka) → workers relay via SMTP to MX with retry/backoff + DKIM signing → track bounces/opens (webhooks) → reputation management (rate limits, warm-up, dedicated IPs) → SPF/DKIM/DMARC aligned. The queue + retry IS store-and-forward done right.

## 14. Follow-Up Questions
1. **Q: What is "greylisting" and how does it work?** A: The receiver *temporarily* rejects unknown sender mail (451), expecting legitimate MTAs to retry; spam bots usually don't. It's a cheap anti-spam filter that exploits SMTP's store-and-forward retry behavior.
2. **Q: What is an open relay and why is it bad?** A: An MTA that relays for *anyone* (not just its domains/users) — spammers abuse it as a laundering point. Modern MTAs refuse unauthenticated third-party relay.
3. **Q: How does "push email" work in the mobile world?** A: IMAP IDLE + persistent connections (or proprietary push like Exchange ActiveSync / APNs-triggered fetches) — a server-initiated signal tells the client to fetch. Classic SMTP/IMAP has no true push; push is a layer above.
4. **Q: What is DKIM alignment and why does DMARC need it?** A: DMARC checks that the SPF/DKIM-authenticated domain *aligns* with the visible From domain (relaxed = subdomain ok, strict = exact). Without alignment, a domain can't control how its mail is treated.
5. **Q: What happens to email if the recipient domain's MX is down for 3 days?** A: Sending MTAs queue + retry (backoff), then bounce after their expiry window (typically 2+ days). Recipient-side: mail is *not* delivered, senders get DSNs. High-availability mail = multiple MX priorities.

## 15. Coding Example
```python
# Minimal SMTP submission client (raw sockets, to see the protocol)
import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg["From"] = "alice@corp.com"
msg["To"] = "bob@example.org"
msg["Subject"] = "Hello"
msg.set_content("Meeting at 3pm.")

with smtplib.SMTP("smtp.corp.com", 587) as s:
    s.ehlo()                 # EHLO greeting
    s.starttls()             # upgrade to TLS
    s.login("alice", "secret")   # SMTP AUTH (submission)
    s.send_message(msg)      # MAIL FROM / RCPT TO / DATA behind the scenes
print("sent")
```
```python
# Minimal IMAP fetch (see folder/flag state = server-authoritative)
import imaplib
m = imaplib.IMAP4_SSL("imap.example.org", 993)
m.login("bob", "secret")
typ, data = m.select("INBOX")
print("Messages in INBOX:", data[0])        # b'3'
typ, data = m.search(None, "UNSEEN")
print("Unseen ids:", data[0])               # b'1 3'
typ, data = m.fetch(b"1", "(RFC822.HEADER)")
print(data[0][1][:120])
m.store(b"1", "+FLAGS", r"(\Seen)")         # mark read (server-side state)
m.logout()
```
```
# See SMTP traffic in action (relay server log style)
# 250 corp.com says HELO
# MAIL FROM:<alice@corp.com>  -> 250 2.1.0 Ok
# RCPT TO:<bob@example.org>   -> 250 2.1.5 Ok
# DATA                         -> 354 End data with <CR><LF>.<CR><LF>
# .                            -> 250 2.0.0 Ok: queued as 1A2B3C
```

## 16. Industry Usage
- **Gmail/Outlook**: submission via SMTP (587/TLS), retrieval via IMAP (993); Gmail's backend is a massive custom SMTP MTA; SPF/DKIM/DMARC enforced.
- **SendGrid/Amazon SES/Postmark**: transactional + bulk email APIs that *warp* SMTP — you call an HTTP API, they relay via SMTP with DKIM signing, queue retries, and report bounces/opens via webhooks. The modern "email as infrastructure."
- **Enterprises**: Microsoft Exchange (MAPI/EWS, IMAP-compatible), Office 365 (SMTP relay for internal apps), on-prem MTAs (Postfix/Exim) — all speaking the same SMTP wire.
- **Mailing lists/Newsletters**: Mailchimp/SendGrid use SMTP relays with dedicated IPs + reputation warm-up; delivery is tuned per-ISP.
- **Every framework**: Python `smtplib`, Node `nodemailer`, Java `JavaMail` — SMTP remains the universal send path even as UIs moved to HTTP.

## 17. References
- RFC 5321 — SMTP (obsoletes 821/2821): https://www.rfc-editor.org/rfc/rfc5321
- RFC 5322 — Internet Message Format.
- RFC 1939 — POP3: https://www.rfc-editor.org/rfc/rfc1939
- RFC 3501 — IMAP4rev1: https://www.rfc-editor.org/rfc/rfc3501
- RFC 2045-2049 — MIME; RFC 6409 — Message Submission (587).
- RFC 7208 — SPF; RFC 6376 — DKIM; RFC 7489 — DMARC.
- Kurose & Ross, *Computer Networking*, 8th ed., Ch. 2.3 (Electronic Mail).

## 18. Cheat Sheet
- Send = SMTP (587 submission w/ auth, 25 relay); Retrieve = POP3 (110/995) or IMAP (143/993).
- Envelope (MAIL FROM/RCPT TO) vs message headers — bounces use envelope.
- MX lookup (DNS) routes to the recipient MTA; priority = lower first.
- Store-and-forward = queue + retry + backoff + DSN/bounce.
- IMAP = server-authoritative sync, folders, flags, IDLE push; POP3 = download-delete.
- MIME = multipart + attachments + encodings.
- Anti-spam: SPF (TXT), DKIM (signature), DMARC (policy), PTR/reverse, no open relays.
- STARTTLS = upgrade to TLS on same port; MTA-STS (RFC 8461) for strict.
- No delivery guarantee in SMTP; DSN for failure.

## 19. Quiz
1. Which protocol sends mail? a) IMAP b) POP3 c) SMTP d) HTTP → **c**
2. Submission port with auth: a) 25 b) 587 c) 110 d) 143 → **b**
3. IMAP keeps mail: a) client-side b) server-side (authoritative) c) both d) neither → **b**
4. Bounces go to: a) From header b) envelope sender c) To header d) Reply-To → **b**
5. SMTP finds the server via: a) A record only b) MX c) SRV d) CNAME → **b**
6. POP3 default behavior: a) sync folders b) download & delete c) search d) IDLE → **b**
7. Attachments use: a) MIME b) base64 only c) JSON d) XML → **a**
8. Greylisting exploits: a) SMTP retry b) IMAP IDLE c) POP3 delete d) DNS → **a**
9. Which is an anti-spam DNS record? a) SPF b) A c) PTR d) both SPF & DMARC → **d**
10. STARTTLS: a) new port b) TLS upgrade on same port c) encryption of body d) auth → **b**

## 20. Flashcards
- **Q: SMTP vs IMAP/POP3?** → **A:** SMTP sends/relays (push); POP3/IMAP retrieve (pull).
- **Q: Ports?** → **A:** SMTP 25/587; POP3 110/995; IMAP 143/993.
- **Q: Envelope vs headers?** → **A:** Envelope = routing (MAIL FROM/RCPT TO), used for bounces; headers are message content.
- **Q: How is the recipient found?** → **A:** DNS MX record → recipient MTA on port 25.
- **Q: IMAP vs POP3?** → **A:** IMAP = server-authoritative sync + folders + IDLE; POP3 = download-delete.
- **Q: What is store-and-forward?** → **A:** Queue + retry + backoff + bounce (async delivery).
- **Q: Anti-spam DNS records?** → **A:** SPF, DKIM, DMARC (all TXT-based).

## 21. Revision
Email = SMTP (push, store-and-forward) + POP3/IMAP (pull). SMTP: submission on 587 (auth, STARTTLS), relay on 25, envelope vs message, MX routing, DSN bounces. IMAP (143/993) keeps the server authoritative — folders, flags, search, IDLE push; POP3 (110/995) downloads-and-deletes. MIME = attachments/multipart. Anti-spam = SPF/DKIM/DMARC (TXT) + PTR + no open relays. No delivery guarantee — retries + backoff then bounce. Start with the split: send=SMTP, receive=IMAP/POP3.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "SMTP vs IMAP/POP3?" | 2 How It Works / 13 Q&A |
| "Why two sets of protocols?" | 4 Why Another Approach / 13 Q&A |
| "How does SMTP route via MX?" | 9 Internal Working / 13 Q&A |
| "Envelope vs headers / bounces?" | 13 Q&A / 9 Internal Working |
| "Email in spam — what do you check?" | 13 Q&A / 16 Industry Usage |
| "IMAP vs POP3 choice?" | 13 Q&A / 10 Time Complexity |
| "What is store-and-forward?" | 13 Q&A / 7 Formal Definition |
| "Design a reliable email service." | 13 Q&A / 14 Follow-Up |
