# Chapter 27 — The DC and AC Analysis Method (Master Workflow)

> **The idea in one line:** every transistor-amplifier problem is the same three
> steps: **① set the DC Q-point, ② convert to the AC small-signal circuit,
> ③ compute gain/input/output impedance.** Master these three steps and you can
> solve any amplifier numerical in the syllabus cold.

---

## 27.0 The method at a glance

| Step | Do | Result |
|------|----|--------|
| 1. DC analysis | Open caps, kill AC sources | `I_C/I_D`, `V_CE/V_DS`, region |
| 2. Small-signal parameters | From Q-point | `gm,rπ,re,ro` (BJT) / `gm,ro` (MOS) |
| 3. AC equivalent | Short caps (midband), ground supplies, replace device | linear circuit |
| 4. Solve | KCL/KVL | `A_v, A_i, R_in, R_out, BW` |

---

## 27.1 Step 1 — DC analysis (find the Q-point)

**Precept:** *the DC Q-point tells you everything, including the region.*

1. **Replace all capacitors with open circuits** (they block DC).
2. **Kill AC sources** (set them to 0). Keep DC supplies; keep AC supplies open
   or with their internal resistance if given.
3. Redraw the DC path: often a divider + a base/emitter loop.
4. Assume a region to start (usually active/saturation), write equations,
   compute; **then verify** the assumption (see the region check table).
5. If the assumption fails, re-solve in the correct region (triode/saturation).

### Region check (both devices)
| Device | Active/Sat condition | Validate |
|--------|----------------------|----------|
| BJT | `V_C > V_B > V_E` (NPN) | `V_CE ≥ 0.2 V` for active |
| NMOS | `V_DS ≥ V_GS − V_th` | use here |
| PMOS | `V_SD ≥ V_SG − |V_th|` | mirror |

**Always write the verify line.** GATE gives traps where the easy assumption
(saturation) is wrong and the transistor is in triode.

---

## 27.2 Step 2 — Know every parameter from the Q-point

**BJT:**
```
gm = I_C/V_T            (V_T = 25 mV @ 300 K)
rπ = β/gm = β·V_T/I_C
re = V_T/I_E ≈ V_T/I_C
ro = V_A/I_C
```
**MOSFET:**
```
gm = 2I_D/(V_GS − V_th) = √(2kI_D) = k(V_GS − V_th)
ro = 1/(λ·I_D)
```
If any is missing from the list, derive from the pair you have (square law /
transport equations).

---

## 27.3 Step 3 — The AC (small-signal) equivalent circuit

Rules to build it *without thinking*:

1. **Short all capacitors** (coupling and bypass) — that's the midband.
2. **Ground all DC supplies** (V_CC, V_DD → AC ground; take the node to 0 V).
3. Replace the transistor with its small-signal model:
   - BJT hybrid-π: `rπ` from B→E; `gm·v_be` from C→(out of emitter);
     `ro` from C→E.
   - MOS: gate open; `gm·v_gs` D→S; `ro` D→S.
4. Redraw neatly; mark `v_in`, `v_out`, and each resistor.

**Common conventions GATE uses:**
- `R_in` = resistance *looking into the amplifier input* (include the source R? 
  separate — GATE usually asks for the input-resistance-at-the-terminals, i.e.,
  not counting source). 
- `R_out` = resistance looking *into the output* with input killed and the 
  load removed.
- `A_v = v_out/v_in`; `A_vs = v_out/v_sig` if source resistance given.
- `A_i = i_out/i_in`.

---

## 27.4 Step 4 — Computation tactics

- **Voltage gain CE/CS:** `−gm·(R_C∥R_L)` or `−gm·(R_D∥R_L)`, with ro added in
  parallel when given.
- **With source resistance:** first find `v_in` from `v_sig` via
  `v_in = v_sig·R_in/(R_in + R_s)`.
- **Input resistance shortcuts:**
  - CE (unbypassed R_E): `R_in = R_b1∥R_b2∥(β+1)(re + R_E)` — note `re+R_E`,
    not `R_E` alone.
  - CE (bypassed): `R_in = R_b1∥R_b2∥rπ`.
  - CB: `R_in ≈ re`.
  - CC: `R_in = (β+1)(re + R_E∥R_L)` (huge).
  - CS: `R_in = R_G`.
  - CG: `R_in ≈ 1/gm`.
  - CD: `R_in = R_G`.
- **Output resistance:** mostly just the load/drain/collector resistor
  (`R_C`, `R_D`) or `ro` figures if λ/V_A given.

---

## 27.5 The four analysis "tools" you must deploy

- **Thevenin trick:** replace complex bias dividers with V_th + R_th (Chapter 1).
- **Test-source method:** to find R_out, kill sources, apply a test V/I at the
  output, solve `R_out = V_test/I_test`.
- **Half-circuit / symmetry:** differential pair solving halves the work.
- **Virtual ground:** inverting op-amp nodes.

---

## 27.6 Complete worked example (only one you'll ever need)

**CE amplifier:** V_CC=12, R1=100k, R2=25k, R_C=4k, R_E=1k (bypassed), R_L=4k,
β=100, V_BE=0.7, V_T=25mV, V_A=100.

**Step 1 — DC:** 
- `V_B = 12·25/125 = 2.4 V`; `V_E = 1.7`; `I_E = 1.7/1k = 1.7 mA`;
  `I_C ≈ 1.7 mA`; `V_C = 12 − 1.7m·4k = 5.2 V` > `V_B` ✓ active.
- `V_CE = 12 − 1.7m·5k = 3.5 V`.

**Step 2 — params:**
- `gm = 1.7m/25m = 68 mA/V`.
- `rπ = β/gm = 100/0.068 ≈ 1.47 kΩ`.
- `ro = 100/1.7m ≈ 59 kΩ`.

**Step 3 — AC circuit:** C_E shorted, supplies ground, transistor = rπ + gm·v_be
(in parallel with ro on output).

**Step 4 — solve:**
- `R_load = R_C ∥ R_L ∥ ro = 4k∥4k∥59k ≈ 1.9 kΩ`.
- `A_v = −gm·R_load = −68m·1.9k = −129`.
- `R_in = R1∥R2∥rπ = 100k∥25k∥1.47k ≈ 1.38 kΩ`.
- `R_out = R_C = 4 kΩ` (ro dominated).
- If source `R_s = 1 kΩ`: `A_vs = A_v·R_in/(R_in+R_s) = −129·1.38/2.38 = −75`.

---

## 27.7 When a capacitor is NOT shorted (low-frequency / high-frequency)

- **Low freq:** coupling/bypass caps become finite → use `1/(jωC)` and
  recompute gains (Chapter 16). The method *same*, just new elements.
- **High freq:** add internal caps Cπ/Cμ (BJT) or Cgs/Cgd (MOS) + Miller
  (Chapter 16).
- **Rule:** if the problem says "midband," short ALL external caps and ignore
  internal caps. That's the default GATE setting.

---

## GATE traps (method)

1. **Always verify region.** A "saturation" answer used in cutoid region is
   worth zero.
2. `R_in` excludes the source resistance; `A_vs` includes it. Read which is
   asked.
3. Bypassed vs unbypassed: look for the capacitor `C_E/C_S`. One cap flip
   changes everything.
4. Don't forget `ro`/`V_A` when given; its inclusion drops gain slightly.
5. `1/(jωC)` low-freq: use both polar/rectangular; don't build heroic algebra —
   GATE numbers are round.
6. Redraw the model; a sloppy drawing = sign slips (particularly −gm paths).

---

## 5-question self-check

1. Order of the 4-step method? → *DC Q, params, AC equivalent, solve.*
2. In midband, external caps? → *shorts.*
3. DC supplies in AC? → *grounded.*
4. R_in of CE with R_E unbypassed ≈ ? → *R_b∥(β+1)(re+R_E).*
5. Saturation verification uses? → *V_CE ≥ 0.2 V (BJT) / V_DS≥V_GS−V_th (MOS).*

Next: **`28-Graphical-Interpretation.md`**