# Chapter 04 — Clamping Circuits

> **The idea in one line:** A clamper *shifts the whole waveform up or down*
> without changing its shape. A capacitor stores a DC offset; the diode decides
> in which direction. Clip → "cut shape"; clamp → "lift shape".

---

## 4.1 The basic clamper (positive)

```
      ┌─ C ─┐
 v_in │     │
      ▼     ▼
      └ ►▷ └────── v_out
            │
           R_L (to ground, large)
```

Elements: coupling capacitor `C`, one diode, load resistor `R_L` (large).
- `R_L` is large so the capacitor discharges very slowly (RC ≫ period).
- The diode conducts only during the interval that clamps one side of the
  waveform to the reference (usually ground).

### Operation of a positive clamper (ideal diode, no offset)
Input `v_in = Vm·sin(ωt)` swinging ±Vm.
1. First negative peak: diode conducts (cathode goes negative), capacitor
   charges to `Vm` with the polarity shown (negative plate toward the left).
2. When input rises back up, diode stops conducting. The capacitor *holds*
   `Vm` (because `R_L` large, discharge negligible).
3. Output = input + the stored `Vm`: the zero of the signal is now *positive*.
   The signal that swung `±Vm` now swings `0 to +2Vm`.
4. Steady state: negative peaks just touch ground.

**Result:** the waveform is shifted *up* so its bottom touches 0.
**Vertical shift = `Vm` for a sine.** Shape is otherwise *identical*.

### Negative clamper
Diode flipped. Capacitor charges to `−Vm` on the positive peak; output swings
`0 to −2Vm`; the *top* of the wave touches ground.
**Result:** shift *down* by `Vm`, top at 0.

---

## 4.2 Key rules you must internalize

1. **Clamping does not change amplitude/shape** — only the DC (vertical) level.
2. The direction of shift is set by the **diode direction**:
   - Anode of diode toward input side → positive clamp (shifts up).
   - Cathode toward input side → negative clamp (shifts down).
3. The level the *reference* side touches equals `±V_ref` (with no DC source,
   reference is 0/ground).
4. Diode conduction interval = the half-cycle that *charges the capacitor*.
5. `R_L·C ≫ T` keeps the offset steady across cycles; if `RC` is small, the
   waveform "droops" (see 4.4).

---

## 4.3 Biased clampers

A DC battery `V_B` in series with the diode changes the reference level to
which the waveform clamps.

### Positive biased clamper
Battery `V_B` (polarity such that it helps the diode conduct) between diode and
ground:
- Capacitor charges until the *lowest* negative excursion, reduced by `V_B`,
  brings diode to conduction. Output bottom clamps to `+V_B`.
- Waveform swing: `V_B` to `V_B + 2Vm` for the standard sine.
- i.e. **positive clamp by `Vm + V_B`**.

### Negative biased clamper
Waveform's top clamps to `−V_B`. Swing: `−(V_B + 2Vm)` to `−V_B`.

General statement: *a biased clamper slides the signal until the extreme that
the diode's orientation sees reaches the level `V_ref` at the diode's other
terminal.*

---

## 4.4 Effect of the RC time constant (droop)

- If `R_L·C ≫ T`: near-perfect clamping (flat top/bottom at reference).
- If `R_L·C` comparable to `T`: capacitor discharges *during* the non-conducting
  interval, so the output decays exponentially **toward zero** (droop/sag).
- Droop across half a period ≈ `(T/2)/(R_L·C)` fraction of the retained voltage.
- GATE may ask: *"If the time constant is small, the clamped peak decays — is it
  charging or discharging between diode pulses?"* Answer: **discharging** through
  `R_L`.

### Initial conditions
- First cycle charges the capacitor; steady state is established after a few
  time constants. GATE usually asks for the **steady-state** waveform.
- If `R_L` is infinite (ideal), the offset holds forever.

---

## 4.5 Cycle-by-cycle analysis (the skill GATE tests)

Given arbitrary periodic input (square, triangle, sine), analyze one full
period in fragments:

1. Pick the first extreme where the diode **conducts** (the direction that
   changes the capacitor voltage). Determine `V_C` it charges to
   (≈ the peak difference seen in that interval).
2. Switch to non-conduction; capacitor voltage is held (or droops if stated).
3. Write `v_out = v_in ± V_C` over each interval.
4. Repeat until the waveform repeats (steady state).

**Square-wave example:** input `0 ↔ +10 V` appearing at `v_in` of a positive
clamper (ideal):
- Diode conducts on the *low* level? No — the cathode is at 10 V? Let's be
  precise with the positive-clamper polarity from 4.1.
- With the shown circuit, cathode side connects to the input through C. On the
  interval `v_in` swings 10→0 (a falling edge), the capacitor holds the
  previous voltage. Standard result: a `0↔10 V` square becomes a
  `0↔10 V` square *inverted* by the capacitor? No inversion: output shifts up by
  charge built on the 0-level → becomes `+10 V` to `+20 V`... The reliable
  approach: run the steady-state loop.

### Master steady-state rule for clampers
In steady state:
1. No net DC current flows through `C` into the diode (node average is the same
  every cycle).
2. The diode conducts only when the instantaneous waveform drives its terminal
  to the reference; the held `V_C` equals `(peak of the waveform reaching the
  diode's anode side) − (reference level at the cathode side)`.

So for input `v_in` with min value `V_min`:
- Positive (shunt-to-ground) clamper ideal: `V_C = |V_min|` → output swing
  `0 to (V_max − V_min)`.
- Negative clamper: `V_C = V_max` → output swing `(V_min − V_max) to 0`.

**Check with a sine `±Vm`:** positive → `0…+2Vm` (V_min = −Vm, so output min 0,
max +2Vm). Matches 4.1. 

---

## Worked example — triangular wave

Input: symmetric triangle `−5 V ↔ +5 V`, positive clamper, ideal, `RC` large.
1. `V_min = −5`. Capacitor charges to `+5 V` during the negative-min interval.
2. Output = input + 5 → swings `0 ↔ +10 V`. Triangle shape unchanged.

Check: bottom touches ground, top at 10. ✓

## Worked example — biased negative clamper

Input `±10 V` sine, negative clamper with bias `V_B = 4 V` (negative reference
`−4 V`), ideal.
1. `V_max = 10`; charge capacitor to `10 + 4 = 14 V` (top must reach the
   `−4 V` reference during diode conduction).
2. Output top lands at `−4 V`, so output swings `−4 − 20 = −24 V` to `−4 V`.

Alternate equivalent statement: shifted down by `10 + 4 = 14 V`.

---

## GATE traps (clampers)

1. **Never confuse clipper and clamper.** Clipper cuts amplitude; clamper shifts
   DC level. "Capacitor + diode only" ⇒ clamp; "no capacitor" ⇒ clip.
2. A clamper's output **amplitude equals the input amplitude** (2Vm range for a
   sine) — students "clip" it by mistake.
3. Capacitor polarity / diode orientation determine up-vs-down shift. Flipping
   the diode flips the clamp direction.
4. Biased clamps: reference adds algebraically to the *charged* voltage, not to
   the output offset twice.
5. Don't forget the 0.7 V: silicon clamp ends at `0.7 V`, not 0 (top or bottom,
   whichever the diode clamps).
6. If `R_L` is small, output droops exponentially — treat as discharge; don't
   draw a perfect flat clamp.

---

## 5-question self-check

1. Positive clamper, ideal, sine `±5 V`. Output range? → *0 to +10 V.*
2. Negative clamper, ideal, sine `±5 V`. Output range? → *−10 to 0 V.*
3. Silicon (0.7) positive clamper, sine `±5 V`. Bottom value? → *+0.7 V.*
4. Positive biased clamper `V_B = 2 V`, sine `±5 V`. Output range? → *+2 to +12 V.*
5. `R_L C ≪ T` in a clamper. Between diode pulses the cap? → *discharges → droop.*

Next chapter: **`05-Rectifiers.md`**