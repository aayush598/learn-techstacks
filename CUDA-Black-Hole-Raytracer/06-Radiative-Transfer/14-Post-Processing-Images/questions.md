# Radiative Transfer — Post Processing Images Interview Questions and Answers

## Q1: What is image post-processing?
**A:** The final pipeline that converts raw per-pixel intensity/Stokes frames into a viewable, scientifically analyzable image (fits, color, metrics).

## Q2: What are the common post steps?
**A:** Tone mapping, color balance, denoising, deconvolving dishes (PSF), converting to physical scale, and overlaying diagnostics (contours, beam).

## Q3: What is the difference between raw and displayed images?
**A:** Raw holds physical intensity at each pixel; display applies nonlinear scales (log/asinh), color tables, and blur - the physics stays in the raw channel.

## Q4: How is the image convolved with a telescope beam?
**A:** The true image is convolved with the PSF (e.g., a Gaussian beam) to mimic observations at a finite resolution - an essential step for realism.

## Q5: What is image-plane rescaling?
**A:** Mapping the render (in units of M/D) to physical angular size and flux units (Jy, mJy/beam) using the source distance and the SED.

## Q6: How do you denoise a Monte Carlo image?
**A:** Sample-count-based variance; higher supersampling near the ring reduces noise; denoise via conservative filters (no structures beyond the PSF).

## Q7: How are colors assembled?
**A:** Render 2-3 bands (e.g., 230 GHz, sub-mm) and map to a color space with the SED weighting - the chromatic image blends flux and shift science.

## Q8: What is the standard image product?
**A:** A FITS datacube (I,Q,U,V; or (I, f, EVPA)) at the chosen band with full WCS metadata - the artifact telescopes can compare to.

## Q9: What diagnostics accompany images?
**A:** Total flux, image moments (center, compactness), asymmetry metrics, and the ring radius profile - quantitative summaries from the pixels.

## Q10: How is temporal post-processing different?
**A:** Movies add frame interpolation/temporal smoothing; variability metrics (rms, power spectrum) ride on filtered light curves.

## Q11: What is the anti-burnout guard?
**A:** Clamp/saturate near-dark pixels before tone mapping; the raw channel is never touched - display brightness only adjusts through the tonemapper.

## Q12: What does a light curve require?
**A:** Time-tagged flux integrations in a band across frames - the renderer emits them alongside images for the time-domain science.

## Q13: How do you validate a post image?
**A:** The circular photon-ring radius, shadow center, and known fractional-polarization (uniform-field checks) reproject onto the final image - a quantitative gate.

## Q14: What is the deliverable contract?
**A:** Raw physical intensity + metadata + display render + diagnostics, all coherent: the post-pipeline is where science meeting images meets the telescope.

## Q15: What is the summary?
**A:** Post-processing turns ray-traced physics into telescope-ready products - PSF convolution, scale, SED color, diagnostics - while keeping the raw data intact and auditable.

## Q16: What question does post processing images answer for a raytracer?
**A:** Given the plasma state along a photon path, it computes how much light reaches the observer after emission, absorption, and frequency shifts.

## Q17: Why is post processing images essential for connecting GRMHD to pixels?
**A:** Plasma data alone is invisible; post processing images converts density, temperature, and magnetic field into the intensity and color every pixel shows.

## Q18: What is the fundamental equation of post processing images?
**A:** The radiative transfer equation dI/ds = j - alpha I along the ray; post processing images integrates it including the relativistic invariant I/nu^3.

## Q19: What simplification is common in post processing images for black holes?
**A:** The optically thin synchrotron-dominated case, where emission is computed per path segment and absorption is often neglected in the first pass.

## Q20: How does post processing images handle moving frames?
**A:** Emissivity and absorption are defined in the fluid rest frame, then redshifted and Doppler-boosted into the coordinate/observer frame using the redshift factor.

## Q21: What are the two integration strategies for post processing images?
**A:** Opacity-based ray casting through grid cells and analytic integration of the transfer equation through integrable models; production codes use the former.

## Q22: How does post processing images determine color?
**A:** By integrating the spectrum at several fiducial frequencies and mapping the log-frequency-integrated intensity to a perceptual color ramp.

## Q23: What role does the optical depth tau play in post processing images?
**A:** tau integrates the absorption along the path; large tau means the flow self-shields, which post processing images must respect to avoid over-bright images.

## Q24: How does post processing images encode a Lorentz boost?
**A:** The emissivity picks up a factor (1/g(1-beta·n))^2-ish from beaming plus the frequency shift; post processing images applies these along the local fluid velocity.

## Q25: Why does synchrotron dominate disk emission in post processing images?
**A:** The field and relativistic electrons radiate efficiently at the observed frequencies; thermal emission contributes where the flow is densest and coolest.

## Q26: What is the invariant form used in post processing images?
**A:** I_nu / nu^3 is invariant along a ray, so post processing images can transfer in any frame by tracking the frequency shift continuously.

## Q27: How do you validate post processing images?
**A:** Reproduce analytic synchrotron spectra, check that a static uniform sphere has constant surface brightness, and compare derived images with published renders.

## Q28: How does post processing images handle scattering?
**A:** Fully including scattering needs Monte Carlo; most pipeline post processing images ignores it for the polarized-total intensity morphology and adds it later.

## Q29: What output does post processing images produce per pixel?
**A:** Total intensity (and optionally Stokes IQUV) per frequency band; post processing images is the last physics stage before tone mapping converts to an image.

## Q30: How do you make post processing images deterministic?
**A:** Run the same snapshot, ray grid, and frequency set twice; bit-identical post processing images means the pipeline is reproducible for science and movies.

## Q31: What do the measured M87-like images imply for post processing images?
**A:** The bright ring and south-side enhancement follow from Doppler boosting of the approaching disk side; post processing images reproduces these signatures from the velocity field.

## Q32: How does post processing images integrate through the grid?
**A:** March through cells with a ray-grid traversal, sampling the fluid state, and update intensity with the segment transfer solution each step.

## Q33: What precision does post processing images need?
**A:** Double precision for the integration of small intensities near the ring; post processing images is the stage where visible artifacts for `dark' and `bright' regions meet.

## Q34: How do you compute the emitted frequency in post processing images?
**A:** The fluid-frame frequency divides by (1+z) where z is the integrated redshift; post processing images sets up spectral bins by emitted frequency in the observer band.

## Q35: What are the simplest usable emission models in post processing images?
**A:** A thermal blackbody-approximation from temperature and density, or synchrotron power laws with gamma-distributed electrons; post processing images starts with the simplest and upgrades.

## Q36: How does post processing images create the visually iconic thin bright ring?
**A:** Near the photon sphere, rays sweep long path lengths through the brightest, most-beamed plasma, so integrated post processing images intensity peaks there.

## Q37: What is the Doppler ratio that drives asymmetry in post processing images?
**A:** The ratio between approaching and receding disk sides, roughly (1+beta cos theta over 1-beta cos theta) powers; post processing images makes one side 3-5x brighter.

## Q38: How is post processing images checked against real observations?
**A:** By comparing ring diameter, asymmetry, and spectrum to EHT measurements - agreement on those is the acceptance test for post processing images.

## Q39: How does post processing images fit the movie pipeline?
**A:** Rendering N frames applies post processing images to each snapshot; post processing images performance (per-ray cost) sets the total render budget for a movie.

## Q40: How does post processing images fit the movie pipeline - justify your answer with a concrete production example.
**A:** Rendering N frames applies post processing images to each snapshot; post processing images performance (per-ray cost) sets the total render budget for a movie. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: How is post processing images checked against real observations - justify your answer with a concrete production example.
**A:** By comparing ring diameter, asymmetry, and spectrum to EHT measurements - agreement on those is the acceptance test for post processing images. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What is the Doppler ratio that drives asymmetry in post processing images - justify your answer with a concrete production example.
**A:** The ratio between approaching and receding disk sides, roughly (1+beta cos theta over 1-beta cos theta) powers; post processing images makes one side 3-5x brighter. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: How does post processing images create the visually iconic thin bright ring - justify your answer with a concrete production example.
**A:** Near the photon sphere, rays sweep long path lengths through the brightest, most-beamed plasma, so integrated post processing images intensity peaks there. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What are the simplest usable emission models in post processing images - justify your answer with a concrete production example.
**A:** A thermal blackbody-approximation from temperature and density, or synchrotron power laws with gamma-distributed electrons; post processing images starts with the simplest and upgrades. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: How do you compute the emitted frequency in post processing images - justify your answer with a concrete production example.
**A:** The fluid-frame frequency divides by (1+z) where z is the integrated redshift; post processing images sets up spectral bins by emitted frequency in the observer band. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: What precision does post processing images need - justify your answer with a concrete production example.
**A:** Double precision for the integration of small intensities near the ring; post processing images is the stage where visible artifacts for `dark' and `bright' regions meet. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: How does post processing images integrate through the grid - justify your answer with a concrete production example.
**A:** March through cells with a ray-grid traversal, sampling the fluid state, and update intensity with the segment transfer solution each step. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: What do the measured M87-like images imply for post processing images - justify your answer with a concrete production example.
**A:** The bright ring and south-side enhancement follow from Doppler boosting of the approaching disk side; post processing images reproduces these signatures from the velocity field. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: How do you make post processing images deterministic - justify your answer with a concrete production example.
**A:** Run the same snapshot, ray grid, and frequency set twice; bit-identical post processing images means the pipeline is reproducible for science and movies. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What output does post processing images produce per pixel - justify your answer with a concrete production example.
**A:** Total intensity (and optionally Stokes IQUV) per frequency band; post processing images is the last physics stage before tone mapping converts to an image. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How does post processing images handle scattering - justify your answer with a concrete production example.
**A:** Fully including scattering needs Monte Carlo; most pipeline post processing images ignores it for the polarized-total intensity morphology and adds it later. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How do you validate post processing images - justify your answer with a concrete production example.
**A:** Reproduce analytic synchrotron spectra, check that a static uniform sphere has constant surface brightness, and compare derived images with published renders. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What is the invariant form used in post processing images - justify your answer with a concrete production example.
**A:** I_nu / nu^3 is invariant along a ray, so post processing images can transfer in any frame by tracking the frequency shift continuously. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: Why does synchrotron dominate disk emission in post processing images - justify your answer with a concrete production example.
**A:** The field and relativistic electrons radiate efficiently at the observed frequencies; thermal emission contributes where the flow is densest and coolest. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: How does post processing images encode a Lorentz boost - justify your answer with a concrete production example.
**A:** The emissivity picks up a factor (1/g(1-beta·n))^2-ish from beaming plus the frequency shift; post processing images applies these along the local fluid velocity. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What role does the optical depth tau play in post processing images - justify your answer with a concrete production example.
**A:** tau integrates the absorption along the path; large tau means the flow self-shields, which post processing images must respect to avoid over-bright images. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How does post processing images determine color - justify your answer with a concrete production example.
**A:** By integrating the spectrum at several fiducial frequencies and mapping the log-frequency-integrated intensity to a perceptual color ramp. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What are the two integration strategies for post processing images - justify your answer with a concrete production example.
**A:** Opacity-based ray casting through grid cells and analytic integration of the transfer equation through integrable models; production codes use the former. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How does post processing images handle moving frames - justify your answer with a concrete production example.
**A:** Emissivity and absorption are defined in the fluid rest frame, then redshifted and Doppler-boosted into the coordinate/observer frame using the redshift factor. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What simplification is common in post processing images for black holes - justify your answer with a concrete production example.
**A:** The optically thin synchrotron-dominated case, where emission is computed per path segment and absorption is often neglected in the first pass. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What is the fundamental equation of post processing images - justify your answer with a concrete production example.
**A:** The radiative transfer equation dI/ds = j - alpha I along the ray; post processing images integrates it including the relativistic invariant I/nu^3. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why is post processing images essential for connecting GRMHD to pixels - justify your answer with a concrete production example.
**A:** Plasma data alone is invisible; post processing images converts density, temperature, and magnetic field into the intensity and color every pixel shows. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What question does post processing images answer for a raytracer - justify your answer with a concrete production example.
**A:** Given the plasma state along a photon path, it computes how much light reaches the observer after emission, absorption, and frequency shifts. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What question does post processing images answer for a raytracer - justify your answer with a concrete production example.
**A:** Given the plasma state along a photon path, it computes how much light reaches the observer after emission, absorption, and frequency shifts. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why is post processing images essential for connecting GRMHD to pixels - justify your answer with a concrete production example.
**A:** Plasma data alone is invisible; post processing images converts density, temperature, and magnetic field into the intensity and color every pixel shows. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What is the fundamental equation of post processing images - justify your answer with a concrete production example.
**A:** The radiative transfer equation dI/ds = j - alpha I along the ray; post processing images integrates it including the relativistic invariant I/nu^3. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What simplification is common in post processing images for black holes - justify your answer with a concrete production example.
**A:** The optically thin synchrotron-dominated case, where emission is computed per path segment and absorption is often neglected in the first pass. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How does post processing images handle moving frames - justify your answer with a concrete production example.
**A:** Emissivity and absorption are defined in the fluid rest frame, then redshifted and Doppler-boosted into the coordinate/observer frame using the redshift factor. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What are the two integration strategies for post processing images - justify your answer with a concrete production example.
**A:** Opacity-based ray casting through grid cells and analytic integration of the transfer equation through integrable models; production codes use the former. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How does post processing images determine color - justify your answer with a concrete production example.
**A:** By integrating the spectrum at several fiducial frequencies and mapping the log-frequency-integrated intensity to a perceptual color ramp. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What role does the optical depth tau play in post processing images - justify your answer with a concrete production example.
**A:** tau integrates the absorption along the path; large tau means the flow self-shields, which post processing images must respect to avoid over-bright images. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: How does post processing images encode a Lorentz boost - justify your answer with a concrete production example.
**A:** The emissivity picks up a factor (1/g(1-beta·n))^2-ish from beaming plus the frequency shift; post processing images applies these along the local fluid velocity. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: Why does synchrotron dominate disk emission in post processing images - justify your answer with a concrete production example.
**A:** The field and relativistic electrons radiate efficiently at the observed frequencies; thermal emission contributes where the flow is densest and coolest. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What is the invariant form used in post processing images - justify your answer with a concrete production example.
**A:** I_nu / nu^3 is invariant along a ray, so post processing images can transfer in any frame by tracking the frequency shift continuously. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How do you validate post processing images - justify your answer with a concrete production example.
**A:** Reproduce analytic synchrotron spectra, check that a static uniform sphere has constant surface brightness, and compare derived images with published renders. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How does post processing images handle scattering - justify your answer with a concrete production example.
**A:** Fully including scattering needs Monte Carlo; most pipeline post processing images ignores it for the polarized-total intensity morphology and adds it later. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What output does post processing images produce per pixel - justify your answer with a concrete production example.
**A:** Total intensity (and optionally Stokes IQUV) per frequency band; post processing images is the last physics stage before tone mapping converts to an image. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: How do you make post processing images deterministic - justify your answer with a concrete production example.
**A:** Run the same snapshot, ray grid, and frequency set twice; bit-identical post processing images means the pipeline is reproducible for science and movies. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What do the measured M87-like images imply for post processing images - justify your answer with a concrete production example.
**A:** The bright ring and south-side enhancement follow from Doppler boosting of the approaching disk side; post processing images reproduces these signatures from the velocity field. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How does post processing images integrate through the grid - justify your answer with a concrete production example.
**A:** March through cells with a ray-grid traversal, sampling the fluid state, and update intensity with the segment transfer solution each step. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: What precision does post processing images need - justify your answer with a concrete production example.
**A:** Double precision for the integration of small intensities near the ring; post processing images is the stage where visible artifacts for `dark' and `bright' regions meet. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: How do you compute the emitted frequency in post processing images - justify your answer with a concrete production example.
**A:** The fluid-frame frequency divides by (1+z) where z is the integrated redshift; post processing images sets up spectral bins by emitted frequency in the observer band. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What are the simplest usable emission models in post processing images - justify your answer with a concrete production example.
**A:** A thermal blackbody-approximation from temperature and density, or synchrotron power laws with gamma-distributed electrons; post processing images starts with the simplest and upgrades. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: How does post processing images create the visually iconic thin bright ring - justify your answer with a concrete production example.
**A:** Near the photon sphere, rays sweep long path lengths through the brightest, most-beamed plasma, so integrated post processing images intensity peaks there. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What is the Doppler ratio that drives asymmetry in post processing images - justify your answer with a concrete production example.
**A:** The ratio between approaching and receding disk sides, roughly (1+beta cos theta over 1-beta cos theta) powers; post processing images makes one side 3-5x brighter. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: How is post processing images checked against real observations - justify your answer with a concrete production example.
**A:** By comparing ring diameter, asymmetry, and spectrum to EHT measurements - agreement on those is the acceptance test for post processing images. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How does post processing images fit the movie pipeline - justify your answer with a concrete production example.
**A:** Rendering N frames applies post processing images to each snapshot; post processing images performance (per-ray cost) sets the total render budget for a movie. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How does post processing images fit the movie pipeline - justify your answer with a concrete production example.
**A:** Rendering N frames applies post processing images to each snapshot; post processing images performance (per-ray cost) sets the total render budget for a movie. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: How is post processing images checked against real observations - justify your answer with a concrete production example.
**A:** By comparing ring diameter, asymmetry, and spectrum to EHT measurements - agreement on those is the acceptance test for post processing images. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What is the Doppler ratio that drives asymmetry in post processing images - justify your answer with a concrete production example.
**A:** The ratio between approaching and receding disk sides, roughly (1+beta cos theta over 1-beta cos theta) powers; post processing images makes one side 3-5x brighter. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: How does post processing images create the visually iconic thin bright ring - justify your answer with a concrete production example.
**A:** Near the photon sphere, rays sweep long path lengths through the brightest, most-beamed plasma, so integrated post processing images intensity peaks there. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What are the simplest usable emission models in post processing images - justify your answer with a concrete production example.
**A:** A thermal blackbody-approximation from temperature and density, or synchrotron power laws with gamma-distributed electrons; post processing images starts with the simplest and upgrades. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: How do you compute the emitted frequency in post processing images - justify your answer with a concrete production example.
**A:** The fluid-frame frequency divides by (1+z) where z is the integrated redshift; post processing images sets up spectral bins by emitted frequency in the observer band. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: What precision does post processing images need - justify your answer with a concrete production example.
**A:** Double precision for the integration of small intensities near the ring; post processing images is the stage where visible artifacts for `dark' and `bright' regions meet. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: How does post processing images integrate through the grid - justify your answer with a concrete production example.
**A:** March through cells with a ray-grid traversal, sampling the fluid state, and update intensity with the segment transfer solution each step. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: What do the measured M87-like images imply for post processing images - justify your answer with a concrete production example.
**A:** The bright ring and south-side enhancement follow from Doppler boosting of the approaching disk side; post processing images reproduces these signatures from the velocity field. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: How do you make post processing images deterministic - justify your answer with a concrete production example.
**A:** Run the same snapshot, ray grid, and frequency set twice; bit-identical post processing images means the pipeline is reproducible for science and movies. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What output does post processing images produce per pixel - justify your answer with a concrete production example.
**A:** Total intensity (and optionally Stokes IQUV) per frequency band; post processing images is the last physics stage before tone mapping converts to an image. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How does post processing images handle scattering - justify your answer with a concrete production example.
**A:** Fully including scattering needs Monte Carlo; most pipeline post processing images ignores it for the polarized-total intensity morphology and adds it later. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How do you validate post processing images - justify your answer with a concrete production example.
**A:** Reproduce analytic synchrotron spectra, check that a static uniform sphere has constant surface brightness, and compare derived images with published renders. A concrete example: consistently applying post processing images in code review and regression tests keeps the whole pipeline trustworthy.
