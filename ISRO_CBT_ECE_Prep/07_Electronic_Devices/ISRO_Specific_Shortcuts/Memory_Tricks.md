# EDC Memory Tricks

## Mnemonic: "**BETA** helps **ALPHA**"

### α ↔ β Conversions
"**Beta is from Alpha, 1 minus Alpha**"
$$\beta = \frac{\alpha}{1-\alpha}$$

Trick: To convert α to β: "One minus alpha in denominator"
- α = 0.99 → 1-0.99 = 0.01 → β = 99

### Reverse
$$\alpha = \frac{\beta}{1+\beta}$$
- β = 100 → 101 in denominator → α = 100/101 ≈ 0.99

---

## Memory Trick: "**GRE**EN Si" for Ge vs Si bandgap

- **G**e = 0.**67** eV (think: 67)
- **R**oom temp
- **Si** = 1.12 eV (approx 1.1)
- **E**luctant: "GaAs = 1.43"

Order: Ge (0.67) < Si (1.12) < GaAs (1.43)

---

## Mobility Trick: "**E**ntel **H**as **S**peed"

**E**lectrons move **F**aster than **H**oles:
- μn > μp always
- Highest μn: GaAs (8500)
- Si μn = 1350, μp = 480

---

## Fermi Level Position: "**D**oped **A**t **C**enter"

- **D**onor (N-type): EF Above i (toward Conduction band)
- **A**cceptor (P-type): EF Below i (toward Valence band)
- **C**enter (Intrinsic): EF at midgap

---

## Depletion Region: "**RV** = **W**ide"

**R**everse bias → **V**aried/wide depletion
**F**orward bias → **F**lat/narrow depletion

reverse = Wider, forward = Narrower

---

## Breakdown: "**Z**en **Aval** - **Z**ero at 56"

- **Z**ener: below 5V, Negative temp coeff
- **Avalanche**: above 6V, Positive temp coeff
- At **5.6V**: Zero temp coefficient

Think: "Z Negative, A Positive, 5.6 Zero"

---

## Diode/Capacitance: "**F**orward **D**iffusion, **R**everse **J**unction"

- **F**orward → **D**iffusion capacitance dominates
- **R**everse → **J**unction (depletion) capacitance dominates

---

## BJT Regions: "**Active** Amplifies, **Sat**urates, **Cut**s"

- **Active** → amplification
- **Saturation** → switch ON (VCE=0.2)
- **Cutoff** → switch OFF

---

## gm Values: "**40 in mA**" for BJT

gm(BJT) = 40 × IC(mA) mS
- "A 1 mA BJT gives 40 mS gm"
- Double current → double gm

---

## MOSFET gm: "**2ID over Vov**"

$$g_m = \frac{2I_D}{V_{OV}}$$

Trick: "Two I-D Over V-Over"

---

## Temperature Coefficients: "**V**ery **N**egative"

- **V**BE: -2 mV/°C (negative)
- **V**T: +0.086 mV/K (positive)

In bandgap: "VBE is down, KT is up, sum = constant (1.2)"

---

## Wavelength: "**1240** over **E**g"

$$\lambda (nm) = \frac{1240}{E_g (eV)}$$
"1240 is gate to light"

Red (690nm) → 1.8 eV
Green (565nm) → 2.2 eV
Blue (496nm) → 2.5 eV

---

## Diffusion Length: "**L** is **S**quare **R**oot"

$$L = \sqrt{D\tau}$$
"L Sqrt cost = Diffusion times Lifetime"

---

## Early vs Channel Modulation: "**Both** give **r**o"

- BJT Early: ro = VA/IC
- MOSFET Channel Length: ro = 1/(λID)
Both finite output resistance.

---

## Einstein Relation: "**D**runk **M**uscle"

$$\frac{D}{\mu} = \frac{kT}{q} = V_T$$
"D over mu = thermal Voltage"
At 300K: 26 mV

---

## IDEAL approximations: "**IDSS Ideal**"

- JFET: ID = IDSS(1 - VGS/VP)²
- "ID squinches when VGS approaches VP"

---

## Series: "**Series** Stops" (stability)
- Fixed bias: S = β+1 (worst, unstable)
- Series RE: S ≈ 1 + RTH/RE (good)
- "More RE → More stable"

---

## Photodiode: "**Light** up the **Current**"
- Iph ∝ light intensity
- R = ηλ/1240 (responsivity)
- "Responsivity = QE times lambda over 1240"

---

## h-parameters: "**H**appy **I**nput, **F**ast **G**ain, **O**utput **E**-ish"

- h**i**e → input impedance
- h**f**e → forward gain (β)
- h**o**e → output admittance (1/ro)
- h**r**e → reverse (≈0)
(I=nput, F=orward, O=utput, R=everse)

---

## Thermal runaway: "**H**ot **R**unaway"

- Heat → More carriers → More current → More heat
- Prevent with RE (emitter degeneration)
- "RE chokes runaway"

---

## Final Quick Set

| Concept | Value/Trick |
|---------|-------------|
| VT | 26 mV @300K |
| JFET gm0 | 2IDSS/VP |
| BJT gm | 40×IC(mA) mS |
| MOSFET gm | 2ID/Vov |
| Wavelength | 1240/Eg |
| VBE temp | -2 mV/°C |
| Is temp | ×2 per 10°C |
| nb Si | 1.5×10¹⁰ |
| Breakdown Z/A | <5V / >6V |
