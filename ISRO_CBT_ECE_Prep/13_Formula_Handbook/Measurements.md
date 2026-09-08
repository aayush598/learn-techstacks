# Measurements & Transducers - Complete Formula Sheet

## Measurement Fundamentals
```
Accuracy = 1 - |measured-true|/true
Precision = repeatability of measurements
Sensitivity = output change / input change = dV/dx
Loading effect = 1 - (Rm/(Rm+Rs)) for voltmeter
Resolution = smallest detectable change
```

## DC Bridges
```
Wheatstone bridge:
  Balanced when: R1/R2 = R3/R4
  Sensitivity: S = d(theta)/dR = (Vb*Gd)/(4*R) approximately
  Best accuracy when all arms approximately equal

Kelvin double bridge: For low resistance measurement (< 1 ohm)
  R = Rs*R1/R2 (when bridge balanced)
```

## AC Bridges
```
Wien bridge: f = 1/(2*pi*R*C)
  Balanced when: R1/R2 = R3/R4 + C4/C3 (for equal arms: f = 1/(2*pi*RC))

Maxwell inductance bridge: Lx = R2*R3*C4, Rx = R2*R3/R4
  Used for: inductance measurement (Q < 10)

Hay bridge: Lx = R2*R3*C4/(1+(w*R4*C4)^2)
  Used for: high Q inductors (Q > 10)

Schering bridge: Cx = C1*(R1/R2), tan(delta) = w*C4*R4
  Used for: capacitance and dissipation factor

Anderson bridge: Universal bridge for inductance
```

## PMMC Instruments
```
Deflecting torque: Td = B*I*A*N
  B = flux density, I = current, A = area, N = turns
Control torque: Tc = k*theta (spring constant)
Damping torque: Tdamp = B^2*l^2*v/R (eddy current)
At equilibrium: Td = Tc

Multi-range extension:
  Shunt resistance: Rs = Rm/(m-1) where m = I/Im (multiplier)
  Series multiplier: Rs = Rm*(m-1) where m = V/Vm
```

## LVDT
```
Output voltage: Vout = k*(x - x0) (linear near null)
Sensitivity: S = Vout/displacement (mV/mm)
Null position: Vout = 0
Phase reversal: crosses null point
Linearity range: typically +/-2.5mm to +/-500mm
```

## Strain Gauges
```
Gauge factor: GF = (dR/R)/epsilon = (1+2*nu) + (dR/R)/epsilon
  where nu = Poisson's ratio
  For metallic: GF approximately 2
  For semiconductor: GF approximately 100-200

Quarter bridge: dV/V = (GF*epsilon)/4
Half bridge: dV/V = (GF*epsilon)/2
Full bridge: dV/V = GF*epsilon

Temperature compensation: Dummy gauge method
```

## Voltmeter Loading
```
Sensitivity: S = Rv/Vfs (ohms per volt)
  Where Rv = voltmeter resistance, Vfs = full-scale voltage
Minimum sensitivity: S >= 1/Rload
Loading error: (Rv/(Rv+Rs) - 1)*100% approximately
For accurate measurement: Rv >> Rs (at least 10x)
```

## Temperature Transducers
```
RTD (Pt100): R = R0*(1 + alpha*T + beta*T^2)
  R0 = 100 ohms, alpha = 0.00385/degree C

Thermistor: R = R0*exp(B*(1/T - 1/T0))
  NTC: B positive, R decreases with T
  PTC: R increases with T

Thermocouple: V = S*(T1-T0) (Seebeck effect)
  S = Seebeck coefficient (uV/degree C)
```
