# Radiative Transfer — Optical Depth Interview Questions and Answers

## Q1: What is the optical depth and its ranges?
**A:** tau = integral alpha ds; tau>1 means 'absorptively opaque' (shielding, reabsorption), tau<1 'transparent' (emission escapes) - the unitless ruler of transfer.

## Q2: How does tau enter the formal solution?
**A:** The attenuation factor e^-tau and the source-weight exp(-(tau-tau')) appear; tau accumulates monotonically along the ray - the RTE's clock.

## Q3: Why is the disk often optically thin?
**A:** In M87-band optically thin synchrotron the emissivity's self-absorption is weak: tau~0.1-0.01 at the ring - the transparency is the reason the image integrates volume emission.

## Q4: What is the condition for 'thin'?
**A:** tau << 1 across the line; the transmitted fraction ~ 1 - small corrections; for thick regions the transfer saturates toward the source function.

## Q5: What does an opaque region do to the image?
**A:** It obstructs background emission (eclipses the far ring) and re-emits at the local source function - a self-absorbed blob appears as a secondary ring feature.

## Q6: How is tau accumulated in the code?
**A:** Integrate alpha along the affine parameter with the frequency-shift bookkeeping: dtau = alpha_rest * (nu_obs/nu_emit) * dl - the combination that makes tau frame-true.

## Q7: What is the tau-path relationship?
**A:** For a constant-density column: tau = alpha L; in the disk, tau varies with the local B^2-dependent absorption - the radiative balance loops back in.

## Q8: How does optical depth affect the observed ring?
**A:** If the inner shell is opaque (tau>1), the visible ring is the surface where tau~1, moving the peak outward vs thin emission - a measurable offset.

## Q9: What is the 'source function' saturation?
**A:** Where tau>>1, I -> S (the local thermal source); synchrotron self-absorption drives S toward the blackbody limit of the emitting electrons.

## Q10: How do you compute tau along a geodesic?
**A:** Each ray segment accumulates alpha_nu(local rest) * (dl / frequency ratios); converting affine to physical length uses the metric components.

## Q11: What is the frequency coupling in alpha?
**A:** alpha_nu ~ n_e B^(...) nu^(-(...)) for synchrotron; the raytracer samples at the shifted frequency - the same map as the emissivity evaluation.

## Q12: What does the floor/clamp do to tau?
**A:** If a cell density floor creates spurious opacity, the image dims - report cell floors with every image (the artifact budget).

## Q13: What is the thin/integration validation?
**A:** A homogeneous column with known j, alpha: the analytic I(tau) must match; drift of that relation is a transfer-kernel bug.

## Q14: How does 'we see through the shadow' work?
**A:** Even inside the shadow region, foreground emission (thin) contributes, so the shadow's blackness is relative to the inflow-bright background - a subtle fill.

## Q15: What is the practical dialog with the image?
**A:** Check the ring's tau map: if the sheath tau is <0.5 the thin-limit render is valid; if it crosses 1, switch the kernel to the full solution and re-render.

## Q16: What question does optical depth answer for a raytracer?
**A:** Given the plasma state along a photon path, it computes how much light reaches the observer after emission, absorption, and frequency shifts.

## Q17: Why is optical depth essential for connecting GRMHD to pixels?
**A:** Plasma data alone is invisible; optical depth converts density, temperature, and magnetic field into the intensity and color every pixel shows.

## Q18: What is the fundamental equation of optical depth?
**A:** The radiative transfer equation dI/ds = j - alpha I along the ray; optical depth integrates it including the relativistic invariant I/nu^3.

## Q19: What simplification is common in optical depth for black holes?
**A:** The optically thin synchrotron-dominated case, where emission is computed per path segment and absorption is often neglected in the first pass.

## Q20: How does optical depth handle moving frames?
**A:** Emissivity and absorption are defined in the fluid rest frame, then redshifted and Doppler-boosted into the coordinate/observer frame using the redshift factor.

## Q21: What are the two integration strategies for optical depth?
**A:** Opacity-based ray casting through grid cells and analytic integration of the transfer equation through integrable models; production codes use the former.

## Q22: How does optical depth determine color?
**A:** By integrating the spectrum at several fiducial frequencies and mapping the log-frequency-integrated intensity to a perceptual color ramp.

## Q23: What role does the optical depth tau play in optical depth?
**A:** tau integrates the absorption along the path; large tau means the flow self-shields, which optical depth must respect to avoid over-bright images.

## Q24: How does optical depth encode a Lorentz boost?
**A:** The emissivity picks up a factor (1/g(1-beta·n))^2-ish from beaming plus the frequency shift; optical depth applies these along the local fluid velocity.

## Q25: Why does synchrotron dominate disk emission in optical depth?
**A:** The field and relativistic electrons radiate efficiently at the observed frequencies; thermal emission contributes where the flow is densest and coolest.

## Q26: What is the invariant form used in optical depth?
**A:** I_nu / nu^3 is invariant along a ray, so optical depth can transfer in any frame by tracking the frequency shift continuously.

## Q27: How do you validate optical depth?
**A:** Reproduce analytic synchrotron spectra, check that a static uniform sphere has constant surface brightness, and compare derived images with published renders.

## Q28: How does optical depth handle scattering?
**A:** Fully including scattering needs Monte Carlo; most pipeline optical depth ignores it for the polarized-total intensity morphology and adds it later.

## Q29: What output does optical depth produce per pixel?
**A:** Total intensity (and optionally Stokes IQUV) per frequency band; optical depth is the last physics stage before tone mapping converts to an image.

## Q30: How do you make optical depth deterministic?
**A:** Run the same snapshot, ray grid, and frequency set twice; bit-identical optical depth means the pipeline is reproducible for science and movies.

## Q31: What do the measured M87-like images imply for optical depth?
**A:** The bright ring and south-side enhancement follow from Doppler boosting of the approaching disk side; optical depth reproduces these signatures from the velocity field.

## Q32: How does optical depth integrate through the grid?
**A:** March through cells with a ray-grid traversal, sampling the fluid state, and update intensity with the segment transfer solution each step.

## Q33: What precision does optical depth need?
**A:** Double precision for the integration of small intensities near the ring; optical depth is the stage where visible artifacts for `dark' and `bright' regions meet.

## Q34: How do you compute the emitted frequency in optical depth?
**A:** The fluid-frame frequency divides by (1+z) where z is the integrated redshift; optical depth sets up spectral bins by emitted frequency in the observer band.

## Q35: What are the simplest usable emission models in optical depth?
**A:** A thermal blackbody-approximation from temperature and density, or synchrotron power laws with gamma-distributed electrons; optical depth starts with the simplest and upgrades.

## Q36: How does optical depth create the visually iconic thin bright ring?
**A:** Near the photon sphere, rays sweep long path lengths through the brightest, most-beamed plasma, so integrated optical depth intensity peaks there.

## Q37: What is the Doppler ratio that drives asymmetry in optical depth?
**A:** The ratio between approaching and receding disk sides, roughly (1+beta cos theta over 1-beta cos theta) powers; optical depth makes one side 3-5x brighter.

## Q38: How is optical depth checked against real observations?
**A:** By comparing ring diameter, asymmetry, and spectrum to EHT measurements - agreement on those is the acceptance test for optical depth.

## Q39: How does optical depth fit the movie pipeline?
**A:** Rendering N frames applies optical depth to each snapshot; optical depth performance (per-ray cost) sets the total render budget for a movie.

## Q40: How does optical depth fit the movie pipeline - justify your answer with a concrete production example.
**A:** Rendering N frames applies optical depth to each snapshot; optical depth performance (per-ray cost) sets the total render budget for a movie. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: How is optical depth checked against real observations - justify your answer with a concrete production example.
**A:** By comparing ring diameter, asymmetry, and spectrum to EHT measurements - agreement on those is the acceptance test for optical depth. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What is the Doppler ratio that drives asymmetry in optical depth - justify your answer with a concrete production example.
**A:** The ratio between approaching and receding disk sides, roughly (1+beta cos theta over 1-beta cos theta) powers; optical depth makes one side 3-5x brighter. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: How does optical depth create the visually iconic thin bright ring - justify your answer with a concrete production example.
**A:** Near the photon sphere, rays sweep long path lengths through the brightest, most-beamed plasma, so integrated optical depth intensity peaks there. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What are the simplest usable emission models in optical depth - justify your answer with a concrete production example.
**A:** A thermal blackbody-approximation from temperature and density, or synchrotron power laws with gamma-distributed electrons; optical depth starts with the simplest and upgrades. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: How do you compute the emitted frequency in optical depth - justify your answer with a concrete production example.
**A:** The fluid-frame frequency divides by (1+z) where z is the integrated redshift; optical depth sets up spectral bins by emitted frequency in the observer band. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: What precision does optical depth need - justify your answer with a concrete production example.
**A:** Double precision for the integration of small intensities near the ring; optical depth is the stage where visible artifacts for `dark' and `bright' regions meet. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: How does optical depth integrate through the grid - justify your answer with a concrete production example.
**A:** March through cells with a ray-grid traversal, sampling the fluid state, and update intensity with the segment transfer solution each step. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: What do the measured M87-like images imply for optical depth - justify your answer with a concrete production example.
**A:** The bright ring and south-side enhancement follow from Doppler boosting of the approaching disk side; optical depth reproduces these signatures from the velocity field. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: How do you make optical depth deterministic - justify your answer with a concrete production example.
**A:** Run the same snapshot, ray grid, and frequency set twice; bit-identical optical depth means the pipeline is reproducible for science and movies. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What output does optical depth produce per pixel - justify your answer with a concrete production example.
**A:** Total intensity (and optionally Stokes IQUV) per frequency band; optical depth is the last physics stage before tone mapping converts to an image. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How does optical depth handle scattering - justify your answer with a concrete production example.
**A:** Fully including scattering needs Monte Carlo; most pipeline optical depth ignores it for the polarized-total intensity morphology and adds it later. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How do you validate optical depth - justify your answer with a concrete production example.
**A:** Reproduce analytic synchrotron spectra, check that a static uniform sphere has constant surface brightness, and compare derived images with published renders. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What is the invariant form used in optical depth - justify your answer with a concrete production example.
**A:** I_nu / nu^3 is invariant along a ray, so optical depth can transfer in any frame by tracking the frequency shift continuously. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: Why does synchrotron dominate disk emission in optical depth - justify your answer with a concrete production example.
**A:** The field and relativistic electrons radiate efficiently at the observed frequencies; thermal emission contributes where the flow is densest and coolest. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: How does optical depth encode a Lorentz boost - justify your answer with a concrete production example.
**A:** The emissivity picks up a factor (1/g(1-beta·n))^2-ish from beaming plus the frequency shift; optical depth applies these along the local fluid velocity. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What role does the optical depth tau play in optical depth - justify your answer with a concrete production example.
**A:** tau integrates the absorption along the path; large tau means the flow self-shields, which optical depth must respect to avoid over-bright images. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How does optical depth determine color - justify your answer with a concrete production example.
**A:** By integrating the spectrum at several fiducial frequencies and mapping the log-frequency-integrated intensity to a perceptual color ramp. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What are the two integration strategies for optical depth - justify your answer with a concrete production example.
**A:** Opacity-based ray casting through grid cells and analytic integration of the transfer equation through integrable models; production codes use the former. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How does optical depth handle moving frames - justify your answer with a concrete production example.
**A:** Emissivity and absorption are defined in the fluid rest frame, then redshifted and Doppler-boosted into the coordinate/observer frame using the redshift factor. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What simplification is common in optical depth for black holes - justify your answer with a concrete production example.
**A:** The optically thin synchrotron-dominated case, where emission is computed per path segment and absorption is often neglected in the first pass. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What is the fundamental equation of optical depth - justify your answer with a concrete production example.
**A:** The radiative transfer equation dI/ds = j - alpha I along the ray; optical depth integrates it including the relativistic invariant I/nu^3. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why is optical depth essential for connecting GRMHD to pixels - justify your answer with a concrete production example.
**A:** Plasma data alone is invisible; optical depth converts density, temperature, and magnetic field into the intensity and color every pixel shows. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What question does optical depth answer for a raytracer - justify your answer with a concrete production example.
**A:** Given the plasma state along a photon path, it computes how much light reaches the observer after emission, absorption, and frequency shifts. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What question does optical depth answer for a raytracer - justify your answer with a concrete production example.
**A:** Given the plasma state along a photon path, it computes how much light reaches the observer after emission, absorption, and frequency shifts. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why is optical depth essential for connecting GRMHD to pixels - justify your answer with a concrete production example.
**A:** Plasma data alone is invisible; optical depth converts density, temperature, and magnetic field into the intensity and color every pixel shows. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What is the fundamental equation of optical depth - justify your answer with a concrete production example.
**A:** The radiative transfer equation dI/ds = j - alpha I along the ray; optical depth integrates it including the relativistic invariant I/nu^3. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What simplification is common in optical depth for black holes - justify your answer with a concrete production example.
**A:** The optically thin synchrotron-dominated case, where emission is computed per path segment and absorption is often neglected in the first pass. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How does optical depth handle moving frames - justify your answer with a concrete production example.
**A:** Emissivity and absorption are defined in the fluid rest frame, then redshifted and Doppler-boosted into the coordinate/observer frame using the redshift factor. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What are the two integration strategies for optical depth - justify your answer with a concrete production example.
**A:** Opacity-based ray casting through grid cells and analytic integration of the transfer equation through integrable models; production codes use the former. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How does optical depth determine color - justify your answer with a concrete production example.
**A:** By integrating the spectrum at several fiducial frequencies and mapping the log-frequency-integrated intensity to a perceptual color ramp. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What role does the optical depth tau play in optical depth - justify your answer with a concrete production example.
**A:** tau integrates the absorption along the path; large tau means the flow self-shields, which optical depth must respect to avoid over-bright images. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: How does optical depth encode a Lorentz boost - justify your answer with a concrete production example.
**A:** The emissivity picks up a factor (1/g(1-beta·n))^2-ish from beaming plus the frequency shift; optical depth applies these along the local fluid velocity. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: Why does synchrotron dominate disk emission in optical depth - justify your answer with a concrete production example.
**A:** The field and relativistic electrons radiate efficiently at the observed frequencies; thermal emission contributes where the flow is densest and coolest. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What is the invariant form used in optical depth - justify your answer with a concrete production example.
**A:** I_nu / nu^3 is invariant along a ray, so optical depth can transfer in any frame by tracking the frequency shift continuously. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How do you validate optical depth - justify your answer with a concrete production example.
**A:** Reproduce analytic synchrotron spectra, check that a static uniform sphere has constant surface brightness, and compare derived images with published renders. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How does optical depth handle scattering - justify your answer with a concrete production example.
**A:** Fully including scattering needs Monte Carlo; most pipeline optical depth ignores it for the polarized-total intensity morphology and adds it later. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What output does optical depth produce per pixel - justify your answer with a concrete production example.
**A:** Total intensity (and optionally Stokes IQUV) per frequency band; optical depth is the last physics stage before tone mapping converts to an image. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: How do you make optical depth deterministic - justify your answer with a concrete production example.
**A:** Run the same snapshot, ray grid, and frequency set twice; bit-identical optical depth means the pipeline is reproducible for science and movies. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What do the measured M87-like images imply for optical depth - justify your answer with a concrete production example.
**A:** The bright ring and south-side enhancement follow from Doppler boosting of the approaching disk side; optical depth reproduces these signatures from the velocity field. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How does optical depth integrate through the grid - justify your answer with a concrete production example.
**A:** March through cells with a ray-grid traversal, sampling the fluid state, and update intensity with the segment transfer solution each step. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: What precision does optical depth need - justify your answer with a concrete production example.
**A:** Double precision for the integration of small intensities near the ring; optical depth is the stage where visible artifacts for `dark' and `bright' regions meet. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: How do you compute the emitted frequency in optical depth - justify your answer with a concrete production example.
**A:** The fluid-frame frequency divides by (1+z) where z is the integrated redshift; optical depth sets up spectral bins by emitted frequency in the observer band. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What are the simplest usable emission models in optical depth - justify your answer with a concrete production example.
**A:** A thermal blackbody-approximation from temperature and density, or synchrotron power laws with gamma-distributed electrons; optical depth starts with the simplest and upgrades. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: How does optical depth create the visually iconic thin bright ring - justify your answer with a concrete production example.
**A:** Near the photon sphere, rays sweep long path lengths through the brightest, most-beamed plasma, so integrated optical depth intensity peaks there. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What is the Doppler ratio that drives asymmetry in optical depth - justify your answer with a concrete production example.
**A:** The ratio between approaching and receding disk sides, roughly (1+beta cos theta over 1-beta cos theta) powers; optical depth makes one side 3-5x brighter. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: How is optical depth checked against real observations - justify your answer with a concrete production example.
**A:** By comparing ring diameter, asymmetry, and spectrum to EHT measurements - agreement on those is the acceptance test for optical depth. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How does optical depth fit the movie pipeline - justify your answer with a concrete production example.
**A:** Rendering N frames applies optical depth to each snapshot; optical depth performance (per-ray cost) sets the total render budget for a movie. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How does optical depth fit the movie pipeline - justify your answer with a concrete production example.
**A:** Rendering N frames applies optical depth to each snapshot; optical depth performance (per-ray cost) sets the total render budget for a movie. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: How is optical depth checked against real observations - justify your answer with a concrete production example.
**A:** By comparing ring diameter, asymmetry, and spectrum to EHT measurements - agreement on those is the acceptance test for optical depth. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What is the Doppler ratio that drives asymmetry in optical depth - justify your answer with a concrete production example.
**A:** The ratio between approaching and receding disk sides, roughly (1+beta cos theta over 1-beta cos theta) powers; optical depth makes one side 3-5x brighter. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: How does optical depth create the visually iconic thin bright ring - justify your answer with a concrete production example.
**A:** Near the photon sphere, rays sweep long path lengths through the brightest, most-beamed plasma, so integrated optical depth intensity peaks there. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What are the simplest usable emission models in optical depth - justify your answer with a concrete production example.
**A:** A thermal blackbody-approximation from temperature and density, or synchrotron power laws with gamma-distributed electrons; optical depth starts with the simplest and upgrades. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: How do you compute the emitted frequency in optical depth - justify your answer with a concrete production example.
**A:** The fluid-frame frequency divides by (1+z) where z is the integrated redshift; optical depth sets up spectral bins by emitted frequency in the observer band. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: What precision does optical depth need - justify your answer with a concrete production example.
**A:** Double precision for the integration of small intensities near the ring; optical depth is the stage where visible artifacts for `dark' and `bright' regions meet. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: How does optical depth integrate through the grid - justify your answer with a concrete production example.
**A:** March through cells with a ray-grid traversal, sampling the fluid state, and update intensity with the segment transfer solution each step. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: What do the measured M87-like images imply for optical depth - justify your answer with a concrete production example.
**A:** The bright ring and south-side enhancement follow from Doppler boosting of the approaching disk side; optical depth reproduces these signatures from the velocity field. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: How do you make optical depth deterministic - justify your answer with a concrete production example.
**A:** Run the same snapshot, ray grid, and frequency set twice; bit-identical optical depth means the pipeline is reproducible for science and movies. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What output does optical depth produce per pixel - justify your answer with a concrete production example.
**A:** Total intensity (and optionally Stokes IQUV) per frequency band; optical depth is the last physics stage before tone mapping converts to an image. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How does optical depth handle scattering - justify your answer with a concrete production example.
**A:** Fully including scattering needs Monte Carlo; most pipeline optical depth ignores it for the polarized-total intensity morphology and adds it later. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How do you validate optical depth - justify your answer with a concrete production example.
**A:** Reproduce analytic synchrotron spectra, check that a static uniform sphere has constant surface brightness, and compare derived images with published renders. A concrete example: consistently applying optical depth in code review and regression tests keeps the whole pipeline trustworthy.
