# Grmhd — Accretion Physics Interview Questions and Answers

## Q1: What sets the accretion rate?
**A:** The turbulent angular-momentum transport (MRI stress alpha) times the surface density; observationally, Mdot ~ alpha (H/R)^2 Omega rho-ish - the Shakura-Sunyaev scaling.

## Q2: What is the Shakura-Sunyaev alpha-disk?
**A:** The standard parametrization: viscosity nu = alpha c_s H; alpha ~ 0.01-0.1 from MRI; all disk models start from this concept.

## Q3: How does MHD transport angular momentum?
**A:** The Maxwell (B_r B_phi) and Reynolds stresses dominate over molecular; their ratio defines the effective alpha - measurable in GRMHD outputs.

## Q4: What is the MRI (Magnetorotational instability)?
**A:** The weak-field turbulence engine: differential rotation stretches and feeds springs in B, destabilizing the flow - the disk's universal dynamo.

## Q5: What is the condition for MRI growth?
**A:** The profile must satisfy the Rayleigh criterion (dOmega^2/dr < 0 region) with fast growth ~ Omega; that holds out to ISCO - the instability saturates into turbulence.

## Q6: How does the disk evolve in the saturation?
**A:** Balanced transport + inflow: surface density evolves toward the steady-state solution with accretion deluged by the turbulence - the 'steady disk' idealization.

## Q7: What is the Novikov-Thorne standard model?
**A:** The thin-disk analytic steady solution with (alpha) transport and inner edge at ISCO - the baseline brightness that GRMHD upgrades beyond.

## Q8: What does GRMHD correct?
**A:** ISCO assumption is approximate: plunging regions, magnetic fields, stress at the ISCO all alter the emission (hence image rings differ from NT).

## Q9: What is the role of electron temperature?
**A:** The image's ring brightness depends on raising electrons above ions (Te != Tp via reconnection+electrons cooling); GRMHD outputs gas temp, emission needs the electron prescription.

## Q10: How does Mdot connect to the raytracer?
**A:** accretion flushes densities; the raytracer samples rho/B from the run, so Mdot translates into emissivity (through the magnetic field's synchrotron scaling).

## Q11: What is the disk's scale height H/r?
**A:** The dimensionless aspect: hotter/ionized disks puff; the emissivity integration in the raytracer spans full z since H/r can be big (0.1-0.4).

## Q12: What is the wind/outflow balance?
**A:** A fraction of the accreted mass leaves as winds/jets; the observed jet power correlates with the magnetic flux threading the horizon (MAD/explosions).

## Q13: What is the variability timescale?
**A:** Orbital timescale ~ a few x M for the inner disk; observed flickers encode that - the raytracer's movie cadence then pictures the orbit-scale dynamics.

## Q14: What is the observable imprint of the plunging region?
**A:** Inside r<=6M the gas plunges; its density/spin structure sets the innermost ring's brightness - arguably the EHT's most exquisite probe.

## Q15: What is the summary statement?
**A:** The disk is turbulence-regulated accretion ending at a plunging inner edge; your raytracer renders exactly this plasma state - its realism derives from the simulation, not the camera.

## Q16: What does accretion physics add to an astrophysical accretion flow model?
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need.

## Q17: Why do black-hole images rely on accretion physics?
**A:** The observed emission comes from hot magnetized plasma; accretion physics produces the density, temperature, velocity, and field data the raytracer converts to light.

## Q18: What is the conservative form in accretion physics?
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume accretion physics codes.

## Q19: How do Athena++ and HARM fit into accretion physics?
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding accretion physics means knowing what each code stores and how.

## Q20: What variables does accretion physics typically output?
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the accretion physics snapshot state.

## Q21: What is the biggest difficulty in accretion physics?
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes.

## Q22: How does accretion physics handle magnetic divergence?
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in accretion physics injects spurious forces and must be actively controlled.

## Q23: What coordinate system does a code like HARM use in accretion physics?
**A:** Logarithmically concentrated coordinates around the horizon; accretion physics interpretation of any Dump file requires reading that grid mapping.

## Q24: What is the resolution requirement of accretion physics?
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; accretion physics results are only physical at sufficient resolution.

## Q25: How does accretion physics produce the classic two-sided jets?
**A:** Magnetic field lines collimate outflows along the spin axis; jets in accretion physics are a natural outcome of magnetically-dominated coronae.

## Q26: What distinguishes an accretion 'state' in accretion physics?
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; accretion physics evolves between them statistically.

## Q27: How do you choose among accretion physics snapshots for rendering?
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant.

## Q28: What roles do floors and ceilings play in accretion physics?
**A:** Codes impose density/pressure floors to prevent negative states; accretion physics consumers must be aware these floors matter near the horizon.

## Q29: How is output frequency chosen in accretion physics?
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; accretion physics files are large so snapshot cadence is a trade-off.

## Q30: What is a typical accretion physics run cost?
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; accretion physics data availability often limits the renderer, not the physics.

## Q31: How do you check a accretion physics snapshot is physical?
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its accretion physics radiative output.

## Q32: What approximation do most accretion physics codes make about gravity?
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; accretion physics is therefore a test particle in a fixed background.

## Q33: How does the disk become so hot in accretion physics?
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; accretion physics emissivity relies on that heat.

## Q34: What happens when accretion physics resolution is doubled?
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates accretion physics robustness.

## Q35: What is the role of initial magnetic field topology in accretion physics?
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; accretion physics initial conditions are a science choice.

## Q36: What output formats should your accretion physics importer accept?
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; accretion physics importer accuracy is as important as the renderer itself.

## Q37: How do you map accretion physics cells to the raytracer grid?
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; accretion physics mapping must be consistent with the code's grid functions.

## Q38: What is the simplest first accretion physics test?
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average.

## Q39: How can missing physics show up in accretion physics images?
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; accretion physics images are calibrated against observed spectra before use.

## Q40: How can missing physics show up in accretion physics images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; accretion physics images are calibrated against observed spectra before use. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is the simplest first accretion physics test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How do you map accretion physics cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; accretion physics mapping must be consistent with the code's grid functions. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What output formats should your accretion physics importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; accretion physics importer accuracy is as important as the renderer itself. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What is the role of initial magnetic field topology in accretion physics - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; accretion physics initial conditions are a science choice. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What happens when accretion physics resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates accretion physics robustness. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does the disk become so hot in accretion physics - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; accretion physics emissivity relies on that heat. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What approximation do most accretion physics codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; accretion physics is therefore a test particle in a fixed background. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How do you check a accretion physics snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its accretion physics radiative output. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What is a typical accretion physics run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; accretion physics data availability often limits the renderer, not the physics. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How is output frequency chosen in accretion physics - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; accretion physics files are large so snapshot cadence is a trade-off. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What roles do floors and ceilings play in accretion physics - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; accretion physics consumers must be aware these floors matter near the horizon. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How do you choose among accretion physics snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What distinguishes an accretion 'state' in accretion physics - justify your answer with a concrete production example.
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; accretion physics evolves between them statistically. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does accretion physics produce the classic two-sided jets - justify your answer with a concrete production example.
**A:** Magnetic field lines collimate outflows along the spin axis; jets in accretion physics are a natural outcome of magnetically-dominated coronae. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What is the resolution requirement of accretion physics - justify your answer with a concrete production example.
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; accretion physics results are only physical at sufficient resolution. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What coordinate system does a code like HARM use in accretion physics - justify your answer with a concrete production example.
**A:** Logarithmically concentrated coordinates around the horizon; accretion physics interpretation of any Dump file requires reading that grid mapping. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How does accretion physics handle magnetic divergence - justify your answer with a concrete production example.
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in accretion physics injects spurious forces and must be actively controlled. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the biggest difficulty in accretion physics - justify your answer with a concrete production example.
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: What variables does accretion physics typically output - justify your answer with a concrete production example.
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the accretion physics snapshot state. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: How do Athena++ and HARM fit into accretion physics - justify your answer with a concrete production example.
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding accretion physics means knowing what each code stores and how. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What is the conservative form in accretion physics - justify your answer with a concrete production example.
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume accretion physics codes. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why do black-hole images rely on accretion physics - justify your answer with a concrete production example.
**A:** The observed emission comes from hot magnetized plasma; accretion physics produces the density, temperature, velocity, and field data the raytracer converts to light. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What does accretion physics add to an astrophysical accretion flow model - justify your answer with a concrete production example.
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What does accretion physics add to an astrophysical accretion flow model - justify your answer with a concrete production example.
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why do black-hole images rely on accretion physics - justify your answer with a concrete production example.
**A:** The observed emission comes from hot magnetized plasma; accretion physics produces the density, temperature, velocity, and field data the raytracer converts to light. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What is the conservative form in accretion physics - justify your answer with a concrete production example.
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume accretion physics codes. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How do Athena++ and HARM fit into accretion physics - justify your answer with a concrete production example.
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding accretion physics means knowing what each code stores and how. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What variables does accretion physics typically output - justify your answer with a concrete production example.
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the accretion physics snapshot state. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What is the biggest difficulty in accretion physics - justify your answer with a concrete production example.
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How does accretion physics handle magnetic divergence - justify your answer with a concrete production example.
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in accretion physics injects spurious forces and must be actively controlled. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What coordinate system does a code like HARM use in accretion physics - justify your answer with a concrete production example.
**A:** Logarithmically concentrated coordinates around the horizon; accretion physics interpretation of any Dump file requires reading that grid mapping. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What is the resolution requirement of accretion physics - justify your answer with a concrete production example.
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; accretion physics results are only physical at sufficient resolution. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does accretion physics produce the classic two-sided jets - justify your answer with a concrete production example.
**A:** Magnetic field lines collimate outflows along the spin axis; jets in accretion physics are a natural outcome of magnetically-dominated coronae. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What distinguishes an accretion 'state' in accretion physics - justify your answer with a concrete production example.
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; accretion physics evolves between them statistically. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How do you choose among accretion physics snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What roles do floors and ceilings play in accretion physics - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; accretion physics consumers must be aware these floors matter near the horizon. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: How is output frequency chosen in accretion physics - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; accretion physics files are large so snapshot cadence is a trade-off. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What is a typical accretion physics run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; accretion physics data availability often limits the renderer, not the physics. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How do you check a accretion physics snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its accretion physics radiative output. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What approximation do most accretion physics codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; accretion physics is therefore a test particle in a fixed background. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does the disk become so hot in accretion physics - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; accretion physics emissivity relies on that heat. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What happens when accretion physics resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates accretion physics robustness. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What is the role of initial magnetic field topology in accretion physics - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; accretion physics initial conditions are a science choice. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What output formats should your accretion physics importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; accretion physics importer accuracy is as important as the renderer itself. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How do you map accretion physics cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; accretion physics mapping must be consistent with the code's grid functions. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the simplest first accretion physics test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How can missing physics show up in accretion physics images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; accretion physics images are calibrated against observed spectra before use. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How can missing physics show up in accretion physics images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; accretion physics images are calibrated against observed spectra before use. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is the simplest first accretion physics test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How do you map accretion physics cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; accretion physics mapping must be consistent with the code's grid functions. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What output formats should your accretion physics importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; accretion physics importer accuracy is as important as the renderer itself. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What is the role of initial magnetic field topology in accretion physics - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; accretion physics initial conditions are a science choice. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What happens when accretion physics resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates accretion physics robustness. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does the disk become so hot in accretion physics - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; accretion physics emissivity relies on that heat. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What approximation do most accretion physics codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; accretion physics is therefore a test particle in a fixed background. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How do you check a accretion physics snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its accretion physics radiative output. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What is a typical accretion physics run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; accretion physics data availability often limits the renderer, not the physics. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How is output frequency chosen in accretion physics - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; accretion physics files are large so snapshot cadence is a trade-off. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What roles do floors and ceilings play in accretion physics - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; accretion physics consumers must be aware these floors matter near the horizon. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How do you choose among accretion physics snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying accretion physics in code review and regression tests keeps the whole pipeline trustworthy.
