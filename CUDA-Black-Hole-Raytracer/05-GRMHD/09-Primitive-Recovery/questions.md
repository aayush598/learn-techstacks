# Grmhd — Primitive Recovery Interview Questions and Answers

## Q1: What is primitive recovery?
**A:** Inverting the conservative-to-primitive map (from D, S, tau, B to rho, p, u^i, B^i) after each conservative update - the bane of every GRMHD code.

## Q2: Why does recovery fail?
**A:** Physical conservations permit states outside the recoverable domain (e.g., negative pressure); their causes include floors, extreme flows, and finite-precision algebra.

## Q3: What is the common strategy?
**A:** Newton-Raphson on a 2D/3D system (e.g., W = gamma^2 rho h from p-W), with fallbacks: bisection, entropy-based, or truncation to floors.

## Q4: What is the 'p-W' system?
**A:** Noble et al.'s variables (p, W) reducing recovery to a 2x2/newtonian subsystem; the standard HARM approach.

## Q5: What is a 1D iterative approach?
**A:** A single-variable root-find on the equation c2(W) using only conserved data + the EOS - cheaper, more branches but more fragile when biting.

## Q6: What are the failure triggers in practice?
**A:** Near-vacuum cells, strong shocks, and the transition to the jet's empty core - exactly the regions where the visuals matter most.

## Q7: What is the role of floors?
**A:** Enforced minima on rho, p, b^2 keep the inverse well-posed; setting them is an art - too high erases physics (jet density), too low breaks the run.

## Q8: How is positivity enforced?
**A:** Clamp negative rho/p to floors (or a 'fix' that scales the energy); the loss in conservativity is the price of survival.

## Q9: How does recovery interact with the EOS?
**A:** A gamma-law closes W's equation; tabulated/electron-tracking EOS make the inverse loop costlier - a real bottleneck for a raytracer-coupled use.

## Q10: What is the 'energy consistency' check?
**A:** Reconstructed W, p must reproduce D, S, tau up to tolerance; the code computes a residual metric - its smallness is the correctness gate.

## Q11: How is recovery vectorized/acclimated for GPU?
**A:** Batched Newton loops with fixed iteration counts (avoids divergence) plus rescue paths - the performance-critical branch of the whole scheme on accelerators.

## Q12: What is a well-known trap?
**A:** Recovering with B in the wrong frame (lab vs fluid) silently corrupts every derived emissivity; the field must be b^mu in the fluid rest frame.

## Q13: What does a hand-written raytracer need?
**A:** The raytracer consumes primitives + B directly from dumps; recovery correctness is the simulation's job, verified once per dump.

## Q14: How do you test recovery?
**A:** Clone a full state: P2C then C2P must recover the same primitives to 1e-10; a suite of pathological (high-beta, low-density) states stresses the fallback path.

## Q15: What is the production-level summary?
**A:** Robust recovery + floors + Newton fallback: the code plays its part by keeping the innermost cells physical enough to ray-trace without artifacts.

## Q16: What does primitive recovery add to an astrophysical accretion flow model?
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need.

## Q17: Why do black-hole images rely on primitive recovery?
**A:** The observed emission comes from hot magnetized plasma; primitive recovery produces the density, temperature, velocity, and field data the raytracer converts to light.

## Q18: What is the conservative form in primitive recovery?
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume primitive recovery codes.

## Q19: How do Athena++ and HARM fit into primitive recovery?
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding primitive recovery means knowing what each code stores and how.

## Q20: What variables does primitive recovery typically output?
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the primitive recovery snapshot state.

## Q21: What is the biggest difficulty in primitive recovery?
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes.

## Q22: How does primitive recovery handle magnetic divergence?
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in primitive recovery injects spurious forces and must be actively controlled.

## Q23: What coordinate system does a code like HARM use in primitive recovery?
**A:** Logarithmically concentrated coordinates around the horizon; primitive recovery interpretation of any Dump file requires reading that grid mapping.

## Q24: What is the resolution requirement of primitive recovery?
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; primitive recovery results are only physical at sufficient resolution.

## Q25: How does primitive recovery produce the classic two-sided jets?
**A:** Magnetic field lines collimate outflows along the spin axis; jets in primitive recovery are a natural outcome of magnetically-dominated coronae.

## Q26: What distinguishes an accretion 'state' in primitive recovery?
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; primitive recovery evolves between them statistically.

## Q27: How do you choose among primitive recovery snapshots for rendering?
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant.

## Q28: What roles do floors and ceilings play in primitive recovery?
**A:** Codes impose density/pressure floors to prevent negative states; primitive recovery consumers must be aware these floors matter near the horizon.

## Q29: How is output frequency chosen in primitive recovery?
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; primitive recovery files are large so snapshot cadence is a trade-off.

## Q30: What is a typical primitive recovery run cost?
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; primitive recovery data availability often limits the renderer, not the physics.

## Q31: How do you check a primitive recovery snapshot is physical?
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its primitive recovery radiative output.

## Q32: What approximation do most primitive recovery codes make about gravity?
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; primitive recovery is therefore a test particle in a fixed background.

## Q33: How does the disk become so hot in primitive recovery?
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; primitive recovery emissivity relies on that heat.

## Q34: What happens when primitive recovery resolution is doubled?
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates primitive recovery robustness.

## Q35: What is the role of initial magnetic field topology in primitive recovery?
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; primitive recovery initial conditions are a science choice.

## Q36: What output formats should your primitive recovery importer accept?
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; primitive recovery importer accuracy is as important as the renderer itself.

## Q37: How do you map primitive recovery cells to the raytracer grid?
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; primitive recovery mapping must be consistent with the code's grid functions.

## Q38: What is the simplest first primitive recovery test?
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average.

## Q39: How can missing physics show up in primitive recovery images?
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; primitive recovery images are calibrated against observed spectra before use.

## Q40: How can missing physics show up in primitive recovery images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; primitive recovery images are calibrated against observed spectra before use. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is the simplest first primitive recovery test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How do you map primitive recovery cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; primitive recovery mapping must be consistent with the code's grid functions. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What output formats should your primitive recovery importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; primitive recovery importer accuracy is as important as the renderer itself. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What is the role of initial magnetic field topology in primitive recovery - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; primitive recovery initial conditions are a science choice. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What happens when primitive recovery resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates primitive recovery robustness. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does the disk become so hot in primitive recovery - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; primitive recovery emissivity relies on that heat. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What approximation do most primitive recovery codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; primitive recovery is therefore a test particle in a fixed background. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How do you check a primitive recovery snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its primitive recovery radiative output. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What is a typical primitive recovery run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; primitive recovery data availability often limits the renderer, not the physics. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How is output frequency chosen in primitive recovery - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; primitive recovery files are large so snapshot cadence is a trade-off. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What roles do floors and ceilings play in primitive recovery - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; primitive recovery consumers must be aware these floors matter near the horizon. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How do you choose among primitive recovery snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What distinguishes an accretion 'state' in primitive recovery - justify your answer with a concrete production example.
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; primitive recovery evolves between them statistically. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does primitive recovery produce the classic two-sided jets - justify your answer with a concrete production example.
**A:** Magnetic field lines collimate outflows along the spin axis; jets in primitive recovery are a natural outcome of magnetically-dominated coronae. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What is the resolution requirement of primitive recovery - justify your answer with a concrete production example.
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; primitive recovery results are only physical at sufficient resolution. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What coordinate system does a code like HARM use in primitive recovery - justify your answer with a concrete production example.
**A:** Logarithmically concentrated coordinates around the horizon; primitive recovery interpretation of any Dump file requires reading that grid mapping. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How does primitive recovery handle magnetic divergence - justify your answer with a concrete production example.
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in primitive recovery injects spurious forces and must be actively controlled. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the biggest difficulty in primitive recovery - justify your answer with a concrete production example.
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: What variables does primitive recovery typically output - justify your answer with a concrete production example.
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the primitive recovery snapshot state. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: How do Athena++ and HARM fit into primitive recovery - justify your answer with a concrete production example.
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding primitive recovery means knowing what each code stores and how. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What is the conservative form in primitive recovery - justify your answer with a concrete production example.
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume primitive recovery codes. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why do black-hole images rely on primitive recovery - justify your answer with a concrete production example.
**A:** The observed emission comes from hot magnetized plasma; primitive recovery produces the density, temperature, velocity, and field data the raytracer converts to light. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What does primitive recovery add to an astrophysical accretion flow model - justify your answer with a concrete production example.
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What does primitive recovery add to an astrophysical accretion flow model - justify your answer with a concrete production example.
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why do black-hole images rely on primitive recovery - justify your answer with a concrete production example.
**A:** The observed emission comes from hot magnetized plasma; primitive recovery produces the density, temperature, velocity, and field data the raytracer converts to light. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What is the conservative form in primitive recovery - justify your answer with a concrete production example.
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume primitive recovery codes. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How do Athena++ and HARM fit into primitive recovery - justify your answer with a concrete production example.
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding primitive recovery means knowing what each code stores and how. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What variables does primitive recovery typically output - justify your answer with a concrete production example.
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the primitive recovery snapshot state. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What is the biggest difficulty in primitive recovery - justify your answer with a concrete production example.
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How does primitive recovery handle magnetic divergence - justify your answer with a concrete production example.
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in primitive recovery injects spurious forces and must be actively controlled. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What coordinate system does a code like HARM use in primitive recovery - justify your answer with a concrete production example.
**A:** Logarithmically concentrated coordinates around the horizon; primitive recovery interpretation of any Dump file requires reading that grid mapping. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What is the resolution requirement of primitive recovery - justify your answer with a concrete production example.
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; primitive recovery results are only physical at sufficient resolution. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does primitive recovery produce the classic two-sided jets - justify your answer with a concrete production example.
**A:** Magnetic field lines collimate outflows along the spin axis; jets in primitive recovery are a natural outcome of magnetically-dominated coronae. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What distinguishes an accretion 'state' in primitive recovery - justify your answer with a concrete production example.
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; primitive recovery evolves between them statistically. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How do you choose among primitive recovery snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What roles do floors and ceilings play in primitive recovery - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; primitive recovery consumers must be aware these floors matter near the horizon. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: How is output frequency chosen in primitive recovery - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; primitive recovery files are large so snapshot cadence is a trade-off. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What is a typical primitive recovery run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; primitive recovery data availability often limits the renderer, not the physics. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How do you check a primitive recovery snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its primitive recovery radiative output. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What approximation do most primitive recovery codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; primitive recovery is therefore a test particle in a fixed background. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does the disk become so hot in primitive recovery - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; primitive recovery emissivity relies on that heat. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What happens when primitive recovery resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates primitive recovery robustness. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What is the role of initial magnetic field topology in primitive recovery - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; primitive recovery initial conditions are a science choice. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What output formats should your primitive recovery importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; primitive recovery importer accuracy is as important as the renderer itself. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How do you map primitive recovery cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; primitive recovery mapping must be consistent with the code's grid functions. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the simplest first primitive recovery test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How can missing physics show up in primitive recovery images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; primitive recovery images are calibrated against observed spectra before use. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How can missing physics show up in primitive recovery images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; primitive recovery images are calibrated against observed spectra before use. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is the simplest first primitive recovery test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How do you map primitive recovery cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; primitive recovery mapping must be consistent with the code's grid functions. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What output formats should your primitive recovery importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; primitive recovery importer accuracy is as important as the renderer itself. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What is the role of initial magnetic field topology in primitive recovery - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; primitive recovery initial conditions are a science choice. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What happens when primitive recovery resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates primitive recovery robustness. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does the disk become so hot in primitive recovery - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; primitive recovery emissivity relies on that heat. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What approximation do most primitive recovery codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; primitive recovery is therefore a test particle in a fixed background. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How do you check a primitive recovery snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its primitive recovery radiative output. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What is a typical primitive recovery run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; primitive recovery data availability often limits the renderer, not the physics. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How is output frequency chosen in primitive recovery - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; primitive recovery files are large so snapshot cadence is a trade-off. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What roles do floors and ceilings play in primitive recovery - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; primitive recovery consumers must be aware these floors matter near the horizon. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How do you choose among primitive recovery snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying primitive recovery in code review and regression tests keeps the whole pipeline trustworthy.
