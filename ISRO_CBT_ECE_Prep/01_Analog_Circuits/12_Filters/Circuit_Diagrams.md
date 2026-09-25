# Analog Filters — Circuit Diagrams

Companion schematics for `Concepts.md`. A filter is a frequency-selective network; making it
active with an op-amp adds gain, buffering and tunability while keeping the passive `RC`
shape.

## 1. Passive First-Order Low-Pass and High-Pass

The two one-resistor one-capacitor networks are the starting point for everything else.

```circuit
src = elm.SourceSin().right().length(2).at((-7, 1.5)).label('Vin', loc='left')
elm.Ground().down().at((-7, 1.5))
elm.Line().at((-5, 1.5)).right(2).to((-3, 1.5))
elm.Resistor().right().length(2).at((-3, 1.5)).label('R', loc='top')
elm.Line().at((-1, 1.5)).right(0.5).to((-0.5, 1.5))
elm.Dot().at((-2, 1.5)).label('Vout', loc='top')
elm.Capacitor().down().length(2).at((-0.5, 1.5)).label('C', loc='right')
elm.Ground().down().at((-0.5, -0.5))
elm.Annotate().at((2.5, 1.2)).delta(0, 0.6).label('low-pass: fc = 1/(2*pi*RC), -20 dB/dec,\nVout/Vin = 1/(1 + j*f/fc)')
src2 = elm.SourceSin().right().length(2).at((-7, -3)).label('Vin', loc='left')
elm.Ground().down().at((-7, -3))
elm.Line().at((-5, -3)).right(2).to((-3, -3))
elm.Capacitor().right().length(1.5).at((-3, -3)).label('C', loc='bottom')
elm.Line().at((-1.5, -3)).right(1).to((-0.5, -3))
elm.Dot().at((-2, -3)).label('Vout', loc='bottom')
elm.Resistor().down().length(2).at((-0.5, -3)).label('R', loc='right')
elm.Ground().down().at((-0.5, -5))
elm.Annotate().at((2.5, -3.3)).delta(0, -0.6).label('high-pass: same corner, opposite tilt;\nVout/Vin = j*f/fc / (1 + j*f/fc)')
elm.Annotate().at((-7, -0.9)).delta(0, -0.6).label('R and C are interchangeable between the two circuits: the response is the same, only the output tap changes')
```

- A first-order network can never be sharper than 20 dB per decade; everything sharper needs
  more reactive elements.
- The passive sections load each other, so cascading them does not give the sum of their
  individual responses.

## 2. First-Order Active Low-Pass (Inverting)

Adding the op-amp gives voltage gain, a high input impedance and a low output impedance
without changing the corner.

```circuit
src = elm.SourceSin().right().length(2).at((-7, 0.875)).label('Vin', loc='left')
elm.Ground().down().at((-7, 0.875))
elm.Line().at((-5, 0.875)).right(2).to((-3, 0.875))
r1 = elm.Resistor().right().length(2).at((-3, 0.875)).label('R1', loc='top')
elm.Line().at((-1, 0.875)).right(1)
elm.Dot().at((-1, 0.875)).label('summing node', loc='bottom')
c = elm.Capacitor().down().length(2).at((-1, 0.875)).label('C', loc='left')
elm.Ground().down().at((-1, -1.125))
elm.Line().at((-1, 0.875)).up(2.125).to((-1, 3))
rf = elm.Resistor().left().length(2).at((-1, 3)).label('Rf', loc='bottom')
elm.Line().at((1.4151, 3)).right(1.5859).to((3.4151, 3))
elm.Line().at((3.4151, 3)).down(1.5).to((3.4151, 1.5))
op = elm.Opamp(leads=True).at((0, 1.5))
elm.Dot().at((3.4151, 1.5))
elm.Line().at((3.4151, 1.5)).right(1.5).to((4.9151, 1.5))
elm.Dot().at((4.9151, 1.5)).label('Vout', loc='top')
elm.Line().at((0, 2.125)).left(1.5).to((-1.5, 2.125))
elm.Ground().down().at((-1.5, 2.125))
elm.Annotate().at((6.5, 1.4)).delta(0, 0.6).label('Vout/Vin = -Rf/R1 * 1/(1 + s*R1*C)\nfc = 1/(2*pi*R1*C), and the gain can be\nanything the resistors set')
elm.Annotate().at((-7, 2.4)).delta(0, 0.6).label('inverting: one input is grounded, so the input impedance is just R1 and the stage inverts')
elm.Annotate().at((6.5, -1.2)).delta(0, -0.6).label('the capacitor returns to the same summing node, so the pole is set by R1 alone:\nusing (R1 || Rf) would be wrong')
```

- Because the capacitor sits at the virtual ground, the corner depends only on the input
  resistor, not on the gain-setting ratio.
- Cascading two of these multiplies two first-order responses, giving a second-order roll-off.

## 3. First-Order Low-Pass with Gain (Non-Inverting)

A passive `RC` into the positive input and a resistive feedback on the negative input gives a
low-pass stage with a passband gain of `K = 1 + Rf/R1`.

```circuit
src = elm.SourceSin().right().length(2).at((-7, 2.125)).label('Vin', loc='left')
elm.Ground().down().at((-7, 2.125))
elm.Line().at((-5, 2.125)).right(2).to((-3, 2.125))
r1 = elm.Resistor().right().length(2).at((-3, 2.125)).label('R1', loc='top')
elm.Line().at((-1, 2.125)).right(1).to((0, 2.125))
elm.Dot().at((-1, 2.125))
c = elm.Capacitor().down().length(2).at((-1, 2.125)).label('C', loc='left')
elm.Ground().down().at((-1, 0.125))
op = elm.Opamp(leads=True).at((0, 1.5))
elm.Line().at((3.4151, 1.5)).up(2.5).to((3.4151, 4))
rf = elm.Resistor().left().length(3).at((3.4151, 4)).label('Rf', loc='top')
elm.Line().at((-0.4151, 4)).left(0.5849).to((-1, 4))
r2 = elm.Resistor().down().length(2).at((-1, 4)).label('R2', loc='left')
elm.Line().at((-1, 2)).down(1.125).to((-1, 0.875))
elm.Dot().at((-1, 0.875))
elm.Line().at((3.4151, 1.5)).right(1.5).to((4.9151, 1.5))
elm.Dot().at((4.9151, 1.5)).label('K*Vin', loc='top')
elm.Annotate().at((6.5, 2.4)).delta(0, 0.6).label('K = 1 + Rf/R2 in the passband, and the -3 dB point\nis still 1/(2*pi*R1*C): the passive section sets\nthe corner, the feedback sets the gain')
elm.Annotate().at((-7, 3.6)).delta(0, 0.6).label('this is the first stage of a Sallen-Key filter:\nadding a second RC section makes it second order')
```

- The non-inverting form is the usual choice when the passband gain must be exact and the
  signal must not be inverted.
- With `K = 1` (a unity-gain follower) the same input network gives a buffered first-order
  low-pass, which is the standard way to isolate two passive sections.

## 4. Second-Order Sallen-Key Low-Pass

Two RC sections plus the amplifier give `-40 dB/dec`; the gain sets the `Q`, and unity gain
gives a Butterworth response.

```circuit
src = elm.SourceSin().right().length(2).at((-6, 3)).label('Vin', loc='left')
elm.Ground().down().at((-6, 3))
elm.Line().at((-4, 3)).right(2).to((-2, 3))
ra = elm.Resistor().right().length(2).at((-2, 3)).label('R1', loc='top')
elm.Line().at((0, 3)).right(2)
elm.Dot().at((0, 3)).label('A', loc='top')
rb = elm.Resistor().right().length(2).at((0, 3)).label('R2', loc='bottom')
elm.Line().at((2, 3)).right(3).to((5, 3))
elm.Dot().at((2, 3)).label('B', loc='top')
c2 = elm.Capacitor().down().length(1.5).at((2, 3)).label('C2', loc='right')
elm.Ground().down().at((2, 1.5))
elm.Line().at((0, 3)).up(1.5).to((0, 4.5))
c1 = elm.Capacitor().right().length(2).at((0, 4.5)).label('C1', loc='top')
elm.Line().at((2, 4.5)).right(8.4151).to((10.4151, 4.5))
elm.Line().at((10.4151, 4.5)).down(4.5).to((10.4151, 0))
op = elm.Opamp(leads=True).at((6, 0))
elm.Line().at((6, -0.625)).left(1.5).to((4.5, -0.625))
elm.Ground().down().at((4.5, -0.625))
elm.Line().at((10.4151, 0)).right(1.5).to((11.9151, 0))
elm.Dot().at((11.9151, 0)).label('Vout', loc='top')
elm.Annotate().at((0, 6.2)).delta(0, 0.6).label('f0 = 1/(2*pi*sqrt(R1*R2*C1*C2))   and   Q = sqrt(R1*C1/(R2*C2))/(2-K), where K is the closed-loop gain')
elm.Annotate().at((14, 1.6)).delta(0, 0.6).label('C1 feeds a fraction of the output back to node A, which is what sets Q;\nfor a Butterworth response with equal R and C,\nK = 1.586 gives Q = 0.707 and unity gain (K = 1)\ngives Q = 0.5, a maximally flat response')
elm.Annotate().at((14, -1.4)).delta(0, -0.6).label('a higher K raises Q: the response peaks before the corner\nand then falls faster, at the cost of peaking in the passband')
```

- `K = 1.586` is the standard Sallen-Key Butterworth gain; unity gain gives a gentler
  response that cannot be made critically damped by gain alone.
- Matching `R1 = R2` and `C1 = C2` makes the corner formula reduce to `1/(2*pi*R*C)`, which
  is worth doing in a first design.

## 5. First-Order Active High-Pass

The series element and the shunt element swap places; everything else about the active
stage is unchanged.

```circuit
src = elm.SourceSin().right().length(2).at((-7, 0.875)).label('Vin', loc='left')
elm.Ground().down().at((-7, 0.875))
elm.Line().at((-5, 0.875)).right(2).to((-3, 0.875))
c = elm.Capacitor().right().length(1.5).at((-3, 0.875)).label('C', loc='bottom')
elm.Line().at((-1.5, 0.875)).right(0.5).to((-1, 0.875))
elm.Dot().at((-1, 0.875))
elm.Resistor().down().length(2).at((-2, 0.875)).label('R1', loc='left')
elm.Ground().down().at((-2, -1.125))
elm.Line().at((-1, 0.875)).up(2.125).to((-1, 3))
rf = elm.Resistor().left().length(2).at((-1, 3)).label('Rf', loc='bottom')
elm.Line().at((1.4151, 3)).right(1.5859).to((3.4151, 3))
elm.Line().at((3.4151, 3)).down(1.5).to((3.4151, 1.5))
op = elm.Opamp(leads=True).at((0, 1.5))
elm.Dot().at((3.4151, 1.5))
elm.Line().at((3.4151, 1.5)).right(1.5).to((4.9151, 1.5))
elm.Dot().at((4.9151, 1.5)).label('Vout', loc='top')
elm.Line().at((0, 2.125)).left(1.5).to((-1.5, 2.125))
elm.Ground().down().at((-1.5, 2.125))
elm.Annotate().at((6.5, 1.4)).delta(0, 0.6).label('Vout/Vin = -Rf/R1 * sRC/(1 + sRC)\nfc = 1/(2*pi*R1*C): gain rises at +20 dB/dec\nbelow the corner and flattens above it')
elm.Annotate().at((6.5, -1.2)).delta(0, -0.6).label('a high-pass stage is used for AC coupling, hum rejection\nand to block the DC offset of a later stage')
```

- A high-pass section followed by a low-pass section gives a band-pass response, and the
  second-order form is the one used for audio crossovers.
- The passband gain is still set by the resistor ratio, so the two sections can be cascaded
  with any desired total gain.

## 6. Band-Pass and Band-Stop

A band-pass is two sections in series; a band-stop is a subtractor fed by a low-pass and a
high-pass of the same signal.

```circuit
elm.Rect(corner1=(-9, 2.5), corner2=(-5, 5.5)).label('high-pass section\npasses above f1', loc='center')
elm.Line(arrow='->').at((-5, 4)).right(1.5)
elm.Rect(corner1=(-3.5, 2.5), corner2=(0.5, 5.5)).label('low-pass section\npasses below f2', loc='center')
elm.Line(arrow='->').at((0.5, 4)).right(1.5)
elm.Rect(corner1=(2, 2.5), corner2=(6, 5.5)).label('band-pass:\nflat only between f1 and f2,\n-20 dB/dec at each end', loc='center')
elm.Line().at((-9, 1.5)).right(15).to((6, 1.5))
elm.Rect(corner1=(-9, -1.5), corner2=(-4, 1.5)).label('low-pass output\nfavours the low band', loc='center')
elm.Line(arrow='->').at((-4, 0)).right(1.5)
elm.Rect(corner1=(-2.5, -1.5), corner2=(2, 1.5)).label('subtractor with\na matching high-pass', loc='center')
elm.Line(arrow='->').at((2, 0)).right(1.5)
elm.Rect(corner1=(3.5, -1.5), corner2=(8, 1.5)).label('band-stop (notch):\nzero output near f0,\nflat at DC and at HF', loc='center')
elm.Annotate().at((-1, -2.6)).delta(0, -0.6).label('a twin-T or bridged-T notch is the classic passive band-stop;\nits centre frequency is set by ratios of R and C, so it is hard to tune\nand its rejection depends on component matching')
elm.Annotate().at((-1, 6.2)).delta(0, 0.6).label('cascading is only valid if each section has a high input impedance:\nuse an op-amp buffer between sections, or build one two-order section instead')
```

- Band-pass bandwidth is the ratio `f2/f1`, and the shape is set by the two corners' spacing
  in octaves.
- A notch is the natural filter for removing 50 or 60 Hz hum because its rejection can be made
  very deep at one frequency.

## 7. Response Shapes: Butterworth, Chebyshev, Elliptic, Bessel

The choice is a trade between passband flatness and stopband sharpness, with Bessel choosing
delay instead.

```circuit
elm.Rect(corner1=(-10, 2.5), corner2=(-5, 5.5)).label('Butterworth:\nmaximally flat, no ripple,\n-20n dB/dec', loc='center')
elm.Rect(corner1=(-3.5, 2.5), corner2=(1.5, 5.5)).label('Chebyshev I:\nripple in the passband,\nsteepest for the order', loc='center')
elm.Rect(corner1=(3, 2.5), corner2=(8, 5.5)).label('Chebyshev II:\nripple in the stopband,\nflat passband', loc='center')
elm.Rect(corner1=(-10, -1.5), corner2=(-5, 1.5)).label('Elliptic:\nripple in both bands,\nsharpest of all', loc='center')
elm.Rect(corner1=(-3.5, -1.5), corner2=(1.5, 1.5)).label('Bessel:\nlinear phase, flat delay,\ngentle roll-off', loc='center')
elm.Rect(corner1=(3, -1.5), corner2=(8, 1.5)).label('order fixes the final\nslope, nothing else does:\nfewer poles means\nmore transition band', loc='center')
elm.Line().at((0, 0)).right(10)
elm.Line().at((0, 0)).up(3.5)
elm.Line().at((0, 2)).to((5, 2))
elm.Line().at((5, 2)).to((10, -0.5))
elm.Line().at((0, 2.1)).to((1, 1.9)).to((2, 2.1)).to((3, 1.9)).to((4, 2.1)).to((5, 2))
elm.Line().at((5, 2)).to((6, 0.5)).to((7, 1.2)).to((8, -0.5))
elm.Line().at((0, 0.15)).to((2, 0.15)).to((2, -0.15)).to((4, -0.15)).to((4, 0.15))
elm.Annotate().at((0, 2.8)).delta(0, 0.6).label('flat and smooth: Butterworth.  ripple then a steep dive: Chebyshev I')
elm.Annotate().at((0, -1)).delta(0, -0.6).label('the transition band is what the specification actually fixes: the frequency between\n-3 dB and the stopband edge, and the number of poles is chosen to cross it')
```

- Elliptic responses achieve the narrowest transition band for a given order, at the cost of
  ripple and a very high stopband termination sensitivity.
- Bessel is chosen for pulse and data signals, where a constant delay matters more than a
  sharp edge.

## 8. Order and Roll-Off

The order is simply the number of poles, and each pole adds 20 dB per decade of attenuation.

```circuit
elm.Line().at((0, 0)).to((6, 0)).to((12, -2))
elm.Line().at((0, 1.25)).to((6, 1.25)).to((9, -1))
elm.Line().at((0, 1.67)).to((6, 1.67)).to((9, -1.67))
elm.Line().at((0, -2)).up(4)
elm.Line().at((0, 0)).right(12.5)
elm.Annotate().at((2, 0.05)).delta(0, -0.6).label('1st order: -20 dB/dec')
elm.Annotate().at((2, 1.3)).delta(0, 0.6).label('2nd order: -40 dB/dec')
elm.Annotate().at((2, 1.72)).delta(0, 0.6).label('3rd order: -60 dB/dec')
elm.Annotate().at((10.5, 0.6)).delta(0, 0.6).label('all three share the same\n-3 dB point; only the\nfinal slope differs')
elm.Annotate().at((0, -3.2)).delta(0, -0.6).label('one decade past the corner puts a pole 20 dB down and two poles 40 dB down,\nso doubling the order buys 20 dB of rejection at one frequency but doubles the\ncomponent count, the noise and the sensitivity to tolerance')
elm.Annotate().at((0, -4.4)).delta(0, -0.6).label('rules of thumb: 4th order is usually the point where stopband ripple starts to matter,\nand beyond 6th order the tolerance of the components dominates the response')
```

- A second-order filter is the practical default; a fourth-order Butterworth is the usual
  compromise in audio and anti-aliasing work.
- Cascading a first-order and a second-order section is a cheap way to reach a given slope
  without a single high-order design.

## 9. Choosing the Sallen-Key Gain for a Butterworth Response

The amplifier gain inside a Sallen-Key section is the one free parameter that sets the `Q`.

```circuit
elm.Rect(corner1=(-9, 2.5), corner2=(-4, 5.5)).label('Q is set by the closed-loop\ngain K of the amplifier\ninside the RC network', loc='center')
elm.Line(arrow='->').at((-4, 4)).right(1.5)
elm.Rect(corner1=(-2.5, 2.5), corner2=(2.5, 5.5)).label('K = 1:  Q = 0.5\noverdamped, gentle corner,\nno peaking', loc='center')
elm.Line(arrow='->').at((2.5, 4)).right(1.5)
elm.Rect(corner1=(4, 2.5), corner2=(9, 5.5)).label('K = 1.586:  Q = 0.707\nButterworth, flat to -3 dB\nat the corner', loc='center')
elm.Rect(corner1=(-9, -1.5), corner2=(-4, 1.5)).label('K approaching 2\nmakes Q and the peak\nrise sharply', loc='center')
elm.Line(arrow='->').at((-4, 0)).right(1.5)
elm.Rect(corner1=(-2.5, -1.5), corner2=(2.5, 1.5)).label('Q = 0.707 is the Butterworth\ncondition; a critically damped\nresponse has Q = 0.5', loc='center')
elm.Line(arrow='->').at((2.5, 0)).right(1.5)
elm.Rect(corner1=(4, -1.5), corner2=(9, 1.5)).label('for equal R and C,\nK = 3 - 1/Q, so the\nresistor ratio is chosen\nas Rf/R1 = K - 1', loc='center')
elm.Annotate().at((0, -2.6)).delta(0, -0.6).label('the passband gain of the whole stage is K, not 1: a Butterworth Sallen-Key low-pass\noften has a passband gain of 1.586, which must be divided out afterwards or designed for\nwith a following stage')
elm.Annotate().at((0, 6.2)).delta(0, 0.6).label('the alternative is a multiple-feedback section, where the gain and Q are independent:\nno passband gain penalty, but four resistors and two capacitors')
```

- A `K` of 1.586 is only correct for equal component values; with unequal values the gain
  equation changes, so set the corner and `Q` from the full expressions.
- A `K` above 1.5 in a non-inverting Sallen-Key stage risks clipping before the filter
  reaches its stopband attenuation, which is why the MFB form is preferred in precision work.

## 10. Switched-Capacitor Filters

A switched capacitor replaces a large resistor with a sampling ratio, so filters become an
integrator problem and integrate well into an IC.

```circuit
elm.Rect(corner1=(-9, 2.5), corner2=(-4, 5.5)).label('a switched capacitor\nbehaves as R = T/C\nwhere T is the clock period', loc='center')
elm.Line(arrow='->').at((-4, 4)).right(1.5)
elm.Rect(corner1=(-2.5, 2.5), corner2=(2.5, 5.5)).label('with C = 100 fF and\na 100 kHz clock:\nR = 10 us/100 fF = 100 MOhm', loc='center')
elm.Line(arrow='->').at((2.5, 4)).right(1.5)
elm.Rect(corner1=(4, 2.5), corner2=(9, 5.5)).label('so a biquad built from\nintegrators sets the corner\nfrom capacitor ratios\nand clock ratios only', loc='center')
elm.Rect(corner1=(-9, -1.5), corner2=(-4, 1.5)).label('continuous-time filters:\nno clock needed, but R\nvalues drift with process', loc='center')
elm.Line(arrow='->').at((-4, 0)).right(1.5)
elm.Rect(corner1=(-2.5, -1.5), corner2=(2.5, 1.5)).label('switched-capacitor:\naccurate and tunable, but\nthe input must not contain\nfrequencies near the clock', loc='center')
elm.Line(arrow='->').at((2.5, 0)).right(1.5)
elm.Rect(corner1=(4, -1.5), corner2=(9, 1.5)).label('the clock spur and the\naliasing at Nyquist are\nwhy a switched-capacitor\nfilter is followed by a simple\ncontinuous anti-alias filter', loc='center')
elm.Annotate().at((0, 6.2)).delta(0, 0.6).label('state-variable, biquad and universal (Tow-Thomas) topologies are the usual integrated realisations')
elm.Annotate().at((0, -2.6)).delta(0, -0.6).label('examination point: a switched-capacitor filter cannot pass DC accurately because the\nDC gain depends on the clock, and it needs at least a few clock cycles to settle')
```

- Tunability is the main advantage: a programmable clock retunes the filter without changing
  any capacitor.
- The clock feedthrough appears as a spur at the clock frequency, so a low-pass section is
  always added at the output.

## 11. Anti-Aliasing: the Practical Application

An anti-alias filter before a sampler must suppress everything above the Nyquist frequency
by enough to keep it under the converter's resolution.

```circuit
elm.Line(arrow='->').at((-8, 0)).right(1.5)
elm.Rect(corner1=(-6.5, -1.5), corner2=(-1.5, 1.5)).label('4th-order Butterworth\nlow-pass at 0.4*fsample\n=-12 dB at Nyquist', loc='center')
elm.Line(arrow='->').at((-1.5, 0)).right(1.5)
elm.Rect(corner1=(0, -1.5), corner2=(4, 1.5)).label('sample-and-hold\nthen a 16-bit ADC:\neach bit needs 6 dB', loc='center')
elm.Line(arrow='->').at((4, 0)).right(1.5)
elm.Rect(corner1=(5.5, -1.5), corner2=(9.5, 1.5)).label('digital domain:\ndecimation filter\ncan now be sharp and\ncheap', loc='center')
elm.Annotate().at((0, 3.2)).delta(0, 0.6).label('a signal at the Nyquist frequency that aliases down to DC is impossible to remove later,\nso the analogue filter must do all the work before the sampler')
elm.Annotate().at((0, -3.2)).delta(0, -0.6).label('design rule: put the -3 dB point at 0.4 to 0.45 of the sampling rate, and check the response at the\nhighest input frequency you must accept, not just at Nyquist')
elm.Annotate().at((0, -4.4)).delta(0, -0.6).label('the same argument in the other direction: a reconstruction filter after a DAC removes the\nimages that the zero-order hold left at multiples of the sampling frequency')
```

- Four poles give 24 dB per decade, so a modest roll-off is usually enough for a 12 to 16 bit
  converter.
- The aperture jitter of the sampler is a separate error that no filter can remove, so a long
  aperture time must be avoided for high `fsample`.

## 12. Summary of the Useful Relations

| Quantity | Formula | Note |
|---|---|---|
| First-order corner | `fc = 1/(2*pi*R*C)` | passive or active |
| Sallen-Key corner | `f0 = 1/(2*pi*sqrt(R1R2C1C2))` | second order |
| Sallen-Key Q (equal R,C) | `Q = 1/(3 - K)` | `K = 1.586` is Butterworth |
| Roll-off | `20n dB/dec` | `n` is the order |
| Transition band | set by poles | the specification usually decides `n` |
| Switched-capacitor resistance | `R = T/C` | `T` is the clock period |
| Anti-alias corner | `0.4 to 0.45*fsample` | 4th order is typical |
