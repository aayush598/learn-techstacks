# Communication Systems - Formulas

## Amplitude Modulation
```
Standard AM: s(t) = Ac[1 + mu* cos(2*pi*fm*t)] cos(2*pi*fc*t)
Modulation index: mu = Am/Ac
Power: Ptotal = Pc(1 + mu^2/2)
  Pc = Ac^2/2 (carrier power)
  PUSB = PLSB = Pc*mu^2/4 (each sideband)
  Psb = Pc*mu^2/2 (total sideband power)
  Efficiency: eta = mu^2/(2+mu^2) * 100%

DSB-SC: s(t) = Ac*Am*cos(2*pi*fm*t)*cos(2*pi*fc*t)
  No carrier, efficiency = 100%

SSB: Only one sideband transmitted
  Bandwidth = fm (half of AM)
```

## FM Modulation
```
Frequency deviation: delta_f = kf * Am
Modulation index: beta = delta_f / fm = kf*Am/fm
Carson's rule: BW = 2*(delta_f + fm) = 2*fm*(beta+1)
For NBFM: beta << 1, BW approximately 2*fm
For WBFM: beta >> 1, BW approximately 2*delta_f

Multi-tone FM: beta_eff = sqrt(beta1^2 + beta2^2 + ...)
```

## PCM and Quantization
```
SQNR (dB) = 6.02*n + 1.76 (n = bits, for sinusoidal input)
For n bits: L = 2^n quantization levels
Step size: Delta = Vpp/(2^n)
Quantization noise power: Delta^2/12

Companding:
  A-law: y = A*x/(1 + ln(A*|x|)) for small x
  mu-law: y = ln(1 + mu*|x|)/ln(1+mu)
  Standard: A=87.6, mu=255
```

## Sampling Theorem
```
Nyquist rate: fs >= 2*fmax
Aliasing occurs when: fs < 2*fmax
Reconstruction: Low-pass filter with cutoff = fmax, passband = fs/2
```

## Information Theory
```
Self-information: I(x) = -log2(P(x))
Entropy: H(X) = -Sum P(xi)*log2(P(xi))
Channel capacity (AWGN): C = B*log2(1 + SNR) (Shannon-Hartley)
For binary: C_max = 1 bit/symbol
```

## Noise Analysis
```
Noise figure: F = SNR_in/SNR_out (linear)
Noise temperature: Te = (F-1)*T0 where T0 = 290K
Cascaded noise figure: F_total = F1 + (F2-1)/G1 + (F3-1)/(G1*G2)
Thermal noise power: N = k*T*B (k = 1.38e-23)
```

## Digital Modulation Error Probability
```
BPSK: Pe = Q(sqrt(2*Eb/N0))
QPSK: Pe = Q(sqrt(2*Eb/N0)) (same as BPSK)
M-PSK: Pe approximately 2*Q(sqrt(2*Eb/N0)*sin(pi/M))
QAM (square M): Pe approximately 4*(1-1/sqrt(M))*Q(sqrt(3*Eb/(M-1)*N0))
```

## Huffman Coding
```
Code length: L = Sum P(xi)*li
Entropy: H <= L < H+1
Efficiency: eta = H/L * 100%
Average code length is between H and H+1 bits
```

## Quick Reference
| Parameter | Formula | Key Point |
|-----------|---------|-----------|
| AM efficiency | mu^2/(2+mu^2) | Max 33.3% at mu=1 |
| FM BW (Carson) | 2(delta_f+fm) | Beta+1 rule |
| SQNR | 6.02n+1.76 dB | Per extra bit: +6dB |
| Shannon | C = B*log2(1+SNR) | Max data rate |
| BPSK Pe | Q(sqrt(2Eb/N0)) |相干 detection |
| Noise figure | F = SNR_in/SNR_out | dB = 10*log10(F) |
