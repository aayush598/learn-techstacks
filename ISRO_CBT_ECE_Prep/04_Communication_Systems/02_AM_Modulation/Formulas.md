# AM Modulation - Formulas

## Standard AM Signal
```
s(t) = Ac[1 + mu*cos(2*pi*fm*t)]*cos(2*pi*fc*t)
s(t) = Ac*cos(2*pi*fc*t) + (mu*Ac/2)*cos(2*pi*(fc+fm)t) + (mu*Ac/2)*cos(2*pi*(fc-fm)t)
      [Carrier]          [USB]                           [LSB]
```

## Modulation Index
```
mu = Am/Ac
mu = (Vmax - Vmin)/(Vmax + Vmin)
From power: mu = sqrt(2*(Ptotal/Pc - 1))
```

## Power Formulas (Load = R)
```
Pc = Ac^2/(2R)     [carrier power]
PUSB = PLSB = Pc*mu^2/4
Psb = Pc*mu^2/2
Ptotal = Pc(1 + mu^2/2) = Pc + Psb

Efficiency: eta = Psb/Ptotal = mu^2/(2+mu^2)
For mu = 1: eta = 1/3 = 33.3%
```

## Multi-Tone AM
```
Effective modulation index: mu_total = sqrt(mu1^2 + mu2^2 + ... + mun^2)
Total bandwith: BW = 2*fm_max (depends on highest frequency)
```

## Bandwidth
```
AM (Standard or DSB-SC): BW = 2*fm
SSB: BW = fm
VSB: BW = fm + (bandwidth of vestige)
```

## Detection Methods
```
Envelope detector (AM): Simple, uses diode + RC filter
  Condition: 1/wc << RC << 1/wm
  RC time constant must be small enough to follow envelope

Coherent/Synchronous detection (DSB-SC, SSB):
  Requires locally generated carrier
  Output: (1/2)*Ac*m(t)
```

## Quick Reference
| Parameter | Formula | Notes |
|-----------|---------|-------|
| mu | (Vmax-Vmin)/(Vmax+Vmin) | 0<=mu<=1 |
| Ptotal | Pc(1+mu^2/2) | Tested often |
| Efficiency | mu^2/(2+mu^2) | Max 33.3% |
| BW (AM) | 2*fm | Highest fm |
| BW (SSB) | fm | Half of AM |
| DSB-SC | 100% efficient | Needs coherent |
