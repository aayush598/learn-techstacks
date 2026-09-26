# Current Mirrors — Practice (Learn by Solving)

> **The idea in one line:** this file drills every current-mirror trick GATE can
> ask — the BJT `β/(β+2)` error, `W/L` scaling, `λ(V_DS)` tilt, compliance
> limits, and the three clever cousins (cascode, Wilson, Widlar).
>
> **How to use:** solve each question fully before reading the answer. Cover the
> **Answer**/**Method** with paper, do it, then reveal. If you miss one, solve
> the next 3 in the file to lock the pattern. No need to read the chapter notes
> first — every concept is taught through the drill itself. Open
> `17-Current-Mirrors.md` or `32-Single-File-Cheatsheet.md` only when you want
> the underlying theory.

## Concept box (what you must internalise)

- Ideal mirror: `I_out = I_ref`. BJT with finite β: `I_out = I_ref·β/(β+2)`
  (BJT only — a MOS gate draws no current, so its ratio is exact).
- MOS mirror ratio: `I_out/I_ref = (W2/L2)/(W1/L1)`; with channel-length
  modulation `I_out = I_ref·(1+λV_DS2)/(1+λV_DS1)`.
- `R_out` of a mirror is **not** ∞: BJT `ro = V_A/I_C`, MOS `1/(λ·I_D)`.
  Cascode/Wilson multiply it by roughly `gm·ro`.
- Widlar trades matching for a *small* current from a big one:
  `I_out = (V_T/R_E)·ln(I_ref/I_out)` — solve by iteration, never by a divider.
- Compliance: BJT keeps working down to `V_CE(sat) ≈ 0.2 V`; MOS needs
  `V_DS ≥ V_GS − V_th` — that is why BJT mirrors win in low-voltage design.
- Trap: the reference resistor supplies `I_C1` **plus both base currents**; it
  does **not** supply `I_C2`. A mirror with `I_ref = 1 mA` draws 1 mA from the
  supply, not 2 mA.

---

## Questions

### Q1. (Easy) An ideal BJT current mirror has a diode-connected reference
transistor and an identical output transistor. The reference current is
`I_ref = 1 mA`. What is `I_out`?
**Answer:** `I_out = 1 mA` exactly (ratio 1:1).
**Method:** Equal `V_BE` + matched devices ⇒ equal `I_S` ⇒ equal `I_C` from
`I_C = I_S·e^(V_BE/V_T)`. Never re-solve `V_BE` per transistor — the tied bases
*are* the statement that `V_BE` is equal. See `17-Current-Mirrors.md` §17.1.

### Q2. (Easy) A MOS mirror has `(W/L)1 = 5` for the reference device and
`(W/L)2 = 20` for the output device. `I_ref = 2 mA`, `λ = 0`, devices matched.
Find `I_out`.
**Answer:** `I_out = 2 mA × (20/5) = 8 mA`.
**Method:** `I_D = ½·k·(W/L)·V_ov²` at equal `V_ov`, so current is **proportional
to W/L**. Ratio = 4, multiply the reference. Widlar-style ratio setting is a
BJT trick; on MOS you just resize the transistor (`17-Current-Mirrors.md`
§17.2).

### Q3. (Easy) BJT mirror, `β = 100`, `I_ref = 1 mA`. What is the true `I_out`
and the percentage error?
**Answer:** `I_out = 1 mA × 100/102 = 0.980 mA`; error `≈ 2%` low.
**Method:** `I_ref = I_C1 + I_B1 + I_B2 = I_out(1 + 2/β)` (matched:
`I_C1 = I_C2 = I_out`, `I_B = I_out/β`). Solve: `I_out = I_ref·β/(β+2)`.
Recognise the shape: error `≈ 2/β` — β = 100 → 2%, β = 50 → 4%.

### Q4. (Easy) A NMOS current source carries `I_D = 1 mA` with
`λ = 0.02 V⁻¹`. What is its output resistance?
**Answer:** `ro = 1/(λ·I_D) = 1/(0.02 × 1 mA) = 50 kΩ`.
**Method:** `ro = 1/(λ·I_D)` = `V_A/I_D` in disguise. BJT style: same numbers
with `V_A = 100 V` give `100 V/1 mA = 100 kΩ`. Get in the habit of writing
`1/(λI_D)` first for MOS and `V_A/I_C` for BJT.

### Q5. (Moderate) A BJT mirror's output transistor carries `1 mA` with
Early voltage `V_A = 100 V`. What is the output resistance seen at the mirror
output, and what dominates it?
**Answer:** `R_out = ro = V_A/I_C = 100 V/1 mA = 100 kΩ`; dominated by the
output device's Early effect (`ro2`).
**Method:** The reference transistor sits at a *fixed* `V_DS = V_BE`, so it
cannot move — the only thing that can move is Q2's `V_CE`, which changes its
`I_C` through Early effect. GATE answer: `R_out of a current mirror = ro`.
(`17-Current-Mirrors.md` §17.1.)

### Q6. (Easy) A BJT mirror uses `V_CC = 10 V` and `R = 9.3 kΩ` with
silicon `V_BE = 0.7 V`. What current does the reference resistor set, and how
much supply current does the whole mirror draw?
**Answer:** `I_ref = (10 − 0.7)/9.3 kΩ = 1.00 mA`; total supply current = **1 mA**
(not 2 mA — Q2's collector is fed by the load, not by `R`).
**Method:** Two steps only: drop `V_BE`, then Ohm. The "how much from the
supply" question is the classic trap; write the KCL at the base node
`I_ref = I_C1 + I_B1 + I_B2` to prove it.

### Q7. (Moderate) In Q6 with `β = 100`, find the base current, the collector
current of each transistor, and verify the KCL.
**Answer:** `I_B = 1 mA/102 = 9.8 µA`; `I_C1 = I_C2 = 0.98 mA`; check
`0.98 + 0.0098 + 0.0098 = 0.9996 ≈ 1 mA` ✓.
**Method:** From `I_ref = I_out(1 + 2/β)`, `I_B = I_out/β = 0.98 m/100 =
9.8 µA`. Always finish a mirror problem with the KCL check — it catches
forgotten base currents in one line.

### Q8. (Easy) A MOS mirror must give `I_out = 3 mA` from `I_ref = 1 mA`.
Give the required `(W/L)` ratio, and the actual `(W/L)2` if `(W/L)1 = 4`.
**Answer:** ratio = 3:1; `(W/L)2 = 4 × 3 = 12`.
**Method:** `I_out/I_ref = (W2/L2)/(W1/L1)`. Note the design direction: current
ratio 3:1 means the **output** device is 3× wider. Getting this backwards is a
one-mark loss.

### Q9. (Moderate) Widlar mirror: `I_ref = 1 mA`, `V_T = 25 mV`,
`R_E = 11.5 kΩ`. Find `I_out`.
**Answer:** `I_out ≈ 10 µA` — exactly a 100:1 reduction.
**Method:** `I_out = (V_T/R_E)·ln(I_ref/I_out)`. Guess the ratio: if
`I_ref/I_out = 100`, `ln 100 = 4.605`; then `I_out` must equal
`(25 m/11.5 k) × 4.605 = 2.174 µA/V × 4.605 = 10.01 µA` — self-consistent.
Verify: `ln(1 mA/10.01 µA) = ln 99.9 = 4.60` → 10.0 µA. **This is the whole
method:** guess the log argument, then check `V_T·ln(ratio)/R_E` reproduces
your guess. (`17-Current-Mirrors.md` §17.4.)

### Q10. (Moderate) A MOS mirror has `I_ref = 1 mA`, `λ = 0.02 V⁻¹`, and the
reference device sits at `V_DS1 = 3 V` while the output sits at
`V_DS2 = 5 V`. Compute `I_out`.
**Answer:** `I_out = 1 mA × (1 + 0.02·5)/(1 + 0.02·3) = 1 mA × 1.10/1.06 =
1.038 mA` (≈ +3.8 % high).
**Method:** `I_D = I_ref(1 + λV_DS)`. Both currents carry the same
`(1 + λV_DS1)` factor through the tied gates, so the ratio is a *ratio of the
two* factors. Rule: **the branch with the larger `V_DS` sources more current.**
Sanity check: 1.10/1.06 ≈ 1.038, small because `λV_DS ≪ 1`.

### Q11. (Easy) A BJT mirror (`V_CE(sat) = 0.2 V`) and a NMOS mirror with
`V_GS = 1.2 V`, `V_th = 0.4 V` are both available. Which can be used with the
lower output voltage, and what is each minimum output voltage?
**Answer:** BJT: `≈ 0.2 V`. NMOS: `V_GS − V_th = 0.8 V`. **The BJT mirror wins**
(lower minimum output voltage).
**Method:** Compliance = the smallest `V_out` at which the device still sits in
its active region. BJT: `V_CE ≥ V_CE(sat)`. NMOS: `V_DS ≥ V_GS − V_th`
(saturation boundary). GATE asks this as "which current source suits a 1 V
supply?" — answer the BJT. (`17-Current-Mirrors.md` §17.2.)

### Q12. (Easy) Emitter-resistor (ratio) BJT mirror: `R_E1 = 4 kΩ` on the
reference device, `R_E2 = 8 kΩ` on the output device, `I_ref = 1 mA`. Find
`I_out`.
**Answer:** `I_out ≈ (R_E1/R_E2)·I_ref = 0.5 × 1 mA = 0.5 mA`.
**Method:** Bigger emitter resistor forces less current, so the ratio is
*inverse*: `I_out/I_ref = R_E1/R_E2`. Since `R_E2 > R_E1`, `I_out < I_ref` — a
free direction check. The BJT's `V_BE` variations now appear divided by `R_E`
(≈ 4 mV per mV at 4 kΩ), which is the point of these resistors.

### Q13. (Moderate) Design an NMOS mirror with `I_D = 1 mA` and
`R_out = 200 kΩ`. What λ (equivalently `V_A`) is needed?
**Answer:** `λ = 1/(I_D·R_out) = 1/(1 mA × 200 kΩ) = 0.005 V⁻¹`, i.e.
`V_A = I_D·R_out = 200 V`.
**Method:** Rearrange `ro = 1/(λI_D)`: `λ = 1/(I_D·R_out)`. Two equivalent
routes — short-channel MOS uses `λ`, BJT uses `V_A`. Useful GATE habit: convert
everything to `V_A` by multiplying `λI_D` by nothing — just remember
`V_A ≡ 1/λ`.

### Q14. (Moderate) A cascode/Wilson current source is built from a basic
mirror with `I = 1 mA`, `V_A = 100 V`, `V_T = 25 mV`. Compute `gm`, `ro`,
`gm·ro`, and the boosted output resistance.
**Answer:** `gm = 1 mA/25 mV = 40 mS`; `ro = 100 V/1 mA = 100 kΩ`;
`gm·ro = 4000`; `R_out(cascode) ≈ gm·ro² = 40 mS × (100 k)² = 400 MΩ`.
**Method:** `gm = I_C/V_T = 40·I_C[mA]`; `ro = V_A/I_C`; then the cascode
multiplies `ro` by `gm·ro`. A 4000× jump — that is the *entire reason*
cascodes and Wilson mirrors exist. (`17-Current-Mirrors.md` §17.4.)

### Q15. (Moderate) In a Widlar mirror, what happens to `I_out` if you remove
the emitter resistor `R_E`?
**Answer:** `R_E → 0` ⇒ the `ln` term no longer limits anything; you are left
with a plain BJT mirror, `I_out ≈ I_ref·β/(β+2) ≈ I_ref`.
**Method:** `I_out = (V_T/R_E)·ln(I_ref/I_out)`; as `R_E → 0` the required
`ln` term → 0 ⇒ `I_ref/I_out → 1`. So `R_E` is exactly the part that creates
the *small* output current; removing it deletes the Widlar's whole purpose.

### Q16. (Easy) BJT mirror with `β = 49`. What is `I_out/I_ref`?
**Answer:** `49/51 = 0.961` (error ≈ 4 % low).
**Method:** `I_out/I_ref = β/(β+2) = 1/(1 + 2/49) = 1/1.0408`. Rule of thumb:
error ≈ `2/β`, so β = 50 → 4 %, β = 100 → 2 %. Doubling β halves the error.

### Q17. (Moderate) `R_out` of a BJT mirror is 100 kΩ at `I_C = 1 mA`. The
output current is doubled to 2 mA. What is the new `R_out`, and why?
**Answer:** `50 kΩ`. Because `ro = V_A/I_C` — `V_A` is a material constant, so
`R_out ∝ 1/I_C`.
**Method:** Bigger current ⇒ stronger Early effect in voltage per volt ⇒
smaller incremental resistance. Same for MOS: `1/(λI_D)`. So **current sources
get *less* accurate as they get bigger** — worth remembering when a design
needs both 1 mA and 10 mA.

### Q18. (Easy) `λ = 0.02 V⁻¹`, `I_D = 0.5 mA`. Output resistance?
**Answer:** `1/(0.02 × 0.5 mA) = 100 kΩ`.
**Method:** `ro = 1/(λI_D)`. Double-check the mental model: 100× smaller current
than Q4 → 2× larger `ro`, not 100× — λ multiplication is what changed nothing;
it was the `I_D`.

### Q19. (Moderate) Design: `I_ref = 100 µA`, required `I_out = 1 mA`, and
`(W/L)1 = 4`. Size the output device. Then state the mirror's `R_out` if
`λ = 0.02`.
**Answer:** `(W/L)2/(W/L)1 = 1 mA/100 µA = 10` ⇒ `(W/L)2 = 40`.
`ro = 1/(0.02 × 1 mA) = 50 kΩ`.
**Method:** Current ratio first (10:1), then multiply the *reference* W/L by it.
Then `R_out` from the **output** current, not the reference current. Both halves
of a GATE mirror question in three lines.

### Q20. (Moderate) The mirror is built from PMOS devices on the high side and
must deliver 1 mA *into* a load. Which quantity changes and which does not?
**Answer:** Nothing in the ratio — it is still `I_out/I_ref = (W2/L2)/(W1/L1)`
= 1. The reference resistor now sits in the low-side path and the mirror
becomes a **current source** (pulling current *out* of the load) instead of a
sink.
**Method:** "Sink" = current into a node (NPN/NMOS on the low side); "source" =
current out of a node (PNP/PMOS high side). Differential-pair tails and op-amp
input stages use the low-side **sink**. Compliance rules are unchanged.

### Q21. (Moderate) A BJT mirror with `I_ref = 1 mA` feeds two 1 mA loads
(through two separate output transistors sharing the same reference node).
What current does the reference resistor now supply?
**Answer:** `≈ 1 mA` still — the reference node supplies one `I_C1` plus the
base currents; every extra output transistor adds only its own base current
(≈ 10 µA each at β = 100).
**Method:** KCL at the base node:
`I_ref = I_C1 + I_B1 + I_B2 + I_B3 = 1 mA·(1 + 3/β)` ≈ 1.03 mA for three
output devices. This is exactly why mirrors are used to **fan out** a bias
current to many stages without re-deriving it.

### Q22. (Moderate) BJT mirror with `β = 200` and `I_ref = 1 mA`. Find
`I_out`, the error, and the offset-current contribution of each base.
**Answer:** `I_out = 1 mA × 200/202 = 0.990 mA`; error 1 %; each base draws
`I_out/β = 4.95 µA`.
**Method:** `I_B = I_ref/(β + 2) = 1 m/202 = 4.95 µA`. Note the exact identity
`I_B = I_ref/(β+2)` — handy when a question asks for base current directly.

### Q23. (GATE-level) Mirror accuracy: a BJT mirror has `β = 100` and a MOS
mirror has identical geometry-ratio matching. Which one gives a truer 1:1 ratio
and why?
**Answer:** The **MOS** mirror. It has no base/gate current at all, so the
reference current divides into `I_D1` alone: `I_ref = I_D1` exactly. The BJT
loses `2/β = 2 %` to the two base currents.
**Method:** The base-current error is the *only* systematic ratio error in a
simple BJT mirror, and it vanishes as β → ∞. It does **not** vanish for MOS.
That single fact is the main reason CMOS analog ICs use MOS mirrors.

### Q24. (GATE-level) A BJT mirror is built from `V_CC = 15 V`, `R = 14.3 kΩ`,
`V_BE = 0.7 V`, `β = 100`. Find `I_ref`, `I_out`, the base-node voltage, the
minimum `V_out` for correct operation, and the base current.
**Answer:** `I_ref = (15 − 0.7)/14.3 k = 1.00 mA`; `I_out = 0.98 mA`;
`V_B = 0.7 V` (emitters at ground); `I_B = 9.8 µA`; minimum `V_out` for correct
mirror action `≈ V_CE(sat) = 0.2 V` (and it must certainly exceed
`V_C2 > V_B = 0.7 V` to stay in forward-active).
**Method:** Order of operations for any mirror: (1) `I_ref` from the resistor,
(2) `I_out` from the β-correction, (3) node voltages, (4) compliance check.
Stating *both* the saturation value (0.2 V) and the forward-active condition
(`V_C > V_B`) is the safest exam answer — GATE sometimes wants either.
(`17-Current-Mirrors.md` §17.1 and §17.2.)

### Q25. (GATE-level) A CE stage carries `I_C = 1 mA` with `V_A = 100 V`.
Compare the gain with (a) a 10 kΩ resistor load and (b) a current-mirror
(active) load. Give the ratio of gains.
**Answer:** (a) `|A_v| = gm·R_C = 40 mS × 10 kΩ = 400`. (b) `|A_v| = gm·ro =
40 mS × 100 kΩ = 4000`. Ratio = **10× more gain** with the mirror load.
**Method:** Resistor load: `A_v = −gm·R_C` (from `09-BJT-Amplifiers.md`).
Mirror load: the collector sees `ro` instead of `R_C`, so `A_v = −gm·ro`. Same
supply, same current — the load resistance is simply 100 kΩ instead of 10 kΩ.
This is the "active load" trick and the reason op-amp gain stages are enormous.
(`17-Current-Mirrors.md` §17.5.)

### Q26. (GATE-level) A BJT mirror with `I_ref = 1 mA` has `β = 50`. Find
`I_out`, the fractional error, and the total current drawn from the supply.
**Answer:** `I_out = 1 mA × 50/52 = 0.9615 mA`; error 3.85 %; supply current
= `I_ref` = 1 mA.
**Method:** `1/(1 + 2/50) = 1/1.04 = 0.9615`. Supply current is **always** `I_ref`
because the output collectors are fed externally. Then: the offset in the output
current is `0.0385 mA = 38.5 µA` — if that drives a 1 mA load through a mirror
ratio of 4, the load error is `4 × 38.5 = 154 µA`.

### Q27. (GATE-level) A MOS mirror has `I_ref = 1 mA`, `λ = 0.03 V⁻¹`,
`V_DS1 = 2.5 V`, `V_DS2 = 4.0 V`. Find `I_out` and the mismatch in per cent.
**Answer:** `I_out = 1 mA × (1 + 0.03·4.0)/(1 + 0.03·2.5) = 1 mA × 1.12/1.075 =
1.042 mA`; **+4.2 %** high.
**Method:** `1 + λV_DS1 = 1.075`, `1 + λV_DS2 = 1.12`. Divide: `1.12/1.075 =
1.0419`. Two habits here: (1) the branch with **higher** `V_DS` gives **more**
current; (2) mirror error grows with `λV_DS`, so long-channel (small λ) devices
give better matching — this is literally why analog input pairs are long-L.

### Q28. (GATE-level) Explain the two prices a cascode (or Wilson) current
source pays for its `gm·ro`-times higher `R_out`. For the numbers in Q14, what
are they?
**Answer:** Price 1 — **voltage headroom**: the output device stack needs an
extra `V_BE ≈ 0.7 V` (BJT) or `V_ov ≈ 0.2–0.4 V` (MOS) of compliance, so a
cascode mirror with a basic mirror needs ≈ 1.4 V of headroom instead of 0.2 V.
Price 2 — **complexity/poles**: two extra devices, more nodes, harder to bias.
Benefit: `R_out` 100 kΩ → 400 MΩ.
**Method:** Say it as: "higher `R_out`, but double the compliance voltage and
double the device count." Any GATE question asking the *drawback* of a cascode
mirror wants the headroom number. (`17-Current-Mirrors.md` §17.4.)

### Q29. (GATE-level) Widlar mirror with `I_ref = 1 mA`, `R_E = 5 kΩ`,
`V_T = 25 mV`. Solve `I_out = (V_T/R_E)·ln(I_ref/I_out)` and give the
reduction ratio.
**Answer:** `I_out ≈ 19.7 µA`, i.e. `I_ref/I_out ≈ 51`.
**Method:** Iterate. Start `x = 20 µA`: `ln(1000/20) = ln 50 = 3.912` ⇒
`(25 m/5 k) × 3.912 = 5 µA/V × 3.912 = 19.56 µA`. Next `x = 19.56`:
`ln 51.1 = 3.934` ⇒ 19.67 µA. Next `x = 19.67`: `ln 50.84 = 3.929` ⇒ 19.64 µA.
Converged: `I_out ≈ 19.65 µA`. **Method for Widlar in an exam:** iterate twice
and accept ~2 % accuracy, or guess the log argument. Ratio `1000/19.65 = 50.9`.

### Q30. (GATE-level) A BJT differential pair has `I_tail = 1 mA`, `R_C = 5 kΩ`
per side, `V_A = 200 V` (mirror tail ⇒ `R_tail = ro = 200 kΩ`), `V_T = 25 mV`.
Find `gm`, `R_out` of the tail, `Ad` (differential out), `Ac`, CMRR in dB, and
the quiescent collector voltage for `V_CC = 15 V`.
**Answer:** Each half `0.5 mA` ⇒ `gm = 0.5 mA/25 mV = 20 mS`;
tail device carries `I_tail = 1 mA` ⇒ `R_tail = ro = 200 V/1 mA = 200 kΩ`;
`Ad = −gm·R_C = −20 mS × 5 kΩ = −100`;
`Ac ≈ −R_C/(2R_tail) = −5 k/(2 × 200 k) = −0.0125`;
`CMRR = 100/0.0125 = 8000` ⇒ `20 log10 8000 = 78.1 dB`;
`V_C = 15 − (0.5 mA)(5 kΩ) = 15 − 2.5 = 12.5 V`.
**Method:** Order: half-current → `gm` → `ro` (tail, at `I_tail` **not**
`I_tail/2`) → `Ad` → `Ac` → CMRR → DC level. `log10(8000) = 3.903` ⇒ 78.06 dB.
(`18-Differential-Amplifiers.md`.)

### Q31. (GATE-level) An NMOS current source delivers `0.5 mA` but only has
`R_out = 2 MΩ`, and the design needs better than `20 MΩ`. Propose the fix and
compute the new `R_out` (take `λ = 0.02 V⁻¹` at `0.5 mA` ⇒ `ro = 100 kΩ`, and
`V_ov = 0.4 V`).
**Answer:** Use a **cascode** mirror. `gm = 2I_D/V_ov = 2(0.5 mA)/0.4 V =
2.5 mS`; improvement factor `gm·ro = 2.5 mS × 100 kΩ = 250`;
`R_out(cascode) ≈ gm·ro² = 250 × 100 kΩ = 25 MΩ`, which clears 20 MΩ.
**Method:** A cascode multiplies `ro` by `gm·ro`. The factor is **hundreds to
thousands**, not tens — so "make `R_out` 10× better" is one cascode device.
The price is headroom: the stack now needs `V_DS ≥ V_ov = 0.4 V` **below** the
output node, i.e. ≈ 0.8 V of compliance instead of 0.4 V. Quote the factor
`gm·ro`, not a remembered number.

### Q32. (GATE-level) An NMOS mirror has `V_GS = 1.2 V`, `V_th = 0.4 V`, and the
output node has only 0.6 V available. Does the mirror work? What happens to
`I_out`?
**Answer:** No. Saturation needs `V_DS ≥ V_GS − V_th = 0.8 V`; with 0.6 V the
output device is in the **triode** (linear) region, so `I_out` collapses below
its commanded value and depends strongly on `V_DS` — the mirror no longer
mirrors. The reference device (diode-connected) is fine, so `I_ref` stays 1:1
with `I_C1` while `I_out` droops.
**Method:** Always do the compliance check: find `V_DS,min` for each output
device, compare with the actual `V_DS`. For a BJT the same check is
`V_CE ≥ 0.2 V`; MOS is usually the binding constraint because
`V_GS − V_th ≥ 0.2 V` always. (`17-Current-Mirrors.md` §17.2 compliance.)

### Q33. (GATE-level) A BJT mirror and a MOS mirror both have `I_ref = 1 mA`.
Temperature rises from 300 K to 350 K. For each, state what happens to
(a) `I_ref`, (b) the ratio `I_out/I_ref`, (c) `V_BE`/`V_GS` required.
**Answer:** (a) `I_ref` **falls** (BJT: `V_BE` falls ≈ 2 mV/°C so
`I_ref = (V_CC − V_BE)/R` drops; MOS: `I_ref` is set by the reference
transistor's own `V_GS`, and `V_T` in `I_D = ½k(W/L)V_ov²` rises so
`I_D = (½k/V_ov²)V_T²`... in practice `I_ref` rises slowly with temperature
through `V_th` fall). (b) The **ratio stays 1** in both cases, because both
devices sit at the same temperature and track each other — that is the whole
point of a mirror. (c) `V_BE` and `V_GS` both fall.
**Method:** The exam-relevant sentence: **a mirror's ratio is
temperature-insensitive; an absolute current is not.** Mirrors are therefore
used to copy currents, while absolute current references (and the β/λ errors)
drift. Note the "mirror ratio error" list: β, `V_A` mismatch, `V_th` mismatch,
`W/L` mismatch — none of which is temperature.

### Q34. (GATE-level) An op-amp input stage needs a tail current source with
`R_out ≥ 100 MΩ` at `I_tail = 100 µA`. You may use a basic mirror, a cascode,
or a Wilson. For each, estimate `R_out` (assume `V_A = 100 V`, `V_T = 25 mV`)
and pick the one that qualifies, justifying with the CMRR consequence.
**Answer:** `gm = 100 µA/25 mV = 4 mS`; `ro = 100 V/100 µA = 1 MΩ`;
`gm·ro = 4000`. Basic mirror: `R_out = ro = 1 MΩ` (too low).
Cascode: `R_out ≈ gm·ro² = 4 mS × (1 MΩ)² = 4 GΩ` ✓.
Wilson: `R_out ≈ gm·ro²` order as well (4 GΩ) ✓ — Wilson reaches a similar
figure with **one** extra device and no extra headroom, so it is the usual
choice. CMRR scales with tail `R_out`: `CMRR ≈ gm·R_tail`, so 1 MΩ → ~4,000
(72 dB) while 4 GΩ → 1.6 × 10⁷ (144 dB, idealised).
**Method:** Steps: (1) `gm = I/V_T`, (2) `ro = V_A/I`, (3) multiply by `gm·ro`
for the improved mirrors, (4) convert to dB with `20 log10`. Remember the
chapter's short version: *Wilson → very high `R_out`; cascode → high `R_out` +
better matching; Widlar → small current from a large reference.*
(`17-Current-Mirrors.md` §17.4, and `18-Differential-Amplifiers.md` for the
CMRR link.)

---

## Trap box (exam-day killers)

- **Forgetting `β/(β+2)`.** A 1:1 BJT mirror with β = 100 outputs 0.98 mA, not
  1 mA. MOS has no such error — don't apply `β` to a MOS mirror.
- **Counting the reference current twice.** `I_supply = I_ref`, not
  `2·I_ref`. The reference node feeds `I_C1` + two base currents only.
- **`I_out = I_ref·R_E2/R_E1` backwards.** More emitter resistance ⇒ *less*
  current. Direction check before you compute.
- **Using `I_tail` instead of `I_tail/2` in `gm`** (see `Practice-18`).
- **Ignoring λ when `V_DS1 ≠ V_DS2`.** `I_out = I_ref(1+λV_DS2)/(1+λV_DS1)`;
  higher `V_DS` ⇒ higher current.
- **`R_out = ∞` for a current source.** It is `ro` (or `gm·ro²` with a cascode).
  "Ideal current source" questions that ask the *real* number want `ro`.
- **Skipping compliance.** Below `V_CE(sat) = 0.2 V` (BJT) or `V_GS − V_th`
  (MOS) the mirror stops mirroring and `I_out` droops.
- **Solving Widlar by divider.** It is `V_T·ln(ratio)/R_E` — always iterate.
- **Ratio error at high current.** `ro = V_A/I` shrinks as `I` grows, so a mirror
  is less accurate at 10 mA than at 1 mA.

## Final recall drill (do in 60 seconds)

1. BJT mirror, β = 100, `I_ref = 1 mA` → `I_out`? → *0.98 mA (2 % low).*
2. MOS mirror `λ = 0.02`, `I_D = 1 mA`: `R_out`? → *50 kΩ.*
3. `(W/L)1 = 5`, `(W/L)2 = 20`, `I_ref = 2 mA` → `I_out`? → *8 mA.*
4. Widlar purpose + formula? → *small current from a big one:
   `I_out = (V_T/R_E)·ln(I_ref/I_out)`.*
5. Which mirror has the *lowest* compliance voltage? → *BJT (≈ 0.2 V).*
6. `gm = 40 mS`, `ro = 100 kΩ` → cascode `R_out`? → *400 MΩ.*
7. Widlar: `I_ref = 1 mA`, `R_E = 5 kΩ` → `I_out`? → *≈ 19.7 µA.*
8. Total supply current of a mirror with `I_ref = 1 mA`? → *1 mA.*

---

