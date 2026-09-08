# Electronic Instruments - Concepts

## 1. Digital Voltmeter (DVM)

### 1.1 Basic Operation
Converts analog voltage to digital display using ADC.
Key components: Input attenuator → ADC → Decoder → Display

### 1.2 Characteristics
- Resolution: 1/2^n (n = number of bits) or 1/(10^digits - 1)
- Accuracy: ±(% of reading) ± (number of digits)
- Input impedance: Very high (10MΩ typical)

## 2. Ramp Type DVM

### 2.1 Principle
Compare input voltage with a linear ramp voltage.
Counter counts time for ramp to reach input level.

### 2.2 Operation
- Start: Ramp begins from zero, counter starts
- Comparator: Compares V_in with ramp
- Stop: When ramp crosses V_in, counter stops
- Count is proportional to V_in

### 2.3 Limitations
- Requires very linear ramp
- Slow conversion time (depends on input voltage)
- Accuracy limited by ramp linearity

## 3. Dual Slope ADC (Integrating DVM)

### 3.1 Principle
Two phases: Integration of unknown, then integration of reference.
Count is independent of R, C values (cancels out).

### 3.2 Operation
- Phase 1 (T₁): Integrate V_in for fixed time T₁
  V_c = (V_in × T₁)/(RC)
- Phase 2 (T₂): Integrate -V_ref until V_c = 0
  Count during T₂ gives digital output
- Result: D = T₂ × f_clk = T₁ × (V_in/V_ref)

### 3.3 Advantages
- High accuracy (independent of R, C drift)
- Excellent noise rejection (integrates over T₁)
- Auto-zero capability
- Used in precision DVMs (5½ digit)

### 3.4 Noise Rejection
If T₁ = integration period = n × (1/f_line), power line noise integrates to zero.
Common: T₁ = 20ms (one cycle of 50Hz) or 16.67ms (60Hz)

## 4. Successive Approximation ADC

### 4.1 Principle
Binary search algorithm: tests each bit from MSB to LSB.
Uses DAC and comparator.

### 4.2 Operation
- Start with MSB = 1, all others 0
- If DAC output > V_in, set bit to 0
- If DAC output < V_in, keep bit at 1
- Repeat for each bit down to LSB

### 4.3 Speed
Conversion time = n clock cycles (n = resolution in bits)
Much faster than ramp type.
Typical: 8-bit → 8 clocks, 12-bit → 12 clocks

### 4.4 Resolution
- 8-bit: 256 levels
- 12-bit: 4096 levels
- 16-bit: 65536 levels

## 5. True RMS Converter

### 5.1 Purpose
Measures RMS value of ANY waveform (not just sinusoidal).

### 5.2 Method
- Thermal conversion: Heat unknown AC → compare with DC heating
- Log-antilog computation: Electronic RMS calculation
- Block diagram: Input → True RMS-to-DC converter → DC output

### 5.3 Formula
```
V_rms = √(1/T ∫₀ᵀ v²(t) dt)
Crest factor = V_peak / V_rms
Form factor = V_rms / V_avg
```

## 6. Frequency Counter

### 6.1 Principle
Counts number of input cycles in a precise time interval (gate time).

### 6.2 Operation
- Gate opens for precise time T (from time base)
- Input signal triggers counter
- Frequency = Count / T

### 6.3 Resolution
- Resolution = 1/Gate time
- For 1s gate: 1 Hz resolution
- For 0.1s gate: 10 Hz resolution

### 6.4 Time Base
Crystal oscillator (typically 10 MHz) provides accurate time reference.

## 7. Comparison of ADC Types
| Type | Speed | Accuracy | Complexity | Application |
|------|-------|----------|------------|-------------|
| Ramp | Slow | Moderate | Low | Basic DVM |
| Dual Slope | Slow | High | Medium | Precision DVM |
| Successive Approx | Fast | High | Medium | General ADC |
| Flash | Very fast | Moderate | High | Video, oscilloscope |

## 8. Digital Instrument Specifications
- Resolution: Number of display digits
- Accuracy: ±(% reading + % range)
- Linearity: Integral and differential
- Conversion time: Time for one measurement
- Input impedance: Typically 10MΩ for DVM

## 9. ISRO Focus Areas
- Dual slope ADC operation (integration phases)
- Successive approximation algorithm
- True RMS measurement principle
- DVM resolution and accuracy specifications
- Frequency counter gate time and resolution
