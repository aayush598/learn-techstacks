# Grmhd — Riemann Solver Interview Questions and Answers

## Q1: What is the Riemann problem?
**A:** The evolution of two constant states (left/right) separated by a discontinuity; Godunov schemes solve it at every intercell face each step.

## Q2: What is an HLL solver?
**A:** The Harten-Lax-van Leer approximate solver assuming two fastest waves; it satisfies conservation and positivity but smears contact discontinuities (needs a few cells).

## Q3: What is the HLLC solver?
**A:** HLL with the contact wave added: sharper resolution of the contact (density jumps) - most modern GRMHD (HARM, Athena++) default to HLLC or its variants.

## Q4: What are the fastest waves?
**A:** The fast magnetosonic speeds c_+/- (along the face normal); a Riemann solver that bounds by them keeps the solution entropy-satisfying.

## Q5: Why can't you use exact solution?
**A:** The relativistic MHD Riemann problem is transcendental and expensive; approximate solvers give shocks to sufficient accuracy for displacement analysis.

## Q6: What is the role of the eigenstructure?
**A:** Fast/Alfven/slow waves determine characteristic speeds for flux splitting and for the CFL; their accuracy sets the effective dissipation.

## Q7: What about moving/discontinuous grids?
**A:** Uniform static grids skip grid-speed terms; AMR-with-refinement adds them - a detail more codes than not get subtly wrong.

## Q8: What is the positivity region?
**A:** For HLL the positivity of density/pressure is provable within the two-wave bound - the theoretical reason production codes prefer HLL for extreme states.

## Q9: How is the solver vectorized?
**A:** Per-face state evaluation, eigen-computation, and flux arithmetic are lock-step: SIMD across faces, with branch-free approximations for the wave speeds.

## Q10: What is a total-variation-diminishing (TVD) pairing?
**A:** Solver + limiter must keep total variation bounded; mismatched (oscillating) pairs create spurious oscillation in strong-field runs.

## Q11: How does the solver relate to capturing jet shocks?
**A:** Jet sheath shocks demand sharp contact + robust fast-wave treatment; over-diffusive solvers blunt the jet's collimation - a visible production-mismatch symptom.

## Q12: What is a classic validation?
**A:** The 1D relativistic MHD shock tube (Balsara & Spicer): reproduce exact wave speeds, jumps, and no oddi jumps - gods of the field.

## Q13: How do you handle vacuum states?
**A:** Floors and the solver's positivity gap: if one side hits floor, the scheme must survive (bounce/remap) - the vacuum catastrophe the fields guard against.

## Q14: What coupling with the limiter matters?
**A:** The limiter reconstructs left/right states; the solver consumes them; a muted limiter + HLL gives the least oscillation but thickens the jet - the tradeoff is documented.

## Q15: What is the performance reality?
**A:** The Riemann solver is 40-60% of GRMHD runtime; vectorization, cut-off logic, and low-precision paths elsewhere are the engineering payoff.

## Q16: What does riemann solver add to an astrophysical accretion flow model?
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need.

## Q17: Why do black-hole images rely on riemann solver?
**A:** The observed emission comes from hot magnetized plasma; riemann solver produces the density, temperature, velocity, and field data the raytracer converts to light.

## Q18: What is the conservative form in riemann solver?
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume riemann solver codes.

## Q19: How do Athena++ and HARM fit into riemann solver?
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding riemann solver means knowing what each code stores and how.

## Q20: What variables does riemann solver typically output?
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the riemann solver snapshot state.

## Q21: What is the biggest difficulty in riemann solver?
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes.

## Q22: How does riemann solver handle magnetic divergence?
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in riemann solver injects spurious forces and must be actively controlled.

## Q23: What coordinate system does a code like HARM use in riemann solver?
**A:** Logarithmically concentrated coordinates around the horizon; riemann solver interpretation of any Dump file requires reading that grid mapping.

## Q24: What is the resolution requirement of riemann solver?
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; riemann solver results are only physical at sufficient resolution.

## Q25: How does riemann solver produce the classic two-sided jets?
**A:** Magnetic field lines collimate outflows along the spin axis; jets in riemann solver are a natural outcome of magnetically-dominated coronae.

## Q26: What distinguishes an accretion 'state' in riemann solver?
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; riemann solver evolves between them statistically.

## Q27: How do you choose among riemann solver snapshots for rendering?
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant.

## Q28: What roles do floors and ceilings play in riemann solver?
**A:** Codes impose density/pressure floors to prevent negative states; riemann solver consumers must be aware these floors matter near the horizon.

## Q29: How is output frequency chosen in riemann solver?
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; riemann solver files are large so snapshot cadence is a trade-off.

## Q30: What is a typical riemann solver run cost?
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; riemann solver data availability often limits the renderer, not the physics.

## Q31: How do you check a riemann solver snapshot is physical?
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its riemann solver radiative output.

## Q32: What approximation do most riemann solver codes make about gravity?
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; riemann solver is therefore a test particle in a fixed background.

## Q33: How does the disk become so hot in riemann solver?
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; riemann solver emissivity relies on that heat.

## Q34: What happens when riemann solver resolution is doubled?
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates riemann solver robustness.

## Q35: What is the role of initial magnetic field topology in riemann solver?
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; riemann solver initial conditions are a science choice.

## Q36: What output formats should your riemann solver importer accept?
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; riemann solver importer accuracy is as important as the renderer itself.

## Q37: How do you map riemann solver cells to the raytracer grid?
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; riemann solver mapping must be consistent with the code's grid functions.

## Q38: What is the simplest first riemann solver test?
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average.

## Q39: How can missing physics show up in riemann solver images?
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; riemann solver images are calibrated against observed spectra before use.

## Q40: How can missing physics show up in riemann solver images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; riemann solver images are calibrated against observed spectra before use. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is the simplest first riemann solver test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How do you map riemann solver cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; riemann solver mapping must be consistent with the code's grid functions. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What output formats should your riemann solver importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; riemann solver importer accuracy is as important as the renderer itself. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What is the role of initial magnetic field topology in riemann solver - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; riemann solver initial conditions are a science choice. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What happens when riemann solver resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates riemann solver robustness. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does the disk become so hot in riemann solver - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; riemann solver emissivity relies on that heat. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What approximation do most riemann solver codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; riemann solver is therefore a test particle in a fixed background. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How do you check a riemann solver snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its riemann solver radiative output. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What is a typical riemann solver run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; riemann solver data availability often limits the renderer, not the physics. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How is output frequency chosen in riemann solver - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; riemann solver files are large so snapshot cadence is a trade-off. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What roles do floors and ceilings play in riemann solver - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; riemann solver consumers must be aware these floors matter near the horizon. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How do you choose among riemann solver snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What distinguishes an accretion 'state' in riemann solver - justify your answer with a concrete production example.
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; riemann solver evolves between them statistically. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does riemann solver produce the classic two-sided jets - justify your answer with a concrete production example.
**A:** Magnetic field lines collimate outflows along the spin axis; jets in riemann solver are a natural outcome of magnetically-dominated coronae. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What is the resolution requirement of riemann solver - justify your answer with a concrete production example.
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; riemann solver results are only physical at sufficient resolution. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What coordinate system does a code like HARM use in riemann solver - justify your answer with a concrete production example.
**A:** Logarithmically concentrated coordinates around the horizon; riemann solver interpretation of any Dump file requires reading that grid mapping. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How does riemann solver handle magnetic divergence - justify your answer with a concrete production example.
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in riemann solver injects spurious forces and must be actively controlled. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the biggest difficulty in riemann solver - justify your answer with a concrete production example.
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: What variables does riemann solver typically output - justify your answer with a concrete production example.
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the riemann solver snapshot state. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: How do Athena++ and HARM fit into riemann solver - justify your answer with a concrete production example.
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding riemann solver means knowing what each code stores and how. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What is the conservative form in riemann solver - justify your answer with a concrete production example.
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume riemann solver codes. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why do black-hole images rely on riemann solver - justify your answer with a concrete production example.
**A:** The observed emission comes from hot magnetized plasma; riemann solver produces the density, temperature, velocity, and field data the raytracer converts to light. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What does riemann solver add to an astrophysical accretion flow model - justify your answer with a concrete production example.
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What does riemann solver add to an astrophysical accretion flow model - justify your answer with a concrete production example.
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why do black-hole images rely on riemann solver - justify your answer with a concrete production example.
**A:** The observed emission comes from hot magnetized plasma; riemann solver produces the density, temperature, velocity, and field data the raytracer converts to light. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What is the conservative form in riemann solver - justify your answer with a concrete production example.
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume riemann solver codes. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How do Athena++ and HARM fit into riemann solver - justify your answer with a concrete production example.
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding riemann solver means knowing what each code stores and how. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What variables does riemann solver typically output - justify your answer with a concrete production example.
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the riemann solver snapshot state. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What is the biggest difficulty in riemann solver - justify your answer with a concrete production example.
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How does riemann solver handle magnetic divergence - justify your answer with a concrete production example.
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in riemann solver injects spurious forces and must be actively controlled. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What coordinate system does a code like HARM use in riemann solver - justify your answer with a concrete production example.
**A:** Logarithmically concentrated coordinates around the horizon; riemann solver interpretation of any Dump file requires reading that grid mapping. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What is the resolution requirement of riemann solver - justify your answer with a concrete production example.
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; riemann solver results are only physical at sufficient resolution. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does riemann solver produce the classic two-sided jets - justify your answer with a concrete production example.
**A:** Magnetic field lines collimate outflows along the spin axis; jets in riemann solver are a natural outcome of magnetically-dominated coronae. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What distinguishes an accretion 'state' in riemann solver - justify your answer with a concrete production example.
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; riemann solver evolves between them statistically. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How do you choose among riemann solver snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What roles do floors and ceilings play in riemann solver - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; riemann solver consumers must be aware these floors matter near the horizon. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: How is output frequency chosen in riemann solver - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; riemann solver files are large so snapshot cadence is a trade-off. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What is a typical riemann solver run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; riemann solver data availability often limits the renderer, not the physics. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How do you check a riemann solver snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its riemann solver radiative output. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What approximation do most riemann solver codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; riemann solver is therefore a test particle in a fixed background. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does the disk become so hot in riemann solver - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; riemann solver emissivity relies on that heat. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What happens when riemann solver resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates riemann solver robustness. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What is the role of initial magnetic field topology in riemann solver - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; riemann solver initial conditions are a science choice. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What output formats should your riemann solver importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; riemann solver importer accuracy is as important as the renderer itself. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How do you map riemann solver cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; riemann solver mapping must be consistent with the code's grid functions. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the simplest first riemann solver test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How can missing physics show up in riemann solver images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; riemann solver images are calibrated against observed spectra before use. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How can missing physics show up in riemann solver images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; riemann solver images are calibrated against observed spectra before use. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is the simplest first riemann solver test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How do you map riemann solver cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; riemann solver mapping must be consistent with the code's grid functions. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What output formats should your riemann solver importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; riemann solver importer accuracy is as important as the renderer itself. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What is the role of initial magnetic field topology in riemann solver - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; riemann solver initial conditions are a science choice. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What happens when riemann solver resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates riemann solver robustness. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does the disk become so hot in riemann solver - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; riemann solver emissivity relies on that heat. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What approximation do most riemann solver codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; riemann solver is therefore a test particle in a fixed background. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How do you check a riemann solver snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its riemann solver radiative output. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What is a typical riemann solver run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; riemann solver data availability often limits the renderer, not the physics. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How is output frequency chosen in riemann solver - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; riemann solver files are large so snapshot cadence is a trade-off. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What roles do floors and ceilings play in riemann solver - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; riemann solver consumers must be aware these floors matter near the horizon. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How do you choose among riemann solver snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying riemann solver in code review and regression tests keeps the whole pipeline trustworthy.
