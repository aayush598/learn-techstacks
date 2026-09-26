# Chapter 18 — Differential Amplifiers

> **The idea in one line:** a differential amplifier amplifies the *difference*
> of its two inputs and rejects the *common* part. That rejection
> (CMRR) is what blocks power-supply hum and offset — the reason every op-amp
> input stage is a differential pair.

---

## 18.1 Signals: differential vs common mode

Two inputs `v1`, `v2`. Remix them:
```
v_id (differential) = v1 − v2
v_icm (common)      = (v1 + v2)/2
```
Or inversely: `v1 = v_icm + v_id/2`, `v2 = v_icm − v_id/2`.

- **Differential-mode signal** wants amplified.
- **Common-mode signal** wants killed.

---

## 18.2 The basic pair

```
        +V_CC
         │
   R_C1 ─┼────► v_o1      R_C2 ─┼────► v_o2
         │                      │
        C1                       C2
       (Q1)                     (Q2)
        E1──────────┬─────────E2
                    │
                I_tail (current source or R_E)
                    │
                  −V_EE / GND
```
- Q1, Q2 matched (identical β, V_BE).
- Emitters tied; common *tail* node feeds a **stiff current** `I_tail`.
- Inputs at the bases; outputs at the collectors; tail in place of a direct
  ground.

---

## 18.3 Differential-mode gain (`Ad`)

Short the two bases apart: signal +v_id/2 at Q1 base, −v_id/2 at Q2 base.

Symmetry trick: the midpoint of the tail is a **virtual ground** for
differential signals (each half "sees" half the tail current). Split the pair
into two halves, each `I_tail/2`:

**BJT:**
```
Ad = −gm·(R_C ∥ R_L)        (each half, differential output  v_o1 − v_o2 )
```
- Single-ended output: `Ad(se) = −gm·R_C/2`.
- Differential output: `Ad(diff) = −gm·R_C` (the two halves add).
- Where `gm` uses the *half* current: `gm = I_C(half)/V_T = (I_tail/2)/V_T`.

**MOS:**
```
Ad = −gm·(R_D ∥ ro)         with gm at I_D = I_tail/2 for each half.
```

### Intuition
In differential mode, each transistor sees one half of the input. Because the
tail node can't move (its voltage is symmetric), each half side behaves like a
standalone CE/CS stage with the tail acting as "AC ground." Gain halves
compared to a full-I current CE — the classic `Ad = gm·R_C` vs `gm·(R_C∥R_L)`
with half-current gm.

---

## 18.4 Common-mode gain (`Ac`)

Both bases swing **together**: v1 = v2 = v_icm. The tail **insists** the total
emitter current stays `I_tail`; so the two emitter currents can't both rise.
Net effect: output nearly doesn't move. If the tail is a perfect current source
(`R_tail → ∞`):

```
Ac → 0   (perfectly stiff tail)
```
With finite tail resistance `R_tail` (=`R_E` large or finite mirror `ro`):
- Both halves act in parallel: each collector sees half of `2·R_tail` doubled
  back... final:
```
Ac(se) ≈ −R_C/(2·R_tail)          [BJT, or −R_D/(2·R_tail)]
```
So a **large tail resistance** gives tiny Ac. That's why the tail is a
current *source* (ro, huge), not a plain resistor.

Derivation one-liner: common-mode turns the pair into a common-mode
*degenerated* stage where the twice-stiff tail (2·R_tail effective per side)
suppresses gain.

---

## 18.5 CMRR — the headline figure

```
CMRR = Ad / Ac        (linear)
CMRR_dB = 20·log10(Ad/Ac)
```
- Ideal: ∞ (Ac = 0).
- Finite-R_tail: `CMRR ≈ gm·R_tail` (roughly — high!). With tail mirror
  `R_tail = ro`, CMRR ≈ `gm·ro` — tens of thousands (80–100 dB).
- GATE favourite: “higher tail current-source resistance → CMRR increases.”

---

## 18.6 BJT vs MOS pair

| | BJT diff pair | MOS diff pair |
|---|---|---|
| Gain (diff-out) | −gm·R_C | −gm·(R_D∥ro) |
| gm | (I_tail/2)/V_T | √(2k·(I_tail/2)) |
| Input R | 2·rπ ≈ high | ∞ |
| CMRR (mirror tail) | gm·ro (BJT has high gm) | gm·ro |
| Input bias current | I_B ≠ 0 | ~zero → better for high-R sensors |

- MOS input stage → **no input bias current**, huge R_in.
- BJT input stage → higher gm → higher gain per µA.

---

## 18.7 Operating point detail (the Q of each half)

- DC: each transistor carries `I_tail/2` (half the tail split).
- Base voltages ≈ 0 (input common-mode = 0); emitter sits at
  `V_E ≈ −V_BE` for BJT (or at the common source).
- Collector voltages `V_C = V_CC − (I_tail/2)·R_C`.
- The active region demands `V_C > V_B`, so `R_C` can't be too large.

---

## 18.8 Large-signal / level-shift (bonus facts)

- Beyond small-signal, the pair differential *swings* the tail current between
  branches — beyond ±√2·V_GS·V_ov the pair "steers" (one transistor takes all).
- GATE may ask the max differential input before one branch cuts off:
  `V_id,max ≈ ... for BJT ≈ V_T·ln(...)` / for MOS ≈ `√2·V_ov`.
- Common-mode input range limited by keeping both branches active.

---

## Worked example

BJT pair: `V_CC = 12 V`, `R_C = 10 kΩ`, `I_tail = 2 mA`, β = 100,
`R_tail = 500 kΩ` (mirror), `V_T = 25 mV`. Find Ad, Ac, CMRR.

- Each half: `I_C = 1 mA`.
- `gm = 1m/25m = 40 mA/V`.
- `rπ = β/gm = 100/40m = 2.5 kΩ`. R_in(diff) = 2·rπ = 5 kΩ.
- `Ad (diff-out) = −gm·R_C = −40m·10k = −400`.
- `Ac ≈ −R_C/(2·R_tail) = −10k/(2·500k) = −0.01`.
- `CMRR = 400/0.01 = 40,000` → `= 20·log10(4e4) ≈ 92 dB`.

---

## Worked example — MOS

`I_tail = 1 mA` (so I_D each = 0.5 mA), `gm each = 2 mA/V`, `R_D = 5 kΩ`,
`ro = 100 kΩ`.
- `Ad = −gm·(R_D∥ro) = −2m·(5k∥100k ≈ 4.76k) = −9.52`.
- CMRR with mirror tail `= gm·ro = 2m·100k = 200` → 46 dB.
  (MOS gets less CMRR than BJT at equal gm·ro since gm per mA is lower.)

---

## GATE traps (differential amplifiers)

1. Each half carries **I_tail/2** — students use full I_tail in gm.
2. `Ad` for **differential output** is `−gm·R_C`; for a *single-ended* tap it's
   half that. Check how many outputs the circuit really has.
3. CMRR inflates only with a big/perfect tail (mirror!). Plain R_tail → low CMRR.
4. Signs: differential-out may be taken as `v_o1 − v_o2`; flipping the order
   flips polarity. GATE usually wants magnitude.
5. MOS pair input current = 0 — never write I_B into a MOS solution.
6. At AC, the tail node is: virtual ground for differential, and 2·R_tail seen
   for common-mode — mix them up and every number comes out wrong.

---

## 5-question self-check

1. Each branch current of I_tail? → *I_tail/2.*
2. Ad(diff output), BJT? → *−gm·R_C.*
3. Ac with finite R_tail ≈? → *−R_C/(2R_tail).*
4. Taller tail resistance → CMRR? → *increases.*
5. MOS pair input current? → *0.*

Next: **`19-Op-Amp-Fundamentals.md`**