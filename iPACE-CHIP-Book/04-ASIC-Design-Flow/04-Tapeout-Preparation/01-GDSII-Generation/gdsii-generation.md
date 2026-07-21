# GDS-II Generation for iPACE-CHIP ASIC

## 1. Introduction

GDS-II (Graphic Data System II) is the industry-standard binary file format used to
describe the physical layout of an integrated circuit. The GDS-II stream file is the
ultimate output of the entire ASIC design flow — it contains every geometric shape,
layer assignment, and hierarchical structure that the foundry needs to manufacture the
iPACE-CHIP.

For a medical implantable device, GDS-II generation is a critical quality gate: any error
in the stream file directly translates to a defective chip that cannot be implanted in
a patient.

## 2. GDS-II Format

### 2.1 GDS-II Data Structure

```
GDS-II File Structure:
═══════════════════════════════════════════════════════════════

  GDS-II uses a hierarchical structure of cells:
  ┌─────────────────────────────────────────────────────────────┐
  │  GDS-II File                                                │
  │  ├── Header (library name, technology)                      │
  │  ├── Structure: ipace_chip_top                              │
  │  │   ├── Reference: u_clk_gen                               │
  │  │   ├── Reference: u_pacing_engine                         │
  │  │   │   ├── Reference: u_av_delay_ctrl                     │
  │  │   │   ├── Reference: u_refractory_timer                  │
  │  │   │   └── Geometry (gates, routing)                      │
  │  │   ├── Reference: u_sensing_engine                        │
  │  │   ├── Reference: u_analog_frontend                       │
  │  │   ├── Reference: u_output_driver_a                       │
  │  │   ├── Reference: u_output_driver_b                       │
  │  │   ├── Reference: u_watchdog_timer                        │
  │  │   ├── Reference: u_telemetry_unit                        │
  │  │   ├── Reference: u_param_store                           │
  │  │   ├── Reference: u_power_manager                         │
  │  │   └── Reference: u_pad_ring                              │
  │  └── End Library                                             │
  └─────────────────────────────────────────────────────────────┘

  Each cell contains:
    • Boundary box (bbox)
    • Geometric elements (boxes, paths, polygons)
    • Cell references (instances of other cells)
    • Layer assignments (technology-specific)
```

### 2.2 Layer Map

```
iPACE-CHIP GDS-II Layer Map:
═══════════════════════════════════════════════════════════════

  ┌──────────┬──────────────┬────────────────────────────────┐
  │ Layer #  │ Name         │ Usage                          │
  ├──────────┼──────────────┼────────────────────────────────┤
  │ 0        │ NWELL        │ N-well regions                 │
  │ 1        │ ACTIVE       │ Diffusion active area          │
  │ 2        │ POLY         │ Polysilicon (gate)             │
  │ 3        │ NIMPLANT     │ N-type implant select          │
  │ 4        │ PIMPLANT     │ P-type implant select          │
  │ 5        │ CONTACT      │ Contact cuts (poly to M1)      │
  │ 10       │ METAL1       │ Metal 1 (horizontal power)     │
  │ 11       │ VIA1         │ Via between M1 and M2          │
  │ 12       │ METAL2       │ Metal 2 (vertical signals)     │
  │ 13       │ VIA2         │ Via between M2 and M3          │
  │ 14       │ METAL3       │ Metal 3 (horizontal signals)   │
  │ 15       │ VIA3         │ Via between M3 and M4          │
  │ 16       │ METAL4       │ Metal 4 (vertical global)      │
  │ 17       │ VIA4         │ Via between M4 and M5          │
  │ 18       │ METAL5       │ Metal 5 (horizontal power)     │
  │ 19       │ VIA5         │ Via between M5 and M6          │
  │ 20       │ METAL6       │ Metal 6 (thick, power/induct)  │
  │ 25       │ MIM_CAP      │ Metal-insulator-metal cap      │
  │ 26       │ MIM_TOP      │ Top plate of MIM cap           │
  │ 30       │ ESD_NWELL    │ ESD protection N-well          │
  │ 31       │ ESD_DIFF     │ ESD diffusion                   │
  │ 40       │ PAD_OPEN     │ Bond pad opening                │
  │ 41       │ PASSIVATION  │ Passivation layer               │
  │ 50       │ FUSE         │ eFuse poly (one-time)           │
  │ 100      │ TEXT         │ Annotation text (non-manuf.)    │
  │ 200      │ BOUNDARY     │ Cell boundary box               │
  └──────────┴──────────────┴────────────────────────────────┘
```

## 3. GDS-II Generation Flow

### 3.1 Stream-Out Process

```
GDS-II Generation Flow:
═══════════════════════════════════════════════════════════════

  ┌─────────────────────────────────────────────────────────────┐
  │  1. PRE-STREAM VERIFICATION                                 │
  │     • DRC clean confirmation                                │
  │     • LVS clean confirmation                                │
  │     • ERC clean confirmation                                │
  │     • Density check passed                                  │
  │     • All signoff checks PASS                               │
  └───────────────────────────┬─────────────────────────────────┘
                              │
  ┌───────────────────────────v─────────────────────────────────┐
  │  2. DEF-to-GDS CONVERSION                                   │
  │     • Read DEF (Design Exchange Format)                     │
  │     • Merge with LEF (Library Exchange Format)              │
  │     • Apply technology rules                                │
  │     • Flatten or preserve hierarchy                         │
  └───────────────────────────┬─────────────────────────────────┘
                              │
  ┌───────────────────────────v─────────────────────────────────┐
  │  3. GDS-II STREAM-OUT                                       │
  │     • Tool: ICV (Synopsys), Calibre (Mentor), PVS (Cadence)│
  │     • Export all cells and geometry                          │
  │     • Apply layer map                                       │
  │     • Include cell hierarchy                                 │
  │     • Verify stream integrity                               │
  └───────────────────────────┬─────────────────────────────────┘
                              │
  ┌───────────────────────────v─────────────────────────────────┐
  │  4. POST-STREAM VERIFICATION                                │
  │     • GDS-II DRC (foundry-independent check)                │
  │     • Layer count verification                              │
  │     • Cell hierarchy verification                           │
  │     • File size check                                       │
  │     • MD5/SHA-256 checksum generation                       │
  └───────────────────────────┬─────────────────────────────────┘
                              │
  ┌───────────────────────────v─────────────────────────────────┐
  │  5. DELIVERY PREPARATION                                    │
  │     • Package GDS-II with supporting files                  │
  │     • Generate read-me with layer descriptions              │
  │     • Create tapeout checklist signoff                      │
  │     • Archive with version control                          │
  └─────────────────────────────────────────────────────────────┘
```

### 3.2 Stream-Out Commands

```tcl
#==========================================================================
# iPACE-CHIP GDS-II Stream-Out Script
#==========================================================================

# Tool: Synopsys IC Validator (ICV)
# or: Mentor Calibre GDSStream
# or: Cadence PVS

# Read final layout database
read_def ./layout/ipace_chip_top.def

# Read technology LEF
read_lef ./tech/tsmc180mw.lef
read_lef ./tech/tsmc180sp_cell.lef

# Stream out GDS-II
stream_out ./gdsii/ipace_chip_top.gds \
    -map_file ./tech/layer_map_gds.map \
    -lib_name iPACE_CHIP \
    -cells {ipace_chip_top} \
    -merge { \
        ./gds/sram_2kb_param.gds \
        ./gds/sram_2kb_data.gds \
        ./gds/rom_1kb.gds \
        ./gds/efuse_256.gds \
        ./gds/analog_lna.gds \
        ./gds/analog_vga.gds \
        ./gds/analog_bpf.gds \
        ./gds/analog_sar_adc.gds \
        ./gds/analog_output_drv.gds \
        ./gds/analog_bandgap.gds \
        ./gds/analog_ldo.gds \
        ./gds/analog_xosc.gds \
    } \
    -stripes 1 \
    -units 1000 \
    -mode ALL

# Post-stream verification
verify_drc -limit 1000 ./gdsii/ipace_chip_top.gds
verify_antenna ./gdsii/ipace_chip_top.gds
```

## 4. GDS-II Quality Checks

### 4.1 Post-Stream Verification

```
Post-Stream GDS-II Quality Checks:
═══════════════════════════════════════════════════════════════

  ┌─────────────────────────────────────┬──────┬──────────────┐
  │ Check                               │ Result│ Status      │
  ├─────────────────────────────────────┼──────┼──────────────┤
  │ DRC (GDS-level)                     │ 0    │ CLEAN        │
  │ Layer count matches LEF            │ 26/26│ MATCH        │
  │ Cell hierarchy depth               │ 5    │ OK            │
  │ Cell count                          │ 16,400│ OK           │
  │ Total geometry elements             │ 285,000│ OK          │
  │ File size                           │ 42 MB│ OK           │
  │ Hierarchy flattening test          │ PASS │ CLEAN        │
  │ Merge with analog GDS             │ PASS │ CLEAN        │
  │ Pad geometry verification          │ PASS │ CLEAN        │
  │ Seal ring completeness             │ PASS │ CLEAN        │
  ├─────────────────────────────────────┼──────┼──────────────┤
  │ GDS-II QUALITY STATUS               │ —    │ PASS         │
  └─────────────────────────────────────┴──────┴──────────────┘
```

### 4.2 File Integrity

```
GDS-II File Integrity:
═══════════════════════════════════════════════════════════════

  File: ipace_chip_top.gds
  Size: 42,156,832 bytes (40.2 MB)
  MD5:   a1b2c3d4e5f6... (generated at stream-out time)
  SHA-256: 7f8a9b0c... (for regulatory traceability)

  Format Version: 6.0
  Units: 1000 (database units per micron)
  Coordinate Range: X [0, 1800000], Y [0, 1800000]
                    (in database units, = 0 to 1800.0 µm)

  Cell Hierarchy:
  ┌────────────────────────────────────────────────────────────┐
  │  ipace_chip_top                                            │
  │    ├─ u_clk_gen (leaf)                                    │
  │    ├─ u_pacing_engine                                      │
  │    │   ├─ u_state_reg_tmr (x3 copies)                     │
  │    │   └─ u_rate_counter                                   │
  │    ├─ u_sensing_engine                                     │
  │    ├─ u_analog_frontend                                    │
  │    │   ├─ u_lna (leaf, custom layout)                      │
  │    │   ├─ u_vga (leaf)                                     │
  │    │   └─ u_sar_adc (leaf)                                 │
  │    ├─ u_output_driver_a (leaf)                             │
  │    ├─ u_output_driver_b (leaf)                             │
  │    ├─ u_watchdog_timer                                     │
  │    ├─ u_telemetry_unit                                     │
  │    │   ├─ u_aes128 (leaf)                                  │
  │    │   └─ u_crc16 (leaf)                                   │
  │    ├─ u_param_store                                        │
  │    │   ├─ u_sram_param (SRAM macro, GDS merged)           │
  │    │   └─ u_sram_data (SRAM macro)                         │
  │    ├─ u_power_manager                                      │
  │    └─ u_pad_ring                                           │
  │        ├─ u_io_cell[0..15] (I/O cells)                     │
  │        └─ u_esd_clamp[0..3] (ESD cells)                    │
  └────────────────────────────────────────────────────────────┘
```

## 5. Tapeout Deliverables

```
iPACE-CHIP Tapeout Delivery Package:
═══════════════════════════════════════════════════════════════

  ┌─────────────────────────────────────────────────────────────┐
  │  TAPEOUT DELIVERABLES                                        │
  │                                                             │
  │  GDS-II FILES:                                              │
  │    ipace_chip_top.gds          (42 MB, final design)       │
  │    ipace_chip_top_flat.gds     (optional, flattened)       │
  │                                                             │
  │  NETLIST FILES:                                             │
  │    ipace_chip_top.v            (post-route netlist)        │
  │    ipace_chip_top.vhdl         (if requested by foundry)   │
  │                                                             │
  │  TIMING FILES:                                              │
  │    ipace_chip_top_tt.sdf       (typical corner)            │
  │    ipace_chip_top_ss.sdf       (slow corner)               │
  │    ipace_chip_top_ff.sdf       (fast corner)               │
  │    ipace_chip_top_aged.sdf     (10-year aged corner)       │
  │                                                             │
  │  PHYSICAL FILES:                                            │
  │    ipace_chip_top.def          (placement/routing)         │
  │    ipace_chip_top.tt SPEF      (parasitic extraction)      │
  │    ipace_chip_top.ss.spef      (slow corner parasitics)    │
  │                                                             │
  │  DOCUMENTATION:                                             │
  │    layer_map_gds.map           (GDS layer mapping)         │
  │    read_me.txt                 (tapeout notes)             │
  │    signoff_checklist.pdf       (all signoff approvals)     │
  │    reliability_report.pdf      (10-year lifetime analysis) │
  │    bond_diagram.pdf            (pad-to-package mapping)    │
  │                                                             │
  │  CHECKSUMS:                                                 │
  │    checksums.md5               (MD5 for all files)         │
  │    checksums.sha256            (SHA-256 for all files)     │
  │                                                             │
  │  Total package size: ~120 MB                                │
  └─────────────────────────────────────────────────────────────┘
```

## 6. GDS-II Archive and Versioning

```
Version Control for GDS-II:
═══════════════════════════════════════════════════════════════

  Naming Convention:
    ipace_chip_<version>_<date>_<corner>.gds

    Example: ipace_chip_v1.0_20240115_signoff.gds

  Version History:
  ┌────────┬───────────┬────────────────────────────────────┐
  │ Version│ Date      │ Changes                            │
  ├────────┼───────────┼────────────────────────────────────┤
  │ v0.1   │ 2023-06-01│ Initial floorplan                  │
  │ v0.5   │ 2023-09-15│ Post-placement                     │
  │ v0.8   │ 2023-11-20│ Post-CTS                           │
  │ v0.9   │ 2023-12-15│ Post-routing (DRC 12 violations)  │
  │ v0.91  │ 2023-12-20│ DRC fix pass 1 (3 violations fixed)│
  │ v0.92  │ 2024-01-05│ DRC fix pass 2 (0 violations)      │
  │ v1.0   │ 2024-01-15│ SIGNOFF RELEASE (all checks clean) │
  └────────┴───────────┴────────────────────────────────────┘

  Archive Location:
    /design/iPACE CHIP/gdsii/<version>/
    /design/iPACE CHIP/gdsii/release/   (symlink to latest)
    /design/iPACE CHIP/backup/<date>/   (nightly backups)
```

## 7. Summary

The iPACE-CHIP GDS-II represents the culmination of the entire ASIC design flow:

1. **42 MB GDS-II file** containing all physical layout information
2. **26 layers** mapped to TSMC 180nm technology
3. **16,400 cells** in hierarchical structure (depth = 5)
4. **Zero DRC violations** at stream-out time
5. **Complete delivery package** with netlists, timing, and documentation
6. **SHA-256 checksums** for regulatory traceability

---

*Previous: [Signoff](../../03-Backend-Design/04-Signoff/signoff.md)*
