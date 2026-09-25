# Circuit Diagrams

## 1. Four-Port Directional Coupler

A directional coupler samples forward power in the coupled port while the through port carries the main signal. The isolated port suppresses reverse-wave leakage and quantifies directivity.

```circuit
elm.SourceI().right().at((-6, 1)).label("input", loc="left")
elm.Block().at((-2, 1)).label("main guide", loc="top")
elm.Arrow().at((0, 1)).to((2, 1)).label("through", loc="top")
elm.Resistor().right().at((2, 1)).label("through port", loc="bottom")
elm.Arrow().at((0, 1)).to((0, -1)).label("coupling", loc="right")
elm.Resistor().down().at((0, -1)).label("coupled port", loc="right")
elm.Arrow().at((0, 1)).to((-2, -3)).label("reverse isolation", loc="bottom")
elm.Resistor().down().at((-2, -3)).label("isolated port", loc="right")
elm.Block().at((5, -1)).label("C = 10log10(Pin/Pc)\nD = isolation of reverse wave", loc="right")
```

## 2. Three-Port Circulator

A circulator routes power from port 1 to port 2, port 2 to port 3, and port 3 back to port 1. The ferrite device is nonreciprocal, so the reverse path is not simply the transpose.

```circuit
elm.SourceI().right().at((-6, 0)).label("port 1 input", loc="left")
elm.Block().at((-2, 0)).label("ferrite\ncirculator", loc="top")
elm.Arrow().at((0, 0)).to((3, 0)).label("1 → 2", loc="top")
elm.Resistor().right().at((3, 0)).label("port 2", loc="bottom")
elm.Arrow().at((3, 0)).to((3, -2)).label("2 → 3", loc="right")
elm.Resistor().down().at((3, -2)).label("port 3", loc="right")
elm.Arrow().at((0, 0)).to((0, -2)).label("3 → 1", loc="right")
elm.Block().at((-2, -2)).label("clockwise power flow\nS21=1, S32=1, S13=1", loc="bottom")
```

## 3. Isolator and Radar Duplexer Path

An isolator protects a source by passing transmit power forward and absorbing the reverse wave. In a radar, a circulator can perform the same transmit/receive separation at a shared antenna.

```circuit
elm.SourceV().up().at((-6, 0)).label("TX amplifier", loc="left")
elm.Arrow().at((-3, 3)).to((0, 3)).label("forward power", loc="top")
elm.Block().at((1, 3)).label("isolator or\ncirculator", loc="top")
elm.Arrow().at((4, 3)).to((7, 3)).label("antenna path", loc="top")
elm.Block().at((8, 3)).label("antenna", loc="right")
elm.Arrow().at((8, 3)).to((4, 0)).label("echo returns", loc="right")
elm.Block().at((1, 0)).label("reverse energy\nabsorbed / routed", loc="bottom")
elm.Arrow().at((0, 0)).to((-3, 0)).label("RX receiver", loc="top")
elm.Block().at((-5, 0)).label("source protected\nS12=0", loc="left")
```

## 4. Magic Tee and E/H-Arm Combining

The magic tee combines the E-plane and H-plane arms. A signal entering one arm divides between the side arms; signals entering the two arms can be summed or differenced.

```circuit
elm.Block().at((-5, 1)).label("E-arm input", loc="top")
elm.Block().at((-5, -1)).label("H-arm input", loc="bottom")
elm.Arrow().at((-2, 1)).to((0, 1)).label("E contribution", loc="top")
elm.Arrow().at((-2, -1)).to((0, -1)).label("H contribution", loc="top")
elm.Dot().at((1, 0)).label("magic tee", loc="top")
elm.Arrow().at((1, 1)).to((4, 1)).label("side arm 1", loc="top")
elm.Arrow().at((1, -1)).to((4, -1)).label("side arm 2", loc="top")
elm.Block().at((5, 0)).label("sum / difference\npower combiner", loc="right")
elm.Block().at((1, 0)).label("E and H arms\nisolated in ideal tee", loc="bottom")
```

## 5. Attenuator, Phase Shifter, and Matched Termination

An attenuator reduces power with a calibrated resistive loss. A phase shifter adds a controlled electrical length, and a matched termination absorbs incident power without reflection.

```circuit
elm.SourceI().right().at((-6, 1)).label("RF input", loc="left")
elm.Block().at((-2, 1)).label("attenuator\nA dB", loc="top")
elm.Arrow().at((0, 1)).to((2, 1)).label("reduced power", loc="top")
elm.Block().at((3, 1)).label("phase shifter\nβl", loc="top")
elm.Arrow().at((5, 1)).to((7, 1)).label("phase-shifted wave", loc="top")
elm.Resistor().right().at((7, 1)).label("matched load", loc="bottom")
elm.Block().at((1, -2)).label("S21 = -A dB", loc="bottom")
elm.Block().at((4, -2)).label("S21 = e^(jφ)", loc="bottom")
elm.Block().at((7, -2)).label("Z₀ termination\nΓ=0", loc="bottom")
```

## 6. Cavity Resonator and Coupling

A shorted waveguide section forms a high-Q resonant cavity. Coupling into and out of the cavity transfers energy while the resonator selects the operating band.

```circuit
elm.SourceI().right().at((-6, 0)).label("input coupling", loc="left")
elm.Block().at((-2, 0)).label("guide cavity\nresonant length", loc="top")
elm.Dot().at((0, 0)).label("energy storage", loc="top")
elm.Arrow().at((0, 0)).to((3, 0)).label("coupled output", loc="top")
elm.Resistor().right().at((3, 0)).label("load", loc="bottom")
elm.Line().right(2).at((0, -2)).to((5, -2))
elm.Line().up(2).at((5, -2)).to((5, 0))
elm.Block().at((1, -2)).label("short / boundary\nhigh-Q filter", loc="bottom")
elm.Block().at((7, 0)).label("f₀ by dimensions", loc="right")
```
