# ISRO CBT ECE - Memory Tricks: Measurements & Transducers

## 1. Voltmeter Loading - "High is Safe"
**R**emember: **H**igh **R**v = **L**ow **E**rror
- Mnemonic: "Happy Rabbits Have Long Ears" -> High Resistance, Low Error
- Loading Error = Rs/(Rs+Rv): If Rs is 1/100 of Rv, error is ~1%
- Quick: "One percent rule" -> Rv > 100 x Rs

## 2. Wheatstone Bridge - "Cross multiply"
**O**pposite arms **P**roduct **E**qual (OPE)
- R1 x R4 = R2 x R3
- Trick: Draw X through the bridge, multiply along each line
- "X marks the spot for balance"

## 3. Maxwell Bridge - "L = RRC"
**L** = **R** x **R** x **C** (remember as "L-RRC")
- Lx = R2 x R3 x C4
- Rx = R2 x R3 / R4
- "Maxwell's Left RRC" (L = R2 R3 C4)

## 4. Wien Bridge Frequency - "1 over 2 pi R C"
**"One Two Pi RC"** -> f = 1/(2pRC)
- For R = R, C = C case
- Wien = "Win frequency" = 1/(2pRC)

## 5. Schering Bridge - "C ratio, D omega CR"
- Cx/C2 = R4/R3 (capacitance ratio = resistance ratio)
- D = wC4R4 (dissipation = omega times CR)
- "Schering: C ratio, D = wCR"

## 6. LVDT - "Phase tells place"
- In phase = displacement in + direction
- Out of phase (180 deg) = displacement in - direction
- Null = zero displacement
- "PDP: Phase Determines Position"

## 7. Strain Gauge Factor - "GF is delta R over R divided by epsilon"
- GF = (dR/R)/e
- "Got Formulas? Delta R by R, divide by Epsilon"
- For quarter bridge: "V over 4 times GF times epsilon"

## 8. Pt100 - "Point 385"
- Pt100 changes by 0.385 ohm per degree C
- At 100 degC: R = 138.5 ohm
- "Point three eight five is Pt's drive"
- Easy calc: R = 100 + 0.385 x T

## 9. NTC Thermistor - "Exponential Decay"
- NTC = "Negative Temperature, Caps Resist"
- R decreases exponentially with T
- "Big B, Big Change" -> B constant (2000-5000K)

## 10. Thermocouple Types - "KJTE" (K jette)
- **K**: Chromel-Alumel (most common, wide range)
- **J**: Iron-Constantan (good general purpose)
- **T**: Copper-Constantan (low temp)
- **E**: Chromel-Constantan (highest sensitivity)
- "King John Took Every"

## 11. LM35 - "10 milli per degree"
- Output = 10 mV per degree C
- "LM35: Ten millivolts per degree, alive!"
- At 25 degC: 250 mV, at 100 degC: 1000 mV

## 12. PMMC Shunt - "Small goes across"
- Shunt is LOW resistance, goes ACROSS meter
- Rs = Rm/(n-1), n = I/Im
- "Small across, big series" (shunt low, multiplier high)

## 13. PMMC Multiplier - "Series makes voltage"
- Multiplier is HIGH resistance, goes in SERIES
- Rs = Rm(V/Vm - 1)
- "Series for voltage, parallel for current"

## 14. Dual Slope ADC - "Integration cancels"
- RC cancels out in final result
- T1 = integration time (choose for noise rejection)
- "Dual Slope: RC cancels, noise rejects"

## 15. Successive Approximation - "Binary search"
- "MSB first, binary quest"
- n bits = n clock cycles
- "Start high, test and try, keep or drop, bit by bit"

## 16. CRO Rise Time - "35 divided by BW"
- tr = 0.35/BW
- "Thirty-five divided by bandwidth"
- BW in MHz, tr in microseconds

## 17. Lissajous - "Count tangencies"
- fy/fx = horizontal tangencies / vertical tangencies
- "Count horizontal over vertical for frequency ratio"
- "H over V = fy over fx"

## 18. Nyquist - "Double the max"
- fs >= 2 x fmax
- "Sample twice the highest, or aliasing will persist"
- Practical: 5-10x fmax

## 19. SNR per bit - "Six dB per bit"
- Each bit adds ~6 dB to SNR
- 12 bits ~ 72 dB, 16 bits ~ 96 dB
- "Six dB per bit, that's the golden fit"

## 20. Flow Meters - "Venturi recovers, orifice suffers"
- Venturi: high Cd (0.95-0.99), low pressure loss
- Orifice: low Cd (0.60-0.65), high pressure loss
- "Venturi is kind, orifice is not"

## Quick Recall Summary Card
```
LOADING:   Error = Rs/(Rs+Rv) x 100
BRIDGE:    R1xR4 = R2xR3
MAXWELL:   L = R2xR3xC4
WIEN:      f = 1/(2pRC)
SCHERING:  D = wC4R4
LVDT:      Phase = Direction
STRAIN:    GF = (dR/R)/e
PT100:     R = 100 + 0.385T
LM35:      10mV/degC
SHUNT:     Rm/(n-1)
MULTIPLIER: Rm(V/Vm-1)
DUAL SLOPE: RC cancels
SAR:       n bits = n clocks
RISE TIME: tr = 0.35/BW
LISSAJOUS: fy/fx = Nh/Nv
NYQUIST:   fs >= 2xfmax
SNR:       6dB per bit
VENTURI:   Cd = 0.95-0.99
ORIFICE:   Cd = 0.60-0.65
```
