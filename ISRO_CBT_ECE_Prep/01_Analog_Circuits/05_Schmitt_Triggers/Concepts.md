# Schmitt Triggers - Concepts

## Regenerative Comparator (Schmitt Trigger)

---

## Inverting Schmitt Trigger
- Input applied to inverting terminal through R1
- Non-inverting terminal has feedback from output through R2
- Output saturates at +Vsat or -Vsat
- Hysteresis prevents noise-induced switching

### Threshold Voltages:
- **Upper Threshold Point (UTP):** Vut = +Vsat * R1/(R1+R2)
- **Lower Threshold Point (LTP):** Vlt = -Vsat * R1/(R1+R2)
- **Hysteresis Width:** VH = Vut - Vlt = 2*Vsat*R1/(R1+R2)
- **Center Voltage:** Vcenter = 0V (symmetric supply)

### Transfer Characteristics:
- When input < LTP: Output = +Vsat
- When input > UTP: Output = -Vsat
- Between LTP and UTP: Output maintains previous state

---

## Non-Inverting Schmitt Trigger
- Input applied to non-inverting terminal
- Inverting terminal has voltage divider from output
- Similar hysteresis behavior

### Threshold Voltages:
- Vut = Vsat * (R2)/(R1+R2) (for reference at inverting terminal)
- Hysteresis width remains: VH = 2*Vsat*R2/(R1+R2)

---

## Key Features:
1. **Noise Immunity:** Input noise within hysteresis band does not cause false triggering
2. **Speed:** Regenerative feedback makes transition very fast (approaches switching speed of op-amp)
3. **Square Wave Generation:** Sinusoidal input produces square wave output
4. **Schmitt Trigger Oscillator:** RC feedback from output to input creates relaxation oscillator

## Schmitt Trigger as Oscillator:
```
Frequency: f = 1 / (R*C*ln((1+beta)/(1-beta)))
where beta = R1/(R1+R2)
```

---

## ISRO Key Points
- Schmitt trigger has TWO threshold voltages (unlike comparator with one)
- Hysteresis width = 2 * Vsat * R1/(R1+R2) for inverting type
- Used for: square wave generation, noise elimination, pulse shaping
- Op-amp in Schmitt trigger runs in saturation (not linear region)
- Transition time depends on op-amp slew rate
