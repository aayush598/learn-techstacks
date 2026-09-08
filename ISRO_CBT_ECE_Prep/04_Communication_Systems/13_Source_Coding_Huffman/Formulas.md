# Source Coding and Huffman - Formulas

## Entropy
```
H = -Sum[i] pi log2(pi)  bits/symbol
Max H = log2(M) (equiprobable)
Redundancy r = 1 - H/H_max
```

## Huffman Length
```
L_avg = Sum[i] pi li
H <= L_avg < H+1
Coding efficiency = H/L_avg
```

## Kraft Inequality
```
Sum 2^(-li) <= 1  (for unique decodable prefix code)
= 1 for compact/complete code
```

## Example With Solution
```
Symbols & probs: A=0.4, B=0.3, C=0.2, D=0.1
Huff tree:
  Combine C(0.2)+D(0.1)=0.3
  Combine B(0.3)+new(0.3)=0.6
  Combine A(0.4)+0.6
Codes (example): A:0, B:10, C:110, D:111
L_avg = 0.4*1+0.3*2+0.2*3+0.1*3 = 0.4+0.6+0.6+0.3=1.9
H = -(0.4lg0.4+0.3lg0.3+0.2lg0.2+0.1lg0.1)
  = -(0.4*-1.32 + 0.3*-1.74 + 0.2*-2.32 + 0.1*-3.32)
  = -(-0.528-0.522-0.464-0.332)=1.846
Efficiency = 1.846/1.9 = 0.97
```

## Shannon-Fano
```
Split symbols into groups with nearly equal probability sum
Assign 0/1 to each group, recurse
Near-optimal but can be worse than Huffman
```

## Code Length (Huffman bound)
```
Each symbol has li, satisfies:
  Sum 2^(-li) = 1  (if compact)
li ~ -log2(pi)  (approximately)
```

## Combined (2-symbol packing)
```
If grinding a set of N symbols without individual code, 
  can code k symbols together: L_block >= H
```

## Quick Reference
| Parameter | Formula |
|-----------|---------|
| Entropy | -Sum p log2 p |
| Max entropy | log2 M |
| Avg length | Sum p li |
| Bound | H <= L < H+1 |
| Efficiency | H/L |
| Kraft | Sum 2^-li <=1 |
