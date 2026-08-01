# Compile-Time Polymorphism: Method Overloading

> **TL;DR**: Method overloading is ad-hoc polymorphism — several methods with the *same name* but different parameter types (or counts) in one class, resolved at **compile time** by the compiler picking the most specific matching signature; it is the opposite of overriding (runtime), and return type alone never distinguishes overloads.

## 1. Why Does This Exist?
Overloading exists because **the same logical operation is often performed on different kinds of input**, and forcing unique names would clutter the API: `print(int)`, `print(String)`, `print(double)` are all "print" — one concept, multiple input types. Without overloading you'd write `printInt()`, `printString()`, `printDouble()` and every caller would juggle awkward names. Overloading keeps one name ("print") and lets the *compiler* choose the right variant from the arguments. It's "polymorphism" because the name is polymorphic — the same word maps to several implementations — but it's *compile-time*: the choice is made by static type analysis, before the program runs, with no vtable involved.

## 2. How Does It Work?
```java
public class Printer {
    public void print(int x) { ... }
    public void print(String s) { ... }
    public void print(double d) { ... }
    public void print(int x, String s) { ... }   // different arity = another overload
}
```
Resolution at compile time: given `printer.print(42)`, the compiler picks the method whose parameter types *best match* the arguments by:
1. **Phase 1**: exact match (no conversion).
2. **Phase 2**: widening primitive conversion (`int` → `long` → `float` → `double`).
3. **Phase 3**: boxing/unboxing (`int` → `Integer`).
4. **Phase 4**: varargs (`int...`).
Pick the *most specific* applicable method (ties → ambiguity error).

## 3. When Is It Used?
- **Utility methods**: `Math.min(int,int)`, `min(long,long)`, `min(float,float)`; `String.valueOf(...)` (10+ overloads).
- **Constructors**: multiple constructors with different parameter sets (`new BigInteger(int)`, `BigInteger(String)`).
- **Convenience APIs**: `Collections.sort(List)`, `sort(List, Comparator)`; `put(key)` vs `put(key, value)`.
- **Fluent/typed entry points**: `Optional.of(x)`, `Optional.ofNullable(x)` (same name, different null contract).
- **Type-directed formatting**: `print(int)` vs `print(double)` for language-appropriate output.

## 4. Why Wasn't Another Approach Chosen?
- *Why not unique names per type?* It pollutes the API (`printInt`, `printDouble`...) and the caller must remember the name — the operation's *identity* is "print," so one name is more honest. Overloading chosen.
- *Why not decide at runtime (make it overriding-like)?* The *argument types* are known statically — the compiler can resolve exactly; runtime resolution would add indirection for no benefit (and Java can't dispatch on argument types dynamically — only the receiver is dispatched). Compile-time chosen: free, precise.
- *Why not allow return-type-based overloading?* Two methods differing only in return type can't be disambiguated when the caller ignores the return (`foo();`) — the compiler can't know which you meant. Rejected in Java/C++; return type can only be *covariant* in overriding, never a discriminator in overloading.
- *Why not generics instead of overloads?* For *identical* logic over many types, a generic `<T>` is better (one method); for *different* behavior per type (print int vs print double), overloading is right. Both exist because they solve different problems.

## 5. Intuition
Think of a **gym class with different routines for different fitness levels**. The instructor says "run the class" — but there's a beginner routine, an intermediate routine, and an advanced routine. The *name* is the same ("run the class"); the *level* (the argument) tells the scheduler which routine to run, chosen before anyone arrives (compile time). If someone new shows up, the scheduler picks the closest matching level. No runtime discussion — the routine is fixed at scheduling time.

## 6. Real-World Analogy
A **ticket counter**. "Buy a ticket" works the same, but the form differs by *what you give the clerk*: a cash amount (one routine), a credit card (another), a student ID (a third), or a name + quantity (a fourth). The clerk picks the correct form by *what you hand over* — the input determines the process. If you handed cash and asked "which form is this?" you'd be confused; the clerk (compiler) already chose. Same request, different forms, decided up front by the input type.

## 7. Formal Definition
**Method overloading** is the declaration, within one class (or inheritance family), of two or more methods with the same name but *different parameter lists* (different number, types, or order of parameters); it is a form of ad-hoc polymorphism. At a call site, the compiler selects the most specific applicable overload using the phases (exact match, widening, boxing/unboxing, varargs); if none applies, it's a compile error; if multiple are equally specific, it's an ambiguity error. Return type is *not* part of the signature and cannot distinguish overloads. Overloading is resolved statically (compile time); it is distinct from overriding, which is resolved dynamically (runtime) and requires identical signatures.

## 8. Example
```java
public class Calc {
    public int add(int a, int b) { return a + b; }          // overload 1
    public long add(long a, long b) { return a + b; }       // overload 2 (widening target)
    public double add(double a, double b) { return a + b; } // overload 3
    public int add(int a, int b, int c) { return a + b + c; } // overload 4 (arity)
}
public class Main {
    public static void main(String[] args) {
        Calc c = new Calc();
        System.out.println(c.add(1, 2));        // overload 1 — exact int,int
        System.out.println(c.add(1L, 2L));      // overload 2 — exact long,long
        System.out.println(c.add(1, 2.0));      // overload 3 — int widens to double
        System.out.println(c.add(1, 2, 3));     // overload 4 — arity
        // c.add(1, 2.0f);   — ambiguous? no: int→? and float→? — resolved to (int? no)...
        //   Actually int,float has no exact match; candidates: (long,long) no, (double,double) — int→double, float→double → OK
    }
}
```
Resolution: exact matches win (`(int,int)`); otherwise widening (`int→double`); otherwise boxing; otherwise varargs. Ambiguity (two equally-good matches) is a compile error — e.g., `null` argument with `print(String)` and `print(Object)` overloads picks `String` (most specific), but `print(String)` vs `print(Integer)` with `null` is ambiguous.

## 9. Internal Working
1. The compiler builds a method table per class with (name, signature) keys.
2. At `c.add(1, 2)`, it collects candidates named `add`; filters by applicability (can the args convert?); among applicable, picks the most specific (each param type of one overload is assignable to the other's).
3. It emits a call to a *specific* method signature — the bytecode contains the fully-resolved method reference (`Calc.add(int,int)`) — no runtime decision.
4. Because resolution is static, overloads compile to distinct method entries with *different descriptor strings* (`(II)I`, `(JJ)J`, `(DD)D`).
5. At runtime, the JVM finds the resolved method directly — O(1) class-metadata lookup, no vtable involved (unless the chosen method is itself overridden → then *that* part dispatches dynamically).
The "overload then maybe override" combo: overload resolution is static, but if the resolved method is overridable and the receiver's runtime type overrides it, the *override* still dispatches dynamically.

## 10. Time Complexity
- Overload resolution: O(#overloads) at compile time — zero runtime cost.
- Call to the resolved method: O(1) (direct or vtable if overridden).
- No asymptotic difference from any other method call; overloading is "free" polymorphism.

## 11. Advantages
- **Clean API**: one name for one concept, several input types.
- **Compile-time safety**: the compiler rejects unsupported argument combos.
- **Zero runtime cost**: static resolution, no dispatch table.
- **Type-directed behavior**: print int differently from print double.
- **Convenience overloads**: `sort(list)` vs `sort(list, cmp)`.

## 12. Disadvantages
- **Ambiguity traps**: `null` with reference overloads, widening/boxing ties → compile errors (or wrong picks).
- **Signature noise**: many overloads clutter autocomplete.
- **No return-type flexibility**: can't have `int x()` and `String x()`.
- **Mismatch with overriding**: a subtle signature difference silently turns an override into an overload (hence `@Override`).
- **Maintenance**: adding an overload can change which one is selected at existing call sites (silent behavior change).

## 13. Interview Questions
1. **Q: What is method overloading?** A: Multiple methods with the same name but different parameter lists (count/types/order) in a class; the compiler picks the most specific matching signature at compile time — ad-hoc (compile-time) polymorphism.
2. **Q: Can you overload on return type?** A: No — return type isn't part of the signature; two methods differing only in return type are a compile error (the caller might ignore the return, making the choice ambiguous).
3. **Q: Overloading vs overriding?** A: Overloading = same name, different parameters, resolved at compile time (static binding), in the same class; overriding = same signature, resolved at runtime (dynamic binding/vtable), in a subclass. Both are polymorphism, opposite timings.
4. **Q: What is the resolution order?** A: Phase 1 exact match → Phase 2 widening primitive → Phase 3 boxing/unboxing → Phase 4 varargs; among applicable, pick the *most specific*; ties → ambiguity error.
5. **Q: TRICKY — `m(null)` with `m(String)` and `m(Integer)` overloads. Which runs?** A: Compile error — `null` is assignable to both `String` and `Integer`, and neither is more specific than the other → ambiguity. (With `m(Object)` too, `String` wins — more specific.)
6. **Q: Why is overloading called "compile-time polymorphism"?** A: The choice of which implementation runs is made by the compiler from static types before execution — no vtable, no runtime decision — unlike overriding's runtime dispatch.
7. **Q: SCENARIO — Design a `log()` API: message only, or with exception.** A: `void log(String msg)` and `void log(String msg, Throwable t)` — convenience overloads; the two-arg version formats stack traces, one-arg doesn't. Callers choose by what they have.
8. **Q: PRACTICAL — Why does `Integer.valueOf(String)` differ from `valueOf(int)`?** A: Different inputs (text vs number) → different parsing/caching logic; the overload gives one name, type-directed behavior, and compile-time selection.
9. **Q: TRICKY — Can overloading be combined with overriding?** A: Yes — a subclass can overload (new signature) and override (same signature) simultaneously; each call is first statically resolved to a signature, then (if overridden) dynamically dispatched.
10. **Q: What's the risk of adding a new overload to a library?** A: Existing call sites may silently resolve to the new overload (if it's "more specific" for their args), changing behavior — a compatibility hazard; that's why library APIs add overloads cautiously.
11. **Q: PRODUCTION — `print(int)` vs `print(double)`; calling `print(5L)`?** A: `5L` is a long — no exact match; widening candidates: `print(long)`? none → `print(double)` (long→double widening) applies. So it calls `print(double)`. Widening beats boxing/varargs.
12. **Q: TRICKY — `foo(byte)` vs `foo(short)` overloads; call `foo(5)`.** A: `5` is an int literal; no exact match; `int` can't widen to `byte`/`short` without narrowing (not allowed in phase 2) — compile error unless you cast `foo((byte) 5)`. The int-literal narrowing trap.
13. **Q: Why can't a constructor be overloaded by return type (obviously)?** A: Constructors have no return type; overloading them is *only* by parameter lists — that's how multiple constructors (`this()`, `this(int)`) coexist.
14. **Q: SCENARIO — Two overloads `m(A)` and `m(B)`, where `B extends A`; call `m(someB)`.** A: `m(B)` wins (most specific — B is assignable to A but not vice versa). If you passed an `A`, `m(A)` wins. Specificity resolves the reference-type choice.
15. **Q: What's the "overloading + autoboxing + null" nightmare?** A: `m(Integer)` and `m(int)` — calling `m(5)` picks `m(int)` (exact); calling `m(null)` is ambiguous (null can't be unboxed). Autoboxing complicates resolution; prefer consistent signatures in APIs.

## 14. Follow-Up Questions
1. **Q: What is the "most specific method" rule precisely?** A: One method is more specific than another if every parameter type of the first is assignable to the corresponding parameter type of the second (and not vice versa); the most specific applicable method is chosen.
2. **Q: How do overloads interact with varargs?** A: Varargs is the *last* phase — exact/widening/boxing matches always beat a varargs match; if only varargs applies, the array argument wins ties.
3. **Q: What is `@Overload`-like tooling?** A: Java has no overload annotation (unlike `@Override`), which is why overload-by-typo is easy; IDEs warn when two overloads have nearly identical signatures.
4. **Q: Do functional interfaces change overloading?** A: Lambdas make overload resolution with functional-interface args tricky — `m(Function<String,Integer>)` vs `m(Function<String,String>)` is ambiguous with a lambda; you often must cast or use explicit types.

## 15. Coding Example
```java
// A production-shaped overloaded API
public class Logger {
    public void log(String message) {                        // 1-arg
        log(message, null);                                   // delegate to the full form
    }
    public void log(String message, Throwable t) {           // 2-arg (full form)
        System.out.print("[log] " + message);
        if (t != null) System.out.print(" -> " + t.getClass().getSimpleName());
        System.out.println();
    }
    public void log(int level, String message) {             // typed severity
        System.out.println("[level " + level + "] " + message);
    }
    public void log(double value) {                          // numeric path
        System.out.printf("[num] %.2f%n", value);
    }
}
public class Main {
    public static void main(String[] args) {
        Logger L = new Logger();
        L.log("hi");                 // 1-arg → delegates
        L.log("boom", new RuntimeException("x"));  // 2-arg
        L.log(3, "warn");            // int, String
        L.log(3.14);                 // double
        L.log(5L);                   // long → widens to double (no long overload)
    }
}
```
```python
# Python: no overloading (a function has one name); default args / dispatch instead
def log(message, level=None, throwable=None):
    if throwable: print(message, throwable.__class__.__name__)
    elif level is not None: print(f"[level {level}] {message}")
    else: print(message)
```
```cpp
// C++ overloading — same rules as Java, plus more conversions
void f(int);
void f(double);
int main() { f(1); f(1.0); f('a'); }  // char → int (promotion)
```

## 16. Industry Usage
- **JDK**: `Math.min/max` (many primitive overloads), `String.valueOf` (10+ overloads), `Collections.sort(List)` vs `sort(List, Comparator)`.
- **Java streams**: `reduce(identity, accumulator)` vs `reduce(accumulator)` vs `reduce(identity, accumulator, combiner)` — overloads express optional params.
- **BigInteger/BigDecimal**: constructors and `valueOf` overloads for different inputs.
- **Guava**: `ImmutableList.of()` with 0..n overloads — overloading drives the fluent API (and why Guava uses varargs for >n).
- **Every library**: convenience overloads are how libraries keep one conceptual method accessible with optional parameters — with the compatibility caution above.

## 17. References
- Java Language Specification, §8.4.9 (Overloading), §15.12 (Method Invocation Expressions, resolution): https://docs.oracle.com/javase/specs/jls/se17/html/jls-15.html
- Joshua Bloch, *Effective Java* — Item 52 (use overloading judiciously).
- Oracle Java Tutorials, "Defining Methods (overloading)": https://docs.oracle.com/javase/tutorial/java/javaOO/methods.html
- GeeksForGeeks, "Method Overloading in Java": https://www.geeksforgeeks.org/method-overloading-in-java/

## 18. Cheat Sheet
- Overloading = same name, different parameter list; resolved at compile time.
- Return type is NOT part of the signature — can't overload on it.
- Resolution phases: exact → widening → boxing → varargs; most specific wins.
- Ties (e.g., `null` for two reference types) = ambiguity error.
- int literals don't narrow to byte/short automatically.
- Overloading ≠ overriding (runtime).
- Adding an overload can silently change existing call sites.
- Constructors overload by parameter lists only.

## 19. Quiz
1. Overloading is resolved: a) at runtime b) at compile time c) by vtable d) randomly → **b**
2. Can two methods differ only by return type? a) yes b) no c) only private d) only static → **b**
3. `m(null)` with `m(String)` & `m(Integer)` is: a) picks String b) ambiguous c) picks Integer d) NPE → **b**
4. Resolution order: a) varargs first b) exact first c) boxing first d) widening first → **b**
5. `foo(5)` with `foo(byte)`/`foo(short)` only: a) picks byte b) picks short c) compile error d) runtime error → **c**
6. True or False: Overriding and overloading can coexist in one subclass. → **True**

## 20. Flashcards
- **Q: What is overloading?** → **A:** Same name, different parameter lists; compile-time (static) resolution.
- **Q: Return type in overloading?** → **A:** Not part of the signature — never a discriminator.
- **Q: Resolution phases?** → **A:** Exact → widening → boxing → varargs; most specific wins.
- **Q: `null` ambiguity?** → **A:** Yes — two equally-specific reference overloads → compile error.
- **Q: Overloading vs overriding?** → **A:** Static/signature vs runtime/dispatch; both are polymorphism.
- **Q: Why is it "compile-time polymorphism"?** → **A:** The compiler picks the implementation from static types; no vtable.

## 21. Revision
Method overloading is ad-hoc, compile-time polymorphism: same name, different parameter lists, resolved by the compiler (exact → widening → boxing → varargs; most specific wins). Return type never discriminates. Ties (like `null`) are ambiguity errors; int literals don't auto-narrow. Adding overloads can silently re-route existing calls. Overloading ≠ overriding — one is static signature matching, the other is runtime vtable dispatch. First-30-seconds answers: "overloading = compile-time, same name different params, no return-type overloading."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is method overloading?" | Formal Definition / Section 13 |
| "Overload on return type?" | Interview Q2 |
| "Overloading vs overriding?" | Interview Q3 |
| "Resolution order?" | Interview Q4 / Internal Working |
| "`m(null)` ambiguity?" | Interview Q5 |
| "Why compile-time polymorphism?" | Interview Q6 |
| "Int-literal narrowing trap?" | Interview Q12 |
| "Risk of adding overloads?" | Interview Q10 |
