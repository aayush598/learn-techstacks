# Binary Communication - Formulas

## Matched Filter
```
h(t) = s(T - t)   (time reversed signal)
Maximum output SNR: SNR_max = 2E/N0
y(T) = integral[0,T] r(tau) s(tau) dtau  (correlator)
```

## Energy
```
E_signal = integral |s(t)|^2 dt
E_b = energy per bit
```

## Error Probabilities
```
Antipodal (BPSK):
  d = sqrt(4 Eb) = 2sqrt(Eb)
  Pb = Q(sqrt(2 Eb/N0))
Orthogonal (FSK):
  d = sqrt(2 Eb)
  Pb = Q(sqrt(Eb/N0))
Center-line threshold (equal priors):
  gamma = 0 for antipodal symmetric
```

## Hypothesis Test
```
Test: y = integral r s dt
Decision:
  y > gamma : decide s1
  y < gamma : decide s0
P(e) = P0 * Q((gamma - mu0)/sigma) + P1 * Q((mu1 - gamma)/sigma)
  (Gaussian noise case)
```

## MAP vs ML Threshold
```
Equal priors: gamma = (mu0+mu1)/2  (midpoint)
Unequal priors (MAP):
  gamma = (N0/2d) ln(P1/P0) + midpoint
  Threshold shifts toward less probable symbol
```

## Noise Statistics
```
White Gaussian: E[n(t)]=0, N0/2 PSD
After filter/coherent: variance = N0/2 (single decision sample)
```

## Signal Space Distance
```
d_ij = ||s_i - s_j|| = sqrt(E_i + E_j - 2 rho sqrt(Ei Ej))
  rho = correlation coefficient
Antipodal: rho = -1, d = 2sqrt(E)
Orthogonal: rho = 0, d = sqrt(2E)
On-off (OOK): rho=0, but half energy, d=sqrt(E)
```

## Union Bound (M-ary)
```
Ps <= (M-1) Q(d_min / (2 sigma))
```

## Quick Reference
| Scheme | d^2/Eb | Pb |
|--------|--------|-----|
| Antipodal | 4 | Q(sqrt(2Eb/N0)) |
| Orthogonal | 2 | Q(sqrt(Eb/N0)) |
| On-off | 2 (with E per bit) | ~Q(sqrt(Eb/N0)) |

## Correlator Receiver structure
```
r(t) -> multiply by s(t) -> integrate 0..T -> sample -> threshold -> decide
Equivalent to matched filter (h=s(T-t))
```
