# Digital Communication Systems - Formulas

## Link Budget
```text
Received power (free space):
  P_r = P_t G_t G_r (lambda/(4 pi R))^2

Path loss:
  L_fs(dB) = 20 log10(4 pi R/lambda)

Received SNR:
  SNR = P_r/(k T B F)
```

## Symbol, Bit, and Energy Quantities
```text
For an M-ary modulation:
  k = log2(M) bits/symbol
  R_s = R_b/k
  E_s = k E_b
  E_s/N0 = (R_b/B)(E_b/N0)   for uncoded transmission, where B is signal bandwidth
```

## PCM and Source Conversion
```text
PCM bit rate:
  R_b = f_s n

Telephone voice example:
  f_s = 8 kHz, n = 8
  R_b = 64 kb/s

Ideal uniform quantizer SQNR (full-scale sine):
  SQNR_dB = 6.02 n + 1.76
```

## Shannon Capacity
```text
AWGN channel:
  C = B log2(1 + S/N) = B log2(1 + SNR)

Spectral efficiency:
  eta = R_b/B
  eta <= log2(1 + SNR)   (for reliable uncoded transmission)
```

## BER of Coherent Binary Modulations
```text
BPSK:  P_b = Q(sqrt(2 E_b/N0))
QPSK:  P_b = Q(sqrt(2 E_b/N0))  (coherent, one bit per symbol-pair decision)
BFSK (coherent, orthogonal): P_b = 0.5 erfc(sqrt(E_b/N0))
```

## Matched Filter
```text
For a known signal s(t) in AWGN, the matched-filter impulse response is:
  h(t) = s*(T - t)

At the sampling instant t = T, the matched filter maximizes output SNR:
  (SNR)_max = 2E/N0    (real baseband signal convention)
```

## Multiple Access
```text
FDMA: separate users by frequency bands
TDMA: separate users by recurring time slots
CDMA: separate users by spreading codes
OFDMA: separate users by frequency-time subcarriers
```

## Link Performance Metrics
```text
Throughput = successful payload bits per unit time

Outage probability:
  P_out = P(SNR < SNR_threshold)
```

## Coding and Redundancy
```text
Code rate:
  R_c = k/n

Channel coding:
  n > k for a practical error-control code
  Adds redundancy to improve power efficiency at the cost of bandwidth efficiency
```

## Quick Reference
| Quantity | Formula |
|----------|---------|
| Shannon capacity | C = B log2(1 + SNR) |
| M-ary spectral efficiency | log2(M) bits/symbol maximum ideal |
| PCM rate | f_s n |
| Eb/N0 to Es/N0 | Es/N0 = (Rb/B) Eb/N0 |
| BPSK BER | Q(sqrt(2Eb/N0)) |
| Matched filter | h(t) = s*(T-t) |
| Free-space path loss | 20log10(4piR/lambda) |
| SQNR | 6.02n + 1.76 dB |
