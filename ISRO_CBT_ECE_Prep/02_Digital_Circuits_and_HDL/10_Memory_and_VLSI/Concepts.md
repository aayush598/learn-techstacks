# Memory and VLSI - Concepts

## Memory Hierarchy
```
Registers (fastest, smallest)
Cache (SRAM) - L1, L2, L3
Main memory (DRAM)
Secondary (SSD/disk - slowest, largest)
Speed/access tradeoff with capacity/cost
```

## SRAM vs DRAM
| Feature | SRAM | DRAM |
|---------|------|------|
| Cell | 6 transistors (latch) | 1 transistor + capacitor |
| Speed | Fast | Slower |
| Density | Low | High |
| Power | High (static) | Low (refresh needed) |
| Refresh | No | Yes (~every 15 ms) |
| Use | Cache | Main memory |
| Volatile | Yes | Yes |

## Memory Types
- **ROM**: read only, non-volatile
- **PROM**: programmable once
- **EPROM**: erasable (UV)
- **EEPROM**: electrically erasable
- **Flash**: block-erasable EEPROM (SSD, USB)

## Memory Organization
```
Capacity = depth x width
  e.g., 256K x 8 = 256K locations, 8-bit each = 2Mbit
Address lines: A, 2^A locations
Data lines: width
Chip select (CS), read/write enable
```

## Address Decoding
```
For memory M depth with A address lines: 2^A = M
Decoder selects the memory chip based on high address bits
Chip select logic for multiple devices
```

## Word & Organization
```
Word = unit of data (width)
Word addressable: each location has unique address
Byte addressing common
```

## Cache Memory
```
Small fast SRAM between CPU and main memory
Locality of reference (temporal, spatial)
Hit: data in cache (fast), Miss: fetch from memory
Hit ratio determines performance
```

## VLSI Introduction
```
Very Large Scale Integration
  SSI <10 gates, MSI <100, LSI <1000, VLSI <100k, ULSI more
CMOS dominant technology (low power)
Scaling: feature size shrinking, more transistors
```

## CMOS Logic
```
nMOS + pMOS complementary
Low static power (only switching power ~CV^2f)
High noise margins
Reference: inverter, NAND, NOR
```

## CMOS Gate Characteristics
```
Fan-out: number of gates a gate can drive
Propagation delay (~RC)
Power: P = C V^2 f (dynamic)
Noise margin: VIL, VIH, VOH, VOL
```

## Devices scaling (Moore's Law)
```
Feature size scales down: faster, lower power, more density
Mobility, leakage reduce scaling benefits
```

## Design flow
```
Spec -> RTL (HDL) -> Synthesis -> Place&Route -> Fabrication
Design reuse, IP cores, standard cells
```

## FPGA vs ASIC
```
FPGA: programmable, reconfigurable, slower, higher power
ASIC: custom, faster, lower power, expensive NRE
```

---

## ISRO Key Points
- SRAM 6T fast, no refresh; DRAM 1T+cap needs refresh
- ROM/PROM/EPROM/EEPROM/Flash types
- Memory size: 2^A x D
- CMOS: low power, ~CV^2f
- Address decoding / chip select
- Cache: locality, hit/miss
