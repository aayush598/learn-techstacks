# Binary Communication (Matched Filter, MAP) - Concepts

## Binary Signaling
- Transmit one of two symbols: binary 0 and binary 1
- Represented by waveforms s1(t) and s2(t)
- Remove: receiver decides 0 or 1 based on received r(t)

## Matched Filter
```
Optimal filter to detect known signal in white Gaussian noise
Impulse response: h(t) = s(T - t)  (time-reversed, shifted)
Output SNR maximized: SNR_out = 2E/N0
  E = energy of signal, N0 = noise PSD
Sampling at t=T gives:
  y(T) = integral s(tau)^2 dtau (autocorrelation at 0)
```

## Correlator Receiver
```
Equivalent to matched filter: multiply by s(t), integrate over symbol
y = integral r(t) s(t) dt  (correlate with s)
Decision: compare y to threshold
```

## MAP (Maximum A Posteriori) Decision
```
Choose symbol with max P(symbol | r)
For equal priors: MAP = ML (Maximum Likelihood)
Decision boundary: where likelihoods equal
```

## Decision Regions
- BPSK: threshold at 0 (two symmetric regions)
- Threshold depends on prior probabilities and costs
- For P(0)=P(1): threshold at midpoint

## Error Probability via Distances
```
For two antipodal signals (distance d between them):
  d = |s1 - s2| = sqrt(2E) for antipodal
  Pb = Q(d/(2 sigma)) with sigma = sqrt(N0/2)
  BPSK: Pb = Q(sqrt(2Eb/N0))
```

## Signal Space (Constellation)
```
Represent signals as points in orthonormal basis
BPSK: 2 points on a line at +sqrt(Eb), -sqrt(Eb)
Distance between points determines error
Minimum distance d_min is key
```

## Binary Hypothesis Testing
```
Test statistic: y
Decision rule: if y > gamma => "1", else "0"
gamma = threshold
Errors:
  P(false alarm) = P(decide 1 | transmit 0)
  P(miss) = P(decide 0 | transmit 1)
  P(e) = P0 * P(1|0) + P1 * P(0|1)
```

## ML vs MAP
```
ML: maximize P(r | s)  (ignores priors) 
   threshold at equal-distance point
MAP: maximize P(s | r) = P(r|s)P(s)/P(r)
   threshold shifts toward less-likely symbol
For equal priors, MAP = ML
```

## Energy Computation
```
Signal energy: E = integral |s(t)|^2 dt
Eb = energy per bit
For antipodal: d_min^2 = 4Eb
For orthogonal: d_min^2 = 2Eb (FSK)
Antipodal better by 3 dB for same Eb
```

## Noise Properties
```
White Gaussian noise: zero mean, N0/2 PSD
After matched filter (single sample): variance N0/2
```

---

## ISRO Key Points
- Matched filter maximizes SNR = 2E/N0
- Matched filter = correlator (equivalent)
- h(t) = s(T-t)
- Antipodal > orthogonal by 3 dB
- BPSK Pb = Q(sqrt(2Eb/N0))
- Equal priors -> ML = MAP
