# Information Theory and Source Coding - Concepts

## Information Content
- Information of an event = log2(1/p) bits
- Rare events carry more information
- If p = 0.5: I = 1 bit
- If p = 1: I = 0 bits (certain event, no info)

## Entropy (H)
```
H = -Sum p_i * log2(p_i)  bits/source symbol
Measures AVERAGE information per symbol
Maximum entropy: H_max = log2(M) when all M symbols equiprobable
Binary source (M=2): H_max = 1 bit
```

## Important Entropy Bounds
```
0 <= H <= log2(M)
H = 0: all mass on one symbol (deterministic)
H = log2(M): uniform distribution (maximum)
Entropy is additive for independent sources
```

## Source Coding
- Goal: minimize average bits per symbol
- **Huffman coding**: optimal, no code is prefix of another
- **Shannon-Fano**: near-optimal (by probability splitting)
- **LZW**: dictionary-based, adaptive

### Huffman Coding
- Most probable symbol gets SHORTEST code
- Least probable gets LONGEST code
- Average code length: L = Sum p_i * l_i
- Always: H <= L < H + 1

### Kraft Inequality
- Necessary/sufficient for prefix codes:
```
Sum 2^(-l_i) <= 1
where l_i are code lengths
```

## Shannon's Source Coding Theorem
- A source with entropy H can be encoded with average length arbitrarily close to H
- Lower bound: L >= H
- Hence entropy measures minimum average code length

## Mutual Information
```
I(X;Y) = H(X) - H(X|Y) = H(Y) - H(Y|X)
Amount of information about X provided by Y
Symmetry: I(X;Y) = I(Y;X)
```

## Shannon's Channel Capacity
```
C = B*log2(1 + SNR)  bits/sec
  B = bandwidth (Hz)
  SNR = signal-to-noise ratio (linear)
Classic derivation (Shannon-Hartley)
```
Key properties:
- C increases logarithmically with SNR (not linearly)
- C increases linearly with bandwidth (in theory)
- White Gaussian noise is the worst-case channel
- Above capacity: error-free transmission impossible (any coding)

## Binary Symmetric Channel (BSC)
```
Capacity: C = 1 - H(p)  bits/channel use
  p = crossover error probability
  H(p) = -p*log2(p) - (1-p)*log2(1-p)
No errors (p=0): C = 1 bit/channel
Completely random (p=0.5): C = 0

Alternative: C = 1 + p*log2(p) + (1-p)*log2(1-p)
```

## Channel Coding
- Add redundancy to detect/correct errors
- **Hamming code**: (7,4) corrects 1 error
- **Block codes**: correct t=floor((d_min-1)/2) errors
- **Convolutional codes**: memory-based, trellis decoding (Viterbi)
- Code rate: R = k/n (information bits / total bits)

---
## ISRO Key Points
- Entropy: maximum log2(M), additive
- H = -Sum p log2 p - MOST TESTED
- Huffman: shortest for most probable
- Capacity: C = B log2(1+SNR) - MOST TESTED
- BSC capacity: 1 - H(p)
