# ADC and DAC - Concepts

## Data Converters
- ADC: analog -> digital (quantize + sample)
- DAC: digital -> analog
- Key specs: resolution, speed, accuracy, error types

## DAC Types

### Weighted-Resistor (Binary-weighted) DAC
```
Each bit drives a weighted resistor (R, 2R, 4R, ...)
Op-amp sums currents
Simple, but wide range of resistor values (accuracy limit)
Vout = -Vref * (b0/1 + b1/2 + b2/4 + ...)
```

### R-2R Ladder DAC
```
Only R and 2R values (easy to match)
Better accuracy than binary-weighted
Most common ladder DAC
Vout = -Vref * sum(bi/2^i)
Current divides evenly, more precise
```

### Other DAC
- Current-output, multiplying DAC
- Delta-sigma (audio, high resolution)
- PWM DAC (simple but slow)

## DAC Resolution
```
Resolution = Vref / 2^N
  (LSB = smallest step = step size)
8-bit: 256 steps, Vref/256 each
N-bit: 2^N possible output levels
```

## DAC Output Formula (R-2R / weighted)
```
Vout = -Vref * (b_{N-1}/2^1 + b_{N-2}/2^2 + ... + b_0/2^N)
    = -Vref * (N-bit code)/2^N
Full scale (all 1s): -Vref(1-1/2^N)
n bit code value D: Vout = -Vref * D/2^N
```

## ADC Types

### Flash (Parallel) ADC
```
2^N - 1 comparators in parallel
Very fast (one conversion)
Expensive, high power (2^N comparators)
N-bit: needs 2^N-1 comparators, 2^N resistors
```

### Successive Approximation ADC (SAR)
```
Uses binary search, one comparator + DAC
N clocks per conversion (trial and error)
Good speed/resolution tradeoff (common 8-12 bit)
Most popular general purpose
```

### Dual-Slope / Integrating ADC
```
Integrate input for fixed time, then integrate known ref
High accuracy, slow (integrators)
Good noise rejection (averages)
Used in digital multimeters
```

### Sigma-Delta (Delta-Sigma) ADC
```
Oversampling + noise shaping + digital filter
Very high resolution, moderate speed
Audio, precision measurement
```

## ADC Conversion Time
```
Flash: ~1 clock (fastest)
SAR: N clock cycles
Dual-slope: slowest (2*integrating period)
Sigma-delta: many samples
```

## Quantization & Error
```
Quantization step (LSB) = Vref/2^N
Quantization error: +/- 0.5 LSB
Resolution sets precision
Non-linearity, offset, gain errors also
Signal-to-quantization-noise (SQNR) = 6.02N + 1.76 dB
```

## Sampling (per Nyquist)
```
Sample at >= 2x max frequency (aliasing avoided)
Anti-alias filter before ADC
Sample-and-hold preserves value during conversion
```

## ADC vs DAC comparison
| Spec | ADC | DAC |
|------|-----|-----|
| Direction | analog->digital | digital->analog |
| Comparators | flash has many | none |
| Reference | yes | yes |
| Application | measurement | generation |

---

## ISRO Key Points
- DAC: Vout = -Vref*D/2^N, step = Vref/2^N
- R-2R better than binary-weighted (2 resistor values)
- Flash: fastest, 2^N-1 comparators
- SAR: N clocks, moderate, common
- Dual-slope: accurate, slow
- SQNR = 6.02N + 1.76 dB
- Quantization error +/- 0.5 LSB
