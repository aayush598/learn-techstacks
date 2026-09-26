# Grmhd — Initial Conditions Interview Questions and Answers

## Q1: What is the canonical GRMHD initial condition?
**A:** A Fishbone-Moncrief (or Chakrabarti) torus in hydrodynamic equilibrium threaded by a weak poloidal field - the standard seed for disk simulations.

## Q2: What is the torus equilibrium?
**A:** An axisymmetric gas configuration with constant specific enthalpy (uniform angular momentum pattern) in the hole's potential - steady if field is ignored.

## Q3: How is the weak seed field chosen?
**A:** A poloidal loop with pressure-balanced beta (e.g., beta=100) through the torus; the MRI then amplifies it - the turbulence onset is seeded, not imposed.

## Q4: What masses/radii are typical?
**A:** Torus scale height, inner radius ~ ISCO, outer ~ 30-60M; mass normalized so Mdot is physical after scaling - all set relative to the hole's mass.

## Q5: Why is the initial field tiny?
**A:** If beta is astronomically small, MRI saturates immediately and lacks the dynamo phase; a gentle seed lets the code 'grow' its own turbulence.

## Q6: What are the alternatives?
**A:** SANE setups (weak field, saturated turbulence) vs MAD (strong field near the horizon); initial B structure decides which attractor the run reaches.

## Q7: How do you set theta/phi discretization to match MRI?
**A:** Cells must resolve the MRI's fastest-growth wavelength; the initial setup must satisfy that constraint across the disk - verified a priori.

## Q8: What happens to a mismatched initial state?
**A:** Shocks launch, the disk relaxes violently, and the transient can dominate the first 1000 M of output (the 'relaxation phase' to discard).

## Q9: How does the initial density profile look?
**A:** A fish-tail cross-section with maximum at the pressure-support radius, tapers in/out; the code keeps density floors in the halo.

## Q10: What is the role of the fictitious viscosity?
**A:** MHD turbulence replaces it; the early transient is effectively the code's way of generating the physical stress - so discard or post-clean it.

## Q11: How do you validate the IC?
**A:** Run the torus with B=0: it must remain stationary to simulation precision - the equilibrium-russia test of the metric + grid implementation.

## Q12: What is a common resolution-study starter?
**A:** Compare two resolutions (e.g., 128^3 vs 256^3) on the same IC; MRI growth rate/max must match the fastest-growing-mode prediction.

## Q13: What output cadence matters?
**A:** Flash-low for discs: aligned analyses like Mdot need cadence < a few x M; the raytracer wants saved snapshots only at its own virtualization times.

## Q14: How are these ICs shared/reproduced?
**A:** Standard problem decks in the literature and code repos; document the seed, mass, beta, grid of every run - else results aren't publishable.

## Q15: What is the analyst's golden rule?
**A:** Every endpoint claim (Mdot, jet power, ring profile) states the IC and grid it came from; reproducibility is the code's scientific contract.

## Q16: What does initial conditions add to an astrophysical accretion flow model?
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need.

## Q17: Why do black-hole images rely on initial conditions?
**A:** The observed emission comes from hot magnetized plasma; initial conditions produces the density, temperature, velocity, and field data the raytracer converts to light.

## Q18: What is the conservative form in initial conditions?
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume initial conditions codes.

## Q19: How do Athena++ and HARM fit into initial conditions?
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding initial conditions means knowing what each code stores and how.

## Q20: What variables does initial conditions typically output?
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the initial conditions snapshot state.

## Q21: What is the biggest difficulty in initial conditions?
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes.

## Q22: How does initial conditions handle magnetic divergence?
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in initial conditions injects spurious forces and must be actively controlled.

## Q23: What coordinate system does a code like HARM use in initial conditions?
**A:** Logarithmically concentrated coordinates around the horizon; initial conditions interpretation of any Dump file requires reading that grid mapping.

## Q24: What is the resolution requirement of initial conditions?
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; initial conditions results are only physical at sufficient resolution.

## Q25: How does initial conditions produce the classic two-sided jets?
**A:** Magnetic field lines collimate outflows along the spin axis; jets in initial conditions are a natural outcome of magnetically-dominated coronae.

## Q26: What distinguishes an accretion 'state' in initial conditions?
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; initial conditions evolves between them statistically.

## Q27: How do you choose among initial conditions snapshots for rendering?
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant.

## Q28: What roles do floors and ceilings play in initial conditions?
**A:** Codes impose density/pressure floors to prevent negative states; initial conditions consumers must be aware these floors matter near the horizon.

## Q29: How is output frequency chosen in initial conditions?
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; initial conditions files are large so snapshot cadence is a trade-off.

## Q30: What is a typical initial conditions run cost?
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; initial conditions data availability often limits the renderer, not the physics.

## Q31: How do you check a initial conditions snapshot is physical?
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its initial conditions radiative output.

## Q32: What approximation do most initial conditions codes make about gravity?
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; initial conditions is therefore a test particle in a fixed background.

## Q33: How does the disk become so hot in initial conditions?
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; initial conditions emissivity relies on that heat.

## Q34: What happens when initial conditions resolution is doubled?
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates initial conditions robustness.

## Q35: What is the role of initial magnetic field topology in initial conditions?
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; initial conditions initial conditions are a science choice.

## Q36: What output formats should your initial conditions importer accept?
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; initial conditions importer accuracy is as important as the renderer itself.

## Q37: How do you map initial conditions cells to the raytracer grid?
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; initial conditions mapping must be consistent with the code's grid functions.

## Q38: What is the simplest first initial conditions test?
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average.

## Q39: How can missing physics show up in initial conditions images?
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; initial conditions images are calibrated against observed spectra before use.

## Q40: How can missing physics show up in initial conditions images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; initial conditions images are calibrated against observed spectra before use. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is the simplest first initial conditions test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How do you map initial conditions cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; initial conditions mapping must be consistent with the code's grid functions. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What output formats should your initial conditions importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; initial conditions importer accuracy is as important as the renderer itself. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What is the role of initial magnetic field topology in initial conditions - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; initial conditions initial conditions are a science choice. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What happens when initial conditions resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates initial conditions robustness. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does the disk become so hot in initial conditions - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; initial conditions emissivity relies on that heat. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What approximation do most initial conditions codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; initial conditions is therefore a test particle in a fixed background. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How do you check a initial conditions snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its initial conditions radiative output. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What is a typical initial conditions run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; initial conditions data availability often limits the renderer, not the physics. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How is output frequency chosen in initial conditions - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; initial conditions files are large so snapshot cadence is a trade-off. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What roles do floors and ceilings play in initial conditions - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; initial conditions consumers must be aware these floors matter near the horizon. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How do you choose among initial conditions snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What distinguishes an accretion 'state' in initial conditions - justify your answer with a concrete production example.
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; initial conditions evolves between them statistically. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does initial conditions produce the classic two-sided jets - justify your answer with a concrete production example.
**A:** Magnetic field lines collimate outflows along the spin axis; jets in initial conditions are a natural outcome of magnetically-dominated coronae. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What is the resolution requirement of initial conditions - justify your answer with a concrete production example.
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; initial conditions results are only physical at sufficient resolution. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What coordinate system does a code like HARM use in initial conditions - justify your answer with a concrete production example.
**A:** Logarithmically concentrated coordinates around the horizon; initial conditions interpretation of any Dump file requires reading that grid mapping. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How does initial conditions handle magnetic divergence - justify your answer with a concrete production example.
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in initial conditions injects spurious forces and must be actively controlled. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the biggest difficulty in initial conditions - justify your answer with a concrete production example.
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: What variables does initial conditions typically output - justify your answer with a concrete production example.
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the initial conditions snapshot state. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: How do Athena++ and HARM fit into initial conditions - justify your answer with a concrete production example.
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding initial conditions means knowing what each code stores and how. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What is the conservative form in initial conditions - justify your answer with a concrete production example.
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume initial conditions codes. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why do black-hole images rely on initial conditions - justify your answer with a concrete production example.
**A:** The observed emission comes from hot magnetized plasma; initial conditions produces the density, temperature, velocity, and field data the raytracer converts to light. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What does initial conditions add to an astrophysical accretion flow model - justify your answer with a concrete production example.
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What does initial conditions add to an astrophysical accretion flow model - justify your answer with a concrete production example.
**A:** It couples the plasma dynamics to magnetic fields through the fluid equations, enabling magnetically-driven turbulence that real disks need. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why do black-hole images rely on initial conditions - justify your answer with a concrete production example.
**A:** The observed emission comes from hot magnetized plasma; initial conditions produces the density, temperature, velocity, and field data the raytracer converts to light. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What is the conservative form in initial conditions - justify your answer with a concrete production example.
**A:** Fluxes expressed in conserved variables so shocks are captured without spurious oscillations - the foundation of finite-volume initial conditions codes. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How do Athena++ and HARM fit into initial conditions - justify your answer with a concrete production example.
**A:** They are production GRMHD solvers; your raytracer consumes their output grids, so understanding initial conditions means knowing what each code stores and how. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What variables does initial conditions typically output - justify your answer with a concrete production example.
**A:** Density, internal energy/pressure, four-velocity or 3-velocity, magnetic field components, and optionally temperature - the initial conditions snapshot state. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What is the biggest difficulty in initial conditions - justify your answer with a concrete production example.
**A:** Recovering primitive variables (pressure, velocity) from conserved ones after an update, an iterative step that can break in extreme regimes. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How does initial conditions handle magnetic divergence - justify your answer with a concrete production example.
**A:** Through constrained transport or divergence cleaning; a non-zero divergence in initial conditions injects spurious forces and must be actively controlled. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What coordinate system does a code like HARM use in initial conditions - justify your answer with a concrete production example.
**A:** Logarithmically concentrated coordinates around the horizon; initial conditions interpretation of any Dump file requires reading that grid mapping. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What is the resolution requirement of initial conditions - justify your answer with a concrete production example.
**A:** The MRI wavelength must be resolved across the disk for turbulence to develop; initial conditions results are only physical at sufficient resolution. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does initial conditions produce the classic two-sided jets - justify your answer with a concrete production example.
**A:** Magnetic field lines collimate outflows along the spin axis; jets in initial conditions are a natural outcome of magnetically-dominated coronae. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What distinguishes an accretion 'state' in initial conditions - justify your answer with a concrete production example.
**A:** The magnetization and density of the flow - SANE flows are weakly magnetized while MAD flows reach magnetic saturation; initial conditions evolves between them statistically. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How do you choose among initial conditions snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What roles do floors and ceilings play in initial conditions - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; initial conditions consumers must be aware these floors matter near the horizon. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: How is output frequency chosen in initial conditions - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; initial conditions files are large so snapshot cadence is a trade-off. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What is a typical initial conditions run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; initial conditions data availability often limits the renderer, not the physics. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How do you check a initial conditions snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its initial conditions radiative output. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What approximation do most initial conditions codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; initial conditions is therefore a test particle in a fixed background. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does the disk become so hot in initial conditions - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; initial conditions emissivity relies on that heat. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What happens when initial conditions resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates initial conditions robustness. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What is the role of initial magnetic field topology in initial conditions - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; initial conditions initial conditions are a science choice. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What output formats should your initial conditions importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; initial conditions importer accuracy is as important as the renderer itself. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How do you map initial conditions cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; initial conditions mapping must be consistent with the code's grid functions. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the simplest first initial conditions test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How can missing physics show up in initial conditions images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; initial conditions images are calibrated against observed spectra before use. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How can missing physics show up in initial conditions images - justify your answer with a concrete production example.
**A:** Without cooling or radiation transfer the temperatures may be unrealistically hot; initial conditions images are calibrated against observed spectra before use. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is the simplest first initial conditions test - justify your answer with a concrete production example.
**A:** Load a snapshot, interpolate density along a ray, and confirm the disk radial profile matches the code's published azimuthal average. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How do you map initial conditions cells to the raytracer grid - justify your answer with a concrete production example.
**A:** Reconstruct cell-centered fields, transform to the raytracer coordinates, and interpolate; initial conditions mapping must be consistent with the code's grid functions. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What output formats should your initial conditions importer accept - justify your answer with a concrete production example.
**A:** HARM binary dumps, Athena++ HDF5, and VTK/CSV conversions; initial conditions importer accuracy is as important as the renderer itself. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What is the role of initial magnetic field topology in initial conditions - justify your answer with a concrete production example.
**A:** Poloidal fields seed the MRI and ultimately set the jet/power output, while toroidal configurations evolve differently; initial conditions initial conditions are a science choice. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What happens when initial conditions resolution is doubled - justify your answer with a concrete production example.
**A:** Turbulent structures, magnetic saturation, and flux through the horizon become better converged; comparing resolutions validates initial conditions robustness. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does the disk become so hot in initial conditions - justify your answer with a concrete production example.
**A:** Turbulent dissipation converts magnetic energy to heat, keeping the MRI-driven flow near virial temperature; initial conditions emissivity relies on that heat. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What approximation do most initial conditions codes make about gravity - justify your answer with a concrete production example.
**A:** However, they are not GRMHD: they fix the metric (often Kerr) and ignore the plasma's own gravity; initial conditions is therefore a test particle in a fixed background. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How do you check a initial conditions snapshot is physical - justify your answer with a concrete production example.
**A:** Verify steady rotation curves, bounded Lorentz factors, real-velocity fields, and conservation trends before trusting its initial conditions radiative output. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What is a typical initial conditions run cost - justify your answer with a concrete production example.
**A:** Millions of core-hours to reach steady state on a few hundred grid cells per axis; initial conditions data availability often limits the renderer, not the physics. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How is output frequency chosen in initial conditions - justify your answer with a concrete production example.
**A:** To resolve the variability timescale of interest - sub-orbital for flares, many orbits for movies; initial conditions files are large so snapshot cadence is a trade-off. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What roles do floors and ceilings play in initial conditions - justify your answer with a concrete production example.
**A:** Codes impose density/pressure floors to prevent negative states; initial conditions consumers must be aware these floors matter near the horizon. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How do you choose among initial conditions snapshots for rendering - justify your answer with a concrete production example.
**A:** Time-average over several snapshots of quasi-steady turbulence so the image is a meaningful average rather than one turbulent instant. A concrete example: consistently applying initial conditions in code review and regression tests keeps the whole pipeline trustworthy.
