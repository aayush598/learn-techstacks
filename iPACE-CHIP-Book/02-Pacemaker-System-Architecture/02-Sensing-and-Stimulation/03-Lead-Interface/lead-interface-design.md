# Lead Interface Design

## 2.2.3 Electrode-Tissue Interface and Lead System

The lead interface connects the pacemaker pulse generator to the intracardiac
electrodes that sense cardiac signals and deliver pacing pulses. This chapter
covers the electrode-tissue interface physics, lead construction, impedance
characteristics, failure modes, and the circuit design of the lead interface
in the pacemaker IC.

---

## 2.7.1 Electrode-Tissue Interface Physics

### Equivalent Circuit Model

The electrode-tissue interface can be modeled as an equivalent electrical
circuit consisting of several impedance components:

```
                    ELECTRODE-TISSUE INTERFACE MODEL

  Pacemaker IC                                Cardiac Tissue
      │                                            │
      │    ┌─────────────────────────────────────┐ │
      │    │                                     │ │
      │    │   R_s      C_dl      R_ct          │ │
      │    │  ┌───┐   ┌───┐   ┌───┐            │ │
      │    ├──┤   ├───┤   ├───┤   ├────────────┤ │
      │    │  └───┘   └───┘   └───┘            │ │
      │    │                                     │ │
      │    │   R_p                               │ │
      │    │  ┌───┐                              │ │
      │    ├──┤   ├──────────────────────────────┤ │
      │    │  └───┘                              │ │
      │    │                                     │ │
      │    └─────────────────────────────────────┘ │
      │                                            │
      │  R_s  = Solution resistance (5-50 Ω)      │
      │  C_dl = Double-layer capacitance           │
      │       (10-100 µF/cm²)                      │
      │  R_ct = Charge-transfer resistance         │
      │       (10-100 kΩ·cm²)                      │
      │  R_p  = Polarization resistance            │
      │       (100 kΩ-1 MΩ)                        │
      │                                            │
```

### Component Descriptions

**Solution Resistance (R_s):**
- Resistance of the body fluid (blood, myocardium) between the electrode
  and the tissue
- Typical value: 5-50 Ω
- Depends on: electrode size, tissue proximity, fluid conductivity
- Frequency-independent (resistive)

**Double-Layer Capacitance (C_dl):**
- Capacitance formed by the charge separation at the electrode-tissue
  interface (Helmholtz double layer)
- Typical value: 10-100 µF/cm² (high surface area electrodes)
- For a 1 mm² tip electrode: C_dl ≈ 10-100 nF
- Frequency-dependent (capacitive)
- Dominates the interface impedance at low frequencies

**Charge-Transfer Resistance (R_ct):**
- Resistance to faradaic (electrochemical) charge transfer at the interface
- Typical value: 10-100 kΩ·cm²
- Depends on: electrode material, tissue type, polarization state
- Modelled in parallel with C_dl

**Polarization Resistance (R_p):**
- Resistance representing the slow polarization processes at the interface
- Typical value: 100 kΩ-1 MΩ
- Dominates the interface impedance at very low frequencies (DC)
- Increases with time after pacing (polarization buildup)

### Interface Impedance vs. Frequency

```
  Impedance
  (log scale)
    │
  10k├──────╲
    │        ╲
   1k├────────╲──────────────────────
    │          ╲
  100├──────────╲──────────────────────
    │            ╲
   10├────────────╲────────────────────
    │              ╲
    1├──────────────╲──────────────────
    │
  0.1├─────────────────────────────────
    │
  0.01├─────────────────────────────────
    │
    1    10    100   1k   10k  100k  1M
              Frequency (Hz)

  At DC:      Z ≈ R_p + R_ct (100 kΩ - 1 MΩ)
  At 1 kHz:   Z ≈ R_s (10-50 Ω)  ← Pacing impedance
  At 100 kHz: Z ≈ R_s (10-50 Ω)
```

---

## 2.7.2 Lead Construction

### Lead Components

| Component | Material | Function | Typical Dimensions |
|-----------|----------|----------|-------------------|
| Tip electrode | Pt/Ir (90/10) | Pacing/sensing | 0.5-1.5 mm² surface |
| Ring electrode | Pt/Ir or MP3N | Bipolar return | 5-10 mm² surface |
| Coil conductor | MP35N (Co-Cr-Ni-Mo) | Signal conduction | 0.2-0.5 mm diameter |
| Outer conductor | MP35N | Shield/return | 0.3-0.6 mm diameter |
| Insulation | Silicone or polyurethane | Electrical isolation | 0.1-0.3 mm wall |
| Connector pin | Pt/Ir or stainless steel | IC connection | 1-2 mm diameter |
| Steroid elutor | Dexamethasone sodium phosphate | Reduce inflammation | 1 mg equivalent |

### Lead Types

| Type | Conductors | Electrodes | Use Case |
|------|-----------|-----------|----------|
| Unipolar | 1 | Tip only | Rare (legacy) |
| Bipolar | 2 | Tip + Ring | Most common |
| Quadripolar | 4 | Tip + 3 Rings | CRT (LV pacing) |
| Steroid-eluting | 2+ | Tip with steroid | Reduce chronic threshold |
| Active-fixation | 2 | Screw-in helix | Secure placement |
| Passive-fixation | 2 | Tines/fins | Secure placement |

### Tip Electrode Design

The tip electrode is the most critical component for stimulation and sensing:

**Surface area:**
- Small (0.5-1.0 mm²): Lower pacing threshold, better sensing, higher impedance
- Large (1.5-3.0 mm²): Lower impedance, more stable, higher threshold
- Optimal: 0.8-1.2 mm² for ventricular, 0.5-1.0 mm² for atrial

**Material properties:**
- Platinum/Iridium (90/10): Most common, excellent biocompatibility
- Titanium Nitride (TiN): High surface area, low polarization
- IrOx (Iridium Oxide): Very high surface area, lowest polarization
- Porous platinum: High surface area, good long-term stability

**Surface treatment:**
- Smooth: Low surface area, higher polarization
- Porous: High surface area, lower polarization
- Platinized: Very high surface area, lowest polarization
- Roughened: Moderate surface area, moderate polarization

---

## 2.7.3 Lead Impedance Characteristics

### Acute vs. Chronic Impedance

| Parameter | Acute (Implant) | Chronic (6 months+) | Unit |
|-----------|----------------|-------------------|------|
| Tip impedance (bipolar) | 300-600 | 400-1000 | Ω |
| Ring impedance (bipolar) | 20-50 | 20-50 | Ω |
| Pacing impedance | 300-600 | 400-1000 | Ω |
| Sensing impedance | 500-1500 | 800-2000 | Ω |

### Impedance Changes Over Time

```
  Impedance
  (Ω)
    │
  1200├──────────────────────────────────
    │                              ╱
  1000├────────────────────────────╱──────
    │                          ╱
   800├──────────────────────╱─────────────
    │                    ╱
   600├────────────────╱───────────────────
    │              ╱
   400├──────────╱─────────────────────────
    │        ╱
   200├────╱───────────────────────────────
    │
     0├────┬────┬────┬────┬────┬────┬────
    0   1wk  1mo  3mo  6mo  1yr  2yr  5yr

  Acute phase (0-3 months): Impedance rises as
  fibrotic capsule forms around the electrode
  Chronic phase (3+ months): Impedance stabilizes
```

### Factors Affecting Impedance

1. **Electrode size**: Smaller electrodes → higher impedance
2. **Electrode material**: TiN/IrOx → lower polarization impedance
3. **Tissue proximity**: Closer contact → lower impedance
4. **Fibrotic capsule**: Increases impedance over time (3-6 months)
5. **Steroid elution**: Reduces fibrosis, limits impedance rise
6. **Lead position**: Endocardial vs. epicardial affects impedance
7. **Blood flow**: Convective effects reduce concentration polarization

---

## 2.7.4 Lead Failure Modes

### Failure Mode Classification

| Failure Mode | Probability | Severity | Detection | Mitigation |
|-------------|------------|----------|-----------|------------|
| Conductor fracture | 1-5% at 10 yr | High | Impedance spike | Redundant conductors |
| Insulation breach | 2-5% at 10 yr | Medium | Impedance drop | Dual insulation |
| Connector failure | 1-2% at 10 yr | High | Impedance spike | Redundant connections |
| Electrode dislodgement | 2-5% at 1 yr | High | Impedance change | Active fixation |
| Threshold rise | 5-10% at 10 yr | Medium | Capture threshold | Steroid elution |
| Lead migration | 1-3% at 5 yr | Medium | Impedance/ECG | Active fixation |
| Twiddler's syndrome | < 1% | High | X-ray, impedance | Surgical revision |

### Conductor Fracture

Conductor fracture is the most common lead failure mode, occurring due to:
- Mechanical stress from cardiac motion (100,000+ flex cycles/day)
- Manufacturing defects in the conductor coil
- Stress corrosion at the connector pin
- Compression between the clavicle and first rib (subclavian crush)

**Detection:**
- Sudden impedance spike (> 2× baseline)
- Loss of capture or sensing
- Pacing artifact present but no cardiac response

**Circuit response:**
- Impedance monitoring circuit detects out-of-range impedance
- Alert transmitted via telemetry
- Automatic mode switch to backup (unipolar if bipolar fails)

### Insulation Breach

Insulation breach allows current leakage between conductors or to body
fluid, causing:
- Reduced pacing efficiency (current shunted through breach)
- Increased risk of inappropriate sensing (noise pickup)
- Potential for tissue damage (leakage current)

**Detection:**
- Sudden impedance drop (< 50% of baseline)
- Increased noise on sensing channel
- Erratic sensing or oversensing

### Connector Failure

Connector failure at the lead-header interface causes:
- Intermittent contact (noisy signals)
- Complete disconnection (no pacing/sensing)
- Increased impedance at the connection point

**Detection:**
- Intermittent impedance spikes
- Motion-dependent sensing artifacts
- Pacing threshold changes with body position

---

## 2.7.5 Lead Impedance Measurement

### Measurement Techniques

**Technique 1: Voltage-Current Method**

Apply a known current pulse and measure the resulting voltage:

```
  V_measured = I_applied × R_lead

  I_applied = 10-100 µA (constant current source)
  V_measured = ADC measurement
  R_lead = V_measured / I_applied

  Measurement accuracy: ±5%
  Measurement time: 10-100 µs
  Power consumption: < 1 µJ per measurement
```

**Technique 2: Voltage Divider Method**

Use the known output capacitor and measure the discharge rate:

```
  V(t) = V₀ × e^(-t/(R×C))

  Measure V(t) at two time points
  Calculate R = (t₂ - t₁) / (C × ln(V₁/V₂))

  Accuracy: ±10%
  Simpler circuit, no current source needed
```

### Impedance Monitoring Circuit

```
                    IMPEDANCE MEASUREMENT CIRCUIT

  From Tip ────────────┬────────────────────────────
                       │                            │
                       ▼                            ▼
                  ┌────────┐                  ┌────────┐
                  │  ADC   │                  │  ADC   │
                  │ (V_meas)│                  │ (I_meas)│
                  └───┬────┘                  └───┬────┘
                      │                           │
                      ▼                           ▼
                  ┌────────────────────────────────┐
                  │         DIGITAL PROCESSOR       │
                  │                                 │
                  │   R = V_meas / I_meas           │
                  │                                 │
                  │   If (R < R_min) → Alert        │
                  │   If (R > R_max) → Alert        │
                  │   Store R in diagnostic log     │
                  └────────────────────────────────┘

  I_applied = 10-100 µA (from constant current source)
  Measurement interval: 8-24 hours (programmable)
```

### Impedance Limits

| Parameter | Minimum | Nominal | Maximum | Unit |
|-----------|---------|---------|---------|------|
| Low impedance threshold | 100 | 300 | 500 | Ω |
| High impedance threshold | 1000 | 1500 | 2000 | Ω |
| Impedance spike threshold | — | 2× baseline | — | Ω |
| Measurement accuracy | — | ±5 | — | % |
| Measurement interval | 1 | 8 | 24 | hours |

---

## 2.7.6 Lead Polarization

### Polarization Mechanism

When a pacing pulse is delivered through the electrode, charge accumulates
at the electrode-tissue interface, creating a polarization voltage that
opposes the pacing pulse. This polarization voltage:

1. Reduces the effective voltage across the tissue
2. Increases the energy required for stimulation
3. Creates a large artifact that can mask the evoked response
4. Takes seconds to minutes to dissipate naturally

### Polarization Voltage

```
  V_polarization(t) = V_max × (1 - e^(-t/τ_pol))

  where:
    V_max = maximum polarization voltage (typically 0.5-2.0 V)
    τ_pol = polarization time constant (typically 0.5-2.0 s)
    t = time after pacing pulse
```

### Polarization Reduction Techniques

1. **Small electrode area**: Reduces C_dl, which reduces polarization
   (but increases impedance).

2. **High surface area materials**: TiN, IrOx, and platinized surfaces
   increase the effective surface area, reducing polarization.

3. **Steroid elution**: Dexamethasone reduces fibrosis, which reduces
   the polarization resistance.

4. **Charge balancing**: Active charge removal after the pacing pulse
   reduces residual polarization.

5. **Biphasic pulses**: The second phase actively removes the charge
   deposited by the first phase.

### Polarization Measurement

The polarization voltage can be measured immediately after the pacing pulse
to verify charge balance:

```
  V_pol = V_electrode(t=0+) - V_baseline

  If (V_pol > V_pol_max) → Charge balance error
  If (V_pol < -V_pol_max) → Charge balance error

  V_pol_max = 50-100 mV (programmable)
```

---

## 2.7.7 Lead Interface Circuit in Pacemaker IC

### Input Protection

The lead interface includes protection circuits to prevent damage from
high-voltage events:

```
                    LEAD INTERFACE PROTECTION

  From Tip ────────┬────────────────────────────
                   │
                   ▼
              ┌────────┐
              │  ESD   │
              │  Clamp │ (Diode to VDD/VSS)
              │  (±4kV │
              │   HBM) │
              └───┬────┘
                  │
                  ▼
              ┌────────┐
              │ Series │
              │ Resistor│ (50-200 kΩ)
              │        │
              └───┬────┘
                  │
                  ▼
              ┌────────┐
              │ Input  │
              │ Protection│ (Active clamp)
              │ Switch  │ (Bypasses R_s during
              │        │  pacing)
              └───┬────┘
                  │
                  ▼
              ┌────────┐
              │ SENSE  │
              │ AMP    │
              │ INPUT  │
              └────────┘
```

### Switching Network

The lead interface includes a switching network that routes the lead
connection to the appropriate circuit block:

```
                    LEAD SWITCHING NETWORK

  From Tip ────────┬────────────────────────────
                   │
            ┌──────┴──────┐
            │             │
            ▼             ▼
      ┌──────────┐  ┌──────────┐
      │  SENSE   │  │  PACE    │
      │  PATH    │  │  PATH    │
      │          │  │          │
      └────┬─────┘  └────┬─────┘
           │             │
           ▼             ▼
      ┌──────────┐  ┌──────────┐
      │  AFE     │  │  OUTPUT  │
      │  INPUT   │  │  STAGE   │
      │          │  │          │
      └──────────┘  └──────────┘

  S1 = Sense/Pace switch (break-before-make)
  Break time: 10-50 µs (prevents simultaneous
  connection of sense amp and output stage)
```

### Break-Before-Make Switching

The break-before-make switching ensures that the sensitive sense amplifier
is never connected to the high-voltage pacing output:

```
  Timing Diagram:
  
  Pace Command
  │
  ▼
  ┌───────────────────────────────────────
  │   │← Break →│← Pace →│← Make →│
  │   │   10µs   │  0.4ms │  10µs  │
  │   │          │        │        │
  │   │ S1 opens │ S2 closes│ S1 closes│
  │   │ (sense   │ (pace   │ (sense │
  │   │  path    │  path   │  path  │
  │   │  open)   │  active)│  restored)│
  └───────────────────────────────────────
```

---

## 2.7.8 Steroid-Eluting Leads

### Mechanism

Steroid-eluting leads contain a small reservoir of dexamethasone sodium
phosphate (typically 1 mg) at the tip electrode. The steroid slowly elutes
into the surrounding tissue, reducing the inflammatory response and
fibrotic capsule formation.

### Benefits

| Parameter | Non-Steroid Lead | Steroid-Eluting Lead | Unit |
|-----------|-----------------|---------------------|------|
| Acute threshold | 0.5-1.0 | 0.3-0.7 | V @ 0.4ms |
| Chronic threshold (1 yr) | 1.0-2.5 | 0.5-1.0 | V @ 0.4ms |
| Threshold rise (acute→chronic) | 50-200% | 10-50% | % |
| Chronic impedance | 500-1000 | 400-800 | Ω |
| Sensing amplitude (R-wave) | 5-15 | 8-20 | mV |
| Long-term stability | Moderate | Excellent | — |

### Steroid Elution Rate

```
  C_steroid(t) = C₀ × e^(-t/τ_elute)

  where:
    C₀ = initial concentration (1 mg equivalent)
    τ_elute = elution time constant (6-12 months)
    t = time since implant

  Effective steroid delivery: 6-12 months
  After elution: Threshold may slowly rise (but remains
  lower than non-steroid leads due to reduced fibrosis)
```

---

## 2.7.9 Lead Compatibility Standards

| Standard | Description | Key Requirements |
|----------|------------|-----------------|
| ISO 5841-1 | Pacemaker leads - General | Biocompatibility, electrical |
| ISO 5841-2 | Pacemaker leads - Electrodes | Material, surface, coating |
| ISO 5841-3 | Pacemaker leads - Connectors | IS-1, DF-1, LS-1 connectors |
| IEC 60601-1 | Medical electrical equipment | Safety, EMC |
| AAMI/ANSI NS15 | Pacemaker lead testing | Mechanical, electrical, environmental |

### Connector Standards

| Standard | Connector Type | Application |
|----------|---------------|------------|
| IS-1 | Single-pass, bipolar | Standard pacing leads |
| DF-1 | Dual-pass, bipolar | ICD leads |
| DF-4 | Triple-pass, quadripolar | CRT leads |
| IS-4 | Quadripolar | LV pacing leads |

---

## 2.7.10 Summary

The lead interface design is critical for reliable pacing and sensing:

1. **Electrode-tissue interface**: The complex impedance of the interface
   affects both pacing threshold and sensing quality. Understanding the
   interface physics is essential for optimizing both functions.

2. **Lead impedance**: Typical chronic bipolar impedance is 400-1000 Ω,
   with monitoring accuracy of ±5%. Impedance trends provide early warning
   of lead failure.

3. **Failure modes**: Conductor fracture and insulation breach are the most
   common failure modes, detectable by impedance monitoring.

4. **Polarization**: Electrode polarization after pacing reduces stimulation
   efficiency and masks evoked response. Mitigation techniques include
   charge balancing, biphasic pulses, and high-surface-area electrodes.

5. **Steroid elution**: Steroid-eluting leads significantly reduce chronic
   pacing thresholds and improve long-term stability.

The lead interface circuit in the pacemaker IC must provide high-impedance
sensing (> 10 MΩ), high-voltage pacing (up to 8V, 25 mA), accurate
impedance measurement (±5%), and robust protection against ESD and
high-voltage events.
