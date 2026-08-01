# Chapter: OSI & TCP/IP Models

## What you'll learn
- The seven OSI layers, in order, with the exact responsibility of each and the PDU names.
- The four-layer TCP/IP model and how it maps to OSI.
- The critical differences between OSI and TCP/IP (reference vs. operational model).
- Encapsulation/decapsulation — how data physically moves down and up the stack, with PDU chaining (data → segment → packet → frame → bits).

## Prerequisites (linked)
- [Chapter 01: Network Basics](../chapter-01-network-basics/README.md) — you need the vocabulary (host, link, protocol) and the concept of networks before understanding the layered organization of protocols.

## Sections (linked table)
- [section-01-osi-model-seven-layers-in-depth](section-01-osi-model-seven-layers-in-depth.md)
- [section-02-tcp-ip-model-four-layers](section-02-tcp-ip-model-four-layers.md)
- [section-03-osi-vs-tcp-ip-model](section-03-osi-vs-tcp-ip-model.md)
- [section-04-encapsulation-decapsulation-and-pdu](section-04-encapsulation-decapsulation-and-pdu.md)

## One-paragraph narrative connecting all sections
The OSI model (section 01) is the conceptual *taxonomy* — seven layers each with a clean responsibility, so engineers can reason about protocol design without hardware details. The TCP/IP model (section 02) is the *actual* protocol suite running the Internet — four layers, built bottom-up around what really got deployed (IP, TCP, HTTP). Comparing them (section 03) shows where theory and practice diverge (e.g., OSI's session/presentation layers collapsed into application in TCP/IP). Finally, encapsulation (section 04) is the *mechanism* that makes layers work together — each layer wraps the previous layer's PDU with its own header, which is how the same stack can carry Ethernet at one hop and IP across the whole Internet.

## Common interview trap in this chapter
Trap: "The OSI model is what the Internet runs on." — **Wrong.** The Internet runs TCP/IP. OSI is a *reference* model that (mostly) failed to be deployed (the OSI protocol stack lost to TCP/IP in the 1990s). Also a trap: memorizing layer numbers but confusing *which protocol* lives at *which layer* — e.g., TLS is often called "layer 4.5" (session layer) because it sits between transport and application. And the classic: "HTTP is layer 7, TCP is layer 4, IP is layer 3, Ethernet is layer 2" — be able to say that instantly.

## Checklist before moving on
- [ ] I can recite OSI layers in order and give one protocol/device for each layer.
- [ ] I can map every TCP/IP layer to the OSI layer(s) it merges.
- [ ] I can list 3 concrete differences between OSI and TCP/IP.
- [ ] I can walk through encapsulation for a web request, naming the PDU at each layer (data → segment → packet → frame → bits).
- [ ] I can name the PDU for every OSI layer.
- [ ] I can explain why "layer 4.5" (TLS) exists conceptually.
