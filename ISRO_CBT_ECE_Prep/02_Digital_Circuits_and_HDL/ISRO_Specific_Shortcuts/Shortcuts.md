# Digital Circuits - Quick Solving Shortcuts

## Number System Quick Conversions
```
Binary to Decimal: Sum of (bit * 2^position)
Decimal to Binary: Repeated division by 2, read remainders bottom-up
Binary to Hex: Group 4 bits, convert each group
Hex to Binary: Each hex digit = 4 binary bits

2's complement of binary: Invert all bits + 1
1's complement of binary: Invert all bits
```

## K-Map Quick Tips
```
2-variable: 4 cells (2x2)
3-variable: 8 cells (2x4)
4-variable: 16 cells (4x4)

Gray code order for columns: 00, 01, 11, 10
NEVER use: 00, 01, 10, 11 (this is binary, not Gray)
```

## Flip-Flop Quick Reference
```
Characteristic Equations:
  SR: Q+ = S + R'Q    (SR=0)
  JK: Q+ = JQ' + K'Q
  D:  Q+ = D
  T:  Q+ = T XOR Q

Excitation (D is simplest): D = Q+ (next state directly)
```

## MUX Quick Implementation
```
n variables using MUX:
  3 vars -> 4:1 MUX (2 select lines)
  4 vars -> 8:1 MUX (3 select lines)
  n vars -> 2^(n-1):1 MUX

Output: Y = Sum(Si * Ii) where Si = select combination, Ii = input
```

## FSM Quick Design
```
1. Draw state diagram
2. State table
3. Assign binary codes (use gray code for fewer literals)
4. D-flip-flop: D = Next State (simplest)
5. K-map for output and next-state logic
```

## VHDL Quick Rules
```
Signal assignment: Y <= A AND B; (concurrent)
Variable assignment: X := A + B; (only in process)
Process: process(CLK) begin if rising_edge(CLK) then... end if; end process;
Delta delay: After simulation step, not real time
```

## ADC Quick Formulas
```
Resolution = Vref / 2^n (n = number of bits)
LSB = Vref / 2^n
Quantization error = +/- LSB/2
SNR (dB) = 6.02*n + 1.76 (for full-scale sinusoidal input)
```

## Metastability Quick Facts
```
MTBF = e^(Tsetup/tau) / (fclk * fdata * T0)
2-FF synchronizer increases MTBF exponentially
Always use 2+ FF for clock domain crossing
Setup violation -> possible metastability
```
