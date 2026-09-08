# S-Parameters - Concepts

## What are S-Parameters?
- Scattering parameters describe microwave network behavior
- Based on traveling waves (incident and reflected)
- Measured at network ports with matched reference impedances (typically 50 ohms)
- S-matrix relates incident and reflected voltage waves

## S-Matrix Definition
```
[b] = [S] [a]
where:
  a = incident wave vector
  b = reflected/scattered wave vector
  S = scattering matrix
```

## Two-Port S-Matrix
```
| b1 |   | S11  S12 |   | a1 |
| b2 | = | S21  S22 | * | a2 |
```

### Physical Meaning:
- **S11**: Input reflection coefficient (a2=0, output matched)
- **S21**: Forward transmission coefficient (gain/loss)
- **S12**: Reverse transmission coefficient (isolation)
- **S22**: Output reflection coefficient (a1=0, input matched)

---

## Properties of S-Matrix

### Reciprocal Network
- S = S^T (symmetric matrix)
- S12 = S21
- Example: Passive networks (couplers, dividers)

### Lossless Network
- S^H * S = I (unitary matrix)
- Sum of power in each column = 1
- No power dissipation in network

### Matched Network
- S11 = S22 = 0 (input and output perfectly matched)
- All power is transmitted or isolated

---

## S-Parameters for Common Networks

### Ideal Isolator
```
S = | 0    0  |
    | 1    0  |
S11=0, S12=0, S21=1, S22=0
Perfect forward transmission, no reverse
```

### Ideal Circulator (3-port)
```
S = | 0  0  1 |
    | 1  0  0 |
    | 0  1  0 |
Port 1 -> Port 2 -> Port 3 -> Port 1
```

### Ideal Directional Coupler (4-port)
```
S = | 0    0    0    j*c |
    | 0    j*s  c    0   |
    | 0    c    j*s  0   |
    | j*c  0    0    0   |
where c = cos(theta), s = sin(theta)
```

---

## ISRO Key Points
- S11 = reflection coeff at port 1 (when port 2 matched)
- S21 = forward transmission (port 1 to port 2)
- Reciprocal: S12 = S21
- Lossless: columns of S-matrix are orthonormal
- 3-port reciprocal matched network cannot be lossless (important theorem)
