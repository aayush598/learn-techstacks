# Sequential Circuits (Flip-Flops) - Formulas

## Characteristic Equations
```
SR: Q+ = S + R' Q      (R'=NOT R)
JK: Q+ = J Q' + K' Q
D:  Q+ = D
T:  Q+ = T Q' + T' Q = T XOR Q
```

## Truth (SR)
```
S R | Q+
0 0 | Q  (hold)
0 1 | 0  (reset)
1 0 | 1  (set)
1 1 | invalid
```

## Truth (JK)
```
J K | Q+
0 0 | Q  (hold)
0 1 | 0  (reset)
1 0 | 1  (set)
1 1 | Q' (toggle)
```

## Truth (D, T)
```
D | Q+    T | Q+
0 | 0     0 | Q  (hold)
1 | 1     1 | Q' (toggle)
```

## Excitation Table (inputs to get next state)
```
Transition | D  | T  | S R  | J K
0 -> 0     | 0  | 0  | 0 X  | 0 X
0 -> 1     | 1  | 1  | 1 0  | 1 X
1 -> 0     | 0  | 1  | 0 1  | X 1
1 -> 1     | 1  | 0  | X 0  | X 0
```

## Conversions
```
D -> T: T = D XOR Q  (since D = T XOR Q)
D -> JK: D = J Q' + K' Q
T -> D:  D = T XOR Q
JK -> D: J = D, K = D'  (i.e. D FF = JK with J=D, K=D')
```

## Toggle / Divide
```
T FF with T=1: frequency divide by 2
N cascaded toggle: divide by 2^N, count 0..2^N-1
```

## Setup/Hold constraints
```
tsu: data before clock edge
th:  data after clock edge
tCO: clock-to-output delay
Max clock: Tmin >= tsu + tCO + tlogic
```

## Quick Reference
| FF | Q+ | Invalid |
|----|----|---------|
| SR | S + R'Q | SR=1 |
| JK | JQ'+K'Q | none through 11 toggle |
| D | D | none |
| T | T XOR Q | none |
