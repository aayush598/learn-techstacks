# 14.4.1 Foundry Selection for iPACE-CHIP

## Overview

Foundry selection is a strategic decision that impacts iPACE-CHIP quality, cost,
schedule, and long-term supply chain resilience. The selected foundry must not only
deliver silicon that meets performance specifications but also maintain consistent
quality over a 20-year product lifecycle, support medical device regulatory requirements,
and provide supply chain security against geopolitical and natural disruption risks.
This chapter evaluates candidate foundries and documents the selection rationale.

## Selection Criteria

### Weighted Evaluation Matrix

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Process Capability | 25% | Ability to meet iPACE-CHIP electrical specs |
| Quality System | 20% | Medical device qualification history |
| Reliability Data | 15% | Existing reliability qualification base |
| Supply Chain Security | 15% | Geographic diversity, capacity commitment |
| Cost Competitiveness | 10% | Wafer price, NRE, ongoing cost |
| Design Support | 10% | PDK quality, FAE support, IP availability |
| Technology Roadmap | 5% | Future node availability and migration |

### Process Requirements for iPACE-CHIP

| Requirement | Specification | Foundry Must-Have |
|------------|--------------|-------------------|
| Node | 180 nm | Production-qualified 180 nm |
| HV Option | 18V minimum | High-voltage transistor available |
| BiCMOS | NPN BJT available | Bipolar integration |
| MIM Capacitor | 2 fF/um2 density | Precision capacitor option |
| EEPROM | 2 KB minimum | Embedded non-volatile memory |
| Metal Layers | 4 minimum | Multi-layer metallization |
| Wafer Size | 200 mm | 200 mm production line |
| SOI | Preferred (not mandatory) | Silicon-on-insulator option |

## Foundry Candidate Assessment

### TSMC (Taiwan Semiconductor Manufacturing Company)

**Profile**:
- Headquarters: Hsinchu, Taiwan
- Revenue: > $70B/year (2024)
- Technology Leadership: 3nm production, 2nm development
- Medical Device Track Record: Extensive (pacemaker, neurostimulator, cochlear ASICs)

**180 nm Platform**:
- Process: TSMC 180HV (18V), 180BCD (Bipolar-CMOS-DMOS)
- Wafer Size: 200 mm
- Capacity: > 50,000 wafers/month at 180 nm
- Qualification: AEC-Q100, multiple medical device qualifications
- IP Available: Standard cell libraries, I/O, memory compilers, analog IP
- PDK Maturity: > 20 years of production history

**Strengths**:
- Highest volume 180 nm producer globally
- Most extensive medical device qualification database
- Best-in-class yield (> 98% for mature processes)
- Comprehensive PDK and IP ecosystem
- Multiple packaging partnerships (ASE, SPIL)
- Financial stability (market cap > $500B)

**Risks**:
- Geographic concentration in Taiwan (seismic and geopolitical risk)
- Largest customers may consume available capacity during shortages
- Lead time for new mask sets: 8-12 weeks
- Process changes may not prioritize small medical customers

**Cost Estimate**:
- 200 mm wafer: $3,000-3,500
- NRE (180HV): $1.5M (masks + engineering)
- Engineering shuttles: Available quarterly ($50K per shuttle)

### GlobalFoundries

**Profile**:
- Headquarters: Malta, New York, USA
- Revenue: ~$7B/year (2024)
- Specialty: Differentiated technologies (RF-SOI, BCDLite, embedded NVM)
- Medical Device Track Record: Growing, with several implantable device customers

**180 nm Platform**:
- Process: GF 180HV (18V), GF 180BCD
- Wafer Size: 200 mm
- Capacity: ~20,000 wafers/month at 180 nm
- Qualification: AEC-Q100, selected medical qualifications
- Wafer Fab Locations: Germany (Dresden), USA (Vermont, New York)

**Strengths**:
- US and European manufacturing (supply chain diversification)
- Strong specialty technology portfolio
- FDA-registered facilities (for certain processes)
- Government-backed (CHIPS Act funding in USA and EU)
- More accessible for mid-size medical device companies

**Risks**:
- Smaller 180 nm capacity than TSMC
- Less extensive medical device qualification database
- Higher per-wafer cost than TSMC for equivalent processes
- Technology roadmap may prioritize advanced nodes over 180 nm

**Cost Estimate**:
- 200 mm wafer: $3,500-4,000
- NRE (180HV): $1.8M
- Engineering shuttles: Available semi-annually ($60K per shuttle)

### X-FAB Silicon Solutions

**Profile**:
- Headquarters: Erfurt, Germany
- Revenue: ~$800M/year (2024)
- Specialty: Analog/mixed-signal, high-voltage, MEMS, biocompatible
- Medical Device Track Record: Strong (dedicated medical business unit)

**180 nm Platform**:
- Process: XH018 (18V), XH018HV (18V), XB018 (BiCMOS)
- Wafer Size: 200 mm
- Capacity: ~10,000 wafers/month
- Qualification: ISO 13485 support, extensive medical track record
- Wafer Fab Locations: Germany (Erfurt), Malaysia (Kulim)

**Strengths**:
- Dedicated medical device support team
- European manufacturing (GDPR compliance, supply chain security)
- Flexible for small-to-medium volume customers
- ISO 13485 certified quality system
- Biocompatible passivation options available
- Process design specifically for medical applications

**Risks**:
- Smaller company (less financial buffer than TSMC/GF)
- Limited high-volume capacity
- Less advanced technology roadmap
- Single EUV lithography platform (may limit density options)

**Cost Estimate**:
- 200 mm wafer: $3,200-3,800
- NRE (XH018): $1.2M
- Engineering shuttles: Available quarterly ($45K per shuttle)

### Samsung Foundry

**Profile**:
- Headquarters: Hwaseong, South Korea
- Revenue: ~$15B/year (foundry segment)
- Technology Leadership: 3nm GAA production
- Medical Device Track Record: Limited medical-specific qualifications

**Assessment**: Samsung has excellent technology capabilities but limited
medical device track record. Their focus on advanced nodes (5nm and below)
means 180 nm is a legacy process with reduced priority and support.

**Decision**: Not recommended as primary foundry due to limited medical
device qualification support at 180 nm.

### Tower Semiconductor

**Profile**:
- Headquarters: Migdal HaEmek, Israel
- Revenue: ~$1.5B/year (2024)
- Specialty: Analog/mixed-signal, high-voltage, RF
- Medical Device Track Record: Moderate

**Assessment**: Tower offers competitive 180 nm capabilities with some medical
device experience. However, their capacity is limited and geopolitical risks
in the Middle East region are a consideration for supply chain security.

**Decision**: Possible secondary source but not recommended as primary.

## Detailed Evaluation: Top 3 Foundries

### Scorecard

| Criterion (Weight) | TSMC | GlobalFoundries | X-FAB |
|-------------------|------|-----------------|-------|
| Process Capability (25%) | 9.5 | 8.0 | 8.5 |
| Quality System (20%) | 9.0 | 7.5 | 9.5 |
| Reliability Data (15%) | 9.5 | 7.0 | 8.0 |
| Supply Chain Security (15%) | 6.0 | 8.5 | 8.0 |
| Cost Competitiveness (10%) | 8.5 | 6.5 | 7.5 |
| Design Support (10%) | 9.0 | 7.5 | 8.5 |
| Technology Roadmap (5%) | 9.0 | 8.0 | 7.0 |
| **Weighted Score** | **8.73** | **7.55** | **8.35** |

### Selection Decision

**Primary Foundry**: TSMC (180HV process)
- Highest overall score driven by process capability and quality system maturity
- Most extensive medical device qualification database
- Best yield and reliability track record

**Secondary/Qualification Foundry**: X-FAB (XH018 process)
- Strong medical device focus and ISO 13485 support
- European manufacturing provides supply chain diversification
- Qualification provides regulatory and supply chain risk mitigation

**Tertiary/Backup**: GlobalFoundries (180HV process)
- US/European manufacturing for additional geographic diversification
- Potential future primary if supply chain risks increase

## Qualification Protocol

### Foundry Qualification Timeline

```
Phase 1: PDK Evaluation (Month 1-3)
    |
    +---> PDK delivery and review
    +---> SPICE model validation against silicon
    +---> DRC/LVS rule verification
    +---> IP library assessment
    |
    v
Phase 2: Test Chip Fabrication (Month 4-8)
    |
    +---> Test chip design (parametric + reliability structures)
    +---> Tapeout (Month 5)
    +---> Fabrication (12-14 weeks)
    +---> Wafer sort and evaluation
    |
    v
Phase 3: Qualification Lots (Month 9-15)
    |
    +---> 3 qualification lots (minimum)
    +---> Full parametric characterization
    +---> WLR testing (HCI, NBTI, TDDB, EM)
    +---> Package-level reliability (HTOL, TC, HAST)
    +---> Yield analysis and process capability
    |
    v
Phase 4: Product Tapeout (Month 16-20)
    |
    +---> iPACE-CHIP design finalization
    +---> Tapeout and fabrication
    +---> Product qualification
    +---> Production release
```

### Qualification Test Matrix

| Test | Standard | Duration | Sample | Pass Criteria |
|------|----------|----------|--------|--------------|
| HTOL | JEDEC JESD47 | 1000 hr at 125C | 77 units | 0 failures |
| ESD HBM | JEDEC JS-001 | - | 30 units | > 2 kV |
| ESD CDM | JEDEC JS-002 | - | 30 units | > 250 V |
| TC | JEDEC JESD22-A104 | 1000 cycles | 77 units | 0 failures |
| HAST | JEDEC JESD22-A110 | 96 hr at 130C/85%RH | 77 units | 0 failures |
| Preconditioning | JEDEC J-STD-020 | MSL3 | 77 units | Before TC |
| WLR HCI | Internal | 10000 sec stress | 50 structures | Lifetime > 100 yr |
| WLR NBTI | Internal | 10000 sec stress | 50 structures | Lifetime > 50 yr |
| WLR TDDB | Internal | Breakdown test | 100 caps | t63 > 100 yr |
| WLR EM | Internal | Breakdown test | 20 lines | MTF > 500 yr |

## Supply Chain Contracting

### Wafer Supply Agreement Structure

| Term | TSMC | X-FAB |
|------|------|-------|
| Minimum Annual Purchase | 500 wafers | 200 wafers |
| Price Lock Period | 2 years | 3 years |
| Capacity Reservation | 25 wafers/month | 10 wafers/month |
| Lead Time (Production) | 12-16 weeks | 10-14 weeks |
| Lead Time (Engineering) | 8-12 weeks | 8-10 weeks |
| Quality Agreement | Required | Included in ISO 13485 |
| Process Change Notification | 12 months advance | 6 months advance |
| Last-Time Buy | 24 months notice | 18 months notice |
| IP Protection | NDA + encryption | NDA + encryption |

### Pricing Model

**Volume Pricing (TSMC 180HV)**:

| Annual Volume | Wafer Price | Annual Spend |
|--------------|-------------|-------------|
| 500 wafers | $3,200 | $1.6M |
| 1,000 wafers | $2,900 | $2.9M |
| 2,000 wafers | $2,700 | $5.4M |
| 5,000+ wafers | $2,500 | $12.5M+ |

**Volume Pricing (X-FAB XH018)**:

| Annual Volume | Wafer Price | Annual Spend |
|--------------|-------------|-------------|
| 200 wafers | $3,500 | $700K |
| 500 wafers | $3,200 | $1.6M |
| 1,000 wafers | $2,900 | $2.9M |

## Risk Management

### Geopolitical Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Taiwan conflict/disruption | Low-Medium | Critical | X-FAB qualification as backup |
| Export control changes | Low | High | Maintain US/EU foundry capability |
| Pandemic disruption | Low | Medium | 3-month wafer inventory buffer |
| Natural disaster (earthquake) | Low | High | Geographic diversification |
| Cyber attack on foundry | Low | Medium | Business continuity agreements |

### Quality Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Process excursion | Medium | High | WLR monitoring, SPC |
| Yield degradation | Low | High | Monthly yield review meetings |
| Material shortage | Low | Medium | 6-month raw material inventory |
| Counterfeit material | Very Low | Critical | ISO-certified suppliers only |
| Design IP theft | Low | Critical | Encryption, access controls |

## Summary

The iPACE-CHIP foundry selection establishes TSMC 180HV as the primary production
foundry, leveraging the world's most mature and qualified 180 nm platform for medical
devices. X-FAB XH018 serves as the secondary qualification foundry, providing supply
chain diversification and dedicated medical device support. This dual-foundry strategy
ensures supply chain resilience while maintaining the quality and reliability standards
required for a 20-year implantable medical device. The comprehensive qualification
protocol and supply agreement structure protect against both quality and supply
continuity risks.

## References

1. TSMC Foundry Technology Overview, 2024.
2. GlobalFoundries 180nm Process Portfolio, 2024.
3. X-FAB XH018 Process Specification, Document XS1X0_0.
4. iPACE-CHIP Foundry Selection Report, Internal Document, Rev 1.0.
5. U.S. CHIPS and Science Act, 2022.
6. EU Chips Act, Regulation 2023/1781.
7. SEMI S2-0718, Environmental, Health, and Safety Guideline.
8. iPACE-CHIP Supply Chain Risk Assessment, Internal, Rev 2.0.
