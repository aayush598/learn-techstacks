# Gr Ray Tracing — Carter Constant Interview Questions and Answers

## Q1: What is the Carter constant?
**A:** A fourth constant of Kerr geodesic motion (beyond E, L, and unit mass) arising from the separability of the Hamilton-Jacobi equation - it tames the theta-motion.

## Q2: What is its explicit form for photons?
**A:** Q = p_theta^2 + cos^2 theta (a^2 E^2 - L^2/sin^2 theta) (plus a mass term for massive particles); it is constant along null geodesics.

## Q3: Why is it 'not trivial'?
**A:** Unlike E and L (from symmetries), Q comes from a hidden separability symmetry - no corresponding Killing vector exists in general, only the Killing tensor.

## Q4: How does Q constrain rays?
**A:** With (E, L, Q) the r and theta equations separate into ordinary differential inequalities; the image is completely classified by the triple.

## Q5: What is the Killing tensor's role?
**A:** K^mu,nu p_mu p_nu = Q + (L - aE)^2; K is the conserved quantity of the Killing-Yano tensor - the deeper geometric origin.

## Q6: How do you compute Q in code?
**A:** From p_theta, p_phi, E at launch: Q = p_theta^2 + cos^2(theta)[...]; monitor it along integration as a built-in correctness check.

## Q7: What happens to Q for equatorial rays?
**A:** On theta=pi/2, Q = p_theta^2 = 0 - equatorial rays are the Q=0 family; the shadow's equatorial boundary corresponds to Q=0 hits.

## Q8: How does Q map to image coordinates?
**A:** The impact parameters b = L/E and gamma such that Q = E^2 (b-something)^2 maps image polar coordinates to (Q, L) - the shadow equation in those terms.

## Q9: What is the separability trick?
**A:** Reduced motion is governed by two independent 1-D potentials from Hamilton-Jacobi; the constants (E,L,Q) fix everything - used by separation-integration codes.

## Q10: How does Q change with L for turning points?
**A:** Theta turnarounds occur where the effective theta-eq Q_bounds switch sign; real geodesics exist iff Q is in the allowed interval at each r.

## Q11: Why is Q so valuable for validation?
**A:** Its conservation is a built-in error monitor: any drift in the Q-accurate trajectory is an integrator defect, not physics.

## Q12: What is Q's sign/range?
**A:** Q >= 0 for equatorial-type orbits (with L^2 >= 0 limit); some formalizations use the normalized, dimensionless auxiliaries leading to valid mapping.

## Q13: How does the code use Q analytically?
**A:** Radius solutions r_r of the effective potential depend on Q; the photon-sphere/ring positions for given (a, direction) are functions of Q - solving them predicts rings.

## Q14: What is the Kerr shadow equation in Q/b terms?
**A:** b_crit(L_or_Q) traces the boundary curve; the classic Stern-Gibson formula for the silhouette uses Q=0 for the equatorial boundary then the general Q.

## Q15: What is the practical takeaway?
**A:** Full 8-D integration conserves Q automatically to integration tolerance; reduced (separated) integration USES Q as an input - both paths are legitimate, documented choices.

## Q16: What does carter constant concretely do inside the raytracer?
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic.

## Q17: Why is carter constant the heart of a black-hole visualizer?
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how carter constant bends and time-shifts each ray.

## Q18: How is carter constant implemented on the GPU?
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through carter constant until the ray is captured or escapes.

## Q19: What are the two families of integration for carter constant?
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; carter constant chooses per codebase.

## Q20: How do you validate carter constant?
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures.

## Q21: What is the typical step-size strategy in carter constant?
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where carter constant gradients are steepest and error grows fastest.

## Q22: What state does the integrator track for carter constant?
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - carter constant state vector is small enough to fit in registers.

## Q23: How does carter constant handle captured photons?
**A:** It terminates integration at the horizon and records absorption; carter constant distinguishes capture from scatter by the radial turning point.

## Q24: What role do conserved constants play in carter constant?
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding carter constant for large image grids.

## Q25: Describe the numerical error budget of carter constant.
**A:** Per-step truncation error and accumulated drift; carter constant budgets a relative tolerance and verifies the final image is stable.

## Q26: How does carter constant map the sky to the image plane?
**A:** Each image pixel defines an initial direction; carter constant evolves that direction backward in time until it leaves the domain to a background sky or hits the disk.

## Q27: What is the most common bug in carter constant?
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; carter constant needs golden-image regression tests.

## Q28: How do you parallelize carter constant?
**A:** Every pixel is an independent carter constant problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication.

## Q29: What determines the visual shadow size in carter constant?
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in carter constant is the photon ring.

## Q30: When do you need full Kerr carter constant instead of Schwarzschild?
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; carter constant must support spin to be credible.

## Q31: What is the 'second/third image' vocabulary of carter constant?
**A:** Light winding around the black hole produces multiple images; carter constant naturally produces the primary, secondary, and higher-order photon ring.

## Q32: How does carter constant produce the bright thin ring?
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the carter constant critical impact parameter.

## Q33: How does carter constant decide frequencies for render?
**A:** It integrates the redshift factor along the ray; carter constant multiplies emitted frequency by it before applying the transfer equation.

## Q34: What modes does carter constant render the accretion disk?
**A:** First as a geometric emitter grid, later using GRMHD data; carter constant is agnostic to the source as long as it can query emissivity along the path.

## Q35: How is carter constant performance quantified?
**A:** Mega-rays per second and time per frame; carter constant usually spends its budget in the integration loop, so its step count is the key metric.

## Q36: What is the effect of camera position in carter constant?
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; carter constant validates each against known renders.

## Q37: How does carter constant incorporate the disk's fluid velocity?
**A:** Doppler and beaming appear when the emissivity frame is boosted; carter constant applies that boost per photon ray path segment.

## Q38: What is the horizon-catching strategy in carter constant?
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; carter constant then terminates that lane.

## Q39: How should you commission carter constant output?
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent.

## Q40: How should you commission carter constant output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is the horizon-catching strategy in carter constant - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; carter constant then terminates that lane. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How does carter constant incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; carter constant applies that boost per photon ray path segment. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What is the effect of camera position in carter constant - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; carter constant validates each against known renders. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How is carter constant performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; carter constant usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What modes does carter constant render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; carter constant is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does carter constant decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; carter constant multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: How does carter constant produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the carter constant critical impact parameter. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: What is the 'second/third image' vocabulary of carter constant - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; carter constant naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: When do you need full Kerr carter constant instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; carter constant must support spin to be credible. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What determines the visual shadow size in carter constant - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in carter constant is the photon ring. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How do you parallelize carter constant - justify your answer with a concrete production example.
**A:** Every pixel is an independent carter constant problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: What is the most common bug in carter constant - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; carter constant needs golden-image regression tests. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: How does carter constant map the sky to the image plane - justify your answer with a concrete production example.
**A:** Each image pixel defines an initial direction; carter constant evolves that direction backward in time until it leaves the domain to a background sky or hits the disk. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: Describe the numerical error budget of carter constant - justify your answer with a concrete production example.
**A:** Per-step truncation error and accumulated drift; carter constant budgets a relative tolerance and verifies the final image is stable. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What role do conserved constants play in carter constant - justify your answer with a concrete production example.
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding carter constant for large image grids. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: How does carter constant handle captured photons - justify your answer with a concrete production example.
**A:** It terminates integration at the horizon and records absorption; carter constant distinguishes capture from scatter by the radial turning point. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: What state does the integrator track for carter constant - justify your answer with a concrete production example.
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - carter constant state vector is small enough to fit in registers. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the typical step-size strategy in carter constant - justify your answer with a concrete production example.
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where carter constant gradients are steepest and error grows fastest. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How do you validate carter constant - justify your answer with a concrete production example.
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What are the two families of integration for carter constant - justify your answer with a concrete production example.
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; carter constant chooses per codebase. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: How is carter constant implemented on the GPU - justify your answer with a concrete production example.
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through carter constant until the ray is captured or escapes. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why is carter constant the heart of a black-hole visualizer - justify your answer with a concrete production example.
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how carter constant bends and time-shifts each ray. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What does carter constant concretely do inside the raytracer - justify your answer with a concrete production example.
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What does carter constant concretely do inside the raytracer - justify your answer with a concrete production example.
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why is carter constant the heart of a black-hole visualizer - justify your answer with a concrete production example.
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how carter constant bends and time-shifts each ray. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: How is carter constant implemented on the GPU - justify your answer with a concrete production example.
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through carter constant until the ray is captured or escapes. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What are the two families of integration for carter constant - justify your answer with a concrete production example.
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; carter constant chooses per codebase. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How do you validate carter constant - justify your answer with a concrete production example.
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What is the typical step-size strategy in carter constant - justify your answer with a concrete production example.
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where carter constant gradients are steepest and error grows fastest. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: What state does the integrator track for carter constant - justify your answer with a concrete production example.
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - carter constant state vector is small enough to fit in registers. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: How does carter constant handle captured photons - justify your answer with a concrete production example.
**A:** It terminates integration at the horizon and records absorption; carter constant distinguishes capture from scatter by the radial turning point. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What role do conserved constants play in carter constant - justify your answer with a concrete production example.
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding carter constant for large image grids. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: Describe the numerical error budget of carter constant - justify your answer with a concrete production example.
**A:** Per-step truncation error and accumulated drift; carter constant budgets a relative tolerance and verifies the final image is stable. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: How does carter constant map the sky to the image plane - justify your answer with a concrete production example.
**A:** Each image pixel defines an initial direction; carter constant evolves that direction backward in time until it leaves the domain to a background sky or hits the disk. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: What is the most common bug in carter constant - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; carter constant needs golden-image regression tests. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How do you parallelize carter constant - justify your answer with a concrete production example.
**A:** Every pixel is an independent carter constant problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What determines the visual shadow size in carter constant - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in carter constant is the photon ring. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: When do you need full Kerr carter constant instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; carter constant must support spin to be credible. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What is the 'second/third image' vocabulary of carter constant - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; carter constant naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How does carter constant produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the carter constant critical impact parameter. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does carter constant decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; carter constant multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What modes does carter constant render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; carter constant is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How is carter constant performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; carter constant usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What is the effect of camera position in carter constant - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; carter constant validates each against known renders. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How does carter constant incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; carter constant applies that boost per photon ray path segment. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the horizon-catching strategy in carter constant - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; carter constant then terminates that lane. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How should you commission carter constant output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How should you commission carter constant output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is the horizon-catching strategy in carter constant - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; carter constant then terminates that lane. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How does carter constant incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; carter constant applies that boost per photon ray path segment. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What is the effect of camera position in carter constant - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; carter constant validates each against known renders. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How is carter constant performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; carter constant usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What modes does carter constant render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; carter constant is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does carter constant decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; carter constant multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: How does carter constant produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the carter constant critical impact parameter. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: What is the 'second/third image' vocabulary of carter constant - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; carter constant naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: When do you need full Kerr carter constant instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; carter constant must support spin to be credible. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What determines the visual shadow size in carter constant - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in carter constant is the photon ring. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How do you parallelize carter constant - justify your answer with a concrete production example.
**A:** Every pixel is an independent carter constant problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: What is the most common bug in carter constant - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; carter constant needs golden-image regression tests. A concrete example: consistently applying carter constant in code review and regression tests keeps the whole pipeline trustworthy.
