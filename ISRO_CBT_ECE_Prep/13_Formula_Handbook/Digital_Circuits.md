# Digital Circuits - Complete Formula Sheet

## Number Systems
```
Binary -> Decimal: Sum(bit * 2^position)
2's complement: Invert + 1
Gray code: G[i] = B[i] XOR B[i+1]
BCD: 4-bit binary for each decimal digit
```

## Boolean Algebra
```
De Morgan: (A+B)' = A'B'    (A.B)' = A'+B'
Consensus: AB + A'C + BC = AB + A'C
Absorption: A+AB = A, A(A+B) = A
```

## K-Map
```
2-var: 4 cells, 3-var: 8 cells, 4-var: 16 cells
Group sizes: 1, 2, 4, 8, 16 (powers of 2)
Gray code ordering for columns: 00, 01, 11, 10
```

## Flip-Flops
```
SR: Q+ = S + R'Q (with SR=0)
JK: Q+ = JQ' + K'Q
D:  Q+ = D
T:  Q+ = T XOR Q

Excitation (D): D = Next State
Number of FF: n >= ceil(log2(states))
```

## Counters
```
Mod-n counter: counts 0 to n-1, needs ceil(log2(n)) FF
Johnson counter: 2n states with n FF (twisted ring)
Ring counter: n states with n FF (one hot)
```

## MUX
```
2:1: Y = S'.I0 + S.I1
n-variable function: 2^(n-1):1 MUX needed
3-var: 4:1 MUX, 4-var: 8:1 MUX
```

## ADC/DAC
```
Resolution: LSB = Vref/2^n
SNR (dB) = 6.02*n + 1.76
Quantization error = +/- LSB/2

Flash ADC: 2^n - 1 comparators
SAR ADC: n cycles for conversion
Dual slope: Conversion time = 2^n * Tclk
```

## Metastability
```
MTBF = e^(Tsetup/tau) / (fclk * fdata * T0)
2-FF synchronizer: MTBF_2FF = MTBF_1FF * e^(Tclk/tau)
Setup time: data stable before clock edge
Hold time: data stable after clock edge
```

## VHDL Quick
```
Signal: <= (concurrent and sequential)
Variable: := (only in process)
rising_edge(CLK): clock edge detection
std_logic, std_logic_vector: most common types
Process sensitivity list: must include clock for sequential logic
```
