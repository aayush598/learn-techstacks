# Counters and Shift Registers - Formulas

## Counter Basics
```
Binary N-bit counter: max count = 2^N - 1
Modulus M: f_out = f_clk/M
Counts 0,1,...,M-1 -> wraps/reset to 0
```

## Number of FFs
```
For modulus M (up to 2^N):
  N = ceil(log2 M) flip-flops
To count 0..99 (mod 100): N = 7 (2^7=128>=100)
```

## Ripple counter
```
Divide-by-2^N
Delay: N * t_prop (worst case)
```

## Johnson Counter
```
N FFs -> 2N states (Johnson)
Ring counter: N FFs -> N states (one-hot)
Mod-6 Johnson: 3 FFs
```

## Johnson sequence (3-FF mod-6)
```
000, 100, 110, 111, 011, 001, then back to 000
(2N = 6 states)
```

## Ring counter
```
One-hot: 1000,0100,0010,0001 (N states, 4 FFs)
Used for FSM state decoding (no decode logic)
```

## Up/Down counter logic (JK/T FF, bit i)
```
Up:  toggle bit i when all lower bits = 1 (for binary up)
Down: toggle bit i when all lower bits = 0
Combined: toggle when lower all 1 (up) or all 0 (down)
```

## Frequency divider
```
Mod-M -> output freq = f_in/M
Cascade of counters multiplies moduli:
  M_total = M1 * M2 * ...
```

## Shift Register delay
```
N-bit SISO shift register: output = input delayed N clocks
Data conversion time: serial -> N clocks
```

## Quick Reference
| Counter | FFs | States |
|---------|-----|--------|
| Binary N-bit | N | 2^N |
| Johnson | N | 2N |
| Ring | N | N |
| Mod-N | ceil(log2N) | N |
| Mod-6 (Johnson) | 3 | 6 |
