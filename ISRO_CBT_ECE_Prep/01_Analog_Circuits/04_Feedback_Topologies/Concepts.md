# Feedback Topologies - Concepts

## Four Basic Feedback Topologies

---

## 1. Voltage Series (Series-Shunt) Feedback
- **Sampling:** Output voltage (shunt at output)
- **Mixing:** Input voltage (series at input)
- **Configuration:** Non-inverting amplifier
- **Effect:** Stabilizes voltage gain, increases input impedance, decreases output impedance
- **Example:** Non-inverting op-amp with R1-R2 divider

### Properties:
- Closed-loop gain: Af = A/(1 + A*beta)
- Input impedance: Zif = Zi(1 + A*beta)
- Output impedance: Zof = Zo/(1 + A*beta)
- Bandwidth: BWf = BW(1 + A*beta)

## 2. Voltage Shunt (Shunt-Shunt) Feedback
- **Sampling:** Output voltage (shunt at output)
- **Mixing:** Input current (shunt at input)
- **Configuration:** Inverting amplifier
- **Effect:** Stabilizes transresistance, decreases both input and output impedance

### Properties:
- Closed-loop transresistance: Rm_f = Rm/(1 + Rm*Gf)
- Input impedance decreases by (1 + A*beta)
- Output impedance decreases by (1 + A*beta)

## 3. Current Series (Series-Series) Feedback
- **Sampling:** Output current (series at output)
- **Mixing:** Input voltage (series at input)
- **Configuration:** Transconductance amplifier
- **Effect:** Stabilizes transconductance, increases both input and output impedance

### Properties:
- Input impedance increases by (1 + A*beta)
- Output impedance increases by (1 + A*beta)

## 4. Current Shunt (Shunt-Series) Feedback
- **Sampling:** Output current (series at output)
- **Mixing:** Input current (shunt at input)
- **Configuration:** Current amplifier
- **Effect:** Stabilizes current gain, decreases input impedance, increases output impedance

---

## Summary Table

| Topology | Sampled | Mixed | Stabilizes | Zi Effect | Zo Effect |
|----------|---------|-------|------------|-----------|-----------|
| Voltage Series | V_out | V_in | Voltage Gain | Increases | Decreases |
| Voltage Shunt | V_out | I_in | Transresistance | Decreases | Decreases |
| Current Series | I_out | V_in | Transconductance | Increases | Increases |
| Current Shunt | I_out | I_in | Current Gain | Decreases | Increases |

---

## ISRO Key Points
- Feedback reduces gain by factor (1 + A*beta) = 1 + T (loop gain)
- Desensitivity factor D = 1 + A*beta
- Gain-bandwidth product remains constant
- Negative feedback reduces distortion, noise, and sensitivity to parameter variations
