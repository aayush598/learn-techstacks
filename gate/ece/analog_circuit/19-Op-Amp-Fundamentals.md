# Chapter 19 — Operational Amplifier Fundamentals

> **The idea in one line:** an op-amp is a very high-gain DC amplifier with two
> inputs (+) and (−). Feedback forces the two input voltages to become equal
> ("virtual short"). That one rule + the ideal assumptions solves every op-amp
> circuit in the syllabus.

---

## 19.1 Op-amp symbol

```
      v+ ───┤+\
             │  \──► v_o
      v− ───┤−/
```
- `v+` = non-inverting input. `v−` = inverting input.
- Output `v_o = A·(v+ − v−)`, with `A` the open-loop gain (huge, 10⁵–10⁶).
- Blocks: input stage (differential pair), gain stage, output stage. Supplies
  ±V_CC / ±V_EE.

---

## 19.2 Ideal op-amp assumptions (memorize the list)

| Property | Ideal value | Consequence |
|----------|-------------|-------------|
| Open-loop gain A | ∞ | with feedback, `v+ = v−` (virtual short) |
| Input resistance | ∞ | input currents = 0 |
| Input offset current | 0 | both input currents equal & zero |
| Input offset voltage | 0 | zero output with both inputs equal |
| Output resistance | 0 | load doesn't affect output |
| CMRR | ∞ | common-mode totally rejected |
| Bandwidth | ∞ | gain flat to any frequency |
| Slew rate | ∞ | instant response |
| Output swing | reaches both rails | saturation at supply |

**The single rule that solves everything:** with **negative feedback**,
`v+ = v−` (the **virtual short**), and **no current flows into the inputs**.

### Virtual short vs virtual ground
- **Virtual short:** `v+ = v−` *because of feedback*, while node is not
  physically connected to the other input. Applies whenever negative feedback
  keeps the op-amp linear.
- **Virtual ground:** special case where one input sits at 0 V (inverting
  amplifier: `v−` = the virtual ground at 0 V even though there's no physical
  ground).
- Saturation (no feedback / huge input): virtual short fails; output slams to a
  rail.

---

## 19.3 Negative feedback (the enabling condition)

- A resistor from output back to the inverting input = negative feedback.
- Result: output moves to whatever voltage makes `v+ = v−`.
- **Open-loop** op-amp as comparator: no feedback → output is at a rail
  (Chapter 23).

---

## 19.4 Practical (real) op-amp specifications

- **Open-loop gain A:** finite (10⁵–10⁶, ~100 dB). With feedback:
  `V_o/V_in = −R2/R1` still accurate while `A·(feedback fraction) ≫ 1`.
- **Input offset voltage `V_os`:** a few mV; the input that appears at both
  terminals as if a tiny battery were inside. Output error `= V_os·(1+R2/R1)`.
- **Input bias current `I_B`:** small DC currents into each input (~µA–pA).
- **Input offset current `I_os = |I_B+ − I_B−|`:** the *difference*.
- **CMRR (finite):** couples common-mode input voltage error into output.
- **Finite bandwidth:** gain × f = GBW ≈ constant (1–10 MHz typical).
- **Slew rate (SR):** max `dv_o/dt` (V/µs). Square/triangle waveform limits.
  Largest amplitude distortion at highest frequency.
- **Output saturation:** output clamped to a rail, virtual short breaks.
- **Common-mode input range, supply limits** — practical rails.

### GATE facts worth one mark each
- Larger open-loop gain → more accurate closed-loop gain (`R2/R1` valid).
- Finite CMRR → common-mode signal leaks to output: `v_o ≈ A_d·v_id + A_cm·v_icm`.
- SR limits: `SR = 2π·f_max·V_pk` for a full-swing sine. If the required SR
  exceeds the part's, output distorts (slew limiting).

---

## 19.5 Fundamental circuit shapes (Chapter 20 will expand)

**Inverting:**
```
                 R2
        ┌──┤──────►────┐
  v_in ─┼─ R1 ─┼─  → − │  op-amp
               v−      + 
                 └──────┴──► v_o
```
- `v− = 0` (virtual ground), no input current:
  `i = v_in/R1`, `v_o = −i·R2` → **`A_v = −R2/R1`**.

**Non-inverting:**
```
  v_in ───────► +  op-amp ──► v_o
              v− ── R1 ─ GND
              └── R2 ────┘  (feedback from v_o to v−)
```
- `v+ = v− = v_in` (virtual short), divider:
  `v_o = v_in·(1 + R2/R1)` → **`A_v = 1 + R2/R1`**.

**Follower:**
- Direct output→inverting input: `v_o = v_in`, **`A_v = 1`**. Buffer.

---

## Worked example — virtual ground inverting amplifier

`R1 = 1 kΩ`, `R2 = 10 kΩ`, ideal op-amp, `v_in = 0.5 V`.
- `v− = 0`.
- `A_v = −R2/R1 = −10`. `v_o = −5 V`. Output swings within rails (say ±12 V) ✓.

Saturation check: if `v_o = −5 V` but rails are ±3 V → clamped at −3 V, virtual
short broken, all the above invalid → GATE loves this "saturate" trap.

---

## 19.6 GATE traps (op-amp fundamentals)

1. **Virtual short needs negative feedback + linear (unsaturated) mode.** The
   second op-amp is often deliberately run open-loop (comparator) → no virtual
   short.
2. Ideal input current = 0 — never set up a node-with-current equation at the
   input pin.
3. `A_v(inverting) = −R2/R1`, `A_v(noninverting) = 1 + R2/R1`. Adding the "1+"
   is the #1 dropped term.
4. Saturation kills everything. Always verify output is inside the rails.
5. In feedback, output is whatever circuit equations demand; the op-amp "does
   not know" the rail — it clips.

---

## 5-question self-check

1. Op-amp virtual short requires? → *negative feedback & linear mode.*
2. Ideal input resistance? → *∞.*
3. Inverting gain? → *−R2/R1.*
4. Non-inverting gain? → *1 + R2/R1.*
5. What breaks when output hits rail? → *virtual short.*

Next: **`20-Op-Amp-Amplifiers-Summers.md`**