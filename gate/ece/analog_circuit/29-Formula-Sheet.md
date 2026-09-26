# Chapter 29 — Formula Sheet (every formula, one place)

> **The idea in one line:** this is the whole subject compressed. If you know
> these equations *cold* (and can re-derive each in 30 seconds), you can solve
> any GATE 1–2 mark analog numerical.

---

## 29.0 Universal constants

- `V_T = kT/q ≈ 25 mV` at 300 K (GATE uses 25 mV).
- Silicon `Vγ ≈ 0.7 V`; Germanium `≈ 0.3 V`.
- The "40": `gm(BJT) = 40·I_C[A]` mA/V.
- `20·log10` voltages, `10·log10` powers.

---

## 29.1 Diodes

```
Shockley:         i_D = I_S·(e^{v_D/(nV_T)} − 1)
Reverse current:  i_D ≈ −I_S      (v_D negative, |v_D| > 4V_T)
Dynamic rees.:    r_d = n·V_T/I_D      (≈ 25 mV/I_D at n=1)
Ideal diode:      ON = short, OFF = open
CVD:              ON = Vγ battery, OFF = open
Piecewise:        ON: v_D = Vγ + r_d·i_D
Q-point:          solve I = (V − V_D)/R against the model
```

### Clippers / clampers (Chapter 03/04)
```
Clipper:   output follows v_in UNTIL threshold; pinned beyond
Clamper:   shift signal by ±(peak) so an extreme touches a reference
           + clamper: bottom→0 ; − clamper: top→0   (ideal, ±Vm sine)
Silicon:   clamping level shifts by 0.7 V
```

---

## 29.2 Rectifiers

| | HWR | FWR (both) |
|---|---|---|
| V_dc | Vm/π | 2Vm/π |
| V_rms | Vm/2 | Vm/√2 |
| γ (ripple) | 1.21 | 0.48 |
| η | 40.6% | 81.2% |
| f_ripple | f | 2f |
| PIV | Vm | CT: 2Vm; bridge: Vm |

```
With drops:  HWR Vdc=(Vm−0.7)/π; CT-FWR=(Vm−0.7)·2/π; bridge=(Vm−1.4)·2/π
Capacitor:   V_r ≈ I_dc/(f_r·C) ;  V_dc ≈ Vm − V_r/2
γ with C ≈ V_r/V_dc
Average current: I_dc = V_dc/R_L
```

---

## 29.3 BJT fundamentals & small-signal

```
I_E = I_C + I_B ;  α = I_C/I_E ;  β = I_C/I_B
β = α/(1−α) ;  α = β/(β+1) ;  I_E = (β+1)·I_B
Active region (NPN):  V_C > V_B > V_E ;  V_BE ≈ 0.7
Saturation: V_CE(sat) ≈ 0.2 V ;  condition β·I_B ≥ I_C(sat)
Small-signal:
gm = I_C/V_T ;  rπ = β/gm = βV_T/I_C ;  re = V_T/I_E ≈ V_T/I_C
rπ = (β+1)·re ;  ro = V_A/I_C
```

### Amplifier gains & impedances
```
CE (bypassed):  A_v = −gm·(R_C∥R_L) ;  R_in = RB∥rπ ;  R_out = RC
CE (unbypassed R_E): A_v = −gm·R_C/(1+gm·R_E) ≈ −R_C/R_E
                  R_in = RB∥(β+1)(re+R_E)  ; R_out = RC
CB:         A_v = gm·(R_C∥R_L) (+non-inv) ; R_in ≈ re ; R_out = RC
CC:         A_v = (R_E∥R_L)/(re + R_E∥R_L) ≈ 1 ; R_in = RB∥(β+1)(re+RE∥RL)
            R_out ≈ re + R_s/(β+1)
Cascade:    A_tot = A_1·A_2·... (loaded gains!) ; dB: add
```

---

## 29.4 MOSFET fundamentals & small-signal

```
Saturation: I_D = ½·k·(V_GS−V_th)²·(1 + λ·V_DS)     [k = μn·Cox·W/L]
Triode:     I_D = k·[(V_GS−V_th)V_DS − V_DS²/2]     (small V_DS: resistor)
Cutoff:     V_GS ≤ V_th → ID = 0
Region:     sat iff V_DS ≥ V_GS − V_th
Small-signal:
gm = k·(V_GS−V_th) = 2I_D/(V_GS−V_th) = √(2k·I_D)
ro = 1/(λ·I_D)
gmb = η·gm (η ≈ 0.1–0.3) — only when body not tied to source
```
### Amplifier gains & impedances
```
CS (bypassed): A_v = −gm·(R_D∥R_L) ; R_in = RG ; R_out = RD
CS (unbypassed RS): A_v = −gm·R_D/(1+gm·RS) ≈ −R_D/RS ; R_in = RG
CG:          A_v = +gm·(R_D∥R_L) ; R_in ≈ 1/gm ; R_out = RD
CD:          A_v = RL/(RL + 1/gm) ≈ 1 ; R_in = RG ; R_out ≈ 1/gm
Cascode:     CS then CG — high BW/R_out
```

---

## 29.5 Frequency response

```
Low cutoff (coupling/bypass):
  f_C = 1/(2π·C·R_eff)
  R_eff C1≈Rs+Rin_stage ; C2≈Rout+RL ; CE bypass ≈ re+R_B/(β+1)
Dominant pole:  f_L ≈ max of the poles (rss if close)
High cutoff:    Miller !!
Miller:      C_M = Cμ·(1 + |A|)      (inverting stages only: CE/CS)
f_H ≈ 1/(2π·R_char·C_in_total)
Bandwidth = f_H − f_L (≈ f_H if dc-coupled)
GBW ≈ A_m·BW = const (single-pole)
N identical stages: f_H,total ≈ f_H·√(2^(1/N)−1)
```

---

## 29.6 Current mirrors

```
BJT: I_out ≈ I_ref·β/(β+2) ; R_out = ro
BJT ratio (emitter resistors): I_out ≈ (R_E1/R_E2)·I_ref
MOS: I_out/I_ref = (W2/L2)/(W1/L1)  (matched, λ=0)
MOS with λ: I_out = I_ref·(1+λV_DS2)/(1+λV_DS1)
R_out(MOS mirror) = 1/(λI_D)
Widlar: I_out ≈ (V_T/R_E)·ln(I_ref/I_out)
Compliance: BJT ≥ V_CE(sat)≈0.2V ; MOS ≥ (V_GS−V_th) (keep in sat)
```

---

## 29.7 Differential amplifier

```
v_id = v1−v2 ; v_icm = (v1+v2)/2
Each branch: I = I_tail/2
Ad(diff-out) BJT = −gm·R_C ; (single-ended) = −gm·R_C/2
Ad MOS = −gm·(R_D∥ro)
Ac ≈ −R_C/(2·R_tail) ; CMRR = Ad/Ac ; dB = 20log10(Ad/Ac)
Perfect tail → Ac→0, CMRR→∞
MOS pair: R_in = ∞ ; BJT: R_in = 2rπ
Max diff input before steering: MOS ≈ √2·(V_GS−V_th)
```

---

## 29.8 Op-amp

```
Ideal: A=∞, R_in=∞, R_out=0, offset=0, CMRR=∞, SR=∞
Virtual short (neg. feedback + linear): v+ = v−
Inverting:   A_v = −R_f/R1 ; R_in = R1 ; R_out ≈ 0
Non-inv:     A_v = 1 + Rf/R1 ; R_in ≈ ∞
Follower:    A_v = +1
Summer:      v_o = −R_f(Σ v_i/R_i)
Difference:  v_o = (R2/R1)(v2 − v1)  (matched)
Integrator:  v_o = −(1/RC)∫v_in dt ; H = −1/(jωRC)
Practical int: add R_f → DC gain −Rf/R1, corner 1/(2πRfC)
Differentiator: v_o = −RC·dv_in/dt ; H = −jωRC
Practical diff: add Rs in series with C
Saturation: output clamps at rail; virtual short breaks
SR limit: SR = 2π·f_max·V_pk(need ≤ device SR)
Offset error at output = V_os·(1 + Rf/R1)
```

---

## 29.9 Filters

```
1st order LPF:  H=1/(1+j f/fc) ; f_c=1/(2πRC) ; 20 dB/dec
1st order HPF:  H=(jf/fc)/(1+jf/fc)
2nd order:      +40 dB/dec ; Q defines peaking
Butterworth:    Q = 1/√2 ≈ 0.707 (maximally flat)
Sallen-Key equal RC unity: ω_o=1/RC, Q=1/3
Sallen-Key gain k: Q = 1/(3−k)   (k→3 → oscillation)
General S-K: Q = √(C1C2R1R2)/(R1C1+R2C1+R1C2(1−k))
Band-pass:  f_o = 1/(2π√(R-C combo...)); Q = f_o/BW; BW = f_H − f_L
Roll-off = 20·order dB/dec
```

---

## 29.10 Schmitt / comparator

```
Comparator (open loop): v_o = ±V_sat (no virtual short)
Non-inv Schmitt:
  UT = V_ref + V_sat·R1/R_f
  LT = V_ref − V_sat·R1/R_f
Hysteresis = UT − LT = 2·V_sat·R1/R_f
```
(with v− = V_ref; symmetric rails ⇒ ±Vth, Vth = V_sat·R1/R_f)

---

## 29.11 Feedback

```
A_f = A/(1 + Aβ)      (negative)
A_f = A/(1 − Aβ)      (positive)
Deep:  A_f ≈ 1/β
Effects: gain ↓(1+Aβ) ; stability ↑ ; BW up ×(1+Aβ) ;
         distortion ↓(1+Aβ)
Topologies:  voltage-sample ↓Rout ; current-sample ↑Rout
             series-mix ↑Rin ; shunt-mix ↓Rin
```

---

## 29.12 Oscillators

```
Barkhausen:  |Aβ| = 1  and  ∠Aβ = 0°
Phase-shift: f_o = 1/(2πRC√6) ; min gain = 29
Wien:        f_o = 1/(2πRC) ; gain = 3
Colpitts:    f_o = 1/(2π√(L·C_series)) ; C_ser = C1C2/(C1+C2)
Hartley:     f_o = 1/(2π√((L1+L2)·C))
Relaxation:  T = 2RC·ln(1 + 2R1/R2)
Thresholds:  ±V_sat·R1/(R1+R2)
```
---

## 29.13 Handy numeric results worth memorising

```
Vm/π = 0.318 Vm ;  2Vm/π = 0.637 Vm ;  Vm/2 = 0.5 Vm ;  Vm/√2 = 0.707 Vm
1/√2 = 0.707 ;  √2 = 1.414 ; 20 dB/dec = 6 dB/oct
gm(BJT)@1mA = 40 mA/V → rπ@β100 = 2.5 kΩ → re = 25 Ω
```

---

## How to use this sheet
- Print / copy it. Practice **deriving each row blind** after finishing its
  chapter. By exam time you should be able to regenerate the whole sheet from
  the "idea in one line" of each chapter.

Next: **`30-Priority-Checklist.md`**