# Temperature Transducers - Formulas

## 1. RTD Resistance
```
R_T = R₀[1 + α(T - T₀)]

For Pt100:
R₀ = 100Ω at T₀ = 0°C
α = 0.00385 Ω/Ω/°C

Example: R at 100°C = 100[1 + 0.00385 × 100] = 138.5Ω
```

## 2. RTD Callendar-Van Dusen Equation
```
For T > 0°C:
R_T = R₀[1 + AT + BT²]

For T < 0°C:
R_T = R₀[1 + AT + BT² + C(T-100)T³]

Where (for Pt100):
A = 3.9083 × 10⁻³ /°C
B = -5.775 × 10⁻⁷ /°C²
C = -4.183 × 10⁻¹² /°C⁴
```

## 3. NTC Thermistor
```
R_T = R₀ × exp[B(1/T - 1/T₀)]

where:
T, T₀ in Kelvin
B = material constant (2000-5000K)
R₀ = resistance at T₀ (usually 25°C = 298K)

Sensitivity: dR/dT = -B/T² × R_T
```

## 4. Thermistor Linearization
```
For small range, approximate linear:
R_T ≈ R₀(1 + α_T × ΔT)

α_T = -B/T₀²  (temperature coefficient at T₀)
For B = 4000K, T₀ = 298K:
α_T = -4000/298² = -0.045/°C = -4.5%/°C
```

## 5. Thermocouple EMF
```
V = S × (T_hot - T_cold)

where S = Seebeck coefficient (μV/°C)
For Type K: S ≈ 41 μV/°C
For Type J: S ≈ 52 μV/°C
```

## 6. Thermocouple Law of Intermediate Temperatures
```
V(T₁, T₃) = V(T₁, T₂) + V(T₂, T₃)

Example: V(500°C, 0°C) = V(500°C, 25°C) + V(25°C, 0°C)
```

## 7. Reference Junction Compensation
```
V_corrected = V_measured + V(T_ref, 0°C)

where V(T_ref, 0°C) = S × T_ref (for small T_ref)
```

## 8. LM35 Output
```
V_out = 10 mV/°C × T

For T = 75°C: V_out = 750 mV = 0.75V
For T = -20°C: V_out = -200 mV = -0.2V
```

## 9. AD590 Output
```
I_out = 1 μA/K × T(K)

For T = 25°C = 298K: I_out = 298 μA
For T = 100°C = 373K: I_out = 373 μA
```

## 10. RTD Lead Wire Error (2-wire)
```
R_measured = R_T + 2R_lead

Error = 2R_lead / R_T × 100%

For R_lead = 5Ω, R_T = 100Ω: Error = 10%
```

## 11. RTD 3-wire Compensation
```
R_true ≈ R_measured - R_lead
Uses Wheatstone bridge to cancel lead resistance
```

## 12. Sensitivity Comparison
```
RTD:       ΔR/ΔT = αR₀ = 0.385 Ω/°C (for Pt100)
NTC:       ΔR/ΔT = -B/T² × R = -4.5 Ω/°C (for 10kΩ at 25°C)
LM35:      ΔV/ΔT = 10 mV/°C
Thermocouple: ΔV/ΔT = S = 41 μV/°C (Type K)
```

## 13. Temperature Coefficient
```
α = (1/R₀) × (dR/dT)

For metals: α > 0 (positive)
For NTC thermistor: α < 0 (negative, large magnitude)
```

## 14. Self-Heating in RTD/Thermistor
```
P = I²R → ΔT = P × θ_jc
Keep excitation current low to minimize self-heating
RTD: < 1mA typical
Thermistor: < 100μA typical
```

## Key Formulas for ISRO MCQs
| Transducer | Formula |
|------------|---------|
| RTD | R_T = R₀(1 + αΔT) |
| Pt100 at 100°C | R = 138.5Ω |
| NTC | R_T = R₀ exp[B(1/T - 1/T₀)] |
| Thermocouple | V = S × ΔT |
| LM35 | V = 10 mV/°C × T |
| AD590 | I = 1 μA/K |
