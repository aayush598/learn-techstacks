# Two-Port Networks - Concepts

## Two-Port Network
- Two terminal pairs: input (port 1) and output (port 2)
- Described by relationships between V1, I1, V2, I2
- Any two variables express the other two

## Parameter Sets
| Parameters | Equations | Elements |
|------------|-----------|----------|
| Z | V1=Z11 I1+Z12 I2, V2=Z21 I1+Z22 I2 | Ohms (impedance) |
| Y | I1=Y11 V1+Y12 V2, I2=Y21 V1+Y22 V2 | Siemens |
| h | V1=h11 I1+h12 V2, I2=h21 I1+h22 V2 | Mixed/hybrid |
| g | I1=g11 V1+g12 I2, V2=g21 V1+g22 I2 | Inverse hybrid |
| ABCD | V1=A V2 - B I2, I1=C V2 - D I2 | Transmission |

## Z-Parameters
```
Z11 = V1/I1 |I2=0   (input impedance, output open)
Z12 = V1/I2 |I1=0   (transfer, input open)
Z21 = V2/I1 |I2=0   (transfer, output open)
Z22 = V2/I2 |I1=0   (output impedance, input open)
Open-circuit parameters
```

## Y-Parameters
```
Y11 = I1/V1 |V2=0   (input admittance, output short)
Y21 = I2/V1 |V2=0   (forward transfer, shorted)
...
Short-circuit parameters
```

## h-Parameters (hybrid)
```
h11 = V1/I1 |V2=0   (input impedance, shorted output)
h12 = V1/V2 |I1=0   (reverse voltage ratio, open input)
h21 = I2/I1 |V2=0   (current gain, shorted output)
h22 = I2/V2 |I1=0   (output admittance, open input)
Used for transistor models
```

## ABCD (Transmission) Parameters
```
V1 = A V2 - B I2
I1 = C V2 - D I2
A = V1/V2 |I2=0   (open circuit)
B = -V1/I2 |V2=0  (short circuit)
For cascade: overall ABCD = product of individual ABCD
This is why ABCD used for cascading (transmission lines)
```

## Reciprocity
```
Reciprocal network: Z12 = Z21, Y12 = Y21, h12 = -h21
Contains only passive (R,L,C,M) elements, no dependent sources
ABCD: AD - BC = 1 (reciprocal)
```

## Symmetry
```
Symmetric network: Z11 = Z22, Y11 = Y22, A = D
```

## Conversions (example Z to Y)
```
Y = Z^(-1)  (matrix inverse)
h and g are inverses
ABCD related by formulas
```

## Network Conditions
- Passive: Z12=Z21
- Symmetric + passive: Z11=Z22, Z12=Z21
- Ideal transformer: ABCD = [n, 0; 0, 1/n], determinant 1
- Lossless (reactive): Z parameters purely imaginary

## Measurements
- Z measured with OPEN (I2=0)
- Y measured with SHORT (V2=0)
- h measured with appropriate opens/shorts

---

## ISRO Key Points
- Z with open, Y with short - key concept
- Reciprocity: Z12=Z21 for passive
- Cascade: multiply ABCD
- h-parameters for transistors
- Symmetry: Z11=Z22
