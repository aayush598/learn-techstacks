# Circuit Diagrams

## 1. Microwave Device Selection by Bandwidth and Power

Vacuum tubes remain useful at high power, while solid-state devices dominate many lower-power and low-noise functions. The selection is a trade-off among frequency, power, bandwidth, and noise.

```circuit
elm.Block().at((-5, 2)).label("high power\nMagnetron / Klystron", loc="top")
elm.Block().at((-5, 0)).label("broadband\nTWT", loc="top")
elm.Block().at((-5, -2)).label("low noise\nHEMT LNA", loc="bottom")
elm.Arrow().at((-2, 2)).to((0, 2)).label("radar TX", loc="top")
elm.Arrow().at((-2, 0)).to((0, 0)).label("wideband amp", loc="top")
elm.Arrow().at((-2, -2)).to((0, -2)).label("receiver", loc="top")
elm.Block().at((2, 1)).label("vacuum tube\ntrade power for size", loc="top")
elm.Block().at((2, -1)).label("solid state\ntrade power for integration", loc="bottom")
elm.Block().at((6, 0)).label("300 MHz–300 GHz\nmicrowave band", loc="right")
```

## 2. Two-Cavity Klystron Signal Flow

The input cavity velocity-modulates the electron beam. Bunching at the output cavity produces current modulation and delivered microwave power.

```circuit
elm.SourceSin().right().at((-6, 0)).label("RF input", loc="left")
elm.Block().at((-2, 0)).label("input cavity\nvelocity modulation", loc="top")
elm.Arrow().at((0, 0)).to((2, 0)).label("electron beam", loc="top")
elm.Block().at((3, 0)).label("bunching", loc="top")
elm.Arrow().at((5, 0)).to((7, 0)).label("beam power", loc="top")
elm.Block().at((8, 0)).label("output cavity\nRF gain", loc="right")
elm.Block().at((3, -2)).label("narrowband amplifier", loc="bottom")
```

## 3. Magnetron Crossed-Field Oscillator

Electrons move through crossed electric and magnetic fields and interact with a resonant cavity. The cavity supplies the microwave feedback needed for high-power radar oscillation.

```circuit
elm.Block().at((-5, 1)).label("DC electric field", loc="top")
elm.Block().at((-5, -1)).label("magnetic field B", loc="bottom")
elm.Arrow().at((-2, 1)).to((0, 1)).label("crossed fields", loc="top")
elm.Arrow().at((-2, -1)).to((0, -1)).label("Lorentz force", loc="top")
elm.Dot().at((1, 0)).label("electron cloud", loc="top")
elm.Arrow().at((1, 0)).to((3, 0)).label("rotating charge", loc="top")
elm.Block().at((4, 0)).label("resonant cavity", loc="right")
elm.Arrow().at((6, 0)).to((8, 0)).label("high-power RF", loc="top")
elm.Block().at((9, 0)).label("radar transmitter", loc="right")
```

## 4. Traveling-Wave Tube Interaction

A slow-wave helix matches the electron velocity to the RF phase velocity. Successive interaction sections provide broadband amplification as the beam travels along the tube.

```circuit
elm.SourceSin().right().at((-6, 0)).label("RF input", loc="left")
elm.Block().at((-2, 0)).label("electron gun", loc="top")
elm.Arrow().at((0, 0)).to((2, 0)).label("beam", loc="top")
elm.Block().at((3, 0)).label("helical slow-wave\nstructure", loc="top")
elm.Arrow().at((5, 0)).to((7, 0)).label("velocity/phase match", loc="top")
elm.Block().at((8, 0)).label("amplified RF", loc="right")
elm.Block().at((3, -2)).label("broadband\nmoderate/high power", loc="bottom")
```

## 5. Negative-Resistance Solid-State Oscillator

A Gunn, IMPATT, or tunnel diode supplies negative small-signal resistance. The resonator and feedback line set the oscillation frequency while the load receives the output power.

```circuit
elm.Block().at((-6, 0)).label("bias source")
elm.Block().at((-2, 0)).label("Gunn / IMPATT /\ntunnel diode", loc="top")
elm.Arrow().at((0, 0)).to((2, 0)).label("negative R", loc="top")
elm.Block().at((3, 0)).label("resonator", loc="top")
elm.Arrow().at((5, 0)).to((7, 0)).label("oscillation", loc="top")
elm.Resistor().right().at((7, 0)).label("load", loc="bottom")
elm.Arrow().at((3, 0)).to((3, -2)).label("feedback", loc="right")
elm.Line().right(6).at((3, -2)).to((9, -2))
elm.Line().up(2).at((9, -2)).to((9, 0))
elm.Block().at((1, -2)).label("oscillator\nGunn: moderate power\nIMPATT: high power/noise", loc="bottom")
```

## 6. Low-Noise Receiver and Tuning Functions

A HEMT provides low-noise amplification, while a Schottky diode handles mixing or detection. A varactor supplies voltage-controlled tuning for oscillator or filter frequency selection.

```circuit
elm.SourceI().right().at((-6, 0)).label("received RF", loc="left")
elm.Block().at((-2, 0)).label("LNA\nHEMT", loc="top")
elm.Arrow().at((0, 0)).to((2, 0)).label("amplify", loc="top")
elm.Diode().right().at((2, 0)).label("Schottky\nmixer/detector", loc="top")
elm.Arrow().at((5, 0)).to((7, 0)).label("IF/baseband", loc="top")
elm.Block().at((8, 0)).label("receiver output", loc="right")
elm.Block().at((2, -2)).label("varactor\nvoltage-variable C", loc="bottom")
elm.Arrow().at((2, -2)).to((2, 0)).label("tune", loc="right")
elm.Block().at((8, -2)).label("HEMT: very low noise\nfast diode: high frequency", loc="bottom")
```
