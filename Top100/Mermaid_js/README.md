# Mermaid.js Interview Questions and Answers

## Q1: What is Mermaid.js?
**A:** Mermaid.js is a JavaScript-based diagramming and charting tool that renders Markdown-inspired text definitions into dynamic diagrams in the browser.

## Q2: How does Mermaid.js work?
**A:** It parses text definitions written in a Markdown-like syntax and generates SVG or PNG diagrams via an internal rendering engine, enabling a text-to-diagram workflow.

## Q3: What does "text-to-diagram" mean?
**A:** It means you write diagram definitions in plain text (like `graph TD; A-->B;`) and Mermaid converts them into visual diagrams automatically.

## Q4: What diagram types does Mermaid.js support?
**A:** It supports flowchart, sequence diagram, class diagram, state diagram, entity-relationship diagram, Gantt chart, pie chart, quadrant chart, requirement diagram, user journey, git graph, mindmap, timeline, and C4 context diagram.

## Q5: How do you define a flowchart in Mermaid?
**A:** Use `graph` followed by direction (`TD`, `LR`, `BT`, `RL`) and then define nodes and edges, for example: `graph TD; A-->B; A-->C;`.

## Q6: What node shapes are available in flowcharts?
**A:** Common shapes include rectangle (default), rounded (`A[text]`), stadium (`A([text])`), subroutine (`A[[text]]`), cylinder (`A[(text)]`), diamond (`A{text}`), and hexagon (`A{{text}}`).

## Q7: How do you add edges in a flowchart?
**A:** Use `-->` for arrow, `---` for line, `==>` for thick arrow, `-.->` for dotted arrow, and `--text-->` for labeled edges.

## Q8: How do you create subgraphs in a flowchart?
**A:** Use `subgraph title ... end` to group nodes into a named subgraph, optionally with a background color.

## Q9: How do you style nodes in a flowchart?
**A:** Use `style nodeId fill:#color,stroke:#color,stroke-width:2px` or apply classes with `classDef` and `class` statements.

## Q10: What is a sequence diagram in Mermaid?
**A:** It shows object interactions arranged in time sequence, defined with `sequenceDiagram` keyword followed by participants and messages.

## Q11: How do you define participants in a sequence diagram?
**A:** Use `participant Alice` or `actor Bob` to declare participants explicitly; they can also be auto-created by message references.

## Q12: How do you show messages in a sequence diagram?
**A:** Use `Alice->>Bob: Message text` for solid arrow, `->` for dashed, `->>` for dotted arrow, and `-->>` for dashed arrow with text.

## Q13: How do you add notes in a sequence diagram?
**A:** Use `Note right of Alice: Note text`, `Note left of Bob: Note text`, or `Note over Alice,Bob: Note text`.

## Q14: How do you create loops in a sequence diagram?
**A:** Use `loop Loop title ... end` to wrap messages that repeat.

## Q15: How do you create conditional paths with alt/opt in sequence diagrams?
**A:** Use `alt Description ... else ... end` for alternatives and `opt Description ... end` for optional paths.

## Q16: How do you represent activation boxes in sequence diagrams?
**A:** Use `activate Alice` and `deactivate Alice` around messages to show when a participant is active.

## Q17: What is a class diagram in Mermaid?
**A:** It models the structure of a system by showing classes, their attributes, methods, and relationships, defined with `classDiagram` keyword.

## Q18: How do you define a class in a class diagram?
**A:** Use `class ClassName` and optionally add a `:` followed by attributes and methods, e.g., `class Animal { +String name +run() }`.

## Q19: How do you show relationships between classes?
**A:** Use `ClassA --|> ClassB` for inheritance, `ClassA --> ClassB` for association, `ClassA o-- ClassB` for aggregation, `ClassA *-- ClassB` for composition, and `ClassA ..> ClassB` for dependency.

## Q20: How do you specify visibility markers in class diagrams?
**A:** Use `+` for public, `-` for private, `#` for protected, and `~` for package-private before attribute or method names.

## Q21: What is an entity-relationship diagram (ERD) in Mermaid?
**A:** It shows entities and their relationships in a database schema, defined with `erDiagram` keyword using `ENTITY [attributes]` syntax.

## Q22: How do you define relationships in an ERD?
**A:** Use `ENTITY1 ||--o{ ENTITY2 : "label"` where `||` means one, `o{` means zero or many, and other cardinality tokens express optionality.

## Q23: What cardinality notations does Mermaid ERD support?
**A:** It supports `|o` (zero or one), `||` (exactly one), `}o` (zero or many), and `}|` (one or many).

## Q24: What is a state diagram in Mermaid?
**A:** It models state machines showing states and transitions, defined with `stateDiagram-v2` keyword.

## Q25: How do you define states and transitions?
**A:** Use `[*] --> State1` for start, `State1 --> State2 : Event` for transitions, and `State1 --> [*]` for end state.

## Q26: How do you create composite states in a state diagram?
**A:** Use `state StateName { ... }` to nest sub-states within a composite state.

## Q27: What is a Gantt chart in Mermaid?
**A:** It visualizes a project schedule with tasks along a timeline, defined with `gantt` keyword, including date format, title, and task sections.

## Q28: How do you define tasks in a Gantt chart?
**A:** Use `task name : status, start date, duration` where status can be `done`, `active`, `crit`, or `milestone`.

## Q29: How do you handle dependencies in Gantt charts?
**A:** Dependencies are implicit by ordering, or you can use `after taskId` to make a task depend on another.

## Q30: How do you define milestones in a Gantt chart?
**A:** Use a task with `milestone` status and `crit` marker, e.g., `Milestone Name : milestone, 2024-01-01, 0d`.

## Q31: What is a pie chart in Mermaid?
**A:** A circular statistical chart divided into slices, defined with `pie` keyword followed by `"Label" : value` pairs.

## Q32: How do you create a pie chart?
**A:** Write `pie title My Title "Category A" : 30 "Category B" : 70` and Mermaid renders a proportional pie chart.

## Q33: What is a quadrant chart in Mermaid?
**A:** It plots points in four quadrants based on two dimensions, defined with `quadrantChart` keyword, useful for prioritization matrices.

## Q34: How do you define points in a quadrant chart?
**A:** Use `point "Label" : [x, y]` with optional quadrant colors and axis labels via configuration.

## Q35: What is a requirement diagram in Mermaid?
**A:** It visualizes requirements and their relationships, defined with `requirementDiagram` keyword, supporting `requirement`, `element`, `satisfies`, `verifies`, and `contains`.

## Q36: How do you define a requirement in a requirement diagram?
**A:** Use `requirement "Req Name" { id: 1, text: "description", risk: high, verifymethod: test }`.

## Q37: What is a user journey diagram in Mermaid?
**A:** It describes user tasks and their satisfaction scores across different personas, defined with `journey` keyword.

## Q38: How do you create a user journey diagram?
**A:** Use `journey title My Journey section Section Name Task A: 5: PersonaA, PersonaB Task B: 3: PersonaA`.

## Q39: What is a git graph in Mermaid?
**A:** It visualizes Git branches, commits, and merge operations, defined with `gitGraph` keyword.

## Q40: How do you simulate commits in a git graph?
**A:** Use `commit` with optional `tag` or `id` to add commits to the current branch.

## Q41: How do you create branches in a git graph?
**A:** Use `branch branchName` to create a new branch from the current position.

## Q42: How do you merge branches in a git graph?
**A:** Use `merge branchName` to merge another branch into the current branch, optionally with a tag.

## Q43: What is a mindmap in Mermaid?
**A:** It creates a hierarchical radial diagram around a central idea, defined with `mindmap` keyword using indentation for levels.

## Q44: How do you define a mindmap?
**A:** Write `mindmap root((Central Idea)) Branch1 SubBranch1 SubBranch2 Branch2` with indentation for hierarchy.

## Q45: What is a timeline diagram in Mermaid?
**A:** It displays events chronologically along a horizontal line, defined with `timeline` keyword.

## Q46: How do you define a timeline?
**A:** Use `timeline title History section Era Period : Event 1 : Event 2` with sections and time periods.

## Q47: What is a C4 context diagram in Mermaid?
**A:** It models software architecture at the context level, defined with `C4Context` keyword showing a system and its users and dependencies.

## Q48: What C4 diagram levels does Mermaid support?
**A:** It supports `C4Context`, `C4Container`, `C4Component`, and `C4Dynamic` for different levels of architectural detail.

## Q49: How do you define a person in a C4 diagram?
**A:** Use `Person(personAlias, "Name", "Description")` to define a system actor.

## Q50: How do you define a system in a C4 diagram?
**A:** Use `System(systemAlias, "Name", "Description")` to define a software system boundary.

## Q51: How do you define relationships in C4 diagrams?
**A:** Use `Rel(personAlias, systemAlias, "Label", "Technology")` to define a directed relationship between elements.

## Q52: How do you define system boundaries in C4 diagrams?
**A:** Use `System_Boundary(alias, "Name") { ... }` to group related containers or components.

## Q53: How do you customize the theme in Mermaid?
**A:** Use `%%{init: { "theme": "base", "themeVariables": { "primaryColor": "#ff0000" } } }%%` at the top of the diagram.

## Q54: What built-in themes does Mermaid offer?
**A:** It offers `default`, `base`, `dark`, `forest`, `neutral`, and `ocean` themes.

## Q55: How do you use themeVariables to customize colors?
**A:** Pass an object with keys like `primaryColor`, `secondaryColor`, `tertiaryColor`, `mainBkg`, `nodeBorder`, etc., inside `themeVariables`.

## Q56: How do you configure font size and family globally?
**A:** Set `fontFamily` and `fontSize` in `themeVariables` or within the `themeVariables` block of your init config.

## Q57: What security levels does Mermaid support?
**A:** It supports `strict`, `loose`, `antiscript`, and `sandbox` security levels controlling which HTML/JS features are allowed.

## Q58: What is the `antiXSS` security level?
**A:** The `antiscript` level prevents script execution in rendered diagrams but allows other HTML elements like links and images.

## Q59: What is the `sandbox` security level?
**A:** It renders the diagram in a sandboxed iframe, blocking all script execution and most external resource loading for maximum security.

## Q60: How do you set the security level in Mermaid?
**A:** Call `mermaid.initialize({ securityLevel: "loose" })` or `mermaid.initialize({ securityLevel: "sandbox" })` before rendering.

## Q61: How does Mermaid integrate with Markdown on GitHub?
**A:** GitHub natively renders Mermaid diagrams inside Markdown code blocks with the `mermaid` language tag in issues, PRs, and Markdown files.

## Q62: How do you embed a Mermaid diagram in GitHub Markdown?
**A:** Place the diagram definition inside a fenced code block with `mermaid` as the language identifier, like ` ```mermaid ... ``` `.

## Q63: Does GitLab support Mermaid in Markdown?
**A:** Yes, GitLab renders Mermaid diagrams within Markdown code blocks using the `mermaid` language tag, similar to GitHub.

## Q64: How do you integrate Mermaid with React?
**A:** Use the `mermaid` npm package with `useEffect` to call `mermaid.run()` on a container ref, or use a community wrapper like `react-mermaid`.

## Q65: How do you integrate Mermaid with Vue?
**A:** Use `mermaid` npm package in a Vue component's `mounted` or `onMounted` hook to render diagrams, or use community components like `vue-mermaid`.

## Q66: How do you integrate Mermaid with Angular?
**A:** Import `mermaid` in your Angular component and call `mermaid.run()` after view initialization, handling SSR with `isPlatformBrowser` checks.

## Q67: What is the Mermaid CLI?
**A:** It is a command-line tool (`mmdc`) that converts Mermaid text files into PNG, SVG, or PDF output without a browser.

## Q68: How do you use the Mermaid CLI?
**A:** Run `mmdc -i input.mmd -o output.png` where `input.mmd` contains the diagram definition and `-o` specifies the output file.

## Q69: What formats can mmdc output?
**A:** It can output PNG, SVG, and PDF file formats, controlled by the file extension in the `-o` argument.

## Q70: What is the rendering flow of Mermaid.js?
**A:** It parses text input into an abstract syntax tree, processes it through the layout engine (Dagre for flowcharts, Daydream for sequence), then renders SVG via the renderer.

## Q71: What layout engine does Mermaid use for flowcharts?
**A:** It uses Dagre, a JavaScript library that computes hierarchical graph layouts, to position flowchart nodes and edges automatically.

## Q72: How does Mermaid handle auto layout?
**A:** It uses automatic graph layout algorithms that arrange nodes and edges to minimize crossings and produce readable diagrams without manual positioning.

## Q73: How do you enable accessibility features in Mermaid?
**A:** Mermaid generates SVG elements with accessible titles and descriptions; you can set `accessibilityTitle` in the config or diagram metadata.

## Q74: How do you add custom CSS to Mermaid diagrams?
**A:** Use the `css` configuration option or define CSS classes that target Mermaid SVG elements, such as `.label` or `.node rect`.

## Q75: What is the Mermaid Live Editor?
**A:** It is a web-based tool at `mermaid.live` where you can write diagram definitions, see instant preview, export images, and share diagrams via URL.

## Q76: How do you integrate Mermaid with Docusaurus?
**A:** Docusaurus has built-in Mermaid support via the `@docusaurus/theme-mermaid` plugin; install it and enable `mermaid` in `docusaurus.config.js`.

## Q77: How do you integrate Mermaid with Jekyll?
**A:** Use the `jekyll-mermaid` plugin or include the Mermaid CDN script in your layout and render diagrams with `{% mermaid %}...{% endmermaid %}` tags.

## Q78: What is the Mermaid API?
**A:** It is the JavaScript API exposed by the `mermaid` npm package, with methods like `mermaid.run()`, `mermaid.render()`, `mermaid.initialize()`, and `mermaid.parse()`.

## Q79: How do you use `mermaid.run()`?
**A:** Call `mermaid.run({ nodes: [document.getElementById("diagram")] })` to render all matching DOM elements with `class="mermaid"`.

## Q80: How do you use `mermaid.render()`?
**A:** Call `mermaid.render("uniqueId", "graph TD;A-->B")` which returns an object with the `svg` string for direct insertion into the DOM.

## Q81: How do you handle errors during rendering?
**A:** Use `mermaid.parse(text)` first to validate syntax, then wrap `mermaid.run()` in try-catch blocks, or listen to the `error` event on the renderer.

## Q82: How do you implement lazy loading of Mermaid?
**A:** Dynamically import the `mermaid` package or defer the `<script>` tag, then call `mermaid.initialize()` only when the diagram container enters the viewport.

## Q83: How do you enable zoom and pan in Mermaid?
**A:** Set `config: { flowchart: { htmlLabels: true, useMaxWidth: false } }` and add zoom libraries, or use Mermaid's built-in pan/zoom via SVG viewBox manipulation.

## Q84: Can Mermaid handle large diagrams efficiently?
**A:** Mermaid can handle moderately large diagrams, but very complex graphs may cause performance issues; consider splitting large diagrams or using the CLI for batch rendering.

## Q85: What is the `%%{init}%%` directive?
**A:** It is a configuration block placed at the top of a Mermaid definition that sets theme, themeVariables, and other rendering options inline.

## Q86: How do you define clickable links on nodes?
**A:** Use `click nodeId "https://example.com" "Tooltip"` in flowcharts or `callback` functions to add interactive links to diagram nodes.

## Q87: How do you add tooltips to nodes?
**A:** Use `click nodeId tooltip "Your tooltip text"` after the node definition to show a tooltip on hover.

## Q88: How do you add notes in flowcharts?
**A:** Use `%% Note text` for comments in the source, or attach notes with `N1[Note text]` connected via invisible edges.

## Q89: What is a subgraph in a flowchart?
**A:** A subgraph groups related nodes visually inside a bordered box with an optional title, defined with `subgraph Title ... end`.

## Q90: How do you style subgraphs in a flowchart?
**A:** Apply `style subgraphTitle fill:#color,stroke:#color` or use `classDef` targeting the subgraph's elements.

## Q91: How do you use Mermaid in Architecture Decision Records (ADRs)?
**A:** Include Mermaid code blocks in ADR Markdown files to visually represent architectural decisions, system relationships, and trade-offs.

## Q92: What are common use cases for Mermaid in documentation?
**A:** Documenting APIs, workflows, data models, system architecture, project timelines, decision trees, and process flows in READMEs and wikis.

## Q93: How does Mermaid handle font configuration?
**A:** Set `fontFamily` via `themeVariables` or in the `mermaid.initialize` config; it applies to all text elements in the diagram.

## Q94: How do you change the direction of a flowchart from top-down to left-to-right?
**A:** Replace `graph TD` with `graph LR` to change the layout direction from top-down to left-to-right.

## Q95: How do you add multiple edges between the same nodes?
**A:** Define them sequentially, e.g., `A-->B; A-->B;` or use edge labels to distinguish them like `A-- text1 -->B; A-- text2 -->B;`.

## Q96: How do you render a Mermaid diagram on page load?
**A:** Call `mermaid.initialize()` after the DOM is ready; Mermaid automatically detects elements with `class="mermaid"` and renders them.

## Q97: How do you prevent Mermaid from auto-rendering on load?
**A:** Set `mermaid.initialize({ startOnLoad: false })` and manually call `mermaid.run()` when ready.

## Q98: What is the difference between `mermaid.parse` and `mermaid.parseError`?
**A:** `mermaid.parse(text)` validates syntax and returns true/false; `mermaid.parseError` is a callback invoked when a parse error occurs.

## Q99: How do you create a custom diagram type in Mermaid?
**A:** Define a custom diagram via `mermaid.registerDiagram("customId", CustomDiagram)` implementing the required interfaces, though this is an advanced API feature.

## Q100: What is the Mermaid ecosystem beyond the core library?
**A:** It includes the Live Editor (mermaid.live), Mermaid CLI (mmdc), VS Code extensions, Confluence/Notion plugins, and integrations with Docusaurus, Jekyll, MkDocs, and many documentation platforms.
