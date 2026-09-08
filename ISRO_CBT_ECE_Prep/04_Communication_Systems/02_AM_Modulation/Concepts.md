# AM Modulation - Concepts

## Standard AM (Amplitude Modulation)
- Carrier amplitude varied in proportion to modulating signal
- Carrier frequency remains constant
- s(t) = Ac[1 + mu*cos(2*pi*fm*t)]*cos(2*pi*fc*t)

### Components:
1. **Carrier:** at frequency fc, amplitude Ac
2. **Lower Sideband (LSB):** at fc - fm
3. **Upper Sideband (USB):** at fc + fm

## Modulation Index (mu)
- mu = Am/Ac (ratio of modulating amplitude to carrier amplitude)
- mu = (Vmax - Vmin)/(Vmax + Vmin) (from waveform measurement)
- Valid range: 0 <= mu <= 1
- mu > 1 = over-modulation (envelope distortion)

## Power Relations
```
Ptotal = Pc(1 + mu^2/2)
Pc = Ac^2/2 (carrier power in load R)
PUSB = PLSB = Pc*mu^2/4 (each sideband)
Psb = Pc*mu^2/2 (total sideband power)
Efficiency: eta = Psideband/Ptotal = mu^2/(2+mu^2)
Max efficiency (mu=1): 33.3%
```

## AM Variants

### DSB-SC (Double Sideband Suppressed Carrier)
- Carrier suppressed (efficiency 100%)
- s(t) = Ac*m(t)*cos(2*pi*fc*t)
- Bandwidth: 2*fm (same as AM)
- Requires coherent detection

### SSB (Single Sideband)
- Only one sideband transmitted
- Bandwidth: fm (half of AM)
- Maximum power efficiency
- Requires coherent detection
- Used in HF communication

### VSB (Vestigial Sideband)
- Compromise between SSB and DSB
- Almost full bandwidth efficiency
- Used in TV broadcasting

## ISRO Key Points
- mu = (Vmax-Vmin)/(Vmax+Vmin) - often tested
- Ptotal = Pc(1+mu^2/2) - most tested formula
- Multi-tone: mu_eff = sqrt(mu1^2+mu2^2+...)
- SSB saves bandwidth (fm vs 2*fm)
- AM receiver uses envelope detector
