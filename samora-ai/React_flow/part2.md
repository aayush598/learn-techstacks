# React Flow Interview Questions and Answers - Part 2

## Q1: How do you implement custom node types with React Flow?
**A:** Define custom node components and register them via the `nodeTypes` prop on `<ReactFlow>`. Each custom node receives `{ id, data, selected, type, dragging, position }` as props. Example: `const nodeTypes = useMemo(() => ({ custom: CustomNode }), []); <ReactFlow nodeTypes={nodeTypes}>`. Custom nodes can have their own state, handlers, and rendering. Always memoize `nodeTypes` to prevent unnecessary re-renders.

## Q2: How do you implement custom edge types with custom rendering?
**A:** Create a custom edge component that renders SVG paths using the `getBezierPath`, `getSmoothStepPath`, or `getStraightPath` utilities from `@reactflow/core`. Register via `edgeTypes` prop. Custom edges receive `{ id, source, target, sourceX, sourceY, targetX, targetY, selected }`. Example: `const CustomEdge = ({ id, sourceX, sourceY, targetX, targetY }) => { const [edgePath] = getBezierPath({ sourceX, sourceY, targetX, targetY }); return <path id={id} d={edgePath} />; }`. Memoize edgeTypes.

## Q3: How do you implement edge markers (arrows) with custom styling?
**A:** Use the `markerEnd` and `markerStart` props on edges. Define markers via SVG defs: `const CustomMarker = ({ id }) => <marker id={id} markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#b1b1b7" /></marker>`. Apply: `edge={{ markerEnd: { type: MarkerType.ArrowClosed, color: '#ff0000', width: 20, height: 20 } }}`. Custom markers can be different shapes (circle, diamond, custom paths).

## Q4: How do you implement edge labels with interactive features?
**A:** Use the `label` prop or render a custom label via `edge.label` or a custom edge component. For interactive labels: `<EdgeLabelRenderer>{selected && <div style={{ position: 'absolute', transform: `translate(-50%, -100%) translate(${labelX}px,${labelY}px)` }}><input /></div>}</EdgeLabelRenderer>`. The `EdgeLabelRenderer` portal renders labels above the SVG layer. Use `getEdgeCenter` to position labels at edge midpoint.

## Q5: How do you customize the minimap component?
**A:** `<MiniMap nodeStrokeColor={(node) => node.data.color} nodeColor={(node) => node.data.bg} nodeBorderRadius={2} maskColor="rgba(0,0,0,0.1)" style={{ width: 150, height: 100 }} />`. Customize with `nodeStrokeColor`, `nodeColor`, `nodeClassName`, `maskColor`, `style`. For pannable minimap: `pannable={true}` and `zoomable={true}`. The minimap can show a node count badge or highlight selected nodes.

## Q6: How do you customize the Controls component?
**A:** `<Controls showInteractive={false} showFitView={false} showZoom={false} position="top-right" style={{ background: '#fff', borderRadius: 8 }} />`. You can add custom buttons: `<Controls><ControlButton onClick={handleSave}>💾</ControlButton></Controls>`. Customize with `position`, `style`, `className`. Override individual control visibility with `showZoom`, `showFitView`, `showInteractive`.

## Q7: How do you implement node resizing?
**A:** Install `@reactflow/node-resizer`. Wrap your custom node: `<NodeResizer minWidth={50} minHeight={50} isVisible={selected} handleStyle={{ width: 8, height: 8 }} lineStyle={{ border: '1px solid #1a192b' }} />`. The `<NodeResizer>` component adds resize handles to corners and edges. For aspect ratio lock: `<NodeResizer keepAspectRatio />`. For color picker integration: resize updates `node.style.width/height`.

## Q8: How do you implement node grouping with React Flow?
**A:** Use parent-child nodes. A parent node wraps child nodes. Set `parentId` on child nodes to the parent's id. The parent node type should be `group`. Enable `extent: 'parent'` on children to keep them within the parent. `nodeExtent` constrains movement. For expand/collapse: animate the parent's dimensions and child visibility. Use `getNodesBounds` to calculate parent size from children.

## Q9: How do you implement sub-flows (nested flow diagrams)?
**A:** Use parent nodes as containers. Each parent node renders a mini `<ReactFlow>` inside. Pass `proOptions={{ hideAttribution: true }}`. The inner flow uses its own nodes, edges, and viewport. Handle drag events to pass coordinates between outer and inner flows. For communication: use a shared store for cross-flow events. Sub-flows can be collapsed/expanded showing a preview of inner nodes.

## Q10: How do you implement dagre tree layout algorithms?
**A:** Use the `dagre` library: `import dagre from 'dagre'`. Create a layout function: `const getLayoutedElements = (nodes, edges) => { const g = new dagre.graphlib.Graph(); g.setDefaultEdgeLabel(() => ({})); g.setGraph({ rankdir: 'LR', nodesep: 50, ranksep: 100 }); nodes.forEach(n => g.setNode(n.id, { width: n.width || 150, height: n.height || 40 })); edges.forEach(e => g.setEdge(e.source, e.target)); dagre.layout(g); return { nodes: nodes.map(n => { const pos = g.node(n.id); return { ...n, position: { x: pos.x - (n.width || 150) / 2, y: pos.y - (n.height || 40) / 2 } }; }), edges }; }`. Call on initial render and on "Layout" button click.

## Q11: How do you implement node/edge selection with multi-select?
**A:** Enable `multiSelectionKeyCode="Shift"` for shift-click multi-select. Use `onSelectionChange` handler. Check `selected` prop on nodes/edges. For programmatic selection: `setNodes(nodes.map(n => ({ ...n, selected: n.id === targetId })))`. For selection box: `selectionOnDrag={true}` or `panOnDrag={[1, 2]}` (middle/right button). Custom selection box via `selectionMode={SelectionMode.Partial}`.

## Q12: How do you implement custom connection validation?
**A:** Use the `isValidConnection` prop on `<ReactFlow>`: `isValidConnection={(connection) => { const sourceNode = nodes.find(n => n.id === connection.source); return sourceNode?.type !== 'output' && connection.sourceHandle !== connection.targetHandle; }}`. For type-based validation: check handle types match. For circular prevention: traverse the graph to detect cycles. For port limits: count existing connections per node/handle.

## Q13: How do you implement custom connection lines?
**A:** Use the `connectionLineComponent` prop: `<ReactFlow connectionLineComponent={CustomConnectionLine} />`. The custom component receives `{ fromX, fromY, toX, toY, connectionStatus }`. Render your own SVG path: `<path d={getBezierPath(...)} stroke={connectionStatus === 'valid' ? 'green' : 'red'} strokeWidth={2} />`. For animated connection: use dashed stroke with CSS animation.

## Q14: How do you optimize performance with large graphs (1000+ nodes)?
**A:** Strategies: 1) Use `onlyRenderVisibleElements={true}` to skip off-screen nodes. 2) Set `nodeTypes` and `edgeTypes` outside component with `useMemo`. 3) Use `efficiency: { nodes: { threshold: 500 }, edges: { threshold: 500 } }`. 4) Disable animations: `animate={false}`. 5) Use React.memo on custom nodes. 6) Minimize re-renders with `useUpdateNodeInternals`. 7) Use `defaultEdgeOptions` instead of per-edge props.

## Q15: How do you integrate React Flow with Redux or Zustand for state management?
**A:** Use the `onNodesChange`, `onEdgesChange`, and `onConnect` callbacks to dispatch actions. With Zustand: `const store = create((set) => ({ nodes: [], edges: [], onNodesChange: (changes) => set(state => ({ nodes: applyNodeChanges(changes, state.nodes) })) }))`. In component: `const { nodes, edges, onNodesChange } = useStore()`. With Redux: dispatch `applyNodeChanges` to reducer. Use `useStoreApi` for imperative store access.

## Q16: How do you implement undo/redo functionality?
**A:** Store history of node/edge states: `const [history, setHistory] = useState([{ nodes: initialNodes, edges: initialEdges }]); const [historyIndex, setHistoryIndex] = useState(0);`. On each change (debounced), push new state: `setHistory(prev => [...prev.slice(0, historyIndex + 1), { nodes, edges }]); setHistoryIndex(prev => prev + 1)`. Undo: `setHistoryIndex(prev => Math.max(0, prev - 1))`. Apply: `setNodes(history[historyIndex].nodes)`. Limit history size.

## Q17: How do you implement keyboard shortcuts for the flow editor?
**A:** Use the `onKeyDown` prop or a global key handler. Check `nodes.filter(n => n.selected)` for Delete: `if (e.key === 'Delete') { setNodes(nodes => nodes.filter(n => !n.selected)); setEdges(edges => edges.filter(e => !e.selected)); }`. For copy/paste: store selected nodes in clipboard. For Ctrl+A: select all. For Ctrl+Z: undo. For Ctrl+D: duplicate selected nodes with offset position.

## Q18: How do you implement viewport transformations programmatically?
**A:** Use `setViewport({ x: 100, y: 200, zoom: 1.5 })` or `fitView({ padding: 0.2, duration: 300 })`. For smooth transitions: `fitView({ duration: 500 })`. For centering specific nodes: `setNodes(nodes => nodes.map(n => ({ ...n, selected: false }))); setCenter(node.position.x, node.position.y, { zoom: 1.5 })`. Use `viewportRef` for imperative control. Get current viewport: `const viewport = reactFlowInstance.getViewport()`.

## Q19: How do you implement node/edge deletion patterns?
**A:** Built-in: set `deleteKeyCode="Delete"` or `deleteKeyCode={['Delete', 'Backspace']}`. For custom behavior: handle deletions in `onNodesChange`/`onEdgesChange` with `remove` type. For cascade deletion: remove connected edges when node is deleted. `onNodesDelete` fires when nodes are removed. `onEdgesDelete` for edges. Use `useNodesData` or `useNodeConnections` for connected edge detection.

## Q20: How do you implement animated edges (dashed, gradient, flow)?
**A:** For animated: set `animated={true}` on edge config. CSS animation: `@keyframes dash { to { stroke-dashoffset: -20; } }`. Custom animated edge with gradient: `<linearGradient id={id}><stop offset="0%" stopColor="#ff0000" /><stop offset="100%" stopColor="#0000ff" /></linearGradient>`. Apply gradient via stroke. For data flow animation: `animated={true}` with CSS class. Multiple animated edges can show direction of data flow.

## Q21: How do you implement handles positioning with custom connections?
**A:** `<Handle type="source" position={Position.Right} id="a" style={{ top: 10 }} />` positions a handle 10px from top. For dynamic positioning: compute handle positions based on node data. Use `isConnectable={false}` to disable specific handles. For hidden handles: `style={{ visibility: 'hidden' }}` show only on hover. Connect multiple handles: different `id` per handle. `type="source"` for outgoing, `type="target"` for incoming.

## Q22: How do you implement node drag and drop from a sidebar?
**A:** On drag start from sidebar: `const onDragStart = (event, nodeType) => { event.dataTransfer.setData('application/reactflow', nodeType); event.dataTransfer.effectAllowed = 'move'; }`. On drop on ReactFlow: `const onDrop = useCallback((event) => { const type = event.dataTransfer.getData('application/reactflow'); const position = reactFlowInstance.screenToFlowPosition({ x: event.clientX, y: event.clientY }); const newNode = { id: uuid(), type, position, data: { label: type } }; setNodes(nds => nds.concat(newNode)); }, [reactFlowInstance])`. Set `onDrop` and `onDragOver` on `<ReactFlow>`.

## Q23: How do you implement zoom controls with constraints?
**A:** Set zoom limits: `<ReactFlow minZoom={0.1} maxZoom={4} defaultZoom={1.5} />`. For smooth zoom: `zoomOnScroll={true}` and `zoomOnDoubleClick={true}`. For pinch zoom on mobile: `panOnDrag={[1, 2]}`. Programmatic zoom: `setViewport({ x, y, zoom: 2 })`. Zoom to fit: `fitView()`. For scroll-to-zoom sensitivity: override with CSS. For zoom percentage display: `const { zoom } = useReactFlow().getViewport()`.

## Q24: How do you implement React Flow with TypeScript for type-safe nodes and edges?
**A:** Define custom types: `type CustomNodeData = { label: string; value?: number }; type CustomNode = Node<CustomNodeData, 'custom'>; type CustomEdge = Edge<{ animated?: boolean }>;`. Use generics: `const [nodes, setNodes] = useState<CustomNode[]>([])`. In custom node: `const data = useNodeData<CustomNodeData>(nodeId)`. For edges: `Edge<{ customProp: string }>`. `NodeProps<CustomNodeData>` for node props typing.

## Q25: How do you implement dark mode with React Flow?
**A:** Apply CSS classes to `<ReactFlow>` wrapper: `bgColor`, `nodeColor`, `edgeColor`. CSS variables: `.react-flow__node { background: #333; color: #fff; } .react-flow__edge-path { stroke: #666; } .react-flow__background { background: #1a1a1a; }`. Use `BackgroundVariant.Lines` with dark colors. Toggle via context: `const { isDark } = useTheme(); <div className={isDark ? 'dark' : 'light'}><ReactFlow ... /></div>`.

## Q26: How do you implement edge updater (interactive edge editing)?
**A:** Use `updatable={true}` on edge or globally: `defaultEdgeOptions={{ updatable: true }}`. Or `edgeUpdaterType="button"` for button-based edge updates. Users click an edge to start editing. Use `onEdgeUpdate` callback to handle the update. For custom update behavior: `onEdgeUpdate={(oldEdge, newConnection) => { setEdges(els => updateEdge(oldEdge, newConnection, els)) }}`. The edge splitting creates two edges with a new node.

## Q27: How do you implement a background grid pattern?
**A:** `<Background variant={BackgroundVariant.Dots} gap={12} size={1} color="#ddd" />`. Variants: `Lines`, `Dots`, `Cross`. Customize: `<Background variant="custom" gap={20} size={2} color="#ccc" style={{ background: '#f8f8f8' }} />`. For performance with large graphs: reduce gap size or use dots. Animated background: `@keyframes move { from { transform: translateX(0); } to { transform: translateX(50px); } }` with CSS.

## Q28: How do you implement auto-layout on node addition?
**A:** Use dagre layout triggered on each node/edge change. Debounce the layout calculation. After adding a node, call `getLayoutedElements(nodes, edges)`. For incremental: add the new node at a computed position near its source/target. Use `getNodePosition` to find available space. For constraint-based layout: assign rank/order in node data. Use `layoutAnimation: true` in React Flow v11 for smooth position transitions.

## Q29: How do you implement node tooltips and context menus?
**A:** Custom node renders tooltip on hover: `const [showTooltip, setShowTooltip] = useState(false); <div onMouseEnter={() => setShowTooltip(true)} onMouseLeave={() => setShowTooltip(false)}>{showTooltip && <div className="tooltip">{data.tooltip}</div>}</div>`. For context menu: `onNodeContextMenu={(event, node) => { event.preventDefault(); setContextMenu({ node, x: event.clientX, y: event.clientY }); }}`. Render a positioned `<div>` as context menu.

## Q30: How do you implement pan and zoom with touch gestures on mobile?
**A:** React Flow handles touch by default. Configure: `panOnDrag={true}`, `panOnScroll={true}`, `zoomOnScroll={true}`, `zoomOnPinch={true}`, `zoomOnDoubleClick={true}`. For two-finger pan: `panOnDrag={[2]}` (middle mouse button). Disable touch actions on flow: `style={{ touchAction: 'none' }}`. For scrollable container inside flow: `preventScrolling={false}`.

## Q31: How do you implement a minimap with node preview thumbnails?
**A:** `<MiniMap nodeComponent={CustomMiniMapNode} />`. Custom node component renders a scaled-down preview: `const CustomMiniMapNode = ({ id, data }) => <div style={{ background: data.color, width: '100%', height: '100%' }} />`. For labeled: show first few characters of label. For group nodes: show all children as smaller dots. Use `nodeStrokeWidth={0}` for clean minimap. `maskColor` for viewport indicator.

## Q32: How do you implement pathfinding edges with avoidance?
**A:** Custom edge component that uses pathfinding. Calculate path avoiding node bounding boxes: `const getSmartEdge = ({ sourceX, sourceY, targetX, targetY, nodes }) => { const nodeRects = nodes.map(n => ({ id: n.id, rect: getNodeRect(n) })); // compute path avoiding obstacles };`. Use `getSmoothStepPath` with `borderRadius` for simple orthogonal routing. For complex pathfinding, integrate with pathfinding libraries or use `@reactflow/smart-edge`.

## Q33: How do you implement a floating/portal node that stays in viewport?
**A:** Use a special node type, like a minimap-like node. This is not natively supported but can be achieved by: 1) Using React portal to render outside the flow. 2) Listening to `onMoveStart`/`onMove` updates. 3) Using `useViewport` hook to get current zoom/pan. 4) Applying inverse transform to keep position: `const { x, y, zoom } = useViewport(); style={{ transform: `translate(${-x}px, ${-y}px) scale(${1/zoom})` }}`. This creates a floating node that stays fixed.

## Q34: How do you implement edge reconnection?
**A:** Enable `reconnect` in `defaultEdgeOptions`: `defaultEdgeOptions={{ reconnectable: true }}`. Use `onReconnectStart`, `onReconnectEnd`, and `onReconnect` callbacks: `<ReactFlow onReconnect={(oldEdge, newConnection) => { setEdges(els => updateEdge(oldEdge, newConnection, els)); }} />`. For validation during reconnect: `isValidConnection`. For visual feedback: change edge color during reconnect.

## Q35: How do you implement a search/filter functionality for nodes?
**A:** Filter nodes based on search: `const filteredNodes = nodes.filter(n => n.data.label.toLowerCase().includes(searchTerm)); setNodes(filteredNodes)`. For highlighting: set `style={{ opacity: match ? 1 : 0.3 }}` on non-matching nodes. For scroll-to-node: `setCenter(node.position.x, node.position.y, { zoom: 1.5 })`. Highlight edges connected to found nodes. Use `useUpdateNodeInternals` after filter changes.

## Q36: How do you implement custom edges with along-path labels and icons?
**A:** Custom edge renders SVG text along path: `<text><textPath href={`#${id}`} startOffset="50%" textAnchor="middle">{data.label}</textPath></text>`. For icons: use SVG `<image>` or foreignObject: `<foreignObject width={20} height={20} x={labelX - 10} y={labelY - 10}><div>icon</div></foreignObject>`. Use `getEdgeCenter` or `getPointAtLength` for positioning. For multiple labels: place at 25%, 50%, 75% along path.

## Q37: How do you implement a snap-to-grid with dynamic grid sizing?
**A:** Enable via `<ReactFlow snapToGrid={true} snapGrid={[20, 20]} />`. For dynamic grid: zoom-dependent grid size. In zoom handler: `const zoom = reactFlowInstance.getViewport().zoom; const grid = zoom > 1 ? 10 : zoom > 0.5 ? 20 : 50`. Update `snapGrid` prop. CSS grid overlay: `<Background gap={snapGrid[0]} variant={BackgroundVariant.Lines} />`. For node resize snap: combine with `NodeResizer`.

## Q38: How do you implement an export/import flow diagram as JSON?
**A:** Export: `const flow = reactFlowInstance.toObject(); const json = JSON.stringify(flow); download(json, 'flow.json')`. The toObject method returns `{ nodes, edges, viewport }`. Import: `const flow = JSON.parse(fileContent); const { nodes, edges, viewport } = flow; reactFlowInstance.setNodes(nodes); reactFlowInstance.setEdges(edges); reactFlowInstance.setViewport(viewport)`. For backward compatibility: validate imported data structure.

## Q39: How do you implement node animations (entrance, exit, position changes)?
**A:** React Flow v11 supports layout animations: `<ReactFlow layoutAnimation={true} />`. For custom animations: wrap node content in `<motion.div>`: `<motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} exit={{ scale: 0 }}>`. For position animation: `useUpdateNodeInternals` triggers layout recalc. For edge connection animation: `animated={true}`. For spring physics on position: `transition={{ type: 'spring', stiffness: 300, damping: 30 }}`.

## Q40: How do you implement a custom connection handle with validation feedback?
**A:** Custom handle: `<Handle type="source" position={Position.Right} id="a" style={{ background: isValidConnection ? '#55dd99' : '#ff4444' }}>`. Use `useConnection` hook: `const connection = useConnection(); const isValid = connection?.target === 'valid'.` For port color coding: change handle color based on node type. For animated handle: `<motion.div animate={{ scale: isConnecting ? 1.2 : 1 }}>`.

## Q41: How do you implement multi-touch gestures for zoom and rotate?
**A:** React Flow handles pinch-zoom natively. For rotate: use CSS transform on the flow wrapper. Track rotation angle in state. `onMove={(_event, viewport) => { rotateRef.current = viewport.rotation }}`. Apply rotation: `<div style={{ transform: `rotate(${rotation}deg)` }}><ReactFlow /></div>`. For pan inertia: `panOnDrag={true}` with momentum. For two-finger rotate: compute angle from touch points.

## Q42: How do you implement auto-connect nodes with matchmaker?
**A:** Use the `onConnect` handler to determine connect behavior. For auto-connect: `onConnect={(connection) => { const sourceNode = nodes.find(n => n.id === connection.source); const targetNode = createNode('default', { position: getNextPosition() }); setNodes(nds => nds.concat(targetNode)); setEdges(eds => eds.concat({ ...connection, target: targetNode.id })) }}`. For matchmaker: suggest available connection points based on node data compatibility.

## Q43: How do you implement nested node editing with inline forms?
**A:** Custom node renders an editable form: `const [editing, setEditing] = useState(false); return <div onDoubleClick={() => setEditing(true)}>{editing ? <input autoFocus onBlur={() => setEditing(false)} onChange={(e) => updateNodeData(id, { label: e.target.value })} value={data.label} /> : <div>{data.label}</div>}</div>`. For multi-field: render inputs for each data property. Use `updateNodeData` from `useReactFlow`.

## Q44: How do you implement a canvas minimap with viewport indicator?
**A:** `<MiniMap pannable zoomable nodeStrokeWidth={3} nodeBorderRadius={10} maskColor="rgba(0,0,0,0.1)" style={{ width: 200, height: 150 }} />`. The viewport indicator is a rectangle showing current visible area. Customize indicator: `maskColor="rgba(0,0,0,0.1)"`. For click-to-pan: `<MiniMap pannable={true}>`. For custom indicator styling: wrap in `<MiniMap>` with CSS overrides on `.react-flow__minimap-mask`.

## Q45: How do you implement edge animations with dynamic data flow visualization?
**A:** `animated={true}` for basic flow. For dynamic: control animation speed with CSS. Edge receives updates via data: `edge.data = { flowRate: 0.5 }`. Custom edge renders animated dash array: `<path d={edgePath} stroke="url(#gradient)" strokeDasharray={5} className="animated-path" style={{ animationDuration: `${1 / data.flowRate}s` }}>`. CSS: `@keyframes dash { to { stroke-dashoffset: -20; } }`.

## Q46: How do you implement a node palette/drawer with drag-to-add?
**A:** Sidebar component with draggable items. Each item: `<div draggable onDragStart={(e) => e.dataTransfer.setData('application/reactflow', 'custom')}>`. Drop zone: `<div onDragOver={(e) => e.preventDefault()} onDrop={handleDrop}>`. The handleDrop uses `reactFlowInstance.screenToFlowPosition` to place at cursor. For category groups: render sections by node type category.

## Q47: How do you implement a zoom-to-fit button with custom animation?
**A:** `const { fitView } = useReactFlow(); <button onClick={() => fitView({ padding: 0.2, duration: 500, maxZoom: 2 })}>Fit</button>`. For custom animation: use `fitView` with `duration` for smooth transition. For fit to selected: `fitView({ nodes: [selectedNode], duration: 300 })`. For progressive zoom: `const animateZoom = async () => { await setViewport({ ...current, zoom: 1 }, { duration: 200 }); await fitView({ duration: 300 }); }`.

## Q48: How do you implement sticky notes/comment nodes?
**A:** Create a `comment` node type with no handles: `<Handle type="target" position={Position.Top} style={{ visibility: 'hidden' }} />`. Style: `background: rgba(255, 229, 100, 0.3); border: none; width: 200px; height: 100px; resize: both;`. Editable textarea for content. Use `draggable` for repositioning. For resizable: `NodeResizer`. Resize observer for content auto-height.

## Q49: How do you implement a flow minimap with zoom level indicator?
**A:** Combine `<MiniMap>` with a zoom display: `const viewport = useViewport(); <div style={{ position: 'absolute', bottom: 10, right: 10 }}>Zoom: {Math.round(viewport.zoom * 100)}%</div>`. For zoom controls: `<Controls showInteractive={false} />`. Custom zoom buttons: `const { zoomIn, zoomOut } = useReactFlow(); <button onClick={() => zoomIn({ duration: 200 })}>+</button>`.

## Q50: How do you implement custom edge path with arrowhead markers at multiple positions?
**A:** `markerEnd` and `markerStart` for begin/end. For mid-edge markers: render additional markers in custom edge: `<path d={edgePath} markerMid="url(#arrow)" />`. Define marker: `<marker id="arrow" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" /></marker>`. For animated moving dot: `<circle r="4" fill="blue"><animateMotion dur="2s" repeatCount="indefinite" path={edgePath} /></circle>`.

## Q51: How do you implement async data loading with loading states on nodes?
**A:** Custom node tracks loading state: `const [loading, setLoading] = useState(data.loading); useEffect(() => { if (data.fetchFn) { data.fetchFn().then(result => { updateNodeData(id, { ...result, loading: false }); setLoading(false); }); } }, [])`. Render spinner when loading: `{loading ? <Spinner /> : <div>{data.content}</div>}`. For error states: `{error && <div className="error">{error}</div>}`.

## Q52: How do you implement conditional edges with branching logic?
**A:** Store condition in edge data: `edge.data = { condition: 'true' }`. Custom edge renders label: `<div>{data.condition}</div>`. For validation: target handle color based on condition type. For visual: true-path green, false-path red. Use `sourceHandle` to differentiate: source handles can be `handle-true` and `handle-false`. Nodes have multiple source handles for each branch.

## Q53: How do you implement a mini-map with custom styling and branded colors?
**A:** `<MiniMap nodeColor={(n) => n.data?.color || '#eee'} nodeStrokeColor={(n) => n.selected ? '#ff0072' : '#333'} maskColor="rgba(0,0,0,0.3)" style={{ background: '#fff', border: '1px solid #ddd', borderRadius: 8, boxShadow: '0 2px 8px rgba(0,0,0,0.15)' }} />`. For brand colors: map node types to brand palette. For dark mode: invert colors.

## Q54: How do you implement node history/audit trail visualization?
**A:** Each node stores `data.history: [{ timestamp, action, user }]`. Custom node renders a history icon when history exists: `{data.history?.length > 0 && <HistoryBadge count={data.history.length} />}`. Tooltip shows timeline. For edge history: color-code edges by last modified time. For audit view: switch to "history mode" that shows all changes as superimposed nodes.

## Q55: How do you implement a ruler/guideline system for node alignment?
**A:** Track node positions. On drag, compare with other nodes' x/y: `const snapToGuidelines = (node, nodes) => { const guidelines = []; nodes.forEach(other => { if (Math.abs(node.position.x - other.position.x) < 5) guidelines.push({ type: 'vertical', x: other.position.x }); if (Math.abs(node.position.y - other.position.y) < 5) guidelines.push({ type: 'horizontal', y: other.position.y }); }); return guidelines; }`. Render guidelines as SVG lines. Snap node to nearest guideline on drop.

## Q56: How do you implement a node transformer (scale, rotate, skew)?
**A:** Render node with CSS transform: `const transform = `scale(${data.scale || 1}) rotate(${data.rotation || 0}deg)``. On the custom node wrapper div. Use handles `onTransformChange` to update node data. For rotate handle: add a small circle above the node. On drag of this handle: compute angle from node center to cursor. Apply to `data.rotation`.

## Q57: How do you implement an always-visible node (locked position)?
**A:** Set `draggable: false` and `selectable: false` on the node. For position lock: `position: { x: 0, y: 0 }` with `parentId: 'root'`. For viewport-fixed (always visible regardless of pan/zoom): use a portal approach. Render the node via `createPortal` and apply inverse viewport transform: `transform: translate(${-viewport.x}px, ${-viewport.y}px) scale(${1/viewport.zoom})`.

## Q58: How do you implement a connection line with intermediate points?
**A:** Custom connection line renders intermediate handles. On connect drag, show points along the path. Users click to add intermediate points. Store points in edge data: `data.points: [{x, y}]`. Custom edge renders path through points: `const path = points.reduce((acc, p) => acc + ` L ${p.x} ${p.y}`, `M ${sourceX} ${sourceY}`)`. For interactive editing: draggable points on the edge.

## Q59: How do you implement a node minimap with full detail view?
**A:** Custom `nodeDetail` component that renders a small version of the node's content: `const MiniNode = ({ data }) => <div style={{ transform: 'scale(0.3)', transformOrigin: 'top left', width: data.width * 3, height: data.height * 3 }}><ActualNodeContent /></div>`. Used in `<MiniMap nodeComponent={MiniNode}>`. For large nodes: limit detail level for performance.

## Q60: How do you implement collaboration (multi-user) with real-time sync?
**A:** Use WebSocket or Yjs for conflict resolution. On each change (nodes, edges, viewport), send delta to server. Receive remote changes and apply: `setNodes(applyNodeChanges(remoteChanges, nodes))`. For cursor presence: render other users' cursors as small floating elements. For selection sync: broadcast selected node IDs. Use `useOnSelectionChange` for local changes. Debounce updates.

## Q61: How do you implement a custom background pattern (e.g., graph paper, dots, grid)?
**A:** `<Background variant="dots" gap={20} size={2} color="#ccc" />`. For custom: use CSS background on the wrapper: `backgroundImage: radial-gradient(circle, #ccc 1px, transparent 1px); backgroundSize: 20px 20px`. SVG background: wrap `<ReactFlow>` in a div with SVG pattern as background. For zoom-aware grid: recalculate background size on zoom: `const gridSize = 20 * zoom`.

## Q62: How do you implement a node inspector panel that updates on selection?
**A:** `const selectedNode = nodes.find(n => n.selected);` Render panel: `<Inspector> <label>Label: <input value={selectedNode?.data.label} onChange={(e) => updateNodeData(selectedNode.id, { label: e.target.value })} /></label> </Inspector>`. For edges: show source/target info. For multi-select: show common properties. Use `useOnSelectionChange` for panel update. For deep inspection: show raw JSON.

## Q63: How do you implement an edge with dynamic thickness based on data?
**A:** Custom edge receives `data.thickness`. Render: `<path d={edgePath} strokeWidth={Math.max(1, data.thickness || 2)} />`. For data flow visualization: thickness maps to data volume. Use spring animation: `strokeWidth: useSpring(data.thickness, { stiffness: 300, damping: 30 })`. For gradient thickness: vary stroke width along path.

## Q64: How do you implement a node that renders a mini-chart (e.g., sparkline)?
**A:** Custom node data includes time series: `data.values: [1, 5, 3, 8, 2]`. Render SVG sparkline: `<svg width="100%" height="30"><path d={computePath(data.values)} fill="none" stroke="blue" strokeWidth={2} /></svg>`. For dynamic: animate path on data change. For responsive: use ResizeObserver. For multiple series: stacked or overlaid lines.

## Q65: How do you implement a connection validation that shows error tooltips?
**A:** `isValidConnection={(connection, sourceNode, targetNode) => { if (!isValidType(sourceNode, targetNode)) { setConnectionError('Incompatible types'); return false; } if (wouldCreateCycle(connection, nodes, edges)) { setConnectionError('Would create cycle'); return false; } return true; }}`. Show error tooltip: `<div style={{ position: 'fixed', top: cursorY, left: cursorX }}>{connectionError}</div>`. Clear error on connect or cancel.

## Q66: How do you implement node copy/paste with offset?
**A:** On Copy (Ctrl+C): store selected nodes and edges. On Paste (Ctrl+V): `const newNodes = clipboard.nodes.map(n => ({ ...n, id: uuid(), position: { x: n.position.x + 50, y: n.position.y + 50 }, selected: true })); const newEdges = clipboard.edges.map(e => ({ ...e, id: uuid(), source: findNewId(e.source), target: findNewId(e.target) }));`. For cross-tab: use clipboard API with JSON. For cut: delete after copy.

## Q67: How do you implement a constraint-based layout where nodes snap to a workbench?
**A:** Define workbench zones: `{ id: 'input', bounds: { x: 0, y: 0, w: 200, h: 400 } }`. On drag: `onNodeDragStop={(event, node) => { const zone = zones.find(z => isInside(node.position, z.bounds)); if (zone) { setNodes(n => n.map(n => n.id === node.id ? { ...n, position: zone.bounds } : n)); } }}`. For snap zones: show visual highlight when node enters zone. Constrain node type to specific zones.

## Q68: How do you implement a node that acts as a router/pass-through?
**A:** A router node has one input and multiple outputs. Custom node renders multiple `<Handle type="source">` handles. On connect, distribute incoming data to all outputs. For pass-through: clone incoming edge data to all outputs. For conditional routing: evaluate route expression in node data. Visual: show routing table inside the node.

## Q69: How do you implement a circuit-like flow with orthogonal routing?
**A:** Use `getSmoothStepPath` with `borderRadius={0}` for 90-degree angles. `defaultEdgeOptions={{ type: 'smoothstep', borderRadius: 0 }}`. For orthogonal with offset: compute custom path with only horizontal and vertical segments. For manhattan routing: `getBezierPath` with custom control points that force right-angle turns. For autorouting: `@reactflow/pathfinding-edge`.

## Q70: How do you implement a node with expand/collapse children?
**A:** Group node with `style={{ overflow: 'hidden' }}`. On collapse: hide children by setting `hidden: true`. Animate parent height: `animate={{ height: collapsed ? collapsedHeight : expandedHeight }}`. Use `getNodesBounds` for expanded size. On expand: `setNodes(nodes => nodes.map(n => n.parentId === id ? { ...n, hidden: false } : n))`. Icon: chevron rotation.

## Q71: How do you implement an edge with multiple segments (waypoints)?
**A:** Store waypoints in edge data: `data.waypoints: [{x, y}, ...]`. Custom edge renders segmented path: `const path = data.waypoints.reduce((acc, p) => acc + ` L ${p.x} ${p.y}`, `M ${sourceX} ${sourceY}`) + ` L ${targetX} ${targetY}``. For draggable waypoints: render handles on each waypoint. On drag: update waypoint position in edge data. For add: double-click on edge.

## Q72: How do you implement a node that displays markdown content?
**A:** Custom node uses a markdown renderer: `import ReactMarkdown from 'react-markdown'; <div className="markdown-node"><ReactMarkdown>{data.content}</ReactMarkdown></div>`. For editing: toggle between markdown source and rendered view. For security: sanitize markdown to prevent XSS. For custom styling: extend markdown components. For live preview: render both side by side.

## Q73: How do you implement a node with dynamic handle creation (add/remove ports)?
**A:** Maintain handle config in node data: `data.handles: [{ id: 'h1', position: 'left' }]`. Render handles dynamically: `{data.handles.map(h => <Handle key={h.id} id={h.id} type="target" position={h.position} />)}`. Add handle: `updateNodeData(id, { handles: [...data.handles, { id: uuid(), position: 'left' }] })`. Remove: filter out. Re-render triggered via `useUpdateNodeInternals`.

## Q74: How do you implement a node alignment toolbar?
**A:** Select multiple nodes. Toolbar buttons: Align left/center/right/top/middle/bottom. Implementation: `const alignLeft = () => { const minX = Math.min(...selectedNodes.map(n => n.position.x)); setNodes(nodes => nodes.map(n => n.selected ? { ...n, position: { ...n.position, x: minX } } : n)) }`. Distribute evenly: calculate total span and equal gaps. For grid align: snap to grid.

## Q75: How do you implement edges with custom styles per status (active, error, success)?
**A:** Edge data includes `status`. Custom edge maps status to colors: `const strokeColor = { active: '#0072ff', error: '#ff4400', success: '#00cc66', default: '#b1b1b7' }[data.status]`. Animate on status change: use CSS transition on stroke. For pulse animation on active: `@keyframes pulse { 0% { stroke-opacity: 1; } 50% { stroke-opacity: 0.5; } 100% { stroke-opacity: 1; } }`.

## Q76: How do you implement a node that functions as a sub-diagram (click to zoom)?
**A:** On double-click: `onNodeDoubleClick={(event, node) => { if (node.type === 'subflow') { setViewport({ x: -node.position.x, y: -node.position.y, zoom: 2 }, { duration: 300 }); showSubFlow(node.data.subNodes, node.data.subEdges); } }`. For breadcrumb: show parent node label at top. For zoom-out: reverse transform or button.

## Q77: How do you implement infinite canvas with minimap navigation?
**A:** React Flow handles infinite canvas by default. For minimap navigation: `<MiniMap pannable zoomable />`. For click-to-center on minimap: `<MiniMap onClick={(event) => { const point = event.currentTarget.relContainerPoint; reactFlowInstance.setCenter(point.x, point.y); }} />`. For labeled areas on canvas: render static text elements with `pointerEvents: none`.

## Q78: How do you implement a node color picker with theme support?
**A:** In node inspector: `<input type="color" value={selectedNode.data.color || '#fff'} onChange={(e) => updateNodeData(selectedNode.id, { color: e.target.value })} />`. For theme presets: color swatches. Apply color to node: `style={{ background: data.color }}`. For theme sync: `const { nodeColor } = useTheme(); style={{ background: data.color || nodeColor }}`.

## Q79: How do you implement edge labels that show relationship type?
**A:** Edge data has `relationship`. Custom edge renders label on path: `<div style={{ position: 'absolute', transform: `translate(${labelX}px,${labelY}px)` }}>{data.relationship}</div>`. For dynamic: update relationship via edge inspector. For visual: color-code by relationship. For direction indicator: arrow shows direction. For multiple labels: `{data.relationships?.map(r => <Label key={r}>{r}</Label>)}`.

## Q80: How do you implement a node that displays an image/rich media?
**A:** Custom node renders image: `{data.imageUrl && <img src={data.imageUrl} alt={data.label} style={{ maxWidth: '100%', height: 'auto' }} />}`. For video: `<video src={data.videoUrl} controls />`. For iframe: `<iframe src={data.url} title={data.label} />`. Handle sizing: use ResizeObserver for responsive. For performance: lazy load images. For placeholder: show loading skeleton.

## Q81: How do you implement custom edge creation behavior (e.g., click to connect)?
**A:** Instead of drag-to-connect, use click mode: `const [connecting, setConnecting] = useState(null); onNodeClick: (event, node) => { if (connecting) { addEdge({ source: connecting.id, target: node.id }); setConnecting(null); } else { setConnecting(node); } }`. Visual feedback: highlight connectable nodes. For keyboard modifier: hold Shift for click-connect mode.

## Q82: How do you implement node and edge history with diff highlighting?
**A:** Store snapshots on each change. Compare current with previous: `const getDiff = (prev, curr) => { const added = curr.filter(c => !prev.find(p => p.id === c.id)); const removed = prev.filter(p => !curr.find(c => c.id === p.id)); const modified = curr.filter(c => { const p = prev.find(pr => pr.id === c.id); return p && JSON.stringify(p) !== JSON.stringify(c); }); return { added, removed, modified }; }`. Highlight: green glow for added, red for removed, yellow for modified.

## Q83: How do you implement a node that acts as a group with configurable padding?
**A:** Group node with `style={{ padding: data.padding || 20 }}`. Children positions are relative. When group moves, children move with it. For resize: update padding. `getNodesBounds` calculates total area. For label: render group label at top-left. For collapsible: animatable padding and child visibility. Recommended children extent: `extent: 'parent'`.

## Q84: How do you implement a node data update that triggers edge recolor?
**A:** When node data changes, update connected edges: `const updateEdges = (nodeId) => { setEdges(edges => edges.map(e => e.source === nodeId || e.target === nodeId ? { ...e, data: { ...e.data, color: computeEdgeColor(nodeId, e) } } : e)) }`. Use `onNodesChange` to detect data changes. For performance: debounce update. For animation: use CSS transition on edge stroke.

## Q85: How do you implement a multi-select drag with group move?
**A:** Select multiple nodes (Shift+click or box select). Drag any selected node moves the group. React Flow handles this natively: `multiSelectionKeyCode="Shift"`. For programmatic move: `setNodes(nodes => nodes.map(n => n.selected ? { ...n, position: { x: n.position.x + dx, y: n.position.y + dy } } : n))`. For proportional move: calculate delta from initial positions.

## Q86: How do you implement a connection line with real-time validation icon?
**A:** Use `connectionLineComponent` with status indicator. On connection drag, validate in real-time. Render checkmark (valid) or X (invalid) near cursor: `<div style={{ position: 'absolute', left: toX, top: toY - 20 }}>{connectionStatus === 'valid' ? '✓' : '✗'}</div>`. Color code: green/red. For custom: show tooltip with validation message. Use `isValidConnection` for all validation logic.

## Q87: How do you implement a node with auto-resize textarea?
**A:** Custom node renders `<textarea>`: `const [height, setHeight] = useState(40); <textarea value={data.label} onChange={(e) => { updateNodeData(id, { label: e.target.value }); setHeight(e.target.scrollHeight); }} style={{ height, resize: 'none', overflow: 'hidden' }} />`. Update node dimensions: `const updateDimensions = useCallback(() => { if (nodeRef.current) { const { width, height } = nodeRef.current.getBoundingClientRect(); updateNodeDimensions(id, { width, height }); } }, [id])`.

## Q88: How do you implement an edge that displays data transfer animation (like a progress bar)?
**A:** Custom edge with animated bar along path: `<path d={edgePath} stroke="#eee" strokeWidth={4} /><path d={edgePath} stroke="#0072ff" strokeWidth={4} strokeDasharray={data.progress * pathLength} strokeDashoffset={-pathLength} />`. For continuous flow: `<circle r="4" fill="#0072ff"><animateMotion dur="2s" repeatCount="indefinite" path={edgePath} /></circle>`. For batch transfer: animate multiple dots.

## Q89: How do you implement a node that shows a loading indicator on async operations?
**A:** Custom node state: `const nodeStatus = data.status || 'idle'`. Render: `{nodeStatus === 'loading' && <Spinner />} {nodeStatus === 'error' && <ErrorIcon message={data.error} />}`. On async operation: `updateNodeData(id, { status: 'loading' }); try { await operation(); updateNodeData(id, { status: 'success' }); } catch (e) { updateNodeData(id, { status: 'error', error: e.message }); }`. For timeout: add progress indicator.

## Q90: How do you implement a node that works as a code editor (Monaco/CodeMirror)?
**A:** Custom node renders an embedded code editor: `<CodeMirror value={data.code} onChange={(val) => updateNodeData(id, { code: val })} />`. Set node dimensions to accommodate editor (min 300x200). For language highlighting: `data.language` prop. For read-only: `editable={!data.readOnly}`. For performance: use `useMemo` for editor instance. Lazy load editor.

## Q91: How do you implement React Flow v11's new features over v10?
**A:** v11 introduces: 1) `useReactFlow` instead of `ReactFlowInstance`. 2) `applyNodeChanges` and `applyEdgeChanges` for state management. 3) `<Background>` replaces `<BackgroundVariant>`. 4) `EdgeLabelRenderer` for edge labels. 5) `layoutAnimation` for smooth layout transitions. 6) `onlyRenderVisibleElements` optimization. 7) `onNodeDragStart`/`onNodeDrag`/`onNodeDragStop` separation. Migration: replace `reactFlowInstance` with `useReactFlow()`, use new apply functions.

## Q92: How do you implement a node that shows a tooltip with connection details?
**A:** On hover over edge: render tooltip. `onEdgeMouseEnter={(event, edge) => setTooltip({ show: true, content: edge.data, x: event.clientX, y: event.clientY })}`. Portal: `<EdgeLabelRenderer>{tooltip.show && <div style={{ position: 'absolute', left: tooltip.x, top: tooltip.y - 30 }}>{tooltip.content}</div>}</EdgeLabelRenderer>`. For nodes: `onNodeMouseEnter`. For edge connection info: show source, target, and data.

## Q93: How do you implement a node that has configurable input/output types?
**A:** Node data has `inputTypes` and `outputTypes`. Each handle has a type label. Custom node renders: `<Handle type="target" position={Position.Left} id="input"><div className="handle-label">{data.inputType}</div></Handle>`. Connection validation: `isValidConnection={(conn) => { const sourceNode = getNode(conn.source); const targetNode = getNode(conn.target); return sourceNode.data.outputType === targetNode.data.inputType; }}`. Color-code handles by type.

## Q94: How do you implement a node with grouped handles (folders)?
**A:** Group handles in node data: `data.handleGroups: [{ name: 'Inputs', handles: [{ id: 'in1' }, { id: 'in2' }] }]`. Custom node renders sections: `<div className="handle-group"><div className="group-label">{group.name}</div>{group.handles.map(h => <Handle ... />)}</div>`. For collapsible groups: toggle visibility. For mixed input/output: separate sections.

## Q95: How do you implement edge bundling for cleaner visualization?
**A:** Custom edge type that draws bundled paths. Group edges by source-target pair. For parallel edges, offset paths: `const offset = index * 10 - (total - 1) * 5; const [path] = getBezierPath({ sourceX, sourceY: sourceY + offset, targetX, targetY: targetY + offset })`. For source/target aggregation: draw a single thick path that fans out at ends. Use SVG curves for smooth bundles.

## Q96: How do you implement a node that shows a custom context menu on right-click?
**A:** `onNodeContextMenu={(event, node) => { event.preventDefault(); setContextMenu({ node, x: event.clientX, y: event.clientY, items: ['Delete', 'Duplicate', 'Edit', ...] }); }}`. Render: `<div className="context-menu" style={{ left: menu.x, top: menu.y, position: 'fixed' }}><MenuItem label="Delete" onClick={() => { deleteNode(menu.node.id); setContextMenu(null) }} /></div>`. Close on click outside.

## Q97: How do you implement a node that synchronizes with external data sources?
**A:** Node data has `sourceConfig: { url, method, interval }`. Effect: `useEffect(() => { const fetchData = async () => { const res = await fetch(data.sourceConfig.url); const result = await res.json(); updateNodeData(id, { ...result, lastSync: Date.now() }); }; fetchData(); const interval = setInterval(fetchData, data.sourceConfig.interval || 30000); return () => clearInterval(interval); }, [data.sourceConfig])`. Show sync status: lastSync time and status indicator.

## Q98: How do you implement a node that renders a form with validation?
**A:** Custom node renders form fields: `{data.fields.map(f => <div key={f.name}>{f.label}: <input value={f.value} onChange={(e) => { const newFields = data.fields.map(fi => fi.name === f.name ? { ...fi, value: e.target.value } : fi); updateNodeData(id, { fields: newFields }); }} style={f.error ? { borderColor: 'red' } : {}} /></div>)}`. Validate: `const errors = validate(fields); updateNodeData(id, { errors })`. Show error messages.

## Q99: How do you implement a node with animated status indicators (pulsing, blinking)?
**A:** Status indicator: `<span className={status ${data.status}} />`. CSS: `.status.active { animation: pulse 2s infinite; } .status.error { animation: blink 1s infinite; } @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(0, 114, 255, 0.7); } 70% { box-shadow: 0 0 0 10px rgba(0, 114, 255, 0); } 100% { box-shadow: 0 0 0 0 rgba(0, 114, 255, 0); } } @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }`. For gradient animation: animate background position.

## Q100: How do you implement a node that acts as a webhook/API trigger with request/response preview?
**A:** Custom node stores `data.method`, `data.url`, `data.body`, `data.response`. Render: `<div><div class="method">{data.method}</div><div class="url">{data.url}</div><button onClick={testWebhook}>Test</button><details><summary>Response</summary><pre>{data.response}</pre></details></div>`. Test: `const res = await fetch(data.url, { method: data.method, body: data.body }); updateNodeData(id, { response: await res.text(), status: res.status })`. Show status badge (2xx=green, 4xx=yellow, 5xx=red).
