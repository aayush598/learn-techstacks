# 10.1.2 Radiation Hardening by Design (RHBD) for Implantable Pacemakers

## Chapter Overview

Radiation Hardening by Design (RHBD) is the practice of incorporating radiation tolerance directly into the circuit and layout design, without requiring specialized fabrication processes or additional masking steps. For the iPACE-CHIP, RHBD techniques are essential because the device must operate reliably for 10+ years inside the human body, where it is continuously exposed to cosmic-ray secondary particles, thermal neutrons, and alpha particles from packaging materials. Unlike military or space-grade rad-hard processes (which add significant cost, limit transistor density, and are generally unavailable in advanced CMOS nodes), RHBD allows the iPACE-CHIP to be manufactured on a standard commercial CMOS process while achieving the necessary radiation tolerance through clever design.

This chapter systematically covers the RHBD techniques employed in the iPACE-CHIP, from basic triple modular redundancy to advanced temporal and spatial mitigation strategies. Each technique is presented with its principles of operation, implementation details specific to the iPACE-CHIP architecture, area/power overhead analysis, and effectiveness against the SEE threats identified in Chapter 10.1.1.

---

## 10.1.2.1 Foundations of RHBD

### Why RHBD Instead of Rad-Hard Processes

The iPACE-CHIP design team evaluated three approaches to radiation tolerance:

**Rad-Hard Process (e.g., Silicon-on-Insulator):** SOI processes dramatically reduce charge collection volume, virtually eliminating latch-up and reducing SEU cross-section by 10–100×. However, SOI wafers cost 5–10× more than bulk CMOS, the available process nodes are limited (typically 180nm or 130nm), and the design ecosystem (PDK, IP libraries, EDA tools) is less mature. For a high-volume implantable medical device, the cost penalty is prohibitive.

**System-Level ECC Only:** Using error-correcting codes on memory and simple redundancy on critical registers is the minimum approach. However, ECC alone cannot protect combinational logic from SETs, cannot prevent latch-up, and provides no protection against multi-bit upsets within a single ECC word. This approach is insufficient for Category A safety functions.

**RHBD on Commercial CMOS:** By combining circuit-level redundancy (TMR), layout-level mitigation (spacing, guard rings), temporal filtering, and architectural techniques (ECC, watchdog timers), the iPACE-CHIP achieves radiation tolerance comparable to rad-hard processes at a fraction of the area and power overhead. The additional design complexity and verification effort are justified by the superior cost and performance of the commercial process.

The iPACE-CHIP design team selected the RHBD approach, targeting a commercial 180nm CMOS process with 1.8V core and 3.3V I/O supply voltages.

### RHBD Hierarchy

RHBD techniques are organized into a hierarchy corresponding to different abstraction levels:

```
┌─────────────────────────────────────────┐
│         SYSTEM-LEVEL RHBD               │
│  • Watchdog timers                      │
│  • Heartbeat monitoring                 │
│  • Safe-state recovery                  │
│  • Redundant communication paths        │
├─────────────────────────────────────────┤
│         ARCHITECTURAL RHBD              │
│  • TMR with majority voting             │
│  • ECC (SEC-DED, ChipKill)             │
│  • Temporal redundancy                  │
│  • Scrubbing (periodic refresh)        │
├─────────────────────────────────────────┤
│         CIRCUIT-LEVEL RHBD              │
│  • Temporal filtering                   │
│  • Dual-interlocked storage cells      │
│  • Current-mode logic (CML)            │
│  • Guard rings for SEL prevention      │
├─────────────────────────────────────────┤
│         LAYOUT-LEVEL RHBD               │
│  • Increased node spacing              │
│  • Enclosed layout transistors (ELT)   │
│  • Guard ring placement                │
│  • Shielding from substrate noise      │
├─────────────────────────────────────────┤
│         PROCESS-LEVEL RHBD              │
│  • Triple-well isolation               │
│  • Substrate doping optimization       │
│  • Dielectric choices                  │
└─────────────────────────────────────────┘
```

Each level provides complementary protection, and the overall radiation tolerance is the product of all levels' contributions.

---

## 10.1.2.2 Triple Modular Redundancy (TMR)

### Basic TMR Architecture

TMR is the most widely used RHBD technique for digital logic. The principle is simple: replicate the logic function three times and use a majority voter to select the correct output:

```
                    ┌──────────┐
              ┌────►│  Logic   │────┐
              │     │ Module 1 │    │
              │     └──────────┘    │
              │                     ▼
 Input ───────┼────►┌──────────┐  ┌───────┐
              │     │  Logic   │──│Majority│──► Output
              │     │ Module 2 │  │ Voter  │
              │     └──────────┘  └───────┘
              │                     ▲
              │     ┌──────────┐    │
              └────►│  Logic   │────┘
                    │ Module 3 │
                    └──────────┘
```

If any one module produces an incorrect output (due to SEU or SET), the majority voter selects the correct value from the other two modules. TMR tolerates a single error in any one module.

### TMR on the iPACE-CHIP

The iPACE-CHIP implements TMR at two granularity levels:

**Register-Level TMR (Fine-Grained):** Individual flip-flops that store critical values are triplicated with independent voters:

```
                        ┌─────┐
                   ┌───►│ FF1 │──┐
                   │    └─────┘  │
 Input ──►D ──┬───┼───►┌─────┐  ├──► VOT ──► Q_out
              │   │    │ FF2 │──┤
              │   │    └─────┘  │
              │   │    ┌─────┐  │
              │   └───►│ FF3 │──┘
                   │    └─────┘
                   └──► VOT ──► Q_feedback (to D input)
```

This is the approach used for the iPACE-CHIP's Category A registers: pacing output amplitude, pulse width, mode control state, and sensing threshold. The area overhead is approximately 3× for the flip-flops plus the voter logic (~15% additional for the voters themselves). Since these registers constitute a small fraction of the total die area (~0.5%), the overall area overhead of register-level TMR is approximately 1.5–2% of the die.

**Block-Level TMR (Coarse-Grained):** Entire functional modules are triplicated. The iPACE-CHIP uses block-level TMR for:

- The pacing rate counter (three independent counters with majority-voted comparison)
- The sensing signal processing chain (three independent digital filter pipelines)
- The telemetry encoder (three independent CRC generators)

Block-level TMR is more area-efficient than fine-grained TMR because the voter overhead is amortized over many logic operations. However, it requires that the inputs to each replica be independent (no shared combinational logic before the triplication point), and the outputs must be synchronized before voting.

### TMR Voter Design

The majority voter is the critical element in TMR — it must be itself radiation-hardened. The iPACE-CHIP uses two voter designs:

**Static Voter (for combinational outputs):** A simple majority gate implemented as:

```
Voter_out = (A AND B) OR (B AND C) OR (A AND C)
```

This gate is inherently SEU-resistant for single-bit voters because a single-bit upset in the voter itself would need to affect two of the three AND gates simultaneously — an extremely unlikely event.

**Clocked Voter (for sequential outputs):** Each replica module drives its own flip-flop, and the three registered outputs are voted:

```
Voted_out = (Q1 AND Q2) OR (Q2 AND Q3) OR (Q1 AND Q3)
```

This design has the advantage of breaking the combinational path through the voter, improving timing closure. However, it introduces an additional clock cycle of latency, which must be accounted for in the timing budget.

### TMR with Feedback

For state elements (FSMs, counters), the voted output must be fed back to the inputs of all three replicas to prevent error accumulation. Without feedback, an upset in one replica could eventually propagate to two replicas through normal state transitions, defeating the TMR protection.

The iPACE-CHIP's TMR feedback architecture for the mode control FSM:

```
                    ┌─────────────────┐
              ┌────►│  FSM Replica 1  │────┐
              │     │  (State: S1)    │    │
              │     └─────────────────┘    │
              │                            ▼
 State ───────┼────►┌─────────────────┐  ┌────────┐
              │     │  FSM Replica 2  │──│ Voter  │──► Next State
              │     │  (State: S2)    │  └───┬────┘
              │     └─────────────────┘      │
              │                         ┌────┴────┐
              │     ┌─────────────────┐  │ Feedback│
              └────►│  FSM Replica 3  │──┘  Logic  │
                    │  (State: S3)    │  └─────────┘
                    └─────────────────┘
```

The feedback logic computes the next state from the voted current state and distributes it identically to all three replicas. This ensures that all replicas remain in the same state (except during a transient upset in one replica, which is corrected by the voter).

### TMR Overhead Analysis

| Parameter | Value |
|---|---|
| TMR area overhead (register-level) | ~2% of die area |
| TMR area overhead (block-level) | ~8% of die area |
| Total TMR area overhead | ~10% of die area |
| TMR power overhead | ~12% (due to triplicated switching and voters) |
| TMR timing impact | 1 additional gate delay per voter |
| SEU mitigation effectiveness | >99.9% of single-bit SEUs corrected |
| SET mitigation effectiveness | >95% of single-node SETs masked (depends on pulse width) |

---

## 10.1.2.3 Temporal Redundancy Techniques

### Temporal Voting

Temporal redundancy samples the same signal multiple times at different clock edges and votes on the result. This is effective against SETs (which are transient) and can complement spatial TMR:

```
                  ┌────────┐
Input ──►────────►│   FF   │──► Q_rise (sampled on rising edge)
                  └────────┘
                          │
                  ┌────────┐
Input ──►────────►│   FF   │──► Q_fall (sampled on falling edge)
                  └────────┘
                          │
                  ┌────────┐
                  │  Voter  │──► Q_out = majority(Q_rise, Q_fall, Q_prev)
                  └────────┘
```

The iPACE-CHIP uses temporal voting on the sensing front-end's digital output, where an SET could cause a false sense event. The signal is sampled on both clock edges, and the two samples must agree for at least two consecutive clock cycles before a sense event is declared. This introduces a maximum detection latency of 1.5 clock periods (at 16 MHz, this is ~94 ns — negligible compared to the cardiac cycle of ~800 ms).

### Delayed Sampling (Triple Sampling)

An extension of temporal voting is triple sampling at staggered time points:

```
Input ──┬──► FF1 (t=0)    ──► Q1
        ├──► FF2 (t=Δ)    ──► Q2
        └──► FF3 (t=2Δ)   ──► Q3

Valid = (Q1==Q2) AND (Q2==Q3)
```

The time offset Δ is chosen to be larger than the maximum expected SET pulse width but smaller than the minimum signal transition time. For the iPACE-CHIP:

- Maximum SET pulse width: ~500 ps (after logical and electrical masking)
- Minimum cardiac signal transition: ~10 ms
- Chosen Δ: 5 ns (10× the SET width, 6 orders of magnitude below the cardiac signal)

This technique is applied to the iPACE-CHIP's pacing output enable signal — the final gate that controls the pacing pulse generator. A false trigger here would deliver an unintended pacing pulse to the patient, so triple sampling provides the highest level of assurance.

### Scrubbing

Scrubbing is the periodic overwriting of memory elements with verified-correct data. It prevents the accumulation of SEUs in redundant memory:

**Periodic Register Scrubbing:** The iPACE-CHIP's DSP periodically (every 100 ms) reads all Category A registers, checks ECC, corrects any single-bit errors, and rewrites the corrected values. The scrub interval is chosen to ensure that the probability of two SEUs occurring in the same register between scrubs (which would defeat the SEC-DED ECC) is acceptably low:

```
P_2SEU = (R_SEU × T_scrub)² / 2

For R_SEU = 10⁻⁹/hr, T_scrub = 100 ms = 2.78 × 10⁻⁵ hr:
P_2SEU = (10⁻⁹ × 2.78 × 10⁻⁵)² / 2 = 3.9 × 10⁻²⁸
```

This is negligible.

**SRAM Scrubbing:** The iPACE-CHIP's data SRAM is scrubbed every 10 ms using a dedicated hardware scrub engine that reads each word, checks ECC, and rewrites corrected data. The scrub engine operates independently of the main DSP, ensuring continuous protection even if the DSP is temporarily busy.

---

## 10.1.2.4 Spatial Separation Techniques

### Increased Node Spacing

The probability that a single particle strike affects two independent nodes decreases exponentially with the distance between them. The iPACE-CHIP's layout rules include:

**Minimum Spacing for TMR Voters:** The three flip-flops constituting a TMR triplet are placed with a minimum center-to-center distance of 10 μm in both X and Y directions. This distance is chosen based on the maximum charge collection radius for 180nm CMOS:

```
R_collection ≈ √(2 × D × μ × τ)

where:
  D  = carrier diffusion coefficient (~30 cm²/s for electrons in Si)
  μ  = carrier mobility
  τ  = carrier lifetime (~1 μs in standard Si)
```

At 180nm, R_collection ≈ 5–15 μm depending on LET. With 10 μm spacing, the probability of a single particle upsetting two TMR replicas is less than 5%.

**Minimum Spacing for ECC Words:** Bits belonging to the same ECC word (e.g., the 7 data bits + 4 check bits of a SEC-DED Hamming code) are separated by at least 8 μm. This reduces the probability of a multi-bit upset within a single ECC word.

### Enclosed Layout Transistors (ELT)

Standard CMOS transistors with flat (rectangular) gate layouts have a parasitic leakage path along the shallow trench isolation (STI) edge. This edge leakage path increases the device's sensitivity to single-event effects because the STI interface creates a charge collection volume.

Enclosed Layout Transistors (ELT) eliminate the STI edge by wrapping the gate in a circular or oval shape:

```
Standard Layout:          ELT Layout:
┌──────────────┐         ┌──────────┐
│   Source     │         │ ┌──────┐ │
├──────────────┤         │ │Source│ │
│    Gate      │         │ │ Gate │ │
│   (STI edge)│         │ │      │ │
├──────────────┤         │ └──────┘ │
│   Drain      │         └──────────┘
└──────────────┘         (gate wraps around source)
```

The iPACE-CHIP uses ELT for:
- All NMOS and PMOS transistors in the analog sensing front-end
- All transistors in the bandgap reference
- All transistors in the output pulse generator's H-bridge
- All ESD protection transistors on I/O pins

ELT transistors have a ~30% larger gate area than equivalent rectangular transistors (due to the wrap-around), which increases gate capacitance and slightly reduces speed. However, the radiation tolerance improvement is substantial: ELT reduces the SEU cross-section by 5–10× for individual transistors and eliminates the edge-related charge collection mechanism entirely.

### Guard Rings

Guard rings are heavily doped regions that surround sensitive circuits, collecting minority carriers generated by particle strikes before they can reach sensitive nodes. The iPACE-CHIP uses three types of guard rings:

**N-Well Guard Rings:** Surround PMOS transistors and p-type substrate regions. Connected to VDD, they collect electrons diffusing through the p-substrate and prevent them from reaching sensitive p-well nodes.

**P+ Guard Rings:** Surround NMOS transistors and n-well regions. Connected to VSS, they collect holes diffusing through the n-well and prevent them from reaching sensitive n-well nodes.

**Trench Guard Rings:** Deep trench isolation (where available in the process) provides physical barriers that block carrier diffusion paths. The iPACE-CHIP evaluates deep-trench guard rings around the analog front-end and the output pulse generator, where latch-up risk is highest.

Guard ring effectiveness depends on spacing and width:

| Guard Ring Type | Minimum Width | Minimum Spacing to Protected Node | SEL Prevention Effectiveness |
|---|---|---|---|
| N-well (on p-sub) | 2 μm | 5 μm | >99% for LET < 40 MeV·cm²/mg |
| P+ (on n-well) | 1.5 μm | 4 μm | >99% for LET < 40 MeV·cm²/mg |
| Deep trench | 1 μm | 3 μm | >99.9% for LET < 100 MeV·cm²/mg |

---

## 10.1.2.5 Circuit-Level SET Mitigation

### Temporal Filtering

The iPACE-CHIP implements hardware temporal filters on all critical combinational outputs:

**RC Filter (Analog Domain):** For the sensing amplifier output, a passive RC filter with τ = 100 ns attenuates transients narrower than ~100 ns. This is appropriate because genuine cardiac signals have time constants of milliseconds.

**Majority Filter (Digital Domain):** For digital signals, a chain of three inverters with majority voting at each stage:

```
Signal ──► INV1 ──┬──► INV2 ──┬──► INV3 ──► Filtered Output
                  │           │
                  ▼           ▼
              (majority vote at each stage)
```

The filter rejects transients narrower than three inverter delays (~300 ps at 180nm). The iPACE-CHIP's standard cell library includes a dedicated "filter_inv" cell optimized for this purpose, with symmetric rise/fall times to avoid pulse-width distortion.

**Programmable Digital Filter:** For signals that may need different filtering characteristics at runtime (e.g., the telemetry data input, which needs to be unfiltered during high-speed data reception), the iPACE-CHIP includes a programmable digital filter:

```
Input ──►┌──────────────────┐──► Output
         │  Configurable    │
         │  Delay + Vote    │
         │                  │
         │  Delay: 1-16 clk│
         │  Vote:  2/3, 3/3│
         └──────────────────┘
```

### Current-Mode Logic (CML)

Standard CMOS (static) logic is highly susceptible to SETs because the voltage swing (0 to VDD) is large, and a transient only needs to cross the logic threshold to cause an upset. Current-mode logic (CML) uses differential signaling with a smaller voltage swing (~200–400 mV), making it inherently more resistant to SETs:

- The smaller voltage swing means a particle-induced current pulse must generate a larger voltage perturbation to cause a logic error.
- CML is inherently differential, so common-mode transients (which affect both differential lines equally) are rejected.
- CML operates at constant current, so the switching noise is lower and more predictable.

The iPACE-CHIP uses CML for:
- The high-speed clock distribution network (reduces SET-induced clock jitter)
- The sense amplifier input stage (improves noise rejection)
- The serial telemetry interface clock recovery (ensures reliable data reception)

The overhead of CML is significant: ~3× power consumption compared to static CMOS for equivalent logic functions, and ~2× area due to the differential signaling and tail current sources. Therefore, CML is used only where the SET sensitivity justifies the cost.

---

## 10.1.2.6 Latch-Up Prevention and Mitigation

### Latch-Up Mechanism Review

Latch-up occurs when a particle strike injects enough charge into the substrate or wells to forward-bias a parasitic PNPN (thyristor) structure formed by the parasitic NPN and PNP transistors inherent in CMOS structures:

```
     VDD
      │
      ▼
    ┌───┐
    │ P+ │ (source of PMOS)
    └─┬─┘
      │
      ▼  PNP transistor (parasitic)
    ┌─┴───┐
    │  N  │ (N-well)
    └─┬───┘
      │
      ▼  Forward-biased junction (triggered by particle)
    ┌─┴───┐
    │  P  │ (P-substrate)
    └─┬───┘
      │
      ▼  NPN transistor (parasitic)
    ┌─┴───┐
    │  N+ │ (source of NMOS)
    └─┬───┘
      │
      ▼
    VSS
```

Once triggered, the latch-up creates a low-impedance path from VDD to VSS that sustains itself through regenerative positive feedback. The current can reach hundreds of mA, which is sufficient to:
1. Heat and destroy the metallization or junction
2. Drain the battery rapidly
3. Cause the supply voltage to drop, resetting digital logic
4. In the worst case, create a permanent short circuit

### iPACE-CHIP Latch-Up Prevention

**Guard Rings (Primary Prevention):** As described in Section 10.1.2.4, guard rings reduce the minority carrier collection efficiency, preventing the parasitic transistors from reaching the forward-bias condition needed to trigger latch-up. The iPACE-CHIP uses guard rings around all CMOS structures with a minimum effectiveness of >99% for LET up to 40 MeV·cm²/mg.

**Substrate Contact Density:** The iPACE-CHIP layout maintains a high density of substrate and well contacts (one contact per 20 μm² of active area) to reduce the substrate resistance. Lower substrate resistance means that the minority carrier current generated by a particle strike is shunted to ground more efficiently, reducing the voltage drop that forward-biases the parasitic transistor.

**Twin-Well / Triple-Well Process:** The iPACE-CHIP uses a triple-well process where the NMOS transistors reside in a deep N-well, providing additional isolation between the P-well (NMOS) and the P-substrate. This isolation reduces the charge collection coupling between the two well types.

### Latch-Up Detection and Recovery

Despite prevention measures, latch-up can still occur at very high LET or in worst-case scenarios. The iPACE-CHIP includes a dedicated latch-up detection circuit:

**Current Monitoring:** A precision current-sense resistor (100 Ω) in series with the VDD supply is monitored by a fast comparator. If the supply current exceeds a threshold (150% of the maximum normal operating current), the comparator triggers a latch-up alarm.

**Power Cycling:** Upon latch-up detection, the iPACE-CHIP executes the following recovery sequence:

```
1. Detect overcurrent (within 1 μs of latch-up onset)
2. Assert power-down signal to all logic blocks (within 100 ns)
3. Wait 10 μs (allows parasitic thyristor to turn off)
4. Re-enable power
5. Verify all registers through ECC check
6. If ECC check passes, resume normal operation
7. If ECC check fails, load backup parameters from redundant storage
8. If backup loading fails, enter safe mode (asynchronous pacing at VOO 60 bpm)
```

The total recovery time from latch-up detection to normal operation is approximately 50 μs — well within the pacemaker's timing margins (the minimum pacing interval is 600 ms).

### Latch-Up Testing

The iPACE-CHIP undergoes latch-up characterization during radiation testing:

**Heavy-Ion Latch-Up Testing:** The device is irradiated at increasing LET values while monitoring supply current. The latch-up cross-section is measured as a function of LET, and the latch-up threshold LET is determined. The iPACE-CHIP specification requires no latch-up at LET < 40 MeV·cm²/mg.

**Latch-Up Hold Current:** The minimum current required to sustain a latch-up is measured by externally limiting the supply current. If the hold current exceeds the maximum possible supply current (limited by the battery's internal resistance and the power management IC's current limit), the latch-up will self-extinguish. The iPACE-CHIP's power management limits the maximum current to 50 mA, and the measured latch-up hold current is >100 mA at 37°C, providing a safety margin.

---

## 10.1.2.7 Memory Hardening

### SRAM SEU Mitigation

The iPACE-CHIP uses several types of SRAM, each requiring different hardening strategies:

**Parameter SRAM (8 Kbit):** Stores all programmable pacemaker parameters. Protected by:
- SEC-DED Hamming ECC on each 32-bit word
- TMR at the register level for the most critical parameters
- Periodic scrubbing (10 ms interval)
- Redundant copy in a separate memory bank

**Data SRAM (16 Kbit):** Used as scratchpad by the DSP. Protected by:
- SEC-DED Hamming ECC on each 32-bit word
- Periodic scrubbing (10 ms interval)
- Parity checking for critical temporary variables

**Instruction SRAM (32 Kbit):** Stores the firmware image. Protected by:
- SEC-DED ECC on each 32-bit word
- CRC-32 verification at power-up and periodic scrub (100 ms interval)
- Redundant copy in flash memory for recovery

### ECC Implementation

The iPACE-CHIP uses a modified Hamming code that provides SEC-DED (Single Error Correction, Double Error Detection):

For a 32-bit data word, the ECC requires 7 check bits (2⁷ = 128 ≥ 32 + 7 + 1):

```
Bit position:  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 ...
Content:       C1 C2 D1 C4 D2 D3 D4 C8 D5 D6 D7 D8 D9 D10 D11 D12 D13 D14 D15 D16 ...
               ↑              ↑                    ↑
           check bits     check bits           check bits
```

The syndrome bits are computed during a read operation:

```
S = C XOR (H × D)

where:
  C = 7-bit check vector
  H = 7×38 generator matrix
  D = 38-bit received word (32 data + 6 check)
```

If S = 0: no error. If S ≠ 0 and the extended syndrome indicates a correctable error (single bit), the erroneous bit is flipped. If S indicates an uncorrectable error (double bit), an ECC error interrupt is raised.

### Multi-Bit Upset (MBU) Mitigation

As discussed in Chapter 10.1.1, multi-bit upsets can affect adjacent bits in the same ECC word. The iPACE-CHIP mitigates MBUs through:

**Bit Interleaving:** Adjacent physical memory cells are assigned to different ECC words. For example, if the physical memory array stores bits in the order:

```
Word 0: bit0, bit1, bit2, bit3, ...
Word 1: bit0, bit1, bit2, bit3, ...
```

After interleaving, the logical arrangement becomes:

```
Word 0: physical_bit0, physical_bit32, physical_bit64, ...
Word 1: physical_bit1, physical_bit33, physical_bit65, ...
```

This ensures that a single particle strike affecting adjacent physical bits will impact different ECC words, each of which can independently correct a single-bit error.

The interleaving factor for the iPACE-CHIP is chosen based on the maximum MBU size:

```
Max MBU size at 180nm: 3 bits (for LET < 40 MeV·cm²/mg)
Interleaving factor: 4 (separate adjacent bits by 4 × word_width)
Result: worst case is 3 bits in the same physical row, spread across 4 ECC words — each word has at most 1 error → all correctable
```

### Non-Volatile Memory Protection

The iPACE-CHIP's flash memory (64 Kbyte) stores the firmware image and permanent parameter backups. Flash memory is inherently more resistant to SEUs than SRAM because the stored charge on the floating gate is much larger than the critical charge of an SRAM cell. However, flash is not immune:

**Flash SEU Sensitivity:** High-energy heavy ions can discharge the floating gate through direct ionization. The threshold LET for flash SEU is typically >100 MeV·cm²/mg for modern flash technology, which is well above the expected environment inside the human body.

**Flash ECC:** The iPACE-CHIP's flash controller includes SEC-DED ECC for each 128-bit flash page, providing an additional safety margin.

**Flash CRC Verification:** The firmware image is protected by a CRC-32 checksum stored in a separate flash page. At every power-up and periodically during operation (every 1 second), the CRC is recomputed and compared against the stored value. A mismatch triggers a firmware reload from the backup copy.

---

## 10.1.2.8 Analog and Mixed-Signal RHBD

### Analog Circuit RHBD Considerations

Analog circuits do not have a direct equivalent of digital TMR or ECC. Instead, RHBD for analog circuits focuses on:

**Reduced Sensitive Volume:** Using ELT transistors and guard rings to minimize the charge collection volume.

**Bandwidth Limiting:** Ensuring that the circuit's bandwidth is low enough that transient pulses are attenuated before they can cause significant output error. The iPACE-CHIP's sensing amplifier has a bandwidth of 0.5–100 Hz (set by the bandpass filter), which naturally attenuates SET pulses (which have effective bandwidth of GHz).

**Differential Topology:** Using fully differential signal paths throughout the analog front-end. A particle strike on one side of a differential pair affects only that side, and the differential output is the difference between the two sides — the common-mode component of the transient is rejected.

**Current-Mode Signal Processing:** In the iPACE-CHIP's DAC and current-sensing circuits, signals are represented as currents rather than voltages. Current-mode circuits are less sensitive to SETs because the transient charge must overcome the bias current, which is typically much larger than the transient charge.

### Bandgap Reference Hardening

The bandgap reference is one of the most critical analog blocks because it provides the reference voltage for all comparators and DACs in the iPACE-CHIP. A transient perturbation of the bandgap output affects every downstream circuit.

The iPACE-CHIP's bandgap reference is hardened by:

1. **Tripling the bandgap core:** Three independent bandgap cores with analog majority voting (three resistive voltage dividers feeding a weighted sum)
2. **Low-pass filtering the output:** A 100 Hz low-pass filter on the bandgap output attenuates transients above 100 Hz
3. **Redundant voltage monitoring:** Two independent comparators monitor the bandgap output against windows; a mismatch triggers a bandgap reset

### Output Pulse Generator Hardening

The output pulse generator delivers the pacing stimulus to the heart. An SET in this circuit could cause:
- Incorrect pulse amplitude (over/under-pacing)
- Incorrect pulse width (over/under-pacing)
- Unintended pulse generation (competitive pacing)
- Absence of a needed pulse (failure to capture)

The iPACE-CHIP's output pulse generator is hardened by:

1. **Analog clamp circuits:** Hardware limiters on the output voltage and current that cannot be overridden by digital logic. These provide absolute maximum output limits regardless of the state of any digital registers.
2. **Triple-redundant output enable:** Three independent enable signals, all of which must be asserted for the output to fire. The probability of all three being simultaneously upset is negligible.
3. **Pulse width monitoring:** A hardware timer measures the actual output pulse width and compares it against the programmed value. If the measured width differs by more than 20%, the pulse is terminated and an alarm is raised.

---

## 10.1.2.9 Clock and Reset Hardening

### Clock Distribution Network

The iPACE-CHIP's clock distribution network is a critical single point of failure for SEEs. An SET on a clock buffer can create a false clock edge, causing all downstream flip-flops to capture incorrect data simultaneously.

**Mitigation Strategies:**

1. **Redundant clock sources:** Two independent crystal oscillators (32.768 kHz) with a majority-voted clock selector. If one oscillator fails or produces spurious edges, the other two continue to provide a valid clock.

2. **Clock buffer guard rings:** All clock buffers are surrounded by guard rings and placed with maximum spacing from other sensitive circuits.

3. **Clock edge filtering:** A hardware filter on the clock input rejects edges narrower than 2 ns. This eliminates SET-induced clock glitches while allowing the normal 16 MHz clock (period = 62.5 ns) to pass unattenuated.

4. **Clock monitoring:** A dedicated watchdog monitors the clock frequency and triggers a reset if the frequency drifts more than 10% from the nominal value.

### Reset and Power-On Reset (POR) Hardening

The reset circuitry must be robust against SEEs because an unintended reset during pacing would interrupt the pacing therapy:

1. **Redundant POR:** Two independent POR circuits with majority voting. Both must agree that the supply is stable before the device exits reset.

2. **Reset filtering:** The reset line is filtered with a 100 μs RC filter and a digital majority filter (three consecutive samples must agree) to reject SET-induced reset glitches.

3. **Brown-out detection:** A dedicated brown-out detector monitors the supply voltage and initiates a controlled shutdown if VDD drops below the minimum operating voltage. This prevents the device from operating in an undefined state during power supply transients.

---

## 10.1.2.10 RHBD Verification and Validation

### Simulation Methodology

RHBD effectiveness is verified through extensive simulation:

**SEU Injection Simulation:** The iPACE-CHIP's gate-level netlist is simulated with single-bit node flips injected at every flip-flop, one at a time. For each injection point, the simulation records:
- Whether the upset propagates to any output
- Whether the TMR voter corrects the upset
- The recovery time
- The impact on pacing output timing

**SET Pulse Simulation:** Voltage transient pulses of varying widths (100 ps to 10 ns) and amplitudes (0.1 VDD to 1.5 VDD) are injected at every combinational node. The simulation determines:
- Whether the transient reaches a flip-flop
- Whether the temporal filter rejects it
- Whether the TMR corrects the resulting SEU

**Monte Carlo Analysis:** Random combinations of simultaneous upsets (multi-bit upsets) are simulated to validate the ECC and interleaving effectiveness. The simulation uses the measured MBU spatial distribution from radiation testing.

### Layout Verification

RHBD layout techniques are verified using:

1. **Design Rule Checking (DRC):** Custom DRC rules verify minimum spacing between TMR voter flip-flops, guard ring widths and placement, and substrate contact density.

2. **Parasitic Extraction:** Detailed parasitic extraction of the TMR voters and critical paths ensures that the timing margins are maintained with the additional routing.

3. **Electrical Rule Checking (ERC):** Verifies that all guard rings are properly connected to the appropriate supply and that no floating guard rings exist.

### Test and Characterization

The RHBD effectiveness is validated through:

1. **Heavy-ion testing:** Full SEE characterization as described in Chapter 10.1.1.7, comparing measured SEU/SET cross-sections against the design targets.

2. **Neutron testing:** High-energy neutron testing to validate the SEU rate in a terrestrial-like environment.

3. **Alpha source testing:** Testing with a calibrated alpha source (e.g., Am-241) to validate the effectiveness of guard rings and ELT transistors against alpha-induced SEUs.

4. **Functional testing under radiation:** The iPACE-CHIP's complete pacing algorithm is exercised during radiation exposure, verifying that no pacing anomaly occurs for particle fluxes up to 10× the expected maximum environment.

---

## 10.1.2.11 Chapter Summary

Radiation Hardening by Design enables the iPACE-CHIP to achieve the necessary SEE tolerance on a standard commercial CMOS process, avoiding the cost and performance penalties of specialized rad-hard fabrication.

Key RHBD techniques employed in the iPACE-CHIP:

| Technique | Target Effect | Area Overhead | Effectiveness |
|---|---|---|---|
| Register-level TMR | SEU in critical registers | ~2% | >99.9% correction |
| Block-level TMR | SEU in functional blocks | ~8% | >99.9% correction |
| SEC-DED ECC | SEU in memory arrays | ~15% (memory) | Corrects single-bit, detects double-bit |
| Temporal filtering | SET in combinational logic | ~3% | Rejects transients < 300 ps |
| ELT transistors | SEU/SEL in analog circuits | ~30% (analog) | 5–10× SEU reduction |
| Guard rings | SEL prevention | ~10% | >99% SEL prevention |
| Spatial separation | Multi-bit upsets | ~5% | <5% probability of correlated upset |
| CML clock distribution | SET-induced clock glitches | ~5% (clock) | >99.9% glitch rejection |
| Periodic scrubbing | SEU accumulation | <1% (power) | Prevents error accumulation |
| Latch-up detection | SEL recovery | <1% | Recovery in 50 μs |

Total RHBD overhead: approximately 25–30% additional area and 15–20% additional power compared to an unprotected design. This is the price of radiation tolerance on a commercial process — a price that is well justified for a life-critical implantable device.

The next chapter (10.1.3) examines Triple Modular Redundancy in greater depth, including advanced TMR variants, voter optimization, and the specific trade-offs for the iPACE-CHIP's architecture.

---

## References

1. Lacoe, R.C., "Improving Integrated Circuit Performance Through the Application of Hardness-by-Design Methodologies," *IEEE Transactions on Nuclear Science*, Vol. 55, No. 4, 2008.
2. Mavis, D.G., and Eaton, P.H., "Soft Error Rate Mitigation Techniques for Modern Microcircuits," *IRPS Proceedings*, 2002.
3. Habchi, C., et al., "A Design Flow for Radiation Hardness by Design," *IEEE Aerospace Conference*, 2005.
4. Kelley, P., et al., "A Hardness-by-Design Methodology for Reliable Operation of Digital ASICs in Radiation Environments," *IEEE NSREC*, 2006.
5. Quinn, H., et al., "Automatic Mitigation of Single-Event Effects in SRAM-Based FPGAs," *IEEE Transactions on Nuclear Science*, Vol. 52, No. 6, 2005.
6. Buchner, S., et al., "A Comparison of SET Pulse-Width Measurement Techniques in Digital Circuits," *IEEE Transactions on Nuclear Science*, Vol. 54, No. 6, 2007.
7. IEC 60601-1:2005, "Medical Electrical Equipment — Part 1: General Requirements for Basic Safety and Essential Performance."
8. MIL-STD-883, "Test Methods and Procedures for Microelectronics," Method 1020, "Ionizing Radiation (Total Dose) Effects."
