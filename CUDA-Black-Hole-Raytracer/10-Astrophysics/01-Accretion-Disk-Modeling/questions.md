# Astrophysics — Accretion Disk Modeling Interview Questions and Answers

## Q1: What is an accretion disk?
**A:** A rotating disk of gas spiraling toward the black hole, heated and radiating as centrifugal support is lost to turbulence - the image's light source.

## Q2: What governs the disk structure?
**A:** Conservation of mass/angular momentum (transport via turbulence/stress), energy balance (cooling), and the vertical hydrostatic equilibrium - the disk equations.

## Q3: What is the thin-disk (Novikov-Thorne) model?
**A:** The analytic steady-state approximation: geometrically thin, optically thick disk with inner edge at ISCO and blackbody-like emission - the classic baseline.

## Q4: What sets the disk's temperature profile?
**A:** Dissipation rate ~ Mdot^0.5 r^-3/4-ish scaling (thin-disk T(r) = T_star (r/rin)^{-3/4}); the emission then follows a multi-temperature blackbody.

## Q5: What is the role of the MRI in the disk?
**A:** The magnetorotational instability drives the turbulence that transports angular momentum - the physical 'alpha-viscosity' source in real disks.

## Q6: How does GRMHD improve on the thin disk?
**A:** It computes the actual stress tensor, evolution, and plunging region - correcting the ISCO-edge and adding magnetic fields the thin model lacks.

## Q7: What is the disk's vertical structure?
**A:** Height H(r) from pressure balance; hot thick flows (H/r ~ 0.3-1) show in images differently than cold thin (H/r ~ 0.01) - a big visual and physics lever.

## Q8: How does disk density fall with radius?
**A:** Peaks near the inner region and decays outward (roughly a power law with the turbulence profile); the profile sets the emissivity radial distribution.

## Q9: What does the disk's spin interaction do?
**A:** Prograde spins truncate disks closer (ISCO drops) and heat the inner edge; retrograde widen and cool - spin controls the ring-gap geometry.

## Q10: What is the 'plunging region'?
**A:** Inside ISCO, the gas in-spirals without stable orbits - barely radiating but magnetically stressed; its emission is a distinct thin feature near the ring.

## Q11: How is the disk's density scaled for rendering?
**A:** Absolute density n_e is set by the accretion rate normalization - the image brightness that a telescope measures depends on using physical Mdot.

## Q12: What is the disk's temperature estimate for a real source?
**A:** T ~ 1e7-1e8 K in the inner region of a bright AGN disk; the M87-ish hot flow sits nearer electron temperatures 1e10-1e11 K - orders matter for emissivity.

## Q13: How do you choose the disk model for a render?
**A:** Thin-disk analytic for speed and starfield images; GRMHD snapshot for realism (the M87-class ring) - the model switch is a CLI flag, not a code branch.

## Q14: What is the summary?
**A:** Accretion-disk modeling ties the turbulence-transport physics to the emission field - the thin-disk or GRMHD choice sets every ring observable you render.

## Q15: Why is accretion disk modeling central to interpreting black-hole images?
**A:** Observables like the ring, shadow, and Doppler asymmetry trace directly to accretion disk modeling, so understanding it lets you read images as physics.

## Q16: What does accretion disk modeling predict about the photon ring?
**A:** The bright ring radius is set by accretion disk modeling quantities like the photon sphere and spin, making it a probe of the spacetime itself.

## Q17: How does accretion disk modeling explain the shadow?
**A:** Captured photons leave a dark central region whose size and asymmetry depend on accretion disk modeling - mass, spin, and viewing angle.

## Q18: What observations constrain accretion disk modeling?
**A:** EHT images of M87* and Sgr A* measure ring diameter and asymmetry; accretion disk modeling inversions use those to constrain the spacetime.

## Q19: Why do accretion disk modeling models show the disk brighter on one side?
**A:** Relativistic beaming amplifies emission from the approaching side; accretion disk modeling visibility depends on the disk velocity and line of sight.

## Q20: How does accretion disk modeling guide the choice of simulation data?
**A:** Disk state (SANE/MAD), electron distribution, and spin control morphology; accretion disk modeling selection is part of the science, not just plumbing.

## Q21: What does accretion disk modeling say about temperature?
**A:** The inner flow reaches billions of Kelvin; accretion disk modeling emission intensity maps to temperature and magnetic field through emissivity relations.

## Q22: How is accretion disk modeling measured with EHT?
**A:** Very long baseline interferometry synthesizes a horizon-scale aperture; accretion disk modeling plausibility is judged against its reconstructed images.

## Q23: What distinguishes accretion disk modeling for supermassive vs stellar black holes?
**A:** Scales shift by mass, but dimensionless quantities like the photon-ring radius are universal; accretion disk modeling transfers across masses by scaling.

## Q24: What role do jets play in accretion disk modeling?
**A:** Poynting-flux outflows can shine in their own right and shape the outermost emission; accretion disk modeling includes them for completeness.

## Q25: How does accretion disk modeling treat the electron thermodynamics?
**A:** Since GRMHD often does not track electron vs ion temperature, accretion disk modeling uses proxies like R-beta prescriptions to convert fluid heating into emissivity.

## Q26: What is the next frontier in accretion disk modeling?
**A:** Time-dependent images and movie predictions from turbulent simulations observed by upgraded EHT arrays; accretion disk modeling is moving from stills to dynamics.

## Q27: What is the next frontier in accretion disk modeling - justify your answer with a concrete production example.
**A:** Time-dependent images and movie predictions from turbulent simulations observed by upgraded EHT arrays; accretion disk modeling is moving from stills to dynamics. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q28: How does accretion disk modeling treat the electron thermodynamics - justify your answer with a concrete production example.
**A:** Since GRMHD often does not track electron vs ion temperature, accretion disk modeling uses proxies like R-beta prescriptions to convert fluid heating into emissivity. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q29: What role do jets play in accretion disk modeling - justify your answer with a concrete production example.
**A:** Poynting-flux outflows can shine in their own right and shape the outermost emission; accretion disk modeling includes them for completeness. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q30: What distinguishes accretion disk modeling for supermassive vs stellar black holes - justify your answer with a concrete production example.
**A:** Scales shift by mass, but dimensionless quantities like the photon-ring radius are universal; accretion disk modeling transfers across masses by scaling. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q31: How is accretion disk modeling measured with EHT - justify your answer with a concrete production example.
**A:** Very long baseline interferometry synthesizes a horizon-scale aperture; accretion disk modeling plausibility is judged against its reconstructed images. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q32: What does accretion disk modeling say about temperature - justify your answer with a concrete production example.
**A:** The inner flow reaches billions of Kelvin; accretion disk modeling emission intensity maps to temperature and magnetic field through emissivity relations. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q33: How does accretion disk modeling guide the choice of simulation data - justify your answer with a concrete production example.
**A:** Disk state (SANE/MAD), electron distribution, and spin control morphology; accretion disk modeling selection is part of the science, not just plumbing. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q34: Why do accretion disk modeling models show the disk brighter on one side - justify your answer with a concrete production example.
**A:** Relativistic beaming amplifies emission from the approaching side; accretion disk modeling visibility depends on the disk velocity and line of sight. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q35: What observations constrain accretion disk modeling - justify your answer with a concrete production example.
**A:** EHT images of M87* and Sgr A* measure ring diameter and asymmetry; accretion disk modeling inversions use those to constrain the spacetime. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q36: How does accretion disk modeling explain the shadow - justify your answer with a concrete production example.
**A:** Captured photons leave a dark central region whose size and asymmetry depend on accretion disk modeling - mass, spin, and viewing angle. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q37: What does accretion disk modeling predict about the photon ring - justify your answer with a concrete production example.
**A:** The bright ring radius is set by accretion disk modeling quantities like the photon sphere and spin, making it a probe of the spacetime itself. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q38: Why is accretion disk modeling central to interpreting black-hole images - justify your answer with a concrete production example.
**A:** Observables like the ring, shadow, and Doppler asymmetry trace directly to accretion disk modeling, so understanding it lets you read images as physics. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q39: Why is accretion disk modeling central to interpreting black-hole images - justify your answer with a concrete production example.
**A:** Observables like the ring, shadow, and Doppler asymmetry trace directly to accretion disk modeling, so understanding it lets you read images as physics. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q40: What does accretion disk modeling predict about the photon ring - justify your answer with a concrete production example.
**A:** The bright ring radius is set by accretion disk modeling quantities like the photon sphere and spin, making it a probe of the spacetime itself. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: How does accretion disk modeling explain the shadow - justify your answer with a concrete production example.
**A:** Captured photons leave a dark central region whose size and asymmetry depend on accretion disk modeling - mass, spin, and viewing angle. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What observations constrain accretion disk modeling - justify your answer with a concrete production example.
**A:** EHT images of M87* and Sgr A* measure ring diameter and asymmetry; accretion disk modeling inversions use those to constrain the spacetime. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: Why do accretion disk modeling models show the disk brighter on one side - justify your answer with a concrete production example.
**A:** Relativistic beaming amplifies emission from the approaching side; accretion disk modeling visibility depends on the disk velocity and line of sight. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How does accretion disk modeling guide the choice of simulation data - justify your answer with a concrete production example.
**A:** Disk state (SANE/MAD), electron distribution, and spin control morphology; accretion disk modeling selection is part of the science, not just plumbing. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What does accretion disk modeling say about temperature - justify your answer with a concrete production example.
**A:** The inner flow reaches billions of Kelvin; accretion disk modeling emission intensity maps to temperature and magnetic field through emissivity relations. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How is accretion disk modeling measured with EHT - justify your answer with a concrete production example.
**A:** Very long baseline interferometry synthesizes a horizon-scale aperture; accretion disk modeling plausibility is judged against its reconstructed images. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What distinguishes accretion disk modeling for supermassive vs stellar black holes - justify your answer with a concrete production example.
**A:** Scales shift by mass, but dimensionless quantities like the photon-ring radius are universal; accretion disk modeling transfers across masses by scaling. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: What role do jets play in accretion disk modeling - justify your answer with a concrete production example.
**A:** Poynting-flux outflows can shine in their own right and shape the outermost emission; accretion disk modeling includes them for completeness. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: How does accretion disk modeling treat the electron thermodynamics - justify your answer with a concrete production example.
**A:** Since GRMHD often does not track electron vs ion temperature, accretion disk modeling uses proxies like R-beta prescriptions to convert fluid heating into emissivity. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What is the next frontier in accretion disk modeling - justify your answer with a concrete production example.
**A:** Time-dependent images and movie predictions from turbulent simulations observed by upgraded EHT arrays; accretion disk modeling is moving from stills to dynamics. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What is the next frontier in accretion disk modeling - justify your answer with a concrete production example.
**A:** Time-dependent images and movie predictions from turbulent simulations observed by upgraded EHT arrays; accretion disk modeling is moving from stills to dynamics. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How does accretion disk modeling treat the electron thermodynamics - justify your answer with a concrete production example.
**A:** Since GRMHD often does not track electron vs ion temperature, accretion disk modeling uses proxies like R-beta prescriptions to convert fluid heating into emissivity. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What role do jets play in accretion disk modeling - justify your answer with a concrete production example.
**A:** Poynting-flux outflows can shine in their own right and shape the outermost emission; accretion disk modeling includes them for completeness. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: What distinguishes accretion disk modeling for supermassive vs stellar black holes - justify your answer with a concrete production example.
**A:** Scales shift by mass, but dimensionless quantities like the photon-ring radius are universal; accretion disk modeling transfers across masses by scaling. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: How is accretion disk modeling measured with EHT - justify your answer with a concrete production example.
**A:** Very long baseline interferometry synthesizes a horizon-scale aperture; accretion disk modeling plausibility is judged against its reconstructed images. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What does accretion disk modeling say about temperature - justify your answer with a concrete production example.
**A:** The inner flow reaches billions of Kelvin; accretion disk modeling emission intensity maps to temperature and magnetic field through emissivity relations. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How does accretion disk modeling guide the choice of simulation data - justify your answer with a concrete production example.
**A:** Disk state (SANE/MAD), electron distribution, and spin control morphology; accretion disk modeling selection is part of the science, not just plumbing. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: Why do accretion disk modeling models show the disk brighter on one side - justify your answer with a concrete production example.
**A:** Relativistic beaming amplifies emission from the approaching side; accretion disk modeling visibility depends on the disk velocity and line of sight. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: What observations constrain accretion disk modeling - justify your answer with a concrete production example.
**A:** EHT images of M87* and Sgr A* measure ring diameter and asymmetry; accretion disk modeling inversions use those to constrain the spacetime. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: How does accretion disk modeling explain the shadow - justify your answer with a concrete production example.
**A:** Captured photons leave a dark central region whose size and asymmetry depend on accretion disk modeling - mass, spin, and viewing angle. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What does accretion disk modeling predict about the photon ring - justify your answer with a concrete production example.
**A:** The bright ring radius is set by accretion disk modeling quantities like the photon sphere and spin, making it a probe of the spacetime itself. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why is accretion disk modeling central to interpreting black-hole images - justify your answer with a concrete production example.
**A:** Observables like the ring, shadow, and Doppler asymmetry trace directly to accretion disk modeling, so understanding it lets you read images as physics. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: Why is accretion disk modeling central to interpreting black-hole images - justify your answer with a concrete production example.
**A:** Observables like the ring, shadow, and Doppler asymmetry trace directly to accretion disk modeling, so understanding it lets you read images as physics. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What does accretion disk modeling predict about the photon ring - justify your answer with a concrete production example.
**A:** The bright ring radius is set by accretion disk modeling quantities like the photon sphere and spin, making it a probe of the spacetime itself. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: How does accretion disk modeling explain the shadow - justify your answer with a concrete production example.
**A:** Captured photons leave a dark central region whose size and asymmetry depend on accretion disk modeling - mass, spin, and viewing angle. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What observations constrain accretion disk modeling - justify your answer with a concrete production example.
**A:** EHT images of M87* and Sgr A* measure ring diameter and asymmetry; accretion disk modeling inversions use those to constrain the spacetime. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: Why do accretion disk modeling models show the disk brighter on one side - justify your answer with a concrete production example.
**A:** Relativistic beaming amplifies emission from the approaching side; accretion disk modeling visibility depends on the disk velocity and line of sight. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How does accretion disk modeling guide the choice of simulation data - justify your answer with a concrete production example.
**A:** Disk state (SANE/MAD), electron distribution, and spin control morphology; accretion disk modeling selection is part of the science, not just plumbing. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What does accretion disk modeling say about temperature - justify your answer with a concrete production example.
**A:** The inner flow reaches billions of Kelvin; accretion disk modeling emission intensity maps to temperature and magnetic field through emissivity relations. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How is accretion disk modeling measured with EHT - justify your answer with a concrete production example.
**A:** Very long baseline interferometry synthesizes a horizon-scale aperture; accretion disk modeling plausibility is judged against its reconstructed images. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What distinguishes accretion disk modeling for supermassive vs stellar black holes - justify your answer with a concrete production example.
**A:** Scales shift by mass, but dimensionless quantities like the photon-ring radius are universal; accretion disk modeling transfers across masses by scaling. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What role do jets play in accretion disk modeling - justify your answer with a concrete production example.
**A:** Poynting-flux outflows can shine in their own right and shape the outermost emission; accretion disk modeling includes them for completeness. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does accretion disk modeling treat the electron thermodynamics - justify your answer with a concrete production example.
**A:** Since GRMHD often does not track electron vs ion temperature, accretion disk modeling uses proxies like R-beta prescriptions to convert fluid heating into emissivity. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What is the next frontier in accretion disk modeling - justify your answer with a concrete production example.
**A:** Time-dependent images and movie predictions from turbulent simulations observed by upgraded EHT arrays; accretion disk modeling is moving from stills to dynamics. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: What is the next frontier in accretion disk modeling - justify your answer with a concrete production example.
**A:** Time-dependent images and movie predictions from turbulent simulations observed by upgraded EHT arrays; accretion disk modeling is moving from stills to dynamics. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How does accretion disk modeling treat the electron thermodynamics - justify your answer with a concrete production example.
**A:** Since GRMHD often does not track electron vs ion temperature, accretion disk modeling uses proxies like R-beta prescriptions to convert fluid heating into emissivity. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What role do jets play in accretion disk modeling - justify your answer with a concrete production example.
**A:** Poynting-flux outflows can shine in their own right and shape the outermost emission; accretion disk modeling includes them for completeness. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What distinguishes accretion disk modeling for supermassive vs stellar black holes - justify your answer with a concrete production example.
**A:** Scales shift by mass, but dimensionless quantities like the photon-ring radius are universal; accretion disk modeling transfers across masses by scaling. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How is accretion disk modeling measured with EHT - justify your answer with a concrete production example.
**A:** Very long baseline interferometry synthesizes a horizon-scale aperture; accretion disk modeling plausibility is judged against its reconstructed images. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What does accretion disk modeling say about temperature - justify your answer with a concrete production example.
**A:** The inner flow reaches billions of Kelvin; accretion disk modeling emission intensity maps to temperature and magnetic field through emissivity relations. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does accretion disk modeling guide the choice of simulation data - justify your answer with a concrete production example.
**A:** Disk state (SANE/MAD), electron distribution, and spin control morphology; accretion disk modeling selection is part of the science, not just plumbing. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: Why do accretion disk modeling models show the disk brighter on one side - justify your answer with a concrete production example.
**A:** Relativistic beaming amplifies emission from the approaching side; accretion disk modeling visibility depends on the disk velocity and line of sight. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What observations constrain accretion disk modeling - justify your answer with a concrete production example.
**A:** EHT images of M87* and Sgr A* measure ring diameter and asymmetry; accretion disk modeling inversions use those to constrain the spacetime. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: How does accretion disk modeling explain the shadow - justify your answer with a concrete production example.
**A:** Captured photons leave a dark central region whose size and asymmetry depend on accretion disk modeling - mass, spin, and viewing angle. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What does accretion disk modeling predict about the photon ring - justify your answer with a concrete production example.
**A:** The bright ring radius is set by accretion disk modeling quantities like the photon sphere and spin, making it a probe of the spacetime itself. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: Why is accretion disk modeling central to interpreting black-hole images - justify your answer with a concrete production example.
**A:** Observables like the ring, shadow, and Doppler asymmetry trace directly to accretion disk modeling, so understanding it lets you read images as physics. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: Why is accretion disk modeling central to interpreting black-hole images - justify your answer with a concrete production example.
**A:** Observables like the ring, shadow, and Doppler asymmetry trace directly to accretion disk modeling, so understanding it lets you read images as physics. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: What does accretion disk modeling predict about the photon ring - justify your answer with a concrete production example.
**A:** The bright ring radius is set by accretion disk modeling quantities like the photon sphere and spin, making it a probe of the spacetime itself. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: How does accretion disk modeling explain the shadow - justify your answer with a concrete production example.
**A:** Captured photons leave a dark central region whose size and asymmetry depend on accretion disk modeling - mass, spin, and viewing angle. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What observations constrain accretion disk modeling - justify your answer with a concrete production example.
**A:** EHT images of M87* and Sgr A* measure ring diameter and asymmetry; accretion disk modeling inversions use those to constrain the spacetime. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: Why do accretion disk modeling models show the disk brighter on one side - justify your answer with a concrete production example.
**A:** Relativistic beaming amplifies emission from the approaching side; accretion disk modeling visibility depends on the disk velocity and line of sight. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How does accretion disk modeling guide the choice of simulation data - justify your answer with a concrete production example.
**A:** Disk state (SANE/MAD), electron distribution, and spin control morphology; accretion disk modeling selection is part of the science, not just plumbing. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What does accretion disk modeling say about temperature - justify your answer with a concrete production example.
**A:** The inner flow reaches billions of Kelvin; accretion disk modeling emission intensity maps to temperature and magnetic field through emissivity relations. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How is accretion disk modeling measured with EHT - justify your answer with a concrete production example.
**A:** Very long baseline interferometry synthesizes a horizon-scale aperture; accretion disk modeling plausibility is judged against its reconstructed images. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What distinguishes accretion disk modeling for supermassive vs stellar black holes - justify your answer with a concrete production example.
**A:** Scales shift by mass, but dimensionless quantities like the photon-ring radius are universal; accretion disk modeling transfers across masses by scaling. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: What role do jets play in accretion disk modeling - justify your answer with a concrete production example.
**A:** Poynting-flux outflows can shine in their own right and shape the outermost emission; accretion disk modeling includes them for completeness. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: How does accretion disk modeling treat the electron thermodynamics - justify your answer with a concrete production example.
**A:** Since GRMHD often does not track electron vs ion temperature, accretion disk modeling uses proxies like R-beta prescriptions to convert fluid heating into emissivity. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What is the next frontier in accretion disk modeling - justify your answer with a concrete production example.
**A:** Time-dependent images and movie predictions from turbulent simulations observed by upgraded EHT arrays; accretion disk modeling is moving from stills to dynamics. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What is the next frontier in accretion disk modeling - justify your answer with a concrete production example.
**A:** Time-dependent images and movie predictions from turbulent simulations observed by upgraded EHT arrays; accretion disk modeling is moving from stills to dynamics. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How does accretion disk modeling treat the electron thermodynamics - justify your answer with a concrete production example.
**A:** Since GRMHD often does not track electron vs ion temperature, accretion disk modeling uses proxies like R-beta prescriptions to convert fluid heating into emissivity. A concrete example: consistently applying accretion disk modeling in code review and regression tests keeps the whole pipeline trustworthy.
