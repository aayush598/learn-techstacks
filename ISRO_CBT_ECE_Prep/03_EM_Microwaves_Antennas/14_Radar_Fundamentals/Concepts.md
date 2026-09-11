# Radar Fundamentals - Concepts

## Radar (Radio Detection and Ranging)
- Detect targets, determine range, velocity, angle
- Transmit EM pulse, receive echo
- Works day/night, all weather

## Basic Block
```
Transmitter -> antenna -> target (reflection) -> antenna -> receiver -> processing
Duplexer: shares antenna between Tx/Rx
```

## Radar Range Equation
```
Pr = Pt Gt Gr lambda^2 sigma / ((4pi)^3 R^4)
  sigma = radar cross section (RCS) of target
  R = range
Note: Pr ~ 1/R^4 (round trip -> R^4 unlike monotonic R^2)
```

## Maximum Range
```
Rmax = [Pt Gt Gr lambda^2 sigma/((4pi)^3 Pmin)]^(1/4)
Detection: SNR >= required threshold
```

## Pulse Radar
```
PRF (pulse repetition frequency): fp
PRI (pulse interval): T = 1/fp
Pulse width: tau
Duty cycle: tau/T
Average power: P_avg = P_peak * duty
Range resolution: c*tau/2  (shorter pulse -> better)
   (Two targets resolvable if spacing > c*tau/2)
Maximum unambiguous range:
  R_unamb = c*T/2 = c/(2 fp)
  (Echo must return before next pulse)
```

## Doppler Radar
```
Doppler shift: fd = 2 v cos(theta)/lambda  (radial velocity)
  v = radial velocity
  v = fd lambda/2 (for radial)
Used: moving target detection, speed measurement
```

## Radar Types
- **Pulse radar**: range measurement
- **CW radar**: velocity only (no range)
- **FMCW**: range + velocity (frequency modulated continuous wave)
- **Doppler/MTI**: moving target indication
- **Phased array**: electronic beam steering

## Radar Cross Section (sigma)
- Target property: how much power reflected
- Depends on size, shape, material, aspect angle
- Stealth: reduce RCS via shape/materials

## Performance factors
```
Integration of multiple pulses improves SNR
Clutter: returns from ground/sea/weather (interference)
Clutter reduction: MTI, Doppler filtering
Minimum detectable signal sets max range
```

## Applications
- Military, air traffic control, weather, automotive (adaptive cruise)
- Navigation, altimetry, imaging

---

## ISRO Key Points
- Radars: Pr ~ 1/R^4 (round trip)
- Rmax formula (4th root)
- Range resolution = c*tau/2
- Max unambiguous range = cT/2 = c/(2fp)
- Doppler: fd = 2v/lambda
- Pulse/Doppler/CW/FMCW classifications
