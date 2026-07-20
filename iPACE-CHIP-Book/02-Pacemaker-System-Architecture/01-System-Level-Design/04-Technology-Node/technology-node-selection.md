# Technology Node Selection

## 2.1.4 iPACE-CHIP Process Technology Selection

### 2.1.4.1 Process Node Comparison

The selection of semiconductor process technology for an implantable pacemaker SoC
involves balancing multiple competing requirements: reliability, power consumption,
analog performance, cost, and long-term availability. This section provides a
comprehensive comparison of available process nodes.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    TECHNOLOGY NODE COMPARISON MATRIX                         │
│                                                                             │
│  ┌─────────────┬───────────┬───────────┬───────────┬───────────┬─────────┐│
│  │ Parameter   │ 180nm     │ 130nm     │ 90nm      │ 65nm      │ 40nm    ││
│  ├─────────────┼───────────┼───────────┼───────────┼───────────┼─────────┤│
│  │ Min Gate    │ 180nm     │ 130nm     │ 90nm      │ 65nm      │ 40nm    ││
│  │ Length      │           │           │           │           │         ││
│  ├─────────────┼───────────┼───────────┼───────────┼───────────┼─────────┤│
│  │ Vdd (nom)   │ 1.8V      │ 1.2V      │ 1.0V      │ 1.0V      │ 0.9V    ││
│  ├─────────────┼───────────┼───────────┼───────────┼───────────┼─────────┤│
│  │ Vdd (I/O)   │ 3.3V/5V   │ 2.5V/3.3V │ 2.5V      │ 1.8V/2.5V │ 1.8V    ││
│  ├─────────────┼───────────┼───────────┼───────────┼───────────┼─────────┤│
│  │ Gate Delay  │ ~20ps     │ ~14ps     │ ~10ps     │ ~7ps      │ ~5ps    ││
│  │ (FO4)       │           │           │           │           │         ││
│  ├─────────────┼───────────┼───────────┼───────────┼───────────┼─────────┤│
│  │ Transistor  │ ~50K/µm²  │ ~90K/µm²  │ ~180K/µm² │ ~360K/µm² │ ~800K/µm²│
│  │ Density     │           │           │           │           │         ││
│  ├─────────────┼───────────┼───────────┼───────────┼───────────┼─────────┤│
│  │ SRAM Bit    │ ~0.5µm²   │ ~0.28µm²  │ ~0.15µm²  │ ~0.09µm²  │ ~0.05µm²│
│  │ Cell Area   │           │           │           │           │         ││
│  ├─────────────┼───────────┼───────────┼───────────┼───────────┼─────────┤│
│  │ Metal       │ 6 layers  │ 6-8 layers│ 8 layers  │ 8-10 layers│ 10+     ││
│  │ Layers      │ Al        │ Al/Cu     │ Cu        │ Cu/Low-k  │ Cu/ULK  ││
│  ├─────────────┼───────────┼───────────┼───────────┼───────────┼─────────┤│
│  │ Interconnect│ ~0.35µm   │ ~0.25µm   │ ~0.18µm   │ ~0.13µm   │ ~0.09µm ││
│  │ Pitch (M1)  │           │           │           │           │         ││
│  ├─────────────┼───────────┼───────────┼───────────┼───────────┼─────────┤│
│  │ Die Cost    │ $2-4K     │ $3-6K     │ $5-10K    │ $8-15K    │ $15-30K ││
│  │ (per wafer) │           │           │           │           │         ││
│  ├─────────────┼───────────┼───────────┼───────────┼───────────┼─────────┤│
│  │ NRE Cost    │ $1-2M     │ $2-3M     │ $3-5M     │ $5-8M     │ $8-15M  ││
│  │ (mask set)  │           │           │           │           │         ││
│  ├─────────────┼───────────┼───────────┼───────────┼───────────┼─────────┤│
│  │ Wafer Size  │ 200mm     │ 200/300mm │ 300mm     │ 300mm     │ 300mm   ││
│  ├─────────────┼───────────┼───────────┼───────────┼───────────┼─────────┤│
│  │ Availability│ Mature    │ Mature    │ Mature    │ Available │ Limited ││
│  │             │ (>20yr)   │ (>15yr)   │ (>10yr)   │ (>7yr)    │ (<5yr)  ││
│  ├─────────────┼───────────┼───────────┼───────────┼───────────┼─────────┤│
│  │ Reliability │ Excellent │ Excellent │ Very Good │ Good      │ Fair    ││
│  │ (HTOL)      │           │           │           │           │         ││
│  ├─────────────┼───────────┼───────────┼───────────┼───────────┼─────────┤│
│  │ TID Toler.  │ >300 krad │ >200 krad │ >150 krad │ >100 krad │ ~50 krad││
│  ├─────────────┼───────────┼───────────┼───────────┼───────────┼─────────┤│
│  │ JEDEC Compl.│ Full      │ Full      │ Full      │ Full      │ Partial ││
│  │             │           │           │           │           │         ││
│  └─────────────┴───────────┴───────────┴───────────┴───────────┴─────────┘│
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.1.4.2 Mixed-Signal Performance Comparison

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MIXED-SIGNAL PERFORMANCE COMPARISON                       │
│                                                                             │
│  ┌─────────────────┬───────────┬───────────┬───────────┬───────────┬──────┐│
│  │ Parameter       │ 180nm     │ 130nm     │ 90nm      │ 65nm      │ 40nm ││
│  ├─────────────────┼───────────┼───────────┼───────────┼───────────┼──────┤│
│  │                 │           │           │           │           │      ││
│  │ ANALOG           │           │           │           │           │      ││
│  │ ──────           │           │           │           │           │      ││
│  │ Op-Amp GBW      │ 50 MHz    │ 80 MHz    │ 120 MHz   │ 200 MHz   │300MHz││
│  │ Op-Amp DC Gain  │ >80 dB    │ >80 dB    │ >70 dB    │ >70 dB    │>60 dB││
│  │ Input Offset    │ <1mV      │ <0.5mV    │ <0.5mV    │ <1mV      │<2mV  ││
│  │ 1/f Noise       │ Low       │ Low-Med   │ Medium    │ Med-High  │ High ││
│  │ (corner freq)   │           │           │           │           │      ││
│  │ Matching (σVth) │ ~5mV      │ ~4mV      │ ~3mV      │ ~3mV      │~4mV  ││
│  │ Mismatch        │ Good      │ Good      │ Fair      │ Fair      │ Poor ││
│  │                 │           │           │           │           │      ││
│  │ ADC              │           │           │           │           │      ││
│  │ ───              │           │           │           │           │      ││
│  │ Max ENOB        │ 12-bit    │ 13-bit    │ 14-bit    │ 15-bit    │16-bit││
│  │ @ 1kSPS         │           │           │           │           │      ││
│  │ SAR ADC         │ Optimal   │ Good      │ Good      │ Fair      │ Fair ││
│  │ (area/power)    │           │           │           │           │      ││
│  │ Sigma-Delta     │ Good      │ Good      │ Optimal   │ Optimal   │ Good ││
│  │ ADC             │           │           │           │           │      ││
│  │                 │           │           │           │           │      ││
│  │ DAC              │           │           │           │           │      ││
│  │ ───              │           │           │           │           │      ││
│  │ Resolution      │ 8-10 bit  │ 10-12 bit │ 12-14 bit │ 12-14 bit │14-16 ││
│  │ INL/DNL         │ <±0.5 LSB │ <±0.5 LSB │ <±0.5 LSB │ <±1 LSB  │<±1LSB││
│  │                 │           │           │           │           │      ││
│  │ COMPARATOR      │           │           │           │           │      ││
│  │ ──────────      │           │           │           │           │      ││
│  │ Speed           │ 500 MHz   │ 800 MHz   │ 1.2 GHz   │ 2 GHz     │3 GHz ││
│  │ Offset          │ <2mV      │ <1.5mV    │ <1mV      │ <1mV      │<1.5mV││
│  │                 │           │           │           │           │      ││
│  │ VOLTAGE         │           │           │           │           │      ││
│  │ REFERENCES      │           │           │           │           │      ││
│  │ ───────────     │           │           │           │           │      ││
│  │ Bandgap TC      │ <50ppm/°C │ <40ppm/°C │ <30ppm/°C │ <30ppm/°C │<25   ││
│  │ PSRR            │ >60 dB    │ >60 dB    │ >50 dB    │ >50 dB    │>40 dB││
│  │                 │           │           │           │           │      ││
│  │ SWITCHED-CAP    │           │           │           │           │      ││
│  │ FILTERS         │           │           │           │           │      ││
│  │ ──────────────  │           │           │           │           │      ││
│  │ Max fc          │ 1 MHz     │ 2 MHz     │ 5 MHz     │ 10 MHz    │20 MHz││
│  │ Capacitor dens. │ Good      │ Good      │ Fair      │ Fair      │ Poor ││
│  │                 │           │           │           │           │      ││
│  │ PASSIVE         │           │           │           │           │      ││
│  │ COMPONENTS      │           │           │           │           │      ││
│  │ ────────────    │           │           │           │           │      ││
│  │ Resistor type   │ Poly/HR   │ Poly/HR   │ Poly      │ Poly      │Poly  ││
│  │ Capacitor type  │ MIM/MOS   │ MIM/MOS   │ MIM       │ MIM/MOS   │MIM   ││
│  │ Varactor        │ Available │ Available │ Available │ Limited   │Poor  ││
│  │                 │           │           │           │           │      ││
│  └─────────────────┴───────────┴───────────┴───────────┴───────────┴──────┘│
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.1.4.3 Reliability and Qualification Data

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    RELIABILITY COMPARISON — Medical Device Perspective       │
│                                                                             │
│  ┌─────────────────┬───────────┬───────────┬───────────┬───────────┬──────┐│
│  │ Test            │ 180nm     │ 130nm     │ 90nm      │ 65nm      │ 40nm ││
│  ├─────────────────┼───────────┼───────────┼───────────┼───────────┼──────┤│
│  │ HTOL            │           │           │           │           │      ││
│  │ (1000hr,125°C)  │ <10 FIT   │ <10 FIT   │ <15 FIT   │ <20 FIT   │<30FIT││
│  │                 │           │           │           │           │      ││
│  │ EFR             │           │           │           │           │      ││
│  │ (Early Failure) │ <50 ppm   │ <50 ppm   │ <100 ppm  │ <200 ppm  │<500  ││
│  │                 │           │           │           │           │ppm   ││
│  │                 │           │           │           │           │      ││
│  │ ELFR            │           │           │           │           │      ││
│  │ (Low Failure)   │ <1 ppm    │ <2 ppm    │ <5 ppm    │ <10 ppm   │<25   ││
│  │                 │           │           │           │           │ppm   ││
│  │                 │           │           │           │           │      ││
│  │ TID             │           │           │           │           │      ││
│  │ (Total Ionizing │ >300 krad │ >200 krad │ >150 krad │ >100 krad │>50   ││
│  │  Dose)          │           │           │           │           │krad  ││
│  │                 │           │           │           │           │      ││
│  │ TDDB            │           │           │           │           │      ││
│  │ (Gate Oxide)    │ >20 years │ >20 years │ >15 years │ >10 years │>10yr ││
│  │ @ 125°C         │           │           │           │           │      ││
│  │                 │           │           │           │           │      ││
│  │ EM              │           │           │           │           │      ││
│  │ (Electromigr.)  │ >20 years │ >15 years │ >15 years │ >10 years │>10yr ││
│  │ @ 125°C, MTTF  │           │           │           │           │      ││
│  │                 │           │           │           │           │      ││
│  │ HCI             │           │           │           │           │      ││
│  │ (Hot Carrier)   │ >10 years │ >10 years │ >8 years  │ >5 years  │>5yr  ││
│  │ @ 125°C         │           │           │           │           │      ││
│  │                 │           │           │           │           │      ││
│  │ NBTI            │           │           │           │           │      ││
│  │ (PMOS Aging)    │ Minor     │ Moderate  │ Moderate  │ Significant│Signif││
│  │                 │           │           │           │           │      ││
│  │ SEU             │           │           │           │           │      ││
│  │ (Single Event)  │ Very Low  │ Low       │ Low-Med   │ Medium    │High  ││
│  │                 │           │           │           │           │      ││
│  │ HTOL Qual.      │ Full      │ Full      │ Full      │ Full      │Partial│
│  │ (JEDEC)         │           │           │           │           │      ││
│  │                 │           │           │           │           │      ││
│  │ Qual Samples    │ 231-770   │ 231-770   │ 231-770   │ 231-770   │77+   ││
│  │ (per stress)    │           │           │           │           │      ││
│  │                 │           │           │           │           │      ││
│  │ Acceleration    │ 10-30×    │ 10-30×    │ 10-20×    │ 10-20×    │5-10× ││
│  │ Factor (AF)     │           │           │           │           │      ││
│  │                 │           │           │           │           │      ││
│  └─────────────────┴───────────┴───────────┴───────────┴───────────┴──────┘│
│                                                                             │
│  KEY RELIABILITY CONCERNS BY NODE:                                         │
│  ─────────────────────────────────                                         │
│  180nm: Minimal concerns. Mature, well-characterized. Excellent match       │
│         to medical device reliability requirements. Long-term data          │
│         available (>20 years of production).                               │
│                                                                             │
│  130nm: Similar to 180nm with better performance. Gate oxide thinning      │
│         begins to matter but still well within safe limits for 10-yr.      │
│                                                                             │
│  90nm:  Gate oxide ~1.2nm. TDDB becomes more of a concern. Need           │
│         careful voltage derating. NBTI starts appearing.                   │
│                                                                             │
│  65nm:  Gate oxide ~1.0nm. Significant NBTI and TDDB concerns.            │
│         Requires careful reliability modeling. SEU rate increases.          │
│                                                                             │
│  40nm:  Gate oxide ~0.8nm. Multiple reliability challenges.                │
│         NBTI, TDDB, HCI all significant. Limited qualification data        │
│         for medical applications.                                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.1.4.4 Power Consumption by Process Node

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    POWER CONSUMPTION COMPARISON                              │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Dynamic Power: P_dyn = α × C_L × V_dd² × f                        │   │
│  │                                                                      │   │
│  │  Where:                                                              │   │
│  │    α = activity factor (~0.1 for pacemaker)                         │   │
│  │    C_L = load capacitance (scales with node)                        │   │
│  │    V_dd = supply voltage                                            │   │
│  │    f = clock frequency                                              │   │
│  │                                                                      │   │
│  │  Static Power: P_stat = I_leak × V_dd                               │   │
│  │                                                                      │   │
│  │  Where:                                                              │   │
│  │    I_leak = subthreshold leakage current (increases with scaling)   │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────┬───────────┬───────────┬───────────┬───────────┬──────┐│
│  │ Power Component │ 180nm     │ 130nm     │ 90nm      │ 65nm      │ 40nm ││
│  ├─────────────────┼───────────┼───────────┼───────────┼───────────┼──────┤│
│  │                 │           │           │           │           │      ││
│  │ Digital Core    │           │           │           │           │      ││
│  │ (100K gates     │           │           │           │           │      ││
│  │  @ 2MHz)        │           │           │           │           │      ││
│  │                 │           │           │           │           │      ││
│  │ Dynamic         │ 5 µW      │ 3 µW      │ 2 µW      │ 1.5 µW    │1 µW  ││
│  │ Static (leak)   │ 0.5 µW    │ 1 µW      │ 3 µW      │ 8 µW      │20 µW ││
│  │ Total           │ 5.5 µW    │ 4 µW      │ 5 µW      │ 9.5 µW    │21 µW ││
│  │                 │           │           │           │           │      ││
│  │ ─────────────────────────────────────────────────────────────────  │      ││
│  │                 │           │           │           │           │      ││
│  │ Analog (per     │           │           │           │           │      ││
│  │ channel)        │           │           │           │           │      ││
│  │                 │           │           │           │           │      ││
│  │ LNA + Filter    │ 2 µW      │ 2.5 µW    │ 3 µW      │ 4 µW      │5 µW  ││
│  │ ADC (SAR)       │ 3 µW      │ 2 µW      │ 1.5 µW    │ 1 µW      │0.8µW ││
│  │ DAC             │ 1 µW      │ 0.8 µW    │ 0.5 µW    │ 0.5 µW    │0.5µW ││
│  │ Total (per ch)  │ 6 µW      │ 5.3 µW    │ 5 µW      │ 5.5 µW    │6.3µW ││
│  │                 │           │           │           │           │      ││
│  │ ─────────────────────────────────────────────────────────────────  │      ││
│  │                 │           │           │           │           │      ││
│  │ I/O and RF      │           │           │           │           │      ││
│  │                 │           │           │           │           │      ││
│  │ Telemetry TX    │ 25 µW     │ 20 µW     │ 18 µW     │ 15 µW     │12 µW ││
│  │ Telemetry RX    │ 50 µW     │ 40 µW     │ 35 µW     │ 30 µW     │25 µW ││
│  │ Output Stage    │ 10 µW     │ 8 µW      │ 7 µW      │ 6 µW      │5 µW  ││
│  │ Total I/O       │ 85 µW     │ 68 µW     │ 60 µW     │ 51 µW     │42 µW ││
│  │                 │           │           │           │           │      ││
│  │ ─────────────────────────────────────────────────────────────────  │      ││
│  │                 │           │           │           │           │      ││
│  │ TOTAL SYSTEM    │           │           │           │           │      ││
│  │ (Nominal)       │           │           │           │           │      ││
│  │                 │           │           │           │           │      ││
│  │ Active          │ 100 µW    │ 80 µW     │ 70 µW     │ 65 µW     │60 µW ││
│  │ Sleep           │ 10 µW     │ 12 µW     │ 15 µW     │ 20 µW     │30 µW ││
│  │ Hibernate       │ 2 µW      │ 3 µW      │ 5 µW      │ 10 µW     │20 µW ││
│  │                 │           │           │           │           │      ││
│  │ NOTE: Sleep/hibernate power dominated by leakage at <65nm nodes    │      ││
│  │                                                                      │   │
│  └─────────────────┴───────────┴───────────┴───────────┴───────────┴──────┘│
│                                                                             │
│  CRITICAL INSIGHT:                                                         │
│  ─────────────────                                                         │
│  While advanced nodes (65nm, 40nm) offer lower dynamic power due to        │
│  reduced capacitance and voltage, their significantly higher leakage        │
│  current makes them WORSE for implantable pacemakers that spend 99%+       │
│  of their time in sleep/hibernate modes. The 180nm node has the            │
│  lowest total power for this specific use case.                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.1.4.5 Foundry Options and Medical Qualification

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FOUNDRY COMPARISON FOR MEDICAL IMPLANTS                  │
│                                                                             │
│  ┌──────────────────┬──────────┬──────────┬──────────┬──────────┬─────────┐│
│  │ Foundry          │ 180nm    │ 130nm    │ 90nm     │ 65nm     │ 40nm    ││
│  ├──────────────────┼──────────┼──────────┼──────────┼──────────┼─────────┤│
│  │                  │          │          │          │          │         ││
│  │ TSMC             │ Yes      │ Yes      │ Yes      │ Yes      │ Yes     ││
│  │ (Taiwan)         │ BCD/LV   │ BCD/LV   │ LV/GP    │ GP       │ GP      ││
│  │                  │          │          │          │          │         ││
│  │ Samsung          │ Yes      │ Yes      │ Yes      │ Yes      │ Yes     ││
│  │ (Korea)          │ LV       │ LV/GP    │ GP       │ GP       │ GP      ││
│  │                  │          │          │          │          │         ││
│  │ GlobalFoundries  │ Yes      │ Yes      │ Yes      │ Yes      │ Yes     ││
│  │ (USA/Germany)    │ BCD/LV   │ BCD/LV   │ LV       │ GP       │ GP      ││
│  │                  │          │          │          │          │         ││
│  │ UMC              │ Yes      │ Yes      │ Yes      │ Yes      │ Yes     ││
│  │ (Taiwan)         │ BCD      │ BCD/LV   │ LV       │ GP       │ GP      ││
│  │                  │          │          │          │          │         ││
│  │ X-FAB            │ Yes      │ Yes      │ Yes      │ No       │ No      ││
│  │ (Germany/USA)    │ BCD/SOI  │ BCD      │ BCD      │          │         ││
│  │                  │          │          │          │          │         ││
│  │ Tower/Jazz       │ Yes      │ Yes      │ Limited  │ No       │ No      ││
│  │ (Israel)         │ BCD/SOI  │ BCD      │          │          │         ││
│  │                  │          │          │          │          │         ││
│  │ Dongbu (DB HiTek)│ Yes      │ Yes      │ Yes      │ Limited  │ No      ││
│  │ (Korea)          │ BCD      │ BCD/LV   │ LV       │          │         ││
│  │                  │          │          │          │          │         ││
│  └──────────────────┴──────────┴──────────┴──────────┴──────────┴─────────┘│
│                                                                             │
│  BCD = Bipolar-CMOS-DMOS (mixed-signal optimized)                         │
│  LV = Low-Voltage CMOS                                                    │
│  GP = General Purpose CMOS                                                │
│  SOI = Silicon-on-Insulator                                                │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  MEDICAL DEVICE QUALIFICATION SUPPORT                                │   │
│  │                                                                      │   │
│  │  ┌──────────────┬────────────┬────────────┬────────────────────┐   │   │
│  │  │ Foundry      │ Qual Flow  │ MPW Service│ Reliability Data   │   │   │
│  │  ├──────────────┼────────────┼────────────┼────────────────────┤   │   │
│  │  │ TSMC         │ Full JEDEC │ Yes        │ Extensive (>20yr)  │   │   │
│  │  │              │ QualEx     │            │                    │   │   │
│  │  │ GlobalFound. │ Full JEDEC │ Yes        │ Good (>15yr)       │   │   │
│  │  │              │ QualEx     │            │                    │   │   │
│  │  │ X-FAB        │ Full JEDEC │ Yes        │ Excellent (BCD)    │   │   │
│  │  │              │            │            │                    │   │   │
│  │  │ Tower/Jazz   │ Full JEDEC │ Yes        │ Good (SOI)         │   │   │
│  │  │              │            │            │                    │   │   │
│  │  │ Samsung      │ Full JEDEC │ Yes        │ Good               │   │   │
│  │  │              │ QualEx     │            │                    │   │   │
│  │  │ UMC          │ Full JEDEC │ Yes        │ Good               │   │   │
│  │  │              │            │            │                    │   │   │
│  │  └──────────────┴────────────┴────────────┴────────────────────┘   │   │
│  │                                                                      │   │
│  │  Qualification Standards:                                           │   │
│  │  • JEDEC JESD47 (Stress-Test-Driven Qualification)                 │   │
│  │  • JEDEC JESD22-A108 (HTOL)                                        │   │
│  │  • JEDEC JESD22-A110 (HAST)                                        │   │
│  │  • JEDEC JESD22-A113 (Preconditioning)                             │   │
│  │  • JEDEC JESD22-B111 (ESD HBM)                                     │   │
│  │  • JEDEC JESD22-C101 (ESD CDM)                                     │   │
│  │  • IEC 60747 (Semiconductor devices)                               │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.1.4.6 Cost Analysis

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    COST ANALYSIS PER PROCESS NODE                           │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  NRE (Non-Recurring Engineering) Costs                               │   │
│  │                                                                      │   │
│  │  ┌─────────────┬───────────┬───────────┬───────────┬───────────┐   │   │
│  │  │ Component   │ 180nm     │ 130nm     │ 90nm      │ 65nm      │   │   │
│  │  ├─────────────┼───────────┼───────────┼───────────┼───────────┤   │   │
│  │  │ Mask Set    │ $800K     │ $1.2M     │ $1.8M     │ $3.0M     │   │   │
│  │  │ MPW Run     │ $50K      │ $80K      │ $120K     │ $200K     │   │   │
│  │  │ DRC/LVS     │ $20K      │ $30K      │ $50K      │ $80K      │   │   │
│  │  │ Place&Route │ $50K      │ $80K      │ $120K     │ $200K     │   │   │
│  │  │ Verification│ $200K     │ $300K     │ $500K     │ $800K     │   │   │
│  │  │ Qual Cost   │ $100K     │ $150K     │ $200K     │ $300K     │   │   │
│  │  │ Total NRE   │ $1.2M     │ $1.8M     │ $2.8M     │ $4.6M     │   │   │
│  │  └─────────────┴───────────┴───────────┴───────────┴───────────┘   │   │
│  │                                                                      │   │
│  │  Recurring Costs (per device, assuming 10K units/year)              │   │
│  │                                                                      │   │
│  │  ┌─────────────┬───────────┬───────────┬───────────┬───────────┐   │   │
│  │  │ Component   │ 180nm     │ 130nm     │ 90nm      │ 65nm      │   │   │
│  │  ├─────────────┼───────────┼───────────┼───────────┼───────────┤   │   │
│  │  │ Wafer Cost  │ $3,000    │ $4,000    │ $6,000    │ $10,000   │   │   │
│  │  │ Dies/Wafer  │ ~1,200    │ ~1,200    │ ~1,200    │ ~1,200    │   │   │
│  │  │ Die Size    │ 25mm²     │ 18mm²     │ 14mm²     │ 10mm²     │   │   │
│  │  │ Yield       │ 85%       │ 82%       │ 78%       │ 72%       │   │   │
│  │  │ Die Cost    │ $3.10     │ $4.25     │ $6.53     │ $11.72    │   │   │
│  │  │ Test/Probe  │ $0.50     │ $0.60     │ $0.75     │ $1.00     │   │   │
│  │  │ Packaging   │ $2.00     │ $2.00     │ $2.00     │ $2.50     │   │   │
│  │  │ Assembly    │ $1.00     │ $1.00     │ $1.00     │ $1.50     │   │   │
│  │  │ Total/Unit  │ $6.60     │ $7.85     │ $10.28    │ $16.72    │   │   │
│  │  └─────────────┴───────────┴───────────┴───────────┴───────────┘   │   │
│  │                                                                      │   │
│  │  Total Cost of Ownership (5 years, 50K units)                       │   │
│  │                                                                      │   │
│  │  ┌─────────────┬───────────┬───────────┬───────────┬───────────┐   │   │
│  │  │             │ 180nm     │ 130nm     │ 90nm      │ 65nm      │   │   │
│  │  ├─────────────┼───────────┼───────────┼───────────┼───────────┤   │   │
│  │  │ NRE         │ $1.2M     │ $1.8M     │ $2.8M     │ $4.6M     │   │   │
│  │  │ Recurring   │ $0.33M    │ $0.39M    │ $0.51M    │ $0.84M    │   │   │
│  │  │ Total TCO   │ $1.53M    │ $2.19M    │ $3.31M    │ $5.44M    │   │   │
│  │  │ Cost/Unit   │ $30.60    │ $43.80    │ $66.20    │ $108.80   │   │   │
│  │  └─────────────┴───────────┴───────────┴───────────┴───────────┘   │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  NOTE: Costs are approximate and vary by foundry, volume, and contract.    │
│  Medical device qualification adds ~20-30% to standard foundry costs.     │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.1.4.7 Process Selection Decision Matrix

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PROCESS SELECTION DECISION MATRIX                         │
│                                                                             │
│  ┌──────────────────────┬────────┬────────┬────────┬────────┬────────┐    │
│  │ Criterion            │ Weight │ 180nm  │ 130nm  │ 90nm   │ 65nm   │    │
│  │                      │        │ Score  │ Score  │ Score  │ Score  │    │
│  ├──────────────────────┼────────┼────────┼────────┼────────┼────────┤    │
│  │                      │        │        │        │        │        │    │
│  │ RELIABILITY          │        │        │        │        │        │    │
│  │ Gate oxide integrity │ 10%    │ 10     │ 9      │ 7      │ 5      │    │
│  │ HTOL failure rate    │ 10%    │ 10     │ 10     │ 8      │ 6      │    │
│  │ TID tolerance        │  5%    │ 10     │ 8      │ 6      │ 4      │    │
│  │ SEU immunity         │  5%    │ 10     │ 9      │ 7      │ 5      │    │
│  │                      │        │        │        │        │        │    │
│  │ POWER                │        │        │        │        │        │    │
│  │ Active power         │ 10%    │ 5      │ 7      │ 8      │ 9      │    │
│  │ Sleep power          │ 10%    │ 10     │ 9      │ 7      │ 4      │    │
│  │ Hibernate power      │ 10%    │ 10     │ 9      │ 7      │ 4      │    │
│  │                      │        │        │        │        │        │    │
│  │ ANALOG PERFORMANCE   │        │        │        │        │        │    │
│  │ Noise performance    │  5%    │ 10     │ 9      │ 8      │ 6      │    │
│  │ Matching             │  5%    │ 10     │ 9      │ 8      │ 6      │    │
│  │ Passive quality      │  5%    │ 10     │ 9      │ 8      │ 7      │    │
│  │                      │        │        │        │        │        │    │
│  │ COST                 │        │        │        │        │        │    │
│  │ NRE cost             │ 10%    │ 10     │ 8      │ 6      │ 3      │    │
│  │ Unit cost            │ 10%    │ 10     │ 8      │ 6      │ 4      │    │
│  │                      │        │        │        │        │        │    │
│  │ AVAILABILITY         │        │        │        │        │        │    │
│  │ Foundry options      │  5%    │ 10     │ 10     │ 9      │ 8      │    │
│  │ Long-term supply     │  5%    │ 10     │ 10     │ 9      │ 7      │    │
│  │ Qualification data   │  5%    │ 10     │ 10     │ 9      │ 8      │    │
│  │                      │        │        │        │        │        │    │
│  ├──────────────────────┼────────┼────────┼────────┼────────┼────────┤    │
│  │ WEIGHTED TOTAL       │ 100%   │ 9.15   │ 8.80   │ 7.40   │ 5.75   │    │
│  ├──────────────────────┼────────┼────────┼────────┼────────┼────────┤    │
│  │ RANK                 │        │ #1     │ #2     │ #3     │ #4     │    │
│  └──────────────────────┴────────┴────────┴────────┴────────┴────────┘    │
│                                                                             │
│  ═══════════════════════════════════════════════════════════════════════   │
│  SELECTION RECOMMENDATION: 180nm BCD Process (TSMC/GF/X-FAB)              │
│  ═══════════════════════════════════════════════════════════════════════   │
│                                                                             │
│  Rationale:                                                                │
│  1. BEST RELIABILITY: 180nm has the longest track record and most          │
│     favorable reliability data for medical implant applications.           │
│                                                                             │
│  2. LOWEST TOTAL POWER: For a device spending 99% of time in sleep/       │
│     hibernate, 180nm's low leakage current dominates the power budget.    │
│                                                                             │
│  3. BEST ANALOG PERFORMANCE: 180nm offers superior matching, noise,       │
│     and passive component quality critical for the analog front-end.       │
│                                                                             │
│  4. LOWEST COST: Both NRE and recurring costs are significantly lower.    │
│                                                                             │
│  5. MAXIMUM AVAILABILITY: 6+ foundries offer qualified 180nm BCD          │
│     processes with >20 year production commitment.                         │
│                                                                             │
│  6. INDUSTRY STANDARD: Most current pacemaker manufacturers use 180nm     │
│     or 130nm processes, providing extensive design ecosystem support.      │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.1.4.8 Recommended Process: 180nm BCD Detailed Specifications

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    RECOMMENDED PROCESS: 180nm BCD                           │
│                    (e.g., TSMC C018, GF C180, X-FAB XH018)                 │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  PROCESS OPTIONS AND FEATURES                                        │   │
│  │                                                                      │   │
│  │  Core CMOS:                                                         │   │
│  │  • N-channel MOSFET: Vth=0.45V, Lmin=180nm                        │   │
│  │  • P-channel MOSFET: Vth=-0.45V, Lmin=180nm                       │   │
│  │  • Gate oxide: 4nm (core), 7nm (I/O), 12nm (high-voltage)         │   │
│  │  • Supply voltage: 1.8V (core), 3.3V/5V (I/O)                     │   │
│  │                                                                      │   │
│  │  Bipolar Transistors:                                               │   │
│  │  • NPN: BVceo > 8V, fT > 30 GHz                                   │   │
│  │  • PNP: BVceo > 12V, fT > 5 GHz                                   │   │
│  │                                                                      │   │
│  │  High-Voltage Devices:                                              │   │
│  │  • HV NMOS: BVdss = 20V, Rds(on) < 50mΩ·mm                      │   │
│  │  • HV PMOS: BVdss = -20V                                           │   │
│  │                                                                      │   │
│  │  Passive Components:                                                │   │
│  │  • Poly resistor: 1kΩ/sq, TC < 100ppm/°C, matching <0.1%         │   │
│  │  • High-value resistor: 10kΩ/sq (for high-impedance nodes)        │   │
│  │  • MIM capacitor: 1fF/µm², TC < 50ppm/°C, matching <0.1%        │   │
│  │  • MOS capacitor: 2fF/µm² (digital decoupling)                     │   │
│  │                                                                      │   │
│  │  Metal Stack:                                                       │   │
│  │  • 6 metal layers (Aluminum-based)                                 │   │
│  │  • M1-M5: 0.35µm minimum width/spacing                            │   │
│  │  • M6 (top): 0.5µm minimum width (for RF, bonding pads)           │   │
│  │  • Via: 0.35µm × 0.35µm                                           │   │
│  │                                                                      │   │
│  │  Special Features:                                                  │   │
│  │  • Deep N-well for isolation                                        │   │
│  │  • EPROM/EEPROM options available                                   │   │
│  │  • MIM capacitor option                                             │   │
│  │  • High-resistance poly option                                      │   │
│  │                                                                      │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  DESIGN RULES SUMMARY (Key Rules)                                   │   │
│  │                                                                      │   │
│  │  ┌────────────────────────┬──────────────┬────────────────────┐    │   │
│  │  │ Rule                   │ Minimum      │ Recommended        │    │   │
│  │  ├────────────────────────┼──────────────┼────────────────────┤    │   │
│  │  │ Gate length            │ 180nm        │ 200-350nm (analog) │    │   │
│  │  │ Gate width             │ 200nm        │ >1µm (matching)    │    │   │
│  │  │ Gate spacing           │ 300nm        │ 500nm+             │    │   │
│  │  │ Active spacing         │ 250nm        │ 400nm+             │    │   │
│  │  │ Metal 1 width          │ 200nm        │ 350nm+             │    │   │
│  │  │ Metal 1 spacing        │ 200nm        │ 350nm+             │    │   │
│  │  │ Contact size           │ 250nm×250nm  │ 300nm×300nm        │    │   │
│  │  │ Via size               │ 350nm×350nm  │ 400nm×400nm        │    │   │
│  │  │ MIM cap area           │ 1µm²         │ >10µm²             │    │   │
│  │  │ Poly resistor L        │ 1µm          │ >5µm               │    │   │
│  │  │ Well spacing           │ 1.5µm        │ 2µm+               │    │   │
│  │  │ Latchup prevention     │ Guard rings  │ Triple well         │    │   │
│  │  └────────────────────────┴──────────────┴────────────────────┘    │   │
│  │                                                                      │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  I/O PAD FRAME SPECIFICATION                                         │   │
│  │                                                                      │   │
│  │  • Standard I/O: 3.3V CMOS compatible                              │   │
│  │  • High-voltage I/O: 5V tolerant                                   │   │
│  │  • ESD protection: 2kV HBM (standard), 4kV (enhanced)             │   │
│  │  • Pad pitch: 100µm (standard), 50µm (fine-pitch)                 │   │
│  │  • Bond pad size: 80µm × 80µm (for wire bond)                     │   │
│  │  • Flip-chip bump: Not supported (use wire bond for hermetic pkg)  │   │
│  │                                                                      │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.1.4.9 Technology Roadmap and Second-Source Strategy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    TECHNOLOGY ROADMAP & SECOND-SOURCE                        │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │  PRIMARY: TSMC C018 (180nm BCD)                                     │   │
│  │  ──────────────────────────────                                     │   │
│  │  • Primary production node                                          │   │
│  │  • Full medical qualification support                               │   │
│  │  • Extensive reliability data library                               │   │
│  │  • MPW runs available quarterly                                     │   │
│  │  • Volume production: 10K-100K wafers/year                          │   │
│  │                                                                      │   │
│  │  SECOND SOURCE: GlobalFoundries C180 (180nm BCD)                    │   │
│  │  ──────────────────────────────────────────────                     │   │
│  │  • Pin-compatible, rule-compatible process                         │   │
│  │  • Same PDK version (C180 v2.0)                                     │   │
│  │  • Qualification data available                                     │   │
│  │  • US/EU manufacturing for supply chain security                    │   │
│  │                                                                      │   │
│  │  THIRD SOURCE: X-FAB XH018 (180nm BCD/SOI)                         │   │
│  │  ──────────────────────────────────────────────                     │   │
│  │  • Optional SOI variant for enhanced isolation                      │   │
│  │  • Superior latchup immunity                                        │   │
│  │  • Higher cost but better for high-reliability applications         │   │
│  │                                                                      │   │
│  │  MIGRATION PATH:                                                    │   │
│  │  ────────────────                                                   │   │
│  │  Current:    180nm BCD (Primary)                                    │   │
│  │  Future:     130nm BCD (if power reduction >30% justified)          │   │
│  │  Far Future: 65nm (only if leakage solved, e.g., FDSOI)            │   │
│  │                                                                      │   │
│  │  MIGRATION CRITERIA:                                                │   │
│  │  • Must demonstrate equivalent reliability (>10yr)                  │   │
│  │  • Must show power savings >25% (including leakage)                 │   │
│  │  • Must have foundry qualification data for medical use             │   │
│  │  • Must maintain analog performance (noise, matching)               │   │
│  │                                                                      │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  RISK MITIGATION:                                                          │
│  ────────────────                                                          │
│  1. Maintain two qualified sources at all times                            │
│  2. Design portability: Use foundry-agnostic design rules (DRC clean)     │
│  3. PDK abstraction: Use standard cell libraries with consistent API      │
│  4. Reliability monitoring: Track lot-specific reliability data           │
│  5. Supply chain: Buffer 6-month wafer inventory                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.1.4.10 Summary: Why 180nm for iPACE-CHIP

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    WHY 180nm IS THE OPTIMAL CHOICE                           │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │  1. RELIABILITY FIRST                                                │   │
│  │     • 20+ years of production data                                  │   │
│  │     • Gate oxide integrity: >300 krad TID tolerance                │   │
│  │     • HTOL: <10 FIT (industry leading)                             │   │
│  │     • Minimal NBTI/TDDB concerns                                   │   │
│  │                                                                      │   │
│  │  2. POWER OPTIMIZED FOR IMPLANTS                                    │   │
│  │     • Lowest leakage current of all nodes                          │   │
│  │     • Sleep power: 2 µW (vs. 30 µW at 40nm)                       │   │
│  │     • 10-year battery life achievable                              │   │
│  │     • Leakage-dominated budget favors older nodes                   │   │
│  │                                                                      │   │
│  │  3. SUPERIOR ANALOG                                                  │   │
│  │     • Best matching for precision circuits                          │   │
│  │     • Lowest 1/f noise corner frequency                             │   │
│  │     • High-quality passive components                               │   │
│  │     • Mature BCD process for mixed-signal                          │   │
│  │                                                                      │   │
│  │  4. ECONOMICALLY VIABLE                                              │   │
│  │     • NRE: $1.2M (vs. $4.6M for 65nm)                             │   │
│  │     • Die cost: $6.60 (vs. $16.72 for 65nm)                       │   │
│  │     • Total TCO: $1.5M vs. $5.4M (5yr)                            │   │
│  │                                                                      │   │
│  │  5. SUPPLY CHAIN SECURITY                                            │   │
│  │     • 6+ qualified foundries                                        │   │
│  │     • Long-term availability guaranteed (>20 years)                 │   │
│  │     • Multiple geographic locations                                 │   │
│  │     • No single-source dependency                                   │   │
│  │                                                                      │   │
│  │  6. DESIGN ECOSYSTEM                                                 │   │
│  │     • Extensive PDK support                                         │   │
│  │     • Mature EDA tool compatibility                                 │   │
│  │     • Large pool of experienced designers                           │   │
│  │     • Extensive IP library availability                             │   │
│  │                                                                      │   │
│  │  ┌──────────────────────────────────────────────────────────────┐   │   │
│  │  │ FINAL RECOMMENDATION: 180nm BCD (TSMC C018 or GF C180)      │   │   │
│  │  │                                                               │   │   │
│  │  │ This node provides the optimal balance of reliability,       │   │   │
│  │  │ power, performance, and cost for a 10-year implantable      │   │   │
│  │  │ pacemaker application. No advanced node provides sufficient  │   │   │
│  │  │ advantages to justify the increased risk, cost, and          │   │   │
│  │  │ complexity for this specific application.                    │   │   │
│  │  └──────────────────────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

*Section 2.1.4 — Technology Node Selection*
*Previous: Section 2.1.3 — Functional Architecture*
*Next: Section 2.2 — Sensing and Stimulation*
