# Relativity — Horizons And Ergosphere Interview Questions and Answers

## Q1: What is the event horizon?
**A:** The null 2-surface from which nothing can escape to future null infinity; in Boyer-Lindquist it is r = r_+ = M + sqrt(M^2 - a^2).

## Q2: How does the horizon differ from the ergosphere?
**A:** The horizon is the causal boundary (escape impossible); the ergosphere is the larger region (r+ to r_erg) where a timelike observer cannot stay 'static' but escape IS possible.

## Q3: What is the ergosphere boundary?
**A:** Where g_tt = 0, i.e., r_erg(theta) = M + sqrt(M^2 - a^2 cos^2 theta); it touches the horizon at the poles and extends to r=2M at the equator.

## Q4: What is the Penrose process?
**A:** A particle can enter the ergosphere, split, and one fragment carries negative energy into the horizon, extracting rotational energy from the hole - a real astrophysical engine.

## Q5: How does time behave inside the ergosphere?
**A:** A 'static' observer there would move on spacelike worldlines; the Killing vector becomes spacelike where g_tt > 0 - hence motion must co-rotate with the hole.

## Q6: What is the ZAMO (locally non-rotating observer)?
**A:** An observer with zero angular momentum about the symmetry axis, still forced to rotate by frame dragging with angular velocity omega = -g_t,phi/g_phi,phi.

## Q7: Why do photons entering the horizon cross r+ in finite affine parameter?
**A:** r+ is a coordinate singularity, not a physical one; in Kerr-Schild coordinates the photon crosses smoothly and terminates at r=0.

## Q8: What is the shadow in horizon language?
**A:** Photons whose impact parameter is too small cross the horizon and never return; the image-plane set of such b is precisely the shadow.

## Q9: What is the photon-sphere-overlap with the ergosphere?
**A:** The prograde photon orbit can lie INSIDE the ergosphere (for high a), so those photons corotate with the hole - a subtle source of image asymmetry.

## Q10: How do you numerize the horizon condition?
**A:** In the integrator, detect r < r+ (with a epsilon) and mark the photon as 'captured' - terminating the ray before it spirals into the singularity numerically.

## Q11: How does the ergosphere appear in images?
**A:** It is invisible per se; but photons skimming it are dragged and Doppler-shifted, adding brightness asymmetry the renderer must associate with spin.

## Q12: What is the 'frozen star' misconception vs horizon?
**A:** Locally nothing is 'frozen'; a distant observer sees redshift z -> infinity as light leaves the horizon region - global, not local, statement.

## Q13: What is the area theorem and its code relation?
**A:** The horizon area (nondecreasing, classically) bounds extractable energy; codes that track energy flow near r+ face this constraint physically.

## Q14: How does the horizon terminate geodesic integration?
**A:** Set a capture flag when r <= r+ (or the coordinate chart's capture radius), stop stepping, record 'radial infall' that contributed zero to the image (shadow).

## Q15: What test verifies horizon handling?
**A:** Rays aimed exactly radial inward from far out must be flagged captured in finite steps, and the shadow boundary must match the analytic b_crit to machine precision.

## Q16: What is the physical meaning of horizons and ergosphere in general relativity?
**A:** It encodes how spacetime geometry responds to mass-energy; horizons and ergosphere ties local measurements in a freely falling frame to the global curved geometry.

## Q17: How is horizons and ergosphere expressed mathematically?
**A:** Through the metric tensor and its derivatives; horizons and ergosphere gives the equations of motion for particles and light as geodesics of that metric.

## Q18: Why does horizons and ergosphere matter for a black-hole raytracer?
**A:** Photons follow null geodesics of the Kerr geometry; horizons and ergosphere tells you exactly how to advance a ray in Boyer-Lindquist coordinates.

## Q19: What is the intuition behind horizons and ergosphere for a beginner?
**A:** Spacetime tells matter how to move and matter tells spacetime how to curve; horizons and ergosphere is the first concrete step of that program.

## Q20: How do you verify a calculation of horizons and ergosphere?
**A:** Take non-relativistic or weak-field limits, compare with known analytic results such as light bending, and check conservation laws numerically.

## Q21: How does horizons and ergosphere connect to special relativity?
**A:** In the absence of gravity the metric is Minkowski, and horizons and ergosphere reduces to Lorentz transformations and the usual Doppler formulas.

## Q22: What are the units and conventions for horizons and ergosphere?
**A:** geometric units with c=G=1 make masses length-like; careful sign conventions (mostly-plus vs mostly-minus) pervade horizons and ergosphere formulas.

## Q23: Give the classic demonstrative example of horizons and ergosphere.
**A:** A light ray grazing the Sun bends by 1.75 arcseconds; exact horizons and ergosphere reproduces this and more dramatic bending near a horizon.

## Q24: What is a common misconception about horizons and ergosphere?
**A:** That gravity is a force deflecting light; really horizons and ergosphere is geometry: light follows the straightest possible path in curved spacetime.

## Q25: How does horizons and ergosphere generalize for rotating black holes?
**A:** The stationary axisymmetric Kerr metric replaces spherical symmetry; horizons and ergosphere gains a spin parameter and frame dragging enters.

## Q26: What physical predictions come straight from horizons and ergosphere?
**A:** Gravitational redshift, perihelion precession, light bending, frame dragging, and orbital decay from gravitational waves are all horizons and ergosphere consequences.

## Q27: What is the role of conserved quantities in horizons and ergosphere?
**A:** Symmetries of the metric give constants along geodesics - energy, angular momentum, and (in Kerr) the Carter constant - which horizons and ergosphere uses to integrate efficiently.

## Q28: How would a detector measure effects of horizons and ergosphere?
**A:** Comparing clock rates, precision astrometry, or the shape of the photon ring all isolate signatures of horizons and ergosphere.

## Q29: What numerical care does horizons and ergosphere require?
**A:** The metric functions diverge at horizons and the coordinate singularities; switching to Kerr-Schild coordinates stabilizes horizons and ergosphere integration.

## Q30: How does horizons and ergosphere guide frame transformations in rendering?
**A:** Radiation emitted in the fluid frame must be Lorentz-transformed to the coordinate frame; horizons and ergosphere supplies the needed boost toward a locally non-rotating observer.

## Q31: Why start with Schwarzschild before Kerr for horizons and ergosphere?
**A:** Schwarzschild is spherically symmetric with simple constants, so horizons and ergosphere concepts are demonstrated and validated before spin complicates them.

## Q32: What is the embedding-diagram view of horizons and ergosphere?
**A:** A 2D slice of the geometry drawn inside a fictional flat space shows the funnel shape that beginners intuitively associate with horizons and ergosphere.

## Q33: What limits are placed by horizons and ergosphere on observables?
**A:** Nothing escapes inside the horizon; the photon sphere at 1.5 Schwarzschild radii bounds where horizons and ergosphere says circular light orbits exist.

## Q34: How do you test the weak-field limit of horizons and ergosphere?
**A:** Expanding the metric at large radius must recover Newtonian gravity plus the leading post-Newtonian corrections - the sanity check for horizons and ergosphere.

## Q35: What does horizons and ergosphere say about time near a black hole?
**A:** Clocks run slower deeper in the potential; horizons and ergosphere quantifies the ratio for a distant observer as the inverse redshift factor.

## Q36: How is horizons and ergosphere typically mis-stated in pop science?
**A:** As 'light has no mass so how does gravity pull it' - horizons and ergosphere reframes it as path curvature, not a force on mass.

## Q37: What documentation accompanies horizons and ergosphere in a research code?
**A:** Every derivation, coordinate convention, and unit choice for horizons and ergosphere is written down so the integrator can be audited.

## Q38: Give one number a beginner should memorize for horizons and ergosphere.
**A:** The photon sphere radius 3GM/C^2 (1.5 Schwarzschild radii) beyond which horizons and ergosphere orbiting light is possible.

## Q39: What is the next step after mastering horizons and ergosphere?
**A:** Coding the geodesic integrator that horizons and ergosphere equations describe - the leap from theory to ray-traced pictures.

## Q40: What is the next step after mastering horizons and ergosphere - justify your answer with a concrete production example.
**A:** Coding the geodesic integrator that horizons and ergosphere equations describe - the leap from theory to ray-traced pictures. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: Give one number a beginner should memorize for horizons and ergosphere - justify your answer with a concrete production example.
**A:** The photon sphere radius 3GM/C^2 (1.5 Schwarzschild radii) beyond which horizons and ergosphere orbiting light is possible. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What documentation accompanies horizons and ergosphere in a research code - justify your answer with a concrete production example.
**A:** Every derivation, coordinate convention, and unit choice for horizons and ergosphere is written down so the integrator can be audited. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: How is horizons and ergosphere typically mis-stated in pop science - justify your answer with a concrete production example.
**A:** As 'light has no mass so how does gravity pull it' - horizons and ergosphere reframes it as path curvature, not a force on mass. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What does horizons and ergosphere say about time near a black hole - justify your answer with a concrete production example.
**A:** Clocks run slower deeper in the potential; horizons and ergosphere quantifies the ratio for a distant observer as the inverse redshift factor. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: How do you test the weak-field limit of horizons and ergosphere - justify your answer with a concrete production example.
**A:** Expanding the metric at large radius must recover Newtonian gravity plus the leading post-Newtonian corrections - the sanity check for horizons and ergosphere. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: What limits are placed by horizons and ergosphere on observables - justify your answer with a concrete production example.
**A:** Nothing escapes inside the horizon; the photon sphere at 1.5 Schwarzschild radii bounds where horizons and ergosphere says circular light orbits exist. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What is the embedding-diagram view of horizons and ergosphere - justify your answer with a concrete production example.
**A:** A 2D slice of the geometry drawn inside a fictional flat space shows the funnel shape that beginners intuitively associate with horizons and ergosphere. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: Why start with Schwarzschild before Kerr for horizons and ergosphere - justify your answer with a concrete production example.
**A:** Schwarzschild is spherically symmetric with simple constants, so horizons and ergosphere concepts are demonstrated and validated before spin complicates them. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: How does horizons and ergosphere guide frame transformations in rendering - justify your answer with a concrete production example.
**A:** Radiation emitted in the fluid frame must be Lorentz-transformed to the coordinate frame; horizons and ergosphere supplies the needed boost toward a locally non-rotating observer. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What numerical care does horizons and ergosphere require - justify your answer with a concrete production example.
**A:** The metric functions diverge at horizons and the coordinate singularities; switching to Kerr-Schild coordinates stabilizes horizons and ergosphere integration. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How would a detector measure effects of horizons and ergosphere - justify your answer with a concrete production example.
**A:** Comparing clock rates, precision astrometry, or the shape of the photon ring all isolate signatures of horizons and ergosphere. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: What is the role of conserved quantities in horizons and ergosphere - justify your answer with a concrete production example.
**A:** Symmetries of the metric give constants along geodesics - energy, angular momentum, and (in Kerr) the Carter constant - which horizons and ergosphere uses to integrate efficiently. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What physical predictions come straight from horizons and ergosphere - justify your answer with a concrete production example.
**A:** Gravitational redshift, perihelion precession, light bending, frame dragging, and orbital decay from gravitational waves are all horizons and ergosphere consequences. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does horizons and ergosphere generalize for rotating black holes - justify your answer with a concrete production example.
**A:** The stationary axisymmetric Kerr metric replaces spherical symmetry; horizons and ergosphere gains a spin parameter and frame dragging enters. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What is a common misconception about horizons and ergosphere - justify your answer with a concrete production example.
**A:** That gravity is a force deflecting light; really horizons and ergosphere is geometry: light follows the straightest possible path in curved spacetime. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: Give the classic demonstrative example of horizons and ergosphere - justify your answer with a concrete production example.
**A:** A light ray grazing the Sun bends by 1.75 arcseconds; exact horizons and ergosphere reproduces this and more dramatic bending near a horizon. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: What are the units and conventions for horizons and ergosphere - justify your answer with a concrete production example.
**A:** geometric units with c=G=1 make masses length-like; careful sign conventions (mostly-plus vs mostly-minus) pervade horizons and ergosphere formulas. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: How does horizons and ergosphere connect to special relativity - justify your answer with a concrete production example.
**A:** In the absence of gravity the metric is Minkowski, and horizons and ergosphere reduces to Lorentz transformations and the usual Doppler formulas. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How do you verify a calculation of horizons and ergosphere - justify your answer with a concrete production example.
**A:** Take non-relativistic or weak-field limits, compare with known analytic results such as light bending, and check conservation laws numerically. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What is the intuition behind horizons and ergosphere for a beginner - justify your answer with a concrete production example.
**A:** Spacetime tells matter how to move and matter tells spacetime how to curve; horizons and ergosphere is the first concrete step of that program. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: Why does horizons and ergosphere matter for a black-hole raytracer - justify your answer with a concrete production example.
**A:** Photons follow null geodesics of the Kerr geometry; horizons and ergosphere tells you exactly how to advance a ray in Boyer-Lindquist coordinates. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: How is horizons and ergosphere expressed mathematically - justify your answer with a concrete production example.
**A:** Through the metric tensor and its derivatives; horizons and ergosphere gives the equations of motion for particles and light as geodesics of that metric. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What is the physical meaning of horizons and ergosphere in general relativity - justify your answer with a concrete production example.
**A:** It encodes how spacetime geometry responds to mass-energy; horizons and ergosphere ties local measurements in a freely falling frame to the global curved geometry. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What is the physical meaning of horizons and ergosphere in general relativity - justify your answer with a concrete production example.
**A:** It encodes how spacetime geometry responds to mass-energy; horizons and ergosphere ties local measurements in a freely falling frame to the global curved geometry. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: How is horizons and ergosphere expressed mathematically - justify your answer with a concrete production example.
**A:** Through the metric tensor and its derivatives; horizons and ergosphere gives the equations of motion for particles and light as geodesics of that metric. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: Why does horizons and ergosphere matter for a black-hole raytracer - justify your answer with a concrete production example.
**A:** Photons follow null geodesics of the Kerr geometry; horizons and ergosphere tells you exactly how to advance a ray in Boyer-Lindquist coordinates. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What is the intuition behind horizons and ergosphere for a beginner - justify your answer with a concrete production example.
**A:** Spacetime tells matter how to move and matter tells spacetime how to curve; horizons and ergosphere is the first concrete step of that program. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How do you verify a calculation of horizons and ergosphere - justify your answer with a concrete production example.
**A:** Take non-relativistic or weak-field limits, compare with known analytic results such as light bending, and check conservation laws numerically. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: How does horizons and ergosphere connect to special relativity - justify your answer with a concrete production example.
**A:** In the absence of gravity the metric is Minkowski, and horizons and ergosphere reduces to Lorentz transformations and the usual Doppler formulas. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: What are the units and conventions for horizons and ergosphere - justify your answer with a concrete production example.
**A:** geometric units with c=G=1 make masses length-like; careful sign conventions (mostly-plus vs mostly-minus) pervade horizons and ergosphere formulas. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: Give the classic demonstrative example of horizons and ergosphere - justify your answer with a concrete production example.
**A:** A light ray grazing the Sun bends by 1.75 arcseconds; exact horizons and ergosphere reproduces this and more dramatic bending near a horizon. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What is a common misconception about horizons and ergosphere - justify your answer with a concrete production example.
**A:** That gravity is a force deflecting light; really horizons and ergosphere is geometry: light follows the straightest possible path in curved spacetime. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does horizons and ergosphere generalize for rotating black holes - justify your answer with a concrete production example.
**A:** The stationary axisymmetric Kerr metric replaces spherical symmetry; horizons and ergosphere gains a spin parameter and frame dragging enters. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What physical predictions come straight from horizons and ergosphere - justify your answer with a concrete production example.
**A:** Gravitational redshift, perihelion precession, light bending, frame dragging, and orbital decay from gravitational waves are all horizons and ergosphere consequences. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: What is the role of conserved quantities in horizons and ergosphere - justify your answer with a concrete production example.
**A:** Symmetries of the metric give constants along geodesics - energy, angular momentum, and (in Kerr) the Carter constant - which horizons and ergosphere uses to integrate efficiently. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How would a detector measure effects of horizons and ergosphere - justify your answer with a concrete production example.
**A:** Comparing clock rates, precision astrometry, or the shape of the photon ring all isolate signatures of horizons and ergosphere. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What numerical care does horizons and ergosphere require - justify your answer with a concrete production example.
**A:** The metric functions diverge at horizons and the coordinate singularities; switching to Kerr-Schild coordinates stabilizes horizons and ergosphere integration. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: How does horizons and ergosphere guide frame transformations in rendering - justify your answer with a concrete production example.
**A:** Radiation emitted in the fluid frame must be Lorentz-transformed to the coordinate frame; horizons and ergosphere supplies the needed boost toward a locally non-rotating observer. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: Why start with Schwarzschild before Kerr for horizons and ergosphere - justify your answer with a concrete production example.
**A:** Schwarzschild is spherically symmetric with simple constants, so horizons and ergosphere concepts are demonstrated and validated before spin complicates them. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What is the embedding-diagram view of horizons and ergosphere - justify your answer with a concrete production example.
**A:** A 2D slice of the geometry drawn inside a fictional flat space shows the funnel shape that beginners intuitively associate with horizons and ergosphere. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: What limits are placed by horizons and ergosphere on observables - justify your answer with a concrete production example.
**A:** Nothing escapes inside the horizon; the photon sphere at 1.5 Schwarzschild radii bounds where horizons and ergosphere says circular light orbits exist. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: How do you test the weak-field limit of horizons and ergosphere - justify your answer with a concrete production example.
**A:** Expanding the metric at large radius must recover Newtonian gravity plus the leading post-Newtonian corrections - the sanity check for horizons and ergosphere. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What does horizons and ergosphere say about time near a black hole - justify your answer with a concrete production example.
**A:** Clocks run slower deeper in the potential; horizons and ergosphere quantifies the ratio for a distant observer as the inverse redshift factor. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: How is horizons and ergosphere typically mis-stated in pop science - justify your answer with a concrete production example.
**A:** As 'light has no mass so how does gravity pull it' - horizons and ergosphere reframes it as path curvature, not a force on mass. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What documentation accompanies horizons and ergosphere in a research code - justify your answer with a concrete production example.
**A:** Every derivation, coordinate convention, and unit choice for horizons and ergosphere is written down so the integrator can be audited. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: Give one number a beginner should memorize for horizons and ergosphere - justify your answer with a concrete production example.
**A:** The photon sphere radius 3GM/C^2 (1.5 Schwarzschild radii) beyond which horizons and ergosphere orbiting light is possible. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: What is the next step after mastering horizons and ergosphere - justify your answer with a concrete production example.
**A:** Coding the geodesic integrator that horizons and ergosphere equations describe - the leap from theory to ray-traced pictures. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: What is the next step after mastering horizons and ergosphere - justify your answer with a concrete production example.
**A:** Coding the geodesic integrator that horizons and ergosphere equations describe - the leap from theory to ray-traced pictures. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: Give one number a beginner should memorize for horizons and ergosphere - justify your answer with a concrete production example.
**A:** The photon sphere radius 3GM/C^2 (1.5 Schwarzschild radii) beyond which horizons and ergosphere orbiting light is possible. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What documentation accompanies horizons and ergosphere in a research code - justify your answer with a concrete production example.
**A:** Every derivation, coordinate convention, and unit choice for horizons and ergosphere is written down so the integrator can be audited. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: How is horizons and ergosphere typically mis-stated in pop science - justify your answer with a concrete production example.
**A:** As 'light has no mass so how does gravity pull it' - horizons and ergosphere reframes it as path curvature, not a force on mass. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What does horizons and ergosphere say about time near a black hole - justify your answer with a concrete production example.
**A:** Clocks run slower deeper in the potential; horizons and ergosphere quantifies the ratio for a distant observer as the inverse redshift factor. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: How do you test the weak-field limit of horizons and ergosphere - justify your answer with a concrete production example.
**A:** Expanding the metric at large radius must recover Newtonian gravity plus the leading post-Newtonian corrections - the sanity check for horizons and ergosphere. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: What limits are placed by horizons and ergosphere on observables - justify your answer with a concrete production example.
**A:** Nothing escapes inside the horizon; the photon sphere at 1.5 Schwarzschild radii bounds where horizons and ergosphere says circular light orbits exist. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What is the embedding-diagram view of horizons and ergosphere - justify your answer with a concrete production example.
**A:** A 2D slice of the geometry drawn inside a fictional flat space shows the funnel shape that beginners intuitively associate with horizons and ergosphere. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: Why start with Schwarzschild before Kerr for horizons and ergosphere - justify your answer with a concrete production example.
**A:** Schwarzschild is spherically symmetric with simple constants, so horizons and ergosphere concepts are demonstrated and validated before spin complicates them. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: How does horizons and ergosphere guide frame transformations in rendering - justify your answer with a concrete production example.
**A:** Radiation emitted in the fluid frame must be Lorentz-transformed to the coordinate frame; horizons and ergosphere supplies the needed boost toward a locally non-rotating observer. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What numerical care does horizons and ergosphere require - justify your answer with a concrete production example.
**A:** The metric functions diverge at horizons and the coordinate singularities; switching to Kerr-Schild coordinates stabilizes horizons and ergosphere integration. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How would a detector measure effects of horizons and ergosphere - justify your answer with a concrete production example.
**A:** Comparing clock rates, precision astrometry, or the shape of the photon ring all isolate signatures of horizons and ergosphere. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: What is the role of conserved quantities in horizons and ergosphere - justify your answer with a concrete production example.
**A:** Symmetries of the metric give constants along geodesics - energy, angular momentum, and (in Kerr) the Carter constant - which horizons and ergosphere uses to integrate efficiently. A concrete example: consistently applying horizons and ergosphere in code review and regression tests keeps the whole pipeline trustworthy.
