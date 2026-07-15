# Command Pattern in TypeScript

## Table of Contents

- [Command Pattern Basics](#command-pattern-basics)
- [Command Interface](#command-interface)
- [Concrete Commands](#concrete-commands)
- [Invoker](#invoker)
- [Undo/Redo](#undoredo)
- [Command Queue](#command-queue)
- [Typed Commands](#typed-commands)
- [Macro Commands](#macro-commands)
- [Real-World Examples](#real-world-examples)
- [Interview Questions](#interview-questions)

---

## Command Pattern Basics

The Command pattern encapsulates a request as an object, allowing parameterization and queuing of requests.

```typescript
// Basic concept
interface Command {
  execute(): void;
  undo(): void;
}

class Light {
  isOn = false;

  turnOn(): void {
    this.isOn = true;
    console.log("Light is on");
  }

  turnOff(): void {
    this.isOn = false;
    console.log("Light is off");
  }
}

class LightOnCommand implements Command {
  constructor(private light: Light) {}

  execute(): void {
    this.light.turnOn();
  }

  undo(): void {
    this.light.turnOff();
  }
}

class LightOffCommand implements Command {
  constructor(private light: Light) {}

  execute(): void {
    this.light.turnOff();
  }

  undo(): void {
    this.light.turnOn();
  }
}

// Invoker
class RemoteControl {
  private history: Command[] = [];

  execute(command: Command): void {
    command.execute();
    this.history.push(command);
  }

  undo(): void {
    const command = this.history.pop();
    command?.undo();
  }
}

// Usage
const light = new Light();
const remote = new RemoteControl();

remote.execute(new LightOnCommand(light));  // Light is on
remote.execute(new LightOffCommand(light)); // Light is off
remote.undo(); // Light is on (undo the off command)
```

---

## Command Interface

```typescript
// Generic command with result
interface Command<T = void> {
  execute(): T;
  undo(): T;
  describe(): string;
}

// Async command
interface AsyncCommand<T = void> {
  execute(): Promise<T>;
  undo(): Promise<T>;
  describe(): string;
}

// Command with metadata
interface TypedCommand<TInput, TOutput> {
  readonly type: string;
  readonly input: TInput;
  execute(): TOutput;
  undo(): void;
}

// Stateful command
interface StatefulCommand<T> {
  execute(): T;
  undo(): T;
  canUndo(): boolean;
  canRedo(): boolean;
  getState(): CommandState;
}

interface CommandState {
  executed: boolean;
  undone: boolean;
  timestamp: Date;
}
```

---

## Concrete Commands

```typescript
// Text editor commands
class TextEditor {
  private content = "";
  private clipboard = "";

  getContent(): string { return this.content; }
  setContent(content: string): void { this.content = content; }
  getClipboard(): string { return this.clipboard; }
  setClipboard(text: string): void { this.clipboard = text; }
}

class InsertTextCommand implements Command {
  private previousContent: string = "";

  constructor(
    private editor: TextEditor,
    private text: string,
    private position: number = -1
  ) {}

  execute(): void {
    this.previousContent = this.editor.getContent();
    const pos = this.position === -1 ? this.previousContent.length : this.position;
    const content = this.previousContent;
    this.editor.setContent(content.slice(0, pos) + this.text + content.slice(pos));
  }

  undo(): void {
    this.editor.setContent(this.previousContent);
  }

  describe(): string {
    return `Insert "${this.text}"`;
  }
}

class DeleteTextCommand implements Command {
  private deletedText: string = "";

  constructor(
    private editor: TextEditor,
    private start: number,
    private end: number
  ) {}

  execute(): void {
    const content = this.editor.getContent();
    this.deletedText = content.slice(this.start, this.end);
    this.editor.setContent(content.slice(0, this.start) + content.slice(this.end));
  }

  undo(): void {
    const content = this.editor.getContent();
    this.editor.setContent(
      content.slice(0, this.start) + this.deletedText + content.slice(this.start)
    );
  }

  describe(): string {
    return `Delete "${this.deletedText}"`;
  }
}

class CopyTextCommand implements Command {
  constructor(private editor: TextEditor, private start: number, private end: number) {}

  execute(): void {
    const content = this.editor.getContent();
    this.editor.setClipboard(content.slice(this.start, this.end));
  }

  undo(): void {
    // Copy is not undoable, but we implement the interface
  }

  describe(): string {
    return "Copy text";
  }
}
```

---

## Invoker

```typescript
// Command invoker with history
class CommandInvoker {
  private history: Command[] = [];
  private redoStack: Command[] = [];

  execute(command: Command): void {
    command.execute();
    this.history.push(command);
    this.redoStack = []; // Clear redo stack on new command
  }

  undo(): void {
    const command = this.history.pop();
    if (command) {
      command.undo();
      this.redoStack.push(command);
    }
  }

  redo(): void {
    const command = this.redoStack.pop();
    if (command) {
      command.execute();
      this.history.push(command);
    }
  }

  canUndo(): boolean {
    return this.history.length > 0;
  }

  canRedo(): boolean {
    return this.redoStack.length > 0;
  }

  getHistory(): string[] {
    return this.history.map((cmd) => cmd.describe());
  }

  clearHistory(): void {
    this.history = [];
    this.redoStack = [];
  }
}

// Usage
const editor = new TextEditor();
const invoker = new CommandInvoker();

invoker.execute(new InsertTextCommand(editor, "Hello"));
invoker.execute(new InsertTextCommand(editor, " World"));
console.log(editor.getContent()); // "Hello World"

invoker.undo();
console.log(editor.getContent()); // "Hello"

invoker.redo();
console.log(editor.getContent()); // "Hello World"

console.log(invoker.getHistory()); // ["Insert \"Hello\"", "Insert \" World\""]
```

---

## Undo/Redo

```typescript
// Full undo/redo system
class UndoRedoManager<T = void> {
  private undoStack: Command<T>[] = [];
  private redoStack: Command<T>[] = [];

  execute(command: Command<T>): T {
    const result = command.execute();
    this.undoStack.push(command);
    this.redoStack = [];
    return result;
  }

  undo(): T | null {
    const command = this.undoStack.pop();
    if (!command) return null;
    const result = command.undo();
    this.redoStack.push(command);
    return result;
  }

  redo(): T | null {
    const command = this.redoStack.pop();
    if (!command) return null;
    const result = command.execute();
    this.undoStack.push(command);
    return result;
  }

  canUndo(): boolean {
    return this.undoStack.length > 0;
  }

  canRedo(): boolean {
    return this.redoStack.length > 0;
  }

  clear(): void {
    this.undoStack = [];
    this.redoStack = [];
  }

  get undoCount(): number {
    return this.undoStack.length;
  }

  get redoCount(): number {
    return this.redoStack.length;
  }
}

// Shape drawing commands
interface Point {
  x: number;
  y: number;
}

class Canvas {
  private shapes: Array<{ type: string; point: Point; size: number }> = [];

  draw(shape: { type: string; point: Point; size: number }): void {
    this.shapes.push(shape);
    console.log(`Drew ${shape.type} at (${shape.point.x}, ${shape.point.y})`);
  }

  removeLast(): void {
    const shape = this.shapes.pop();
    if (shape) {
      console.log(`Removed ${shape.type} at (${shape.point.x}, ${shape.point.y})`);
    }
  }

  getShapes(): readonly Array<{ type: string; point: Point; size: number }> {
    return this.shapes;
  }
}

class DrawShapeCommand implements Command {
  constructor(
    private canvas: Canvas,
    private shape: { type: string; point: Point; size: number }
  ) {}

  execute(): void {
    this.canvas.draw(this.shape);
  }

  undo(): void {
    this.canvas.removeLast();
  }

  describe(): string {
    return `Draw ${this.shape.type}`;
  }
}
```

---

## Command Queue

```typescript
// Async command queue
class CommandQueue {
  private queue: Array<() => Promise<void>> = [];
  private processing = false;

  enqueue(command: AsyncCommand): void {
    this.queue.push(async () => {
      await command.execute();
    });
    this.processNext();
  }

  private async processNext(): Promise<void> {
    if (this.processing || this.queue.length === 0) return;

    this.processing = true;
    const task = this.queue.shift()!;

    try {
      await task();
    } finally {
      this.processing = false;
      this.processNext();
    }
  }

  get size(): number {
    return this.queue.length;
  }
}

// Batch command execution
class BatchExecutor {
  private commands: Command[] = [];

  add(command: Command): void {
    this.commands.push(command);
  }

  executeAll(): void {
    for (const command of this.commands) {
      command.execute();
    }
  }

  undoAll(): void {
    for (const command of [...this.commands].reverse()) {
      command.undo();
    }
  }

  clear(): void {
    this.commands = [];
  }
}
```

---

## Typed Commands

```typescript
// Type-safe command system
interface TypedCommand<TInput, TOutput> {
  readonly type: string;
  readonly input: TInput;
  execute(input: TInput): TOutput;
  undo(output: TOutput): void;
}

// Command registry
class CommandRegistry {
  private commands = new Map<string, TypedCommand<any, any>>();

  register<TInput, TOutput>(command: TypedCommand<TInput, TOutput>): void {
    this.commands.set(command.type, command);
  }

  execute<TInput, TOutput>(
    type: string,
    input: TInput
  ): TOutput {
    const command = this.commands.get(type);
    if (!command) throw new Error(`Unknown command: ${type}`);
    return command.execute(input);
  }
}

// Concrete typed commands
class CreateUserCommand implements TypedCommand<CreateUserDTO, User> {
  readonly type = "create_user";

  constructor(private userService: UserService) {}

  execute(input: CreateUserDTO): User {
    return this.userService.create(input);
  }

  undo(output: User): void {
    this.userService.delete(output.id);
  }
}

class SendEmailCommand implements TypedCommand<EmailDTO, void> {
  readonly type = "send_email";

  constructor(private emailService: EmailService) {}

  execute(input: EmailDTO): void {
    this.emailService.send(input);
  }

  undo(): void {
    // Email cannot be undone, but we implement the interface
  }
}

// Usage
const registry = new CommandRegistry();
registry.register(new CreateUserCommand(userService));
registry.register(new SendEmailCommand(emailService));

const user = registry.execute<CreateUserDTO, User>("create_user", {
  name: "Alice",
  email: "alice@example.com",
});
```

---

## Macro Commands

```typescript
// Macro command (composite command)
class MacroCommand implements Command {
  private commands: Command[] = [];

  add(command: Command): void {
    this.commands.push(command);
  }

  execute(): void {
    for (const command of this.commands) {
      command.execute();
    }
  }

  undo(): void {
    for (const command of [...this.commands].reverse()) {
      command.undo();
    }
  }

  describe(): string {
    return `Macro (${this.commands.length} commands)`;
  }
}

// Usage
const macro = new MacroCommand();
macro.add(new InsertTextCommand(editor, "Hello"));
macro.add(new InsertTextCommand(editor, " "));
macro.add(new InsertTextCommand(editor, "World"));

invoker.execute(macro);
console.log(editor.getContent()); // "Hello World"

invoker.undo();
console.log(editor.getContent()); // ""

// Predefined macros
class TextEditorMacros {
  static greeting(editor: TextEditor): MacroCommand {
    const macro = new MacroCommand();
    macro.add(new InsertTextCommand(editor, "Dear "));
    macro.add(new InsertTextCommand(editor, "[Name]"));
    macro.add(new InsertTextCommand(editor, ",\n\n"));
    macro.add(new InsertTextCommand(editor, "Thank you for your message."));
    macro.add(new InsertTextCommand(editor, "\n\nBest regards"));
    return macro;
  }

  static signature(editor: TextEditor): MacroCommand {
    const macro = new MacroCommand();
    macro.add(new InsertTextCommand(editor, "\n\n---\n"));
    macro.add(new InsertTextCommand(editor, "John Doe"));
    macro.add(new InsertTextCommand(editor, "\nSoftware Engineer"));
    return macro;
  }
}
```

---

## Real-World Examples

```typescript
// Git-like version control
interface CommitCommand {
  id: string;
  message: string;
  changes: FileChange[];
  execute(): void;
  undo(): void;
}

interface FileChange {
  path: string;
  action: "create" | "modify" | "delete";
  content?: string;
  previousContent?: string;
}

class GitRepository {
  private commits: CommitCommand[] = [];
  private currentChanges: FileChange[] = [];

  stage(change: FileChange): void {
    this.currentChanges.push(change);
  }

  commit(message: string): CommitCommand {
    const commit: CommitCommand = {
      id: crypto.randomUUID(),
      message,
      changes: [...this.currentChanges],
      execute: () => {
        // Apply changes
        for (const change of commit.changes) {
          if (change.action === "create" || change.action === "modify") {
            // Write file
          } else if (change.action === "delete") {
            // Delete file
          }
        }
      },
      undo: () => {
        // Revert changes
        for (const change of [...commit.changes].reverse()) {
          if (change.action === "create") {
            // Delete created file
          } else if (change.action === "modify") {
            // Restore previous content
          } else if (change.action === "delete") {
            // Recreate deleted file
          }
        }
      },
    };

    this.commits.push(commit);
    this.currentChanges = [];
    return commit;
  }
}

// Task management
interface TaskCommand {
  type: "create" | "update" | "delete" | "complete";
  taskId?: string;
  data?: Partial<Task>;
  execute(): string;
  undo(id: string): void;
}

class TaskManager {
  private tasks = new Map<string, Task>();

  create(data: Task): string {
    const id = crypto.randomUUID();
    this.tasks.set(id, { ...data, id });
    return id;
  }

  update(id: string, data: Partial<Task>): void {
    const task = this.tasks.get(id);
    if (task) this.tasks.set(id, { ...task, ...data });
  }

  delete(id: string): void {
    this.tasks.delete(id);
  }
}

// Undo/redo for database operations
class DatabaseCommand implements AsyncCommand {
  constructor(
    private db: Database,
    private operation: "insert" | "update" | "delete",
    private table: string,
    private data: Record<string, unknown>,
    private id?: string
  ) {}

  async execute(): Promise<string> {
    switch (this.operation) {
      case "insert":
        const result = await this.db.insert(this.table, this.data);
        this.id = result.id;
        return result.id;
      case "update":
        await this.db.update(this.table, this.id!, this.data);
        return this.id!;
      case "delete":
        await this.db.delete(this.table, this.id!);
        return this.id!;
    }
  }

  async undo(): Promise<void> {
    switch (this.operation) {
      case "insert":
        await this.db.delete(this.table, this.id!);
        break;
      case "update":
        // Would need to store previous data
        break;
      case "delete":
        await this.db.insert(this.table, this.data);
        break;
    }
  }

  describe(): string {
    return `${this.operation} on ${this.table}`;
  }
}
```

---

## Interview Questions

1. **What is the Command pattern?**
   A behavioral pattern that encapsulates a request as an object, allowing parameterization, queuing, and undo/redo.

2. **When would you use the Command pattern?**
   For undo/redo functionality, macro recording, command queues, and decoupling invocation from execution.

3. **What is a Macro command?**
   A composite command that executes multiple commands as a single unit.

4. **How do you implement undo/redo?**
   Keep a history stack of executed commands. Undo pops from history and calls undo(). Redo maintains a separate stack.

5. **What is the difference between Command and Strategy patterns?**
   Command encapsulates a request as an object. Strategy encapsulates an algorithm. Commands can be undone; strategies cannot.

6. **How do you handle async commands?**
   Use Promise-based execute/undo methods and manage the async lifecycle appropriately.

7. **What is the advantage of the Command pattern?**
   Decouples sender from receiver, enables undo/redo, allows command queuing, and supports macro recording.

8. **Can commands be serialized?**
   Yes, if their inputs are serializable. Useful for logging, auditing, and replay.

9. **How does the Command pattern relate to CQRS?**
   CQRS separates command and query responsibilities. Commands in CQRS are typically domain events that change state.

10. **What are real-world examples of the Command pattern?**
    Text editor undo/redo, transaction systems, task queues, GUI buttons, and macro recording.
