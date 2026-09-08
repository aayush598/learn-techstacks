# Schmitt Triggers - Formulas

## Inverting Schmitt Trigger (Reference at Non-Inverting Terminal)
```
Upper Threshold:  UTP = +Vsat * R1/(R1 + R2)
Lower Threshold:  LTP = -Vsat * R1/(R1 + R2)
Hysteresis Width: VH  = UTP - LTP = 2*Vsat*R1/(R1 + R2)
Center Voltage:   Vc  = (UTP + LTP)/2 = 0V (symmetric supply)
```

## Non-Inverting Schmitt Trigger
```
UTP = Vsat * R2/(R1 + R2) (when output is +Vsat)
LTP = -Vsat * R2/(R1 + R2) (when output is -Vsat)
VH = 2*Vsat*R2/(R1 + R2)
```

## Asymmetric Supply (Non-Inverting with Reference)
```
UTP = Vref + (Vsat - Vref) * R1/(R1 + R2)
LTP = Vref + (-Vsat - Vref) * R1/(R1 + R2)
```

## Schmitt Trigger Oscillator
```
Frequency: f = 1/(R*C*ln((1+beta)/(1-beta)))
where beta = R1/(R1+R2) = feedback factor

Period: T = R*C*ln((1+beta)/(1-beta))
```

## For Symmetric Case:
```
T = 2*R*C*ln((R1+R2)/R2 * (R1+2*R2)/(R1)) ... (approximate)
Or: T = 2*R*C*ln(1 + 2*R2/R1)
```

## Design Equations (Given UTP and LTP):
```
R1/R2 = LTP/(Vsat - LTP)  ... from UTP equation
VH = UTP - LTP
Choose R1, R2 to satisfy the ratio
```

## Quick Reference Table
| Parameter | Formula |
|-----------|---------|
| UTP (inverting) | +Vsat * R1/(R1+R2) |
| LTP (inverting) | -Vsat * R1/(R1+R2) |
| Hysteresis | 2*Vsat*R1/(R1+R2) |
| Oscillator freq | 1/(RC*ln((1+beta)/(1-beta))) |
