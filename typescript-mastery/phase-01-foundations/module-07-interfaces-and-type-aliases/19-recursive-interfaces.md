# Recursive Interfaces

> Phase 1 · Module 07 · Interfaces and Type Aliases

**TL;DR** — A recursive interface refers to itself, directly or through another type, to model trees, linked lists, and nested structures.

## Syntax
```ts
interface TreeNode {
  value: number;
  children: TreeNode[];
}
```

## Examples
### Basic
```ts
interface TreeNode {
  value: number;
  children: TreeNode[];
}

const tree: TreeNode = {
  value: 1,
  children: [
    { value: 2, children: [] },
    { value: 3, children: [{ value: 4, children: [] }] },
  ],
};
```

### Practical
```ts
interface LinkedList<T> {
  value: T;
  next: LinkedList<T> | null;
}

function toArray<T>(node: LinkedList<T> | null): T[] {
  const result: T[] = [];
  let current = node;
  while (current) {
    result.push(current.value);
    current = current.next;
  }
  return result;
}

const list: LinkedList<number> = {
  value: 1,
  next: { value: 2, next: { value: 3, next: null } },
};

console.log(toArray(list)); // [1, 2, 3]
```

### Advanced / edge cases
```ts
// Mutually recursive interfaces.
interface FileNode {
  kind: "file";
  name: string;
  size: number;
}

interface FolderNode {
  kind: "folder";
  name: string;
  children: TreeEntry[];
}

type TreeEntry = FileNode | FolderNode;

const root: FolderNode = {
  kind: "folder",
  name: "root",
  children: [
    { kind: "file", name: "a.ts", size: 120 },
    {
      kind: "folder",
      name: "src",
      children: [{ kind: "file", name: "b.ts", size: 80 }],
    },
  ],
};

function totalSize(node: TreeEntry): number {
  return node.kind === "file"
    ? node.size
    : node.children.reduce((sum, child) => sum + totalSize(child), 0);
}

console.log(totalSize(root)); // 200
```

## Key points
- Recursive interfaces model self-similar data.
- Recursion usually goes through an array, object, or nullable link.
- Mutual recursion works when each interface references the other.
- Recursive functions pair naturally with recursive types.
- The compiler handles recursion lazily during type checking.

## Gotchas
- A required direct self-reference like `interface Node { parent: Node }` compiles, but no finite value can ever satisfy it.
- Deeply nested data can hit recursion limits in the compiler or at runtime.
- Forgetting `| null` on a linked list makes the end impossible to represent.

## Best practice
- Always provide a terminating case: `[]`, `null`, or an optional child.
- Write a recursive traversal with an explicit base case alongside the type.
