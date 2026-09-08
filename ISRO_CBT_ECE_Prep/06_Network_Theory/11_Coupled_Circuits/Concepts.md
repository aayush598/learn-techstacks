# Coupled Circuits and Transformers - Concepts

## Mutual Inductance
- Two coils magnetically coupled (sharing flux)
- Mutual inductance M (Henries)
- Voltage in coil 2 due to coil 1 current:
  V2 = M di1/dt
- M = k sqrt(L1 L2), where k = coupling coefficient (0 <= k <= 1)

## Coupling Coefficient
```
k = M/sqrt(L1 L2)
k = 1: perfect coupling (all flux shared)
k = 0: no coupling
k close to 1: tight coupling
```

## Dot Convention
- Determines sign of mutual voltages
- If currents both enter (or exit) dotted terminals: mutual voltage adds
- If one enters, one exits: mutual voltage subtracts
- Dot = same flux direction reference

## Series Connection of Coupled Coils
```
Series aiding (same direction): L_total = L1+L2+2M
Series opposing: L_total = L1+L2-2M
```

## Parallel Connection
```
Parallel aiding: L = (L1 L2 - M^2)/(L1+L2-2M)
Parallel opposing: L = (L1 L2 - M^2)/(L1+L2+2M)
```

## Ideal Transformer
```
V2/V1 = N2/N1 = n  (turns ratio)
I1/I2 = N2/N1 = n
Impedance transformation: Z_in = Z_L/n^2 (from primary)
Power conservation: V1 I1 = V2 I2
No losses, perfect coupling, no magnetizing current (ideal)
```

## Real (Non-Ideal) Transformer
- Has leakage inductance, magnetizing inductance, losses (R, core loss)
- Equivalent circuit includes these
- k < 1 (leakage), magnetizing current not zero

## Thevenin from Secondary
- Refer primary impedance to secondary: Z' = n^2 Z_primary
- Load referencing: match via turns ratio

## Voltage & Current Reflecting
```
Reflected impedance: Z_load(looking into primary) = Z_L / n^2
  (n = N2/N1, secondary-to-primary ratio)
Reflected voltage: V_primary_view = Vi + ...
```

## Applications
- Power transfer (mains transformer)
- Impedance matching
- Isolation (galvanic)
- Signal coupling, DC blocking
- Current transformers

## Energy in Coupled Coils
```
Energy = (1/2)L1 i1^2 + (1/2)L2 i2^2 + M i1 i2  (sign by dots)
Passive constraint: M <= sqrt(L1 L2), k <= 1
```

---

## ISRO Key Points
- k = M/sqrt(L1 L2)
- Series aiding: L1+L2+2M; opposing: L1+L2-2M
- Ideal transformer: V2 = n V1, I1 = n I2, Zin = ZL/n^2
- k=1 perfect, k=0 no coupling
