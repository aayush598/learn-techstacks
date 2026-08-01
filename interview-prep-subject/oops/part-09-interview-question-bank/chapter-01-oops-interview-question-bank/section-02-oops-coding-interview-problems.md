# OOPs Coding Interview Problems

> **TL;DR**: Six classic OOP coding prompts (Tic-Tac-Toe, LRU Cache, Vending Machine, Library System, Restaurant Ordering, Employee Hierarchy) with full modeling and Java solutions — the "design a class/object system" prompts that follow the theory round at most interviews.

## 1. Why Does This Exist?
Beyond pure algorithms, interviewers test **object modeling**: can you take a fuzzy English description ("design a vending machine") and produce clean classes, correct relationships, SOLID-compliant responsibilities, and working code — on a whiteboard, in 30-45 minutes? These problems exist because they measure the exact production skill of turning requirements into maintainable OOP systems, and they are the most reliable signal of "design thinking" a short interview can get.

## 2. How Does It Work?
Each problem below follows the same loop you should use in the interview: **1) clarify requirements → 2) identify objects → 3) define relationships (IS-A / HAS-A) → 4) sketch the class diagram → 5) write clean Java → 6) test with a scenario**. The code is complete but lean — no framework noise — so you can read the modeling decisions, then re-type the solution from memory as practice.

## 3. When Is It Used?
- **30-45 minute "design a X" questions** after the theory round.
- **Take-home LLD assignments** (less common but real at product companies).
- **Warm-ups** before a full system-design round.
- Study companions to Section 03 (LLD guide) — these are the "single-object-system" size of the LLD loop.

## 4. Why Wasn't Another Approach Chosen?
These problems are solved with **object modeling** rather than pure algorithms because the interview tests OOP, not just data structures. Where an algorithmic solution exists (e.g., LRU), the OOP wrapper (an interface, a node class, encapsulated eviction) is what makes it "an OOP problem." Alternatives like procedural implementations or god-classes are deliberately avoided in the solutions to model good practice: interfaces for contracts (SRP/DIP), composition over inheritance, and small focused classes. The solutions show *one* good design — in the interview, the *process* matters more than the exact class list.

## 5. Intuition
Think of each problem as **an interview with a small company**: the nouns in the description are your *classes* (ParkingSpot, Vehicle, Ticket), the verbs are your *methods* (park, unpark, pay), and the "is a" phrases are your *inheritance* (Car is a Vehicle). The design skill is: find the nouns, decide what each class *owns* (HAS-A) and *is* (IS-A), and keep each class responsible for exactly one thing (SRP). Once the nouns are mapped, the code writes itself.

## 6. Real-World Analogy
Like **LEGO instructions**: the problem statement is the box-art picture; your job is to figure out which bricks (classes) snap where (relationships) so the model stands up (compiles and runs). A good designer doesn't invent new brick shapes for every set — they reuse standard bricks (interfaces, base classes, patterns) the way the solutions reuse `Vehicle` abstraction and `HashMap`-based caches.

## 7. Formal Definition
An OOP coding problem is a design task specified in natural language whose evaluation criteria are: correct object decomposition (identifiable entities with single responsibilities), appropriate relationships (inheritance vs composition), use of abstraction/polymorphism to keep behavior extensible, and clean, working code demonstrating the modeled design under a specified scenario.

## 8. Example (walk through one fully)
**Problem: Design Tic-Tac-Toe.**
1. **Clarify**: single board 3x3, two players, X/O, detect win (row/col/diagonal), avoid invalid moves, optional AI opponent.
2. **Objects**: `Board`, `Player`, `Move`, `Game`, `Piece` (enum), `GameState`.
3. **Relationships**: `Game` HAS-A `Board` and two `Player`s; `Player` HAS-A `Piece`; `Game` IS-A nothing (composition). `MoveValidator` (interface) → simple rules; polymorphism for "human vs bot player" via abstract `Player`.
4. **Class sketch**:
```
Game --has--> Board (3x3 Square/Piece)
Game --has--> Player[2]  (abstract; HumanPlayer, BotPlayer)
Player --has--> Piece (X/O)
Game --has--> MoveValidator (Strategy)
```
5. **Code** (below, Problem 1) models this with enums, an abstract `Player`, and a `GameState`.
6. **Test**: play "X center, O corner, X opposite center" → win by center row/col.

## 9. Internal Working (the standard solution loop)
1. Parse the problem for **nouns** → candidate classes; drop anything that's just a property (use a field).
2. For each class: what data (fields) and what behavior (methods)? Keep one responsibility.
3. Find **IS-A** pairs → inheritance/interfaces; everything else is **HAS-A** (fields).
4. Decide **who owns whom** (composition vs aggregation) — lifetime matters (board dies with game; a player may outlive a game).
5. Define **polymorphic seams**: where behavior varies (payment method, piece logic, move rules) → interface/abstract + implementations.
6. Code the skeleton (classes + signatures), then fill methods, then test one scenario.
7. Interview delivery: narrate steps 1-5 before writing any code — interviewers grade the thinking.

## 10. Time Complexity
- Modeling itself: O(n) time to sketch classes (n = number of entities), the dominant cost is *thinking*, not computation.
- Solutions below: Tic-Tac-Toe move O(9) check; LRU get/put O(1); Vending Machine O(1) ops; Library search O(n) or O(log n) with sorted index; Ordering service O(1) dispatch. Always state complexity when you present a solution.

## 11. Advantages
- These problems are the **most repeated** class of OOP interview question at product companies.
- They force the exact production skill (requirement → design → code) in one sitting.
- Clean solutions are short (~80-200 lines) — improvable with the interview loop.
- Same set covers object modeling, patterns, SOLID, and language mechanics.

## 12. Disadvantages
- Interview time pressure makes process sloppiness costly (jumping to code).
- No single "right" answer — different valid designs; over-engineering (extra patterns) is penalized.
- Many candidates over-index on inheritance (e.g., `Car extends Vehicle` everywhere) when composition is cleaner.
- Language-specific pitfalls (Java equals/hashCode, C++ copy/move, Python dunders) add friction under time pressure.

## 13. Interview Questions
1. **Q: What's the first thing you do when given a design problem?** A: Clarify requirements — scope, constraints, edge cases — then state assumptions aloud before designing.
2. **Q: Inheritance or composition for `BotPlayer`?** A: `BotPlayer extends Player` is legitimate IS-A (a bot *is a* player that makes a move), while the move *strategy* is composed (Strategy pattern).
3. **Q: How do you make the win check efficient?** A: Track per-row/col/diagonal counts; O(1) per move instead of O(9) scan each time.
4. **Q: Why an enum for `Piece`?** A: Fixed, compile-time-safe set (X, O, EMPTY); prevents invalid state and gives `switch`/pattern-matching.
5. **Q: How would you add an AI opponent?** A: Add `BotPlayer extends Player` overriding `chooseMove()` with a strategy (minimax or heuristic) — the design is open for extension (OCP).
6. **Q: How do you prevent invalid moves in a vending machine?** A: State pattern — transitions only allowed in valid states (Idle→Ready requires product selected; out-of-stock rejects).
7. **Q: LRU — why a HashMap + doubly-linked list?** A: O(1) lookup (map) + O(1) removal/insertion at head/tail (linked list); the map values point to nodes.
8. **Q: How does the library system support multiple search keys?** A: Maintain separate indexes (Map by title, by author) or a generic `Index<Key, Book>` — keeps O(1)/O(log n) lookups.
9. **Q: Where would you use the Observer pattern here?** A: Vending machine display / order status updates — listeners get notified on state change instead of polling.
10. **Q: How would you test Tic-Tac-Toe?** A: Unit-test `GameState` transitions and `MoveValidator`; simulate a full game asserting the winner; test invalid-move rejection.

## 14. Follow-Up Questions
1. **"Make it multi-threaded (concurrent orders)."** → Use `ConcurrentHashMap` for inventory/lookup, atomic counters, synchronized short critical sections; or make state immutable and copy-on-write.
2. **"Add a new product type without changing core classes."** → Ensure polymorphic seams (abstract `Product`, interface `Stockable`) so new types plug in (OCP).
3. **"What patterns did you use and why?"** → Name 2-3 explicitly: State (vending), Strategy (moves/validation), Factory (player/product creation), Observer (displays/notifications).
4. **"How would you make the cache thread-safe?"** → `ConcurrentHashMap` + synchronized on linked-list mutation (or a `ReentrantLock`); note that a simple `synchronized` on every op serializes and kills the O(1) advantage.
5. **"Your inventory went negative — how do you prevent it?"** → Encapsulate inventory with validation in the mutator (throw on insufficient stock) rather than exposing the field.

## 15. Coding Example

### Problem 1: Tic-Tac-Toe (Java)
```java
enum Piece { X, O, EMPTY }
enum GameState { IN_PROGRESS, X_WINS, O_WINS, DRAW }

class Board {
    private final Piece[][] grid = new Piece[3][3];
    Board() { for (var row : grid) java.util.Arrays.fill(row, Piece.EMPTY); }
    boolean isValid(int r, int c) { return r >= 0 && r < 3 && c >= 0 && c < 3 && grid[r][c] == Piece.EMPTY; }
    void set(int r, int c, Piece p) { grid[r][c] = p; }
    boolean isFull() { for (var row : grid) for (var p : row) if (p == Piece.EMPTY) return false; return true; }
    boolean line(int r, int c, int dr, int dc) {
        Piece p = grid[r][c];
        if (p == Piece.EMPTY) return false;
        return grid[r + dr][c + dc] == p && grid[r + 2*dr][c + 2*dc] == p;
    }
    Piece winner() {
        for (int r = 0; r < 3; r++) if (line(r, 0, 0, 1)) return grid[r][0];
        for (int c = 0; c < 3; c++) if (line(0, c, 1, 0)) return grid[0][c];
        if (line(0, 0, 1, 1)) return grid[0][0];
        if (line(0, 2, 1, -1)) return grid[0][2];
        return Piece.EMPTY;
    }
}

abstract class Player {                       // IS-A seam: polymorphism for human/bot
    protected final Piece piece;
    Player(Piece p) { piece = p; }
    abstract int[] chooseMove(Board b);
}

class Game {
    private final Board board = new Board();
    private final Player[] players = new Player[2];
    private int turn = 0;
    Game(Player a, Player b) { players[0] = a; players[1] = b; }
    GameState play() {
        while (true) {
            if (board.isFull()) return GameState.DRAW;
            int[] m = players[turn].chooseMove(board);
            board.set(m[0], m[1], players[turn].piece);
            Piece w = board.winner();
            if (w != Piece.EMPTY) return w == Piece.X ? GameState.X_WINS : GameState.O_WINS;
            turn = 1 - turn;
        }
    }
}
```

### Problem 2: LRU Cache (Java, O(1))
```java
import java.util.HashMap;
import java.util.Map;

class LRUCache<K, V> {
    private static class Node<K, V> { K key; V val; Node<K, V> prev, next; Node(K k, V v) { key = k; val = v; } }
    private final int capacity;
    private final Map<K, Node<K, V>> map = new HashMap<>();
    private final Node<K, V> head = new Node<>(null, null);   // sentinels
    private final Node<K, V> tail = new Node<>(null, null);
    LRUCache(int cap) { capacity = cap; head.next = tail; tail.prev = head; }

    private void unlink(Node<K, V> n) { n.prev.next = n.next; n.next.prev = n.prev; }
    private void linkToHead(Node<K, V> n) { n.next = head.next; n.prev = head; head.next.prev = n; head.next = n; }

    V get(K key) {
        Node<K, V> n = map.get(key);
        if (n == null) return null;
        unlink(n); linkToHead(n);          // most-recently-used moves to head
        return n.val;
    }
    void put(K key, V val) {
        Node<K, V> n = map.get(key);
        if (n != null) { n.val = val; unlink(n); linkToHead(n); return; }
        n = new Node<>(key, val); map.put(key, n); linkToHead(n);
        if (map.size() > capacity) {       // evict least-recently-used (tail)
            map.remove(tail.prev.key);
            unlink(tail.prev);
        }
    }
}
```

### Problem 3: Vending Machine (Java, State pattern)
```java
import java.util.EnumMap; import java.util.Map;

enum Product { COLA(100), CHIPS(80), WATER(50); final int price; Product(int p) { price = p; } }

class VendingMachine {
    private final Map<Product, Integer> inventory = new EnumMap<>(Product.class);
    private int balance = 0;
    private Product selected = null;

    VendingMachine() { for (Product p : Product.values()) inventory.put(p, 5); }

    void select(Product p) {
        if (inventory.get(p) == 0) throw new IllegalStateException("Out of stock");
        selected = p;                                // State transition: Idle -> Ready
    }
    void insert(int cents) {
        if (selected == null) throw new IllegalStateException("Select a product first");
        balance += cents;
    }
    int dispense() {
        if (selected == null || balance < selected.price) throw new IllegalStateException("Insufficient funds");
        inventory.put(selected, inventory.get(selected) - 1);
        int change = balance - selected.price;       // Encapsulation: balance only changes via methods
        balance = 0; selected = null;
        return change;                               // -> Idle
    }
}
```

### Problem 4: Library System (Java, search + checkout)
```java
import java.util.*; import java.util.stream.*;

class Book { final String title, author, isbn; int copies;
    Book(String t, String a, String i, int c) { title = t; author = a; isbn = i; copies = c; } }

class Library {
    private final List<Book> books = new ArrayList<>();
    private final Map<String, Book> byIsbn = new HashMap<>();          // O(1) lookup
    private final Map<String, List<Book>> byTitle = new HashMap<>();   // pre-built index

    void add(Book b) { books.add(b); byIsbn.put(b.isbn, b); byTitle.computeIfAbsent(b.title.toLowerCase(), k -> new ArrayList<>()).add(b); }
    List<Book> searchByTitle(String t) { return byTitle.getOrDefault(t.toLowerCase(), List.of()); }
    boolean checkout(String isbn) {
        Book b = byIsbn.get(isbn);
        if (b == null || b.copies == 0) return false;
        b.copies--; return true;
    }
    void returnBook(String isbn) { byIsbn.get(isbn).copies++; }
}
```

### Problem 5: Restaurant Ordering (Java, Command + Strategy)
```java
import java.util.*; import java.util.function.*;

interface Command { void execute(); }                      // Command pattern: queued actions
class Kitchen {
    void cook(String dish) { System.out.println("cooking " + dish); }
    void cleanUp() { System.out.println("cleaning"); }
}
class CookCommand implements Command {
    private final Kitchen kitchen; private final String dish;
    CookCommand(Kitchen k, String d) { kitchen = k; dish = d; }
    public void execute() { kitchen.cook(dish); }
}
class Order {
    private final List<Command> steps = new ArrayList<>();
    Order addStep(Command c) { steps.add(c); return this; }
    void process() { steps.forEach(Command::execute); }   // queued, undoable, replayable
}
class Waiter {
    private final Map<String, Predicate<Double>> paymentChecks = Map.of(  // Strategy: payment rules
        "card",  amt -> amt > 0,
        "cash",  amt -> amt > 0
    );
    boolean accept(String method, double amount) {
        return paymentChecks.getOrDefault(method, a -> false).test(amount);
    }
}
```

### Problem 6: Employee Hierarchy (Python, composition + polymorphism)
```python
class Employee:
    def __init__(self, name, salary): self.name, self.salary = name, salary
    def total_salary(self): return self.salary

class Manager(Employee):                       # IS-A, plus HAS-A team (composition)
    def __init__(self, name, salary):
        super().__init__(name, salary)
        self.team = []
    def add(self, e): self.team.append(e)
    def total_salary(self):                    # override: recursive aggregate
        return self.salary + sum(m.total_salary() for m in self.team)

mgmt = Manager("Alice", 100)
mgmt.add(Employee("Bob", 50)); mgmt.add(Manager("Carol", 80))  # composite hierarchy
print(mgmt.total_salary())                     # 230 — polymorphism through the tree
```

## 16. Industry Usage
- **Amazon SDE-I/II interviews** routinely include "Design a Parking Lot / Vending Machine / LRU Cache" — the Section 03/02 pair is the core drill.
- **Flipkart, Walmart, Uber, Google (L4/L5)** use similar single-system LLD prompts; Google tends to probe the *extensibility* (add a feature without touching core).
- **Take-homes** at startups reuse these exact systems (library, vending, ordering) as 1-2 hour assignments.
- The patterns used here (State, Strategy, Command, Observer) are the same ones production systems use (Spring state machines, payment orchestrators, caching layers), so interview answers transfer to on-the-job design reviews.

## 17. References
- *Cracking the Coding Interview* (McDowell) — OOP/design problems chapter.
- *System Design Interview* (Xu) — LLD process in Part 1.
- Refactoring Guru — pattern catalog for State/Strategy/Command/Observer.
- LeetCode design-problem set (LRU, etc.).
- Educative "Grokking the Low Level Design Interview".

## 18. Cheat Sheet
- Loop: clarify → nouns→classes → IS-A/HAS-A → sketch → code → test.
- Nouns = classes; verbs = methods; "is a" = inheritance; everything else = fields.
- Keep classes single-purpose (SRP); favor composition (HAS-A) unless true IS-A.
- Polymorphic seams: abstract `Player`, interface `Command`, `Predicate` payment rules.
- Patterns used: State (vending), Strategy (validation), Command (ordering), Observer (updates).
- State your assumptions before coding; narrate as you go.
- Always state time complexity (LRU O(1), search via index O(1)/O(log n)).
- End by naming 2-3 patterns and why (the interviewer's favorite closing question).

## 19. Quiz
1. The first step in any design problem is: a) Write code b) Clarify requirements c) Pick a pattern d) Draw UML → **b**
2. `BotPlayer extends Player` is: a) Composition b) Inheritance (IS-A) c) Aggregation d) Association → **b**
3. LRU cache's data structures: a) Two arrays b) HashMap + doubly-linked list c) TreeMap + stack d) Queue only → **b**
4. The Vending Machine solution uses which pattern? a) Observer b) State c) Proxy d) Bridge → **b**
5. To avoid invalid moves in a game, you should: a) Validate in the mutator b) Trust the caller c) Make moves public d) Skip validation → **a**
6. Pre-built title index makes `searchByTitle` roughly: a) O(n) b) O(log n) c) O(1) hash lookup d) O(n²) → **c**
7. Adding a new product type without editing core classes satisfies: a) SRP b) OCP c) LSP d) ISP → **b**
8. The Command pattern's key benefit: a) Faster execution b) Actions as queued/replayable/undoable objects c) Less memory d) Type safety → **b**
9. `Manager.total_salary` recursively summing the team is an example of: a) State b) Composite (tree traversal) c) Adapter d) Factory → **b**
10. Making the LRU thread-safe while keeping O(1) is best done with: a) Synchronize every op b) ConcurrentHashMap + guarded list c) Copy whole cache d) A global lock → **b**

## 20. Flashcards
- **Q: Design loop?** → **A:** Clarify → nouns→classes → IS-A/HAS-A → sketch → code → test.
- **Q: When to use inheritance?** → **A:** True IS-A with behavior reuse; otherwise composition.
- **Q: LRU internals?** → **A:** HashMap to nodes + doubly-linked list (head = MRU, tail = LRU).
- **Q: Vending pattern?** → **A:** State pattern for valid transitions + encapsulated inventory.
- **Q: Command pattern?** → **A:** Actions as objects → queue, replay, undo.
- **Q: How to add a product without editing core?** → **A:** Polymorphic seam (abstract Product) → OCP.
- **Q: Why narrate design before code?** → **A:** Interviewers grade the process, not just output.
- **Q: Concurrency for the cache?** → **A:** ConcurrentHashMap + guarded linked list.

## 21. Revision
For any OOP coding prompt: clarify scope and state assumptions, extract nouns into classes (SRP), decide IS-A (inherit) vs HAS-A (compose), sketch relationships, then code and test one scenario. Canonical patterns: LRU = HashMap→Node + doubly-linked list (O(1) get/put, evict tail); Vending = State transitions + encapsulated inventory; Ordering = Command objects for queue/replay; Library = pre-built indexes for O(1) search; HR = composite tree with polymorphic `total_salary`. Close by naming the 2-3 patterns used and why (OCP/Strategy/State) — interviewers always ask. Never jump to code before sketching classes; never over-engineer.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Design a LRU cache / vending machine / library / game" | 15 Coding Example (solutions) |
| "What's your design process?" | 8 / 9 Internal Working / 18 Cheat Sheet |
| "Which patterns did you use and why?" | 15 Coding / 18 Cheat Sheet |
| "Make it thread-safe / add a product type" | 14 Follow-Up Questions |
| "How would you test this design?" | 13 Interview Questions |
| "What's the time complexity?" | 10 Time Complexity |
