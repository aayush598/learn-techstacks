# Command Pattern

> **TL;DR**: The Command pattern encapsulates a **request as an object** — with `execute()` and (optionally) `undo()` — so requests can be queued, logged, retried, scheduled, undone, and made transactional; it exists because a direct method call cannot be *stored, delayed, or reversed*.

## 1. Why Does This Exist?
A plain method call (`editor.cut()`) is *ephemeral*: it happens now and vanishes. But real systems need requests to be **first-class things**:
- **Undo/redo**: an editor must reverse the last operation — a method call has no memory of what it did.
- **Queueing/scheduling**: a request must wait, be batched, retried, or run in a worker thread.
- **Logging/auditing**: every user action must be recorded (who did what, when) for replay or audit.
- **Transactionality**: a set of requests must commit together or roll back together.
- **Decoupling**: the *invoker* (button, menu, task) must not know the *receiver* (the object that does the work) or *what* the work is.

The Command pattern exists to turn "do this" into an **object** that can be stored (undo stack), passed (queues), logged, serialized, and replayed — the fundamental enabling pattern for undo/redo, job queues, macro recording, and transactional UIs. It decouples the object that *issues* the request from the object that *performs* it, and adds an undo/redo/replay capability that method calls structurally cannot have.

## 2. How Does It Work?
```
Invoker ──calls──> Command (interface: execute(), undo())
                        ▲
                    ConcreteCommand ──operates on──> Receiver
Client ──configures──> ConcreteCommand
```
Participants:
1. **Command** — the interface (`execute()`, optional `undo()`).
2. **ConcreteCommand** — binds the *receiver* and the *action* (holds a receiver reference + parameters; `execute()` calls the receiver's method).
3. **Receiver** — the object that actually does the work (the "how").
4. **Invoker** — the object that triggers the command (button, menu, worker, macro recorder); it knows only the Command interface.
5. **Client** — creates the ConcreteCommand and binds it to the receiver, then hands it to the invoker.

```java
interface Command { void execute(); void undo(); }

class Light {                                          // Receiver
    void on() { System.out.println("Light ON"); }
    void off() { System.out.println("Light OFF"); }
}
class LightOnCommand implements Command {              // ConcreteCommand
    private final Light light;
    LightOnCommand(Light l) { this.light = l; }
    public void execute() { light.on(); }
    public void undo() { light.off(); }                // reverse
}

class RemoteButton {                                   // Invoker — knows only Command
    private final Command command;
    RemoteButton(Command c) { this.command = c; }
    void press() { command.execute(); }
}
// Usage
Light l = new Light();
RemoteButton btn = new RemoteButton(new LightOnCommand(l));
btn.press();   // Light ON
```

## 3. When Is It Used?
- **Undo/redo systems**: editors, image tools, database transactions' reverse operations.
- **Task/job queues**: each queued item is a Command; workers `execute()` them (Runnable/Callable are commands).
- **Macro recording**: record a sequence of commands and replay them.
- **Menus/buttons/actions that must be configurable**: a toolbar button is an Invoker bound to a Command — remapping buttons doesn't change the button.
- **Transactional operations**: a sequence of commands with undo support (compensation).
- **Logging & replay**: audit trails of user actions (every command logged, replayable).
- **JDK/frameworks**: `Runnable`/`Callable`/`Supplier` (commands), Swing/AWT `Action` (a Command with GUI state), `javax.swing.Timer`, `ExecutorService.submit(runnable)` (queues commands), Spring's `TransactionTemplate`/`PlatformTransactionManager` (command-like), undo frameworks (`javax.swing.undo.UndoManager`).
- **Interviews**: "undo/redo", "queue requests", "decouple button from action", "macro recording" → Command.

## 4. Why Wasn't Another Approach Chosen?
- **Direct method call**: simplest, but ephemeral — cannot be stored (undo), queued, logged, or replayed. The entire value of Command is *reifying* the request. Rejected wherever requests must be first-class.
- **Callbacks (passing a function)**: valid for the simple case — a lambda `() -> light.on()` IS a Command (Runnable is a Command). Command *adds* the formal interface, `undo()`, and multi-step/multi-receiver support. For stateless single actions, lambdas suffice; for undo/redo and transactionality, a full Command object with state is needed.
- **Strategy pattern**: similar shape (interface + injected object), but Strategy *selects an algorithm to run now*; Command *reifies a request to be executed later/queued/undone*. Strategy is "how to do it"; Command is "what to do, deferred." A command *may* use a strategy internally.
- **Observer**: Observer pushes *state-change notifications*; Command *encapsulates requests*. Different intents (notification fan-out vs request reification).
- **Memento**: Memento captures *state* for restore; Command captures *operations* for execute/undo. They often combine (a Command stores a Memento to undo).
- **Hard-coding undo in the receiver**: receiver would need an undo method per operation — rejected because undo *policy* (stacking, batching, limits) belongs outside the receiver; Command gives it a natural home.

## 5. Intuition
A Command is a **meal ticket / work order / purchase order**. A customer doesn't tell the kitchen to cook directly (that would couple the customer to the cook). Instead they write a *work order* (a ticket): "grill 1 steak, 2 sides" — a *thing* that can be queued at the kitchen, executed by a cook, *reversed* (canceled) before cooking, logged, and re-run by another cook. The ticket is the command; the cook is the receiver; the expediter (who holds the ticket queue) is the invoker; the kitchen manager is the client. The ticket exists *as an object* — that's what the pattern provides.

## 6. Real-World Analogy
An **airline boarding pass / flight change**. The passenger (client) creates a *change request* (command): "move me to the 9am flight." That request is an object — it can be queued at the counter (invoker), executed by the reservation system (receiver), *undone* (revert to the original booking), logged (audit), and retried if the system hiccups. A direct "you move me now" isn't an object — it can't be undone or replayed. The boarding-pass swap request *is* the command, and its undo is the original booking.

## 7. Formal Definition
> **Command** (a.k.a. Action, Transaction): Encapsulate a request as an **object**, thereby letting you parameterize clients with different requests, **queue or log requests**, and support **undoable operations**. (GoF, p. 233)
>
> Participants: **Command** (interface), **ConcreteCommand** (binds receiver + action), **Receiver** (does the work), **Invoker** (triggers commands; knows only the interface), **Client** (creates commands, sets receiver). Key property: the invoker and the receiver are *decoupled* — the invoker has no idea what the command does.

## 8. Example
An **editor with undo/redo**:
```java
class TextEditor {                                    // Receiver
    private String text = "";
    void insert(String s) { text += s; }
    void deleteLast(int n) { text = text.substring(0, Math.max(0, text.length() - n)); }
    String getText() { return text; }
}
class InsertCommand implements Command {              // ConcreteCommand with undo state
    private final TextEditor editor;
    private final String inserted;
    InsertCommand(TextEditor e, String s) { editor = e; inserted = s; }
    public void execute() { editor.insert(inserted); }
    public void undo() { editor.deleteLast(inserted.length()); }   // reverse
}
class EditorInvoker {                                 // Invoker
    private final Deque<Command> undoStack = new ArrayDeque<>();
    private final Deque<Command> redoStack = new ArrayDeque<>();
    void run(Command c) { c.execute(); undoStack.push(c); redoStack.clear(); }
    void undo() {
        if (undoStack.isEmpty()) return;
        Command c = undoStack.pop();
        c.undo();
        redoStack.push(c);
    }
    void redo() {
        if (redoStack.isEmpty()) return;
        Command c = redoStack.pop();
        c.execute();
        undoStack.push(c);
    }
}
// Usage
TextEditor ed = new TextEditor();
EditorInvoker inv = new EditorInvoker();
inv.run(new InsertCommand(ed, "Hello "));
inv.run(new InsertCommand(ed, "World"));
System.out.println(ed.getText());   // "Hello World"
inv.undo();                          // removes "World"
inv.undo();                          // removes "Hello "
System.out.println(ed.getText());    // ""
inv.redo();                          // re-applies "Hello "
System.out.println(ed.getText());    // "Hello "
```
- Two stacks (undo/redo), commands pushed/popped, each command knows how to reverse itself. Direct method calls could never do this.

## 9. Internal Working
1. **Client** constructs a ConcreteCommand, wiring it to the *receiver* and the *action parameters* (`new InsertCommand(editor, "World")`).
2. The command is handed to an **Invoker** (button, menu, queue, macro recorder, undo manager).
3. When triggered, the invoker calls `command.execute()` — the command invokes the receiver's method(s).
4. **Undo support**: the invoker (or a stack) pushes executed commands onto an undo stack; `undo()` pops and calls `command.undo()` (the command reverses the receiver's state — either by inverse operation or by restoring a Memento snapshot), pushing it onto a redo stack; `redo()` re-executes.
5. **Queueing/logging**: the invoker may hold commands in a queue (executed by workers) or serialize them to a log (replay = re-execute).
6. The invoker never knows the receiver — decoupling is total: the same button can be rebound to any command.

**Why undo works**: each ConcreteCommand *captures the delta* (what was inserted, the previous state) — that's the state a plain method call discards. This is the essence of reifying requests.

## 10. Time Complexity
- **execute()**: O(1) dispatch + the receiver's operation cost.
- **undo()**: O(1) dispatch + the inverse operation (restoring a Memento can be O(S) for state size S).
- **Stack operations**: push/pop O(1); unbounded undo depth → O(K) memory for K commands.
- **Queue-based invokers**: enqueue/dequeue O(1); batch execution O(N) for N commands.
- **Macro recording**: recording is O(1) per command append; replay is O(N).
- **No algorithmic change** — Command adds constant-factor dispatch; its value is *capability* (undo, queue, log), not speed.

## 11. Advantages
- **Undo/redo**: commands carry the inverse operation — the pattern's signature win.
- **Decoupling**: invokers (buttons, queues) know only the Command interface; receivers are interchangeable.
- **Queueing/scheduling**: requests become objects you can store, delay, batch, retry.
- **Logging & replay**: serialize commands to an audit log; replay for testing/recovery.
- **Macros/scripts**: record and replay command sequences.
- **Transactional semantics**: a sequence of commands can commit/rollback via their undos (compensation).
- **Open-Closed**: new operations = new command classes; invoker and receiver unchanged.
- **Lambda-friendly**: `Runnable`/`Supplier` give the pattern in one line for simple cases.

## 12. Disadvantages
- **Class proliferation**: one class per operation (Insert, Delete, Format, Spellcheck...) — many small classes.
- **Overhead of capturing state**: each command must store enough to execute *and* undo (memory + design care).
- **Undo fidelity is hard**: making `undo()` truly exact (especially for complex, non-invertible operations like formatting or I/O) is difficult — some operations can't be cleanly undone.
- **Invoker/command plumbing**: wiring commands into invokers adds indirection for trivial actions.
- **Can hide business logic**: everything becomes "a command" and the receiver becomes a thin facade — a design smell if overused.

## 13. Interview Questions
1. **Q: What is the Command pattern?** A: Encapsulate a request as an object (with `execute()` and optional `undo()`), decoupling the invoker from the receiver and enabling queueing, logging, and undo/redo.
2. **Q: What problem does it solve?** A: A method call is ephemeral — it can't be stored, queued, undone, or replayed. Command *reifies* the request, enabling undo stacks, job queues, macros, logging, and transaction-like semantics.
3. **Q: How does Command enable undo?** A: Each ConcreteCommand captures the *inverse operation* (or a state snapshot), so the undo stack can reverse each executed command; a redo stack re-executes. The delta is stored in the command object — exactly what a direct call discards.
4. **Q: Command vs Strategy? (Tricky)** A: Both inject an object behind an interface. Strategy *selects an algorithm to run now* (behavioral choice); Command *reifies a request to execute later* (deferred/queued/undone). A command can internally use a strategy; but the intents differ — "how" vs "what, deferred."
5. **Q: Command vs Observer?** A: Observer pushes *state-change notifications* (1→N); Command encapsulates *requests* (1→1 execution with undo). Notifications vs operations.
6. **Q: Is a `Runnable` a Command?** A: Yes — `Runnable.run()` is `execute()`; `ExecutorService.submit(runnable)` queues commands executed by a worker thread. `Callable<T>` adds a result; `Supplier` is a value-returning command. The JDK's task/thread APIs *are* the Command pattern.
7. **Q: What are the participants?** A: Command (interface), ConcreteCommand (binds receiver + action + undo data), Receiver (does the work), Invoker (triggers; knows only the interface), Client (creates/wires commands).
8. **Q: How do you implement undo when an operation isn't naturally invertible? (Production)** A: Two strategies: (1) *inverse operation* (insert/delete) when clean; (2) *Memento* — the command snapshots the receiver's state before executing and restores it on undo (O(S) memory per command but exact). The Command + Memento combination is the standard undo design.
9. **Q: What are the two undo-stack invariants?** A: (1) On a new command, push to undo stack and *clear the redo stack* (new actions invalidate redo history); (2) undo pops and pushes to redo; redo pops and re-executes. Getting the "clear redo on new action" right is the classic bug.
10. **Q: How does Command help macro recording?** A: A recorder (a special invoker) appends every executed command to a list instead of (or in addition to) executing it; replay re-executes the list. The commands *are* the macro.
11. **Q: How does Swing/AWT use Command?** A: `javax.swing.Action` is a Command with GUI state (name, icon, enabled) — a button/menu item is an Invoker bound to an Action; rebinding actions to different UI elements is trivial. `javax.swing.undo.UndoManager` implements the undo/redo stacks.
12. **Q: Where does Spring use command-like abstractions?** A: `TransactionTemplate` (execute a transaction command with rollback rules), `PlatformTransactionManager` (`TransactionCallback` — a command executed within a transaction), `RestTemplate`/`JdbcTemplate` callbacks (`StatementCallback`, `ResultSetExtractor` are commands executed by the template). Callback-based templates ARE command-flavored.
13. **Q: Command + Memento — describe the combined pattern. (Scenario)** A: For non-invertible ops: before executing, the command asks the receiver for a Memento (state snapshot); on undo, it restores that Memento. The undo stack holds commands, each carrying a snapshot. This gives *exact* undo at the cost of memory.
14. **Q: When would you NOT use Command? (Production)** A: For trivial, synchronous, non-reversible single actions — a direct call or lambda is clearer. Command earns its weight when requests must be queued, logged, undone, or parameterized across an interface.
15. **Q: How does Command support transactionality?** A: A "transaction" = a list of commands; commit = execute all; rollback = execute all undos in reverse. This "compensating action" model is the foundation of sagas and distributed transactions (each step is a command with a compensation).
16. **Q: What is a "command with priority" (for scheduling)?** A: An invoker queue that orders commands by a priority field (e.g., `PriorityQueue<Command>`) — request reification makes prioritization trivial because the request is a comparable object. Direct calls can't be prioritized.
17. **Q: How do you log commands for replay/audit? (Production)** A: Make commands *serializable* (store receiver, params, timestamp); write them to an event log (Kafka, DB); replay = read the log and execute each command against a fresh receiver state. This is event-sourcing in miniature — commands-as-log.
18. **Q: What's the difference between the Command and the Receiver?** A: The Receiver contains the *actual logic* (how); the Command contains the *request* (what + who + undo data) and delegates to the receiver. Splitting them keeps the receiver reusable and the command decoupled from the invoker.
19. **Q: Can a single command do multiple receiver calls?** A: Yes — a command's `execute()` can orchestrate several receiver operations (e.g., "placeOrder" = reserve stock + charge + ship). That's a *composite command*; the invoker still sees one Command. This is why commands are great facades over workflows.
20. **Q: Design a remote-controlled device system with undo and macros. (Scenario)** A: `Command` interface with `execute()`/`undo()`; receivers `Light`, `Fan`, `TV`; commands `LightOnCommand`, `FanSpeedCommand`, `TVOnCommand`; an `Invoker` with undo/redo stacks + a `MacroCommand` that holds a list of commands (execute all, undo in reverse). Buttons bind to commands; a "movie night" macro = a list of commands. Full answer: participants + two stacks + composite macro.

## 14. Follow-Up Questions
1. **Q: What is the relationship between Command and the "Saga" pattern in distributed systems?** A: A saga is a sequence of steps, each a command with a *compensating* command; on failure, compensating commands run in reverse to roll back. Command reification (storing requests + inverses) is precisely what makes sagas implementable.
2. **Q: What is "command vs callback"?** A: A callback is a lightweight command (a function to call); the Command *pattern* adds the formal interface, undo semantics, state capture, and multi-receiver orchestration. For simple, stateless actions, callbacks/lambdas are commands without ceremony.
3. **Q: What is the "transactional undo" problem?** A: Undoing multiple commands must be atomic — if undoing command 2 of 3 fails, you're in an inconsistent state. Solution: undo in reverse with compensation and a failure policy (log and stop, or force-restore via mementos). Interviewers probe "what if undo itself fails?"
4. **Q: How does the Command pattern interact with serialization for distributed execution?** A: Commands with serializable parameters can be shipped to remote workers (queue + execute). This is how task queues (Sidekiq, Celery, Kafka tasks) work — the task payload IS a serialized command. Also enables *exactly-once* replay semantics.
5. **Q: What's the difference between a "pure" GoF Command and a "smart" Command?** A: GoF's command is *dumb* (delegates to a receiver); a "smart" command performs the logic itself (no separate receiver). Smart commands are simpler but couple the command to domain logic; pure commands keep the receiver reusable. Both are valid; interviewers may ask which you'd choose and why.

## 15. Coding Example
```java
// Full undo/redo editor with composite macro command
import java.util.*;

interface Command { void execute(); void undo(); }

class Buffer {                                   // Receiver
    private String text = "";
    void insert(String s) { text += s; }
    void delete(int n) { text = text.substring(0, Math.max(0, text.length() - n)); }
    String get() { return text; }
}

class InsertTextCommand implements Command {
    private final Buffer buf; private final String text;
    InsertTextCommand(Buffer b, String t) { buf = b; text = t; }
    public void execute() { buf.insert(text); }
    public void undo() { buf.delete(text.length()); }
}

class MacroCommand implements Command {          // Composite command
    private final List<Command> commands;
    MacroCommand(List<Command> cs) { commands = cs; }
    public void execute() { commands.forEach(Command::execute); }
    public void undo() {
        List<Command> rev = new ArrayList<>(commands);
        Collections.reverse(rev);
        rev.forEach(Command::undo);              // undo in reverse order
    }
}

class UndoManager {                              // Invoker
    private final Deque<Command> undo = new ArrayDeque<>();
    private final Deque<Command> redo = new ArrayDeque<>();
    void execute(Command c) { c.execute(); undo.push(c); redo.clear(); }
    void undo() { if (!undo.isEmpty()) { Command c = undo.pop(); c.undo(); redo.push(c); } }
    void redo() { if (!redo.isEmpty()) { Command c = redo.pop(); c.execute(); undo.push(c); } }
}

public class Main {
    public static void main(String[] args) {
        Buffer buf = new Buffer();
        UndoManager um = new UndoManager();
        um.execute(new InsertTextCommand(buf, "Hello "));
        um.execute(new MacroCommand(List.of(
                new InsertTextCommand(buf, "Java "),
                new InsertTextCommand(buf, "World"))));
        System.out.println(buf.get());           // "Hello Java World"
        um.undo();                                // undoes the macro (2 steps)
        System.out.println(buf.get());            // "Hello "
        um.undo();                                // "Hello " → ""
        um.redo();
        System.out.println(buf.get());            // "Hello "
    }
}
```
```python
# Python Command
class Light:
    def on(self): print("Light ON")
    def off(self): print("Light OFF")

class LightOnCommand:
    def __init__(self, light): self.light = light
    def execute(self): self.light.on()
    def undo(self): self.light.off()

class RemoteInvoker:
    def __init__(self): self.stack = []
    def press(self, cmd):
        cmd.execute(); self.stack.append(cmd)
    def undo(self):
        if self.stack: self.stack.pop().undo()

light = Light()
inv = RemoteInvoker()
inv.press(LightOnCommand(light))   # Light ON
inv.undo()                          # Light OFF
```
```cpp
// C++ Command
#include <iostream>
#include <memory>
#include <vector>

struct Command { virtual ~Command() = default; virtual void execute() = 0; virtual void undo() = 0; };
class Buffer { std::string text_; public:
    void insert(const std::string& s) { text_ += s; }
    void removeLast(size_t n) { text_ = text_.substr(0, text_.size() > n ? text_.size() - n : 0); }
    const std::string& get() const { return text_; }
};
class InsertCommand : public Command {
    Buffer& buf_; std::string text_;
public:
    InsertCommand(Buffer& b, std::string t) : buf_(b), text_(std::move(t)) {}
    void execute() override { buf_.insert(text_); }
    void undo() override { buf_.removeLast(text_.size()); }
};
// int main(){ Buffer b; InsertCommand c(b, "hi"); c.execute(); c.undo(); }
```

## 16. Industry Usage
- **JDK**: `Runnable`/`Callable`/`Supplier` (commands), `ExecutorService` (command queue), `javax.swing.Action` (command with GUI state), `javax.swing.undo.UndoManager` (undo/redo), `javax.swing.Timer` (delayed command).
- **Spring**: `TransactionTemplate`/`TransactionCallback` (transaction commands), `JdbcTemplate` callbacks, `RestTemplate` callbacks — callback-as-command.
- **Task queues/jobs**: Celery, Sidekiq, BullMQ, AWS SQS consumers — each job is a serialized command executed by workers; retries = re-execution.
- **Event sourcing / CQRS**: commands are the write-side requests; the event log stores the results — Command reification is foundational.
- **UI frameworks**: menu/button/action systems in Swing, Qt (`QAction`), Android (`MenuItem` with actions), VSCode/Atom command palettes (all editor commands are reified for undo + palette execution).
- **Games**: input buffering (a queue of commands per frame), replay systems, scripting.
- **Distributed transactions**: Sagas and compensation patterns — each step a command with a compensating command.
- **Interviews**: "undo/redo editor", "queue + workers", "macro", "how does `Runnable` relate to Command", "command palette" — a top behavioral-pattern question.

## 17. References
- **Gamma et al., *Design Patterns* — "Command" (p. 233)**: canonical definition, undoable commands, macro commands.
- **Oracle Docs: `java.util.concurrent.Runnable`/`Callable`, `javax.swing.Action`, `javax.swing.undo.UndoManager`, `ExecutorService`** — https://docs.oracle.com/javase/8/docs/api/
- **Spring Framework Docs: `TransactionTemplate`, `TransactionCallback`** — https://docs.spring.io/spring-framework/reference/
- **Martin Fowler — "Command pattern" (martinfowler.com) and Event Sourcing docs** — command reification in enterprise systems.
- **Chris Richardson, "Saga" pattern (microservices.io)** — command+compensation in distributed transactions.
- **refactoring.guru — "Command"** — modern diagrams and Java/C++/Python examples.
- **Head First Design Patterns — "Command" chapter** — the remote-control worked example with undo.

## 18. Cheat Sheet
- Command = **encapsulate a request as an object** — `execute()` + `undo()`, stored/queued/logged/replayed.
- Participants: Command (interface), ConcreteCommand (receiver + action + undo data), Receiver (work), Invoker (triggers), Client (wires).
- **Undo**: undo stack + redo stack; new command clears redo; undo pops→undo→push to redo; redo re-executes.
- Command vs Strategy: Strategy selects an algorithm now; Command defers/reifies a request.
- `Runnable`/`Callable`/`Supplier` + `ExecutorService` = Command in the JDK.
- Undo implementation: inverse operation OR Memento snapshot (exact but O(S) memory).
- Macros = composite commands (execute all; undo in reverse).
- Sagas/compensation = commands + compensating commands (distributed undo).
- Swing `Action`/`UndoManager`, Spring `TransactionTemplate`, task queues = production Commands.
- Use when requests must be stored/deferred/undone; skip for trivial synchronous actions.

## 19. Quiz
1. Command encapsulates: a) an algorithm b) a request as an object c) a state d) an interface → **b**
2. Which capability does Command uniquely enable? a) faster calls b) undo/redo and queueing c) inheritance d) caching → **b**
3. On a new command, the redo stack should be: a) kept b) cleared c) copied d) reversed → **b**
4. `Runnable` in `ExecutorService.submit()` is a: a) Strategy b) Command c) Observer d) Memento → **b**
5. Command vs Strategy: a) command selects algorithms b) strategy reifies requests c) strategy selects an algorithm; command defers/reifies a request d) identical → **c**
6. `javax.swing.undo.UndoManager` implements: a) the observer list b) undo/redo stacks c) command queue d) strategy selection → **b**
7. A MacroCommand executes: a) one command b) a list of commands c) nothing d) a strategy → **b**
8. Undo can be implemented by: a) inverse operation OR memento b) only inverse c) only memento d) logging → **a**
9. In event sourcing, the ___ side is commands; the log stores ___. a) write; results b) read; commands c) both d) neither → **a**
10. When is Command overkill? a) undo needed b) jobs to queue c) trivial synchronous non-reversible call d) macros → **c**

## 20. Flashcards
- **Q: Command intent?** → **A:** Encapsulate a request as an object — queueable, loggable, undoable.
- **Q: Participants?** → **A:** Command, ConcreteCommand, Receiver, Invoker, Client.
- **Q: How does undo work?** → **A:** Undo+redo stacks; commands carry the inverse (or a memento); new command clears redo.
- **Q: Command vs Strategy?** → **A:** Strategy selects an algorithm now; Command defers/reifies a request.
- **Q: JDK command examples?** → **A:** `Runnable`/`Callable`/`Supplier`, `ExecutorService`, Swing `Action`/`UndoManager`.
- **Q: How to undo non-invertible ops?** → **A:** Memento snapshot (exact, O(S) memory) or compensation.
- **Q: Macros?** → **A:** Composite command — list of commands; execute all, undo in reverse.
- **Q: Distributed undo?** → **A:** Sagas — commands with compensating commands, run in reverse on failure.

## 21. Revision
Command **encapsulates a request as an object** (`execute()` + `undo()`), turning ephemeral method calls into storable, queueable, loggable, replayable first-class things. It exists because direct calls can't be undone, queued, or audited. Participants: Command (interface), ConcreteCommand (binds receiver + action + undo data), Receiver (the work), Invoker (triggers — knows only the interface), Client (wires). Signature capability: **undo/redo** via two stacks (new command clears redo; undo pops → calls undo() → pushes to redo), implemented by inverse operations or **Memento** snapshots for non-invertible ops. Discriminate: Strategy selects an algorithm now; Command defers/reifies a request. `Runnable`/`Callable`/`Supplier` + `ExecutorService`, Swing `Action`/`UndoManager`, Spring `TransactionTemplate` are production Commands. Macros = composite commands (undo in reverse); sagas = commands + compensations for distributed rollback; event sourcing stores command results as events. Interview hook: "undo/redo editor", "queue + workers", "macro recording" → Command.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is the Command pattern?" | 2 How / 7 Formal Definition |
| "How does Command enable undo?" | 13 Q3 / 13 Q9 / 15 Coding |
| "Command vs Strategy?" | 13 Q4 / 18 Cheat Sheet |
| "Is a Runnable a Command?" | 13 Q6 / 16 Industry Usage |
| "Participants?" | 13 Q7 / 2 How |
| "Undo for non-invertible operations?" | 13 Q8 / 14 Q3 / 15 Coding |
| "Macros / composite commands?" | 13 Q10 / 13 Q19 |
| "Where does Spring use commands?" | 13 Q12 / 16 Industry Usage |
| "Commands + sagas in distributed systems?" | 14 Q1 / 16 Industry Usage |
| "Design an undo/redo editor (scenario)." | 13 Q20 / 15 Coding |
