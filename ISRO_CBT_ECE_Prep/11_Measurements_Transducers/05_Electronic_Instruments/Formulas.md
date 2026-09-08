# Electronic Instruments - Formulas

## 1. DVM Resolution
```
Resolution = Full Scale / (10^n - 1)  for n½ digit display
Example: 3½ digit → max = 1999, resolution = 1/1999 of range

Resolution (V) = Range / (Number of counts)
For 2V range, 3½ digit: 2/2000 = 1 mV
```

## 2. Ramp Type DVM
```
V_in = V_ramp × (t_count / t_ramp)
V_ramp = V_max / t_ramp
Count = f_clk × t_count
```

## 3. Dual Slope ADC
```
Phase 1: V_c = (V_in × T₁)/(RC)
Phase 2: 0 = V_c - (V_ref × T₂)/(RC)

Result: D = T₂/T₁ × (V_ref/V_ref) 
     or: D = (f_clk × T₂) = T₁ × V_in/V_ref

Resolution: N = T₁ × f_clk
Output count: n = (V_in/V_ref) × N
```

## 4. Dual Slope Noise Rejection
```
For power line rejection:
T₁ = k × (1/f_line)    where k = integer

For 50 Hz: T₁ = 20ms, 40ms, 60ms...
For 60 Hz: T₁ = 16.67ms, 33.33ms...
```

## 5. Successive Approximation ADC
```
Conversion time = n × T_clk  (n = number of bits)
Resolution = V_ref / 2^n

For 12-bit, V_ref = 10V:
Resolution = 10/4096 = 2.44 mV
```

## 6. True RMS
```
V_rms = √(1/T ∫₀ᵀ v²(t) dt)

For sinusoidal: V_rms = V_peak / √2 = 0.707 × V_peak
For square: V_rms = V_peak
For triangular: V_rms = V_peak / √3

Crest factor = V_peak / V_rms
Form factor = V_rms / V_avg
```

## 7. Frequency Counter
```
f = N / T_gate

Resolution = 1 / T_gate
For 1s gate: 1 Hz resolution
For 0.1s gate: 10 Hz resolution

Period measurement: T = N × T_clk
```

## 8. ADC Conversion Comparison
```
Ramp:     t_conv = V_in / (slew rate)
Dual Slope: t_conv = T₁ + T₂ = T₁(1 + V_in/V_ref)
Successive:  t_conv = n × T_clk
Flash:     t_conv = T_clk (single clock)
```

## 9. DVM Accuracy
```
Accuracy = ±(a% of reading + b% of range + c counts)

Example: ±(0.05% of reading + 0.02% of range + 1 digit)
For 10V range, reading 5.000V:
Error = 0.05%×5 + 0.02%×10 + 0.001 = 2.5mV + 2mV + 1mV = 5.5mV
```

## 10. Input Impedance Effect
```
Loading error = R_source / (R_source + R_input) × 100%
For DVM: R_input = 10MΩ typical
For 1MΩ source: Error = 1M/(1M+10M) × 100 = 9.09%
```

## 11. Conversion Time Comparison
```
Ramp (8-bit): ~256 clock cycles (slowest)
Dual Slope (3½ digit): ~20ms + conversion (slow, accurate)
Successive (12-bit): 12 clock cycles (fast)
Flash (8-bit): 1 clock cycle (fastest)
```

## 12. Digital Instrument Display
```
3½ digit: displays 0 to 1999
4 digit: displays 0 to 9999
4½ digit: displays 0 to 19999

Half digit: can only be 0 or 1
```

## 13. Quantization Error
```
Quantization error = ± 1/2 LSB = ± Resolution/2
For V_ref = 10V, 12-bit: ± 1.22 mV
```

## Key Formulas for ISRO MCQs
| Quantity | Formula |
|----------|---------|
| Dual slope output | n = (V_in/V_ref) × N |
| Successive approx time | t = n × T_clk |
| Frequency counter | f = N/T_gate |
| DVM accuracy | ±(a% reading + b% range + c counts) |
| Resolution | Range / (10^n - 1) |
| True RMS | V_rms = √(avg(v²)) |
