# Electronic Devices - Complete Formula Sheet

## Semiconductor Physics
```
Mass action law: n*p = ni^2
Conductivity: sigma = q*(n*mun + p*mup)
Intrinsic carrier concentration: ni = sqrt(Nc*Nv)*exp(-Eg/(2kT))
Fermi level (n-type): Ef = Ec - kT*ln(Nc/ND)
Fermi level (p-type): Ef = Ev + kT*ln(Nv/NA)
```

## PN Junction
```
Built-in potential: Vbi = (kT/q)*ln(NA*ND/ni^2)
At room temp: kT/q = 0.026V = 26mV
Depletion width: W = sqrt(2*epsilon*(Vbi-Vr)*(1/NA+1/ND)/q)
Junction capacitance: Cj = epsilon*A/W
Ideal diode: I = Is*(e^(V/Vt) - 1)
```

## BJT
```
Ic = beta*Ib = alpha*Ie
Ie = (beta+1)*Ib
beta = alpha/(1-alpha), alpha = beta/(beta+1)
gm = Ic/Vt = Ic/0.026
rpi = beta/gm = Vt/Ib
ro = Va/Ic (Early voltage Va = 50-100V)
re = Vt/Ie = alpha/gm
```

## MOSFET
```
Linear region: Id = kn*((Vgs-Vt)*Vds - Vds^2/2)*(1+lambda*Vds)
Saturation: Id = (kn/2)*(Vgs-Vt)^2*(1+lambda*Vds)
  Valid when Vds >= Vgs - Vt

Transconductance: gm = kn*(Vgs-Vt) = sqrt(2*kn*Id)
Output resistance: rds = 1/(lambda*Id)
Threshold voltage: Vt = Vt0 + gamma*(sqrt(2*phi_f+Vsb) - sqrt(2*phi_f))
```

## Small Signal Models
```
BJT hybrid-pi:
  gm = Ic/Vt, rpi = beta/gm, ro = Va/Ic
  Input: between B and E (rpi)
  Output: between C and E (ro)
  Current source: gm*Vbe

MOSFET:
  gm = sqrt(2*kn*Id), rds = 1/(lambda*Id)
  Current source: gm*Vgs
```

## Diode Special Types
```
Zener: Vz = constant in breakdown
Tunnel: negative resistance region
Varactor: Cj = Cj0/sqrt(1+Vr/Vbi)
Schottky: lower Vf (0.2-0.3V), faster switching
```

## Bandgap Reference
```
Vref = Vbe + (delta_Vbe)*(R2/R1)
Temperature coefficient of Vbe: approximately -2 mV/degree C
Bandgap: Eg = 1.12 eV (silicon)
```

## Carrier Mobility
```
Drift velocity: vd = mu*E
Mobility: mu = q*tau/m* (tau = mean free time)
Saturation velocity: vsat = mu*Esat
Scattering: lattice (decreases with T), ionized impurity (increases with T)
```
