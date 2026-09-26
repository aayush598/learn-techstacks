# Grmhd — Harm Overview Interview Questions and Answers

## Q1: What is HARM?
**A:** High-Accuracy Relativistic Magnetodynamics - a conservative, stationary-grid GRMHD code from Gammie/McKinney/Tóth, specialized for single black-hole disks.

## Q2: What is its grid?
**A:** Analytic coordinate systems (e.g., Boyer-Lindquist-based or 'financial horizontal' grids) with cell volume factors; a fixed hierarchy, no AMR.

## Q3: What is its numerics?
**A:** Finite volume conservative form, HLL-family solver, MUSCL/van Leer reconstruction, constrained transport for B, and the now-generic primitive-recovery p-W system.

## Q4: What is the 'p-W' inversion?
**A:** Noble et al.'s quartic method for conservative-to-primitive - the famous HARM recovery; robust with floors and fallbacks, at moderate cost.

## Q5: What makes HARM's disk runs cheap and canonical?
**A:** Single-hole setups, modest resolutions (e.g., 256^3), semi-analytic initial tori: the standard figures of accretion literature come from it.

## Q6: What are HARM's strengths?
**A:** Simplicity, robustness, correctness on disks, and the entire community's library of initial conditions (Fishbone-Moncrief tori) validates it.

## Q7: What are HARM's weaknesses?
**A:** No AMR, limited to its analytic grids, somewhat dated C, and a steep curve to modify boundaries vs tree codes.

## Q8: How does HARM handle the outer boundary?
**A:** Outflow + floor boundary beyond the 'hot zone'; the outer radius is a free parameter (often hundreds of M).

## Q9: How does HARM express the stress-energy?
**A:** Uses the covariant T^mu
u with the 3+1 projections; conservative variables remain D, S, tau, B - the same contract as Athena++ GRMHD.

## Q10: What is HARM's time integration?
**A:** Second-order RK (or predictor-corrector) with a CFL-limiting step: the standard explicit Godunov marching.

## Q11: How does HARM feed a raytracer?
**A:** Dumps provide (rho, u^i, B^i, p) on the grid; the raytracer interpolates them to sample emissivity along geodesics - the exact bridge this package provides.

## Q12: What is HARM's validation history?
**A:** The standard tests: Keplerian rotating disk, Bondi-like accretion, and the M87/Millennium initial-data suite - all documented and reproducible.

## Q13: What does HARM provide that's hard elsewhere?
**A:** A minimal, legible, single-file-flavored codebase - ideal for a custom raytracer pipeline to couple to and for teaching.

## Q14: What is HARM's status today?
**A:** Though old, its algorithms are industry standard and embodied in successors (KORAL, BHAC, Athena++ GRMHD); the legacy is as a reference semantics.

## Q15: What is the takeaway for this project?
**A:** Use HARM-style conservative / recovery / static-grid discipline as the reference (even if you run Athena++), because its clean semantics map 1:1 to the raytracer scene file.

## Q16: What does harm overview add to an astrophysical accretion flow model?
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need.

## Q17: Why do black-hole images rely on harm overview?
**A:** The observed emission comes from hot magnetized plasma; harm overview produces the density, temperature, velocity, and field data the raytracer converts to light.

## Q18: What is the conservative form in harm overview?
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume harm overview codes.

## Q19: How do Athena++ and HARM fit into harm overview?
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding harm overview means knowing what each code stores and how.

## Q20: What variables does harm overview typically output?
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the harm overview snapshot state.

## Q21: What is the biggest difficulty in harm overview?
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes.

## Q22: How does harm overview handle magnetic divergence?
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in harm overview injects spurious forces and must be actively controlled.

## Q23: What coordinate system does a code like HARM use in harm overview?
**A:** Logarithmically concentrated coordinates around the horizon; harm overview interpretation of any Dump file requires reading that grid mapping.

## Q24: What is the resolution requirement of harm overview?
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; harm overview results are only physical at sufficient resolution.

## Q25: How does harm overview produce the classic two-sided jets?
**A:** Magnetic field lines collimate outflows along the spin axis; jets in harm overview are a natural outcome of magnetically-dominated coronae.

## Q26: What distinguishes an accretion 'state' in harm overview?
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; harm overview evolves between them statistically.

## Q27: How do you choose among harm overview snapshots for rendering?
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant.

## Q28: What roles do floors and ceilings play in harm overview?
**A:** Codes impose density/pressure floors to prevent negative states; harm overview consumers must be aware these floors matter near the horizon.

## Q29: How is output frequency chosen in harm overview?
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; harm overview files are large so snapshot cadence is a trade-off.

## Q30: What is a typical harm overview run cost?
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; harm overview data availability often limits the renderer, not the physics.

## Q31: How do you check a harm overview snapshot is physical?
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its harm overview radiative output.

## Q32: What approximation do most harm overview codes make about gravity?
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; harm overview is therefore a test particle in a fixed background.

## Q33: How does the disk become so hot in harm overview?
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; harm overview emissivity relies on that heat.

## Q34: What happens when harm overview resolution is doubled?
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates harm overview robustness.

## Q35: What is the role of initial magnetic field topology in harm overview?
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; harm overview initial conditions are a science choice.

## Q36: What output formats should your harm overview importer accept?
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; harm overview importer accuracy is as important as the renderer itself.

## Q37: How do you map harm overview cells to the raytracer grid?
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; harm overview mapping must be consistent with the code's grid functions.

## Q38: What is the simplest first harm overview test?
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average.

## Q39: How can missing physics show up in harm overview images?
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; harm overview images are calibrated against observed spectra before use.

## Q40: How can missing physics show up in harm overview images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; harm overview images are calibrated against observed spectra before use. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is the simplest first harm overview test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How do you map harm overview cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; harm overview mapping must be consistent with the code's grid functions. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What output formats should your harm overview importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; harm overview importer accuracy is as important as the renderer itself. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What is the role of initial magnetic field topology in harm overview - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; harm overview initial conditions are a science choice. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What happens when harm overview resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates harm overview robustness. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does the disk become so hot in harm overview - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; harm overview emissivity relies on that heat. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What approximation do most harm overview codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; harm overview is therefore a test particle in a fixed background. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How do you check a harm overview snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its harm overview radiative output. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What is a typical harm overview run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; harm overview data availability often limits the renderer, not the physics. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How is output frequency chosen in harm overview - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; harm overview files are large so snapshot cadence is a trade-off. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What roles do floors and ceilings play in harm overview - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; harm overview consumers must be aware these floors matter near the horizon. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How do you choose among harm overview snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What distinguishes an accretion 'state' in harm overview - justify your answer with a concrete production example.
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; harm overview evolves between them statistically. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does harm overview produce the classic two-sided jets - justify your answer with a concrete production example.
**A:** Magnetic field lines collimate outflows along the spin axis; jets in harm overview are a natural outcome of magnetically-dominated coronae. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What is the resolution requirement of harm overview - justify your answer with a concrete production example.
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; harm overview results are only physical at sufficient resolution. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What coordinate system does a code like HARM use in harm overview - justify your answer with a concrete production example.
**A:** Logarithmically concentrated coordinates around the horizon; harm overview interpretation of any Dump file requires reading that grid mapping. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How does harm overview handle magnetic divergence - justify your answer with a concrete production example.
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in harm overview injects spurious forces and must be actively controlled. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the biggest difficulty in harm overview - justify your answer with a concrete production example.
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: What variables does harm overview typically output - justify your answer with a concrete production example.
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the harm overview snapshot state. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: How do Athena++ and HARM fit into harm overview - justify your answer with a concrete production example.
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding harm overview means knowing what each code stores and how. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What is the conservative form in harm overview - justify your answer with a concrete production example.
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume harm overview codes. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why do black-hole images rely on harm overview - justify your answer with a concrete production example.
**A:** The observed emission comes from hot magnetized plasma; harm overview produces the density, temperature, velocity, and field data the raytracer converts to light. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What does harm overview add to an astrophysical accretion flow model - justify your answer with a concrete production example.
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What does harm overview add to an astrophysical accretion flow model - justify your answer with a concrete production example.
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why do black-hole images rely on harm overview - justify your answer with a concrete production example.
**A:** The observed emission comes from hot magnetized plasma; harm overview produces the density, temperature, velocity, and field data the raytracer converts to light. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What is the conservative form in harm overview - justify your answer with a concrete production example.
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume harm overview codes. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How do Athena++ and HARM fit into harm overview - justify your answer with a concrete production example.
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding harm overview means knowing what each code stores and how. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What variables does harm overview typically output - justify your answer with a concrete production example.
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the harm overview snapshot state. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What is the biggest difficulty in harm overview - justify your answer with a concrete production example.
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How does harm overview handle magnetic divergence - justify your answer with a concrete production example.
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in harm overview injects spurious forces and must be actively controlled. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What coordinate system does a code like HARM use in harm overview - justify your answer with a concrete production example.
**A:** Logarithmically concentrated coordinates around the horizon; harm overview interpretation of any Dump file requires reading that grid mapping. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What is the resolution requirement of harm overview - justify your answer with a concrete production example.
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; harm overview results are only physical at sufficient resolution. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does harm overview produce the classic two-sided jets - justify your answer with a concrete production example.
**A:** Magnetic field lines collimate outflows along the spin axis; jets in harm overview are a natural outcome of magnetically-dominated coronae. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What distinguishes an accretion 'state' in harm overview - justify your answer with a concrete production example.
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; harm overview evolves between them statistically. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How do you choose among harm overview snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What roles do floors and ceilings play in harm overview - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; harm overview consumers must be aware these floors matter near the horizon. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: How is output frequency chosen in harm overview - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; harm overview files are large so snapshot cadence is a trade-off. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What is a typical harm overview run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; harm overview data availability often limits the renderer, not the physics. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How do you check a harm overview snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its harm overview radiative output. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What approximation do most harm overview codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; harm overview is therefore a test particle in a fixed background. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does the disk become so hot in harm overview - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; harm overview emissivity relies on that heat. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What happens when harm overview resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates harm overview robustness. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What is the role of initial magnetic field topology in harm overview - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; harm overview initial conditions are a science choice. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What output formats should your harm overview importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; harm overview importer accuracy is as important as the renderer itself. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How do you map harm overview cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; harm overview mapping must be consistent with the code's grid functions. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the simplest first harm overview test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How can missing physics show up in harm overview images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; harm overview images are calibrated against observed spectra before use. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How can missing physics show up in harm overview images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; harm overview images are calibrated against observed spectra before use. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is the simplest first harm overview test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How do you map harm overview cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; harm overview mapping must be consistent with the code's grid functions. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What output formats should your harm overview importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; harm overview importer accuracy is as important as the renderer itself. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What is the role of initial magnetic field topology in harm overview - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; harm overview initial conditions are a science choice. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What happens when harm overview resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates harm overview robustness. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does the disk become so hot in harm overview - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; harm overview emissivity relies on that heat. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What approximation do most harm overview codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; harm overview is therefore a test particle in a fixed background. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How do you check a harm overview snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its harm overview radiative output. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What is a typical harm overview run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; harm overview data availability often limits the renderer, not the physics. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How is output frequency chosen in harm overview - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; harm overview files are large so snapshot cadence is a trade-off. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What roles do floors and ceilings play in harm overview - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; harm overview consumers must be aware these floors matter near the horizon. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How do you choose among harm overview snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying harm overview in code review and regression tests keeps the whole pipeline trustworthy.
