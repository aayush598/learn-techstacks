# Bitwise Operators

## Operators

| Operator | Name | Example | Result |
|---|---|---|---|
| & | AND | 5 & 3 (101 & 011) | 001 = 1 |
| \| | OR | 5 \| 3 (101 \| 011) | 111 = 7 |
| ^ | XOR | 5 ^ 3 (101 ^ 011) | 110 = 6 |
| ~ | NOT | ~5 | -6 (flips all bits) |
| << | Left Shift | 5 << 1 | 10 (multiply by 2) |
| >> | Signed Right Shift | -5 >> 1 | -3 (divides by 2, preserves sign) |
| >>> | Unsigned Right Shift | -5 >>> 1 | 2147483645 |

## Truth Tables

```
AND: 0&0=0, 0&1=0, 1&0=0, 1&1=1
OR:  0|0=0, 0|1=1, 1|0=1, 1|1=1
XOR: 0^0=0, 0^1=1, 1^0=1, 1^1=0
```
