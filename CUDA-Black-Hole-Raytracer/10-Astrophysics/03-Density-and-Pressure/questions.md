# Astrophysics — Density And Pressure Interview Questions and Answers

## Q1: What is the density structure of the inner disk?
**A:** A peak near the ISCO and a decaying outward to the outer boundary; below a floor density the code interpolates - the density field is the emissivity's volume weight.

## Q2: Why does density matter to the image?
**A:** Synchrotron emissivity scales ~ n_e B^2-ish; the density times field product sets brightness - dense regions and B-peaks both light up.

## Q3: How does pressure determine the flow?
**A:** Gas+magetic pressure sets the height/profile and the turbulence state (beta); the density/pressure/B relationship is the GRMHD's internal equilibrium.

## Q4: What is the plasma-beta map?
**A:** beta = p_gas/p_B varies from beta>>1 in the disk body to beta~1 near the plunging edge - the image's contrast between disk and magnetized funnel.

## Q5: What is the outer-atmosphere behavior?
**A:** The floor density halo fills the domain edges; its presence biases outer-ray images - report the floor with every density-relevant render.

## Q6: How is density scaled to real n_e?
**A:** n_e is derived from the code density times a normalization determined by the accretion rate model - the 'mass scale' factor converting code units.

## Q7: What is the 'density floor' artifact?
**A:** The ad-hoc minimum density inflates emission in vacuum (funnel/jet); the code flags floor-affected cells in the emissivity map - transparent rendering.

## Q8: How does density peak with the plunging region?
**A:** The near-ISCO density max concentrates the ring emission - exactly why the ring hugs the horizon scale rather than the thin-disk 6M edge.

## Q9: What is the relation to Mdot?
**A:** Mdot = 2 pi r rho v at the ISCO; the density profile and velocity normalize each other - a consistency check the model must obey.

## Q10: How do you validate density in the render?
**A:** The radially-integrated column density and total flux from a snapshot must match an independent 1-D calculation - the density-to-light pipeline test.

## Q11: What is the summary?
**A:** Density and pressure set WHERE and HOW MUCH the disk glows: n_e is the volume weight, beta the morphology, floors the honest artifact flag.

## Q12: Why is density and pressure central to interpreting black-hole images?
**A:** Observables like the ring, shadow, and Doppler asymmetry trace directly to density and pressure, so understanding it lets you read images as physics.

## Q13: What does density and pressure predict about the photon ring?
**A:** The bright ring radius is set by density and pressure quantities like the photon sphere and spin, making it a probe of the spacetime itself.

## Q14: How does density and pressure explain the shadow?
**A:** Captured photons leave a dark central region whose size and asymmetry depend on density and pressure - mass, spin, and viewing angle.

## Q15: What observations constrain density and pressure?
**A:** EHT images of M87* and Sgr A* measure ring diameter and asymmetry; density and pressure inversions use those to constrain the spacetime.

## Q16: Why do density and pressure models show the disk brighter on one side?
**A:** Relativistic beaming amplifies emission from the approaching side; density and pressure visibility depends on the disk velocity and line of sight.

## Q17: How does density and pressure guide the choice of simulation data?
**A:** Disk state (SANE/MAD), electron distribution, and spin control morphology; density and pressure selection is part of the science, not just plumbing.

## Q18: What does density and pressure say about temperature?
**A:** The inner flow reaches billions of Kelvin; density and pressure emission intensity maps to temperature and magnetic field through emissivity relations.

## Q19: How is density and pressure measured with EHT?
**A:** Very long baseline interferometry synthesizes a horizon-scale aperture; density and pressure plausibility is judged against its reconstructed images.

## Q20: What distinguishes density and pressure for supermassive vs stellar black holes?
**A:** Scales shift by mass, but dimensionless quantities like the photon-ring radius are universal; density and pressure transfers across masses by scaling.

## Q21: What role do jets play in density and pressure?
**A:** Poynting-flux outflows can shine in their own right and shape the outermost emission; density and pressure includes them for completeness.

## Q22: How does density and pressure treat the electron thermodynamics?
**A:** Since GRMHD often does not track electron vs ion temperature, density and pressure uses proxies like R-beta prescriptions to convert fluid heating into emissivity.

## Q23: What is the next frontier in density and pressure?
**A:** Time-dependent images and movie predictions from turbulent simulations observed by upgraded EHT arrays; density and pressure is moving from stills to dynamics.

## Q24: What is the next frontier in density and pressure - justify your answer with a concrete production example.
**A:** Time-dependent images and movie predictions from turbulent simulations observed by upgraded EHT arrays; density and pressure is moving from stills to dynamics. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q25: How does density and pressure treat the electron thermodynamics - justify your answer with a concrete production example.
**A:** Since GRMHD often does not track electron vs ion temperature, density and pressure uses proxies like R-beta prescriptions to convert fluid heating into emissivity. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q26: What role do jets play in density and pressure - justify your answer with a concrete production example.
**A:** Poynting-flux outflows can shine in their own right and shape the outermost emission; density and pressure includes them for completeness. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q27: What distinguishes density and pressure for supermassive vs stellar black holes - justify your answer with a concrete production example.
**A:** Scales shift by mass, but dimensionless quantities like the photon-ring radius are universal; density and pressure transfers across masses by scaling. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q28: How is density and pressure measured with EHT - justify your answer with a concrete production example.
**A:** Very long baseline interferometry synthesizes a horizon-scale aperture; density and pressure plausibility is judged against its reconstructed images. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q29: What does density and pressure say about temperature - justify your answer with a concrete production example.
**A:** The inner flow reaches billions of Kelvin; density and pressure emission intensity maps to temperature and magnetic field through emissivity relations. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q30: How does density and pressure guide the choice of simulation data - justify your answer with a concrete production example.
**A:** Disk state (SANE/MAD), electron distribution, and spin control morphology; density and pressure selection is part of the science, not just plumbing. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q31: Why do density and pressure models show the disk brighter on one side - justify your answer with a concrete production example.
**A:** Relativistic beaming amplifies emission from the approaching side; density and pressure visibility depends on the disk velocity and line of sight. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q32: What observations constrain density and pressure - justify your answer with a concrete production example.
**A:** EHT images of M87* and Sgr A* measure ring diameter and asymmetry; density and pressure inversions use those to constrain the spacetime. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q33: How does density and pressure explain the shadow - justify your answer with a concrete production example.
**A:** Captured photons leave a dark central region whose size and asymmetry depend on density and pressure - mass, spin, and viewing angle. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q34: What does density and pressure predict about the photon ring - justify your answer with a concrete production example.
**A:** The bright ring radius is set by density and pressure quantities like the photon sphere and spin, making it a probe of the spacetime itself. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q35: Why is density and pressure central to interpreting black-hole images - justify your answer with a concrete production example.
**A:** Observables like the ring, shadow, and Doppler asymmetry trace directly to density and pressure, so understanding it lets you read images as physics. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q36: Why is density and pressure central to interpreting black-hole images - justify your answer with a concrete production example.
**A:** Observables like the ring, shadow, and Doppler asymmetry trace directly to density and pressure, so understanding it lets you read images as physics. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q37: What does density and pressure predict about the photon ring - justify your answer with a concrete production example.
**A:** The bright ring radius is set by density and pressure quantities like the photon sphere and spin, making it a probe of the spacetime itself. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q38: How does density and pressure explain the shadow - justify your answer with a concrete production example.
**A:** Captured photons leave a dark central region whose size and asymmetry depend on density and pressure - mass, spin, and viewing angle. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q39: What observations constrain density and pressure - justify your answer with a concrete production example.
**A:** EHT images of M87* and Sgr A* measure ring diameter and asymmetry; density and pressure inversions use those to constrain the spacetime. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q40: Why do density and pressure models show the disk brighter on one side - justify your answer with a concrete production example.
**A:** Relativistic beaming amplifies emission from the approaching side; density and pressure visibility depends on the disk velocity and line of sight. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: How does density and pressure guide the choice of simulation data - justify your answer with a concrete production example.
**A:** Disk state (SANE/MAD), electron distribution, and spin control morphology; density and pressure selection is part of the science, not just plumbing. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What does density and pressure say about temperature - justify your answer with a concrete production example.
**A:** The inner flow reaches billions of Kelvin; density and pressure emission intensity maps to temperature and magnetic field through emissivity relations. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: How is density and pressure measured with EHT - justify your answer with a concrete production example.
**A:** Very long baseline interferometry synthesizes a horizon-scale aperture; density and pressure plausibility is judged against its reconstructed images. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What distinguishes density and pressure for supermassive vs stellar black holes - justify your answer with a concrete production example.
**A:** Scales shift by mass, but dimensionless quantities like the photon-ring radius are universal; density and pressure transfers across masses by scaling. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What role do jets play in density and pressure - justify your answer with a concrete production example.
**A:** Poynting-flux outflows can shine in their own right and shape the outermost emission; density and pressure includes them for completeness. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does density and pressure treat the electron thermodynamics - justify your answer with a concrete production example.
**A:** Since GRMHD often does not track electron vs ion temperature, density and pressure uses proxies like R-beta prescriptions to convert fluid heating into emissivity. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What is the next frontier in density and pressure - justify your answer with a concrete production example.
**A:** Time-dependent images and movie predictions from turbulent simulations observed by upgraded EHT arrays; density and pressure is moving from stills to dynamics. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: What is the next frontier in density and pressure - justify your answer with a concrete production example.
**A:** Time-dependent images and movie predictions from turbulent simulations observed by upgraded EHT arrays; density and pressure is moving from stills to dynamics. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: How does density and pressure treat the electron thermodynamics - justify your answer with a concrete production example.
**A:** Since GRMHD often does not track electron vs ion temperature, density and pressure uses proxies like R-beta prescriptions to convert fluid heating into emissivity. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What role do jets play in density and pressure - justify your answer with a concrete production example.
**A:** Poynting-flux outflows can shine in their own right and shape the outermost emission; density and pressure includes them for completeness. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What distinguishes density and pressure for supermassive vs stellar black holes - justify your answer with a concrete production example.
**A:** Scales shift by mass, but dimensionless quantities like the photon-ring radius are universal; density and pressure transfers across masses by scaling. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How is density and pressure measured with EHT - justify your answer with a concrete production example.
**A:** Very long baseline interferometry synthesizes a horizon-scale aperture; density and pressure plausibility is judged against its reconstructed images. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What does density and pressure say about temperature - justify your answer with a concrete production example.
**A:** The inner flow reaches billions of Kelvin; density and pressure emission intensity maps to temperature and magnetic field through emissivity relations. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does density and pressure guide the choice of simulation data - justify your answer with a concrete production example.
**A:** Disk state (SANE/MAD), electron distribution, and spin control morphology; density and pressure selection is part of the science, not just plumbing. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: Why do density and pressure models show the disk brighter on one side - justify your answer with a concrete production example.
**A:** Relativistic beaming amplifies emission from the approaching side; density and pressure visibility depends on the disk velocity and line of sight. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What observations constrain density and pressure - justify your answer with a concrete production example.
**A:** EHT images of M87* and Sgr A* measure ring diameter and asymmetry; density and pressure inversions use those to constrain the spacetime. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How does density and pressure explain the shadow - justify your answer with a concrete production example.
**A:** Captured photons leave a dark central region whose size and asymmetry depend on density and pressure - mass, spin, and viewing angle. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What does density and pressure predict about the photon ring - justify your answer with a concrete production example.
**A:** The bright ring radius is set by density and pressure quantities like the photon sphere and spin, making it a probe of the spacetime itself. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: Why is density and pressure central to interpreting black-hole images - justify your answer with a concrete production example.
**A:** Observables like the ring, shadow, and Doppler asymmetry trace directly to density and pressure, so understanding it lets you read images as physics. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: Why is density and pressure central to interpreting black-hole images - justify your answer with a concrete production example.
**A:** Observables like the ring, shadow, and Doppler asymmetry trace directly to density and pressure, so understanding it lets you read images as physics. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What does density and pressure predict about the photon ring - justify your answer with a concrete production example.
**A:** The bright ring radius is set by density and pressure quantities like the photon sphere and spin, making it a probe of the spacetime itself. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: How does density and pressure explain the shadow - justify your answer with a concrete production example.
**A:** Captured photons leave a dark central region whose size and asymmetry depend on density and pressure - mass, spin, and viewing angle. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What observations constrain density and pressure - justify your answer with a concrete production example.
**A:** EHT images of M87* and Sgr A* measure ring diameter and asymmetry; density and pressure inversions use those to constrain the spacetime. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: Why do density and pressure models show the disk brighter on one side - justify your answer with a concrete production example.
**A:** Relativistic beaming amplifies emission from the approaching side; density and pressure visibility depends on the disk velocity and line of sight. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: How does density and pressure guide the choice of simulation data - justify your answer with a concrete production example.
**A:** Disk state (SANE/MAD), electron distribution, and spin control morphology; density and pressure selection is part of the science, not just plumbing. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What does density and pressure say about temperature - justify your answer with a concrete production example.
**A:** The inner flow reaches billions of Kelvin; density and pressure emission intensity maps to temperature and magnetic field through emissivity relations. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How is density and pressure measured with EHT - justify your answer with a concrete production example.
**A:** Very long baseline interferometry synthesizes a horizon-scale aperture; density and pressure plausibility is judged against its reconstructed images. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What distinguishes density and pressure for supermassive vs stellar black holes - justify your answer with a concrete production example.
**A:** Scales shift by mass, but dimensionless quantities like the photon-ring radius are universal; density and pressure transfers across masses by scaling. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What role do jets play in density and pressure - justify your answer with a concrete production example.
**A:** Poynting-flux outflows can shine in their own right and shape the outermost emission; density and pressure includes them for completeness. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How does density and pressure treat the electron thermodynamics - justify your answer with a concrete production example.
**A:** Since GRMHD often does not track electron vs ion temperature, density and pressure uses proxies like R-beta prescriptions to convert fluid heating into emissivity. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What is the next frontier in density and pressure - justify your answer with a concrete production example.
**A:** Time-dependent images and movie predictions from turbulent simulations observed by upgraded EHT arrays; density and pressure is moving from stills to dynamics. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What is the next frontier in density and pressure - justify your answer with a concrete production example.
**A:** Time-dependent images and movie predictions from turbulent simulations observed by upgraded EHT arrays; density and pressure is moving from stills to dynamics. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does density and pressure treat the electron thermodynamics - justify your answer with a concrete production example.
**A:** Since GRMHD often does not track electron vs ion temperature, density and pressure uses proxies like R-beta prescriptions to convert fluid heating into emissivity. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What role do jets play in density and pressure - justify your answer with a concrete production example.
**A:** Poynting-flux outflows can shine in their own right and shape the outermost emission; density and pressure includes them for completeness. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: What distinguishes density and pressure for supermassive vs stellar black holes - justify your answer with a concrete production example.
**A:** Scales shift by mass, but dimensionless quantities like the photon-ring radius are universal; density and pressure transfers across masses by scaling. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How is density and pressure measured with EHT - justify your answer with a concrete production example.
**A:** Very long baseline interferometry synthesizes a horizon-scale aperture; density and pressure plausibility is judged against its reconstructed images. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What does density and pressure say about temperature - justify your answer with a concrete production example.
**A:** The inner flow reaches billions of Kelvin; density and pressure emission intensity maps to temperature and magnetic field through emissivity relations. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: How does density and pressure guide the choice of simulation data - justify your answer with a concrete production example.
**A:** Disk state (SANE/MAD), electron distribution, and spin control morphology; density and pressure selection is part of the science, not just plumbing. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: Why do density and pressure models show the disk brighter on one side - justify your answer with a concrete production example.
**A:** Relativistic beaming amplifies emission from the approaching side; density and pressure visibility depends on the disk velocity and line of sight. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What observations constrain density and pressure - justify your answer with a concrete production example.
**A:** EHT images of M87* and Sgr A* measure ring diameter and asymmetry; density and pressure inversions use those to constrain the spacetime. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does density and pressure explain the shadow - justify your answer with a concrete production example.
**A:** Captured photons leave a dark central region whose size and asymmetry depend on density and pressure - mass, spin, and viewing angle. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What does density and pressure predict about the photon ring - justify your answer with a concrete production example.
**A:** The bright ring radius is set by density and pressure quantities like the photon sphere and spin, making it a probe of the spacetime itself. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: Why is density and pressure central to interpreting black-hole images - justify your answer with a concrete production example.
**A:** Observables like the ring, shadow, and Doppler asymmetry trace directly to density and pressure, so understanding it lets you read images as physics. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: Why is density and pressure central to interpreting black-hole images - justify your answer with a concrete production example.
**A:** Observables like the ring, shadow, and Doppler asymmetry trace directly to density and pressure, so understanding it lets you read images as physics. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What does density and pressure predict about the photon ring - justify your answer with a concrete production example.
**A:** The bright ring radius is set by density and pressure quantities like the photon sphere and spin, making it a probe of the spacetime itself. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: How does density and pressure explain the shadow - justify your answer with a concrete production example.
**A:** Captured photons leave a dark central region whose size and asymmetry depend on density and pressure - mass, spin, and viewing angle. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: What observations constrain density and pressure - justify your answer with a concrete production example.
**A:** EHT images of M87* and Sgr A* measure ring diameter and asymmetry; density and pressure inversions use those to constrain the spacetime. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: Why do density and pressure models show the disk brighter on one side - justify your answer with a concrete production example.
**A:** Relativistic beaming amplifies emission from the approaching side; density and pressure visibility depends on the disk velocity and line of sight. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: How does density and pressure guide the choice of simulation data - justify your answer with a concrete production example.
**A:** Disk state (SANE/MAD), electron distribution, and spin control morphology; density and pressure selection is part of the science, not just plumbing. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What does density and pressure say about temperature - justify your answer with a concrete production example.
**A:** The inner flow reaches billions of Kelvin; density and pressure emission intensity maps to temperature and magnetic field through emissivity relations. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: How is density and pressure measured with EHT - justify your answer with a concrete production example.
**A:** Very long baseline interferometry synthesizes a horizon-scale aperture; density and pressure plausibility is judged against its reconstructed images. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What distinguishes density and pressure for supermassive vs stellar black holes - justify your answer with a concrete production example.
**A:** Scales shift by mass, but dimensionless quantities like the photon-ring radius are universal; density and pressure transfers across masses by scaling. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What role do jets play in density and pressure - justify your answer with a concrete production example.
**A:** Poynting-flux outflows can shine in their own right and shape the outermost emission; density and pressure includes them for completeness. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does density and pressure treat the electron thermodynamics - justify your answer with a concrete production example.
**A:** Since GRMHD often does not track electron vs ion temperature, density and pressure uses proxies like R-beta prescriptions to convert fluid heating into emissivity. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What is the next frontier in density and pressure - justify your answer with a concrete production example.
**A:** Time-dependent images and movie predictions from turbulent simulations observed by upgraded EHT arrays; density and pressure is moving from stills to dynamics. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: What is the next frontier in density and pressure - justify your answer with a concrete production example.
**A:** Time-dependent images and movie predictions from turbulent simulations observed by upgraded EHT arrays; density and pressure is moving from stills to dynamics. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: How does density and pressure treat the electron thermodynamics - justify your answer with a concrete production example.
**A:** Since GRMHD often does not track electron vs ion temperature, density and pressure uses proxies like R-beta prescriptions to convert fluid heating into emissivity. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What role do jets play in density and pressure - justify your answer with a concrete production example.
**A:** Poynting-flux outflows can shine in their own right and shape the outermost emission; density and pressure includes them for completeness. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What distinguishes density and pressure for supermassive vs stellar black holes - justify your answer with a concrete production example.
**A:** Scales shift by mass, but dimensionless quantities like the photon-ring radius are universal; density and pressure transfers across masses by scaling. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How is density and pressure measured with EHT - justify your answer with a concrete production example.
**A:** Very long baseline interferometry synthesizes a horizon-scale aperture; density and pressure plausibility is judged against its reconstructed images. A concrete example: consistently applying density and pressure in code review and regression tests keeps the whole pipeline trustworthy.
