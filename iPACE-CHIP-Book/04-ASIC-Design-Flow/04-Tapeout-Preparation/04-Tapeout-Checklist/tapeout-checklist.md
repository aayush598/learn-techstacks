# Tapeout Checklist for iPACE-CHIP ASIC

## 1. Introduction

The tapeout checklist is the final quality gate before the iPACE-CHIP GDS-II file is
sent to TSMC for fabrication. This checklist represents the cumulative verification
result of the entire ASIC design flow — every item must be signed off before the
irreversible decision to manufacture.

For a medical implantable device, tapeout is a critical regulatory milestone:
- A defective chip delays FDA/CE submission by 3-6 months (re-spin)
- A safety-critical bug discovered post-tapeout may require full re-verification
- The tapeout checklist forms part of the Design History File (DHF)

## 2. Tapeout Checklist Structure

### 2.1 Pre-Tapeout Quality Gates

```
iPACE-CHIP Tapeout Quality Gates:
═══════════════════════════════════════════════════════════════

  ┌─────────────────────────────────────────────────────────────┐
  │  GATE 1: RTL COMPLETE                                        │
  │  ✓ All RTL modules coded and reviewed                       │
  │  ✓ Lint check clean (0 errors)                              │
  │  ✓ RTL simulation passing                                   │
  │  ✓ Code review signoff                                      │
  └───────────────────────────┬─────────────────────────────────┘
                              │ PASS
  ┌───────────────────────────v─────────────────────────────────┐
  │  GATE 2: SYNTHESIS COMPLETE                                 │
  │  ✓ Synthesis passing at all corners                         │
  │  ✓ Timing clean (0 setup/hold violations)                   │
  │  ✓ Area within budget                                       │
  │  ✓ Power within budget                                      │
  │  ✓ RTL-to-netlist equivalence verified                      │
  └───────────────────────────┬─────────────────────────────────┘
                              │ PASS
  ┌───────────────────────────v─────────────────────────────────┐
  │  GATE 3: PHYSICAL DESIGN COMPLETE                           │
  │  ✓ Floorplan approved                                       │
  │  ✓ Placement clean                                          │
  │  ✓ CTS clean (skew < 5 ns)                                 │
  │  ✓ Routing complete (no DRC violations)                     │
  │  ✓ Post-route timing clean                                  │
  └───────────────────────────┬─────────────────────────────────┘
                              │ PASS
  ┌───────────────────────────v─────────────────────────────────┐
  │  GATE 4: SIGNOFF COMPLETE                                   │
  │  ✓ DRC clean (0 violations)                                 │
  │  ✓ LVS clean (full match)                                   │
  │  ✓ ERC clean                                                │
  │  ✓ Antenna clean                                            │
  │  ✓ Density check passing                                    │
  │  ✓ EM/IR analysis passing                                   │
  │  ✓ Formal verification passing                              │
  │  ✓ Post-route STA clean (all corners)                       │
  └───────────────────────────┬─────────────────────────────────┘
                              │ PASS
  ┌───────────────────────────v─────────────────────────────────┐
  │  GATE 5: TAPEOUT AUTHORIZATION                              │
  │  ✓ All checklists signed                                    │
  │  ✓ GDS-II integrity verified                                │
  │  ✓ Delivery package complete                                │
  │  ✓ Management authorization                                 │
  └─────────────────────────────────────────────────────────────┘
```

## 3. Detailed Tapeout Checklist

### 3.1 Design Verification Checklist

```
DESIGN VERIFICATION CHECKLIST:
═══════════════════════════════════════════════════════════════

┌────┬────────────────────────────────────┬──────┬──────────────┐
│ #  │ Item                               │ Sign │ Date         │
├────┼────────────────────────────────────┼──────┼──────────────┤
│    │ RTL VERIFICATION                    │      │              │
│ 1  │ All RTL modules coded              │      │              │
│ 2  │ RTL lint clean (SpyGlass/HAL)      │      │              │
│ 3  │ RTL simulation passing (all tests) │      │              │
│ 4  │ Functional coverage > 95%          │      │              │
│ 5  │ Code review completed              │      │              │
│ 6  │ CDC verification clean             │      │              │
│ 7  │ Formal property verification pass  │      │              │
│ 8  │ Assertion coverage > 90%           │      │              │
├────┼────────────────────────────────────┼──────┼──────────────┤
│    │ SYNTHESIS                          │      │              │
│ 9  │ Synthesis timing clean (all corners)│     │              │
│ 10 │ Area within budget (2.0 mm²)       │      │              │
│ 11 │ Power within budget (50 µW)        │      │              │
│ 12 │ RTL-to-netlist equivalence (LEC)   │      │              │
│ 13 │ Gate-level simulation passing      │      │              │
│ 14 │ Clock gating insertion verified    │      │              │
│ 15 │ DFT scan chain insertion complete   │      │              │
├────┼────────────────────────────────────┼──────┼──────────────┤
│    │ PHYSICAL DESIGN                    │      │              │
│ 16 │ Floorplan approved                 │      │              │
│ 17 │ Placement quality verified         │      │              │
│ 18 │ CTS clean (skew < 5 ns)           │      │              │
│ 19 │ Routing complete (no DRC)          │      │              │
│ 20 │ Post-route timing clean            │      │              │
│ 21 │ Post-route STA (all 8 corners)     │      │              │
│ 22 │ IR drop analysis passing           │      │              │
│ 23 │ EM analysis passing                │      │              │
│ 24 │ SI/crosstalk analysis passing      │      │              │
├────┼────────────────────────────────────┼──────┼──────────────┤
│    │ PHYSICAL VERIFICATION              │      │              │
│ 25 │ DRC clean (0 violations)           │      │              │
│ 26 │ LVS clean (full match)             │      │              │
│ 27 │ ERC clean (0 violations)           │      │              │
│ 28 │ Antenna check clean                │      │              │
│ 29 │ Density check passing              │      │              │
│ 30 │ Latch-up check passing             │      │              │
│ 31 │ Seal ring verification             │      │              │
│ 32 │ Bond pad verification              │      │              │
├────┼────────────────────────────────────┼──────┼──────────────┤
│    │ SAFETY VERIFICATION                │      │              │
│ 33 │ FMEA review completed              │      │              │
│ 34 │ Safety properties formally proven  │      │              │
│ 35 │ Fault injection testing passing    │      │              │
│ 36 │ Watchdog timer verified            │      │              │
│ 37 │ Dual-redundancy verified           │      │              │
│ 38 │ ECC functionality verified         │      │              │
│ 39 │ Safe-mode behavior verified        │      │              │
│ 40 │ Reset behavior verified            │      │              │
├────┼────────────────────────────────────┼──────┼──────────────┤
│    │ DFT VERIFICATION                   │      │              │
│ 41 │ Scan coverage > 95%               │      │              │
│ 42 │ Transition coverage > 90%         │      │              │
│ 43 │ MBIST coverage 100%               │      │              │
│ 44 │ Analog BIST coverage > 90%        │      │              │
│ 45 │ Test vectors generated             │      │              │
│ 46 │ Test time < 1 second              │      │              │
├────┼────────────────────────────────────┼──────┼──────────────┤
│    │ GDS-II AND DELIVERABLES            │      │              │
│ 47 │ GDS-II stream-out verified         │      │              │
│ 48 │ GDS-II DRC (post-stream) clean    │      │              │
│ 49 │ File integrity (SHA-256) generated │      │              │
│ 50 │ Delivery package complete          │      │              │
│ 51 │ Layer mapping verified             │      │              │
│ 52 │ Post-route netlist included        │      │              │
│ 53 │ SPEF files included (all corners)  │      │              │
│ 54 │ SDF files included                 │      │              │
│ 55 │ Bond diagram verified              │      │              │
└────┴────────────────────────────────────┴──────┴──────────────┘
```

### 3.2 Safety-Specific Checklist

```
SAFETY-CRITICAL TAPEOUT CHECKLIST (IEC 62304):
═══════════════════════════════════════════════════════════════

┌────┬────────────────────────────────────┬──────┬──────────────┐
│ #  │ Safety Requirement                 │ Sign │ Evidence     │
├────┼────────────────────────────────────┼──────┼──────────────┤
│ S1 │ No unreviewed RTL changes since    │      │              │
│    │ last safety review                 │      │              │
├────┼────────────────────────────────────┼──────┼──────────────┤
│ S2 │ All SF-xxx safety requirements     │      │              │
│    │ verified (see requirements matrix) │      │              │
├────┼────────────────────────────────────┼──────┼──────────────┤
│ S3 │ Dual-redundancy of output drivers  │      │              │
│    │ verified in layout (LVS clean)     │      │              │
├────┼────────────────────────────────────┼──────┼──────────────┤
│ S4 │ Watchdog timer independent clock   │      │              │
│    │ verified (CTS report)              │      │              │
├────┼────────────────────────────────────┼──────┼──────────────┤
│ S5 │ ECC on all safety-critical SRAM    │      │              │
│    │ verified (functional sim + layout) │      │              │
├────┼────────────────────────────────────┼──────┼──────────────┤
│ S6 │ TMR on all safety-critical FFs     │      │              │
│    │ verified (netlist + layout)        │      │              │
├────┼────────────────────────────────────┼──────┼──────────────┤
│ S7 │ Fault injection simulation passing │      │              │
│    │ (all single-point faults)          │      │              │
├────┼────────────────────────────────────┼──────┼──────────────┤
│ S8 │ Safe-mode behavior verified under  │      │              │
│    │ all fault conditions               │      │              │
├────┼────────────────────────────────────┼──────┼──────────────┤
│ S9 │ Reliability prediction meets 10-yr │      │              │
│    │ target (< 10 FIT)                 │      │              │
├────┼────────────────────────────────────┼──────┼──────────────┤
│ S10│ Derating rules applied to all      │      │              │
│    │ safety-critical cells              │      │              │
├────┼────────────────────────────────────┼──────┼──────────────┤
│ S11│ Test mode does not affect safety   │      │              │
│    │ (TEST_EN permanently disableable)  │      │              │
├────┼────────────────────────────────────┼──────┼──────────────┤
│ S12│ Safety design review minutes       │      │              │
│    │ attached                          │      │              │
└────┴────────────────────────────────────┴──────┴──────────────┘
```

## 4. Tapeout Signoff Sheet

```
iPACE-CHIP TAPEOUT SIGNOFF SHEET
═══════════════════════════════════════════════════════════════

  Design: iPACE-CHIP Implantable Pacemaker ASIC
  Version: v1.0
  Process: TSMC 180nm CMOS
  Die Size: 1.8 mm × 1.8 mm
  Package: Ceramic hermetic, 16-pin

  Tapeout Date: _____________
  Target Fab Date: _____________
  Expected Return: _____________

  ┌─────────────────────────────────────────────────────────────┐
  │  SIGNOFF SIGNATURES                                          │
  │                                                             │
  │  RTL Lead:          _____________  Date: _________         │
  │                     (Design complete, lint clean)           │
  │                                                             │
  │  Synthesis Lead:    _____________  Date: _________         │
  │                     (Timing/area/power met)                 │
  │                                                             │
  │  Physical Lead:     _____________  Date: _________         │
  │                     (DRC/LVS clean, layout complete)        │
  │                                                             │
  │  Verification Lead: _____________  Date: _________         │
  │                     (All simulations passing)               │
  │                                                             │
  │  DFT Lead:          _____________  Date: _________         │
  │                     (Scan/MBIST coverage met)               │
  │                                                             │
  │  Safety Lead:       _____________  Date: _________         │
  │                     (Safety requirements verified)          │
  │                                                             │
  │  Analog Lead:       _____________  Date: _________         │
  │                     (Analog blocks verified)                │
  │                                                             │
  │  Quality Lead:      _____________  Date: _________         │
  │                     (DHF documentation complete)            │
  │                                                             │
  │  Program Manager:   _____________  Date: _________         │
  │                     (Authorization to tapeout)              │
  │                                                             │
  │  VP Engineering:    _____________  Date: _________         │
  │                     (Executive authorization)               │
  └─────────────────────────────────────────────────────────────┘
```

## 5. Risk Assessment

```
Tapeout Risk Assessment:
═══════════════════════════════════════════════════════════════

  ┌──────────────────────┬────────────┬────────────┬──────────┐
  │ Risk                 │ Likelihood │ Impact     │ Mitigation│
  ├──────────────────────┼────────────┼────────────┼──────────┤
  │ Yield below 90%      │ Low        │ Medium     │ DFM opt  │
  │                      │            │            │ +10% die  │
  ├──────────────────────┼────────────┼────────────┼──────────┤
  │ Analog block spec    │ Medium     │ High       │ Post-sil │
  │ not met              │            │            │ tuning   │
  ├──────────────────────┼────────────┼────────────┼──────────┤
  │ SRAM single-cell     │ Low        │ High       │ ECC +    │
  │ failure              │            │            │ redundancy│
  ├──────────────────────┼────────────┼────────────┼──────────┤
  │ Package bond failure │ Low        │ Critical   │ 2× probe │
  │                      │            │            │ testing  │
  ├──────────────────────┼────────────┼────────────┼──────────┤
  │ ESD damage during    │ Low        │ High       │ ESD      │
  │ assembly             │            │            │ protocol │
  ├──────────────────────┼────────────┼────────────┼──────────┤
  │ Hermeticity failure  │ Low        │ Critical   │ MIL-STD  │
  │                      │            │            │ 1014 test│
  ├──────────────────────┼────────────┼────────────┼──────────┤
  │ Regulatory finding   │ Low        │ High       │ Complete │
  │ requiring re-spin    │            │            │ DHF      │
  └──────────────────────┴────────────┴────────────┴──────────┘

  Overall Risk Level: LOW
  Confidence in tapeout: HIGH
  Recommendation: PROCEED TO TAPEOUT
```

## 6. Post-Tapeout Plan

```
Post-Tapeout Activities:
═══════════════════════════════════════════════════════════════

  Week 1-2:  Foundry wafer processing begins
  Week 2-3:  Wafer probe testing (on-wafer electrical test)
  Week 3-4:  Wafer dicing and die sorting
  Week 4-5:  Wire bonding and package assembly
  Week 5-6:  Package-level electrical testing
  Week 6-7:  Burn-in testing (168 hours at 125°C)
  Week 7-8:  Final package testing and hermeticity check
  Week 8-9:  Sample delivery to design team
  Week 9-10: Silicon validation (characterization)
  Week 10-12: Full qualification testing
  Week 12+:  Design History File completion for regulatory

  Expected timeline from tapeout to qualified parts: 12 weeks
```

## 7. Summary

The iPACE-CHIP tapeout checklist covers 55 design verification items and 12 safety-
critical items, all requiring signoff from designated leads. Key summary:

1. **55 design verification items** — all must PASS
2. **12 safety-specific items** — all must PASS (IEC 62304 compliance)
3. **9 signoffs required** from RTL, synthesis, physical, verification, DFT, safety,
   analog, quality, and management leads
4. **Risk assessment**: LOW overall risk, HIGH confidence
5. **Post-tapeout plan**: 12 weeks to qualified silicon
6. **DHF integration**: Checklist forms part of FDA 510(k) submission package

---

*Previous: [Manufacturing Rules](../03-Manufacturing-Rules/manufacturing-rules.md)*
