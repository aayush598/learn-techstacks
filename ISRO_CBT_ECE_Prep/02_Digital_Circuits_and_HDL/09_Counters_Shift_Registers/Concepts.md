# Counters and Shift Registers - Concepts

## Counters
- Sequential circuits that count clock pulses (state sequence)
- Two types: ripple (asynchronous) and synchronous

## Ripple (Asynchronous) Counter
- Each FF clocked by previous FF output
- Simple, but delay accumulates (propagation through stages)
- Modulus = 2^N for N flip-flops
- NOT reliable for high frequency (skew)

## Synchronous Counter
- All FFs clocked simultaneously by same clock
- Parallel, faster, no ripple delay
- More logic (carry/control)

## Counter Types
| Type | Counts | Use |
|------|--------|-----|
| Binary up | 0..2^N-1 | general |
| Binary down | 2^N-1..0 | subtraction |
| Up/down | select direction | bidirectional |
| Mod-N | 0..N-1 (N not power of 2) | frequency division |
| Johnson | cyclic | sequence generation |
| Ring | one-hot | control sequencing |

## Modulus
```
Modulus M = number of states
Binary: M = 2^N (N FFs)
Mod-N (N<2^N): reset at count N-1
N FFs can count up to 2^N
```

## Frequency Division
```
Counter with modulus M divides clock by M
f_out = f_clk/M
Ex: M=2 toggles once/2 clocks -> divide-by-2
```

## Mod-N Counter Realization
```
Use N FFs, detect N-1 state, reset to 0
Example mod-6 (0-5): reset when count reaches 6
```

## Up/Down Counter
```
Control U/D: 
  U: increment, D: decrement
Control logic on each FF based on direction
```

## Shift Register
- Series/parallel of D FFs shifting data each clock
- Types:
  - SISO (serial in, serial out)
  - SIPO (serial in, parallel out)
  - PISO (parallel in, serial out)
  - PIPO (parallel in, parallel out)

## Shift Register Applications
```
- Serial-parallel data conversion (UART)
- Delay line (n clocks delay)
- Ring counter, Johnson counter
- Pattern generation
- Multiplication by 2 (left shift)
- Division by 2 (right shift)
```

## Ring Counter
- Last FF output fed back to first
- One-hot: single 1 circulates
- N states out of 2^N possible (N FFs)
- Used for sequencing (FSM one-hot)

## Johnson (Twisted-Ring) Counter
- Complement of last FF fed to first
- 2N states (N FFs) - more efficient than ring
- Ex: 3-FF Johnson -> 6 states (typical mod-6)

## Counter Design (Synchronous)
```
Use JK/T FFs:
  For binary up count, each bit toggles under certain carries
  Bit i toggles when all lower bits = 1
Down: toggles when all lower bits = 0
FLIP automates
```

## Shift Register - Shift Right
```
Q0 <- Data_in
Q1 <- Q0, Q2 <- Q1, ... (ripple through)
Parallel load: preset all FFs simultaneously
```

---

## ISRO Key Points
- Modulus M, f_out = f_clk/M
- Ripple slow (asynchronous), sync fast
- Mod-6/Johnson common
- Ring: N states, Johnson: 2N states
- Divide-by-2 = toggle FF
- Shift register: data conversion/delay
