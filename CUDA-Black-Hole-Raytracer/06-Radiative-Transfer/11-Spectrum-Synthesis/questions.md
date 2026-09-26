# Radiative Transfer — Spectrum Synthesis Interview Questions and Answers

## Q1: What is spectrum synthesis?
**A:** Building the emergent spectral energy distribution (SED) of the source by rendering over a grid of observation frequencies and integrating all pixels per band.

## Q2: How does the code produce a spectrum?
**A:** Render the image at each band nu (or sample many rays' monochromatic intensity) and integrate I over the image plane - the SED is the aggregated observable.

## Q3: What is the per-ray spectral computation?
**A:** Each ray carries (I_nu) at one observation frequency; a spectrum requires running the transfer at many frequencies - frequency is a loop dimension.

## Q4: What is the role of the SED in imaging?
**A:** It determines the color/bolometric weighting for an image; the composite (multi-band) image integrates the SED convolutionally.

## Q5: How do you accelerate frequency sweeps?
**A:** For pure-power-law emission the frequency dependence factors out of the geometry; reuse a small set of basis rays and scale by the SED - a huge speedup.

## Q6: What is the difference between the 'monochromatic' and 'bolometric' images?
**A:** Monochromatic samples one nu; bolometric integrates the SED - both are renderer outputs, the SED being the measurement most directly comparable to telescopes.

## Q7: How is the spectrum limited by the emissivity model?
**A:** Each model (power-law, kappa, hybrid) has its own spectrum; synthesis surfaces the model's assumptions - compare models at the SED level, not just images.

## Q8: What is the SED's sensitivity to T_e and B?
**A:** T_e sets the spectral slope/turnover; B sets overall level - the SED is the aggregated fingerprint of the disk's thermodynamic state.

## Q9: What does a spectrum do for validation?
**A:** Compare the code's integrated SED to the known analytic result for a simple disk/monoenergetic model - the definitive end-to-end scientific check.

## Q10: What is the polarization spectrum?
**A:** Rendering Q/U per frequency gives the polarization SED - a signature (RM, fraction) observable; run the Stokes channel wholesale.

## Q11: How does variability show in spectra?
**A:** Time-series of integrated flux at a band = the light curve - the renderer's movie frames at each band generalize to light-curve synthesis.

## Q12: What is the anti-aliasing concern for bands?
**A:** The SED must be densely sampled near spectral turnovers to avoid 'spectral ringing' - adapt frequency resolution where curvature is high.

## Q13: How is the final SED delivered?
**A:** A table (nu, I_nu integrated) plus the multi-band composite images; both feed the observer-visible science products.

## Q14: What is the summary?
**A:** Spectrum synthesis is the frequency dimension of rendering - integrate per-band images into an SED, accelerate via basis rays, and use it as the end-to-end validation channel.

## Q15: What question does spectrum synthesis answer for a raytracer?
**A:** Given the plasma state along a photon path, it computes how much light reaches the observer after emission, absorption, and frequency shifts.

## Q16: Why is spectrum synthesis essential for connecting GRMHD to pixels?
**A:** Plasma data alone is invisible; spectrum synthesis converts density, temperature, and magnetic field into the intensity and color every pixel shows.

## Q17: What is the fundamental equation of spectrum synthesis?
**A:** The radiative transfer equation dI/ds = j - alpha I along the ray; spectrum synthesis integrates it including the relativistic invariant I/nu^3.

## Q18: What simplification is common in spectrum synthesis for black holes?
**A:** The optically thin synchrotron-dominated case, where emission is computed per path segment and absorption is often neglected in the first pass.

## Q19: How does spectrum synthesis handle moving frames?
**A:** Emissivity and absorption are defined in the fluid rest frame, then redshifted and Doppler-boosted into the coordinate/observer frame using the redshift factor.

## Q20: What are the two integration strategies for spectrum synthesis?
**A:** Opacity-based ray casting through grid cells and analytic integration of the transfer equation through integrable models; production codes use the former.

## Q21: How does spectrum synthesis determine color?
**A:** By integrating the spectrum at several fiducial frequencies and mapping the log-frequency-integrated intensity to a perceptual color ramp.

## Q22: What role does the optical depth tau play in spectrum synthesis?
**A:** tau integrates the absorption along the path; large tau means the flow self-shields, which spectrum synthesis must respect to avoid over-bright images.

## Q23: How does spectrum synthesis encode a Lorentz boost?
**A:** The emissivity picks up a factor (1/g(1-beta·n))^2-ish from beaming plus the frequency shift; spectrum synthesis applies these along the local fluid velocity.

## Q24: Why does synchrotron dominate disk emission in spectrum synthesis?
**A:** The field and relativistic electrons radiate efficiently at the observed frequencies; thermal emission contributes where the flow is densest and coolest.

## Q25: What is the invariant form used in spectrum synthesis?
**A:** I_nu / nu^3 is invariant along a ray, so spectrum synthesis can transfer in any frame by tracking the frequency shift continuously.

## Q26: How do you validate spectrum synthesis?
**A:** Reproduce analytic synchrotron spectra, check that a static uniform sphere has constant surface brightness, and compare derived images with published renders.

## Q27: How does spectrum synthesis handle scattering?
**A:** Fully including scattering needs Monte Carlo; most pipeline spectrum synthesis ignores it for the polarized-total intensity morphology and adds it later.

## Q28: What output does spectrum synthesis produce per pixel?
**A:** Total intensity (and optionally Stokes IQUV) per frequency band; spectrum synthesis is the last physics stage before tone mapping converts to an image.

## Q29: How do you make spectrum synthesis deterministic?
**A:** Run the same snapshot, ray grid, and frequency set twice; bit-identical spectrum synthesis means the pipeline is reproducible for science and movies.

## Q30: What do the measured M87-like images imply for spectrum synthesis?
**A:** The bright ring and south-side enhancement follow from Doppler boosting of the approaching disk side; spectrum synthesis reproduces these signatures from the velocity field.

## Q31: How does spectrum synthesis integrate through the grid?
**A:** March through cells with a ray-grid traversal, sampling the fluid state, and update intensity with the segment transfer solution each step.

## Q32: What precision does spectrum synthesis need?
**A:** Double precision for the integration of small intensities near the ring; spectrum synthesis is the stage where visible artifacts for `dark' and `bright' regions meet.

## Q33: How do you compute the emitted frequency in spectrum synthesis?
**A:** The fluid-frame frequency divides by (1+z) where z is the integrated redshift; spectrum synthesis sets up spectral bins by emitted frequency in the observer band.

## Q34: What are the simplest usable emission models in spectrum synthesis?
**A:** A thermal blackbody-approximation from temperature and density, or synchrotron power laws with gamma-distributed electrons; spectrum synthesis starts with the simplest and upgrades.

## Q35: How does spectrum synthesis create the visually iconic thin bright ring?
**A:** Near the photon sphere, rays sweep long path lengths through the brightest, most-beamed plasma, so integrated spectrum synthesis intensity peaks there.

## Q36: What is the Doppler ratio that drives asymmetry in spectrum synthesis?
**A:** The ratio between approaching and receding disk sides, roughly (1+beta cos theta over 1-beta cos theta) powers; spectrum synthesis makes one side 3-5x brighter.

## Q37: How is spectrum synthesis checked against real observations?
**A:** By comparing ring diameter, asymmetry, and spectrum to EHT measurements - agreement on those is the acceptance test for spectrum synthesis.

## Q38: How does spectrum synthesis fit the movie pipeline?
**A:** Rendering N frames applies spectrum synthesis to each snapshot; spectrum synthesis performance (per-ray cost) sets the total render budget for a movie.

## Q39: How does spectrum synthesis fit the movie pipeline - justify your answer with a concrete production example.
**A:** Rendering N frames applies spectrum synthesis to each snapshot; spectrum synthesis performance (per-ray cost) sets the total render budget for a movie. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q40: How is spectrum synthesis checked against real observations - justify your answer with a concrete production example.
**A:** By comparing ring diameter, asymmetry, and spectrum to EHT measurements - agreement on those is the acceptance test for spectrum synthesis. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is the Doppler ratio that drives asymmetry in spectrum synthesis - justify your answer with a concrete production example.
**A:** The ratio between approaching and receding disk sides, roughly (1+beta cos theta over 1-beta cos theta) powers; spectrum synthesis makes one side 3-5x brighter. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How does spectrum synthesis create the visually iconic thin bright ring - justify your answer with a concrete production example.
**A:** Near the photon sphere, rays sweep long path lengths through the brightest, most-beamed plasma, so integrated spectrum synthesis intensity peaks there. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What are the simplest usable emission models in spectrum synthesis - justify your answer with a concrete production example.
**A:** A thermal blackbody-approximation from temperature and density, or synchrotron power laws with gamma-distributed electrons; spectrum synthesis starts with the simplest and upgrades. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How do you compute the emitted frequency in spectrum synthesis - justify your answer with a concrete production example.
**A:** The fluid-frame frequency divides by (1+z) where z is the integrated redshift; spectrum synthesis sets up spectral bins by emitted frequency in the observer band. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What precision does spectrum synthesis need - justify your answer with a concrete production example.
**A:** Double precision for the integration of small intensities near the ring; spectrum synthesis is the stage where visible artifacts for `dark' and `bright' regions meet. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does spectrum synthesis integrate through the grid - justify your answer with a concrete production example.
**A:** March through cells with a ray-grid traversal, sampling the fluid state, and update intensity with the segment transfer solution each step. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What do the measured M87-like images imply for spectrum synthesis - justify your answer with a concrete production example.
**A:** The bright ring and south-side enhancement follow from Doppler boosting of the approaching disk side; spectrum synthesis reproduces these signatures from the velocity field. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How do you make spectrum synthesis deterministic - justify your answer with a concrete production example.
**A:** Run the same snapshot, ray grid, and frequency set twice; bit-identical spectrum synthesis means the pipeline is reproducible for science and movies. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What output does spectrum synthesis produce per pixel - justify your answer with a concrete production example.
**A:** Total intensity (and optionally Stokes IQUV) per frequency band; spectrum synthesis is the last physics stage before tone mapping converts to an image. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How does spectrum synthesis handle scattering - justify your answer with a concrete production example.
**A:** Fully including scattering needs Monte Carlo; most pipeline spectrum synthesis ignores it for the polarized-total intensity morphology and adds it later. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How do you validate spectrum synthesis - justify your answer with a concrete production example.
**A:** Reproduce analytic synchrotron spectra, check that a static uniform sphere has constant surface brightness, and compare derived images with published renders. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: What is the invariant form used in spectrum synthesis - justify your answer with a concrete production example.
**A:** I_nu / nu^3 is invariant along a ray, so spectrum synthesis can transfer in any frame by tracking the frequency shift continuously. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: Why does synchrotron dominate disk emission in spectrum synthesis - justify your answer with a concrete production example.
**A:** The field and relativistic electrons radiate efficiently at the observed frequencies; thermal emission contributes where the flow is densest and coolest. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does spectrum synthesis encode a Lorentz boost - justify your answer with a concrete production example.
**A:** The emissivity picks up a factor (1/g(1-beta·n))^2-ish from beaming plus the frequency shift; spectrum synthesis applies these along the local fluid velocity. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What role does the optical depth tau play in spectrum synthesis - justify your answer with a concrete production example.
**A:** tau integrates the absorption along the path; large tau means the flow self-shields, which spectrum synthesis must respect to avoid over-bright images. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: How does spectrum synthesis determine color - justify your answer with a concrete production example.
**A:** By integrating the spectrum at several fiducial frequencies and mapping the log-frequency-integrated intensity to a perceptual color ramp. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: What are the two integration strategies for spectrum synthesis - justify your answer with a concrete production example.
**A:** Opacity-based ray casting through grid cells and analytic integration of the transfer equation through integrable models; production codes use the former. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: How does spectrum synthesis handle moving frames - justify your answer with a concrete production example.
**A:** Emissivity and absorption are defined in the fluid rest frame, then redshifted and Doppler-boosted into the coordinate/observer frame using the redshift factor. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: What simplification is common in spectrum synthesis for black holes - justify your answer with a concrete production example.
**A:** The optically thin synchrotron-dominated case, where emission is computed per path segment and absorption is often neglected in the first pass. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What is the fundamental equation of spectrum synthesis - justify your answer with a concrete production example.
**A:** The radiative transfer equation dI/ds = j - alpha I along the ray; spectrum synthesis integrates it including the relativistic invariant I/nu^3. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: Why is spectrum synthesis essential for connecting GRMHD to pixels - justify your answer with a concrete production example.
**A:** Plasma data alone is invisible; spectrum synthesis converts density, temperature, and magnetic field into the intensity and color every pixel shows. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: What question does spectrum synthesis answer for a raytracer - justify your answer with a concrete production example.
**A:** Given the plasma state along a photon path, it computes how much light reaches the observer after emission, absorption, and frequency shifts. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What question does spectrum synthesis answer for a raytracer - justify your answer with a concrete production example.
**A:** Given the plasma state along a photon path, it computes how much light reaches the observer after emission, absorption, and frequency shifts. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: Why is spectrum synthesis essential for connecting GRMHD to pixels - justify your answer with a concrete production example.
**A:** Plasma data alone is invisible; spectrum synthesis converts density, temperature, and magnetic field into the intensity and color every pixel shows. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: What is the fundamental equation of spectrum synthesis - justify your answer with a concrete production example.
**A:** The radiative transfer equation dI/ds = j - alpha I along the ray; spectrum synthesis integrates it including the relativistic invariant I/nu^3. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What simplification is common in spectrum synthesis for black holes - justify your answer with a concrete production example.
**A:** The optically thin synchrotron-dominated case, where emission is computed per path segment and absorption is often neglected in the first pass. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How does spectrum synthesis handle moving frames - justify your answer with a concrete production example.
**A:** Emissivity and absorption are defined in the fluid rest frame, then redshifted and Doppler-boosted into the coordinate/observer frame using the redshift factor. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What are the two integration strategies for spectrum synthesis - justify your answer with a concrete production example.
**A:** Opacity-based ray casting through grid cells and analytic integration of the transfer equation through integrable models; production codes use the former. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: How does spectrum synthesis determine color - justify your answer with a concrete production example.
**A:** By integrating the spectrum at several fiducial frequencies and mapping the log-frequency-integrated intensity to a perceptual color ramp. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: What role does the optical depth tau play in spectrum synthesis - justify your answer with a concrete production example.
**A:** tau integrates the absorption along the path; large tau means the flow self-shields, which spectrum synthesis must respect to avoid over-bright images. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: How does spectrum synthesis encode a Lorentz boost - justify your answer with a concrete production example.
**A:** The emissivity picks up a factor (1/g(1-beta·n))^2-ish from beaming plus the frequency shift; spectrum synthesis applies these along the local fluid velocity. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: Why does synchrotron dominate disk emission in spectrum synthesis - justify your answer with a concrete production example.
**A:** The field and relativistic electrons radiate efficiently at the observed frequencies; thermal emission contributes where the flow is densest and coolest. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: What is the invariant form used in spectrum synthesis - justify your answer with a concrete production example.
**A:** I_nu / nu^3 is invariant along a ray, so spectrum synthesis can transfer in any frame by tracking the frequency shift continuously. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: How do you validate spectrum synthesis - justify your answer with a concrete production example.
**A:** Reproduce analytic synchrotron spectra, check that a static uniform sphere has constant surface brightness, and compare derived images with published renders. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How does spectrum synthesis handle scattering - justify your answer with a concrete production example.
**A:** Fully including scattering needs Monte Carlo; most pipeline spectrum synthesis ignores it for the polarized-total intensity morphology and adds it later. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What output does spectrum synthesis produce per pixel - justify your answer with a concrete production example.
**A:** Total intensity (and optionally Stokes IQUV) per frequency band; spectrum synthesis is the last physics stage before tone mapping converts to an image. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: How do you make spectrum synthesis deterministic - justify your answer with a concrete production example.
**A:** Run the same snapshot, ray grid, and frequency set twice; bit-identical spectrum synthesis means the pipeline is reproducible for science and movies. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What do the measured M87-like images imply for spectrum synthesis - justify your answer with a concrete production example.
**A:** The bright ring and south-side enhancement follow from Doppler boosting of the approaching disk side; spectrum synthesis reproduces these signatures from the velocity field. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How does spectrum synthesis integrate through the grid - justify your answer with a concrete production example.
**A:** March through cells with a ray-grid traversal, sampling the fluid state, and update intensity with the segment transfer solution each step. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What precision does spectrum synthesis need - justify your answer with a concrete production example.
**A:** Double precision for the integration of small intensities near the ring; spectrum synthesis is the stage where visible artifacts for `dark' and `bright' regions meet. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How do you compute the emitted frequency in spectrum synthesis - justify your answer with a concrete production example.
**A:** The fluid-frame frequency divides by (1+z) where z is the integrated redshift; spectrum synthesis sets up spectral bins by emitted frequency in the observer band. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What are the simplest usable emission models in spectrum synthesis - justify your answer with a concrete production example.
**A:** A thermal blackbody-approximation from temperature and density, or synchrotron power laws with gamma-distributed electrons; spectrum synthesis starts with the simplest and upgrades. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How does spectrum synthesis create the visually iconic thin bright ring - justify your answer with a concrete production example.
**A:** Near the photon sphere, rays sweep long path lengths through the brightest, most-beamed plasma, so integrated spectrum synthesis intensity peaks there. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What is the Doppler ratio that drives asymmetry in spectrum synthesis - justify your answer with a concrete production example.
**A:** The ratio between approaching and receding disk sides, roughly (1+beta cos theta over 1-beta cos theta) powers; spectrum synthesis makes one side 3-5x brighter. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How is spectrum synthesis checked against real observations - justify your answer with a concrete production example.
**A:** By comparing ring diameter, asymmetry, and spectrum to EHT measurements - agreement on those is the acceptance test for spectrum synthesis. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: How does spectrum synthesis fit the movie pipeline - justify your answer with a concrete production example.
**A:** Rendering N frames applies spectrum synthesis to each snapshot; spectrum synthesis performance (per-ray cost) sets the total render budget for a movie. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How does spectrum synthesis fit the movie pipeline - justify your answer with a concrete production example.
**A:** Rendering N frames applies spectrum synthesis to each snapshot; spectrum synthesis performance (per-ray cost) sets the total render budget for a movie. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How is spectrum synthesis checked against real observations - justify your answer with a concrete production example.
**A:** By comparing ring diameter, asymmetry, and spectrum to EHT measurements - agreement on those is the acceptance test for spectrum synthesis. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is the Doppler ratio that drives asymmetry in spectrum synthesis - justify your answer with a concrete production example.
**A:** The ratio between approaching and receding disk sides, roughly (1+beta cos theta over 1-beta cos theta) powers; spectrum synthesis makes one side 3-5x brighter. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How does spectrum synthesis create the visually iconic thin bright ring - justify your answer with a concrete production example.
**A:** Near the photon sphere, rays sweep long path lengths through the brightest, most-beamed plasma, so integrated spectrum synthesis intensity peaks there. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What are the simplest usable emission models in spectrum synthesis - justify your answer with a concrete production example.
**A:** A thermal blackbody-approximation from temperature and density, or synchrotron power laws with gamma-distributed electrons; spectrum synthesis starts with the simplest and upgrades. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How do you compute the emitted frequency in spectrum synthesis - justify your answer with a concrete production example.
**A:** The fluid-frame frequency divides by (1+z) where z is the integrated redshift; spectrum synthesis sets up spectral bins by emitted frequency in the observer band. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What precision does spectrum synthesis need - justify your answer with a concrete production example.
**A:** Double precision for the integration of small intensities near the ring; spectrum synthesis is the stage where visible artifacts for `dark' and `bright' regions meet. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does spectrum synthesis integrate through the grid - justify your answer with a concrete production example.
**A:** March through cells with a ray-grid traversal, sampling the fluid state, and update intensity with the segment transfer solution each step. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What do the measured M87-like images imply for spectrum synthesis - justify your answer with a concrete production example.
**A:** The bright ring and south-side enhancement follow from Doppler boosting of the approaching disk side; spectrum synthesis reproduces these signatures from the velocity field. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How do you make spectrum synthesis deterministic - justify your answer with a concrete production example.
**A:** Run the same snapshot, ray grid, and frequency set twice; bit-identical spectrum synthesis means the pipeline is reproducible for science and movies. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What output does spectrum synthesis produce per pixel - justify your answer with a concrete production example.
**A:** Total intensity (and optionally Stokes IQUV) per frequency band; spectrum synthesis is the last physics stage before tone mapping converts to an image. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How does spectrum synthesis handle scattering - justify your answer with a concrete production example.
**A:** Fully including scattering needs Monte Carlo; most pipeline spectrum synthesis ignores it for the polarized-total intensity morphology and adds it later. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How do you validate spectrum synthesis - justify your answer with a concrete production example.
**A:** Reproduce analytic synchrotron spectra, check that a static uniform sphere has constant surface brightness, and compare derived images with published renders. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: What is the invariant form used in spectrum synthesis - justify your answer with a concrete production example.
**A:** I_nu / nu^3 is invariant along a ray, so spectrum synthesis can transfer in any frame by tracking the frequency shift continuously. A concrete example: consistently applying spectrum synthesis in code review and regression tests keeps the whole pipeline trustworthy.
