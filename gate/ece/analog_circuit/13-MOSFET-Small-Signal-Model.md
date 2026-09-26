# Chapter 13 — MOSFET Small-Signal Model

> **The idea in one line:** in saturation, a MOSFET turns V_GS variation into
> I_D variation through **gm** (its transconductance). The small-signal model
> is simpler than the BJT: an **infinite input resistance** at the gate, a
> current `gm·v_gs` from drain to source, and an output resistance `ro`.

---

## 13.1 The model (saturation, λ ≠ 0)

```
        G ──────────────── (open — no gate current)
                           │
   v_gs ─(+)     gm·v_gs ▼ D
        S ──────────────── ┤
                           │
                        ┌──┤ (ro between D and S)
                        ro │
                        └──┤
                           S
```
Three elements only:
- **Open circuit** between gate and source (infinite R_in).
- **Current source** `gm·v_gs` between drain and source (direction: from drain
  to source for NMOS).
- **Output resistance** `ro = 1/(λ·I_D)` between drain and source, in parallel
  with the current source.

### Key parameters (all at the Q-point)
```
gm  = 2·I_D / (V_GS − V_th)      (from square law: gm = ∂I_D/∂V_GS)
    = √(2·k·I_D)                 (equivalently)
    = k·(V_GS − V_th)            (since I_D = ½k(V_GS−V_th)²)
ro  = 1/(λ·I_D)                  (λ>0 in saturation)
```
Pick whichever form has given numbers. All three are connected through the
square law — pick one identity and derive the rest.

---

## 13.2 gm derivation (intuition vs formula)

From `I_D = ½k(V_GS − V_th)²`:
```
gm = dI_D/dV_GS = k·(V_GS − V_th)
                     = 2·I_D/(V_GS − V_th)
                     = √(2·k·I_D)
```
So:
- Larger `I_D` (or larger overdrive `V_GS−V_th`) → bigger gm.
- Double I_D → gm × √2 (not 2×). Classic multiple-choice check.

---

## 13.3 Body effect in the small-signal model

If source and body are NOT tied together, an extra term appears:
```
i_d = gm·v_gs + gmb·v_bs
gmb = η·gm,   η = gmb/gm ≈ 0.1–0.3  (typ 0.1–0.2)
```
- `v_bs` between body and source also modulates I_D.
- `gmb` adds a second (smaller) source between source and body.
- For most GATE problems: bulk–source connected → no body effect. Only worry
  when the figure shows a separate body terminal to supply.

---

## 13.4 Model simplifications (what GATE expects)

| If | Then |
|----|------|
| λ = 0 (ideal) | remove ro; leave only gm·v_gs source |
| Body tied to source | no gmb |
| "∞ output resistance" | ro → ∞, i.e., drop it |
| Source degenerated (R_S unbypassed) | keep R_S in the AC path (Ch 14) |

Practical numbers: `gm ≈ 1–10 mA/V`, `ro ≈ 10–500 kΩ`.

---

## 13.5 Worked parameter set

NMOS: `k = 2 mA/V²`, `I_D = 2 mA`, `V_th = 1 V`, `λ = 0.02`.

- `V_GS − V_th = √(2·I_D/k) = √(2·2m/2m) = √2 ≈ 1.414 V`.
- `gm = 2·I_D/(V_GS−V_th) = 4m/1.414 = 2.83 mA/V`.
  (Check: gm = k·(V_GS−V_th) = 2m·1.414 = 2.83 ✓)
- `ro = 1/(λ·I_D) = 1/(0.02·2m) = 25 kΩ`.

---

## 13.6 How to find parameters from a circuit

1. Do the DC analysis (Ch 12) → get `I_D`, `V_GS`, region (must be saturation).
2. Compute `gm` (pick the formula with data you have).
3. Compute `ro` if λ given.
4. Replace the MOSFET with the model, ground the supplies, solve the linear
   circuit (Ch 14).

---

## GATE traps (MOSFET small-signal)

1. **gm formula form mismatch:** `√(2kI_D)` vs `k(V_GS−V_th)` — both are the same
   number; students mix units (mA/V vs mA/V²×V).
2. Gate is open — R_in at gate = ∞ (no rπ!). Students "borrow" BJT habits.
3. `gm = k·(V_GS-V_th)`: if V_GS−V_th is doubled, gm doubles; but doubling I_D
   only raises gm by √2 — know the *dependences*.
4. ro = `1/(λI_D)`, not `1/λ` alone.
5. gmb only when body not tied to source — check the schematic.
6. In saturation only. If triode/cutoff, the entire model is invalid.

---

## 5-question self-check

1. `I_D = 0.5 mA`, `V_GS−V_th = 1 V`. gm? → *2·0.5m/1 = 1 mA/V.*
2. Same but λ=0.04: ro? → *1/(0.04·0.5m) = 50 kΩ.*
3. Double I_D → gm multiplies by? → *√2.*
4. Input resistance at MOSFET gate? → *∞.*
5. gmb/gm typical ratio? → *≈ 0.1–0.3.*

Next: **`14-MOSFET-Amplifiers.md`**