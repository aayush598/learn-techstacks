# Gr Ray Tracing — Capture And Scatter Interview Questions and Answers

## Q1: What is capture?
**A:** A ray whose impact parameter is small enough reaches the horizon and is trapped - ending as 'shadow' in the image.

## Q2: What is scatter?
**A:** A ray with large enough b avoids the hole and escapes to the observer, bringing with it lensed/scattered images of the source.

## Q3: What is the capture boundary?
**A:** The b_crit(gamma) curve in the image plane that separates capture from scatter - exactly the shadow silhouette.

## Q4: How does b_crit depend on spin and angle?
**A:** For a>0 the prograde b_crit is smaller than retrograde; the boundary becomes offset/asymmetric - visible as the crescent shadow.

## Q5: How is capture detected in the ray loop?
**A:** The integrator returns a flag when r crosses below r+ plus margin (capture) instead of a hit - pixels where all rays capture are pure shadow.

## Q6: What is the half-angle resolution near the boundary?
**A:** Rays exponentially closer to b_crit wind more; without adaptive sampling a dozen-pixel fuzz appears - mitigated by supersample and exact-boundary seeding.

## Q7: What is the relation of capture to the disk emission?
**A:** Nested images of the near disk all sit inside/around the ring; emission at the center of the shadow is entirely lensed disk up over the top (the secondary arch).

## Q8: What is scatter in scattering-language?
**A:** Rays that pass r_min(b, gamma) with b > b_crit emerge deflected by (r_min-dependent) angle - the lens map's domain is the scattered parameter space.

## Q9: How do you map captured fraction?
**A:** Grid the image into (b, gamma) and test capture analytically (V_r discriminant) - the shadow equation can be solved without any integration.

## Q10: What is the Doppler/capture interplay?
**A:** Relativistic beaming tilts where the brightest capture-adjacent photons land (the bright crescent), but the SHADOW EDGE itself stays at b_crit - a clean separation.

## Q11: What is a near-capture latency effect?
**A:** Photons hugging b_crit have enormous arrival delays - the source appears stretched in time; relevant for variability of the innermost ring.

## Q12: What is the spin-dependence test?
**A:** At a=M, prograde b_crit approaches ~M^1/2-ish; the crescent boundary distorts maximally - the strongest spin-contrast observable.

## Q13: How do you derive b_crit from V_r?
**A:** Solve V_r = V_r' = 0 simultaneously for (r_ph, b_crit) and repeat over gamma via Q; the resulting closed path is the shadow silhouette formula.

## Q14: How does a renderer decide supersampling?
**A:** Only pixels near the smooth capture boundary need extra rays; the rest of the image-fire samples then - the cost-accuracy sweet spot.

## Q15: How do you validate capture vs scatter?
**A:** For known (b, gamma) predict the classification analytically (discriminant) and cross-check with 50% supersampled integrals - bug-free boundary code.

## Q16: What does capture and scatter concretely do inside the raytracer?
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic.

## Q17: Why is capture and scatter the heart of a black-hole visualizer?
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how capture and scatter bends and time-shifts each ray.

## Q18: How is capture and scatter implemented on the GPU?
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through capture and scatter until the ray is captured or escapes.

## Q19: What are the two families of integration for capture and scatter?
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; capture and scatter chooses per codebase.

## Q20: How do you validate capture and scatter?
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures.

## Q21: What is the typical step-size strategy in capture and scatter?
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where capture and scatter gradients are steepest and error grows fastest.

## Q22: What state does the integrator track for capture and scatter?
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - capture and scatter state vector is small enough to fit in registers.

## Q23: How does capture and scatter handle captured photons?
**A:** It terminates integration at the horizon and records absorption; capture and scatter distinguishes capture from scatter by the radial turning point.

## Q24: What role do conserved constants play in capture and scatter?
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding capture and scatter for large image grids.

## Q25: Describe the numerical error budget of capture and scatter.
**A:** Per-step truncation error and accumulated drift; capture and scatter budgets a relative tolerance and verifies the final image is stable.

## Q26: How does capture and scatter map the sky to the image plane?
**A:** Each image pixel defines an initial direction; capture and scatter evolves that direction backward in time until it leaves the domain to a background sky or hits the disk.

## Q27: What is the most common bug in capture and scatter?
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; capture and scatter needs golden-image regression tests.

## Q28: How do you parallelize capture and scatter?
**A:** Every pixel is an independent capture and scatter problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication.

## Q29: What determines the visual shadow size in capture and scatter?
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in capture and scatter is the photon ring.

## Q30: When do you need full Kerr capture and scatter instead of Schwarzschild?
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; capture and scatter must support spin to be credible.

## Q31: What is the 'second/third image' vocabulary of capture and scatter?
**A:** Light winding around the black hole produces multiple images; capture and scatter naturally produces the primary, secondary, and higher-order photon ring.

## Q32: How does capture and scatter produce the bright thin ring?
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the capture and scatter critical impact parameter.

## Q33: How does capture and scatter decide frequencies for render?
**A:** It integrates the redshift factor along the ray; capture and scatter multiplies emitted frequency by it before applying the transfer equation.

## Q34: What modes does capture and scatter render the accretion disk?
**A:** First as a geometric emitter grid, later using GRMHD data; capture and scatter is agnostic to the source as long as it can query emissivity along the path.

## Q35: How is capture and scatter performance quantified?
**A:** Mega-rays per second and time per frame; capture and scatter usually spends its budget in the integration loop, so its step count is the key metric.

## Q36: What is the effect of camera position in capture and scatter?
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; capture and scatter validates each against known renders.

## Q37: How does capture and scatter incorporate the disk's fluid velocity?
**A:** Doppler and beaming appear when the emissivity frame is boosted; capture and scatter applies that boost per photon ray path segment.

## Q38: What is the horizon-catching strategy in capture and scatter?
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; capture and scatter then terminates that lane.

## Q39: How should you commission capture and scatter output?
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent.

## Q40: How should you commission capture and scatter output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is the horizon-catching strategy in capture and scatter - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; capture and scatter then terminates that lane. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How does capture and scatter incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; capture and scatter applies that boost per photon ray path segment. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What is the effect of camera position in capture and scatter - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; capture and scatter validates each against known renders. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How is capture and scatter performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; capture and scatter usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What modes does capture and scatter render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; capture and scatter is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does capture and scatter decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; capture and scatter multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: How does capture and scatter produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the capture and scatter critical impact parameter. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: What is the 'second/third image' vocabulary of capture and scatter - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; capture and scatter naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: When do you need full Kerr capture and scatter instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; capture and scatter must support spin to be credible. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What determines the visual shadow size in capture and scatter - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in capture and scatter is the photon ring. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How do you parallelize capture and scatter - justify your answer with a concrete production example.
**A:** Every pixel is an independent capture and scatter problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: What is the most common bug in capture and scatter - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; capture and scatter needs golden-image regression tests. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: How does capture and scatter map the sky to the image plane - justify your answer with a concrete production example.
**A:** Each image pixel defines an initial direction; capture and scatter evolves that direction backward in time until it leaves the domain to a background sky or hits the disk. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: Describe the numerical error budget of capture and scatter - justify your answer with a concrete production example.
**A:** Per-step truncation error and accumulated drift; capture and scatter budgets a relative tolerance and verifies the final image is stable. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What role do conserved constants play in capture and scatter - justify your answer with a concrete production example.
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding capture and scatter for large image grids. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: How does capture and scatter handle captured photons - justify your answer with a concrete production example.
**A:** It terminates integration at the horizon and records absorption; capture and scatter distinguishes capture from scatter by the radial turning point. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: What state does the integrator track for capture and scatter - justify your answer with a concrete production example.
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - capture and scatter state vector is small enough to fit in registers. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the typical step-size strategy in capture and scatter - justify your answer with a concrete production example.
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where capture and scatter gradients are steepest and error grows fastest. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How do you validate capture and scatter - justify your answer with a concrete production example.
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What are the two families of integration for capture and scatter - justify your answer with a concrete production example.
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; capture and scatter chooses per codebase. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: How is capture and scatter implemented on the GPU - justify your answer with a concrete production example.
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through capture and scatter until the ray is captured or escapes. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why is capture and scatter the heart of a black-hole visualizer - justify your answer with a concrete production example.
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how capture and scatter bends and time-shifts each ray. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What does capture and scatter concretely do inside the raytracer - justify your answer with a concrete production example.
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What does capture and scatter concretely do inside the raytracer - justify your answer with a concrete production example.
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why is capture and scatter the heart of a black-hole visualizer - justify your answer with a concrete production example.
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how capture and scatter bends and time-shifts each ray. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: How is capture and scatter implemented on the GPU - justify your answer with a concrete production example.
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through capture and scatter until the ray is captured or escapes. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What are the two families of integration for capture and scatter - justify your answer with a concrete production example.
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; capture and scatter chooses per codebase. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How do you validate capture and scatter - justify your answer with a concrete production example.
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What is the typical step-size strategy in capture and scatter - justify your answer with a concrete production example.
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where capture and scatter gradients are steepest and error grows fastest. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: What state does the integrator track for capture and scatter - justify your answer with a concrete production example.
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - capture and scatter state vector is small enough to fit in registers. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: How does capture and scatter handle captured photons - justify your answer with a concrete production example.
**A:** It terminates integration at the horizon and records absorption; capture and scatter distinguishes capture from scatter by the radial turning point. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What role do conserved constants play in capture and scatter - justify your answer with a concrete production example.
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding capture and scatter for large image grids. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: Describe the numerical error budget of capture and scatter - justify your answer with a concrete production example.
**A:** Per-step truncation error and accumulated drift; capture and scatter budgets a relative tolerance and verifies the final image is stable. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: How does capture and scatter map the sky to the image plane - justify your answer with a concrete production example.
**A:** Each image pixel defines an initial direction; capture and scatter evolves that direction backward in time until it leaves the domain to a background sky or hits the disk. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: What is the most common bug in capture and scatter - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; capture and scatter needs golden-image regression tests. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How do you parallelize capture and scatter - justify your answer with a concrete production example.
**A:** Every pixel is an independent capture and scatter problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What determines the visual shadow size in capture and scatter - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in capture and scatter is the photon ring. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: When do you need full Kerr capture and scatter instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; capture and scatter must support spin to be credible. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What is the 'second/third image' vocabulary of capture and scatter - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; capture and scatter naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How does capture and scatter produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the capture and scatter critical impact parameter. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does capture and scatter decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; capture and scatter multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What modes does capture and scatter render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; capture and scatter is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How is capture and scatter performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; capture and scatter usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What is the effect of camera position in capture and scatter - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; capture and scatter validates each against known renders. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How does capture and scatter incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; capture and scatter applies that boost per photon ray path segment. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the horizon-catching strategy in capture and scatter - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; capture and scatter then terminates that lane. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How should you commission capture and scatter output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How should you commission capture and scatter output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is the horizon-catching strategy in capture and scatter - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; capture and scatter then terminates that lane. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How does capture and scatter incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; capture and scatter applies that boost per photon ray path segment. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What is the effect of camera position in capture and scatter - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; capture and scatter validates each against known renders. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How is capture and scatter performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; capture and scatter usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What modes does capture and scatter render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; capture and scatter is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does capture and scatter decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; capture and scatter multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: How does capture and scatter produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the capture and scatter critical impact parameter. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: What is the 'second/third image' vocabulary of capture and scatter - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; capture and scatter naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: When do you need full Kerr capture and scatter instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; capture and scatter must support spin to be credible. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What determines the visual shadow size in capture and scatter - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in capture and scatter is the photon ring. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How do you parallelize capture and scatter - justify your answer with a concrete production example.
**A:** Every pixel is an independent capture and scatter problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: What is the most common bug in capture and scatter - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; capture and scatter needs golden-image regression tests. A concrete example: consistently applying capture and scatter in code review and regression tests keeps the whole pipeline trustworthy.
