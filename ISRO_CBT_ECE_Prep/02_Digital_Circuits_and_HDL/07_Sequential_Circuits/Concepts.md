# Sequential Circuits (Flip-Flops) - Concepts

## Sequential vs Combinational
- Combinational: output depends on current inputs only (no memory)
- Sequential: output depends on inputs AND previous state (memory)
- Sequential circuits have memory elements (flip-flops)

## Latch vs Flip-Flop
```
Latch: level-triggered (transparent during active level)
Flip-flop: edge-triggered (captures on clock edge)
Edge-triggered preferred for synchronous design
```

## Basic Flip-Flops

### SR Flip-Flop
```
Set (S=1): output Q=1
Reset (R=1): Q=0
S=R=1: invalid (race/undefined)
Characteristic: Q+ = S + R' Q
```

### JK Flip-Flop
```
Like SR but S=R=1: TOGGLE (JK=11 -> Q toggles)
Removes invalid state
Characteristic: Q+ = J Q' + K' Q
J=K=1 -> toggle (divide-by-2)
```

### D Flip-Flop
```
Q+ = D
Data register, most common (1-bit memory)
No ambiguity
```

### T Flip-Flop
```
T=1: toggle, T=0: hold
Q+ = T Q' + T' Q = T XOR Q
Divide-by-2 counter building block
```

## Characteristic & Excitation Tables

### Characteristic (next state Q+)
```
SR:  Q+ = S + R' Q
JK:  Q+ = J Q' + K' Q
D:   Q+ = D
T:   Q+ = T XOR Q
```

### Excitation (required inputs for transition)
```
0->0: D=0, T=0, S=0 R=X, J=0 K=X
0->1: D=1, T=1, S=1 R=0, J=1 K=X
1->0: D=0, T=1, S=0 R=1, J=X K=1
1->1: D=1, T=0, S=X R=0, J=X K=0
```

## Master-Slave & Edge-Triggered
- Master-slave: two latches, master on half, slave on other (pulse-triggered)
- Edge-triggered: capture on single clock edge (rising/falling)
- Avoids race conditions, preferred

## Flip-Flop Conversions
- Convert D -> JK, T, SR via characteristic equations
- Common ISRO: D to T, D to JK, etc.

## Timing Parameters
```
Setup time (tsu): data must be stable before clock edge
Hold time (th): data stable after clock edge
Propagation delay (tCO): clock to output delay
Violation -> metastability
```

## Applications
```
- Registers (D FF)
- Counters (T/JK)
- Shift registers
- State machines (FSM memory)
- Data storage/synchronization
```

## Common ICs
```
7474: dual D flip-flop (edge-triggered)
7473: dual JK
7476: dual JK (master-slave)
```

---

## ISRO Key Points
- SR: S=R=1 invalid
- JK: 11 toggles
- D: Q=D (register)
- T: toggle, divide-by-2
- Q+ characteristic equations - important
- Edge-triggered for synchronous
- Setup/hold timing
