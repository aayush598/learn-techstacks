# Power Electronics - Complete Formula Sheet

## SCR/Thyristors
```
Two-transistor analogy: SCR = PNP + NPN
V-I characteristics: forward blocking, forward conduction, reverse blocking
Holding current: IH (minimum current to keep SCR ON)
Latching current: IL (minimum current to turn SCR ON)
Turn-off time: tq = tbr + trr (reverse recovery time)
dv/dt protection: snubber circuit (RC across SCR)
di/dt protection: series inductor
```

## Rectifiers
```
Single-phase half-wave: Vdc = Vm/pi = 0.318*Vm
Single-phase full-wave (center tap): Vdc = 2*Vm/pi = 0.636*Vm
Single-phase bridge: Vdc = 2*Vm/pi = 0.636*Vm
3-phase half-wave: Vdc = 3*sqrt(3)*Vm/(2*pi) = 0.827*Vm
3-phase bridge: Vdc = 3*sqrt(3)*Vm/pi = 1.35*Vml = 2.34*Vmp

Ripple factor: rf = sqrt((Vrms/Vdc)^2 - 1)
Form factor: FF = Vrms/Vdc
Efficiency: eta = Pdc/Pac
```

## DC-DC Converters
```
Buck (step-down): Vo = D*Vin
Boost (step-up): Vo = Vin/(1-D)
Buck-Boost: Vo = D*Vin/(1-D) (inverted polarity)
Flyback: Vo = (D/(1-D))*Vin*(N2/N1)

Duty cycle: D = Ton/T
For CCM:
  Buck: IL = Io, delta_IL = Vin*D*(1-D)/(f*L)
  Boost: IL = Io/(1-D), delta_IL = Vin*D/(f*L)
```

## Inverters
```
Single-phase half-bridge: Vo = +/-Vin/2
Single-phase full-bridge: Vo = +/-Vin
3-phase VSI: line voltage = sqrt(3)*phase voltage
Square wave: fundamental = 4*Vin/(pi*sqrt(2))
THD (square wave) = 48.3%
SPWM THD = 3-5%
SVM THD = 2-4%
```

## Commutation
```
Class A: Load commutation (resonant load)
Class B: Capacitor commutation (self-commutation)
Class C: Complementary commutation
Class D: Auxiliary commutation
Class E: External pulse commutation
Class F: Line commutation
```

## Choppers
```
Type A: 1st quadrant (buck)
Type B: 2nd quadrant (boost再生)
Type C: 1st and 2nd quadrant
Type D: 1st and 4th quadrant
Type E: 1st, 2nd, 3rd, 4th quadrant
```

## Inverter Harmonics
```
Square wave output: harmonics at 3rd, 5th, 7th, ...
Amplitude of nth harmonic: Vn = V1/n
THD = sqrt(sum(Vn^2)/V1^2) for n>=3
SPWM eliminates harmonics around switching frequency
Selective harmonic elimination: can eliminate specific harmonics
```
