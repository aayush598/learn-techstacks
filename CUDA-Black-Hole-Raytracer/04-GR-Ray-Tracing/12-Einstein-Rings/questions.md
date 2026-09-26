# Gr Ray Tracing — Einstein Rings Interview Questions and Answers

## Q1: What is an Einstein ring?
**A:** The apparent circular image of a source when the observer, source, and lens (the hole) are aligned - light from the source bent into a full annulus.

## Q2: What is the Einstein radius?
**A:** For a point mass lens, theta_E = sqrt(4GM D_ls / (c^2 D_l D_s)) (small-angle); for the hole's strong field the ring is the photon-ring-scale annulus.

## Q3: What happens in full strong-field alignment?
**A:** The Einstein ring splits into the nested ring family around the photon sphere - the hole's scharacteristic multiple-ring annulus.

## Q4: How does the code produce rings?
**A:** Rays launched on trivial b_axis directions wind around the hole at constant-lambda geometry; aligned sources magnify into continuous annuli.

## Q5: What is the caustic at perfect alignment?
**A:** The lens map degenerates (infinite magnification along a circle) forming the ring - a critical-curve caustic; physically the annulus is an image of the whole source disc.

## Q6: How large is the ring in units of M?
**A:** On the sky the ring subtends ~ (5.2 M)/D radians; the EHT famously sees the M87 ring at ~ 42 +- 3 microarcsec.

## Q7: What is the difference between the photon ring and the Einstein ring?
**A:** The Einstein ring is the aligned-lens enhancement (first order); the photon ring is the physical orbit's shadow boundary - in images they coincide to first sight, separated by n-order copies.

## Q8: Why is the ring insensitive to source details?
**A:** Its radius is set by geometry (M, a) not emissivity, so it's the robust observable; emission shape changes brightness within the ring, not its edge.

## Q9: What is the 'lensed ring' of the accretion disk?
**A:** The disk itself forms multiple arcs/ring segments - the near edge looks like a thin arc, the far edge doubled, combined into the ring feature.

## Q10: How do you render an artificial Einstein ring demo?
**A:** Place a uniform spherical source behind the hole; its aligned image is a full annulus whose boundary you compare with the analytic ring radius.

## Q11: What happens at high inclination?
**A:** The ring is no longer circular on the sky: it brightens/sharpens toward the barycentered crescent - the classic observed asymmetry.

## Q12: What is the ring's chromatic role?
**A:** Doppler+gravity shift the ring's color (blue on prograde side); the radius is achromatic - geometry dominates color contrast.

## Q13: How is the ring measured?
**A:** Diameter at the ring brightness maximum - the EHT team's defining observable, robust to emission modeling - the code outputs diameter(b_crit portrait).

## Q14: What validation closes the ring loop?
**A:** The rendered ring's diameter must match b_crit(portrait) to sub-pixel; that double-check links renderer to analytic backbone.

## Q15: What is the resolution requirement?
**A:** To resolve the ring you need 12+ pixels across the shadow; EHT used phased-array VLBI; in-simulation this is simply the sampling grid at b~5M.

## Q16: What does einstein rings concretely do inside the raytracer?
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic.

## Q17: Why is einstein rings the heart of a black-hole visualizer?
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how einstein rings bends and time-shifts each ray.

## Q18: How is einstein rings implemented on the GPU?
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through einstein rings until the ray is captured or escapes.

## Q19: What are the two families of integration for einstein rings?
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; einstein rings chooses per codebase.

## Q20: How do you validate einstein rings?
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures.

## Q21: What is the typical step-size strategy in einstein rings?
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where einstein rings gradients are steepest and error grows fastest.

## Q22: What state does the integrator track for einstein rings?
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - einstein rings state vector is small enough to fit in registers.

## Q23: How does einstein rings handle captured photons?
**A:** It terminates integration at the horizon and records absorption; einstein rings distinguishes capture from scatter by the radial turning point.

## Q24: What role do conserved constants play in einstein rings?
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding einstein rings for large image grids.

## Q25: Describe the numerical error budget of einstein rings.
**A:** Per-step truncation error and accumulated drift; einstein rings budgets a relative tolerance and verifies the final image is stable.

## Q26: How does einstein rings map the sky to the image plane?
**A:** Each image pixel defines an initial direction; einstein rings evolves that direction backward in time until it leaves the domain to a background sky or hits the disk.

## Q27: What is the most common bug in einstein rings?
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; einstein rings needs golden-image regression tests.

## Q28: How do you parallelize einstein rings?
**A:** Every pixel is an independent einstein rings problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication.

## Q29: What determines the visual shadow size in einstein rings?
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in einstein rings is the photon ring.

## Q30: When do you need full Kerr einstein rings instead of Schwarzschild?
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; einstein rings must support spin to be credible.

## Q31: What is the 'second/third image' vocabulary of einstein rings?
**A:** Light winding around the black hole produces multiple images; einstein rings naturally produces the primary, secondary, and higher-order photon ring.

## Q32: How does einstein rings produce the bright thin ring?
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the einstein rings critical impact parameter.

## Q33: How does einstein rings decide frequencies for render?
**A:** It integrates the redshift factor along the ray; einstein rings multiplies emitted frequency by it before applying the transfer equation.

## Q34: What modes does einstein rings render the accretion disk?
**A:** First as a geometric emitter grid, later using GRMHD data; einstein rings is agnostic to the source as long as it can query emissivity along the path.

## Q35: How is einstein rings performance quantified?
**A:** Mega-rays per second and time per frame; einstein rings usually spends its budget in the integration loop, so its step count is the key metric.

## Q36: What is the effect of camera position in einstein rings?
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; einstein rings validates each against known renders.

## Q37: How does einstein rings incorporate the disk's fluid velocity?
**A:** Doppler and beaming appear when the emissivity frame is boosted; einstein rings applies that boost per photon ray path segment.

## Q38: What is the horizon-catching strategy in einstein rings?
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; einstein rings then terminates that lane.

## Q39: How should you commission einstein rings output?
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent.

## Q40: How should you commission einstein rings output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is the horizon-catching strategy in einstein rings - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; einstein rings then terminates that lane. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How does einstein rings incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; einstein rings applies that boost per photon ray path segment. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What is the effect of camera position in einstein rings - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; einstein rings validates each against known renders. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How is einstein rings performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; einstein rings usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What modes does einstein rings render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; einstein rings is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does einstein rings decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; einstein rings multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: How does einstein rings produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the einstein rings critical impact parameter. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: What is the 'second/third image' vocabulary of einstein rings - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; einstein rings naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: When do you need full Kerr einstein rings instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; einstein rings must support spin to be credible. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What determines the visual shadow size in einstein rings - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in einstein rings is the photon ring. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How do you parallelize einstein rings - justify your answer with a concrete production example.
**A:** Every pixel is an independent einstein rings problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: What is the most common bug in einstein rings - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; einstein rings needs golden-image regression tests. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: How does einstein rings map the sky to the image plane - justify your answer with a concrete production example.
**A:** Each image pixel defines an initial direction; einstein rings evolves that direction backward in time until it leaves the domain to a background sky or hits the disk. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: Describe the numerical error budget of einstein rings - justify your answer with a concrete production example.
**A:** Per-step truncation error and accumulated drift; einstein rings budgets a relative tolerance and verifies the final image is stable. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What role do conserved constants play in einstein rings - justify your answer with a concrete production example.
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding einstein rings for large image grids. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: How does einstein rings handle captured photons - justify your answer with a concrete production example.
**A:** It terminates integration at the horizon and records absorption; einstein rings distinguishes capture from scatter by the radial turning point. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: What state does the integrator track for einstein rings - justify your answer with a concrete production example.
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - einstein rings state vector is small enough to fit in registers. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the typical step-size strategy in einstein rings - justify your answer with a concrete production example.
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where einstein rings gradients are steepest and error grows fastest. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How do you validate einstein rings - justify your answer with a concrete production example.
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What are the two families of integration for einstein rings - justify your answer with a concrete production example.
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; einstein rings chooses per codebase. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: How is einstein rings implemented on the GPU - justify your answer with a concrete production example.
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through einstein rings until the ray is captured or escapes. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why is einstein rings the heart of a black-hole visualizer - justify your answer with a concrete production example.
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how einstein rings bends and time-shifts each ray. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What does einstein rings concretely do inside the raytracer - justify your answer with a concrete production example.
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What does einstein rings concretely do inside the raytracer - justify your answer with a concrete production example.
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why is einstein rings the heart of a black-hole visualizer - justify your answer with a concrete production example.
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how einstein rings bends and time-shifts each ray. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: How is einstein rings implemented on the GPU - justify your answer with a concrete production example.
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through einstein rings until the ray is captured or escapes. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What are the two families of integration for einstein rings - justify your answer with a concrete production example.
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; einstein rings chooses per codebase. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How do you validate einstein rings - justify your answer with a concrete production example.
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What is the typical step-size strategy in einstein rings - justify your answer with a concrete production example.
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where einstein rings gradients are steepest and error grows fastest. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: What state does the integrator track for einstein rings - justify your answer with a concrete production example.
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - einstein rings state vector is small enough to fit in registers. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: How does einstein rings handle captured photons - justify your answer with a concrete production example.
**A:** It terminates integration at the horizon and records absorption; einstein rings distinguishes capture from scatter by the radial turning point. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What role do conserved constants play in einstein rings - justify your answer with a concrete production example.
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding einstein rings for large image grids. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: Describe the numerical error budget of einstein rings - justify your answer with a concrete production example.
**A:** Per-step truncation error and accumulated drift; einstein rings budgets a relative tolerance and verifies the final image is stable. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: How does einstein rings map the sky to the image plane - justify your answer with a concrete production example.
**A:** Each image pixel defines an initial direction; einstein rings evolves that direction backward in time until it leaves the domain to a background sky or hits the disk. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: What is the most common bug in einstein rings - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; einstein rings needs golden-image regression tests. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How do you parallelize einstein rings - justify your answer with a concrete production example.
**A:** Every pixel is an independent einstein rings problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What determines the visual shadow size in einstein rings - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in einstein rings is the photon ring. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: When do you need full Kerr einstein rings instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; einstein rings must support spin to be credible. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What is the 'second/third image' vocabulary of einstein rings - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; einstein rings naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How does einstein rings produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the einstein rings critical impact parameter. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does einstein rings decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; einstein rings multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What modes does einstein rings render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; einstein rings is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How is einstein rings performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; einstein rings usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What is the effect of camera position in einstein rings - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; einstein rings validates each against known renders. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How does einstein rings incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; einstein rings applies that boost per photon ray path segment. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the horizon-catching strategy in einstein rings - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; einstein rings then terminates that lane. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How should you commission einstein rings output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How should you commission einstein rings output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is the horizon-catching strategy in einstein rings - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; einstein rings then terminates that lane. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How does einstein rings incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; einstein rings applies that boost per photon ray path segment. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What is the effect of camera position in einstein rings - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; einstein rings validates each against known renders. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How is einstein rings performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; einstein rings usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What modes does einstein rings render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; einstein rings is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does einstein rings decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; einstein rings multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: How does einstein rings produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the einstein rings critical impact parameter. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: What is the 'second/third image' vocabulary of einstein rings - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; einstein rings naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: When do you need full Kerr einstein rings instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; einstein rings must support spin to be credible. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What determines the visual shadow size in einstein rings - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in einstein rings is the photon ring. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How do you parallelize einstein rings - justify your answer with a concrete production example.
**A:** Every pixel is an independent einstein rings problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: What is the most common bug in einstein rings - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; einstein rings needs golden-image regression tests. A concrete example: consistently applying einstein rings in code review and regression tests keeps the whole pipeline trustworthy.
