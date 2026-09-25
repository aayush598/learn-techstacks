# Circuit Diagrams

## 1. DC Motor Armature Chopper

The chopper controls average armature voltage and therefore motor speed. The freewheel diode carries armature current when the main switch is off.

```circuit
elm.SourceV().up().at((-4, -2)).label("V_dc", loc="left")
elm.Switch().right().at((-4, 1)).label("Q1", loc="top")
elm.Dot().at((-2, 1)).label("armature node", loc="top")
elm.Inductor().right().at((-2, 1)).label("L_a", loc="top")
elm.Motor().right().at((1, 1)).label("M armature", loc="bottom")
elm.Line().right(1).at((4, 1))
elm.Diode().down().at((-2, 0)).label("freewheel D", loc="right")
elm.Line().down(1).at((-2, 0))
elm.Line().left(2).at((-2, -2)).to((-4, -2))
elm.Line().down(3).at((4, -2))
elm.Line().left(8).at((4, -2)).to((-4, -2))
```

## 2. DC Motor H-Bridge Drive

The two bridge legs select forward or reverse armature voltage. Reversing the voltage can command braking before the current has decayed to zero.

```circuit
elm.SourceV().up().at((-5, 0)).label("V_bus", loc="left")
elm.Line().up(3).at((-5, 3))
elm.Line().right(8).at((-5, 3)).label("DC +", loc="top")
elm.Line().right(8).at((-5, -3)).label("DC -", loc="bottom")
elm.Switch().down().at((-2, 3)).label("Q1", loc="right")
elm.Switch().down().at((-2, 0)).label("Q2", loc="right")
elm.Dot().at((-2, 0)).label("A", loc="left")
elm.Switch().down().at((3, 3)).label("Q3", loc="right")
elm.Switch().down().at((3, 0)).label("Q4", loc="right")
elm.Dot().at((3, 0)).label("B", loc="right")
elm.Motor().right().at((-1, 0)).label("M", loc="bottom")
elm.Line().right(2).at((3, 0)).to((2, 0))
elm.Line().right(1).at((-5, -3))
```

## 3. Regenerative Braking of a DC Motor

When the motor emf exceeds the bus voltage, controlled switching sends armature energy back into the source or a recovered bus capacitor. The direction of power flow is opposite to motoring.

```circuit
elm.SourceV().up().at((-4, 0)).label("DC bus", loc="left")
elm.Inductor().right().at((-4, 3)).label("L_a", loc="top")
elm.Motor().right().at((-1, 3)).label("M", loc="bottom")
elm.Line().right(2).at((2, 3))
elm.Switch().left().at((2, 3)).label("regen switch", loc="bottom")
elm.Diode().up().at((-1, 1)).label("return D", loc="right")
elm.Line().up(1).at((-1, 1)).to((-1, 3))
elm.Line().left(3).at((-1, 1)).to((-4, 1))
elm.Line().up(1).at((-4, 1)).to((-4, 0))
elm.Line().down(3).at((2, 0))
elm.Line().left(6).at((2, 0)).to((-4, 0))
elm.Arrow().right().at((3, 1)).to((6, 1)).label("energy to bus", loc="top")
```

## 4. BLDC Three-Phase Commutation

Hall or sensorless position information selects the active bridge state that keeps the rotor and stator fields nearly perpendicular. The sequence produces torque in the commanded direction.

```circuit
elm.Line().right(2).at((-5, 0)).label("rotor position", loc="left")
elm.Arrow().right().at((-3, 0)).to((-1, 0)).label("commutation table", loc="top")
elm.Dot().at((-1, 0)).label("six-step sequence", loc="top")
elm.Arrow().right().at((-1, 0)).to((1, 0)).label("select Q1 to Q6", loc="top")
elm.Arrow().right().at((1, 0)).to((3, 0)).label("three-phase bridge", loc="top")
elm.Line().down(2).at((3, 0))
elm.Line().left(8).at((3, -2)).to((-5, -2))
elm.Line().up(2).at((-5, -2)).to((-5, 0))
elm.Dot().at((3, 0)).label("rotating field", loc="right")
```

## 5. Induction-Motor V/f Control

The stator frequency is ramped with voltage so the air-gap flux remains approximately constant below base speed. Above base speed, voltage is held and frequency is increased separately.

```circuit
elm.SourceV().up().at((-5, 0)).label("speed command", loc="left")
elm.Arrow().right().at((-3, 0)).to((-1, 0)).label("ramp", loc="top")
elm.Arrow().right().at((-1, 0)).to((1, 0)).label("V/f law", loc="top")
elm.Dot().at((1, 0)).label("f_s", loc="top")
elm.Arrow().right().at((1, 0)).to((3, 0)).label("PWM inverter", loc="top")
elm.Arrow().right().at((3, 0)).to((5, 0)).label("stator flux", loc="top")
elm.Line().down(2).at((5, 0))
elm.Line().left(10).at((5, -2)).to((-5, -2))
elm.Line().up(2).at((-5, -2)).to((-5, 0))
```

## 6. Field-Oriented Vector Control

Measured currents are transformed into rotating-frame components. A current regulator then produces voltage commands for the inverter using inverse transforms and the rotor angle.

```circuit
elm.Line().right(1).at((-6, 1)).label("i_abc")
elm.Line().right(1).at((-6, -1)).label("theta_e")
elm.Arrow().right().at((-4, 1)).to((-2, 1)).label("Clarke and Park", loc="top")
elm.Dot().at((-2, 1)).label("i_d, i_q", loc="top")
elm.Arrow().right().at((-2, 1)).to((0, 1)).label("current PI", loc="top")
elm.Dot().at((0, 1)).label("v_d, v_q", loc="top")
elm.Arrow().right().at((0, 1)).to((2, 1)).label("inverse Park", loc="top")
elm.Arrow().right().at((2, 1)).to((4, 1)).label("PWM", loc="top")
elm.Line().up(1).at((-2, 1)).to((-2, 0))
elm.Line().right(2).at((-4, -1)).to((-2, -1))
elm.Line().up(1).at((-2, -1)).to((-2, 0))
```

## 7. Four-Phase Unipolar Stepper Drive

Two windings are energized in sequence. Energizing one phase at a time produces small stable steps, while two phases can be energized for more torque.

```circuit
elm.SourceV().up().at((-5, -2)).label("V_motor", loc="left")
elm.Line().up(1).at((-5, -1)).dot()
elm.Switch().right().at((-5, -1)).label("A+", loc="top")
elm.Inductor().right().at((-3, -1)).label("phase A", loc="top")
elm.Switch().right().at((-1, -1)).label("B+", loc="top")
elm.Inductor().right().at((1, -1)).label("phase B", loc="top")
elm.Line().right(2).at((3, -1)).label("unipolar sequence", loc="right")
elm.Switch().left().at((-5, -1)).label("A-", loc="bottom")
elm.Switch().left().at((-3, -1)).label("B-", loc="bottom")
elm.Line().left(2).at((-5, -1)).to((-7, -1))
elm.Line().down(1).at((-7, -1)).to((-7, -2))
elm.Line().right(2).at((-7, -2)).to((-5, -2))
```

## 8. Dynamic Braking Resistor

When the drive disconnects the motor from the power stage, the motor's kinetic energy produces a voltage across the windings. A resistor and braking chopper dissipate that energy in a controlled way.

```circuit
elm.SourceSin().up().at((-4, 0)).label("motor emf", loc="left")
elm.Line().up(1).at((-4, 1))
elm.Line().right(2).at((-2, 1))
elm.Switch().right().at((-2, 1)).label("brake chopper", loc="top")
elm.Line().right(1).at((0, 1))
elm.Dot().at((1, 1)).label("DC link", loc="top")
elm.Resistor().down().at((1, 1)).label("R_brake", loc="right")
elm.Line().down(3).at((1, -2))
elm.Line().left(5).at((1, -2)).to((-4, -2))
elm.Line().up(2).at((-4, -2)).to((-4, 0))
elm.Capacitor().down().at((3, 1)).label("C_dc", loc="right")
elm.Line().down(3).at((3, -2))
elm.Line().left(2).at((1, -2)).to((3, -2))
```

