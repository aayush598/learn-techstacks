# Op-Amp Non-Linear Circuits - Concepts

## Comparators

### Basic Comparator
- Op-amp operating in open-loop (no feedback)
- Compares two input voltages
- Output saturates to +Vsat or -Vsat
- Very high gain causes output to switch rapidly

### Inverting Comparator
- Reference voltage at non-inverting terminal (+)
- Input signal at inverting terminal (-)
- When Vin > Vref: output = -Vsat
- When Vin < Vref: output = +Vsat

### Non-Inverting Comparator
- Reference voltage at inverting terminal (-)
- Input signal at non-inverting terminal (+)
- When Vin > Vref: output = +Vsat
- When Vin < Vref: output = -Vsat

### Comparator vs Op-Amp
- Comparators are optimized for switching speed
- Op-amps can be used as comparators but slower
- Dedicated comparators have faster response time
- Output stages may differ (open-collector vs push-pull)

### Propagation Delay
- Time between input crossing and output switching
- Typically 100ns to 1μs for general-purpose comparators
- Faster comparators: 10-50ns
- Important for high-frequency applications

## Zero-Crossing Detector

### Circuit Configuration
- Reference voltage = 0V (ground)
- Input signal applied to one input
- Output switches when input crosses zero

### Inverting Zero-Crossing Detector
- Input to inverting terminal
- Non-inverting terminal grounded
- Output: +Vsat when Vin < 0, -Vsat when Vin > 0

### Non-Inverting Zero-Crossing Detector
- Input to non-inverting terminal
- Inverting terminal grounded
- Output: +Vsat when Vin > 0, -Vsat when Vin < 0

### Applications
- Frequency measurement
- Phase detection
- AC zero-crossing switching
- Waveform conversion (sine to square)

## Schmitt Trigger (Hysteresis Comparator)

### Why Hysteresis Needed
- Noise on input causes multiple output transitions
- Comparator "chatters" near threshold
- Hysteresis provides noise immunity
- Two different threshold voltages: UTP and LTP

### Inverting Schmitt Trigger
- Positive feedback through voltage divider
- Input to inverting terminal
- Non-inverting terminal gets fraction of output

### Upper Threshold Point (UTP)
- Threshold when output is +Vsat
- UTP = +Vsat × R1/(R1 + R2)
- Input must rise above UTP to switch output

### Lower Threshold Point (LTP)
- Threshold when output is -Vsat
- LTP = -Vsat × R1/(R1 + R2)
- Input must fall below LTP to switch output

### Hysteresis Width
- H = UTP - LTP = 2 × Vsat × R1/(R1 + R2)
- Larger hysteresis = better noise immunity
- Trade-off: reduced sensitivity

### Non-Inverting Schmitt Trigger
- Input through resistor to non-inverting terminal
- Feedback to non-inverting terminal
- Similar UTP/LTP calculations

## Window Comparator

### Circuit Structure
- Two comparators in parallel
- Upper reference (VrefHigh) and lower reference (VrefLow)
- Output indicates if input is within window

### Operating Principle
- When Vin < VrefLow: one comparator triggers
- When Vin > VrefHigh: other comparator triggers
- When VrefLow < Vin < VrefHigh: output in one state

### Output Logic
- Typically active-low outputs with AND gate
- Window detected when both comparators agree
- Can use open-collector outputs for wired-AND

### Applications
- Voltage monitoring
- Over/under voltage detection
- Battery voltage monitoring
- Process control limits

## Phase-Locked Loop (PLL) Building Blocks

### Phase Detector
- Compares input and VCO frequencies
- Output proportional to phase difference
- Types: XOR, multiplier, edge-triggered

### Low-Pass Filter
- Smooths phase detector output
- Controls loop dynamics
- Sets bandwidth and stability

### Voltage-Controlled Oscillator (VCO)
- Output frequency proportional to input voltage
- Center frequency set by external components
- Tuning range depends on control voltage

## Analog Switches

### Transmission Gate
- CMOS parallel N and P channel FETs
- Bidirectional switch
- Low on-resistance
- Used in sample-and-hold circuits

### Charge Injection
- Clock feedthrough in switched circuits
- Causes voltage errors in S/H
- Minimized by complementary switches

## Sample-and-Hold Circuits

### Basic Operation
- Sample mode: capacitor charges to input voltage
- Hold mode: capacitor maintains voltage
- Op-amp buffers for input and output

### Key Parameters
- Acquisition time: time to charge capacitor
- Hold droop: voltage decay during hold
- Feedthrough: signal leakage during hold

## ISRO Exam Key Points

### Comparator vs Schmitt Trigger
- Comparator: single threshold, susceptible to noise
- Schmitt trigger: two thresholds, noise immune
- Always prefer Schmitt trigger for noisy signals

### Threshold Calculations
- UTP = +Vsat × R1/(R1+R2) for inverting Schmitt trigger
- LTP = -Vsat × R1/(R1+R2) for inverting Schmitt trigger
- For non-inverting: UTP = Vsat × R2/(R1+R2) + Vin × R1/(R1+R2)

### Common ISRO Patterns
- Questions on UTP/LTP calculations
- Hysteresis width problems
- Window comparator output states
- Zero-crossing detector applications

### Practical Considerations
- Comparator response time affects maximum frequency
- Op-amp slew rate limits switching speed
- Hysteresis reduces accuracy but improves stability
- Reference voltage stability affects threshold accuracy
