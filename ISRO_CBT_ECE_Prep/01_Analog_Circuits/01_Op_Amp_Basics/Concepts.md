# Op-Amp Basics - Concepts

## 1. Ideal Op-Amp Properties

### Infinite Parameters
- Open-loop voltage gain (A_OL) = infinity
- Input impedance (Z_in) = infinity
- Bandwidth (BW) = infinity
- CMRR = infinity

### Zero Parameters
- Output impedance (Z_out) = 0
- Input offset voltage = 0
- Input bias current = 0
- Power supply rejection ratio (PSRR) = infinity

### Practical Op-Amp (741 type)
- A_OL ~ 10^5 to 10^6 (100-120 dB)
- Z_in ~ 2 MΩ (BJT input), ~10^12 Ω (FET input)
- Z_out ~ 75 Ω
- BW ~ 1 MHz (GBW product)
- Slew rate ~ 0.5 V/μs (741)
- CMRR ~ 90 dB
- Input offset voltage ~ 2-5 mV
- Input bias current ~ 80 nA (BJT), ~pA (FET)

---

## 2. Virtual Ground / Virtual Short Concept

### Virtual Short (Between Input Terminals)
- When op-amp is in negative feedback, V+ ≈ V-
- The two input terminals are at nearly same potential
- NOT a physical short - no current flows between them
- Always valid when: negative feedback exists AND op-amp is in linear region

### Virtual Ground
- Special case of virtual short
- When V+ = 0V (grounded), then V- ≈ 0V
- Node is at ground potential but NOT connected to ground
- Current can flow into/out of this node

### When Virtual Ground FAILS
- Open-loop configuration (comparator mode)
- Positive feedback (Schmitt trigger)
- Op-amp is saturated (output at rail voltage)
- During large transient signals

---

## 3. Input Bias Current (I_B)

### Definition
- Average of currents flowing into the two input terminals
- I_B = (I_B+ + I_B-) / 2
- For 741: I_B ~ 80 nA

### Input Offset Current
- Difference between bias currents
- I_OS = |I_B+ - I_B-|
- For 741: I_OS ~ 20 nA

### Effect on Circuit
- Creates unwanted voltage drop across input resistors
- Causes DC offset at output
- Compensation: Connect R_comp = R1 || Rf to non-inverting terminal

---

## 4. Input Offset Voltage (V_OS)

### Definition
- Small differential DC voltage needed at input to make output zero
- For 741: V_OS ~ 2 mV
- Caused by mismatch in input transistor pair

### Effects
- Output has DC offset: V_out(offset) = V_OS × (1 + Rf/R1)
- Temperature dependent - drifts with temperature

### Nulling
- Use offset null pins (pins 1 and 5 on 741)
- External potentiometer connected between pins 1 and 5 with wiper to V-

---

## 5. Common Mode Rejection Ratio (CMRR)

### Definition
- Ratio of differential gain to common-mode gain
- CMRR = A_d / A_cm
- In dB: CMRR(dB) = 20 log(A_d / A_cm)

### Significance
- Measures ability to reject noise common to both inputs
- Higher CMRR = better noise rejection
- 741: CMRR ~ 90 dB (about 31,623)

### Common Mode Gain (A_cm)
- Output when same signal applied to both inputs
- For ideal op-amp: A_cm = 0
- Finite due to resistor mismatches

---

## 6. Slew Rate (SR)

### Definition
- Maximum rate of change of output voltage
- SR = (dV_out/dt)_max
- For 741: SR = 0.5 V/μs
- Determined by internal compensation capacitor charging current

### Full-Power Bandwidth
- FPBW = SR / (2π × V_peak)
- Maximum frequency for undistorted large-signal output

### Relationship with Small-Signal BW
- Small signal: BW = GBW (gain-bandwidth product)
- Large signal: limited by slew rate
- If slew rate limiting → output becomes triangular wave

### ISRO Tip
- For sinusoidal output V = V_p sin(2πft):
- Max slew rate needed: SR_needed = 2πf × V_p
- If SR_needed > SR_available → distortion occurs

---

## 7. Gain-Bandwidth Product (GBW)

### Definition
- Product of closed-loop gain and bandwidth = constant
- GBW = A_CL × BW = A_OL × f_3dB(open-loop)
- For 741: GBW = 1 MHz

### Key Relationships
- Higher the gain → narrower the bandwidth
- At unity gain (voltage follower): BW = GBW = 1 MHz
- At gain of 100: BW = 1 MHz / 100 = 10 kHz

### Unity Gain Frequency (f_T)
- Frequency where open-loop gain drops to unity
- f_T = GBW for voltage feedback op-amps
- f_T = GBW for 741 = 1 MHz

---

## 8. Op-Amp with Negative Feedback

### Why Negative Feedback?
- Stabilizes gain (makes it independent of A_OL variations)
- Increases bandwidth
- Reduces distortion
- Lowers output impedance
- Increases input impedance

### Feedback Factor (β)
- Fraction of output fed back to input
- β = R1 / (R1 + Rf) for inverting amplifier
- Loop gain = A_OL × β

### Closed-Loop Gain
- A_CL = A_OL / (1 + A_OL × β)
- For large A_OL × β: A_CL ≈ 1/β
- This is the ideal gain formula

### Inverting Amplifier
- The inverting input is a virtual ground when the non-inverting input is grounded
- Gain: A_CL = -R_f / R_in
- For R_in = 10 kΩ and R_f = 20 kΩ, A_CL = -2

```circuit
op = elm.Opamp(leads=True).label("U1", loc="center")
elm.Line().down(0.25).at(op.in2)
elm.Ground(lead=False)
Rin = elm.Resistor().left().at(op.in1).idot().label("Rin 10k", loc="bottom")
elm.Line().left(0.25).at(Rin.start).label("Vin", loc="left")
elm.Line().up(0.5).at(op.in1)
elm.Resistor().tox(op.out).label("Rf 20k", loc="left")
elm.Line().toy(op.out).dot()
elm.Line().right(0.5).at(op.out).label("Vout", loc="right")
```

### Non-Inverting Amplifier
- The input is applied to the non-inverting terminal
- Gain: A_CL = 1 + R_f / R_1
- For R_1 = 10 kΩ and R_f = 20 kΩ, A_CL = 3

```circuit
op = elm.Opamp(leads=True).label("U1", loc="center")
out = elm.Line().at(op.out).length(0.75)
elm.Line().up().at(op.in1).length(1.5).dot()
elm.Resistor().left().label("R1 10k", loc="bottom")
elm.Ground()
elm.Resistor().tox(op.out).label("Rf 20k", loc="left")
elm.Line().toy(op.out).dot()
elm.Resistor().left().at(op.in2).idot().label("R2 20k", loc="bottom")
elm.SourceV().down().reverse().label("Vin", loc="left")
elm.Line().right().dot()
elm.Resistor().up().label("R3 20k", loc="right").hold()
elm.Line().tox(out.end)
elm.Gap().toy(op.out).label(["-", "Vout", "+"])
```

### Open-Loop Comparator
- No negative feedback is present
- V+ = 0 V and V- = V_in
- A positive V_in drives the output negative; a negative V_in drives it positive
- The virtual-short condition does not apply because the op-amp operates in saturation

```circuit
op = elm.Opamp(leads=True).label("Comparator", loc="center")
Rin = elm.Resistor().left().at(op.in1).idot().label("Rin 1k", loc="bottom")
elm.Line().left(0.25).at(Rin.start).label("Vin", loc="left")
elm.Ground().at(op.in2)
elm.Line().right(0.75).at(op.out).label("Vout: saturated", loc="right")
```

---

## 9. Op-Amp Specifications for ISRO

| Parameter | 741 Value | Importance |
|-----------|-----------|------------|
| A_OL | 10^6 | High gain needed |
| GBW | 1 MHz | Sets max frequency |
| SR | 0.5 V/μs | Large signal response |
| CMRR | 90 dB | Noise rejection |
| V_OS | 2 mV | DC accuracy |
| I_B | 80 nA | Input loading |
| Z_out | 75 Ω | Driving capability |
| Supply | ±15V | Output swing ±13V |

---

## 10. Op-Amp Internal Architecture

### Differential Input Stage
- First stage: Differential pair (BJT or MOSFET)
- Provides most of the voltage gain
- Determines CMRR and input characteristics

### Gain Stage
- Common-emitter/source amplifier
- Provides additional voltage gain

### Output Stage
- Class AB push-pull amplifier
- Low output impedance
- High current driving capability

### Compensation Capacitor
- Internal capacitor (typically 30 pF in 741)
- Ensures stability (prevents oscillation)
- Limits slew rate and bandwidth

---

## 11. Rail-to-Rail Op-Amps

### Concept
- Output can swing close to both supply rails
- Input common-mode range includes both rails
- Important for single-supply applications

### ISRO Relevance
- Modern low-voltage circuits
- Battery-powered applications
- DSP interfacing

---

## 12. Chopper-Stabilized Op-Amps

- Eliminate offset voltage and drift
- Use internal chopping to cancel DC offsets
- V_OS < 1 μV achievable
- Used in precision instrumentation

---

## 13. ISRO-Specific Tips for Op-Amp Basics

1. **Most asked**: Virtual ground concept - understand when it applies and when it fails
2. **Slew rate questions**: Always check if signal is small-signal or large-signal
3. **GBW trade-off**: Higher gain = lower bandwidth
4. **Compensation**: Internal compensation makes 741 "unconditionally stable"
5. **ISRO favorite**: Calculate output offset due to V_OS and I_B
6. **Remember**: For ideal op-amp, both input currents are zero AND voltage difference is zero
7. **Quick check**: If output is at rail → virtual ground concept is INVALID
8. **CMRR dB conversion**: Every 20 dB = factor of 10 in gain ratio
