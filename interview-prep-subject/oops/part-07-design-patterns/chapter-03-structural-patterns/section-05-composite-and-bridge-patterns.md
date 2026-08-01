# Composite and Bridge Patterns

> **TL;DR**: The **Composite** pattern treats individual objects and their **groupings uniformly** as a single tree (part-whole hierarchy), and the **Bridge** pattern **decouples an abstraction from its implementation so both can vary independently** — Composite exists to make "leaf" and "container" the same to the caller, Bridge exists to break the 2D class explosion of abstraction×implementation.

## 1. Why Does This Exist?
**Composite** exists because real structures are *recursive*: a folder contains files and folders; a UI window contains buttons and panels that contain more buttons; an organization chart has employees and managers who manage employees. Without a uniform abstraction, the caller must special-case: "if it's a folder, iterate children; if it's a file, print it" — every operation duplicates the recursion and every client must know the tree's node types. The Composite pattern makes `File` and `Folder` *the same interface* (`Component`), so a client can call `render()` on either without knowing which it is, and containers recursively delegate to children. The part and the whole become interchangeable — you can render one node or an entire tree with the *same code path*.

**Bridge** exists because some concepts vary along **two independent axes** that inheritantly multiply: a `Shape` that comes in `Circle`/`Square`/`Triangle` and is rendered as `OpenGL`/`DirectX`/`Vulkan`. Modeling with inheritance gives 3×3 = 9 classes (`OpenGLCircle`, `DirectXCircle`, ...); adding a shape or renderer multiplies the set. The Bridge pattern splits the two axes — the *abstraction* (Shape) holds a reference to the *implementation* (Renderer interface) — so shapes and renderers vary independently: 3 shape classes + 3 renderer classes = 6 classes, and adding either axis is one new class. It exists to replace *inheritance-combinatorial* designs with *composition*.

## 2. How Does It Work?
**Composite:**
```
Component (interface: operation(); add/remove children)
   ▲                      ▲
Leaf (no children)    Composite (holds List<Component>;
   implements            operation() { for each child → child.operation() }
   operation directly)   add/remove children)
```
- `Leaf` implements the interface without children.
- `Composite` also implements the interface and holds children; its `operation()` **recurses** to each child.
- The client sees only `Component` — uniform treatment of leaves and composites.

```java
interface FileSystemNode {              // Component
    String name();
    void printTree(String indent);      // uniform operation
}
class File implements FileSystemNode {  // Leaf
    private final String name;
    File(String n) { this.name = n; }
    public String name() { return name; }
    public void printTree(String indent) { System.out.println(indent + "📄 " + name); }
}
class Directory implements FileSystemNode {   // Composite
    private final String name;
    private final List<FileSystemNode> children = new ArrayList<>();
    Directory(String n) { this.name = n; }
    public void add(FileSystemNode c) { children.add(c); }
    public String name() { return name; }
    public void printTree(String indent) {       // recursion = the pattern
        System.out.println(indent + "📁 " + name);
        for (FileSystemNode child : children) child.printTree(indent + "  ");
    }
}
// Client — uniform:
FileSystemNode root = new Directory("root");
Directory docs = new Directory("docs"); docs.add(new File("readme.md"));
root.add(docs); root.add(new File("build.gradle"));
root.printTree("");   // same call for a file or a directory tree
```

**Bridge:**
```
Abstraction ──has-a──> Implementor (interface)
   ▲                           ▲
RefinedAbstraction       ConcreteImplementorA/B
```
- `Abstraction` (e.g., `Shape`) defines high-level operations and holds an `Implementor` reference.
- `Implementor` (e.g., `Renderer`) defines the low-level primitive operations.
- `ConcreteImplementor`s (OpenGL/DirectX renderers) do the actual work.
- Both hierarchies vary independently.

```java
interface Renderer { void drawCircle(double r); void drawSquare(double s); }   // Implementor
class OpenGLRenderer implements Renderer { public void drawCircle(double r){/* GL */} public void drawSquare(double s){/* GL */} }
class DirectXRenderer implements Renderer { public void drawCircle(double r){/* DX */} public void drawSquare(double s){/* DX */} }

abstract class Shape {                 // Abstraction
    protected final Renderer renderer;
    Shape(Renderer r) { this.renderer = r; }
    abstract void draw();
}
class Circle extends Shape {           // RefinedAbstraction
    private final double r;
    Circle(Renderer r, double radius) { super(r); this.r = radius; }
    void draw() { renderer.drawCircle(r); }   // delegates to the implementation
}
class Square extends Shape {
    private final double s;
    Square(Renderer r, double side) { super(r); this.s = side; }
    void draw() { renderer.drawSquare(s); }
}
// 2 shapes × 2 renderers = 4 combinations, only 4+2 classes. Adding Triangle = 1 class.
```

## 3. When Is It Used?
- **Composite**: recursive/hierarchical structures — filesystems, UI widget trees (Swing/React/Flutter component trees), organization charts, HTML DOM, expression trees, product categories with subcategories, menus with submenus. Whenever clients must treat "one thing" and "a group of things" identically.
- **Bridge**: two independent variation axes that multiply — device/remote (remote controls that work across TVs/radios), shape/rendering, database-specific queries/code that must work across DBs, message formats across transports, GUI controls across operating systems.
- **Interviews**: "design a filesystem/menu/DOM tree" → Composite; "shape and color / device and remote" → Bridge.

## 4. Why Wasn't Another Approach Chosen?
**For Composite:**
- **Type-check and special-case in the client** (`if (node instanceof Directory) ... else ...`): rejected — duplicates the recursion logic at every call site, breaks Open-Closed (new node types need client changes), and couples clients to concrete types. Composite *removes* the client's need to distinguish.
- **A separate "container" type with no shared interface**: rejected — the client must switch on type; the whole point is uniform treatment.
- **Visitor pattern instead**: Visitor separates *operations* from tree structure (good when operations vary a lot); Composite *is* the structure; they're complementary (Composite + Iterator to traverse, Composite + Visitor to operate). For simple uniform operations, Composite alone suffices.
- **Flat collections with explicit tree links**: rejected — no uniform interface; recursion lives in the client.

**For Bridge:**
- **Inheritance matrix (class per combination)**: rejected — 3 shapes × 3 renderers = 9 classes; N×M explosion; adding a dimension makes it worse. Bridge = N + M classes.
- **One "fat" class with every renderer baked in**: rejected — violates SRP, cannot add renderers without editing shapes.
- **A renderer interface used by shapes without the abstract `Shape` layer**: that's essentially the Bridge (the `Shape` abstraction holds the `Implementor`); the refinement layer (`Circle`/`Square`) is what makes shapes vary independently too.
- **Strategy pattern**: superficially similar (composition of an algorithm) — but Strategy is *behavioral* (swapping a whole algorithm inside a context) while Bridge is *structural* (decoupling abstraction and implementation hierarchies from the start). Bridge's intent is about *decoupling axes*; Strategy's is about *algorithm selection*.
- **Adapter**: rejected — adapter is a retrofit for incompatibility; bridge is forward-looking design separating axes before the class explosion happens.

## 5. Intuition
**Composite intuition**: a **family tree / org chart**. "Print everyone under Bob" shouldn't care whether Bob manages a team of 1 (leaf-ish) or a team with sub-managers (composite). You walk the tree: "Bob → each direct report → if they have reports, recurse." The *uniform interface* is "a node with a name"; the recursion handles the rest. Same for a filesystem: `du folder` doesn't distinguish file from folder beyond recursing.

**Bridge intuition**: a **universal remote** that works with any TV. The "remote" (abstraction — high-level controls: power, volume, channel) and the "TV" (implementation — specific signal protocol) are *two independent hierarchies*. A `SmartRemote` works on a `SonyTV` or a `LGTV`; a `BasicRemote` too. No "SonySmartRemote" class exists — the remote *holds a reference* to the TV and delegates. Adding a new remote brand or a new TV brand doesn't multiply classes.

## 6. Real-World Analogy
- **Composite**: a **restaurant menu with categories**. A menu has items (leaf) and sections like "Appetizers" or "Combo deals" that contain more items or sub-sections (composite). The waiter computes the price of anything the same way: "price = my price + sum of children's prices" — whether it's a single appetizer or a whole combo. One operation, recursive, uniform.
- **Bridge**: a **car and its steering wheel**. The "driving" abstraction (accelerate, brake, steer) is decoupled from the implementation (front-wheel vs all-wheel drive, electric vs petrol powertrain). You don't build a "FrontWheelElectricCar" for every combo — the car (abstraction) delegates to its drivetrain (implementation). The two axes (car model × drivetrain) evolve independently.

## 7. Formal Definition
> **Composite**: Compose objects into **tree structures** to represent part-whole hierarchies. Composite lets clients treat **individual objects and compositions of objects uniformly**. (GoF, p. 163)
>
> **Bridge**: **Decouple an abstraction from its implementation** so that the two can **vary independently**. (GoF, p. 151)
>
> Participants (Composite): **Component** (interface, may include child-management ops), **Leaf** (no children, implements operations directly), **Composite** (holds children, implements operations by recursion). Participants (Bridge): **Abstraction** (high-level interface, holds Implementor), **RefinedAbstraction**, **Implementor** (low-level interface), **ConcreteImplementor**.

## 8. Example
**Composite — UI widget tree**: A `Component.render()` on a `Button` draws itself; on a `Panel` it draws its background then renders every child. The same `render()` call draws a whole screen. Adding `Checkbox`, `TextField`, `Container` = new leaf/container types, zero client changes (Open-Closed). `javax.swing.JComponent` *is* this pattern — Swing components are a composite tree; `JPanel.add(component)` nests anything in anything.

**Bridge — a cross-database query builder**: `Query` (Abstraction) with dialects `MySqlDialect`/`PostgresDialect` (Implementors). `SelectQuery`, `InsertQuery` (RefinedAbstractions) delegate string generation to the dialect. Adding SQL Server = 1 dialect class; adding a `DeleteQuery` = 1 query class. No 2×N explosion.

## 9. Internal Working
**Composite internal working:**
1. Client holds a `Component` reference (leaf or composite — same type).
2. Client calls `component.operation()`.
3. **Dynamic dispatch**: if leaf → executes its own operation; if composite → the composite calls `operation()` on *each child*, which recursively dispatches again (children may themselves be composites).
4. The recursion terminates at leaves; the tree is walked depth-first.
5. **Client advantage**: the caller has *no branching* — no `instanceof`, no "is this a folder?" check. Adding new node types never touches clients (Open-Closed).
6. Optional safety: a leaf's `add()`/`remove()` can throw (`UnsupportedOperationException`) or the interface can be *separated* (transparent vs safe composite — a known design trade-off).

**Bridge internal working:**
1. The abstraction is constructed with an `Implementor` (injected at run time — e.g., "use OpenGL").
2. High-level `Abstraction` methods are implemented by *delegating* to the implementor's primitives.
3. A `RefinedAbstraction` adds more high-level ops, still delegating low-level work.
4. Changing the implementation at run time = replacing the implementor reference (composition — the implementor is swappable).
5. The two hierarchies evolve separately: new refined abstractions need no implementor changes and vice versa — **no cross-hierarchy edits**.

## 10. Time Complexity
- **Composite operation**: O(N) where N = number of nodes in the subtree (each node does O(1) work + recursion). Traversal is inherently O(N). A single-node operation is O(1).
- **Composite add/remove**: O(1) (append to a list).
- **Memory**: O(N) nodes + O(1) per leaf; a shallow tree with many leaves costs the same as a deep tree (depth only affects recursion stack, O(depth) worst case — deep trees risk `StackOverflowError`).
- **Bridge**: O(1) per delegated operation (one extra virtual dispatch). The *design* cost: O(N+M) classes instead of O(N×M) — the class-explosion win.
- **Neither changes algorithmic Big-O** of the underlying work; both trade structure for maintainability.

## 11. Advantages
**Composite:**
- **Uniformity**: clients treat leaves and composites identically — no type checks, no special cases.
- **Recursion for free**: containers handle their own children; new operations are added per-Component (once).
- **Open-Closed**: adding a node type never touches clients or the tree logic.
- **Natural for real hierarchies**: filesystems, UI trees, menus, DOM.
- **Composes with Iterator/Visitor/Decorator** for traversal, operations, and augmentation.
**Bridge:**
- **Kills the N×M explosion**: independent hierarchies = N+M classes.
- **Independent evolution**: changing a renderer never touches shapes; new shapes never touch renderers.
- **Run-time swapping**: implementation can change at run time (composition).
- **SRP**: abstraction owns high-level behavior; implementor owns platform details.
- **Open-Closed on both axes**: extend either axis with one new class.

## 12. Disadvantages
**Composite:**
- **Over-generalization**: every node exposes child operations (`add`/`remove`) even when meaningless for leaves — the "transparent vs safe" dilemma (leaves throwing `UnsupportedOperationException` is ugly).
- **Type safety lost**: clients can't easily say "this must be a leaf" — the interface hides the distinction.
- **Deep trees**: recursion can overflow the stack; iteration requires explicit traversal.
- **Can be overkill**: a flat structure with one nesting level doesn't need the pattern.
**Bridge:**
- **More initial structure**: you design two hierarchies up front even if one axis currently has a single implementor (YAGNI risk — premature bridge).
- **Indirection**: every operation passes through the abstraction → implementor delegation.
- **Hard to apply retroactively**: it's a forward-looking design decision; retrofitting is expensive (unlike Adapter).
- **Abstraction/implementor naming confusion**: teams mis-model the two axes (putting too much in the abstraction).

## 13. Interview Questions
1. **Q: What is the Composite pattern?** A: A structural pattern that composes objects into tree structures (part-whole hierarchies) and lets clients treat leaves and composites uniformly through a single `Component` interface.
2. **Q: What problem does Composite solve?** A: Clients would otherwise branch on node type ("is this a folder?") and duplicate recursion logic at every call site — breaking Open-Closed and coupling clients to concrete types. Composite makes one interface handle both.
3. **Q: What is the Bridge pattern?** A: A structural pattern that decouples an abstraction from its implementation — the abstraction holds a reference to an `Implementor`, so the two hierarchies vary independently.
4. **Q: What problem does Bridge solve?** A: The N×M class explosion of modeling two independent variation axes with inheritance (3 shapes × 3 renderers = 9 classes). Bridge makes it N+M classes and lets each axis evolve independently.
5. **Q: How does a Composite's `operation()` work on a container?** A: It executes its own part, then iterates children calling `child.operation()` — which recurses (children may themselves be composites). Leaves implement it directly. That recursion is the whole pattern.
6. **Q: Leaf vs Composite — how are they different internally?** A: Leaves have no children and implement operations directly; Composites hold a list of children and implement operations by delegation+recursion. Externally (to the client) they're identical — that's the point.
7. **Q: What's the "transparent vs safe" Composite trade-off? (Tricky)** A: *Transparent*: `Component` declares `add`/`remove`, so leaves must implement them (often throwing `UnsupportedOperationException`) — uniform but unsafe. *Safe*: only `Composite` declares child ops — type-safe but the client must cast to use them. GoF discusses both; production often mixes.
8. **Q: Where does the JDK/Swing use Composite?** A: `javax.swing.JComponent` is a Composite — `JPanel` (container) and `JButton` (leaf) both extend `JComponent`; `add()` nests any component in any container; rendering recurses through the tree. Also `java.awt.Container`, XML `NodeList`, JavaFX `Node` trees.
9. **Q: Composite vs Decorator?** A: Both are structural wrappers, but Composite forms *trees* (one interface, many children, recursion) while Decorator forms *linear chains* (one inner reference, augmentation). They're often combined (a decorator wrapping a composite).
10. **Q: How does Composite relate to Iterator/Visitor?** A: Composite defines the *structure* (the tree); Iterator defines how to *traverse* it; Visitor defines how to *operate* on it without changing the tree. They compose: a composite tree + an iterator + a visitor = flexible tree processing. This is the classic pattern-composition interview point.
11. **Q: Give a real Bridge example in production.** A: JDBC `Driver`/`Connection` — the JDBC API (abstraction) is implemented by each vendor's driver (implementor): switching `DriverManager` from MySQL to Postgres swaps the implementor without changing application code. Also GUI toolkits (Java AWT: `Toolkit` abstracts platform widgets) and Java's `AWT`/`Swing` peer architecture (a real Bridge: windowing abstraction over OS peers).
12. **Q: Bridge vs Adapter?** A: Adapter retrofits an *existing* incompatible interface for compatibility; Bridge *deliberately* separates abstraction from implementation up front to avoid class explosion. Adapter is reactive; Bridge is proactive design.
13. **Q: Bridge vs Strategy?** A: Both use composition with an injected collaborator. Strategy is *behavioral* — it varies an algorithm inside a context. Bridge is *structural* — it decouples two hierarchies so both vary independently. Strategy swaps behavior; Bridge separates abstraction/implementation dimensions.
14. **Q: When is Bridge over-engineering? (Production)** A: When only one implementation exists and none is predicted — you'd be designing two hierarchies for nothing (YAGNI). Introduce Bridge when the *second* implementor actually arrives (or is strongly forecast), then refactor. Interviewers respect this "defer the pattern" judgment.
15. **Q: How do you traverse a composite without recursion (to avoid stack overflow)? (Production)** A: Use an explicit stack/queue (DFS/BFS with a `Stack`/`Deque`) or an iterator (the pattern's iterator variant). Deep DOM/filesystem trees can overflow the call stack with recursive `operation()`.
16. **Q: Design a menu system with submenus using Composite. (Scenario)** A: `MenuItem` (leaf: name, click), `Menu` (composite: holds `List<MenuItem>`/`Menu`, `render()` recurses, `click()` propagates). A submenu IS a menu — nesting is free; the client renders a `MenuComponent` regardless of depth.
17. **Q: Can a Composite contain itself (cycles)? (Tricky)** A: Yes, if nothing prevents it — infinite recursion. Production guards: don't allow adding a parent as its own descendant, or track visited nodes during traversal. Real DOM/filesystems prevent cycles by ownership rules.
18. **Q: What's the difference between the "Abstraction" and "RefinedAbstraction" in Bridge?** A: `Abstraction` defines the general high-level interface and holds the `Implementor`; `RefinedAbstraction` (e.g., `Circle`) *extends* the abstraction with specific behavior while still delegating primitives to the implementor. The refinement is where the abstraction axis varies.
19. **Q: Composite — do children and parents have to be the same type?** A: In the classic pattern yes — children are typed `Component`. Some designs relax this (children typed to a supertype) but then uniformity weakens. Keeping one `Component` type is what makes recursion uniform.
20. **Q: Design a shape system with two renderers and three shapes. Count the classes with and without Bridge.** A: Without Bridge (inheritance): 3 shapes × 2 renderers = 6 concrete classes (plus base) = 7+. With Bridge: 3 shape classes + 2 renderer classes + interfaces = 6 total; adding a renderer = +1 class (not +3). That arithmetic is the interview answer.

## 14. Follow-Up Questions
1. **Q: What is the "safe composite" variant exactly?** A: Only the Composite class declares `add`/`remove`; `Component` declares only the shared operation. The client must cast to `Composite` to add children — type-safe but less uniform. Contrast: transparent composite puts child ops on `Component` (uniform, but leaves must implement or throw).
2. **Q: How does Bridge relate to the "Pimpl" idiom in C++?** A: Pimpl (pointer-to-implementation) hides a class's implementation behind a pointer to keep ABI stable — it's Bridge's *structural mechanism* applied to a single class. Bridge generalizes it: an explicit Implementor hierarchy so the abstraction and implementation each have their own class families.
3. **Q: Composite and Flyweight — why paired?** A: Flyweight shares the *intrinsic* (shared) state of many fine-grained objects. A tree with millions of leaves (e.g., file icons) can be a Flyweight-shared leaf reused across the Composite — the pattern pair is the classic way to handle huge trees with bounded memory.
4. **Q: In Bridge, what belongs in the abstraction vs the implementation?** A: The abstraction holds *high-level, platform-independent* operations (draw circle at coords); the implementation holds *low-level, platform-specific* primitives (put pixels via OpenGL). The line is drawn where platform variability begins.
5. **Q: When do Composite and Bridge co-occur?** A: A composite tree whose leaf behavior is platform-dependent: the leaves (or the tree's rendering) delegate through a Bridge to platform implementors. Real example: Java AWT — the component tree (Composite) delegates painting through the peer architecture (Bridge).

## 15. Coding Example
```java
// Composite: a file system
interface FSNode { long size(); void print(int depth); }

class File implements FSNode {                 // Leaf
    private final String name; private final long size;
    File(String n, long s) { name = n; size = s; }
    public long size() { return size; }
    public void print(int depth) { System.out.println("  ".repeat(depth) + "- " + name + " (" + size + "B)"); }
}
class Directory implements FSNode {             // Composite
    private final String name; private final List<FSNode> children = new ArrayList<>();
    Directory(String n) { name = n; }
    public void add(FSNode c) { children.add(c); }
    public long size() { return children.stream().mapToLong(FSNode::size).sum(); }  // recursion
    public void print(int depth) {
        System.out.println("  ".repeat(depth) + "+ " + name);
        children.forEach(c -> c.print(depth + 1));                                  // recursion
    }
}
// Client: uniform — size()/print() work on any node
FSNode root = new Directory("app");
Directory src = new Directory("src");
src.add(new File("Main.java", 4_000));
src.add(new File("Util.java", 2_000));
root.add(src); root.add(new File("README.md", 500));
root.print(0);
System.out.println("Total size: " + root.size() + " bytes");
```
```java
// Bridge: shapes over renderers
interface Renderer { void renderCircle(double r); void renderSquare(double s); }
class OpenGLRenderer implements Renderer {
    public void renderCircle(double r) { System.out.println("OpenGL: circle r=" + r); }
    public void renderSquare(double s) { System.out.println("OpenGL: square s=" + s); }
}
class VulkanRenderer implements Renderer {
    public void renderCircle(double r) { System.out.println("Vulkan: circle r=" + r); }
    public void renderSquare(double s) { System.out.println("Vulkan: square s=" + s); }
}
abstract class Shape {                          // Abstraction
    protected final Renderer r;
    Shape(Renderer r) { this.r = r; }
    abstract void draw();
}
class Circle extends Shape {
    private final double radius;
    Circle(Renderer r, double radius) { super(r); this.radius = radius; }
    public void draw() { r.renderCircle(radius); }
}
class Square extends Shape {
    private final double side;
    Square(Renderer r, double side) { super(r); this.side = side; }
    public void draw() { r.renderSquare(side); }
}
// Client: choose renderer at run time
Shape s = new Circle(new VulkanRenderer(), 5.0);  s.draw();
Shape q = new Square(new OpenGLRenderer(), 3.0);  q.draw();
// Adding "Triangle" = 1 class; adding "MetalRenderer" = 1 class. No cross-edits.
```
```python
# Python Composite
class Node:                                  # Component (protocol-ish)
    def size(self) -> int: ...
    def name(self) -> str: ...

class File(Node):
    def __init__(self, name: str, size: int): self._n, self._s = name, size
    def size(self) -> int: return self._s
    def name(self) -> str: return self._n

class Directory(Node):                       # Composite
    def __init__(self, name: str): self._n = name; self._children = []
    def add(self, n: Node) -> None: self._children.append(n)
    def size(self) -> int: return sum(c.size() for c in self._children)
    def name(self) -> str: return self._n

root = Directory("app")
src = Directory("src"); src.add(File("Main.java", 4000)); src.add(File("Util.java", 2000))
root.add(src); root.add(File("README.md", 500))
print(root.size())                            # 6500 — uniform call
```
```cpp
// C++ Bridge
#include <iostream>

struct Renderer { virtual ~Renderer() = default; virtual void drawCircle(double) = 0; };
struct OpenGL : Renderer { void drawCircle(double r) override { std::cout << "GL circle " << r << "\n"; } };
struct Vulkan : Renderer { void drawCircle(double r) override { std::cout << "Vulkan circle " << r << "\n"; } };

class Shape {                       // Abstraction
protected:
    Renderer& renderer_;
public:
    explicit Shape(Renderer& r) : renderer_(r) {}
    virtual ~Shape() = default;
    virtual void draw() = 0;
};
class Circle : public Shape {       // RefinedAbstraction
    double r_;
public:
    Circle(Renderer& r, double radius) : Shape(r), r_(radius) {}
    void draw() override { renderer_.drawCircle(r_); }
};
// int main(){ OpenGL gl; Circle c(gl, 5.0); c.draw(); }
```

## 16. Industry Usage
- **Composite**: Swing/AWT `Component`+`Container` (Java's canonical composite), XML/HTML DOM (Node → element/container nodes), Spring `CompositePropertySource`, `CompositeBeanDefinitionRegistry`, Guava `CompositeService`, filesystem APIs, React/Flutter/Compose widget trees (every widget tree is a composite), JUnit suites (`TestSuite` containing tests), menu systems in POS/UI apps.
- **Bridge**: JDBC (`Driver`/`Connection` abstraction over vendor drivers), Java AWT peer architecture (abstract windowing over OS-specific peers), SLF4J (abstraction over logging backends — arguably), ORM dialects (Hibernate `Dialect` per DB), audio codecs (abstraction over codec implementations), platform-specific rendering in games.
- **Interviews**: "design a filesystem/menu/widget tree" → Composite; "shape/renderer, device/remote, DB dialects" → Bridge; both are stock LLD scenarios, and the composite-iterator-visitor composition is a favorite hard question.

## 17. References
- **Gamma et al., *Design Patterns* — "Composite" (p. 163), "Bridge" (p. 151)**: canonical definitions, participants, transparent-vs-safe discussion (Composite), abstraction/implementor discussion (Bridge).
- **Oracle Docs: `java.awt.Container`/`java.awt.Component`, `java.sql.Driver`/`Connection`, Swing `JComponent`** — https://docs.oracle.com/javase/8/docs/api/
- **Hibernate Docs: `Dialect`** (Bridge example for cross-DB SQL) — https://hibernate.org/orm/documentation/
- **refactoring.guru — "Composite" and "Bridge"** — modern diagrams and Java/C++/Python examples.
- **Head First Design Patterns — "Composite" and "Bridge" chapters** — worked analogies.
- **Baeldung — "Composite Pattern in Java", "Bridge Pattern in Java"** — practical tutorials.
- **W3C DOM spec** (Node/element tree — the web's composite) — https://dom.spec.whatwg.org/

## 18. Cheat Sheet
- Composite = **tree + uniform interface**: leaves and composites both implement `Component`; containers recurse.
- Client code has **no `instanceof` branching** — one call renders a node or a whole tree.
- Leaf: no children, direct op. Composite: children list, op = own work + `child.op()` recursion.
- Transparent vs safe composite: child ops on `Component` (uniform, leaves throw) vs on `Composite` only (type-safe, needs cast).
- Composite + Iterator (traverse) + Visitor (operate) is the classic composition.
- Bridge = **decouple abstraction from implementation** — abstraction holds an `Implementor`; both hierarchies vary independently.
- Bridge kills the **N×M class explosion** (N+M classes) and allows run-time implementor swap.
- Bridge ≠ Adapter (retrofit vs proactive); Bridge ≠ Strategy (structural decoupling vs behavioral algorithm swap).
- Real composites: Swing/AWT component trees, DOM, widget trees. Real bridges: JDBC drivers, Hibernate Dialect, AWT peers.
- Introduce Bridge when the *second* implementor appears (YAGNI before that).

## 19. Quiz
1. Composite lets clients treat: a) only leaves b) only composites c) leaves and composites uniformly d) only trees → **c**
2. In a Composite, a container's operation is implemented by: a) direct logic b) recursing to children c) a visitor d) a factory → **b**
3. The "transparent" composite variant: a) only Composite has add/remove b) Component declares add/remove (leaves may throw) c) no children allowed d) is a bridge → **b**
4. Bridge decouples: a) two algorithms b) abstraction from implementation c) leaf from composite d) interface from client → **b**
5. Without Bridge, 3 shapes × 3 renderers = ___ classes (with Bridge ___ ). a) 6, 3 b) 9, 6 c) 12, 3 d) 6, 9 → **b**
6. JDBC `DriverManager`/`Connection` over vendor drivers is an example of: a) Composite b) Bridge c) Decorator d) Singleton → **b**
7. `JPanel` and `JButton` both extending `JComponent` is: a) Bridge b) Composite c) Adapter d) Strategy → **b**
8. Composite + ___ for traversal + ___ for operations. a) Strategy, State b) Iterator, Visitor c) Factory, Builder d) Proxy, Facade → **b**
9. Bridge differs from Strategy because: a) bridge swaps algorithms b) strategy swaps algorithms (behavioral); bridge decouples hierarchies (structural) c) they're identical d) strategy is structural → **b**
10. When is Bridge premature? a) two implementations exist b) one implementation and no forecast of another c) class explosion d) when shapes vary → **b**

## 20. Flashcards
- **Q: Composite intent?** → **A:** Compose objects into trees; treat leaves and composites uniformly via one interface.
- **Q: How does a container's op work?** → **A:** Own work + recurse into children (leaf: direct op).
- **Q: Transparent vs safe composite?** → **A:** Transparent puts child ops on Component (uniform, leaves throw); safe puts them on Composite (type-safe, needs cast).
- **Q: Bridge intent?** → **A:** Decouple abstraction from implementation so both vary independently (N+M classes vs N×M).
- **Q: Bridge vs Adapter?** → **A:** Adapter retrofits compatibility; Bridge proactively decouples two hierarchies.
- **Q: Bridge vs Strategy?** → **A:** Strategy swaps algorithms (behavioral); Bridge decouples hierarchies (structural).
- **Q: Real Composite examples?** → **A:** Swing/AWT component trees, HTML DOM, widget trees, JUnit suites.
- **Q: Real Bridge examples?** → **A:** JDBC drivers, Hibernate `Dialect`, AWT peers.

## 21. Revision
**Composite** composes objects into **tree structures** and exposes one `Component` interface, so clients treat leaves and containers uniformly — containers implement operations by *recursing into children*, and clients never branch on node type. It exists because real hierarchies (filesystems, widget trees, menus, DOM) would otherwise force `instanceof`-based special-casing at every call site. Trade-offs: the transparent-vs-safe child-op dilemma and deep-tree recursion (use iterators/stack for very deep trees). **Bridge** decouples an **abstraction from its implementation** (the abstraction holds an `Implementor`), so both axes vary independently — turning the N×M class explosion (3 shapes × 3 renderers = 9) into N+M (6). It exists wherever two dimensions multiply (shape/renderer, device/remote, DB dialects). Discriminate: Adapter retrofits compatibility; Strategy swaps algorithms (behavioral); Bridge is proactive structural decoupling. Real world: Swing/AWT component trees and DOM (composite); JDBC drivers, Hibernate `Dialect`, AWT peers (bridge). Introduce Bridge only when the second implementor actually arrives — YAGNI before that. Composite pairs with Iterator (traversal) and Visitor (operations).

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is the Composite / Bridge pattern?" | 2 How / 7 Formal Definition |
| "What problem does each solve?" | 1 Why / 13 Q2 / 13 Q4 |
| "How does a container's operation recurse?" | 9 Internal Working / 13 Q5 |
| "Transparent vs safe composite?" | 13 Q7 / 14 Q1 |
| "Composite + Iterator + Visitor?" | 13 Q10 / 14 Q4 |
| "Bridge vs Adapter / Strategy?" | 13 Q12 / 13 Q13 |
| "Class-count arithmetic with/without Bridge?" | 13 Q20 / 5 Intuition |
| "Real JDK/framework examples?" | 13 Q8 / 13 Q11 / 16 Industry Usage |
| "When is Bridge over-engineering?" | 13 Q14 / 14 Q3 |
| "Design a filesystem/menu (Composite) or shapes (Bridge) (scenario)." | 13 Q16 / 13 Q20 / 15 Coding |
