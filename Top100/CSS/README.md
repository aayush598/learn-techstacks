# CSS Interview Questions and Answers (Top 100)

## Q1: What is the CSS box model?
**A:** Every element is a rectangular box composed of content, padding, border, and margin (from inside out). The total width = content + padding + border + margin.

## Q2: What is the difference between `content-box` and `border-box`?
**A:** `content-box` (default) includes only content in the declared width; padding/border are added outside. `border-box` includes padding and border within the declared width, making sizing predictable.

```css
* { box-sizing: border-box; }
```

## Q3: How do you set `box-sizing` globally?
**A:** Apply `box-sizing: border-box` to all elements (and `:before`/`:after`) so declared widths include padding and border.

## Q4: What are the parts of the box model in order?
**A:** Content → padding → border → margin, from innermost to outermost.

## Q5: Does margin collapse? Explain.
**A:** Yes, adjacent vertical margins of block-level siblings (and parent-child in some cases) collapse to the larger of the two, since margins are outside the box and shared.

## Q6: What is the difference between padding and margin?
**A:** Padding is inside the border and affects background area and element size; margin is outside the border and creates space between elements without a background.

## Q7: What are the types of CSS selectors?
**A:** Type, class, id, attribute, universal, pseudo-class, and pseudo-element selectors, plus combinators for relationships.

## Q8: What is a class selector?
**A:** It targets elements with a matching `class` attribute using a leading dot, e.g. `.btn` selects `<div class="btn">`.

## Q9: What is an id selector?
**A:** It targets a single element by its `id` using `#`, e.g. `#header`. IDs must be unique per page.

## Q10: What is an attribute selector?
**A:** It targets elements by attribute presence or value, e.g. `[type="text"]` or `[href^="https"]`.

## Q11: What are pseudo-classes? Give examples.
**A:** Pseudo-classes match elements in a specific state, e.g. `:hover`, `:focus`, `:nth-child()`, `:first-child`, `:not()`.

## Q12: What are pseudo-elements? Give examples.
**A:** Pseudo-elements style specific parts of an element, e.g. `::before` and `::after` create generated content, `::first-line`, `::selection`.

## Q13: What is the difference between `::before`/`::after` and `:hover`?
**A:** `::before`/`::after` are pseudo-elements (target generated content, two colons); `:hover` is a pseudo-class (targets a state, one colon).

## Q14: Explain descendant vs child combinator.
**A:** `div p` (descendant) matches any `<p>` inside a `<div>` at any depth; `div > p` (child) matches only direct `<p>` children.

## Q15: What is the adjacent sibling combinator?
**A:** `h2 + p` selects the `<p>` immediately following an `<h2>` as a sibling.

## Q16: What is the general sibling combinator?
**A:** `h2 ~ p` selects all `<p>` siblings that appear after an `<h2>`.

## Q17: How is CSS specificity calculated?
**A:** It is a tuple (inline styles, IDs, classes/attributes/pseudo-classes, elements/pseudo-elements). Higher counts win left-to-right; e.g. `#id .class` beats `.class div`.

## Q18: What is the specificity order from lowest to highest?
**A:** Universal `*` < type/elements < class/attribute/pseudo-class < id < inline style < `!important`.

## Q19: What does `!important` do?
**A:** It overrides normal specificity so the declaration wins regardless of order, except against another `!important` with higher specificity. Use sparingly.

## Q20: What is the cascade in CSS?
**A:** The cascade resolves conflicts between rules using source order, specificity, and importance to decide which declaration applies.

## Q21: What is inheritance in CSS?
**A:** Some properties (e.g. `color`, `font-family`) are inherited by child elements automatically unless overridden; others (like `margin`) are not.

## Q22: How do you prevent inheritance?
**A:** Set the property explicitly, or use `property: initial` to reset to the default, or `unset` to act as inherit/initial.

## Q23: What is the difference between `initial`, `inherit`, and `unset`?
**A:** `inherit` takes the parent's computed value; `initial` takes the property's default; `unset` uses `inherit` if inheritable, otherwise `initial`.

## Q24: What are the differences between px, em, and rem?
**A:** `px` is an absolute pixel; `em` is relative to the parent's font-size; `rem` is relative to the root (`html`) font-size.

## Q25: When would you use rem over em?
**A:** Use `rem` for predictable, consistent scaling from the root; `em` compounds through nested elements, which is useful for component-relative sizing.

## Q26: What are vw and vh units?
**A:** `vw` is 1% of viewport width; `vh` is 1% of viewport height. They size elements relative to the screen.

## Q27: What are vmin and vmax?
**A:** `vmin` is 1% of the smaller viewport dimension; `vmax` is 1% of the larger one.

## Q28: What are ch and ex units?
**A:** `ch` is the width of the "0" glyph; `ex` is the x-height of the font. They are font-relative units.

## Q29: What is the difference between % and vw?
**A:** `%` is relative to the parent element's size; `vw` is relative to the viewport width regardless of parent.

## Q30: How do you represent colors in CSS?
**A:** Via named colors, hex (`#fff`), `rgb()`/`rgba()`, `hsl()`/`hsla()`, and modern `oklch()`/`oklab()`.

## Q31: What is the difference between rgba and hsla?
**A:** Both add alpha; `rgba()` uses red/green/blue; `hsl()` uses hue/saturation/lightness, which is more intuitive for adjusting tones.

## Q32: What is oklch and why use it?
**A:** `oklch()` is a perceptual color space with better, more uniform gradients and accessible lightness control than hsl/rgb.

## Q33: What does `display: none` do?
**A:** It removes the element from rendering and layout entirely (no space reserved), unlike `visibility: hidden` which hides but keeps space.

## Q34: What is the difference between `display: block` and `inline`?
**A:** Block elements take full width and break lines; inline elements flow with text, ignore width/height, and don't force line breaks.

## Q35: What is `inline-block`?
**A:** It flows inline like text but respects width/height and vertical padding/margins like a block.

## Q36: What does `display: flex` do?
**A:** It turns the element into a flex container, laying children (flex items) out along a main axis with powerful alignment.

## Q37: What does `display: grid` do?
**A:** It creates a two-dimensional grid container where children are placed into rows and columns.

## Q38: Explain `position: static`.
**A:** The default; elements flow in normal document order and `top`/`left` have no effect.

## Q39: What is `position: relative`?
**A:** The element stays in flow but can be offset with `top/left` without affecting siblings; it also establishes a containing block.

## Q40: What is `position: absolute`?
**A:** The element is removed from flow and positioned relative to its nearest positioned ancestor.

## Q41: What is `position: fixed`?
**A:** The element is removed from flow and positioned relative to the viewport, staying put on scroll.

## Q42: What is `position: sticky`?
**A:** The element behaves as relative until it crosses a threshold, then sticks (like fixed) within its parent's bounds.

## Q43: How does `z-index` work?
**A:** It controls stacking order among positioned elements within the same stacking context; higher values appear on top.

## Q44: What is a stacking context?
**A:** A stacking context is created by properties like `position`+`z-index`, `opacity`, `transform`, etc.; `z-index` only compares within the same context.

## Q45: What is `overflow` and its common values?
**A:** It controls content that exceeds the box: `visible` (default), `hidden`, `scroll`, `auto`.

## Q46: What is the difference between `overflow: auto` and `scroll`?
**A:** `auto` shows scrollbars only when needed; `scroll` always shows them.

## Q47: How do you center a block element horizontally?
**A:** Set a width and `margin: 0 auto` to split remaining space evenly on both sides.

## Q48: How do you center text?
**A:** Use `text-align: center` on the container.

## Q49: How do you vertically center with Flexbox?
**A:** On the container: `display: flex; align-items: center;` (and `justify-content: center` for both axes).

## Q50: How do you center with CSS Grid?
**A:** Use `display: grid; place-items: center;` for both horizontal and vertical centering.

## Q51: How do you center an absolutely positioned element?
**A:** Set `top: 50%; left: 50%; transform: translate(-50%, -50%);` to offset by its own size.

## Q52: What is the clearfix hack?
**A:** A technique to contain floated children so the parent doesn't collapse, e.g. using `::after { content: ""; display: block; clear: both; }`.

## Q53: What is float used for today?
**A:** Mostly legacy; historically for wrapping text around images. Modern layout uses Flexbox/Grid instead.

## Q54: What are the main Flexbox container properties?
**A:** `flex-direction`, `flex-wrap`, `justify-content`, `align-items`, `align-content`, and `gap`.

## Q55: What does `justify-content` do?
**A:** It aligns flex items along the main axis (e.g. `flex-start`, `center`, `space-between`, `space-around`).

## Q56: What does `align-items` do?
**A:** It aligns items along the cross axis (e.g. `stretch`, `center`, `flex-start`, `baseline`).

## Q57: Explain `flex-grow`, `flex-shrink`, and `flex-basis`.
**A:** `flex-grow` is the share of free space taken; `flex-shrink` is how it shrinks when space is tight; `flex-basis` is the initial main size.

## Q58: What is the `flex` shorthand?
**A:** `flex: grow shrink basis`; common `flex: 1` means `flex: 1 1 0`, distributing space equally.

## Q59: What does `flex-wrap` do?
**A:** Allows items to wrap onto multiple lines instead of shrinking to fit one line.

## Q60: What does the `order` property do?
**A:** It changes the visual order of flex (or grid) items without altering the HTML source order.

## Q61: What is the `align-self` property?
**A:** It overrides `align-items` for a single flex item along the cross axis.

## Q62: What is CSS Grid's `fr` unit?
**A:** A fractional unit representing a share of available space in the grid container, e.g. `1fr 2fr`.

## Q63: How do you define grid columns and rows?
**A:** With `grid-template-columns` and `grid-template-rows`, e.g. `grid-template-columns: 100px 1fr 1fr;`.

## Q64: What is `grid-gap` / `gap`?
**A:** `gap` sets spacing between grid (and flex) tracks; modern syntax is just `gap`, replacing `grid-gap`.

## Q65: What is `grid-template-areas`?
**A:** It lets you lay out the grid using named template regions for readable, visual placement.

```css
grid-template-areas: "header header" "sidebar main";
```

## Q66: How do you place an item in a named grid area?
**A:** Set `grid-area: header;` on the item to assign it to that named region.

## Q67: What is `minmax()`?
**A:** It defines a track size range, e.g. `minmax(200px, 1fr)` allows growth but enforces a minimum.

## Q68: What does `repeat()` do?
**A:** It repeats track definitions, e.g. `repeat(3, 1fr)` creates three equal columns.

## Q69: What is the difference between explicit and implicit grid?
**A:** Explicit tracks are defined by `grid-template-*`. Implicit tracks are auto-created for items overflowing the defined grid, sized by `grid-auto-rows/columns`.

## Q70: What is `grid-auto-flow`?
**A:** It controls how auto-placed items fill the implicit grid: `row` (default), `column`, or `dense`.

## Q71: What is `subgrid`?
**A:** A nested grid that inherits its parent's track sizing, keeping alignment across nested components.

## Q72: How do you add a transition?
**A:** Use `transition: property duration timing-function delay;` to animate changes between states.

```css
.button { transition: background-color 0.3s ease; }
```

## Q73: What is `transform` and its functions?
**A:** It visually modifies an element: `translate()`, `rotate()`, `scale()`, `skew()`, and `matrix()`.

## Q74: What is `transform-origin`?
**A:** It sets the point around which transforms (rotate/scale) are applied, defaulting to center.

## Q75: How do you create a CSS animation?
**A:** Define `@keyframes` and apply it with `animation: name duration ...` on the element.

```css
@keyframes spin { to { transform: rotate(360deg); } }
```

## Q76: What are key animation properties?
**A:** `animation-name`, `duration`, `timing-function`, `delay`, `iteration-count`, `direction`, `fill-mode`, and `play-state`.

## Q77: What is the difference between transition and animation?
**A:** Transitions animate between two states triggered by a change; animations run predefined keyframes independently and can loop.

## Q78: How do you use CSS variables?
**A:** Define with `--name` (often on `:root`) and consume with `var(--name, fallback)`.

```css
:root { --primary: #3498db; }
.btn { background: var(--primary); }
```

## Q79: What is a fallback in `var()`?
**A:** The second argument used when the variable is undefined, e.g. `var(--gap, 16px)`.

## Q80: What is the difference between `:root` and `html`?
**A:** `:root` matches the document root (html) but has higher specificity, making it ideal for global variables.

## Q81: What are media queries?
**A:** Conditional blocks applying CSS based on device characteristics like width, height, or resolution.

```css
@media (max-width: 600px) { .nav { display: none; } }
```

## Q82: What is mobile-first design?
**A:** Write base styles for small screens, then use `min-width` media queries to enhance larger screens progressively.

## Q83: What are `clamp()`, `min()`, and `max()`?
**A:** `clamp(min, val, max)` bounds a value; `min()` picks the smallest; `max()` picks the largest — all usable in any length context.

```css
font-size: clamp(1rem, 2vw + 1rem, 2rem);
```

## Q84: What does `calc()` do?
**A:** It performs math with mixed units, e.g. `width: calc(100% - 80px);`.

## Q85: What are container queries?
**A:** They let styles respond to a container's size (`@container`) rather than the viewport, enabling component-based responsiveness.

```css
@container (min-width: 400px) { .card { grid-template-columns: 2; } }
```

## Q86: What is the `:has()` selector?
**A:** A parent/previous-sibling selector: `article:has(img)` matches articles containing an image (the "parent" selector).

## Q87: What is `aspect-ratio`?
**A:** It sets an element's width-to-height ratio, e.g. `aspect-ratio: 16 / 9;` for responsive video boxes.

## Q88: What is `gap` in Flexbox?
**A:** Modern Flexbox supports `gap` for consistent spacing between items, avoiding margins.

## Q89: How do you use web fonts with `@font-face`?
**A:** Declare a font family with a `src` URL and apply it; `font-display` controls loading behavior.

```css
@font-face { font-family: "My"; src: url("my.woff2") format("woff2"); font-display: swap; }
```

## Q90: What is `font-display: swap`?
**A:** It shows fallback text immediately and swaps to the custom font once loaded, avoiding invisible text (FOIT).

## Q91: What properties affect typography?
**A:** `font-family`, `font-size`, `font-weight`, `line-height`, `letter-spacing`, `text-transform`, and `font-style`.

## Q92: What is a good `line-height` practice?
**A:** Use unitless values (e.g. `line-height: 1.5`) so it scales with the element's font-size.

## Q93: How do you create a linear gradient?
**A:** Use `background: linear-gradient(direction, color stops)` for smooth color transitions.

```css
background: linear-gradient(90deg, red, blue);
```

## Q94: How do you use multiple backgrounds?
**A:** Separate layers with commas, earliest on top: `background: url(a.png), linear-gradient(...);`.

## Q95: What do `background-size` and `background-position` do?
**A:** `background-size` scales the image (`cover`/`contain`/lengths); `background-position` sets its placement.

## Q96: How do you add shadows?
**A:** `box-shadow` for element boxes and `text-shadow` for text, each with offset, blur, spread, and color.

```css
box-shadow: 0 4px 8px rgba(0,0,0,0.2);
```

## Q97: How do you make rounded corners?
**A:** Use `border-radius` with a length or percentage; `50%` creates circles/ellipses.

## Q98: What is the difference between a CSS reset and Normalize.css?
**A:** A reset removes all default browser styling; Normalize.css preserves useful defaults and fixes cross-browser inconsistencies.

## Q99: How do you support dark mode?
**A:** Use `@media (prefers-color-scheme: dark)` to apply dark palettes, often via CSS variables.

```css
@media (prefers-color-scheme: dark) { :root { --bg: #000; } }
```

## Q100: How do you respect reduced motion for accessibility?
**A:** Wrap animations in `@media (prefers-reduced-motion: reduce)` to disable or minimize motion for sensitive users.

```css
@media (prefers-reduced-motion: reduce) { * { animation: none; transition: none; } }
```
