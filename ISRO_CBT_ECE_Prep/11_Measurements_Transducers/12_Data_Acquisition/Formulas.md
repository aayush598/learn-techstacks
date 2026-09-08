# Data Acquisition - Formulas

## 1. Nyquist Theorem
```
fs_min = 2 * fmax

where:
fs = sampling frequency
fmax = highest frequency component in signal
```

## 2. Aliasing Frequency
```
f_alias = |fs - f_signal|  or  |n*fs +/- f_signal|

Aliased frequency appears at incorrect lower frequency
```

## 3. Quantization Error
```
QE = +/- 1/2 LSB = +/- Vfs / (2^(n+1))

where:
Vfs = full-scale voltage
n = number of bits
```

## 4. Signal-to-Noise Ratio (Quantization)
```
SNR = 6.02n + 1.76 dB  (for full-scale sinusoid)

where n = number of bits
For 12-bit: SNR = 72.24 + 1.76 = 74 dB
For 16-bit: SNR = 96.32 + 1.76 = 98 dB
```

## 5. Effective Number of Bits (ENOB)
```
ENOB = (SNR_actual - 1.76) / 6.02

ENOB <= n (actual resolution)
```

## 6. Sampling Rate and Reconstruction
```
For good reconstruction:
fs >= 10 * fmax (practical rule)
fs >= 2 * fmax (Nyquist minimum)

Reconstruction filter cutoff: fc = fs/2
```

## 7. Oversampling Advantage
```
SNR improvement = 10 * log10(oversampling_ratio) dB

Oversampling ratio (OSR) = fs / (2 * fmax)
Doubling OSR: SNR improves by 3 dB (0.5 bit)
```

## 8. Channel Scanning Rate
```
Effective rate per channel = ADC_rate / N_channels

For 100 kSPS ADC, 8 channels:
Each channel gets 12.5 kSPS
```

## 9. Anti-Aliasing Filter Design
```
Cutoff frequency: fc = fs/2 = fmax (at Nyquist)
Filter order: Higher = sharper roll-off

Butterworth: maximally flat passband
Bessel: maximally flat group delay (preserves waveform)
```

## 10. Aperture Time Effect
```
Error due to aperture uncertainty:
dV = dV/dt * t_aperture

For 10 mV/ns signal, 100 ps aperture:
Error = 10mV/ns * 0.1ns = 1 mV
```

## 11. Hold Mode Error
```
Droop: dV/dt = I_leak / C_hold

For I_leak = 1 nA, C_hold = 100 pF:
Droop = 1nA/100pF = 10 V/s
```

## 12. DAQ System Resolution
```
LSB = Vfs / 2^n

For Vfs = 10V, n = 12:
LSB = 10/4096 = 2.44 mV

For n = 16:
LSB = 10/65536 = 0.153 mV
```

## 13. Maximum Input Frequency
```
fmax = fs / 2 (Nyquist limit)
fmax = fs / 10 (practical with simple filter)
fmax = fs / 5 (with good anti-aliasing filter)
```

## 14. Throughput Rate
```
Throughput = 1 / (conversion_time + overhead)

For DAQ card:
Total throughput = Channels x Samples/sec
```

## Key Formulas for ISRO MCQs
| Quantity | Formula |
|----------|---------|
| Nyquist | fs >= 2*fmax |
| Quantization noise | SNR = 6.02n + 1.76 dB |
| QE | +/- Vfs/2^(n+1) |
| ENOB | (SNR-1.76)/6.02 |
| Anti-alias fc | fc = fs/2 |
| LSB | Vfs/2^n |
| Oversampling SNR | 3 dB per doubling |
