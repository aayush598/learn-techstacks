# Part: Data Link Layer

## What this part covers
Layer 2 of the OSI model — everything that moves a *frame* across a single physical link or a shared medium. This part explains why the data link layer exists (turning an unreliable physical bit pipe into a reliable, framed channel), how it achieves reliability without end-to-end intelligence (framing, error detection, error correction, flow control), how shared media are arbitrated (ALOHA → CSMA → CSMA/CD → WiFi's CSMA/CA), and how hardware addressing (MAC addresses, ARP) and switching (VLANs, STP) build real Ethernet and WiFi networks. This is the layer FAANG interviewers probe with classic computation questions: CRC, Hamming distance, Ethernet frame layout, and stop-and-wait/go-back-N utilization math.

## Chapter map (table: chapter → sections → key skills)

| Chapter | Sections | Key skills you gain |
|---|---|---|
| ch-01 Data Link Fundamentals | Role of DLL & Framing, Error Detection (Parity/Checksum/CRC), Error Correction (Hamming code) | Explain why framing is needed, compute CRC remainder by hand, compute Hamming distance and minimum Hamming distance, correct single-bit errors with Hamming code |
| ch-02 MAC and Access Control | MAC addresses & ARP, Flow Control (Stop-and-Wait/GBN/Selective Repeat), Multiple Access (ALOHA/CSMA/CSMA-CD), Ethernet in Depth, WiFi 802.11, Switching/VLAN/STP | Explain MAC address format, ARP/RARP/GARP, compute stop-and-wait utilization, walk CSMA/CD collision math, lay out an Ethernet frame byte-by-byte, explain 802.1Q VLAN tagging, walk STP root-bridge election |

## Study order
1. **ch-01 first** — framing and error control are the *reasons* the layer exists; every other section assumes you know why frames exist and how errors are caught.
2. **ch-02** — access control and Ethernet/WiFi build the mechanism layer: how does a device actually get to transmit, and what do real L2 networks look like?
3. **Sections must be read in numbered order** within each chapter — Section 01 (MAC addresses) is a prerequisite for Section 06 (switching), and Section 03 (multiple access) is a prerequisite for Sections 04-05 (Ethernet/WiFi).

## Interview importance (0-5 stars) + which companies emphasize it
- **Importance: ⭐⭐⭐⭐ (4/5)** — CRC and Hamming-distance questions are among the most *computable* networking interview questions, so interviewers love them (you cannot bluff your way through a polynomial division). Ethernet frame and ARP questions are standard "networking 101" filters.
- **Emphasized by**: networking-infra teams at Cloudflare, Google (network engineering + SWE for GCP), Amazon (VPC/EC2 networking), Meta (datacenter networking), Arista/Cisco, and any role interviewing "the OSI stack top-down or bottom-up."
- Typical asked: "Compute the CRC for this bitstring", "What is the minimum Hamming distance to detect/correct d errors?", "What is in an Ethernet frame?", "How does CSMA/CD detect collisions?", "Why does WiFi use CSMA/CA and not CSMA/CD?", "How does ARP work and what is ARP spoofing?"

## How the parts connect (roadmap)
- **Part 05 sits between the Physical layer and the Network layer.** The Physical layer (Part 06) sends raw bits; the data link layer turns those bits into *frames* with addresses and checksums. The Network layer (Part 03/04, handled by the parallel parts) hands the data link layer IP packets that become frames.
- **Part 06 (Physical Layer)** supplies the medium (twisted pair, fiber, radio) that frames must survive — CRC and framing are precisely the compensation for noisy media described there.
- **Part 07 (Network Security)** builds on ARP (ARP spoofing), MAC address randomization (privacy), and switch security (VLAN hopping, MAC flooding) — the attacks live at the layer this part describes.
- **Part 08 (Advanced Topics)** uses Layer 2 switching, VLANs, and anycast/broadcast mechanics that you'll only understand after this part.
