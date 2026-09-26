# Grmhd — Jets And Outflows Interview Questions and Answers

## Q1: What are jets?
**A:** Relativistic outflows of plasma + Poynting flux along the poles, launched magnetocentrifugally from the spinning hole/disk - visible as the luminous spine rays in renderings.

## Q2: How are they launched?
**A:** Blandford-Znajek (BZ): spin power extracted from the hole via the magnetic field's spinning tube; Blandford-Payne (BP): centrifugal sling from the disk.

## Q3: What is the Poynting-flux jet?
**A:** Energy flux S ~ B^2/8pi * Omega accelerating plasma against the weak matter - the jet is magnetically-dominated power (low matter, high field).

## Q4: What distinguishes a BZ from a BP jet?
**A:** BZ from the ergosphere/horizon (proportional to a^2, efficient at high spin), BP from the disk itself (proportional to rotation); observed jets blend both.

## Q5: How does MAD vs SANE set jets?
**A:** MAD threads the horizon with strong poloidal field -> powerful jets; SANE is weaker-field -> weak jets - the spin+flux combo sets the jet's power.

## Q6: What is the jet's collimation?
**A:** Magnetic tension confines; external pressure governs the opening; GRMHD computes the evolutionary collimation directly (the slender/then-parabolic shape).

## Q7: How does the jet appear in a raytripple?
**A:** The jet's low-density high-velocity plasma emits weakly in synchrotron; images show it as the outer brightness/Doppler-boosted lobes around the funnel.

## Q8: What is the funnel?
**A:** The evacuated polar region near the hole where plasma density is at floors and the field dominates - the visual 'hidden region' the jet lives in.

## Q9: What is the relativistic speed in jets?
**A:** Jet v ~ 0.6-0.99 c via ideal MHD acceleration; beaming hence hugely contrasts the approaching vs receding jet — a striking asymmetry.

## Q10: What is the mass-loading issue?
**A:** Actual jet plasma comes from pair production, wind entrainment, magnetopause; ideal MHD with floors creates artificial loading - a known caveat for jet densities.

## Q11: How does spin power drive observations?
**A:** BZ power ~ a^2 Mdot c^2-ish; measuring jet power effectively measures a - a link the raytracer films directly through brightness asymmetry.

## Q12: What validation checks jets?
**A:** Construct a force-free field + rotating frame: the Poynting flux matches the analytic BZ formula; jet opening/beam speed follow the field geometry.

## Q13: What do movies show about jets?
**A:** The jet 'sloshes' as turbulent spikes load it; variability in the spine is a real diagnostic of disk/jet coupling - frame-to-frame features.

## Q14: What does a renderer's jet need physically?
**A:** Low-density floor with emissivity from synchrotron + beaming; the emission's polarization and shift trace the field - treat it as the field's tracker.

## Q15: What is the summary?
**A:** Jets are magnetically-driven outflows; your raytracer samples their synchrotron beaming - dominant contrast near the poles, strongest spin-dependence in the frame-to-frame morphology.

## Q16: What does jets and outflows add to an astrophysical accretion flow model?
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need.

## Q17: Why do black-hole images rely on jets and outflows?
**A:** The observed emission comes from hot magnetized plasma; jets and outflows produces the density, temperature, velocity, and field data the raytracer converts to light.

## Q18: What is the conservative form in jets and outflows?
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume jets and outflows codes.

## Q19: How do Athena++ and HARM fit into jets and outflows?
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding jets and outflows means knowing what each code stores and how.

## Q20: What variables does jets and outflows typically output?
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the jets and outflows snapshot state.

## Q21: What is the biggest difficulty in jets and outflows?
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes.

## Q22: How does jets and outflows handle magnetic divergence?
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in jets and outflows injects spurious forces and must be actively controlled.

## Q23: What coordinate system does a code like HARM use in jets and outflows?
**A:** Logarithmically concentrated coordinates around the horizon; jets and outflows interpretation of any Dump file requires reading that grid mapping.

## Q24: What is the resolution requirement of jets and outflows?
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; jets and outflows results are only physical at sufficient resolution.

## Q25: How does jets and outflows produce the classic two-sided jets?
**A:** Magnetic field lines collimate outflows along the spin axis; jets in jets and outflows are a natural outcome of magnetically-dominated coronae.

## Q26: What distinguishes an accretion 'state' in jets and outflows?
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; jets and outflows evolves between them statistically.

## Q27: How do you choose among jets and outflows snapshots for rendering?
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant.

## Q28: What roles do floors and ceilings play in jets and outflows?
**A:** Codes impose density/pressure floors to prevent negative states; jets and outflows consumers must be aware these floors matter near the horizon.

## Q29: How is output frequency chosen in jets and outflows?
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; jets and outflows files are large so snapshot cadence is a trade-off.

## Q30: What is a typical jets and outflows run cost?
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; jets and outflows data availability often limits the renderer, not the physics.

## Q31: How do you check a jets and outflows snapshot is physical?
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its jets and outflows radiative output.

## Q32: What approximation do most jets and outflows codes make about gravity?
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; jets and outflows is therefore a test particle in a fixed background.

## Q33: How does the disk become so hot in jets and outflows?
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; jets and outflows emissivity relies on that heat.

## Q34: What happens when jets and outflows resolution is doubled?
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates jets and outflows robustness.

## Q35: What is the role of initial magnetic field topology in jets and outflows?
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; jets and outflows initial conditions are a science choice.

## Q36: What output formats should your jets and outflows importer accept?
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; jets and outflows importer accuracy is as important as the renderer itself.

## Q37: How do you map jets and outflows cells to the raytracer grid?
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; jets and outflows mapping must be consistent with the code's grid functions.

## Q38: What is the simplest first jets and outflows test?
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average.

## Q39: How can missing physics show up in jets and outflows images?
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; jets and outflows images are calibrated against observed spectra before use.

## Q40: How can missing physics show up in jets and outflows images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; jets and outflows images are calibrated against observed spectra before use. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is the simplest first jets and outflows test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How do you map jets and outflows cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; jets and outflows mapping must be consistent with the code's grid functions. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What output formats should your jets and outflows importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; jets and outflows importer accuracy is as important as the renderer itself. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What is the role of initial magnetic field topology in jets and outflows - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; jets and outflows initial conditions are a science choice. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What happens when jets and outflows resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates jets and outflows robustness. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does the disk become so hot in jets and outflows - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; jets and outflows emissivity relies on that heat. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What approximation do most jets and outflows codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; jets and outflows is therefore a test particle in a fixed background. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How do you check a jets and outflows snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its jets and outflows radiative output. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What is a typical jets and outflows run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; jets and outflows data availability often limits the renderer, not the physics. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How is output frequency chosen in jets and outflows - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; jets and outflows files are large so snapshot cadence is a trade-off. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What roles do floors and ceilings play in jets and outflows - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; jets and outflows consumers must be aware these floors matter near the horizon. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How do you choose among jets and outflows snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What distinguishes an accretion 'state' in jets and outflows - justify your answer with a concrete production example.
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; jets and outflows evolves between them statistically. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does jets and outflows produce the classic two-sided jets - justify your answer with a concrete production example.
**A:** Magnetic field lines collimate outflows along the spin axis; jets in jets and outflows are a natural outcome of magnetically-dominated coronae. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What is the resolution requirement of jets and outflows - justify your answer with a concrete production example.
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; jets and outflows results are only physical at sufficient resolution. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What coordinate system does a code like HARM use in jets and outflows - justify your answer with a concrete production example.
**A:** Logarithmically concentrated coordinates around the horizon; jets and outflows interpretation of any Dump file requires reading that grid mapping. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How does jets and outflows handle magnetic divergence - justify your answer with a concrete production example.
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in jets and outflows injects spurious forces and must be actively controlled. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the biggest difficulty in jets and outflows - justify your answer with a concrete production example.
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: What variables does jets and outflows typically output - justify your answer with a concrete production example.
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the jets and outflows snapshot state. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: How do Athena++ and HARM fit into jets and outflows - justify your answer with a concrete production example.
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding jets and outflows means knowing what each code stores and how. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What is the conservative form in jets and outflows - justify your answer with a concrete production example.
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume jets and outflows codes. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why do black-hole images rely on jets and outflows - justify your answer with a concrete production example.
**A:** The observed emission comes from hot magnetized plasma; jets and outflows produces the density, temperature, velocity, and field data the raytracer converts to light. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What does jets and outflows add to an astrophysical accretion flow model - justify your answer with a concrete production example.
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What does jets and outflows add to an astrophysical accretion flow model - justify your answer with a concrete production example.
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why do black-hole images rely on jets and outflows - justify your answer with a concrete production example.
**A:** The observed emission comes from hot magnetized plasma; jets and outflows produces the density, temperature, velocity, and field data the raytracer converts to light. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What is the conservative form in jets and outflows - justify your answer with a concrete production example.
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume jets and outflows codes. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How do Athena++ and HARM fit into jets and outflows - justify your answer with a concrete production example.
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding jets and outflows means knowing what each code stores and how. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What variables does jets and outflows typically output - justify your answer with a concrete production example.
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the jets and outflows snapshot state. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What is the biggest difficulty in jets and outflows - justify your answer with a concrete production example.
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How does jets and outflows handle magnetic divergence - justify your answer with a concrete production example.
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in jets and outflows injects spurious forces and must be actively controlled. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What coordinate system does a code like HARM use in jets and outflows - justify your answer with a concrete production example.
**A:** Logarithmically concentrated coordinates around the horizon; jets and outflows interpretation of any Dump file requires reading that grid mapping. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What is the resolution requirement of jets and outflows - justify your answer with a concrete production example.
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; jets and outflows results are only physical at sufficient resolution. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does jets and outflows produce the classic two-sided jets - justify your answer with a concrete production example.
**A:** Magnetic field lines collimate outflows along the spin axis; jets in jets and outflows are a natural outcome of magnetically-dominated coronae. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What distinguishes an accretion 'state' in jets and outflows - justify your answer with a concrete production example.
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; jets and outflows evolves between them statistically. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How do you choose among jets and outflows snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What roles do floors and ceilings play in jets and outflows - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; jets and outflows consumers must be aware these floors matter near the horizon. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: How is output frequency chosen in jets and outflows - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; jets and outflows files are large so snapshot cadence is a trade-off. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What is a typical jets and outflows run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; jets and outflows data availability often limits the renderer, not the physics. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How do you check a jets and outflows snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its jets and outflows radiative output. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What approximation do most jets and outflows codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; jets and outflows is therefore a test particle in a fixed background. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does the disk become so hot in jets and outflows - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; jets and outflows emissivity relies on that heat. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What happens when jets and outflows resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates jets and outflows robustness. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What is the role of initial magnetic field topology in jets and outflows - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; jets and outflows initial conditions are a science choice. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What output formats should your jets and outflows importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; jets and outflows importer accuracy is as important as the renderer itself. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How do you map jets and outflows cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; jets and outflows mapping must be consistent with the code's grid functions. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the simplest first jets and outflows test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How can missing physics show up in jets and outflows images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; jets and outflows images are calibrated against observed spectra before use. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How can missing physics show up in jets and outflows images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; jets and outflows images are calibrated against observed spectra before use. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is the simplest first jets and outflows test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How do you map jets and outflows cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; jets and outflows mapping must be consistent with the code's grid functions. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What output formats should your jets and outflows importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; jets and outflows importer accuracy is as important as the renderer itself. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What is the role of initial magnetic field topology in jets and outflows - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; jets and outflows initial conditions are a science choice. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What happens when jets and outflows resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates jets and outflows robustness. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does the disk become so hot in jets and outflows - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; jets and outflows emissivity relies on that heat. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What approximation do most jets and outflows codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; jets and outflows is therefore a test particle in a fixed background. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How do you check a jets and outflows snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its jets and outflows radiative output. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What is a typical jets and outflows run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; jets and outflows data availability often limits the renderer, not the physics. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How is output frequency chosen in jets and outflows - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; jets and outflows files are large so snapshot cadence is a trade-off. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What roles do floors and ceilings play in jets and outflows - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; jets and outflows consumers must be aware these floors matter near the horizon. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How do you choose among jets and outflows snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying jets and outflows in code review and regression tests keeps the whole pipeline trustworthy.
