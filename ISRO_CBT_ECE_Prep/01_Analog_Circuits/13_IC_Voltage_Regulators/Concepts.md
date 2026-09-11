# IC Voltage Regulators - Concepts

## Voltage Regulator
- Maintains constant output voltage despite input/load changes
- Two types: linear and switching
- Key parameters: line regulation, load regulation, ripple rejection

## Performance Parameters
```
Line regulation = ΔVout/ΔVin  (V/V or %/V)
Load regulation = ΔVout/ΔI_load  (per amp or %)
Ripple rejection: attenuation of input ripple
Dropout voltage: min input-output differential
```

## Linear Regulators
```
Series (pass) transistor: controlled by feedback to drop excess voltage
Advantages: low noise, simple, fast transient response
Disadvantages: low efficiency (P = (Vin-Vout)*I wasted as heat)
Three-terminal ICs: 7805, 7812, 7912 etc.
```

## 78xx / 79xx Series
```
78xx: positive fixed voltage (7805=+5V, 7812=+12V, 7824=+24V)
79xx: negative fixed voltage (7905=-5V, 7912=-12V)
Three pins: IN, GND, OUT
Internal: bandgap reference + error amp + pass transistor
Current up to ~1A typical (7805), heat sink needed
```

## Adjustable Regulators
```
LM317: adjustable positive (1.25V to 37V)
LM337: adjustable negative
Vout = 1.25*(1 + R2/R1) (LM317)
Uses external resistor divider from reference 1.25V
High accuracy, low dropout possible
```

## LDO (Low Dropout Regulator)
- Dropout ~ 0.1-0.5V (vs 2V for standard)
- Uses PNP/PMOS pass element (no Vbe loss)
- Used in battery-powered (maximize efficiency)
- Trade: stability more complex (need ESR control)

## Switching Regulators
```
Buck (step-down), Boost (step-up), Buck-Boost
High efficiency (80-95%)
Uses inductor + switch + control
More complex, more noise
Used for high-power/portability
```

## Zener-based shunt regulator
```
Simple: Zener + series R
Vout = Vz, dissipates excess in zener/resistor
Low current applications, references
```

## Series vs Shunt
| Type | Topology | Efficiency | Use |
|------|----------|------------|-----|
| Series (linear) | pass transistor | low | low noise |
| Shunt (zener) | zener in parallel | low | reference |
| Switching | inductor/sw | high | high power |

## IC Regulator Internals
```
Reference (bandgap/ zener)
Error amplifier (op-amp)
Series pass element
Protection: current limit, thermal shutdown, SOA
Feedback divider (fixed or external)
```

## Applications
- Fixed power supplies (7805/7812)
- Reference (LM317, TL431)
- Battery systems (LDO)
- High efficiency board (switching DC-DC)

## Regulation quality
```
Better: lower line regulation, lower load regulation
Temperature stability from bandgap reference
Good design: <0.1% regulation typical
```

---

## ISRO Key Points
- 7805 = +5V, 7812 = +12V, 79xx = negative
- LM317: Vout = 1.25(1+R2/R1)
- Linear: simple/low-noise, low efficiency
- LDO: low dropout for battery
- Line/load regulation definitions
- Switching: high efficiency
