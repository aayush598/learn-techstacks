# DFT and FFT - Concepts

## Discrete Fourier Transform (DFT)
```
X[k] = Sum[n=0 to N-1] x[n] e^(-j 2pi kn/N),  k=0..N-1
x[n] = (1/N) Sum[k=0 to N-1] X[k] e^(j 2pi kn/N), n=0..N-1
```
- Samples the DTFT at N equally spaced frequencies
- Periodicity: X[k+N] = X[k], x[n+N] = x[n] (inherently periodic)
- Matrix: X = W x where W is DFT matrix

## Twiddle Factor
```
W_N = e^(-j 2pi/N)
X[k] = Sum x[n] W_N^(kn)
Properties: W_N^(k+N) = W_N^k, W^(N/2) = -1, etc.
```

## FFT (Fast Fourier Transform)
- Divide-and-conquer on DFT
- **Radix-2 DIT** (Decimation In Time): split even/odd samples
- **Radix-2 DIF** (Decimation In Frequency): split halves
- Complexity: O(N log2 N) vs O(N^2) direct

### Number of Operations
```
Direct DFT: N^2 complex multiplications, N(N-1) additions
Radix-2 FFT: (N/2)*log2(N) complex multiplications
  N/2 butterflies per stage, log2(N) stages
Complex additions: N*log2(N)
```
For N=1024:
- Direct: 1,048,576 multiplications
- FFT: 5120 multiplications (200x faster)

## Butterfly Structure
```
Each butterfly: 
  X0' = X0 + W_N^m X1
  X1' = X0 - W_N^m X1
One complex multiply + two complex adds

Bit-reversal input order (for DIT)
3 stages for N=8, 4 stages for N=16
```

## FFT Size Requirements
- N = 2^m always for radix-2
- Work with N as power of 2 (zero-pad if needed)
- Number of stages = log2(N)

## DFT Properties
| Property | DFT |
|----------|-----|
| Linearity | Sum of DFTs |
| Circular shift | phase shift with e^(-j2pi km/N) |
| Circular convolution | X1[k]*X2[k] |
| Time reversal | X[-k mod N] |
| Parseval | (1/N)Sum|X[k]|^2 |

## Circular vs Linear Convolution
```
Circular convolution length: N
Linear convolution length: N1 + N2 - 1
For linear = circular: N >= N1 + N2 - 1 (zero-pad)
Overlap-save/Overlap-add methods: compute linear conv using circular
```

## Leakage & Windowing
- Finite data -> rectangular window -> spectral leakage
- Leakage: energy spread to neighboring frequencies
- Solution: window functions (Hamming, Hann, Blackman) reduce sidelobes
- Trade-off: wider main lobe (worse resolution)

## Applications
- Spectral analysis
- Fast convolution (filtering) via FFT
- OFDM (uses IFFT/FFT)
- Radar/sonar signal processing

---

## ISRO Key Points
- FFT ops: (N/2)*log2(N) mults - MOST TESTED
- N=1024 -> 10 stages
- Circular conv = linear conv with zero-padding to N>=N1+N2-1
- Twiddle factor W_N = e^(-j2pi/N)
- Bit reversal for DIT FFT
