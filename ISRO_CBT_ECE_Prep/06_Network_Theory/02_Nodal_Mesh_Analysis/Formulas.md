# Network Theory - Nodal and Mesh Analysis - Formulas

## Nodal Analysis
```
At node j:
  Sum over k of Gjk (Vj - Vk) + (currents out) = 0
  = Sum I_sources entering j

Matrix form: G V = I
  Gij = sum of conductances at node i (diagonal)
  Gij = -conductance between i,j (off-diagonal)
  Ii = sum of current sources entering node i
```

## Supernode
```
Nodes V1, V2 connected by voltage source Vs:
  Constraint: V2 - V1 = Vs
  KCL across combined region (sum currents = 0)
This adds one equation and one unknown (treated as single region)
```

## Mesh Analysis
```
Around mesh j:
  Sum Rjk (Ij) - Sum(neighbor mesh currents * shared R) = Sum V rising in mesh
Matrix: R I = V
  Rii = sum resistances in mesh i
  Rij = -shared resistance between meshes i,j
  Vi = sum of voltage sources (rise) in mesh i
```

## Supermesh
```
Current source shared between meshes i, j:
  Combine to supermesh, apply KVL around outer boundary
  Constraint: Ij - Ii = Is (current source value)
```

## Source Transformation
```
V in series with R  <->  I = V/R in parallel with R
Same terminal behavior. Both directions possible.
```

## Current/Voltage from Solution
```
Branch current past resistor R between nodes Va, Vb:
  I = (Va - Vb)/R
Branch voltage from mesh currents:
  V = R(Ii - Ij)
```

## Reduction Techniques
```
Parallel conductances add; series resistances add
Delta-Y: convert to simplify
Symmetry: split balanced nodes -> parallel paths
```

## Quick Reference
| Technique | Law | Unknown | Best for |
|-----------|-----|---------|----------|
| Nodal | KCL | node V | current sources, parallel |
| Mesh | KVL | loop I | voltage sources, series |
| Supernode | KCL+constraint | combined V | between-node V source |
| Supermesh | KVL+constraint | combined I | shared current source |
