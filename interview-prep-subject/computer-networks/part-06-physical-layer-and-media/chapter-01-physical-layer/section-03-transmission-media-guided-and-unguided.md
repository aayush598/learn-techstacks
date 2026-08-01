# Transmission Media: Guided and Unguided

> **TL;DR**: Transmission media are the physical paths signals travel — guided (twisted pair, coaxial cable, optical fiber) and unguided (radio, microwave, infrared) — and choosing among them is a distance/rate/cost/interference trade-off: fiber wins for long-haul and high rate, twisted pair for short cheap links, and radio where mobility is non-negotiable.

## 1. Why Does This Exist?
The physical layer must move energy between transmitter and receiver, and it needs a medium to do it. Every medium is a channel with specific properties — bandwidth, attenuation, noise susceptibility, cost per meter, installation difficulty, and mobility — and those properties are exactly the "physics" that Nyquist/Shannon and the encodings in Sections 01-02 operate on. Choosing a medium is the single most consequential physical-layer decision: it sets the maximum rate, the maximum distance, the error rate, the cost, and the deployment model. Media exist because there is no one "best" channel — a data center rack, a transatlantic cable, a phone in your pocket, and a warehouse sensor need completely different physical paths. The design job is matching the medium to the requirement.

## 2. How Does It Work?
**Guided media** confine the signal: **twisted pair** — two insulated copper wires twisted together (twisting cancels electromagnetic interference/crosstalk), used differentially (a signal + its inverse; the receiver subtracts → common-mode noise cancels). **Coaxial cable** — center conductor + braided shield (shield blocks EMI; high bandwidth, long reach). **Optical fiber** — a glass/silica core with a cladding of lower refractive index; light is confined by total internal reflection; single-mode (small core, laser, long reach) vs multi-mode (larger core, LED/VCSEL, short reach); WDM multiplies wavelengths. **Unguided/radio** — an antenna radiates an EM wave; the wave's frequency band, power, and propagation (LOS, reflection, diffraction) determine range; no physical guide, so anyone in range can receive. Transmitters couple energy into the medium; receivers extract it; repeaters/amplifiers regenerate where attenuation wins.

## 3. When Is It Used?
- **Twisted pair (Cat5e/6/6A/7/8)**: Ethernet to the desktop, homes, offices; short (<100 m) links; the cheapest guided medium; also telephony and DSL.
- **Coaxial cable**: cable TV/Internet (DOCSIS), legacy 10BASE2/5, short-haul RF, and (in passive form) antenna runs.
- **Fiber**: data centers (10G-400G), metro/long-haul/undersea, campus backbone, SAN (Fibre Channel), and any link over ~100 m or needing immunity to EMI (power stations, factories).
- **Radio (WiFi, cellular, Bluetooth, satellite, microwave backhaul, 5G mmWave, LoRa)**: anything mobile, no-cabling, broadcast, or beyond reach of wired media.
- **Infrared**: remote controls, IrDA, short-range line-of-sight (legacy).
- **Undersea fiber**: ~99% of international traffic — the ultimate long-haul case.

## 4. Why Wasn't Another Approach Chosen?
- *Alternative: use radio for everything.* No cabling, mobility — but radio is shared, half-duplex, low-bandwidth per user, interference-prone, and range-limited (and needs licenses in many bands). Wired media give dedicated, gigabit+ channels at cents-per-meter. This is why fixed infrastructure is always wired.
- *Alternative: use fiber for everything.* Fiber has unbeatable bandwidth and reach, but terminating it is expensive (optics, splicing, alignment) and it's fragile (bending), so the *last meters* to a desktop/phone are copper or radio. The split is economic: fiber where bandwidth/distance matters, copper where cost matters.
- *Alternative: unshielded everywhere.* Twisting + shielding (STP) trades cost for EMI immunity — chosen when noise (industrial, cross-run cables) demands it. Shielded Cat6A costs more and is harder to terminate.
- *Alternative: multi-mode for long distances.* Multi-mode (MMF) is cheap (LED/VCSEL) but dispersion limits it to ~100-500 m; single-mode (SMF) with lasers goes 80+ km. The choice follows reach: MMF in-rack/short, SMF for everything far.
- *Alternative: stay guided with coax everywhere.* Coax is robust and high-bandwidth but bulky, expensive, and single-channel per cable; twisted pair is cheaper per drop, and fiber beats both at distance. Coax survives only in cable plant and legacy RF.

## 5. Intuition
Think of media as **roads for energy**: twisted pair is a narrow city street (cheap, short, noise gets in at intersections), coax is a divided highway with sound walls (faster, shielded), fiber is a laser-carved tunnel (incredibly fast, isolated, but expensive to build), and radio is the sky (you can go anywhere, but everyone shares the air and weather affects you). The longer and faster you need to go, the more you pay for a better "road"; the more mobile you need to be, the more you rely on the "sky."

## 6. Real-World Analogy
A **city's delivery network**: letter carriers on foot (twisted pair — cheap, slow, short hops, every door), cargo vans (coax — faster, shielded, medium distance), an expressway trucking system (fiber — huge capacity, long distance, expensive infrastructure), and helicopters (radio — anywhere, but limited capacity and weather-dependent). Nobody ships everything by helicopter; you choose per delivery. Similarly, a 400G data-center spine is fiber, the last 3 meters to your desk is Cat6A, and your phone is radio — all three "delivering packets" differently.

## 7. Formal Definition
**Guided media**: transmission where the signal is constrained along a physical path.
- **Twisted pair**: two insulated conductors twisted in a helix; differential signaling rejects common-mode noise; categories (Cat5e/6/6A) specify bandwidth (100 MHz-500 MHz) and reach (~100 m for 10GBASE-T); unshielded (UTP) vs shielded (STP/FTP).
- **Coaxial cable**: concentric structure — inner conductor, dielectric, braided shield, jacket; characteristic impedance 50-75 Ω; bandwidth tens of MHz to GHz; used for broadband cable (DOCSIS) and RF distribution.
- **Optical fiber**: core (8-9 µm SMF, 50-62.5 µm MMF) + cladding; total internal reflection (NA = sin θ_max); attenuation ~0.2 dB/km at 1550 nm (SMF); dispersion limits MMF; WDM/DWDM multiplies capacity (100+ wavelengths × 400G each).
**Unguided media**: radio waves propagate in free space — governed by frequency band (ISM 2.4/5/6 GHz, licensed cellular, mmWave 24-71 GHz), path loss (free-space loss ∝ d²f²), multipath/fading, and antenna gain; communication is inherently broadcast (shared, insecure) and half-duplex unless full-duplex radios (5G) are used.

## 8. Example
**Choosing a link for a data center** — the decision tree:
- ToR switch → server: **twinax/DAC (copper)** up to 5 m (cheap, low power) or **multi-mode fiber + VCSEL** up to 100 m.
- Leaf → spine: **single-mode fiber** (reaches across the building/campus, 100G-400G per lane).
- Building → building or to the WAN: **single-mode fiber**, possibly **DWDM** (128 wavelengths on one fiber = 128× capacity without pulling more glass).
- Office user: **Cat6A copper** (up to 100 m, 10GBASE-T).
- Warehouse/field workers: **WiFi/5G** (unguided).
Numbers: SMF @ 1550 nm: 0.2 dB/km, 80 km reach without regeneration; MMF @ 850 nm: 3.5 dB/km, ~100 m at 40G; Cat6A: 100 m; free-space 2.4 GHz at 100 m: path loss ≈ 20·log₁₀(4π·d/λ) ≈ 80 dB.

## 9. Internal Working
1. **Twisted pair**: differential pair — wire A carries +V(t), wire B carries −V(t); receiver reads (A − B), so noise induced equally on both (common mode) cancels. Twists per meter determine crosstalk rejection (Cat6A has tighter twists for 500 MHz).
2. **Coax**: the shield confines the EM field (no external radiation/interference); signal rides the center conductor vs the shield as return — an inherently balanced-to-earth structure; bandwidth scales with dielectric quality.
3. **Fiber**: light injected by laser (SMF) or VCSEL/LED (MMF); total internal reflection requires the cladding index < core index; attenuation from scattering (Rayleigh, ∝ λ⁻⁴) and absorption (OH⁻); dispersion (modal in MMF, chromatic in SMF) widens pulses → reach limits; coherent receivers (DSP) recover phase for 400G+.
4. **Radio**: antenna converts guided current to a free-space wave; free-space path loss = (4πd/λ)²; fading from multipath (reflections sum destructively); OFDM and MIMO (Section 02/05) fight it; power limits by regulation (EIRP), and spectrum is allocated in bands.
5. **Repeaters/amplifiers**: regenerate the signal where attenuation exceeds the budget (fiber EDFA every ~80-100 km; cellular towers every ~km; WiFi APs every ~30-100 m) — the reason media maps to distances.

## 10. Time Complexity / Performance
- **Channel capacity** is set by the medium (Sections 01-02): Cat6A ≈ 10 Gbps/100 m; MMF ≈ 100 Gbps/100 m; SMF ≈ 400+ Gbps/lambda/80 km (DWDM → 100+ Tbps/fiber).
- **Attenuation**: UTP ~9-20 dB/100 m at 100 MHz; coax ~2-5 dB/100 m; MMF ~3.5 dB/km; SMF ~0.2 dB/km at 1550 nm — the numbers that decide repeater spacing.
- **Propagation velocity**: ~0.6-0.7c in copper, ~0.67c in fiber — the delay math (Section 05).
- **Cost ordering** per meter (typical): UTP < coax < MMF < SMF; plus termination costs (fiber optics/splicing) and power per port.
- "Complexity": media selection is a constraint problem (rate × distance × cost × EMI × mobility), not an algorithmic one.

## 11. Advantages
- **Twisted pair**: cheapest, ubiquitous, easy termination, plenty for 1-10G at short reach, differential noise rejection.
- **Coax**: shielded (EMI-immune), high bandwidth, long reach per cost in cable plant, simple connectors.
- **Fiber**: enormous bandwidth (Tbps), tiny attenuation (80+ km unregenerated), immune to EMI/ground loops/tapping concerns (harder to tap), no crosstalk, light weight, secure-ish.
- **Radio**: mobility, no cabling, broadcast/multicast natural, fast deployment, reach where wires can't go (satellites, IoT in the field).

## 12. Disadvantages
- **Twisted pair**: distance-limited (~100 m), EMI/crosstalk-sensitive, capped bandwidth.
- **Coax**: bulky, hard to run, single-connector per drop, legacy ecosystem.
- **Fiber**: expensive optics/termination, fragile (bend radius), harder to tap into (a feature for security, a problem for diagnostics — need OTDR), single-fiber failure = big outage.
- **Radio**: shared/unlicensed → interference; range limits; security exposure (anyone can listen/jam); power/battery; line-of-sight needs for microwave/mmWave.

## 13. Interview Questions
1. **Q: Compare twisted pair, coax, and fiber for bandwidth, distance, and cost.** A: Twisted pair: 1-10G/100 m, cheapest. Coax: hundreds of MHz-GHz, ~km, mid-cost, shielded. Fiber: 100G-400G+ per lambda, 80+ km (SMF), most expensive to install but highest capacity and EMI-immunity.

2. **Q: Why is twisted pair twisted?** A: To cancel electromagnetic interference and crosstalk: adjacent twists pick up noise in opposite phases, canceling at the receiver; differential signaling (pair carries +V and −V) further rejects common-mode noise.

3. **Q: What's the difference between single-mode and multi-mode fiber?** A: SMF has an ~9 µm core and laser light (one propagation mode) → low dispersion, 80+ km reach. MMF has 50-62.5 µm core and VCSEL/LED → multiple modes → modal dispersion limits to ~100-500 m but cheap optics for short links (racks, buildings).

4. **Q: Why does fiber win over copper at long distances?** A: Attenuation: SMF ~0.2 dB/km vs copper ~9-20 dB/100 m — a factor of ~1000× in reach per loss budget; also no EMI, no ground loops, huge bandwidth, and lighter weight. Repeaters spaced ~80-100 km on fiber vs ~100 m on copper.

5. **Q: What is WDM/DWDM and why is it a big deal?** A: Wavelength Division Multiplexing runs many wavelengths (colors) on one fiber simultaneously; DWDM packs 80-160 channels (C-band) × 400G = tens of Tbps on a single strand — multiplying capacity without pulling more cable (Section 04 covers this too).

6. **Q: What are the main unguided media and their bands?** A: Radio: 3 kHz-300 GHz. Unlicensed ISM: 2.4 GHz, 5 GHz, 6 GHz (WiFi), 900 MHz/2.4 GHz (Bluetooth/Zigbee). Cellular: 600 MHz-71 GHz (5G mmWave). Microwave: 6-42 GHz (point-to-point backhaul). Satellite: C/Ku/Ka bands. Infrared: ~430 THz (LOS only). Each trades range for bandwidth.

7. **Q: TRICKY — A fiber link is suddenly dropping frames but the fiber "looks fine." What physical factors degrade it invisibly?** A: Macrobending/microbending (attenuation spikes), dirty/contaminated connectors (most common), wrong wavelength/transceiver mismatch (SMF vs MMF), damaged patch panel, or modal/ chromatic dispersion at longer spans. Diagnose with an OTDR + optical power meter (light loss budget), and clean connectors.

8. **Q: Why is MMF not used for long haul?** A: Modal dispersion: multiple modes arrive at different times, widening each pulse until adjacent symbols overlap (ISI) — the reach limit is ~100-500 m. SMF's single mode eliminates this; chromatic dispersion remains but is manageable/corrected (DCF, DSP).

9. **Q: PRODUCTION — What is "path loss" and why does it limit radio links?** A: Free-space path loss ∝ (d²·f²): doubling distance or frequency adds ~6 dB of loss. This is why WiFi drops fast with distance, why mmWave (28 GHz) has ~100 m range vs 900 MHz's kilometers, and why antenna gain matters.

10. **Q: What is 10GBASE-T vs DAC vs optical for a data center ToR-to-server link?** A: 10GBASE-T: Cat6A copper, 100 m, but hot (5-6 W/port) and costly DSP. DAC (direct-attach copper/twinax): 1-5 m, cheapest, low power. Optical (SFP+ MMF): up to ~100 m, higher cost but flexible routing. Modern DCs favor DAC + optical, avoiding 10GBASE-T power.

11. **Q: SCENARIO — Two buildings 500 m apart need 100G. What's the best medium?** A: Single-mode fiber — 100G over 500 m is trivial on SMF (MMF can't reach; copper can't reach; radio can't do 100G). Use SFP-DD/QSFP-DD 100G LR optics or DWDM if multiple 100G lambdas are needed.

12. **Q: What is total internal reflection and how does it confine light?** A: Light in the higher-index core hitting the cladding at an angle beyond the critical angle reflects back instead of escaping. This is why the core index > cladding index and why NA (acceptance angle) defines which rays enter — the physics that makes fiber loss so low.

13. **Q: Why is unguided media "insecure" by nature?** A: A radio wave propagates in free space — anyone with an antenna in range can receive it (no physical confinement). Security requires encryption (WPA3, TLS) and directional antennas, whereas fiber's signal stays in the glass (though tapping is possible, it's detectable).

14. **Q: TRICKY — Your fiber link runs 40 km but the vendor says 80 km reach. You see BER climbing. List what eats the budget.** A: Splices/patch panels each add loss (0.1-0.5 dB), dirty connectors (0.5-2 dB), macrobends, the transceiver's TX power/RX sensitivity, and chromatic dispersion at 1550 nm over 40 km. Compute the actual link budget (TX − RX sensitivity − all losses) vs margin; a clean 40 km at "80 km optics" should be fine unless optics are mismatched or the fiber is degraded.

15. **Q: Why do undersea cables use fiber, not copper or radio?** A: 10,000+ km needs <0.2 dB/km attenuation and repeaters every ~60-80 km (EDFAs) — only fiber meets that; copper's attenuation is ~1000× worse; radio can't cross oceans (path loss, curvature). ~99% of intercontinental traffic rides submarine SMF/DWDM.

16. **Q: What is differential signaling and why is it used on twisted pair?** A: Send +V and −V on the pair; the receiver computes (A−B): any noise coupled equally into both conductors (common mode) cancels exactly. This halves susceptibility to EMI — the core reason Ethernet over UTP works at all.

17. **Q: What are the key fiber attenuation mechanisms?** A: Rayleigh scattering (∝ λ⁻⁴ — why 1550 nm beats 850 nm), absorption by OH⁻/impurities (why high-purity glass), and macrobending/microbending. Together they give the ~0.2 dB/km floor that defines long-haul economics.

18. **Q: SCENARIO — A campus can't trench new cable for a 200 m 40G link. Radio, coax, MMF, or SMF?** A: SMF is still best (40G/200 m trivial, and re-termination is one splice); MMF can't do 40G at 200 m reliably; radio can't do 40G. If trenching is impossible but pulling fiber in an existing duct is possible, do that — the medium choice is dominated by rate+reach, and only fiber meets both.

## 14. Follow-Up Questions
1. **Q: Why does 5G mmWave have poor penetration while sub-6 GHz works indoors?** A: Higher frequency = higher path loss and lower penetration through walls (diffraction degrades); mmWave needs LOS and dense small cells. Lower bands (600 MHz-3.5 GHz) diffract/penetrate better — the band-vs-range trade-off in radio.

2. **Q: What is an OTDR and what does it measure?** A: Optical Time Domain Reflectometer — injects pulses and measures backscattered light vs time to map fiber loss, locate breaks/splices/bends precisely (in distance). It's fiber's answer to "where is the fault?"

3. **Q: How do you extend SMF reach beyond 80 km?** A: EDFA/Raman amplifiers (span ~80-100 km between them), and coherent DSP + FEC at the endpoints — modern 400G undersea systems run hundreds of km between regenerators.

4. **Q: What's the difference between UTP and STP?** A: UTP has no shielding (cheap, fine for offices); STP/FTP wraps pairs in foil/braid for EMI-heavy environments (industrial, high-noise), at higher cost and harder termination.

## 15. Coding Example
```python
import math

def free_space_loss(d_m, f_hz):
    return 20 * math.log10(4 * math.pi * d_m * f_hz / 3e8)

def link_budget(tx_dbm, rx_sens_dbm, loss_db, margin_db=3):
    return (tx_dbm - rx_sens_dbm) - loss_db - margin_db

def fiber_atten(fiber_km, db_per_km, splices=0, splice_db=0.05):
    return fiber_km * db_per_km + splices * splice_db

print(f"2.4 GHz @100 m path loss: {free_space_loss(100, 2.4e9):.1f} dB")   # ~80 dB
print(f"28 GHz @100 m path loss: {free_space_loss(100, 28e9):.1f} dB")     # ~101 dB
print(f"40 km SMF loss: {fiber_atten(40, 0.2, splices=8):.1f} dB")          # 8.4 dB
# Link budget: TX +3 dBm, RX sens -25 dBm, fiber 8.4 dB + connector 2 dB
print(f"Link margin: {link_budget(3, -25, 8.4 + 2):.1f} dB")                # 9.6 dB
```
```python
# Media selection helper — the decision matrix as code
def choose_medium(rate_gbps, distance_m, mobile=False, emi_noise=False, budget=1000):
    if mobile: return "radio (wifi/5g)"
    if distance_m > 1000: return "single-mode fiber (DWDM if multi-lambda)"
    if rate_gbps >= 100 and distance_m > 100: return "single-mode fiber"
    if distance_m <= 100 and rate_gbps <= 10 and not emi_noise:
        return "cat6a copper"
    return "multi-mode fiber or smf (per cost/EMI)"

for r, d, mob in [(1, 30, False), (400, 300, False), (0.1, 20, True), (10, 200, True)]:
    print(f"{r}G, {d}m, mobile={mob} -> {choose_medium(r, d, mob)}")
```
```bash
# Physical-layer inspection on Linux (media & signal quality)
ethtool eth0 | grep -E "Speed|Duplex|Link detected"      # negotiated link
sudo ethtool -S eth0 | grep -Ei "crc|symbol|signal"       # media-level errors
# Fiber:
ethtool -m eth0 | head -30                                # SFP/QSFP optical power, wavelength
sudo ethtool --identify eth0 10                           # blink the port to find the cable
# Radio:
iw dev wlan0 link | grep -E "signal|tx bitrate"           # RSSI + negotiated MCS
iw dev wlan0 survey dump | grep -E "noise|busy"           # channel noise floor
```

## 16. Industry Usage
- **Data centers**: DAC (1-5 m), MMF (10-100 m), SMF (spine/fabrics); optics from 10G SFP+ to 400G QSFP-DD/OSFP; NVIDIA/Arista/Cisco fabrics are fiber-core.
- **Cloud WANs**: AWS/Azure/GCP inter-region backbones are SMF/DWDM; undersea cables (SubCom, TE SubCom, Alcatel) ~99% of international traffic.
- **Cable/telecom**: DOCSIS over coax to the home; DSL over UTP; GPON/EPON fiber to the home (PON).
- **Mobile**: 4G/5G RAN — fiber fronthaul/midhaul (CPRI/eCPRI) between base stations and cores; microwave backhaul where fiber is unavailable.
- **Industrial**: shielded copper + fiber for EMI immunity (power plants, factories, oil & gas); PROFINET/EtherCAT over STP.
- **Satellite/IoT**: radio (LEO Starlink, LoRa, NB-IoT) where no wire can reach.

## 17. References
- IEEE Std 802.3-2022 (PHYs: UTP, fiber, DAC) — https://standards.ieee.org/ieee/802.3/10422/
- TIA/EIA-568 (structured cabling, categories) — https://www.tiaonline.org/
- ITU-T G.652/G.657 (single-mode fiber), G.694.1 (DWDM grid) — https://www.itu.int/rec/T-REC-G.652
- Kurose & Ross, *Computer Networking*, 8th ed., §1.3 (Physical Media).
- Tanenbaum & Wetherall, *Computer Networks*, 6th ed., §2.3 (Transmission Media).
- Stallings, *Data and Computer Communications*, Ch. 4 (Transmission Media).

## 18. Cheat Sheet
- Guided: twisted pair (<100 m, cheap, EMI-prone), coax (shielded, GHz, ~km), fiber (SMF 80+ km, MMF ~100-500 m, immune to EMI).
- Twisting + differential signaling cancels common-mode noise.
- SMF ~0.2 dB/km @1550 nm vs MMF ~3.5 dB/km vs UTP ~9-20 dB/100 m.
- WDM/DWDM: 80-160 lambdas × 400G = tens of Tbps on one fiber.
- Unguided: radio (2.4/5/6 GHz ISM, cellular, mmWave), microwave (LOS), IR (LOS only).
- Free-space path loss ∝ (d·f)² → ~6 dB per doubling of d or f.
- Fiber is broadcast-safe-ish, radio is inherently shared/insecure.
- Media selection = rate × distance × cost × EMI × mobility.
- Undersea = SMF + EDFA (60-80 km spans) — 99% of international traffic.
- OTDR maps fiber faults; optical power meters do link budgets.

## 19. Quiz
1. Twisted pair's practical Ethernet reach: a) 500 m b) 100 m c) 2 km d) 10 km → **b**
2. SMF attenuation at 1550 nm ≈: a) 3.5 dB/km b) 0.2 dB/km c) 20 dB/km d) 1 dB/m → **b**
3. MMF's reach limit is caused by: a) noise b) modal dispersion c) attenuation d) EMI → **b**
4. Which is best for 80 km 400G? a) MMF b) SMF c) UTP d) coax → **b**
5. DWDM multiplexes by: a) time b) frequency/wavelength c) code d) voltage → **b**
6. Doubling distance doubles path loss by ~: a) 3 dB b) 6 dB c) 20 dB d) 10 dB → **b**
7. Why is radio "insecure by nature"? a) weak signals b) broadcasts in free space c) no encryption d) low power → **b**
8. 5G mmWave (28 GHz) has: a) longer range b) shorter range c) better penetration d) lower bandwidth → **b**

**Answers**: 1-b, 2-b, 3-b, 4-b, 5-b, 6-b, 7-b, 8-b.

## 20. Flashcards
- **Q: Why are wires twisted?** → **A:** Cancel EMI/crosstalk + differential signaling rejects common-mode noise.
- **Q: SMF vs MMF?** → **A:** SMF: 9 µm core, laser, 80+ km. MMF: 50-62.5 µm, VCSEL, ~100-500 m (modal dispersion).
- **Q: Why is fiber loss so low?** → **A:** Total internal reflection + Rayleigh scattering floor ~0.2 dB/km @1550 nm.
- **Q: What is DWDM?** → **A:** Many wavelengths on one fiber → 80-160 × 400G = Tbps per fiber.
- **Q: What limits radio range?** → **A:** Free-space path loss ∝ (d·f)² — distance and frequency both cost ~6 dB per doubling.
- **Q: Why no copper across oceans?** → **A:** Attenuation ~1000× fiber's; only SMF + EDFA spans 10,000+ km.
- **Q: What's the media-selection trade-off?** → **A:** Rate × distance × cost × EMI × mobility; fiber for bandwidth/distance, copper for cheap short links, radio for mobility.

## 21. Revision
Transmission media are the physical channels: guided (twisted pair — cheap, 100 m, differential+twisting for noise rejection; coax — shielded, GHz; fiber — SMF 0.2 dB/km/80+ km, MMF ~100-500 m, immune to EMI) and unguided (radio — shared, path loss ∝ (d·f)², insecure by nature; microwave LOS; IR). The key numbers: SMF 1550 nm 0.2 dB/km; MMF 3.5 dB/km; UTP ~9-20 dB/100 m; WiFi range ~30-100 m; 5G mmWave ~100 m LOS. DWDM multiplies fiber by 80-160 lambdas. Media selection is a four-way trade: rate × distance × cost × mobility × EMI. Undersea = SMF + EDFA every ~70 km (99% of intercontinental traffic). Anchor: *fiber for speed and distance, copper for cheap short hops, radio for mobility — and the physical path defines the noise that Section 05's bandwidth math assumes.*

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Compare UTP/coax/fiber" | 13-Q1 / 7 |
| "Why twist wires?" | 13-Q2 / 9 |
| "SMF vs MMF and reach limits" | 13-Q3,8 |
| "Why fiber for long haul?" | 13-Q4 |
| "What is WDM/DWDM?" | 13-Q5 |
| "Unguided media / path loss math" | 13-Q6,9 |
| "Choose media for X (scenario)" | 8 / 13-Q11,18 / 15 |
| "Fiber failing invisibly / OTDR" | 13-Q7,14 / 14-Q2 |
| "Why radio is insecure" | 13-Q13 |
| "Why undersea = fiber" | 13-Q15 |
