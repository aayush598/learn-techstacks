# Network Theory - Nodal and Mesh Analysis - Concepts

## Nodal Analysis
- Based on KCL
- Unknowns: node voltages
- Steps:
  1. Select a reference (ground) node
  2. Assign voltage variables to other nodes
  3. Write KCL at each non-reference node
  4. Solve linear equations
- Natural for current sources and parallel elements
- Node voltages simplify voltage calculations

### Nodal equation form
```
Sum(conductances connected to node) * V_node - Sum(adjacent * V_adj) = Sum(current sources in)
G11 V1 + G12 V2 = I1  (matrix form G V = I)
```

## Mesh Analysis
- Based on KVL
- Unknowns: mesh currents (loop currents)
- Steps:
  1. Identify independent meshes (inner loops)
  2. Assign clockwise mesh currents
  3. Write KVL around each mesh
  4. Solve for mesh currents
- Natural for voltage sources and series elements
- Only planar circuits

### Mesh equation form
```
Sum(R in mesh) * I_mesh - Sum(shared R * neighbor current) = Sum(V sources)
R11 I1 + R12 I2 = V1 (matrix R I = V)
```

## Choosing the Method
| Factor | Nodal | Mesh |
|--------|-------|------|
| Unknowns | node voltages | mesh currents |
| Basis | KCL | KVL |
| Good for | current sources, parallel | voltage sources, series |
| Extra nodes | many (transistors) | many |
| Non-planar | OK | NOT OK |
| IC rate | easier for some | good for expected |

## Supernode
- When a voltage source is BETWEEN two non-reference nodes
- Combine the two nodes into a supernode
- KCL applied over combined region
- Voltage constraint from source: V2 - V1 = Vs

## Supermesh
- When a current source is shared between two meshes
- Combine into a supermesh (avoid the shared current source)
- KVL around outer boundary
- Constraint from current source relating the two mesh currents

## Source Transformation
- Voltage source V with series R <-> Current source I=V/R with parallel R
- Nodal/mesh both benefit from strategic transformations

## Matrix Methods
```
Nodal: G V = I   (G = conductance matrix, symmetric)
Mesh:  R I = V   (R = resistance matrix, symmetric)
Solve via: Cramer's rule, Gaussian elimination, matrix inverse
For big circuits: use supernodes/supermeshes, symmetry to reduce order
```

---

## ISRO Key Points
- Nodal = KCL, unknowns = node voltages
- Mesh = KVL, unknowns = mesh currents
- Supernode/supermesh handle floating sources
- Choose the method giving FEWEST equations
- Matrix methods for multi-node/mesh
