# Signals Classification — Circuit Diagrams

## 1. Energy and Power Measurement

- Integrate the squared signal to obtain total energy; a symmetric long-time average gives power.
- A finite-energy pulse has zero long-term power, while a periodic sinusoid has finite average power and infinite total energy.

```circuit
elm.SourceSin().right().label('x(t)')
elm.Line().right()
elm.Block().right().label('Square and integrate\nE = ∫ |x(t)|² dt')
elm.Line().right()
elm.Block().right().label('Energy signal\nE finite, P = 0')

elm.SourceSin().right().label('periodic x(t)')
elm.Line().right()
elm.Block().right().label('Long-time average\nP = lim (1/2T) ∫ |x(t)|² dt')
elm.Line().right()
elm.Block().right().label('Power signal\nP finite, E infinite')
```

## 2. Even–Odd Decomposition

- Delay the original signal to form x(-t), then add and subtract the two versions.
- The even and odd outputs recombine exactly as x(t) = xₑ(t) + xₒ(t).

```circuit
source = elm.SourceSin()
source.label('x(t)')
elm.Line().at(source).right()

reflected = elm.Block()
reflected.label('Time reversal\nx(-t)')
elm.Line().at(reflected).right()

adder = elm.Block()
adder.label('Add and scale\n[x(t)+x(-t)]/2')
elm.Line().at(adder).right()
elm.Block().label('Even part xₑ(t)')

subtractor = elm.Block()
subtractor.label('Subtract and scale\n[x(t)-x(-t)]/2')
elm.Line().at(subtractor).right()
elm.Block().label('Odd part xₒ(t)')

reconstructor = elm.Block()
reconstructor.label('xₑ(t) + xₒ(t) = x(t)')
```

## 3. Baseband-to-Bandpass Conversion

- Multiply in-phase and quadrature baseband components by orthogonal carrier branches.
- Adding the branches gives the real passband signal; the I/Q pair is its complex envelope.

```circuit
in_phase = elm.SourceSin()
in_phase.label('I(t) = gᵢ(t)')
quadrature = elm.SourceSin()
quadrature.label('Q(t) = g_q(t)')

elm.Line().at(in_phase).right()
elm.Block().label('× cos(2πf_c t)')
elm.Line().right()

elm.Line().at(quadrature).down()
elm.Block().label('× sin(2πf_c t)')
elm.Line().right()

elm.Block().label('Add branches')
elm.Line().right()
elm.Block().label('s(t) = Re{g(t)eʲ²πf_ct}')

carrier = elm.SourceSin()
carrier.label('Local carrier / quadrature oscillator')
elm.Line().at(carrier).down()
```

## 4. Periodic Signal Analysis Path

- A repeating waveform is represented by its fundamental period and Fourier-series harmonics.
- An aperiodic finite-duration signal instead uses the continuous Fourier transform.

```circuit
elm.SourceSin().right().label('periodic x(t)')
elm.Line().right()
elm.Block().right().label('Find smallest T₀\nx(t)=x(t+T₀)')
elm.Line().right()
elm.Block().right().label('Fourier series\na₀ + Σ aₖ cos + Σ bₖ sin')
elm.Line().right()
elm.Block().right().label('Discrete line spectrum\nk/T₀')

elm.SourceSin().down().label('aperiodic pulse x(t)')
elm.Line().down()
elm.Block().label('Fourier transform\nX(f) = ∫ x(t)e⁻ʲ²πft dt')
```
