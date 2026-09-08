# SCR Thyristors - Concepts

## 1. SCR Construction

### Four-Layer Structure
- P1-N1-P2-N2 layers forming three PN junctions (J1, J2, J3)
- Anode connected to P1 (outer P layer)
- Cathode connected to N2 (outer N layer)
- Gate connected to P2 (inner P layer, near cathode)

### Physical Construction
- **Diffused junction**: Junctions formed by diffusion process
- **Amplifying gate**: Small SCR triggers larger area of main SCR
- **Hockey puck (press-pack)**: Disc-shaped for high power (up to 5kA, 10kV)
- **Stud mount**: Bolt-on package for medium power (up to 1kA, 2kV)
- **TO-220/TO-247**: Package for low-medium power (up to 100A, 1200V)

### Key Construction Features
- Gate terminal close to cathode for better turn-on control
- Shorted anode or cathode bases reduce leakage current
- Gold doping reduces minority carrier lifetime → faster switching
- Cathode shorts improve dv/dt immunity

## 2. Two-Transistor Analogy

### Equivalent Circuit
- SCR equivalent to two complementary transistors:
  - Q1: PNP transistor (P1-N1-P2 → E-B-C)
  - Q2: NPN transistor (N1-P2-N2 → C-B-E)

### Operation
- Q1 collector current = Q2 base current (Ic1 = Ib2)
- Q2 collector current = Q1 base current (Ic2 = Ib1)
- Total anode current: IA = Ic1 + Ic2
- Gate current: IG feeds into Q2 base, increasing Ic2
- Regenerative feedback: Ic2 → Ib1 → Ic1 → Ib2 → Ic2 → ...
- Once α1 + α2 ≈ 1, latch occurs (IG no longer needed)

### Condition for Latching
```
IA = (α2 × IG + Ico1 + Ico2) / (1 - (α1 + α2))
```
Where:
- α1, α2 = common-base current gains of Q1, Q2
- Ico1, Ico2 = collector-base leakage currents
- When α1 + α2 → 1, IA → ∞ (latching condition)

### Current Gains
- α increases with current (due to current gain nonlinearity)
- Initially α1 + α2 < 1 → SCR is OFF
- Gate current increases collector currents → α increases
- At critical current, α1 + α2 = 1 → SCR turns ON

## 3. SCR Operation

### Forward Blocking (OFF State)
- Anode positive, cathode negative
- J1 and J3 forward biased, J2 reverse biased
- Only small leakage current flows (IFWO: forward off-state current)
- SCR blocks forward voltage up to VBO (breakover voltage)

### Forward Conduction (ON State)
- Triggered by: gate pulse, breakover, dv/dt, temperature
- All three junctions forward biased (J2 becomes forward biased)
- VAK drops to VTM (on-state voltage, 1-2V)
- Current limited by external circuit
- Once ON, cannot be turned OFF by gate (latching behavior)

### Reverse Blocking
- Anode negative, cathode positive
- J1 and J3 reverse biased, J2 forward biased
- Blocks reverse voltage up to VRRM
- Similar to reverse-biased diode

### Turn-On Mechanisms
1. **Gate triggering**: Most common, apply positive gate pulse
2. **Forward breakover**: Exceed VBO (avoid in normal operation)
3. **dv/dt triggering**: High rate of voltage rise causes capacitive displacement current through J2
4. **Temperature**: Increased leakage current can trigger at lower voltage
5. **Light triggering**: For specific applications (pulse power)

## 4. V-I Characteristics

### Regions
1. **Forward blocking region**: 0 < VA < VBO, IA = IFWO (small)
2. **Forward conduction region**: VA = VTM (≈1-2V), IA determined by load
3. **Reverse blocking region**: VA < 0, VR < VRRM, IA = small leakage
4. **Reverse breakdown**: VA < -VRRM, avalanche breakdown (destructive)

### Key Points
- **VBO (Breakover voltage)**: Forward voltage at which SCR turns on without gate
- **VTM (On-state voltage)**: Forward voltage in conduction (typically 1-2V)
- **IH (Holding current)**: Minimum anode current to maintain conduction
- **IL (Latching current)**: Minimum anode current to ensure turn-on completes
- **IL > IH** always (typically IL ≈ 2-3 × IH)

### Temperature Effects
- VBO decreases with temperature (negative temp coefficient, -0.1%/°C)
- IH decreases with temperature
- Leakage current increases with temperature
- At high temperature, SCR may self-trigger (thermally induced)

## 5. Firing Methods

### DC Gate Firing
- Constant DC voltage applied to gate-cathode
- Simple but wasteful (continuous gate power dissipation)
- Gate must be triggered each cycle for half-wave operation
- Not commonly used in AC circuits

### AC Gate Firing
- AC voltage synchronized with supply
- Gate pulse timed for desired firing angle α
- Natural zero-crossing provides turn-off opportunity
- Used in phase-controlled rectifiers

### Pulse Gate Firing
- Narrow pulses (1-10 μs) applied to gate
- Minimum pulse width to ensure latching
- IL × tON ≥ minimum gate energy requirement
- More efficient than DC gate firing

### Pulsed Train Firing
- Series of narrow pulses at high frequency
- Ensures turn-on even with slow load inductance
- Preferred for inductive loads
- Typically 1-10 μs pulse width at 1-10 kHz

### Optical Firing (Light-Activated SCR)
- Photogenerate carriers in gate region
- Provides galvanic isolation
- Used in HVDC and high-power converters
- dv/dt immunity is excellent

### dv/dt Firing (Unintentional)
- High rate of voltage rise across SCR
- Displacement current through J2 capacitance
- C × dv/dt acts like gate current
- Usually avoided (can cause false triggering)

## 6. Firing Circuits

### Resistance Firing
- Simple RC circuit with variable resistor
- α range limited: 30° to 150° approximately
- Poor linearity between R and α
- Limited to low power, resistive loads

### RC Firing
- RC phase shift provides timing
- Better α range: 0° to 180° theoretically
- More linear R-α relationship
- Can trigger inductive loads

### UJT Triggering (Programmable Unijunction Transistor)
- UJT relaxation oscillator generates pulses
- Sync pulses ensure proper timing
- α range: 0° to 180°
- Reliable, commonly used in textbooks

### DIAC-TRIAC Triggering
- DIAC provides symmetric breakdown voltage (≈32V)
- Capacitor charges through resistor, fires DIAC when Vcap > VDIAC
- Provides sharp gate pulse
- Good for light dimmers, simple circuits

### IC-Based Triggering (TCA785, MC34060)
- Modern ICs provide precise firing
- Built-in synchronization, soft-start, protection
- Digital control capability
- Preferred in industrial applications

## 7. SCR Ratings

### Voltage Ratings
- **VDRM (DRM)**: Repetitive peak forward off-state voltage
- **VRRM (RRM)**: Repetitive peak reverse voltage
- **VDSM (DSM)**: Non-repetitive peak forward off-state voltage (surge)
- **VRSM (RSM)**: Non-repetitive peak reverse voltage (surge)
- **VBO**: Forward breakover voltage (must be > VDRM)
- Design rule: VDRM ≥ 2 × Vpeak (for AC applications)

### Current Ratings
- **IT(RMS)**: RMS on-state current
- **IT(AV)**: Average on-state current
- **ITSM**: Non-repetitive peak on-state surge current
- **IL**: Latching current
- **IH**: Holding current
- **IGT**: Gate trigger current
- **VGT**: Gate trigger voltage

### dv/dt and di/dt Ratings
- **dv/dt (critical)**: Maximum rate of rise of forward voltage
- **di/dt (critical)**: Maximum rate of rise of on-state current
- Exceeding dv/dt → false triggering
- Exceeding di/dt → localized heating near gate → destruction

## 8. Protection Circuits

### dv/dt Protection (Snubber Circuit)
- R-C snubber across SCR: damps voltage oscillation
- C limits dv/dt: dv/dt = V/C
- R limits discharge current through SCR
- Typical: R = 10-100Ω, C = 0.01-1 μF

### di/dt Protection
- Series inductor (commutation reactor)
- Limits di/dt = V/L
- Also helps with load commutation
- Typical: L = 10-100 μH

### Overcurrent Protection
- Fuses (fast-acting semiconducting fuses)
- Current limiters
- SCR crowbar circuits
- Thermal protection (temperature sensors)

### Gate Protection
- Zener diodes across gate-cathode (limit VGT)
- Series gate resistor (limit IGT)
- Bypass capacitor (filter noise)

### Thermal Protection
- Heatsink with thermal paste
- Temperature sensors (thermistors, RTDs)
- Thermal shutdown circuits
- derating curves for reliable operation

## 9. SCR Turn-Off Methods

### Natural Commutation (Line Commutation)
- Current zero-crossing in AC circuits
- SCR turns off when current drops below IH
- Simple, reliable, used in most AC applications
- Limited to AC line frequency applications

### Forced Commutation
- External circuit forces current to zero
- Required in DC circuits
- Different classes (A-F) based on method
- Adds complexity and cost

### Gate Turn-Off (GTO)
- Large negative gate current to turn off
- Turns off controlled portion of current
- Limited turn-off capability (typically 3× on-state current)
- Used in medium power inverters

### Load Commutation
- Load provides natural zero crossing
- Works with RLC loads or resonant loads
- No external commutation circuit needed
- Used in resonant converters

## 10. ISRO-Specific Focus

- SCR firing circuits for satellite power systems
- Phase-controlled rectifiers for battery charging
- SCR crowbar circuits for overvoltage protection
- Radiation effects on SCR triggering thresholds
- Reliability requirements for space-grade SCRs
- Redundancy requirements for critical applications
