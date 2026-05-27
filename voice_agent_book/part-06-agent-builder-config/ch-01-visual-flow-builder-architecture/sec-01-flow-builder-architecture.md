# Section 01: Flow Builder Architecture

## Overview

The Visual Flow Builder is the no-code interface where users design conversation flows for their AI agents. It uses React Flow for the node-based editor, Zustand for state management, and a custom execution engine for runtime flow interpretation. The builder must support drag-and-drop node placement, edge routing, undo/redo, and real-time validation.

The architecture follows a layered pattern: (1) Canvas Layer - React Flow rendering and interaction, (2) State Layer - Zustand store with Immer for immutable updates, (3) Validation Layer - runtime flow validation, and (4) Serialization Layer - flow import/export as JSON.

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                  Visual Flow Builder                           │
├──────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────────┐      │
│  │  Canvas Layer (React Flow)                          │      │
│  │  - Node placement & drag  - Edge routing           │      │
│  │  - Zoom/pan              - Selection               │      │
│  └──────────────────┬─────────────────────────────────┘      │
│                     │                                          │
│  ┌──────────────────▼─────────────────────────────────┐      │
│  │  State Layer (Zustand + Immer)                       │      │
│  │  - Nodes Map: Record<id, Node>                       │      │
│  │  - Edges Map: Record<id, Edge>                       │      │
│  │  - Undo/Redo stacks (max 100)                        │      │
│  │  - Selected items set                                │      │
│  └──────────────────┬─────────────────────────────────┘      │
│                     │                                          │
│  ┌──────────────────▼─────────────────────────────────┐      │
│  │  Validation Layer                                    │      │
│  │  - Required fields check  - Cycle detection         │      │
│  │  - Unreachable nodes     - Type checking           │      │
│  └──────────────────┬─────────────────────────────────┘      │
│                     │                                          │
│  ┌──────────────────▼─────────────────────────────────┐      │
│  │  Serialization Layer                                 │      │
│  │  - JSON export/import  - Versioning               │      │
│  │  - Diff generation    - Migration support         │      │
│  └────────────────────────────────────────────────────┘      │
└──────────────────────────────────────────────────────────────┘
```

## Design Decisions

- **React Flow over Custom Canvas**: React Flow provides battle-tested node/edge rendering, drag-and-drop, zoom/pan, and accessibility out of the box. Custom canvas would require 6+ months of development for comparable functionality.
- **Zustand over Redux**: Zustand offers simpler API, better TypeScript inference, and smaller bundle (1KB vs 12KB). The Immer middleware enables immutable updates for undo/redo without boilerplate.
- **Local-First State**: All state is local first with automatic debounced saves to the backend (2s debounce). This provides instant UI response without waiting for API calls.
- **Function-as-Edge**: Edges represent function calls between nodes. Each edge can carry conditions (for conditional branching) and transforms (for data mapping).

## Implementation Approach

```typescript
import { useCallback } from 'react';
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';

interface FlowState {
  nodes: Record<string, FlowNode>;
  edges: Record<string, FlowEdge>;
  selectedIds: Set<string>;
  undoStack: FlowSnapshot[];
  redoStack: FlowSnapshot[];

  addNode: (type: string, position: XYPosition) => string;
  removeNode: (id: string) => void;
  addEdge: (source: string, target: string, condition?: string) => string;
  undo: () => void;
  redo: () => void;
}

const useFlowStore = create<FlowState>()(
  immer((set) => ({
    nodes: {},
    edges: {},
    selectedIds: new Set(),
    undoStack: [],
    redoStack: [],

    addNode: (type, position) => {
      const id = crypto.randomUUID();
      set((state) => {
        state.undoStack.push(snapshot(state));
        state.nodes[id] = { id, type, position, data: {} };
      });
      return id;
    },

    undo: () => {
      set((state) => {
        const snapshot = state.undoStack.pop();
        if (snapshot) {
          state.redoStack.push(snapshot(state));
          restore(state, snapshot);
        }
      });
    },
  }))
);
```

## Integration Points

- **Node Library (P6 Ch 02)**: Node types registered via plugin system. Each type provides renderer, editor component, and validation rules.
- **Prompt Editor (P6 Ch 03)**: Message nodes link to prompt templates. Variable injection uses the flow context.
- **Execution Engine**: The flow JSON is consumed by the runtime execution engine. Each node executes its handler in sequence.

## Open-Source Tools

- **React Flow** (MIT): Node-based UI builder by xyflow. 20k+ GitHub stars.
- **Zustand** (MIT): Lightweight state management. 45k+ GitHub stars.
- **Immer** (MIT): Immutable state updates with mutable syntax.
- **React DnD** (MIT): Drag and drop for node palette.

## Production Considerations

- **Performance**: Render optimization: virtualize nodes if >100, use React.memo for node components, batch Zustand updates with React 18 batching.
- **Persistence**: Autosave every 2 seconds. Version every save. Conflict resolution for concurrent edits.
- **Undo/Redo Limit**: Max 100 undo steps to control memory usage. Each snapshot ~2KB for average flow.
- **Mobile Support**: Touch events for mobile browsers. Pinch-to-zoom. Snappier interaction on tablets.
