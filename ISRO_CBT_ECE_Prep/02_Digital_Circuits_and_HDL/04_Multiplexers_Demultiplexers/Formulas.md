# Multiplexers and Demultiplexers - Formulas

## MUX Output Expression
```
For 2:1 MUX:
  Y = S'.I0 + S.I1

For 4:1 MUX:
  Y = S1'.S0'.I0 + S1'.S0.I1 + S1.S0'.I2 + S1.S0.I3

For 8:1 MUX:
  Y = S2'.S1'.S0'.I0 + S2'.S1'.S0.I1 + S2'.S1.S0'.I2 + S2'.S1.S0.I3
    + S2.S1'.S0'.I4 + S2.S1'.S0.I5 + S2.S1.S0'.I6 + S2.S1.S0.I7

General: 2^n:1 MUX
  Y = Sum over k=0 to 2^n-1 of: (select combination).Ik
```

## MUX as n+1 Variable Function Implementer
```
Using 2^(n-1):1 MUX for n variables:
- Connect (n-1) variables to select lines
- Connect remaining variable (or its complement, 0, or 1) to data inputs
- Number of data inputs needed = 2^(n-1)
```

## Decoder Output
```
For n-to-2^n decoder with active HIGH output:
  Yi = minterm(i) of the input variables

Example: 3-to-8 decoder
  Y0 = A'B'C    Y4 = AB'C'
  Y1 = A'B'C'   Y5 = AB'C
  Y2 = A'BC     Y6 = ABC'
  Y3 = A'BC'    Y7 = ABC
```

## Function Implementation
```
Any SOP: f = Sigma m(intersections)
Using decoder: Connect variables to decoder inputs
              OR together the outputs corresponding to minterms

Using MUX: Connect (n-1) variables to select
           Set data inputs based on truth table
```

## Enable Gate
```
With Enable E (active HIGH):
  Decoder output = Yi = E . (minterm i)

With Enable E (active LOW):
  Decoder output = Yi = E' . (minterm i)
```

## Quick Reference
| Device | Inputs | Select | Output | Use |
|--------|--------|--------|--------|-----|
| 2:1 MUX | 2 | 1 | 1 | Data selection |
| 4:1 MUX | 4 | 2 | 1 | 3-variable function |
| 8:1 MUX | 8 | 3 | 1 | 4-variable function |
| 2-to-4 DEC | 2 | - | 4 | Address decoding |
| 3-to-8 DEC | 3 | - | 8 | SOP implementation |
