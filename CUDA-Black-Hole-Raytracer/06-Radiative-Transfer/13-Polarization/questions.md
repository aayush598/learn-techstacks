# Radiative Transfer — Polarization Interview Questions and Answers

## Q1: What is synchrotron polarization?
**A:** The linear polarization produced by the anisotropic gyrating radiation of aligned-helix electrons - typically 60-75% in the E-vector for a uniform B.

## Q2: What is the polarization fraction?
**A:** For a power-law electron index p: pi = (p+1)/(p+7/3); for a monoenergetic gas: 75% - the code must output this geometric fraction.

## Q3: What is the polarization angle?
**A:** The electric-vector position angle (EVPA) on the sky - measures the B-field's sky-projected direction; its pattern is the image's B-field map.

## Q4: What is Faraday rotation?
**A:** The rotation of the polarization angle with wavelength as the wave passes magnetized plasma: chi(lambda) ~ lambda^2 RM - the RM is a plasma diagnostic.

## Q5: What is the rotation measure (RM)?
**A:** RM ~ integral n_e B_parallel ds (in suitable units) - the aggregate magneto-ionic column; its sign flips with B direction.

## Q6: How is polarization a tensor in the RTE?
**A:** The transfer expands to Stokes parameters (I,Q,U,V) with emissivity/absorption matrices (absorption, rotation, conversion) - the '7-coefficient' formalism.

## Q7: How does the raytracer handle it?
**A:** Per quadrature segment, the Stokes vector is advanced: emission adds (p_JI, p_JQ, ...); Faraday rotates Q,U; absorption multiplies - integrated like I alone.

## Q8: What is the parallel transport of polarization?
**A:** The polarization basis must be parallel-propagated along the geodesic - the EVPA's orientation on the sky derives from the transported basis, not the naive image frame.

## Q9: What does polarization add to the image?
**A:** It reveals field structure invisible in intensity (kinks, loops, reconnection) - maps of fractional polarization are richer than I alone.

## Q10: What is the stability (EVPA swing) observable?
**A:** The EVPA sweeping as a spot orbits reflects both the field geometry and the beaming - a time-domain polarization probe.

## Q11: What is the validation of the Stokes integrator?
**A:** Uniform B, no Faraday: analytic fractional polarization matches; with constant RM: the lambda^2 law holds per pixel - both closed-form checks.

## Q12: What are the numerical pitfalls?
**A:** Division-by-I when computing fractional polarization near the shadow; EVPA wrap-around at 180 deg; and the basis's discontinuities at the poles - all must be handled.

## Q13: How does the code output polarized images?
**A:** Channels (I,Q,U,V) per pixel at each band, or the derived (fraction, EVPA) maps - the deliverable for both display and analysis.

## Q14: How does polarization connect to GRMHD?
**A:** The pattern of the EVPA trace-out the magnetic structure at the emission site - polarization imaging is a direct probe of the B-field the GRMHD predicts.

## Q15: What is the summary?
**A:** Polarization is the Stokes extension of the transfer - emissivity/absorption/Faraday matrices plus parallel-transported bases - turning B-maps into field diagnostics.

## Q16: What question does polarization answer for a raytracer?
**A:** Given the plasma state along a photon path, it computes how much light reaches the observer after emission, absorption, and frequency shifts.

## Q17: Why is polarization essential for connecting GRMHD to pixels?
**A:** Plasma data alone is invisible; polarization converts density, temperature, and magnetic field into the intensity and color every pixel shows.

## Q18: What is the fundamental equation of polarization?
**A:** The radiative transfer equation dI/ds = j - alpha I along the ray; polarization integrates it including the relativistic invariant I/nu^3.

## Q19: What simplification is common in polarization for black holes?
**A:** The optically thin synchrotron-dominated case, where emission is computed per path segment and absorption is often neglected in the first pass.

## Q20: How does polarization handle moving frames?
**A:** Emissivity and absorption are defined in the fluid rest frame, then redshifted and Doppler-boosted into the coordinate/observer frame using the redshift factor.

## Q21: What are the two integration strategies for polarization?
**A:** Opacity-based ray casting through grid cells and analytic integration of the transfer equation through integrable models; production codes use the former.

## Q22: How does polarization determine color?
**A:** By integrating the spectrum at several fiducial frequencies and mapping the log-frequency-integrated intensity to a perceptual color ramp.

## Q23: What role does the optical depth tau play in polarization?
**A:** tau integrates the absorption along the path; large tau means the flow self-shields, which polarization must respect to avoid over-bright images.

## Q24: How does polarization encode a Lorentz boost?
**A:** The emissivity picks up a factor (1/g(1-beta·n))^2-ish from beaming plus the frequency shift; polarization applies these along the local fluid velocity.

## Q25: Why does synchrotron dominate disk emission in polarization?
**A:** The field and relativistic electrons radiate efficiently at the observed frequencies; thermal emission contributes where the flow is densest and coolest.

## Q26: What is the invariant form used in polarization?
**A:** I_nu / nu^3 is invariant along a ray, so polarization can transfer in any frame by tracking the frequency shift continuously.

## Q27: How do you validate polarization?
**A:** Reproduce analytic synchrotron spectra, check that a static uniform sphere has constant surface brightness, and compare derived images with published renders.

## Q28: How does polarization handle scattering?
**A:** Fully including scattering needs Monte Carlo; most pipeline polarization ignores it for the polarized-total intensity morphology and adds it later.

## Q29: What output does polarization produce per pixel?
**A:** Total intensity (and optionally Stokes IQUV) per frequency band; polarization is the last physics stage before tone mapping converts to an image.

## Q30: How do you make polarization deterministic?
**A:** Run the same snapshot, ray grid, and frequency set twice; bit-identical polarization means the pipeline is reproducible for science and movies.

## Q31: What do the measured M87-like images imply for polarization?
**A:** The bright ring and south-side enhancement follow from Doppler boosting of the approaching disk side; polarization reproduces these signatures from the velocity field.

## Q32: How does polarization integrate through the grid?
**A:** March through cells with a ray-grid traversal, sampling the fluid state, and update intensity with the segment transfer solution each step.

## Q33: What precision does polarization need?
**A:** Double precision for the integration of small intensities near the ring; polarization is the stage where visible artifacts for `dark' and `bright' regions meet.

## Q34: How do you compute the emitted frequency in polarization?
**A:** The fluid-frame frequency divides by (1+z) where z is the integrated redshift; polarization sets up spectral bins by emitted frequency in the observer band.

## Q35: What are the simplest usable emission models in polarization?
**A:** A thermal blackbody-approximation from temperature and density, or synchrotron power laws with gamma-distributed electrons; polarization starts with the simplest and upgrades.

## Q36: How does polarization create the visually iconic thin bright ring?
**A:** Near the photon sphere, rays sweep long path lengths through the brightest, most-beamed plasma, so integrated polarization intensity peaks there.

## Q37: What is the Doppler ratio that drives asymmetry in polarization?
**A:** The ratio between approaching and receding disk sides, roughly (1+beta cos theta over 1-beta cos theta) powers; polarization makes one side 3-5x brighter.

## Q38: How is polarization checked against real observations?
**A:** By comparing ring diameter, asymmetry, and spectrum to EHT measurements - agreement on those is the acceptance test for polarization.

## Q39: How does polarization fit the movie pipeline?
**A:** Rendering N frames applies polarization to each snapshot; polarization performance (per-ray cost) sets the total render budget for a movie.

## Q40: How does polarization fit the movie pipeline - justify your answer with a concrete production example.
**A:** Rendering N frames applies polarization to each snapshot; polarization performance (per-ray cost) sets the total render budget for a movie. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: How is polarization checked against real observations - justify your answer with a concrete production example.
**A:** By comparing ring diameter, asymmetry, and spectrum to EHT measurements - agreement on those is the acceptance test for polarization. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What is the Doppler ratio that drives asymmetry in polarization - justify your answer with a concrete production example.
**A:** The ratio between approaching and receding disk sides, roughly (1+beta cos theta over 1-beta cos theta) powers; polarization makes one side 3-5x brighter. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: How does polarization create the visually iconic thin bright ring - justify your answer with a concrete production example.
**A:** Near the photon sphere, rays sweep long path lengths through the brightest, most-beamed plasma, so integrated polarization intensity peaks there. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What are the simplest usable emission models in polarization - justify your answer with a concrete production example.
**A:** A thermal blackbody-approximation from temperature and density, or synchrotron power laws with gamma-distributed electrons; polarization starts with the simplest and upgrades. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: How do you compute the emitted frequency in polarization - justify your answer with a concrete production example.
**A:** The fluid-frame frequency divides by (1+z) where z is the integrated redshift; polarization sets up spectral bins by emitted frequency in the observer band. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: What precision does polarization need - justify your answer with a concrete production example.
**A:** Double precision for the integration of small intensities near the ring; polarization is the stage where visible artifacts for `dark' and `bright' regions meet. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: How does polarization integrate through the grid - justify your answer with a concrete production example.
**A:** March through cells with a ray-grid traversal, sampling the fluid state, and update intensity with the segment transfer solution each step. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: What do the measured M87-like images imply for polarization - justify your answer with a concrete production example.
**A:** The bright ring and south-side enhancement follow from Doppler boosting of the approaching disk side; polarization reproduces these signatures from the velocity field. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: How do you make polarization deterministic - justify your answer with a concrete production example.
**A:** Run the same snapshot, ray grid, and frequency set twice; bit-identical polarization means the pipeline is reproducible for science and movies. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What output does polarization produce per pixel - justify your answer with a concrete production example.
**A:** Total intensity (and optionally Stokes IQUV) per frequency band; polarization is the last physics stage before tone mapping converts to an image. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How does polarization handle scattering - justify your answer with a concrete production example.
**A:** Fully including scattering needs Monte Carlo; most pipeline polarization ignores it for the polarized-total intensity morphology and adds it later. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How do you validate polarization - justify your answer with a concrete production example.
**A:** Reproduce analytic synchrotron spectra, check that a static uniform sphere has constant surface brightness, and compare derived images with published renders. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What is the invariant form used in polarization - justify your answer with a concrete production example.
**A:** I_nu / nu^3 is invariant along a ray, so polarization can transfer in any frame by tracking the frequency shift continuously. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: Why does synchrotron dominate disk emission in polarization - justify your answer with a concrete production example.
**A:** The field and relativistic electrons radiate efficiently at the observed frequencies; thermal emission contributes where the flow is densest and coolest. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: How does polarization encode a Lorentz boost - justify your answer with a concrete production example.
**A:** The emissivity picks up a factor (1/g(1-beta·n))^2-ish from beaming plus the frequency shift; polarization applies these along the local fluid velocity. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What role does the optical depth tau play in polarization - justify your answer with a concrete production example.
**A:** tau integrates the absorption along the path; large tau means the flow self-shields, which polarization must respect to avoid over-bright images. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How does polarization determine color - justify your answer with a concrete production example.
**A:** By integrating the spectrum at several fiducial frequencies and mapping the log-frequency-integrated intensity to a perceptual color ramp. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What are the two integration strategies for polarization - justify your answer with a concrete production example.
**A:** Opacity-based ray casting through grid cells and analytic integration of the transfer equation through integrable models; production codes use the former. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How does polarization handle moving frames - justify your answer with a concrete production example.
**A:** Emissivity and absorption are defined in the fluid rest frame, then redshifted and Doppler-boosted into the coordinate/observer frame using the redshift factor. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What simplification is common in polarization for black holes - justify your answer with a concrete production example.
**A:** The optically thin synchrotron-dominated case, where emission is computed per path segment and absorption is often neglected in the first pass. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What is the fundamental equation of polarization - justify your answer with a concrete production example.
**A:** The radiative transfer equation dI/ds = j - alpha I along the ray; polarization integrates it including the relativistic invariant I/nu^3. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why is polarization essential for connecting GRMHD to pixels - justify your answer with a concrete production example.
**A:** Plasma data alone is invisible; polarization converts density, temperature, and magnetic field into the intensity and color every pixel shows. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What question does polarization answer for a raytracer - justify your answer with a concrete production example.
**A:** Given the plasma state along a photon path, it computes how much light reaches the observer after emission, absorption, and frequency shifts. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What question does polarization answer for a raytracer - justify your answer with a concrete production example.
**A:** Given the plasma state along a photon path, it computes how much light reaches the observer after emission, absorption, and frequency shifts. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why is polarization essential for connecting GRMHD to pixels - justify your answer with a concrete production example.
**A:** Plasma data alone is invisible; polarization converts density, temperature, and magnetic field into the intensity and color every pixel shows. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What is the fundamental equation of polarization - justify your answer with a concrete production example.
**A:** The radiative transfer equation dI/ds = j - alpha I along the ray; polarization integrates it including the relativistic invariant I/nu^3. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What simplification is common in polarization for black holes - justify your answer with a concrete production example.
**A:** The optically thin synchrotron-dominated case, where emission is computed per path segment and absorption is often neglected in the first pass. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How does polarization handle moving frames - justify your answer with a concrete production example.
**A:** Emissivity and absorption are defined in the fluid rest frame, then redshifted and Doppler-boosted into the coordinate/observer frame using the redshift factor. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What are the two integration strategies for polarization - justify your answer with a concrete production example.
**A:** Opacity-based ray casting through grid cells and analytic integration of the transfer equation through integrable models; production codes use the former. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How does polarization determine color - justify your answer with a concrete production example.
**A:** By integrating the spectrum at several fiducial frequencies and mapping the log-frequency-integrated intensity to a perceptual color ramp. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What role does the optical depth tau play in polarization - justify your answer with a concrete production example.
**A:** tau integrates the absorption along the path; large tau means the flow self-shields, which polarization must respect to avoid over-bright images. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: How does polarization encode a Lorentz boost - justify your answer with a concrete production example.
**A:** The emissivity picks up a factor (1/g(1-beta·n))^2-ish from beaming plus the frequency shift; polarization applies these along the local fluid velocity. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: Why does synchrotron dominate disk emission in polarization - justify your answer with a concrete production example.
**A:** The field and relativistic electrons radiate efficiently at the observed frequencies; thermal emission contributes where the flow is densest and coolest. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What is the invariant form used in polarization - justify your answer with a concrete production example.
**A:** I_nu / nu^3 is invariant along a ray, so polarization can transfer in any frame by tracking the frequency shift continuously. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How do you validate polarization - justify your answer with a concrete production example.
**A:** Reproduce analytic synchrotron spectra, check that a static uniform sphere has constant surface brightness, and compare derived images with published renders. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How does polarization handle scattering - justify your answer with a concrete production example.
**A:** Fully including scattering needs Monte Carlo; most pipeline polarization ignores it for the polarized-total intensity morphology and adds it later. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What output does polarization produce per pixel - justify your answer with a concrete production example.
**A:** Total intensity (and optionally Stokes IQUV) per frequency band; polarization is the last physics stage before tone mapping converts to an image. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: How do you make polarization deterministic - justify your answer with a concrete production example.
**A:** Run the same snapshot, ray grid, and frequency set twice; bit-identical polarization means the pipeline is reproducible for science and movies. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What do the measured M87-like images imply for polarization - justify your answer with a concrete production example.
**A:** The bright ring and south-side enhancement follow from Doppler boosting of the approaching disk side; polarization reproduces these signatures from the velocity field. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How does polarization integrate through the grid - justify your answer with a concrete production example.
**A:** March through cells with a ray-grid traversal, sampling the fluid state, and update intensity with the segment transfer solution each step. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: What precision does polarization need - justify your answer with a concrete production example.
**A:** Double precision for the integration of small intensities near the ring; polarization is the stage where visible artifacts for `dark' and `bright' regions meet. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: How do you compute the emitted frequency in polarization - justify your answer with a concrete production example.
**A:** The fluid-frame frequency divides by (1+z) where z is the integrated redshift; polarization sets up spectral bins by emitted frequency in the observer band. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What are the simplest usable emission models in polarization - justify your answer with a concrete production example.
**A:** A thermal blackbody-approximation from temperature and density, or synchrotron power laws with gamma-distributed electrons; polarization starts with the simplest and upgrades. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: How does polarization create the visually iconic thin bright ring - justify your answer with a concrete production example.
**A:** Near the photon sphere, rays sweep long path lengths through the brightest, most-beamed plasma, so integrated polarization intensity peaks there. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What is the Doppler ratio that drives asymmetry in polarization - justify your answer with a concrete production example.
**A:** The ratio between approaching and receding disk sides, roughly (1+beta cos theta over 1-beta cos theta) powers; polarization makes one side 3-5x brighter. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: How is polarization checked against real observations - justify your answer with a concrete production example.
**A:** By comparing ring diameter, asymmetry, and spectrum to EHT measurements - agreement on those is the acceptance test for polarization. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How does polarization fit the movie pipeline - justify your answer with a concrete production example.
**A:** Rendering N frames applies polarization to each snapshot; polarization performance (per-ray cost) sets the total render budget for a movie. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How does polarization fit the movie pipeline - justify your answer with a concrete production example.
**A:** Rendering N frames applies polarization to each snapshot; polarization performance (per-ray cost) sets the total render budget for a movie. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: How is polarization checked against real observations - justify your answer with a concrete production example.
**A:** By comparing ring diameter, asymmetry, and spectrum to EHT measurements - agreement on those is the acceptance test for polarization. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What is the Doppler ratio that drives asymmetry in polarization - justify your answer with a concrete production example.
**A:** The ratio between approaching and receding disk sides, roughly (1+beta cos theta over 1-beta cos theta) powers; polarization makes one side 3-5x brighter. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: How does polarization create the visually iconic thin bright ring - justify your answer with a concrete production example.
**A:** Near the photon sphere, rays sweep long path lengths through the brightest, most-beamed plasma, so integrated polarization intensity peaks there. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What are the simplest usable emission models in polarization - justify your answer with a concrete production example.
**A:** A thermal blackbody-approximation from temperature and density, or synchrotron power laws with gamma-distributed electrons; polarization starts with the simplest and upgrades. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: How do you compute the emitted frequency in polarization - justify your answer with a concrete production example.
**A:** The fluid-frame frequency divides by (1+z) where z is the integrated redshift; polarization sets up spectral bins by emitted frequency in the observer band. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: What precision does polarization need - justify your answer with a concrete production example.
**A:** Double precision for the integration of small intensities near the ring; polarization is the stage where visible artifacts for `dark' and `bright' regions meet. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: How does polarization integrate through the grid - justify your answer with a concrete production example.
**A:** March through cells with a ray-grid traversal, sampling the fluid state, and update intensity with the segment transfer solution each step. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: What do the measured M87-like images imply for polarization - justify your answer with a concrete production example.
**A:** The bright ring and south-side enhancement follow from Doppler boosting of the approaching disk side; polarization reproduces these signatures from the velocity field. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: How do you make polarization deterministic - justify your answer with a concrete production example.
**A:** Run the same snapshot, ray grid, and frequency set twice; bit-identical polarization means the pipeline is reproducible for science and movies. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What output does polarization produce per pixel - justify your answer with a concrete production example.
**A:** Total intensity (and optionally Stokes IQUV) per frequency band; polarization is the last physics stage before tone mapping converts to an image. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How does polarization handle scattering - justify your answer with a concrete production example.
**A:** Fully including scattering needs Monte Carlo; most pipeline polarization ignores it for the polarized-total intensity morphology and adds it later. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How do you validate polarization - justify your answer with a concrete production example.
**A:** Reproduce analytic synchrotron spectra, check that a static uniform sphere has constant surface brightness, and compare derived images with published renders. A concrete example: consistently applying polarization in code review and regression tests keeps the whole pipeline trustworthy.
