# Grmhd — Ideal Mhd Interview Questions and Answers

## Q1: What is ideal MHD?
**A:** The limit of infinite conductivity + nonrelativistic flow, where the field is frozen into the plasma; GRMHD is its relativistic, curved-spacetime generalization.

## Q2: What does flux-freezing mean for a disk?
**A:** Field lines are advected with the matter; a disk's B profile therefore follows the gas - the base of MRI-driven transport models.

## Q3: What are the ideal MHD normal modes?
**A:** Alfven, fast, and slow magnetosonic waves; their speeds are the state-dependent eigenvalues of the system - the Riemann solver must resolve all three.

## Q4: What is the Alfven speed?
**A:** v_A = B/sqrt(4 pi rho) (in nonrel form); in GRMHD, the relativistic b^2-weighted expression; it sets the anisotropic transport speed along field lines.

## Q5: What is the equation of motion with B?
**A:** rho dv/dt = -grad p + 1/(4pi)(curl B) x B; magnetic tension (curvature) and pressure (gradient) both accelerate the plasma.

## Q6: What is the magnetic pressure?
**A:** P_B = B^2/(8pi); it contributes to total pressure and to the energy budget - observations of jet collimation root in its dominance.

## Q7: What is the beta parameter?
**A:** beta = p_gas/p_B (plasma beta); beta >> 1 gas-dominated (typical disk), beta << 1 magnetically-dominated (jets, corona).

## Q8: What are the disagreements between ideal MHD and reality?
**A:** It ignores resistivity, Hall, electron kinetics; real disks have reconnection - but ideal captures the large-scale dynamics of accretion+jets faithfully.

## Q9: How do velocities compare (nonrel vs GR)?
**A:** The GR version replaces v with the 4-velocity and spatial basis; the induction becomes d_iF = 0 with the full b^mu - a heavier algebra, same physics.

## Q10: What is the 'magnetic field in the fluid frame'?
**A:** b^mu = (1/2) u^nu *F^mu
u (the co-moving projection); all forward-frame formulas (emissivity) use b (and its norm) rather than the lab B.

## Q11: How does ideal MHD energy evolve?
**A:** Polytropic (gamma-law) energy flux plus Poynting; in GRMHD the total energy-momentum is conserved as T^mu
u - internal energy via p rho gamma(integral term).

## Q12: What are the limitations for disk simulations?
**A:** Turbulent dissipation is numerical; true electron heating needs closure - a known KeR/ipole-hybrid gap the analyst must report.

## Q13: What is the MRI threshold?
**A:** For weak B, MRI linearly drives modes unless rotation profile is too stiff (the Lindblad/MRI criterion); codes must resolve the fastest-growing wavelength.

## Q14: How does ideal MHD set the jet?
**A:** Poynting flux along poloidal field: the plasma accelerated by magnetic slingshot - simulated jets are a successful ideal-MHD prediction.

## Q15: What validation test is canonical?
**A:** The 1D nonrelativistic shock tube / Orszag-Tang vortex; GR codes additionally test the stationary torus equilibrium - the 'artificial disk' stability run.

## Q16: What does ideal mhd add to an astrophysical accretion flow model?
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need.

## Q17: Why do black-hole images rely on ideal mhd?
**A:** The observed emission comes from hot magnetized plasma; ideal mhd produces the density, temperature, velocity, and field data the raytracer converts to light.

## Q18: What is the conservative form in ideal mhd?
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume ideal mhd codes.

## Q19: How do Athena++ and HARM fit into ideal mhd?
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding ideal mhd means knowing what each code stores and how.

## Q20: What variables does ideal mhd typically output?
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the ideal mhd snapshot state.

## Q21: What is the biggest difficulty in ideal mhd?
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes.

## Q22: How does ideal mhd handle magnetic divergence?
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in ideal mhd injects spurious forces and must be actively controlled.

## Q23: What coordinate system does a code like HARM use in ideal mhd?
**A:** Logarithmically concentrated coordinates around the horizon; ideal mhd interpretation of any Dump file requires reading that grid mapping.

## Q24: What is the resolution requirement of ideal mhd?
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; ideal mhd results are only physical at sufficient resolution.

## Q25: How does ideal mhd produce the classic two-sided jets?
**A:** Magnetic field lines collimate outflows along the spin axis; jets in ideal mhd are a natural outcome of magnetically-dominated coronae.

## Q26: What distinguishes an accretion 'state' in ideal mhd?
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; ideal mhd evolves between them statistically.

## Q27: How do you choose among ideal mhd snapshots for rendering?
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant.

## Q28: What roles do floors and ceilings play in ideal mhd?
**A:** Codes impose density/pressure floors to prevent negative states; ideal mhd consumers must be aware these floors matter near the horizon.

## Q29: How is output frequency chosen in ideal mhd?
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; ideal mhd files are large so snapshot cadence is a trade-off.

## Q30: What is a typical ideal mhd run cost?
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; ideal mhd data availability often limits the renderer, not the physics.

## Q31: How do you check a ideal mhd snapshot is physical?
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its ideal mhd radiative output.

## Q32: What approximation do most ideal mhd codes make about gravity?
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; ideal mhd is therefore a test particle in a fixed background.

## Q33: How does the disk become so hot in ideal mhd?
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; ideal mhd emissivity relies on that heat.

## Q34: What happens when ideal mhd resolution is doubled?
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates ideal mhd robustness.

## Q35: What is the role of initial magnetic field topology in ideal mhd?
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; ideal mhd initial conditions are a science choice.

## Q36: What output formats should your ideal mhd importer accept?
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; ideal mhd importer accuracy is as important as the renderer itself.

## Q37: How do you map ideal mhd cells to the raytracer grid?
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; ideal mhd mapping must be consistent with the code's grid functions.

## Q38: What is the simplest first ideal mhd test?
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average.

## Q39: How can missing physics show up in ideal mhd images?
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; ideal mhd images are calibrated against observed spectra before use.

## Q40: How can missing physics show up in ideal mhd images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; ideal mhd images are calibrated against observed spectra before use. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is the simplest first ideal mhd test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How do you map ideal mhd cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; ideal mhd mapping must be consistent with the code's grid functions. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What output formats should your ideal mhd importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; ideal mhd importer accuracy is as important as the renderer itself. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What is the role of initial magnetic field topology in ideal mhd - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; ideal mhd initial conditions are a science choice. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What happens when ideal mhd resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates ideal mhd robustness. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does the disk become so hot in ideal mhd - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; ideal mhd emissivity relies on that heat. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What approximation do most ideal mhd codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; ideal mhd is therefore a test particle in a fixed background. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How do you check a ideal mhd snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its ideal mhd radiative output. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What is a typical ideal mhd run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; ideal mhd data availability often limits the renderer, not the physics. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How is output frequency chosen in ideal mhd - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; ideal mhd files are large so snapshot cadence is a trade-off. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What roles do floors and ceilings play in ideal mhd - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; ideal mhd consumers must be aware these floors matter near the horizon. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How do you choose among ideal mhd snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What distinguishes an accretion 'state' in ideal mhd - justify your answer with a concrete production example.
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; ideal mhd evolves between them statistically. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does ideal mhd produce the classic two-sided jets - justify your answer with a concrete production example.
**A:** Magnetic field lines collimate outflows along the spin axis; jets in ideal mhd are a natural outcome of magnetically-dominated coronae. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What is the resolution requirement of ideal mhd - justify your answer with a concrete production example.
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; ideal mhd results are only physical at sufficient resolution. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What coordinate system does a code like HARM use in ideal mhd - justify your answer with a concrete production example.
**A:** Logarithmically concentrated coordinates around the horizon; ideal mhd interpretation of any Dump file requires reading that grid mapping. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How does ideal mhd handle magnetic divergence - justify your answer with a concrete production example.
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in ideal mhd injects spurious forces and must be actively controlled. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the biggest difficulty in ideal mhd - justify your answer with a concrete production example.
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: What variables does ideal mhd typically output - justify your answer with a concrete production example.
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the ideal mhd snapshot state. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: How do Athena++ and HARM fit into ideal mhd - justify your answer with a concrete production example.
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding ideal mhd means knowing what each code stores and how. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What is the conservative form in ideal mhd - justify your answer with a concrete production example.
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume ideal mhd codes. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why do black-hole images rely on ideal mhd - justify your answer with a concrete production example.
**A:** The observed emission comes from hot magnetized plasma; ideal mhd produces the density, temperature, velocity, and field data the raytracer converts to light. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What does ideal mhd add to an astrophysical accretion flow model - justify your answer with a concrete production example.
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What does ideal mhd add to an astrophysical accretion flow model - justify your answer with a concrete production example.
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why do black-hole images rely on ideal mhd - justify your answer with a concrete production example.
**A:** The observed emission comes from hot magnetized plasma; ideal mhd produces the density, temperature, velocity, and field data the raytracer converts to light. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What is the conservative form in ideal mhd - justify your answer with a concrete production example.
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume ideal mhd codes. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How do Athena++ and HARM fit into ideal mhd - justify your answer with a concrete production example.
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding ideal mhd means knowing what each code stores and how. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What variables does ideal mhd typically output - justify your answer with a concrete production example.
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the ideal mhd snapshot state. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What is the biggest difficulty in ideal mhd - justify your answer with a concrete production example.
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How does ideal mhd handle magnetic divergence - justify your answer with a concrete production example.
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in ideal mhd injects spurious forces and must be actively controlled. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What coordinate system does a code like HARM use in ideal mhd - justify your answer with a concrete production example.
**A:** Logarithmically concentrated coordinates around the horizon; ideal mhd interpretation of any Dump file requires reading that grid mapping. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What is the resolution requirement of ideal mhd - justify your answer with a concrete production example.
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; ideal mhd results are only physical at sufficient resolution. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does ideal mhd produce the classic two-sided jets - justify your answer with a concrete production example.
**A:** Magnetic field lines collimate outflows along the spin axis; jets in ideal mhd are a natural outcome of magnetically-dominated coronae. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What distinguishes an accretion 'state' in ideal mhd - justify your answer with a concrete production example.
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; ideal mhd evolves between them statistically. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How do you choose among ideal mhd snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What roles do floors and ceilings play in ideal mhd - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; ideal mhd consumers must be aware these floors matter near the horizon. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: How is output frequency chosen in ideal mhd - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; ideal mhd files are large so snapshot cadence is a trade-off. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What is a typical ideal mhd run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; ideal mhd data availability often limits the renderer, not the physics. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How do you check a ideal mhd snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its ideal mhd radiative output. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What approximation do most ideal mhd codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; ideal mhd is therefore a test particle in a fixed background. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does the disk become so hot in ideal mhd - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; ideal mhd emissivity relies on that heat. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What happens when ideal mhd resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates ideal mhd robustness. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What is the role of initial magnetic field topology in ideal mhd - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; ideal mhd initial conditions are a science choice. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What output formats should your ideal mhd importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; ideal mhd importer accuracy is as important as the renderer itself. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How do you map ideal mhd cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; ideal mhd mapping must be consistent with the code's grid functions. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the simplest first ideal mhd test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How can missing physics show up in ideal mhd images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; ideal mhd images are calibrated against observed spectra before use. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How can missing physics show up in ideal mhd images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; ideal mhd images are calibrated against observed spectra before use. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is the simplest first ideal mhd test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How do you map ideal mhd cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; ideal mhd mapping must be consistent with the code's grid functions. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What output formats should your ideal mhd importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; ideal mhd importer accuracy is as important as the renderer itself. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What is the role of initial magnetic field topology in ideal mhd - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; ideal mhd initial conditions are a science choice. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What happens when ideal mhd resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates ideal mhd robustness. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does the disk become so hot in ideal mhd - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; ideal mhd emissivity relies on that heat. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What approximation do most ideal mhd codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; ideal mhd is therefore a test particle in a fixed background. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How do you check a ideal mhd snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its ideal mhd radiative output. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What is a typical ideal mhd run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; ideal mhd data availability often limits the renderer, not the physics. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How is output frequency chosen in ideal mhd - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; ideal mhd files are large so snapshot cadence is a trade-off. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What roles do floors and ceilings play in ideal mhd - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; ideal mhd consumers must be aware these floors matter near the horizon. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How do you choose among ideal mhd snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying ideal mhd in code review and regression tests keeps the whole pipeline trustworthy.
