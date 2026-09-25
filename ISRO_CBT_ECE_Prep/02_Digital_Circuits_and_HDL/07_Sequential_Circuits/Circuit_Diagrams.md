# Sequential Circuits — Circuit Diagrams

## 1. SR Flip-Flop State Control

An SR storage element holds its state when both inputs are low, sets on `S=1,R=0`, and resets on `S=0,R=1`. The forbidden `S=R=1` case must be avoided.

```circuit
s = elm.SourceI().right().at((-8, 1)).label('S')
r = elm.SourceI().right().at((-8, -1)).label('R')
clock = elm.SourceI().right().at((-8, 4)).label('clock edge')
storage = elm.Block().at((-3, 0)).label('SR storage element\nQ⁺ = S + R\'Q')
q = elm.SourceI().right().at((3, 1)).label('Q')
qbar = elm.SourceI().right().at((3, -1)).label('Q\' output')
invalid = elm.Block().at((0, 4)).label('S=R=1: forbidden')
elm.Line().right().at(s).to(storage)
elm.Line().right().at(r).to(storage)
elm.Line().up().at((-5, 0)).to((-5, 4))
elm.Line().right().at(clock)
elm.Line().right().at(storage)
elm.Line().right().at(q)
elm.Line().down().at((1, 0)).to((1, -1))
elm.Line().right().at(qbar)
elm.Line().right().at(clock).to(invalid)
```

## 2. JK Flip-Flop

JK removes the SR forbidden state by defining `J=K=1` as toggle. Its characteristic equation is `Q⁺ = JQ' + K'Q`.

```circuit
j = elm.SourceI().right().at((-8, 1)).label('J')
k = elm.SourceI().right().at((-8, -1)).label('K')
clock = elm.SourceI().right().at((-8, 4)).label('clock edge')
jk = elm.Block().at((-3, 0)).label('JK flip-flop\nJ,K=11 → Q toggles')
q = elm.SourceI().right().at((3, 0)).label('Q')
elm.Line().right().at(j).to(jk)
elm.Line().right().at(k).to(jk)
elm.Line().up().at((-5, 0)).to((-5, 4))
elm.Line().right().at(clock)
elm.Line().right().at(jk)
elm.Line().right().at(q)
```

## 3. D Flip-Flop Register Element

A positive-edge D flip-flop samples `D` only at the active clock edge, making it the usual one-bit register and counter storage element.

```circuit
d = elm.SourceI().right().at((-8, 1)).label('D')
clock = elm.SourceI().right().at((-8, -1)).label('CLK')
dff = elm.Block().at((-3, 0)).label('positive-edge D flip-flop\nQ⁺ = D')
q = elm.SourceI().right().at((3, 0)).label('Q')
qbar = elm.SourceI().right().at((3, 3)).label('complement output')
elm.Line().right().at(d).to(dff)
elm.Line().right().at(clock).to(dff)
elm.Line().right().at(dff)
elm.Line().right().at(q)
elm.Line().up().at((1, 0)).to((1, 3))
elm.Line().right().at(qbar)
```

## 4. T Flip-Flop and Frequency Division

Holding `T=1` makes every active edge toggle `Q`. One toggle stage divides frequency by two; cascaded stages divide by `2ⁿ`.

```circuit
t = elm.SourceI().right().at((-9, 1)).label('T = 1')
clock = elm.SourceI().right().at((-9, -1)).label('input clock')
tff = elm.Block().at((-4, 0)).label('T flip-flop\nQ⁺ = T ⊕ Q')
q1 = elm.SourceI().right().at((1, 1)).label('fclk / 2')
clock2 = elm.SourceI().right().at((1, -2)).label('fclk / 2')
tff2 = elm.Block().at((5, 0)).label('second T flip-flop')
q2 = elm.SourceI().right().at((9, 0)).label('fclk / 4')
elm.Line().right().at(t).to(tff)
elm.Line().right().at(clock).to(tff)
elm.Line().right().at(tff).to(q1)
elm.Line().down().at((-2, 0)).to((-2, -2))
elm.Line().right().at(clock2).to(tff2)
elm.Line().right().at(tff2)
elm.Line().right().at(q2)
```

## 5. Master–Slave Edge-Triggered Register

The master latch accepts data during one clock phase and the slave updates during the opposite phase. Two opposite-polarity latches isolate the storage node and prevent race-through.

```circuit
d = elm.SourceI().right().at((-10, 1)).label('D')
clock = elm.SourceI().right().at((-10, -2)).label('clock')
master = elm.Block().at((-5, 1)).label('master latch\ntransparent on φ1')
slave = elm.Block().at((1, 1)).label('slave latch\ntransparent on φ2')
q = elm.SourceI().right().at((7, 1)).label('Q')
complement = elm.Block().at((7, -2)).label("Q'")
elm.Line().right().at(d).to(master)
elm.Line().right().at(clock).to(master)
elm.Line().right().at(master).to(slave)
elm.Line().down().at((-2, 1)).to((-2, -2))
elm.Line().right().at(clock)
elm.Line().right().at(slave).to(q)
elm.Line().right().at(slave).to(complement)
```

## 6. Flip-Flop Type Conversions

The characteristic equations allow equivalent input logic. A D flip-flop is a JK flip-flop with `J=D` and `K=D'`, while a D-to-T conversion uses `T=D⊕Q`.

```circuit
d = elm.SourceI().right().at((-9, 1)).label('D')
q_feedback = elm.SourceI().right().at((-9, -2)).label('Q feedback')
not_d = elm.NotGate().at((-5, 1)).label("D'")
jk_equiv = elm.Block().at((-1, 1)).label('D flip-flop as JK\nJ=D, K=D\'')
d_to_t = elm.Block().at((4, -2)).label('D-to-T\nT = D ⊕ Q')
t_to_d = elm.Block().at((8, -2)).label('T-to-D\nD = T ⊕ Q')
elm.Line().right().at(d).to(not_d)
elm.Line().right().at(d).to(jk_equiv)
elm.Line().right().at(not_d).to(jk_equiv)
elm.Line().right().at(jk_equiv)
elm.Line().right().at(d).to(d_to_t)
elm.Line().right().at(q_feedback).to(d_to_t)
elm.Line().right().at(d_to_t).to(t_to_d)
```

## 7. Excitation-Table Signal Flow

For a required transition of `Q`, the excitation table identifies the input values required by D, T, SR, and JK storage elements. Unknown entries are don't-cares that can be optimized in a state-assignment design.

```circuit
transition = elm.SourceI().right().at((-9, 0)).label('required Q → Q⁺')
table = elm.Block().at((-4, 0)).label('excitation table\n0→0, 0→1, 1→0, 1→1')
d_input = elm.Block().at((1, 3)).label('D = Q⁺')
t_input = elm.Block().at((1, 1)).label('T = Q ⊕ Q⁺')
sr_input = elm.Block().at((1, -1)).label('S,R values')
jk_input = elm.Block().at((1, -3)).label('J,K values')
elm.Line().right().at(transition).to(table)
elm.Line().right().at(table)
elm.Line().up().at((-2, 0)).to((-2, 3))
elm.Line().right().at(d_input)
elm.Line().down().at((-2, 3)).to((-2, 1))
elm.Line().right().at(t_input)
elm.Line().down().at((-2, 1)).to((-2, -1))
elm.Line().right().at(sr_input)
elm.Line().down().at((-2, -1)).to((-2, -3))
elm.Line().right().at(jk_input)
```

## 8. Setup and Hold Timing Window

Data must be stable for the setup interval before the active edge and for the hold interval after it. A transition inside the forbidden aperture can make the sampled state unpredictable and lead to metastability.

```circuit
clock = elm.SourceSin().right().at((-9, 0)).label('clock')
data = elm.SourceSin().right().at((-9, 3)).label('data')
edge = elm.Arrow().up().at((-2, 0)).to((-2, 3)).label('active edge')
setup = elm.Block().at((2, -2)).label('stable before edge\nTsetup')
hold = elm.Block().at((5, -2)).label('stable after edge\nThold')
violation = elm.Block().at((8, 1)).label('unstable aperture\nmetastability risk')
elm.Line().right().at(clock)
elm.Line().right().at(data)
elm.Line().right().at(edge)
elm.Line().right().at(setup)
elm.Line().right().at(hold)
elm.Line().right().at(violation)
```
