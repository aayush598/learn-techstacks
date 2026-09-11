# Radar Fundamentals - Formulas

## Radar Range Equation
```
Pr = Pt Gt Gr lambda^2 sigma / ((4 pi)^3 R^4)
Pr ~ 1/R^4  (round-trip)
```

## Maximum Range
```
Rmax = [ Pt Gt Gr lambda^2 sigma / ((4pi)^3 P_min ) ]^(1/4)
Max range grows as 4th root of Pt (doubling Pt -> 1.19x range)
```

## Pulse Radar Parameters
```
PRF: fp = 1/T (T = PRI)
Duty cycle = tau/T
Pavg = Ppeak * tau/T
Range resolution: delta_R = c*tau/2
Max unambiguous range: R_unamb = c T/2 = c/(2 fp)
```

## Doppler Shift
```
fd = 2 v cos(theta)/lambda   (radial component v_r = v cos theta)
For radial: v = fd lambda/2
Approaching target -> positive Doppler
```

## FMCW
```
Range: tau_d = 2R/c (time delay), 
Beat freq ~ 2B R/(c T) (sweep)
Velocity: centroid/doppler
```

## Link / SNR
```
SNR = Pt Gt Gr lambda^2 sigma T_integration / ( (4pi)^3 R^4 k T0 B F )
Integration of N pulses: gain ~ N (coherent) or sqrt(N) (noncoherent)
```

## RCS (sigma)
```
sigma = reflected power per unit solid angle / incident power density at target
Typical (m^2): aircraft ~ 1-10, bird ~ 0.01, stealth < 0.001
```

## Quick Reference
| Value | Formula |
|-------|---------|
| Pr | ~1/R^4 |
| Rmax | 4th root |
| Range resolution | c tau/2 |
| Unambiguous range | c/(2 fp) |
| Doppler | 2v/lambda |
| Radial velocity | fd lambda/2 |
| Duty | tau/T |
| Pavg | Ppeak duty |
