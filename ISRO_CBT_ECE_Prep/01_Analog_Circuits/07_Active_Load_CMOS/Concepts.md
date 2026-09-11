# Active Load and CMOS Amplifiers - Concepts

## Active Load Concept
- Use a transistor (instead of resistor) as load
- High output impedance at DC (like high R)
- Low voltage drop (transistor saturates) -> larger voltage swing
- Used in op-amps, analog ICs
- Gain = gm * (high output impedance) = very large

## Why Active Load
```
Resistor load: R is large value but consumes headroom (V_DC drop)
Active (current-source) load: 
  high impedance (large R_o) without large DC drop
  => very high voltage gain in single stage
```

## Current Mirror
- Core building block: sets bias currents
- Basic MOSFET current mirror: two matched MOSFETs same Vgs
- I_out = I_ref (for matched, in saturation)
- Ratio controlled by W/L ratio

### Mirror ratio (MOSFET)
```
I_out/I_ref = (W/L)_out/(W/L)_ref  (in saturation)
For BJT mirror: Iout ~ Iref (approx equal)
```

## Common Source with Active Load
```
Av = -gm1 * (r_o1 || r_o2)   (gain stage)
PIELES: load transistor pMOS provides high r_o
Very high gain (~ gm * ro tens of thousands, or thousands)
```
- gm1 of driver, r_o1||r_o2 of both transistors

## CMOS Amplifier configurations
```
Single CS with diode-connected load (lower gain)
CS with current mirror load (high gain)
CMOS inverter amplifier (large gain near switching)
Cascode (wide BW, high impedance)
```

## CMOS Inverter as Analog Amp
- Biased at VDD/2 (transition region)
- Both nMOS and pMOS conduct
- High small-signal gain at steep switching point
- Used as simple amplifier / output stage

## Output Impedance
```
High-impedance active-load stage: R_out = r_o_n || r_o_p
Want high R_out for high gain
Cascode increases R_out further (gm*ro^2)
```

## CMOS Small-Signal Model
```
gm = 2ID/(Vgs - Vt) = sqrt(2 kn ID)
r_o = 1/(lambda ID) = VA/ID
Gain (CS): Av = -gm * R_out
```

## Applications
- Op-amp input stage (differential + active load)
- Very high gain single stage
- Low voltage IC design (rail-to-rail)
- Same technology as digital CMOS (mixed-signal)

## Trade-offs
```
Active load -> high gain but lower bandwidth (high impedance, parasitic cap)
Lower supply voltage benefits from low-drop active loads
Matching requirement for current mirrors
```

---

## ISRO Key Points
- Active load = transistor as load (high impedance, low DC drop)
- CS + active load: Av = -gm(ro1||ro2)
- Current mirror sets / replicates bias current
- Mirror ratio: (W/L) ratio
- CMOS inverter biased mid -> high gain
- Active load used in op-amps for high gain
