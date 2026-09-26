# Grmhd — Mad Vs Sane Interview Questions and Answers

## Q1: What are MAD and SANE?
**A:** Two magnetic-accretion regimes: Magnetically Arrested Disk (flux-saturated near the hole) and Standard And Normal Evolution (weak flux, MRI-driven).

## Q2: What is the MAD state?
**A:** Accretion B saturates the horizon-adjacent field, the magnetic pressure halts radial inflow, plasma moves in streams around magnetic islands - strong jets, sharp flux.

## Q3: What is the SANE state?
**A:** The field stays MRI-turbulent and weak; the disk is quasi-Keplerian with benign jets - the standard thin-disk picture of the last decade.

## Q4: What is the MAD/SANE diagnostic?
**A:** phi_B ~ magnetic flux / sqrt(Mdot) threading the horizon: MAD phi ~ 15+, SANE phi ~ <10 (in suitable normalization) - a well-tested discriminator.

## Q5: How do you reach each state?
**A:** The initial poloidal-field strength and mass supply choose the attractor; MAD needs enough flux carried in, SANE preserves the weak seed - the IC matters.

## Q6: How does MAD change the image?
**A:** The magnetically-driven inner shell makes the image ring thinner, hotter (electron heating in current sheets) and gaze-strong - a sharp, compact crescent.

## Q7: How does MAD change variability?
**A:** Flux eruptions ('flux eruptions' / MAD cycles) produce periodic blowouts - bursts in the image ring brightness - a time-domain signature.

## Q8: How does spin interplay with MAD?
**A:** High spin + high flux -> efficient BZ jets and strong frame dragging; MAD is the regime in which spin power is most visible.

## Q9: What does SANE's image look like?
**A:** Broader ring, softer profile (more volume emission), brighter extended corona - the images differ enough that M87/Sgr*A* fits discriminate fits.

## Q10: Which is more realistic for M87?
**A:** The EHT finds images consistent with strong spin+flux -> MAD-family models fit best; Sgr A* is closer to moderate/SANE - the fits decide.

## Q11: How does the raytracer see the difference?
**A:** The emissivity field (rho, B, Te) looks different: SANE's volume-filling vs MAD's thin magnetized shell - the ring profile propagates into the render.

## Q12: What is the resolution burden?
**A:** MAD's inner-shell gradients need high inner resolution; its flux tubes are thin - resolution-convergence studies matter doubly there.

## Q13: How does MAD's accretion get into movies?
**A:** MAD's intermittent flux supply makes the disk flicker on 10-100M timescales - a distinct movie signature to look for when animating.

## Q14: What validation distinguishes the regimes?
**A:** Measure phi_B vs time: the attractor must hold; crossing signals a regime change mid-run (often the IC being wrong).

## Q15: What is the summary?
**A:** MAD vs SANE is a bifurcation in magnetic flux; your raytracer renders either state from its dumps - always label which regime the snapshot carries.

## Q16: What does mad vs sane add to an astrophysical accretion flow model?
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need.

## Q17: Why do black-hole images rely on mad vs sane?
**A:** The observed emission comes from hot magnetized plasma; mad vs sane produces the density, temperature, velocity, and field data the raytracer converts to light.

## Q18: What is the conservative form in mad vs sane?
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume mad vs sane codes.

## Q19: How do Athena++ and HARM fit into mad vs sane?
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding mad vs sane means knowing what each code stores and how.

## Q20: What variables does mad vs sane typically output?
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the mad vs sane snapshot state.

## Q21: What is the biggest difficulty in mad vs sane?
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes.

## Q22: How does mad vs sane handle magnetic divergence?
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in mad vs sane injects spurious forces and must be actively controlled.

## Q23: What coordinate system does a code like HARM use in mad vs sane?
**A:** Logarithmically concentrated coordinates around the horizon; mad vs sane interpretation of any Dump file requires reading that grid mapping.

## Q24: What is the resolution requirement of mad vs sane?
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; mad vs sane results are only physical at sufficient resolution.

## Q25: How does mad vs sane produce the classic two-sided jets?
**A:** Magnetic field lines collimate outflows along the spin axis; jets in mad vs sane are a natural outcome of magnetically-dominated coronae.

## Q26: What distinguishes an accretion 'state' in mad vs sane?
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; mad vs sane evolves between them statistically.

## Q27: How do you choose among mad vs sane snapshots for rendering?
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant.

## Q28: What roles do floors and ceilings play in mad vs sane?
**A:** Codes impose density/pressure floors to prevent negative states; mad vs sane consumers must be aware these floors matter near the horizon.

## Q29: How is output frequency chosen in mad vs sane?
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; mad vs sane files are large so snapshot cadence is a trade-off.

## Q30: What is a typical mad vs sane run cost?
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; mad vs sane data availability often limits the renderer, not the physics.

## Q31: How do you check a mad vs sane snapshot is physical?
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its mad vs sane radiative output.

## Q32: What approximation do most mad vs sane codes make about gravity?
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; mad vs sane is therefore a test particle in a fixed background.

## Q33: How does the disk become so hot in mad vs sane?
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; mad vs sane emissivity relies on that heat.

## Q34: What happens when mad vs sane resolution is doubled?
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates mad vs sane robustness.

## Q35: What is the role of initial magnetic field topology in mad vs sane?
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; mad vs sane initial conditions are a science choice.

## Q36: What output formats should your mad vs sane importer accept?
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; mad vs sane importer accuracy is as important as the renderer itself.

## Q37: How do you map mad vs sane cells to the raytracer grid?
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; mad vs sane mapping must be consistent with the code's grid functions.

## Q38: What is the simplest first mad vs sane test?
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average.

## Q39: How can missing physics show up in mad vs sane images?
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; mad vs sane images are calibrated against observed spectra before use.

## Q40: How can missing physics show up in mad vs sane images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; mad vs sane images are calibrated against observed spectra before use. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is the simplest first mad vs sane test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How do you map mad vs sane cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; mad vs sane mapping must be consistent with the code's grid functions. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What output formats should your mad vs sane importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; mad vs sane importer accuracy is as important as the renderer itself. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What is the role of initial magnetic field topology in mad vs sane - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; mad vs sane initial conditions are a science choice. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What happens when mad vs sane resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates mad vs sane robustness. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does the disk become so hot in mad vs sane - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; mad vs sane emissivity relies on that heat. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What approximation do most mad vs sane codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; mad vs sane is therefore a test particle in a fixed background. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How do you check a mad vs sane snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its mad vs sane radiative output. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What is a typical mad vs sane run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; mad vs sane data availability often limits the renderer, not the physics. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How is output frequency chosen in mad vs sane - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; mad vs sane files are large so snapshot cadence is a trade-off. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What roles do floors and ceilings play in mad vs sane - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; mad vs sane consumers must be aware these floors matter near the horizon. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How do you choose among mad vs sane snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What distinguishes an accretion 'state' in mad vs sane - justify your answer with a concrete production example.
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; mad vs sane evolves between them statistically. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does mad vs sane produce the classic two-sided jets - justify your answer with a concrete production example.
**A:** Magnetic field lines collimate outflows along the spin axis; jets in mad vs sane are a natural outcome of magnetically-dominated coronae. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What is the resolution requirement of mad vs sane - justify your answer with a concrete production example.
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; mad vs sane results are only physical at sufficient resolution. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What coordinate system does a code like HARM use in mad vs sane - justify your answer with a concrete production example.
**A:** Logarithmically concentrated coordinates around the horizon; mad vs sane interpretation of any Dump file requires reading that grid mapping. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How does mad vs sane handle magnetic divergence - justify your answer with a concrete production example.
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in mad vs sane injects spurious forces and must be actively controlled. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the biggest difficulty in mad vs sane - justify your answer with a concrete production example.
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: What variables does mad vs sane typically output - justify your answer with a concrete production example.
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the mad vs sane snapshot state. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: How do Athena++ and HARM fit into mad vs sane - justify your answer with a concrete production example.
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding mad vs sane means knowing what each code stores and how. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What is the conservative form in mad vs sane - justify your answer with a concrete production example.
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume mad vs sane codes. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why do black-hole images rely on mad vs sane - justify your answer with a concrete production example.
**A:** The observed emission comes from hot magnetized plasma; mad vs sane produces the density, temperature, velocity, and field data the raytracer converts to light. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What does mad vs sane add to an astrophysical accretion flow model - justify your answer with a concrete production example.
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What does mad vs sane add to an astrophysical accretion flow model - justify your answer with a concrete production example.
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why do black-hole images rely on mad vs sane - justify your answer with a concrete production example.
**A:** The observed emission comes from hot magnetized plasma; mad vs sane produces the density, temperature, velocity, and field data the raytracer converts to light. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What is the conservative form in mad vs sane - justify your answer with a concrete production example.
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume mad vs sane codes. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How do Athena++ and HARM fit into mad vs sane - justify your answer with a concrete production example.
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding mad vs sane means knowing what each code stores and how. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What variables does mad vs sane typically output - justify your answer with a concrete production example.
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the mad vs sane snapshot state. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What is the biggest difficulty in mad vs sane - justify your answer with a concrete production example.
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How does mad vs sane handle magnetic divergence - justify your answer with a concrete production example.
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in mad vs sane injects spurious forces and must be actively controlled. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What coordinate system does a code like HARM use in mad vs sane - justify your answer with a concrete production example.
**A:** Logarithmically concentrated coordinates around the horizon; mad vs sane interpretation of any Dump file requires reading that grid mapping. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What is the resolution requirement of mad vs sane - justify your answer with a concrete production example.
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; mad vs sane results are only physical at sufficient resolution. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does mad vs sane produce the classic two-sided jets - justify your answer with a concrete production example.
**A:** Magnetic field lines collimate outflows along the spin axis; jets in mad vs sane are a natural outcome of magnetically-dominated coronae. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What distinguishes an accretion 'state' in mad vs sane - justify your answer with a concrete production example.
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; mad vs sane evolves between them statistically. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How do you choose among mad vs sane snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What roles do floors and ceilings play in mad vs sane - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; mad vs sane consumers must be aware these floors matter near the horizon. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: How is output frequency chosen in mad vs sane - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; mad vs sane files are large so snapshot cadence is a trade-off. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What is a typical mad vs sane run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; mad vs sane data availability often limits the renderer, not the physics. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How do you check a mad vs sane snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its mad vs sane radiative output. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What approximation do most mad vs sane codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; mad vs sane is therefore a test particle in a fixed background. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does the disk become so hot in mad vs sane - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; mad vs sane emissivity relies on that heat. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What happens when mad vs sane resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates mad vs sane robustness. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What is the role of initial magnetic field topology in mad vs sane - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; mad vs sane initial conditions are a science choice. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What output formats should your mad vs sane importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; mad vs sane importer accuracy is as important as the renderer itself. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How do you map mad vs sane cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; mad vs sane mapping must be consistent with the code's grid functions. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the simplest first mad vs sane test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How can missing physics show up in mad vs sane images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; mad vs sane images are calibrated against observed spectra before use. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How can missing physics show up in mad vs sane images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; mad vs sane images are calibrated against observed spectra before use. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is the simplest first mad vs sane test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How do you map mad vs sane cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; mad vs sane mapping must be consistent with the code's grid functions. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What output formats should your mad vs sane importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; mad vs sane importer accuracy is as important as the renderer itself. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What is the role of initial magnetic field topology in mad vs sane - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; mad vs sane initial conditions are a science choice. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What happens when mad vs sane resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates mad vs sane robustness. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does the disk become so hot in mad vs sane - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; mad vs sane emissivity relies on that heat. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What approximation do most mad vs sane codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; mad vs sane is therefore a test particle in a fixed background. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How do you check a mad vs sane snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its mad vs sane radiative output. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What is a typical mad vs sane run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; mad vs sane data availability often limits the renderer, not the physics. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How is output frequency chosen in mad vs sane - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; mad vs sane files are large so snapshot cadence is a trade-off. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What roles do floors and ceilings play in mad vs sane - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; mad vs sane consumers must be aware these floors matter near the horizon. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How do you choose among mad vs sane snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying mad vs sane in code review and regression tests keeps the whole pipeline trustworthy.
