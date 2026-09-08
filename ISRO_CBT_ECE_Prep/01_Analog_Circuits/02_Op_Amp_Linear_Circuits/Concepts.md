# Op-Amp Linear Circuits - Concepts

## Inverting Amplifier Configuration

### Circuit Structure
- Input signal applied to inverting terminal (-) through resistor R1
- Non-inverting terminal (+) connected to ground
- Feedback resistor Rf connects output to inverting terminal
- Virtual ground concept applies at inverting terminal

### Key Principles
- Virtual short: V+ = V- (due to negative feedback)
- Input current into op-amp terminals is zero (ideal)
- Node at inverting terminal is at virtual ground (0V)
- Current through R1 = current through Rf (KCL at inverting node)

### Voltage Gain
- Av = -Rf/R1 (negative sign indicates 180° phase shift)
- Magnitude of gain depends only on external resistors
- Gain is independent of op-amp open-loop gain (if AOL is very large)

### Input and Output Impedance
- Input impedance seen by source = R1 (not infinite due to virtual ground)
- Output impedance approaches zero (with negative feedback)

## Non-Inverting Amplifier Configuration

### Circuit Structure
- Input signal applied directly to non-inverting terminal (+)
- Feedback network (R1 and Rf) connected to inverting terminal (-)
- No virtual ground - inverting terminal follows input

### Key Principles
- Input signal sees very high impedance (op-amp input impedance)
- No phase shift between input and output
- Feedback fraction β = R1/(R1 + Rf)

### Voltage Gain
- Av = 1 + Rf/R1 (always greater than unity)
- Can be exactly unity when Rf = 0 (voltage follower)
- Higher gain requires larger Rf/R1 ratio

### Unity Gain Buffer (Voltage Follower)
- Special case: Rf = 0, R1 = ∞
- Av = 1 (unity gain)
- Infinite input impedance, zero output impedance
- Used for impedance matching and isolation

## Summing Amplifier (Inverting Summer)

### Circuit Structure
- Multiple inputs through individual resistors to inverting terminal
- Single feedback resistor Rf
- Non-inverting terminal grounded

### Output Voltage
- Vout = -(V1·Rf/R1 + V2·Rf/R2 + V3·Rf/R3 + ...)
- Each input has independent gain setting
- Sign of output is inverted

### Equal Weights (R1 = R2 = R3 = R)
- Vout = -(Rf/R)·(V1 + V2 + V3 + ...)
- Acts as weighted summer with equal weights
- Simple averaging when Rf = R

### Non-Inverting Summing
- Use non-inverting input for summing
- Output = (1 + Rf/R1) × (weighted sum at + terminal)
- Requires voltage divider network at input

## Difference Amplifier (Subtractor)

### Circuit Structure
- Two inputs: V1 to inverting path, V2 to non-inverting path
- Four resistors: R1, R2 (inverting side), R3, R4 (non-inverting side)
- Balanced condition: R2/R1 = R4/R3

### Output Voltage (General)
- Vout = V2·(R4/(R3+R4))·(1+R2/R1) - V1·(R2/R1)

### Balanced Difference Amplifier
- When R2/R1 = R4/R3: Vout = (R2/R1)·(V2 - V1)
- Common-mode rejection is excellent
- CMRR depends on resistor matching

### Instrumentation Amplifier
- Three op-amp configuration
- Very high CMRR (>100 dB)
- Adjustable gain through single resistor
- High input impedance on both inputs

## T-Network Feedback

### Circuit Structure
- Replaces single feedback resistor Rf
- Three resistors: R2, R3, R4 forming T-network
- Located between output and inverting input

### Purpose
- Achieve high gain with moderate resistor values
- Avoid using very large resistors (which have noise/leakage issues)
- Useful for gains > 100

### Equivalent Feedback Resistance
- Req = R2 + R4 + (R2·R4/R3)
- Can be much larger than individual resistors
- Gain = -Req/R1

### Advantages Over Large Rf
- Better noise performance
- Reduced parasitic effects
- More practical component values
- Easier to implement on PCB

## Current-to-Voltage Converter (Transimpedance Amplifier)

### Circuit Structure
- Input current applied to inverting terminal
- Feedback resistor Rf from output to inverting input
- Non-inverting terminal grounded

### Output Voltage
- Vout = -If × Rf (where If is input current)
- Acts as current amplifier with voltage output
- Transimpedance gain = -Rf (in ohms)

### Applications
- Photodiode amplification
- Current measurement
- Sensor signal conditioning
- Low-level current detection

## Voltage-to-Current Converter

### Howland Current Pump
- Uses both inverting and non-inverting paths
- Balanced bridge configuration
- Load connected to ground
- Output current independent of load resistance

### Floating Load V-to-I
- Simple op-amp with feedback to inverting input
- Load in feedback path
- Iout = Vin/R1

### Grounded Load V-to-I
- Requires additional components
- Multiple op-amp circuits often needed
- Precision applications

## Integrator Circuit

### Basic Integrator
- Capacitor in feedback path (replaces Rf)
- Input through resistor R1
- Vout = -(1/R1C) × ∫Vin dt

### Practical Issues
- DC offset causes output saturation
- Need reset switch or DC feedback path
- Op-amp offset and bias currents cause drift

### Miller Integrator
- Uses Miller effect to multiply capacitance
- Improved linearity
- Better high-frequency performance

## Differentiator Circuit

### Basic Differentiator
- Capacitor at input (in series with R1)
- Feedback resistor Rf
- Vout = -RfC × dVin/dt

### Practical Issues
- High-frequency noise amplification
- Stability problems at high frequencies
- Need series resistor to limit bandwidth

### Practical Differentiator
- Series resistor with input capacitor
- Limits high-frequency gain
- Improves stability and noise performance

## ISRO Exam Key Points

### Virtual Ground vs Virtual Short
- Virtual ground: Node at 0V when non-inverting terminal is grounded
- Virtual short: V+ = V- (more general, applies to all negative feedback configs)

### Gain Stability
- Closed-loop gain depends on external components
- Insensitive to op-amp parameter variations (if AOL is large)
- Temperature stability depends on resistor temperature coefficients

### Bandwidth Considerations
- Gain-Bandwidth Product (GBP) is constant
- Higher closed-loop gain → lower bandwidth
- Av × BW = GBP (for voltage feedback op-amps)

### Input Bias Current Compensation
- Match DC resistance at both input terminals
- For inverting amp: R_comp = R1 || Rf
- For non-inverting amp: R_comp = R1 || Rf (at inverting input)
