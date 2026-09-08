# Network Theory - Thevenin and Norton - Concepts

## Thevenin's Theorem
Any linear two-terminal network can be replaced by:
```
Vth (voltage source) in SERIES with Rth
```
- Valid only for LINEAR networks
- Works for any load connected across terminals

### Finding Vth
- Open-circuit voltage across terminals (with load removed)

### Finding Rth
1. Deactivate sources:
   - Voltage source -> short circuit
   - Current source -> open circuit
2. Compute equivalent resistance looking into terminals

### Alternative Rth (using short-circuit)
```
Rth = Vth / Isc  (Isc = short-circuit current)
```
Useful when dependent sources present (higher method)

## Norton's Theorem
Any linear network can be replaced by:
```
In (current source) in PARALLEL with Rn
```
- In = short-circuit current across terminals
- Rn = Rth (same Thevenin resistance)

## Thevenin - Norton Relation
```
Vth = In * Rn
In = Vth / Rth
Rth = Rn
```
They are source transformations of each other!

## Maximum Power Transfer
```
Load resistance for max power: RL = Rth (load = source resistance)
Max power: Pmax = Vth^2 / (4 Rth)
Efficiency: 50% at max power
```

## Dependent Source Handling
- When deactivating, independent sources are zeroed; dependent sources KEPT
- Rth found via test source: Vtest/Itest applied at terminals
- OR: Rth = Vth/Isc

## Thevenin vs Norton Table
| Property | Thevenin | Norton |
|----------|----------|--------|
| Source | Voltage Vth | Current In |
| Topology | V in series with Rth | I in parallel with Rn |
| Rth/Rn | Equal | Equal |
| Relation | Vth = In*Rn | In = Vth/Rth |
| Ideal case | Rth=0 | Rn=inf |

## Ideal Source Implications
- Ideal voltage source: Rth = 0 (can supply any current)
- Ideal current source: Rn = infinity (can supply any voltage)
- Practical sources have nonzero Rth / finite Rn

## Why It Matters
- Simplify complex circuits
- Analyze load variations easily
- Load changes don't require re-solving entire circuit
- Thevenin equivalent is the standard "source model"

---

## ISRO Key Points
- Rth: zero independent sources then compute
- Vth: open circuit voltage
- In: short circuit current
- Max power: RL = Rth, Pmax = Vth^2/(4Rth)
- Dependent sources: use Vth/Isc
