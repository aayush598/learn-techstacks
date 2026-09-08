# Microwave Passive Components - Quick Reference

## Directional Coupler (4-port)
```
Coupling = 10 log10(P_in/P_coupled)
Directivity = 10 log10(P_coupled_reverse/P_coupled_forward_iso)
Isolation = Coupling + Directivity
Ideal: infinite directivity
It couples forward power; reverse isolated
```

## Circulator (3-port)
```
Scattering:
  Port1->2, Port2->3, Port3->1 (transmit)
  Reverse path isolated
  S21 (1->2) = 1, S12 = 0 (nonreciprocal)
Used as duplexer: TX amp -> antenna -> RX (isolation)
```

## Isolator (2-port)
```
S21 = 1 (forward pass), S12 = 0 (reverse absorbed)
Protects source: reflected power from load absorbed at isolator input
Nonreciprocal (ferrite)
```

## Magic Tee (4-port)
```
Ports: E-arm (sum), H-arm (sum), two side arms
S-parameter properties: some ports isolated (0 coupling)
Splits/combines; E and H arms isolated from each other
```

## E/H Tees
```
E-plane tee: series tee (side arm in E plane)
H-plane tee: shunt (side arm in H plane)
Power splits: in -> two equal halves (ideally)
```

## Cavity Resonator
```
Resonant frequency by dimensions
Q factor: high (thousands) for lossless walls
Used in: filters, oscillators (frequency selection)
lambda/2 guide section resonant
```

## Attenuator
```
Pad / loss element (resistive)
dB attenuation = 20 log10(V_in/V_out) (voltage) 
Fixed/variable
```

## Phase shifter
```
Phase shift = beta * length
Ferrite or mechanical type
```

## S-parameter summary table
| Device | Key S |
|--------|-------|
| Isolator | S21=1, S12=0 |
| Circulator | S21=1, S32=1, S13=1 |
| Tee | splits S_j1 ~ -3dB |
| Coupler | coupling <=0dB, iso≈0 |
| Attenuator | S21 = -Atten(dB) |
| Phase shifter | S21 = e^(j phi) |
