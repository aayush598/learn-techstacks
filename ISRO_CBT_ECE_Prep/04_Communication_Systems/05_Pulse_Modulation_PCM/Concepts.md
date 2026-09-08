# PCM and Pulse Modulation - Concepts

## Pulse Modulation Types
1. **PAM** (Pulse Amplitude Modulation): Amplitude varies with signal
2. **PWM** (Pulse Width Modulation): Width varies with signal
3. **PPM** (Pulse Position Modulation): Position varies with signal
4. **PCM** (Pulse Code Modulation): Digital encoding (most important)

---

## PCM Process
1. **Sampling:** Sample analog signal at Nyquist rate (fs >= 2*fmax)
2. **Quantization:** Map to nearest quantization level (n bits -> 2^n levels)
3. **Encoding:** Convert quantization level to binary code

## Quantization
- n bits: 2^n quantization levels
- Step size: Delta = Vpp/(2^n) (peak-to-peak / levels)
- Quantization noise: Nq = Delta^2/12
- SQNR = 6.02*n + 1.76 dB (for full-scale sinusoidal)

## Signal-to-Quantization Noise Ratio
```
SQNR = 6.02n + 1.76 dB  [for sinusoid]
SQNR = 6.02n dB         [for uniform distribution]
Each additional bit: +6.02 dB
```

## Companding
- **A-law** (Europe, A=87.6): More uniform for small signals
- **mu-law** (North America, mu=255): More uniform for small signals
- Improves SQNR for low-amplitude signals
- Effective bits after companding: increased dynamic range

## PCM Bit Rate and Bandwidth
```
Bit rate: Rb = n * fs = n * 2 * fmax (bits/sec)
Minimum bandwidth: BW = Rb/2 = n * fmax (Sinc pulse)
Practical bandwidth: BW = Rb = 2*n*fmax (rectangular pulse)

Example: 8-bit PCM, 4kHz signal
  Rb = 8 * 8000 = 64 kbps
  BW_min = 32 kHz
  This is the standard telephone line (64 kbps)
```

## Differential PCM (DPCM)
- Encodes difference between samples (not absolute)
- Fewer bits needed for same quality
- Used in image/video compression

## Delta Modulation (DM)
- 1-bit quantization of the difference
- Slope overload: signal changes too fast
- Granular noise: constant small steps when signal is flat
- Slope overload condition: delta/Ts >= max slope of signal

---

## ISRO Key Points
- PCM: 6.02n + 1.76 dB is the key formula
- Nyquist rate links sampling and PCM
- Companding (A-law, mu-law) improves SQNR
- Standard telephone: 64 kbps (8kHz x 8 bits)
- Quantization noise is unavoidable error
