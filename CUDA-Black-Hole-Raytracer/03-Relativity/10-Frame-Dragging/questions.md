# Relativity — Frame Dragging Interview Questions and Answers

## Q1: What is frame dragging?
**A:** The rotational dragging of inertial frames by a spinning body, encoded in gravitational waves of the metric; in Kerr it appears as the t-phi coupling term.

## Q2: How is frame dragging quantified?
**A:** By the angular velocity of inertial frames: omega = -g_t,phi/g_phi,phi; the ZAMO's omega measures how fast local space 'spins' with the hole.

## Q3: What does the ZAMO see?
**A:** Constant-radius observers with zero angular momentum at infinity still revolve with angular velocity omega - the textbook signature of frame dragging.

## Q4: How does frame dragging affect photons?
**A:** Passing photons acquire a phi-component; prograde photons are dragged inward more, retrograde less - shifting the image's ring and shadow asymmetry.

## Q5: How does dragging shape the image?
**A:** The photon ring is distorted and the shadow becomes a crescent/D-shape with the bright side dragged; the asymmetry strength scales with |a| and inclination.

## Q6: What is the dragging radial profile?
**A:** omega drops as ~2Ma/r^3 at large r (the Lense-Thirring 1/r^3 law), approaching the hole's rotation rate near the horizon.

## Q7: What is 'frame-dragging' observable in the solar system?
**A:** Lense-Thirring precession of orbiting bodies (tested by Gravity Probe B ~ -2.0e-9 rad/orbit); it is the weak-field cousin of the Kerr effect.

## Q8: How does drag relate to the orbital plane precession?
**A:** The axis node of inclined orbits precesses around the hole's spin axis; strong near the horizon, weak at large r - a first test of the metric's phi-t coupling.

## Q9: What does dragging do to the ISCO and disk inner edge?
**A:** Dragging lowers the prograde ISCO; real disks therefore truncate closer for prograde - a geometric reason for the innermost emission ring asymmetry.

## Q10: How does the code compute the ZAMO basis?
**A:** zamo 4-velocity = (1/A, 0, 0, omega)/norm; the orthonormal basis for azimuthal emission uses that frame - where emissivity beaming is evaluated.

## Q11: How do you verify frame dragging numerically?
**A:** Place a photon with p_phi=0 far out at r=r0 and r'=0; it must immediately drift in phi with dphi = omega(r) dt - a direct metric-consistent check.

## Q12: What is the weak-field vs strong-field boundary?
**A:** For r >> M, a's Lense-Thirring term scales 1/r^3; the regime where dragging is a perturbation vs the dominant geometry is the strong-field hierarchy to keep in mind.

## Q13: Does the ergosphere make dragging compulsory?
**A:** Yes - inside the ergosphere the ZAMO's own speed needed exceeds a split of the light cone; no observer can resist the hole's rotation there.

## Q14: How does drag interplay with beaming in images?
**A:** The boosted emissivity follows the fluid's 4-velocity; near the hole fluid moves partly from dragging, so the beaming map � and the media visual asymmetry � encodes a.)

## Q15: What validation image isolates dragging?
**A:** Render a static cold shell around a spinning hole with no fluid; the resulting photon paths must follow the analytic ZAMO streamlines - puristic dragging signature.

## Q16: What is the physical meaning of frame dragging in general relativity?
**A:** It encodes how spacetime geometry responds to mass-energy; frame dragging ties local measurements in a freely falling frame to the global curved geometry.

## Q17: How is frame dragging expressed mathematically?
**A:** Through the metric tensor and its derivatives; frame dragging gives the equations of motion for particles and light as geodesics of that metric.

## Q18: Why does frame dragging matter for a black-hole raytracer?
**A:** Photons follow null geodesics of the Kerr geometry; frame dragging tells you exactly how to advance a ray in Boyer-Lindquist coordinates.

## Q19: What is the intuition behind frame dragging for a beginner?
**A:** Spacetime tells matter how to move and matter tells spacetime how to curve; frame dragging is the first concrete step of that program.

## Q20: How do you verify a calculation of frame dragging?
**A:** Take non-relativistic or weak-field limits, compare with known analytic results such as light bending, and check conservation laws numerically.

## Q21: How does frame dragging connect to special relativity?
**A:** In the absence of gravity the metric is Minkowski, and frame dragging reduces to Lorentz transformations and the usual Doppler formulas.

## Q22: What are the units and conventions for frame dragging?
**A:** geometric units with c=G=1 make masses length-like; careful sign conventions (mostly-plus vs mostly-minus) pervade frame dragging formulas.

## Q23: Give the classic demonstrative example of frame dragging.
**A:** A light ray grazing the Sun bends by 1.75 arcseconds; exact frame dragging reproduces this and more dramatic bending near a horizon.

## Q24: What is a common misconception about frame dragging?
**A:** That gravity is a force deflecting light; really frame dragging is geometry: light follows the straightest possible path in curved spacetime.

## Q25: How does frame dragging generalize for rotating black holes?
**A:** The stationary axisymmetric Kerr metric replaces spherical symmetry; frame dragging gains a spin parameter and frame dragging enters.

## Q26: What physical predictions come straight from frame dragging?
**A:** Gravitational redshift, perihelion precession, light bending, frame dragging, and orbital decay from gravitational waves are all frame dragging consequences.

## Q27: What is the role of conserved quantities in frame dragging?
**A:** Symmetries of the metric give constants along geodesics - energy, angular momentum, and (in Kerr) the Carter constant - which frame dragging uses to integrate efficiently.

## Q28: How would a detector measure effects of frame dragging?
**A:** Comparing clock rates, precision astrometry, or the shape of the photon ring all isolate signatures of frame dragging.

## Q29: What numerical care does frame dragging require?
**A:** The metric functions diverge at horizons and the coordinate singularities; switching to Kerr-Schild coordinates stabilizes frame dragging integration.

## Q30: How does frame dragging guide frame transformations in rendering?
**A:** Radiation emitted in the fluid frame must be Lorentz-transformed to the coordinate frame; frame dragging supplies the needed boost toward a locally non-rotating observer.

## Q31: Why start with Schwarzschild before Kerr for frame dragging?
**A:** Schwarzschild is spherically symmetric with simple constants, so frame dragging concepts are demonstrated and validated before spin complicates them.

## Q32: What is the embedding-diagram view of frame dragging?
**A:** A 2D slice of the geometry drawn inside a fictional flat space shows the funnel shape that beginners intuitively associate with frame dragging.

## Q33: What limits are placed by frame dragging on observables?
**A:** Nothing escapes inside the horizon; the photon sphere at 1.5 Schwarzschild radii bounds where frame dragging says circular light orbits exist.

## Q34: How do you test the weak-field limit of frame dragging?
**A:** Expanding the metric at large radius must recover Newtonian gravity plus the leading post-Newtonian corrections - the sanity check for frame dragging.

## Q35: What does frame dragging say about time near a black hole?
**A:** Clocks run slower deeper in the potential; frame dragging quantifies the ratio for a distant observer as the inverse redshift factor.

## Q36: How is frame dragging typically mis-stated in pop science?
**A:** As 'light has no mass so how does gravity pull it' - frame dragging reframes it as path curvature, not a force on mass.

## Q37: What documentation accompanies frame dragging in a research code?
**A:** Every derivation, coordinate convention, and unit choice for frame dragging is written down so the integrator can be audited.

## Q38: Give one number a beginner should memorize for frame dragging.
**A:** The photon sphere radius 3GM/C^2 (1.5 Schwarzschild radii) beyond which frame dragging orbiting light is possible.

## Q39: What is the next step after mastering frame dragging?
**A:** Coding the geodesic integrator that frame dragging equations describe - the leap from theory to ray-traced pictures.

## Q40: What is the next step after mastering frame dragging - justify your answer with a concrete production example.
**A:** Coding the geodesic integrator that frame dragging equations describe - the leap from theory to ray-traced pictures. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: Give one number a beginner should memorize for frame dragging - justify your answer with a concrete production example.
**A:** The photon sphere radius 3GM/C^2 (1.5 Schwarzschild radii) beyond which frame dragging orbiting light is possible. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What documentation accompanies frame dragging in a research code - justify your answer with a concrete production example.
**A:** Every derivation, coordinate convention, and unit choice for frame dragging is written down so the integrator can be audited. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: How is frame dragging typically mis-stated in pop science - justify your answer with a concrete production example.
**A:** As 'light has no mass so how does gravity pull it' - frame dragging reframes it as path curvature, not a force on mass. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What does frame dragging say about time near a black hole - justify your answer with a concrete production example.
**A:** Clocks run slower deeper in the potential; frame dragging quantifies the ratio for a distant observer as the inverse redshift factor. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: How do you test the weak-field limit of frame dragging - justify your answer with a concrete production example.
**A:** Expanding the metric at large radius must recover Newtonian gravity plus the leading post-Newtonian corrections - the sanity check for frame dragging. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: What limits are placed by frame dragging on observables - justify your answer with a concrete production example.
**A:** Nothing escapes inside the horizon; the photon sphere at 1.5 Schwarzschild radii bounds where frame dragging says circular light orbits exist. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What is the embedding-diagram view of frame dragging - justify your answer with a concrete production example.
**A:** A 2D slice of the geometry drawn inside a fictional flat space shows the funnel shape that beginners intuitively associate with frame dragging. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: Why start with Schwarzschild before Kerr for frame dragging - justify your answer with a concrete production example.
**A:** Schwarzschild is spherically symmetric with simple constants, so frame dragging concepts are demonstrated and validated before spin complicates them. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: How does frame dragging guide frame transformations in rendering - justify your answer with a concrete production example.
**A:** Radiation emitted in the fluid frame must be Lorentz-transformed to the coordinate frame; frame dragging supplies the needed boost toward a locally non-rotating observer. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What numerical care does frame dragging require - justify your answer with a concrete production example.
**A:** The metric functions diverge at horizons and the coordinate singularities; switching to Kerr-Schild coordinates stabilizes frame dragging integration. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How would a detector measure effects of frame dragging - justify your answer with a concrete production example.
**A:** Comparing clock rates, precision astrometry, or the shape of the photon ring all isolate signatures of frame dragging. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: What is the role of conserved quantities in frame dragging - justify your answer with a concrete production example.
**A:** Symmetries of the metric give constants along geodesics - energy, angular momentum, and (in Kerr) the Carter constant - which frame dragging uses to integrate efficiently. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What physical predictions come straight from frame dragging - justify your answer with a concrete production example.
**A:** Gravitational redshift, perihelion precession, light bending, frame dragging, and orbital decay from gravitational waves are all frame dragging consequences. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does frame dragging generalize for rotating black holes - justify your answer with a concrete production example.
**A:** The stationary axisymmetric Kerr metric replaces spherical symmetry; frame dragging gains a spin parameter and frame dragging enters. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What is a common misconception about frame dragging - justify your answer with a concrete production example.
**A:** That gravity is a force deflecting light; really frame dragging is geometry: light follows the straightest possible path in curved spacetime. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: Give the classic demonstrative example of frame dragging - justify your answer with a concrete production example.
**A:** A light ray grazing the Sun bends by 1.75 arcseconds; exact frame dragging reproduces this and more dramatic bending near a horizon. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: What are the units and conventions for frame dragging - justify your answer with a concrete production example.
**A:** geometric units with c=G=1 make masses length-like; careful sign conventions (mostly-plus vs mostly-minus) pervade frame dragging formulas. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: How does frame dragging connect to special relativity - justify your answer with a concrete production example.
**A:** In the absence of gravity the metric is Minkowski, and frame dragging reduces to Lorentz transformations and the usual Doppler formulas. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How do you verify a calculation of frame dragging - justify your answer with a concrete production example.
**A:** Take non-relativistic or weak-field limits, compare with known analytic results such as light bending, and check conservation laws numerically. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What is the intuition behind frame dragging for a beginner - justify your answer with a concrete production example.
**A:** Spacetime tells matter how to move and matter tells spacetime how to curve; frame dragging is the first concrete step of that program. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: Why does frame dragging matter for a black-hole raytracer - justify your answer with a concrete production example.
**A:** Photons follow null geodesics of the Kerr geometry; frame dragging tells you exactly how to advance a ray in Boyer-Lindquist coordinates. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: How is frame dragging expressed mathematically - justify your answer with a concrete production example.
**A:** Through the metric tensor and its derivatives; frame dragging gives the equations of motion for particles and light as geodesics of that metric. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What is the physical meaning of frame dragging in general relativity - justify your answer with a concrete production example.
**A:** It encodes how spacetime geometry responds to mass-energy; frame dragging ties local measurements in a freely falling frame to the global curved geometry. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What is the physical meaning of frame dragging in general relativity - justify your answer with a concrete production example.
**A:** It encodes how spacetime geometry responds to mass-energy; frame dragging ties local measurements in a freely falling frame to the global curved geometry. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: How is frame dragging expressed mathematically - justify your answer with a concrete production example.
**A:** Through the metric tensor and its derivatives; frame dragging gives the equations of motion for particles and light as geodesics of that metric. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: Why does frame dragging matter for a black-hole raytracer - justify your answer with a concrete production example.
**A:** Photons follow null geodesics of the Kerr geometry; frame dragging tells you exactly how to advance a ray in Boyer-Lindquist coordinates. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What is the intuition behind frame dragging for a beginner - justify your answer with a concrete production example.
**A:** Spacetime tells matter how to move and matter tells spacetime how to curve; frame dragging is the first concrete step of that program. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How do you verify a calculation of frame dragging - justify your answer with a concrete production example.
**A:** Take non-relativistic or weak-field limits, compare with known analytic results such as light bending, and check conservation laws numerically. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: How does frame dragging connect to special relativity - justify your answer with a concrete production example.
**A:** In the absence of gravity the metric is Minkowski, and frame dragging reduces to Lorentz transformations and the usual Doppler formulas. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: What are the units and conventions for frame dragging - justify your answer with a concrete production example.
**A:** geometric units with c=G=1 make masses length-like; careful sign conventions (mostly-plus vs mostly-minus) pervade frame dragging formulas. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: Give the classic demonstrative example of frame dragging - justify your answer with a concrete production example.
**A:** A light ray grazing the Sun bends by 1.75 arcseconds; exact frame dragging reproduces this and more dramatic bending near a horizon. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What is a common misconception about frame dragging - justify your answer with a concrete production example.
**A:** That gravity is a force deflecting light; really frame dragging is geometry: light follows the straightest possible path in curved spacetime. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does frame dragging generalize for rotating black holes - justify your answer with a concrete production example.
**A:** The stationary axisymmetric Kerr metric replaces spherical symmetry; frame dragging gains a spin parameter and frame dragging enters. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What physical predictions come straight from frame dragging - justify your answer with a concrete production example.
**A:** Gravitational redshift, perihelion precession, light bending, frame dragging, and orbital decay from gravitational waves are all frame dragging consequences. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: What is the role of conserved quantities in frame dragging - justify your answer with a concrete production example.
**A:** Symmetries of the metric give constants along geodesics - energy, angular momentum, and (in Kerr) the Carter constant - which frame dragging uses to integrate efficiently. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How would a detector measure effects of frame dragging - justify your answer with a concrete production example.
**A:** Comparing clock rates, precision astrometry, or the shape of the photon ring all isolate signatures of frame dragging. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What numerical care does frame dragging require - justify your answer with a concrete production example.
**A:** The metric functions diverge at horizons and the coordinate singularities; switching to Kerr-Schild coordinates stabilizes frame dragging integration. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: How does frame dragging guide frame transformations in rendering - justify your answer with a concrete production example.
**A:** Radiation emitted in the fluid frame must be Lorentz-transformed to the coordinate frame; frame dragging supplies the needed boost toward a locally non-rotating observer. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: Why start with Schwarzschild before Kerr for frame dragging - justify your answer with a concrete production example.
**A:** Schwarzschild is spherically symmetric with simple constants, so frame dragging concepts are demonstrated and validated before spin complicates them. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What is the embedding-diagram view of frame dragging - justify your answer with a concrete production example.
**A:** A 2D slice of the geometry drawn inside a fictional flat space shows the funnel shape that beginners intuitively associate with frame dragging. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: What limits are placed by frame dragging on observables - justify your answer with a concrete production example.
**A:** Nothing escapes inside the horizon; the photon sphere at 1.5 Schwarzschild radii bounds where frame dragging says circular light orbits exist. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: How do you test the weak-field limit of frame dragging - justify your answer with a concrete production example.
**A:** Expanding the metric at large radius must recover Newtonian gravity plus the leading post-Newtonian corrections - the sanity check for frame dragging. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What does frame dragging say about time near a black hole - justify your answer with a concrete production example.
**A:** Clocks run slower deeper in the potential; frame dragging quantifies the ratio for a distant observer as the inverse redshift factor. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: How is frame dragging typically mis-stated in pop science - justify your answer with a concrete production example.
**A:** As 'light has no mass so how does gravity pull it' - frame dragging reframes it as path curvature, not a force on mass. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What documentation accompanies frame dragging in a research code - justify your answer with a concrete production example.
**A:** Every derivation, coordinate convention, and unit choice for frame dragging is written down so the integrator can be audited. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: Give one number a beginner should memorize for frame dragging - justify your answer with a concrete production example.
**A:** The photon sphere radius 3GM/C^2 (1.5 Schwarzschild radii) beyond which frame dragging orbiting light is possible. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: What is the next step after mastering frame dragging - justify your answer with a concrete production example.
**A:** Coding the geodesic integrator that frame dragging equations describe - the leap from theory to ray-traced pictures. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: What is the next step after mastering frame dragging - justify your answer with a concrete production example.
**A:** Coding the geodesic integrator that frame dragging equations describe - the leap from theory to ray-traced pictures. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: Give one number a beginner should memorize for frame dragging - justify your answer with a concrete production example.
**A:** The photon sphere radius 3GM/C^2 (1.5 Schwarzschild radii) beyond which frame dragging orbiting light is possible. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What documentation accompanies frame dragging in a research code - justify your answer with a concrete production example.
**A:** Every derivation, coordinate convention, and unit choice for frame dragging is written down so the integrator can be audited. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: How is frame dragging typically mis-stated in pop science - justify your answer with a concrete production example.
**A:** As 'light has no mass so how does gravity pull it' - frame dragging reframes it as path curvature, not a force on mass. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What does frame dragging say about time near a black hole - justify your answer with a concrete production example.
**A:** Clocks run slower deeper in the potential; frame dragging quantifies the ratio for a distant observer as the inverse redshift factor. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: How do you test the weak-field limit of frame dragging - justify your answer with a concrete production example.
**A:** Expanding the metric at large radius must recover Newtonian gravity plus the leading post-Newtonian corrections - the sanity check for frame dragging. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: What limits are placed by frame dragging on observables - justify your answer with a concrete production example.
**A:** Nothing escapes inside the horizon; the photon sphere at 1.5 Schwarzschild radii bounds where frame dragging says circular light orbits exist. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What is the embedding-diagram view of frame dragging - justify your answer with a concrete production example.
**A:** A 2D slice of the geometry drawn inside a fictional flat space shows the funnel shape that beginners intuitively associate with frame dragging. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: Why start with Schwarzschild before Kerr for frame dragging - justify your answer with a concrete production example.
**A:** Schwarzschild is spherically symmetric with simple constants, so frame dragging concepts are demonstrated and validated before spin complicates them. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: How does frame dragging guide frame transformations in rendering - justify your answer with a concrete production example.
**A:** Radiation emitted in the fluid frame must be Lorentz-transformed to the coordinate frame; frame dragging supplies the needed boost toward a locally non-rotating observer. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What numerical care does frame dragging require - justify your answer with a concrete production example.
**A:** The metric functions diverge at horizons and the coordinate singularities; switching to Kerr-Schild coordinates stabilizes frame dragging integration. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How would a detector measure effects of frame dragging - justify your answer with a concrete production example.
**A:** Comparing clock rates, precision astrometry, or the shape of the photon ring all isolate signatures of frame dragging. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: What is the role of conserved quantities in frame dragging - justify your answer with a concrete production example.
**A:** Symmetries of the metric give constants along geodesics - energy, angular momentum, and (in Kerr) the Carter constant - which frame dragging uses to integrate efficiently. A concrete example: consistently applying frame dragging in code review and regression tests keeps the whole pipeline trustworthy.
