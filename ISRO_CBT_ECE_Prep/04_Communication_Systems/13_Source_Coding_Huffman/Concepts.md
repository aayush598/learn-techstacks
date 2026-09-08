# Source Coding and Huffman - Concepts

## Purpose
Remove redundancy from source symbols before transmission -> fewer bits

## Entropy (lower bound)
```
H = -Sum pi log2(pi)  bits/symbol
Minimum average bits to represent source = H
No code can average less than H (Shannon)
```

## Huffman Coding
- Optimal prefix code (no codeword is prefix of another)
- Algorithm:
  1. List symbols by probability (descending)
  2. Combine two lowest probabilities, assign 0/1
  3. Repeat until one node (tree)
  4. Read codewords from root to leaf
- Most probable symbol gets shortest code

## Properties of Huffman
```
Average length L: H <= L < H + 1
No code is a prefix of another (instantaneous decode)
Optimal for a given set (minimizes L)
Not necessarily unique (tie-breaking)
```

## Prefix (Instantaneous) Code
- No codeword is a prefix of any other
- Decodable immediately without lookahead
- Kraft inequality governs existence:
  Sum 2^(-li) <= 1

## Huffman vs Shannon-Fano
- Both produce prefix codes
- Huffman is optimal (min L for given p)
- Shannon-Fano: near-optimal, simpler, split roughly equal halves
- Huffman generally better for skewed distributions

## Fixed vs Variable Length
- Fixed (e.g. 8-bit ASCII): simple, rigid
- Variable (Huffman): efficient for skewed probs, needs tree
- Variable-length frames/orphans on error (no sync)

## Example
Symbols p: A=0.5, B=0.25, C=0.125, D=0.125
Huffman:
  A: 0, B: 10, C: 110, D: 111
L_avg = 0.5*1 + 0.25*2 + 0.125*3 + 0.125*3 = 0.5+0.5+0.375+0.375 = 1.75
H = 1.75 (for these probs, optimal!!)

## Kraft Inequality
Sum 2^(-li) <= 1 (necessary & sufficient for prefix code)
If strict < 1: some redundancy remains
If = 1: compact (complete) code

## Other Source Codings
- LZW / LZ77/78: dictionary based, adaptive
- Arithmetic coding: fractional bits/symbol (approaches H)
- Run-length coding: for repeated data
- Image: Huffman on DCT coefficients (JPEG)

---

## ISRO Key Points
- H <= L < H+1, H = -Sum p log p
- Huffman: shortest for most probable
- Prefix property: no codeword is prefix
- Kraft: Sum 2^-li <= 1
- Huffman reduces average length to ~ entropy
