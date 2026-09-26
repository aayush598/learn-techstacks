# Chapter 26 — Transistor as a Switch

> **The idea in one line:** a transistor is a switch in two deep regions —
> **cutoff** (fully OFF, no current) and **saturation** (fully ON, minimum
> voltage drop). Same device as the amplifier, but pushed past its linear zone.

---

## 26.1 BJT as a switch

```
   +V_CC
    │
   R_C ─┬──► v_out  (load R_C, e.g., LED+resistor)
    │
  v_in ── R_B ── B
    │          E ── GND
```

### OFF (cutoff) — condition `V_BE < V_γ`
- E-B reverse / barely forward, B-C reverse → no base current.
- `I_C = 0`, `V_CE ≈ V_CC`. The "open switch."

### ON (saturation) — condition `I_B ≥ I_B(min)`
- Both junctions forward; `V_CE(sat) ≈ 0.2 V` (silicon; some books 0.1–0.3 V).
- `I_C(sat) ≈ (V_CC − V_CE(sat))/R_C ≈ V_CC/R_C`.
- **Condition to saturate:** `β·I_B > I_C(sat)` (drive the base harder than
  needed). Overdriving `I_B` by 2–10× ("forced β" less than nominal) guarantees
  saturation with margin.
- `I_B ≥ I_C(sat)/β_min` — the design minimum.

### The switch timing numbers (GATE favourites)
- `t_on`: from OFF to ON — turn-on delay + rise time.
- `t_off`: from ON to OFF — storage time (minority charge removal, the SLOW
  one) + fall time.
- **Saturation slows turn-off** — the transistor must "empty" stored base
  charge. That's why logic gates often clamp base current / use Baker clamps.
- Speeding up: add a turn-off path (resistor from base to emitter for current to
  reverse out).

---

## 26.2 MOSFET as a switch

```
   +V_DD
    │
   R_D ──► v_out
  v_GS ── G (gate directly, no current!)
        S ── GND
```

### OFF — `V_GS < V_th`
- No channel → `I_D = 0`, `V_DS ≈ V_DD`.

### ON — `V_GS ≫ V_th` (drive into triode)
- MOSFET in triode region → behaves as a resistor:
  `R_ds(on) = 1/(k·(V_GS − V_th))` (small; mΩ–Ω).
- `V_DS(ON) = I_D·R_ds(on) ≈ 0` with hard overdrive.
- **Advantage over BJT:** no storage-time delay at turn-off (no minority
  carriers), so it *switches faster*. Driving a gate costs only capacitive
  current (Cgs), not steady base current. This is why power supplies/motor
  drives use MOSFETs.

### Body diode
- A MOSFET has a parasitic diode source→drain; in many switch circuits that
  diode matters (you learn it in power electronics, but GATE analog loves a 1-
  mark "why does it conduct both ways sometimes?" answer: body diode).

---

## 26.3 Comparing switch behaviour — one table

| | BJT | MOSFET |
|---|---|---|
| Driver input | base current (needs I_B) | gate voltage (needs charge, no steady current) |
| Saturation leakage | very low | ~0 when hard off |
| "ON" state | V_CE(sat) ≈ 0.2 V | V_DS(on) = I_D·Ron ≈ 0 |
| Turn-off speed | storage-time limited (slow) | fast (no minority storage) |
| Control polarity | current | voltage |
| Load current capacity | needs big I_B | driven by (W/L), V_GS |

---

## 26.4 Worked switch examples

**Q1.** BJT in saturation, V_CC = 10 V, R_C = 1 kΩ, β_min = 50, V_CE(sat)=0.2.
- `I_C(sat) = (10 − 0.2)/1k = 9.8 mA`.
- Need `I_B ≥ 9.8m/50 = 196 µA` → choose `I_B = 0.5 mA` for margin.
- With `v_in = 5 V`: `R_B = (5 − 0.7)/0.5m = 8.6 kΩ` → standard 8.2 kΩ.

**Q2.** MOSFET, k = 1 mA/V², V_th = 1 V, V_GS = 5 V, I_D = 100 mA.
- `R_ds(on) = 1/(1m·4) = 250 Ω`?? — no: with mA·V²... watch units. `k = 1 mA/V²
  → 10⁻³ A/V²`; `R_ds(on) = 1/(10^-3·4) = 250 Ω` — that's a weak switch; in a
  real design you'd pump V_GS/(W/L). The formula is right; the numbers chosen
  poor — note: V_GS must be several volts above V_th.

---

## GATE traps (switches)

1. **Saturated = V_CE(sat) ≈ 0.2 V, NOT 0.** Students force 0.
2. Condition: `β·I_B > I_C(sat)` → saturated; run the check.
3. MOSFET switch: gate current = 0; driving is *voltage*, not current.
4. Turn-off for BJT is slow due to storage time; MOSFET quick. "Which switches
   faster?" → MOSFET.
5. Triode = switch ON; saturation = amplifier ON — different transistor it is!
6. v_in logic thresholds: BJT needs 0.7 V to start turning on; MOS needs only
   above V_th (which may be < 1 V).

---

## 5-question self-check

1. Cutoff condition for BJT? → *V_BE < Vγ (no base current).*
2. V_CE(sat) typical? → *~0.2 V.*
3. Which has storage-time delay at turn-off? → *BJT.*
4. MOSFET ON region? → *triode (V_GS≫V_th).*
5. Saturation test? → *I_B ≥ I_C(sat)/β.*

Next: **`27-DC-and-AC-Analysis-Method.md`**