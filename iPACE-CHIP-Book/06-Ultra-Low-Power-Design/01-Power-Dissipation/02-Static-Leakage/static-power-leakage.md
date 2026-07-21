# Static Power Leakage in Implantable Pacemaker ASICs

## 1. Introduction to Static Power

Static power consumption, also known as leakage power, represents the energy dissipated by transistors when they are not actively switching. In modern CMOS processes, static power has become an increasingly significant portion of total power consumption, particularly for always-on circuits in implantable medical devices like the iPACE-CHIP pacemaker.

Unlike dynamic power, which is proportional to switching activity and can be reduced through clock gating or activity reduction, static power persists as long as the circuit is powered. For a pacemaker requiring 10-year battery life, even nanoamps of continuous leakage current translate to significant energy drain over the device lifetime.

## 2. Sources of Leakage Current

### 2.1 Subthreshold Leakage

Subthreshold leakage is the dominant leakage mechanism in modern CMOS processes:

```
Subthreshold Current Equation:

I_sub = I_0 × exp((V_GS - V_th) / (n × V_T)) × (1 - exp(-V_DS / V_T))

Where:
- I_0 = process-dependent reference current
- V_GS = gate-to-source voltage
- V_th = threshold voltage
- n = subthreshold swing factor (1.0 to 2.5)
- V_T = thermal voltage (kT/q ≈ 26 mV at 300K)
- V_DS = drain-to-source voltage

Key Parameters:
- V_T ≈ 26 mV at 37°C (body temperature)
- Subthreshold swing: S = n × V_T × ln(10) ≈ 60-150 mV/decade
- Lower S = sharper turn-off = less leakage
```

### 2.2 Gate Oxide Tunneling

Direct tunneling through thin gate oxides:

```
Gate Leakage Current:

I_gate = A_gate × (V_DD / t_ox)² × exp(-B × t_ox / V_DD)

Where:
- A_gate = area-dependent coefficient
- t_ox = gate oxide thickness
- B = material-dependent constant

For iPACE-CHIP 180nm process:
- t_ox = 4.0 nm (thin oxide)
- I_gate ≈ 1-10 nA/cm² at 1.8V
- Significant for large gate areas
```

### 2.3 Junction Leakage

Reverse-biased pn junction leakage:

```
Junction Leakage Components:

I_junction = I_generation + I_band_to_band_tunneling

I_generation = (q × n_i × A_j) / τ_gen

Where:
- n_i = intrinsic carrier concentration
- A_j = junction area
- τ_gen = generation lifetime

Temperature Dependence:
- Doubles approximately every 8-10°C increase
- Critical at body temperature (37°C)
```

### 2.4 GIDL (Gate-Induced Drain Leakage)

Gate-induced drain leakage occurs under specific bias conditions:

```
GIDL Current:

I_GIDL = A × (V_DG - V_DGO)² / V_DG × exp(-C × t_ox / V_DG)

Occurs when:
- V_DG > V_DGO (gate-to-drain overlap field)
- Strong band-to-band tunneling at drain junction

Impact: Typically 10-20% of total leakage in standby mode
```

### 2.5 Summary of Leakage Components

```
Leakage Component Breakdown (iPACE-CHIP 180nm):
┌───────────────────────┬────────────┬────────────┐
│ Component             │ Typical    │ % of Total │
├───────────────────────┼────────────┼────────────┤
│ Subthreshold leakage  │ 3.2 nA     │ 55%        │
│ Gate oxide tunneling  │ 1.5 nA     │ 26%        │
│ Junction leakage      │ 0.8 nA     │ 14%        │
│ GIDL                  │ 0.3 nA     │ 5%         │
├───────────────────────┼────────────┼────────────┤
│ TOTAL per gate        │ 5.8 nA     │ 100%       │
└───────────────────────┴────────────┴────────────┘

For iPACE-CHIP total logic (~500K transistors):
Total leakage ≈ 50-100 nA
```

## 3. Temperature Dependence

### 3.1 Leakage Temperature Coefficient

Leakage current has strong temperature dependence:

```
Temperature Coefficient Analysis:

I_leakage(T) = I_leakage(T₀) × exp(α × (T - T₀))

Where:
- T₀ = reference temperature (25°C)
- α = temperature coefficient

Typical values:
- Subthreshold: α ≈ 0.07-0.10 /°C
- Junction: α ≈ 0.08-0.12 /°C
- Gate tunneling: α ≈ -0.01 /°C (weak decrease)

Net effect: Leakage approximately doubles every 10°C
```

### 3.2 Body Temperature Considerations

```
Leakage at Body Temperature (37°C):

Component          │ 25°C     │ 37°C     │ Increase
───────────────────┼──────────┼──────────┼─────────
Subthreshold       │ 1.0 nA   │ 2.5 nA   │ 2.5×
Junction           │ 0.3 nA   │ 0.9 nA   │ 3.0×
Gate tunneling     │ 1.5 nA   │ 1.4 nA   │ 0.9×
GIDL               │ 0.1 nA   │ 0.2 nA   │ 2.0×
───────────────────┼──────────┼──────────┼─────────
TOTAL              │ 2.9 nA   │ 5.0 nA   │ 1.7×

Design Impact: Must design for 37°C operating condition
Power budget must account for ~1.7× increase from 25°C
```

### 3.3 Thermal Runaway Considerations

```
Thermal Stability Analysis:

P_leakage(T) → increases with T → T increases → P_leakage increases

Stability condition: dP_leakage/dT < dP_cooling/dT

For iPACE-CHIP:
- Maximum die temperature: 40°C (limited by tissue interface)
- Thermal resistance: R_th ≈ 50°C/W (implant environment)
- Power dissipation: < 100 μW (maximum)
- Temperature rise: ΔT = P × R_th = 0.1 mW × 50 = 5°C
- Die temperature: 37°C + 5°C = 42°C maximum

Thermal runaway is not a concern for implantable devices
due to body temperature regulation and low power levels.
```

## 4. Process Variation Effects

### 4.1 Threshold Voltage Variation

Threshold voltage variation directly impacts subthreshold leakage:

```
V_th Variation Sources:

1. Random Dopant Fluctuation (RDF):
   σ_Vth_RDF = A_Vth / √(W × L)
   A_Vth ≈ 3-5 mV·μm (process dependent)

2. Line Edge Roughness (LER):
   σ_Vth_LER = B × σ_LER
   B ≈ 20-50 mV/nm

3. oxide Thickness Variation:
   ΔV_th = -Δt_ox × V_th / t_ox

4. Systematic Variations:
   - Across-die variation (pattern density)
   - Across-wafer variation (CMP, etch)
   - Lot-to-lot variation

Total σ_Vth ≈ 30-60 mV (180nm process)
```

### 4.2 Leakage Sensitivity to V_th

```
Subthreshold Leakage vs. V_th:

ΔI_sub / I_sub = ΔV_th / (n × V_T)

For n = 1.5, V_T = 26 mV:
- ΔV_th = 30 mV → ΔI_sub = 77% increase
- ΔV_th = 60 mV → ΔI_sub = 154% increase

Impact: 3σ V_th variation can cause 3-5× leakage variation
Design must account for worst-case leakage scenarios
```

### 4.3 Statistical Leakage Analysis

```
Monte Carlo Leakage Simulation:

Input Parameters:
- V_th: Gaussian, μ = nominal, σ = 40 mV
- L_eff: Gaussian, μ = nominal, σ = 5% of L
- t_ox: Gaussian, μ = nominal, σ = 2%
- Temperature: Uniform, 36°C to 38°C

Results for iPACE-CHIP (500K transistors):
┌───────────┬──────────┬──────────┬──────────┐
│ Percentile│ I_leak   │ P_leak   │ Battery  │
│           │ (nA)     │ (nW)     │ Impact   │
├───────────┼──────────┼──────────┼──────────┤
│ 10th      │ 35       │ 63       │ -25%     │
│ 50th      │ 55       │ 99       │ Nominal  │
│ 90th      │ 85       │ 153      │ +40%     │
│ 99th      │ 120      │ 216      │ +80%     │
└───────────┴──────────┴──────────┴──────────┘

Design Margin: Budget for 99th percentile leakage
```

## 5. Leakage Reduction Techniques

### 5.1 Multi-Threshold Voltage (Multi-Vt)

Using different threshold voltage flavors strategically:

```
Multi-Vt Assignment Strategy:

High-Vt (HVT) Gates:
- V_th ≈ 400 mV (180nm)
- Leakage: 0.1× of standard Vt
- Use for: Non-critical timing paths, always-on logic
- Area penalty: ~5%

Standard-Vt (SVT) Gates:
- V_th ≈ 300 mV (180nm)
- Leakage: 1× (baseline)
- Use for: General logic, moderate timing

Low-Vt (LVT) Gates:
- V_th ≈ 200 mV (180nm)
- Leakage: 10× of standard Vt
- Use for: Critical timing paths only
- Speed improvement: ~15%

Ultra-Low-Vt (ULVT) Gates:
- V_th ≈ 150 mV (180nm)
- Leakage: 50× of standard Vt
- Use for: Extremely critical paths (rare)
- Speed improvement: ~25%

iPACE-CHIP Allocation:
- HVT: 60% of gates (leakage sensitive)
- SVT: 30% of gates (balanced)
- LVT: 10% of gates (timing critical)
```

### 5.2 Power Gating

Completely turning off unused blocks (detailed in Section 03):

```
Power Gating Impact on Leakage:

Without Power Gating:
- Total leakage: 55 nA (always present)

With Power Gating:
- Always-on leakage: 5 nA (always-on blocks)
- Gated leakage: 0 nA (powered off)
- Sleep transistor leakage: 2 nA (overhead)
- Total: 7 nA (87% reduction)

Power Gating Effectiveness:
- Best for: Large blocks used intermittently
- Typical savings: 80-95% of block leakage
- Overhead: Area for power switches, wake-up latency
```

### 5.3 Input Vector Control (IVC)

Setting inputs to minimize leakage during standby:

```
IVC Principle:

Leakage depends on input state:
- Many gates have minimum leakage input combination
- Can reduce total leakage by 20-50%

Optimal Input Patterns:
┌─────────────┬──────────────┬──────────────┐
│ Gate Type    │ Min Leakage  │ Max Leakage  │
│              │ Input        │ Input        │
├─────────────┼──────────────┼──────────────┤
│ NAND2       │ (1,1)        │ (0,0)        │
│ NOR2        │ (0,0)        │ (1,1)        │
│ Inverter    │ 0            │ 1            │
│ AND2        │ (1,1)        │ (0,1)        │
│ OR2         │ (0,0)        │ (1,0)        │
└─────────────┴──────────────┴──────────────┘

Implementation:
- Scan chain input to known state during sleep
- Retention flops hold state while inputs minimized
- Wake-up restores operational inputs
```

### 5.4 Body Biasing

Applying reverse body bias to increase V_th:

```
Reverse Body Bias (RBB) Effect:

V_th(V_BS) = V_th0 + γ × (√(|2φ_F - V_BS|) - √(|2φ_F|))

Where:
- V_th0 = zero-bias threshold voltage
- γ = body effect coefficient
- φ_F = Fermi potential
- V_BS = body-to-source voltage

RBB Application:
- Apply V_BS = -0.5V to -1.5V
- V_th increase: 50-150 mV
- Leakage reduction: 3-10×

Implementation in iPACE-CHIP:
- Separate body contact for each block
- Body bias generator circuit
- Automatic bias adjustment based on mode
```

### 5.5 Summary of Leakage Reduction

```
Technique Comparison:
┌──────────────────────┬────────────┬───────────┬──────────┐
│ Technique            │ Reduction  │ Overhead  │ Area     │
├──────────────────────┼────────────┼───────────┼──────────┤
│ Multi-Vt             │ 3-5×       │ Design    │ 5%       │
│ Power Gating         │ 10-100×    │ Circuit   │ 10-20%   │
│ Input Vector Control │ 1.5-2×     │ Control   │ 2%       │
│ Reverse Body Bias    │ 3-10×      │ Circuit   │ 8%       │
│ Combined Approach    │ 50-200×    │ All       │ 25-35%   │
└──────────────────────┴────────────┴───────────┴──────────┘
```

## 6. Leakage Power Budget

### 6.1 iPACE-CHIP Leakage Budget

```
Leakage Power Budget Allocation:

Total Leakage Budget: 100 nW (37°C, worst-case)

Allocation:
┌─────────────────────────┬──────────┬──────────┐
│ Block                   │ Budget   │ Current  │
├─────────────────────────┼──────────┼──────────┤
│ Always-on oscillator    │ 15 nW    │ 8.3 nA   │
│ Watchdog timer          │ 10 nW    │ 5.6 nA   │
│ Power management unit   │ 10 nW    │ 5.6 nA   │
│ Sensing amplifier (always-on)│ 20 nW│ 11.1 nA │
│ Configuration registers │ 5 nW     │ 2.8 nA   │
│ I/O pads                │ 10 nW    │ 5.6 nA   │
│ Logic (retention)       │ 15 nW    │ 8.3 nA   │
│ Margin                  │ 15 nW    │ 8.3 nA   │
├─────────────────────────┼──────────┼──────────┤
│ TOTAL                   │ 100 nW   │ 55.6 nA  │
└─────────────────────────┴──────────┴──────────┘

Battery Life Impact:
- Battery capacity: 120 mAh = 432,000 mAs
- Leakage energy over 10 years: 100 nW × 3.15×10⁸ s = 31.5 mJ
- Equivalent charge: 31.5 mJ / 3.0V = 10.5 mC = 2.9 μAh
- Percentage of battery: 0.0024%
- Leakage is NOT the dominant battery drain factor
```

### 6.2 Leakage vs. Dynamic Power Ratio

```
Power Ratio Analysis:

Operating Mode     │ Dynamic  │ Static   │ Static/Dynamic
───────────────────┼──────────┼──────────┼───────────────
Deep Sleep         │ ~0 nW    │ 10 nW    │ ∞
Monitoring         │ 420 nW   │ 90 nW    │ 21%
Processing         │ 4.5 μW   │ 500 nW   │ 11%
Stimulation        │ 48 μW    │ 2 μW     │ 4%
Average (typical)  │ 2.5 μW   │ 95 nW    │ 3.8%

Observation:
- Deep sleep: Leakage dominates (100% of power)
- Active modes: Dynamic dominates (>80%)
- Overall average: Leakage is ~4% of total power

Design Priority: Dynamic power reduction has greater impact
on battery life, but leakage cannot be ignored.
```

## 7. Leakage Measurement Techniques

### 7.1 Direct Current Measurement

```
Measurement Setup for Nanoamp Currents:

Equipment:
- Keithley 6221 Current Source (for calibration)
- Keithley 6517A Electrometer (fA resolution)
- Custom test socket with guard rings
- Shielded enclosure
- Temperature-controlled chamber

Measurement Protocol:
1. Calibrate measurement system (short/open/known R)
2. Set temperature to 37°C ± 0.1°C
3. Apply supply voltage (1.8V ± 1 mV)
4. Allow 100 ms settling time
5. Average 1000 readings (1 second window)
6. Repeat 10 times for statistical confidence
7. Subtract leakage from measurement fixture

Accuracy Requirements:
- Resolution: < 1 nA
- Accuracy: ±5%
- Repeatability: ±2%
```

### 7.2 On-Chip Leakage Monitoring

```
Built-In Leakage Sensor:

┌─────────────────────────────────┐
│ Leakage Monitor Circuit         │
│                                 │
│  V_DD ─────┬──────┬─────┐      │
│            │      │     │      │
│         ┌──┴──┐┌──┴──┐  │      │
│         │ DUT ││ Ref │  │      │
│         │     ││     │  │      │
│         └──┬──┘└──┬──┘  │      │
│            │      │     │      │
│            ▼      ▼     │      │
│         ┌──────────────┐│      │
│         │   Current    ││      │
│         │   Mirror     ││      │
│         └──────┬───────┘│      │
│                │        │      │
│            ┌───▼───┐    │      │
│            │ ADC   │    │      │
│            │ (12b) │    │      │
│            └───┬───┘    │      │
│                │        │      │
│            ┌───▼───┐    │      │
│            │Digital │    │      │
│            │Output  │    │      │
│            └────────┘    │      │
└─────────────────────────────────┘

Resolution: ~100 pA (with 12-bit ADC, 1 μA full scale)
Update rate: 1 Hz (low overhead)
Application: Run-time leakage monitoring and compensation
```

### 7.3 Process Monitoring

```
Leakage Process Monitor Structures:

Test Structures on iPACE-CHIP:
- Array of 1000 NMOS transistors (leakage measurement)
- Array of 1000 PMOS transistors (leakage measurement)
- Chain of minimum-size inverters (process speed)
- Ring oscillator (frequency = process corner indicator)

Usage:
- Wafer-level testing: Sort by leakage current
- Identify fast/weak (high leakage) vs. slow/strong (low leakage)
- Calibrate on-chip body bias circuits
- Correlate with reliability testing
```

## 8. Leakage Impact on Battery Life

### 8.1 Battery Life Calculation

```
iPACE-CHIP Battery Life Analysis:

Battery Specifications:
- Chemistry: Lithium-Iodine (LiI)
- Capacity: 120 mAh
- Voltage: 2.8V nominal
- End-of-life voltage: 2.4V
- Self-discharge: < 1% per year

Leakage Power Impact:
- Average leakage: 100 nW (at 37°C)
- Operating time: 10 years = 3.15 × 10⁸ seconds
- Leakage energy: 100 × 10⁻⁹ × 3.15 × 10⁸ = 31.5 mJ
- Leakage charge: 31.5 × 10⁻³ / 3.0V = 10.5 mC = 2.92 μAh

Leakage Percentage of Battery:
- Leakage: 2.92 μAh / 120 mAh = 0.0024%
- Remaining for dynamic power and stimulation: 99.9976%

Dynamic Power Impact:
- Average dynamic + stimulation: 3 μW
- Dynamic energy over 10 years: 3 × 10⁻⁶ × 3.15 × 10⁸ = 945 mJ
- Dynamic charge: 945 × 10⁻³ / 3.0V = 0.315 C = 87.5 μAh

Total Battery Consumption:
- Total: 2.92 + 87.5 = 90.4 μAh
- Remaining: 120 mAh - 0.0904 mAh ≈ 119.91 mAh
- The limiting factor is battery self-discharge and
  hermetic seal degradation, not circuit power consumption
```

### 8.2 End-of-Life Leakage Analysis

```
Aging Effects on Leakage:

Leakage Evolution Over 10 Years:

1. BTI (Bias Temperature Instability):
   - Threshold voltage increases over time
   - V_th shift: 20-50 mV over lifetime
   - Leakage reduction: 30-60%
   - Effect: Leakage DECREASES with aging

2. HCI (Hot Carrier Injection):
   - Threshold voltage increases
   - Less severe than BTI for implantable applications
   - Leakage reduction: 10-20%

3. TDDB (Time-Dependent Dielectric Breakdown):
   - Can cause gate leakage increase
   - Rare in well-designed circuits
   - Not significant for 180nm at 1.8V

Net Effect:
- Leakage decreases 40-60% over 10 years
- Battery life improves slightly with aging
- Worst-case leakage is at time zero
```

## 9. Leakage in Sub-Threshold Operation

### 9.1 Sub-Threshold Logic Considerations

For ultra-low-power modes using sub-threshold operation:

```
Sub-Threshold Logic Operation:

Operating Point: V_DD < V_th
- Typical V_DD: 0.3-0.5V
- Transistors operate in sub-threshold region
- Current: Exponential function of V_DD

Advantages:
- Ultra-low power: 0.1-1 nW
- Energy efficiency: fJ/op
- Suitable for: Housekeeping, timers

Disadvantages:
- Slow: MHz to kHz range
- High sensitivity to V_th variation
- Reduced noise margins
- Complex design methodology

iPACE-CHIP Application:
- Housekeeping controller: Sub-threshold
- Watchdog timer: Sub-threshold
- Always-on oscillator reference: Sub-threshold
```

### 9.2 Leakage in Sub-Threshold Designs

```
Leakage vs. Operating Current in Sub-Threshold:

In sub-threshold logic, leakage IS the operating current.

I_operation = I_sub × (1 - exp(-V_DD / V_T))
I_leakage = I_sub × exp(-V_DD / V_T)

Ratio: I_operation / I_leakage = exp(V_DD / V_T) - 1

For V_DD = 0.4V:
- exp(0.4 / 0.026) - 1 ≈ 4.2 × 10⁶
- Operating current is 4 million times leakage

Design Implication:
- "Leakage" is the fundamental current mechanism
- Power reduction comes from minimizing total sub-threshold current
- Not traditional leakage reduction techniques
```

## 10. Advanced Leakage Management

### 10.1 Adaptive Body Biasing (ABB)

```
ABB Control Loop:

┌───────────────┐
│ Leakage Sensor │
│ (on-chip)     │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Comparator    │──► Too much leakage
│               │──► Too little leakage
└───────┬───────┘──► Optimal
        │
        ▼
┌───────────────┐
│ Body Bias     │
│ Controller    │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Body Bias     │
│ Voltage Gen.  │
└───────┬───────┘
        │
        └──► Adjust V_BS to maintain target leakage

Control Loop Parameters:
- Update rate: 1 Hz (low overhead)
- Bias range: -1.0V to +0.5V (RBB to FBB)
- Response time: ~100 ms
- Power overhead: < 1 nW
```

### 10.2 Leakage-Aware Design Flow

```
Leakage-Aware RTL Synthesis:

Step 1: Timing Analysis
├── Identify critical paths
├── Classify paths by slack
└── Group into timing bins

Step 2: Vt Assignment
├── Paths with slack > 200 ps: HVT
├── Paths with slack 50-200 ps: SVT
├── Paths with slack < 50 ps: LVT
└── Critical paths: LVT only if necessary

Step 3: Power Optimization
├── Leakage budget per block
├── Iterative Vt swapping
├── Verify timing closure
└── Generate leakage report

Step 4: Verification
├── Corner analysis (SS/TT/FF)
├── Temperature sweep (0-40°C)
├── Statistical analysis (Monte Carlo)
└── Worst-case verification
```

### 10.3 Leakage in Memory Arrays

```
SRAM Leakage Management:

6T SRAM Cell Leakage Components:
- Cell NMOS leakage: 2 transistors
- Cell PMOS leakage: 2 transistors
- Access NMOS leakage: 2 transistors
- Total per cell: ~6× single transistor leakage

iPACE-CHIP Memory Hierarchy:
┌──────────────┬────────┬──────────┬───────────┐
│ Memory       │ Size   │ Leakage  │ Technique │
├──────────────┼────────┼──────────┼───────────┤
│ Register File│ 256B   │ 5 nA     │ HVT cells │
│ Data SRAM    │ 2 KB   │ 15 nA    │ Power gate│
│ Code Flash   │ 8 KB   │ 3 nA     │ Deep sleep│
│ Config NVM   │ 1 KB   │ 1 nA     │ Always-off│
└──────────────┴────────┴──────────┴───────────┘

SRAM Leakage Reduction:
1. Use high-Vt cells for low-leakage SRAM
2. Power gating for data SRAM (standby mode)
3. Voltage reduction in standby (0.5V retention)
4. Word-line gating (prevent accidental access)
```

## 11. Summary

Static power leakage in the iPACE-CHIP pacemaker ASIC represents approximately 4% of average total power consumption but dominates during deep sleep modes. Subthreshold leakage is the primary component, contributing 55% of total leakage, with gate tunneling and junction leakage as secondary sources. Temperature has a profound effect, with leakage approximately doubling every 10°C increase. Multi-threshold voltage assignment, power gating, and reverse body biasing collectively achieve 50-200× leakage reduction. Over the 10-year device lifetime, leakage consumes only 0.0024% of battery capacity, confirming that leakage management, while important, is secondary to dynamic power optimization for battery life. However, proper leakage management is essential for meeting the ultra-low-power deep sleep targets required for the pacemaker's standby modes.

## References

1. Kim, N.S., et al., "Leakage Current: Moore's Law Meets Static Power," IEEE Computer, Vol. 36, No. 12, 2003.
2. Narendra, S., Chandrakasan, A., "Leakage in Nanometer CMOS Technologies," Springer, 2006.
3. iPACE-CHIP Project Internal Documentation: Leakage Characterization Report, Rev 1.8.
4. Song, S., et al., "Static Power Optimization Methodology for Medical Implant ASICs," IEEE Trans. Biomedical Circuits and Systems, 2019.
5. TSMC 0.18μm Mixed-Signal Process Design Manual, Rev 5.0.
