# Gr Ray Tracing — Doppler Beaming Interview Questions and Answers

## Q1: What is Doppler beaming?
**A:** Relativistic motion sharpens emitted light into the direction of motion: approaching emitters appear brighter and bluer, receding ones fainter and redder.

## Q2: What is the Doppler factor?
**A:** delta = 1/(gamma(1 - beta cos theta)) where theta is the angle between emitter velocity and the photon direction in the emitter frame.

## Q3: Why is the disk's approaching side brighter?
**A:** Gas orbiting at the hole moves toward the observer on one side; beaming boosts its intensity and blueshifts spectra - the iconic hot crescent.

## Q4: What is the code formula?
**A:** The transfer factor includes (nu_obs/nu_emit)^2 (or ^3 depending on frame of emission) - related to the Doppler/cluster factor in intensity transfer.

## Q5: How do you compute it from the integrated ray?
**A:** At the hit site, form p.u_emit and p.u_obs; the redshift factor z = (p.u) ratios fold Doppler + gravitational into one scalar per hit.

## Q6: What sets the Doppler strength?
**A:** The orbital beta ~ 0.2-0.6 c for the innermost disk (Keplerian, prograde); the factor difference between sides reaches orders of magnitude at high inclination.

## Q7: What is the angular dependence (edge-on vs face-on)?
**A:** Face-on (i~0) sees almost no asymmetry (cos theta ~ 0); edge-on maximizes it - a key handle on inclination in fits.

## Q8: How does beaming combine with gravitational redshift?
**A:** Total shift factor = Doppler * gravitational; near the hole both operate and partially cancel, net producing the specific blue on prograde.

## Q9: What does beaming do to the photon ring?
**A:** The prograde ring sector is boosted (the hole spins, dragging light along) - the intensity asymmetry of the ring is layered on top of shape asymmetry.

## Q10: How is the flux per frequency affected?
**A:** I_obs(nu) = (delta)^k I_emit(nu/delta) with k depending on the angular distribution (k=2 for bolometric, k=3 for specific-intensity direction); code must pick and document k.

## Q11: What does beaming do to the colors?
**A:** The shift moves frequency; spectra (e.g., power-law) sampled at the shifted frequency produce the full chromatic result - measured as colors.

## Q12: How do you validate beaming?
**A:** Use a rigidly rotating, optically-thin annulus at radius r; apply the analytic delta to a known spectrum and check the image intensity/color at two azimuths.

## Q13: What is the 'spotlight' alignment in movies?
**A:** As a hot spot orbits, its Doppler-boosted image peaks when moving toward the observer - the periodic bright flash used to probe disk scale in time-domain imaging.

## Q14: What pitfall hides beaming bugs?
**A:** Using frame confusion: boosting with the wrong velocity (e.g., coordinate beta instead of ZAMO-frame) silently flips the asymmetry; always define the emitter's 4-velocity frame explicitly.

## Q15: What is the beaming check image?
**A:** Render a symmetric cold disk; the hot crescent must sit on the approaching (prograde) side for prograde spin - invert a, the crescent flips - self-evident smoke test.

## Q16: What does doppler beaming concretely do inside the raytracer?
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic.

## Q17: Why is doppler beaming the heart of a black-hole visualizer?
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how doppler beaming bends and time-shifts each ray.

## Q18: How is doppler beaming implemented on the GPU?
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through doppler beaming until the ray is captured or escapes.

## Q19: What are the two families of integration for doppler beaming?
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; doppler beaming chooses per codebase.

## Q20: How do you validate doppler beaming?
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures.

## Q21: What is the typical step-size strategy in doppler beaming?
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where doppler beaming gradients are steepest and error grows fastest.

## Q22: What state does the integrator track for doppler beaming?
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - doppler beaming state vector is small enough to fit in registers.

## Q23: How does doppler beaming handle captured photons?
**A:** It terminates integration at the horizon and records absorption; doppler beaming distinguishes capture from scatter by the radial turning point.

## Q24: What role do conserved constants play in doppler beaming?
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding doppler beaming for large image grids.

## Q25: Describe the numerical error budget of doppler beaming.
**A:** Per-step truncation error and accumulated drift; doppler beaming budgets a relative tolerance and verifies the final image is stable.

## Q26: How does doppler beaming map the sky to the image plane?
**A:** Each image pixel defines an initial direction; doppler beaming evolves that direction backward in time until it leaves the domain to a background sky or hits the disk.

## Q27: What is the most common bug in doppler beaming?
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; doppler beaming needs golden-image regression tests.

## Q28: How do you parallelize doppler beaming?
**A:** Every pixel is an independent doppler beaming problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication.

## Q29: What determines the visual shadow size in doppler beaming?
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in doppler beaming is the photon ring.

## Q30: When do you need full Kerr doppler beaming instead of Schwarzschild?
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; doppler beaming must support spin to be credible.

## Q31: What is the 'second/third image' vocabulary of doppler beaming?
**A:** Light winding around the black hole produces multiple images; doppler beaming naturally produces the primary, secondary, and higher-order photon ring.

## Q32: How does doppler beaming produce the bright thin ring?
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the doppler beaming critical impact parameter.

## Q33: How does doppler beaming decide frequencies for render?
**A:** It integrates the redshift factor along the ray; doppler beaming multiplies emitted frequency by it before applying the transfer equation.

## Q34: What modes does doppler beaming render the accretion disk?
**A:** First as a geometric emitter grid, later using GRMHD data; doppler beaming is agnostic to the source as long as it can query emissivity along the path.

## Q35: How is doppler beaming performance quantified?
**A:** Mega-rays per second and time per frame; doppler beaming usually spends its budget in the integration loop, so its step count is the key metric.

## Q36: What is the effect of camera position in doppler beaming?
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; doppler beaming validates each against known renders.

## Q37: How does doppler beaming incorporate the disk's fluid velocity?
**A:** Doppler and beaming appear when the emissivity frame is boosted; doppler beaming applies that boost per photon ray path segment.

## Q38: What is the horizon-catching strategy in doppler beaming?
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; doppler beaming then terminates that lane.

## Q39: How should you commission doppler beaming output?
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent.

## Q40: How should you commission doppler beaming output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is the horizon-catching strategy in doppler beaming - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; doppler beaming then terminates that lane. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How does doppler beaming incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; doppler beaming applies that boost per photon ray path segment. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What is the effect of camera position in doppler beaming - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; doppler beaming validates each against known renders. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How is doppler beaming performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; doppler beaming usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What modes does doppler beaming render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; doppler beaming is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does doppler beaming decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; doppler beaming multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: How does doppler beaming produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the doppler beaming critical impact parameter. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: What is the 'second/third image' vocabulary of doppler beaming - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; doppler beaming naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: When do you need full Kerr doppler beaming instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; doppler beaming must support spin to be credible. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What determines the visual shadow size in doppler beaming - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in doppler beaming is the photon ring. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How do you parallelize doppler beaming - justify your answer with a concrete production example.
**A:** Every pixel is an independent doppler beaming problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: What is the most common bug in doppler beaming - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; doppler beaming needs golden-image regression tests. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: How does doppler beaming map the sky to the image plane - justify your answer with a concrete production example.
**A:** Each image pixel defines an initial direction; doppler beaming evolves that direction backward in time until it leaves the domain to a background sky or hits the disk. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: Describe the numerical error budget of doppler beaming - justify your answer with a concrete production example.
**A:** Per-step truncation error and accumulated drift; doppler beaming budgets a relative tolerance and verifies the final image is stable. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What role do conserved constants play in doppler beaming - justify your answer with a concrete production example.
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding doppler beaming for large image grids. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: How does doppler beaming handle captured photons - justify your answer with a concrete production example.
**A:** It terminates integration at the horizon and records absorption; doppler beaming distinguishes capture from scatter by the radial turning point. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: What state does the integrator track for doppler beaming - justify your answer with a concrete production example.
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - doppler beaming state vector is small enough to fit in registers. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the typical step-size strategy in doppler beaming - justify your answer with a concrete production example.
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where doppler beaming gradients are steepest and error grows fastest. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How do you validate doppler beaming - justify your answer with a concrete production example.
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What are the two families of integration for doppler beaming - justify your answer with a concrete production example.
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; doppler beaming chooses per codebase. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: How is doppler beaming implemented on the GPU - justify your answer with a concrete production example.
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through doppler beaming until the ray is captured or escapes. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why is doppler beaming the heart of a black-hole visualizer - justify your answer with a concrete production example.
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how doppler beaming bends and time-shifts each ray. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What does doppler beaming concretely do inside the raytracer - justify your answer with a concrete production example.
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What does doppler beaming concretely do inside the raytracer - justify your answer with a concrete production example.
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why is doppler beaming the heart of a black-hole visualizer - justify your answer with a concrete production example.
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how doppler beaming bends and time-shifts each ray. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: How is doppler beaming implemented on the GPU - justify your answer with a concrete production example.
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through doppler beaming until the ray is captured or escapes. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What are the two families of integration for doppler beaming - justify your answer with a concrete production example.
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; doppler beaming chooses per codebase. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How do you validate doppler beaming - justify your answer with a concrete production example.
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What is the typical step-size strategy in doppler beaming - justify your answer with a concrete production example.
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where doppler beaming gradients are steepest and error grows fastest. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: What state does the integrator track for doppler beaming - justify your answer with a concrete production example.
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - doppler beaming state vector is small enough to fit in registers. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: How does doppler beaming handle captured photons - justify your answer with a concrete production example.
**A:** It terminates integration at the horizon and records absorption; doppler beaming distinguishes capture from scatter by the radial turning point. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What role do conserved constants play in doppler beaming - justify your answer with a concrete production example.
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding doppler beaming for large image grids. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: Describe the numerical error budget of doppler beaming - justify your answer with a concrete production example.
**A:** Per-step truncation error and accumulated drift; doppler beaming budgets a relative tolerance and verifies the final image is stable. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: How does doppler beaming map the sky to the image plane - justify your answer with a concrete production example.
**A:** Each image pixel defines an initial direction; doppler beaming evolves that direction backward in time until it leaves the domain to a background sky or hits the disk. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: What is the most common bug in doppler beaming - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; doppler beaming needs golden-image regression tests. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How do you parallelize doppler beaming - justify your answer with a concrete production example.
**A:** Every pixel is an independent doppler beaming problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What determines the visual shadow size in doppler beaming - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in doppler beaming is the photon ring. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: When do you need full Kerr doppler beaming instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; doppler beaming must support spin to be credible. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What is the 'second/third image' vocabulary of doppler beaming - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; doppler beaming naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How does doppler beaming produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the doppler beaming critical impact parameter. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does doppler beaming decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; doppler beaming multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What modes does doppler beaming render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; doppler beaming is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How is doppler beaming performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; doppler beaming usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What is the effect of camera position in doppler beaming - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; doppler beaming validates each against known renders. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How does doppler beaming incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; doppler beaming applies that boost per photon ray path segment. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the horizon-catching strategy in doppler beaming - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; doppler beaming then terminates that lane. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How should you commission doppler beaming output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How should you commission doppler beaming output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is the horizon-catching strategy in doppler beaming - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; doppler beaming then terminates that lane. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How does doppler beaming incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; doppler beaming applies that boost per photon ray path segment. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What is the effect of camera position in doppler beaming - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; doppler beaming validates each against known renders. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How is doppler beaming performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; doppler beaming usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What modes does doppler beaming render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; doppler beaming is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does doppler beaming decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; doppler beaming multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: How does doppler beaming produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the doppler beaming critical impact parameter. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: What is the 'second/third image' vocabulary of doppler beaming - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; doppler beaming naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: When do you need full Kerr doppler beaming instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; doppler beaming must support spin to be credible. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What determines the visual shadow size in doppler beaming - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in doppler beaming is the photon ring. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How do you parallelize doppler beaming - justify your answer with a concrete production example.
**A:** Every pixel is an independent doppler beaming problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: What is the most common bug in doppler beaming - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; doppler beaming needs golden-image regression tests. A concrete example: consistently applying doppler beaming in code review and regression tests keeps the whole pipeline trustworthy.
