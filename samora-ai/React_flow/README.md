# React Flow Interview Questions and Answers

## Q1: What is React Flow?
**A:** React Flow is a customizable React library for building node-based editors, interactive diagrams, and workflow applications. It provides components for rendering nodes, edges, and handles, along with zoom, pan, drag-and-drop, and selection capabilities.

## Q2: What are the core components of React Flow?
**A:** The core components are `<ReactFlow>` (the main canvas wrapper), `<Node>` (custom node components), `<Edge>` (connection lines), and `<Handle>` (connection points on nodes). Built-in node types include `input`, `default`, and `output`.

## Q3: How do you set up a basic React Flow instance?
**A:** ```jsx
import { ReactFlow } from '@xyflow/react';
function Flow() {
  const nodes = [{ id: '1', position: { x: 0, y: 0 }, data: { label: 'Node' } }];
  const edges = [];
  return <ReactFlow nodes={nodes} edges={edges} />;
}
```
Provide `nodes` and `edges` arrays (possibly with state management) and render the `ReactFlow` component.

## Q4: What is the `@xyflow/react` package?
**A:** `@xyflow/react` is the modern React Flow v12+ package. It replaced the older `reactflow` package. It provides improved TypeScript support, better tree-shaking, hooks like `useNodesState` and `useEdgesState`, and the new internal graph engine.

## Q5: What are `useNodesState` and `useEdgesState`?
**A:** Hooks that manage nodes and edges state with built-in change handlers: `const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes)`. `onNodesChange` handles position changes, selection, removal, etc. Similarly `useEdgesState` for edges.

## Q6: How do you handle drag-and-drop from outside React Flow?
**A:** Listen for `onDragOver` and `onDrop` on the React Flow wrapper. In `onDrop`, use `reactFlowInstance.screenToFlowPosition()` to convert screen coordinates to flow coordinates, then add a new node with `setNodes`.

## Q7: How do you add a new node programmatically?
**A:** Use `setNodes(nds => [...nds, { id: nanoid(), type: 'custom', position: { x: 100, y: 100 }, data: { label: 'New' } }])`. Use a unique ID (e.g., `nanoid` or `crypto.randomUUID()`).

## Q8: How do you delete selected nodes and edges?
**A:** Use the `onNodesDelete` and `onEdgesDelete` callbacks, or handle keyboard events (Delete key) by calling `setNodes(nds => nds.filter(n => !n.selected))` and similarly for edges.

## Q9: How do you customize node rendering?
**A:** Create a custom component and register it via the `nodeTypes` prop:
```jsx
const CustomNode = ({ data }) => <div>{data.label}</div>;
const nodeTypes = { custom: CustomNode };
<ReactFlow nodeTypes={nodeTypes} />
```
The `data` prop contains user-defined data passed when creating the node.

## Q10: How do you customize edge rendering?
**A:** Create a custom edge component and register it via the `edgeTypes` prop. Edge components receive `sourceX`, `sourceY`, `targetX`, `targetY`, `sourcePosition`, `targetPosition`, and `style` props.

## Q11: What built-in edge types does React Flow provide?
**A:** Built-in edge types: `default` (straight bezier), `straight` (straight line), `step` (right-angle step), `smoothstep` (rounded step), and `simplebezier`. Custom edge types can be registered.

## Q12: What is an edge marker?
**A:** Edge markers are arrowheads or other SVG markers applied to the end of edges. Configurable via the `markerEnd` and `markerStart` props on edges: `markerEnd={{ type: MarkerType.ArrowClosed }}`.

## Q13: What is the `<Handle>` component?
**A:** `<Handle>` defines connection points on a custom node. It accepts `type` (`source` or `target`), `position` (`Top`, `Bottom`, `Left`, `Right`), and `id` (for multiple handles). Handles are the visual anchors for edges.

## Q14: How do you create a node with multiple handles?
**A:** Add multiple `<Handle>` components in your custom node with different `id`s and `position`s. Set the `id` prop on each handle. Edges reference handles via `sourceHandle` and `targetHandle`.

## Q15: How do you validate connections?
**A:** Use the `isValidConnection` prop on `<ReactFlow>`. It receives a connection object `{ source, target, sourceHandle, targetHandle }` and returns a boolean. Prevent circular connections or enforce type constraints.

## Q16: How do you prevent connections to a specific handle?
**A:** In `isValidConnection`, check the source and target handle IDs/node types. For example, prevent connecting an output handle to another output handle, or restrict connections to compatible node types.

## Q17: How do you enable edge creation by dragging?
**A:** Set `connectOnClick={false}` and use `onConnect` callback. Users can drag from a source handle to a target handle. `onConnect` receives the connection params; add the new edge via `setEdges`.

## Q18: What is an edge `id` and how is it generated?
**A:** Edge `id` uniquely identifies an edge. Typically generated as `${source}-${target}` or `${source}${sourceHandle}-${target}${targetHandle}`. React Flow does not auto-generate it — you set it in `onConnect`.

## Q19: How do you handle edge updates?
**A:** Use `onEdgeUpdate` callback or the `updatable` prop on edges. React Flow supports edge update by allowing users to drag an edge endpoint to a different handle. `updatable` can be `true`, `false`, or `'source'`/`'target'`.

## Q20: How do you implement undo/redo in React Flow?
**A:** Maintain a history stack of nodes and edges states. Push current state before each change. Implement undo by restoring the previous state and redo by restoring forward state. Libraries like `useUndoableReducer` or Zustand middleware can help.

## Q21: How do you use React Flow with a state management library?
**A:** Use Zustand, Redux, or Jotai to manage nodes and edges outside React Flow. Create a store with `applyNodeChanges` and `applyEdgeChanges` helper functions, and pass the store's state and setters to `<ReactFlow>`.

## Q22: What are `applyNodeChanges` and `applyEdgeChanges`?
**A:** Utility functions that compute the next nodes/edges array given the current array and a list of changes (from `onNodesChange` or `onEdgesChange`). They handle position updates, selection, removal, and dimension changes.

## Q23: What is the React Flow viewport?
**A:** The viewport defines the visible area of the canvas: `{ x, y, zoom }`. `x` and `y` are the pan offset. `zoom` is the scale factor. Use `onMoveEnd` or `onMove` to get viewport changes. Use `setViewport()` to programmatically set it.

## Q24: How do you programmatically zoom to fit all nodes?
**A:** Call `reactFlowInstance.fitView()` or `reactFlowInstance.fitView({ padding: 0.2 })`. It calculates the bounding box of all nodes and adjusts the viewport so all nodes are visible.

## Q25: How do you center the view on a specific node?
**A:** Use `reactFlowInstance.setCenter(node.position.x, node.position.y, { zoom: 1.5 })` or `reactFlowInstance.fitView({ nodes: [node] })` to center on a specific node.

## Q26: How do you capture the React Flow instance?
**A:** Use the `onInit` callback: `<ReactFlow onInit={reactFlowInstance => { /* store it */ }} />`. Or use `useReactFlow()` hook inside a child component to access the instance.

## Q27: What is the `useReactFlow` hook?
**A:** `useReactFlow()` provides access to the React Flow instance methods: `getNodes()`, `setNodes()`, `getEdges()`, `setEdges()`, `fitView()`, `setViewport()`, `screenToFlowPosition()`, `flowToScreenPosition()`, etc.

## Q28: How do you convert screen coordinates to flow coordinates?
**A:** Use `reactFlowInstance.screenToFlowPosition({ x: event.clientX, y: event.clientY })`. This accounts for pan, zoom, and the React Flow container offset.

## Q29: How do you implement mini-map?
**A:** Import `<MiniMap>` from React Flow and add it inside `<ReactFlow>`: `<ReactFlow><MiniMap /></ReactFlow>`. The mini-map shows a scaled-down view of the entire graph with node positions.

## Q30: How do you implement controls (zoom in/out)?
**A:** Import `<Controls>` and add it inside `<ReactFlow>`: `<ReactFlow><Controls /></ReactFlow>`. It renders zoom in, zoom out, and fit view buttons.

## Q31: How do you implement a background grid?
**A:** Import `<Background>` and add it inside `<ReactFlow>`: `<ReactFlow><Background variant="dots" gap={16} size={1} /></ReactFlow>`. Variants include `dots`, `lines`, and `cross`.

## Q32: How do you customize the mini-map?
**A:** Use props on `<MiniMap>`: `nodeStrokeColor`, `nodeColor`, `nodeBorderRadius`, `maskColor`, `style`, `className`, `pannable`, `zoomable`, `inversePan`, and `ariaLabel`.

## Q33: How do you handle node selection?
**A:** Nodes can be selected by clicking. Use `onSelectionChange` callback, or read `selected` property from node objects. Use `nodes.selectable` to disable selection per node.

## Q34: How do you handle multi-selection?
**A:** Hold Shift (or Cmd/Ctrl) and click multiple nodes, or drag a selection rectangle (lasso). React Flow handles multi-selection natively. Use `onSelectionChange` to get selected nodes/edges.

## Q35: How do you copy and paste nodes?
**A:** Listen for keyboard events (Ctrl+C/V). On copy, serialize selected nodes (and connected edges) to clipboard as JSON. On paste, deserialize, offset positions, and add via `setNodes`.

## Q36: How do you implement keyboard shortcuts in React Flow?
**A:** Use the `onKeyDown` prop on `<ReactFlow>` or add a global keydown listener. Check for key combinations (Delete, Ctrl+C, Ctrl+V, Ctrl+Z, etc.) and trigger corresponding actions.

## Q37: How do you limit zoom levels?
**A:** Use `minZoom` and `maxZoom` props on `<ReactFlow>`. Default: `minZoom={0.5}`, `maxZoom={2}`.

## Q38: How do you restrict panning?
**A:** Use `panOnDrag` prop (set to `[1, 2]` to require middle mouse button). Use `translateExtent` to restrict the panning area: `translateExtent={[[0, 0], [1000, 1000]]}`.

## Q39: How do you use sub-flows (nested/group nodes)?
**A:** Use `parentId` on a node to make it a child of another node. The parent node must have `type: 'group'`. Children positions are relative to the parent. Moving the parent moves all children.

## Q40: How do you create a group node?
**A:** Add a node with `type: 'group'` and optionally `style: { width, height }`. Child nodes reference the parent via `parentId`. Set `extent: 'parent'` on children to constrain them within the group.

## Q41: How do you auto-layout nodes?
**A:** React Flow does not include auto-layout out of the box. Integrate with `dagre` (for directed graphs), `elkjs` (Eclipse Layout Kernel), or `d3-force` (force-directed) to compute positions and update nodes.

## Q42: How do you integrate dagre for auto-layout?
**A:** Pass nodes and edges to `dagre`'s `layout()` which assigns `x`/`y` positions. Then apply those positions to your nodes. Use `setNodes` after layout. Call layout on initial render and after structural changes.

## Q43: How do you animate node positions?
**A:** Use the `animationOptions` prop on nodes: `{ duration: 300 }`. Or use CSS transitions on the custom node component's container. React Flow supports animated position changes.

## Q44: How do you handle large graphs (performance)?
**A:** Use virtualization (onlyNodesVisible prop), set `nodesDraggable`/`nodesConnectable` globally to false, use `minZoom` to prevent zooming out too far, use `nodeOrigin` for consistent positioning, and keep custom node components light.

## Q45: What is `onlyRenderVisibleElements`?
**A:** A performance optimization prop that only renders nodes and edges within the visible viewport. Non-visible elements are not rendered, reducing DOM nodes. Enable with `<ReactFlow onlyRenderVisibleElements={true}>`.

## Q46: How do you use React Flow in a controlled vs uncontrolled manner?
**A:** Controlled: you manage nodes/edges state externally via `nodes`/`edges` props and `onNodesChange`/`onEdgesChange`. Uncontrolled: you provide initial nodes/edges and let React Flow manage internal state (not recommended for dynamic graphs).

## Q47: What is `defaultNodes` and `defaultEdges`?
**A:** Props for uncontrolled React Flow usage. Provide initial nodes/edges. Changes are handled internally. Use `onNodesChange` to be notified of changes if needed.

## Q48: How do you customize connection lines?
**A:** Use the `connectionLineComponent` or `connectionLineStyle` props on `<ReactFlow>`. Create a custom connection line component that renders during edge creation from an SVG path.

## Q49: How do you style edges globally?
**A:** Use `defaultEdgeOptions` prop: `<ReactFlow defaultEdgeOptions={{ style: { stroke: '#b1b1b7', strokeWidth: 2 }, type: 'smoothstep' }} />`. These apply to all new edges.

## Q50: How do you style nodes globally?
**A:** Use `defaultNodeOptions` prop: `<ReactFlow defaultNodeOptions={{ style: { background: '#fff', border: '1px solid #ddd' } }} />`. Or set defaults in the node data schema.

## Q51: What is an interactive node?
**A:** An interactive node contains interactive elements (inputs, buttons, selects) that should not trigger React Flow gestures (pan, select, drag). Use `noDragClassName` and `noPanClassName` on these elements.

## Q52: What are `noDragClassName` and `noPanClassName`?
**A:** CSS class names that prevent React Flow from intercepting pointer events on child elements. Add `noDragClassName` to inputs/buttons inside a custom node to allow normal interaction without dragging the node.

## Q53: How do you handle touch devices?
**A:** React Flow supports touch events natively. Use `panOnDrag` with `touch` considerations. Set `nodesDraggable` and `nodesConnectable` appropriately for touch UIs. Use larger handle sizes.

## Q54: How do you export the flow as an image?
**A:** Access the React Flow wrapper DOM element, use `html-to-image` library (`toPng`, `toJpeg`, `toSvg`), and call the export function. React Flow's `getViewport()` helps determine the viewport state to include.

## Q55: How do you serialize/deserialize the flow state?
**A:** Store nodes and edges as JSON (they are plain objects). Serialize: `JSON.stringify({ nodes, edges })`. Deserialize: `const { nodes, edges } = JSON.parse(json)` and restore via `setNodes`/`setEdges`.

## Q56: How do you handle edge labels?
**A:** Use the `label` prop on edges, or create a custom edge with a label component. React Flow supports edge labels with `edgeLabelBgStyle` and `labelStyle` props for styling.

## Q57: How do you create a custom edge with a label?
**A:** Register a custom edge component that renders SVG text or HTML foreignObject. Use `sourceX`, `sourceY`, `targetX`, `targetY` to calculate the label's midpoint position.

## Q58: How do you update node data dynamically?
**A:** Use `setNodes(nds => nds.map(n => n.id === nodeId ? { ...n, data: { ...n.data, label: newLabel } } : n))`. This triggers React Flow to re-render the node with new data.

## Q59: How do you programmatically add an edge?
**A:** Call `setEdges(eds => [...eds, { id: `e-${source}-${target}`, source, target, sourceHandle, targetHandle }])`. Typically done in the `onConnect` callback.

## Q60: How do you connect nodes programmatically (without user interaction)?
**A:** Same as adding edges: use `setEdges` to add a connection `{ id, source, target, sourceHandle, targetHandle }`. Ensure both nodes exist before connecting.

## Q61: What happens when a node is deleted with connected edges?
**A:** React Flow does not automatically delete connected edges. In `onNodesDelete`, iterate over deleted node IDs and filter out edges that reference them: `setEdges(eds => eds.filter(e => !deletedNodeIds.includes(e.source) && !deletedNodeIds.includes(e.target)))`.

## Q62: How do you prevent a specific node from being deleted?
**A:** Check the node's ID or type in `onNodesDelete` and conditionally prevent deletion. Alternatively, set `deletable: false` on the node object.

## Q63: How do you implement a snap-to-grid?
**A:** Use the `snapToGrid` prop and `snapGrid` prop: `<ReactFlow snapToGrid snapGrid={[20, 20]} />`. Nodes will snap to the nearest grid intersection when dragged.

## Q64: How do you handle node resizing?
**A:** React Flow does not have built-in node resizing. Use the `reactflow-resizable` package or implement custom resize handles within your custom node component.

## Q65: How do you add a context menu to React Flow?
**A:** Use `onNodeContextMenu`, `onEdgeContextMenu`, and `onPaneContextMenu` callbacks. Show a custom context menu component at the mouse position (prevent default browser menu with `e.preventDefault()`).

## Q66: How do you implement a minimap with a custom node?
**A:** Pass the custom node type to `<MiniMap nodeColor={node => node.data.color}>` or use `nodeComponent` prop on `<MiniMap>` to fully customize the mini-map node rendering.

## Q67: How do you handle scroll behavior inside React Flow?
**A:** Use `zoomOnScroll` (default true), `panOnScroll` (default false), and `panOnScrollSpeed`. Set `zoomOnScroll={false}` to disable zoom on scroll (useful when React Flow is inside a scrollable container).

## Q68: How do you use React Flow inside a scrollable page?
**A:** Set `panOnDrag={false}` or `panOnDrag={[1, 2]}` (require middle mouse button). Set `zoomOnScroll={false}`. The page scrolls normally, and users use middle-click or controls to navigate the flow.

## Q69: What is the `elevateEdgesOnSelect` prop?
**A:** When true, edges connected to a selected node are visually elevated (rendered above other edges). Improves visibility of connections for selected nodes.

## Q70: How do you create a branching workflow with React Flow?
**A:** Use nodes with multiple source handles (each representing an output path). Custom edges can represent different conditions. Use `sourceHandle` to track which output branch an edge originates from.

## Q71: How do you validate a workflow before execution?
**A:** Traverse the graph using topological sort. Check for cycles (React Flow's `isValidConnection` can prevent cycle creation). Validate required connections, data types, and that all required fields are set.

## Q72: How do you detect cycles in the graph?
**A:** In `isValidConnection`, check if the proposed connection would create a cycle by traversing from target to all descendants. If source is found in descendants, reject the connection. Use DFS/BFS traversal.

## Q73: How do you highlight connected nodes on hover?
**A:** Use `onNodeMouseEnter`/`onNodeMouseLeave` to track hovered node. Compute connected node IDs. Apply highlight CSS classes to connected nodes and edges. React Flow's `getConnectedEdges` and `getOutgoers`/`getIncomers` helpers are useful.

## Q74: What are `getOutgoers` and `getIncomers`?
**A:** Utility functions from React Flow. `getOutgoers(node, nodes, edges)` returns nodes that are targets of edges from the given node. `getIncomers(node, nodes, edges)` returns source nodes. Useful for graph traversal.

## Q75: How do you implement a node palette (toolbox)?
**A:** Create a sidebar with draggable items. On `onDragStart`, set `event.dataTransfer.setData('application/reactflow', nodeType)`. In the flow's `onDrop`, create the node based on the dragged type.

## Q76: How do you use React Flow with TypeScript?
**A:** Define typed node and edge data: `type NodeData = { label: string; value: number }`. Use `Node<NodeData>` and `Edge<NodeData>` types. The `@xyflow/react` package provides full TypeScript support.

## Q77: How do you create a node with dynamic inputs?
**A:** In the custom node component, render form elements (input, select) using the `data` prop for values. Update data via `useReactFlow().setNodes()` or pass a callback through `data`.

## Q78: How do you handle asynchronous node updates?
**A:** Use React state or a state management library. After async operations (API calls, computations), call `setNodes` with the updated data. Show loading state within the custom node component.

## Q79: How do you implement auto-save of a flow?
**A:** Debounce `onNodesChange` and `onEdgesChange` callbacks, serialize nodes/edges to JSON, and save to localStorage or send to an API. Restore on load from saved state.

## Q80: How do you add a toolbar to a node on selection?
**A:** In the custom node component, check `selected` prop (passed by React Flow). Render a floating toolbar with actions (delete, duplicate, configure) when `selected` is true.

## Q81: How do you highlight edges on hover?
**A:** Edge components receive `selected` and `animated` props. Use `onEdgeMouseEnter`/`onEdgeMouseLeave` callbacks on `<ReactFlow>` to set a highlighted edge ID in state, then pass highlighted style.

## Q82: How do you animate an edge?
**A:** Set `animated: true` on the edge object. React Flow applies a CSS animation that moves stroke-dasharray along the path, creating a flowing connection effect.

## Q83: How do you use edge markers with custom paths?
**A:** Set `markerEnd` on the edge config. For custom markers, define `<defs><marker id="custom" ...></defs>` in your SVG and reference it: `markerEnd: 'url(#custom)'`.

## Q84: How do you handle drop events on a specific node?
**A:** In the custom node component, use standard `onDrop` with `onDragOver` handlers. Check `event.dataTransfer.types` to identify drop data. Update node data on drop.

## Q85: How do you implement a resizable panel split with React Flow?
**A:** Use a split pane library (react-resizable-panels, allotment) on the side. React Flow occupies one pane. Resize events may require calling `fitView()` on the React Flow instance.

## Q86: How do you use React Flow with Next.js?
**A:** React Flow requires the browser. Import it dynamically with `next/dynamic`: `const ReactFlow = dynamic(() => import('@xyflow/react'), { ssr: false })`. Wrap with `ReactFlowProvider` for hooks.

## Q87: What is `ReactFlowProvider`?
**A:** A context provider that makes the React Flow instance available via `useReactFlow()` to components outside the `<ReactFlow>` component tree. Wrap your app or page with it.

## Q88: How do you use React Flow hooks outside the `<ReactFlow>` component?
**A:** Wrap the component tree with `<ReactFlowProvider>`. Any descendant can use `useReactFlow()`, `useNodesState()`, `useEdgesState()`, and other hooks even outside `<ReactFlow>`.

## Q89: How do you add a watermark or overlay to the flow?
**A:** Position a div absolutely over the ReactFlow component with `pointer-events: none` for overlays. For watermarks, render an SVG element within the flow area.

## Q90: How do you implement dark mode in React Flow?
**A:** Use CSS variables or inline styles. React Flow's built-in components accept `style` and `className` props. Set dark theme via `<ReactFlow>` container's `className` and override `.react-flow__node`, `.react-flow__edge`, etc.

## Q91: How do you test React Flow components?
**A:** Use React Testing Library or Vitest. Mock the React Flow instance if needed. For integration tests, render `<ReactFlow>` with test nodes/edges. Use `data-testid` on custom nodes.

## Q92: How do you change the default connection line style?
**A:** Set `connectionLineStyle` prop on `<ReactFlow>`: `connectionLineStyle={{ stroke: '#000', strokeWidth: 2, strokeDasharray: '5 5' }}`. Or create a custom connection line component.

## Q93: How do you disable connections on a specific node?
**A:** Set `connectable: false` on the node object. This hides the source handle's connection ability. For individual handles, set `isConnectable={false}` on the `<Handle>` component.

## Q94: How do you prevent specific nodes from being dragged?
**A:** Set `draggable: false` on the node object. Or use `nodesDraggable={false}` on `<ReactFlow>` to disable all dragging.

## Q95: How do you implement a search/filter for nodes?
**A:** Filter nodes based on search input. Use `setNodes` to update which nodes are visible (set `hidden: true/false`). Or filter the nodes array before passing to React Flow.

## Q96: How do you handle node z-ordering?
**A:** Nodes are rendered in the order of the nodes array (later = on top). Use `onNodeDragStart`/`onNodeDragStop` to move dragged nodes to the end of the array. React Flow automatically handles z-ordering within the SVG.

## Q97: How do you create a node with an image or icon?
**A:** In the custom node component, render an `<img>` tag or an icon component in the render output. Pass the image URL or icon name via `data` prop.

## Q98: How do you integrate React Flow with a form?
**A:** Render form elements inside custom node components. Sync form changes to node `data` using callbacks. For a properties panel, use `onNodeClick` to select a node and show its data in a side panel.

## Q99: How do you implement a collapsible/expandable group?
**A:** Use a group node. Toggle its `style.height`/`style.width` and child nodes' visibility. Animate using CSS transitions or React Flow's `animationOptions`. Set child nodes' `hidden` property when collapsed.

## Q100: What are the alternatives to React Flow?
**A:** Alternatives include: xyflow (React Flow's pendant for Svelte), Cytoscape.js (graph visualization), D3.js (lower-level, more flexible), Joint.js (diagramming), GoJS (commercial, feature-rich), and Mermaid (text-to-diagram, not interactive).
