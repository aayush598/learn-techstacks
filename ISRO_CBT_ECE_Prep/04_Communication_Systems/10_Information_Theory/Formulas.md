# Information Theory and Source Coding - Formulas

## Information & Entropy
```
I(xi) = log2(1/pi) = -log2(pi)  [information of event, bits]
H(X) = -Sum pi*log2(pi)  [entropy, bits/symbol]
H_max = log2(M)  [equiprobable, M symbols]
Redundancy = H_max - H
```

## Two-Symbol Source
```
H = -p*log2(p) - (1-p)*log2(1-p)
  p = 0.5: H = 1 (max)
  p = 0 or 1: H = 0
```

## Three-Symbol Source (e.g. 0.5, 0.25, 0.25)
```
H = -0.5*log2(0.5) - 0.25*log2(0.25) - 0.25*log2(0.25)
  = 0.5 + 0.5 + 0.5 = 1.5 bits/symbol
H_max = log2(3) = 1.585 bits
```

## Source Coding Bounds
```
H <= L_avg < H+1  (Huffman)
L_avg = Sum pi*li  (avg code length)
Kraft: Sum 2^(-li) <= 1
```

## Mutual Information
```
I(X;Y) = H(X) - H(X|Y)
I(X;Y) = H(Y) - H(Y|X)
I(X;Y) = H(X) + H(Y) - H(X,Y)
For BSC: I = 1 - H(p)
```

## Channel Capacity
```
Shannon: C = B*log2(1+SNR)  bps
  For small SNR: C ~ B*SNR/ln2 (linear in SNR)
BSC: C = 1 - H(p)  bits/channel
M-ary orthogonal: stays ~log2(M)
```

## Equivocation & Joint Entropy
```
H(X,Y) = H(X) + H(Y|X) = H(Y) + H(X|Y)
H(X|Y) <= H(X) (conditioning reduces entropy)
Joint max: H(X,Y) <= H(X) + H(Y) (equality when independent)
```

## Rate for Digital Signaling (noiseless)
```
Maximum data rate (noiseless): R = 2*B*log2(M)  (Nyquist)
  M = number of levels
  B = bandwidth
  This is the Nyquist limit, no noise
Shannon: R <= C = B*log2(1+SNR)  (with noise)
For M levels + noise, usable symbols: M_eff = sqrt(1+SNR)
```

## Quick Reference Table
| Concept | Formula |
|---------|---------|
| Information | log2(1/p) |
| Entropy | -Sum p log2(p) |
| Max entropy | log2(M) |
| Capacity (Shannon) | B log2(1+SNR) |
| BSC capacity | 1-H(p) |
| Kraft | Sum 2^-li <= 1 |
| Huffman avg length | H <= L < H+1 |
| Nyquist rate (noiseless) | 2B log2(M) |
