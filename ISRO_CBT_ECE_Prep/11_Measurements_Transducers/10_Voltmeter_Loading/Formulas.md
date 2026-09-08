# Voltmeter Loading Effect - Formulas

## 1. Voltmeter Sensitivity
```
S = R_v / V_range  (ohm/volt)
S = 1 / I_fs  (where I_fs = full-scale current of movement)
```

## 2. Internal Resistance
```
R_v = S × V_range

Example: S = 20 kohm/V, V_range = 15V
R_v = 20,000 × 15 = 300 kohm
```

## 3. Loading Error (General)
```
Error(%) = (V_meas - V_true) / V_true × 100%

where:
V_true = true voltage without voltmeter
V_meas = voltage with voltmeter connected
```

## 4. Loading Error (Series Circuit)
```
Circuit: Vs -- Rs -- Rload -- GND
Voltmeter across Rload

V_true = Vs × Rload / (Rs + Rload)
V_meas = Vs × (Rload||Rv) / (Rs + (Rload||Rv))

Loading Error(%) = -Rs / (Rs + Rv) × 100%  (approximate for Rv >> Rload)
```

## 5. Thevenin Approach
```
At measurement point:
V_th = open-circuit voltage (true voltage)
R_th = Thevenin resistance (source impedance)

V_meas = V_th × Rv / (Rth + Rv)

Loading Error(%) = -Rth / (Rth + Rv) × 100%
```

## 6. Minimum Sensitivity
```
For maximum error epsilon:
Rv = Rs × (1/epsilon - 1)

Sensitivity S_min = Rv / V_range = Rs × (1/epsilon - 1) / V_range
```

## 7. Loading Factor
```
Loading Factor = V_meas / V_true = Rv / (Rth + Rv)

For negligible loading (>99%): Rv > 100 × Rth
```

## 8. Source Resistance Effect
```
Higher Rs -> Higher loading error
Lower Rv -> Higher loading error

Error is maximum when Rs = Rv (50% error!)
Error < 1% when Rv > 99 × Rs
```

## 9. Range Effect on Analog Voltmeter
```
For same sensitivity S:
R_v1 = S × V1  (at range V1)
R_v2 = S × V2  (at range V2)

At higher range: R_v is higher BUT V_true is also higher
Loading fraction: Rs/(Rs + Sv) remains same
```

## 10. Digital Voltmeter Loading
```
DVM has fixed Rv (typically 10 MOhm)
Loading Error(%) = Rth / (Rth + 10M) × 100%

For Rth = 1 kohm: Error = 0.01%
For Rth = 1 MOhm: Error = 9.09%
```

## 11. Corrected Reading
```
V_true = V_meas × (Rth + Rv) / Rv
V_true = V_meas / Loading_Factor
```

## 12. Multi-Range Voltmeter
```
For Ayrton multiplier:
Total resistance = Rs1 + Rs2 + Rs3 + Rm
Each range uses different tap point

Sensitivity varies: higher range -> higher Rv
But loading fraction Rs/(Rs+Rv) stays constant for same S
```

## Key Formulas for ISRO MCQs
| Quantity | Formula |
|----------|---------|
| Sensitivity | S = Rv/V_range = 1/I_fs |
| Internal R | Rv = S × V_range |
| Loading Error | Error(%) = -Rth/(Rth+Rv) × 100% |
| Min Sensitivity | S_min = Rs(1/epsilon - 1)/V_range |
| Loading Factor | LF = Rv/(Rth+Rv) |
| Corrected V | V_true = V_meas × (Rth+Rv)/Rv |
