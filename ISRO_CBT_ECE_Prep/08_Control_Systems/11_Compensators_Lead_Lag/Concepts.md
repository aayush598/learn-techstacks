# Compensators (Lead, Lag) - Concepts

## 1. Purpose of Compensation
- **Compensators** are added to improve system performance (stability, accuracy, response speed).
- Modify the open-loop frequency response to:
  - Increase phase margin (lead).
  - Improve steady-state accuracy & low-frequency gain (lag).
  - Achieve desired bandwidth & transient response.
- Compensation modifies the root locus / frequency response to meet specs.

## 2. Lead Compensator

### Transfer Function
G_c(s) = (1 + αTs) / (1 + Ts) = K_c·(s + 1/αT)/(s + 1/T),  with α > 1.

### Characteristics
- Adds **phase lead** (positive phase).
- Zero located further from origin than pole (zero at 1/αT, pole at 1/T; α>1 → zero is left... actually zero closer? zero at s=−1/αT which is closer to origin than pole −1/T).
- **Increases bandwidth** → faster response.
- Increases magnitude at high frequency (by factor α).
- Improves phase margin → reduces overshoot.
- Increases the crossover frequency → reduces settling time.

### Phase Lead Maximum
The maximum phase lead φ_max added at frequency:
ω_max = 1/(T·√α)
φ_max = sin⁻¹[(α−1)/(α+1)]

### Design effects
- Raises gain crossover frequency (ω_gc increases).
- Adds 20log(√α) dB magnitude boost at ω_max.
- Shift (PM increase).

## 3. Lag Compensator

### Transfer Function
G_c(s) = (1 + βTs) / (1 + Ts),  with β < 1 (usually β between 0.05 and 0.2).

Equivalently (1+Ts)/(1+β... ) formulations. Zero closer to origin than pole.

### Characteristics
- Adds **phase lag** (negative phase).
- **Improves steady-state accuracy** (increases low-frequency gain).
- Reduces bandwidth (slower response).
- Increases the DC/low-frequency gain while keeping high-frequency gain unchanged.

### Design philosophy
- Place the lag compensator's corner frequencies well below the crossover so that at crossover the added phase lag is small (avoid excessive PM reduction).
- Improves K_p/K_v (error constants), reduces steady-state error.

### Maximum phase lag location
The larger α (or T ratio), the more low-frequency gain.

## 4. Lead-Lag Compensator
- Combines both: lead part (near crossover) to improve PM/bandwidth, lag part (low freq) to improve accuracy.
- Transfer function: G_c(s) = [(1+αT₁s)/(1+T₁s)]·[(1+T₂s)/(1+βT₂s)] with α>1, β<1.
- Used when both transient and steady-state specs need improvement simultaneously.

## 5. Design Procedure (Frequency Domain)

### Lead Compensator Design Steps
1. Determine required PM from damping/overshoot spec.
2. Compute existing (uncompensated) PM.
3. Find added phase needed, plus margin (5–12°) for ω_gc shift.
4. Compute α from sin⁻¹[(α−1)/(α+1)] = φ_max_added.
5. Determine new gain crossover where added magnitude boost (10log₁₀α) aligns magnitude to 0 dB.
6. Compute T from ω_max = 1/(T√α).
7. Verify.

### Lag Compensator Design Steps
1. Compute required (increased) static error constant → gain boost.
2. Choose lag to add that gain at low frequency.
3. Place zero 1/(βT) one decade below the gain crossover.
4. Place pole 1/T one decade below the zero.
5. Verify PM/bandwidth.

## 6. Root Locus Design
- Lead: add zero-pole with zero closer to origin to pull locus left (increase PM, fast).
- Lag: add a pair near origin (pole near zero) to improve accuracy without changing dominant poles much.

## 7. Effect Summary Table

| Compensator | PM | Bandwidth | Steady-state error | Response speed | Stability |
|---|---|---|---|---|---|
| Lead | ↑ | ↑ | little change | ↑ | ↑ |
| Lag | ↓ (slightly if done right) | ↓ | ↓ (improves) | ↓ | slight |
| Lead-lag | ↑ | ↑ | ↓ | ↑ | ↑ |

## 8. Rule of Thumb
- Small phase margin → use lead (or PD).
- Small error constant → use lag (or PI).
- Both → lead-lag (or PID).

## 9. Physical Implementation
- Lead: RC network with capacitor & phase-leading zero.
- Lag: RC network with pole near origin, zero closer to origin.
- Electronic (op-amp) networks for both.

## 10. ISRO Exam Relevance
- Identify the transfer function of lead/lag compensator.
- Compute φ_max from α.
- Know that lead increases bandwidth, lag improves accuracy.
- Determine what compensator to use from specs.
