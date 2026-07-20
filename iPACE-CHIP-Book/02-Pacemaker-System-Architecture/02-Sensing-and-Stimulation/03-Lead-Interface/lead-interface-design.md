# Lead Interface Design

## 2.2.3 Lead Interface Design

### 2.2.3.1 Lead System Overview

The lead system provides the electrical connection between the pacemaker pulse
generator and the cardiac tissue. It is a critical component that must maintain
reliable electrical contact over decades of implantation.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LEAD SYSTEM OVERVIEW                                      │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  LEAD COMPONENTS:                                                    │  │
│  │                                                                      │  │
│  │  ┌──────────────────────────────────────────────────────────────┐   │  │
│  │  │                                                              │   │  │
│  │  │  ┌─────────┐  ┌─────────────┐  ┌──────────┐  ┌──────────┐ │   │  │
│  │  │  │ CONNECTOR│  │   CONDUCTOR │  │INSULATION│  │   TIP    │ │   │  │
│  │  │  │ (Pin/   │  │   (Wire/    │  │ (Polyure-│  │ELECTRODE │ │   │  │
│  │  │  │  Can-   │  │    Cable)   │  │  thane/  │  │(Platinum │ │   │  │
│  │  │  │  nector)│  │             │  │  Silicone)│  │  or Ir)  │ │   │  │
│  │  │  └─────────┘  └─────────────┘  └──────────┘  └──────────┘ │   │  │
│  │  │                                                              │   │  │
│  │  │  ◄─────────────── Lead Length: 40-60 cm ──────────────────► │   │  │
│  │  │                                                              │   │  │
│  │  └──────────────────────────────────────────────────────────────┘   │  │
│  │                                                                      │  │
│  │  LEAD TYPES:                                                        │  │
│  │  ────────────                                                       │  │
│  │                                                                      │  │
│  │  ┌──────────────────────────────────────────────────────────────┐   │  │
│  │  │  UNIPOLAR LEAD                                                │   │  │
│  │  │  ┌──────────────────────────────────────────────────────┐   │   │  │
│  │  │  │  Pin ──── Conductor ──── Tip Electrode              │   │   │  │
│  │  │  │                     (single wire)                    │   │   │  │
│  │  │  │                                                      │   │   │  │
│  │  │  │  Return path: Can (pulse generator case)            │   │   │  │
│  │  │  │                                                      │   │   │  │
│  │  │  │  Advantages:                                         │   │   │  │
│  │  │  │  • Simpler construction                              │   │   │  │
│  │  │  │  • Smaller diameter                                  │   │   │  │
│  │  │  │  • Lower cost                                        │   │   │  │
│  │  │  │                                                      │   │   │  │
│  │  │  │  Disadvantages:                                      │   │   │  │
│  │  │  │  • Larger sensing field (more far-field)            │   │   │  │
│  │  │  │  • More susceptible to EMI                           │   │   │  │
│  │  │  │  • Cannot measure true lead impedance               │   │   │  │
│  │  │  └──────────────────────────────────────────────────────┘   │   │  │
│  │  │                                                              │   │  │
│  │  │  BIPOLAR LEAD (Recommended)                                 │   │  │
│  │  │  ┌──────────────────────────────────────────────────────┐   │   │  │
│  │  │  │  Tip Pin ──── Conductor 1 ──── Tip Electrode        │   │   │  │
│  │  │  │                                                      │   │   │  │
│  │  │  │  Ring Pin ── Conductor 2 ──── Ring Electrode        │   │   │  │
│  │  │  │  (2mm from tip)                                      │   │   │  │
│  │  │  │                                                      │   │   │  │
│  │  │  │  Advantages:                                         │   │   │  │
│  │  │  │  • Localized sensing (less far-field)               │   │   │  │
│  │  │  │  • Better EMI rejection                              │   │   │  │
│  │  │  │  • Accurate impedance measurement                   │   │   │  │
│  │  │  │  • Industry standard for modern pacemakers           │   │   │  │
│  │  │  │                                                      │   │   │  │
│  │  │  │  Disadvantages:                                      │   │   │  │
│  │  │  │  • Slightly larger diameter                          │   │   │  │
│  │  │  │  • Higher cost                                       │   │   │  │
│  │  │  └──────────────────────────────────────────────────────┘   │   │  │
│  │  │                                                              │  │
│  │  └──────────────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.3.2 Lead Impedance Characteristics

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LEAD IMPEDANCE CHARACTERISTICS                            │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  IMPEDANCE COMPONENTS:                                               │  │
│  │                                                                      │  │
│  │  Z_lead = R_conductor + R_electrode + Z_interface + R_tissue       │  │
│  │                                                                      │  │
│  │  ┌──────────────────────────────────────────────────────────────┐   │  │
│  │  │                                                              │   │  │
│  │  │  1. CONDUCTOR RESISTANCE (R_conductor)                      │   │  │
│  │  │     • Source: Resistance of lead wire/cable                 │   │  │
│  │  │     • Value: 20-100 Ω (depends on length and gauge)        │   │  │
│  │  │     • Material: MP35N (Ni-Co-Cr-Mo) or silver              │   │  │
│  │  │     • Increases with lead length (longer = higher R)        │   │  │
│  │  │                                                              │   │  │
│  │  │  2. ELECTRODE RESISTANCE (R_electrode)                      │   │  │
│  │  │     • Source: Contact resistance at electrode tip           │   │  │
│  │  │     • Value: 10-50 Ω (depends on surface area)             │   │  │
│  │  │     • Material: Pt/Ir (90/10) or Pt coating                │   │  │
│  │  │     • Surface area: 4-12 mm² (tip electrode)               │   │  │
│  │  │                                                              │   │  │
│  │  │  3. ELECTRODE-TISSUE INTERFACE (Z_interface)                │   │  │
│  │  │     • Source: Electrochemical double layer                  │   │  │
│  │  │     • Value: 100-500 Ω (frequency dependent)               │   │  │
│  │  │     • Behaves as parallel RC (charge transfer + capacitive)│   │  │
│  │  │     • R_ct: 200-1000 Ω (charge transfer resistance)       │   │  │
│  │  │     • C_dl: 1-10 µF (double-layer capacitance)            │   │  │
│  │  │     • Varies with: heart rate, tissue health, drugs        │   │  │
│  │  │                                                              │   │  │
│  │  │  4. TISSUE RESISTANCE (R_tissue)                            │   │  │
│  │  │     • Source: Myocardial tissue resistivity                 │   │  │
│  │  │     • Value: 50-200 Ω                                      │   │  │
│  │  │     • Varies with: tissue hydration, fibrosis             │   │  │
│  │  │                                                              │   │  │
│  │  └──────────────────────────────────────────────────────────────┘   │  │
│  │                                                                      │  │
│  │  IMPEDANCE FREQUENCY RESPONSE:                                      │  │
│  │                                                                      │  │
│  │  |Z| (Ω)                                                            │  │
│  │    │                                                                 │  │
│  │  800┤                                                               │  │
│  │     │                                                               │  │
│  │  600┤  ╲                                                            │  │
│  │     │   ╲                                                           │  │
│  │  500┤    ╲────────────────────────────── DC impedance              │  │
│  │     │     ╲                    ═══════════════════════             │  │
│  │  400┤      ╲                                                          │  │
│  │     │       ╲                                                        │  │
│  │  300┤        ╲                                                       │  │
│  │     │         ╲────────────────────────── AC impedance (1kHz)       │  │
│  │  200┤          ╲       ═══════════════════════════════             │  │
│  │     │           ╲                                                    │  │
│  │  100┤            ╲────────────────────────── High-freq limit       │  │
│  │     │             ╲       ═══════════════════════════════          │  │
│  │    0┤──────────────┼──────────────┼──────────────┼──────▶          │  │
│  │     0.1            1             10            100      f(kHz)    │  │
│  │                                                                      │  │
│  │  Note: Impedance decreases with frequency due to C_dl shunting     │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  IMPEDANCE RANGES BY LEAD TYPE:                                      │  │
│  │                                                                      │  │
│  │  ┌──────────────────────┬──────────┬──────────┬────────────────┐   │  │
│  │  │ Lead Type            │ DC (Ω)   │ 1kHz (Ω) │ Notes          │   │  │
│  │  ├──────────────────────┼──────────┼──────────┼────────────────┤   │  │
│  │  │ Active-fixation     │ 300-800  │ 200-500  │ Helix tip      │   │  │
│  │  │ (screw-in)          │          │          │                │   │  │
│  │  │ Passive-fixation    │ 300-800  │ 200-500  │ Tined tip      │   │  │
│  │  │ (tined)             │          │          │                │   │  │
│  │  │ Steroid-eluting     │ 300-800  │ 200-400  │ Lower chronic  │   │  │
│  │  │                      │          │          │ thresholds     │   │  │
│  │  │ LV lead (CRT)       │ 400-1000 │ 300-600  │ Longer, more   │   │  │
│  │  │                      │          │          │ resistance     │   │  │
│  │  └──────────────────────┴──────────┴──────────┴────────────────┘   │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.3.3 Lead Failure Modes

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LEAD FAILURE MODES                                        │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  FAILURE MODE 1: CONDUCTOR FRACTURE                                  │  │
│  │  ──────────────────────────────────                                  │  │
│  │                                                                      │  │
│  │  Cause: Mechanical stress (flexion at rib-clavicle junction)       │  │
│  │  Frequency: ~0.5% per year (varies by lead model)                  │  │
│  │                                                                      │  │
│  │  Lead: ═══════════╗  ╔══════════                                    │  │
│  │                    ║  ║                                              │  │
│  │                    ╚══╝                                              │  │
│  │                   (fracture point)                                  │  │
│  │                                                                      │  │
│  │  Electrical effect:                                                 │  │
│  │  • Open circuit: Z → ∞ (no pacing, no sensing)                    │  │
│  │  • Intermittent: Z fluctuates (noise on sensing channel)           │  │
│  │  • Detection: Impedance >2000 Ω or erratic measurements           │  │
│  │                                                                      │  │
│  │  Detection algorithm:                                               │  │
│  │  • If Z > 2000 Ω for >5 minutes → Lead fracture alert            │  │
│  │  • If Z fluctuates >50% within 1 minute → Intermittent alert     │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  FAILURE MODE 2: INSULATION BREACH                                   │  │
│  │  ────────────────────────────────                                    │  │
│  │                                                                      │  │
│  │  Cause: Mechanical wear, chemical degradation, manufacturing defect│  │
│  │  Frequency: ~0.1-0.3% per year                                     │  │
│  │                                                                      │  │
│  │  Lead: ═══════════════════════════                                  │  │
│  │                    ╲                                                 │  │
│  │                     ╲──── (insulation breach)                       │  │
│  │                                                                      │  │
│  │  Electrical effect:                                                 │  │
│  │  • Current leak to adjacent conductor or tissue                    │  │
│  │  • Impedance decreases: Z < 200 Ω                                 │  │
│  │  • Cross-talk between channels                                     │  │
│  │                                                                      │  │
│  │  Detection: Z < 200 Ω for >5 minutes → Insulation breach alert  │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  FAILURE MODE 3: ELECTRODE DISLODGING                               │  │
│  │  ────────────────────────────────────                                │  │
│  │                                                                      │  │
│  │  Cause: Lead tip migration from implantation site                   │  │
│  │  Frequency: ~2-5% in first month (acute), <0.5% thereafter        │  │
│  │                                                                      │  │
│  │  Electrical effect:                                                 │  │
│  │  • Capture threshold increases dramatically                        │  │
│  │  • Sensing amplitude decreases                                     │  │
│  │  • Impedance may increase (if tip contacts non-conductive tissue) │  │
│  │                                                                      │  │
│  │  Detection:                                                        │  │
│  │  • Capture threshold >5V @ 0.5ms (acute)                          │  │
│  │  • R-wave amplitude <2mV sustained                                │  │
│  │  • Both conditions persisting >24 hours                           │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  FAILURE MODE 4: LEAD-DEVICE CONNECTION ISSUE                       │  │
│  │  ─────────────────────────────────────────────                       │  │
│  │                                                                      │  │
│  │  Cause: Loose set screw, corrosion at connector, wrong lead type   │  │
│  │                                                                      │  │
│  │  Electrical effect:                                                 │  │
│  │  • High impedance at connector interface                           │  │
│  │  • Intermittent high impedance (motion-dependent)                  │  │
│  │  • Noise artifacts on sensing channel                              │  │
│  │                                                                      │  │
│  │  Detection:                                                        │  │
│  │  • Impedance >1000 Ω intermittent                                 │  │
│  │  • Noise rate >10 events/minute                                   │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  FAILURE MODE SUMMARY:                                                     │
│  ┌─────────────────────┬───────────┬───────────┬───────────┬────────────┐ │
│  │ Failure Mode        │ Impedance │ Sensing   │ Capture   │ Detection  │ │
│  │                     │ Change    │ Effect    │ Effect    │ Method     │ │
│  ├─────────────────────┼───────────┼───────────┼───────────┼────────────┤ │
│  │ Conductor fracture  │ ↑↑↑ (>2k)│ None/Noise│ No capture│ Z > 2kΩ   │ │
│  │ Insulation breach   │ ↓↓ (<200) │ Cross-talk│ May work  │ Z < 200Ω  │ │
│  │ Electrode dislodge  │ ↑ (mod)  │ ↓ Amplitude│ ↑ Thresh │ Dual check│ │
│  │ Connector issue     │ ↑↑ (int) │ Noise      │ Intermitt│ Z erratic │ │
│  │ Lead infection      │ Variable │ Variable  │ Variable  │ Clinical  │ │
│  │ Twiddler's syndrome │ Variable │ ↓ Amp     │ ↑ Thresh  │ Imaging   │ │
│  └─────────────────────┴───────────┴───────────┴───────────┴────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.3.4 Polarization Effects

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ELECTRODE POLARIZATION                                    │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  POLARIZATION MECHANISM:                                             │  │
│  │                                                                      │  │
│  │  During pacing, ions accumulate at the electrode-tissue interface,  │  │
│  │  creating a voltage (afterpotential) that opposes the pacing pulse. │  │
│  │                                                                      │  │
│  │  Voltage                                                             │  │
│  │  at electrode:                                                       │  │
│  │    │                                                                 │  │
│  │    │    Pace pulse                                                   │  │
│  │    │    ┌──────┐                                                    │  │
│  │    │    │      │                                                    │  │
│  │  0 ┤────┘      ├──────┬────────────────────────────               │  │
│  │    │           │      │                                             │  │
│  │    │           │      │  Afterpotential (polarization)              │  │
│  │    │           │      │  (exponential decay)                        │  │
│  │    │           │      │                                             │  │
│  │    │           │      └─────────────────────────────               │  │
│  │    │           │                                                    │  │
│  │    │           │  ◄──── Afterpotential ────►                       │  │
│  │    │           │      (typically 200-500mV)                        │  │
│  │    │           │                                                    │  │
│  │    │  ◄─ Vp ─►│                                                    │  │
│  │    │           │                                                    │  │
│  │    └───────────┼────────────────────────────────────▶              │  │
│  │                0                    Time                            │  │
│  │                                                                      │  │
│  │  The afterpotential obscures the intrinsic cardiac signal during    │  │
│  │  the post-pace blanking period, limiting sensing sensitivity.      │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  POLARIZATION REDUCTION TECHNIQUES:                                  │  │
│  │                                                                      │  │
│  │  1. SMALL ELECTRODE SURFACE AREA                                    │  │
│  │     • Smaller electrodes → lower polarization                       │  │
│  │     • But: Higher current density → more tissue damage             │  │
│  │     • Balance: 4-8 mm² tip area                                    │  │
│  │                                                                      │  │
│  │  2. POROUS ELECTRODE SURFACE                                        │  │
│  │     • Micro/macro porous surface increases effective area           │  │
│  │     • Reduces effective current density                             │  │
│  │     • Reduces polarization by 30-50%                               │  │
│  │                                                                      │  │
│  │  3. STEROID ELUTION                                                  │  │
│  │     • Dexamethasone sodium phosphate eluted from tip                │  │
│  │     • Reduces inflammation at electrode-tissue interface            │  │
│  │     • Maintains low chronic thresholds (1-2V vs 3-5V)            │  │
│  │     • Reduces polarization afterpotential by 40-60%                │  │
│  │                                                                      │  │
│  │  4. CHARGE BALANCING                                                 │  │
│  │     • Active charge balance after each pace pulse                   │  │
│  │     • Removes residual charge from interface                       │  │
│  │     • Reduces DC polarization component                            │  │
│  │                                                                      │  │
│  │  5. BIPHASIC PULSES (research)                                      │  │
│  │     • Positive phase followed by equal negative phase              │  │
│  │     • Perfectly charge-balanced inherently                          │  │
│  │     • Not commonly used in pacemakers (more complex)               │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  POLARIZATION MEASUREMENT:                                           │  │
│  │                                                                      │  │
│  │  Measured immediately after pace pulse:                              │  │
│  │                                                                      │  │
│  │  Vpol = V_pace × (R_interface / (R_interface + R_lead))           │  │
│  │                                                                      │  │
│  │  Typical values:                                                    │  │
│  │  • Platinum electrode: 300-500 mV (after 0.5ms pulse)             │  │
│  │  • Porous Pt electrode: 150-300 mV                                │  │
│  │  • Steroid-eluting: 100-200 mV                                    │  │
│  │  • Carbon electrode: 100-250 mV                                   │  │
│  │                                                                      │  │
│  │  Measurement circuit:                                               │  │
│  │  • High-impedance buffer (>1 GΩ)                                  │  │
│  │  • Sample-and-hold after pace                                       │  │
│  │  • ADC conversion (10-bit sufficient)                              │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.3.5 Tip Electrode Materials and Design

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    TIP ELECTRODE MATERIALS AND DESIGN                        │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  ELECTRODE MATERIALS COMPARISON:                                     │  │
│  │                                                                      │  │
│  │  ┌───────────────┬────────────┬────────────┬────────────┬────────┐ │  │
│  │  │ Material      │ Surface    │ Polarizat. │ Chronic    │ Cost   │ │  │
│  │  │               │ Area (mm²) │ (mV)       │ Threshold  │        │ │  │
│  │  ├───────────────┼────────────┼────────────┼────────────┼────────┤ │  │
│  │  │ Pt/Ir (90/10) │ 4-12       │ 300-500    │ 1.5-3.0V   │ $$$$   │ │  │
│  │  │ Platinum      │ 4-12       │ 250-450    │ 1.5-2.5V   │ $$$    │ │  │
│  │  │ Elgiloy       │ 6-15       │ 350-550    │ 2.0-4.0V   │ $$     │ │  │
│  │  │ Titanium      │ 6-15       │ 400-600    │ 2.5-5.0V   │ $      │ │  │
│  │  │ Carbon        │ 4-10       │ 100-250    │ 1.0-2.0V   │ $$$    │ │  │
│  │  │ Iridium oxide│ 4-8        │ 80-200     │ 0.5-1.5V   │ $$$$   │ │  │
│  │  └───────────────┴────────────┴────────────┴────────────┴────────┘ │  │
│  │                                                                      │  │
│  │  RECOMMENDED: Pt/Ir (90/10) with porous surface coating           │  │
│  │  (Industry standard, proven long-term reliability)                  │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  ELECTRODE GEOMETRY:                                                 │  │
│  │                                                                      │  │
│  │  ┌──────────────────────────────────────────────────────────────┐   │  │
│  │  │                                                              │   │  │
│  │  │  ACTIVE-FIXATION (SCREW-IN):                                 │   │  │
│  │  │                                                              │   │  │
│  │  │       ┌───┐                                                  │   │  │
│  │  │       │   │  Helix (active screw)                           │   │  │
│  │  │       │   │  Material: Pt/Ir or Elgiloy                     │   │  │
│  │  │       │   │  Diameter: 1.0-1.5 mm                           │   │  │
│  │  │       │   │  Length: 1.0-2.0 mm                             │   │  │
│  │  │       │   │  Turns: 2-4                                     │   │  │
│  │  │       └───┘                                                  │   │  │
│  │  │       ┌───┐                                                  │   │  │
│  │  │       │   │  Ring electrode                                 │   │  │
│  │  │       │   │  2-5 mm from tip                                │   │  │
│  │  │       │   │  Material: Pt/Ir                                │   │  │
│  │  │       │   │  Width: 1-2 mm                                  │   │  │
│  │  │       └───┘                                                  │   │  │
│  │  │                                                              │   │  │
│  │  │  Advantages:                                                 │   │  │
│  │  │  • Secure fixation (less dislodgement)                      │   │  │
│  │  │  • Can be placed anywhere (not dependent on trabeculae)     │   │  │
│  │  │  • Lower acute dislodgement rate (<1%)                      │   │  │
│  │  │                                                              │   │  │
│  │  │  Passive-FIXATION (TINED):                                   │   │  │
│  │  │                                                              │   │  │
│  │  │       ┌───┐                                                  │   │  │
│  │  │       │   │  Tip electrode                                  │   │  │
│  │  │       │   │  Material: Pt/Ir                                │   │  │
│  │  │       └───┘                                                  │   │  │
│  │  │      ╱│╲                                                     │   │  │
│  │  │     ╱ │ ╲  Silicone tines                                  │   │  │
│  │  │        │     (4 tines, 90° apart)                           │   │  │
│  │  │                                                              │   │  │
│  │  │  Advantages:                                                 │   │  │
│  │  │  • Simpler design                                            │   │  │
│  │  │  • Less trauma during placement                             │   │  │
│  │  │  • Self-tenting in trabeculae                               │   │  │
│  │  │                                                              │   │  │
│  │  └──────────────────────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  SURFACE TREATMENTS:                                                 │  │
│  │                                                                      │  │
│  │  1. MACROPOROUS COATING                                              │  │
│  │     • Sintered platinum powder                                      │  │
│  │     • Surface area: 10-100× geometric area                          │  │
│  │     • Reduces effective current density                             │  │
│  │     • Reduces polarization by 40-60%                               │  │
│  │                                                                      │  │
│  │  2. MICROPOROUS COATING                                              │  │
│  │     • Electrochemical deposition                                   │  │
│  │     • Surface area: 5-20× geometric area                           │  │
│  │     • More uniform coating                                          │  │
│  │                                                                      │  │
│  │  3. IRIDIUM OXIDE COATING (IrOx)                                   │  │
│  │     • Electrochemically deposited                                   │  │
│  │     • Very high surface area                                        │  │
│  │     • Lowest polarization (<100 mV)                                │  │
│  │     • Higher cost                                                   │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.3.6 Lead Impedance Measurement Circuit

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LEAD IMPEDANCE MEASUREMENT CIRCUIT                        │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  MEASUREMENT METHOD: DC PULSE TECHNIQUE                             │  │
│  │                                                                      │  │
│  │  A known current pulse is applied to the lead, and the resulting    │  │
│  │  voltage is measured. Impedance = V/I (Ohm's law).                 │  │
│  │                                                                      │  │
│  │  ┌──────────────────────────────────────────────────────────────┐   │  │
│  │  │                                                              │   │  │
│  │  │  Vdd                                                         │   │  │
│  │  │   │                                                          │   │  │
│  │  │   ├──────┐                                                  │   │  │
│  │  │   │      │                                                  │   │  │
│  │  │   │  ┌───┴───┐                                             │   │  │
│  │  │   │  │ Current│                                            │   │  │
│  │  │   │  │ Source │  I = 10µA (typical)                       │   │  │
│  │  │   │  │        │  Duration: 10µs                           │   │  │
│  │  │   │  └───┬───┘                                             │   │  │
│  │  │   │      │                                                  │   │  │
│  │  │   │      ├──────┬──────────────────┐                      │   │  │
│  │  │   │      │      │                  │                      │   │  │
│  │  │   │      │   ┌──┴──┐           ┌──┴──┐                   │   │  │
│  │  │   │      │   │ V-  │           │Tip  │                   │   │  │
│  │  │   │      │   │     │           │(Lead)│                   │   │  │
│  │  │   │      │   │ ADC │           └──┬──┘                   │   │  │
│  │  │   │      │   │(10b)│              │                      │   │  │
│  │  │   │      │   └──┬──┘           ┌──┴──┐                   │   │  │
│  │  │   │      │      │              │Ring/│                   │   │  │
│  │  │   │      │      │              │ Can │                   │   │  │
│  │  │   │      │      │              └─────┘                   │   │  │
│  │  │   │      │      │                                         │   │  │
│  │  │   │      │      └────── Return path                       │   │  │
│  │  │   │      │                                                  │   │  │
│  │  │   │      └──── Sense point (high-impedance buffer)        │   │  │
│  │  │   │                                                         │   │  │
│  │  │   └──── Supply                                               │   │  │
│  │  │                                                              │   │  │
│  │  │  MEASUREMENT SEQUENCE:                                       │   │  │
│  │  │  1. Apply current pulse (10µA, 10µs)                       │   │  │
│  │  │  2. Wait for settling (5µs)                                 │   │  │
│  │  │  3. Sample voltage (ADC: 10-bit)                            │   │  │
│  │  │  4. Compute Z = V_meas / I_source                           │   │  │
│  │  │  5. Repeat 4 times, average result                          │   │  │
│  │  │                                                              │   │  │
│  │  │  ACCURACY: ±5% (0-2000 Ω range)                           │   │  │
│  │  │  RESOLUTION: 2 Ω (10-bit ADC, 10µA source)                │   │  │
│  │  │  MEASUREMENT RATE: 1× per 8 seconds (low power)           │   │  │
│  │  │                                                              │   │  │
│  │  └──────────────────────────────────────────────────────────────┘   │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  IMPEDANCE MONITORING ALGORITHM:                                          │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  1. Measure impedance every 8 seconds                               │  │
│  │  2. Compare to baseline (stored in EEPROM)                         │  │
│  │  3. Trend analysis over 24-hour window                             │  │
│  │  4. Alert conditions:                                              │  │
│  │     • Z > 2000 Ω for >5 minutes → Lead fracture warning        │  │
│  │     • Z < 200 Ω for >5 minutes → Insulation breach warning    │  │
│  │     • Z changes >50% from baseline → Lead integrity alert      │  │
│  │  5. Store trending data in EEPROM (64 points × 8 bytes)          │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.3.7 Steroid-Eluting Leads

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    STEROID-ELUTING LEADS                                     │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  MECHANISM:                                                          │  │
│  │                                                                      │  │
│  │  Dexamethasone sodium phosphate (DEX) is embedded in the tip       │  │
│  │  electrode and slowly elutes into surrounding tissue.              │  │
│  │                                                                      │  │
│  │  ┌──────────────────────────────────────────────────────────────┐   │  │
│  │  │                                                              │   │  │
│  │  │  WITHOUT STEROID:                                            │   │  │
│  │  │  ┌──────────────────────────────────────────────────────┐   │   │  │
│  │  │  │                                                      │   │   │  │
│  │  │  │  Threshold (V)                                        │   │   │  │
│  │  │  │    │                                                   │   │   │  │
│  │  │  │  5 ┤         ╱──────────────── Chronic               │   │   │  │
│  │  │  │    │        ╱                                           │   │   │  │
│  │  │  │  4 ┤       ╱                                            │   │   │  │
│  │  │  │    │      ╱                                             │   │   │  │
│  │  │  │  3 ┤     ╱                                              │   │   │  │
│  │  │  │    │    ╱                                               │   │   │  │
│  │  │  │  2 ┤   ╱                                                │   │   │  │
│  │  │  │    │──╱─── Acute threshold                             │   │   │  │
│  │  │  │  1 ┤ ╱                                                   │   │   │  │
│  │  │  │    │╱                                                    │   │   │  │
│  │  │  │  0 ┤──────────────────────────────────────────────────  │   │   │  │
│  │  │  │    └──┬────┬────┬────┬────┬────┬────┬────┬────▶        │   │   │  │
│  │  │  │       1    3    6    12   24   36   48   60     Months  │   │   │  │
│  │  │  │                                                      │   │   │  │
│  │  │  │  Note: Significant rise in chronic threshold         │   │   │  │
│  │  │  │  (2-5× acute value due to fibrotic tissue growth)   │   │   │  │
│  │  │  └──────────────────────────────────────────────────────┘   │   │  │
│  │  │                                                              │   │  │
│  │  │  WITH STEROID:                                               │   │  │
│  │  │  ┌──────────────────────────────────────────────────────┐   │   │  │
│  │  │  │                                                      │   │   │  │
│  │  │  │  Threshold (V)                                        │   │   │  │
│  │  │  │    │                                                   │   │   │  │
│  │  │  │  5 ┤                                                   │   │   │  │
│  │  │  │    │                                                   │   │   │  │
│  │  │  │  4 ┤                                                   │   │   │  │
│  │  │  │    │                                                   │   │   │  │
│  │  │  │  3 ┤                                                   │   │   │  │
│  │  │  │    │                                                   │   │   │  │
│  │  │  │  2 ┤───────┬──────────────── Chronic (stable)       │   │   │  │
│  │  │  │    │       └─────────────────────────────────         │   │   │  │
│  │  │  │  1 ┤─── Acute threshold                               │   │   │  │
│  │  │  │    │                                                    │   │   │  │
│  │  │  │  0 ┤──────────────────────────────────────────────────  │   │   │  │
│  │  │  │    └──┬────┬────┬────┬────┬────┬────┬────┬────▶        │   │   │  │
│  │  │  │       1    3    6    12   24   36   48   60     Months  │   │   │  │
│  │  │  │                                                      │   │   │  │
│  │  │  │  Note: Minimal rise in chronic threshold             │   │   │  │
│  │  │  │  (1.2-1.5× acute value - much better!)              │   │   │  │
│  │  │  └──────────────────────────────────────────────────────┘   │   │  │
│  │  │                                                              │   │  │
│  │  └──────────────────────────────────────────────────────────────┘   │  │
│  │                                                                      │  │
│  │  BENEFITS:                                                          │  │
│  │  • Chronic threshold reduction: 40-60% (vs. non-steroid leads)    │  │
│  │  • Pacing energy savings: 50-70% (extending battery life)         │  │
│  │  • Lower polarization afterpotential (better sensing)             │  │
│  │  • Reduced inflammation at electrode-tissue interface             │  │
│  │  • Industry standard for modern pacemaker leads                   │  │
│  │                                                                      │  │
│  │  ELUTION RATE:                                                      │  │
│  │  • Dose: 1.0 mg dexamethasone sodium phosphate                   │  │
│  │  • Elution duration: 12-18 months                                 │  │
│  │  • Elution rate: ~0.05 µg/day (exponential decay)                │  │
│  │  • Therapeutic level maintained for >12 months                     │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.3.8 Lead Interface Specifications Summary

| Parameter                    | Atrial Lead | Ventricular Lead | LV Lead (CRT) | Unit   |
|------------------------------|-------------|------------------|---------------|--------|
| Lead length                  | 45–55       | 55–65            | 75–95         | cm     |
| Lead diameter                | 4.0–6.0     | 4.0–6.0          | 5.0–7.0       | Fr     |
| Tip electrode area           | 4–8         | 4–12             | 4–8           | mm²    |
| Tip material                 | Pt/Ir       | Pt/Ir            | Pt/Ir         | —      |
| Tip surface                  | Porous      | Porous           | Porous        | —      |
| Steroid-eluting              | Yes         | Yes              | Yes           | —      |
| Fixation type                | Active/Passive | Active/Passive | Active/Passive | —     |
| Ring electrode area          | 6–12        | 6–12             | 6–12          | mm²    |
| Conductor material           | MP35N       | MP35N            | MP35N         | —      |
| Insulation material          | Silicone/PU | Silicone/PU      | Silicone/PU   | —      |
| DC impedance range           | 200–1000    | 200–1000         | 300–1200      | Ω      |
| 1kHz impedance               | 200–500     | 200–500          | 300–600       | Ω      |
| Fracture rate                | <0.5%/yr    | <0.5%/yr         | <1%/yr        | —      |
| Insulation breach rate       | <0.2%/yr    | <0.2%/yr         | <0.3%/yr      | —      |
| Dislodgement rate (acute)    | <2%         | <2%              | <5%           | —      |
| Chronic threshold (steroid)  | 0.5–1.5V    | 0.5–2.0V         | 1.0–3.0V      | V      |
| R-wave amplitude (chronic)  | 2–10mV      | 5–20mV           | 2–10mV        | mV     |
| Steroid dose                 | 1.0mg DEX   | 1.0mg DEX        | 1.0mg DEX     | —      |
| Steroid duration             | >12 months  | >12 months       | >12 months    | —      |
| Connector type               | IS-1        | IS-1             | IS-1          | —      |

---

*Section 2.2.3 — Lead Interface Design*
*Previous: Section 2.2.2 — Pacing Pulse Generation | Next: Section 2.2.4 — Multi-Chamber Pacing*
