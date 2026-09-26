# Radiative Transfer — Disk Photon Sources Interview Questions and Answers

## Q1: What are the photon sources in a disk scene?
**A:** The GRMHD gas volume (synchrotron/bremsstrahlung from plasma), possibly the disk surface ('photosphere'), and external background - all folded into j along the ray.

## Q2: How is the disk's emission seeded?
**A:** From the snapshot fields (rho, B, T_e): the emissivity model (e.g., thermal synchrotron with a power-law tail) maps each cell to j at the sampled frequency.

## Q3: What does the photon source include for polarization?
**A:** The synchrotron polarization fraction and angle from the B-field's sky-projected orientation - the initial Stokes vector per quadrature sample.

## Q4: How is the vertical structure accounted for?
**A:** The simulation's actual density stratification is used; the renderer doesn't assume a thin disk - volume emissivity picks up the corona, funnel, and plunging region.

## Q5: What is the difference between photosphere and volume sources?
**A:** A photosphere is a surface model (one hit per pixel); volume sources integrate the whole column - the former is cheaper, the latter physically faithful.

## Q6: How do seed photons get their frequency?
**A:** The observation band plus the local shift sets the emitted frequency; each source's SED is then sampled - consistency across the spectrum is the goal.

## Q7: What is the treatment of foreground vs background?
**A:** Attenuation along the path (alpha) decides whether a far source shines through; thick foreground dims/re-emits - the RTE's built-in ordering.

## Q8: How does the disk's emissivity couple to B?
**A:** Thermal synchrotron j ~ n_e B^(...); the B-map is the brightness driver - high-stress (high B) patches light up, the ring is the field's high-water mark.

## Q9: What is the role of the electron temperature?
**A:** T_e sets the spectrum's slope and the SSA turnover; a Te map from the GRMHD closure (Rbeta or similar) is the essential third ingredient.

## Q10: How do you validate a disk scene source?
**A:** Render one snapshot with a simple emissivity: the total flux and spectral shape must match an independent calculation (or the code's own 1-D column sanity).

## Q11: What is the variability source for movies?
**A:** The GRMHD's turbulent density/magnetic evolution modulates j - the per-frame flicker of the ring is the simulation's physics, not a render artifact.

## Q12: How do discrete cells become smooth emissivity law?
**A:** Interpolation of (rho, B, Te) from the staggered/cell-centered grid into a smooth field (trilinear/Catmull) before computing j - smoothness directly affects image quality.

## Q13: What is the photon-counting view?
**A:** The renderer attributes each pixel's energy to the physical source contributions; diagnostics can split the map by dominate source (disk, corona, funnel).

## Q14: What is the summary?
**A:** Disk photon sources are the GRMHD state rendered into j - density, field, and temperature driving emissivity/polarization; the fidelity of the final image rests on reading them correctly.

## Q15: What question does disk photon sources answer for a raytracer?
**A:** Given the plasma state along a photon path, it computes how much light reaches the observer after emission, absorption, and frequency shifts.

## Q16: Why is disk photon sources essential for connecting GRMHD to pixels?
**A:** Plasma data alone is invisible; disk photon sources converts density, temperature, and magnetic field into the intensity and color every pixel shows.

## Q17: What is the fundamental equation of disk photon sources?
**A:** The radiative transfer equation dI/ds = j - alpha I along the ray; disk photon sources integrates it including the relativistic invariant I/nu^3.

## Q18: What simplification is common in disk photon sources for black holes?
**A:** The optically thin synchrotron-dominated case, where emission is computed per path segment and absorption is often neglected in the first pass.

## Q19: How does disk photon sources handle moving frames?
**A:** Emissivity and absorption are defined in the fluid rest frame, then redshifted and Doppler-boosted into the coordinate/observer frame using the redshift factor.

## Q20: What are the two integration strategies for disk photon sources?
**A:** Opacity-based ray casting through grid cells and analytic integration of the transfer equation through integrable models; production codes use the former.

## Q21: How does disk photon sources determine color?
**A:** By integrating the spectrum at several fiducial frequencies and mapping the log-frequency-integrated intensity to a perceptual color ramp.

## Q22: What role does the optical depth tau play in disk photon sources?
**A:** tau integrates the absorption along the path; large tau means the flow self-shields, which disk photon sources must respect to avoid over-bright images.

## Q23: How does disk photon sources encode a Lorentz boost?
**A:** The emissivity picks up a factor (1/g(1-beta·n))^2-ish from beaming plus the frequency shift; disk photon sources applies these along the local fluid velocity.

## Q24: Why does synchrotron dominate disk emission in disk photon sources?
**A:** The field and relativistic electrons radiate efficiently at the observed frequencies; thermal emission contributes where the flow is densest and coolest.

## Q25: What is the invariant form used in disk photon sources?
**A:** I_nu / nu^3 is invariant along a ray, so disk photon sources can transfer in any frame by tracking the frequency shift continuously.

## Q26: How do you validate disk photon sources?
**A:** Reproduce analytic synchrotron spectra, check that a static uniform sphere has constant surface brightness, and compare derived images with published renders.

## Q27: How does disk photon sources handle scattering?
**A:** Fully including scattering needs Monte Carlo; most pipeline disk photon sources ignores it for the polarized-total intensity morphology and adds it later.

## Q28: What output does disk photon sources produce per pixel?
**A:** Total intensity (and optionally Stokes IQUV) per frequency band; disk photon sources is the last physics stage before tone mapping converts to an image.

## Q29: How do you make disk photon sources deterministic?
**A:** Run the same snapshot, ray grid, and frequency set twice; bit-identical disk photon sources means the pipeline is reproducible for science and movies.

## Q30: What do the measured M87-like images imply for disk photon sources?
**A:** The bright ring and south-side enhancement follow from Doppler boosting of the approaching disk side; disk photon sources reproduces these signatures from the velocity field.

## Q31: How does disk photon sources integrate through the grid?
**A:** March through cells with a ray-grid traversal, sampling the fluid state, and update intensity with the segment transfer solution each step.

## Q32: What precision does disk photon sources need?
**A:** Double precision for the integration of small intensities near the ring; disk photon sources is the stage where visible artifacts for `dark' and `bright' regions meet.

## Q33: How do you compute the emitted frequency in disk photon sources?
**A:** The fluid-frame frequency divides by (1+z) where z is the integrated redshift; disk photon sources sets up spectral bins by emitted frequency in the observer band.

## Q34: What are the simplest usable emission models in disk photon sources?
**A:** A thermal blackbody-approximation from temperature and density, or synchrotron power laws with gamma-distributed electrons; disk photon sources starts with the simplest and upgrades.

## Q35: How does disk photon sources create the visually iconic thin bright ring?
**A:** Near the photon sphere, rays sweep long path lengths through the brightest, most-beamed plasma, so integrated disk photon sources intensity peaks there.

## Q36: What is the Doppler ratio that drives asymmetry in disk photon sources?
**A:** The ratio between approaching and receding disk sides, roughly (1+beta cos theta over 1-beta cos theta) powers; disk photon sources makes one side 3-5x brighter.

## Q37: How is disk photon sources checked against real observations?
**A:** By comparing ring diameter, asymmetry, and spectrum to EHT measurements - agreement on those is the acceptance test for disk photon sources.

## Q38: How does disk photon sources fit the movie pipeline?
**A:** Rendering N frames applies disk photon sources to each snapshot; disk photon sources performance (per-ray cost) sets the total render budget for a movie.

## Q39: How does disk photon sources fit the movie pipeline - justify your answer with a concrete production example.
**A:** Rendering N frames applies disk photon sources to each snapshot; disk photon sources performance (per-ray cost) sets the total render budget for a movie. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q40: How is disk photon sources checked against real observations - justify your answer with a concrete production example.
**A:** By comparing ring diameter, asymmetry, and spectrum to EHT measurements - agreement on those is the acceptance test for disk photon sources. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is the Doppler ratio that drives asymmetry in disk photon sources - justify your answer with a concrete production example.
**A:** The ratio between approaching and receding disk sides, roughly (1+beta cos theta over 1-beta cos theta) powers; disk photon sources makes one side 3-5x brighter. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How does disk photon sources create the visually iconic thin bright ring - justify your answer with a concrete production example.
**A:** Near the photon sphere, rays sweep long path lengths through the brightest, most-beamed plasma, so integrated disk photon sources intensity peaks there. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What are the simplest usable emission models in disk photon sources - justify your answer with a concrete production example.
**A:** A thermal blackbody-approximation from temperature and density, or synchrotron power laws with gamma-distributed electrons; disk photon sources starts with the simplest and upgrades. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How do you compute the emitted frequency in disk photon sources - justify your answer with a concrete production example.
**A:** The fluid-frame frequency divides by (1+z) where z is the integrated redshift; disk photon sources sets up spectral bins by emitted frequency in the observer band. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What precision does disk photon sources need - justify your answer with a concrete production example.
**A:** Double precision for the integration of small intensities near the ring; disk photon sources is the stage where visible artifacts for `dark' and `bright' regions meet. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does disk photon sources integrate through the grid - justify your answer with a concrete production example.
**A:** March through cells with a ray-grid traversal, sampling the fluid state, and update intensity with the segment transfer solution each step. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What do the measured M87-like images imply for disk photon sources - justify your answer with a concrete production example.
**A:** The bright ring and south-side enhancement follow from Doppler boosting of the approaching disk side; disk photon sources reproduces these signatures from the velocity field. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How do you make disk photon sources deterministic - justify your answer with a concrete production example.
**A:** Run the same snapshot, ray grid, and frequency set twice; bit-identical disk photon sources means the pipeline is reproducible for science and movies. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What output does disk photon sources produce per pixel - justify your answer with a concrete production example.
**A:** Total intensity (and optionally Stokes IQUV) per frequency band; disk photon sources is the last physics stage before tone mapping converts to an image. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How does disk photon sources handle scattering - justify your answer with a concrete production example.
**A:** Fully including scattering needs Monte Carlo; most pipeline disk photon sources ignores it for the polarized-total intensity morphology and adds it later. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How do you validate disk photon sources - justify your answer with a concrete production example.
**A:** Reproduce analytic synchrotron spectra, check that a static uniform sphere has constant surface brightness, and compare derived images with published renders. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: What is the invariant form used in disk photon sources - justify your answer with a concrete production example.
**A:** I_nu / nu^3 is invariant along a ray, so disk photon sources can transfer in any frame by tracking the frequency shift continuously. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: Why does synchrotron dominate disk emission in disk photon sources - justify your answer with a concrete production example.
**A:** The field and relativistic electrons radiate efficiently at the observed frequencies; thermal emission contributes where the flow is densest and coolest. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does disk photon sources encode a Lorentz boost - justify your answer with a concrete production example.
**A:** The emissivity picks up a factor (1/g(1-beta·n))^2-ish from beaming plus the frequency shift; disk photon sources applies these along the local fluid velocity. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What role does the optical depth tau play in disk photon sources - justify your answer with a concrete production example.
**A:** tau integrates the absorption along the path; large tau means the flow self-shields, which disk photon sources must respect to avoid over-bright images. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: How does disk photon sources determine color - justify your answer with a concrete production example.
**A:** By integrating the spectrum at several fiducial frequencies and mapping the log-frequency-integrated intensity to a perceptual color ramp. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: What are the two integration strategies for disk photon sources - justify your answer with a concrete production example.
**A:** Opacity-based ray casting through grid cells and analytic integration of the transfer equation through integrable models; production codes use the former. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: How does disk photon sources handle moving frames - justify your answer with a concrete production example.
**A:** Emissivity and absorption are defined in the fluid rest frame, then redshifted and Doppler-boosted into the coordinate/observer frame using the redshift factor. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: What simplification is common in disk photon sources for black holes - justify your answer with a concrete production example.
**A:** The optically thin synchrotron-dominated case, where emission is computed per path segment and absorption is often neglected in the first pass. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What is the fundamental equation of disk photon sources - justify your answer with a concrete production example.
**A:** The radiative transfer equation dI/ds = j - alpha I along the ray; disk photon sources integrates it including the relativistic invariant I/nu^3. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: Why is disk photon sources essential for connecting GRMHD to pixels - justify your answer with a concrete production example.
**A:** Plasma data alone is invisible; disk photon sources converts density, temperature, and magnetic field into the intensity and color every pixel shows. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: What question does disk photon sources answer for a raytracer - justify your answer with a concrete production example.
**A:** Given the plasma state along a photon path, it computes how much light reaches the observer after emission, absorption, and frequency shifts. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What question does disk photon sources answer for a raytracer - justify your answer with a concrete production example.
**A:** Given the plasma state along a photon path, it computes how much light reaches the observer after emission, absorption, and frequency shifts. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: Why is disk photon sources essential for connecting GRMHD to pixels - justify your answer with a concrete production example.
**A:** Plasma data alone is invisible; disk photon sources converts density, temperature, and magnetic field into the intensity and color every pixel shows. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: What is the fundamental equation of disk photon sources - justify your answer with a concrete production example.
**A:** The radiative transfer equation dI/ds = j - alpha I along the ray; disk photon sources integrates it including the relativistic invariant I/nu^3. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What simplification is common in disk photon sources for black holes - justify your answer with a concrete production example.
**A:** The optically thin synchrotron-dominated case, where emission is computed per path segment and absorption is often neglected in the first pass. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How does disk photon sources handle moving frames - justify your answer with a concrete production example.
**A:** Emissivity and absorption are defined in the fluid rest frame, then redshifted and Doppler-boosted into the coordinate/observer frame using the redshift factor. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What are the two integration strategies for disk photon sources - justify your answer with a concrete production example.
**A:** Opacity-based ray casting through grid cells and analytic integration of the transfer equation through integrable models; production codes use the former. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: How does disk photon sources determine color - justify your answer with a concrete production example.
**A:** By integrating the spectrum at several fiducial frequencies and mapping the log-frequency-integrated intensity to a perceptual color ramp. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: What role does the optical depth tau play in disk photon sources - justify your answer with a concrete production example.
**A:** tau integrates the absorption along the path; large tau means the flow self-shields, which disk photon sources must respect to avoid over-bright images. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: How does disk photon sources encode a Lorentz boost - justify your answer with a concrete production example.
**A:** The emissivity picks up a factor (1/g(1-beta·n))^2-ish from beaming plus the frequency shift; disk photon sources applies these along the local fluid velocity. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: Why does synchrotron dominate disk emission in disk photon sources - justify your answer with a concrete production example.
**A:** The field and relativistic electrons radiate efficiently at the observed frequencies; thermal emission contributes where the flow is densest and coolest. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: What is the invariant form used in disk photon sources - justify your answer with a concrete production example.
**A:** I_nu / nu^3 is invariant along a ray, so disk photon sources can transfer in any frame by tracking the frequency shift continuously. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: How do you validate disk photon sources - justify your answer with a concrete production example.
**A:** Reproduce analytic synchrotron spectra, check that a static uniform sphere has constant surface brightness, and compare derived images with published renders. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How does disk photon sources handle scattering - justify your answer with a concrete production example.
**A:** Fully including scattering needs Monte Carlo; most pipeline disk photon sources ignores it for the polarized-total intensity morphology and adds it later. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What output does disk photon sources produce per pixel - justify your answer with a concrete production example.
**A:** Total intensity (and optionally Stokes IQUV) per frequency band; disk photon sources is the last physics stage before tone mapping converts to an image. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: How do you make disk photon sources deterministic - justify your answer with a concrete production example.
**A:** Run the same snapshot, ray grid, and frequency set twice; bit-identical disk photon sources means the pipeline is reproducible for science and movies. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What do the measured M87-like images imply for disk photon sources - justify your answer with a concrete production example.
**A:** The bright ring and south-side enhancement follow from Doppler boosting of the approaching disk side; disk photon sources reproduces these signatures from the velocity field. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How does disk photon sources integrate through the grid - justify your answer with a concrete production example.
**A:** March through cells with a ray-grid traversal, sampling the fluid state, and update intensity with the segment transfer solution each step. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What precision does disk photon sources need - justify your answer with a concrete production example.
**A:** Double precision for the integration of small intensities near the ring; disk photon sources is the stage where visible artifacts for `dark' and `bright' regions meet. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How do you compute the emitted frequency in disk photon sources - justify your answer with a concrete production example.
**A:** The fluid-frame frequency divides by (1+z) where z is the integrated redshift; disk photon sources sets up spectral bins by emitted frequency in the observer band. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What are the simplest usable emission models in disk photon sources - justify your answer with a concrete production example.
**A:** A thermal blackbody-approximation from temperature and density, or synchrotron power laws with gamma-distributed electrons; disk photon sources starts with the simplest and upgrades. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How does disk photon sources create the visually iconic thin bright ring - justify your answer with a concrete production example.
**A:** Near the photon sphere, rays sweep long path lengths through the brightest, most-beamed plasma, so integrated disk photon sources intensity peaks there. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What is the Doppler ratio that drives asymmetry in disk photon sources - justify your answer with a concrete production example.
**A:** The ratio between approaching and receding disk sides, roughly (1+beta cos theta over 1-beta cos theta) powers; disk photon sources makes one side 3-5x brighter. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How is disk photon sources checked against real observations - justify your answer with a concrete production example.
**A:** By comparing ring diameter, asymmetry, and spectrum to EHT measurements - agreement on those is the acceptance test for disk photon sources. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: How does disk photon sources fit the movie pipeline - justify your answer with a concrete production example.
**A:** Rendering N frames applies disk photon sources to each snapshot; disk photon sources performance (per-ray cost) sets the total render budget for a movie. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How does disk photon sources fit the movie pipeline - justify your answer with a concrete production example.
**A:** Rendering N frames applies disk photon sources to each snapshot; disk photon sources performance (per-ray cost) sets the total render budget for a movie. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How is disk photon sources checked against real observations - justify your answer with a concrete production example.
**A:** By comparing ring diameter, asymmetry, and spectrum to EHT measurements - agreement on those is the acceptance test for disk photon sources. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is the Doppler ratio that drives asymmetry in disk photon sources - justify your answer with a concrete production example.
**A:** The ratio between approaching and receding disk sides, roughly (1+beta cos theta over 1-beta cos theta) powers; disk photon sources makes one side 3-5x brighter. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How does disk photon sources create the visually iconic thin bright ring - justify your answer with a concrete production example.
**A:** Near the photon sphere, rays sweep long path lengths through the brightest, most-beamed plasma, so integrated disk photon sources intensity peaks there. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What are the simplest usable emission models in disk photon sources - justify your answer with a concrete production example.
**A:** A thermal blackbody-approximation from temperature and density, or synchrotron power laws with gamma-distributed electrons; disk photon sources starts with the simplest and upgrades. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How do you compute the emitted frequency in disk photon sources - justify your answer with a concrete production example.
**A:** The fluid-frame frequency divides by (1+z) where z is the integrated redshift; disk photon sources sets up spectral bins by emitted frequency in the observer band. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What precision does disk photon sources need - justify your answer with a concrete production example.
**A:** Double precision for the integration of small intensities near the ring; disk photon sources is the stage where visible artifacts for `dark' and `bright' regions meet. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does disk photon sources integrate through the grid - justify your answer with a concrete production example.
**A:** March through cells with a ray-grid traversal, sampling the fluid state, and update intensity with the segment transfer solution each step. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What do the measured M87-like images imply for disk photon sources - justify your answer with a concrete production example.
**A:** The bright ring and south-side enhancement follow from Doppler boosting of the approaching disk side; disk photon sources reproduces these signatures from the velocity field. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How do you make disk photon sources deterministic - justify your answer with a concrete production example.
**A:** Run the same snapshot, ray grid, and frequency set twice; bit-identical disk photon sources means the pipeline is reproducible for science and movies. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What output does disk photon sources produce per pixel - justify your answer with a concrete production example.
**A:** Total intensity (and optionally Stokes IQUV) per frequency band; disk photon sources is the last physics stage before tone mapping converts to an image. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How does disk photon sources handle scattering - justify your answer with a concrete production example.
**A:** Fully including scattering needs Monte Carlo; most pipeline disk photon sources ignores it for the polarized-total intensity morphology and adds it later. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How do you validate disk photon sources - justify your answer with a concrete production example.
**A:** Reproduce analytic synchrotron spectra, check that a static uniform sphere has constant surface brightness, and compare derived images with published renders. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: What is the invariant form used in disk photon sources - justify your answer with a concrete production example.
**A:** I_nu / nu^3 is invariant along a ray, so disk photon sources can transfer in any frame by tracking the frequency shift continuously. A concrete example: consistently applying disk photon sources in code review and regression tests keeps the whole pipeline trustworthy.
