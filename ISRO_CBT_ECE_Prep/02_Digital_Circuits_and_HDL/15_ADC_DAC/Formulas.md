# ADC and DAC - Formulas

## DAC Resolution / LSB
```
Step size (LSB) = Vref / 2^N
Full-scale (all 1s): Vout = Vref * (1 - 1/2^N)
```

## DAC Output Value
```
For N-bit code with value D (0..2^N-1):
  Vout = Vref * D / 2^N   (unipolar, 0 to Vref)
  Weighted/R-2R with op-amp: Vout = -Vref * D / 2^N
```

## Binary-weighted resistor values
```
R_0 = R (MSB), R_1 = 2R, R_2 = 4R, ..., R_{N-1} = 2^{N-1}R
Vout = -Vref * sum(bi / 2^i)  = -Vref*R_load*sum(bi/Ri)
```

## R-2R ladder current
```
I_out = (Vref/R) * sum(bi/2^i)   (each bit contributes Vref/(R 2^i))
With op-amp: Vout = -I_out * Rf = -Vref*(Rf/R)*sum(bi/2^i)
```

## Quantization error
```
Step = Vref/2^N
Max quantization error = +/- 0.5 LSB = +/- Vref/(2*2^N)
```

## SQNR (Signal to Quantization Noise)
```
SQNR = 6.02 * N + 1.76 dB   (full-scale sine input)
Each bit adds ~6 dB
```

## ADC resolution bits needed
```
To represent analog with step Vref/2^N:
  N = ceil(log2(Vref/step))
samples to represent V in 2^N levels
```

## Flash ADC resource
```
Comparators = 2^N - 1
Resistors for reference divider = 2^N
```

## SAR conversion time
```
t = N clock cycles (N bits)
```

## Dual-slope: input voltage relation
```
V_in = Vref * T_in / T_ref   (T_in fixed integration time)
Converts unknown input time proportional to V
```

## Sampling (Nyquist rate)
```
fs >= 2 * f_max  (minimum), fs = 2fmax = Nyquist rate
```

## Quick Reference
| Formula | Value |
|---------|-------|
| Step (LSB) | Vref/2^N |
| Vout | Vref*D/2^N |
| Quant error | +/-0.5 LSB |
| SQNR | 6.02N+1.76 dB |
| Flash comps | 2^N-1 |
| SAR time | N clocks |
| Nyquist | fs>=2fmax |
