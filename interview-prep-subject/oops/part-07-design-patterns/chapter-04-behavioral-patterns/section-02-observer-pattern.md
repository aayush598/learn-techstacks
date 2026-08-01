# Observer Pattern

> **TL;DR**: The Observer pattern defines a **one-to-many dependency** where a subject notifies all its registered observers of state changes — it exists to decouple *event producers* from *event consumers*, so publishers broadcast changes without knowing who (or how many) is listening.

## 1. Why Does This Exist?
When one object's state changes and *many other objects* need to react, the naive approach is **tight coupling**: the subject directly calls each dependent's method (`emailService.send(...)`, `auditLog.record(...)`, `dashboard.refresh(...)`). This fails because:
1. **The subject knows every dependent's class and method** — adding a new dependent edits the subject (Open-Closed violation).
2. **The dependent list is hard-coded** — it can't grow, shrink, or change at run time (a notification's subscribers change constantly).
3. **The subject and dependents can't evolve independently** — a change to any dependent's API ripples into the subject.

The Observer pattern exists to **invert that coupling**: the subject knows only the `Observer` *interface*, keeps a *dynamic list* of observers, and broadcasts a notification. Observers register/unregister themselves at run time. Adding a new listener means writing a class that implements `Observer` and subscribing it — *zero changes* to the subject (Open-Closed). It's the publish/subscribe contract that powers event-driven systems: GUI event listeners, reactive programming, message-queue consumers, and framework callback lists.

## 2. How Does It Work?
```
Subject ──notifies──> Observer (interface: update(event))
  ▲                          ▲
  │ holds                     │ implements
  List<Observer>      ConcreteObserverA/B/C
```
Participants:
1. **Subject** (a.k.a. Observable) — holds a list of observers; `attach(o)`, `detach(o)`, `notifyObservers(event)`.
2. **Observer** — the interface with `update(event)`.
3. **ConcreteSubject** — extends the subject with state; on state change calls `notifyObservers()`.
4. **ConcreteObserver** — registers itself; on `update(event)`, reacts.

```java
interface Observer { void update(String event); }

class WeatherStation implements Subject {          // ConcreteSubject
    private final List<Observer> observers = new ArrayList<>();
    private int temperature;
    public void attach(Observer o) { observers.add(o); }
    public void detach(Observer o) { observers.remove(o); }
    public void setTemperature(int t) {
        this.temperature = t;
        notifyObservers("temp=" + t);               // broadcast on change
    }
    private void notifyObservers(String event) {
        for (Observer o : observers) o.update(event);
    }
}

class PhoneDisplay implements Observer {            // ConcreteObserver
    public void update(String event) { System.out.println("Phone: " + event); }
}
class WebDashboard implements Observer {
    public void update(String event) { System.out.println("Web: " + event); }
}
// Usage
WeatherStation ws = new WeatherStation();
ws.attach(new PhoneDisplay());
ws.attach(new WebDashboard());
ws.setTemperature(32);   // both displays react; station knows neither class
```

## 3. When Is It Used?
- **State change must trigger many independent reactions**: UI refresh, logging, analytics, alerts, cache invalidation.
- **GUI event handling**: button clicks, mouse moves — Swing/AWT listeners, Android listeners, browser DOM events.
- **Reactive/propagated state**: Redux/MobX/Flux stores, reactive streams, live-updating dashboards, stock tickers.
- **Message-queue / pub-sub backends**: consumers subscribe to topics (a distributed observer).
- **Notification fan-out**: order-placed → email + SMS + push + audit.
- **JDK**: `java.util.Observable`/`Observer` (deprecated), `PropertyChangeSupport` (JavaBeans), `EventListenerList` in Swing, `CompletableFuture`/`CompletionStage` (observer-ish callbacks).
- **Interviews**: "notify multiple components when X changes", "decouple sender from receivers", "publish/subscribe" → Observer.

## 4. Why Wasn't Another Approach Chosen?
- **Direct hard-coded calls from the subject** (`emailService.send(...)` in the subject): rejected — couples subject to every dependent's class/method (Open-Closed violation), can't vary the listener set at run time, and a change to any dependent ripples into the subject.
- **Polling** (dependents periodically check the subject's state): rejected — wasteful (constant polling even when nothing changes), introduces latency (only notices changes on the next poll), and can't push rich event data. Observer is *event-driven push*: immediate, and only when something happens. This "push vs pull" argument is the pattern's core rationale.
- **Callbacks (pass a function)**: valid — callbacks are a *lightweight* observer (register a `Consumer<Event>` instead of a full Observer object). Modern Java prefers `Consumer`/`CompletableFuture` callbacks for simple cases; the Observer *pattern* adds the formal interface + attach/detach lifecycle, which matters when observers need identity, removal, or priority.
- **Message queue / event bus (a separate broker)**: chosen when producers and consumers must be *fully decoupled* (different processes, async, guaranteed delivery). The Observer is the in-process, direct-notification variant; an event bus is the distributed/async variant (Kafka, RabbitMQ) — Observer's architectural cousin.
- **Listener lists via framework (Swing `EventListenerList`, Spring events)**: these ARE Observer implemented with type safety — chosen over hand-rolled observer lists for framework integration.

## 5. Intuition
Observer is **a mailing list / newsletter subscription**. The publisher (subject) keeps a subscriber list (observers). When new content arrives (state change), the publisher *pushes* the newsletter to every subscriber — it doesn't know or care who's subscribed, how many, or what they'll do with it. Subscribers join/leave freely at run time. Nobody polls the publisher's website every minute (polling); they get pushed the news the moment it happens. The publisher's only contract: "I send to everyone on my list."

## 6. Real-World Analogy
A **sports news desk and its subscribers**. The desk (subject) publishes a score update (event). It has a subscriber list (observers): the mobile app, the website ticker, the TV broadcast, the betting system. The desk just *broadcasts* "SCORE: 2-1"; each subscriber reacts in its own way — the app pushes a notification, the ticker scrolls, the bettor settles a bet. The desk never calls the app's push method or the bettor's settle method directly; it only knows "everyone on my list gets the update." Adding a new subscriber (a new sportsbook) = one more subscription, zero changes to the desk.

## 7. Formal Definition
> **Observer** (a.k.a. Dependents, Publish-Subscribe): Define a **one-to-many dependency** between objects so that when one object changes state, all its **dependents are notified and updated automatically**. (GoF, p. 293)
>
> Participants: **Subject** (knows its observers; provides attach/detach; notifies on state change), **Observer** (the interface with `update`), **ConcreteSubject** (holds state; calls notify on change), **ConcreteObserver** (registers and reacts). Key property: the subject knows *only* the Observer interface — no concrete dependent classes.

## 8. Example
A **stock-ticker fan-out** — order events push to many subscribers:
```java
record Order(String id, double amount) {}

interface OrderListener { void onOrder(Order o); }     // Observer

class OrderService {                                    // Subject
    private final List<OrderListener> listeners = new CopyOnWriteArrayList<>();
    void subscribe(OrderListener l) { listeners.add(l); }
    void unsubscribe(OrderListener l) { listeners.remove(l); }
    void placeOrder(Order o) {
        System.out.println("[SERVICE] order placed: " + o);
        for (OrderListener l : listeners) l.onOrder(o);   // push
    }
}

class EmailNotifier implements OrderListener { public void onOrder(Order o){ System.out.println("  -> email sent"); } }
class AuditLog implements OrderListener { public void onOrder(Order o){ System.out.println("  -> audit recorded"); } }
class FraudCheck implements OrderListener { public void onOrder(Order o){ System.out.println("  -> fraud screen run"); } }

// Client: subscribers join/leave at run time
OrderService svc = new OrderService();
svc.subscribe(new EmailNotifier());
svc.subscribe(new AuditLog());
OrderListener fraud = new FraudCheck();
svc.subscribe(fraud);
svc.placeOrder(new Order("A1", 250));
svc.unsubscribe(fraud);                       // runtime unregister
svc.placeOrder(new Order("A2", 90));          // fraud check no longer runs
```
- The service never names a concrete listener; listeners attach/detach at run time; adding "PushNotifier" = one class + one `subscribe` call.

## 9. Internal Working
1. **Registration**: observers call `subject.attach(observer)` (or DI auto-wires a listener list). The subject stores them in a list.
2. **State change**: the subject's method (`placeOrder`, `setTemperature`) mutates state.
3. **Notification**: the subject iterates its listener list calling `listener.onEvent(...)` — a *push* (data passed) or *pull* (observer reads the subject's state via a getter) model. GoF describes both; modern practice pushes an event object (decoupled payload).
4. **Reaction**: each observer reacts independently — and observers *must not* block or mutate the subject during notification (re-entrancy).
5. **Unregistration**: observers detach themselves (when views close, when no longer interested).

**Concurrency**: iterating a listener list while another thread attaches/detaches is a classic bug. Production solutions: `CopyOnWriteArrayList` (snapshot iteration — safe, cheap reads), synchronized lists, or event-loop confinement (single thread owns the subject). Notification order is typically registration order (or priority if supported).

**Failure isolation**: one observer throwing must not stop notification to the others — production subjects wrap each `observer.update(...)` in try/catch (or rely on the framework's listener-dispatch safety).

## 10. Time Complexity
- **attach/detach**: O(1) amortized (list add/remove; `CopyOnWriteArrayList` add is O(N) copy but reads are O(1)).
- **notify**: O(N) where N = number of observers — the subject must visit each listener. This is inherent (each observer must be told); it's why very large fan-outs use async batching.
- **Observer reaction**: the observer's own cost, plus (with push) the event object construction O(E).
- **Polling comparison**: polling is O(N) checks *per poll interval* even with no changes; Observer notifies only on change (O(N) per *event*). That's the asymptotic/operational win of push over pull.
- **Memory**: O(N) listener references — a leak if observers are never detached (the classic memory-leak trap).

## 11. Advantages
- **Open-Closed**: the subject never changes when new observers appear (add a class + subscribe).
- **Loose coupling**: subject knows only the Observer interface; observers know the subject's type (or even only an event).
- **Runtime dynamics**: subscribe/unsubscribe at run time — the listener set reflects live state.
- **Push immediacy**: dependents react *the moment* state changes (no polling latency).
- **Independent reactions**: each observer reacts in its own way; failures are isolated (with proper exception handling).
- **One-to-many fan-out**: single source of truth broadcasts to any number of consumers.

## 12. Disadvantages
- **Unexpected updates**: a subject can have many observers with unclear ordering/dependencies — "who else is listening?" is hard to answer; cascading updates are hard to reason about.
- **No error propagation contract**: a failing observer (without isolation) breaks notification to all.
- **Memory leaks**: observers never detached → the subject holds strong references forever (the GUI/reactive classic leak; fixed with weak references or explicit detach).
- **Notification storms**: many observers + frequent state changes = performance cliffs (mitigated with coalescing/batching).
- **Re-entrancy bugs**: an observer triggering another state change during notification can cause infinite recursion or inconsistent iteration (mitigated with snapshot lists / guard flags).
- **Order not guaranteed** (by default) — if order matters, you must add priority, adding complexity.

## 13. Interview Questions
1. **Q: What is the Observer pattern?** A: A behavioral pattern defining a one-to-many dependency where a subject notifies all registered observers of state changes — decoupling the event producer from its consumers through an Observer interface.
2. **Q: What problem does it solve?** A: The tight coupling of "subject directly calls each dependent" (Open-Closed violation, hard-coded listener set, no runtime dynamics) and the waste/latency of polling. Observer pushes change events to a dynamic, decoupled listener list.
3. **Q: Push vs pull — which does Observer use and when?** A: Push (subject sends the event data: `update(event)`) — decouples observers from reading subject internals, preferred when the payload is small/known. Pull (observer reads the subject's getters) — works when the subject is already shared; requires observers to know the subject's API. GoF supports both; modern practice favors pushing an event object.
4. **Q: Why is `java.util.Observable` deprecated? (Tricky)** A: Because it's a *class* (you must extend it — single-inheritance cost), it leaks a `Vector` (synchronized, slow), its API is clunky, and it can't convey rich event payloads. Modern practice: use a custom `Subject` interface + a listener list (`CopyOnWriteArrayList`) or framework events (Spring `ApplicationEvent`), or reactive streams.
5. **Q: How is Observer different from Mediator?** A: Observer is *one-to-many broadcast* (a subject pushes to its observer list; observers are anonymous to the subject). Mediator is *many-to-many centralized coordination* (peers communicate *through* a mediator, which knows all of them). Observer = fan-out; Mediator = hub.
6. **Q: Observer vs pub/sub (message queue)? (Production)** A: Observer is *in-process, direct, synchronous* notification (subject holds observer references). Pub/sub (Kafka, RabbitMQ) is *decoupled via a broker*, possibly cross-process and async. Observer is the simple form; pub/sub adds broker-mediated, distributed, durable, async delivery. Choose Observer for in-process fan-out; a broker when producers/consumers are separate services.
7. **Q: How do you make the observer list thread-safe?** A: Use `CopyOnWriteArrayList` (snapshot iteration — safe concurrent attach/detach with O(1) reads), a synchronized list, or confine notification to one thread (event loop). Never iterate a plain `ArrayList` while another thread mutates it — `ConcurrentModificationException`.
8. **Q: How do you prevent an observer's exception from killing notification? (Production)** A: Wrap each `listener.onEvent(...)` in try/catch (log + continue) so one bad observer doesn't block the rest. Production frameworks (Swing `EventListenerList`, Spring events) do exactly this.
9. **Q: How do you avoid infinite recursion / re-entrancy?** A: Use a *snapshot* for iteration (so an observer that mutates the list during notification doesn't cause `ConcurrentModificationException` or missed updates), and guard re-entrant notifications with a flag (`notifying`) that defers re-broadcasts. Also detach the observer that triggered the change if appropriate.
10. **Q: What is the memory-leak trap in Observer?** A: If observers never call `detach` (e.g., a closed UI panel keeps its listener attached), the subject holds a strong reference forever — the observer and its whole object graph can't be GC'd. Fixes: explicit detach on dispose, weak references in the listener list, or framework-managed lifecycle.
11. **Q: How does Swing use Observer? (Production)** A: Every component is a subject: `button.addActionListener(listener)`, `addMouseListener`, `addChangeListener` — listeners are Observer objects notified on events. `EventListenerList` provides the thread-safe typed listener list. The entire Swing event model is Observer.
12. **Q: How does Spring implement observer-ish events?** A: `ApplicationEventPublisher.publishEvent(...)` notifies registered `ApplicationListener`s / `@EventListener` methods (synchronous by default; `@Async` for async). It's Observer with type-based dispatch and framework-managed listener registration.
13. **Q: What's the difference between observer callback and a regular method call?** A: A regular call is *direct and static* (the subject names the callee); an observer callback is *registered and dynamic* (the subject knows only the interface, and the listener set can change at run time). The decoupling + dynamic registration is the whole point.
14. **Q: When would you choose polling over Observer? (Tricky)** A: When the change source is external and can't push (e.g., a remote server with no callback channel), when changes are rare and latency-tolerant, or when observers are themselves transient. Polling is also simpler to reason about. But for in-process, frequent, latency-sensitive changes, Observer wins.
15. **Q: Design a notification system: order placed → email + SMS + push + audit, new channels expected. (Scenario)** A: `OrderEvent` (event object); `OrderListener` (Observer interface); `EmailListener`, `SmsListener`, `PushListener`, `AuditListener`; an `OrderService` subject with a `CopyOnWriteArrayList` of listeners; `placeOrder()` pushes the event. Adding "WhatsApp channel" = one class + one subscribe call — zero subject changes. That's the complete answer.
16. **Q: What does "the subject should broadcast, not call" mean?** A: The subject's contract is "I will call `onEvent(evt)` on everyone registered" — it never reaches into an observer's specific methods. This is what keeps the subject stable as observers evolve. Violations (subject calling `emailService.sendX(...)`) collapse the pattern back into tight coupling.
17. **Q: Can observers observe multiple subjects?** A: Yes — an observer can register with several subjects; its `update` receives the subject/event to distinguish the source. That's fine; the coupling is still only to the Observer interface.
18. **Q: How do you pass complex event data without coupling observers to the subject? (Production)** A: Define an *event object* (record/DTO) carrying the change (`OrderPlacedEvent(orderId, amount, ts)`). Observers depend on the event type, not the subject. This is the standard "event object" refinement of Observer.
19. **Q: What's the ordering guarantee of notification?** A: By default, registration order with a `List`; `CopyOnWriteArrayList` preserves order too. There's no *inherent* guarantee — if observers have dependencies ("audit must run before email"), add explicit priorities or a dedicated event pipeline. Never rely on unspecified order.
20. **Q: How do reactive streams (RxJava, Project Reactor) relate to Observer?** A: They're Observer with *backpressure* and *operators*: `Flux.subscribe(consumer)` is attach+update; backpressure lets the observer signal the subject "slow down" (push with flow control). Reactive = Observer + asynchronous pipelining + backpressure — the modern industrial successor to plain Observer.

## 14. Follow-Up Questions
1. **Q: What is the difference between a "model-view" observer and an event-driven observer?** A: MVC's Model is a Subject and Views are Observers (classic GoF example); event-driven observers (GUI listeners, pub/sub) are the same shape but with richer event objects and often async. Both are Observer; MVC is the historical motivating example.
2. **Q: Weak references in observer lists — when are they appropriate?** A: When observers are short-lived (UI components) and you can't guarantee explicit detach. `WeakHashMap`/`WeakReference` listener lists let observers be GC'd without detach — but break "unexpected updates" reasoning if a live observer is collected. Explicit detach + strong refs is the predictable default; weak refs are a leak-safety fallback.
3. **Q: How does batching/coalescing reduce notification storms?** A: Multiple rapid state changes can be coalesced into one notification (e.g., a counter that flushes once per frame/tick). The subject defers `notify` until the storm settles (or batches events) — trading immediacy for throughput, a standard production technique in reactive/UI systems.
4. **Q: Observer vs Chain of Responsibility?** A: Observer *broadcasts to all* listeners (each reacts independently). Chain of Responsibility *passes a request along a chain until one handler claims it*. One-to-many vs many-to-one-until-handled. Both decouple sender from receiver, but with opposite fan-out semantics.
5. **Q: What is the "self-invocation" hazard in Observer?** A: If an observer's reaction causes another state change on the same subject, `notifyObservers` may be re-entered — leading to recursion or re-broadcast of the same event. Guard with a `notifying` flag, a snapshot, or event-loop confinement.

## 15. Coding Example
```java
// Thread-safe Observer with event object
import java.util.concurrent.*;

record TemperatureEvent(String city, double value) {}

@FunctionalInterface
interface TemperatureListener { void onTemperature(TemperatureEvent e); }

class WeatherStation {
    private final List<TemperatureListener> listeners = new CopyOnWriteArrayList<>();
    private double current;

    void subscribe(TemperatureListener l) { listeners.add(l); }
    void unsubscribe(TemperatureListener l) { listeners.remove(l); }

    void update(double value) {
        this.current = value;
        TemperatureEvent evt = new TemperatureEvent("Bengaluru", value);
        for (TemperatureListener l : listeners) {
            try { l.onTemperature(evt); }          // isolate failures
            catch (RuntimeException ex) { System.err.println("listener failed: " + ex.getMessage()); }
        }
    }
}
public class Main {
    public static void main(String[] args) {
        WeatherStation ws = new WeatherStation();
        ws.subscribe(e -> System.out.println("App  → " + e.city() + " is " + e.value() + "°C"));
        ws.subscribe(e -> System.out.println("Alert→ threshold check: " + (e.value() > 40 ? "HEAT WAVE" : "ok")));
        ws.update(39.8);   // both listeners react
        ws.update(41.2);   // alert triggers
    }
}
```
```python
# Python Observer
from typing import Protocol, Callable

Event = tuple[str, float]

class WeatherStation:
    def __init__(self) -> None:
        self._listeners: list[Callable[[Event], None]] = []
    def subscribe(self, listener: Callable[[Event], None]) -> None:
        self._listeners.append(listener)
    def unsubscribe(self, listener: Callable[[Event], None]) -> None:
        self._listeners.remove(listener)
    def update(self, city: str, value: float) -> None:
        for listener in self._listeners:
            listener((city, value))

def phone(e: Event) -> None: print(f"Phone: {e[0]} {e[1]}°C")
def alert(e: Event) -> None:
    if e[1] > 40: print("HEAT WAVE")

ws = WeatherStation()
ws.subscribe(phone); ws.subscribe(alert)
ws.update("Bengaluru", 41.2)   # phone + alert fire
```
```cpp
// C++ Observer
#include <iostream>
#include <vector>
#include <string>

struct Observer {
    virtual ~Observer() = default;
    virtual void update(const std::string& event) = 0;
};
class WeatherStation {                  // Subject
    std::vector<Observer*> observers_;
public:
    void attach(Observer* o) { observers_.push_back(o); }
    void notify(const std::string& evt) {
        for (auto* o : observers_) o->update(evt);
    }
};
struct PhoneDisplay : Observer {
    void update(const std::string& e) override { std::cout << "Phone: " << e << "\n"; }
};
struct WebDisplay : Observer {
    void update(const std::string& e) override { std::cout << "Web: " << e << "\n"; }
};
// int main(){ WeatherStation ws; PhoneDisplay p; WebDisplay w; ws.attach(&p); ws.attach(&w); ws.notify("temp=32"); }
```

## 16. Industry Usage
- **Swing/AWT**: the entire event model (`ActionListener`, `MouseListener`, `ChangeListener`) over `EventListenerList` — Observer everywhere.
- **Android**: `View.setOnClickListener` (Observer), LiveData/StateFlow (Observer + reactive).
- **JavaScript/React**: DOM events, `EventTarget.addEventListener`, `Redux.subscribe`, `MobX` — Observer in the web.
- **Spring**: `ApplicationEventPublisher` + `@EventListener` (Observer with type-based dispatch); `@Async` for async.
- **JDK**: `java.util.Observable`/`Observer` (deprecated but historically canonical), `PropertyChangeSupport` (JavaBeans), `CompletableFuture` callbacks (observer-ish).
- **Reactive streams**: RxJava, Reactor, Kafka consumers, RSocket — Observer plus backpressure/async (the modern industrial evolution).
- **Live UI**: dashboards, stock tickers, chat apps, collaborative editing — all push-based via Observer.
- **Interviews**: "notify many components on change", "decouple sender/receivers", "publish-subscribe", "why is Observable deprecated", "Swing event model" — among the most asked pattern questions.

## 17. References
- **Gamma et al., *Design Patterns* — "Observer" (p. 293)**: canonical definition, the MVC discussion, push vs pull, participant responsibilities.
- **Oracle Docs: `java.util.Observable`/`Observer`, `java.util.concurrent.CopyOnWriteArrayList`, Swing `EventListenerList`** — https://docs.oracle.com/javase/8/docs/api/
- **Spring Framework Docs: `ApplicationEventPublisher`, `@EventListener`** — https://docs.spring.io/spring-framework/reference/core/events.html
- **Martin Fowler, "Observer and Event Sourcing" (martinfowler.com)** — the evolution of the pattern.
- **refactoring.guru — "Observer"** — modern diagrams and Java/C++/Python examples.
- **Head First Design Patterns — "Observer" chapter** — the weather-station worked example.
- **Project Reactor / RxJava docs** — reactive streams as the Observer successor (reactor.io, reactivex.io).

## 18. Cheat Sheet
- Observer = **one-to-many push**: subject notifies registered observers via an Observer interface.
- Participants: Subject (list + attach/detach/notify), Observer (interface), ConcreteSubject (state), ConcreteObserver (reacts).
- Solves: tight coupling (subject names dependents), no runtime dynamics, polling waste/latency.
- Push (event object) vs pull (observer reads subject getters) — prefer push.
- `java.util.Observable` deprecated: it's a class (extends), leaky Vector, clunky — use a custom subject + `CopyOnWriteArrayList` or framework events.
- Thread safety: `CopyOnWriteArrayList` snapshot iteration; isolate each listener's exception.
- Memory leak: observers never detached → subject holds them forever; detach on dispose (or weak refs).
- Observer vs Mediator: broadcast (1→N) vs hub (many→many). Observer vs pub/sub: in-process direct vs broker-decoupled.
- Swing `EventListenerList` and Spring `@EventListener`/`ApplicationEventPublisher` are production Observers.
- Reactive streams = Observer + backpressure + async.

## 19. Quiz
1. Observer defines a ___ dependency. a) many-to-one b) one-to-many c) one-to-one d) many-to-many → **b**
2. The subject knows its observers via: a) their concrete classes b) the Observer interface only c) a config file d) reflection → **b**
3. `java.util.Observable` is deprecated because: a) slow b) it's a class (extends) with a leaky Vector and clunky API c) too fast d) too abstract → **b**
4. Which is the standard thread-safe listener list? a) ArrayList b) CopyOnWriteArrayList c) LinkedList d) HashMap → **b**
5. Observer vs Mediator: a) both broadcast b) observer broadcasts (1→N), mediator centralizes (many→many) c) both centralize d) mediator broadcasts → **b**
6. The classic memory-leak trap is: a) observers never detached b) too many events c) push model d) weak refs → **a**
7. Which is NOT an Observer example? a) button.addActionListener b) Spring @EventListener c) Collections.sort d) Redux.subscribe → **c**
8. Reactive streams (Reactor) = Observer + a) backpressure + async b) inheritance c) static methods d) polling → **a**
9. To isolate a failing observer: a) throw b) try/catch around each listener call c) remove the subject d) ignore → **b**
10. Push vs pull — modern practice prefers: a) pull b) push with an event object c) both always d) neither → **b**

## 20. Flashcards
- **Q: Observer intent?** → **A:** Define a one-to-many dependency; subject notifies all registered observers of state changes (publish-subscribe).
- **Q: Why not direct calls or polling?** → **A:** Direct calls couple the subject to dependents (Open-Closed violation); polling wastes resources and adds latency. Observer pushes on change.
- **Q: Thread-safe listener list?** → **A:** `CopyOnWriteArrayList` (snapshot iteration) or synchronized list.
- **Q: Why is `Observable` deprecated?** → **A:** Class-based (extends), leaky synchronized Vector, clunky API — use custom subject + `CopyOnWriteArrayList` or framework events.
- **Q: Observer vs Mediator?** → **A:** Observer broadcasts 1→N; Mediator centralizes many→many peer coordination.
- **Q: The memory-leak trap?** → **A:** Observers never detached → strong refs forever; detach on dispose or use weak references.
- **Q: Production Observer examples?** → **A:** Swing `EventListenerList`, Spring `@EventListener`, Redux.subscribe, reactive streams.
- **Q: How to isolate listener failures?** → **A:** Try/catch around each `listener.onEvent(...)`.

## 21. Revision
Observer defines a **one-to-many dependency** where a subject notifies all registered observers via an Observer interface — decoupling event producers from consumers and enabling dynamic subscribe/unsubscribe at run time. It exists because direct calls from the subject to dependents violate Open-Closed (adding a listener edits the subject), hard-code the listener set, and are impossible to vary at run time; polling is wasteful and slow. Mechanics: subject holds a listener list (use `CopyOnWriteArrayList` for thread safety), `notify()` iterates pushing an event object, each observer reacts independently (isolate exceptions per listener). Critical traps: memory leaks from never-detached observers, `ConcurrentModificationException` from mutating during iteration, re-entrancy/recursion, and notification storms. Discriminate: Mediator centralizes many-to-many; pub/sub brokers distribute async. Production: Swing `EventListenerList`, Spring `ApplicationEventPublisher`/`@EventListener`, Redux/MobX, reactive streams (Observer + backpressure). `java.util.Observable` is deprecated — be ready to say why and what to use instead. Interview hook: "notify many components / decouple sender and receivers / publish-subscribe" → Observer.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is the Observer pattern?" | 2 How / 7 Formal Definition |
| "Why not direct calls or polling?" | 4 Alternatives / 13 Q2 / 13 Q14 |
| "Push vs pull?" | 13 Q3 / 9 Internal Working |
| "Why is `java.util.Observable` deprecated?" | 13 Q4 / 18 Cheat Sheet |
| "Observer vs Mediator / pub-sub?" | 13 Q5 / 13 Q6 |
| "Thread-safety of the listener list?" | 13 Q7 / 9 Internal Working |
| "The memory-leak trap?" | 13 Q10 / 18 Cheat Sheet |
| "How does Swing/Spring use Observer?" | 13 Q11 / 13 Q12 / 16 Industry Usage |
| "Design a notification fan-out (scenario)." | 13 Q15 / 8 Example |
| "How do reactive streams relate?" | 13 Q20 / 16 Industry Usage |
