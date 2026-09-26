# Radiative Transfer — Lorentz Frequency Shift Interview Questions and Answers

## Q1: What is the Lorentz frequency shift?
**A:** The relation between emitted and observed photon frequencies for a moving source: nu_obs = nu_emit * delta, with delta the Doppler factor of the emitter's 4-velocity frame.

## Q2: What is the standard form?
**A:** delta = 1/(gamma (1 - beta mu)) where beta is the emitter's 3-speed and mu = cos of the angle between its velocity and the photon direction in the emitter frame.

## Q3: How does it differ from gravitational shift?
**A:** The Doppler shift comes from the emitter's motion (p.u_emit); the gravitational shift comes from the g_00 between points; total z combines them multiplicatively.

## Q4: How does the code compute shifts?
**A:** Per quadrature point: keep p_mu and the fluid 4-velocity; the ratio p.u_obs / p.u_emit gives the full factor, no separate Doppler/gravity split needed.

## Q5: What is the sign convention?
**A:** A receding (or static-with-gravity) emitter shifts to nu_emit < nu_obs (redshift, z>0); an approaching emitter blueshifts (z<0) - sign of delta tracks.

## Q6: How does the shift affect emissivity evaluation?
**A:** The rest-frame emissivity is sampled at nu_emit = nu_obs/delta; then the I_nu transfer flows with the delta^2 power - the code must apply both consistently.

## Q7: What is the combination with the RTE?
**A:** The formal solution over a path evaluates j and alpha at the REDSHIFTED local frequency at each step - the frequency tracking rides along the geodesic.

## Q8: What does shift do to band images?
**A:** At fixed observer band, a blueshifted emitter is seen at higher rest-frame nu (different spectral slope); colors and flux both change.

## Q9: What validation checks the shift?
**A:** Known emitter: analytic beta/mu reproduce the classical Doppler formula; static emitter at r reproduces sqrt(1-2M/r) - both to high precision.

## Q10: What is the frame bookkeeping rule?
**A:** Store p_mu; at each node compute u^mu from the fluid and b^mu; all dot products in the SAME (mostly - ) signature - one helper function, no ad-hoc algebra.

## Q11: How does the shift interact with limb beaming?
**A:** Same factor drives both: the direction projected onto u gives hu the Doppler - the bright approaching limb and its bluish color are the same phenomenon.

## Q12: What is the relativistic aberration fold-in?
**A:** The direction cosine mu is computed in the emitter frame with the photon direction transformed by the aberration formula - a subtle correction beyond naive 3D dot.

## Q13: What happens at the intermediate-redshift (z~1) rows?
**A:** The innermost ring's net shift flips sign across azimuth; the image's color gradient across the crescent is the visual diary of the shift.

## Q14: How is shift accumulated in movie rendering?
**A:** Each frame runs one frequency map; batches recompute the shift only for the moving fluid from the snapshot's velocity - cheap reuse of a static geometry.

## Q15: What is the summary?
**A:** The Lorentz shift is the 'color engine' of relativistic images - computed exactly as p.u ratios, applied to emissivity sampling, and validated against Doppler analytics.

## Q16: What question does lorentz frequency shift answer for a raytracer?
**A:** Given the plasma state along a photon path, it computes how much light reaches the observer after emission, absorption, and frequency shifts.

## Q17: Why is lorentz frequency shift essential for connecting GRMHD to pixels?
**A:** Plasma data alone is invisible; lorentz frequency shift converts density, temperature, and magnetic field into the intensity and color every pixel shows.

## Q18: What is the fundamental equation of lorentz frequency shift?
**A:** The radiative transfer equation dI/ds = j - alpha I along the ray; lorentz frequency shift integrates it including the relativistic invariant I/nu^3.

## Q19: What simplification is common in lorentz frequency shift for black holes?
**A:** The optically thin synchrotron-dominated case, where emission is computed per path segment and absorption is often neglected in the first pass.

## Q20: How does lorentz frequency shift handle moving frames?
**A:** Emissivity and absorption are defined in the fluid rest frame, then redshifted and Doppler-boosted into the coordinate/observer frame using the redshift factor.

## Q21: What are the two integration strategies for lorentz frequency shift?
**A:** Opacity-based ray casting through grid cells and analytic integration of the transfer equation through integrable models; production codes use the former.

## Q22: How does lorentz frequency shift determine color?
**A:** By integrating the spectrum at several fiducial frequencies and mapping the log-frequency-integrated intensity to a perceptual color ramp.

## Q23: What role does the optical depth tau play in lorentz frequency shift?
**A:** tau integrates the absorption along the path; large tau means the flow self-shields, which lorentz frequency shift must respect to avoid over-bright images.

## Q24: How does lorentz frequency shift encode a Lorentz boost?
**A:** The emissivity picks up a factor (1/g(1-beta·n))^2-ish from beaming plus the frequency shift; lorentz frequency shift applies these along the local fluid velocity.

## Q25: Why does synchrotron dominate disk emission in lorentz frequency shift?
**A:** The field and relativistic electrons radiate efficiently at the observed frequencies; thermal emission contributes where the flow is densest and coolest.

## Q26: What is the invariant form used in lorentz frequency shift?
**A:** I_nu / nu^3 is invariant along a ray, so lorentz frequency shift can transfer in any frame by tracking the frequency shift continuously.

## Q27: How do you validate lorentz frequency shift?
**A:** Reproduce analytic synchrotron spectra, check that a static uniform sphere has constant surface brightness, and compare derived images with published renders.

## Q28: How does lorentz frequency shift handle scattering?
**A:** Fully including scattering needs Monte Carlo; most pipeline lorentz frequency shift ignores it for the polarized-total intensity morphology and adds it later.

## Q29: What output does lorentz frequency shift produce per pixel?
**A:** Total intensity (and optionally Stokes IQUV) per frequency band; lorentz frequency shift is the last physics stage before tone mapping converts to an image.

## Q30: How do you make lorentz frequency shift deterministic?
**A:** Run the same snapshot, ray grid, and frequency set twice; bit-identical lorentz frequency shift means the pipeline is reproducible for science and movies.

## Q31: What do the measured M87-like images imply for lorentz frequency shift?
**A:** The bright ring and south-side enhancement follow from Doppler boosting of the approaching disk side; lorentz frequency shift reproduces these signatures from the velocity field.

## Q32: How does lorentz frequency shift integrate through the grid?
**A:** March through cells with a ray-grid traversal, sampling the fluid state, and update intensity with the segment transfer solution each step.

## Q33: What precision does lorentz frequency shift need?
**A:** Double precision for the integration of small intensities near the ring; lorentz frequency shift is the stage where visible artifacts for `dark' and `bright' regions meet.

## Q34: How do you compute the emitted frequency in lorentz frequency shift?
**A:** The fluid-frame frequency divides by (1+z) where z is the integrated redshift; lorentz frequency shift sets up spectral bins by emitted frequency in the observer band.

## Q35: What are the simplest usable emission models in lorentz frequency shift?
**A:** A thermal blackbody-approximation from temperature and density, or synchrotron power laws with gamma-distributed electrons; lorentz frequency shift starts with the simplest and upgrades.

## Q36: How does lorentz frequency shift create the visually iconic thin bright ring?
**A:** Near the photon sphere, rays sweep long path lengths through the brightest, most-beamed plasma, so integrated lorentz frequency shift intensity peaks there.

## Q37: What is the Doppler ratio that drives asymmetry in lorentz frequency shift?
**A:** The ratio between approaching and receding disk sides, roughly (1+beta cos theta over 1-beta cos theta) powers; lorentz frequency shift makes one side 3-5x brighter.

## Q38: How is lorentz frequency shift checked against real observations?
**A:** By comparing ring diameter, asymmetry, and spectrum to EHT measurements - agreement on those is the acceptance test for lorentz frequency shift.

## Q39: How does lorentz frequency shift fit the movie pipeline?
**A:** Rendering N frames applies lorentz frequency shift to each snapshot; lorentz frequency shift performance (per-ray cost) sets the total render budget for a movie.

## Q40: How does lorentz frequency shift fit the movie pipeline - justify your answer with a concrete production example.
**A:** Rendering N frames applies lorentz frequency shift to each snapshot; lorentz frequency shift performance (per-ray cost) sets the total render budget for a movie. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: How is lorentz frequency shift checked against real observations - justify your answer with a concrete production example.
**A:** By comparing ring diameter, asymmetry, and spectrum to EHT measurements - agreement on those is the acceptance test for lorentz frequency shift. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What is the Doppler ratio that drives asymmetry in lorentz frequency shift - justify your answer with a concrete production example.
**A:** The ratio between approaching and receding disk sides, roughly (1+beta cos theta over 1-beta cos theta) powers; lorentz frequency shift makes one side 3-5x brighter. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: How does lorentz frequency shift create the visually iconic thin bright ring - justify your answer with a concrete production example.
**A:** Near the photon sphere, rays sweep long path lengths through the brightest, most-beamed plasma, so integrated lorentz frequency shift intensity peaks there. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What are the simplest usable emission models in lorentz frequency shift - justify your answer with a concrete production example.
**A:** A thermal blackbody-approximation from temperature and density, or synchrotron power laws with gamma-distributed electrons; lorentz frequency shift starts with the simplest and upgrades. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: How do you compute the emitted frequency in lorentz frequency shift - justify your answer with a concrete production example.
**A:** The fluid-frame frequency divides by (1+z) where z is the integrated redshift; lorentz frequency shift sets up spectral bins by emitted frequency in the observer band. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: What precision does lorentz frequency shift need - justify your answer with a concrete production example.
**A:** Double precision for the integration of small intensities near the ring; lorentz frequency shift is the stage where visible artifacts for `dark' and `bright' regions meet. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: How does lorentz frequency shift integrate through the grid - justify your answer with a concrete production example.
**A:** March through cells with a ray-grid traversal, sampling the fluid state, and update intensity with the segment transfer solution each step. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: What do the measured M87-like images imply for lorentz frequency shift - justify your answer with a concrete production example.
**A:** The bright ring and south-side enhancement follow from Doppler boosting of the approaching disk side; lorentz frequency shift reproduces these signatures from the velocity field. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: How do you make lorentz frequency shift deterministic - justify your answer with a concrete production example.
**A:** Run the same snapshot, ray grid, and frequency set twice; bit-identical lorentz frequency shift means the pipeline is reproducible for science and movies. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What output does lorentz frequency shift produce per pixel - justify your answer with a concrete production example.
**A:** Total intensity (and optionally Stokes IQUV) per frequency band; lorentz frequency shift is the last physics stage before tone mapping converts to an image. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How does lorentz frequency shift handle scattering - justify your answer with a concrete production example.
**A:** Fully including scattering needs Monte Carlo; most pipeline lorentz frequency shift ignores it for the polarized-total intensity morphology and adds it later. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How do you validate lorentz frequency shift - justify your answer with a concrete production example.
**A:** Reproduce analytic synchrotron spectra, check that a static uniform sphere has constant surface brightness, and compare derived images with published renders. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What is the invariant form used in lorentz frequency shift - justify your answer with a concrete production example.
**A:** I_nu / nu^3 is invariant along a ray, so lorentz frequency shift can transfer in any frame by tracking the frequency shift continuously. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: Why does synchrotron dominate disk emission in lorentz frequency shift - justify your answer with a concrete production example.
**A:** The field and relativistic electrons radiate efficiently at the observed frequencies; thermal emission contributes where the flow is densest and coolest. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: How does lorentz frequency shift encode a Lorentz boost - justify your answer with a concrete production example.
**A:** The emissivity picks up a factor (1/g(1-beta·n))^2-ish from beaming plus the frequency shift; lorentz frequency shift applies these along the local fluid velocity. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What role does the optical depth tau play in lorentz frequency shift - justify your answer with a concrete production example.
**A:** tau integrates the absorption along the path; large tau means the flow self-shields, which lorentz frequency shift must respect to avoid over-bright images. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How does lorentz frequency shift determine color - justify your answer with a concrete production example.
**A:** By integrating the spectrum at several fiducial frequencies and mapping the log-frequency-integrated intensity to a perceptual color ramp. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What are the two integration strategies for lorentz frequency shift - justify your answer with a concrete production example.
**A:** Opacity-based ray casting through grid cells and analytic integration of the transfer equation through integrable models; production codes use the former. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How does lorentz frequency shift handle moving frames - justify your answer with a concrete production example.
**A:** Emissivity and absorption are defined in the fluid rest frame, then redshifted and Doppler-boosted into the coordinate/observer frame using the redshift factor. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What simplification is common in lorentz frequency shift for black holes - justify your answer with a concrete production example.
**A:** The optically thin synchrotron-dominated case, where emission is computed per path segment and absorption is often neglected in the first pass. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What is the fundamental equation of lorentz frequency shift - justify your answer with a concrete production example.
**A:** The radiative transfer equation dI/ds = j - alpha I along the ray; lorentz frequency shift integrates it including the relativistic invariant I/nu^3. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why is lorentz frequency shift essential for connecting GRMHD to pixels - justify your answer with a concrete production example.
**A:** Plasma data alone is invisible; lorentz frequency shift converts density, temperature, and magnetic field into the intensity and color every pixel shows. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What question does lorentz frequency shift answer for a raytracer - justify your answer with a concrete production example.
**A:** Given the plasma state along a photon path, it computes how much light reaches the observer after emission, absorption, and frequency shifts. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What question does lorentz frequency shift answer for a raytracer - justify your answer with a concrete production example.
**A:** Given the plasma state along a photon path, it computes how much light reaches the observer after emission, absorption, and frequency shifts. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why is lorentz frequency shift essential for connecting GRMHD to pixels - justify your answer with a concrete production example.
**A:** Plasma data alone is invisible; lorentz frequency shift converts density, temperature, and magnetic field into the intensity and color every pixel shows. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What is the fundamental equation of lorentz frequency shift - justify your answer with a concrete production example.
**A:** The radiative transfer equation dI/ds = j - alpha I along the ray; lorentz frequency shift integrates it including the relativistic invariant I/nu^3. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What simplification is common in lorentz frequency shift for black holes - justify your answer with a concrete production example.
**A:** The optically thin synchrotron-dominated case, where emission is computed per path segment and absorption is often neglected in the first pass. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How does lorentz frequency shift handle moving frames - justify your answer with a concrete production example.
**A:** Emissivity and absorption are defined in the fluid rest frame, then redshifted and Doppler-boosted into the coordinate/observer frame using the redshift factor. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What are the two integration strategies for lorentz frequency shift - justify your answer with a concrete production example.
**A:** Opacity-based ray casting through grid cells and analytic integration of the transfer equation through integrable models; production codes use the former. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How does lorentz frequency shift determine color - justify your answer with a concrete production example.
**A:** By integrating the spectrum at several fiducial frequencies and mapping the log-frequency-integrated intensity to a perceptual color ramp. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What role does the optical depth tau play in lorentz frequency shift - justify your answer with a concrete production example.
**A:** tau integrates the absorption along the path; large tau means the flow self-shields, which lorentz frequency shift must respect to avoid over-bright images. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: How does lorentz frequency shift encode a Lorentz boost - justify your answer with a concrete production example.
**A:** The emissivity picks up a factor (1/g(1-beta·n))^2-ish from beaming plus the frequency shift; lorentz frequency shift applies these along the local fluid velocity. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: Why does synchrotron dominate disk emission in lorentz frequency shift - justify your answer with a concrete production example.
**A:** The field and relativistic electrons radiate efficiently at the observed frequencies; thermal emission contributes where the flow is densest and coolest. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What is the invariant form used in lorentz frequency shift - justify your answer with a concrete production example.
**A:** I_nu / nu^3 is invariant along a ray, so lorentz frequency shift can transfer in any frame by tracking the frequency shift continuously. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How do you validate lorentz frequency shift - justify your answer with a concrete production example.
**A:** Reproduce analytic synchrotron spectra, check that a static uniform sphere has constant surface brightness, and compare derived images with published renders. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How does lorentz frequency shift handle scattering - justify your answer with a concrete production example.
**A:** Fully including scattering needs Monte Carlo; most pipeline lorentz frequency shift ignores it for the polarized-total intensity morphology and adds it later. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What output does lorentz frequency shift produce per pixel - justify your answer with a concrete production example.
**A:** Total intensity (and optionally Stokes IQUV) per frequency band; lorentz frequency shift is the last physics stage before tone mapping converts to an image. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: How do you make lorentz frequency shift deterministic - justify your answer with a concrete production example.
**A:** Run the same snapshot, ray grid, and frequency set twice; bit-identical lorentz frequency shift means the pipeline is reproducible for science and movies. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What do the measured M87-like images imply for lorentz frequency shift - justify your answer with a concrete production example.
**A:** The bright ring and south-side enhancement follow from Doppler boosting of the approaching disk side; lorentz frequency shift reproduces these signatures from the velocity field. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How does lorentz frequency shift integrate through the grid - justify your answer with a concrete production example.
**A:** March through cells with a ray-grid traversal, sampling the fluid state, and update intensity with the segment transfer solution each step. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: What precision does lorentz frequency shift need - justify your answer with a concrete production example.
**A:** Double precision for the integration of small intensities near the ring; lorentz frequency shift is the stage where visible artifacts for `dark' and `bright' regions meet. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: How do you compute the emitted frequency in lorentz frequency shift - justify your answer with a concrete production example.
**A:** The fluid-frame frequency divides by (1+z) where z is the integrated redshift; lorentz frequency shift sets up spectral bins by emitted frequency in the observer band. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What are the simplest usable emission models in lorentz frequency shift - justify your answer with a concrete production example.
**A:** A thermal blackbody-approximation from temperature and density, or synchrotron power laws with gamma-distributed electrons; lorentz frequency shift starts with the simplest and upgrades. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: How does lorentz frequency shift create the visually iconic thin bright ring - justify your answer with a concrete production example.
**A:** Near the photon sphere, rays sweep long path lengths through the brightest, most-beamed plasma, so integrated lorentz frequency shift intensity peaks there. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What is the Doppler ratio that drives asymmetry in lorentz frequency shift - justify your answer with a concrete production example.
**A:** The ratio between approaching and receding disk sides, roughly (1+beta cos theta over 1-beta cos theta) powers; lorentz frequency shift makes one side 3-5x brighter. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: How is lorentz frequency shift checked against real observations - justify your answer with a concrete production example.
**A:** By comparing ring diameter, asymmetry, and spectrum to EHT measurements - agreement on those is the acceptance test for lorentz frequency shift. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How does lorentz frequency shift fit the movie pipeline - justify your answer with a concrete production example.
**A:** Rendering N frames applies lorentz frequency shift to each snapshot; lorentz frequency shift performance (per-ray cost) sets the total render budget for a movie. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How does lorentz frequency shift fit the movie pipeline - justify your answer with a concrete production example.
**A:** Rendering N frames applies lorentz frequency shift to each snapshot; lorentz frequency shift performance (per-ray cost) sets the total render budget for a movie. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: How is lorentz frequency shift checked against real observations - justify your answer with a concrete production example.
**A:** By comparing ring diameter, asymmetry, and spectrum to EHT measurements - agreement on those is the acceptance test for lorentz frequency shift. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What is the Doppler ratio that drives asymmetry in lorentz frequency shift - justify your answer with a concrete production example.
**A:** The ratio between approaching and receding disk sides, roughly (1+beta cos theta over 1-beta cos theta) powers; lorentz frequency shift makes one side 3-5x brighter. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: How does lorentz frequency shift create the visually iconic thin bright ring - justify your answer with a concrete production example.
**A:** Near the photon sphere, rays sweep long path lengths through the brightest, most-beamed plasma, so integrated lorentz frequency shift intensity peaks there. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What are the simplest usable emission models in lorentz frequency shift - justify your answer with a concrete production example.
**A:** A thermal blackbody-approximation from temperature and density, or synchrotron power laws with gamma-distributed electrons; lorentz frequency shift starts with the simplest and upgrades. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: How do you compute the emitted frequency in lorentz frequency shift - justify your answer with a concrete production example.
**A:** The fluid-frame frequency divides by (1+z) where z is the integrated redshift; lorentz frequency shift sets up spectral bins by emitted frequency in the observer band. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: What precision does lorentz frequency shift need - justify your answer with a concrete production example.
**A:** Double precision for the integration of small intensities near the ring; lorentz frequency shift is the stage where visible artifacts for `dark' and `bright' regions meet. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: How does lorentz frequency shift integrate through the grid - justify your answer with a concrete production example.
**A:** March through cells with a ray-grid traversal, sampling the fluid state, and update intensity with the segment transfer solution each step. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: What do the measured M87-like images imply for lorentz frequency shift - justify your answer with a concrete production example.
**A:** The bright ring and south-side enhancement follow from Doppler boosting of the approaching disk side; lorentz frequency shift reproduces these signatures from the velocity field. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: How do you make lorentz frequency shift deterministic - justify your answer with a concrete production example.
**A:** Run the same snapshot, ray grid, and frequency set twice; bit-identical lorentz frequency shift means the pipeline is reproducible for science and movies. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What output does lorentz frequency shift produce per pixel - justify your answer with a concrete production example.
**A:** Total intensity (and optionally Stokes IQUV) per frequency band; lorentz frequency shift is the last physics stage before tone mapping converts to an image. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How does lorentz frequency shift handle scattering - justify your answer with a concrete production example.
**A:** Fully including scattering needs Monte Carlo; most pipeline lorentz frequency shift ignores it for the polarized-total intensity morphology and adds it later. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How do you validate lorentz frequency shift - justify your answer with a concrete production example.
**A:** Reproduce analytic synchrotron spectra, check that a static uniform sphere has constant surface brightness, and compare derived images with published renders. A concrete example: consistently applying lorentz frequency shift in code review and regression tests keeps the whole pipeline trustworthy.
