# Measurement Fundamentals - Concepts

## 1. Basic Measurement System
A measurement system converts a physical quantity into a readable output.
Components: Primary sensing element → Variable conversion → Variable manipulation → Data transmission → Data presentation

## 2. Accuracy
Closeness of measured value to the true (accepted) value.
Expressed as % of full-scale deflection (FSD) or % of reading.
Accuracy = 1 - |True Value - Measured Value| / True Value

## 3. Precision
Closeness of agreement among independent test results obtained under stipulated conditions.
Related to repeatability and reproducibility.
High precision does NOT imply high accuracy.

## 4. Resolution
Smallest detectable change in the input that produces a measurable change in output.
For digital instruments: smallest step size (1 LSB).
For analog instruments: typically 1/2 of smallest division.

## 5. Sensitivity
Ratio of change in output to change in input (S = ΔOutput / ΔInput).
For a voltmeter: sensitivity = R_v / V_range (ohms per volt).
Higher sensitivity means less loading effect.

## 6. Error Types

### 6.1 Systematic Errors (Deterministic)
Consistent, repeatable errors from known causes.
- Instrumental errors: calibration drift, worn parts
- Environmental errors: temperature, humidity, pressure
- Observational errors: parallax, personal bias
- Method errors: approximations in measurement theory

### 6.2 Random Errors (Indeterminate)
Unpredictable fluctuations from unknown causes.
Follow Gaussian (normal) distribution.
Reduced by statistical averaging over many measurements.

### 6.3 Gross Errors (Blunders)
Human mistakes: misreading, incorrect recording, wrong connections.
Cannot be corrected mathematically; must be identified and eliminated.

## 7. Loading Effect
When a measuring instrument draws energy from the circuit under test, it alters the circuit behavior.
Voltage measurement: voltmeter with finite resistance draws current → voltage drop across source resistance → measured V < true V.
Minimize by using high-input-impedance instruments (FET-based, digital).

## 8. Null Type vs Deflection Type

### 8.1 Deflection Type
Output is proportional to the quantity being measured.
Example: PMMC moving-coil galvanometer.
- Simple, direct reading
- Subject to loading effect
- Accuracy limited by friction, calibration

### 8.2 Null Type
Instrument is balanced until output = zero.
Example: Wheatstone bridge.
- Higher accuracy (no loading at balance)
- Slower (requires manual/automatic balancing)
- Accuracy depends on standard components, not on galvanometer calibration

## 9. Static Characteristics
- Sensitivity
- Resolution
- Accuracy and Precision
- Linearity
- Dead zone
- Range (span)
- Repeatability

## 10. Dynamic Characteristics
Response to time-varying inputs.
- Speed of response
- Fidelity
- Lag
- Dynamic error

## 11. Standards
- International standard (SI units)
- Primary standard (national labs like NPL)
- Secondary standard (calibration labs)
- Working standard (industrial labs)

## 12. Calibration
Comparison of instrument reading with a standard of known accuracy.
Calibration curve: plot of instrument output vs standard input.
Hysteresis in calibration: difference in readings when input increases vs decreases.

## 13. Figure of Merit
- For analog: % accuracy of full-scale deflection
- For digital: number of digits + 1 (half digit)
  Example: 3½ digit DVM reads 0 to 1999 → resolution = 1 mV on 2V range

## 14. Measuring Methods
- Direct method: compare with standard directly
- Comparison method: bridge, potentiometer
- Substitution method: replace unknown with standard
- Differential method: measure difference from known
- Deflection method: instrument deflects proportionally

## 15. ISRO Focus Areas
- Loading effect calculations for voltmeters
- Relationship between accuracy, precision, resolution
- Null type vs deflection type trade-offs
- Error analysis: combination of systematic and random errors (RSS for random)
