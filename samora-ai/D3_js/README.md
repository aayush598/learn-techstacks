# D3.js Interview Questions and Answers

## Q1: What is D3.js?
**A:** D3.js (Data-Driven Documents) is a JavaScript library for producing dynamic, interactive data visualizations in web browsers using SVG, HTML, and CSS.

## Q2: What does D3 stand for?
**A:** D3 stands for Data-Driven Documents.

## Q3: What is the core philosophy of D3.js?
**A:** D3 binds data to DOM elements and then applies data-driven transformations to the document, enabling full control over the final visual representation.

## Q4: How does D3.js differ from Chart.js or Highcharts?
**A:** D3 is a low-level visualization library that gives full control over the visual output, while Chart.js and Highcharts are higher-level charting libraries with pre-built chart types and less customization.

## Q5: What is a selection in D3?
**A:** A selection is a D3 object that represents a set of DOM elements, allowing you to manipulate them using methods like `attr`, `style`, `text`, and `classed`.

## Q6: What is the difference between `d3.select` and `d3.selectAll`?
**A:** `d3.select` returns the first matching element, while `d3.selectAll` returns all matching elements as a grouped selection.

## Q7: What is a data join in D3?
**A:** A data join binds an array of data to DOM elements, pairing each datum with a corresponding element using the `data()` method.

## Q8: Explain the enter-update-exit pattern.
**A:** After joining data, `enter` creates new elements for data without matching DOM nodes, `exit` removes DOM nodes without matching data, and the merged selection updates existing elements.

## Q9: What does the `enter` selection contain?
**A:** The `enter` selection contains placeholder nodes for each data item that does not have a corresponding DOM element.

## Q10: What does the `exit` selection contain?
**A:** The `exit` selection contains existing DOM elements that no longer have corresponding data items, typically used for removal.

## Q11: How do you merge enter and update selections?
**A:** Use `selection.merge(enterSelection)` to combine the update and enter selections so that both sets of elements receive the same attributes and styles.

## Q12: What is the `data()` method in D3?
**A:** `data()` binds an array of data to a selection, optionally using a key function to match data to elements by identity rather than index.

## Q13: What is the `datum()` method?
**A:** `datum()` binds a single data value to each element in a selection, unlike `data()` which expects an array.

## Q14: What is a key function in data joins?
**A:** A key function is passed to `data()` to control how data items are matched to DOM elements, ensuring stable updates across re-renders.

## Q15: What is `d3.scaleLinear`?
**A:** It creates a linear scale that maps continuous input domain values to a continuous output range using a linear transformation.

## Q16: What is `d3.scaleOrdinal`?
**A:** It maps discrete categorical input values to discrete output values, typically used for assigning colors to categories.

## Q17: What is `d3.scaleTime`?
**A:** It is a scale similar to `scaleLinear` but specialized for JavaScript `Date` objects as the input domain.

## Q18: What is `d3.scaleBand`?
**A:** It creates a band scale for ordinal data with a continuous output range, automatically dividing the range into equal-width bands with optional padding.

## Q19: What is `d3.scaleSqrt`?
**A:** It creates a square root scale, useful for scaling circle areas where the visual area should be proportional to the data value.

## Q20: What is `d3.scaleLog`?
**A:** It creates a logarithmic scale where the output is proportional to the logarithm of the input, useful for data spanning multiple orders of magnitude.

## Q21: How do you create an axis in D3?
**A:** Use `d3.axisBottom()`, `d3.axisLeft()`, `d3.axisTop()`, or `d3.axisRight()` and call them on a selection to render tick marks and labels.

## Q22: What is `d3.axisBottom`?
**A:** It creates a horizontal axis with ticks below the axis line, typically used for the x-axis at the bottom of a chart.

## Q23: How do you customize axis ticks?
**A:** Use `axis.tickValues()`, `axis.tickFormat()`, `axis.ticks(count)`, and `axis.tickSize()` to control tick placement, formatting, count, and length.

## Q24: What is an SVG element?
**A:** SVG (Scalable Vector Graphics) is an XML-based vector image format used by D3 to render scalable, resolution-independent visualizations.

## Q25: How do you create an SVG element with D3?
**A:** Use `d3.select(container).append(svg).attr(width, w).attr(height, h)` to create and configure an SVG element.

## Q26: What is a `g` element in SVG?
**A:** The `g` (group) element is a container used to group related SVG shapes together, allowing collective transformations and styling.

## Q27: How do you draw a circle in D3?
**A:** Append a `circle` element and set its `cx`, `cy`, and `r` attributes using D3 selection methods.

## Q28: How do you draw a rectangle in D3?
**A:** Append a `rect` element and set its `x`, `y`, `width`, `height`, and optionally `rx`/`ry` attributes.

## Q29: What is `d3.line`?
**A:** `d3.line()` creates a line generator function that produces a path data string from an array of points for drawing lines.

## Q30: What is `d3.area`?
**A:** `d3.area()` creates an area generator that produces a filled region defined by a top line and a bottom baseline.

## Q31: What is `d3.arc`?
**A:** `d3.arc()` creates an arc generator used to produce pie/donut chart segments with inner and outer radius and start/end angles.

## Q32: What is `d3.pie`?
**A:** `d3.pie()` computes the start and end angles for an array of data, preparing it for use with an arc generator to draw a pie chart.

## Q33: How do you create a simple bar chart in D3?
**A:** Bind data to `rect` elements, map data values to the `height` and `y` attributes using a linear scale, and use `d3.axisBottom` for the x-axis.

## Q34: How do you create a line chart in D3?
**A:** Use `d3.line()` to generate a path from data points, bind the path data to a `path` element, and render axes with appropriate scales.

## Q35: How do you create a scatter plot in D3?
**A:** Bind data to `circle` elements, use linear scales for x and y positions, and set `cx`, `cy`, and `r` attributes accordingly.

## Q36: How do you create a pie chart in D3?
**A:** Use `d3.pie()` to compute angles from data, then use `d3.arc()` with those angles to generate SVG path data for each slice.

## Q37: What is a layout in D3?
**A:** A layout is a data transformation function that computes positional information from data, such as `d3.stack`, `d3.force`, `d3.tree`, and `d3.partition`.

## Q38: What is `d3.stack`?
**A:** `d3.stack()` computes stacked series from multi-dimensional data, producing per-series arrays with baseline and top values for stacked bar/area charts.

## Q39: What is `d3.force`?
**A:** `d3.force` is a simulation module for physics-based layouts, commonly used for network graphs where nodes repel and edges attract.

## Q40: What is a force-directed graph?
**A:** A graph layout where nodes are positioned by simulating physical forces (repulsion, attraction, gravity) until the system reaches equilibrium.

## Q41: What forces are available in `d3.force`?
**A:** Common forces include `forceManyBody` (repulsion), `forceLink` (edge attraction), `forceCenter` (centering), `forceCollide` (collision avoidance), and `forceX`/`forceY`.

## Q42: How do you start a force simulation?
**A:** Create a simulation with `d3.forceSimulation(nodes)`, configure forces with `.force()`, and listen to the `tick` event to update positions.

## Q43: What is `d3.tree`?
**A:** `d3.tree()` creates a tree layout that positions nodes in a tidy hierarchical arrangement from root to leaves.

## Q44: What is `d3.cluster`?
**A:** `d3.cluster()` creates a dendrogram layout where leaf nodes are placed at equal depths, useful for clustering visualizations.

## Q45: What is `d3.partition`?
**A:** `d3.partition()` creates a space-filling layout that recursively subdivides a rectangular area into nodes proportional to their value, such as in icicle or sunburst diagrams.

## Q46: What is `d3.chord`?
**A:** `d3.chord()` computes the chord layout for visualizing directed relationships in a matrix, often drawn as arcs between groups on a circle.

## Q47: How do transitions work in D3?
**A:** Call `selection.transition()` to animate changes to attributes and styles over a specified duration using easing functions.

## Q48: How do you set transition duration?
**A:** Use `.duration(milliseconds)` on a transition to specify how long the animation lasts.

## Q49: How do you add a delay to a transition?
**A:** Use `.delay(milliseconds)` to stagger animations across elements, often using a function of the index or data.

## Q50: What is an easing function in D3?
**A:** An easing function controls the animation's speed curve, such as `d3.easeLinear`, `d3.easeCubicInOut`, `d3.easeBounce`, or `d3.easeElastic`.

## Q51: How do you chain transitions?
**A:** Use `.transition()` again in the `.on(end, ...)` callback or chain `.transition()` after a preceding transition to create sequential animations.

## Q52: What are D3 modules?
**A:** D3 is modular; its functionality is split into packages like `d3-array`, `d3-scale`, `d3-shape`, `d3-selection`, `d3-transition`, `d3-force`, and `d3-geo`.

## Q53: What is `d3-array` used for?
**A:** `d3-array` provides array manipulation utilities including statistics functions like `d3.min`, `d3.max`, `d3.extent`, `d3.mean`, and `d3.bisect`.

## Q54: What is `d3-shape` used for?
**A:** `d3-shape` provides geometric shape generators including `d3.line`, `d3.area`, `d3.arc`, `d3.pie`, `d3.symbol`, and `d3.stack`.

## Q55: What is `d3-geo` used for?
**A:** `d3-geo` provides geographic projection and path generation for creating maps, including `d3.geoAlbersUsa`, `d3.geoMercator`, and `d3.geoPath`.

## Q56: What is a geographic projection in D3?
**A:** A projection is a function that converts spherical latitude/longitude coordinates to planar x/y coordinates for rendering maps.

## Q57: What is `d3.geoPath`?
**A:** `d3.geoPath()` generates SVG path data for geographic features (countries, states) using a specified projection and GeoJSON data.

## Q58: How do you create a choropleth map in D3?
**A:** Use a color scale to map data values to fill colors, then apply the scale to geographic features rendered with `d3.geoPath`.

## Q59: How do you implement zooming in D3?
**A:** Use `d3.zoom()` to create a zoom behavior, then apply it to a selection and handle the `zoom` event to update scales and elements.

## Q60: How do you implement panning in D3?
**A:** Panning is built into `d3.zoom()`; dragging the canvas translates the view automatically when the zoom behavior is applied.

## Q61: What is `d3.zoomIdentity`?
**A:** `d3.zoomIdentity` represents the identity transform (translate 0,0 and scale 1), used to reset zoom or programmatically set zoom state.

## Q62: What is brushing in D3?
**A:** Brushing is an interactive selection technique using `d3.brush()` that lets users select a rectangular region to filter or highlight data.

## Q63: How do you use `d3.drag`?
**A:** `d3.drag()` creates a drag behavior; apply it to a selection and handle `start`, `drag`, and `end` events to move elements interactively.

## Q64: What is the difference between SVG and Canvas with D3?
**A:** SVG is element-based, easier for interactivity, and works well for up to a few thousand elements, while Canvas is pixel-based and better for large datasets with lower memory overhead.

## Q65: When should you use Canvas over SVG in D3?
**A:** Use Canvas when rendering more than 5,000-10,000 elements, when performance is critical, or for pixel-level control like heatmaps.

## Q66: How do you render D3 on Canvas?
**A:** D3 binds data and computes positions, but instead of setting SVG attributes, you draw directly to a Canvas context in the data join or animation loop.

## Q67: How do you create responsive D3 charts?
**A:** Use `viewBox` and `preserveAspectRatio` on the SVG, and listen for `resize` events to recalculate scales and re-render.

## Q68: What is a reusable chart in D3?
**A:** A reusable chart is a function-based pattern that encapsulates chart logic as a configurable module, following the convention of D3's own components.

## Q69: How do you use D3 with React?
**A:** Use a `useRef` to attach the D3 selection to a DOM node, run D3 code inside `useEffect`, and clean up on unmount to avoid memory leaks.

## Q70: What are common pitfalls when using D3 with React?
**A:** Direct DOM manipulation by D3 conflicts with React's virtual DOM; always isolate D3 within a dedicated container and manage lifecycle with hooks.

## Q71: How do you use D3 with Angular?
**A:** Create a directive or component, access the native element via `ElementRef`, and execute D3 code in `ngAfterViewInit` with cleanup in `ngOnDestroy`.

## Q72: What is `d3.format`?
**A:** `d3.format()` returns a function that formats numbers into strings using locale-aware formatting, similar to Python's format specification.

## Q73: What is `d3.timeFormat`?
**A:** `d3.timeFormat()` creates a function to format JavaScript Date objects into human-readable strings using specifiers like `%Y`, `%m`, and `%d`.

## Q74: What is `d3.timeParse`?
**A:** `d3.timeParse()` creates a function that parses date strings into JavaScript Date objects based on a given format specifier.

## Q75: How do you handle missing data in D3?
**A:** Use array methods like `Array.filter` before joining data, or use `d3.defined()` with line/area generators to create gaps for undefined values.

## Q76: What is `d3.quantile`?
**A:** `d3.quantile()` returns the quantile value from a sorted array, useful for box plots and statistical visualizations.

## Q77: What is `d3.bisect`?
**A:** `d3.bisect` provides binary search utilities to find the insertion point for a value in a sorted array, commonly used for data lookup in time series.

## Q78: What is `d3.hierarchy`?
**A:** `d3.hierarchy()` constructs a hierarchical data structure from flat data, providing methods like `sum`, `sort`, `descendants`, and `links`.

## Q79: What is `d3.pack`?
**A:** `d3.pack()` creates a circular packing layout where nodes are nested circles whose areas are proportional to their data values.

## Q80: What is `d3.treemap`?
**A:** `d3.treemap()` creates a space-filling rectangular layout for hierarchical data, useful for showing proportions across nested categories.

## Q81: What is `d3.histogram`?
**A:** `d3.histogram()` (now `d3.bin()`) bins continuous data into discrete intervals and computes frequency counts for histogram visualizations.

## Q82: How do you add tooltips in D3?
**A:** Append a hidden `div` or SVG `text`/`rect` element, show it on `mouseover` events, position it with the mouse coordinates, and hide on `mouseout`.

## Q83: How do you add legends in D3?
**A:** Manually create legend elements by binding scale domain values to small colored `rect` or `circle` shapes with accompanying text labels.

## Q84: What is `d3.symbol`?
**A:** `d3.symbol()` produces path data for predefined shapes like circles, crosses, diamonds, squares, stars, triangles, and wye symbols for scatter plots.

## Q85: What is `d3.interpolate`?
**A:** `d3.interpolate` provides interpolation functions for smoothly transitioning between values, used internally by transitions and scales.

## Q86: How do you create a color scale in D3?
**A:** Use `d3.scaleOrdinal(d3.schemeCategory10)` for categorical colors or `d3.scaleSequential(d3.interpolateViridis)` for continuous color ramps.

## Q87: What are D3 scheme color interpolators?
**A:** Built-in color schemes like `d3.schemeCategory10`, `d3.interpolateBlues`, `d3.interpolateViridis`, and `d3.interpolateRdYlGn` provide predefined color palettes.

## Q88: What is `d3.curve` in the context of line/area generators?
**A:** Curve factories like `d3.curveLinear`, `d3.curveBasis`, `d3.curveCardinal`, `d3.curveMonotoneX`, and `d3.curveStep` control how lines interpolate between points.

## Q89: How do you optimize D3 performance for large datasets?
**A:** Use Canvas instead of SVG, limit DOM manipulations with data joins, reduce redraws with throttled events, and use Web Workers for heavy computations.

## Q90: What are D3 v7 features?
**A:** D3 v7 includes flat namespacing, improved `d3-array` methods, `d3.blob` and `d3.buffer` for binary data, and continued ES module support.

## Q91: How does D3 v7 differ from v5?
**A:** D3 v7 removed the `d3-request` module in favor of `fetch`, adopted flat module namespacing, and deprecated legacy APIs like `d3.event`.

## Q92: What is the `d3.local` module?
**A:** `d3.local` declares local variables scoped to DOM elements, useful for storing per-element state without polluting data objects.

## Q93: How do you create a horizontal bar chart in D3?
**A:** Swap the roles of x and y: use `scaleLinear` for the x-axis (width) and `scaleBand` with `bandwidth()` for the y-axis (categories).

## Q94: How do you create a grouped bar chart in D3?
**A:** Use nested data joins or compute sub-band offsets manually, applying separate scales or sub-ranges for each group within each category.

## Q95: How do you create a donut chart in D3?
**A:** Use `d3.arc()` with a non-zero `innerRadius` applied to pie-computed angles, leaving a hollow center.

## Q96: What is a streamgraph in D3?
**A:** A streamgraph is a stacked area chart with a centered baseline, created using `d3.stack().offset(d3.stackOffsetWiggle)` and `d3.area`.

## Q97: How do you handle events in D3?
**A:** Use `selection.on(eventType, handler)` for DOM events, and access event data via the `event` parameter and bound datum via `d3.select(this).datum()`.

## Q98: What is `d3.mouse`?
**A:** `d3.mouse(container)` returns the mouse position relative to a given container, useful for positioning tooltips and interactive elements.

## Q99: How do you export a D3 chart as an image?
**A:** Serialize the SVG to XML string, create a Blob URL, load it into an `Image`, draw onto a Canvas, and use `canvas.toDataURL()` for PNG/JPEG export.

## Q100: What are the best practices for D3 project structure?
**A:** Organize by component or chart type, use reusable chart pattern, separate data loading from rendering, and keep D3 logic isolated from framework code.
