# Grmhd — Grid And Amr Interview Questions and Answers

## Q1: What coordinate grids are used in GRMHD?
**A:** Log-spaced radial, uniform/cosine theta, and cell-centered phi; or utilitarian mapped coordinates fitting the horizon - choices that set resolution where it matters.

## Q2: What is a logarithmic radial grid?
**A:** r_i at geometric spacing d r/r ~ const, packing resolution near the horizon where density gradients live; then spacing grows to the outer boundary.

## Q3: What is the role of the radial boundary?
**A:** Inner: horizon-inflow boundary; outer: free-flow or floor. Mismatches poison jets/disks, so boundary stencils must be tested like physics.

## Q4: What is AMR (adaptive mesh refinement)?
**A:** Refining regions (e.g., the disk midplane and jet) as needed, coarsening quiescent regions; Athena++ is built around a block-based AMR.

## Q5: What triggers refinement?
**A:** Gradient/smoothness estimators on density/pressure/B plus refinement zones tied to the physics (inner disk radius, jet spine).

## Q6: What are the challenges of AMR for GRMHD?
**A:** Conservation across refinement boundaries, advancing rization of faces, and the cost of the tree - mature codes (Athena++) solve via ghost cells at fine/coarse interfaces.

## Q7: What is a 'de-refine' criterion?
**A:** Error estimator below a floor for several intervals - coarsen back; hysteresis prevents flapping between levels near critical radii.

## Q8: How does grid choice affect numerical diffusion?
**A:** The effective dissipation scales with the local cell size; a stretched log grid enlarges cells at r>100M where jets are - inevitably a compromise.

## Q9: What is the equilibrium of resolution?
**A:** Resolving MRI fastest-grow wavelength in the disk AND the jet sheath needs 100+ cells across each - the reason 3D GRMHD is a petascale sport.

## Q10: How do you set grid parameters from physics?
**A:** Match the MRI wavelength ~ sqrt(3)/Omega * v_A: cells <= that in the midplane; the jet's scale ~ RH of the hole - measured, not guessed.

## Q11: What is the 'outer boundary prescription'?
**A:** Floor-filled flat state + damping zone at the outer boundary (outflow b.c.); jets can reflect otherwise - a common simulation-fiddle artifact.

## Q12: How is AMR verified?
**A:** Run a fixed-resolution and an AMR run with the same effective max resolution; derived accretion rate/MRI quantities must agree to tolerance.

## Q13: What is the storage implication?
**A:** Multi-level AMR stores each level separately; transient I/O becomes a bottleneck - compress-level outputs and keep checkpoint/restart bare.

## Q14: How does HARM differ in grid?
**A:** HARM uses stationary analytic grids (often 'phi-normalized') coded directly, not a tree; it trades flexibility for tensor-managed simplicity.

## Q15: What is the physics-correct grid slogan?
**A:** Put cells where the gradients live (inner rho, disk midplane, jet spine) and let the metric do the rest - every resolution budget is spent there.

## Q16: What does grid and amr add to an astrophysical accretion flow model?
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need.

## Q17: Why do black-hole images rely on grid and amr?
**A:** The observed emission comes from hot magnetized plasma; grid and amr produces the density, temperature, velocity, and field data the raytracer converts to light.

## Q18: What is the conservative form in grid and amr?
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume grid and amr codes.

## Q19: How do Athena++ and HARM fit into grid and amr?
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding grid and amr means knowing what each code stores and how.

## Q20: What variables does grid and amr typically output?
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the grid and amr snapshot state.

## Q21: What is the biggest difficulty in grid and amr?
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes.

## Q22: How does grid and amr handle magnetic divergence?
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in grid and amr injects spurious forces and must be actively controlled.

## Q23: What coordinate system does a code like HARM use in grid and amr?
**A:** Logarithmically concentrated coordinates around the horizon; grid and amr interpretation of any Dump file requires reading that grid mapping.

## Q24: What is the resolution requirement of grid and amr?
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; grid and amr results are only physical at sufficient resolution.

## Q25: How does grid and amr produce the classic two-sided jets?
**A:** Magnetic field lines collimate outflows along the spin axis; jets in grid and amr are a natural outcome of magnetically-dominated coronae.

## Q26: What distinguishes an accretion 'state' in grid and amr?
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; grid and amr evolves between them statistically.

## Q27: How do you choose among grid and amr snapshots for rendering?
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant.

## Q28: What roles do floors and ceilings play in grid and amr?
**A:** Codes impose density/pressure floors to prevent negative states; grid and amr consumers must be aware these floors matter near the horizon.

## Q29: How is output frequency chosen in grid and amr?
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; grid and amr files are large so snapshot cadence is a trade-off.

## Q30: What is a typical grid and amr run cost?
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; grid and amr data availability often limits the renderer, not the physics.

## Q31: How do you check a grid and amr snapshot is physical?
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its grid and amr radiative output.

## Q32: What approximation do most grid and amr codes make about gravity?
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; grid and amr is therefore a test particle in a fixed background.

## Q33: How does the disk become so hot in grid and amr?
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; grid and amr emissivity relies on that heat.

## Q34: What happens when grid and amr resolution is doubled?
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates grid and amr robustness.

## Q35: What is the role of initial magnetic field topology in grid and amr?
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; grid and amr initial conditions are a science choice.

## Q36: What output formats should your grid and amr importer accept?
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; grid and amr importer accuracy is as important as the renderer itself.

## Q37: How do you map grid and amr cells to the raytracer grid?
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; grid and amr mapping must be consistent with the code's grid functions.

## Q38: What is the simplest first grid and amr test?
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average.

## Q39: How can missing physics show up in grid and amr images?
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; grid and amr images are calibrated against observed spectra before use.

## Q40: How can missing physics show up in grid and amr images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; grid and amr images are calibrated against observed spectra before use. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is the simplest first grid and amr test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How do you map grid and amr cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; grid and amr mapping must be consistent with the code's grid functions. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What output formats should your grid and amr importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; grid and amr importer accuracy is as important as the renderer itself. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What is the role of initial magnetic field topology in grid and amr - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; grid and amr initial conditions are a science choice. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What happens when grid and amr resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates grid and amr robustness. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does the disk become so hot in grid and amr - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; grid and amr emissivity relies on that heat. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What approximation do most grid and amr codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; grid and amr is therefore a test particle in a fixed background. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How do you check a grid and amr snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its grid and amr radiative output. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What is a typical grid and amr run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; grid and amr data availability often limits the renderer, not the physics. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How is output frequency chosen in grid and amr - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; grid and amr files are large so snapshot cadence is a trade-off. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What roles do floors and ceilings play in grid and amr - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; grid and amr consumers must be aware these floors matter near the horizon. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How do you choose among grid and amr snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What distinguishes an accretion 'state' in grid and amr - justify your answer with a concrete production example.
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; grid and amr evolves between them statistically. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does grid and amr produce the classic two-sided jets - justify your answer with a concrete production example.
**A:** Magnetic field lines collimate outflows along the spin axis; jets in grid and amr are a natural outcome of magnetically-dominated coronae. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What is the resolution requirement of grid and amr - justify your answer with a concrete production example.
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; grid and amr results are only physical at sufficient resolution. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What coordinate system does a code like HARM use in grid and amr - justify your answer with a concrete production example.
**A:** Logarithmically concentrated coordinates around the horizon; grid and amr interpretation of any Dump file requires reading that grid mapping. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How does grid and amr handle magnetic divergence - justify your answer with a concrete production example.
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in grid and amr injects spurious forces and must be actively controlled. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the biggest difficulty in grid and amr - justify your answer with a concrete production example.
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: What variables does grid and amr typically output - justify your answer with a concrete production example.
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the grid and amr snapshot state. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: How do Athena++ and HARM fit into grid and amr - justify your answer with a concrete production example.
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding grid and amr means knowing what each code stores and how. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What is the conservative form in grid and amr - justify your answer with a concrete production example.
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume grid and amr codes. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why do black-hole images rely on grid and amr - justify your answer with a concrete production example.
**A:** The observed emission comes from hot magnetized plasma; grid and amr produces the density, temperature, velocity, and field data the raytracer converts to light. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What does grid and amr add to an astrophysical accretion flow model - justify your answer with a concrete production example.
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What does grid and amr add to an astrophysical accretion flow model - justify your answer with a concrete production example.
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why do black-hole images rely on grid and amr - justify your answer with a concrete production example.
**A:** The observed emission comes from hot magnetized plasma; grid and amr produces the density, temperature, velocity, and field data the raytracer converts to light. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What is the conservative form in grid and amr - justify your answer with a concrete production example.
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume grid and amr codes. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How do Athena++ and HARM fit into grid and amr - justify your answer with a concrete production example.
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding grid and amr means knowing what each code stores and how. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What variables does grid and amr typically output - justify your answer with a concrete production example.
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the grid and amr snapshot state. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What is the biggest difficulty in grid and amr - justify your answer with a concrete production example.
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How does grid and amr handle magnetic divergence - justify your answer with a concrete production example.
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in grid and amr injects spurious forces and must be actively controlled. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What coordinate system does a code like HARM use in grid and amr - justify your answer with a concrete production example.
**A:** Logarithmically concentrated coordinates around the horizon; grid and amr interpretation of any Dump file requires reading that grid mapping. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What is the resolution requirement of grid and amr - justify your answer with a concrete production example.
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; grid and amr results are only physical at sufficient resolution. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does grid and amr produce the classic two-sided jets - justify your answer with a concrete production example.
**A:** Magnetic field lines collimate outflows along the spin axis; jets in grid and amr are a natural outcome of magnetically-dominated coronae. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What distinguishes an accretion 'state' in grid and amr - justify your answer with a concrete production example.
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; grid and amr evolves between them statistically. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How do you choose among grid and amr snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What roles do floors and ceilings play in grid and amr - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; grid and amr consumers must be aware these floors matter near the horizon. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: How is output frequency chosen in grid and amr - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; grid and amr files are large so snapshot cadence is a trade-off. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What is a typical grid and amr run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; grid and amr data availability often limits the renderer, not the physics. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How do you check a grid and amr snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its grid and amr radiative output. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What approximation do most grid and amr codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; grid and amr is therefore a test particle in a fixed background. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does the disk become so hot in grid and amr - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; grid and amr emissivity relies on that heat. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What happens when grid and amr resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates grid and amr robustness. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What is the role of initial magnetic field topology in grid and amr - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; grid and amr initial conditions are a science choice. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What output formats should your grid and amr importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; grid and amr importer accuracy is as important as the renderer itself. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How do you map grid and amr cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; grid and amr mapping must be consistent with the code's grid functions. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the simplest first grid and amr test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How can missing physics show up in grid and amr images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; grid and amr images are calibrated against observed spectra before use. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How can missing physics show up in grid and amr images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; grid and amr images are calibrated against observed spectra before use. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is the simplest first grid and amr test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How do you map grid and amr cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; grid and amr mapping must be consistent with the code's grid functions. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What output formats should your grid and amr importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; grid and amr importer accuracy is as important as the renderer itself. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What is the role of initial magnetic field topology in grid and amr - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; grid and amr initial conditions are a science choice. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What happens when grid and amr resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates grid and amr robustness. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does the disk become so hot in grid and amr - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; grid and amr emissivity relies on that heat. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What approximation do most grid and amr codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; grid and amr is therefore a test particle in a fixed background. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How do you check a grid and amr snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its grid and amr radiative output. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What is a typical grid and amr run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; grid and amr data availability often limits the renderer, not the physics. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How is output frequency chosen in grid and amr - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; grid and amr files are large so snapshot cadence is a trade-off. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What roles do floors and ceilings play in grid and amr - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; grid and amr consumers must be aware these floors matter near the horizon. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How do you choose among grid and amr snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying grid and amr in code review and regression tests keeps the whole pipeline trustworthy.
