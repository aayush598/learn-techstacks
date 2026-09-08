# Network Theory - Memory Tricks

## Initial Condition Rules
- **Capacitor**: "**C - continuity of Voltage**" (Vc same at t=0+)
- **Inductor**: "**L - Let current flow the same**" (iL same at t=0+)
- At t = infinity (DC): "**C = Open, L = Short**" (opposites)
- Mnemonic: "**C-eption Voltage, L-current**" (CLV-LC)

## RLC Resonance
- **Series: Z = R minimum** (like a "short" passage for current)
- **Parallel: Z = L/RC maximum** (like a "blocked" passage)
- "**Series is Slender (low Z), Parallel is Proud (high Z)**"

## Q-Factor
- **Series Q = w0*L/R** - "**Q = wL over R**"
- **Parallel Q = R/(w0*L)** - "**Q = R over wL**"
- Completely opposite formulas!

## Thevenin vs Norton
- **Thevenin**: Voltage source in series with Rth
- **Norton**: Current source in parallel with Rn
- "**TV** (Thevenin Voltage) in series, **NC** (Norton Current) in parallel"

## Superposition
- **Voltage source = 0 -> short circuit** ("**kill the V, close the wire**")
- **Current source = 0 -> open circuit** ("**kill the I, open the wire**")
- Only valid for LINEAR circuits

## Mason's Gain
- **Delta = 1 - sum(loops) + sum(2 non-touching products) - ...**
- "**Single, Double, Triple -> subtract, add, subtract**"

## Two-Port Parameters
- **Z**: impedance (Volts over Amps) - "**Z-V**" (matrix gives V)
- **Y**: admittance (Amps over Volts) - "**Y-I**" (matrix gives I)
- **ABCD**: cascade convenient - "**Multiply for series**"

## Time Constant
- **RC**: tau = R*C - "**Tau = R times C**" (product of resistor and capacitor)
- **RL**: tau = L/R - "**Tau = L over R**" (division)
- The formula is ALWAYS the inverse-looking one

## First Order Universal
- **x(t) = x(inf) + [x(0+) - x(inf)]*e^(-t/tau)**
- "**Final plus difference times exponential decay**"
- If x(0+) > x(inf): exponential term subtracts (decay from initial to final)
