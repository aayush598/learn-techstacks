# Power Amplifiers - Formulas

## Class A Amplifier
```
Maximum Efficiency (resistive load):  eta_max = 25%
Maximum Efficiency (transformer):    eta_max = 50%

DC Power Supply:  Pdc = Vcc * Icq
AC Output Power:  Po = Vcc * Icq / 2 (peak sine wave)
Efficiency:       eta = Po/Pdc * 100%

For maximum output swing:
  Vce_q = Vcc/2 (center of load line)
  Icq = Vcc/(2*Rl)
```

## Class B Amplifier (Push-Pull)
```
Maximum Efficiency:  eta_max = pi/4 = 78.5%

DC Power Supply:  Pdc = 2*Vcc*Ipeak/pi
AC Output Power:  Po = Ipeak*Vcc/2
Efficiency:       eta = Po/Pdc = pi*Vpeak/(4*Vcc)

For maximum efficiency: Vpeak = Vcc
  Po_max = Vcc^2/(2*Rl)
  eta_max = pi/4 = 78.5%
```

## Class AB Amplifier
```
Efficiency: 25% < eta < 78.5%
Typical: 50-60%

Bias voltage: Vbias = 2*Vbe (for silicon transistors)
  Vbias approximately 1.2V - 1.4V
```

## Class C Amplifier
```
Conduction angle: theta < 180 degrees
Efficiency: 80-90%

With tank circuit:
  Output frequency = resonant frequency of tank
  f0 = 1/(2*pi*sqrt(LC))
```

## Class D Amplifier
```
Efficiency: 90-95% (practical)
Output: PWM signal filtered by LPF

Output voltage: Vo = D * Vcc (D = duty cycle)
```

## Crossover Distortion
```
Dead zone: -Vbe < Vin < +Vbe (approximately -0.7V to +0.7V for Si)
Both transistors OFF in this region
Eliminated by Class AB biasing: Vbias = 2*Vbe
```

## Thermal Considerations
```
Power dissipation per transistor:
  Class A: Pd = Pdc (all power dissipated when no signal)
  Class B: Pd_max = 0.1*Po_max (at 50% of max output)

Heat sink formula:
  Tj = T Ambient + Pd * (Rth_jc + Rth_cs + Rth_sa)
  where Rth = thermal resistance (degrees C/W)
```

## Quick Reference
| Class | Max eta | Pd_max formula | Key Formula |
|-------|---------|---------------|-------------|
| A | 25% | Vcc*Icq | eta = Po/(Vcc*Icq) |
| B | 78.5% | 0.2*Vcc^2/(pi^2*Rl) | eta = pi/4 |
| AB | ~50% | Between A and B | - |
| C | 90% | - | Needs tank circuit |
| D | 95% | Near zero (switching) | PWM based |
