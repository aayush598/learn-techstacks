# Gr Ray Tracing — Gravitational Lensing Interview Questions and Answers

## Q1: What is gravitational lensing in the ray-tracing context?
**A:** The bending and focusing of light by the hole's spacetime geometry itself, producing multiple images, Einstein rings, and the shadow - all emergent from geodesic integration.

## Q2: What is the basic quantity (the 'lens map')?
**A:** A mapping from source coordinates to image coordinates (direction of arrival), induced by the geometry; strong lensing near the photon sphere is its wild limit.

## Q3: What are the classic signatures?
**A:** Deflection angles, magnification, multiple images (photon-ring copies), Einstein rings around lines-of-sight, and the central shadow.

## Q4: What is critical/magnification contrast?
**A:** Where the lens map folds (caustics/critical curves), the local magnification diverges - making ring/caustic folds the brightest structures in images.

## Q5: How does a black hole lens differ from a galaxy lens?
**A:** Galaxy-scale lensing multiplies thin lenses' potential; a hole's full strong-field geometry bends rays even within the shadow - the extreme multiplicity limit.

## Q6: How does the photon-ring become a sequence of Einstein rings?
**A:** Different winding numbers produce copies of the source at geometrically smaller radii - a chain of Einstein rings nested around the shadow boundary.

## Q7: What is 'secondary' image?
**A:** Light from the far side reaching the observer over the top/bottom of the hole - the bright 'arch' spanning the north of the shadow.

## Q8: How does the observer's inclination matter?
**A:** Edge-on views (i~90 deg) show the arch with maximal asymmetry; near-face-on (i~0) the shadow trends circular - inclination is a fit parameter of the image.

## Q9: What is magnification in the intensity picture?
**A:** The intensity ratio image/source equals the inverse Jacobian of the lens map; the code obtains it implicitly via the ray integral weighting.

## Q10: How do you render lensed intensity?
**A:** Each ray accumulates emissivity*transmission(redshift) along its path; magnification appears naturally as rays compress - no explicit Jacobian needed in Monte Carlo.

## Q11: What makes the lensing observable 'robust'?
**A:** The shadow/ring occur for ANY disk: their shape depends almost entirely on (M, a, inclination), not on the emitter - making them excellent event-horizon-telescope probes.

## Q12: What is the effective distance scaling?
**A:** Angles scale with M/D; ray-tracing naturally produces the geometry and the code only maps to the sky using the observed size (scaling).

## Q13: How do you fit a real EHT image in this code?
**A:** Simulate the (a, i, M/D) portrait; the resulting shadow/ring parametrize the observed radiation - a forward model for parameter estimation.

## Q14: What are the lensing qualitative tests for the visualizer?
**A:** Verify: ring continuous, shadow boundary closed, far-side disk appears flipped (secondary), edge-on shows two distinct arcs - quick sanity of the geometry module.

## Q15: What is the ultimate quality gate of lensing?
**A:** Overlay analytic shadow silhouette (from V_r) on the rendered image: pixel-accurate match at b_crit is the definitive lensing validation.

## Q16: What does gravitational lensing concretely do inside the raytracer?
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic.

## Q17: Why is gravitational lensing the heart of a black-hole visualizer?
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how gravitational lensing bends and time-shifts each ray.

## Q18: How is gravitational lensing implemented on the GPU?
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through gravitational lensing until the ray is captured or escapes.

## Q19: What are the two families of integration for gravitational lensing?
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; gravitational lensing chooses per codebase.

## Q20: How do you validate gravitational lensing?
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures.

## Q21: What is the typical step-size strategy in gravitational lensing?
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where gravitational lensing gradients are steepest and error grows fastest.

## Q22: What state does the integrator track for gravitational lensing?
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - gravitational lensing state vector is small enough to fit in registers.

## Q23: How does gravitational lensing handle captured photons?
**A:** It terminates integration at the horizon and records absorption; gravitational lensing distinguishes capture from scatter by the radial turning point.

## Q24: What role do conserved constants play in gravitational lensing?
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding gravitational lensing for large image grids.

## Q25: Describe the numerical error budget of gravitational lensing.
**A:** Per-step truncation error and accumulated drift; gravitational lensing budgets a relative tolerance and verifies the final image is stable.

## Q26: How does gravitational lensing map the sky to the image plane?
**A:** Each image pixel defines an initial direction; gravitational lensing evolves that direction backward in time until it leaves the domain to a background sky or hits the disk.

## Q27: What is the most common bug in gravitational lensing?
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; gravitational lensing needs golden-image regression tests.

## Q28: How do you parallelize gravitational lensing?
**A:** Every pixel is an independent gravitational lensing problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication.

## Q29: What determines the visual shadow size in gravitational lensing?
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in gravitational lensing is the photon ring.

## Q30: When do you need full Kerr gravitational lensing instead of Schwarzschild?
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; gravitational lensing must support spin to be credible.

## Q31: What is the 'second/third image' vocabulary of gravitational lensing?
**A:** Light winding around the black hole produces multiple images; gravitational lensing naturally produces the primary, secondary, and higher-order photon ring.

## Q32: How does gravitational lensing produce the bright thin ring?
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the gravitational lensing critical impact parameter.

## Q33: How does gravitational lensing decide frequencies for render?
**A:** It integrates the redshift factor along the ray; gravitational lensing multiplies emitted frequency by it before applying the transfer equation.

## Q34: What modes does gravitational lensing render the accretion disk?
**A:** First as a geometric emitter grid, later using GRMHD data; gravitational lensing is agnostic to the source as long as it can query emissivity along the path.

## Q35: How is gravitational lensing performance quantified?
**A:** Mega-rays per second and time per frame; gravitational lensing usually spends its budget in the integration loop, so its step count is the key metric.

## Q36: What is the effect of camera position in gravitational lensing?
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; gravitational lensing validates each against known renders.

## Q37: How does gravitational lensing incorporate the disk's fluid velocity?
**A:** Doppler and beaming appear when the emissivity frame is boosted; gravitational lensing applies that boost per photon ray path segment.

## Q38: What is the horizon-catching strategy in gravitational lensing?
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; gravitational lensing then terminates that lane.

## Q39: How should you commission gravitational lensing output?
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent.

## Q40: How should you commission gravitational lensing output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is the horizon-catching strategy in gravitational lensing - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; gravitational lensing then terminates that lane. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How does gravitational lensing incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; gravitational lensing applies that boost per photon ray path segment. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What is the effect of camera position in gravitational lensing - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; gravitational lensing validates each against known renders. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How is gravitational lensing performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; gravitational lensing usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What modes does gravitational lensing render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; gravitational lensing is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does gravitational lensing decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; gravitational lensing multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: How does gravitational lensing produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the gravitational lensing critical impact parameter. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: What is the 'second/third image' vocabulary of gravitational lensing - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; gravitational lensing naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: When do you need full Kerr gravitational lensing instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; gravitational lensing must support spin to be credible. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What determines the visual shadow size in gravitational lensing - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in gravitational lensing is the photon ring. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How do you parallelize gravitational lensing - justify your answer with a concrete production example.
**A:** Every pixel is an independent gravitational lensing problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: What is the most common bug in gravitational lensing - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; gravitational lensing needs golden-image regression tests. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: How does gravitational lensing map the sky to the image plane - justify your answer with a concrete production example.
**A:** Each image pixel defines an initial direction; gravitational lensing evolves that direction backward in time until it leaves the domain to a background sky or hits the disk. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: Describe the numerical error budget of gravitational lensing - justify your answer with a concrete production example.
**A:** Per-step truncation error and accumulated drift; gravitational lensing budgets a relative tolerance and verifies the final image is stable. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What role do conserved constants play in gravitational lensing - justify your answer with a concrete production example.
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding gravitational lensing for large image grids. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: How does gravitational lensing handle captured photons - justify your answer with a concrete production example.
**A:** It terminates integration at the horizon and records absorption; gravitational lensing distinguishes capture from scatter by the radial turning point. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: What state does the integrator track for gravitational lensing - justify your answer with a concrete production example.
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - gravitational lensing state vector is small enough to fit in registers. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the typical step-size strategy in gravitational lensing - justify your answer with a concrete production example.
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where gravitational lensing gradients are steepest and error grows fastest. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How do you validate gravitational lensing - justify your answer with a concrete production example.
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What are the two families of integration for gravitational lensing - justify your answer with a concrete production example.
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; gravitational lensing chooses per codebase. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: How is gravitational lensing implemented on the GPU - justify your answer with a concrete production example.
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through gravitational lensing until the ray is captured or escapes. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why is gravitational lensing the heart of a black-hole visualizer - justify your answer with a concrete production example.
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how gravitational lensing bends and time-shifts each ray. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What does gravitational lensing concretely do inside the raytracer - justify your answer with a concrete production example.
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What does gravitational lensing concretely do inside the raytracer - justify your answer with a concrete production example.
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why is gravitational lensing the heart of a black-hole visualizer - justify your answer with a concrete production example.
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how gravitational lensing bends and time-shifts each ray. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: How is gravitational lensing implemented on the GPU - justify your answer with a concrete production example.
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through gravitational lensing until the ray is captured or escapes. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What are the two families of integration for gravitational lensing - justify your answer with a concrete production example.
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; gravitational lensing chooses per codebase. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How do you validate gravitational lensing - justify your answer with a concrete production example.
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What is the typical step-size strategy in gravitational lensing - justify your answer with a concrete production example.
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where gravitational lensing gradients are steepest and error grows fastest. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: What state does the integrator track for gravitational lensing - justify your answer with a concrete production example.
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - gravitational lensing state vector is small enough to fit in registers. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: How does gravitational lensing handle captured photons - justify your answer with a concrete production example.
**A:** It terminates integration at the horizon and records absorption; gravitational lensing distinguishes capture from scatter by the radial turning point. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What role do conserved constants play in gravitational lensing - justify your answer with a concrete production example.
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding gravitational lensing for large image grids. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: Describe the numerical error budget of gravitational lensing - justify your answer with a concrete production example.
**A:** Per-step truncation error and accumulated drift; gravitational lensing budgets a relative tolerance and verifies the final image is stable. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: How does gravitational lensing map the sky to the image plane - justify your answer with a concrete production example.
**A:** Each image pixel defines an initial direction; gravitational lensing evolves that direction backward in time until it leaves the domain to a background sky or hits the disk. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: What is the most common bug in gravitational lensing - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; gravitational lensing needs golden-image regression tests. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How do you parallelize gravitational lensing - justify your answer with a concrete production example.
**A:** Every pixel is an independent gravitational lensing problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What determines the visual shadow size in gravitational lensing - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in gravitational lensing is the photon ring. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: When do you need full Kerr gravitational lensing instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; gravitational lensing must support spin to be credible. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What is the 'second/third image' vocabulary of gravitational lensing - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; gravitational lensing naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How does gravitational lensing produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the gravitational lensing critical impact parameter. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does gravitational lensing decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; gravitational lensing multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What modes does gravitational lensing render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; gravitational lensing is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How is gravitational lensing performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; gravitational lensing usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What is the effect of camera position in gravitational lensing - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; gravitational lensing validates each against known renders. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How does gravitational lensing incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; gravitational lensing applies that boost per photon ray path segment. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the horizon-catching strategy in gravitational lensing - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; gravitational lensing then terminates that lane. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How should you commission gravitational lensing output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How should you commission gravitational lensing output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is the horizon-catching strategy in gravitational lensing - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; gravitational lensing then terminates that lane. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How does gravitational lensing incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; gravitational lensing applies that boost per photon ray path segment. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What is the effect of camera position in gravitational lensing - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; gravitational lensing validates each against known renders. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How is gravitational lensing performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; gravitational lensing usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What modes does gravitational lensing render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; gravitational lensing is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does gravitational lensing decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; gravitational lensing multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: How does gravitational lensing produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the gravitational lensing critical impact parameter. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: What is the 'second/third image' vocabulary of gravitational lensing - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; gravitational lensing naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: When do you need full Kerr gravitational lensing instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; gravitational lensing must support spin to be credible. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What determines the visual shadow size in gravitational lensing - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in gravitational lensing is the photon ring. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How do you parallelize gravitational lensing - justify your answer with a concrete production example.
**A:** Every pixel is an independent gravitational lensing problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: What is the most common bug in gravitational lensing - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; gravitational lensing needs golden-image regression tests. A concrete example: consistently applying gravitational lensing in code review and regression tests keeps the whole pipeline trustworthy.
