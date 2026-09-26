# Rectifiers — Practice (Learn by Solving)

> **The idea in one line:** this file teaches the whole of Chapter 05 through 36
> questions — every rectifier number (`V_dc`, `V_rms`, ripple factor, efficiency,
> PIV) is *derived once* and then reused, so the table stops being something to
> memorise and becomes something you can rebuild under pressure.
>
> **How to use:** solve each question fully before reading the answer. Cover the
> **Answer**/**Method** with paper, do it, then reveal. If you miss one, solve
> the next 3 in the file to lock the pattern. No need to read the chapter notes
> first — every concept is taught through the drill itself. Open
> `05-Rectifiers.md` or `32-Single-File-Cheatsheet.md` only when you want the
> underlying theory.

## Concept box (what you must internalise)

- `V_dc = (1/T)∫v dt`; `V_rms = sqrt((1/T)∫v² dt)`. **These are different things**
  and swapping them is the most common rectifier error.
- Half-wave: `V_dc = Vm/π = 0.318 Vm`, `V_rms = Vm/2 = 0.5 Vm`.
  Full-wave: `V_dc = 2Vm/π = 0.637 Vm`, `V_rms = Vm/√2 = 0.707 Vm`.
- Ripple factor `γ = V_r/V_dc = sqrt((V_rms/V_dc)² − 1)` ⇒
  **1.21 (half) vs 0.48 (full)**.
- Efficiency `η = P_dc/P_ac = (V_dc/V_rms)²` ⇒ `4/π² = 40.5 %` (half),
  `8/π² = 81.1 %` (full). Quote **40.6 % / 81.2 %** in the exam.
- Ripple frequency `f_r = f` (half-wave) or **`2f` (full-wave)**.
- **PIV: HWR = `Vm`; bridge = `Vm`; centre-tap = `2Vm`.**
- With silicon drops: HWR `(Vm−0.7)/π`; CT-FWR `(Vm−0.7)·2/π`; **bridge
  `(Vm−1.4)·2/π`** — two drops in a bridge path.
- Capacitor filter: `V_r ≈ I_dc/(f_r·C)`, `V_dc ≈ Vm − V_r/2`,
  `γ ≈ 1/(f_r R_L C)`. Ripple `∝ 1/C`, `∝ 1/f_r`, `∝ I_dc`.

---

## Questions

### Q1. (Easy) Half-wave rectifier, ideal, `Vm = 100 V`, `R_L = 1 kΩ`. Find
`V_dc`, `V_rms`, `I_dc`.
**Answer:** `V_dc = 100/π =` **31.8 V**; `V_rms = 100/2 = ` **50.0 V**;
`I_dc = 31.8/1000 = ` **31.8 mA**.
**Method:** The half-wave pair is `Vm/π` (average) and `Vm/2` (rms). Memorise the
factors, not the derivation: `1/π = 0.318`, `1/2 = 0.5`. Then one Ohm's law.
Note the sanity check that catches the classic swap: `V_dc < V_rms` always, and
the ratio is `π/2 = 1.57`. If your `V_dc` came out larger than your `V_rms`, you
have interchanged them.

---

### Q2. (Easy) Full-wave rectifier (bridge), ideal, `Vm = 100 V`. Find `V_dc` and
`V_rms`.
**Answer:** `V_dc = 200/π = ` **63.7 V**; `V_rms = 100/√2 = ` **70.7 V**.
**Method:** Full-wave pair is `2Vm/π = 0.637 Vm` and `Vm/√2 = 0.707 Vm`. The
**full-wave RMS equals the RMS of the original sine** — rectification does not
change the average of `v²` at all, it only repeats the half-sine. That one fact
is the cleanest way to remember `Vm/√2` for full-wave and `Vm/2` for half-wave.

---

### Q3. (Easy) Which rectifier has a ripple frequency equal to the input frequency,
and which has double it?
**Answer:** **Half-wave: `f_r = f`** (one hump per input cycle). **Full-wave:
`f_r = 2f`** (two humps).
**Method:** Count the humps. A half-wave rectifier passes only the positive half,
so exactly one output pulse per input period. Full-wave uses *both* halves, so two
pulses. This single fact drives the capacitor-filter ripple frequency, so getting
it right here pays twice.

---

### Q4. (Easy) Centre-tapped full-wave rectifier: each half-secondary has a peak of
40 V. Find the PIV of each diode.
**Answer:** **80 V = 2·Vm.**
**Method:** On the positive half, one diode conducts and the other is reverse
biased. The blocking diode sees the voltage across the *whole* secondary (both
halves), which is `2·Vm`. Trace the off-state loop: the reverse voltage is the sum
of the two half-secondary voltages, because the centre tap sits between them.

---

### Q5. (Easy) Bridge rectifier with `Vm = 20 V`. Find the PIV of each diode and the
number of diodes.
**Answer:** PIV = **20 V = Vm**; **4 diodes**.
**Method:** In a bridge, when one pair conducts the other pair is reverse biased
across **one half-cycle of the secondary only**, so each diode blocks just `Vm`.
That is the bridge's headline advantage over the centre-tap: **half the PIV** for
the same output. The price is 4 diodes and *two* forward drops per half-cycle.

---

### Q6. (Easy) How many diodes does each configuration use, and how many forward
drops does the output lose per half-cycle?
**Answer:** HWR: **1** diode, **1** drop (0.7 V). CT-FWR: **2** diodes, **1** drop
per half-cycle (only one diode conducts). Bridge: **4** diodes, **2** drops
(1.4 V) per half-cycle.
**Method:** Draw the conduction path, not the schematic. In a centre-tap both
diodes exist but **only one** conducts at a time. In a bridge **two** conduct in
series. This is why the bridge needs a higher `Vm` for the same `V_dc`:
`V_dc = (Vm − 1.4)·2/π` vs `(Vm − 0.7)·2/π`.

---

### Q7. (Easy) State the ripple factors of the ideal half-wave and full-wave
rectifiers, and say which is better and by roughly how much.
**Answer:** Half-wave **γ = 1.21**; full-wave **γ = 0.48**. Full-wave is better:
its DC is twice as large while its ripple (RMS of the AC component) is *lower*, so
`γ` falls by a factor of ≈ **2.5**.
**Method:** `γ = sqrt((V_rms/V_dc)² − 1)`. Half-wave: `(Vm/2)/(Vm/π) = π/2 = 1.5708`;
`γ = sqrt(1.5708² − 1) = sqrt(1.4674) = 1.211`. Full-wave:
`(Vm/√2)/(2Vm/π) = π/(2√2) = 1.1107`; `γ = sqrt(1.2337 − 1) = 0.483`.
Note `γ = 1.21` means the ripple RMS is *larger* than the DC itself.

---

### Q8. (Easy) State the ideal rectification efficiency of the half-wave and
full-wave rectifiers, and explain why full-wave is nearly double.
**Answer:** Half-wave **40.6 %** (exactly `4/π² = 40.5 %`); full-wave **81.2 %**
(exactly `8/π² = 81.1 %`).
**Method:** `η = P_dc/P_ac = V_dc²/V_rms²` (the same `R` cancels). Half-wave:
`(1/π)²/(1/2)² = 4/π²`. Full-wave: `(2/π)²/(1/√2)² = 8/π²`. The ratio is exactly
**2** because `V_dc` doubles and `V_rms` barely changes. The remaining ~19 % is the
power the rectifier throws away in the "missing" half-cycle and in diode drops.

---

### Q9. (Easy) 230 V (rms) mains feeds an **ideal half-wave** rectifier with a
1 kΩ load. Find `Vm`, `V_dc`, `V_rms`, `I_dc`, `P_dc`, `P_ac` and PIV.
**Answer:** `Vm = 230·√2 =` **325.3 V**; `V_dc = 325.3/π = ` **103.5 V**;
`V_rms = 325.3/2 = ` **162.6 V**; `I_dc = ` **103.5 mA**;
`P_dc = 103.5²/1000 = ` **10.72 W**; `P_ac = 162.6²/1000 = ` **26.45 W**;
**PIV = 325.3 V**.
**Method:** Mains is specified in **rms**, everything else wants the **peak**, so
the very first line is `Vm = V_rms·√2 = 230 × 1.4142 = 325.27 V`. Then the standard
half-wave factors. Powers from `P = V²/R` (note `P_ac` uses the *output* rms, which
is the power actually dissipated). Check: `10.72/26.45 = 40.5 %` ✔.

---

### Q10. (Easy) Same 230 V mains, but a **bridge with silicon diodes**, 1 kΩ load.
Find `V_dc`, `V_rms`, `P_dc`, `P_ac`, η and PIV.
**Answer:** `V_dc = (325.3 − 1.4)·2/π = 323.87 × 0.63662 = ` **206.2 V**;
`V_rms = 323.87/√2 = ` **229.0 V**; `P_dc = 206.2²/1000 = ` **42.51 W**;
`P_ac = 229.0²/1000 = ` **52.45 W**; η = ` **81.1 %**; **PIV = 325.3 V**.
**Method:** The bridge loses **two** drops, so first reduce the peak:
`Vm' = 325.3 − 1.4 = 323.87 V`, then `V_dc = Vm'·2/π`. Arithmetic:
`323.87 × 0.63662 = 194.32 + 11.86 = 206.18 V`. η comes out at 81.1 % — the same as
the ideal case — because **the diode drop scales `V_dc` and `V_rms` together, so it
reduces the output level without reducing efficiency.**

---

### Q11. (Easy) Bridge rectifier, `Vm = 20 V`, silicon diodes, `R_L = 1 kΩ`. Find
`V_dc`, `I_dc`, `V_rms`, `I_rms`, `P_dc`, `P_ac`, η and PIV.
**Answer:** `V_dc = 18.6 × 0.63662 = ` **11.84 V**; `I_dc = ` **11.84 mA**;
`V_rms = 18.6/1.4142 = ` **13.15 V**; `I_rms = ` **13.15 mA**;
`P_dc = 11.84²/1000 = ` **140.2 mW**; `P_ac = 13.15²/1000 = ` **173.0 mW**;
η = ` **81.1 %**; **PIV = 20 V**.
**Method:** One combined step: compute everything on the *reduced* peak
`Vm' = Vm − 1.4 = 18.6 V`, then apply the ideal bridge factors. Powers:
`11.84² = 140.2`; `13.15² = 172.9`; ratio `140.2/172.9 = 0.811`. This
"reduce the peak first, then apply the table" shortcut removes most of the
arithmetic-error risk.

---

### Q12. (Moderate) Full-wave rectifier with a capacitor filter: load draws 10 mA,
`C = 100 µF`, mains 50 Hz. Find the ripple voltage.
**Answer:** `f_r = 2 × 50 = 100 Hz`;
`V_r = I_dc/(f_r·C) = 10 mA/(100 × 100 µF) = 0.010/0.01 = ` **1.0 V**.
**Method:** Three lines, always in this order: (1) `f_r = 2f` for full-wave;
(2) `V_r = I_dc/(f_r·C)`; (3) if asked, `γ ≈ V_r/V_dc`. Do the units check once:
`f_r·C` has units of `1/s`, so `I/(f_r·C)` is volts — after that the factor of 1000
stops biting you.

---

### Q13. (Moderate) The same load and capacitor on a **half-wave** rectifier at
50 Hz. Ripple? How does it compare with Q12?
**Answer:** `f_r = 50 Hz`; `V_r = 10 mA/(50 × 100 µF) = 0.010/0.005 = ` **2.0 V** —
exactly **twice** Q12.
**Method:** The capacitor discharges for a full input period in a half-wave
rectifier but only half a period in a full-wave one, so half-wave ripple is 2×
worse for identical `C` and load. This is the quantitative reason full-wave
rectifiers dominate in power supplies, and it is Q3 seen from the filter's side.

---

### Q14. (Moderate) To halve the ripple of a full-wave C-filtered rectifier by
changing **only** `C`, what is the new value? Name two other ways.
**Answer:** **Double `C`** (since `V_r ∝ 1/C`). Equally valid: halve the load
current (i.e. double `R_L`), or double the input frequency, or add a second
rectifier section (voltage doubler / two bridges in a push-pull arrangement).
**Method:** From `V_r = I_dc/(f_r·C)`, three of the four variables sit in the
denominator, so raising `f_r`, raising `C` or lowering `I_dc` all reduce ripple.
Only `C` and `f_r` are cheap to control; the price of a very large `C` is a large
inrush/peak diode current at every peak.

---

### Q15. (Moderate) Bridge (silicon, `Vm = 20 V`, `R_L = 1 kΩ`) with `C = 1000 µF`
on 60 Hz mains. Find the ripple voltage and the ripple factor.
**Answer:** `I_dc = ` **11.84 mA**; `f_r = ` **120 Hz**;
`V_r = 11.84 mA/(120 × 1000 µF) = 0.01184/0.12 = ` **98.7 mV ≈ 0.099 V**;
γ = `0.0987/11.84 = ` **0.0083 = 0.83 %**.
**Method:** `I_dc` comes from Q11, then the Q12 template. The ripple factor is just
`V_r/V_dc`, and a well-designed filtered supply reaches well under 1 %. Note the
improvement: γ went from 0.483 (unfiltered, Q7) to 0.0083 — the filter is worth
about **58×** in ripple factor for 20× more capacitance.

---

### Q16. (Moderate) Which configuration gives the **lower PIV per diode** for the same
`Vm`, and which gives the larger `V_dc`?
**Answer:** **Bridge and half-wave tie at PIV = `Vm`; the centre-tap needs `2Vm`.**
For `V_dc`: bridge and centre-tap are identical (`2Vm/π`, ideal) and both beat the
half-wave (`Vm/π`) by 2×.
**Method:** The PIV and the `V_dc` orderings are *different* questions — the
centre-tap is worst on PIV but equal-best on `V_dc`, while the half-wave is worst
on `V_dc` but tied-best on PIV. The bridge is the only configuration that is never
worst at anything, which is why it is the default. This is the "pros/cons table"
logic GATE tests: never pick on a single criterion.

---

### Q17. (Moderate) Centre-tap full-wave, each half-secondary peak 40 V. Find
`V_dc` (ideal and silicon), `I_dc` for 1 kΩ, and the PIV.
**Answer:** Ideal: `V_dc = 2 × 40/π = 80/π = ` **25.46 V**.
Silicon: `V_dc = (40 − 0.7)·2/π = 39.3 × 0.63662 = ` **25.02 V**;
`I_dc = ` **25.02 mA**; **PIV = 80 V**.
**Method:** "Each half" means `Vm = 40 V` is the peak of *one* half-winding, so the
full-wave factors apply directly: `V_dc = 2Vm/π`. Only **one** diode conducts per
half-cycle, so only **one** 0.7 V drop: `(Vm − 0.7)·2/π` — the same form as the
half-wave's `(Vm − 0.7)/π` but with `2/π` instead of `1/π`.

---

### Q18. (Moderate) In a bridge, on the positive half-cycle name the conducting pair
and give the PIV of the blocking pair.
**Answer:** Two diagonally opposite diodes conduct (call them D1 and D3); the other
two (D2, D4) are reverse biased, each across the full secondary ⇒ **PIV = Vm** for
each blocking diode.
**Method:** The bridge is two series paths across the same AC source. The forward
path carries current; in the blocking path the *whole* secondary voltage appears
across one of its diodes, which is `Vm` — **not** `2Vm`, because there is no centre
tap adding a second half-winding. This is precisely why the bridge beats the
centre-tap on PIV.

---

### Q19. (Moderate) State the **form factor** (peak/average) of the half-wave and
full-wave outputs, and the transformer utilisation factor (TUF) of the three
circuits.
**Answer:** Form factor: half-wave **π = 3.14**, full-wave **π/2 = 1.57**
(lower is better — it measures how peaky the output is).
TUF: half-wave **0.287**, centre-tap full-wave **0.693**, bridge **0.81**
(higher is better). The bridge is exactly `8/π² = 0.8106`; many tables round it to
**0.812**, so either is accepted — but write `0.81` if you derive it yourself.
**Method:** Form factor `= V_peak/V_dc`, so `Vm/(Vm/π) = π` and `Vm/(2Vm/π) = π/2`.
TUF `= P_dc / VA_rating(secondary)`. The bridge value follows directly:
`VA = V_rms(sec)·I_rms(sec) = (Vm/√2)(Vm/(√2R)) = Vm²/2R` while
`P_dc = 4Vm²/(π²R)`, so `TUF = 8/π² = 0.8106` (≈ 0.81). The half-wave is bad because its
secondary current is a half-wave (high rms) while its DC power is low:
`(Vm²/π²R)/(Vm²/2√2·R) = 0.287`. The centre-tap's 0.693 is a *tabulated* figure
(its VA-rating convention differs); quote it, do not re-derive it.

---

### Q20. (Moderate) A half-wave rectifier has a filter capacitor. Sketch the diode
current waveform and compare its *average* with the load current.
**Answer:** The diode current is a **narrow spike** at each peak: it rises to a large
value, dumps the charge into `C`, and falls to ≈ 0 for the rest of the cycle. Its
**average equals the load current** (charge balance), but its **peak is many times
larger**: the charge per cycle is `ΔQ = I_load/f_r = 10/50 = 0.2 C`, delivered in a
conduction window of only a few ms out of 20 ms, so `I_peak = ΔQ/t_c` is easily
5–10× the 10 A load current.
**Method:** Charge in = charge out, so `⟨i_diode⟩ = I_load`. But that current has a
terrible form factor (a few percent duty), so the **peak/surge** rating, the
transformer's current rating and the diode's `I_FSM` are all set by the spike, not
the average. This is the standard answer to "why is rectifier diode current
pulsating / why is the diode's current rating so much higher than the load
current?"

---

### Q21. (Moderate) A half-wave rectifier with a filter capacitor has **no load**
(`R_L → ∞`). What is the output voltage?
**Answer:** **`V_out = Vm`** (minus the diode drop). The capacitor charges to the
peak on the first cycle and never discharges, so the output is a constant `Vm`.
**Method:** "No load ⇒ no discharge ⇒ the cap holds the peak." The moment you
connect a load, the output drops by roughly `V_r/2` (Q23). This is also why a
"12 V" unregulated supply reads ≈ 17 V at no load and ≈ 12 V at full load — a
classic practical surprise.

---

### Q22. (Moderate) A C-filtered bridge has `V_dc` fixed at 15 V. What happens to
the ripple when the load resistance is (a) halved, (b) doubled?
**Answer:** `I_dc = V_dc/R_L`, so halving `R_L` **doubles** `I_dc` and therefore
**doubles** the ripple; doubling `R_L` **halves** it. Ripple `∝ 1/R_L`.
**Method:** Chain the two dependencies: `V_r = I_dc/(f_r C)` and `I_dc = V_dc/R_L`,
so `V_r = V_dc/(f_r R_L C)`. **Inverses everywhere:** bigger `C`, bigger `R_L`,
higher `f_r` ⇒ smaller ripple. A "stiffer" supply is obtained with all three at
once. The flip side is that regulation gets *worse* as `R_L` rises (Q28).

---

### Q23. (Moderate) Bridge, `Vm = 20 V`, `C`-filtered, ripple `V_r = 1 V`. What is
`V_dc`, and how much better is it than the unfiltered value?
**Answer:** `V_dc ≈ Vm − V_r/2 = 20 − 0.5 = ` **19.5 V** ideal; with silicon
`V_dc = (20 − 1.4) − 0.5 = ` **18.1 V**. Unfiltered (silicon) it was
`18.6 × 0.637 = 11.84 V`, so the filter improves `V_dc` by `18.1/11.84 = ` **1.53×**
(the ideal ceiling is `1/0.637 = 1.571×`).
**Method:** Two facts: (1) the capacitor charges to the peak, so the *mean* of the
ripple triangle is half its height — hence `−V_r/2`; (2) unfiltered,
`V_dc = 0.637 Vm`, so a filter buys at most `1/0.637 = 1.571×`. **A filter cannot
beat the peak: `V_dc` can never exceed `Vm`** (or `Vm − 1.4` with silicon).

---

### Q24. (Moderate) A bridge with silicon diodes must deliver `V_dc = 12 V`. What
`Vm` is required, and what transformer secondary rms rating?
**Answer:** `Vm − 1.4 = 12/(2/π) = 12 × π/2 = 18.85 V` ⇒ **`Vm = 20.25 V`**.
Secondary rms `= 20.25/√2 = ` **14.32 V**.
**Method:** Invert the drop-corrected formula: `Vm = V_dc·π/2 + 1.4`.
`12 × 1.5708 = 18.85 V`; `+1.4 = 20.25 V`; `/1.4142 = 14.32 V`. Practical answer:
specify a **15 V** secondary so that regulation and mains tolerance are covered.

---

### Q25. (Moderate) A **10 V rms** sine is rectified. Find `Vm`, `V_dc` and `V_rms`
for a half-wave and for a full-wave rectifier.
**Answer:** `Vm = 10 × √2 = ` **14.14 V**.
Half-wave: `V_dc = 14.14/π = ` **4.50 V**; `V_rms = 14.14/2 = ` **7.07 V**.
Full-wave: `V_dc = 28.28/π = ` **9.00 V**; `V_rms = 14.14/√2 = ` **10.0 V**.
**Method:** `Vm = 10√2 = 14.142` once, then the two factor pairs. Note two useful
anchors: **full-wave `V_dc ≈ 0.9 × V_in,rms`** (9.00/10) and **half-wave
`V_dc ≈ 0.45 × V_in,rms`** (4.50/10). If a problem gives rms, these ratios often
let you skip the `√2` step entirely.

---

### Q26. (Gate) Bridge (silicon, `Vm = 20 V`, 50 Hz) with a **470 µF** filter and
a **470 Ω** load. Find `I_dc`, `V_r` and γ.
**Answer:** `Vm' = 18.6 V`; `I_dc = 18.6 × 0.63662/470 = 11.842/470 = ` **25.2 mA**;
`f_r = ` **100 Hz**; `V_r = 0.0252/(100 × 470 µF) = 0.0252/0.047 = ` **0.536 V**;
γ = `0.536/11.84 = ` **4.53 %**.
**Method:** Order of operations matters — `I_dc` is an **unfiltered** result
(`2Vm'/πR`), because the filter barely changes the average. Then use
`V_r = I_dc/(f_r C)`. The single most common error here is dividing the *ripple* by
the *peak* (`0.536/18.6 = 2.9 %`) instead of by `V_dc` (`11.84 V`).

---

### Q27. (Gate) In Q26, find the `C` needed to bring the ripple to **≤ 0.25 V**.
**Answer:** `C ≥ I_dc/(f_r·V_r) = 0.0252/(100 × 0.25) = 0.0252/25 = ` **1.008 mF**.
So **1000 µF** (the nearest standard value); the resulting ripple is
`0.0252/(100 × 0.001) = ` **0.252 V** ✔.
**Method:** Rearrange `V_r = I_dc/(f_r C)` for `C` — *the one thing worth being able
to do in your sleep*, because design questions always give ripple and ask for `C`.
Every design question reduces to: halve the ripple, double `C`. With 1000 µF,
γ falls to `0.252/11.84 = 2.13 %`.

---

### Q28. (Gate) Bridge, silicon, `Vm = 20 V`, C-filtered. At no load the output is
18.6 V; under load the ripple is 1.2 V. Find the full-load `V_dc` and the
**percentage regulation**.
**Answer:** `V_FL = 18.6 − 1.2/2 = 18.6 − 0.6 = ` **18.0 V**;
`%reg = (V_NL − V_FL)/V_FL × 100 = (18.6 − 18.0)/18.0 = ` **3.33 %**.
**Method:** `V_dc(loaded) ≈ V_NL − V_r/2` (Q23) — the half-ripple offset, because the
mean of a triangle is half its height. Then the standard regulation definition,
which is **always** `ΔV/V_FL` (not `ΔV/V_NL`, not `ΔV/V_avg`) — 3 % is an excellent
raw supply, 10 % is acceptable, 20 % means you need a regulator.

---

### Q29. (Gate) Bridge, silicon, `Vm = 25 V`, `R_L = 1 kΩ`. Find `V_dc`, `V_rms`,
`P_dc`, `P_ac`, η, and the **power lost in the diodes**.
**Answer:** `Vm' = 23.6 V`; `V_dc = 23.6 × 0.63662 = ` **15.02 V**;
`V_rms = 23.6/1.4142 = ` **16.69 V**; `P_dc = 15.02²/1000 = ` **225.7 mW**;
`P_ac = 16.69²/1000 = ` **278.5 mW**; η = ` **81.1 %** (the drop does not change it).
Diode loss: each diode conducts **half** the time, so its average over conduction is
`2 × 15.02 = 30.04 mA`; per diode `0.7 × 30.04 mA = ` **21.0 mW**, and **two** diodes
carry current at once ⇒ `2 × 21.0 = ` **42.1 mW total**.
**Method:** η is unchanged from the ideal case because both `V_dc` and `V_rms` are
computed from the same `Vm'` — **drops cost voltage, not efficiency.** The diode-loss
trap is forgetting the *conduction duty*: a diode in a bridge carries the **full**
load current during its half-cycle, so its average over the whole cycle is `I_dc`,
but its average over the *conducting* half is `2 I_dc`, and that is what multiplies
the 0.7 V.

---

### Q30. (Gate) Give **three** independent reasons a C-filtered full-wave supply
beats a C-filtered half-wave one, and one reason the half-wave is still used.
**Answer:** Full-wave wins on three independent counts: (1) **ripple frequency `2f`
vs `f`** ⇒ half the ripple for the same `C`; (2) **γ = 0.48 vs 1.21** unfiltered
and `V_dc` is 2× for the same `Vm`, so the same ripple *ratio* is much easier to
filter; (3) **η = 81.2 % vs 40.6 %** ⇒ less than half the wasted AC power, so a
smaller transformer and a cooler one. The half-wave is still used when the **cost and
simplicity of a single diode plus a tapped winding beat the wasted power** — e.g.
low-current trickle supplies, battery chargers, and the inputs of small-signal
envelope detectors, where the absolute power thrown away is milliwatts and the extra
diode of a bridge is not worth it.
**Method:** Build the comparison on the three *quantities that actually differ* —
`f_r`, `γ` and `η` — and note that all three trace back to a single fact: **full-wave
uses both half-cycles.** `f_r` doubles, which halves `V_r` for a given `C`; the missing
half-cycle is no longer missing, which doubles `V_dc` and therefore halves the wasted
power. Then give the honest counter-case: whenever the wasted power is negligible
(mA-level loads), cost and part count decide instead, and the single diode wins.

---

### Q31. (Gate) Which is the better choice for a **5 V, 2 A** supply — bridge or
centre-tap? Justify with at least three criteria, and name one case where the
centre-tap wins.
**Answer:** **Bridge.** 2 A means the path carries two drops: the bridge wastes
`2 diodes × 0.7 V × 2 A = ` **2.8 W** against a useful output of
`5 V × 2 A = 10 W` — so the diodes burn **22 % of everything the transformer has
to deliver** (`2.8/12.8`), which at 2 A is several watts of hot silicon you must
heatsink. On top of that, PIV is only `Vm` so a smaller, cheaper transformer works,
and there is no centre-tap balancing constraint. The
**centre-tap wins** when PIV is the binding constraint — e.g. very high-voltage
secondaries where 2× the PIV would need an expensive, huge diode — and its
single-drop path (1.4 W instead of 2.8 W) is a real advantage at high current.
**Method:** Score candidates on a **criteria table**, never on one number:
`PIV`, `#diodes`, `drops in path`, `V_dc`, `TUF`, `cost`. The correct answer to any
such question is *"it depends on which criterion dominates"* — and stating that
explicitly, with the two regimes named, is what earns the mark.

---

### Q32. (Gate) Distinguish the **DC component**, the **AC (ripple) component** and
the **total (RMS) value** of a C-filtered output. Which one sets the heating of the
load, and which one sets the capacitor's voltage rating?
**Answer:** Output `= V_dc + v_r(t)`. `V_dc` is the DC component (the useful part,
~18 V); `v_r` is the AC/ripple component (a triangle of height `V_r`, RMS `V_r/√3`);
`V_rms = sqrt(V_dc² + V_r²/3) ≈ V_dc`. **Heating of the load** is set by
`V_rms` (≈ `V_dc`, since ripple is small). **The capacitor's voltage rating** must
exceed the **peak** `V_peak ≈ V_dc + V_r/2`, not `V_dc` — a 25 V cap is needed for an
18 V supply with 1 V ripple, not a 20 V one.
**Method:** Remember the three-number discipline: **DC (average), AC (RMS of the
ripple), total RMS**. `V_r,rms = V_r/√3` is the triangle-wave result. The rating
point is the practically important one: capacitor voltage ratings are *not*
generous, and `V_peak = V_dc + V_r/2` is the number to write on the BOM.

---

### Q33. (Gate) **Design:** bridge, silicon, 50 Hz, must deliver `V_dc = 5.0 V` at
100 mA with ripple ≤ 50 mV. Find the required `Vm`, the secondary rms voltage, and
`C`.
**Answer:** `V_r/2 = 0.025 V`; `Vm − 1.4 = V_dc + V_r/2 = 5.025 V` ⇒
**`Vm = 6.43 V`**; secondary rms `= 6.43/1.4142 = ` **4.54 V** (specify a 5 V
winding).
`C = I_dc/(f_r·V_r) = 0.1/(100 × 0.05) = 0.1/5 = ` **0.02 F = 20 000 µF**.
**Method:** Work backwards from the output. Invert the filter relation
`V_dc ≈ (Vm − V_d) − V_r/2` for `Vm`, add the bridge's 1.4 V drop, then
`Vm → V_rms` via `√2`. Then `C` from the ripple relation with `f_r = 100 Hz`. Every
design question is this same three-step inversion; write the three relations down
before substituting.

---

### Q34. (Gate) Q33 asks for **20 000 µF**. Why is that impractical, and what is
the standard fix?
**Answer:** 20 mF at 100 Hz has a reactance `1/(2π·100·0.02) = ` **80 mΩ** — small, so
it *works*, but at 25 V and 100 mA it is a physically enormous, expensive electrolytic
bank with high leakage, high ESR, and a large inrush/peak-diode-current surge
(`ΔQ = I_dc/f_r = 0.1/100 = 1 mC` dumped in a short window each cycle). The standard
fix is a **linear regulator** (a few µF of reservoir plus a 7805-style IC that
absorbs the ripple and the excess voltage as heat) or, properly, a **switching
(switch-mode) regulator**, which achieves the same 50 mV at 5 V/100 mA with ~100 µF.
**Method:** Whenever a design demands an absurd capacitor, the intended lesson is that
**linear regulation and switching regulation solve the same problem at very different
component costs.** Say the capacitor is impractical *and* name the fix — half the
mark.

---

### Q35. (Gate) For a required `V_dc`, the bridge needs a **higher** `Vm` than the
centre-tap, yet a **lower** PIV per diode. Explain both, and say which wins for a
50 V DC supply.
**Answer:** The **bridge** path has two drops: `(Vm − 1.4)·2/π = V_dc` ⇒
`Vm = V_dc·π/2 + 1.4`, so its peak must be **1.4 V higher** than the centre-tap's
`(Vm − 0.7)·2/π` ⇒ `Vm = V_dc·π/2 + 0.7`. Conversely the centre-tap's blocking diode
sees the **whole** secondary, `2Vm`, while a bridge diode sees only `Vm`. For a 50 V
supply the 1.4 V is negligible next to a 0.7 V/50 V = 1.4 % efficiency loss, whereas
PIV is a hard *device-selection* limit — so the **bridge wins**: higher PIV
capability outweighs 1.4 V of extra drop and a wasted diode.
**Method:** Separate **analogue/energy** costs (drops, efficiency) from **hard
limits** (PIV, current, voltage rating). A design is decided by whichever category is
*binding*. This "one circuit is better in one regime, worse in another" framing is
what the GATE pros/cons questions are testing.

---

### Q36. (Gate) **Consolidation.** Bridge, silicon, `Vm = 30 V`, 60 Hz, `C = 500 µF`,
`R_L = 500 Ω`. Find `V_dc`, ripple `V_r`, γ, PIV, efficiency, and the order of
magnitude of the **peak diode current**.
**Answer:**
`I_dc = (30 − 1.4) × 0.63662/500 = 18.207/500 = ` **36.4 mA**;
`f_r = ` **120 Hz**; `V_r = 0.0364/(120 × 500 µF) = 0.0364/0.06 = ` **0.607 V**;
`V_dc ≈ (30 − 1.4) − 0.607/2 = 28.6 − 0.30 = ` **28.30 V**;
γ = `0.607/28.30 = ` **2.14 %**; **PIV = 30 V**; η = ` **81.1 %**.
Peak diode current: the charge delivered per ripple period is
`ΔQ = I_dc/f_r = 0.0364/120 = 303 µC`. It goes in as a short spike, so
`I_peak = ΔQ/t_c`. The ripple period is `1/120 = 8.33 ms`; if conduction occupies ≈ ⅓ of
it (`t_c = 2.78 ms`) ⇒ `I_peak ≈ 0.303 mC/2.78 ms ≈ ` **0.11 A ≈ 3× the load
current**. Shorter `t_c` (stiffer source, smaller `C`) makes it larger still.
**Method:** This is the whole chapter in one problem, and it is always the same
five-step order: **(1)** `Vm' = Vm − drops`; **(2)** `I_dc = 2Vm'/πR`; **(3)**
`f_r = 2f`, then `V_r = I_dc/(f_r C)`; **(4)** `V_dc = Vm' − V_r/2`, `γ = V_r/V_dc`;
**(5)** PIV and efficiency from the tables. Do them in that order and each step is
one substitution with no algebra under pressure.

---

## Quick-reference comparison table (ideal, no drops)

| Quantity | Half-wave | Full-wave (centre-tap) | Full-wave (bridge) |
|---|---|---|---|
| Diodes | 1 | 2 | 4 |
| Drops in path | 1 (0.7 V) | 1 (0.7 V) | **2 (1.4 V)** |
| `V_dc` | `Vm/π = 0.318 Vm` | `2Vm/π = 0.637 Vm` | `2Vm/π = 0.637 Vm` |
| `V_rms` | `Vm/2 = 0.5 Vm` | `Vm/√2 = 0.707 Vm` | `Vm/√2 = 0.707 Vm` |
| Ripple factor γ | **1.21** | **0.48** | **0.48** |
| Efficiency η | **40.6 %** | **81.2 %** | **81.2 %** |
| Ripple freq `f_r` | `f` | `2f` | `2f` |
| PIV per diode | `Vm` | **`2Vm`** | `Vm` |
| TUF | 0.287 | 0.693 | 0.81 (`8/π²`) |
| Form factor | 3.14 | 1.57 | 1.57 |

**Silicon versions:** `V_dc(HWR) = (Vm − 0.7)/π`;
`V_dc(CT-FWR) = (Vm − 0.7)·2/π`; `V_dc(bridge) = (Vm − 1.4)·2/π`.
Efficiency, γ, form factor and `V_rms` factors are **unchanged** by the drop.

**C-filter versions:** `V_dc ≈ Vm' − V_r/2`;
`V_r = I_dc/(f_r C)`; γ = `V_r/V_dc`; `V_r,rms = V_r/√3`;
`I_peak ≈ ΔQ/t_c` with `ΔQ = I_dc/f_r`.

---

## Common traps & mistakes

1. **`V_dc` vs `V_rms` swapped.** `V_dc = 0.318/0.637 Vm` is an *average*;
   `V_rms = 0.5/0.707 Vm` is an RMS. **`V_dc < V_rms` always** — if your DC exceeds
   your RMS, stop and swap.
2. **Using `f` instead of `2f`** in the ripple formula. Full-wave ripple is at
   `2f`; getting this wrong doubles every capacitor you compute.
3. **`V_r/2` vs `V_r`.** The *mean* of the sawtooth ripple is half its height, so
   `V_dc ≈ Vm − V_r/2`, **not** `Vm − V_r`.
4. **PIV = 2Vm everywhere.** It is `2Vm` **only for a centre-tap**; HWR and bridge
   are `Vm`. Q4/Q5/Q18 exist to kill this.
5. **Forgetting the bridge's second drop.** `Vm − 1.4`, not `Vm − 0.7` (Q11, Q24).
6. **PIV of a clamper/clipper diode confused with a rectifier PIV.** A *shunt*
   clipper's off-state diode is the source voltage; a *series* clamp's is `V_C`.
7. **Assuming the filter improves efficiency.** It improves `V_dc` and γ, but η is
   unchanged by drops and the filter itself dissipates nothing ideal — the waste is
   in the *missing* half-cycles (Q8) and the diode drops.
8. **"More capacitance = more current, so worse."** `C` does not set the average
   diode current (charge balance fixes it at `I_load`); it sets the ripple and the
   peak. Bigger `C` ⇒ *lower* ripple, *higher* peak charging current.
9. **Ignoring that a C-filtered output is a *sawtooth*, not a flat line.** Use
   `Vm' − V_r/2` for `V_dc`, and `V_peak = Vm'` for capacitor and diode ratings.
10. **Adding drops to the PIV.** PIV is a property of the transformer and the
    topology; diode drops affect `V_dc` and efficiency, not the blocking voltage.

---

## Recall drill (close the file — answers below)

1. Ideal `V_dc` and `V_rms` for half-wave and full-wave?
2. Ripple factors? Which is better and by what factor?
3. Ideal efficiencies? Why is full-wave exactly double?
4. PIV of each of the three circuits?
5. Ripple frequency of each?
6. Silicon `V_dc` for each of the three circuits?
7. Form factors? TUF values?
8. With a C filter: `V_r` formula, `V_dc` correction, and the γ formula?
9. Charge delivered to the capacitor per cycle, and how it fixes the average
   diode current?
10. Which circuit is never worst, and on which criterion does the centre-tap beat it?
11. Bridge vs centre-tap: which has more drops, which has higher PIV, and which
    matters more for a 50 V supply?
12. What value of `C` halves the ripple? Doubles it?
13. Why is `V_dc` for a filtered rectifier always *less* than `Vm`?
14. What does a filter do to η, γ and PIV respectively?

### Answers

1. HWR: `Vm/π`, `Vm/2`. FWR: `2Vm/π`, `Vm/√2`.
2. 1.21 and 0.48; full-wave is ≈ 2.5× better.
3. 40.6 % (`4/π²`) and 81.2 % (`8/π²`); `V_dc` doubles while `V_rms` is unchanged.
4. HWR `Vm`; CT-FWR `2Vm`; bridge `Vm`.
5. `f` and `2f` respectively.
6. `(Vm−0.7)/π`; `(Vm−0.7)·2/π`; `(Vm−1.4)·2/π`.
7. 3.14 and 1.57; 0.287, 0.693, 0.81 (`8/π²`).
8. `V_r = I_dc/(f_r C)`; `V_dc ≈ Vm' − V_r/2`; `γ ≈ V_r/V_dc`.
9. `ΔQ = I_dc/f_r`; charge balance gives `⟨i_diode⟩ = I_load`.
10. The bridge; the centre-tap wins on PIV (half the bridge's, so usable where
    `2Vm` diodes would be prohibitive).
11. Bridge has 2 drops and lower PIV; for 50 V the PIV advantage dominates.
12. Halve ripple ⇒ double `C`; double ripple ⇒ halve `C`.
13. The mean of the ripple sits `V_r/2` below the peak, and the diode drop removes
    more still.
14. η unchanged; γ falls sharply; PIV unchanged.
