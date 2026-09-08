# Finite State Machines - Formulas

## Moore Machine Output
```
Output(t) = g(State(t))
Output changes ONLY on clock edge (synchronous)
```

## Mealy Machine Output
```
Output(t) = g(State(t), Input(t))
Output can change asynchronously with input
```

## Flip-Flop Excitation Table

### SR Flip-Flop
```
Present -> Next | S | R
  0 -> 0       | 0 | X
  0 -> 1       | 1 | 0
  1 -> 0       | 0 | 1
  1 -> 1       | X | 0
```

### JK Flip-Flop
```
Present -> Next | J | K
  0 -> 0       | 0 | X
  0 -> 1       | 1 | X
  1 -> 0       | X | 1
  1 -> 1       | X | 0
```

### D Flip-Flop
```
Present -> Next | D
  0 -> 0       | 0
  0 -> 1       | 1
  1 -> 0       | 0
  1 -> 1       | 1
(D = Next State)
```

### T Flip-Flop
```
Present -> Next | T
  0 -> 0       | 0
  0 -> 1       | 1
  1 -> 0       | 1
  1 -> 1       | 0
(T = 1 for toggle, T = 0 for hold)
```

## Characteristic Equations
```
SR: Q(next) = S + R'.Q  (with SR=0 constraint)
JK: Q(next) = J.Q' + K'.Q
D:  Q(next) = D
T:  Q(next) = T XOR Q = T.Q' + T'.Q
```

## Number of Flip-Flops Required
```
For n states: minimum flip-flops = ceil(log2(n))

States | Min FF
  2    |   1
  3-4  |   2
  5-8  |   3
  9-16 |   4
```
