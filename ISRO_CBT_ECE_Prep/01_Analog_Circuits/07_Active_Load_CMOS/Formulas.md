# Active Load and CMOS Amplifiers - Formulas

## Gain with Active Load
```
CS with active (current-source) load:
  Av = -gm1 * (r_o1 || r_o2)
  = -gm1 * R_out
R_out = r_o1 || r_o2
For cascade load: R_out ~ gm*ro^2 (higher)
```

## MOSFET Small Signal
```
gm = 2ID/Vov = sqrt(2 kn (W/L) ID)  
r_o = 1/(lambda ID) = VA/ID
Vov = Vgs - Vt
```

## Current Mirror
```
MOSFET (matched, saturation):
  I_out = I_ref  (equal)
  I_out = I_ref * (W/L)_out/(W/L)_ref  (ratio control, 
              if same Vgs and saturation)
BJT mirror: I_out ~ I_ref (beta large)
  Better (cascode/Wilson) improved for accuracy
```

## Mirror output resistance
```
Simple mirror: R_out = r_o (one device)
Cascode mirror: R_out ~ gm2 r_o2 r_o1 (much higher)
Wilson: compares
```

## CMOS Inverter small signal
```
Gain near transition: Av = -(gm_n + gm_p)*(r_o_n || r_o_p)
High at steep region (bias at VDD/2)
```

## Improved gain via cascode
```
Cascode: R_out ~ gm2 * r_o2 * r_o1
Gain: Av = -gm1 * R_out (very large)
```

## Current mirror design formulas
```
Reference current: I_ref = (VDD - Vgs)/R  (for resistor-referenced)
Or I_ref from a diode-connected pair
Output accuracy depends on channel-length modulation (Vds matching)
```

## Quick Reference
| Quantity | Formula |
|----------|---------|
| CS active load Av | -gm1 (ro1||ro2) |
| CMOS inverter Av | -(gm_n+gm_p)(ro_n||ro_p) |
| MOSFET gm | 2ID/Vov |
| r_o | VA/ID |
| Mirror ratio | (W/L)_o/(W/L)_r |
| Cascode Rout | gm ro^2 |
