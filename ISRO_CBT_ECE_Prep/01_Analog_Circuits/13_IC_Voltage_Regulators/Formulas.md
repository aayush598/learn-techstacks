# IC Voltage Regulators - Formulas

## LM317 Output
```
Vout = 1.25 * (1 + R2/R1) + I_adj*R2  (I_adj ~ 50uA, often neglected)
For I_adj negligible: Vout = 1.25(1 + R2/R1)
Typical: R2 adjustable, R1=240 ohm
```

## Series Regulator Efficiency
```
eta = Pout/Pin = Vout*I / (Vin*I) = Vout/Vin
  (for linear regulator)
Wasted power: P = (Vin - Vout)*I  (heat)
Lower dropout -> higher efficiency
```

## Dropout Voltage
```
V_dropout = Vin(min) - Vout (minimum input-output differential)
Standard: ~2V, LDO: ~0.1-0.5V
```

## Zener Shunt Regulator
```
Vout = Vz
R = (Vin - Vz)/I_z(nom)
I_z varies to absorb load changes
Output ripple attenuated: ripple_out = ripple_in * r_z/(r_z + R)
'''

## Line Regulation
```
Line reg = ΔVout/ΔVin |const Iload   (V/V or %V)
Better if small
```

## Load Regulation
```
Load reg = ΔVout/ΔI_load |const Vin  (V/A or % of Vout)
Measures output impedance effect
```

## Ripple Rejection Ratio (RRR)
```
RRR = Input ripple / Output ripple (ratio or dB)
Linear regulators high (~60-80 dB)
```

## Switching Regulator Efficiency
```
eta = Pout/Pin ~ 85-95%
Buck: Vout = D*Vin (D = duty cycle)
Boost: Vout = Vin/(1-D)
D = duty ratio
```

## Quick Reference
| Formula | Value |
|---------|-------|
| LM317 Vout | 1.25(1+R2/R1) |
| Linear eta | Vout/Vin |
| Waste power | (Vin-Vout)I |
| Buck Vout | D Vin |
| Boost Vout | Vin/(1-D) |
| Zener R | (Vin-Vz)/Iz |
| Line reg | ΔVout/ΔVin |
