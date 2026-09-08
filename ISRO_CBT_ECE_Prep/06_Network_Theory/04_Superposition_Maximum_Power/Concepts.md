# Network Theory - Superposition & Maximum Power - Concepts

## Superposition Theorem
```
In a LINEAR circuit with multiple independent sources,
the response (voltage/current) is the sum of responses from each
source acting ALONE (others deactivated).
```
Valid only for linear circuits (R, L, C, linear dependent sources).
NOT valid for power (power is not linear).

## Steps
1. Select one independent source
2. Deactivate others:
   - Voltage source -> short (0 V)
   - Current source -> open (0 A)
   - (Dependent sources stay active)
3. Solve for desired voltage/current
4. Repeat for each source
5. Sum all contributions (respecting sign/direction)

## Why Useful
- Isolates contribution of each source
- Simplifies analysis of circuits with many sources
- Superposition of linear responses mathematically valid

## Linearity Requirement
- Only variable elements (R, L, C, linear dependent) allowed
- Diodes, transistors (nonlinear) do NOT obey superposition
- Power (V^2/R or I^2 R) does NOT add linearly -> don't sum powers

## Maximum Power Transfer
```
A source with internal resistance Rth delivers max power to load when:
  R_L = Rth
P_max = Vth^2 / (4 Rth)  [Thevenin source Vth in series Rth]
```

### Derivation Insight
```
P_L = I^2 R_L = [Vth/(Rth+RL)]^2 RL
dP_L/dR_L = 0 => R_L = Rth
P_max = Vth^2/(4 Rth)
```

## Efficiency at Max Power
```
Efficiency = P_L/P_total = R_L/(Rth + R_L) = 1/2 = 50%
Only half of generated power reaches load at max power
For maximum EFFICIENCY (not power): R_L >> Rth (efficiency -> 100%)
Practical trade-off:
  - Power transfer wants RL=Rth
  - Efficiency wants RL large
```

## Relation to Matching
- Transmission line/antenna matching: ZL = Z0* (conjugate matching for complex)
- Conjugate match: ZL = Zth*
- For resistive only: RL = Rth

---

## ISRO Key Points
- Deactivation: V source -> short, I source -> open
- Dependent sources remain active
- Can't apply to power (only V, I)
- RL = Rth for max power, Pmax = Vth^2/4Rth
- Efficiency at max power = 50%
