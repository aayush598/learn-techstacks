# Relativity — Units And Conventions Interview Questions and Answers

## Q1: What are natural/geometric units and why use them?
**A:** c = G = 1 make mass dimensionally a length (M = l = t), removing factors from formulas; the code keeps them internally and only converts at I/O boundaries.

## Q2: How do you restore SI-ish numbers for comparison?
**A:** Multiply by powers of G and c: M_solar ~ 1.477 km, t ~ 4.93 us per km, etc.; all conversions stay in one unit-conversion module.

## Q3: What is the relationship M in geometrical units?
**A:** 1 solar mass = 1.4776 km = 4.925e-6 s of geometric time; the code stores M and a in those units and renders r distances in M.

## Q4: What is the 'M' scaling of the photon ring?
**A:** All key radii are pure numbers times M: horizon 2M, photon sphere 3M, ISCO 6M - so a visually scaled render is literally just the same geometry in different M.

## Q5: What is the convention for the photon energy/frequency?
**A:** p_t = -E; the redshift factor sets nu_obs/nu_emit; frequencies in Hz only enter when mapping to real spectra at I/O.

## Q6: What is the sign of the metric (the convention trap)?
**A:** (-,+,+,+) vs (+,-,-,-) flips every spatial signature; pick one, document it, and never mix - the code asserts the signature at startup.

## Q7: What are the two common coordinate charts?
**A:** Boyer-Lindquist (analytic formulas, singular at Delta=0) and Kerr-Schild (numerically smooth through the horizon); conversions between them must be exact functions.

## Q8: What is the isometric angular convention?
**A:** theta measured from the axis (0..pi), phi in [0, 2pi); the singular points at theta=0 plus the polar cap need the azimuthal index avoided there.

## Q9: How are angular velocities normalized?
**A:** The boost beta uses c=1; physical omega = dphi/dt times a conversion if output in Hz/arcsec. The ZAMO omega is dimensionless in geometric units.

## Q10: What does 'M=1 say about the Newtonian limit?
**A:** Radii in units of M: large r means b >> M is the weak-field regime; the 4M/b deflection formula is the M-small placeholder.

## Q11: Why do colors need physical frequencies?
**A:** Spectrum integration needs nu in Hz; the code keeps a scale factor (frequency unit) multiplying the geometric-unit frequencies at the transfer stage.

## Q12: What is the gravitational radius and its significance?
**A:** r_g = GM/c^2 is the natural length of the hole; EHT discusses angular sizes via r_g/D - the observational twin of the internal M-unit.

## Q13: What is the code's unit test set?
**A:** At M in one unit, the horizon radius is 2M, the photon sphere 3M, ISCO 6M, shadow 3sqrt(3)M - these four numbers are unit-correctness gates.

## Q14: What is the rule for printing/output?
**A:** Always print with explicit unit labels (M, r_g, Hz, deg); every log and metadata field carries its unit so frames are auditable.

## Q15: What single decision most prevents unit bugs?
**A:** Freezing ALL math in geometric units with c=G=1 and converting only in three named I/O functions (unitsFromSI, unitsToSI, frequenciesFromHz) - no scattered conversions.

## Q16: What is the physical meaning of units and conventions in general relativity?
**A:** It encodes how spacetime geometry responds to mass-energy; units and conventions ties local measurements in a freely falling frame to the global curved geometry.

## Q17: How is units and conventions expressed mathematically?
**A:** Through the metric tensor and its derivatives; units and conventions gives the equations of motion for particles and light as geodesics of that metric.

## Q18: Why does units and conventions matter for a black-hole raytracer?
**A:** Photons follow null geodesics of the Kerr geometry; units and conventions tells you exactly how to advance a ray in Boyer-Lindquist coordinates.

## Q19: What is the intuition behind units and conventions for a beginner?
**A:** Spacetime tells matter how to move and matter tells spacetime how to curve; units and conventions is the first concrete step of that program.

## Q20: How do you verify a calculation of units and conventions?
**A:** Take non-relativistic or weak-field limits, compare with known analytic results such as light bending, and check conservation laws numerically.

## Q21: How does units and conventions connect to special relativity?
**A:** In the absence of gravity the metric is Minkowski, and units and conventions reduces to Lorentz transformations and the usual Doppler formulas.

## Q22: What are the units and conventions for units and conventions?
**A:** geometric units with c=G=1 make masses length-like; careful sign conventions (mostly-plus vs mostly-minus) pervade units and conventions formulas.

## Q23: Give the classic demonstrative example of units and conventions.
**A:** A light ray grazing the Sun bends by 1.75 arcseconds; exact units and conventions reproduces this and more dramatic bending near a horizon.

## Q24: What is a common misconception about units and conventions?
**A:** That gravity is a force deflecting light; really units and conventions is geometry: light follows the straightest possible path in curved spacetime.

## Q25: How does units and conventions generalize for rotating black holes?
**A:** The stationary axisymmetric Kerr metric replaces spherical symmetry; units and conventions gains a spin parameter and frame dragging enters.

## Q26: What physical predictions come straight from units and conventions?
**A:** Gravitational redshift, perihelion precession, light bending, frame dragging, and orbital decay from gravitational waves are all units and conventions consequences.

## Q27: What is the role of conserved quantities in units and conventions?
**A:** Symmetries of the metric give constants along geodesics - energy, angular momentum, and (in Kerr) the Carter constant - which units and conventions uses to integrate efficiently.

## Q28: How would a detector measure effects of units and conventions?
**A:** Comparing clock rates, precision astrometry, or the shape of the photon ring all isolate signatures of units and conventions.

## Q29: What numerical care does units and conventions require?
**A:** The metric functions diverge at horizons and the coordinate singularities; switching to Kerr-Schild coordinates stabilizes units and conventions integration.

## Q30: How does units and conventions guide frame transformations in rendering?
**A:** Radiation emitted in the fluid frame must be Lorentz-transformed to the coordinate frame; units and conventions supplies the needed boost toward a locally non-rotating observer.

## Q31: Why start with Schwarzschild before Kerr for units and conventions?
**A:** Schwarzschild is spherically symmetric with simple constants, so units and conventions concepts are demonstrated and validated before spin complicates them.

## Q32: What is the embedding-diagram view of units and conventions?
**A:** A 2D slice of the geometry drawn inside a fictional flat space shows the funnel shape that beginners intuitively associate with units and conventions.

## Q33: What limits are placed by units and conventions on observables?
**A:** Nothing escapes inside the horizon; the photon sphere at 1.5 Schwarzschild radii bounds where units and conventions says circular light orbits exist.

## Q34: How do you test the weak-field limit of units and conventions?
**A:** Expanding the metric at large radius must recover Newtonian gravity plus the leading post-Newtonian corrections - the sanity check for units and conventions.

## Q35: What does units and conventions say about time near a black hole?
**A:** Clocks run slower deeper in the potential; units and conventions quantifies the ratio for a distant observer as the inverse redshift factor.

## Q36: How is units and conventions typically mis-stated in pop science?
**A:** As 'light has no mass so how does gravity pull it' - units and conventions reframes it as path curvature, not a force on mass.

## Q37: What documentation accompanies units and conventions in a research code?
**A:** Every derivation, coordinate convention, and unit choice for units and conventions is written down so the integrator can be audited.

## Q38: Give one number a beginner should memorize for units and conventions.
**A:** The photon sphere radius 3GM/C^2 (1.5 Schwarzschild radii) beyond which units and conventions orbiting light is possible.

## Q39: What is the next step after mastering units and conventions?
**A:** Coding the geodesic integrator that units and conventions equations describe - the leap from theory to ray-traced pictures.

## Q40: What is the next step after mastering units and conventions - justify your answer with a concrete production example.
**A:** Coding the geodesic integrator that units and conventions equations describe - the leap from theory to ray-traced pictures. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: Give one number a beginner should memorize for units and conventions - justify your answer with a concrete production example.
**A:** The photon sphere radius 3GM/C^2 (1.5 Schwarzschild radii) beyond which units and conventions orbiting light is possible. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What documentation accompanies units and conventions in a research code - justify your answer with a concrete production example.
**A:** Every derivation, coordinate convention, and unit choice for units and conventions is written down so the integrator can be audited. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: How is units and conventions typically mis-stated in pop science - justify your answer with a concrete production example.
**A:** As 'light has no mass so how does gravity pull it' - units and conventions reframes it as path curvature, not a force on mass. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What does units and conventions say about time near a black hole - justify your answer with a concrete production example.
**A:** Clocks run slower deeper in the potential; units and conventions quantifies the ratio for a distant observer as the inverse redshift factor. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: How do you test the weak-field limit of units and conventions - justify your answer with a concrete production example.
**A:** Expanding the metric at large radius must recover Newtonian gravity plus the leading post-Newtonian corrections - the sanity check for units and conventions. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: What limits are placed by units and conventions on observables - justify your answer with a concrete production example.
**A:** Nothing escapes inside the horizon; the photon sphere at 1.5 Schwarzschild radii bounds where units and conventions says circular light orbits exist. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What is the embedding-diagram view of units and conventions - justify your answer with a concrete production example.
**A:** A 2D slice of the geometry drawn inside a fictional flat space shows the funnel shape that beginners intuitively associate with units and conventions. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: Why start with Schwarzschild before Kerr for units and conventions - justify your answer with a concrete production example.
**A:** Schwarzschild is spherically symmetric with simple constants, so units and conventions concepts are demonstrated and validated before spin complicates them. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: How does units and conventions guide frame transformations in rendering - justify your answer with a concrete production example.
**A:** Radiation emitted in the fluid frame must be Lorentz-transformed to the coordinate frame; units and conventions supplies the needed boost toward a locally non-rotating observer. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What numerical care does units and conventions require - justify your answer with a concrete production example.
**A:** The metric functions diverge at horizons and the coordinate singularities; switching to Kerr-Schild coordinates stabilizes units and conventions integration. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How would a detector measure effects of units and conventions - justify your answer with a concrete production example.
**A:** Comparing clock rates, precision astrometry, or the shape of the photon ring all isolate signatures of units and conventions. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: What is the role of conserved quantities in units and conventions - justify your answer with a concrete production example.
**A:** Symmetries of the metric give constants along geodesics - energy, angular momentum, and (in Kerr) the Carter constant - which units and conventions uses to integrate efficiently. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What physical predictions come straight from units and conventions - justify your answer with a concrete production example.
**A:** Gravitational redshift, perihelion precession, light bending, frame dragging, and orbital decay from gravitational waves are all units and conventions consequences. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does units and conventions generalize for rotating black holes - justify your answer with a concrete production example.
**A:** The stationary axisymmetric Kerr metric replaces spherical symmetry; units and conventions gains a spin parameter and frame dragging enters. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What is a common misconception about units and conventions - justify your answer with a concrete production example.
**A:** That gravity is a force deflecting light; really units and conventions is geometry: light follows the straightest possible path in curved spacetime. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: Give the classic demonstrative example of units and conventions - justify your answer with a concrete production example.
**A:** A light ray grazing the Sun bends by 1.75 arcseconds; exact units and conventions reproduces this and more dramatic bending near a horizon. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: What are the units and conventions for units and conventions - justify your answer with a concrete production example.
**A:** geometric units with c=G=1 make masses length-like; careful sign conventions (mostly-plus vs mostly-minus) pervade units and conventions formulas. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: How does units and conventions connect to special relativity - justify your answer with a concrete production example.
**A:** In the absence of gravity the metric is Minkowski, and units and conventions reduces to Lorentz transformations and the usual Doppler formulas. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How do you verify a calculation of units and conventions - justify your answer with a concrete production example.
**A:** Take non-relativistic or weak-field limits, compare with known analytic results such as light bending, and check conservation laws numerically. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What is the intuition behind units and conventions for a beginner - justify your answer with a concrete production example.
**A:** Spacetime tells matter how to move and matter tells spacetime how to curve; units and conventions is the first concrete step of that program. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: Why does units and conventions matter for a black-hole raytracer - justify your answer with a concrete production example.
**A:** Photons follow null geodesics of the Kerr geometry; units and conventions tells you exactly how to advance a ray in Boyer-Lindquist coordinates. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: How is units and conventions expressed mathematically - justify your answer with a concrete production example.
**A:** Through the metric tensor and its derivatives; units and conventions gives the equations of motion for particles and light as geodesics of that metric. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What is the physical meaning of units and conventions in general relativity - justify your answer with a concrete production example.
**A:** It encodes how spacetime geometry responds to mass-energy; units and conventions ties local measurements in a freely falling frame to the global curved geometry. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What is the physical meaning of units and conventions in general relativity - justify your answer with a concrete production example.
**A:** It encodes how spacetime geometry responds to mass-energy; units and conventions ties local measurements in a freely falling frame to the global curved geometry. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: How is units and conventions expressed mathematically - justify your answer with a concrete production example.
**A:** Through the metric tensor and its derivatives; units and conventions gives the equations of motion for particles and light as geodesics of that metric. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: Why does units and conventions matter for a black-hole raytracer - justify your answer with a concrete production example.
**A:** Photons follow null geodesics of the Kerr geometry; units and conventions tells you exactly how to advance a ray in Boyer-Lindquist coordinates. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What is the intuition behind units and conventions for a beginner - justify your answer with a concrete production example.
**A:** Spacetime tells matter how to move and matter tells spacetime how to curve; units and conventions is the first concrete step of that program. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How do you verify a calculation of units and conventions - justify your answer with a concrete production example.
**A:** Take non-relativistic or weak-field limits, compare with known analytic results such as light bending, and check conservation laws numerically. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: How does units and conventions connect to special relativity - justify your answer with a concrete production example.
**A:** In the absence of gravity the metric is Minkowski, and units and conventions reduces to Lorentz transformations and the usual Doppler formulas. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: What are the units and conventions for units and conventions - justify your answer with a concrete production example.
**A:** geometric units with c=G=1 make masses length-like; careful sign conventions (mostly-plus vs mostly-minus) pervade units and conventions formulas. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: Give the classic demonstrative example of units and conventions - justify your answer with a concrete production example.
**A:** A light ray grazing the Sun bends by 1.75 arcseconds; exact units and conventions reproduces this and more dramatic bending near a horizon. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What is a common misconception about units and conventions - justify your answer with a concrete production example.
**A:** That gravity is a force deflecting light; really units and conventions is geometry: light follows the straightest possible path in curved spacetime. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does units and conventions generalize for rotating black holes - justify your answer with a concrete production example.
**A:** The stationary axisymmetric Kerr metric replaces spherical symmetry; units and conventions gains a spin parameter and frame dragging enters. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What physical predictions come straight from units and conventions - justify your answer with a concrete production example.
**A:** Gravitational redshift, perihelion precession, light bending, frame dragging, and orbital decay from gravitational waves are all units and conventions consequences. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: What is the role of conserved quantities in units and conventions - justify your answer with a concrete production example.
**A:** Symmetries of the metric give constants along geodesics - energy, angular momentum, and (in Kerr) the Carter constant - which units and conventions uses to integrate efficiently. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How would a detector measure effects of units and conventions - justify your answer with a concrete production example.
**A:** Comparing clock rates, precision astrometry, or the shape of the photon ring all isolate signatures of units and conventions. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What numerical care does units and conventions require - justify your answer with a concrete production example.
**A:** The metric functions diverge at horizons and the coordinate singularities; switching to Kerr-Schild coordinates stabilizes units and conventions integration. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: How does units and conventions guide frame transformations in rendering - justify your answer with a concrete production example.
**A:** Radiation emitted in the fluid frame must be Lorentz-transformed to the coordinate frame; units and conventions supplies the needed boost toward a locally non-rotating observer. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: Why start with Schwarzschild before Kerr for units and conventions - justify your answer with a concrete production example.
**A:** Schwarzschild is spherically symmetric with simple constants, so units and conventions concepts are demonstrated and validated before spin complicates them. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What is the embedding-diagram view of units and conventions - justify your answer with a concrete production example.
**A:** A 2D slice of the geometry drawn inside a fictional flat space shows the funnel shape that beginners intuitively associate with units and conventions. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: What limits are placed by units and conventions on observables - justify your answer with a concrete production example.
**A:** Nothing escapes inside the horizon; the photon sphere at 1.5 Schwarzschild radii bounds where units and conventions says circular light orbits exist. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: How do you test the weak-field limit of units and conventions - justify your answer with a concrete production example.
**A:** Expanding the metric at large radius must recover Newtonian gravity plus the leading post-Newtonian corrections - the sanity check for units and conventions. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What does units and conventions say about time near a black hole - justify your answer with a concrete production example.
**A:** Clocks run slower deeper in the potential; units and conventions quantifies the ratio for a distant observer as the inverse redshift factor. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: How is units and conventions typically mis-stated in pop science - justify your answer with a concrete production example.
**A:** As 'light has no mass so how does gravity pull it' - units and conventions reframes it as path curvature, not a force on mass. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What documentation accompanies units and conventions in a research code - justify your answer with a concrete production example.
**A:** Every derivation, coordinate convention, and unit choice for units and conventions is written down so the integrator can be audited. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: Give one number a beginner should memorize for units and conventions - justify your answer with a concrete production example.
**A:** The photon sphere radius 3GM/C^2 (1.5 Schwarzschild radii) beyond which units and conventions orbiting light is possible. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: What is the next step after mastering units and conventions - justify your answer with a concrete production example.
**A:** Coding the geodesic integrator that units and conventions equations describe - the leap from theory to ray-traced pictures. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: What is the next step after mastering units and conventions - justify your answer with a concrete production example.
**A:** Coding the geodesic integrator that units and conventions equations describe - the leap from theory to ray-traced pictures. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: Give one number a beginner should memorize for units and conventions - justify your answer with a concrete production example.
**A:** The photon sphere radius 3GM/C^2 (1.5 Schwarzschild radii) beyond which units and conventions orbiting light is possible. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What documentation accompanies units and conventions in a research code - justify your answer with a concrete production example.
**A:** Every derivation, coordinate convention, and unit choice for units and conventions is written down so the integrator can be audited. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: How is units and conventions typically mis-stated in pop science - justify your answer with a concrete production example.
**A:** As 'light has no mass so how does gravity pull it' - units and conventions reframes it as path curvature, not a force on mass. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What does units and conventions say about time near a black hole - justify your answer with a concrete production example.
**A:** Clocks run slower deeper in the potential; units and conventions quantifies the ratio for a distant observer as the inverse redshift factor. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: How do you test the weak-field limit of units and conventions - justify your answer with a concrete production example.
**A:** Expanding the metric at large radius must recover Newtonian gravity plus the leading post-Newtonian corrections - the sanity check for units and conventions. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: What limits are placed by units and conventions on observables - justify your answer with a concrete production example.
**A:** Nothing escapes inside the horizon; the photon sphere at 1.5 Schwarzschild radii bounds where units and conventions says circular light orbits exist. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What is the embedding-diagram view of units and conventions - justify your answer with a concrete production example.
**A:** A 2D slice of the geometry drawn inside a fictional flat space shows the funnel shape that beginners intuitively associate with units and conventions. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: Why start with Schwarzschild before Kerr for units and conventions - justify your answer with a concrete production example.
**A:** Schwarzschild is spherically symmetric with simple constants, so units and conventions concepts are demonstrated and validated before spin complicates them. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: How does units and conventions guide frame transformations in rendering - justify your answer with a concrete production example.
**A:** Radiation emitted in the fluid frame must be Lorentz-transformed to the coordinate frame; units and conventions supplies the needed boost toward a locally non-rotating observer. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What numerical care does units and conventions require - justify your answer with a concrete production example.
**A:** The metric functions diverge at horizons and the coordinate singularities; switching to Kerr-Schild coordinates stabilizes units and conventions integration. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How would a detector measure effects of units and conventions - justify your answer with a concrete production example.
**A:** Comparing clock rates, precision astrometry, or the shape of the photon ring all isolate signatures of units and conventions. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: What is the role of conserved quantities in units and conventions - justify your answer with a concrete production example.
**A:** Symmetries of the metric give constants along geodesics - energy, angular momentum, and (in Kerr) the Carter constant - which units and conventions uses to integrate efficiently. A concrete example: consistently applying units and conventions in code review and regression tests keeps the whole pipeline trustworthy.
