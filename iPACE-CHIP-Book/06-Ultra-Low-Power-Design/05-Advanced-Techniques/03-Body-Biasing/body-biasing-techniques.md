# Body Biasing Techniques for Implantable Pacemaker ASICs

## 1. Introduction to Body Biasing

Body biasing is a circuit technique that modifies the threshold voltage (V_th) of MOSFET transistors by applying a voltage to the body (substrate) terminal. By controlling the body-to-source voltage (V_BS), designers can dynamically adjust circuit performance and power consumption. For the iPACE-CHIP pacemaker ASIC, body biasing provides a powerful tool for compensating process variations, optimizing power-performance trade-offs, and extending battery life through adaptive threshold voltage control.

The body effect, where V_th changes with V_BS, is normally considered a nuisance in circuit design. However, body biasing techniques exploit this effect constructively, using it as a design knob to fine-tune circuit behavior after fabrication. This is particularly valuable for implantable medical devices where reliability across process corners and temperature extremes is critical.

## 2. Body Effect Physics

### 2.1 Threshold Voltage Equation

```
Threshold Voltage with Body Bias:

V_th = V_th0 + γ × (√(|2φ_F - V_BS|) - √(|2φ_F|))

Where:
- V_th0 = zero-bias threshold voltage
- γ = body effect coefficient = √(2 × q × ε_si × N_a) / C_ox
- φ_F = Fermi potential = (kT/q) × ln(N_a / n_i)
- V_BS = body-to-source voltage
- q = electron charge = 1.6 × 10⁻¹⁹ C
- ε_si = silicon permittivity = 1.04 × 10⁻¹² F/cm
- N_a = substrate doping concentration
- C_ox = gate oxide capacitance per unit area

For iPACE-CHIP 180nm process:
- V_th0 = 0.4V (NMOS), -0.4V (PMOS)
- γ = 0.4 V^(1/2) (NMOS), 0.5 V^(1/2) (PMOS)
- φ_F = 0.3V (P-type substrate)

Example:
At V_BS = 0V: V_th = V_th0 = 0.4V
At V_BS = -0.5V (reverse bias): V_th = 0.4 + 0.4 × (√0.8 - √0.3) = 0.4 + 0.4 × (0.894 - 0.548) = 0.4 + 0.138 = 0.538V
At V_BS = +0.5V (forward bias): V_th = 0.4 - 0.138 = 0.262V
```

### 2.2 Bias Modes

```
Body Biasing Modes:

1. Zero Body Bias (ZBB):
   - V_BS = 0V
   - V_th = V_th0 (nominal)
   - Standard operation
   - Default for most circuits

2. Reverse Body Bias (RBB):
   - V_BS < 0V (NMOS), V_BS > 0V (PMOS)
   - V_th increases
   - Leakage decreases
   - Speed decreases
   - Application: Sleep modes, leakage reduction

3. Forward Body Bias (FBB):
   - V_BS > 0V (NMOS), V_BS < 0V (PMOS)
   - V_th decreases
   - Leakage increases
   - Speed increases
   - Application: Performance boost, process compensation

Body Bias Summary for iPACE-CHIP NMOS:
┌──────────┬──────────┬──────────┬──────────┬──────────┐
│ V_BS (V) │ V_th (V) │ I_sub    │ Speed    │ Power    │
├──────────┼──────────┼──────────┼──────────┼──────────┤
│ -1.0     │ 0.64     │ 0.1×     │ 0.3×     │ 0.1×     │
│ -0.5     │ 0.54     │ 0.3×     │ 0.5×     │ 0.3×     │
│ 0.0      │ 0.40     │ 1.0×     │ 1.0×     │ 1.0×     │
│ +0.3     │ 0.30     │ 3.0×     │ 1.5×     │ 3.0×     │
│ +0.5     │ 0.26     │ 5.0×     │ 2.0×     │ 5.0×     │
└──────────┴──────────┴──────────┴──────────┴──────────┘
```

### 2.3 Impact on Circuit Parameters

```
Body Biasing Impact on Key Parameters:

1. Leakage Current (sub-threshold):
ΔI_leak/I_leak = -ΔV_th / (n × V_T)
At V_T = 26 mV, n = 1.5:
- RBB of -0.5V: V_th increase = 0.14V → leakage reduced 3.6×
- FBB of +0.3V: V_th decrease = 0.10V → leakage increased 2.6×

2. Gate Delay:
t_delay ∝ V_DD / (V_DD - V_th)^α
At V_DD = 1.8V, α = 1.3:
- RBB: V_th increase 0.14V → delay increase 15%
- FBB: V_th decrease 0.10V → delay decrease 10%

3. Dynamic Power:
P_dynamic ∝ C × V_DD² × f
No direct effect (V_DD unchanged)
Indirect effect: Can reduce V_DD if FBB provides speed margin

4. Short-Circuit Power:
P_sc ∝ I_peak × t_rise × f
FBB increases I_peak → increases short-circuit power
RBB decreases I_peak → decreases short-circuit power
```

## 3. Body Biasing Architectures

### 3.1 Global Body Biasing

```
Global Body Biasing Architecture:

A single body bias voltage is applied to all transistors
in a block or the entire chip:

                    V_BB_generator
                         │
                    ┌────┴────┐
                    │ Bias    │
                    │ Voltage │
                    │ Generator│
                    └────┬────┘
                         │
              ┌──────────┼──────────┐
              │          │          │
         ┌────┴────┐┌───┴────┐┌────┴────┐
         │ Block A ││ Block B││ Block C │
         │ V_BB    ││ V_BB   ││ V_BB    │
         └─────────┘└────────┘└─────────┘

Implementation:
- Shared bias generator for all blocks
- Simple routing (single V_BB wire)
- Uniform bias across chip
- Low overhead

Disadvantages:
- Cannot optimize per-block
- Global optimum, not local
- Less effective for mixed-activity designs
```

### 3.2 Local Body Biasing

```
Local Body Biasing Architecture:

Each block has its own independent body bias voltage:

                    V_BB_gen_A
                         │
                    ┌────┴────┐
                    │ Block A │
                    │ Bias    │
                    └─────────┘

                    V_BB_gen_B
                         │
                    ┌────┴────┐
                    │ Block B │
                    │ Bias    │
                    └─────────┘

                    V_BB_gen_C
                         │
                    ┌────┴────┐
                    │ Block C │
                    │ Bias    │
                    └─────────┘

Implementation:
- Independent bias generator per block
- More complex routing
- Per-block optimization
- Higher overhead

Advantages:
- Optimal bias for each block's workload
- Better power-performance trade-off
- Can compensate local process variations
- Most effective for mixed-activity designs
```

### 3.3 Adaptive Body Biasing (ABB)

```
Adaptive Body Biasing System:

ABB automatically adjusts body bias based on workload:

┌─────────────────────────────────────────────────────────┐
│ Adaptive Body Biasing Controller                         │
│                                                         │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │  Workload       │  │  Bias           │              │
│  │  Monitor        │──│  Generator      │              │
│  │  (activity      │  │  (DAC)          │              │
│  │   counter)      │  └────────┬────────┘              │
│  └─────────────────┘           │                        │
│                                │                        │
│  ┌─────────────────┐  ┌───────▼─────────┐              │
│  │  Temperature    │──│  V_BB           │              │
│  │  Sensor         │  │  Output         │              │
│  └─────────────────┘  │  (to body       │              │
│                       │   contacts)     │              │
│  ┌─────────────────┐  └─────────────────┘              │
│  │  Process        │                                   │
│  │  Monitor        │                                   │
│  │  (ring osc.)    │                                   │
│  └─────────────────┘                                   │
│                                                         │
│  Control Algorithm:                                     │
│  1. Measure workload (activity counter)                │
│  2. Measure temperature (sensor)                       │
│  3. Measure process speed (ring oscillator)            │
│  4. Calculate optimal V_BB                             │
│  5. Apply V_BB via DAC                                 │
│  6. Repeat every 100 ms                               │
│                                                         │
│  Power: 10 nW (controller) + 5 nW (DAC)               │
│  Area: 0.01 mm²                                        │
└─────────────────────────────────────────────────────────┘
```

## 4. Body Biasing for iPACE-CHIP

### 4.1 Block-Specific Biasing

```
iPACE-CHIP Body Biasing Strategy:

Block              │ Mode    │ V_BS    │ Purpose
───────────────────┼─────────┼─────────┼─────────────────
Sensing amplifier  │ ZBB     │ 0V      │ Nominal performance
DSP engine (active)│ FBB     │ +0.3V   │ Speed boost
DSP engine (idle)  │ RBB     │ -0.5V   │ Leakage reduction
Stimulation ctrl   │ ZBB     │ 0V      │ Nominal performance
Communication      │ ZBB     │ 0V      │ Nominal performance
Housekeeping       │ RBB     │ -0.3V   │ Minimum leakage
Always-on monitor  │ RBB     │ -0.5V   │ Minimum leakage

Bias Generator Requirements:
- ZBB: Direct connection to GND (V_BS = 0V)
- RBB: Negative voltage generator (-0.3V to -0.5V)
- FBB: Positive voltage generator (+0.3V)

Power Consumption:
- RBB generator: 5 nW (charge pump)
- FBB generator: 5 nW (charge pump)
- Control logic: 10 nW
- Total: 20 nW

Leakage Savings:
- DSP idle: 3.6× reduction (RBB)
- Housekeeping: 2× reduction (RBB)
- Always-on monitor: 3.6× reduction (RBB)
- Total leakage savings: 50 nW
```

### 4.2 Process Compensation

```
Process Compensation with Body Biasing:

Problem: Process variations cause V_th spread of ±40 mV

Impact on iPACE-CHIP:
- Fast corner (FF): 2× leakage, 15% faster
- Slow corner (SS): 0.5× leakage, 15% slower

ABB Compensation Strategy:
1. Measure process speed at startup (ring oscillator)
2. Apply appropriate body bias:
   - Fast corner: RBB to reduce leakage
   - Slow corner: FBB to improve speed
   - Typical corner: ZBB (nominal)

Compensation Results:
┌──────────────┬──────────────┬──────────────┬──────────┐
│ Corner       │ Without ABB  │ With ABB     │ Improved │
├──────────────┼──────────────┼──────────────┼──────────┤
│ FF (fast)    │ 2× leakage   │ 1.1× leakage │ 45%      │
│ TT (typical) │ 1× leakage   │ 1× leakage   │ 0%       │
│ SS (slow)    │ 0.5× leakage │ 0.9× leakage │ 80%      │
└──────────────┴──────────────┴──────────────┴──────────┘

Speed Compensation:
┌──────────────┬──────────────┬──────────────┬──────────┐
│ Corner       │ Without ABB  │ With ABB     │ Improved │
├──────────────┼──────────────┼──────────────┼──────────┤
│ FF (fast)    │ 115% speed   │ 105% speed   │ 87%      │
│ TT (typical) │ 100% speed   │ 100% speed   │ 0%       │
│ SS (slow)    │ 85% speed    │ 95% speed    │ 67%      │
└──────────────┴──────────────┴──────────────┴──────────┘

ABB significantly reduces process variation impact.
```

### 4.3 Temperature Compensation

```
Temperature Compensation with Body Biasing:

Problem: At low temperature (-20°C), circuits are 3× slower
Solution: Apply FBB to restore speed

Temperature-Body Bias Mapping:
┌──────────────┬──────────────┬──────────────┬──────────┐
│ Temperature  │ V_th Change  │ Required V_BS│ I_sub    │
├──────────────┼──────────────┼──────────────┼──────────┤
│ -20°C        │ +40 mV       │ +0.3V (FBB)  │ 1.0×     │
│ 0°C          │ +20 mV       │ +0.15V (FBB) │ 1.0×     │
│ 25°C         │ 0 mV         │ 0V (ZBB)     │ 1.0×     │
│ 37°C         │ -12 mV       │ -0.1V (RBB)  │ 1.0×     │
│ 50°C         │ -25 mV       │ -0.2V (RBB)  │ 1.0×     │
└──────────────┴──────────────┴──────────────┴──────────┘

Result: Constant speed across temperature range
Power overhead: < 5% (from bias generators)
Area overhead: 0.01 mm² (bias generators)
```

## 5. Body Biasing Circuit Design

### 5.1 Bias Voltage Generator

```
Body Bias Voltage Generator:

For generating negative (RBB) and positive (FBB) voltages:

RBB Generator (Negative Voltage):
┌─────────────────────────────────────────────────────────┐
│ Charge Pump for Negative Voltage                         │
│                                                         │
│  V_DD (1.8V) ────┐                                    │
│                  │                                      │
│             ┌────┴────┐                                │
│             │  NMOS   │                                │
│             │  M1     │                                │
│             │ (switch)│                                │
│             └────┬────┘                                │
│                  │                                      │
│  CLK ────────────┤                                      │
│                  │                                      │
│             ┌────┴────┐                                │
│             │ Capacitor│                                │
│             │ C1      │                                │
│             └────┬────┘                                │
│                  │                                      │
│             ┌────┴────┐                                │
│             │  Diode  │                                │
│             │  D1     │                                │
│             └────┬────┘                                │
│                  │                                      │
│             V_BB_neg (-0.5V)                           │
│                  │                                      │
│             ┌────┴────┐                                │
│             │ Filter  │                                │
│             │ Cap C2  │                                │
│             └─────────┘                                │
│                                                         │
│  Specifications:                                        │
│  - Output: -0.5V ± 50 mV                              │
│  - Current capability: 1 μA                            │
│  - Ripple: < 10 mV                                     │
│  - Power: 5 nW (at 32 kHz clock)                       │
│  - Area: 0.005 mm²                                      │
└─────────────────────────────────────────────────────────┘
```

### 5.2 Body Contact Design

```
Body Contact Design:

For applying body bias, proper body contacts are required:

NMOS Body Contact (P-substrate):
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  N+ ────┬────┬────┬────┬────┬────┬────┬────┬────       │
│         │    │    │    │    │    │    │    │            │
│  ┌──────┴────┴────┴────┴────┴────┴────┴────┴──────┐    │
│  │              P-substrate                        │    │
│  │                                                 │    │
│  │    ┌──────────────────────────────────────┐    │    │
│  │    │           NMOS Transistors           │    │    │
│  │    │     (V_BS controlled via substrate)  │    │    │
│  │    └──────────────────────────────────────┘    │    │
│  │                                                 │    │
│  └────────────────────────────────────────────────┘    │
│         │                                              │
│    P+ body contact                                      │
│    (connected to V_BB)                                  │
│                                                         │
│  Contact Specifications:                                │
│  - Contact size: 0.36 μm × 0.36 μm                    │
│  - Contact spacing: 2 μm                               │
│  - Number per block: 10-20                             │
│  - Contact resistance: < 100 Ω                         │
└─────────────────────────────────────────────────────────┘
```

### 5.3 Layout Considerations

```
Body Biasing Layout Guidelines:

Rule 1: Well Proximity Effect
- NMOS body contacts placed near transistors
- Maximum distance: 10 μm
- Minimizes resistance between contact and channel

Rule 2: Substrate Resistance
- Multiple body contacts per block
- Distributed contacts for uniform bias
- Contact spacing: < 10 μm

Rule 3: Guard Rings
- Guard rings between differently biased blocks
- Prevent latch-up between RBB and FBB regions
- Connected to substrate potential

Rule 4: Noise Isolation
- Separate bias generators for analog and digital
- Decoupling capacitance on bias lines
- Filter capacitors at bias generator output

iPACE-CHIP Layout:
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │  RBB Block  │  │  ZBB Block  │  │  FBB Block  │    │
│  │             │  │             │  │             │    │
│  │  V_BB=-0.5V │  │  V_BB=0V    │  │  V_BB=+0.3V │    │
│  │             │  │             │  │             │    │
│  │  ┌───────┐  │  │  ┌───────┐  │  │  ┌───────┐  │    │
│  │  │ Guard │  │  │  │ Guard │  │  │  │ Guard │  │    │
│  │  │ Ring  │  │  │  │ Ring  │  │  │  │ Ring  │  │    │
│  │  └───────┘  │  │  └───────┘  │  │  └───────┘  │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 6. Verification and Testing

### 6.1 Body Biasing Verification

```
Body Biasing Verification:

Test 1: V_th Measurement
- Apply different V_BS values
- Measure V_th via I-V characterization
- Verify V_th vs. V_BS relationship
- Pass: Within ±10 mV of model

Test 2: Leakage Reduction
- Apply RBB (-0.5V)
- Measure leakage current
- Verify 3.6× reduction
- Pass: Within ±20% of target

Test 3: Speed Enhancement
- Apply FBB (+0.3V)
- Measure maximum frequency
- Verify 15% speed increase
- Pass: Within ±10% of target

Test 4: Temperature Compensation
- Sweep temperature -20°C to 50°C
- Apply appropriate body bias
- Verify constant speed
- Pass: Speed varies < 10% across temperature

Test 5: Process Compensation
- Test across FF/TT/SS corners
- Apply ABB
- Verify consistent performance
- Pass: Performance varies < 15% across corners
```

### 6.2 On-Chip Monitoring

```
On-Chip Body Biasing Monitor:

┌─────────────────────────────────────────────────────────┐
│ Body Biasing Monitor                                     │
│                                                         │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │  V_th Sensor    │  │  Leakage Sensor │              │
│  │  (ring osc.     │  │  (current mirror│              │
│  │   frequency)    │  │   + ADC)        │              │
│  └────────┬────────┘  └────────┬────────┘              │
│           │                    │                        │
│  ┌────────▼────────┐  ┌───────▼─────────┐              │
│  │  Comparator     │  │  Comparator     │              │
│  │  (vs. reference)│  │  (vs. reference)│              │
│  └────────┬────────┘  └───────┬─────────┘              │
│           │                    │                        │
│           └──────────┬─────────┘                        │
│                      │                                  │
│              ┌───────▼───────┐                          │
│              │  Bias         │                          │
│              │  Adjustment   │                          │
│              │  Logic        │                          │
│              └───────┬───────┘                          │
│                      │                                  │
│              ┌───────▼───────┐                          │
│              │  V_BB Output  │                          │
│              │  (DAC)        │                          │
│              └───────────────┘                          │
│                                                         │
│  Resolution: 10 mV                                      │
│  Update rate: 10 Hz                                     │
│  Power: 5 nW                                            │
└─────────────────────────────────────────────────────────┘
```

## 7. Summary

Body biasing techniques provide the iPACE-CHIP pacemaker ASIC with dynamic control over transistor threshold voltages, enabling adaptive power-performance optimization. Reverse body bias (RBB) reduces leakage by 3.6× during idle periods, while forward body bias (FBB) provides 15% speed boost for timing-critical operations. Adaptive body biasing (ABB) automatically compensates for process variations, reducing performance variation from ±15% to ±7.5%. Temperature compensation maintains constant speed across the -20°C to 50°C operating range. The body biasing infrastructure adds 20 nW of power overhead and 0.01 mm² of area, while providing 50 nW of leakage savings for a net benefit of 30 nW. Body biasing is a valuable technique for implantable medical devices where reliability across process corners and temperatures is essential.

## References
1. Tschanz, J., et al., "Adaptive Body Biasing for Reduced Power," IEEE JSSC, 2002.
2. iPACE-CHIP Project Internal Documentation: Body Biasing Design Guide, Rev 1.4.
3. TSMC 0.18μm Mixed-Signal Process Design Manual: Body Biasing Characterization.
4. Kao, J., et al., "Adaptive Body Biasing for Low-Power CMOS," IEEE DAC, 2001.
5. Ferretti, L., et al., "Body Biasing Techniques for Medical ASICs," IEEE BioCAS, 2019.
