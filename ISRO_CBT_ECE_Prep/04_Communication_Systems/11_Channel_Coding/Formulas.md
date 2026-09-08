# Channel Coding - Formulas

## Code Parameters
```
(n,k) block code
  k = information bits per block
  n = total bits per codeword
  r = n - k = parity/redundancy bits
  R = k/n code rate
  d_min = min Hamming distance
```

## Detection / Correction Capability
```
Detect up to (d_min - 1) errors
Correct up to floor((d_min - 1)/2) errors    [t]
Detect AND correct combined: t detect + t+1 ... 
Sphere packing (Hamming) bound for t-error correcting:
  Sum[i=0..t] C(n,i) * 2^k <= 2^n
```

## Hamming Code
```
For single-error-correcting Hamming (m parity bits):
  n = 2^m - 1
  k = n - m = 2^m - 1 - m
  (7,4): m=3 -> n=7, k=4, d_min=3
  (15,11): m=4 -> n=15, k=11
  (31,26): m=5
Minimum parity for k info bits: smallest m with 2^m >= k+m+1
```

## Syndrome Decoding
```
Codeword: c = m G (G = generator matrix)
Received: r = c + e (e = error vector)
Syndrome: s = H r^T
  H = parity check matrix ((n-k) x n)
  If s = 0: no error (or undetectable)
  s = H e^T (depends on error only)
Correct: use syndrome lookup to find e, then c = r + e
Valid codeword condition: H c^T = 0
```

## Hamming Distance (d)
```
For two codewords x, y:
  d(x,y) = number of positions where they differ
  d_min = min over all distinct pairs
Parity check matrix columns must be distinct & nonzero for 1-error correct
```

## Code Rate
```
R = k/n
For (7,4): R = 4/7 = 0.571
For (15,11): R = 11/15 = 0.733
For (31,26): R = 26/31 = 0.839
Higher rate = less redundancy = more efficiency but less protection
```

## CRC (Cyclic)
```
Message polynomial M(x) * x^r / G(x) (generator degree r)
CRC = remainder R(x) of length r
Transmitted: M(x)x^r + R(x)
Detect: division remainder 0 if no error
Generator examples: CRC-16 (x16+x15+x2+1), CRC-32
```

## Viterbi (Convolutional)
```
Decoding = shortest path through trellis
Complexity: O(2^K * N) states
K = constraint length
```

## Quick Reference
| Code | n | k | d_min | taps |
|------|---|---|-------|------|
| Hamming(7,4) | 7 | 4 | 3 | 1 |
| Hamming(15,11) | 15 | 11 | 3 | 1 |
| Hamming(31,26) | 31 | 26 | 3 | 1 |

## Formula Recap
```
R = k/n
t = floor((d_min-1)/2)
detect = d_min - 1
2^m >= n+1  (single error, n = 2^m -1)
```
