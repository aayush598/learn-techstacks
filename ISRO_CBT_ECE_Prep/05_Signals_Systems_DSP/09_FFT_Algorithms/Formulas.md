# DFT and FFT - Formulas

## DFT/IDFT
```
X[k] = Sum[n=0..N-1] x[n] W_N^(nk),   W_N = e^(-j2pi/N)
x[n] = (1/N) Sum[k=0..N-1] X[k] W_N^(-nk)
```

## Complexity
```
Direct DFT: N^2 complex multiplications
Radix-2 FFT: (N/2)*log2(N) complex mults, N*log2(N) adds
Stages: log2(N)
Butterflies total: (N/2)*log2(N)
```

## Complexity Table
```
N        Direct(N^2)      FFT((N/2)log2N)      Speedup
64       4096             192                  21x
256      65536            1024                 64x
1024     1,048,576        5120                 204x
4096     16,777,216       24576                682x
8192     67,108,864       53248                1260x
```

## Circular Convolution
```
y[n] = Sum[m=0..N-1] x1[m] x2[(n-m) mod N]
Y[k] = X1[k] X2[k]  (multiply DFTs)
Length of circular conv = N
Linear conv: L = N1 + N2 - 1
For linear via circular: zero-pad to N >= N1+N2-1
```

## Twiddle Factor Properties
```
W_N^k = e^(-j2pi k/N)
W_N^(k+N) = W_N^k  (period N)
W_N^(N/2) = -1
W_N^(N/4) = -j
W_N^k * W_N^m = W_N^(k+m)
```

## Butterfly (Radix-2 DIT)
```
Given inputs A (even) and B (odd):
  Output_real = A + W * B
  Output_low  = A - W * B
Per stage: N/2 butterflies
Bit-reversal ordering of input required for DIT, output for DIF
```

## Zero Padding
```
Zero-pad to next power of 2: N >= N_signal
Improves DFT frequency resolution:
  df = fs/N  (frequency spacing)
  Larger N -> finer resolution
```

## DTFT-DFT relation
```
DFT X[k] = DTFT X(e^jw) evaluated at w = 2pi k/N
DFT is the uniformly-sampled DTFT over one period
```

## Window Functions
```
Rectangular: w[n] = 1 (high sidelobes -13.3dB)
Hann: w[n] = 0.5(1-cos(2pi n/(N-1))), sidelobes -31.5dB
Hamming: w[n] = 0.54 - 0.46cos(...), -43dB
Blackman: -58dB (best sidelobe, widest main lobe)
Main lobe width trades with sidelobe level
```

## Quick Reference
| Parameter | Formula |
|-----------|---------|
| DFT mults | N^2 |
| FFT mults | (N/2)log2 N |
| FFT stages | log2 N |
| DFT period | N |
| Zero-pad for linear conv | N1+N2-1 |
| Freq resolution | fs/N |
