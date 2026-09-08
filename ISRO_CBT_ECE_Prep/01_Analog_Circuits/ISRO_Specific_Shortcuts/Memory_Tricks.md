# Analog Circuits - Memory Tricks

## Op-Amp Memory Aids

### Gain Signs
- **I**nverting = negative gain (I looks like minus sign)
- **N**on-inverting = positive gain (N for Normal/positive)

### Virtual Ground Rule
- If negative feedback exists: V+ = V- ALWAYS
- If positive feedback: V+ = V- NEVER (comparator/Schmitt trigger)

### Feedback Topology Quick ID
- **Voltage** sampling = shunt at output (V same node)
- **Current** sampling = series at output (I same path)
- **Series** mixing = voltage input
- **Shunt** mixing = current input
- Mnemonic: "VIVI" - Voltage-In, Voltage-Out series feedback stabilizes Voltage gain

### Power Amplifier Efficiency Memory
- **A** = Always 25% (like always late, only 25% on time)
- **B** = Best at 78.5% (B for Best = pi/4)
- **C** = Champion at 90% (C for Champion)

### Oscillator Frequency Mnemonics
- **W**ien bridge = 1/(2piRC) - W for "wavelength depends on R and C"
- **C**olpitts = uses **C**apacitors in divider
- **H**artley = uses **H**-like inductors (tapped coil)
- **Crystal** = most **C**ertain frequency (highest stability)

### Wien Bridge Remember
- Resonant frequency: f = 1/(2piRC)
- At resonance: beta = 1/3
- So gain must be exactly 3 for oscillation
- "One third requires three" (beta=1/3 needs gain=3)

### Diode Drop Quick Reference
- Si = 0.7V: "**S**even point **S**even" - **S**i = **S**eventy
- Ge = 0.3V: "**G**ermanium = point **G**ree" (green = 0.3)
- LED = 1.5-2V: "**L**ED = **L**arger"

### Rectifier Formulas
- Half wave = "**H**alf the work = **H**alved output" (Vm/pi)
- Full wave = "**F**ull = **F**aster" (2Vm/pi = double)
- Bridge = "**B**ridge = **B**etter ripple" (ripple factor 0.48 vs 1.21)

### Filter Order Memory
- **1st order** = -20 dB/decade slope
- **2nd order** = -40 dB/decade slope
- **nth order** = -20n dB/decade slope
- "Each pole pushes down by 20" (like a slope)
