# Grmhd — Resolution And Convergence Interview Questions and Answers

## Q1: What is resolution in GRMHD?
**A:** The number of cells per dimension per characteristic scale; the practical bottleneck of the whole discipline (realistic runs are 3D and huge).

## Q2: What is convergence?
**A:** The property that a resolution increase reduces solution error predictably; for turbulent flows, only STATISTICAL convergence is meaningful.

## Q3: What are the canonical metrics?
**A:** Accretion rate Mdot, stress alpha, MRI saturation amplitude, jet Poynting power - each quantified with its error bars vs resolution.

## Q4: How do you establish convergence for a turbulent run?
**A:** Run at 2 resolutions; compare time-and-space averaged spectra and the mean of Mdot: converge to a plateau within tolerance = accept.

## Q5: Why is Mdot noisy?
**A:** MHRIT turbulence is intermittent; measuring Mdot needs long time-averages (1000M+) to beat the noise - a common pitfall is premature claims.

## Q6: What is the resolution-MRI link?
**A:** Resolving the fastest-growing MRI wavelength ~ sqrt(v_A/Omega) regions dictates cell count in the disk midplane; under-resolution kills the dynamo and the turbulence dies.

## Q7: What does under-resolution falsely produce?
**A:** Absent turbulence -> smooth laminar accretion -> WRONG image; the death knell of a disk run is a grace-check at insufficient cells.

## Q8: What are the AMR convergence upsides?
**A:** Matching local resolution only where turbulence needs it; convergence criteria must be localized, not global (the disk vs jet have different zones).

## Q9: How do you quantify noise bounds?
**A:** Jackknife/block bootstrap on Mdot series gives error bars; compare them across resolutions - the bar's overlap is the honest statement.

## Q10: What is a 'converged quantity' vs a 'trend'?
**A:** Local turbulent snapshots never converge (chaos), only statistics do; always label figure captions with the averaged quantities.

## Q11: What is the cost of resolution doubling?
**A:** ~2^3-2^4x runtime (3D + dt from c/dx): the whole GRMHD field's economics live in this line.

## Q12: How do grids influence apparent convergence?
**A:** A log-spaced grid converges differently from uniform; state grids in convergence tests - otherwise 'resolution' claims are ambiguous.

## Q13: What does a resolution test on images give?
**A:** The ring profile stabilizes at moderate resolution (image features are macroscopic); the raytracer then sees the COVERGED state - a distinct advantage of images.

## Q14: What is a recommended pattern?
**A:** Run 2 medium grids to select a production grid, prove statistics converge on cheap runs, then commit the big one for output.

## Q15: What is the takeaway for the raytracer?
**A:** Feed the raytracer converged snapshots; the image quality belongs to the emitter's statistics, not the hole of the ray-solute - assert convergence first.

## Q16: What does resolution and convergence add to an astrophysical accretion flow model?
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need.

## Q17: Why do black-hole images rely on resolution and convergence?
**A:** The observed emission comes from hot magnetized plasma; resolution and convergence produces the density, temperature, velocity, and field data the raytracer converts to light.

## Q18: What is the conservative form in resolution and convergence?
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume resolution and convergence codes.

## Q19: How do Athena++ and HARM fit into resolution and convergence?
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding resolution and convergence means knowing what each code stores and how.

## Q20: What variables does resolution and convergence typically output?
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the resolution and convergence snapshot state.

## Q21: What is the biggest difficulty in resolution and convergence?
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes.

## Q22: How does resolution and convergence handle magnetic divergence?
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in resolution and convergence injects spurious forces and must be actively controlled.

## Q23: What coordinate system does a code like HARM use in resolution and convergence?
**A:** Logarithmically concentrated coordinates around the horizon; resolution and convergence interpretation of any Dump file requires reading that grid mapping.

## Q24: What is the resolution requirement of resolution and convergence?
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; resolution and convergence results are only physical at sufficient resolution.

## Q25: How does resolution and convergence produce the classic two-sided jets?
**A:** Magnetic field lines collimate outflows along the spin axis; jets in resolution and convergence are a natural outcome of magnetically-dominated coronae.

## Q26: What distinguishes an accretion 'state' in resolution and convergence?
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; resolution and convergence evolves between them statistically.

## Q27: How do you choose among resolution and convergence snapshots for rendering?
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant.

## Q28: What roles do floors and ceilings play in resolution and convergence?
**A:** Codes impose density/pressure floors to prevent negative states; resolution and convergence consumers must be aware these floors matter near the horizon.

## Q29: How is output frequency chosen in resolution and convergence?
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; resolution and convergence files are large so snapshot cadence is a trade-off.

## Q30: What is a typical resolution and convergence run cost?
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; resolution and convergence data availability often limits the renderer, not the physics.

## Q31: How do you check a resolution and convergence snapshot is physical?
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its resolution and convergence radiative output.

## Q32: What approximation do most resolution and convergence codes make about gravity?
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; resolution and convergence is therefore a test particle in a fixed background.

## Q33: How does the disk become so hot in resolution and convergence?
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; resolution and convergence emissivity relies on that heat.

## Q34: What happens when resolution and convergence resolution is doubled?
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates resolution and convergence robustness.

## Q35: What is the role of initial magnetic field topology in resolution and convergence?
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; resolution and convergence initial conditions are a science choice.

## Q36: What output formats should your resolution and convergence importer accept?
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; resolution and convergence importer accuracy is as important as the renderer itself.

## Q37: How do you map resolution and convergence cells to the raytracer grid?
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; resolution and convergence mapping must be consistent with the code's grid functions.

## Q38: What is the simplest first resolution and convergence test?
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average.

## Q39: How can missing physics show up in resolution and convergence images?
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; resolution and convergence images are calibrated against observed spectra before use.

## Q40: How can missing physics show up in resolution and convergence images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; resolution and convergence images are calibrated against observed spectra before use. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is the simplest first resolution and convergence test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How do you map resolution and convergence cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; resolution and convergence mapping must be consistent with the code's grid functions. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What output formats should your resolution and convergence importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; resolution and convergence importer accuracy is as important as the renderer itself. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What is the role of initial magnetic field topology in resolution and convergence - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; resolution and convergence initial conditions are a science choice. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What happens when resolution and convergence resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates resolution and convergence robustness. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does the disk become so hot in resolution and convergence - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; resolution and convergence emissivity relies on that heat. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What approximation do most resolution and convergence codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; resolution and convergence is therefore a test particle in a fixed background. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How do you check a resolution and convergence snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its resolution and convergence radiative output. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What is a typical resolution and convergence run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; resolution and convergence data availability often limits the renderer, not the physics. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How is output frequency chosen in resolution and convergence - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; resolution and convergence files are large so snapshot cadence is a trade-off. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What roles do floors and ceilings play in resolution and convergence - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; resolution and convergence consumers must be aware these floors matter near the horizon. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How do you choose among resolution and convergence snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What distinguishes an accretion 'state' in resolution and convergence - justify your answer with a concrete production example.
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; resolution and convergence evolves between them statistically. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does resolution and convergence produce the classic two-sided jets - justify your answer with a concrete production example.
**A:** Magnetic field lines collimate outflows along the spin axis; jets in resolution and convergence are a natural outcome of magnetically-dominated coronae. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What is the resolution requirement of resolution and convergence - justify your answer with a concrete production example.
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; resolution and convergence results are only physical at sufficient resolution. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What coordinate system does a code like HARM use in resolution and convergence - justify your answer with a concrete production example.
**A:** Logarithmically concentrated coordinates around the horizon; resolution and convergence interpretation of any Dump file requires reading that grid mapping. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How does resolution and convergence handle magnetic divergence - justify your answer with a concrete production example.
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in resolution and convergence injects spurious forces and must be actively controlled. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the biggest difficulty in resolution and convergence - justify your answer with a concrete production example.
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: What variables does resolution and convergence typically output - justify your answer with a concrete production example.
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the resolution and convergence snapshot state. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: How do Athena++ and HARM fit into resolution and convergence - justify your answer with a concrete production example.
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding resolution and convergence means knowing what each code stores and how. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What is the conservative form in resolution and convergence - justify your answer with a concrete production example.
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume resolution and convergence codes. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why do black-hole images rely on resolution and convergence - justify your answer with a concrete production example.
**A:** The observed emission comes from hot magnetized plasma; resolution and convergence produces the density, temperature, velocity, and field data the raytracer converts to light. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What does resolution and convergence add to an astrophysical accretion flow model - justify your answer with a concrete production example.
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What does resolution and convergence add to an astrophysical accretion flow model - justify your answer with a concrete production example.
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why do black-hole images rely on resolution and convergence - justify your answer with a concrete production example.
**A:** The observed emission comes from hot magnetized plasma; resolution and convergence produces the density, temperature, velocity, and field data the raytracer converts to light. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What is the conservative form in resolution and convergence - justify your answer with a concrete production example.
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume resolution and convergence codes. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How do Athena++ and HARM fit into resolution and convergence - justify your answer with a concrete production example.
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding resolution and convergence means knowing what each code stores and how. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What variables does resolution and convergence typically output - justify your answer with a concrete production example.
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the resolution and convergence snapshot state. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What is the biggest difficulty in resolution and convergence - justify your answer with a concrete production example.
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How does resolution and convergence handle magnetic divergence - justify your answer with a concrete production example.
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in resolution and convergence injects spurious forces and must be actively controlled. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What coordinate system does a code like HARM use in resolution and convergence - justify your answer with a concrete production example.
**A:** Logarithmically concentrated coordinates around the horizon; resolution and convergence interpretation of any Dump file requires reading that grid mapping. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What is the resolution requirement of resolution and convergence - justify your answer with a concrete production example.
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; resolution and convergence results are only physical at sufficient resolution. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does resolution and convergence produce the classic two-sided jets - justify your answer with a concrete production example.
**A:** Magnetic field lines collimate outflows along the spin axis; jets in resolution and convergence are a natural outcome of magnetically-dominated coronae. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What distinguishes an accretion 'state' in resolution and convergence - justify your answer with a concrete production example.
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; resolution and convergence evolves between them statistically. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How do you choose among resolution and convergence snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What roles do floors and ceilings play in resolution and convergence - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; resolution and convergence consumers must be aware these floors matter near the horizon. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: How is output frequency chosen in resolution and convergence - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; resolution and convergence files are large so snapshot cadence is a trade-off. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What is a typical resolution and convergence run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; resolution and convergence data availability often limits the renderer, not the physics. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How do you check a resolution and convergence snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its resolution and convergence radiative output. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What approximation do most resolution and convergence codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; resolution and convergence is therefore a test particle in a fixed background. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does the disk become so hot in resolution and convergence - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; resolution and convergence emissivity relies on that heat. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What happens when resolution and convergence resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates resolution and convergence robustness. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What is the role of initial magnetic field topology in resolution and convergence - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; resolution and convergence initial conditions are a science choice. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What output formats should your resolution and convergence importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; resolution and convergence importer accuracy is as important as the renderer itself. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How do you map resolution and convergence cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; resolution and convergence mapping must be consistent with the code's grid functions. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the simplest first resolution and convergence test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How can missing physics show up in resolution and convergence images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; resolution and convergence images are calibrated against observed spectra before use. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How can missing physics show up in resolution and convergence images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; resolution and convergence images are calibrated against observed spectra before use. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is the simplest first resolution and convergence test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How do you map resolution and convergence cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; resolution and convergence mapping must be consistent with the code's grid functions. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What output formats should your resolution and convergence importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; resolution and convergence importer accuracy is as important as the renderer itself. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What is the role of initial magnetic field topology in resolution and convergence - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; resolution and convergence initial conditions are a science choice. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What happens when resolution and convergence resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates resolution and convergence robustness. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does the disk become so hot in resolution and convergence - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; resolution and convergence emissivity relies on that heat. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What approximation do most resolution and convergence codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; resolution and convergence is therefore a test particle in a fixed background. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How do you check a resolution and convergence snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its resolution and convergence radiative output. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What is a typical resolution and convergence run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; resolution and convergence data availability often limits the renderer, not the physics. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How is output frequency chosen in resolution and convergence - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; resolution and convergence files are large so snapshot cadence is a trade-off. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What roles do floors and ceilings play in resolution and convergence - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; resolution and convergence consumers must be aware these floors matter near the horizon. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How do you choose among resolution and convergence snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying resolution and convergence in code review and regression tests keeps the whole pipeline trustworthy.
