# Astrophysics — Horizon Scale Imaging Interview Questions and Answers

## Q1: What is horizon-scale imaging?
**A:** Observing/imaging the region within ~10 r_g of the horizon - the regime where strong-field GR effects (shadow, photon ring, beaming) dominate the picture.

## Q2: What resolution is required?
**A:** Angles ~ a few times M/D; for M87* that's ~10-40 microarcsec - beyond a single telescope, hence VLBI networks (EHT).

## Q3: What telescopes form the EHT?
**A:** Millimeter (1.3mm) telescopes on 6+ continents (ALMA, NOEMA, SMT, etc.) acting as one Earth-sized interferometer - the aggregate aperture.

## Q4: What is the array's limiting function (uv coverage)?
**A:** The finite baselines truncate Fourier coverage -> a point-spread beam ~25-50 microarcsec; images are therefore blurred reconstructions, not raw snapshots.

## Q5: Why chose 230 GHz (1.3mm)?
**A:** At this band the inner disk is optically thin (sees the photon ring) while atmospheric opacity is still manageable - the sweet spot of the field.

## Q6: What are the key VLBI challenges?
**A:** Phase calibration, weather, array sensitivity, and scattering (Sgr A*) - the observing side of imaging; the theory side is your raytracer.

## Q7: How does theory aid reconstruction?
**A:** Forward-modeling: a GRMHD+raytracer ensemble predicts images; the EHT's reconstruction uses them as priors/constraints (the 'imaging' hands the PRIOR power).

## Q8: What is the 'image-domain' comparison?
**A:** Blur the rendered frame to the array's beam and compare pixel-residuals with the observed image - the quantitative scientific face-off.

## Q9: What is the shadow's observational status?
**A:** The dark region's angular size matches the Kerr prediction for both M87* and Sgr A* - the most direct evidence for an event horizon to date.

## Q10: What are the next-generation upgrades?
**A:** ngEHT adds telescopes/bands for better uv coverage and movies - more frames, sharper rings, and ultimately the photon-ring peak measured directly.

## Q11: What is the summary?
**A:** Horizon-scale imaging is the observational arena of this project: VLBI-blurred renders compared to EHT images, with the photon ring and shadow as the theory-observation bridge.

## Q12: Why is horizon scale imaging central to interpreting black-hole images?
**A:** Observables like the ring, shadow, and Doppler asymmetry trace directly to horizon scale imaging, so understanding it lets you read images as physics.

## Q13: What does horizon scale imaging predict about the photon ring?
**A:** The bright ring radius is set by horizon scale imaging quantities like the photon sphere and spin, making it a probe of the spacetime itself.

## Q14: How does horizon scale imaging explain the shadow?
**A:** Captured photons leave a dark central region whose size and asymmetry depend on horizon scale imaging - mass, spin, and viewing angle.

## Q15: What observations constrain horizon scale imaging?
**A:** EHT images of M87* and Sgr A* measure ring diameter and asymmetry; horizon scale imaging inversions use those to constrain the spacetime.

## Q16: Why do horizon scale imaging models show the disk brighter on one side?
**A:** Relativistic beaming amplifies emission from the approaching side; horizon scale imaging visibility depends on the disk velocity and line of sight.

## Q17: How does horizon scale imaging guide the choice of simulation data?
**A:** Disk state (SANE/MAD), electron distribution, and spin control morphology; horizon scale imaging selection is part of the science, not just plumbing.

## Q18: What does horizon scale imaging say about temperature?
**A:** The inner flow reaches billions of Kelvin; horizon scale imaging emission intensity maps to temperature and magnetic field through emissivity relations.

## Q19: How is horizon scale imaging measured with EHT?
**A:** Very long baseline interferometry synthesizes a horizon-scale aperture; horizon scale imaging plausibility is judged against its reconstructed images.

## Q20: What distinguishes horizon scale imaging for supermassive vs stellar black holes?
**A:** Scales shift by mass, but dimensionless quantities like the photon-ring radius are universal; horizon scale imaging transfers across masses by scaling.

## Q21: What role do jets play in horizon scale imaging?
**A:** Poynting-flux outflows can shine in their own right and shape the outermost emission; horizon scale imaging includes them for completeness.

## Q22: How does horizon scale imaging treat the electron thermodynamics?
**A:** Since GRMHD often does not track electron vs ion temperature, horizon scale imaging uses proxies like R-beta prescriptions to convert fluid heating into emissivity.

## Q23: What is the next frontier in horizon scale imaging?
**A:** Time-dependent images and movie predictions from turbulent simulations observed by upgraded EHT arrays; horizon scale imaging is moving from stills to dynamics.

## Q24: What is the next frontier in horizon scale imaging - justify your answer with a concrete production example.
**A:** Time-dependent images and movie predictions from turbulent simulations observed by upgraded EHT arrays; horizon scale imaging is moving from stills to dynamics. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q25: How does horizon scale imaging treat the electron thermodynamics - justify your answer with a concrete production example.
**A:** Since GRMHD often does not track electron vs ion temperature, horizon scale imaging uses proxies like R-beta prescriptions to convert fluid heating into emissivity. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q26: What role do jets play in horizon scale imaging - justify your answer with a concrete production example.
**A:** Poynting-flux outflows can shine in their own right and shape the outermost emission; horizon scale imaging includes them for completeness. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q27: What distinguishes horizon scale imaging for supermassive vs stellar black holes - justify your answer with a concrete production example.
**A:** Scales shift by mass, but dimensionless quantities like the photon-ring radius are universal; horizon scale imaging transfers across masses by scaling. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q28: How is horizon scale imaging measured with EHT - justify your answer with a concrete production example.
**A:** Very long baseline interferometry synthesizes a horizon-scale aperture; horizon scale imaging plausibility is judged against its reconstructed images. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q29: What does horizon scale imaging say about temperature - justify your answer with a concrete production example.
**A:** The inner flow reaches billions of Kelvin; horizon scale imaging emission intensity maps to temperature and magnetic field through emissivity relations. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q30: How does horizon scale imaging guide the choice of simulation data - justify your answer with a concrete production example.
**A:** Disk state (SANE/MAD), electron distribution, and spin control morphology; horizon scale imaging selection is part of the science, not just plumbing. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q31: Why do horizon scale imaging models show the disk brighter on one side - justify your answer with a concrete production example.
**A:** Relativistic beaming amplifies emission from the approaching side; horizon scale imaging visibility depends on the disk velocity and line of sight. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q32: What observations constrain horizon scale imaging - justify your answer with a concrete production example.
**A:** EHT images of M87* and Sgr A* measure ring diameter and asymmetry; horizon scale imaging inversions use those to constrain the spacetime. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q33: How does horizon scale imaging explain the shadow - justify your answer with a concrete production example.
**A:** Captured photons leave a dark central region whose size and asymmetry depend on horizon scale imaging - mass, spin, and viewing angle. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q34: What does horizon scale imaging predict about the photon ring - justify your answer with a concrete production example.
**A:** The bright ring radius is set by horizon scale imaging quantities like the photon sphere and spin, making it a probe of the spacetime itself. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q35: Why is horizon scale imaging central to interpreting black-hole images - justify your answer with a concrete production example.
**A:** Observables like the ring, shadow, and Doppler asymmetry trace directly to horizon scale imaging, so understanding it lets you read images as physics. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q36: Why is horizon scale imaging central to interpreting black-hole images - justify your answer with a concrete production example.
**A:** Observables like the ring, shadow, and Doppler asymmetry trace directly to horizon scale imaging, so understanding it lets you read images as physics. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q37: What does horizon scale imaging predict about the photon ring - justify your answer with a concrete production example.
**A:** The bright ring radius is set by horizon scale imaging quantities like the photon sphere and spin, making it a probe of the spacetime itself. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q38: How does horizon scale imaging explain the shadow - justify your answer with a concrete production example.
**A:** Captured photons leave a dark central region whose size and asymmetry depend on horizon scale imaging - mass, spin, and viewing angle. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q39: What observations constrain horizon scale imaging - justify your answer with a concrete production example.
**A:** EHT images of M87* and Sgr A* measure ring diameter and asymmetry; horizon scale imaging inversions use those to constrain the spacetime. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q40: Why do horizon scale imaging models show the disk brighter on one side - justify your answer with a concrete production example.
**A:** Relativistic beaming amplifies emission from the approaching side; horizon scale imaging visibility depends on the disk velocity and line of sight. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: How does horizon scale imaging guide the choice of simulation data - justify your answer with a concrete production example.
**A:** Disk state (SANE/MAD), electron distribution, and spin control morphology; horizon scale imaging selection is part of the science, not just plumbing. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What does horizon scale imaging say about temperature - justify your answer with a concrete production example.
**A:** The inner flow reaches billions of Kelvin; horizon scale imaging emission intensity maps to temperature and magnetic field through emissivity relations. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: How is horizon scale imaging measured with EHT - justify your answer with a concrete production example.
**A:** Very long baseline interferometry synthesizes a horizon-scale aperture; horizon scale imaging plausibility is judged against its reconstructed images. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What distinguishes horizon scale imaging for supermassive vs stellar black holes - justify your answer with a concrete production example.
**A:** Scales shift by mass, but dimensionless quantities like the photon-ring radius are universal; horizon scale imaging transfers across masses by scaling. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What role do jets play in horizon scale imaging - justify your answer with a concrete production example.
**A:** Poynting-flux outflows can shine in their own right and shape the outermost emission; horizon scale imaging includes them for completeness. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does horizon scale imaging treat the electron thermodynamics - justify your answer with a concrete production example.
**A:** Since GRMHD often does not track electron vs ion temperature, horizon scale imaging uses proxies like R-beta prescriptions to convert fluid heating into emissivity. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What is the next frontier in horizon scale imaging - justify your answer with a concrete production example.
**A:** Time-dependent images and movie predictions from turbulent simulations observed by upgraded EHT arrays; horizon scale imaging is moving from stills to dynamics. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: What is the next frontier in horizon scale imaging - justify your answer with a concrete production example.
**A:** Time-dependent images and movie predictions from turbulent simulations observed by upgraded EHT arrays; horizon scale imaging is moving from stills to dynamics. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: How does horizon scale imaging treat the electron thermodynamics - justify your answer with a concrete production example.
**A:** Since GRMHD often does not track electron vs ion temperature, horizon scale imaging uses proxies like R-beta prescriptions to convert fluid heating into emissivity. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What role do jets play in horizon scale imaging - justify your answer with a concrete production example.
**A:** Poynting-flux outflows can shine in their own right and shape the outermost emission; horizon scale imaging includes them for completeness. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What distinguishes horizon scale imaging for supermassive vs stellar black holes - justify your answer with a concrete production example.
**A:** Scales shift by mass, but dimensionless quantities like the photon-ring radius are universal; horizon scale imaging transfers across masses by scaling. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How is horizon scale imaging measured with EHT - justify your answer with a concrete production example.
**A:** Very long baseline interferometry synthesizes a horizon-scale aperture; horizon scale imaging plausibility is judged against its reconstructed images. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What does horizon scale imaging say about temperature - justify your answer with a concrete production example.
**A:** The inner flow reaches billions of Kelvin; horizon scale imaging emission intensity maps to temperature and magnetic field through emissivity relations. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does horizon scale imaging guide the choice of simulation data - justify your answer with a concrete production example.
**A:** Disk state (SANE/MAD), electron distribution, and spin control morphology; horizon scale imaging selection is part of the science, not just plumbing. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: Why do horizon scale imaging models show the disk brighter on one side - justify your answer with a concrete production example.
**A:** Relativistic beaming amplifies emission from the approaching side; horizon scale imaging visibility depends on the disk velocity and line of sight. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What observations constrain horizon scale imaging - justify your answer with a concrete production example.
**A:** EHT images of M87* and Sgr A* measure ring diameter and asymmetry; horizon scale imaging inversions use those to constrain the spacetime. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How does horizon scale imaging explain the shadow - justify your answer with a concrete production example.
**A:** Captured photons leave a dark central region whose size and asymmetry depend on horizon scale imaging - mass, spin, and viewing angle. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What does horizon scale imaging predict about the photon ring - justify your answer with a concrete production example.
**A:** The bright ring radius is set by horizon scale imaging quantities like the photon sphere and spin, making it a probe of the spacetime itself. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: Why is horizon scale imaging central to interpreting black-hole images - justify your answer with a concrete production example.
**A:** Observables like the ring, shadow, and Doppler asymmetry trace directly to horizon scale imaging, so understanding it lets you read images as physics. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: Why is horizon scale imaging central to interpreting black-hole images - justify your answer with a concrete production example.
**A:** Observables like the ring, shadow, and Doppler asymmetry trace directly to horizon scale imaging, so understanding it lets you read images as physics. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What does horizon scale imaging predict about the photon ring - justify your answer with a concrete production example.
**A:** The bright ring radius is set by horizon scale imaging quantities like the photon sphere and spin, making it a probe of the spacetime itself. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: How does horizon scale imaging explain the shadow - justify your answer with a concrete production example.
**A:** Captured photons leave a dark central region whose size and asymmetry depend on horizon scale imaging - mass, spin, and viewing angle. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What observations constrain horizon scale imaging - justify your answer with a concrete production example.
**A:** EHT images of M87* and Sgr A* measure ring diameter and asymmetry; horizon scale imaging inversions use those to constrain the spacetime. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: Why do horizon scale imaging models show the disk brighter on one side - justify your answer with a concrete production example.
**A:** Relativistic beaming amplifies emission from the approaching side; horizon scale imaging visibility depends on the disk velocity and line of sight. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: How does horizon scale imaging guide the choice of simulation data - justify your answer with a concrete production example.
**A:** Disk state (SANE/MAD), electron distribution, and spin control morphology; horizon scale imaging selection is part of the science, not just plumbing. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What does horizon scale imaging say about temperature - justify your answer with a concrete production example.
**A:** The inner flow reaches billions of Kelvin; horizon scale imaging emission intensity maps to temperature and magnetic field through emissivity relations. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How is horizon scale imaging measured with EHT - justify your answer with a concrete production example.
**A:** Very long baseline interferometry synthesizes a horizon-scale aperture; horizon scale imaging plausibility is judged against its reconstructed images. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What distinguishes horizon scale imaging for supermassive vs stellar black holes - justify your answer with a concrete production example.
**A:** Scales shift by mass, but dimensionless quantities like the photon-ring radius are universal; horizon scale imaging transfers across masses by scaling. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What role do jets play in horizon scale imaging - justify your answer with a concrete production example.
**A:** Poynting-flux outflows can shine in their own right and shape the outermost emission; horizon scale imaging includes them for completeness. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How does horizon scale imaging treat the electron thermodynamics - justify your answer with a concrete production example.
**A:** Since GRMHD often does not track electron vs ion temperature, horizon scale imaging uses proxies like R-beta prescriptions to convert fluid heating into emissivity. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What is the next frontier in horizon scale imaging - justify your answer with a concrete production example.
**A:** Time-dependent images and movie predictions from turbulent simulations observed by upgraded EHT arrays; horizon scale imaging is moving from stills to dynamics. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What is the next frontier in horizon scale imaging - justify your answer with a concrete production example.
**A:** Time-dependent images and movie predictions from turbulent simulations observed by upgraded EHT arrays; horizon scale imaging is moving from stills to dynamics. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does horizon scale imaging treat the electron thermodynamics - justify your answer with a concrete production example.
**A:** Since GRMHD often does not track electron vs ion temperature, horizon scale imaging uses proxies like R-beta prescriptions to convert fluid heating into emissivity. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What role do jets play in horizon scale imaging - justify your answer with a concrete production example.
**A:** Poynting-flux outflows can shine in their own right and shape the outermost emission; horizon scale imaging includes them for completeness. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: What distinguishes horizon scale imaging for supermassive vs stellar black holes - justify your answer with a concrete production example.
**A:** Scales shift by mass, but dimensionless quantities like the photon-ring radius are universal; horizon scale imaging transfers across masses by scaling. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How is horizon scale imaging measured with EHT - justify your answer with a concrete production example.
**A:** Very long baseline interferometry synthesizes a horizon-scale aperture; horizon scale imaging plausibility is judged against its reconstructed images. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What does horizon scale imaging say about temperature - justify your answer with a concrete production example.
**A:** The inner flow reaches billions of Kelvin; horizon scale imaging emission intensity maps to temperature and magnetic field through emissivity relations. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: How does horizon scale imaging guide the choice of simulation data - justify your answer with a concrete production example.
**A:** Disk state (SANE/MAD), electron distribution, and spin control morphology; horizon scale imaging selection is part of the science, not just plumbing. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: Why do horizon scale imaging models show the disk brighter on one side - justify your answer with a concrete production example.
**A:** Relativistic beaming amplifies emission from the approaching side; horizon scale imaging visibility depends on the disk velocity and line of sight. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What observations constrain horizon scale imaging - justify your answer with a concrete production example.
**A:** EHT images of M87* and Sgr A* measure ring diameter and asymmetry; horizon scale imaging inversions use those to constrain the spacetime. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does horizon scale imaging explain the shadow - justify your answer with a concrete production example.
**A:** Captured photons leave a dark central region whose size and asymmetry depend on horizon scale imaging - mass, spin, and viewing angle. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What does horizon scale imaging predict about the photon ring - justify your answer with a concrete production example.
**A:** The bright ring radius is set by horizon scale imaging quantities like the photon sphere and spin, making it a probe of the spacetime itself. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: Why is horizon scale imaging central to interpreting black-hole images - justify your answer with a concrete production example.
**A:** Observables like the ring, shadow, and Doppler asymmetry trace directly to horizon scale imaging, so understanding it lets you read images as physics. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: Why is horizon scale imaging central to interpreting black-hole images - justify your answer with a concrete production example.
**A:** Observables like the ring, shadow, and Doppler asymmetry trace directly to horizon scale imaging, so understanding it lets you read images as physics. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What does horizon scale imaging predict about the photon ring - justify your answer with a concrete production example.
**A:** The bright ring radius is set by horizon scale imaging quantities like the photon sphere and spin, making it a probe of the spacetime itself. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: How does horizon scale imaging explain the shadow - justify your answer with a concrete production example.
**A:** Captured photons leave a dark central region whose size and asymmetry depend on horizon scale imaging - mass, spin, and viewing angle. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: What observations constrain horizon scale imaging - justify your answer with a concrete production example.
**A:** EHT images of M87* and Sgr A* measure ring diameter and asymmetry; horizon scale imaging inversions use those to constrain the spacetime. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: Why do horizon scale imaging models show the disk brighter on one side - justify your answer with a concrete production example.
**A:** Relativistic beaming amplifies emission from the approaching side; horizon scale imaging visibility depends on the disk velocity and line of sight. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: How does horizon scale imaging guide the choice of simulation data - justify your answer with a concrete production example.
**A:** Disk state (SANE/MAD), electron distribution, and spin control morphology; horizon scale imaging selection is part of the science, not just plumbing. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What does horizon scale imaging say about temperature - justify your answer with a concrete production example.
**A:** The inner flow reaches billions of Kelvin; horizon scale imaging emission intensity maps to temperature and magnetic field through emissivity relations. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: How is horizon scale imaging measured with EHT - justify your answer with a concrete production example.
**A:** Very long baseline interferometry synthesizes a horizon-scale aperture; horizon scale imaging plausibility is judged against its reconstructed images. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What distinguishes horizon scale imaging for supermassive vs stellar black holes - justify your answer with a concrete production example.
**A:** Scales shift by mass, but dimensionless quantities like the photon-ring radius are universal; horizon scale imaging transfers across masses by scaling. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What role do jets play in horizon scale imaging - justify your answer with a concrete production example.
**A:** Poynting-flux outflows can shine in their own right and shape the outermost emission; horizon scale imaging includes them for completeness. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does horizon scale imaging treat the electron thermodynamics - justify your answer with a concrete production example.
**A:** Since GRMHD often does not track electron vs ion temperature, horizon scale imaging uses proxies like R-beta prescriptions to convert fluid heating into emissivity. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What is the next frontier in horizon scale imaging - justify your answer with a concrete production example.
**A:** Time-dependent images and movie predictions from turbulent simulations observed by upgraded EHT arrays; horizon scale imaging is moving from stills to dynamics. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: What is the next frontier in horizon scale imaging - justify your answer with a concrete production example.
**A:** Time-dependent images and movie predictions from turbulent simulations observed by upgraded EHT arrays; horizon scale imaging is moving from stills to dynamics. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: How does horizon scale imaging treat the electron thermodynamics - justify your answer with a concrete production example.
**A:** Since GRMHD often does not track electron vs ion temperature, horizon scale imaging uses proxies like R-beta prescriptions to convert fluid heating into emissivity. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What role do jets play in horizon scale imaging - justify your answer with a concrete production example.
**A:** Poynting-flux outflows can shine in their own right and shape the outermost emission; horizon scale imaging includes them for completeness. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What distinguishes horizon scale imaging for supermassive vs stellar black holes - justify your answer with a concrete production example.
**A:** Scales shift by mass, but dimensionless quantities like the photon-ring radius are universal; horizon scale imaging transfers across masses by scaling. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How is horizon scale imaging measured with EHT - justify your answer with a concrete production example.
**A:** Very long baseline interferometry synthesizes a horizon-scale aperture; horizon scale imaging plausibility is judged against its reconstructed images. A concrete example: consistently applying horizon scale imaging in code review and regression tests keeps the whole pipeline trustworthy.
