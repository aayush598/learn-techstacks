# Exceptions and OOP

> **TL;DR**: Java models errors as a class hierarchy rooted at `Throwable` (checked vs unchecked), thrown objects unwind the stack through frames, and the OOP design decisions — what to extend, whether to declare `throws`, and how `finally` composes — are what interviewers actually probe.

## 1. Why Does This Exist?
Before exceptions, C used return codes and `errno`: callers had to check every function's return value, errors were silently swallowed when a check was forgotten, and error paths were scattered through business logic. Java's exceptions give **structured, type-checked error propagation**: an error is an *object* carrying rich context, thrown at the failure point and caught where the caller chooses, with guaranteed cleanup via `finally`. The OOP angle: because exceptions are objects, you can build an *inheritance hierarchy* of error types, and because throws are checked at compile time, the compiler enforces error handling as part of the type system.

## 2. How Does It Work?
At a glance:
- `Throwable` is the root. `Exception` (recoverable) and `Error` (JVM-level, `OutOfMemoryError`, `StackOverflowError`) extend it.
- `Exception` splits into `RuntimeException` (unchecked) and checked exceptions (anything else that extends `Exception` but not `RuntimeException`).
- **Checked** exceptions must be declared (`throws`) or caught — enforced by the compiler.
- **Unchecked** (`RuntimeException` + `Error`) need not be declared.
- When thrown, the exception object travels up the call stack until a matching `catch` (by class or superclass) handles it; `finally` blocks run as the stack unwinds (or before a return).

## 3. When Is It Used?
- **I/O and parsing** — `IOException`, `SQLException`, `ParseException` are classic checked exceptions in library APIs.
- **Programmer bugs** — `NullPointerException`, `IndexOutOfBoundsException`, `IllegalArgumentException`, `ArithmeticException` are unchecked.
- **Resource cleanup** — `finally` or try-with-resources (`AutoCloseable`) for files, sockets, DB connections.
- **Multi-catch** — handle several unrelated exception types in one block (Java 7+).
- **Custom hierarchies** — `PaymentException` → `InsufficientFundsException` / `CardDeclinedException` for domain error modeling.

## 4. Why Wasn't Another Approach Chosen?
Alternatives:
- **Return codes (`errno`/Go-style)**: fast, but error propagation is manual and easy to forget; Java chose exceptions for enforced handling. (Go's `if err != nil` shows the alternative's cost.)
- **All-unchecked (Python/C#-style)**: C# dropped checked exceptions; Java *kept* them. Trade-off: checked exceptions force handling at compile time but pollute signatures (`throws Exception` everywhere) and hurt evolution (adding a checked exception to a method breaks all callers). Modern Java opinion (Effective Java Item 72, Spring) prefers unchecked for most cases.
- **`Error` vs `Exception` split**: the language reserves `Error` for conditions you can't recover from, so you don't waste catch blocks on JVM faults.
- **Global error object (C setjmp/longjmp)**: unstructured, no type info, no cleanup guarantees — rejected.

## 5. Intuition
Think of a **hospital triage system**: when a patient (error) arrives, you don't hand them a note to carry through every corridor (return code). Instead, a medical officer (throw) *raises the alarm* and the patient is transported (stack unwinding) until an appropriate specialist (catch block) takes over. Triage *classes* the patient first: "this is a fracture (recoverable) vs this is a cardiac arrest (Error)". The `finally` block is the *cleaning crew* that always sterilizes the operating room — even if the surgeon walks out mid-procedure.

## 6. Real-World Analogy
A **restaurant kitchen with a head chef**: if a sous-chef finds the fish is spoiled, he doesn't quietly serve it (swallowed error) nor shut down the whole restaurant (crash). He *shouts* "Order 42 — fish bad!" (throw). Each station (stack frame) that can deal with it stops passing it up; the *dishwasher* (finally) always cleans the station no matter what; if no station handles it, the restaurant (JVM) prints the ticket and closes that order (uncaught → thread terminates, stack trace printed).

## 7. Formal Definition
- **Checked exception**: "A checked exception is a subtype of `Throwable` that is not a subtype of either `RuntimeException` or `Error`" (JLS §11.2) — the compiler verifies every method that can throw it either catches it or declares it in `throws`.
- **Unchecked exception**: subtype of `RuntimeException` (or `Error`); no declaration required.
- **`try`-`catch`-`finally`**: `try` guards code; `catch (E e)` handles exceptions assignable to `E` (runtime type checking via instanceof against the catch type, using the exception's type); `finally` always executes.
- **Try-with-resources** (JLS §14.20.3): resources implementing `AutoCloseable` are closed automatically in reverse order of declaration, and suppressed exceptions are attached to the primary exception.

## 8. Example
Walk a real flow:
```java
try (BufferedReader r = new BufferedReader(new FileReader("orders.csv"))) {
    String line = r.readLine();
    int qty = Integer.parseInt(line.split(",")[1]);   // may throw
    System.out.println(qty);
} catch (FileNotFoundException e) {
    System.err.println("Missing file: " + e.getMessage());  // recover: fall back
} catch (NumberFormatException | ArrayIndexOutOfBoundsException e) {  // multi-catch
    System.err.println("Bad row format");
} finally {   // (finally not needed with try-with-resources here, but legal)
    System.out.println("cleanup pass done");
}
```
Step trace if `line` = "apple,banana":
1. `readLine()` succeeds; split gives `["apple","banana"]`; `Integer.parseInt("banana")` throws `NumberFormatException`.
2. Exception object created with stack trace, thrown from the parse line.
3. JVM unwinds: no `catch` in the try block → checks `catch(FileNotFoundException)` → not assignable → checks `catch(NumberFormatException | ArrayIndexOutOfBoundsException)` → `NumberFormatException` IS assignable → handler runs, prints "Bad row format".
4. Try-with-resources closes `r` (close may throw → suppressed exceptions appended).
5. Program continues after the catch chain; if no catch matched, the thread dies and the stack trace prints to stderr.

## 9. Internal Working
1. **Compile time**: the compiler builds a per-method *exception table* (`try`-`catch` mapping with start/end/handler PCs) and verifies checked-exception declaration (JLS §11.2).
2. **Runtime**: `athrow` bytecode pops the exception reference; the JVM finds the current frame's exception table, checks the range and catch type (type check), and jumps to the handler if matched.
3. **Unwinding**: if no handler in the frame, the frame is popped (its local variables discarded), and the search continues in the caller — the stack trace records the sequence.
4. **`finally`**: implemented by copying the `finally` block's bytecode into both the normal exit and every exception path of the try block.
5. **Try-with-resources**: the compiler generates `try { ... } catch (Throwable t) { close(); throw t; }` with suppressed-exception bookkeeping.
6. **Exception object cost**: stack-trace capture (`fillInStackTrace`) is the dominant cost — a *thrown-and-handled* exception can cost ~µs because every frame's method/line is captured; this is why hot-loop exception use is an anti-pattern.

## 10. Time Complexity
- Throw + catch in same method: O(1) but expensive constant (~µs due to stack-trace capture).
- Unwinding through N frames: O(N) in stack depth plus capture cost per frame.
- `getMessage()`/`getCause()`: O(1).
- **Filling the stack trace** dominates; you can override `fillInStackTrace()` to return `this` and skip capture if you only need control flow (a documented performance hack).
- Try-with-resources adds O(1) close per resource (each `close()` may itself throw).

## 11. Advantages
- Error propagation is automatic and type-safe (checked by compiler).
- Rich context: message, cause chain (`initCause`), stack trace, custom fields.
- `finally`/try-with-resources guarantee cleanup even on early return or exception.
- Hierarchical catch: `catch (Exception e)` handles a whole family; multi-catch reduces duplication.
- Forces developers to think about failure modes at compile time (checked exceptions).

## 12. Disadvantages
- Checked exceptions pollute method signatures and break evolving APIs (adding one breaks all callers — Effective Java Item 72 calls them "the exception to the rule").
- Stack-trace capture makes exceptions slow in hot paths (misuse → order-of-magnitude slowdown).
- Over-use of `catch (Exception)` swallows bugs.
- Hiding exceptions (`catch { log; }`) creates silent failures; "checked exceptions can reduce reliability" when handlers are empty.
- `finally` interacting with `return` is subtle: a `return` in `finally` overrides a return in `try` — a classic bug.

## 13. Interview Questions
1. **Q: Difference between checked and unchecked exceptions?** A: Checked must be declared/caught (compiler-enforced); unchecked (`RuntimeException`/`Error`) need not be. Checked represent recoverable, expected conditions; unchecked represent programmer bugs.
2. **Q: What is the base class of all exceptions?** A: `Throwable`; `Error` and `Exception` extend it; `RuntimeException` extends `Exception`.
3. **Q: Can a method throw a checked exception without declaring it?** A: No — that's a compile error; unchecked exceptions need no declaration.
4. **Q: What does `finally` do?** A: Always executes when the try block exits, whether normally, via return, or via exception — the standard place for cleanup.
5. **Q: Does `finally` run if the JVM exits (`System.exit`)?** A: No — `System.exit` halts the JVM before `finally` runs; `RuntimeException`/`Error` don't prevent `finally`.
6. **Q: What happens if a `return` is in both `try` and `finally`?** A: The `finally` return wins (overrides the try's value) — a subtle, usually-unintended behavior.
7. **Q: How do you create a custom exception?** A: Extend `Exception` (checked) or `RuntimeException` (unchecked), provide message/cause constructors.
8. **Q: Should you catch `Exception` or `Throwable`?** A: Catch the most specific types you can handle; catching `Throwable` also catches `Error` (like `OutOfMemoryError`) which you almost never should.
9. **Q: What is the cause chain?** A: An exception can wrap another via `initCause`/constructor; `getCause()` walks it, letting you preserve the original failure at a higher layer.
10. **Q: What are suppressed exceptions?** A: In try-with-resources, if `close()` throws while the primary exception is propagating, the close exception is *suppressed* and attached to the primary (`getSuppressed()`).
11. **Q: Why are exceptions slow?** A: Stack-trace capture (`fillInStackTrace`) walks and records every frame — microseconds per throw; avoid exceptions for normal control flow.
12. **Q: What is multi-catch?** A: `catch (A | B e)` handles multiple unrelated types in one block (Java 7+), with the handler type being their common supertype.
13. **Q: What is try-with-resources and what interface is required?** A: `try (Resource r = ...)` auto-closes resources implementing `AutoCloseable`/`Closeable` in reverse declaration order, even on exception.
14. **Q: Checked or unchecked for a library API?** A: Modern guidance (Effective Java Item 72): use checked for truly recoverable conditions the caller should handle; otherwise unchecked; avoid inventing checked exceptions for everything.
15. **Q: What is the difference between `Error` and `Exception`?** A: `Error` = JVM-level, non-recoverable (`OutOfMemoryError`, `StackOverflowError`); `Exception` = recoverable program-level conditions.
16. **Q: Can a `catch` for a checked exception be "unreachable"?** A: The compiler flags `catch (SomeCheckedException)` if the try block can't throw it — a compile error, unlike unchecked which are always allowed.
17. **Q: What is an exception's `toString()` vs `getMessage()`?** A: `toString()` = class name + message (used by printStackTrace); `getMessage()` = just the message string.
18. **Q: How do you rethrow while preserving the original?** A: `throw e;` inside a catch rethrows the same object (keeping the stack); don't `throw new X(e)` unless you intend to wrap.

## 14. Follow-Up Questions
1. **Q: What is "exception transparency" with generics (Java 7 improved catch)?** A: If a generic method's caller throws a checked exception, a single `catch (Exception)` rethrowing it can propagate the *precise* type — the compiler tracks rethrown exception types more precisely.
2. **Q: Why does the compiler allow `catch (RuntimeException)` anywhere?** A: Because the compiler can't prove a method won't throw unchecked exceptions (any method may), so unchecked handlers are always potentially reachable.
3. **Q: What's the cost profile of exceptions vs return codes?** A: Return codes are near-free; exceptions cost ~µs (stack capture) when thrown. In hot paths, prefer returning `Optional`/a result type and reserving exceptions for truly exceptional paths.
4. **Q: What happens if the constructor of an exception throws?** A: The throwing `throw` statement itself fails with the new exception; the original exception object is lost (the JVM reports the new one).
5. **Q: How does `finally` interact with `AutoCloseable.close()`?** A: Pre-Java-7 you'd write try/finally manually; try-with-resources generates the same structure but also suppresses close-exceptions during unwinding.
6. **Q: What is a "thrown but never caught" exception's final destination?** A: The thread's default uncaught exception handler (prints stack trace to stderr, thread dies; `main` thread → JVM exits with non-zero status). You can install `Thread.UncaughtExceptionHandler`.
7. **Q: Why might a framework like Spring prefer unchecked exceptions?** A: So that checked exceptions (e.g., `IOException`) get translated into runtime exceptions (like `DataAccessException`) — letting framework code pass through layers without `throws` noise and enabling declarative rollback.

## 15. Coding Example
```java
// Custom hierarchy: checked for recoverable domain errors
public class PaymentException extends Exception {                  // checked
    public PaymentException(String msg) { super(msg); }
    public PaymentException(String msg, Throwable cause) { super(msg, cause); }
}
public class InsufficientFundsException extends PaymentException {
    public InsufficientFundsException(String msg) { super(msg); }
}
public class CardDeclinedException extends PaymentException {
    public InsufficientFundsException(String msg) { super(msg); }
}
```
```java
public class PaymentService {
    public void charge(Account a, long cents) throws InsufficientFundsException, CardDeclinedException {
        if (a.balanceCents() < cents) throw new InsufficientFundsException("Need " + cents + " have " + a.balanceCents());
        if (a.cardBlocked()) throw new CardDeclinedException("Card blocked by issuer");
        a.debit(cents);
    }
}
```
```java
// Handling: hierarchical catch + finally semantics
public class OrderProcessor {
    static void ship(Account a, long cents) {
        PaymentService svc = new PaymentService();
        try {
            svc.charge(a, cents);
        } catch (InsufficientFundsException e) {          // specific first
            System.out.println("Retry with different card: " + e.getMessage());
        } catch (PaymentException e) {                     // family (card declined etc.)
            System.out.println("Payment failed: " + e.getCause());
        } finally {
            System.out.println("Audit entry written (always).");   // runs even on exception/return
        }
    }
}
```
```java
// Try-with-resources + suppressed exceptions
import java.io.*;
public class ResourceDemo {
    static void readAll(String path) {
        try (BufferedReader br = new BufferedReader(new FileReader(path))) {
            br.lines().forEach(System.out::println);
        } catch (IOException e) {
            System.err.println("IO failure: " + e.getMessage());
            for (Throwable s : e.getSuppressed()) System.err.println("  suppressed: " + s);
        }
    }
}
```
```java
// finally vs return trap
public class Trap {
    static int get() {
        try { return 1; } finally { return 2; }   // returns 2! finally overrides
    }
}
```

## 16. Industry Usage
- **Spring**: `@Transactional` rolls back on runtime exceptions; checked exceptions do NOT trigger rollback by default — a classic production gotcha. Spring translates JDBC checked `SQLException` into unchecked `DataAccessException` subclasses.
- **JDK**: `Files`/`InputStream` throw checked `IOException`; `ExecutorService` wraps worker exceptions; `Future.get` throws `ExecutionException` wrapping the original.
- **Concurrency**: `CompletableFuture` chains propagate exceptions; `exceptionally`/`handle` recover them.
- **Netflix/Hystrix**: failure types (timeout/error) are modeled to decide fallbacks; resilience libraries treat "expected business exception" vs "infrastructure failure" differently.
- **Web frameworks**: `@ControllerAdvice` maps exception types to HTTP status codes — the hierarchy IS the API contract (e.g., 404 for `NotFoundException`).
- **Guava**: `Throwables.propagate` (now `Throwables.throwIfUnchecked`) — explicit unchecked-rethrow idiom.

## 17. References
- Oracle, *The Java Language Specification*, §11 "Exceptions", §14.20 "try-catch-finally", §14.20.3 "try-with-resources".
- Joshua Bloch, *Effective Java (3rd ed.)*, Items 69-77 (exceptions chapter): "Use exceptions only for exceptional conditions", "Use checked exceptions for recoverable conditions and runtime exceptions for programming errors", "Prefer standard exceptions", "Never ignore exceptions".
- Oracle tutorial, "Exceptions" (docs.oracle.com/javase/tutorial/essential/exceptions/index.html).
- Brian Goetz et al., *Java Concurrency in Practice* (exception handling in tasks, §6.3).
- Baeldung, "Java Exceptions" series and "Try-with-Resources" guide.

## 18. Cheat Sheet
- `Throwable` ← `Error` | `Exception` ← `RuntimeException` | (checked exceptions).
- Checked = must catch/declare; unchecked = optional. Errors = don't catch.
- `finally` always runs (unless `System.exit`); `return` in `finally` overrides try's return.
- Try-with-resources closes `AutoCloseable` in reverse order; suppressed exceptions attach to primary.
- Multi-catch: `catch (A | B e)` (types can't be in same family).
- Cost: throw+catch ≈ µs (stack capture); don't use exceptions for control flow.
- Catch the most specific type first; catching `Throwable` catches `Error` too.
- `getCause()` walks the wrap chain; `getSuppressed()` lists close-failures.
- Custom exceptions: extend `RuntimeException` unless recovery is expected.
- Empty catches are bugs — always log or handle.

## 19. Quiz
1. Which is unchecked? a) `IOException` b) `SQLException` c) `IllegalArgumentException` d) `FileNotFoundException` → **c**
2. The root class of the exception hierarchy is: a) `Object` b) `Exception` c) `Throwable` d) `RuntimeException` → **c**
3. `finally` does NOT run when: a) An exception is thrown b) A `return` occurs c) `System.exit(0)` runs d) A checked exception is caught → **c**
4. `static int f() { try { return 1; } finally { return 2; } }` returns: a) 1 b) 2 c) Compile error d) Exception → **b**
5. Try-with-resources requires the resource to implement: a) `Serializable` b) `AutoCloseable` c) `Runnable` d) `Cloneable` → **b**
6. Which is TRUE about checked exceptions? a) Always propagated b) Must be caught or declared c) Only thrown by JDK d) Slower than unchecked → **b**
7. Catching `Throwable`: a) Is best practice b) Catches `Error` too c) Only catches exceptions d) Fails to compile → **b**
8. `NumberFormatException` extends: a) `Exception` b) `IOException` c) `RuntimeException` d) `Error` → **c**
9. The dominant cost of throwing an exception is: a) Object allocation b) Stack-trace capture c) GC pressure d) The catch block → **b**
10. Which design is recommended for a library API? a) Checked exceptions everywhere b) Checked for recoverable conditions, runtime for bugs c) Never throw d) Always throw `Exception` → **b**

## 20. Flashcards
- **Q: What's the exception hierarchy root?** → **A:** `Throwable` → `Error`/`Exception`; `RuntimeException` extends `Exception`.
- **Q: Checked vs unchecked?** → **A:** Checked must be caught/declared; unchecked need not; Errors shouldn't be caught.
- **Q: When does `finally` not run?** → **A:** On `System.exit` (JVM halt); otherwise always.
- **Q: Try-with-resources?** → **A:** Auto-closes `AutoCloseable` resources; suppressed close-exceptions attached.
- **Q: Why are exceptions slow?** → **A:** Stack-trace capture per throw (~µs); avoid in hot loops.
- **Q: What does a `return` in `finally` do?** → **A:** Overrides the try's return value.
- **Q: How to create a custom exception?** → **A:** Extend `RuntimeException` (bugs) or `Exception` (recoverable), with message/cause constructors.
- **Q: Why do frameworks prefer unchecked?** → **A:** To let errors propagate without `throws` noise and enable declarative handling.

## 21. Revision
Java errors are objects under `Throwable`: `Error` (don't catch), checked `Exception` (compiler enforces catch/declare), unchecked `RuntimeException` (programmer bugs). Throw → JVM matches the runtime type against `catch` types via the exception table → unwinds frames (capturing the stack trace) → `finally` runs on every exit path (except `System.exit`). Try-with-resources closes `AutoCloseable`s and preserves suppressed close-exceptions. Cost: ~µs per throw due to stack capture, so never use exceptions for control flow. Design: catch the most specific type; custom exceptions extend `RuntimeException` unless callers are expected to recover; Spring rolls back only on runtime exceptions. Beware `return` in `finally` and empty catch blocks. When asked to design an exception hierarchy, map failure kinds (InsufficientFunds, CardDeclined) onto a common checked base.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Checked vs unchecked exceptions?" | 2 How It Works / 7 Formal Definition / 13 Interview |
| "What's the difference between Error and Exception?" | 2 How It Works / 13 Interview |
| "Does `finally` always run?" | 8 Example / 13 Interview |
| "What happens if `finally` has a `return`?" | 13 / 14 Follow-Up |
| "What is try-with-resources?" | 7 Formal Definition / 9 Internal Working |
| "Why are exceptions expensive?" | 9 Internal Working / 10 Time Complexity |
| "How do you design an exception hierarchy?" | 15 Coding Example / 13 Interview |
| "Checked exceptions in a library — good or bad?" | 4 Alternatives / 13 Interview |
| "Why does Spring prefer runtime exceptions?" | 14 Follow-Up / 16 Industry Usage |
| "What are suppressed exceptions?" | 13 Interview / 9 Internal Working |
