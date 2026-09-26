# Radiative Transfer — Line Of Sight Integration Interview Questions and Answers

## Q1: What is line-of-sight integration?
**A:** Evaluating the formal RTE solution along a geodesic by integrating emissivity (and opacity) at sampled points - the 'compose the image' step.

## Q2: How are sample points chosen along the ray?
**A:** Adaptively: fine steps where density/B gradient is large (near the disk/ring), coarse in vacuum; often tied to the geodesic integrator's own step.

## Q3: What is the quadrature rule used?
**A:** Trapezoid/Simpson in the thin limit; for alpha>0 a sub-step multiplication scheme (thick pixels handle saturation); order matches the geometry integrator.

## Q4: How does one combine emission and attenuation?
**A:** Backwards integration: start with I=0 at the observer, add j*ds and multiply by exp(-alpha*ds) per segment - walk forward or backward, consistent.

## Q5: What is the 'first surface' vs 'volume' model?
**A:** Thin-disks render one surface hit; real volume emission integrates over the whole path - the line integral is the volume generalization.

## Q6: How does the code handle the frequency at integration?
**A:** Each segment evaluates j at the emitted frequency that maps to the fixed observation bin; alpha likewise - the frequency map is threaded through the integral.

## Q7: What are the cost drivers?
**A:** The number of radiative samples per ray: adaptive density-based sampling keeps it ~O(100) per pixel even at 4k - the transfer budget is fractions of the geodesic budget.

## Q8: What is the emitted-boost integration?
**A:** The total intensity I at the observer is the sum over segments of boosted, attenuated j - mathematically the formal solution sampled.

## Q9: What is the hit-based vs full-path integration?
**A:** Disk shadow rendering often uses a dedicated hit; full-path is robust for volume (MHD-like) data - pick per-use-case in the pipeline.

## Q10: How do you avoid double-counting?
**A:** Sampling weights (ds proportionality) and the per-sample volume need consistent normalization - the ds measure is derived from the metric and the grid volumes.

## Q11: What validation pins the integrator?
**A:** A constant-alpha, varying-j analytic column: closed-form result matches to quadrature order; a vacuum ray returns exactly the sky background.

## Q12: What is the polarization fold-in?
**A:** Each segment also rotates/attenuates the Stokes vector (Faraday) - the line-of-sight integrator carries (I,Q,U,V) or complex amplitude per frequency.

## Q13: How does path termination interact with integration?
**A:** Capture (horizon) ends the integral; sky-miss ends with zero added intensity - both terminate cleanly, preserving the no-spurious-flux contract.

## Q14: What is the movie-frame cache?
**A:** Static-geometry frames reuse the sample-path weights; only the fluid state (thus j) changes - a large speedup for animations.

## Q15: What is the summary?
**A:** Line-of-sight integration is the transfer core - a path-weighted quadrature of j and alpha along each geodesic, adaptive, frame-true, and validated against analytic columns.

## Q16: What question does line of sight integration answer for a raytracer?
**A:** Given the plasma state along a photon path, it computes how much light reaches the observer after emission, absorption, and frequency shifts.

## Q17: Why is line of sight integration essential for connecting GRMHD to pixels?
**A:** Plasma data alone is invisible; line of sight integration converts density, temperature, and magnetic field into the intensity and color every pixel shows.

## Q18: What is the fundamental equation of line of sight integration?
**A:** The radiative transfer equation dI/ds = j - alpha I along the ray; line of sight integration integrates it including the relativistic invariant I/nu^3.

## Q19: What simplification is common in line of sight integration for black holes?
**A:** The optically thin synchrotron-dominated case, where emission is computed per path segment and absorption is often neglected in the first pass.

## Q20: How does line of sight integration handle moving frames?
**A:** Emissivity and absorption are defined in the fluid rest frame, then redshifted and Doppler-boosted into the coordinate/observer frame using the redshift factor.

## Q21: What are the two integration strategies for line of sight integration?
**A:** Opacity-based ray casting through grid cells and analytic integration of the transfer equation through integrable models; production codes use the former.

## Q22: How does line of sight integration determine color?
**A:** By integrating the spectrum at several fiducial frequencies and mapping the log-frequency-integrated intensity to a perceptual color ramp.

## Q23: What role does the optical depth tau play in line of sight integration?
**A:** tau integrates the absorption along the path; large tau means the flow self-shields, which line of sight integration must respect to avoid over-bright images.

## Q24: How does line of sight integration encode a Lorentz boost?
**A:** The emissivity picks up a factor (1/g(1-beta·n))^2-ish from beaming plus the frequency shift; line of sight integration applies these along the local fluid velocity.

## Q25: Why does synchrotron dominate disk emission in line of sight integration?
**A:** The field and relativistic electrons radiate efficiently at the observed frequencies; thermal emission contributes where the flow is densest and coolest.

## Q26: What is the invariant form used in line of sight integration?
**A:** I_nu / nu^3 is invariant along a ray, so line of sight integration can transfer in any frame by tracking the frequency shift continuously.

## Q27: How do you validate line of sight integration?
**A:** Reproduce analytic synchrotron spectra, check that a static uniform sphere has constant surface brightness, and compare derived images with published renders.

## Q28: How does line of sight integration handle scattering?
**A:** Fully including scattering needs Monte Carlo; most pipeline line of sight integration ignores it for the polarized-total intensity morphology and adds it later.

## Q29: What output does line of sight integration produce per pixel?
**A:** Total intensity (and optionally Stokes IQUV) per frequency band; line of sight integration is the last physics stage before tone mapping converts to an image.

## Q30: How do you make line of sight integration deterministic?
**A:** Run the same snapshot, ray grid, and frequency set twice; bit-identical line of sight integration means the pipeline is reproducible for science and movies.

## Q31: What do the measured M87-like images imply for line of sight integration?
**A:** The bright ring and south-side enhancement follow from Doppler boosting of the approaching disk side; line of sight integration reproduces these signatures from the velocity field.

## Q32: How does line of sight integration integrate through the grid?
**A:** March through cells with a ray-grid traversal, sampling the fluid state, and update intensity with the segment transfer solution each step.

## Q33: What precision does line of sight integration need?
**A:** Double precision for the integration of small intensities near the ring; line of sight integration is the stage where visible artifacts for `dark' and `bright' regions meet.

## Q34: How do you compute the emitted frequency in line of sight integration?
**A:** The fluid-frame frequency divides by (1+z) where z is the integrated redshift; line of sight integration sets up spectral bins by emitted frequency in the observer band.

## Q35: What are the simplest usable emission models in line of sight integration?
**A:** A thermal blackbody-approximation from temperature and density, or synchrotron power laws with gamma-distributed electrons; line of sight integration starts with the simplest and upgrades.

## Q36: How does line of sight integration create the visually iconic thin bright ring?
**A:** Near the photon sphere, rays sweep long path lengths through the brightest, most-beamed plasma, so integrated line of sight integration intensity peaks there.

## Q37: What is the Doppler ratio that drives asymmetry in line of sight integration?
**A:** The ratio between approaching and receding disk sides, roughly (1+beta cos theta over 1-beta cos theta) powers; line of sight integration makes one side 3-5x brighter.

## Q38: How is line of sight integration checked against real observations?
**A:** By comparing ring diameter, asymmetry, and spectrum to EHT measurements - agreement on those is the acceptance test for line of sight integration.

## Q39: How does line of sight integration fit the movie pipeline?
**A:** Rendering N frames applies line of sight integration to each snapshot; line of sight integration performance (per-ray cost) sets the total render budget for a movie.

## Q40: How does line of sight integration fit the movie pipeline - justify your answer with a concrete production example.
**A:** Rendering N frames applies line of sight integration to each snapshot; line of sight integration performance (per-ray cost) sets the total render budget for a movie. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: How is line of sight integration checked against real observations - justify your answer with a concrete production example.
**A:** By comparing ring diameter, asymmetry, and spectrum to EHT measurements - agreement on those is the acceptance test for line of sight integration. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What is the Doppler ratio that drives asymmetry in line of sight integration - justify your answer with a concrete production example.
**A:** The ratio between approaching and receding disk sides, roughly (1+beta cos theta over 1-beta cos theta) powers; line of sight integration makes one side 3-5x brighter. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: How does line of sight integration create the visually iconic thin bright ring - justify your answer with a concrete production example.
**A:** Near the photon sphere, rays sweep long path lengths through the brightest, most-beamed plasma, so integrated line of sight integration intensity peaks there. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What are the simplest usable emission models in line of sight integration - justify your answer with a concrete production example.
**A:** A thermal blackbody-approximation from temperature and density, or synchrotron power laws with gamma-distributed electrons; line of sight integration starts with the simplest and upgrades. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: How do you compute the emitted frequency in line of sight integration - justify your answer with a concrete production example.
**A:** The fluid-frame frequency divides by (1+z) where z is the integrated redshift; line of sight integration sets up spectral bins by emitted frequency in the observer band. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: What precision does line of sight integration need - justify your answer with a concrete production example.
**A:** Double precision for the integration of small intensities near the ring; line of sight integration is the stage where visible artifacts for `dark' and `bright' regions meet. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: How does line of sight integration integrate through the grid - justify your answer with a concrete production example.
**A:** March through cells with a ray-grid traversal, sampling the fluid state, and update intensity with the segment transfer solution each step. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: What do the measured M87-like images imply for line of sight integration - justify your answer with a concrete production example.
**A:** The bright ring and south-side enhancement follow from Doppler boosting of the approaching disk side; line of sight integration reproduces these signatures from the velocity field. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: How do you make line of sight integration deterministic - justify your answer with a concrete production example.
**A:** Run the same snapshot, ray grid, and frequency set twice; bit-identical line of sight integration means the pipeline is reproducible for science and movies. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What output does line of sight integration produce per pixel - justify your answer with a concrete production example.
**A:** Total intensity (and optionally Stokes IQUV) per frequency band; line of sight integration is the last physics stage before tone mapping converts to an image. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How does line of sight integration handle scattering - justify your answer with a concrete production example.
**A:** Fully including scattering needs Monte Carlo; most pipeline line of sight integration ignores it for the polarized-total intensity morphology and adds it later. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How do you validate line of sight integration - justify your answer with a concrete production example.
**A:** Reproduce analytic synchrotron spectra, check that a static uniform sphere has constant surface brightness, and compare derived images with published renders. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What is the invariant form used in line of sight integration - justify your answer with a concrete production example.
**A:** I_nu / nu^3 is invariant along a ray, so line of sight integration can transfer in any frame by tracking the frequency shift continuously. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: Why does synchrotron dominate disk emission in line of sight integration - justify your answer with a concrete production example.
**A:** The field and relativistic electrons radiate efficiently at the observed frequencies; thermal emission contributes where the flow is densest and coolest. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: How does line of sight integration encode a Lorentz boost - justify your answer with a concrete production example.
**A:** The emissivity picks up a factor (1/g(1-beta·n))^2-ish from beaming plus the frequency shift; line of sight integration applies these along the local fluid velocity. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What role does the optical depth tau play in line of sight integration - justify your answer with a concrete production example.
**A:** tau integrates the absorption along the path; large tau means the flow self-shields, which line of sight integration must respect to avoid over-bright images. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How does line of sight integration determine color - justify your answer with a concrete production example.
**A:** By integrating the spectrum at several fiducial frequencies and mapping the log-frequency-integrated intensity to a perceptual color ramp. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What are the two integration strategies for line of sight integration - justify your answer with a concrete production example.
**A:** Opacity-based ray casting through grid cells and analytic integration of the transfer equation through integrable models; production codes use the former. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How does line of sight integration handle moving frames - justify your answer with a concrete production example.
**A:** Emissivity and absorption are defined in the fluid rest frame, then redshifted and Doppler-boosted into the coordinate/observer frame using the redshift factor. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What simplification is common in line of sight integration for black holes - justify your answer with a concrete production example.
**A:** The optically thin synchrotron-dominated case, where emission is computed per path segment and absorption is often neglected in the first pass. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What is the fundamental equation of line of sight integration - justify your answer with a concrete production example.
**A:** The radiative transfer equation dI/ds = j - alpha I along the ray; line of sight integration integrates it including the relativistic invariant I/nu^3. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why is line of sight integration essential for connecting GRMHD to pixels - justify your answer with a concrete production example.
**A:** Plasma data alone is invisible; line of sight integration converts density, temperature, and magnetic field into the intensity and color every pixel shows. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What question does line of sight integration answer for a raytracer - justify your answer with a concrete production example.
**A:** Given the plasma state along a photon path, it computes how much light reaches the observer after emission, absorption, and frequency shifts. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What question does line of sight integration answer for a raytracer - justify your answer with a concrete production example.
**A:** Given the plasma state along a photon path, it computes how much light reaches the observer after emission, absorption, and frequency shifts. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why is line of sight integration essential for connecting GRMHD to pixels - justify your answer with a concrete production example.
**A:** Plasma data alone is invisible; line of sight integration converts density, temperature, and magnetic field into the intensity and color every pixel shows. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What is the fundamental equation of line of sight integration - justify your answer with a concrete production example.
**A:** The radiative transfer equation dI/ds = j - alpha I along the ray; line of sight integration integrates it including the relativistic invariant I/nu^3. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What simplification is common in line of sight integration for black holes - justify your answer with a concrete production example.
**A:** The optically thin synchrotron-dominated case, where emission is computed per path segment and absorption is often neglected in the first pass. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How does line of sight integration handle moving frames - justify your answer with a concrete production example.
**A:** Emissivity and absorption are defined in the fluid rest frame, then redshifted and Doppler-boosted into the coordinate/observer frame using the redshift factor. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What are the two integration strategies for line of sight integration - justify your answer with a concrete production example.
**A:** Opacity-based ray casting through grid cells and analytic integration of the transfer equation through integrable models; production codes use the former. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How does line of sight integration determine color - justify your answer with a concrete production example.
**A:** By integrating the spectrum at several fiducial frequencies and mapping the log-frequency-integrated intensity to a perceptual color ramp. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What role does the optical depth tau play in line of sight integration - justify your answer with a concrete production example.
**A:** tau integrates the absorption along the path; large tau means the flow self-shields, which line of sight integration must respect to avoid over-bright images. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: How does line of sight integration encode a Lorentz boost - justify your answer with a concrete production example.
**A:** The emissivity picks up a factor (1/g(1-beta·n))^2-ish from beaming plus the frequency shift; line of sight integration applies these along the local fluid velocity. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: Why does synchrotron dominate disk emission in line of sight integration - justify your answer with a concrete production example.
**A:** The field and relativistic electrons radiate efficiently at the observed frequencies; thermal emission contributes where the flow is densest and coolest. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What is the invariant form used in line of sight integration - justify your answer with a concrete production example.
**A:** I_nu / nu^3 is invariant along a ray, so line of sight integration can transfer in any frame by tracking the frequency shift continuously. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How do you validate line of sight integration - justify your answer with a concrete production example.
**A:** Reproduce analytic synchrotron spectra, check that a static uniform sphere has constant surface brightness, and compare derived images with published renders. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How does line of sight integration handle scattering - justify your answer with a concrete production example.
**A:** Fully including scattering needs Monte Carlo; most pipeline line of sight integration ignores it for the polarized-total intensity morphology and adds it later. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What output does line of sight integration produce per pixel - justify your answer with a concrete production example.
**A:** Total intensity (and optionally Stokes IQUV) per frequency band; line of sight integration is the last physics stage before tone mapping converts to an image. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: How do you make line of sight integration deterministic - justify your answer with a concrete production example.
**A:** Run the same snapshot, ray grid, and frequency set twice; bit-identical line of sight integration means the pipeline is reproducible for science and movies. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What do the measured M87-like images imply for line of sight integration - justify your answer with a concrete production example.
**A:** The bright ring and south-side enhancement follow from Doppler boosting of the approaching disk side; line of sight integration reproduces these signatures from the velocity field. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How does line of sight integration integrate through the grid - justify your answer with a concrete production example.
**A:** March through cells with a ray-grid traversal, sampling the fluid state, and update intensity with the segment transfer solution each step. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: What precision does line of sight integration need - justify your answer with a concrete production example.
**A:** Double precision for the integration of small intensities near the ring; line of sight integration is the stage where visible artifacts for `dark' and `bright' regions meet. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: How do you compute the emitted frequency in line of sight integration - justify your answer with a concrete production example.
**A:** The fluid-frame frequency divides by (1+z) where z is the integrated redshift; line of sight integration sets up spectral bins by emitted frequency in the observer band. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What are the simplest usable emission models in line of sight integration - justify your answer with a concrete production example.
**A:** A thermal blackbody-approximation from temperature and density, or synchrotron power laws with gamma-distributed electrons; line of sight integration starts with the simplest and upgrades. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: How does line of sight integration create the visually iconic thin bright ring - justify your answer with a concrete production example.
**A:** Near the photon sphere, rays sweep long path lengths through the brightest, most-beamed plasma, so integrated line of sight integration intensity peaks there. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What is the Doppler ratio that drives asymmetry in line of sight integration - justify your answer with a concrete production example.
**A:** The ratio between approaching and receding disk sides, roughly (1+beta cos theta over 1-beta cos theta) powers; line of sight integration makes one side 3-5x brighter. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: How is line of sight integration checked against real observations - justify your answer with a concrete production example.
**A:** By comparing ring diameter, asymmetry, and spectrum to EHT measurements - agreement on those is the acceptance test for line of sight integration. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How does line of sight integration fit the movie pipeline - justify your answer with a concrete production example.
**A:** Rendering N frames applies line of sight integration to each snapshot; line of sight integration performance (per-ray cost) sets the total render budget for a movie. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How does line of sight integration fit the movie pipeline - justify your answer with a concrete production example.
**A:** Rendering N frames applies line of sight integration to each snapshot; line of sight integration performance (per-ray cost) sets the total render budget for a movie. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: How is line of sight integration checked against real observations - justify your answer with a concrete production example.
**A:** By comparing ring diameter, asymmetry, and spectrum to EHT measurements - agreement on those is the acceptance test for line of sight integration. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What is the Doppler ratio that drives asymmetry in line of sight integration - justify your answer with a concrete production example.
**A:** The ratio between approaching and receding disk sides, roughly (1+beta cos theta over 1-beta cos theta) powers; line of sight integration makes one side 3-5x brighter. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: How does line of sight integration create the visually iconic thin bright ring - justify your answer with a concrete production example.
**A:** Near the photon sphere, rays sweep long path lengths through the brightest, most-beamed plasma, so integrated line of sight integration intensity peaks there. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What are the simplest usable emission models in line of sight integration - justify your answer with a concrete production example.
**A:** A thermal blackbody-approximation from temperature and density, or synchrotron power laws with gamma-distributed electrons; line of sight integration starts with the simplest and upgrades. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: How do you compute the emitted frequency in line of sight integration - justify your answer with a concrete production example.
**A:** The fluid-frame frequency divides by (1+z) where z is the integrated redshift; line of sight integration sets up spectral bins by emitted frequency in the observer band. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: What precision does line of sight integration need - justify your answer with a concrete production example.
**A:** Double precision for the integration of small intensities near the ring; line of sight integration is the stage where visible artifacts for `dark' and `bright' regions meet. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: How does line of sight integration integrate through the grid - justify your answer with a concrete production example.
**A:** March through cells with a ray-grid traversal, sampling the fluid state, and update intensity with the segment transfer solution each step. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: What do the measured M87-like images imply for line of sight integration - justify your answer with a concrete production example.
**A:** The bright ring and south-side enhancement follow from Doppler boosting of the approaching disk side; line of sight integration reproduces these signatures from the velocity field. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: How do you make line of sight integration deterministic - justify your answer with a concrete production example.
**A:** Run the same snapshot, ray grid, and frequency set twice; bit-identical line of sight integration means the pipeline is reproducible for science and movies. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What output does line of sight integration produce per pixel - justify your answer with a concrete production example.
**A:** Total intensity (and optionally Stokes IQUV) per frequency band; line of sight integration is the last physics stage before tone mapping converts to an image. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How does line of sight integration handle scattering - justify your answer with a concrete production example.
**A:** Fully including scattering needs Monte Carlo; most pipeline line of sight integration ignores it for the polarized-total intensity morphology and adds it later. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How do you validate line of sight integration - justify your answer with a concrete production example.
**A:** Reproduce analytic synchrotron spectra, check that a static uniform sphere has constant surface brightness, and compare derived images with published renders. A concrete example: consistently applying line of sight integration in code review and regression tests keeps the whole pipeline trustworthy.
