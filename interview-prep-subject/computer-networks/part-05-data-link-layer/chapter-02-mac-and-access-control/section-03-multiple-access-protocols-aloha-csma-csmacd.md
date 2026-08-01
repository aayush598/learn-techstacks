# Multiple Access Protocols: ALOHA, CSMA, CSMA/CD

> **TL;DR**: When many stations share one medium (a wire, a radio channel, a satellite transponder), a multiple access protocol decides *who gets to talk and when* — from ALOHA's sloppy 18% utilization, through listen-before-talk (CSMA) and collision detection + backoff (CSMA/CD) that powered classic Ethernet, up to the collision-*avoidance* (CSMA/CA) WiFi had to invent because radios can't listen while they transmit.

## 1. Why Does This Exist?
Sharing a medium is the original networking problem: in the 1970s a single coaxial cable carried all traffic in a building — anyone could transmit, and if two transmitted at once, the signals collided and both frames were destroyed. Without coordination, efficiency collapses (when everyone transmits, nobody's data survives). Multiple access protocols exist to (a) decide *when* a station may transmit so that throughput stays high, (b) detect when a collision happened so the sender can retry, and (c) give *fair* access so one station can't hog the channel. They also underpin modern systems: cellular (TDMA/FDMA/CDMA/OFDMA), satellite, and WiFi all descend from the same "shared channel" problem. Ethernet, WiFi, and cellular each chose a different point on the *centralized-vs-random* spectrum, and the ALOHA→CSMA→CSMA/CD evolution is a pure lesson in engineering trade-offs.

## 2. How Does It Work?
Three families: **(1) Random access** — stations transmit whenever they have data and deal with collisions: ALOHA (transmit anytime), slotted ALOHA (transmit in fixed slots), CSMA (listen first — *carrier sense*), CSMA/CD (listen + detect collision + binary exponential backoff), CSMA/CA (listen + wait a random backoff *before* transmitting to avoid collisions). **(2) Channel partitioning** — divide the medium by time (TDMA), frequency (FDMA), or code (CDMA): deterministic, no collisions, but wasteful when few stations are active. **(3) Taking turns** — polling, token passing (Token Ring): fair and collision-free but has token/poll overhead. The key numbers to memorize: pure ALOHA max throughput = 1/(2e) ≈ 18%, slotted ALOHA = 1/e ≈ 37%, and CSMA/CD with a 512-bit slot time (Ethernet).

## 3. When Is It Used?
- **Pure/slotted ALOHA**: satellite uplinks and early packet radio; a *historical* but mathematically famous model.
- **CSMA/CD**: classic shared-Ethernet (10BASE5/2/T 10 Mb/s half-duplex) and its collision domain math; still required knowledge because the "minimum frame size / slot time" constraint is tested.
- **CSMA/CA**: all WiFi (IEEE 802.11 DCF) — WiFi *cannot* detect collisions because a radio can't hear while transmitting, so it avoids them.
- **FDMA/TDMA/CDMA/OFDMA**: 2G/3G/4G/5G cellular, satellite transponders, and cable (DOCSIS); deterministic sharing.
- **Token passing**: Token Ring / FDDI (legacy) — deterministic access for real-time LAN traffic.

## 4. Why Wasn't Another Approach Chosen?
- *Alternative: give everyone a dedicated line (FDMA-style) from the start.* Deterministic and collision-free but idle capacity is wasted — with N users you get 1/N of the channel even when others are silent; random access lets a single active user take the whole channel. That's the fundamental tension random access answers.
- *Alternative: central controller scheduling (polling) always.* Works (Token Ring, cellular) but needs the controller to know demand, adds latency, and creates a single point of failure; on a flat shared cable, decentralized random access was simpler and more robust.
- *Alternative: ALOHA (no sensing).* Trivially simple but max 18% throughput because it doesn't exploit the obvious fact that you can *listen* to see if the channel is busy. Adding carrier sense (CSMA) was nearly free and doubled practical efficiency.
- *Alternative: CSMA without collision detection.* Better than ALOHA but the *entire* frame is wasted on a collision and the sender doesn't know; CSMA/CD lets the sender abort within one slot, freeing the channel faster — that's where Ethernet's "64-byte minimum" comes from (so a sender is still transmitting when its own collided echo returns).
- *Alternative: CSMA/CD for WiFi.* Impossible — a WiFi radio can't transmit and receive simultaneously on the same frequency (no "listen while talk"); hence CSMA/CA + ACKs, and hidden/exposed terminal handling via RTS/CTS. The choice is forced by physics.

## 5. Intuition
A shared medium is a **room full of people trying to speak** (a party). ALOHA: everyone shouts whenever they like — when two shout at once (collision), both sentences are garbled, and it turns out the room can only ever be ~18% "useful speech." Slotted ALOHA: everyone speaks only at the tick of a clock — collisions still happen but waste half as much time (37%). CSMA: everyone *listens first* and only speaks when the room is quiet (carrier sense) — the useful speech jumps. CSMA/CD: while speaking, you also *listen for your own voice coming back garbled*; the instant you hear two voices, you stop, wait a random time, and retry (binary exponential backoff). WiFi is the room where you *can't listen while you speak* (your radio can't hear), so you use CSMA/CA: check it's quiet, then wait a *random* extra moment and only then speak, hoping others don't start at the same instant.

## 6. Real-World Analogy
A **single-lane bridge shared by neighbors**. ALOHA: everyone drives across whenever they want — when two enter at once, both crash, and each must tow away (retransmit); the bridge is efficient only ~18% of the time. CSMA: before driving on, you look to see if anyone's on the bridge (carrier sense). CSMA/CD: while driving across, you also watch for a car coming the other way; on sighting one you *reverse immediately* (abort), wait a random time (backoff), and try again. WiFi (CSMA/CA) is a foggy bridge where you can't see the far end: you listen, then wait a random extra delay and *honk first* (RTS/CTS) to make sure no one else is crossing before you commit.

## 7. Formal Definition
A multiple access protocol coordinates transmissions by M stations sharing a single broadcast channel so that, ideally, exactly one station transmits successfully at a time. **Pure ALOHA**: a station transmits immediately; a frame succeeds only if no other frame began in the previous *or* current frame time → max throughput S_max = G·e^(−2G) = **1/(2e) ≈ 0.184** (at offered load G = 0.5). **Slotted ALOHA**: transmissions start only at slot boundaries → S_max = G·e^(−G) = **1/e ≈ 0.368** (G = 1). **CSMA**: listen before transmit; **persistent variants** (1-persistent: transmit if idle; p-persistent: transmit with probability p). **CSMA/CD**: additionally detect a collision and abort — the **slot time** (512 bit-times = 51.2 µs at 10 Mb/s) is the time a sender must transmit to guarantee collision detection; binary exponential backoff after each collision doubles the wait window (k-th collision: choose k ∈ [0, 2^k − 1] slots, capped at 1023).

## 8. Example
**Ethernet CSMA/CD collision window math.** At 10 Mb/s, a 2.5 km network (with repeaters) has worst-case round-trip ≈ 51.2 µs = 512 bit-times. A sender must still be transmitting when the collided echo returns — so the minimum frame must be ≥ 512 bits = **64 bytes** (preamble excluded). Worked: t_prop ≈ 25 µs one-way → RTT ≈ 50 µs; add repeater/jabber margins → 51.2 µs. A 46-byte payload + 18-byte header = 64 bytes minimum. If frames could be shorter than the slot, a station would finish, drop carrier, and *never learn* about the collision — silent corruption. That's the "why 64 bytes" answer.

**ALOHA throughput.** Frame time = 1 unit. G = 0.5: P(success) = e^(−2·0.5) = e^(−1) = 0.368 → S = 0.184. At G = 1 (each frame time sees 1 arrival on average), slotted P = e^(−1) = 0.368. Doubling efficiency just by slotting.

## 9. Internal Working
1. **ALOHA**: transmit on demand; no sensing; if no ACK within timeout, wait random time and retransmit. A frame collides if *any* other frame overlaps it — the 2G window (two frame times) explains the e^(−2G).
2. **Slotted ALOHA**: divide time into slots ≥ frame time; start only at slot edges → collision window halves → e^(−G).
3. **CSMA**: listen; if busy, wait (1-persistent: keep sensing and grab immediately when free; non-persistent: wait a random time then re-sense — less collision-prone but more latency). Even so, two stations may sense idle *simultaneously* and collide — carrier sense can't eliminate collisions, only reduce them.
4. **CSMA/CD**: (a) sense idle → transmit; (b) while transmitting, monitor the receive pair for a signal stronger than expected (collision); (c) on collision → jam (send 32-bit jamming signal to make sure everyone detects), abort; (d) exponential backoff: k-th collision, wait uniform random in [0, 2^k − 1] slots (k capped at 10, retry cap 16); (e) retry.
5. **Efficiency model**: with A stations each probing with probability p in a slot, P(success) = A·p·(1−p)^(A−1), maximized when p = 1/A → tends to 1/e as A→∞. The slot time is the natural unit of this analysis.
6. **Modern Ethernet**: full-duplex point-to-point links have no shared medium → CSMA/CD is disabled; the 64-byte minimum survives as a legacy compatibility rule.

## 10. Time Complexity / Efficiency Math
- Pure ALOHA: S_max = 1/(2e) ≈ **18.4%** (G = 0.5).
- Slotted ALOHA: S_max = 1/e ≈ **36.8%** (G = 1).
- CSMA/CD Ethernet: efficiency ≈ 1/(1 + 5·t_prop/t_frame) for small contention — near 100% for long frames on short networks; degrades as A grows and frames shrink.
- Backoff: expected wait grows exponentially — O(2^k) slots on the k-th collision; the protocol is *decentralized*, so complexity is per-station constant state.
- Slot time: 512 bit-times at 10 Mb/s → 51.2 µs; scales with speed (at 100 Mb/s the max distance shrinks to ~200 m precisely to keep the slot time feasible).

## 11. Advantages
- **ALOHA**: dead simple, no sync, works for any topology — the reason it's still the model for bursty satellite access.
- **Slotted ALOHA**: doubles throughput with just clock sync.
- **CSMA/CD**: high efficiency on wired LANs (~90%+), fully decentralized, robust to station failure, no central point of failure, graceful degradation via backoff.
- **General lesson**: random access is *work-conserving* — an idle station doesn't consume capacity, and a single active station can use the entire channel.
- **Backoff fairness**: binary exponential backoff smooths contention without global state.

## 12. Disadvantages
- **ALOHA**: catastrophic at high load (throughput falls after G = 0.5); no fairness guarantee; collisions waste whole frames.
- **CSMA**: still wastes whole frames on collisions (no abort); "capture effect" — one station may repeatedly win backoff, starving others (unfairness under some loads).
- **CSMA/CD**: requires a bounded diameter (min frame ≥ 2·max propagation) — that's why distance is capped; useless on radio (can't listen while transmit) and on full-duplex point-to-point links (no collisions to detect).
- **All random access**: no latency guarantee — unsuitable for real-time/isochronous traffic (hence TDMA/token for that).
- **Hidden terminal problem**: in radio, two stations out of range of each other both transmit to a common receiver → collision at the receiver, invisible to either sender (RTS/CTS only partially fixes this).

## 13. Interview Questions
1. **Q: What is the max throughput of pure and slotted ALOHA, and why the difference?** A: Pure = 1/(2e) ≈ 18.4% (collision window is 2 frame times → e^(−2G)); slotted = 1/e ≈ 36.8% (transmissions align to slots → e^(−G), window is 1 frame time). Slotting halves the vulnerable period.

2. **Q: Why can carrier sense (CSMA) never eliminate collisions?** A: Because of propagation delay: two stations can sense the channel idle *simultaneously* and both start — neither hears the other until their signals meet, which is after they've both committed. CSMA reduces but cannot remove collisions.

3. **Q: What does CSMA/CD stand for and what does the "CD" enable?** A: Carrier Sense Multiple Access with Collision Detection — the sender listens *while transmitting* and aborts as soon as it detects a collision, saving the rest of the frame and freeing the channel within one slot time.

4. **Q: Explain the 64-byte minimum Ethernet frame size.** A: The slot time (512 bit-times at 10 Mb/s ≈ 51.2 µs) must exceed the worst-case round-trip propagation so a sender is still transmitting when its collided signal returns; 512 bits = 64 bytes. Shorter frames would finish before detecting the collision.

5. **Q: What is binary exponential backoff?** A: After the k-th collision, a station waits a random number of slots drawn uniformly from [0, 2^k − 1], capped at 2¹⁰ = 1023 slots, and stops retrying after 16 attempts. Doubling the range adapts to heavier contention and randomizes retries.

6. **Q: TRICKY — Why did 100 Mb/s Ethernet shrink the maximum network diameter?** A: The slot time must stay ≥ the collision window. At 100 Mb/s, 512 bit-times = 5.12 µs, so the round-trip must be ≤ 5.12 µs → max ~200 m (vs 2.5 km at 10 Mb/s). Fast Ethernet accepted a shorter span instead of a bigger minimum frame.

7. **Q: Why does WiFi use CSMA/CA and not CSMA/CD?** A: A WiFi radio cannot transmit and receive on the same channel at once (no full-duplex on the air), so it can't "hear" a collision while talking. It must *avoid* collisions: sense idle, then wait a random backoff (DIFS + CW) before transmitting, and confirm with an ACK.

8. **Q: What are the hidden and exposed terminal problems?** A: Hidden: A→B and C→B, but A and C can't hear each other → both transmit → collide at B. Exposed: A→B and C→D where C can hear A but not interfere → C needlessly defers. RTS/CTS handshake reduces hidden-terminal collisions; exposed terminals remain a known inefficiency.

9. **Q: PRODUCTION — Why is CSMA/CD "disabled" on modern Ethernet?** A: Switches connect every node on a *dedicated full-duplex* point-to-point link — there's no shared medium, so no collisions can occur. The 64-byte minimum and slot-time machinery survive as compatibility constraints; duplex negotiation sets FD and the MAC never senses.

10. **Q: SCENARIO — Two hosts on half-duplex Ethernet keep colliding under load. How do you diagnose?** A: Check duplex mismatch (one side auto-negotiated FD, other forced HD → late collisions), cable length/quality, faulty NIC, or a too-large collision domain. Use `ethtool eth0` for speed/duplex, `mii-tool`, and NIC `collisions`/`late_collisions` counters — on a properly configured switch link these should be ~0.

11. **Q: What is the relationship between slot time, minimum frame size, and network diameter?** A: Min frame (bits) ≥ slot time ≥ 2 × worst-case propagation (round trip). Given speed and diameter you derive the minimum frame; given frame and speed you derive max diameter. 512 bit-times ties 64 bytes, 10 Mb/s, and 2.5 km together.

12. **Q: TRICKY — In slotted ALOHA with 10 stations each sending in a slot with probability p, what p maximizes throughput and what's the max?** A: p = 1/10. P(success) = 10·(1/10)·(9/10)⁹ ≈ 0.348; as N→∞ the max tends to 1/e ≈ 0.368. The formula: maximize N·p·(1−p)^(N−1).

13. **Q: What is a "capture effect"?** A: In CSMA/CD, after a collision the backoff is random, but a station with better luck (smaller waits) can keep winning the channel repeatedly while another starves — throughput becomes unfair. It's a known pathology of exponential backoff under asymmetric load.

14. **Q: Compare random access vs channel partitioning for a bursty workload.** A: Partitioning (TDMA/FDMA) guarantees each user 1/N capacity but wastes it when users are idle — bad for bursty traffic. Random access is work-conserving: idle users consume nothing and active users get the whole channel — great for bursts but no latency bound. This trade-off drives "reservation" hybrid schemes.

15. **Q: PRODUCTION — Why does cellular use scheduled (OFDMA/TDMA) access instead of CSMA?** A: Cells have tight synchronization, centralized scheduling, and QoS/latency requirements (voice, 5G URLLC) that random access can't guarantee; the base station *assigns* resource blocks. Random access is reserved for *initial access* (PRACH) before scheduling starts.

16. **Q: What happens to ALOHA throughput at very high load (G → ∞)?** A: It collapses toward 0 — everyone transmits, everything collides, throughput falls, and delay grows without bound (throughput peaks at G = 0.5 for pure ALOHA then declines). This is the classic "congestion collapse" that motivated carrier sense.

17. **Q: What is a jamming signal for?** A: After detecting a collision, the sender transmits a 32-bit (sometimes 48-bit) jam sequence so that *all* stations — including ones that might not detect the weak collided signal — are guaranteed to see a violation and back off. It ensures everyone enters backoff, not just the two involved.

18. **Q: TRICKY — Ethernet min frame is 64 bytes, but payload minimum is 46 bytes. Why the 46?** A: 64 bytes total − 14 (header) − 4 (FCS) = 46 bytes of payload. If the IP packet is shorter, the MAC pads to 46 (with a length/type field indicating the true length). The 64-byte floor exists for collision detection, and the padding preserves it.

## 14. Follow-Up Questions
1. **Q: Why does WiFi's DCF use a random backoff even when the channel seems idle?** A: After a DIFS idle period, several stations that were waiting may all sense idle at once and transmit simultaneously — the random backoff (contention window 15→1023 slots) decorrelates them. It's "CSMA with randomized start" to make collisions rare instead of guaranteed.

2. **Q: What is the difference between 1-persistent and p-persistent CSMA?** A: 1-persistent grabs the channel the moment it's idle (low latency, more collisions when many wait); p-persistent transmits with probability p after sensing idle (spreads starts, fewer collisions, more delay). Non-persistent waits a random time before re-sensing.

3. **Q: How does the slot-time constraint translate to a *maximum* frame or network size at higher speeds?** A: Since speed rises, 512 bit-times shrink; keeping min frame 64 bytes forces diameter to shrink (100 Mb/s → ~200 m) unless you raise the minimum frame (Gigabit uses carrier extension to 512 bytes to keep the collision window). At 10 GbE it's full-duplex-only — no CD at all.

4. **Q: What's the "backoff slot" duration on real Ethernet?** A: One slot time = 512 bit-times = 51.2 µs at 10 Mb/s, 5.12 µs at 100 Mb/s; the backoff counter increments in slots, so latency scales with line speed.

## 15. Coding Example
```python
import random

def aloha_throughput(g, slots=False):
    """Efficient frontier: pure vs slotted ALOHA."""
    if slots:
        return g * (2.71828 ** -g)        # e^{-G}
    return g * (2.71828 ** (-2 * g))      # e^{-2G}

print(f"pure max @G=0.5: {aloha_throughput(0.5):.3f}")      # 0.184
print(f"slotted max @G=1: {aloha_throughput(1, slots=True):.3f}")  # 0.368

def csma_cd_sim(stations=4, frames=1000, max_attempts=16):
    """Simplified CSMA/CD with binary exponential backoff."""
    losses = 0
    for _ in range(frames):
        attempts = 0
        while True:
            if random.random() < 0.85:      # channel "free"
                if random.random() < 0.7:   # no collision
                    break
            attempts += 1
            if attempts >= max_attempts:
                losses += 1
                break
            k = min(attempts, 10)
            random.uniform(0, 2 ** k)       # BEB wait
    return losses / frames

def slot_time_mins(speed_mbps, diameter_km, v=0.66 * 299792458):
    """Minimum frame size (bits) for a given speed & diameter (CSMA/CD)."""
    prop = diameter_km * 1000 / v            # one-way
    return 2 * prop * (speed_mbps * 1e6)     # RTT in bit-times

print(f"10Mb/s 2.5km -> min {int(slot_time_mins(10, 2.5))} bits")   # ~512
print(f"100Mb/s 0.2km -> min {int(slot_time_mins(100, 0.2))} bits") # ~512
```
```bash
# Observe collisions/backoff on real interfaces
ethtool eth0 | grep -E "Speed|Duplex"            # must be 1000/full on modern nets
ethtool -S eth0 | grep -Ei "collision|tx_abort|late_collision"  # CSMA/CD-era counters
ip -s link show eth0                             # tx/rx packet + error stats
# On a legacy hub you'd see: ethtool -S | grep collisions rising
```

## 16. Industry Usage
- **Legacy Ethernet (10BASE-T, 100BASE-TX half-duplex)**: CSMA/CD; still taught and still on old hardware; Gigabit+ Ethernet is effectively full-duplex-only.
- **WiFi (IEEE 802.11)**: CSMA/CA + DCF with exponential backoff; 802.11ax adds OFDMA (scheduled) access on top for efficiency — a hybrid of random and partitioned access.
- **Cellular (4G/5G)**: OFDMA/FDMA/TDMA scheduling; random access only for initial connection (PRACH).
- **Satellite**: ALOHA variants for bursty VSAT/DVB return channels; TDMA/FDMA for structured services.
- **Cable (DOCSIS)**: TDMA upstream with contention slots for registration — hybrid reservation/random.
- **Data centers**: modern DC Ethernet is all full-duplex point-to-point; but the *congestion* problem is handled by PFC (Priority Flow Control) and ECN — different tools for the same "shared bottleneck" goal.

## 17. References
- Kurose & Ross, *Computer Networking*, 8th ed., §6.3 (Multiple Access Links and Protocols).
- Tanenbaum & Wetherall, *Computer Networks*, 6th ed., §4.2 (Ethernet), §4.3 (Wireless LANs).
- N. Abramson, "The ALOHA System," 1970 (the original 1/2e result).
- R. Metcalfe & D. Boggs, "Ethernet: Distributed Packet Switching for Local Computer Networks," CACM 1976 (CSMA/CD original paper).
- IEEE Std 802.3-2022, §4 (MAC) and §13 (full duplex) — https://standards.ieee.org/ieee/802.3/10422/
- IEEE Std 802.11-2020, §9 (MAC sublayer, DCF) — https://standards.ieee.org/ieee/802.11/7028/

## 18. Cheat Sheet
- Pure ALOHA S_max = 1/(2e) ≈ 18% (G=0.5); slotted = 1/e ≈ 37% (G=1).
- CSMA: listen before talk; CD: listen *while* talking + abort + backoff.
- Slot time = 512 bit-times = 51.2 µs @10 Mb/s = 2×max propagation.
- Min Ethernet frame = 64 B = 512 bits; 46 B payload min (pad rest).
- Binary exponential backoff: k-th collision → wait U[0, 2^k −1] slots, cap 1023, give up at 16.
- CSMA/CD needs bounded diameter; 100 Mb/s → ~200 m max.
- WiFi can't do CD → CSMA/CA (DIFS + random contention window + ACK); RTS/CTS for hidden terminals.
- Random access = work-conserving but no latency bound; partitioning = deterministic but wasteful when idle.
- Jam signal (32-bit) makes everyone back off after a collision.
- Full-duplex switch links = no shared medium = no CSMA/CD at all.

## 19. Quiz
1. Pure ALOHA max efficiency: a) 50% b) 18.4% c) 36.8% d) 90% → **b**
2. Slotted ALOHA max efficiency: a) 18.4% b) 50% c) 36.8% d) 100% → **c**
3. Ethernet slot time at 10 Mb/s: a) 5.12 µs b) 51.2 µs c) 512 µs d) 100 µs → **b**
4. Minimum Ethernet frame: a) 46 B b) 64 B c) 1500 B d) 128 B → **b**
5. Why can't WiFi use CSMA/CD? a) too slow b) can't hear while transmitting c) too many users d) uses fiber → **b**
6. On the k-th collision, backoff is uniform in: a) [0,k] b) [0,2^k −1] c) [0, k²] d) [1,2^k] → **b**
7. RTS/CTS addresses the: a) capture effect b) hidden terminal c) jamming d) slot time → **b**
8. Modern switched Ethernet runs: a) CSMA/CD b) full duplex, no collisions c) token passing d) ALOHA → **b**

**Answers**: 1-b, 2-c, 3-b, 4-b, 5-b, 6-b, 7-b, 8-b.

## 20. Flashcards
- **Q: Pure vs slotted ALOHA efficiency?** → **A:** 1/(2e) ≈ 18% vs 1/e ≈ 37%; slotting halves the vulnerable window.
- **Q: Why doesn't CSMA eliminate collisions?** → **A:** Propagation delay lets two stations sense idle simultaneously and both start.
- **Q: What does the 512-bit slot time enforce?** → **A:** Minimum frame ≥ 64 bytes so the sender is still transmitting when its collision returns.
- **Q: What is binary exponential backoff?** → **A:** k-th collision → wait U[0, 2^k−1] slots, cap 1023, abort at 16 tries.
- **Q: Why WiFi uses CA not CD?** → **A:** Radios can't listen while transmitting; must avoid collisions, not detect them.
- **Q: What is the hidden terminal problem?** → **A:** Two senders can't hear each other but collide at the receiver; mitigated by RTS/CTS.
- **Q: Why is CSMA/CD gone on modern LANs?** → **A:** Full-duplex point-to-point switch links have no shared medium → no collisions to detect.

## 21. Revision
Multiple access decides who speaks on a shared channel. **ALOHA** (transmit anytime) tops out at 1/2e ≈ 18%; **slotted ALOHA** at 1/e ≈ 37%. **CSMA** adds listen-before-talk, but propagation delay still causes collisions. **CSMA/CD** (Ethernet) listens while transmitting, aborts on collision, and backs off exponentially — and its constraints live in the 512-bit slot time / 64-byte minimum frame / bounded diameter. **WiFi** can't detect collisions over the air, so it uses CSMA/CA (sense idle → random backoff → transmit → ACK) plus RTS/CTS against hidden terminals. Trade-off to remember: random access is work-conserving but unpredictable; partitioning (TDMA/FDMA) is deterministic but wastes idle capacity. Modern data centers are all full-duplex switched links where CSMA/CD is history — but its math is still a favorite whiteboard question.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Max throughput of ALOHA/slotted ALOHA?" | 8 / 13-Q1 |
| "Why can't CSMA eliminate collisions?" | 13-Q2 / 9 |
| "Explain the 64-byte minimum / slot time" | 8 / 13-Q4,11 |
| "What is binary exponential backoff?" | 13-Q5 / 9 |
| "Why WiFi uses CSMA/CA not CSMA/CD?" | 13-Q7 / 4 |
| "Hidden vs exposed terminal / RTS-CTS" | 13-Q8 |
| "Why is CSMA/CD disabled on modern switches?" | 13-Q9 / 6 |
| "Diagnose repeated collisions in production" | 13-Q10 |
| "Random access vs partitioning trade-off" | 13-Q14 / 4 |
