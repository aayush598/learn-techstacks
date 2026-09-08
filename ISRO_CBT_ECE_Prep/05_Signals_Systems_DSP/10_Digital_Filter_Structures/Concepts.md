# Digital Filter Structures - Concepts

## Block Diagram Elements
- Adder (summing junction)
- Multiplier (gain)
- Delay element: z^-1 (unit delay, stores one sample)

## FIR Direct Form (Transversal)
```
y[n] = b0 x[n] + b1 x[n-1] + ... + bM-1 x[n-M+1]
Structure: cascade of delays, tap coefficients
Known as: transposed/tapped-delay line
Cost: M multipliers, M-1 adders
```

## IIR Direct Form I
```
y[n] = Sum bk x[n-k] - Sum ak y[n-k]
Two chains: feedforward (b) + feedback (a)
Cost: fairly large (M+N+1 mults)
```

## IIR Direct Form II (Canonical)
```
Merges the two delay chains (shares delays)
Uses minimum number of delays: max(M,N)
More economical than Direct Form I
```

## Cascade Form
- Factored H(z) into 2nd-order sections (biquads)
- Common for higher-order IIR (numerical stability)
- Each section: 2nd-order direct form
- Orders increase => poles closer, quantization issues

## Parallel Form
- Partial fraction expansion
- Sum of 2nd-order sections in parallel
- Also efficient/stable

## Comparison
| Form | Multipliers | Adders | Delays |
|------|-------------|--------|--------|
| FIR direct | M | M-1 | M-1 |
| IIR DF-I | M+N+1 | M+N | M+N |
| IIR DF-II | M+N+1 | M+N | max(M,N) |
| Cascade/parallel | varies | varies | 2 per biquad |

## Finite Word-Length Effects
- Quantization of coefficients
  - Poles move -> filter may become unstable near unit circle
- Roundoff noise
  - From multiplication/rounding in arithmetic
- Overflow (saturation/clipping)
  - Large signals -> two's complement wrap-around

## Pole/Zero Placement
- Poles: must be inside unit circle (stability)
- Zeros: can be anywhere
- Closer to unit circle = sharper filter, more sensitive to quantization

## Realization of Linear Phase FIR
- Symmetric coefficients -> reduce multiplications by ~half
- Use multiply-accumulate (MAC) architecture in DSP

---

## ISRO Key Points
- Direct Form II uses FEWEST delays (max(M,N)) - key
- Cascade for high-order IIR stability
- Poles inside unit circle for stability
- FIR: no feedback, always stable
- Finite word length moves poles
