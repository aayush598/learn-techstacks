# 10.1.1 Single-Event Effects (SEE) — SEU and SET in Implantable Pacemakers

## Chapter Overview

Single-event effects (SEE) represent one of the most insidious reliability threats to implantable pacemaker electronics. Unlike gradual aging mechanisms such as BTI or electromigration, SEEs strike instantaneously — a single particle traversing a sensitive circuit node can flip a bit, trigger a transient pulse, or even cause destructive latch-up. In a life-critical device like the iPACE-CHIP, where a corrupted pacing parameter or a missed sense event can directly endanger the patient, understanding and mitigating single-event effects is not optional — it is fundamental to the device's safety architecture.

This chapter provides a comprehensive treatment of SEEs as they apply to implantable pacemaker ICs. We begin with the underlying physics of particle interactions with silicon, classify the taxonomy of single-event effects, and then focus deeply on the two most operationally significant non-destructive effects: single-event upsets (SEU) and single-event transients (SET). Throughout, we use the iPACE-CHIP as the concrete design context, examining how each effect threatens specific functional blocks — from the analog sensing front-end to the digital pacing controller and telemetry interface.

---

## 10.1.1.1 Physics of Single-Event Interactions

### Particle Sources in the Implantable Environment

When the iPACE-CHIP is implanted inside the human body, it is shielded by several centimeters of tissue. This shielding attenuates many external radiation sources but does not eliminate them. The primary particle sources of concern are:

**Cosmic Ray Secondary Particles:** Primary cosmic rays (mostly protons and alpha particles from solar and galactic sources) interact with the upper atmosphere and with the body's tissue, producing cascades of secondary particles — neutrons, protons, pions, and muons. At sea level, the neutron flux is approximately 12–15 neutrons/cm²/hour across a broad energy spectrum (thermal to GeV). These neutrons are the dominant source of SEEs in terrestrial and near-terrestrial environments, including inside the human body.

**Radioactive Contamination in Implant Materials:** Trace radioactive isotopes (primarily uranium-238, thorium-232, and potassium-40) exist in trace quantities in the hermetic packaging materials, ceramic substrates, and even the titanium can of the pulse generator. While the activity levels are extremely low (typically below regulatory limits), the alpha particles emitted can have energies of 4–8 MeV, and their short range (~20–40 μm in silicon) means they deposit all their energy within a few transistor depths.

**Thermal Neutrons and Boron-10:** If the iPACE-CHIP fabrication process uses borophosphosilicate glass (BPSG) as an interlayer dielectric, thermal neutrons can capture on boron-10 nuclei (10B(n,α)7Li reaction), producing alpha particles and lithium ions with a combined energy of ~2.3 MeV. This reaction has a thermal neutron capture cross-section of 3840 barns — enormously large compared to most nuclear reactions — making BPSG a significant internal alpha source.

**Proton Recoil from Tissue:** High-energy neutrons passing through the body can knock protons out of hydrogen nuclei in tissue. These recoil protons can reach the chip with sufficient energy to cause ionization events.

### Linear Energy Transfer (LET)

The severity of a single-event interaction is characterized by the linear energy transfer (LET) of the incident particle — the amount of energy the particle deposits per unit path length as it traverses the silicon. LET is expressed in units of MeV·cm²/mg, which accounts for the density of the material:

```
LET = (dE/dx) / ρ

where:
  dE/dx = energy loss per unit path length (MeV/cm)
  ρ     = material density (mg/cm³ for silicon, ρ = 2.33 g/cm³ = 2330 mg/cm³)
```

A 1 MeV alpha particle traversing silicon (~4 μm range) deposits roughly 0.27 MeV, giving an LET of approximately 0.27 / (4 × 10⁻⁴ × 2.33) ≈ 290 MeV·cm²/mg at its Bragg peak. However, the average LET over its path is much lower — around 40–80 MeV·cm²/mg.

For the iPACE-CHIP, the critical LET threshold depends on the circuit node sensitivity:

| Circuit Block | Typical Critical Charge (fC) | Effective LET Threshold (MeV·cm²/mg) |
|---|---|---|
| SRAM cell (6T, 180nm) | 2–5 | 1–3 |
| D flip-flop (180nm) | 5–15 | 3–8 |
| Analog comparator (sensing front-end) | 10–30 | 5–15 |
| Clock divider (sequential logic) | 3–8 | 2–5 |
| SRAM cell (6T, 65nm) | 0.3–1 | 0.3–1 |
| D flip-flop (65nm) | 1–3 | 0.5–2 |

As technology scales downward, the critical charge (Qcrit) decreases roughly linearly with node capacitance and supply voltage, making smaller geometries inherently more susceptible to SEEs.

### Charge Collection Mechanisms

When an ionizing particle strikes silicon, it generates electron-hole pairs along its trajectory. The total charge deposited is:

```
Q_deposited = (LET × ρ × L) / (q × E_pair)

where:
  L        = path length through the sensitive volume
  q        = electron charge (1.6 × 10⁻¹⁹ C)
  E_pair   = average energy to create an electron-hole pair in Si (3.6 eV)
```

The charge collection from the generated carriers occurs through two primary mechanisms:

**Drift Collection (Prompt):** Immediately after the particle strike, the electric field in the depletion region of reverse-biased junctions sweeps the carriers to the electrodes. This process is fast (sub-nanosecond) and collects carriers generated within or very close to the depletion region. The collected charge through drift is often called the "funneling" contribution because the electric field lines are distorted into a funnel shape along the ion track.

**Diffusion Collection (Delayed):** Carriers generated outside the depletion region diffuse toward it and are eventually collected. This process is slower (nanoseconds to tens of nanoseconds) and contributes a "tail" to the current pulse. Diffusion collection can be significant for particles that pass through regions distant from the junction.

The total collected charge must exceed the critical charge (Qcrit) of the circuit node for an upset to occur. For the iPACE-CHIP's digital logic, Qcrit depends on the node capacitance and supply voltage:

```
Qcrit = C_node × V_DD + I_feedback × τ_recovery

where:
  C_node        = total capacitance at the sensitive node
  V_DD          = supply voltage
  I_feedback    = feedback current from the cross-coupled latch (for SRAM/FF)
  τ_recovery    = time window during which the feedback can restore state
```

---

## 10.1.1.2 Taxonomy of Single-Event Effects

The SEE taxonomy divides effects into destructive and non-destructive categories:

### Non-Destructive Effects

**Single-Event Upset (SEU):** A bit-flip in a memory element (SRAM cell, flip-flop, latch). The stored logic state changes from 0→1 or 1→0. SEUs are soft errors — they do not damage the circuit, and the correct value can be restored by rewriting the memory. In the iPACE-CHIP, SEUs in the pacing parameter registers, mode control FSM, or telemetry buffer are critical concerns.

**Single-Event Transient (SET):** A temporary voltage glitch combinational logic. When a particle strikes a node in a combinational path, the resulting current pulse propagates through the logic chain and may be latched at a downstream flip-flop, converting the transient into an SEU (this is called an "indirect SEU" or "multiple-bit upset through logical masking"). SETs are particularly dangerous in wide OR/AND gates and in analog circuits where the transient can be amplified.

**Single-Event Functional Interrupt (SEFI):** An upset in control or configuration logic that causes a functional disruption — for example, a state machine getting stuck in an undefined state, or a clock manager losing lock. SEFIs are more complex than simple SEUs because they affect the device's behavior rather than just stored data.

### Destructive Effects

**Single-Event Latch-Up (SEL):** The particle strike triggers a parasitic thyristor (PNPN) structure in CMOS circuits, creating a low-impedance path between VDD and ground. SEL can cause extremely high currents (hundreds of mA to amps) and permanent damage if not quickly interrupted. The iPACE-CHIP must have latch-up detection and power-cycling circuits.

**Single-Event Gate Rupture (SEGR):** The particle strike, combined with the electric field across a gate oxide, causes oxide breakdown. This is a permanent, destructive failure. SEGR is primarily a concern for power MOSFETs and memory cells with thin oxides under high voltage stress.

**Single-Event Burnout (SEB):** In power devices (DMOS transistors, IGBTs), the parasitic bipolar transistor can be triggered, leading to thermal runaway and device destruction. While the iPACE-CHIP's output stage drives relatively low-current loads, the charging output pulse generator must still be evaluated for SEB.

### Multiple-Bit Effects

As technology scales, the physical proximity of memory cells increases the likelihood that a single particle strike affects multiple adjacent bits:

**Multiple-Bit Upset (MBU):** Two or more bits in the same word or adjacent words are upset simultaneously. Traditional Hamming-based SEC-DED codes cannot correct MBUs within the same word. The iPACE-CHIP must use interleaving or more powerful ECC to handle MBUs.

**Multiple-Cell Upset (MCU):** A broader term encompassing upsets in physically adjacent cells across different words or even different functional blocks. At 65nm and below, a single heavy-ion or high-energy neutron can upset 3–7 adjacent SRAM cells.

---

## 10.1.1.3 Single-Event Upsets in the iPACE-CHIP

### Critical Register Vulnerability Analysis

Not all registers in the iPACE-CHIP carry equal criticality. A systematic vulnerability analysis classifies each register by the patient safety impact of an upset:

**Category A — Immediately Life-Threatening:**
- Pacing output amplitude register: an upset could set the output voltage to zero (no capture) or maximum (tissue damage)
- Pacing output pulse width register: an upset could narrow the pulse below the chronaxie or widen it dangerously
- Pacing rate limit registers: an upset could set the lower rate limit to zero (asystole detection disabled) or upper rate limit to dangerously high values
- Sensing threshold register: an upset could desensitize the amplifier (missed EGM events) or oversensitize it (noise oversensing triggers inappropriate inhibition)
- Refractory period registers: an upset could shorten the refractory period, enabling T-wave oversensing

**Category B — Clinically Significant:**
- Mode control state machine: an upset could transition the pacemaker to an inappropriate mode (e.g., VOO during atrial fibrillation)
- Counter/timer values for rate adaptation: an upset could cause inappropriate rate response
- Telemetry command registers: an upset could initiate an unintended parameter change
- Battery monitoring threshold: an upset could mask a genuine low-battery condition

**Category C — Operational Impact:**
- Status and diagnostic registers: an upset could report incorrect status to the telemetry system
- Non-volatile memory write enable: an upset could trigger an unintended parameter save or erase
- Interrupt enable/disable bits: an upset could mask or falsely trigger interrupts

### SEU Rate Estimation for iPACE-CHIP

The SEU rate for a specific memory element depends on the particle flux, the element's effective cross-section (σ_SEU), and the operating conditions:

```
R_SEU = Φ × σ_SEU × K_volt × K_temp × K_duty

where:
  R_SEU    = SEU rate (upsets per device per hour)
  Φ        = particle flux relevant to the energy spectrum (particles/cm²/hr)
  σ_SEU   = SEU cross-section (cm²/bit) — probability of upset per particle per bit
  K_volt   = voltage derating factor (depends on V_DD)
  K_temp   = temperature derating factor (body temperature = 37°C)
  K_duty   = duty cycle factor (not all nodes are sensitive at all times)
```

For a typical 180nm CMOS process at the iPACE-CHIP's operating conditions, representative values are:

```
Φ (neutron)    ≈ 12 neutrons/cm²/hr (sea level)
σ_SEU (SRAM)   ≈ 1 × 10⁻¹⁴ cm²/bit (for 180nm, LET threshold ~3 MeV·cm²/mg)
K_volt (1.8V)  ≈ 1.2 (derated from 2.5V nominal)
K_temp (37°C)  ≈ 0.9 (slightly lower than room temperature sensitivity)
K_duty         ≈ 0.3 (nodes are not continuously sensitive)

R_SEU per bit  = 12 × 1 × 10⁻¹⁴ × 1.2 × 0.9 × 0.3
              ≈ 3.9 × 10⁻¹⁴ upsets/bit/hr
```

For a 4-Kbit parameter register array:
```
R_SEU_total = 3.9 × 10⁻¹⁴ × 4096 ≈ 1.6 × 10⁻¹⁰ upsets/hr
```

This is extremely low for a single bit, but when considering the entire chip (estimated 50,000+ flip-flops and 256 Kbit of SRAM), the aggregate SEU rate becomes:

```
R_SEU_chip ≈ 3.9 × 10⁻¹⁴ × 256000 + contributions from flip-flops
           ≈ 1.0 × 10⁻⁸ + 5.0 × 10⁻⁹
           ≈ 1.5 × 10⁻⁸ upsets/hr
           ≈ 1.3 × 10⁻⁴ upsets/year
           ≈ 1 upset per ~7,700 years
```

While this seems negligible, the cumulative probability over a 10-year device lifetime with millions of deployed devices is significant. Moreover, the critical registers (Category A) must have SEU rates below 10⁻⁹ per hour to meet IEC 60601-1 requirements for single-fault tolerance in life-critical systems.

### SEU in Analog Circuits

The iPACE-CHIP's analog front-end — the sensing amplifier, bandgap reference, and DAC — is also susceptible to single-event effects, though the manifestation differs from digital SEUs:

**Sense Amplifier Upset:** A particle strike on the differential input stage can inject a transient current that temporarily saturates the amplifier. If the transient exceeds the blanking window duration (~50–100 μs for the iPACE-CHIP), the pacemaker may interpret it as a cardiac event (false positive sensing) or miss a genuine cardiac event during the recovery period (false negative sensing).

**Bandgap Reference Perturbation:** A strike on the bandgap reference can momentarily shift the reference voltage, affecting all circuits that depend on it — comparators, DACs, and voltage monitors. The recovery time depends on the bandgap's bandwidth; for a typical low-power bandgap, this can be 1–10 μs.

**DAC Glitch:** A single-event transient in the DAC register or the DAC's current source array can cause a momentary output voltage spike. If this occurs during a pacing pulse, the output amplitude can momentarily exceed the safe limit. The iPACE-CHIP addresses this with an output clamp circuit (discussed in Chapter 12).

---

## 10.1.1.4 Single-Event Transients in the iPACE-CHIP

### SET Propagation in Combinational Logic

A SET occurs when a particle strikes a combinational logic node and generates a voltage transient that propagates through subsequent logic stages. The transient is "captured" if it arrives at a sequential element (flip-flop or latch) during the setup/hold time window of the clock edge. This phenomenon is sometimes called a "race" between the transient pulse width and the clock period.

**Pulse Width vs. Logical Depth:** The initial current pulse from a particle strike is typically 1–10 ps wide. However, as it propagates through logic gates, the pulse broadens due to asymmetric rise/fall times and logical masking. A general rule of thumb is that the SET pulse width increases by approximately 20–50 ps per logic gate of depth. After 10 gates of logic, the pulse can be 200–500 ps wide — easily captured by a flip-flop in a design running at 1–32 MHz (typical for the iPACE-CHIP's low-power clock).

**Logical Masking:** A transient on an AND gate input is masked if the other input is logic 0. Similarly, a transient on an OR gate input is masked if the other input is logic 1. The logical masking probability depends on the circuit topology and signal statistics. For random logic, approximately 50% of transients are logically masked.

**Electrical Masking:** The transient pulse attenuates as it passes through gates due to the limited drive strength and capacitive loading. A very narrow pulse may be completely absorbed before reaching a flip-flop. Electrical masking is more effective at lower process nodes where the intrinsic gate delay is shorter.

**Temporal Masking:** The transient must arrive at the flip-flop during the aperture window (setup + hold time, typically 100–500 ps at 180nm). If the transient arrives outside this window, it is not captured. Temporal masking probability is roughly:

```
P_temporal ≈ (setup_time + hold_time) / clock_period
           ≈ 300 ps / 62.5 ns (at 16 MHz)
           ≈ 0.48%
```

### SET in the iPACE-CHIP Critical Paths

The most SET-sensitive combinational paths in the iPACE-CHIP are:

**Pacing Rate Counter Comparison Logic:** The binary comparator that matches the current timer value against the programmed rate interval. A SET in this comparator could cause an early or late pacing pulse. The comparator output feeds directly into the pacing state machine's clock input.

**Sensing Threshold Comparator:** The analog comparator that compares the amplified EGM signal against the programmed threshold. While the comparator is an analog circuit, its output is a digital signal that can be affected by a SET in the output buffer or the subsequent digital filtering stages.

**Mode Decision Logic:** The combinational logic that determines the next pacing mode based on current sensed events, timers, and programmed parameters. A SET here could cause an inappropriate mode transition.

### SET Mitigation in the iPACE-CHIP

The iPACE-CHIP employs several SET mitigation strategies:

**Temporal Filtering:** All critical combinational outputs are passed through a majority-vote filter (three-stage delay chain with voting). A transient must persist through all three stages to be accepted as valid. This rejects transients narrower than three gate delays.

**Dual-Edge Sampling:** Critical signals are sampled on both rising and falling clock edges. An upset is flagged only if the two samples disagree, and the valid sample is determined by majority voting with a redundant copy.

**Reduced Clock Frequency:** The iPACE-CHIP's core logic operates at 1–4 MHz, which reduces the temporal masking probability but increases the logical depth in clock cycles. The design trade-off is optimized for the specific circuit topologies.

**Analog Filtering:** The sensing front-end includes a bandpass filter (0.5–100 Hz) before the digital threshold comparator, which attenuates high-frequency transients from particle strikes.

---

## 10.1.1.5 SEU Effects on Pacemaker State Machine

### Pacing Mode State Machine Vulnerability

The iPACE-CHIP's pacing controller is implemented as a finite state machine (FSM) with the following critical states:

```
                    ┌──────────┐
        ┌──────────►│  IDLE    │◄──────────┐
        │           │ (Monitor)│           │
        │           └────┬─────┘           │
        │                │                 │
        │   Atrial       │  Ventricular    │
        │   Sensed       │  Sensed         │
        │                ▼                 │
        │           ┌──────────┐           │
        │           │  A sensed│           │
        │           │  wait V  │           │
        │           └────┬─────┘           │
        │                │                 │
        │                │ V-sensed        │ A-sensed
        │                ▼                 │
        │           ┌──────────┐           │
        │           │ AV delay │           │
        │           │  timer   │           │
        │           └────┬─────┘           │
        │                │                 │
        │                │ AV timeout      │
        │                ▼                 │
        │           ┌──────────┐           │
        │           │  Pace V  │───────────┘
        │           └──────────┘
        │
        │ Atrial timeout (LRI)
        ▼
  ┌──────────┐
  │  Pace A  │
  └────┬─────┘
       │
       │ AV delay
       ▼
  ┌──────────┐
  │  Pace V  │
  └──────────┘
```

An SEU in the FSM state register can transition the machine to an undefined state or to a valid state at the wrong time. The consequences include:

**Asynchronous Pacing (VOO/AOO):** If the FSM transitions to a pacing state without sensing, the pacemaker paces at the programmed lower rate regardless of the patient's intrinsic rhythm. This is dangerous if the patient has an underlying rhythm, as competitive pacing can trigger ventricular fibrillation.

**Inhibited Pacing (VVI at inappropriate time):** If the FSM enters a "sensed and waiting" state when no event was actually sensed, the pacemaker may inhibit pacing when the patient needs it, leading to asystole.

**Rapid Pacing:** If the FSM state register gets stuck in a "pacing" state and re-triggers immediately, the output can pace at rates far exceeding the programmed upper rate limit, potentially inducing tachycardia.

### FSM SEU Hardening

The iPACE-CHIP protects the FSM state register using:

1. **Triple Modular Redundancy (TMR)** on the state register with majority voting (see Chapter 10.1.3)
2. **State encoding with Hamming distance ≥ 2** between adjacent states, so a single-bit upset cannot transition between states that are one clock cycle apart in normal operation
3. **Default state assignment:** all undefined states decode to the IDLE (safe) state
4. **Watchdog timeout:** if the FSM does not return to IDLE within a maximum period, a hardware watchdog forces a reset to IDLE

### Pacing Parameter Register Protection

The pacing parameter registers (amplitude, pulse width, rate limits, refractory periods) are protected by:

1. **ECC (SEC-DED):** Each register is protected by a Hamming code that can correct single-bit errors and detect double-bit errors
2. **Redundant storage:** Critical parameters (output amplitude, pulse width) are stored in triplicated registers with continuous majority voting
3. **Periodic read-back verification:** The DSP periodically reads back parameter registers, computes ECC, and corrects any single-bit errors
4. **Voting-based write:** All writes to critical registers go through a triple-redundant write path, and the read-back value must match the intended value before the write is committed

---

## 10.1.1.6 Soft Error Rate (SER) in Modern CMOS

### Technology Scaling and SER Trends

The soft error rate per bit has a complex relationship with technology scaling:

**Reducing Critical Charge:** As supply voltage and node capacitance decrease, the critical charge (Qcrit) decreases, making each bit more sensitive to lower-LET particles. This increases the susceptible cross-section.

**Reducing Cell Area:** Smaller cells have a smaller physical target area for particle strikes, reducing the geometric cross-section.

**Increasing Density:** More bits per unit area means more potential upset sites per particle strike.

The net effect has been a roughly constant or slightly increasing SER per bit across technology generations from 180nm to 7nm. However, the total SER per chip increases because of the dramatic increase in the number of transistors per chip.

### SER at Body Temperature (37°C)

Temperature affects SER through several mechanisms:

**Increased carrier mobility at higher temperature** reduces the collection efficiency slightly, as carriers undergo more scattering before reaching the junction.

**Increased leakage current** raises the noise floor, which can interact with the transient pulse from a particle strike to create additional vulnerability in analog circuits.

**Thermal neutron flux varies with altitude and latitude**, but the body's hydrogen content provides some moderation. Inside the body, the thermal neutron flux is approximately 2–3× higher than the free-space thermal flux due to neutron thermalization in tissue.

The iPACE-CHIP's SER is characterized at 37°C in a tissue-equivalent phantom to capture these effects accurately.

### Alpha Particle SER from Package Materials

The alpha particle SER from trace radioactive contamination in packaging materials is characterized by:

```
R_alpha = A_alpha × σ_alpha × f_geometric × f_angular

where:
  A_alpha     = alpha activity of the package material (Bq/cm²)
  σ_alpha     = alpha SEU cross-section (cm²/alpha)
  f_geometric = geometric factor accounting for distance and angle
  f_angular   = angular distribution factor
```

Typical alpha activities for iPACE-CHIP packaging materials:

| Material | Activity (Bq/cm²) | Dominant Isotope |
|---|---|---|
| Ceramic substrate (Al₂O₃) | 0.001–0.01 | U-238, Th-232 |
| Gold wire bond | <0.001 | — |
| Solder (Sn-Ag) | 0.01–0.05 | U-238 |
| Titanium can | <0.001 | — |
| Epoxy mold compound | 0.005–0.02 | U-238, K-40 |

The iPACE-CHIP specifies low-alpha materials (alpha activity < 0.01 Bq/cm²) for all components within 100 μm of the die surface.

---

## 10.1.1.7 SEE Characterization and Testing

### Heavy Ion Testing

The iPACE-CHIP undergoes heavy ion testing at a cyclotron facility to determine its SEU and SET cross-sections as a function of LET. The test methodology involves:

1. **Device Under Test (DUT):** Production-representative iPACE-CHIP devices with test modes that allow direct access to internal register states and timing measurements.

2. **Ion Beams:** A range of ion species (C, O, Si, Cl, Ti, Fe, Ni, Kr, Xe) at energies selected to achieve LET values from 1 to 100 MeV·cm²/mg.

3. **Test Patterns:** Specific data patterns are loaded into memory arrays and registers, the device is irradiated, and the stored data is read back to count upsets. The test is repeated at multiple fluences (particles/cm²) to build up statistics.

4. **Cross-Section Curve:** The SEU cross-section (upsets per particle per cm²) is plotted vs. LET. The curve typically follows a Weibull distribution:

```
σ_SEU(LET) = σ_sat × [1 - exp(-(LET/LET_th)^s)]

where:
  σ_sat  = saturation cross-section (at very high LET)
  LET_th = threshold LET (below which no upsets occur)
  s      = shape parameter (typically 1.5–3)
```

### Neutron Testing

Neutron SEU testing is performed at a spallation neutron source (e.g., Los Alamos LANSCE, TRIUMF, or the IHEP facility) to simulate the terrestrial neutron environment. The test provides:

1. **High-energy neutron SEU cross-section** (σ_SEU vs. neutron energy)
2. **High-energy neutron SET cross-section** (σ_SET vs. neutron energy)
3. **Boron-10 thermal neutron contribution** (measured separately with and without thermal neutron filtering)

### Proton Testing

Proton testing is important because protons interact with silicon nuclei through nuclear reactions that produce heavy ion recoils. The proton SEU cross-section is:

```
σ_SEU_proton(E) = ∫ σ_SEU_ion(LET) × φ_n(LET, E) d(LET)

where:
  φ_n(LET, E) = neutron-like recoil LET spectrum at proton energy E
```

### Radiation Test Report

The iPACE-CHIP radiation test report includes:

- SEU cross-section curves for all memory types (SRAM, registers, latches)
- SET cross-section curves for combinational logic blocks
- SEL characteristics (LET threshold and cross-section)
- Functional interrupt (SEFI) characterization
- Dose rate effects (latch-up at dose rate)
- Total ionizing dose (TID) characterization
- Recommendations for derating factors in the device's operational environment

---

## 10.1.1.8 Design Implications for iPACE-CHIP

### Minimum SER Requirements

Based on the safety analysis for the iPACE-CHIP (derived from IEC 60601-1 and ISO 14708-3), the following maximum allowable SEU rates apply:

| Functional Block | Max Allowable SEU Rate | Justification |
|---|---|---|
| Pacing output registers | < 10⁻⁹ per hour | Category A — single-fault tolerant |
| Mode control FSM | < 10⁻⁹ per hour | Category A — single-fault tolerant |
| Sensing threshold | < 10⁻⁹ per hour | Category A — single-fault tolerant |
| Rate limit registers | < 10⁻⁸ per hour | Category B — redundant monitoring |
| Telemetry registers | < 10⁻⁷ per hour | Category C — non-life-critical |
| Diagnostic data | < 10⁻⁶ per hour | Category C — logged and reported |

### Mitigation Architecture Summary

The iPACE-CHIP's SEE mitigation architecture is layered:

1. **Process level:** Triple-well isolation, resistive SOI substrates (under evaluation for future nodes)
2. **Circuit level:** Guard rings for latch-up prevention, temporal filtering, current-mode logic for critical paths
3. **Logic level:** TMR on critical registers, ECC on parameter storage, Hamming-distance encoding on FSM states
4. **System level:** Watchdog timers, periodic self-test, heartbeat monitoring, out-of-range detection
5. **Software level:** Periodic register read-back and ECC check, parameter voting, safe-state recovery

Each layer provides defense-in-depth. No single mitigation is sufficient; the combination ensures that the probability of a single SEE causing a patient safety event is below 10⁻⁹ per hour, meeting the single-fault tolerance requirement for life-critical implantable devices.

---

## 10.1.1.9 Chapter Summary

Single-event effects — particularly SEUs and SETs — are an ever-present threat to the iPACE-CHIP's reliability. The physics of particle interaction with silicon creates a stochastic error source that cannot be eliminated, only mitigated through careful design.

Key takeaways:

- **SEUs** flip stored data in memory elements; **SETs** create transient glitches in combinational logic that can be captured as SEUs
- The iPACE-CHIP's environment includes cosmic ray secondaries, thermal neutrons, and alpha particles from packaging materials
- Technology scaling reduces critical charge but also reduces cell size; the net SER per bit is roughly constant
- **Category A registers** (pacing parameters, mode control, sensing threshold) require SEU rates below 10⁻⁹ per hour
- **Layered mitigation** — from process through system level — is required to achieve the necessary soft error resilience
- Comprehensive characterization through heavy-ion, neutron, and proton testing validates the mitigation effectiveness

In the next chapter (10.1.2), we examine the specific radiation hardening by design (RHBD) techniques that the iPACE-CHIP employs to achieve these reliability targets.

---

## References

1. Dodd, P.E., and Massengill, L.W., "Basic Mechanisms and Modeling of Single-Event Upset in Digital CMOS," *IEEE Transactions on Nuclear Science*, Vol. 50, No. 3, 2003.
2. Baumann, R.C., "Soft Errors in Advanced Semiconductor Devices — Part I: The Three Radiation Sources," *IEEE Transactions on Device and Materials Reliability*, Vol. 1, No. 1, 2001.
3. IEC 60601-1:2005, "Medical Electrical Equipment — Part 1: General Requirements for Basic Safety and Essential Performance."
4. IEC 62132-4:2006, "Integrated Circuits — Measurement of Electromagnetic Immunity — Part 4: Transient Magnetic Field Direct Power Injection."
5. ISO 14708-3:2017, "Implants for Surgery — Active Implantable Medical Devices — Part 3: Implantable Neurostimulators."
6. Black, P.J., et al., "A 130nm Generation Serdes Macro for High-Reliability Applications," *IEEE Nuclear and Space Radiation Effects Conference (NSREC)*, 2006.
7. Gadlage, M.J., et al., "Single-Event Transient Measurements in CMOS and BiCMOS Circuits at X-ray and Heavy-Ion Facilities," *IEEE Transactions on Nuclear Science*, Vol. 57, No. 6, 2010.
8. Warren, K.M., et al., "Predicting Single-Event Effects in Combinational Circuits," *IEEE Aerospace Conference*, 2007.
