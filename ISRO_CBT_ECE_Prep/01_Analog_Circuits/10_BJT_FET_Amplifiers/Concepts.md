# BJT and FET Amplifiers - Concepts

## BJT Amplifier Configurations
| Config | Gain Av | Ai | Zi | Ro | Phase |
|--------|---------|----|----|----|-------|
| Common Emitter (CE) | high | high | med | high | 180 deg |
| Common Base (CB) | high | ~1 | low | high | 0 |
| Common Collector (CC) | ~1 | high | high | low | 0 |

- CE: most common amplifier
- CB: for high frequency (cascode)
- CC: emitter follower, buffer (impedance)

## BJT DC Biasing
```
IE = (VBB - VBE)/RE (approx, with emitter resistor)
Stable biasing: self-bias (voltage divider + emitter R)
IC ~ IE (beta large), gain stability
Operating point (Q): IC, VCE set in active region
```

## CE Amplifier Small Signal
```
gm = IC/VT  (transconductance, VT=26mV)
r_pi = beta/gm = VT/IB
r_o = VA/IC (output resistance, early effect)
Av = -gm (RC || r_o || RL)  (approx -gm RC)
Zi = RB || r_pi
Zo ~ RC
```

## BJT Current relationships
```
IC = beta IB = alpha IE
alpha = beta/(beta+1)
beta = alpha/(1-alpha)
IF equality: alpha = IC/IE
```

## Early Effect
- Output resistance r_o due to base-width modulation
- r_o = VA/IC; VA = Early voltage
- Reduces gain slightly (finite output impedance)

## FET Amplifier (MOSFET/JFET)
```
Configs: Common Source (CS), Common Drain (CD), Common Gate (CG)
Similar roles to CE/CB/CC
gm: transconductance
  MOSFET: gm = 2*ID/Vov (Vov = Vgs - Vt)
CS gain: Av = -gm (RD || r_o || RL)
CD (source follower): Av ~ 1, high Zi, low Zo
CG: low Zi, high gain, buffer
```

## MOSFET region conditions
```
Cutoff: Vgs < Vt
Saturation (active): Vds > Vov, gm = 2ID/Vov
Triode: Vds < Vov, behaves as resistor
Drain current (saturation): ID = (1/2)kn(Vov)^2
```

## Small-Signal Summary
```
Common Source: -gmRD, high Zi, high Zo
Common Drain: ~+1, highest Zi, low Zo
Common Gate: +gmRD, low Zi, high Zo
```

## Cascode
- CE (CS) + CB (CG) stacked
- High output impedance, low Miller effect (high BW)
- Used in high-frequency amps

## Frequency considerations
- Miller effect capacitance: Cm = Cgd*(1 + Av) (CS/CE)
- Limits bandwidth
- Cascode reduces Miller cap

## Amplifier Coupling
- Direct, RC (capacitive), transformer
- RC coupling: blocks DC between stages
- Direct: DC coupling, more gain at low freq

---

## ISRO Key Points
- CE: max gain, 180 deg phase
- Av = -gm RC (CE), gm = IC/VT
- CC: buffer, Av~1, high Zi
- CS: -gm RD, gm=2ID/Vov
- Cascode: wide BW (low Miller)
- CF (Darlington): very high gain
