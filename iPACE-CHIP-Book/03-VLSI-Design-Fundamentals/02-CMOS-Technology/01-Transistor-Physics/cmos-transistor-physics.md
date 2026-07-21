# CMOS Transistor Physics

## 1. Introduction to MOSFET

The Metal-Oxide-Semiconductor Field-Effect Transistor (MOSFET) is the fundamental building block of CMOS technology. Understanding transistor physics is essential for VLSI design, as it directly impacts circuit performance, power consumption, and reliability.

### 1.1 MOSFET Structure

```
MOSFET Cross-Section:

         Gate (G)
          |
    ┌─────┴─────┐
    │  Metal     │
    ├────────────┤ ← Gate Oxide (SiO₂)
    │            │
S ──┤   Channel  ├── D
    │            │
    └────────────┘
         │
         B (Body/Bulk)

NMOS vs PMOS:
- NMOS: n+ source/drain in p-substrate
- PMOS: p+ source/drain in n-well

CMOS Process:
┌────────────────────────────────────┐
│        n-well                       │
│  ┌──────────┐                      │
│  │  PMOS    │                      │
│  └──────────┘                      │
│           p-substrate              │
│  ┌──────────┐                      │
│  │  NMOS    │                      │
│  └──────────┘                      │
└────────────────────────────────────┘
```

### 1.2 MOSFET Symbols

```
NMOS Symbol:
    D
    ↑
────┤
    │ ←── G
────┤
    ↓
    S

PMOS Symbol:
    S
    ↑
────┤
    │ ←── G (with bubble)
────┤
    ↓
    D

Four-Terminal Symbol (NMOS):
      D
      |
  ────┤
G ────┤
  ────┤
      |
      S
      |
      B
```

## 2. MOSFET Operating Regions

### 2.1 Region Definitions

```
NMOS Operating Regions:
Let V_GS = Gate-Source voltage
Let V_DS = Drain-Source voltage
Let V_TH = Threshold voltage

1. Cutoff Region (V_GS < V_TH):
   - Transistor is OFF
   - No current flows (I_D = 0)
   - Used for digital logic OFF state

2. Linear/Triode Region (V_GS ≥ V_TH and V_DS < V_GS - V_TH):
   - Transistor behaves like a resistor
   - Current increases linearly with V_DS
   - Used for analog resistors

3. Saturation Region (V_GS ≥ V_TH and V_DS ≥ V_GS - V_TH):
   - Current is independent of V_DS (approximately)
   - Used for analog amplifiers and digital ON state

4. Velocity Saturation (short-channel effect):
   - At high V_DS, carrier velocity saturates
   - Current becomes independent of V_DS
   - Important in sub-micron technologies
```

### 2.2 Current-Voltage Equations

```
NMOS Transistor Equations:

1. Cutoff Region:
   I_D = 0
   When: V_GS < V_TH

2. Linear (Triode) Region:
   I_D = μ_n × C_ox × (W/L) × [(V_GS - V_TH) × V_DS - V_DS²/2]
   
   Simplified (for small V_DS):
   I_D ≈ μ_n × C_ox × (W/L) × (V_GS - V_TH) × V_DS

   Where:
   μ_n = electron mobility (cm²/V·s)
   C_ox = gate oxide capacitance per unit area (F/cm²)
   W/L = transistor aspect ratio (width/length)
   V_GS = gate-source voltage
   V_TH = threshold voltage
   V_DS = drain-source voltage

3. Saturation Region:
   I_D = (1/2) × μ_n × C_ox × (W/L) × (V_GS - V_TH)² × (1 + λ × V_DS)

   Where:
   λ = channel-length modulation parameter (V⁻¹)
   λ ≈ 1/V_A (V_A = Early voltage)

4. Velocity Saturation (short-channel):
   I_D = W × v_sat × C_ox × (V_GS - V_TH)  [for high V_DS]

   Where:
   v_sat = saturation velocity (~10⁷ cm/s for electrons)
```

### 2.3 PMOS Transistor Equations

```
PMOS Transistor Equations:
(All voltages referenced to source, which is at V_DD)

1. Cutoff Region:
   I_D = 0
   When: V_SG < |V_TP|  (or V_GS > V_TP, where V_TP < 0)

2. Linear (Triode) Region:
   I_D = μ_p × C_ox × (W/L) × [(V_SG - |V_TP|) × V_SD - V_SD²/2]

3. Saturation Region:
   I_D = (1/2) × μ_p × C_ox × (W/L) × (V_SG - |V_TP|)² × (1 + λ × V_SD)

Key Differences from NMOS:
- Hole mobility μ_p ≈ 0.4 × μ_n (slower)
- Threshold voltage V_TP < 0 (negative)
- For same W/L, PMOS is ~2.5× weaker than NMOS
```

## 3. Key Parameters

### 3.1 Threshold Voltage (V_TH)

```
Threshold Voltage Components:
V_TH = V_FB + 2Φ_F + γ × √(2Φ_F + V_SB)

Where:
V_FB = Flat-band voltage = Φ_MS - Q_ox/C_ox
Φ_F = Fermi potential = (kT/q) × ln(N_A/n_i)
γ = Body effect coefficient = √(2 × q × ε_si × N_A) / C_ox
V_SB = Source-body voltage
N_A = Substrate doping concentration
ε_si = Permittivity of silicon
n_i = Intrinsic carrier concentration

Typical Values (65nm technology):
- NMOS V_TH0 ≈ 0.3-0.5 V
- PMOS |V_TH0| ≈ 0.3-0.5 V
- Low-V_TH devices: 0.15-0.25 V
- High-V_TH devices: 0.5-0.7 V
```

### 3.2 Body Effect

```
When source-body voltage V_SB ≠ 0:

V_TH = V_TH0 + γ × (√(2Φ_F + V_SB) - √(2Φ_F))

Effect:
- V_TH increases as V_SB increases
- PMOS in n-well: body tied to V_DD, no body effect
- NMOS in p-substrate: body tied to GND, no body effect
- NMOS in n-well: body effect possible

Body Effect Coefficient γ:
- Typical: 0.3-0.5 V^(1/2)
- Higher doping → higher γ → stronger body effect

Impact on Circuit:
- Increases V_TH of series NMOS transistors
- Reduces current drive in stacked configurations
- Important for pass-transistor logic
```

### 3.3 Channel Length Modulation

```
Effect of V_DS on current in saturation:

I_D = I_D(sat) × (1 + λ × V_DS)

λ = Channel Length Modulation Parameter
λ ≈ 1/L (approximately inversely proportional to channel length)

Typical Values:
- Long channel (L > 1 μm): λ ≈ 0.01-0.1 V⁻¹
- Short channel (L < 0.1 μm): λ ≈ 0.1-1 V⁻¹

Impact:
- Reduces output resistance: r_o = 1/(λ × I_D)
- Affects analog circuit gain: A_v = -g_m × r_o
- Important for current mirrors and amplifiers
```

### 3.4 Subthreshold Conduction

```
Below threshold (V_GS < V_TH), small current flows:

I_sub = I_0 × exp((V_GS - V_TH)/(n × V_T)) × (1 - exp(-V_DS/V_T))

Where:
I_0 = Reference current (technology dependent)
n = Subthreshold swing coefficient (1 < n < 2)
V_T = Thermal voltage = kT/q ≈ 26 mV at 300K

Subthreshold Swing (SS):
SS = n × V_T × ln(10) ≈ 60-120 mV/decade at room temperature

Impact on Digital Circuits:
- Leakage current in OFF state
- Increases with temperature
- Dominant leakage mechanism in older technologies
- Limits minimum operating voltage

Leakage Power:
P_leak = V_DD × I_leak
I_leak = I_sub (V_GS = 0)
```

## 4. Device Parameters

### 4.1 Transconductance (g_m)

```
Transconductance: Measure of how effectively gate voltage controls drain current

Linear Region:
g_m = ∂I_D/∂V_GS = μ_n × C_ox × (W/L) × V_DS

Saturation Region:
g_m = ∂I_D/∂V_GS = μ_n × C_ox × (W/L) × (V_GS - V_TH)
    = √(2 × μ_n × C_ox × (W/L) × I_D)
    = 2 × I_D / (V_GS - V_TH)

Units: A/V or Siemens (S)

Typical Values (65nm):
- Minimum size NMOS: g_m ≈ 0.5-1 mA/V
- Typical NMOS: g_m ≈ 5-10 mA/V

Importance:
- Determines amplifier gain: A_v = g_m × R_out
- Higher g_m → faster switching
- Higher g_m → more current for same voltage
```

### 4.2 Output Resistance (r_o)

```
Output Resistance: Resistance looking into drain

r_o = 1/(∂I_D/∂V_DS) = 1/(λ × I_D)

Or equivalently:
r_o = V_A / I_D

Where:
V_A = Early voltage = 1/λ

Typical Values:
- V_A ≈ 10-50 V (depends on channel length)
- Longer channel → higher V_A → higher r_o
- r_o ≈ 10-100 kΩ for typical currents

Importance:
- Determines amplifier output resistance
- Affects cascode gain: A_v = g_m × r_o²
- Limits precision of current mirrors
```

### 4.3 Gate Capacitance

```
Total Gate Capacitance:
C_g = C_ox × W × L + C_fringe

Where:
C_ox = ε_ox / t_ox = ε₀ × κ_SiO₂ / t_ox
ε₀ = 8.854 × 10⁻¹⁴ F/cm
κ_SiO₂ = 3.9 (dielectric constant of SiO₂)
t_ox = Gate oxide thickness

For 65nm technology:
t_ox ≈ 1.2 nm (SiO₂)
C_ox ≈ 28.5 fF/μm²

Gate Capacitance Components:
C_g = C_gs + C_gd + C_gb

In digital operation:
C_load ≈ C_g + C_wire + C_diffusion

Impact on Speed:
τ = R_on × C_load
f_max = 1/(2π × R_on × C_load)
```

### 4.4 Device Parameters Table

| Parameter | Symbol | NMOS | PMOS | Units |
|-----------|--------|------|------|-------|
| Threshold Voltage | V_TH | 0.4 | -0.4 | V |
| Transconductance | g_m | 1.0 | 0.4 | mA/V |
| Output Resistance | r_o | 50 | 50 | kΩ |
| Gate Capacitance | C_g | 1.0 | 1.0 | fF/μm |
| Drain Capacitance | C_d | 0.5 | 0.5 | fF/μm |
| Mobility | μ | 400 | 150 | cm²/V·s |
| Subthreshold Swing | SS | 80 | 80 | mV/dec |

## 5. Transistor Sizing

### 5.1 Sizing for Equal Rise/Fall Times

```
PMOS/NMOS Ratio:
For equal rise and fall times (symmetric switching):

μ_n × (W/L)_n = μ_p × (W/L)_p

Since μ_n ≈ 2.5-3 × μ_p:
(W/L)_p ≈ 2.5-3 × (W/L)_n

Example:
If (W/L)_n = 1 (minimum size)
Then (W/L)_p = 2.5-3 (PMOS 2.5-3× wider)

Area Penalty:
- Larger PMOS → more gate capacitance
- More diffusion capacitance
- Increases dynamic power

Trade-off:
- For speed: Use equal drive strength
- For area/power: Use minimum PMOS, accept asymmetric timing
```

### 5.2 Fanout and Delay

```
Logical Effort Method:

Delay = g × h + p

Where:
g = Logical effort (technology-dependent)
h = Electrical effort = C_out/C_in
p = Parasitic delay

For a CMOS inverter:
g = 1 (reference)
p ≈ 1 (parasitic delay)

For a 2-input NAND:
g = 4/3 (worse than inverter)
p ≈ 2 (more diffusion capacitance)

For a 2-input NOR:
g = 5/3 (worst of common gates)
p ≈ 2

Minimum Delay Stage:
h = √(p/g) (optimal fanout)
Stage delay = 2√(p × g)
```

### 5.3 Wire Loading

```
Wire Capacitance Model:
C_wire = C_ground + C_coupling

C_ground = ε × W × L / t_oxide
C_coupling = ε × L × t / s

Where:
W = Wire width
L = Wire length
t = Wire thickness
s = Wire spacing
ε = Permittivity of interlayer dielectric

Wire Resistance:
R_wire = ρ × L / (W × t)

RC Delay:
τ_wire = R_wire × C_wire / 2 (Elmore delay)

Scaling Impact:
- As technology shrinks, wire resistance increases
- Wire capacitance coupling becomes dominant
- Wire delay can dominate gate delay
```

## 6. Short-Channel Effects

### 6.1 Velocity Saturation

```
At high electric fields, carrier velocity saturates:

v = μ × E / (1 + E/E_sat)

Where:
E = Electric field = V_DS / L
E_sat = Saturation electric field ≈ 1-3 × 10⁴ V/cm

Impact on Current:
Long channel: I_D ∝ (V_GS - V_TH)²
Short channel: I_D ∝ (V_GS - V_TH) (linear dependence)

This reduces the advantage of reducing V_TH for speed
```

### 6.2 Drain-Induced Barrier Lowering (DIBL)

```
As V_DS increases, V_TH decreases:

V_TH = V_TH0 - η × V_DS

Where:
DIBL coefficient η ≈ 0.05-0.15 V/V

Impact:
- Increases OFF-state leakage current
- Reduces output resistance
- Makes V_DS-dependent threshold voltage
- Worsens in shorter channel devices

Mitigation:
- Higher doping concentration
- Retrograde well profiles
- Halo/pocket implants
```

### 6.3 Hot Carrier Injection

```
High-energy carriers near drain can inject into gate oxide:

Effects:
- Threshold voltage shift over time
- Transconductance degradation
- Device reliability concerns

Mechanism:
1. High V_DS creates high electric field near drain
2. Carriers gain energy (become "hot")
3. Some carriers have enough energy to overcome Si-SiO₂ barrier
4. Injected into gate oxide, creating trapped charge

Hot Carrier Lifetime:
τ_HC ∝ exp(V_D/ΔV_D)

Mitigation:
- LDD (Lightly Doped Drain) structures
- Lower supply voltage
- Optimized doping profiles
```

### 6.4 Gate Tunneling

```
As oxide thickness decreases, direct tunneling becomes significant:

Tunnel current density:
J = A × (V/T_ox)² × exp(-B × T_ox/V)

Where:
A, B = Constants depending on barrier height
T_ox = Oxide thickness

Impact:
- Gate leakage increases exponentially with thinner oxides
- Significant for T_ox < 2 nm
- Limits minimum oxide thickness

Mitigation:
- High-κ dielectrics (HfO₂, ZrO₂)
- κ ≈ 20-30 vs κ_SiO₂ = 3.9
- Equivalent oxide thickness (EOT) = T_ox × κ_SiO₂/κ_high-κ
```

## 7. Temperature Effects

### 7.1 Mobility Variation

```
Mobility decreases with temperature:

μ(T) = μ(T₀) × (T₀/T)^α

Where:
α ≈ 1.5-2.0
T₀ = Reference temperature (300K)

Impact:
- Higher temperature → lower mobility → slower switching
- PMOS more affected than NMOS
- Reduces drive current at high temperature

Example:
At T = 350K (77°C):
μ(350) ≈ μ(300) × (300/350)^1.5 ≈ 0.78 × μ(300)
22% reduction in mobility!
```

### 7.2 Threshold Voltage Variation

```
Threshold voltage decreases with temperature:

V_TH(T) = V_TH(T₀) - α_VTH × (T - T₀)

Where:
α_VTH ≈ 0.5-1.5 mV/°C

Impact:
- Higher temperature → lower V_TH → more leakage
- Increases OFF-state current exponentially
- Can cause thermal runaway in worst case

Temperature Coefficient:
TC = ∂V_TH/∂T ≈ -1 mV/°C (typical)

At T = 350K (77°C):
V_TH(350) ≈ V_TH(300) - 50 mV
```

### 7.3 Temperature Effects on Circuit

```
Temperature Impact Summary:

Parameter     | Temperature Effect | Circuit Impact
-------------|-------------------|---------------
Mobility      | Decreases ↑T      | Slower switching
Threshold V   | Decreases ↑T      | More leakage
Leakage       | Increases ↑T      | More static power
Resistance    | Increases ↑T      | Slower RC delay
Carrier V     | Decreases ↑T      | Reduced current

Operating Range for Implants:
- Body temperature: 37°C (310K)
- Maximum implant temp: 41°C (314K)
- Very narrow range, minimal temperature effects

For external electronics:
- Commercial: 0-70°C
- Industrial: -40-85°C
- Military: -55-125°C
```

## 8. Process Variation

### 8.1 Types of Variation

```
Sources of Process Variation:

1. Global (Die-to-Die) Variation:
   - Affects all transistors on a die similarly
   - Caused by wafer-level processing variations
   - Example: V_TH ± 50 mV across wafer

2. Local (Within-Die) Variation:
   - Affects individual transistors differently
   - Caused by random dopant fluctuation (RDF)
   - Example: V_TH ± 20 mV between adjacent transistors

3. Systematic Variation:
   - Pattern-dependent effects
   - Lithography proximity effects
   - Etch loading effects

4. Random Variation:
   - Truly random, unpredictable
   - Follows Gaussian distribution
   - Dominant source in advanced nodes
```

### 8.2 Variation Modeling

```
Statistical Modeling:

For a parameter X with mean μ_X and std dev σ_X:

X = μ_X + ΔX_global + ΔX_local

Where:
ΔX_global ~ N(0, σ_global²)
ΔX_local ~ N(0, σ_local²)

Typical Variations (65nm):
- V_TH: μ = 0.4V, σ = 20-50 mV
- L_eff: μ = 60nm, σ = 5-10 nm
- W_eff: μ = 120nm, σ = 5-10 nm
- T_ox: μ = 1.2nm, σ = 0.05-0.1 nm

Monte Carlo Simulation:
- Run 1000+ simulations with random parameter variations
- Characterize yield, performance spread
- Identify critical parameters
```

### 8.3 Yield Analysis

```
Yield = Probability that circuit meets specifications

Factors affecting yield:
1. Parametric yield: Performance within specs
2. Defect yield: No manufacturing defects
3. Functional yield: Correct operation

Parametric Yield Calculation:
Y = Φ((X_spec - μ_X) / σ_X)

Where:
Φ = Cumulative normal distribution function
X_spec = Specification limit
μ_X = Mean performance
σ_X = Standard deviation

Example:
If delay spec = 2 ns, μ = 1.8 ns, σ = 0.1 ns:
Y = Φ((2.0 - 1.8) / 0.1) = Φ(2.0) ≈ 97.7%

To achieve 99.9% yield:
Need spec ≥ μ + 3.29σ = 1.8 + 0.329 = 2.13 ns
```

## 9. Advanced Transistor Structures

### 9.1 FinFET

```
FinFET Structure:
- 3D transistor with fin-shaped channel
- Gate wraps around channel on 3 sides
- Better electrostatic control
- Reduced short-channel effects

Cross-Section:
    Gate
   / | \
  /  |  \
┌────┐
│Fin │
└────┘
  Source Drain

Advantages:
- Better subthreshold swing (steeper)
- Reduced DIBL
- Lower V_TH variation
- Improved performance at low voltage

FinFET Parameters (16nm):
- Fin width: 7-10 nm
- Fin height: 30-40 nm
- Gate length: 7-10 nm
- Equivalent gate oxide: 0.7-1.0 nm
```

### 9.2 Gate-All-Around (GAA)

```
GAA Structure:
- Gate completely surrounds channel
- Best electrostatic control
- Ultimate scaling potential

Types:
1. Nanowire FET: Circular channel
2. Nanosheet FET: Rectangular channel
3. Forksheet FET: n/p separation

Advantages:
- Excellent V_TH control
- Reduced leakage
- Higher drive current per area
- Better scalability than FinFET

Technology Roadmap:
- 3nm: GAA introduction
- 2nm: Full GAA transition
- Sub-2nm: Complementary FET (CFET)
```

### 9.3 Transistor Evolution

| Generation | Year | Gate Length | Structure | V_DD |
|------------|------|------------|-----------|------|
| 1μm | 1985 | 1 μm | Planar | 5V |
| 0.5μm | 1990 | 0.5 μm | Planar | 5V |
| 0.35μm | 1995 | 0.35 μm | Planar | 3.3V |
| 0.18μm | 1999 | 0.18 μm | Planar | 1.8V |
| 0.13μm | 2001 | 0.13 μm | Planar | 1.2V |
| 65nm | 2006 | 65 nm | Planar | 1.2V |
| 45nm | 2008 | 45 nm | Planar | 1.1V |
| 28nm | 2011 | 28 nm | Planar | 0.9V |
| 16nm | 2014 | 16 nm | FinFET | 0.8V |
| 10nm | 2017 | 10 nm | FinFET | 0.7V |
| 7nm | 2018 | 7 nm | FinFET | 0.7V |
| 5nm | 2020 | 5 nm | FinFET | 0.65V |
| 3nm | 2022 | 3 nm | GAA | 0.6V |

## 10. CMOS Inverter Analysis

### 10.1 Voltage Transfer Characteristic

```
CMOS Inverter:
PMOS connected to V_DD
NMOS connected to GND
Gates tied together (input)
Drains tied together (output)

VTC Curve:
V_out
  │
V_DD ──────────────┐
  │                │
  │                │
V_M ───────────────┼─── Threshold
  │                │
  │                │
  └────────────────┘──── V_in
  0                V_DD

Key Points:
- V_M = Switching threshold (V_in = V_out)
- At V_M: I_DN = I_DP (equal currents)
- Sharp transition indicates good noise margins
```

### 10.2 Noise Margins

```
Noise Margin Definitions:
NM_H (High-level noise margin) = V_OH - V_IH
NM_L (Low-level noise margin) = V_IL - V_OL

Where:
V_OH = Output high voltage = V_DD
V_OL = Output low voltage = 0
V_IH = Input high voltage (VTC slope = -1)
V_IL = Input low voltage (VTC slope = -1)

For ideal CMOS inverter:
NM_H = NM_L = V_DD/2

Typical Values (1.2V supply):
V_OH = 1.2 V
V_OL = 0 V
V_IH ≈ 0.72 V
V_IL ≈ 0.48 V

NM_H = 1.2 - 0.72 = 0.48 V
NM_L = 0.48 - 0 = 0.48 V
```

## 11. Applications in Medical Implant Design

### 11.1 Ultra-Low-Voltage Operation

```
For implantable devices, minimizing voltage is critical:

Power Savings: P ∝ V²
Halving voltage → 75% power reduction!

Challenges at Low Voltage:
1. Reduced noise margins
2. Increased delay
3. Increased sensitivity to V_TH variation
4. Reduced signal-to-noise ratio

Solutions:
- Use low-V_TH transistors (more leakage)
- Adaptive body biasing
- Multi-threshold design
- Near-threshold computing

Near-Threshold Operation:
V_DD ≈ V_TH + 100-200 mV
- Optimal energy efficiency
- 5-10× energy reduction
- 3-5× slower operation
```

### 11.2 Reliability Considerations

```
Implant Reliability Requirements:
- Lifetime: 10-20 years
- Failure rate: < 10⁻⁶ FIT (Failures In Time)
- No field repair possible

Key Reliability Mechanisms:
1. Hot Carrier Injection (HCI)
   - Threshold voltage shift over time
   - Mitigation: operate at reduced voltage

2. Negative Bias Temperature Instability (NBTI)
   - PMOS V_TH increases over time
   - Mitigation: AC operation, voltage guardbands

3. Time-Dependent Dielectric Breakdown (TDDB)
   - Oxide breakdown over time
   - Mitigation: thicker oxides, lower voltage

4. Electromigration
   - Metal atom movement in wires
   - Mitigation: current density limits, wider wires

Reliability Guardbands:
- Add 10-20% margin to critical parameters
- Use worst-case models for design
- Periodic self-test and calibration
```

## 12. Summary

| Parameter | Symbol | Typical Value (65nm) | Importance |
|-----------|--------|---------------------|------------|
| Threshold Voltage | V_TH | 0.4 V | Leakage, speed |
| Transconductance | g_m | 1 mA/V | Current drive |
| Output Resistance | r_o | 50 kΩ | Gain, matching |
| Gate Capacitance | C_g | 1 fF/μm | Speed, power |
| Mobility | μ_n | 400 cm²/V·s | Current drive |
| Subthreshold Swing | SS | 80 mV/dec | Leakage control |
| Channel Length Mod. | λ | 0.1 V⁻¹ | Output resistance |

## 13. Exercises

1. Calculate the drain current for an NMOS with W/L=2, μ_n=400 cm²/V·s, C_ox=28.5 fF/μm², V_GS=0.8V, V_TH=0.4V, V_DS=0.5V
2. Determine the body effect on V_TH when V_SB=0.5V with γ=0.4 V^(1/2)
3. Calculate the subthreshold leakage at T=37°C for V_GS=0V, SS=80 mV/dec
4. Design a CMOS inverter with equal rise/fall times for μ_n/μ_p=2.5
5. Analyze the impact of 10% V_TH variation on circuit delay
6. Compare power consumption at V_DD=1.2V vs V_DD=0.6V for the same circuit
7. Calculate the gate tunneling current for T_ox=1.2nm at V_DD=1.2V
8. Design a low-power implant circuit using near-threshold computing principles
