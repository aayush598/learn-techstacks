# Low-Level Design (LLD) Interview Guide

> **TL;DR**: LLD is the interview round where you turn a one-line requirement ("design a parking lot") into a full object model — requirements → class diagram → SOLID-compliant code — and the rubric rewards *process* (assumptions, edge cases, trade-offs) as much as the code.

## 1. Why Does This Exist?
LLD exists because companies need to know whether you can produce **maintainable, testable, extensible code** for a single system — the exact daily work of an SDE. Unlike a high-level system design (boxes and queues) or an algorithm question (one function), LLD probes whether you can *model a domain*: discover entities, set relationships, apply SOLID and patterns, handle edge cases, and write clean code in 45 minutes. It's the closest proxy for "can this person design software other people can maintain?" that a short interview offers.

## 2. How Does It Work?
The LLD loop (repeat for every problem):
1. **Clarify requirements** — scope, actors, constraints (multi-floor? payment? valet?).
2. **Identify entities** — nouns → classes.
3. **Map relationships** — IS-A (inherit/interface), HAS-A (fields), dependencies.
4. **Design the class skeleton** — fields, methods, interfaces; a rough diagram.
5. **Apply SOLID + patterns** — where behavior varies, add seams.
6. **Write code** for the core flows.
7. **Discuss trade-offs, edge cases, extensibility.**
Interviewers grade all seven, not just step 6.

## 3. When Is It Used?
- **Amazon SDE-I/II**: LLD is a standard screen/loop round (Parking Lot, Elevator, Splitwise).
- **Flipkart / Walmart / Uber / Google L4-L5**: LLD rounds with variations (BookMyShow, Chess, Snake & Ladder, Ride Hailing).
- **Indian product companies** (Swiggy, Zomato, Paytm, Razorpay): heavy LLD emphasis.
- **Backend/application roles** generally: 1-2 LLD questions in the loop.

## 4. Why Wasn't Another Approach Chosen?
LLD problems could be answered with pure data structures (a `Map` and a while-loop), but that fails the *design* test. Alternatives like "god class" implementations (one class doing everything) or procedural scripts are rejected because they don't scale or change — the entire point is demonstrating **object modeling**: responsibilities split by SRP, extension via OCP seams, dependency on abstractions (DIP) so tests can mock. The "right" answer isn't one canonical design — it's a design whose *rationale* you can defend. This guide teaches the process because process is what's scored.

## 5. Intuition
Designing a system is like **hiring staff for a restaurant**: the requirement "serve food" turns into roles (host, chef, cashier, cleaner — each with one job = SRP), a hierarchy (head chef manages cooks = composition), and standard ways to swap people ("any chef can cook any dish" = an interface). You wouldn't hire one person to do everything (god class) or chain everyone to one employee's habits (tight coupling). LLD is that staffing exercise in code: name the roles, give each a clear job, and let the manager (a small orchestrator) delegate.

## 6. Real-World Analogy
A **hotel front desk**: when a guest arrives (the client), the desk (the orchestrator/controller) does a tiny bit of coordination and delegates everything: the bellhop (a class) handles luggage, housekeeping (another class) prepares the room, the billing system (a service) charges the card. Each department has one responsibility and communicates through the desk, not by calling each other directly (low coupling). If the hotel adds a spa (a new feature), they just open a new department that implements the same "service" interface — nobody rewrites the lobby (OCP). That's LLD.

## 7. Formal Definition
Low-Level Design (LLD), also called machine-coding or object design, is the practice of producing a *class-level* design for a single software module or small system: a set of classes, interfaces, and their relationships (inheritance, composition, association) that satisfies functional requirements, adheres to design principles (SOLID, DRY, YAGNI), and can be implemented, tested, and extended. Evaluation dimensions: correctness, object decomposition, abstraction quality, extensibility, edge-case handling, and code quality.

## 8. Example (full walkthrough — Parking Lot)
**Requirement**: "Design a parking lot with multiple floors, different spot types, vehicle types, and payments."
1. **Clarify**: multiple floors (say 3), spot types (Compact, Large, Motorcycle), vehicle types (Car, Motorcycle, Truck), per-hour billing, exit with payment, display board showing free spots.
2. **Entities (nouns)**: ParkingLot, Floor, ParkingSpot, Vehicle, Ticket, Payment, DisplayBoard.
3. **Relationships**: ParkingLot HAS-A list of Floors; Floor HAS-A list of Spots; Vehicle IS-A (abstract) → Car/Truck/Motorcycle; Ticket HAS-A Spot + Vehicle + entryTime; ParkingLot HAS-A DisplayBoard.
4. **Skeleton**:
```
ParkingLot --1..*--> Floor --1..*--> ParkingSpot
ParkingLot --1--> DisplayBoard (Observer of spot changes)
Ticket --1--> ParkingSpot
Ticket --1--> Vehicle
Vehicle (abstract) <- Car, Truck, Motorcycle
SpotAssignmentStrategy (interface) <- NearestToEntry, FirstAvailable
Payment (interface) <- Cash, Card, UPI
```
5. **SOLID + patterns**: SpotAssignment is a **Strategy** (swap algorithms); DisplayBoard is an **Observer** of spot availability; `ParkingSpot` exposes `isFree/occupy/release` (encapsulation); vehicle type → spot type via an abstract `Vehicle.getSpotType()` (polymorphism, OCP).
6. **Code** (Problem 1 below): core flows — `park(vehicle)`, `exit(ticket)`, `notifyDisplay()`.
7. **Trade-offs/edges**: what if no spot of the right type? (return null / throw). Expired ticket? (charge a max or re-enter). Thread-safety of simultaneous park/exit? (synchronize per-floor or atomic spot assignment). Display staleness? (update on every occupy/release event).

## 9. Internal Working (the LLD rubric and how to maximize it)
1. **Requirements clarity** (20%): ask 3-5 clarifying questions; restate scope. Interviewers dock candidates who design a valet system when a self-park was meant.
2. **Object model** (25%): correct entities, right relationships, no god objects, appropriate inheritance vs composition.
3. **SOLID/pattern application** (20%): name the seams — where would a new feature plug in? (OCP, DIP).
4. **Edge cases** (15%): out-of-stock, null, concurrency, boundary values, failure modes.
5. **Code quality** (20%): clean, compilable-in-head, idiomatic, with tests/assertions if time allows.
Maximize by *narrating*: say "I'm extracting Vehicle as abstract so a new vehicle type won't touch core" — interviewers reward visible reasoning.

## 10. Time Complexity
- The design itself is O(n) in entities; the *discussion* dominates the clock (45 min).
- Implementation hotspots worth stating: park/exit with indexed spots O(1) (or O(n) scan if no index); display update O(1) per event; payment O(1).
- Always mention the cost of a naive approach vs an indexed one (e.g., "finding a free spot is O(n) unless we maintain a per-type free list → O(1)").

## 11. Advantages
- Highest-yield interview round for SDE-I/II at product companies — one strong LLD answer often carries the loop.
- Teaches the object-modeling skill that transfers directly to production design reviews.
- Reusable process: same loop for parking, elevators, games, ordering, splitwise, etc.
- Distinguishes candidates who *apply* SOLID from those who merely recite it.

## 12. Disadvantages
- Time pressure biases toward jumping into code; the rubric punishes that (process is graded).
- No canonical answer → candidates feel "unsure if it's right"; confidence comes from defending trade-offs.
- Easy to over-engineer (patterns everywhere) or under-engineer (god class); calibrating to scope is hard.
- Language details (Java equals/hashCode, C++ ownership, Python dunders) add friction mid-design.

## 13. Interview Questions
1. **Q: How do you start an LLD problem?** A: Clarify scope and constraints, restate them, then extract entities — never code before requirements are locked.
2. **Q: What's the difference between a class diagram and a design?** A: The diagram shows entities and relationships; the design is those relationships *justified* (why composition, why an interface) plus behaviors and edge cases.
3. **Q: When do you use an abstract class vs an interface in a design?** A: Shared base behavior/state → abstract class; a capability contract or need for multiple implementations → interface. In LLD, interfaces at *change points* (assignment strategy, payment).
4. **Q: How do you handle concurrency in a parking lot?** A: Guard spot assignment (per-floor lock or atomic "occupy" with CAS); keep counters atomic; the display updates are read-mostly so a lock-free snapshot or observer with a volatile flag suffices.
5. **Q: How would you add electric-vehicle charging?** A: Add an `EVSpot extends ParkingSpot` or a `ChargingFeature` composed into a spot (favor composition), implement `Chargeable` — no core change (OCP).
6. **Q: What edge cases do you test?** A: Full lot, wrong spot type, invalid ticket, double exit, expired ticket, payment failure, concurrent bookings, zero inventory.
7. **Q: Where does the Observer pattern appear?** A: The display board subscribes to spot-availability changes and updates on `occupy/release` events instead of polling.
8. **Q: How do you keep search/assignment fast?** A: Index free spots per floor/type (e.g., `EnumMap<SpotType, Deque<ParkingSpot>>`) → O(1) assignment.
9. **Q: What if the interviewer says "make it scalable"?** A: Move state to a DB, shard by lot, cache availability — but clarify that LLD is single-node; scaling belongs to HLD.
10. **Q: How would you test this design?** A: Unit-test each entity (Spot, Ticket, Payment) with mocks for the interfaces; integration-test park→pay→exit; test edge cases (full, wrong type, concurrent).

## 14. Follow-Up Questions
1. **"What patterns did you use and why?"** → Strategy (assignment/payment), Observer (display), Factory (ticket/vehicle creation) — each tied to a change point.
2. **"Add feature X without touching core classes."** → Point at the seam: new implementation of an existing interface (OCP); e.g., add `EVSpot` or `ValetService` implementing the same contract.
3. **"Your system is slow under load."** → Index free spots, avoid O(n) scans, keep the display updated via events not polling, offload payments async.
4. **"What breaks if two people exit at once?"** → Ticket lookup and payment are independent; the risk is double-releasing a spot — make `release` idempotent/atomic.
5. **"Would you store this in memory or a DB?"** → For LLD, in-memory is fine and expected; mention that a DB with transactional spot state is the production upgrade.

## 15. Coding Example

### Parking Lot (Java — core flows)
```java
import java.util.*;

enum SpotType { COMPACT, LARGE, MOTORCYCLE }

abstract class Vehicle {                       // IS-A seam + polymorphic spot needs
    final String plate;
    Vehicle(String p) { plate = p; }
    abstract SpotType requiredSpot();
}
class Car extends Vehicle { Car(String p) { super(p); } public SpotType requiredSpot() { return SpotType.LARGE; } }
class Motorcycle extends Vehicle { Motorcycle(String p) { super(p); } public SpotType requiredSpot() { return SpotType.MOTORCYCLE; } }

class ParkingSpot {
    final int id; final SpotType type; Vehicle vehicle; long entryMs;
    ParkingSpot(int i, SpotType t) { id = i; type = t; }
    boolean isFree() { return vehicle == null; }
    void occupy(Vehicle v) { vehicle = v; entryMs = System.currentTimeMillis(); }
    Vehicle release() { Vehicle v = vehicle; vehicle = null; return v; }
}

class Ticket { final ParkingSpot spot; final Vehicle vehicle; final long entryMs;
    Ticket(ParkingSpot s, Vehicle v) { spot = s; vehicle = v; entryMs = s.entryMs; }
    long durationMs() { return System.currentTimeMillis() - entryMs; }
}

interface SpotAssignmentStrategy { Optional<ParkingSpot> find(Floor floor, Vehicle v); }
class FirstAvailable implements SpotAssignmentStrategy {
    public Optional<ParkingSpot> find(Floor floor, Vehicle v) {           // O(n)
        for (ParkingSpot s : floor.spots()) if (s.isFree() && s.type == v.requiredSpot()) return Optional.of(s);
        return Optional.empty();
    }
}
class IndexedFirstAvailable implements SpotAssignmentStrategy {           // O(1) with index
    private final Map<SpotType, ArrayDeque<ParkingSpot>> free = new EnumMap<>(SpotType.class);
    public Optional<ParkingSpot> find(Floor floor, Vehicle v) {
        ArrayDeque<ParkingSpot> q = free.get(v.requiredSpot());
        return q == null || q.isEmpty() ? Optional.empty() : Optional.of(q.poll());
    }
    void release(ParkingSpot s) { free.computeIfAbsent(s.type, k -> new ArrayDeque<>()).add(s); }
}

class Floor { private final List<ParkingSpot> spots; final int number;
    Floor(int n, List<ParkingSpot> s) { number = n; spots = s; }
    List<ParkingSpot> spots() { return spots; } }

class DisplayBoard {                                  // Observer of availability
    private final Map<SpotType, Integer> freeCount = new EnumMap<>(SpotType.class);
    void onOccupy(SpotType t) { freeCount.merge(t, -1, Integer::sum); }
    void onRelease(SpotType t) { freeCount.merge(t, 1, Integer::sum); }
    String render() { return "free=" + freeCount; }
}

class ParkingLot {                                    // orchestrator: delegates, no god logic
    private final List<Floor> floors;
    private final SpotAssignmentStrategy strategy;
    private final DisplayBoard display = new DisplayBoard();

    ParkingLot(List<Floor> f, SpotAssignmentStrategy s) { floors = f; strategy = s; }

    Optional<Ticket> park(Vehicle v) {
        for (Floor floor : floors) {
            Optional<ParkingSpot> s = strategy.find(floor, v);
            if (s.isPresent()) { s.get().occupy(v); display.onOccupy(v.requiredSpot()); return Optional.of(new Ticket(s.get(), v)); }
        }
        return Optional.empty();                       // full -> caller handles
    }
    long exit(Ticket t) {
        ParkingSpot spot = t.spot;
        Vehicle v = spot.release();                    // idempotent: safe if called twice
        display.onRelease(v.requiredSpot());
        return t.durationMs();
    }
}
```

### Snake and Ladder (Python — board game with OOP)
```python
import random

class Player:
    def __init__(self, name): self.name, self.pos = name, 0

class Board:
    def __init__(self, snakes, ladders):
        self.snakes, self.ladders = snakes, ladders
    def move(self, player, steps):
        nxt = player.pos + steps
        if nxt > 100: return                   # must land exactly
        if nxt in self.snakes: nxt = self.snakes[nxt]
        elif nxt in self.ladders: nxt = self.ladders[nxt]
        player.pos = nxt

class Game:
    def __init__(self, board, players): self.board, self.players = board, players
    def play(self, dice=lambda: random.randint(1, 6)):
        while True:
            for p in self.players:
                self.board.move(p, dice())
                if p.pos == 100: return p.name

game = Game(Board({98: 5, 66: 22}, {7: 28, 51: 88}), [Player("A"), Player("B")])
print(game.play())
```

### Splitwise / Expense Splitter (Java — entity relationships)
```java
import java.util.*;

class User { final String id; final String name; User(String i, String n) { id = i; name = n; } }

class Expense { final String paidBy; final double amount; final List<String> splitAmong; final Map<String, Double> shares;
    Expense(String paidBy, double amount, List<String> users, String splitType) {
        this.paidBy = paidBy; this.amount = amount; this.splitAmong = users; this.shares = compute(users, amount, splitType);
    }
    private Map<String, Double> compute(List<String> users, double amount, String splitType) {
        Map<String, Double> m = new LinkedHashMap<>();
        if (splitType.equals("EQUAL")) users.forEach(u -> m.put(u, amount / users.size()));
        else { /* PERCENT/EXACT handled by a Strategy — see below */ }
        return m;
    }
}

class BalanceSheet {   // HAS-A map of balances; settle() nets creditor/debtor
    private final Map<String, Double> balances = new HashMap<>();
    void record(Expense e) {
        balances.merge(e.paidBy, +e.amount, Double::sum);
        e.shares.forEach((u, amt) -> balances.merge(u, -amt, Double::sum));
    }
    List<String> settle() {   // print minimal transactions (greedy)
        List<String> out = new ArrayList<>();
        balances.forEach((k, v) -> { if (v > 0) out.add(k + " is owed " + v); else if (v < 0) out.add(k + " owes " + (-v)); });
        return out;
    }
}
```

## 16. Industry Usage
- **Amazon**: "Design a Parking Lot" is a documented standard LLD screen; LLD interviews at L5 probe extensibility (add EV charging, valet).
- **Google**: LLD (called "OOD" at L4/L5) uses games/boards (Snake & Ladder, Chess, Poker) and API-module designs; graders reward pattern usage and edge cases.
- **Flipkart/Walmart**: "Design BookMyShow / a grocery delivery / Splitwise" with explicit pattern questions as follow-ups.
- **Uber/OLA**: ride-hailing mini-models (trip, driver allocation) — Strategy + Observer heavy.
- **Production carry-over**: the patterns here (Strategy, Observer, State, Command, Factory) are the same building blocks in real services, so LLD skill transfers to design reviews at the same companies.

## 17. References
- Alex Xu, *System Design Interview — An Insider's Guide*, Part 1 (LLD process, object design).
- Robert C. Martin, *Clean Architecture* / *Agile Principles, Patterns, and Practices in C#* (SOLID origin).
- Erich Gamma et al., *Design Patterns* (GoF) — pattern catalog for LLD solutions.
- *Cracking the Coding Interview* (McDowell) — OOD/design questions.
- Grokking the Low-Level Design Interview (Educative).
- Workat.tech / InterviewBit LLD problem sets.

## 18. Cheat Sheet
- Process: clarify → entities → relationships → skeleton → SOLID/patterns → code → trade-offs.
- Nouns→classes; verbs→methods; IS-A→inherit; HAS-A→compose.
- No god classes: one responsibility per class (SRP).
- Put interfaces at change points (assignment, payment, splitting) → OCP + DIP.
- Name the patterns you used and why — the interviewer will ask.
- Edge cases: full/null/out-of-stock/duplicate/expired/concurrency.
- State complexity (indexed free-spot assignment → O(1)).
- LLD = in-memory single node; scaling belongs to HLD (say it).
- Narrate your reasoning as you go; graded on process.
- End with how you'd test the design.

## 19. Quiz
1. The first step of LLD is: a) Code b) Clarify requirements c) Choose patterns d) Draw diagram → **b**
2. "Vehicle" modeled as abstract with requiredSpot() is an example of: a) SRP b) Polymorphism/OCP c) LSP d) ISP → **b**
3. The DisplayBoard updating on spot events uses: a) Strategy b) Observer c) Command d) Factory → **b**
4. A god class violates: a) SRP b) DRY c) YAGNI d) LSP → **a**
5. Indexed free-spot assignment makes parking: a) O(n) b) O(1) c) O(log n) d) O(n²) → **b**
6. Adding `EVSpot` without touching core classes satisfies: a) SRP b) OCP c) ISP d) LSP → **b**
7. Interfaces belong at: a) Every class b) Change points c) Only abstract classes d) Never → **b**
8. In Snake & Ladder, landing exactly on 100 is: a) Optional b) Required c) A ladder rule d) Ignored → **b**
9. Which round is LLD? a) HLD b) Single-module object design c) Algorithm-only d) Behavioral → **b**
10. To defend a design you should: a) Only show code b) Explain trade-offs and alternatives c) Avoid mentioning patterns d) Skip edge cases → **b**

## 20. Flashcards
- **Q: LLD loop?** → **A:** Clarify → entities → relationships → skeleton → SOLID → code → trade-offs.
- **Q: Where do interfaces go?** → **A:** At change points (strategies, payments) → OCP/DIP.
- **Q: Strategy vs Observer in Parking Lot?** → **A:** Strategy = spot assignment; Observer = display updates.
- **Q: How to make assignment O(1)?** → **A:** Index free spots per floor/type.
- **Q: God class violation?** → **A:** SRP — split into focused classes.
- **Q: Add EV charging?** → **A:** New spot implementation / composed feature — no core change.
- **Q: What's graded?** → **A:** Process (requirements, edge cases, trade-offs) + code quality.
- **Q: LLD vs HLD?** → **A:** LLD = single-module class design; HLD = distributed architecture.

## 21. Revision
Run the LLD loop: clarify scope, extract entities (nouns), set IS-A (inherit) vs HAS-A (compose), sketch the skeleton, add interfaces at change points (Strategy, Observer, Factory, State), code the core flows, and close with edge cases + trade-offs + how you'd test. Canonical moves: `Vehicle` abstract → `Car extends Vehicle`; `SpotAssignmentStrategy` interface → O(1) indexed impl; `DisplayBoard` observes spot events; orchestration lives in `ParkingLot` (no god logic). Remember to state complexity, name 2-3 patterns and their purpose, keep LLD in-memory (say scaling is HLD), and narrate the whole journey — the rubric scores the process as much as the code.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Design a Parking Lot / Elevator / Game / Splitwise" | 8 Example / 15 Coding Example |
| "What's your LLD process?" | 2 / 9 Internal Working |
| "Which patterns did you use?" | 8 / 18 Cheat Sheet |
| "How do you handle edge cases / concurrency?" | 8 / 13 Interview Questions |
| "Add a feature without touching core" | 14 Follow-Up Questions |
| "What's the time complexity of assignment?" | 10 Time Complexity |
| "How would you test this?" | 13 Interview Questions |
