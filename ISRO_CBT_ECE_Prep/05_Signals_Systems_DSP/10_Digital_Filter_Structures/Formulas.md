# Digital Filter Structures - Formulas

## FIR Transversal
```
y[n] = Sum[k=0..M-1] b k x[n-k]
H(z) = Sum bk z^-k
Multipliers: M, Adders: M-1, Delays: M-1
```

## IIR Direct Form I
```
y[n] = Sum[M] bk x[n-k] - Sum[N] ak y[n-k]
H(z) = (b0+b1 z^-1+...)/(1+a1 z^-1+...)
Multipliers: M+N+1, Adders: M+N, Delays: M+N
```

## IIR Direct Form II (Canonical)
```
Intermediate: w[n] = x[n] - Sum ak w[n-k]
Output: y[n] = Sum bk w[n-k]
Shares single delay chain
Delays: max(M,N)  <- minimal
Multipliers: M+N+1
```

## Cascade Form (Biquads)
```
H(z) = prod of Hk(z), each:
  Hk(z) = (b0k + b1k z^-1 + b2k z^-2)/(1 + a1k z^-1 + a2k z^-2)
2nd-order sections for stability and lowered sensitivity
```

## Parallel Form
```
Partial fractions:
  H(z) = C + Sum Hk(z)  (each 2nd-order)
```

## Direct vs Cascade (stab/sensitivity)
```
Higher order direct -> poles clustered, sensitive to coefficient quantization
Cascade of 2nd-order -> more robust, better stability margins
```

## Linear Phase FIR Symmetry
```
If h[n] = h[M-1-n], coefficients symmetric
Group delay: (M-1)/2 samples
Save ~half multiplies: combine symmetric taps:
  b_k (x[n-k] + x[n-(M-1-k)])
```

## Finite Word Length
```
Coefficient quantization: 
  error in pole radius ~ 2^(-B) (B bits)
Roundoff: white noise, PSD ~ 2^(-2B)/12
Overflow: minimize via scaling/gain staging
```

## Quantization Noise Power
```
Step: q = 2^(-B) (B bits, fraction)
Noise variance: q^2/12 (per multiplication roundoff)
```

## Quick Reference
| Form | #Delays | Notes |
|------|---------|-------|
| FIR direct | M-1 | no feedback |
| IIR DF-I | M+N | simple but more |
| IIR DF-II | max(M,N) | minimal delays |
| Biquad cascade | 2/section | stable/robust |
| Parallel | similar | partial fractions |
