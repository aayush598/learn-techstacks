# Communication Systems - Complete Formula Sheet

## AM Modulation
```
Standard AM:  s(t) = Ac[1+mu*cos(2*pi*fm*t)]*cos(2*pi*fc*t)
DSB-SC:       s(t) = Ac*Am*cos(2*pi*fm*t)*cos(2*pi*fc*t)
SSB:          s(t) = (Ac*Am/2)*cos(2*pi*(fc+/-fm)*t)

Modulation index: mu = Am/Ac (0 <= mu <= 1 for envelope detection)
Power: Ptotal = Pc(1+mu^2/2) where Pc = Ac^2/2
Sideband power: Psb = Pc*mu^2/2
Efficiency: eta = mu^2/(2+mu^2)
For mu=1: eta = 1/3 = 33.3%

Multi-tone AM: mu_eff = sqrt(mu1^2+mu2^2+...)
Over-modulation: mu > 1 (envelope distortion)
```

## FM Modulation
```
Frequency deviation: delta_f = kf*Am
Modulation index: beta = delta_f/fm
Carson's rule: BW = 2*(delta_f+fm) = 2*fm*(beta+1)
NBFM: beta << 1, BW approximately 2*fm
WBFM: beta >> 1, BW approximately 2*delta_f

Power in FM: Pt = Ac^2/2 (constant, same as unmodulated)
SINAD = (Signal+Noise+Distortion)/(Noise+Distortion)
```

## PCM
```
SQNR (dB) = 6.02*n + 1.76 (sinusoidal input)
For n bits: 2^n levels, Delta = Vpp/2^n
Quantization noise: Nq = Delta^2/12

PCM bit rate: Rb = n*fs (bits/sec)
Minimum bandwidth: BW_min = Rb/2 = n*fs/2
T1 carrier: 24 channels, 1.544 Mbps
E1 carrier: 32 channels, 2.048 Mbps
```

## Sampling
```
Nyquist rate: fs >= 2*fmax
Aliasing: fs < 2*fmax
Oversampling: fs >> 2*fmax
Reconstruction BW: fmax < BW < fs-fmax
```

## Information Theory
```
Entropy: H(X) = -Sum P(xi)*log2(P(xi))
Mutual information: I(X;Y) = H(X) - H(X|Y)
Channel capacity: C = max I(X;Y)
Shannon-Hartley: C = B*log2(1+SNR) (AWGN channel)
For BSC: C = 1-H(p) where p = error probability
```

## Noise
```
Thermal noise: N = kTB (k=1.38e-23 J/K)
Noise figure: F = SNR_in/SNR_out (linear)
NF(dB) = 10*log10(F)
Noise temperature: Te = (F-1)*T0 (T0=290K)
Cascaded: F = F1+(F2-1)/G1+(F3-1)/(G1*G2)
Friis for noise: F_total = F1+(F2-1)/G1
```

## Digital Modulation
```
BPSK:  Pe = Q(sqrt(2*Eb/N0))
QPSK:  Pe = Q(sqrt(2*Eb/N0)) (same BW as BPSK, double data rate)
8-PSK: Pe = 2*Q(sqrt(2*Eb/N0)*sin(pi/8))
16-QAM: Pe approximately 3*Q(sqrt(Eb/(5*N0)))
M-QAM:  Pe = 4*(1-1/sqrt(M))*Q(sqrt(3*Eb/((M-1)*N0)))
BFSK:   Pe = Q(sqrt(Eb/N0))
```

## Huffman Coding
```
Average code length: L = Sum P(xi)*li
H <= L < H+1 (entropy bounds)
Efficiency: eta = H/L * 100%
```

## Eye Diagram
```
Eye opening: signal quality indicator
Noise margin: maximum noise without error
Timing jitter: variation in zero crossing
Optimal sampling: at maximum eye opening
```
