# Sub-Threshold Operation for Implantable Pacemaker ASICs

## 1. Introduction to Sub-Threshold Operation

Sub-threshold operation in CMOS circuits involves operating transistors with gate-to-source voltages below the threshold voltage, where the drain current is dominated by diffusion rather than drift. This operating regime provides the lowest possible power consumption for digital circuits, making it essential for always-on functions in the iPACE-CHIP pacemaker ASIC. While sub-threshold circuits are significantly slower than their strong-inversion counterparts, they achieve energy efficiency levels that are impossible to reach in normal operation.

For the iPACE-CHIP pacemaker requiring 10-year battery life, sub-threshold operation enables housekeeping functions, wake-up detectors, and monitoring circuits to operate continuously with femtowatt-level power consumption. This chapter explores the theory, design, and implementation of sub-threshold circuits for implantable medical devices.

## 2. Sub-Threshold Physics

### 2.1 Current-Voltage Relationship

```
Sub-Threshold Drain Current:

In the sub-threshold region (V_GS < V_th), the drain current
is governed by diffusion rather than drift:

I_D = I_0 × exp(V_GS / (n × V_T)) × (1 - exp(-V_DS / V_T))

Where:
- I_0 = process-dependent parameter
  I_0 = μ × C_ox × (W/L) × (n-1) × V_T²
- μ = carrier mobility
- C_ox = gate oxide capacitance
- n = body effect coefficient (1.2 to 2.0)
- V_T = thermal voltage = kT/q ≈ 26 mV at 300K

For iPACE-CHIP 180nm process:
- μ_n = 400 cm²/V·s (electron mobility)
- C_ox = 8.6 fF/μm²
- n = 1.5
- V_T = 26 mV at 37°C

At V_GS = 0.3V (below V_th = 0.4V):
I_D = I_0 × exp(0.3 / (1.5 × 0.026)) = I_0 × exp(7.7)
I_D = I_0 × 2200

The exponential relationship means small voltage changes
produce large current changes.
```

### 2.2 Sub-Threshold Swing

```
Sub-Threshold Swing (SS):

Definition: Gate voltage change required for 10× change in
drain current.

SS = dV_GS / d(log₁₀(I_D)) = n × V_T × ln(10)

For iPACE-CHIP:
SS = 1.5 × 26 mV × 2.303 = 90 mV/decade

Implications:
- 90 mV increase in V_GS → 10× increase in I_D
- 180 mV increase → 100× increase in I_D
- 270 mV increase → 1000× increase in I_D

Comparison with strong inversion:
- Strong inversion: I ∝ (V_GS - V_th)² (quadratic)
- Sub-threshold: I ∝ exp(V_GS / (n × V_T)) (exponential)

The exponential relationship makes sub-threshold circuits
extremely sensitive to voltage variations.
```

### 2.3 Speed Limitations

```
Sub-Threshold Circuit Speed:

Propagation delay of a sub-threshold inverter:

t_p = (C_L × V_DD) / I_D

Where:
- C_L = load capacitance (1 fF typical)
- V_DD = supply voltage (0.5V)
- I_D = sub-threshold current

At V_DD = 0.5V:
I_D ≈ 10 nA (for W/L = 1 μm / 0.18 μm)

t_p = (1 fF × 0.5V) / 10 nA = 50 ns

Maximum frequency:
f_max = 1 / (2 × t_p) = 10 MHz (theoretical)

In practice, for complex logic:
- Critical path delay: 200-500 ns
- Maximum frequency: 1-5 MHz
- For iPACE-CHIP housekeeping: 32-100 kHz (adequate)

Speed Comparison:
┌──────────────────┬──────────┬──────────┬──────────────┐
│ Operating Point  │ V_DD     │ f_max    │ Speed Ratio  │
├──────────────────┼──────────┼──────────┼──────────────┤
│ Strong inversion │ 1.8V     │ 500 MHz  │ 1×           │
│ Moderate inv.    │ 1.0V     │ 50 MHz   │ 0.1×         │
│ Sub-threshold    │ 0.5V     │ 5 MHz    │ 0.01×        │
│ Deep sub-thresh. │ 0.3V     │ 100 kHz  │ 0.0002×      │
└──────────────────┴──────────┴──────────┴──────────────┘
```

## 3. Sub-Threshold Logic Design

### 3.1 Static CMOS in Sub-Threshold

```
Static CMOS Inverter in Sub-Threshold:

                    V_DD (0.5V)
                        │
                   ┌────┴────┐
                   │  PMOS   │
                   │  M1     │
                   │  W/L =  │
                   │  0.5/0.18│
                   └────┬────┘
                        │
IN ─────────────────────┤──────────────── OUT
(0V to 0.5V)           │                 (0V to 0.5V)
                   ┌────┴────┐
                   │  NMOS   │
                   │  M2     │
                   │  W/L =  │
                   │  0.36/0.18│
                   └────┬────┘
                        │
                   GND (0V)

Operating Point:
- V_IL = 0.20V (input low threshold)
- V_IH = 0.30V (input high threshold)
- V_OL = 0.05V (output low)
- V_OH = 0.45V (output high)
- Noise margin: 100 mV (NM_L) and 150 mV (NM_H)

Note: Reduced noise margins compared to strong inversion.
Requires careful design for adequate noise immunity.
```

### 3.2 Sub-Threshold NAND2 Gate

```
Sub-Threshold NAND2 Gate:

                    V_DD (0.5V)
                        │
                   ┌────┴────┐
                   │  PMOS   │
                   │  M1     │
                   │  (A)    │
                   └────┬────┘
                        │
                   ┌────┴────┐
                   │  PMOS   │
                   │  M2     │
                   │  (B)    │
                   └────┬────┘
                        │
A ──────────────────────┤
B ──────────────────────┼──────────────── OUT
                        │
                   ┌────┴────┐
                   │  NMOS   │
                   │  M3     │
                   │  (A)    │
                   └────┬────┘
                        │
                   ┌────┴────┐
                   │  NMOS   │
                   │  M4     │
                   │  (B)    │
                   └────┬────┘
                        │
                   GND (0V)

Truth Table:
A │ B │ OUT
──┼───┼────
0 │ 0 │ 1
0 │ 1 │ 1
1 │ 0 │ 1
1 │ 1 │ 0

Sub-Threshold Behavior:
- When A=0, B=0: Both PMOS ON, both NMOS OFF → OUT = V_DD
- When A=1, B=1: Both PMOS OFF, both NMOS ON → OUT = 0
- Mixed inputs: Partial conduction, intermediate output
- Propagation delay: 100 ns (typical at 0.5V)
```

### 3.3 Sub-Threshold Flip-Flop

```
Sub-Threshold D Flip-Flop:

Implementation: Transmission gate master-slave

                    V_DD (0.5V)
                        │
         ┌──────────────┼──────────────┐
         │              │              │
    ┌────┴────┐    ┌────┴────┐    ┌────┴────┐
    │ Master  │    │ Slave   │    │ Output  │
    │ Latch   │───►│ Latch   │───►│ Buffer  │
    └────┬────┘    └────┬────┘    └────┬────┘
         │              │              │
    CLK ─┴──────────────┴──────────────┘
         │
    D ───┘

Master Latch (CLK high = transparent):
┌─────────────────────────────────────────────────────────┐
│ Transmission gate + cross-coupled inverters              │
│                                                         │
│  D ──── TG1 ────┬──── Q_m                              │
│                  │                                      │
│             ┌────┴────┐                                 │
│             │ Cross-  │                                 │
│             │ coupled │                                 │
│             │ inv.    │                                 │
│             └─────────┘                                 │
│                                                         │
│  TG1: Controlled by CLK                                │
│  When CLK=1: D passes to Q_m                           │
│  When CLK=0: Q_m held by feedback                      │
└─────────────────────────────────────────────────────────┘

Specifications at 0.5V:
- Setup time: 25 ns
- Hold time: 5 ns
- Clock-to-Q: 60 ns
- Power: 0.5 fW at 32 kHz
- Area: 4.8 μm × 3.6 μm = 17.28 μm²
```

## 4. Sub-Threshold Memory

### 4.1 Sub-Threshold SRAM

```
Sub-Threshold SRAM Cell:

6T SRAM cell adapted for sub-threshold operation:

                    V_DD (0.5V)
                        │
                   ┌────┴────┐
                   │  PMOS   │
                   │  M1     │
                   └────┬────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   ┌────┴────┐     ┌────┴────┐     ┌────┴────┐
   │  NMOS   │     │  NMOS   │     │  NMOS   │
   │  M2     │     │  M3     │     │  M4     │
   │(access) │     │(access) │     │(access) │
   └────┬────┘     └────┬────┘     └────┬────┘
        │               │               │
   WL ──┤               │               ├── WL
        │               │               │
        └───────────────┼───────────────┘
                        │
                   GND (0V)

Sub-Threshold SRAM Challenges:
1. Reduced read current (slow read)
2. Reduced write margin (hard to flip state)
3. Increased sensitivity to V_th variation
4. Higher leakage relative to read current

Solutions:
- Increase transistor sizes (W/L)
- Use 8T or 10T SRAM cells (separate read port)
- Apply body biasing to improve margins
- Use error correction codes (ECC)
```

### 4.2 Sub-Threshold Register File

```
Sub-Threshold Register File Design:

For iPACE-CHIP housekeeping:

Specifications:
- 32 registers × 8 bits = 256 bits
- Read/Write frequency: 32 Hz
- Access time: 1 μs (adequate for 32 Hz)
- Power: 10 fW (active), 50 fW (retention)

Architecture:
┌─────────────────────────────────────────────────────────┐
│ 32×8 Register File (Sub-Threshold)                      │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  256 Retention Flip-Flops (V_DD = 0.5V)          │  │
│  │  - Cross-coupled inverter pairs                  │  │
│  │  - Write gates for state update                  │  │
│  │  - Read buffers (tri-state)                      │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  5-bit Address Decoder                           │  │
│  │  - 32 word lines                                 │  │
│  │  - Dynamic logic (precharge-evaluate)            │  │
│  │  - Propagation delay: 200 ns                     │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Read/Write Control                              │  │
│  │  - Read enable, write enable                     │  │
│  │  - Data input/output multiplexers                │  │
│  │  - Propagation delay: 150 ns                     │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  Performance at 0.5V, 37°C:                             │
│  - Read access time: 350 ns                             │
│  - Write access time: 200 ns                            │
│  - Active power: 10 fW at 32 Hz                        │
│  - Retention power: 50 fW                               │
│  - Area: 0.01 mm²                                       │
└─────────────────────────────────────────────────────────┘
```

## 5. Sub-Threshold Analog Circuits

### 5.1 Sub-Threshold Comparator

```
Sub-Threshold Comparator:

For always-on cardiac activity detection:

Architecture: Simple differential pair comparator

                    V_DD (0.5V)
                        │
                   ┌────┴────┐
                   │  PMOS   │
                   │  M1     │
                   │  (bias) │
                   └────┬────┘
                        │
              ┌─────────┼─────────┐
              │                   │
         ┌────┴────┐         ┌────┴────┐
         │  NMOS   │         │  NMOS   │
         │  M2     │         │  M3     │
         │  (+)    │         │  (-)    │
         └────┬────┘         └────┬────┘
              │                   │
V_in+ ────────┤                   ├──────── V_ref
              │                   │
              └─────────┬─────────┘
                        │
                   ┌────┴────┐
                   │ Output  │
                   │ Stage   │
                   └────┬────┘
                        │
                   OUT (0 to 0.5V)

Specifications at 0.5V:
- Input range: 0.1V to 0.4V
- Offset: < 10 mV
- Response time: 1 μs
- Power: 1 fW
- Gain: 20 V/V
- CMRR: 60 dB
```

### 5.2 Sub-Threshold Bandgap Reference

```
Sub-Threshold Bandgap Reference:

For ultra-low-voltage reference generation:

Architecture: Sub-threshold bandgap with current-mode output

                    V_DD (0.5V)
                        │
                   ┌────┴────┐
                   │  PMOS   │
                   │  M1     │
                   │  (cascode)│
                   └────┬────┘
                        │
                   ┌────┴────┐
                   │  PMOS   │
                   │  M2     │
                   │  (mirror)│
                   └────┬────┘
                        │
              ┌─────────┼─────────┐
              │                   │
         ┌────┴────┐         ┌────┴────┐
         │  Diode  │         │  Resistor│
         │  D1     │         │  R1      │
         │  (PTAT) │         │  (CTAT)  │
         └────┬────┘         └────┬────┘
              │                   │
              └─────────┬─────────┘
                        │
                   ┌────┴────┐
                   │ Output  │
                   │ Buffer  │
                   └────┬────┘
                        │
                   V_ref (0.25V)

Specifications at 0.5V:
- Output voltage: 250 mV ± 1%
- Temperature coefficient: 50 ppm/°C
- Line regulation: 1%/V
- Power: 0.5 fW
- Load regulation: 0.1%/μA
- Start-up time: 10 μs
```

## 6. Sub-Threshold Design Challenges

### 6.1 Process Variation Sensitivity

```
Process Variation Impact:

In sub-threshold, current varies exponentially with V_th:
ΔI/I = ΔV_th / (n × V_T)

For iPACE-CHIP:
- n = 1.5
- V_T = 26 mV
- σ_V_th = 40 mV (typical for 180nm)

Current variation:
σ_I/I = 40 / (1.5 × 26) = 102%

This means 68% of chips will have current within ±102%
of nominal, and 95% within ±204%.

Impact on circuit operation:
- Delay variation: ±100%
- Power variation: ±100%
- Frequency variation: ±100%

Mitigation Strategies:
1. Design for worst-case (slow corner)
2. Use adaptive body biasing
3. Implement on-chip calibration
4. Use redundancy for critical functions
```

### 6.2 Noise Sensitivity

```
Noise Analysis in Sub-Threshold:

Sub-threshold circuits have reduced noise margins:

At V_DD = 0.5V:
- Logic swing: 0.45V (0.05V to 0.5V)
- Noise margin (low): 100 mV
- Noise margin (high): 150 mV

Noise sources:
1. Power supply noise: < 50 mV (filtered by decap)
2. Substrate noise: < 20 mV (guard rings)
3. Crosstalk: < 10 mV (shielding)
4. Thermal noise: < 5 mV (negligible)

Total noise: ~55 mV
Noise margin: 100 mV (adequate with 45 mV margin)

Design Rules for Sub-Threshold:
- Minimum wire spacing: 2× normal
- Guard rings around all sub-threshold blocks
- Separate power supply with filtering
- Decoupling capacitance: 2× normal
```

### 6.3 Temperature Effects

```
Temperature Effects on Sub-Threshold:

Temperature affects sub-threshold circuits through:
1. V_th temperature coefficient: -1 mV/°C
2. V_T temperature coefficient: +0.087 mV/°C
3. Mobility temperature coefficient: -0.5%/°C

Net effect on current:
dI/dT = I × (-dV_th/dT + dV_T/dT) / (n × V_T)

At 0.5V V_DD:
- V_th at -20°C: 0.44V
- V_th at 37°C: 0.38V
- V_th at 50°C: 0.37V

Current variation:
- At -20°C: 0.3× nominal
- At 37°C: 1.5× nominal
- At 50°C: 2.5× nominal

Design Implications:
- Must verify at -20°C (slowest corner)
- At -20°C, circuits are 3× slower
- Solution: Reduce frequency or apply FBB at low temperature
```

## 7. Summary

Sub-threshold operation in the iPACE-CHIP pacemaker ASIC enables always-on functions to operate with femtowatt-level power consumption, essential for the 10-year battery life requirement. The exponential current-voltage relationship provides maximum energy efficiency at supply voltages around 0.3-0.5V, with energy per operation as low as 5 fJ. The primary challenges are reduced speed (100× slower than strong inversion), high sensitivity to process variation (±100% current variation), and reduced noise margins. These challenges are addressed through worst-case design, adaptive body biasing, redundancy, and careful physical design. Sub-threshold circuits are limited to non-time-critical functions: housekeeping, monitoring, wake-up detection, and always-on timers, where their ultra-low power consumption justifies the performance limitations.

## References

1. Calhoun, B., et al., "Modeling and Sizing for Minimum Energy Operation in Sub-Threshold," IEEE JSSC, 2004.
2. iPACE-CHIP Project Internal Documentation: Sub-Threshold Design Guide, Rev 1.3.
3. Wang, A., et al., "Design of Ultra-Low-Voltage Circuits," IEEE JSSC, 2005.
4. Hanson, S., et al., "Ultralow-Voltage, Minimum-Energy CMOS," IBM Journal, 2006.
5. TSMC 0.18μm Mixed-Signal Process Design Manual: Sub-Threshold Characterization.
