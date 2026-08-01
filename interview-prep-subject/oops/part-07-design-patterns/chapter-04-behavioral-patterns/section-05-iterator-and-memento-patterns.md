# Iterator and Memento Patterns

> **TL;DR**: The **Iterator** pattern provides a way to **traverse a collection's elements without exposing its internal structure** (O(1) `next()`, `hasNext()`), and the **Memento** pattern **captures and restores an object's internal state** (a snapshot for undo/rollback) without violating encapsulation — Iterator exists to decouple traversal from the collection, Memento to snapshot state without exposing internals.

## 1. Why Does This Exist?
**Iterator** exists because "walk through the elements" is *not* a property of any one data structure — but *how* you walk differs per structure (array index, linked-list next-pointer, tree DFS, hash-map bucket scan). If every client wrote its own traversal, every client would depend on the collection's internals (exposed `Node`, index arithmetic, bucket arrays), and changing the structure would break every loop. The Iterator pattern **decouples traversal from representation**: the collection returns an *Iterator* (a separate object with a uniform `next()`/`hasNext()` interface), and clients traverse *any* collection with the *same* code. The internals stay hidden (encapsulation preserved), the traversal logic is reusable (the same iterator protocol serves lists, sets, trees, streams), and the collection can change its guts without breaking clients.

**Memento** exists because "undo/rollback" needs a *snapshot* of an object's state — but exposing the state (getters/setters for everything) violates encapsulation and creates a huge coupling surface. The Memento pattern has the *originator* produce an opaque **Memento** object (a black box even to the *caretaker* that stores it) and restore itself from it later: the caretaker (undo manager) holds mementos *without ever seeing inside them*. State can be snapshotted and restored with zero access to internals — enabling undo, save/restore, and transactional rollback while keeping the originator's fields private.

## 2. How Does It Work?
**Iterator:**
```
Client ──traverses──> Iterator (interface: hasNext(), next())
                            ▲
                        ConcreteIterator (wraps a cursor over the collection)
Collection ──creates──> iterator()
```
- `Iterable` (JDK): a collection returns an `Iterator` from `iterator()`.
- The iterator holds the *traversal state* (current position/cursor); `hasNext()` checks more elements; `next()` advances and returns the element.
- Each collection supplies its own `ConcreteIterator`; clients use the interface only.

**Memento:**
```
Originator ──creates──> Memento (opaque state snapshot; wide interface only for Originator)
     ▲                         │
     │ restore(memento)        │ stored by
     └─────────────────────────┘
                      Caretaker (holds Mementos; never inspects them)
```
- **Originator** (the object with state) creates a Memento capturing its state; later calls `restore(memento)`.
- **Memento** stores the snapshot; its *narrow interface* (visible to the caretaker) is opaque; only the Originator can see inside (wide interface — via package-private access or a `restoreFrom(memento)` method).
- **Caretaker** (undo manager, save system) holds Mementos and triggers create/restore but never reads them.

```java
class TextEditor {                          // Originator
    private String text;
    public Memento save() { return new Memento(text); }
    public void restore(Memento m) { this.text = m.getSavedText(); }
    public static class Memento {           // opaque to the caretaker
        private final String savedText;
        private Memento(String t) { savedText = t; }
        private String getSavedText() { return savedText; }   // visible only via originator's restore
    }
}
// Caretaker:
Deque<TextEditor.Memento> history = new ArrayDeque<>();
history.push(editor.save());      // snapshot (caretaker can't see inside)
editor.restore(history.pop());    // restore
```

## 3. When Is It Used?
- **Iterator**: for-each loops over any collection (Java `Iterable`/`Iterator`), streams (`Stream.iterator()`), custom data structures that must offer standard traversal, database cursors, tree/graph traversal APIs.
- **Memento**: undo/redo (the caretaker = undo manager holding snapshots), save/load systems (a save file is a memento), transaction rollback (capture state before a transaction; restore on failure), checkpointing, wizards ("back" button restores prior screen state).
- **Interviews**: "traverse a custom collection", "why can't clients iterate directly?", "undo/restore state without exposing internals" → Iterator / Memento.

## 4. Why Wasn't Another Approach Chosen?
**For Iterator:**
- **Expose the internal structure (public `Node`, index arithmetic)**: rejected — clients couple to internals, the structure can't evolve, and traversal logic is duplicated everywhere (a maintenance and bug mine).
- **Make the collection itself movable (index getters/setters on the collection)**: rejected — a *single* cursor on the collection breaks with nested/concurrent traversal (two loops can't share one cursor). The iterator *owns a private cursor*, so multiple iterators can traverse the same collection independently.
- **Client-side functional composition (map/filter/forEach on the collection)**: modern and preferred for *in-place processing* — but iterator remains the *primitive* under streams (`Stream.iterator()`), and it's the only way to write *custom* traversals (skip, reverse, break early) without materializing everything.
- **Copy the collection for traversal**: rejected — O(N) memory and time per traversal; breaks the "lazy, one-element-at-a-time" model needed for huge/streaming data.
- **A global traversal utility with type switches**: rejected — Open-Closed violation and duplicate per-type logic; the iterator pattern *embeds* traversal in the collection where it belongs.
- **Generators (Python `yield`, C# `yield`, Java 19+ no direct)**: the *language-level* iterator — a generator function `yield`s values with the iterator protocol built in. Chosen where available; the Java `Iterator` interface is the pattern's canonical form.

**For Memento:**
- **Public getters/setters for all state**: rejected — destroys encapsulation (any caller can read/change internals) and makes every future state change a breaking API change. Memento keeps the snapshot opaque.
- **Serialization (write state to bytes/JSON for restore)**: a valid snapshot mechanism — chosen when the snapshot must survive processes/reboots (save files, checkpoints). Rejected for in-memory undo because it's slow (reflection, allocation) and couples to serializable types.
- **Command pattern alone (inverse operations)**: for *invertible* operations, commands with inverse methods are cheaper than snapshots (O(1) vs O(S)). Memento is chosen when operations aren't naturally invertible or when you want a uniform snapshot mechanism. The two often combine (a command stores a memento for its undo).
- **Copy the whole object graph**: that's effectively a deep-copy memento — fine for small objects, wasteful for large ones; memento can capture *only the delta* or a compact representation.
- **Keeping snapshots inside the originator**: rejected — mixes snapshot *policy* (how many, eviction) with the originator's state; the caretaker owns that policy.

## 5. Intuition
**Iterator intuition**: a **bookmark / page marker**. "Read the book" (traverse) doesn't require the reader to know the book's binding, spine, or print machinery. The bookmark (iterator) remembers *where you are* and lets you take *one step at a time* — and multiple bookmarks can mark the same book independently (two loops, two iterators). The book (collection) can change its binding (internal structure) without breaking the reader's habit of "next page, is there a next page?".

**Memento intuition**: a **save-game / photocopy of a chess position**. To "undo," you don't rewrite the game rules; you take a *photograph* of the current board (memento), and to undo you just put the photograph back. The photograph is opaque — the undo manager (caretaker) doesn't understand chess; it only *stores and returns* the photos. The chess engine (originator) is the only one who can read a photo and restore the board from it. Opaque snapshot = state saved with no leakage of internals.

## 6. Real-World Analogy
- **Iterator**: a **music playlist's "next track" button** and the **TV remote's channel button**. You press "next" — you don't care whether the player uses an array, a linked list, or a database of tracks; the player hands you one track at a time through a uniform "next" protocol. And two listeners with two remotes (two iterators) on the same playlist can traverse independently.
- **Memento**: a **time machine / camera in a board game**. You photograph the board state (memento). The photo is just a picture — the referee (caretaker) can store and hand you photos but can't tell a checkmate from a stalemate; only the players (originator) know how to read the photo and rebuild the board exactly.

## 7. Formal Definition
> **Iterator**: Provide a way to **access the elements of an aggregate object sequentially without exposing its underlying representation**. (GoF, p. 257)
>
> **Memento** (a.k.a. Token): Without violating encapsulation, **capture and externalize an object's internal state** so that the object can be **restored to this state later**. (GoF, p. 283)
>
> Participants (Iterator): **Iterator** (interface), **ConcreteIterator** (traversal cursor), **Aggregate/Collection** (creates iterators), **ConcreteAggregate**. Participants (Memento): **Originator** (creates/restores mementos), **Memento** (opaque snapshot), **Caretaker** (stores mementos, never inspects).

## 8. Example
**Iterator — a custom `LinkedList` offering the standard protocol:**
```java
interface Iterator<T> { boolean hasNext(); T next(); }
interface IterableCollection<T> { Iterator<T> iterator(); }

class Node<T> { T data; Node<T> next; Node(T d){ data=d; } }

class LinkedList<T> implements IterableCollection<T> {
    private Node<T> head;
    void add(T d) { Node<T> n = new Node<>(d); n.next = head; head = n; }

    public Iterator<T> iterator() { return new ListIterator(); }
    private class ListIterator implements Iterator<T> {     // ConcreteIterator — private cursor
        private Node<T> cur = head;
        public boolean hasNext() { return cur != null; }
        public T next() { T d = cur.data; cur = cur.next; return d; }
    }
}
// Client — uniform traversal, zero knowledge of Node/linked structure:
IterableCollection<String> list = new LinkedList<>();
list.add("a"); list.add("b"); list.add("c");
Iterator<String> it = list.iterator();
while (it.hasNext()) System.out.println(it.next());   // c, b, a
```
- The client never touches `Node`; two iterators can traverse concurrently (independent cursors); changing to an array-backed structure keeps the client identical.

**Memento — an editor's undo history:**
```java
class TextBuffer {                              // Originator
    private String text = "";
    void append(String s) { text += s; }
    void deleteLast(int n) { text = text.substring(0, Math.max(0, text.length() - n)); }
    Snapshot save() { return new Snapshot(text); }
    void restore(Snapshot s) { this.text = s.content; }
    static class Snapshot {                     // Memento — opaque
        private final String content;
        private Snapshot(String c) { content = c; }
    }
}
class History {                                 // Caretaker
    private final Deque<TextBuffer.Snapshot> stack = new ArrayDeque<>();
    void push(TextBuffer b) { stack.push(b.save()); }
    void undo(TextBuffer b) { if (!stack.isEmpty()) b.restore(stack.pop()); }
}
// Usage
TextBuffer buf = new TextBuffer();
History h = new History();
h.push(buf); buf.append("Hello ");              // snapshot of "" 
h.push(buf); buf.append("World");               // snapshot of "Hello "
h.undo(buf); System.out.println(buf); // "Hello " (restored)
h.undo(buf); System.out.println(buf); // ""       (restored)
// The History never saw buf's internals — only opaque snapshots.
```
- Undo happens with *no* access to `text` from outside — the caretaker holds opaque tokens.

## 9. Internal Working
**Iterator internal working:**
1. Client calls `collection.iterator()`, which returns a fresh `ConcreteIterator` holding a *private cursor* initialized to the first position.
2. The client calls `hasNext()` → the iterator inspects its cursor (O(1)) and reports more elements.
3. `next()` (a) reads the current element, (b) advances the cursor, (c) returns the element. O(1) amortized.
4. Multiple iterators = multiple independent cursors over the same collection — concurrent traversal is safe (as long as the collection itself isn't structurally modified).
5. **Fail-fast (JDK)**: `ArrayList`'s iterator tracks a `modCount`; if the collection is structurally modified during iteration, `next()` throws `ConcurrentModificationException` — protecting against subtle corruption.
6. The interface is all the client needs — traversal *strategy* (index walk, pointer walk, DFS) is buried in the concrete iterator.

**Memento internal working:**
1. The caretaker requests a snapshot: `originator.save()`.
2. The originator constructs a Memento holding its internal state (a private-copy/immutable value) and returns it — the caretaker holds an *opaque token* (can't read fields).
3. Later, the caretaker hands the token back: `originator.restore(memento)`.
4. The originator extracts the state (the wide/private interface — e.g., a private method visible through the originator's own code) and re-applies it, replacing its fields.
5. Encapsulation holds: *no other class ever reads the memento's content*. The narrow interface (opaque object) is all the caretaker sees; the wide interface (state access) is visible only to the originator (package-private nested class in Java).
6. Policy (how many snapshots, eviction, disk persistence) lives in the caretaker.

## 10. Time Complexity
**Iterator:**
- `hasNext()`: **O(1)**.
- `next()`: **O(1)** amortized (advance a cursor; for a tree iterator, O(1) amortized with a stack).
- Creating an iterator: O(1).
- Full traversal of N elements: **O(N)** — each element visited exactly once, total cost = N × O(1).
- Memory: O(1) per iterator (a cursor) or O(depth) for tree iterators.
**Memento:**
- `save()`: **O(S)** where S = size of the captured state (copies the snapshot).
- `restore()`: O(S) (re-applies the snapshot).
- Undo history: O(K × S) memory for K snapshots.
- vs Command-undo (O(1) per inverse): Memento is more expensive but works for non-invertible operations — the classic trade-off.

## 11. Advantages
**Iterator:**
- **Encapsulation**: traversal never exposes collection internals (private nodes, indexes).
- **Uniform protocol**: one interface traverses lists, sets, maps, trees, streams — client code is structure-agnostic.
- **Independent traversal**: multiple iterators over the same collection (separate cursors).
- **Lazy/streaming**: one element at a time — enables huge/streaming data.
- **Fail-fast safety** (JDK): catches structural modification during traversal.
- **Extensible**: new collections implement the same protocol (Open-Closed for traversal).
**Memento:**
- **Undo/rollback**: state snapshots enable undo without inverse-operation logic.
- **Encapsulation preserved**: snapshots are opaque; internals never leak.
- **Uniform undo mechanism**: works for any state, invertible or not.
- **Caretaker policy separation**: snapshot policy (how many, when) lives outside the originator.
- **Supports persistence**: snapshots can be serialized (save files, checkpoints).

## 12. Disadvantages
**Iterator:**
- **External iteration is explicit**: clients must manage the loop (`hasNext`/`next`) — more verbose than internal iteration (for-each/streams), which the JDK's enhanced `for` and streams hide.
- **Not always O(1)**: some iterators (sorted/tree) are O(log n) or amortized; and skip/remove operations complicate the contract.
- **Fail-fast is best-effort**: `ConcurrentModificationException` is a *heuristic* (modCount); truly concurrent-safe iteration needs concurrent collections, not iterators.
- **Interface rigidity**: the classic `Iterator` can't do reverse/skip without extra methods (bidirectional iterators are a separate concept).
**Memento:**
- **Memory cost**: O(S) per snapshot — deep state or long histories are expensive (mitigate with deltas/compression).
- **Full-state capture**: every snapshot copies the whole state even when only a small part changed (delta mementos mitigate but are complex).
- **Encapsulation strain**: the originator must trust the caretaker to *not* inspect the opaque token (in Java, reflection can break the "opaque" guarantee).
- **Stale/expensive**: if the state is huge or the originator changes shape, mementos break silently (incompatible snapshots).

## 13. Interview Questions
1. **Q: What is the Iterator pattern?** A: Provide sequential access to an aggregate's elements without exposing its internal representation — the collection returns an `Iterator` (cursor) with a uniform `hasNext()`/`next()` protocol.
2. **Q: What problem does it solve?** A: Clients would otherwise couple to collection internals (public nodes, index arithmetic) and duplicate traversal logic per structure. Iterator decouples traversal from representation and gives one uniform protocol.
3. **Q: Why can't the collection itself be the cursor? (Tricky)** A: A single cursor on the collection breaks *nested/concurrent* traversal (two loops can't share one position). Each iterator owns an independent private cursor, so many traversals coexist.
4. **Q: What's the time complexity of `hasNext()`/`next()`?** A: O(1) for most iterators (advance a cursor); full traversal is O(N). Tree/sorted iterators are O(1) amortized with an internal stack (O(depth) memory).
5. **Q: What is fail-fast iteration? (Production)** A: JDK collections track a `modCount`; structural modification during iteration triggers `ConcurrentModificationException` in `next()`. It's a *safety heuristic*, not a correctness guarantee — for real concurrent use, use concurrent collections (`ConcurrentHashMap` — weakly consistent iterators).
6. **Q: How do Java for-each and streams relate to Iterator?** A: Enhanced `for (X x : coll)` is *compiled into* `iterator()` + `hasNext()` + `next()`. Streams use spliterators (a parallel-aware iterator variant). The pattern is the primitive underneath both.
7. **Q: Can you implement an iterator for a binary tree? What's the traversal order and memory?** A: An in-order iterator: an explicit stack of nodes; `next()` pops, then pushes the node's right subtree's left spine — O(1) amortized per next, O(depth) stack memory. Using a stack instead of recursion avoids stack overflow on deep trees.
8. **Q: Iterator vs a client-side stream/forEach?** A: For-each/streams are *internal iteration* (the collection drives); an explicit Iterator is *external iteration* (the client drives, with the ability to break early, skip, or reorder). External iteration is necessary when the client controls the loop.
9. **Q: What is the Memento pattern?** A: Capture and restore an originator's internal state in an *opaque* Memento object that a caretaker stores without ever inspecting — enabling undo/rollback without violating encapsulation.
10. **Q: What problem does Memento solve?** A: Undo/restore requires a snapshot, but exposing state via getters/setters breaks encapsulation. Memento keeps the snapshot opaque to the caretaker and readable only by the originator.
11. **Q: Who are the three participants and what does each know?** A: **Originator** — creates/restores mementos (sees the snapshot). **Memento** — opaque state holder (wide interface to originator, narrow to everyone else). **Caretaker** — stores and returns mementos but *never inspects* them (holds the policy: how many, when to save).
12. **Q: How do you keep the Memento truly opaque in Java? (Production)** A: Make it a *private static nested class* of the originator — its constructor and accessor are private to the originator; the caretaker can hold references but can't read fields (reflection aside). This is the "narrow interface" in practice.
13. **Q: Memento vs Command for undo — when each?** A: **Command** stores the *inverse operation* (O(1) memory, needs invertible ops). **Memento** stores the *state snapshot* (O(S) memory, works for anything). Non-invertible or complex ops → Memento; simple invertible ops → Command. They combine: a command can carry a memento for its undo.
14. **Q: What is a "delta memento"? (Tricky)** A: A snapshot that stores only the *changes* since the previous snapshot (rather than full state) — O(Δ) memory per undo step instead of O(S). More complex; used when state is large and changes are small (text editors, spreadsheets).
15. **Q: When is the caretaker more than a stack? (Production)** A: It can be a bounded history (LRU/capped), a branching history (time-travel with redo), an undo manager with group/transactional undo, or a persistence layer (serialize mementos to disk/DB for checkpoints). The policy lives in the caretaker — that's the pattern's separation.
16. **Q: Does Memento break if the originator changes shape?** A: Yes — a memento captured before the originator's fields changed restores an *incompatible* state (missing/renamed fields). Version the memento or validate on restore; this is a real maintenance concern in evolving codebases.
17. **Q: What does "external vs internal iteration" mean and which is Iterator?** A: External = the *client* drives the loop (`hasNext`/`next`) — the Iterator pattern. Internal = the *collection/stream* drives and calls a callback (for-each, forEach). Iterator is external; modern code often prefers internal (cleaner), but external is needed for early-exit/custom control.
18. **Q: How does a database cursor relate to Iterator?** A: A DB cursor *is* an iterator over query results — O(1) per row fetch, lazy (doesn't materialize the whole result set), with the DB hiding its internal scan structure. `ResultSet.next()` is `next()`; `isBeforeFirst()/isAfterLast()` are `hasNext()`-like.
19. **Q: Design an undo system for a text editor with large documents. (Scenario)** A: Originator = the document buffer; each `save()` produces a memento. To bound memory: store *delta mementos* (only the edited ranges) or periodic full snapshots + deltas; caretaker caps history (e.g., 1000 steps) and supports redo via a branching stack. This mixes Memento + delta optimization + caretaker policy — the complete design answer.
20. **Q: Iterator — how would you implement `remove()` (optional op)? (Tricky)** A: JDK's `Iterator.remove()` removes the last element returned by `next()` (one remove per next; illegal state otherwise). Implementation: keep the "last returned" reference; on remove, unlink it and update `modCount`. It exists to support safe removal during iteration without `ConcurrentModificationException`.

## 14. Follow-Up Questions
1. **Q: What is a "weakly consistent" iterator vs fail-fast?** A: Concurrent collections' iterators are weakly consistent: they reflect the state when created (or a snapshot) and may or may not see later changes, never throwing `ConcurrentModificationException`. Fail-fast (non-concurrent collections) detects modification and throws. Choose weakly consistent for real concurrent iteration.
2. **Q: How does the Memento pattern interact with serialization?** A: A memento can be made `Serializable` so the caretaker persists snapshots (save files, checkpoints). Trade-off: serialization is reflection-based and slower than in-memory copies; also, restoring must handle incompatible serialized shapes (versioning).
3. **Q: What is the relationship between Iterator and the Composite pattern?** A: A Composite tree can be traversed by an iterator (depth-first or breadth-first via a stack/queue) — the iterator *is* the traversal strategy over the tree. The two patterns are designed to compose: Composite = structure; Iterator = walk.
4. **Q: When would you use a *generator* (Python `yield`) over an Iterator class?** A: When the language supports them: a generator is a compact iterator (the `yield` builds the iterator protocol automatically, preserving lazy evaluation). Use generators when traversal is a simple sequential function; use an Iterator class when traversal needs shared state, bidirectional moves, or a complex internal cursor.
5. **Q: How do you make a Memento cheap for very large originators?** A: Store *only the changed fields* (delta), or store a *reference + copy-on-write* (share the base, copy the modified parts — persistent data structures), or compress/encrypt on save. The trade-off is complexity vs memory — the classic "snapshot cost" optimization question.

## 15. Coding Example
```java
// Iterator: a range iterator (lazy, O(1) per step) + custom collection
import java.util.Iterator;

class Range implements Iterable<Integer> {          // a lazy, infinite-friendly range
    private final int start, end;
    Range(int s, int e) { start = s; end = e; }
    public Iterator<Integer> iterator() {
        return new Iterator<>() {
            private int cur = start;
            public boolean hasNext() { return cur < end; }
            public Integer next() { return cur++; }
        };
    }
}
public class Main {
    public static void main(String[] args) {
        for (int x : new Range(1, 5)) System.out.print(x + " ");   // 1 2 3 4
        // Two independent iterators over the same range:
        Range r = new Range(0, 10);
        Iterator<Integer> a = r.iterator();
        Iterator<Integer> b = r.iterator();
        System.out.print(a.next() + " " + b.next());               // 0 0 (independent cursors)
    }
}
```
```java
// Memento: transactional bank account
import java.util.*;

class BankAccount {                                 // Originator
    private long balance;
    BankAccount(long b) { balance = b; }
    void deposit(long v) { balance += v; }
    void withdraw(long v) { balance -= v; }
    long balance() { return balance; }

    Snapshot save() { return new Snapshot(balance); }
    void restore(Snapshot s) { this.balance = s.balance; }

    static class Snapshot {                          // Memento — opaque to everyone outside
        private final long balance;
        private Snapshot(long b) { balance = b; }
    }
}
class TransactionManager {                           // Caretaker
    private final Deque<BankAccount.Snapshot> stack = new ArrayDeque<>();
    void begin(BankAccount a) { stack.push(a.save()); }          // snapshot — opaque
    void rollback(BankAccount a) { if (!stack.isEmpty()) a.restore(stack.pop()); }
}
public class Main {
    public static void main(String[] args) {
        BankAccount acc = new BankAccount(100);
        TransactionManager tm = new TransactionManager();
        tm.begin(acc);                                // snapshot of 100
        acc.withdraw(90);                             // balance 10
        tm.rollback(acc);                             // restore → 100
        System.out.println(acc.balance());            // 100
    }
}
```
```python
# Iterator as a generator (Pythonic)
def counter(start: int, end: int):
    cur = start
    while cur < end:
        yield cur          # generator IS an iterator
        cur += 1

print(list(counter(1, 5)))            # [1, 2, 3, 4]

# Memento
class BankAccount:
    class Snapshot:                     # opaque to outsiders (naming convention)
        def __init__(self, balance): self.balance = balance
    def __init__(self, balance):
        self._balance = balance
        self._history: list[BankAccount.Snapshot] = []
    def deposit(self, v): self._balance += v
    def begin_tx(self): self._history.append(BankAccount.Snapshot(self._balance))
    def rollback(self):
        self._balance = self._history.pop().balance

acc = BankAccount(100)
acc.begin_tx(); acc.deposit(50)
acc.rollback()
print(acc._balance)                    # 100
```
```cpp
// C++ iterator (std-like minimal)
#include <iostream>

template <typename T>
struct Iterator {
    virtual ~Iterator() = default;
    virtual bool hasNext() = 0;
    virtual T next() = 0;
};
class Range : public Iterator<int> {
    int cur_, end_;
public:
    Range(int s, int e) : cur_(s), end_(e) {}
    bool hasNext() override { return cur_ < end_; }
    int next() override { return cur_++; }
};
// int main(){ Range r(1, 5); while (r.hasNext()) std::cout << r.next() << " "; }
```

## 16. Industry Usage
- **Iterator**: the *entire* Java collections framework (`Iterator`/`Iterable`), enhanced for-each (compiled to iterator calls), `Stream.iterator()`/spliterators, database `ResultSet` cursors, ORM query result iteration (Hibernate `Query.iterate()`), network pagination iterators, generators in Python/C#/Kotlin (`yield`), Guava's `Iterators` utilities, Spring `CompositeIterator`. It's arguably the most-used pattern in the JDK.
- **Memento**: undo/redo in every serious editor (VSCode, IntelliJ, Photoshop — snapshot-based or command+snapshot hybrid), JPA/Hibernate's persistence context rollback (snapshots of loaded entities), distributed transaction compensation (snapshot before op, restore on failure), game save systems (memento serialized to disk), `git`'s objects (a commit tree *is* a memento of the repo state — restore = checkout), browser history/session restore.
- **Interviews**: "implement an iterator for a custom collection / tree", "what is fail-fast?", "design undo/redo", "save/load system", "how does git restore state?" — all classic; the Memento+Command combo and delta-memento optimization are favorite hard questions.

## 17. References
- **Gamma et al., *Design Patterns* — "Iterator" (p. 257), "Memento" (p. 283)**: canonical definitions, participants, consequences, external vs internal iteration.
- **Oracle Docs: `java.util.Iterator`, `java.lang.Iterable`, `ConcurrentModificationException`, `java.util.concurrent` (weakly consistent iterators)** — https://docs.oracle.com/javase/8/docs/api/
- **Brian Goetz et al., *Java Concurrency in Practice*, Ch. 5**: fail-fast vs weakly consistent iteration.
- **Martin Fowler, "Memento" (martinfowler.com) and *Patterns of Enterprise Application Architecture*** — memento for transactional/checkpoint state.
- **Pro Git — "Git Internals"** — commits as state snapshots (memento in version control).
- **refactoring.guru — "Iterator" and "Memento"** — modern diagrams and Java/C++/Python examples.
- **Baeldung — "Iterator Pattern in Java", "Memento Pattern in Java"** — practical tutorials.

## 18. Cheat Sheet
- **Iterator** = traverse an aggregate *without exposing structure*: `hasNext()` O(1), `next()` O(1), full walk O(N).
- For-each (`for (X x : coll)`) compiles to iterator calls; streams use spliterators.
- Each iterator owns a **private cursor** → independent/concurrent traversals.
- **Fail-fast** (`ConcurrentModificationException`) = heuristic safety; use concurrent collections for real concurrency (weakly consistent).
- Iterators are **external iteration** (client-driven); for-each/streams are internal.
- **Memento** = opaque snapshot: Originator creates/restores; Caretaker stores but never inspects.
- Keep the Memento opaque: private nested class / package-private access (narrow interface).
- **Memento vs Command-undo**: Memento = snapshot O(S) (works for anything); Command = inverse op O(1) (needs invertibility). They combine (command carries a memento).
- **Delta memento** = store only changes → O(Δ) memory.
- Caretaker owns policy (history cap, branching, persistence); originator stays clean.

## 19. Quiz
1. Iterator's purpose: a) sort elements b) traverse without exposing representation c) filter d) copy → **b**
2. `next()` complexity for a typical iterator: a) O(N) b) O(1) amortized c) O(log N) always d) O(N²) → **b**
3. Why not make the collection the cursor? a) slower b) breaks nested/concurrent traversal (one shared cursor) c) memory d) API style → **b**
4. For-each over a collection is compiled into: a) recursion b) iterator hasNext/next calls c) stream d) reflection → **b**
5. Fail-fast iteration: a) always safe for concurrency b) a heuristic that throws on structural modification c) never used d) a memento → **b**
6. Memento's key property: a) public state b) opaque snapshot c) inverse ops d) traversal → **b**
7. Who can read a Memento's contents? a) the caretaker b) the originator only c) anyone d) the client → **b**
8. Memento vs Command undo: a) memento = snapshot O(S); command = inverse O(1) b) identical c) command stores state d) memento stores inverse → **a**
9. A "delta memento" stores: a) everything b) only changes since last snapshot c) nothing d) an inverse op → **b**
10. `git checkout <commit>` is closest to: a) Iterator b) Memento (restore a state snapshot) c) Observer d) Strategy → **b**

## 20. Flashcards
- **Q: Iterator intent?** → **A:** Traverse an aggregate's elements without exposing its internal representation (hasNext/next, O(1) per step).
- **Q: Why private cursors?** → **A:** Independent traversals; one collection, many iterators (nested/concurrent loops).
- **Q: What is fail-fast?** → **A:** `modCount` tracking → `ConcurrentModificationException` on structural change during iteration (heuristic, not a concurrency guarantee).
- **Q: External vs internal iteration?** → **A:** External = client drives (Iterator); internal = collection drives (for-each/streams).
- **Q: Memento intent?** → **A:** Capture/restore an originator's state via an opaque snapshot (undo/rollback) without exposing internals.
- **Q: Three participants?** → **A:** Originator (create/restore), Memento (opaque snapshot), Caretaker (stores, never inspects).
- **Q: Memento vs Command undo?** → **A:** Memento = snapshot O(S) (any op); Command = inverse O(1) (invertible ops); they combine.
- **Q: What's a delta memento?** → **A:** Stores only changes since the last snapshot — O(Δ) memory.

## 21. Revision
**Iterator** provides sequential access to an aggregate's elements *without exposing its representation*: the collection returns an `Iterator` (a private-cursor object) and clients traverse any structure with the same `hasNext()`/`next()` protocol — O(1) per step, O(N) full walk. It exists because client-side traversal couples clients to internals (public nodes, index arithmetic) and can't support nested/concurrent loops (a single shared cursor breaks). For-each compiles to iterator calls; streams use spliterators; DB cursors and generators are iterators. **Fail-fast** (modCount → `ConcurrentModificationException`) is a heuristic — use concurrent collections for real concurrency. **Memento** captures an originator's state in an *opaque* snapshot that a caretaker stores without inspecting, enabling undo/rollback without leaking internals — participants Originator (create/restore), Memento (opaque), Caretaker (policy: caps, branching, persistence). Keep it opaque via a private nested class (narrow interface). **Memento vs Command undo**: snapshot O(S) vs inverse O(1) — non-invertible ops need Memento; they combine (a command carries a memento). **Delta mementos** store only changes (O(Δ)). Production: Iterator powers all of `java.util`; Memento powers editor undo, Hibernate rollback, and git's commit/checkout model.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is the Iterator pattern / why private cursors?" | 13 Q1–Q3 / 9 Internal Working |
| "Iterator time complexity?" | 13 Q4 / 10 Time Complexity |
| "What is fail-fast / weakly consistent?" | 13 Q5 / 14 Q1 / 16 Industry Usage |
| "How do for-each and streams relate?" | 13 Q6 / 18 Cheat Sheet |
| "Implement an iterator for a binary tree?" | 13 Q7 / 15 Coding |
| "What is the Memento pattern / participants?" | 13 Q9–Q11 / 2 How |
| "How do you keep the memento opaque?" | 13 Q12 / 18 Cheat Sheet |
| "Memento vs Command for undo?" | 13 Q13 / 18 Cheat Sheet |
| "What's a delta memento / when to use it?" | 13 Q14 / 14 Q5 |
| "Design an undo system for a large document (scenario)." | 13 Q19 / 8 Example |
