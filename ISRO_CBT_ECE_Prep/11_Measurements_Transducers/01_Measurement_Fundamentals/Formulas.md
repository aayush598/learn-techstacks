# Measurement Fundamentals - Formulas

## 1. Accuracy
```
Accuracy (%) = (1 - |True Value - Measured Value| / True Value) × 100
```

## 2. Precision (Repeatability)
```
Precision = 1 - (Standard Deviation / Mean of Readings)
```

## 3. Resolution
```
Analog: Resolution = Smallest Division / 2
Digital: Resolution = 1 LSB = Full Scale / 2^n
         (n = number of bits)
```

## 4. Sensitivity
```
Sensitivity (S) = ΔOutput / ΔInput
For voltmeter: S_v = R_v / V_fs  (Ω/V)
```

## 5. Loading Error (Voltmeter)
```
True Voltage:     V_true = V_source × R_load / (R_source + R_load)
Measured Voltage: V_meas = V_source × R_vm / (R_source + R_vm)
Loading Error = V_meas - V_true
Loading Error (%) = (V_meas - V_true) / V_true × 100

Simplified: Error(%) = R_source / (R_source + R_vm) × 100
```

## 6. Loading Error (Ammeter)
```
True Current:     I_true = V / R_load
Measured Current: I_meas = V / (R_load + R_am)
Loading Error (%) = -R_am / (R_load + R_am) × 100
```

## 7. Relative Error
```
Relative Error = |True Value - Measured Value| / |True Value|
Percent Error = Relative Error × 100
```

## 8. Absolute Error
```
Absolute Error = Measured Value - True Value
                = (Systematic Error) + (Random Error)
```

## 9. Combined Uncertainty (Random Errors)
```
If σ₁, σ₂, ... σₙ are individual standard deviations:
Combined σ = √(σ₁² + σ₂² + ... + σₙ²)
```

## 10. Confidence Interval
```
For Gaussian distribution:
68.27% confidence: μ ± σ
95.45% confidence: μ ± 2σ
99.73% confidence: μ ± 3σ
```

## 11. Sensitivity of Measurement System
```
S_total = S₁ × S₂ × S₃ × ... × Sₙ
where S₁, S₂, ... are sensitivities of individual stages
```

## 12. Minimum Sensitivity of Voltmeter
```
For given R_source and maximum loading error ε:
R_vm = R_source × (1/ε - 1)
Sensitivity = R_vm / V_range  (Ω/V)
```

## 13. Digital Instrument Resolution
```
For n½ digit display (e.g., 3½):
Maximum count = 2 × 10^(n-1) - 1  or  2 × 10^(n) - 1
Resolution = Full Scale / (10^(n) - 1)  for 3½: 1999
```

## 14. Merit Figure of PMMC
```
Figure of Merit = Torque / Weight of moving system (T/W)
Higher T/W → better performance
```

## 15. Gross Error Detection (Chauvenet's Criterion)
```
For N readings, reject if:
|X_i - X_mean| / σ > d_max
where d_max is from Chauvenet's table:
N=5: 1.65, N=10: 1.96, N=20: 2.24, N=50: 2.58
```

## Key Relations for ISRO MCQs
| Quantity | Formula |
|----------|---------|
| Voltmeter Loading Error (%) | R_s / (R_s + R_vm) × 100 |
| Minimum S (Ω/V) | R_vm / V_range |
| Relative Error | Δx / x_true × 100 |
| Total Uncertainty | √(σ_sys² + σ_rand²) |
| Resolution (digital) | V_fs / (10^n - 1) |
