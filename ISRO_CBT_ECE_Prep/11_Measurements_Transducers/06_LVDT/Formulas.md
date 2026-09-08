# LVDT - Formulas

## 1. Sensitivity
```
Sensitivity = ΔE_out / Δx  (mV/mm)

Overall sensitivity includes excitation:
Sensitivity = ΔE_out / (Δx × V_exc)  (mV/mm/V)

Typical: S = 40-100 mV/mm/V
```

## 2. Output Voltage
```
At null: E_out = E₁ - E₂ = 0
Off-null: E_out = E₁ - E₂ = k × x

where k = sensitivity constant
x = displacement from null
```

## 3. Linearity Error
```
Linearity (% FSD) = (Max deviation from straight line) / (Full scale output) × 100%

Typical: ±0.25% FSD
```

## 4. Phase Relationship
```
When core moves toward S₁:
E_out = E₁ - E₂ (in phase with primary)

When core moves toward S₂:
E_out = E₂ - E₁ (180° out of phase with primary)
```

## 5. Mutual Inductance
```
E₁ = M₁ × (dI_p/dt)
E₂ = M₂ × (dI_p/dt)

At null: M₁ = M₂ → E₁ = E₂ → E_out = 0
```

## 6. Coupling Coefficient
```
k = M / √(L₁ × L₂)

For LVDT: coupling depends on core position
Maximum at full overlap, decreases as core moves out
```

## 7. Dynamic Response
```
Natural frequency: f_n = (1/2π)√(k_core/m_core)
k_core = spring constant of core suspension
m_core = mass of core

Bandwidth depends on core mass and spring
```

## 8. Excitation Frequency Effect
```
Higher frequency → higher sensitivity
But: higher eddy current losses, reduced penetration depth

Optimal: 1-10 kHz for most LVDTs
Typical: 50 Hz to 10 kHz
```

## 9. Temperature Effects
```
Sensitivity drift: ΔS/S ≈ (temperature coefficient) × ΔT
Typical: 0.01-0.05% per °C

Null voltage (residual at null): increases with temperature
Typical null voltage: 0.1-1% of full-scale output
```

## 10. Demodulator Output
```
After phase-sensitive rectification:
V_DC = |E_out| × (demodulator gain)

DC output polarity indicates direction
DC output magnitude indicates displacement
```

## 11. Resolution Calculation
```
Resolution = (Smallest detectable ΔE_out) / (Sensitivity)

If electronics resolve 1μV and sensitivity = 100 mV/mm:
Resolution = 1μV / 100 mV/mm = 0.01 μm
```

## 12. Stroke Length
```
Linear range: ±x_max (typically ±2.5mm to ±750mm)
Total stroke: 2 × x_max

Sensitivity decreases outside linear range
```

## 13. Null Residual Voltage
```
V_null = (Residual output at null) 
Caused by:
- Winding asymmetry
- Core permeability variations
- Stray capacitances
Typical: 0.1-1% of full-scale output
```

## Key Formulas for ISRO MCQs
| Quantity | Formula |
|----------|---------|
| Sensitivity | S = ΔE_out/Δx (mV/mm) |
| Output | E_out = k × x |
| Phase | In-phase → +x, 180° → -x |
| Linearity | ±0.25% FSD typical |
| Null | E_out = 0 when M₁ = M₂ |
| Resolution | ΔV_min / S |
