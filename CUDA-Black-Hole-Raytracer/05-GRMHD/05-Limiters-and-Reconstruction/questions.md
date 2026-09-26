# Grmhd — Limiters And Reconstruction Interview Questions and Answers

## Q1: What is reconstruction?
**A:** Building sub-cell left/right states from cell averages before feeding the Riemann solver, enabling second/higher order accuracy beyond flat first order.

## Q2: What is a limiter?
**A:** A nonlinear controller that clamps reconstructed slopes to avoid new extrema/oscillations near shocks - the TVD/MUSCL family (minmod, van Leer, MC).

## Q3: What is the minmod limiter?
**A:** The most diffusive common choice: slope = the CommonReflection of the left/right one-sided differences; maximal stability at cost of smearing.

## Q4: What is the van Leer (MUSCL) reconstruction?
**A:** Monotonic piecewise linear reconstruction with a harmonic-mean slope - sharper contacts than minmod while remaining TVD.

## Q5: What is the MC (monotonized central) limiter?
**A:** A blend of the central and minmod stencils - sharper than van Leer-ish variants with modest oscillation cost.

## Q6: What is the piecewise parabolic method (PPM)?
**A:** Higher-order (3rd) reconstruction with contact steepening; used in Athena++ for high-resolution shock capturing - costlier but crisper on disks.

## Q7: What is the role of the limiter in a disk simulation?
**A:** Disk turbulence is smooth, jets carry shocks: a limiter must not damp turbulence (over-diffuse) nor ring on shocks (under-limited) - the classic tradeoff.

## Q8: What is 'shock-steepening vs turbulence' balance?
**A:** Steep limiters sharpen shocks but also steepen numerical noise in a turbulent column; the balance is tuned by the resolve-in-time test.

## Q9: How is reconstruction implemented efficiently?
**A:** Per-direction passes with pre-staged face stencils; AVX gathers across cells and memory-order fuses with the flux kernel.

## Q10: What is the flux error of first order vs MUSCL?
**A:** First order adds numerical dissipation ~ c dx; MUSCL reduces it to ~ (Delta)^2 - visibly blunting the jet/disc contrast at moderate resolution.

## Q11: What is the 'positive' reconstruction constraint?
**A:** Reconstructed density/pressure must stay positive even near floors - the limiter's clamp is designed for that failure mode.

## Q12: How does reconstruction interplay with the CFL?
**A:** The effective scheme signal speed gets limited (MUSCL face slope constrains time step); coupled with the solver, this sets global dt.

## Q13: What is a residual-based limiter?
**A:** Clamps based on the residual smoothness estimator (like the 'Barth-Jespersen' in unstructured) - adaptive by region.

## Q14: What validation isolates reconstruction?
**A:** The advection of a smooth Gaussian: amplitude error order ~ 2 for MUSCL (no limiter); through-flow of a contact: minmod spreads > MC -> verifiable QoI.

## Q15: What does the visualization look for?
**A:** The jet spine sharpness, the disk's vorticity cascade, and the absence of the staircase (staircase = poor reconstruction) around shocks.

## Q16: What does limiters and reconstruction add to an astrophysical accretion flow model?
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need.

## Q17: Why do black-hole images rely on limiters and reconstruction?
**A:** The observed emission comes from hot magnetized plasma; limiters and reconstruction produces the density, temperature, velocity, and field data the raytracer converts to light.

## Q18: What is the conservative form in limiters and reconstruction?
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume limiters and reconstruction codes.

## Q19: How do Athena++ and HARM fit into limiters and reconstruction?
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding limiters and reconstruction means knowing what each code stores and how.

## Q20: What variables does limiters and reconstruction typically output?
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the limiters and reconstruction snapshot state.

## Q21: What is the biggest difficulty in limiters and reconstruction?
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes.

## Q22: How does limiters and reconstruction handle magnetic divergence?
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in limiters and reconstruction injects spurious forces and must be actively controlled.

## Q23: What coordinate system does a code like HARM use in limiters and reconstruction?
**A:** Logarithmically concentrated coordinates around the horizon; limiters and reconstruction interpretation of any Dump file requires reading that grid mapping.

## Q24: What is the resolution requirement of limiters and reconstruction?
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; limiters and reconstruction results are only physical at sufficient resolution.

## Q25: How does limiters and reconstruction produce the classic two-sided jets?
**A:** Magnetic field lines collimate outflows along the spin axis; jets in limiters and reconstruction are a natural outcome of magnetically-dominated coronae.

## Q26: What distinguishes an accretion 'state' in limiters and reconstruction?
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; limiters and reconstruction evolves between them statistically.

## Q27: How do you choose among limiters and reconstruction snapshots for rendering?
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant.

## Q28: What roles do floors and ceilings play in limiters and reconstruction?
**A:** Codes impose density/pressure floors to prevent negative states; limiters and reconstruction consumers must be aware these floors matter near the horizon.

## Q29: How is output frequency chosen in limiters and reconstruction?
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; limiters and reconstruction files are large so snapshot cadence is a trade-off.

## Q30: What is a typical limiters and reconstruction run cost?
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; limiters and reconstruction data availability often limits the renderer, not the physics.

## Q31: How do you check a limiters and reconstruction snapshot is physical?
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its limiters and reconstruction radiative output.

## Q32: What approximation do most limiters and reconstruction codes make about gravity?
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; limiters and reconstruction is therefore a test particle in a fixed background.

## Q33: How does the disk become so hot in limiters and reconstruction?
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; limiters and reconstruction emissivity relies on that heat.

## Q34: What happens when limiters and reconstruction resolution is doubled?
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates limiters and reconstruction robustness.

## Q35: What is the role of initial magnetic field topology in limiters and reconstruction?
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; limiters and reconstruction initial conditions are a science choice.

## Q36: What output formats should your limiters and reconstruction importer accept?
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; limiters and reconstruction importer accuracy is as important as the renderer itself.

## Q37: How do you map limiters and reconstruction cells to the raytracer grid?
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; limiters and reconstruction mapping must be consistent with the code's grid functions.

## Q38: What is the simplest first limiters and reconstruction test?
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average.

## Q39: How can missing physics show up in limiters and reconstruction images?
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; limiters and reconstruction images are calibrated against observed spectra before use.

## Q40: How can missing physics show up in limiters and reconstruction images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; limiters and reconstruction images are calibrated against observed spectra before use. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is the simplest first limiters and reconstruction test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How do you map limiters and reconstruction cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; limiters and reconstruction mapping must be consistent with the code's grid functions. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What output formats should your limiters and reconstruction importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; limiters and reconstruction importer accuracy is as important as the renderer itself. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What is the role of initial magnetic field topology in limiters and reconstruction - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; limiters and reconstruction initial conditions are a science choice. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What happens when limiters and reconstruction resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates limiters and reconstruction robustness. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does the disk become so hot in limiters and reconstruction - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; limiters and reconstruction emissivity relies on that heat. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What approximation do most limiters and reconstruction codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; limiters and reconstruction is therefore a test particle in a fixed background. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How do you check a limiters and reconstruction snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its limiters and reconstruction radiative output. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What is a typical limiters and reconstruction run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; limiters and reconstruction data availability often limits the renderer, not the physics. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How is output frequency chosen in limiters and reconstruction - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; limiters and reconstruction files are large so snapshot cadence is a trade-off. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What roles do floors and ceilings play in limiters and reconstruction - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; limiters and reconstruction consumers must be aware these floors matter near the horizon. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How do you choose among limiters and reconstruction snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What distinguishes an accretion 'state' in limiters and reconstruction - justify your answer with a concrete production example.
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; limiters and reconstruction evolves between them statistically. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does limiters and reconstruction produce the classic two-sided jets - justify your answer with a concrete production example.
**A:** Magnetic field lines collimate outflows along the spin axis; jets in limiters and reconstruction are a natural outcome of magnetically-dominated coronae. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What is the resolution requirement of limiters and reconstruction - justify your answer with a concrete production example.
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; limiters and reconstruction results are only physical at sufficient resolution. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What coordinate system does a code like HARM use in limiters and reconstruction - justify your answer with a concrete production example.
**A:** Logarithmically concentrated coordinates around the horizon; limiters and reconstruction interpretation of any Dump file requires reading that grid mapping. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How does limiters and reconstruction handle magnetic divergence - justify your answer with a concrete production example.
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in limiters and reconstruction injects spurious forces and must be actively controlled. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the biggest difficulty in limiters and reconstruction - justify your answer with a concrete production example.
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: What variables does limiters and reconstruction typically output - justify your answer with a concrete production example.
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the limiters and reconstruction snapshot state. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: How do Athena++ and HARM fit into limiters and reconstruction - justify your answer with a concrete production example.
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding limiters and reconstruction means knowing what each code stores and how. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What is the conservative form in limiters and reconstruction - justify your answer with a concrete production example.
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume limiters and reconstruction codes. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why do black-hole images rely on limiters and reconstruction - justify your answer with a concrete production example.
**A:** The observed emission comes from hot magnetized plasma; limiters and reconstruction produces the density, temperature, velocity, and field data the raytracer converts to light. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What does limiters and reconstruction add to an astrophysical accretion flow model - justify your answer with a concrete production example.
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What does limiters and reconstruction add to an astrophysical accretion flow model - justify your answer with a concrete production example.
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why do black-hole images rely on limiters and reconstruction - justify your answer with a concrete production example.
**A:** The observed emission comes from hot magnetized plasma; limiters and reconstruction produces the density, temperature, velocity, and field data the raytracer converts to light. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What is the conservative form in limiters and reconstruction - justify your answer with a concrete production example.
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume limiters and reconstruction codes. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How do Athena++ and HARM fit into limiters and reconstruction - justify your answer with a concrete production example.
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding limiters and reconstruction means knowing what each code stores and how. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What variables does limiters and reconstruction typically output - justify your answer with a concrete production example.
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the limiters and reconstruction snapshot state. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What is the biggest difficulty in limiters and reconstruction - justify your answer with a concrete production example.
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How does limiters and reconstruction handle magnetic divergence - justify your answer with a concrete production example.
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in limiters and reconstruction injects spurious forces and must be actively controlled. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What coordinate system does a code like HARM use in limiters and reconstruction - justify your answer with a concrete production example.
**A:** Logarithmically concentrated coordinates around the horizon; limiters and reconstruction interpretation of any Dump file requires reading that grid mapping. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What is the resolution requirement of limiters and reconstruction - justify your answer with a concrete production example.
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; limiters and reconstruction results are only physical at sufficient resolution. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does limiters and reconstruction produce the classic two-sided jets - justify your answer with a concrete production example.
**A:** Magnetic field lines collimate outflows along the spin axis; jets in limiters and reconstruction are a natural outcome of magnetically-dominated coronae. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What distinguishes an accretion 'state' in limiters and reconstruction - justify your answer with a concrete production example.
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; limiters and reconstruction evolves between them statistically. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How do you choose among limiters and reconstruction snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What roles do floors and ceilings play in limiters and reconstruction - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; limiters and reconstruction consumers must be aware these floors matter near the horizon. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: How is output frequency chosen in limiters and reconstruction - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; limiters and reconstruction files are large so snapshot cadence is a trade-off. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What is a typical limiters and reconstruction run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; limiters and reconstruction data availability often limits the renderer, not the physics. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How do you check a limiters and reconstruction snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its limiters and reconstruction radiative output. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What approximation do most limiters and reconstruction codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; limiters and reconstruction is therefore a test particle in a fixed background. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does the disk become so hot in limiters and reconstruction - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; limiters and reconstruction emissivity relies on that heat. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What happens when limiters and reconstruction resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates limiters and reconstruction robustness. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What is the role of initial magnetic field topology in limiters and reconstruction - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; limiters and reconstruction initial conditions are a science choice. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What output formats should your limiters and reconstruction importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; limiters and reconstruction importer accuracy is as important as the renderer itself. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How do you map limiters and reconstruction cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; limiters and reconstruction mapping must be consistent with the code's grid functions. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the simplest first limiters and reconstruction test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How can missing physics show up in limiters and reconstruction images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; limiters and reconstruction images are calibrated against observed spectra before use. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How can missing physics show up in limiters and reconstruction images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; limiters and reconstruction images are calibrated against observed spectra before use. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is the simplest first limiters and reconstruction test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How do you map limiters and reconstruction cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; limiters and reconstruction mapping must be consistent with the code's grid functions. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What output formats should your limiters and reconstruction importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; limiters and reconstruction importer accuracy is as important as the renderer itself. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What is the role of initial magnetic field topology in limiters and reconstruction - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; limiters and reconstruction initial conditions are a science choice. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What happens when limiters and reconstruction resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates limiters and reconstruction robustness. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does the disk become so hot in limiters and reconstruction - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; limiters and reconstruction emissivity relies on that heat. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What approximation do most limiters and reconstruction codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; limiters and reconstruction is therefore a test particle in a fixed background. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How do you check a limiters and reconstruction snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its limiters and reconstruction radiative output. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What is a typical limiters and reconstruction run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; limiters and reconstruction data availability often limits the renderer, not the physics. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How is output frequency chosen in limiters and reconstruction - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; limiters and reconstruction files are large so snapshot cadence is a trade-off. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What roles do floors and ceilings play in limiters and reconstruction - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; limiters and reconstruction consumers must be aware these floors matter near the horizon. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How do you choose among limiters and reconstruction snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying limiters and reconstruction in code review and regression tests keeps the whole pipeline trustworthy.
