# Java Modern OOP: Records, Sealed Classes and Patterns — 100 Interview Q&A

## Q1: What is a record in Java and why was it introduced?

**A:** A record is a type of class whose purpose is to carry immutable data. Introduced as a preview in Java 14 and finalized in Java 16, it collapses the boilerplate of a POJO: fields, constructor, accessors, `equals()`, `hashCode()`, and `toString()` are all generated automatically from the component list.

```java
// Instead of ~40 lines of boilerplate
class Point {
    private final int x;
    private final int y;
    Point(int x, int y) { this.x = x; this.y = y; }
    int x() { return x; }
    int y() { return y; }
    boolean equals(Object o) { ... }
    int hashCode() { ... }
    String toString() { ... }
}

// You write this
public record Point(int x, int y) {}
```

Records were introduced to encourage the "data carrier" idiom: immutable, value-based objects whose equality is defined by their state, not their identity. They also serve as the data side of a bigger modernization — combined with sealed classes and pattern matching, they give Java algebraic data type (ADT) capabilities previously found only in Kotlin, Scala, or Haskell.

Why not just keep writing POJOs? Because boilerplate invites bugs: hand-written `equals`/`hashCode` drift, mutable fields breaking hash-based collections, and copy-paste errors. Records remove the entire class of accidental state mutation bugs.

## Q2: What are the components of a record?

**A:** A record's components are the list of fields declared in its header. They are the source of everything generated.

```java
public record User(String name, String email, int age) { }
```

Here `name`, `email`, `age` are components. From them the compiler generates:

1. A **canonical constructor** that assigns each component to a `private final` field.
2. **Accessor methods** named exactly like the components (`name()`, `email()`, `age()`) — NOT `getName()`.
3. **`equals(Object)`**, **`hashCode()`**, and **`toString()`** using all components.
4. Private final fields backing the components.

Components are implicitly `private final`. You cannot declare a field with the same name as a component. You CAN declare additional static fields, static methods, instance methods, nested types, and static initializers. You cannot declare non-static (instance) fields outside components — that would break the "immutable data carrier" invariant (an instance field can't be set through the constructor, so it would always be default, or you'd have to mutate — prohibited).

```java
public record Circle(double radius) {
    // static allowed
    public static final double TAU = 2 * Math.PI;

    // instance method allowed
    public double area() { return Math.PI * radius * radius; }

    // instance field — NOT allowed
    // private String hidden;  // compile error
}
```

Components must be declared first thing after the header; you reorder them? No — order is significant because field names, constructor params, accessors, equals/hashCode/toString all mirror it.

## Q3: What is the canonical constructor in a record?

**A:** The canonical constructor is the constructor whose parameter list exactly matches the record's component list. It is generated automatically to initialize all fields. You can provide your own version via the "compact constructor" — a constructor with no parameter list that appears in the body.

```java
// Compact constructor — no parameter list!
public record Fraction(int numerator, int denominator) {
    public Fraction {
        if (denominator == 0) throw new IllegalArgumentException("denominator != 0");
        int g = gcd(Math.abs(numerator), Math.abs(denominator));
        numerator /= g;
        denominator /= g;
        if (denominator < 0) {
            numerator = -numerator;
            denominator = -denominator;
        }
    }
}
```

Inside the compact constructor, the parameters are available by their component names (`numerator`, `denominator`). Assigning to them (`numerator /= g`) is legal — it stores the normalized value into the final field. You cannot leave a component unassigned.

If you need the "long form" (explicit parameters), you can also write a normal constructor with the same signature as the header — but the compact form is usually cleaner for validation and normalization.

The canonical constructor enforces invariants at the single creation point. Every instance — however created — passes through it, guaranteeing validation everywhere.

## Q4: How are accessors named and why aren't they `getX()`?

**A:** Record accessors are named after the components themselves: `user.name()`, not `user.getName()`. Java's naming convention for methods that just read state is the same-name method, and records formalize that.

```java
public record Money(BigDecimal amount, String currency) {
    // currency() already generated
    public boolean isUsd() { return "USD".equals(currency); }
}
```

Why not `getX()`?
- Records avoid the confusion between the field and the method; readability improves (`amount()` reads naturally in fluent code).
- It distinguishes records from traditional JavaBeans. JavaBeans used `getX` because reflection-based frameworks (EL, JSP, older serialization) matched on that convention. Records don't need legacy bean compatibility.
- Jackson and other JSON libraries already support records via the component/accessor shape, and library support for `x()` naming is complete in current releases.

You can explicitly override an accessor with your own implementation (for defensive copies or normalization on read), and the convention remains `x()`:

```java
public record Board(Point[] cells) {
    public Point[] cells() { return cells.clone(); }  // defensive copy on read
}
```

The takeaway: `getName()` is JavaBean heritage; `name()` is the record idiom. Frameworks targeting beans vs. records must be told which convention to expect.

## Q5: What `equals`, `hashCode`, and `toString` does a record generate?

**A:** A record generates value-based implementations:

- `equals(Object)` returns true only if the other object is a record of the SAME type and all corresponding components are `Objects.equals`-equal.
- `hashCode()` is derived from all components (via `Objects.hash(...)` semantics) so the contract `equals => same hash` holds.
- `toString()` produces `<RecordName>[component1=value1, component2=value2]`, e.g. `Point[x=1, y=2]`.

```java
record Point(int x, int y) {}

Point a = new Point(1, 2);
Point b = new Point(1, 2);
System.out.println(a.equals(b)); // true — value equality, not identity
System.out.println(a.hashCode() == b.hashCode()); // true
System.out.println(new Point(1, 2)); // Point[x=1, y=2]
```

Key consequences:
- Use records for map keys and set elements freely — value equality is exactly what you want there.
- `equals` compares COMPONENTS as-in. If a component is an array or a collection, the comparison is reference-based (arrays) or element-based (lists/maps) depending on the component type. Do not rely on record equality for mutable components.
- Records do NOT implement `Comparable` automatically; you add it yourself if you need natural order.

You can override these methods in the body, but doing so usually signals that a record is the wrong type. Semantically, a record that needs custom equality should probably be a regular class.

## Q6: Are records immutable? What are the limits?

**A:** Records enforce shallow immutability. The components are `private final` — the reference cannot be reassigned, and you cannot add instance fields. But the OBJECTS that components point to can be mutable.

```java
record Team(String name, List<String> members) {}
// members is final — cannot assign a new list
// but team.members().add("x") IS possible — mutates the list held by the record
```

To reach deep immutability:
- Defensive copies: either at construction (clone the input) or on access.
- Use immutable component types in the first place: `List.copyOf(...)`, `Map.copyOf(...)`, `Set.copyOf(...)`, `Optional` (which forbids null), Java time types, etc.

```java
record Team(String name, List<String> members) {
    Team {
        members = List.copyOf(members);  // unmodifiable, disallows null
    }
}
```

Limits to keep in mind:
- A record cannot extend another class (it implicitly extends `java.lang.Record`).
- It cannot have mutable instance fields.
- The canonical constructor is the only guaranteed construction point — you cannot "mutate" a record instance after creation.

So: records are immutable in the reference sense and structurally immutable IF their component types are immutable. For total immutability guarantees, prefer immutable component types + `List.copyOf` normalization in the compact constructor.

## Q7: Can a record have methods? Can it implement interfaces?

**A:** Yes, on both counts. Records are classes, so they can have:

- Instance methods (regular behavior).
- Static methods and static fields.
- Custom accessor overrides.
- Compact or explicit constructors.
- Nested types (including records).

```java
public sealed interface Shape permits Circle, Rectangle {}

public record Circle(double radius) implements Shape {
    public double area() { return Math.PI * radius * radius; }

    public static Circle unit() { return new Circle(1); }

    @Override
    public String toString() { return "circle(radius=" + radius + ")"; }
}
```

And they can implement interfaces:

```java
public record Money(BigDecimal amount, String currency) implements Comparable<Money> {
    @Override
    public int compareTo(Money o) {
        return this.amount.compareTo(o.amount);
    }
}
```

What they CANNOT do:
- Extend a class (`record X extends Y` — forbidden; the base is fixed to `Record`).
- Have instance (non-static) fields beyond components.

The combination "record implements Comparable/Serializable/interface" is idiomatic — data + one small behavior (ordering, formatting) is fine. If a record needs substantial behavior, consider whether the behavior belongs in the record or in a separate service/function.

## Q8: Can a record be extended (subclassed)?

**A:** No. Records are implicitly `final`; you cannot subclass them, and a record cannot extend any other class (it must extend `java.lang.Record`). A record cannot be `abstract` either — an abstract record is a contradiction in terms.

```java
public record Point(int x, int y) {}        // implicitly final

// Illegal
public class ColoredPoint extends Point { } // compile error
public record Sub() extends Point { }       // compile error
```

Consequences for design:
- Records cannot be used as "base classes." Keep records leaf types.
- Interfaces are the extension mechanism: a record implements interfaces; the interface may be sealed.
- Records cannot be made `abstract` and later implemented — so a record family for variants is done with a sealed interface + multiple records, one per variant.
- The immutability guarantee is airtight — no subclass can add mutable state or break invariants.

This is a deliberate trade. Java records are strict about "a data carrier is final because data carriers that can be extended invite mutation creep." The replacement pattern is sealed interfaces: closed set of record implementations.

```java
public sealed interface Result permits Success, Failure {}
record Success(Object data) implements Result {}
record Failure(String error) implements Result {}
```

## Q9: Do records work with Jackson/Gson serialization?

**A:** Yes — modern Jackson (2.12+) and Gson (2.10+) support records natively; older versions needed modules like `jackson-module-parameter-names` or Kotlin-style reflection hacks. Records serialize naturally because Jackson's databind now introspects record components rather than JavaBeans getters.

```java
public record User(String name, int age) {}

ObjectMapper mapper = new ObjectMapper();
String json = mapper.writeValueAsString(new User("Alice", 30));
// {"name":"Alice","age":30}

// Deserialization works through the canonical constructor:
User u = mapper.readValue(json, User.class);
```

Design considerations when serializing records:
- **Deserialization validation**: The canonical (compact) constructor runs on deserialization, so your invariants (e.g., reject negative age) are enforced even for untrusted input. This is a real advantage over POJOs.
- **Unknown properties**: By default, Jackson fails on unknown JSON properties. Configure `FAIL_ON_UNKNOWN_PROPERTIES=false` if strictness is unwanted.
- **Component names**: The JSON field names match component names by default. `@JsonProperty` still works for mapping/renaming.
- **Sensitivity**: `@JsonIgnore` on a component is awkward — you can't technically ignore a component. Instead, avoid widespread reliance and use a separate DTO projected without the sensitive field. Are records safe as DTOs? Yes, and they're the recommended DTO shape.
- **Records + polymorphism**: When using Jackson's `@JsonTypeInfo` with records implementing an interface, records work, but the type mapping must be configured.

Records are now the default recommended DTO type for serialization — immutable, validated-at-construction, and framework-supported.

## Q10: What is the difference between a record and an ordinary immutable class?

**A:** A record and an ordinary immutable class (all fields final, no setters, `equals`/`hashCode`/`toString` written manually) are functionally equivalent, but records bake the semantics into the language:

- **Generated members**: equals/hashCode/toString/accessors are generated and kept in sync with the component list automatically. A hand-written immutable class risks drift.
- **Canonical construction**: Only ONE constructor signature is supported (well, extras delegating via `this(...)`). Ordinary immutable classes allow any constructor shape; records standardize it.
- **Restrictions**: Records are final, cannot have instance state beyond components, can't extend classes. Ordinary immutable classes have no such compiler enforcement — you must police by discipline.
- **Reflection & pattern matching**: Records announce their shape via the `RecordComponent` metadata; JVM protocols (serialization, Jackson, Hibernate, pattern matching) treat records specially.
- **Semantics**: Records are value-based ("equals by state"); ordinary classes default to identity equality unless you override.

```java
// Ordinary immutable class — all due diligence manual
public final class Point {
    private final int x, y;
    public Point(int x, int y) { this.x = x; this.y = y; }
    public int x() { return x; }
    // equals/hashCode/toString to be written by hand
}

// Record — identical semantics, zero manual code
public record Point(int x, int y) {}
```

The takeaway: use records by default for immutable data holders. Use an ordinary immutable class when you need construction flexibility beyond the canonical shape, custom equality that can't derive from components, or inheritance of an abstract base.

## Q11: What is a sealed class?

**A:** A sealed class restricts which classes can extend or implement it. The `sealed` modifier, together with an optional `permits` clause, enumerates the allowed subtypes.

```java
public abstract sealed class Shape permits Circle, Triangle, Rectangle {
    public abstract double area();
}

// Every permitted subtype must be final, sealed, or non-sealed
public final class Circle extends Shape { /* ... */ }

// Was omitted from permits → compile error if extended elsewhere
```

Key rules:
- All permitted subtypes must be in the same module; if the sealed class is in an unnamed module, the subtypes must be in the same package.
- A permitted subclass must be marked `final`, `sealed`, or `non-sealed`.
- If you omit `permits`, the subtypes are implied to be any classes in the same file/source unit.
- The classes in `permits` must actually extend/implement the sealed type — the compiler checks.
- A sealed class can be abstract or concrete (though concrete+sealed means none of its instances except the direct ones... effectively abstract is usual).
- Sealed works for interfaces too: `sealed interface X permits A, B {}`.

The purpose: gives the compiler a closed, known set of subtypes. This enables exhaustive pattern matching (switch over the sealed type is guaranteed complete) and protects invariants of the hierarchy. It's the language-level mechanism that makes algebraic data types practical.

```java
public sealed interface Operation permits Add, Subtract, Multiply {
    int apply(int a, int b);
}
record Add() implements Operation { public int apply(int a, int b) { return a + b; } }
```

## Q12: What is the `permits` clause and when is it needed?

**A:** The `permits` clause enumerates the direct permitted subtypes of a sealed class/interface. Without it, Java assumes the permitted types are all subtypes declared in the same file as the sealed type.

```java
// File: Shape.java — permits inferred to same-file subtypes
sealed interface Shape permits Circle, Square {}
record Circle(int r) implements Shape {}
record Square(int side) implements Shape {}

// Explicit permits — the subtypes can live in the same package, other files
package geom;
public sealed interface Shape permits geom.Circle, geom.Square {}
```

Rules/details:
- If the sealed type is in an unnamed module, permitted subtypes must be in the same package (regardless of file).
- If it's in a named module, subtypes may be in different packages within that module; then `permits` is required.
- Every class named in `permits` must directly extend/implement the sealed type.
- Subtypes may be nested inside the sealed type, referenced as `Shape.Circle`.
- If your sealed type has a `permits` that lists a nested subtype, use its qualified name.

Practical guidance: if all subtypes are in one file, consider nesting them or keeping them top-level in the same file — then `permits` is optional. If subtypes span files in the same package, use `permits` explicitly — it documents the closed set. If you want a subtype that allows further (unrestricted) extension, declare it `non-sealed`.

```java
sealed interface Shape {
    record Circle(int r) implements Shape {}
    record Square(int side) implements Shape {}
}
```

## Q13: What are the restrictions on subtypes of a sealed class?

**A:** Each permitted subtype must be one of:

1. **`final`** — no further subclassing. Most common; makes the variant truly closed.
2. **`sealed`** — permits its own closed set of descendants, extending the hierarchy one more level while keeping it closed.
3. **`non-sealed`** — explicitly reopens the hierarchy: any class can extend it. Rarely used; it "leaks" the closed boundary.

```java
// Node has a closed set of subtypes: Leaf, Composite
sealed interface Node permits Leaf, Composite {}

final class Leaf implements Node {}

// Composite is itself sealed — console sees only two leaf composites
sealed class Composite implements Node permits Group, Folder {}
final class Group extends Composite {}
final class Folder extends Composite {}

// An escaped subtype
non-sealed class Anything extends Shape {}
```

Additional restrictions:
- The permitted subtypes must be in the same module (or same package for unnamed modules).
- They must be directly related (extends/implements the sealed type; a transitive grandchild alone isn't permitted — only direct children).
- A permitted class cannot cross a module boundary (e.g., no separate "shape-plugins" module).
- The sealed type itself cannot be instantiated outside its permits — effectively its constructor is restricted to permitted subclasses.

Non-sealed is a pragmatic escape hatch, but overuse defeats the point of sealed. For airtight ADTs, keep every permitted subtype `final`.

## Q14: Can interfaces be sealed? What is the difference from sealed classes?

**A:** Yes, interfaces can be sealed, and for modern ADT-style modeling they're the more common choice.

```java
public sealed interface Payment permits Card, UPI, Wallet {}
public record Card(String number, String expiry) implements Payment {}
public record UPI(String vpa) implements Payment {}
public record Wallet(String walletId) implements Payment {}
```

Differences from sealed classes:
- Sealed interfaces permit only classes that `implements` them (records, classes). A sealed interface with permitted subtypes that are interfaces is allowed too — an interface can permit another interface.
- Implementation: `record ... implements Payment`, or `class X implements Payment`.
- You get multiple-inheritance-of-type benefits: a `CardPayment` record can implement `Payment` AND `Comparable`, `Serializable`.
- Sealed interfaces are the canonical way to model sum types ("one of"): the contract says "these are all the ways this type can appear."

```java
public sealed interface Result<T> permits Ok<T>, Err<T> {}
public record Ok<T>(T value) implements Result<T> {}
public record Err<T>(String message) implements Result<T> {}
```

Where sealed classes still win: when you need a shared, protected (not fully abstract) implementation — that is, common fields/methods with private/protected access among subtypes. Interfaces can't carry instance fields, so if the shared description includes state, sealed abstract classes are the fit.

Typical guidance: prefer sealed interfaces for pure type contracts; use sealed abstract classes when the variants must share implementation details or package-private access.

## Q15: What is pattern matching for `instanceof`?

**A:** Pattern matching for `instanceof` (preview Java 15, finalized Java 16) lets you combine a type test with a variable binding in one step.

```java
// Old way
if (obj instanceof String) {
    String s = (String) obj;          // explicit cast, easy to forget
    System.out.println(s.toUpperCase());
}

// Modern way
if (obj instanceof String s) {
    System.out.println(s.toUpperCase());  // s is in scope, typed String
}
```

Details:
- Scope: the pattern variable `s` is in scope only where the `instanceof` check definitely succeeded: the if/else branch, the `&&` continuation, the ternary.
- `&&` chaining: `if (obj instanceof String s && s.length() > 3)` — `s` usable after the check.
- `||` binding: In `if (obj instanceof String s || ...)` you cannot reference `s` in a branch where the check might be false — compiler enforces definite assignment.
- Works in non-sealed hierarchies fine (any type bound).
- `instanceof` still returns `false` for `null` even with a pattern.

```java
public double area(Object o) {
    if (o instanceof Circle c) return Math.PI * c.radius() * c.radius();
    if (o instanceof Square s) return s.side() * s.side();
    throw new IllegalArgumentException("Unknown: " + o);
}
```

This is the first rung of the pattern-matching ladder. Combined with `switch` expressions and sealed types, you get compiler-checked exhaustive dispatch, eliminating the instanceof-chain + cast boilerplate entirely.

## Q16: What is a switch expression and how does it differ from a switch statement?

**A:** A switch expression produces a value and assigns it; a switch statement only performs side effects.

```java
// Statement (classic) — no value, must use break or fall-through discipline
switch (day) {
    case MONDAY:
        System.out.println("start");
        break;
    default:
        System.out.println("normal");
}

// Expression (Java 14+) — yields a value
int workingHours = switch (day) {
    case MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY -> 8;
    case SATURDAY, SUNDAY -> 0;
};
```

Differences and features:
- Arrow syntax (`->`) with implicit `break`/no fall-through; the right-hand side is a single expression, block (`{ ... yield value; }`), or throw.
- `yield` returns a value from a block arm.
- Exhaustiveness: switch expressions over enums must be exhaustive or provide a `default`.
- Case labels can group constants: `case MONDAY, TUESDAY -> ...`.
- Selector types: `int`, `String`, enums, and (Java 21+) reference types with patterns.
- A switch statement (old) never exhausts; a switch expression always produces a value (or throws).

```java
String describe(int x) {
    return switch (x) {
        case 0 -> "zero";
        case 1, 2, 3 -> "small";
        default -> "large";   // required for int
    };
}
```

The modern idiom is switch expressions with pattern labels over sealed types — giving a value-producing, exhaustive dispatch table. That's the combination that replaces visitor patterns and chains of if-else.

## Q17: What is a type pattern in a switch?

**A:** A type pattern is a case label of the form `case Type var -> ...`, matching values of the given type (or a subtype) and binding them to the variable.

```java
sealed interface Shape permits Circle, Rectangle {}
record Circle(double radius) implements Shape {}
record Rectangle(double w, double h) implements Shape {}

double area(Shape s) {
    return switch (s) {
        case Circle c    -> Math.PI * c.radius() * c.radius();
        case Rectangle r -> r.w() * r.h();
    };
}
```

Behavior:
- Checks `s instanceof Circle`, binds `c`; checks `s instanceof Rectangle`, binds `r`.
- Order matters — later cases can be unreachable (the compiler rejects unreachable patterns, e.g. a `Shape` case after `Circle`).
- Works with regular classes too, not only sealed: `case String s -> ...`, `case Integer i -> ...`.
- Mixed with `null`: `case null -> ...` matches null; without it, null falls through to `default`/fails.
- Guarded patterns: `case Circle c when c.radius() > 10 -> "big circle"` — a guard refines a type pattern.

Exhaustiveness: For sealed types the compiler knows the full list — missing a permitted subtype is a compile error. For open hierarchies you need a `default` arm. This makes switch-based dispatch both safe and complete.

```java
String describe(Object o) {
    return switch (o) {
        case null -> "nil";
        case String s when s.isBlank() -> "blank";
        case String s -> "text:" + s;
        case Integer i -> "int:" + i;
        default -> "unknown";
    };
}
```

## Q18: How do records, sealed classes, and pattern matching combine?

**A:** Together they form Java's answer to algebraic data types (ADTs) and exhaustive, type-safe dispatch.

- **Records** model the "product" part: each variant holds its fields.
- **Sealed types** model the "sum" part: one type, a closed set of variants.
- **Pattern matching** (switch + instanceof) does the decomposition: extract the variant and its fields safely.

```java
sealed interface Expr permits Num, Var, Add, Mul {}

record Num(double value) implements Expr {}
record Var(String name) implements Expr {}
record Add(Expr l, Expr r) implements Expr {}
record Mul(Expr l, Expr r) implements Expr {}

double eval(Expr e, java.util.Map<String, Double> env) {
    return switch (e) {
        case Num n                  -> n.value();
        case Var v                  -> env.getOrDefault(v.name(), 0.0);
        case Add a                  -> eval(a.l(), env) + eval(a.r(), env);
        case Mul m                  -> eval(m.l(), env) * eval(m.r(), env);
    };
}
```

The compiler guarantees exhaustiveness: add a new `Expr`, and every `switch` on it fails to compile until the new case is handled. That's a massive correctness win versus the visitor pattern or chains of if-else with casts.

Bonus: with record patterns (nested destructuring) you can match into the structure:

```java
// With record patterns (nested)
String classify(Expr e) {
    return switch (e) {
        case Add(Num x, Num y) -> "add of literals: " + (x.value() + y.value());
        case Mul(Num x, Num y) -> "square/times: " + (x.value() * y.value());
        default -> "complex";
    };
}
```

This trio is the recommended style for domain models with a fixed set of variants (result types, state machines, ASTs, error unions).

## Q19: What is the `non-sealed` modifier?

**A:** `non-sealed` reopens a permitted subtype to unrestricted further subclassing — it's the "escape hatch" in a sealed hierarchy.

```java
sealed interface Shape permits Circle, OpenShape {}

final class Circle implements Shape {}

// OpenShape escapes the closure — anyone can extend it
non-sealed interface OpenShape extends Shape {}
```

Semantics:
- Only a DIRECT permitted subtype can be `non-sealed` (it must appear in the parent's `permits`).
- After `non-sealed`, the type loses its participation in the sealed closure: you can extend/implement it freely, and the compiler no longer knows the full set of its subtypes.
- Consequences for exhaustiveness: any switch over `Shape` still covers `Circle` and `OpenShape`, but anything behind `OpenShape` is unknown — so a switch handling the sealed type must cover `OpenShape` and may need a `default` for its open descendants.

When to use it:
- When a variant genuinely needs plugin-style extension (e.g., a "CustomHandler" that third parties implement).
- To allow a mix: some variants tightly modeled, one variant reserved for open extension.
- Generally, prefer NOT to use it — non-sealed defeats the sealed guarantees. Model all variants, or split the hierarchy (solve "one open world" by adding an interface that itself is open).

It's the explicit acknowledgment that sometimes closed is too strict; `non-sealed` makes the openness loud and deliberate rather than accidental.

## Q20: What is the `when` clause in a switch pattern?

**A:** The `when` clause (also called a guard) is an additional boolean condition attached to a case label; the case matches only if the guard is true.

```java
sealed interface Shape permits Circle, Box {}
record Circle(double r) implements Shape {}
record Box(double w, double h) implements Shape {}

String classify(Shape s) {
    return switch (s) {
        case Circle c when c.r() > 10  -> "big circle";
        case Circle c                  -> "small circle";
        case Box b when b.w() == b.h() -> "square";
        case Box b                     -> "rectangle";
    };
}
```

Rules:
- The pattern variable (e.g., `c`) is in scope inside the guard AND in the case body.
- Guards can chain multiple conditions; they cannot be arbitrary statements — just a boolean expression.
- If the guard fails, the compiler tries the NEXT case. Ordering of guards matters.
- A guard does not make a case "definitely matched," so you can't add a later unguarded `default` when some guarded patterns might still fall through — the compiler tracks whether every value is covered.
- Exhaustiveness: treating guarded patterns, the compiler may require a final catch-all or an unguarded last case to guarantee coverage. If coverage isn't provable, you get a compile error demanding a `default`.

```java
record Person(String name, int age) {}

String adultOrMinor(Person p) {
    return switch (p) {
        case Person q when q.age() >= 18 -> "adult";
        // need an unguarded case for < 18
        case Person q -> "minor";
    };
}
```

Guards make switch patterns expressive: instead of writing separate visitor logic, conditions live inline beside the type.

## Q21: What is a `record pattern` and how does destructuring work?

**A:** A record pattern deconstructs a record into its components directly in a pattern. `case Circle(double r) -> ...` binds the radius.

```java
sealed interface Shape permits Circle, Box {}
record Circle(double r) implements Shape {}
record Box(double w, double h) implements Shape {}

String classify(Shape s) {
    return switch (s) {
        case Circle(double r) when r > 10 -> "big circle r=" + r;
        case Circle(double r)             -> "circle r=" + r;
        case Box(double w, double h)      -> "box " + w + "x" + h;
    };
}
```

Nested destructuring — patterns compose:

```java
record Wrapper(Shape inner) {}
// matches Circle wrapped directly inside Wrapper
case Wrapper(Circle(double r)) -> "wrapped circle of r=" + r;
case Wrapper(Shape s)          -> "wrapped " + s;
```

Behaviors to note:
- The component names in the pattern are variable declarations: `double r` binds r. Their types must match the component types (or be wider).
- Patterns can match against more general components via type patterns within the parentheses.
- `var` is allowed: `case Circle(var r)`; the compiler infers the component type.
- Record patterns work in `instanceof` too: `if (p instanceof Point(int x, int y))`.
- Compile-time verifies the pattern's component types vs. the record's accessors; accessing a component calls the accessor.

Record patterns give you Guava-style "destructuring" built into the language, eliminating the boilerplate of repeated `.field()` access in the body — and they compose infinitely, making deeply nested ADT dispatch clean.

## Q22: What is `switch` expression exhaustiveness and why is it enforced?

**A:** Exhaustiveness means a switch over a given type covers every possible value. For enums and sealed types, the compiler enforces it on switch expressions: if any case is missing, compilation fails.

```java
enum Direction { NORTH, SOUTH, EAST, WEST }

int value(Direction d) {
    return switch (d) {              // exhaustiveness required
        case NORTH -> 0;
        case SOUTH -> 100;
        case EAST -> 50;
        case WEST -> -50;
    };
}
```

Why enforced:
- A switch expression must produce a value on every path. If a value slips through unmatched, the expression would return nothing — so the compiler forces completeness (`default` or all cases).
- When you add a new enum constant (or a new sealed subtype), EVERY switch expression quietly becomes a compile error — surfacing missing handling at build time instead of runtime defaulting.

```java
// Enumerating a new case fails compilation until handled
// new enum case UP; the switch above now errors
```

Subtleties:
- Guarded patterns don't guarantee coverage, so the compiler may still demand a catch-all.
- `default` is allowed and suppresses the exhaustiveness demand — use it when you genuinely have unknown types (open hierarchies).
- For sealed hierarchies, exhaustiveness is checked structurally: all permitted subtypes, or a `default`.
- Pattern checks are more specific than constants; ordering matters for reachability.

The real benefit: compile-time "total" functions. No runtime `EnumSwitch` fallthrough, no `IllegalStateException` from unhandled cases — the compiler guarantees it. This is industrial-strength typed dispatch.

## Q23: What Java version introduced records, sealed classes, and pattern matching?

**A:** All three landed in the Java 14–21 era:

- **14** (March 2020): Records and pattern matching for `instanceof` as PREVIEW features. Statement `switch` expressions finalized in 14.
- **15** (Sept 2020): Sealed classes preview; records still preview.
- **16** (March 2021): Records and pattern matching for `instanceof` FINALIZED. Sealed classes still preview.
- **17** (Sept 2021): Sealed classes FINALIZED. (LTS release.)
- **18**–**20**: Preview iterations for pattern matching for `switch`, plus record patterns preview.
- **21** (Sept 2021, LTS): Pattern matching for `switch` and record patterns FINALIZED in Java 21.

So the practical answer:
- Records: Java 16+
- Sealed classes/interfaces: Java 17+
- Pattern matching for instanceof: Java 16+
- Switch patterns + record patterns: Java 21+ (also backported to some LTS toolchains via preview).

```text
Java 14  preview  records, instanceof patterns
Java 16  final    records, instanceof patterns
Java 17  final    sealed types
Java 21  final    switch patterns, record patterns
```

If your codebase is on Java 17 (LTS), you get records + sealed + instanceof patterns, but switch patterns need Java 21. Many enterprises standardize on 17; knowing which feature is in which release is a common interview axis.

## Q24: Can a record be used as a map key?

**A:** Yes, and it's one of the best uses — records give value equality with stable hash codes.

```java
record GeoKey(double lat, double lon) {}

Map<GeoKey, String> cities = new HashMap<>();
cities.put(new GeoKey(40.71, -74.00), "New York");
System.out.println(cities.get(new GeoKey(40.71, -74.00))); // New York
```

Why records make great keys:
- **Immutable** — cannot mutate after construction, so the hash can't change while inside the map (avoids the "lost key" bug).
- **Value-based equals/hashCode** — two records with equal components are equal; hashing matches.
- **Compact construction** — normalization (e.g., rounding lat/lon) runs in the constructor, keeping keys canonical:

```java
record GeoKey(double lat, double lon) {
    GeoKey {
        lat = Math.round(lat * 1e6) / 1e6;
        lon = Math.round(lon * 1e6) / 1e6;
    }
}
```

Caveats:
- If a component is a mutable list/array, records are still equal by the component's `equals` — for lists that's element equality (and arrays are identity-based, so normalize arrays to lists). Prefer immutable component types.
- USE within maps and sets frequently requires custom ordering → add `Comparable` when natural ordering is needed.
- Records have no `.clone()` and no copying tool like Kotlin's `copy`; to alter a key, construct a new record.

In short: records are the cleanest possible HashMap/HashSet keys in modern Java — value semantics without the boxed-key pitfalls of mutable POJOs.

## Q25: How do records help with API design (DTOs, return types)?

**A:** Records give you compact, immutable, self-documenting data carriers — ideal for the boundaries between components.

```java
// API response type
public record CreateOrderResponse(String orderId, String status, BigDecimal total) {}

// Service-internal result (with validation in the compact constructor)
public record OrderSummary(OrderId id, Money total, int lineCount) {
    public OrderSummary {
        Objects.requireNonNull(id);
        Objects.requireNonNull(total);
        if (lineCount < 0) throw new IllegalArgumentException("lineCount >= 0");
    }
}
```

Design benefits:

1. **Immutable boundary objects**: Callers can't accidentally mutate a response. With POJO DTOs, mutable fields invite races and accidental writes.
2. **Concise API**: The header IS the documentation — component names and types show the full contract at a glance.
3. **Equals/hashCode for free**: Testing, caching (as map keys), and comparison use generated value equality.
4. **Fails-fast validation**: Compact constructor enforces invariants for all creation paths, including deserialization.
5. **Directly supported by frameworks**: Jackson, validation libraries (Jakarta Bean Validation since 3.0), and JDBC/DAO mappings handle records.

Anti-patterns to avoid:
- Records for objects with mutable domain state (like JPA entities — records make Hibernate's dirty-checking painful; use regular classes for entities).
- Records that leak internals without defensive copies when exposing immutable views of mutable collections.

Recommended split: records for the API/transport layer (DTOs, events, commands), classes for domain entities with behavior and identity. This is the modern default recommendation at FAANG-scale Java backends.


## Q26: How do records interact with inheritance and interfaces?

**A:** Records cannot extend a class or another record — they are implicitly `final` and extend `java.lang.Record`. What they CAN do:

1. **Implement interfaces**: fully supported, including generic and sealed interfaces.
```java
public sealed interface Payment permits CardPay, WallePay {}
public record CardPay(String number, String exp) implements Payment {}
```
2. **Be nested inside other types** (classes, interfaces, records, enums).
3. **Contain nested types** themselves.

So "record inheritance" is really "record implements interfaces." The design:

```java
public interface Describable { String describe(); }

public record Point(int x, int y) implements Describable {
    public String describe() { return "(" + x + ", " + y + ")"; }
}
```

Why records are final: because the record's contract (value semantics, generated equality, immutable components, canonical constructor) would fray the moment subclassing is allowed. A subclass could add fields, breaking equals/hashCode symmetry, or override accessors to return different values — the invariants Java guarantees for records would be unverifiable.

Practical pattern: build a hierarchy with an INTERFACE for the variants (ideally sealed), each variant a record implementing it. This gives you multiple inheritance of type, sealed exhaustiveness, and immutable data.

```java
sealed interface Shape permits Circle, Square {}
record Circle(double r) implements Shape {}
record Square(double side) implements Shape {}
```

So the answer: records don't extend, they implement. To model a family of related records, use a (sealed) interface.

## Q27: What is the difference between a sealed class and an abstract class with subclasses?

**A:** Both restrict instantiation and define a common base, but sealed adds a compiler-enforced, closed set of subtypes:

| Aspect | abstract class + open subclasses | sealed class + permits |
|---|---|---|
| Subtype set | Unknown, open (any class may extend) | Compiler-known, closed (`permits`) |
| Exhaustive switch | Impossible (unknown subtypes) | Compiler-enforced (must cover all) |
| Extensibility | Trivial (new subclass anywhere) | Restricted (same module/package) |
| The "closed world" guarantee | None | Yes |
| Design intent | Reuse + polymorphism over an open model | Finite variant model (ADT-style) |

```java
// Open — anyone in the codebase (or dependency) can extend
public abstract class Animal { }

// Closed — compiler knows the full set is Cat, Dog
public abstract sealed class Pet permits Cat, Dog { }
final class Cat extends Pet { }
final class Dog extends Pet { }
```

What remains the same: shared fields/methods, abstract methods, Liskov reasoning.

Differences that matter in interviews:
- An abstract class is open BY DEFAULT. Your `default` branch in code over abstract classes is usually "handle unknown" — whereas over a sealed you omit the "unknown" handling and the compiler keeps it exhaustive.
- Abstract classes allow trivially extending third-party libs; sealed types force the plugin extension to happen within the module (or through a `non-sealed` escape hatch you explicitly provide).
- Sealed types interact with records and pattern matching in ways abstract+open cannot: exhaustive switches, and effectively sum types.

Summary: use abstract for open extensibility (strategy/provider/plugin). Use sealed when the set of variants is a domain truth ("direction", "payment method", "result state") and you want the compiler to force completeness.

## Q28: What are the Java keywords introduced for sealed classes?

**A:** Four: `sealed`, `permits`, `non-sealed`, and — newly reused — nothing else. Specifically:

- `sealed` — marks a class or interface as having a closed set of permitted subtypes.
- `permits` — names the direct permitted subtypes. Optional if all permitted types are declared in the same source file.
- `non-sealed` — marks a permitted subtype as explicitly OPEN (escapes the closed set).
- `final` — already existed; a permitted subtype declared `final` closes the branch.

```java
public sealed interface Command
    permits Start, Stop, ConfigCommand {}

public record Start() implements Command {}          // final by being a record
public record Stop() implements Command {}           // final

public abstract sealed class ConfigCommand implements Command
    permits StaticConfig, DynamicConfig {}

public final class StaticConfig extends ConfigCommand {}
public final class DynamicConfig extends ConfigCommand {}
```

Rules relevant here:
- `sealed`, `permits`, `non-sealed` have no other meanings in the language — they were added (as contextual? Actually sealed/permits/non-sealed are reserved keywords/modifiers) in JEP 409.
- A permitted subtype MUST be one of `final`, `sealed`, or `non-sealed` — that triad is enforced for every class named in `permits` (or, for same-file/inferred cases, in the file).
- Records and enums are implicitly final supports this trio.

So, exactly three new keywords: `sealed`, `permits`, `non-sealed` (plus reusing the existing `final`). Being able to list them precisely is a quick check interviewers use.

## Q29: When would you choose a sealed interface over a sealed class?

**A:** Choose sealed INTERFACE when the variants carry no shared STATE and you want type-multiple-inheritance or record-based variants:

```java
// Sealed interface — the norm for ADTs
public sealed interface Result<T> permits Success, Failure {}
public record Success<T>(T value) implements Result<T> {}
public record Failure<T>(String error) implements Result<T> {}
```

Choose sealed CLASS when a common implementation or shared protected access is required:

```java
// Sealed abstract class — variants share state/behavior
public abstract sealed class Shape permits Circle, Box {
    protected final String fillColor;
    Shape(String fillColor) { this.fillColor = fillColor; }
    public abstract double area();
    public String description() { return "shape(fill=" + fillColor + ")"; }
}
final class Circle extends Shape {
    private final double r;
    Circle(double r, String color) { super(color); this.r = r; }
    public double area() { return Math.PI * r * r; }
}
```

Decision table:
| Need | Choose |
|---|---|
| Records as variants | sealed interface |
| Multiple interfaces per variant | sealed interface |
| Zero shared state | sealed interface |
| Shared protected fields / constructors | sealed class |
| Private access among variants | sealed class |
| Public API for parsing/serialization | sealed interface (records) |

Also note: a sealed interface can permit OTHER interfaces (java `sealed interface A permits B {}` where B is also an interface). That's useful for layered hierarchies.

In practice, the sealed-interface + records approach is the modern default because records give immutability and value equality for free.

## Q30: How do you handle exhaustive switch when the sealed type is nested?

**A:** Nested types and exhaustiveness work the same as top-level — the compiler understands qualified nested types in case labels.

```java
public sealed interface Shape {
    record Circle(double r) implements Shape {}
    record Box(double w, double h) implements Shape {}
}

double area(Shape s) {
    return switch (s) {
        case Shape.Circle c -> Math.PI * c.r() * c.r();
        case Shape.Box b -> b.w() * b.h();
    };
}
```

`case Shape.Circle c` — the qualified name still binds `c`. If the records are nested but the sealed interface is in the same file, `permits` is optional.

For deeply nested (record-in-record) there's no special handling — patterns compose:

```java
public sealed interface Expr {}
record Pair(Expr l, Expr r) implements Expr {}

// A pair of literals...
record Lit(int n) implements Expr {}

int sumValues(Expr e) {
    return switch (e) {
        case Pair(Lit a, Lit b) -> a.n() + b.n();
        case Lit n -> n.n();
        default -> throw new IllegalStateException("not exhaustive");
    };
}
```

The nuance when nesting: if a nested record implements a sealed interface but you reference it via the outer name in a switch, use the qualified name (`Outer.Inner`). The compiler still performs full exhaustiveness across all permitted subtypes — including nested ones.

The real gotcha: when permitted subtypes are declared in the same file as the sealed interface, `permits` may be omitted, but if you miss a subtype entirely, the set is implied from same-file classes; once you name ANY `permits`, the list is authoritative — missing a subtype is a compile error.

## Q31: What is the interaction between sealed types and serialization?

**A:** Sealed types have meaningful serialization implications — both trust and safety:

- The closed subtype set gives your deserializer a guaranteed "universe" of types. Combined with a whitelist registry, you ensure only known variants can be deserialized (fighting gadget-chain attacks).
- The compiler-verified uniqueness of sealed types makes polymorphism serialization unambiguous where type IDs are stable.

```java
@JsonTypeInfo(use = Id.NAME, property = "type")
@JsonSubTypes({
    @JsonSubTypes.Type(value = OmakaseCustomerDto.class, name = "omakase"),
    @JsonSubTypes.Type(value = FreemiumCustomerDto.class, name = "freemium"),
})
public sealed interface CustomerDto {
    record OmakaseCustomerDto(String name) implements CustomerDto {}
    record FreemiumCustomerDto(String name, int planLevel) implements CustomerDto {}
}
```

Considerations:
1. **Records + sealed**: Jackson serializes records naturally; deserialization runs the canonical constructor, so invariants (in compact constructor) are enforced on hostile input — good.
2. **Versioning**: `@JsonTypeInfo` names are stable; changing a record's component names breaks old payloads — evolve by adding records, not renaming components.
3. **Not for JPA entities**: Records + sealed are transport/dtos; entities should stay as mutable classes because Hibernate requires no-arg constructor & setters.
4. **`serialization UID`**: For Java serialization, records serialize through canonical constructors (not reflection over fields) — safer, and sealed-ness doesn't change that. Records make Serializable less dangerous because the constructor runs and enforces validation.

So the "API designed with sealed + records" is the safest modern shape: whitelisted variants, immutable deserialization, and validation in the constructor.

## Q32: How do records handle `clone()`, `finalize()`, and `wait/notify`?

**A:** Records keep the Object methods with modified semantics:

- **`clone()`**: Records do NOT implement `Cloneable`. Calling `clone()` throws `CloneNotSupportedException` (unless the record or a component tree makes it cloneable — but records deliberately don't). They encourage immutable value types where clone is pointless: to "copy", construct a new record.
- **`finalize()`**: Deprecated since Java 9, removed in Java 18 (JEP 421 removed finalization). Records inherit from Object but never finalize; no override is generated. Good — value types shouldn't finalize.
- **`wait/notify/notifyAll`**: Inherited from Object — technically available. But records are pure value classes; using monitor methods on them is pointless and subtly dangerous (records as keys/=lock objects can produce identity surprises; two "equal" records are different objects with separate monitors). Don't synchronize on records.

Important nuance: `getClass()` — records return the actual record class. `finalize()` is gone.

What records DO redefine: `equals`, `hashCode`, and `toString` (value semantics). `clone`, `finalize`, monitor methods are inherited from Object (or removed in modern JDKs).

```java
record Point(int x, int y) {}

Point p = new Point(1, 2);
try {
    p.clone(); // CloneNotSupportedException
} catch (CloneNotSupportedException e) { /* expected */ }
```

One more: `String`-style invariant — all record instances are "definitely equal to each other if same components". This "value-based" behavior warns against identity-monitor usage (`synchronized(record)`).

Senior takeaway: records should be treated like primitives-in-a-box — copy by reconstruction, never synchronize, never finalize.

## Q33: What serialization caveats exist when a record's component is a mutable collection?

**A:** The record itself is shallow-immutable, but the mutable component can be mutated or escaped, breaking value semantics.

```java
record Team(String name, List<String> members) {}

var t = new Team("rockets", new ArrayList<>(List.of("a", "b")));
t.members().add("c");        // mutates the list INSIDE the record — no longer "immutable"
t.members().clear();         // empty — equals/hashCode have changed
```

Consequences:
- `hashCode()` changes after mutation → using the record as a map key becomes unsafe (lost lookups).
- Serialization roundtrips can produce unexpected structures when the internal mutable collection is referenced elsewhere (aliasing).
- Equality becomes fragile depending on mutation timing.

Solutions:

1. **Normalize during construction** — unmodifiable copy:
```java
record Team(String name, List<String> members) {
    Team {
        members = List.copyOf(members);   // throws on null elements, unmodifiable
    }
    @Override
    public List<String> members() { return members; }  // view already immutable
}
```

2. **Defensive accessors** — return clones:
```java
public List<String> members() { return new ArrayList<>(members); }
```
(More overhead but protects against caller aliasing when callers pass AND read.)

3. **Prefer immutable component types**: use `List.copyOf`, `Map.copyOf`, `Set.copyOf`, `ImmutableList` (Guava), or streams-based collectors. Then deep immutability is structural.

The "gotcha" interviewers probe: shallow vs deep immutability, and whether a defensive copy is made on construction OR access (or both). Prefer both-normalization at the boundary and treated components as read-only.

## Q34: What is the relationship between records and `java.lang.Record`?

**A:** Every record class extends `java.lang.Record` implicitly — the JVM's base class for records (analogous to `Enum`, the base for enum types).

- Records can't extend anything else — `Record` is the superclass.
- `Record` is an abstract final-ish class (yes, `Record` is abstract and can't be instantiated directly) exposing:
  - `equals(Object)` — abstract.
  - `hashCode()` — abstract.
  - `toString()` — abstract.
  - A single protected no-arg constructor (the reflective machinery constructs records).

The JVM defines a "record" via the `javac`-generated `Record` attribute; the `Record` class and the `RecordComponent[]` reflection API let tools discover record semantics:

```java
Class<?> clz = User.class;
if (clz.isRecord()) {
    RecordComponent[] comps = <User record components>;
    for (RecordComponent rc : ...) {
        System.out.println(rc.getName());           // component names
        System.out.println(rc.getGenericType());    // types
        rc.getAccessor().invoke(instance);          // invoke the accessor
    }
}
```

Why this matters:
- Frameworks (Jackson, Hibernate validation, Spring) check `isRecord()` to route to record-aware construction and serialization.
- The language spec forbids extending `Record` except for record definitions.

Note: `Record` is `java.lang.Record`, a class, not special-cased in the JVM's verifier — the "recordness" is data in bytecode attributes. Tools must use reflection `Class.isRecord()` and `RecordComponent`.

Thus: records get a language-level base + metadata that POJOs lack; frameworks use that metadata instead of guessing getter/setter naming conventions.

## Q35: What does `Class.isRecord()` tell you, and how is it used by frameworks?

**A:** `Class.isRecord()` returns `true` for record classes. Combined with the `RecordComponent[]` metadata, frameworks detect and enforce record-aware behavior.

```java
if (Person.class.isRecord()) {
    // access record components
    for (RecordComponent rc : Person.class.getRecordComponents()) {
        System.out.println(rc.getName() + ": " + rc.getType());
    }
}
```

What frameworks do with it:

1. **Jackson**: uses record components for field binding (names, and accessors) instead of bean getters; deserialization through the canonical constructor.
2. **Hibernate Validator / Bean Validation 3.0**: `@Valid` on record components; validation framework inspects the canonical constructor.
3. **Spring Data / JDBC**: record-based projections result from `SELECT` into `record Foo(Long id, String name)`.
4. **Object mappers (MapStruct)**: detect record accessors for source/target mapping.
5. **Serialization**: `Record` uses the canonical constructor to deserialize (rather than reflection over instance fields), enabling validation on hostile input.

Caveat: `isRecord()` doesn't mean "everything auto-works." Frameworks must explicitly support `RecordComponent`. Older libs treat records as beans with no default constructor → break. That's the CLI reality: check framework versions.

Reactive libraries (Guava Preconditions, Lombok) treat records like final classes — nothing special needed.

So `isRecord()` is the runtime signal that the class:
- Has canonical components (via `getRecordComponents()`).
- Uses value semantics (equal by state).
- Is construction-time-validated (canonical constructor path).

## Q36: What is the difference between `record` and an enum?

**A:** Both are value-ish, but they model different things: an enum is a fixed, small set of NAMED instances; a record is a data carrier with arbitrary values.

| Aspect | `enum` | `record` |
|---|---|---|
| Instance set | Finite, fixed at compile time (constants) | Unbounded (new records anytime) |
| Equality | By identity (singleton per constant) | By value (all components) |
| State | Immutable enum constants (may have fields) | Immutable components |
| Construction | `Enum` base, private constructor per constant | Canonical constructor |
| Patterns | Enum constants match `case MONDAY` | Record patterns destructure |
| Extends | extends `java.lang.Enum` | extends `java.lang.Record` |
| Nested | Can nest types | Can nest types |
| Ordering | `ordinal()` built-in | No ordinal; add Comparable manually |

```java
enum Direction { NORTH(0), SOUTH(1), EAST(2), WEST(3);
    private final int deg;
    Direction(int deg){ this.deg = deg; }
    int degrees(){ return deg; }
}

record Point(int x, int y) {}
```

When to use which:
- Use `enum` for a finite known set of distinct values: status (ACTIVE/BLOCKED/UNKNOWN), modes, directions, category codes.
- Use sealed(`record`) hierarchy when each variant carries different data: `sealed interface Status permits Ok(...), Error(...)`, Payload variants, AST nodes.

Interplay: an enum is a kind of value type; records are the "payload" carrier. A classic design: an enum selector maps to record-backed subtypes via a switch.

```java
switch (direction) {
    case NORTH -> new Point(0, -1);
    case SOUTH -> new Point(0, 1);
    // exhaustive by enum
}
```

## Q37: Can records be used in multi-threaded contexts safely?

**A:** Records are safe in concurrent contexts BECAUSE of immutability — no mutable state that can be torn or half-written. Any thread reading the fields of a properly published record (publication through a stable reference, volatile, or an appropriate happens-before) observes the fully-constructed state.

But two caveats:

1. **Publication**: If you share a record reference without synchronization, it's the standard visibility problem — the reference (if observed) may observe partially initialized fields? Actually, since all fields are final, Java's "final field semantics" guarantee that once the constructor completes, ANY thread that reads the reference to that constructed object (even without synchronization) sees the final-field values correctly — provided the reference itself is safely published (e.g., through a shared volatile/static). So records enjoy the strong final-field guarantee automatically.

2. **Component mutability**: If a component is a mutable `List`, the LIST is shared mutable state. `members().add(...)` from multiple threads races. Records do nothing to protect that: normalize with `List.copyOf` at construction and treat components as immutable.

```java
record Stats(long hits, long total) { 
    static volatile Stats current = new Stats(0, 0);
    static synchronized void bump() {
        long h = current.hits() + 1;
        long t = current.total() + 1;
        current = new Stats(h, t);   // safe publication via volatile — replaces immutable snapshot
    }
}
```

Patterns that exploit record immutability:
- **Immutable snapshots** (as above), avoiding locks.
- **Cache keys** and dedup sets — no risk of hash corruption.
- **Event payloads / messages** in queues — no shared mutable state.

So the answer: records are concurrency-friendly by construction, as long as the components are immutable. You get final-field visibility guarantees and safe value semantics for free, but you must keep the CONTENTS immutable too.

## Q38: What is a local/static/nested record?

**A:** Records can be declared in many scopes:

1. **Top-level**: usual (file name matches).
2. **Nested** (member): inside another class/interface — implicitly static.
3. **Local** (inside a method/constructor): allowed — and they can capture effectively final locals, like lambdas.
4. **Inside ANSI bodies?** — also allowed within method bodies, static initializers, etc.

```java
public class Outer {
    // nested (member) — implicitly static
    record Inner(int a) {}

    void method() {
        // local record — captures effectively-final local
        record Result(double sum, int count) {}
        Result r = new Result(42.0, 1);
        System.out.println(r.sum());
    }
}
```

Why local records matter:
- Great for defining a small intermediate ADT inside an algorithm (pair of results) without leaking it as a top-level type.
- The local record has its own scope; it cannot be static (a local record is implicitly static?) — actually local records are NOT implicitly static and are declared inside a method (like local classes), so they CANNOT have static members except constants, and they cannot have static initializers. They CAN capture effectively-final method locals.

Rules: local records cannot be annotated with some type-use annotations, can't be generic? (No — local records CAN be generic). Local records are final-like.

Practical: use local records mainly for multi-value returns and algorithm-local ADTs:

```java
public Optional<Interval> narrowest(Interval a, Interval b) {
    record Pair(Interval a, Interval b) {}   // local record
    return Optional.of(new Pair(a, b))...
}
```

When scope creeps, promote to an actual `record` at class level.

## Q39: What is the relationship between records and object pooling?

**A:** Records are value-based and immutable — the natural targets for sharing/caching:

- Since `new Point(1,2).equals(new Point(1,2))` and hashCodes match, interchangeable. So you can safely REPLACE a record instance with an equal instance — enabling canonicalization (e.g., intern them).
- `Integer`/`String` style: JVM might (JEP 190) cache/intern common value types. Records being value-based means a future JVM can deduplicate equal records safely.

Pooling considerations:
- Pooling trades allocation for lookup overhead. Records are cheap to construct; pools only pay off if equals cost is low AND lifecycle is high-churn.
- Use `Map<K, Record>` as an interning registry keyed by a canonical key:
```java
private static final ConcurrentMap<GeoKey, GeoKey> POOL = new ConcurrentHashMap<>();
GeoKey intern(GeoKey k) {
    return POOL.computeIfAbsent(k, Function.identity());  // reuses existing
}
```
- Thread-safety: immutable records are safe to share; the POOL map itself must be concurrent (as above).

Big caveat: pooling is a memory control decision, not a correctness one. A record's identity is irrelevant (value semantics); equal records are interchangeable — which is exactly why pooling is safe. Contrast with a mutable entity class where identity matters.

Don't over-engineer: modern JVMs allocate cheaply; profiling usually shows pooling is not the bottleneck. Interning is worth it when the same record value repeats thousands of times (like geo-coordinate keys).

## Q40: Do records support zero-arg constructors?

**A:** Records generate a canonical constructor whose parameters match all components — so a record with ZERO components is the only record with a zero-arg canonical constructor:

```java
record Empty() {}          // canonical constructor: Empty()
record Something(int a) {} // canonical constructor: Something(int)
```

There is NO implicit no-arg constructor for a record that has components. You can't write `new Person()` when `Person(int id, String name)` is the shape.

You CAN define additional overloaded constructors that delegate to the canonical one via `this(...)`:

```java
record Person(String name, int age) {
    // overload — must delegate to canonical
    public Person(String name) {
        this(name, 0);
    }
}
```

Rules:
- Every constructor must ultimately call the canonical constructor (`this(...)`) — no `super()` invocation is allowed directly.
- The canonical compact constructor (`public Person { ... }`) has no parameter list and no `this(...)` call.
- You cannot give a record an "extra" no-arg constructor unless it delegates: `public Person() { this("default", 0); }`.

This is at the heart of the "no default no-arg constructor" property — which affects frameworks relying on reflection `newInstance()` (bean-style containers, Hibernate). That's precisely WHY records are (mostly) unsuitable for JPA entity classes. Frameworks that understand records fetch the canonical constructor or components instead.

Zero-component records are useful as type markers (variants without data in a sealed ADT):

```java
sealed interface JsonValue permits JsonNumber, JsonNull, JsonString, JsonArray {}
record JsonNull() implements JsonValue {}   // zero args — fine
```

## Q41: What is the difference between switch statement and switch expression in terms of fall-through?

**A:** The classic switch statement uses fall-through (unless you `break` or `return`); a switch expression uses `->` arms, which never fall through (with arrow syntax), or block arms whose last expression is `yield`.

```java
// STATEMENT — fall-through hazard
int j = 0;
switch (day) {
    case MONDAY:
    case TUESDAY:
        j = 1;
        break;          // explicit break needed
    case WEDNESDAY:
        j = 2;
        // fall-through → j becomes 3 below if we forget break!
    case THURSDAY:
        j = 3;
        break;
}

// EXPRESSION — never falls through; grouping handled by comma lists
int j = switch (day) {
    case MONDAY, TUESDAY -> 1;
    case WEDNESDAY, THURSDAY -> 2;
    default -> 3;
};
```

Rules for the expression form:
- Arrow cases implicitly don't fall through; you group with `case A, B ->`.
- Block cases: `case X -> { int r = compute(); yield r; }` — the `yield` value exits the arm; no fall-through by design.
- No `break`; `yield` only in expression.
- Mandatory exhaustiveness via `default` when not provably total.

The old statement with `->` also doesn't fall through (Java 14 allowed `->` in statements too, with the same semantics, just without producing a value).

For interview: the key phrase is "arrow form has no fall-through; expression form requires a value on every path (exhaustive)." Break vs yield are the two control-transfer keywords.

## Q42: How do you express "default behavior" in a switch expression over a sealed type?

**A:** You have two options:

1. **Add a `default` arm** — this suppresses exhaustiveness, so the compiler no longer forces you to enumerate every permitted subtype:

```java
String classify(Shape s) {
    return switch (s) {
        case Circle c -> "circle";
        default -> "other";   // Box, Triangle, future types unknown
    };
}
```

2. **Prefer NOT to use `default`** — with exhaustive sealed types, reserve a dedicated catch-all ARM (a "null-or-other" pattern):

```java
String classify(Shape s) {
    return switch (s) {
        case null -> "nil";                          // explicit null handling
        case Circle c -> "circle";
        case Box b -> "bounding box";
        // Box is the only remaining permitted subtype → exhaustive
    };
}
```

Why avoid `default`:
- It defeats the compiler's exhaustiveness checking — future subtypes slip silently into `default`.
- It's a semantic shorthand that hides missing logic (dangerous: a new variant silently "falls through" to default).

Occasionally `default` is legitimate — when the sealed type has a `non-sealed` subtype you can't enumerate. Then a default IS the correct model for the open part.

For "family default", another idiomatic pattern is a design-level default in the interface: a `default String describe()` in the sealed interface, overridden only by specific records → base behavior shared, with pattern matching reserved for the distinguishing logic.

So prefer explicit exhaustive arms (± null) and use `default` only when an open branch REQUIRES it (non-sealed subtrees, or genuinely open hierarchies).

## Q43: What is the interaction between pattern matching and `Optional`?

**A:** Pattern matching lets you destructure `Optional` in a switch without `.isPresent()` / `.get()` ceremony — though the idiomatic path remains composition:

```java
Optional<String> maybe = get(id);

// Functional style — recommended
maybe.ifPresent(s -> ...);
String value = maybe.orElseThrow(() -> new NotFound(id));
```

Pattern matching with Optional is possible but awkward; the cleaner decomposition:

```java
String out = switch (maybe.orElse(null)) {
    case String s -> s.toUpperCase();
    case null -> "none";
};
```

Extracting the inner type: `switch (maybe)` can't match on the wrapped value directly (Optional isn't a record pattern; you'd need `case Optional<String> o` and then `o.orElse(null)`). Since Java 21, `Optional` is not a record — the design guidance is:

- Prefer `flatMap`, `map`, `orElse`, `stream()` for transformations.
- Use pattern matching when the handling BLOCK is large and imperative: destructure `Optional<T>` into "present/absent".

```java
sealed interface Maybe<T> permits Just<T>, Nothing {}
record Just<T>(T value) implements Maybe<T> {}
record Nothing() implements Maybe<T> {}

// Your own sum type gives pattern matching for free
String describe(Maybe<String> m) {
    return switch (m) {
        case Just(String v) -> "value=" + v;
        case Nothing() -> "nothing";
    };
}
```

The real "Optional + patterns" story: `Optional` composition is the idiomatic path; if you constantly need `switch` on presence, consider a custom ADT (Just/Nothing) or stream operations. `Optional.ofNullable(it)` + `orElse` covers most.

But pattern matching shines when a single switch handles nullable/enum/record/boxed uniformly — combine:

```java
switch (input) {
    case null -> "none";
    case Optional<String> o when o.isPresent() -> o.get();
    case String s -> s;
    case Integer i -> String.valueOf(i * 2);
    default -> "unknown";
}
```

## Q44: How do records interact with reflection?

**A:** Records have first-class reflection support:

- `Class.isRecord()` — true for records.
- `getRecordComponents()` → `RecordComponent[]`, with `getName()`, `getType()`, `getGenericType()`, `getAccessor()`, `getAnnotations()`.
- `getConstructor(componentTypes...)` — the canonical constructor is available (including package-private).
- `Class.getDeclaredFields()` sees the backing fields.
- `getMethods()` includes accessors (named after components) — NOT bean getters.

```java
record User(String name, int age) {}

Class<User> c = User.class;
System.out.println(c.isRecord());
for (RecordComponent rc : c.getRecordComponents()) {
    System.out.println(rc.getName() + " -> " + rc.getGenericType());
}
Method accessor = c.getRecordComponents()[0].getAccessor();
Object value = accessor.invoke(new User("Ann", 30));
```

Framework use:
- Jackson: `isRecord()` → map JSON names to component names, invoke accessors on serialization; on deserialization build via the canonical constructor.
- Prorities: records' canonical constructor runs validation → deserialization enforces it.

Caveats:
- The canonical constructor's PARAMETER NAMES are metadata (via `-parameters` or embedded names). Get name/type from `getRecordComponents()`.
- Some libraries incorrectly assume a no-arg constructor — guard with `isRecord()` when integrating.
- `getDeclaredConstructor` vs canonical: use `getRecordComponents()` + type resolution; there is no "generic canonical constructor" method call.
- Serialization (Java native): records serialize via the canonical constructor (see `ObjectInputFilter` discussion).

This reflection surface is how "modern Java frameworks" (Spring, Jackson, Vert.x, Micronaut) deliver record support without resorting to hacks.

## Q45: What happens if you try to `new` an abstract record?

**A:** You can't — abstract records don't exist, because records are implicitly `final`. `abstract record X(...)` is a compile error. Every record is concrete and instantiable (visible constructor).

```java
record Shape(double size) {} // fine
abstract record Shape2(double size) {} // compile error: 'abstract' not allowed
```

Wait — records CAN be declared abstract if... no. Let me be precise: the JLS forbids `abstract` modifier on records because a record with abstract methods or abstract status cannot exist (records can implement interfaces which may carry abstract methods, but the record itself must implement them). The compiler rejects `abstract` on a record declaration.

Consequences:
- You can't subclass to add behavior; behavior must live in the record body (methods) and its components.
- The only hierarchy tool for "multiple shapes with different structure" is sealed interfaces + multiple records.
- A record can't be partially defined; all components always exist.

So:

```java
sealed interface Shape permits Circle, Triangle {}   // the "abstract" layer
record Circle(double r) implements Shape {}
record Triangle(double base, double height) implements Shape {}
```

The sealed interface IS the abstraction; records are concrete leaves. If you need abstract behavior (a method every variant must implement), declare it in the sealed interface (or a default method), and each record overrides it. Records can't be abstract, but the abstraction lives one level up.

## Q46: What is the difference between a record's canonical constructor and a builder?

**A:** A record's canonical constructor is the single mandatory construction path — you MUST pass every component. A builder allows incremental, optional, validated construction.

- Record's compact constructor: validates + normalizes; no optional fields; single signature.
- Static factory + builder: flexible assembly (optional params, validation, fluent).

```java
record HttpRequest(String method, String url, Map<String,String> headers, byte[] body) {
    HttpRequest {
        Objects.requireNonNull(method);
        Objects.requireNonNull(url);
        headers = Map.copyOf(headers);
        body = body == null ? new byte[0] : body.clone();
    }
}

// Builder-style factory for complex requests
static HttpRequest of(String method, String url) {
    return new HttpRequest(method, url, Map.of(), new byte[0]);
}
```

When do you actually want builder for records?

1. Many optional parameters (URL, headers, query, auth...) — record canonical makes you pass all.
2. Validation logic at multiple steps.
3. Chaining/dsl.

But: for many cases, records + a couple of overloads + `withX`-style copy methods suffice:

```java
record Config(String host, int port, boolean tls, int timeoutMs) {
    static final Config DEFAULT = new Config("localhost", 8080, true, 3000);
    Config withPort(int p) { return new Config(host, p, tls, timeoutMs); }
}
// Config.DEFAULT.withPort(8443)
```

Old-school builders become unnecessary. The trade-off isn't "record vs builder"; it's "record+copy vs builder-class." The 80/20 rule: records win for DTO/immutable value objects; a compact builder is only warranted when construction has dozens of optional axes and cross-parameter validation.

## Q47: Can a record contain a collection that is a component? Concerns with identity and hash.

**A:** Yes — a component can be any type, including collections. The caveats:

1. **Equality**: record equals uses component `equals`. A `List` component uses element equality (good); a `Set` uses set equality (order-independent, good); a `Map` similar; an ARRAY component uses identity equality (BAD for value semantics) — arrays don't override equals/hashCode.

```java
record Inventory(String sku, List<String> bins) {}
// bins equality is element-wise — good
record Snapshot(String name, File[] files) {}
// files equality is IDENTITY — two records with identical file arrays are NOT equal
```

2. **Mutability**: collections are mutable → breaking immutable contract and hash stability.

```java
List<String> bins = new ArrayList<>(List.of("A","B"));
Inventory inv = new Inventory("sk-1", bins);
inv.bins().add("C");        // mutation — inv.bins() now has 3 elements
// hashCode changed — if used as a key: risk of lost lookups.
```

3. **Defensive practices**:
```java
record Inventory(String sku, List<String> bins) {
    Inventory {
        bins = List.copyOf(bins);     // unmodifiable snapshot, no nulls
    }
    @Override
    public List<String> bins() { return bins; } // already safe (unmodifiable)
}
```

4. **Arrays**: avoid as components; wrap or convert to `List.copyOf(Arrays.asList(arr))`, or clone on access.

5. **Ordering**: with collections that are Sets, equality is order-independent but hashing must be consistent — use well-behaved immutable sets (`Set.copyOf` creates a LinkedHashSet — order stable, equals via Set). For maps same.

Summary: collections as components are fine IF you normalize at construction (`List.copyOf`, `Set.copyOf`, `Map.copyOf`) and avoid arrays. Otherwise you inherit aliasing, mutation, and unstable-hash bugs.

## Q48: What is the recommended way to create a copy of a record with one field changed?

**A:** Records don't auto-generate a `copy()` (unlike Kotlin's `data class`). Two idiomatic options:

1. **Inline reconstruction**: `new Point(p.x(), 99)`.

2. **Add a `withX` method**:
```java
record Point(int x, int y) {
    Point withY(int newY) { return new Point(x, newY); }
}
Point p = new Point(1, 2).withY(5); // Point[x=1, y=5]
```

For many components, a full "with" matrix is verbose — add only the ones you actually need, or provide a copy-with-builder style method:

```java
record Config(String host, int port, boolean tls, int timeout) {
    Config with(Port p) { return p == Port.DEFAULT ? this : new Config(host, p.value(), tls, timeout); }
}
```

Nested-record updates need explicit reconstruction:

```java
record Address(String street, String city) {}
record User(String name, Address address) {}
User u = new User("Ann", new Address("1 Main", "SF"));
User moved = new User(u.name(), new Address(u.address().street(), "Oakland"));
```

Java has NO built-in auto-copy (`with`); the Lisp/FP `with` isn't added. If you want automatic `copy(with=...)`, use a code generator library (e.g., Lombok doesn't do records well; some libraries like Guava or custom processors can), but the idiomatic plain-Java answer is a manual `withX` or reconstruction. For APIs with heavy immutable-object churn, provide dedicated `with` methods.

## Q49: What is the relationship between records and `Comparable`?

**A:** Records do NOT automatically implement `Comparable` — unlike Scala case classes (which don't either) — but value-based ordering is trivial to add when needed:

```java
record Score(int points) implements Comparable<Score> {
    public int compareTo(Score o) { return Integer.compare(points, o.points()); }
}
```

Design considerations:
- For multi-field natural ordering, use `Comparator`:

```java
record Rank(int score, String name) implements Comparable<Rank> {
    public int compareTo(Rank o) {
        return Comparator.comparingInt(Rank::score)
                         .thenComparing(Rank::name)
                         .compare(this, o);
    }
}
```

- Comparing by ALL components is not automatic; equals/hashCode/toString ARE. Ordering must be explicit.
- Use records in `TreeSet`/`TreeMap` requires `Comparable` or a `Comparator` — since records don't implement it by default, provide one:

```java
TreeSet<Score> set = new TreeSet<>(Comparator.comparingInt(Score::points));
```

- Keep compareTo consistent with equals()? Not strictly required by the language, but it is good practice (otherwise you get surprising set semantics: `compareTo==0` but `equals false`).

Note the difference: equals/hashCode are generated, compareTo is not. If you use a record as a key in a sorted structure, or sort lists of records, you must supply ordering. This is a common interview probe ("Can you sort records? Yes, via Comparable interface you add manually").

## Q50: What is a canonical constructor's relationship with frameworks that need default constructors?

**A:** Records have no implicit no-arg constructor — the canonical constructor requires all components. Frameworks designed for mutable beans (JPA with default no-arg + setters, Spring's old bean style, `newInstance()` reflection) break with records unless they support the canonical constructor.

Examples:
- **Hibernate/JPA**: Historically requires a no-arg constructor. Modern Hibernate 6 supports records for read-only projections but NOT as managed entities (they're immutable). So "record as entity" is a mismatch.
- **Jackson**: fine — supports records via component introspection + canonical constructor.
- **Bean Validation**: works via `@Valid` on components / canonical constructor parameter validation.
- **Spring**: DTOs as records fine; JDBC row mappers (`BeanPropertyRowMapper`) need beans — use `DataClassRowMapper` or record-aware mappers.

The upshot: a record's canonical constructor is its identity — validation lives there, so any integration path through that constructor preserves it. Frameworks that assume zero-arg + setters bypass this and should be avoided for records.

Workaround if a library insists on a no-arg constructor: define a delegating zero-arg constructor with defaults — but that's usually a smell. Better: pick a record-aware library or convert at the boundary:

```java
record UserDto(String name, int age) {
    // if REALLY needed
    public UserDto() { this("", 0); }
}
```

Senior takeaway: choose frameworks that understand records (Jackson 2.12+, Hibernate 6 for projections, MapStruct for mapping); otherwise map records at the boundaries via repositories/services and keep the framework's bean models separate.


## Q51: How do you model a state machine with sealed classes and records?

**A:** A state machine fits the sealed-type pattern beautifully: each state is a variant (record), and transitions are exhaustive functions over the state.

```java
sealed interface OrderState permits Created, Paid, Shipped, Delivered, Cancelled {}

record Created(Instant at) implements OrderState {}
record Paid(OrderId id, PaymentMethod method, Instant at) implements OrderState {}
record Shipped(OrderId id, Instant at) implements OrderState {}
record Delivered(OrderId id, Instant at) implements OrderState {}
record Cancelled(OrderId id, String reason, Instant at) implements OrderState {}

OrderState transition(OrderState current, Event ev) {
    return switch (current) {
        case Created c -> paid(c, ev);     // to Paid
        case Paid p   -> p.ship() ? new Shipped(p.id(), ev.at()) : current;
        case Shipped s-> delivered(s, ev);
        case Delivered d, Cancelled x -> current;   // terminal states
    };
}
```

Design wins:
- **Exhaustiveness**: adding `Refunded` state forces every switch to handle it — impossible to forget.
- **Validation in constructors**: `Paid` compact constructor can reject inconsistent payment details.
- **No invalid transitions silently**: a switch that doesn't handle a state does not compile.

Watch-outs:
- Illegal transitions are caught at compile time only if the switch is exhaustive AND you don't hide them behind `default`. Always write explicit arms, no catch-all.
- Nested/parallel state machines quickly outgrow this pattern; consider `enum` + transition tables for complex ones.
- Immutable records mean "transitioning" produces a new value rather than mutating — that's the FP-style state transition that many teams prefer anyway.

```java
sealed interface Payment {
    record Authorized(Money amount, String token) implements Payment {}
    record Captured(Money amount, String token, String authCode) implements Payment {}
    record Failed(Money amount, String error) implements Payment {}
}
```

This "records + sealed + switch" models the WHAT-IS-CURRENT and transitions without object graphs or mutable state — a strong improvement over classic OOP state machine implementations.

## Q52: What are record components and how are they different from fields?

**A:** Components are the logical elements declared in the record header; fields are the physical `private final` storage the compiler generates for them.

```java
record Person(String name, int age) {}
// Components: name, age
// Fields: private final String name; private final int age;
```

Differences:
- Components appear in: the canonical constructor (parameters), accessors (`name()`, `age()`), equals/hashCode/toString, reflection's `getRecordComponents()`.
- Fields: accessible `package-private`? Actually fields are `private final` — direct access only inside the record; external code reads via accessors.
- You can't declare a field with the same name as a component.
- Extra fields are allowed only as `static` — instance fields outside components are forbidden.

```java
record Book(String title) {
    public static final String UNKNOWN_AUTHOR = "anonymous";
    // public String extra; // ERROR: instance field not allowed
}
```

Reflection framing: `getRecordComponents()` gives the logical view (name, type, accessor); `getDeclaredFields()` gives the physical view (backing fields). Not always 1:1 conceptually — the component is the contract, the field is the storage.

Use component names for serialization binding (Jackson reads component names), and treat accessors as the read path (through `getRecordComponents()[i].getAccessor()`).

The key rule: "field" connotes implementation, "component" connotes the record's contract. When extending a record's API surface, touch components; when talking about internals, talk about fields.

## Q53: What is the difference between `record` and Kotlin's `data class`?

**A:** Both generate data-class boilerplate, but with important differences:

| Aspect | Java record | Kotlin data class |
|---|---|---|
| Immutability | Enforced (components final) | `val`/`var` — mutable allowed |
| `copy()` | Not generated | Generated |
| Destructuring | Record patterns (Java 21+) | `component1()`, component2... |
| Default values | No defaults in canonical | Supported (default params) |
| Zero-arg ctor | Only if no components | If all components have defaults |
| Inheritance | final, no extension | final, no extension |
| toString/equals/hc | Generated from components | Generated from `val/var` properties |
| Secondary constructors | Must delegate to canonical | Free (delegates optional) |
| Companion | N/A | `companion object` |
| Interface impl | Yes | Yes |

Kotlin:
```kotlin
data class User(val name: String, val age: Int = 0) {
    init { require(age >= 0) }
}
val u = User("Ann").copy(age = 30)
```

Java:
```java
record User(String name, int age) {
    User { if (age < 0) throw new IllegalArgumentException(); }
}
User u = new User("Ann", 0);
```

Practical notes:
- Kotlin data classes are more flexible (mutable `var` components, defaults, copy), Java records more restrictive but safer.
- `copy()` has no Java equivalent auto — add `with` methods manually if needed.
- Destructuring: Kotlin has componentN + `val (name, age) = user`; Java uses record patterns `case User(String name, int age) ->`.

Choose records when strict immutability and JVM-generic tooling matter (Jackson, etc.); Kotlin data classes when you need copy/defaults/mutability and are already on Kotlin.

## Q54: What is `sealed` in Kotlin and how does it compare?

**A:** Kotlin's `sealed class` (and `sealed interface`, stable since 1.5) is conceptually the same as Java's sealed types: closed set of subclasses. Differences:

```kotlin
sealed class Result {
    data class Success(val value: Any) : Result()
    data class Error(val msg: String) : Result()
}

fun describe(r: Result): String = when (r) {
    is Result.Success -> "ok: ${r.value}"
    is Result.Error -> "err: ${r.msg}"
}
```

- Kotlin: subtypes must be nested (or same file in Kotlin <1.5; since 1.5 allowed in same package/module depending on version). Java: same package/module, explicitly via permits.
- Kotlin enforces exhaustiveness at `when`; Java requires it for switch expressions (with `->`).
- Kotlin sealed classes can have data classes as subtypes (immutable), but Java's records supercharge the symmetry.
- Kotlin `sealed interface` is now common for exhaustiveness too.
- Kotlin when-blocks destructure with `is Success -> ...` and nested `val` in data class patterns; Java uses record patterns.

Migration notes:
- If you're on Kotlin and model ADTs with sealed + data classes, Java 17+ records + sealed + switch gives the same.
- Interop: records and sealed types are plain Java — Kotlin can consume them, but exhaustive `when` in Kotlin over a Java sealed type requires the same closed-set knowledge.

The "parent insight": both languages converge on the same ADT modeling; Kotlin got there earlier (2016), Java followed with records/sealed/patterns (2021-2023). Interviewers often ask which paradigm unifies them — exhaustion at compile time over closed trees.

## Q55: How do you test pattern-matching exhaustive switches?

**A:** Testing exhaustiveness is two-fold:

1. **Compile-time**: The compiler enforces it for sealed types. Add a new permitted subtype → all non-exhaustive switches fail. That's structural "testing" at build time.

```java
sealed interface Payment permits Card, Upi {}
switch (payment) { case Card c -> ...; } // compile error — Payment not exhaustive
```

2. **Runtime behavior**: For open hierarchies (interfaces, classes, non-sealed crosses), write tests that the `default` branch (or the unhandled path) behaves correctly:

```java
@Test
void unknownVariantHitsDefault() {
    // a subclass outside the sealed set
    class Custom extends Shape { ... }
    assertEquals("unknown", classify(new Custom()));
}
```

Test strategy:
- **Exhaustiveness tests** with one case per permitted subtype.
- **Guard tests**: hit every `when` branch — each guard true and false.
- **Ordering tests**: verify pattern precedence (guarded before unguarded, specific types before general).
- **Null tests** (sealed switch: `case null`, else pass through).
- **Combinatorial nested** record pattern tests: nested destructuring produces stack.

```java
@Test
void evalHandlesAllNodes() {
    assertAll(
        () -> assertEquals(3.0, eval(new Num(3))),
        () -> assertEquals(7.0, eval(new Add(new Num(3), new Num(4)))),
        () -> assertEquals(12.0, eval(new Mul(new Num(3), new Num(4))))
    );
}
```

Also worth testing:
- That a newly added subtype fails compilation in test code referencing the switch (a compile-finish assertion — more structural linting than test).
- That tokens/IDs for serialized forms stay stable if you add a subtype later (semantic version).

Senior note: let the compiler do the heavy lifting. When you add `record Refund(...) implements Payment`, all switches fail until updated — the build IS the exhaustive test. Runtime tests then focus on guard logic and the behavior of each branch.

## Q56: How do records compare to JavaBeans for serialization and frameworks?

**A:** Records and JavaBeans are fundamentally different modeling philosophies:

| Aspect | JavaBean (POJO) | Record |
|---|---|---|
| Fields | private + getters/setters | immutable components + accessors |
| Default ctor | Required (no-arg) | Not available (component ctors) |
| Mutability | Mutable (setters) | Immutable |
| equals/hashCode | Manual/reflection | Generated (value) |
| Framework support | Universal (beans) | Modern libs only (Jackson 2.12+, Hibernate 6 projection) |
| Validation | Bean Validation on fields/setters | Compact constructor |

Serialization:
- Jackson: both. Records bound by component names; beans by getter names.
- Java serialization: records serialize through the canonical constructor — validating on deserialization; beans use field access (can deserialize invalid objects).

Framework implications:
- ORM (Hibernate/JPA): beans natural (entities need mutable, proxyable). Records NOT for entities; Hibernate 6 supports read-only records as projections/DTOs.
- Validation: records fine with Bean Validation 3.0 (`@Valid` on components/params).
- MVVM/UI: beans historically; modern UI can use records as immutable DTOs.

```java
// Bean
public final class UserBean {
    private String name;
    public UserBean() {}
    public String getName() { return name; }
    public void setName(String n) { this.name = n; }
}

// Record
public record User(String name) {}
```

Guidance: prefer records for new DTO/API border types; keep JavaBeans where mutability, proxying, or legacy framework integration is mandatory (JPA entities, Spring form beans). Jackson/MapStruct/Hibernate projections handle records today.

## Q57: How do you use pattern matching with optionals and null in a switch?

**A:** Pattern matching lets you handle null and named types uniformly in one switch (Java 21):

```java
String classify(Object o) {
    return switch (o) {
        case null -> "nil";
        case String s -> "str:" + s;
        case Integer i -> "int:" + i;
        case Optional<String> os -> "opt:" + os.orElse("?");
        default -> "other";
    };
}
```

Rules for null:
- A `case null` matches the null value explicitly.
- Without `case null`, null falls through to `default` (if present) or throws `NullPointerException`.
- Combined with a type object that can be null: `case (SomeType t) when t != null` — but in the switch selector, null is handled before matching since `instanceof` returns false for null.

With Optional:
- `Optional` is not a record; you cannot destructure it with `case Optional(String s)`. Handle it as above: check via `.isPresent()`/`orElse`, or use a custom ADT (Just/Nothing) to destructure.

```java
sealed interface Maybe<T> permits Just, Nothing {}
record Just<T>(T value) implements Maybe<T> {}
record Nothing() implements Maybe<T> {}

String describe(Maybe<String> m) {
    return switch (m) {
        case Just(String s) -> "value=" + s;
        case Nothing() -> "none";
    };
}
```

Better still, switch over `Optional`'s presence explicitly:

```java
String resolve(Optional<String> maybe) {
    return switch (maybe) {
        case Optional<String> o when o.isPresent() -> "present: " + o.get();
        case Optional<String> o -> "empty";
    };
}
```

The cleanest answer: for nullables, use `case null`. For Optionals, prefer composition (map/orElse), but pattern-matching switches handle them when branching logic dominates. Never use `Objects.toString(o)` in a switch default — a string inferred too early.

## Q58: What are the benefits and drawbacks of `non-sealed`?

**A:** `non-sealed` escapes the closed hierarchy for one permitted subtype. Benefits:

- Allows plugin-style extension: third-party subclasses of one designated branch.
- Keeps the rest of the hierarchy sealed/enforceable (exhaustiveness for the others still checked).
- Explicitly marks the "open world" part of your model.

Drawbacks:

- Loses exhaustiveness: switch over the sealed type must cover the `non-sealed` subtype AND a `default` for its open descendants.
- The closed-set guarantee is diluted — unknown implementations can appear under that branch.
- Reflection/subtype scans (Spring et al.) may find arbitrary classes.

```java
public sealed interface Task permits ImmediateTask, DeferredTask, ExternalTask {}

// ImmediateTask & DeferredTask remain enumerated
// ExternalTask opens the door for any runtime-discovered implementation
non-sealed interface ExternalTask extends Task {}
```

Usage guidance:
- Reserve `non-sealed` for the genuinely extensible branch (e.g., vendor-provided handlers) and keep the domain core sealed.
- Prefer instead a separate interface with its OWN open hierarchy if possible — then the sealed part stays closed and the open part is explicitly opt-in.

```java
public sealed interface CoreCommand permits Create, Delete {}
public interface PlugCommand extends CoreCommand { /* open extension */ }
```

Downsides in interviews are worth pointing out clearly: `non-sealed` is rarely justified; usually the right move is to make THAT part a separate open interface rather than mixing open/closed in one sealed tree.

## Q59: How do records and sealed interfaces improve API design compared to inheritance-based polymorphism?

**A:** Inheritance-based polymorphism (abstract base + subtype classes) is behavior-oriented and open-aware; records + sealed interfaces push the model to "data first, exhaustive dispatch":

| Aspect | Abstract base + subclasses | Sealed + records |
|---|---|---|
| Subtype set | Open (unknown) | Closed (permits) |
| New operation | Edit every subclass (or visitor) | New switch function (no edits to variants) |
| New variant | Trivial (new class) | Edit sealed permits + update switches |
| State | Any | Immutable components |
| Exhaustive invariants | Runtime `instanceof` chains | Compile-time switch |

```java
// inheritance-based
abstract class Shape { abstract double area(); }
class Circle extends Shape { ... area(); }
class Square extends Shape { ... area(); }

// sealed+records
sealed interface Shape permits Circle, Square {}
record Circle(double r) implements Shape {}
record Square(double s) implements Shape {}
double area(Shape x) { return switch(x){ case Circle c->PI*c.r()*c.r(); case Square q->q.s()*q.s(); }; }
```

Benefits for API design:
- Client code enumerates exhaustively; no unhandled-unknown type.
- Adding behavior (prettyPrint, serialize, equals) doesn't touch data types; you add functions instead.
- Shape of data and behavior decouple — the compiler tracks completeness.

The principle heard in FAANG interviews: "Open/Closed" applies to VARIANT ADDITIONS (sealed was explicitly designed to make adding a variant require updating the permits, keeping the rest functionally closed), and Liskov is upheld structurally by the closed set.

Watch that sealed+records isn't used for genuinely open extensibility — that's a mismatch; the design tells you when to switch back to abstract classes.

## Q60: What is the recommended approach to handling `null` in records?

**A:** Records do not prevent null components; `Person(null, 30)` is legal. Design guidance:

1. **Validation in the compact constructor**:
```java
record Person(String name, int age) {
    Person {
        Objects.requireNonNull(name, "name");
        if (age < 0) throw new IllegalArgumentException("age >= 0");
    }
}
```

2. **Optional components**: don't store null stores — use `Optional`/`OptionalInt` or explicit fields:
```java
record User(String name, String email) {
    User { email = email == null ? "" : email; }   // normalize empty
}
```

3. **Factory/alternative constructors** to provide defaults:
```java
record Contact(String phone, String email) {
    Contact { phone = Objects.requireNonNullElse(phone, ""); ... }
    static Contact withoutPhone(String email) { return new Contact(null /* normalized */, email); }
}
```

4. **Collections as components**: normalize with `List.copyOf(col)` — rejects null elements and returns an immutable copy.

Where null is semantic:
- Some APIs need "absent" vs "empty string." For those, use `Optional` fields or explicit boolean/flag variants; nullable `String` in a record is acceptable but must be documented and validated.

Jackson deserialization: `null` JSON values become null components — the compact constructor can reject them (fail fast) or normalize them. This is where "validate at construction" pays off.

```java
record Money(@NotNull BigDecimal amount, @NotNull Currency currency) {
    Money {
        Objects.requireNonNull(amount);
        Objects.requireNonNull(currency);
    }
}
```

The senior-style answer: records + null is handled by (a) requiring non-null for fields that must be present (requireNonNull), (b) normalizing optional ones at construction, (c) choosing Optional/empty-collection facets for genuine absence. Hibernate/DB nulls map to Optional for query results.

## Q61: How do sealed types affect garbage collection or memory footprint?

**A:** Not directly. Sealed types add only the `permits` metadata in the class file — negligible. The memory/GC story is governed by the underlying data model:

- If sealed variants are RECORDS (immutable, no mutable state), limited mutations mean fewer writes, and immutable snapshots age out of young gen cleanly — but allocation still happens per event/record (except the JVM may fold value-based instances; no aggressive dedup by default).
- Sealed guarantees (known, closed set) ENABLE the JIT compiler's devirtualization and monomorphic call optimization — improving performance, not allocations. Instead of megamorphic calls across unknown subclasses, monomorphic call sites with sealed sets can inline.
- `non-sealed`/open subtrees lose some of those optimizations but don't change GC.

Senior measurement: records/sealed do NOT magically reduce allocations. If you're allocating a huge number of small records in a hot loop, consider:
- Value classes (Project Valhalla `inline class`) — future-proof design but not yet GA.
- Primitive-specialized data structures (custom `long`-keyed maps instead of `Record<Long,...>`) to avoid boxing.
- Object pooling of IMMUTABLE records (safe because value equality: equal records interchangeable).

```java
// hot loop allocating records — fine, but GC pressure
for (...) { Money m = new Money(amount, "USD"); ... }

// alternative: reuse canonical values when amounts repeat
Map<BigDecimal, Money> cache = new HashMap<>();
```

So the answer: sealed → better devirtualization/jit (performance), never more memory; records → value semantics allow pooling if allocation is hot; GC is orthogonal unless you mis-shape data (mutable collections as components).

## Q62: What is the recommended pattern for exception handling in records?

**A:** Records can't avoid exceptions — they throw them in the constructor or in behavior. Guidance:

1. **Constructor validation throws `IllegalArgumentException`/`NullPointerException`** immediately at creation:
```java
record Money(BigDecimal amount, String currency) {
    Money {
        Objects.requireNonNull(amount);
        if (amount.signum() < 0) throw new IllegalArgumentException("amount >= 0");
    }
}
```

2. **Checked vs. unchecked**: record constructors rarely declare checked exceptions (serializers + frameworks map them). Keep constructors free of checked throws if possible; if a component is expensive to build, build outside and pass the result in.

3. **Behavior exceptions**: methods on records can throw. For API errors, throw domain exceptions. Records are data — don't embed exceptions in components unless it's an error-carrier (that's arguably a non-record design).

4. **Handling missing components / Optional**: `Optional.orElseThrow(() -> new NotFoundException(id))` is natural around records.

5. **Error-carrying result types**: with records you can model errors as VALUES, not exceptions:
```java
sealed interface Result<T> permits Ok, Err {}
record Ok<T>(T value) implements Result<T> {}
record Err<T>(String message) implements Result<T> {}

Result<Integer> divide(int a, int b) {
    return b == 0 ? new Err<>("div by zero") : new Ok<>(a / b);
}
```
No exception thrown; caller switches exhaustively.

The "senior" nuance: records favor fail-fast (validate in constructor) + explicit error values over exceptions-in-flow, especially in reactive/streaming code. Keep transportation of failures explicit; use records as the sum type `Result`.

## Q63: How do you handle equals/hashCode/toString for records in JPA or Hibernate projections?

**A:** When records are used as read-only projections (also ranges in mapped queries), the generated equals/hashCode/toString are fine — value equality over immutable data. Hibernate 6 supports records as `select new` projections and tuple transforms:

```java
// JPQL
List<User> users = em.createQuery(
    "select new com.example.User(u.name, u.email) from UserEntity u", User.class)
    .getResultList();
```

Where Hibernate needs care:
1. **Entities should NOT be records** — managed entities need mutability, no-arg contructor, identity-based equals. Use records only for read models.
2. **Roundtrip identity**: since records are value-equal, two projections for the same DB row that map to equal records compare equal — which is what you want for DTOs. But the same record used as an ENTITY fails cascade/session semantics.
3. **toString/JSON**: document logging uses record toString — helpful.
4. **Comparison in Where clauses**: don't use record equals to drive SQL.

```java
record UserProjection(Long id, String name) {}

// recommendation
public interface UserProjectionData {
    Long getId();
    String getName();
}
// select u.id, u.name ... -> projection proxy (fine too)
```

Record projection best practice:
- Keep records as the API/transport layer; use entities / projections in the persistence layer.
- Use record in `select new`, and ensure constructor matches component types.
- hashCode on records = value-based — fine for in-memory maps, not for id-based session lookups.

The nuanced answer: records' equals/hashCode are a feature for DTO results, a liability for entities; use Bean Validation-based invariants and records at the boundary.

## Q64: What are `scoped values`? How do they relate to records?

**A:** `ScopedValue` (JEP 429/446, JDK 21/22, incubating/preview) is a form of safe thread-local context: a value bound for a scope, usable by code running in that scope (including virtual threads), immutable during it.

```java
static final ScopedValue<String> REQUEST_ID = ScopedValue.newInstance();

void call() {
    ScopedValue.where(REQUEST_ID, "req-123", () -> {
        String id = REQUEST_ID.get();   // visible in this scope
        doWork();
    });
}
```

Relationship to records:
- Records are often the VALUES being scoped: `ScopedValue<RequestContext>` where `RequestContext` is a record: `record RequestContext(String userId, String traceId, Instant receivedAt) {}`.
- Because records are immutable/value-based, they're safe to store in a ScopedValue (no mutable state to race).
- FP-style code running in a scope uses records as immutable context — no thread-locals mutation hazards.

```java
static final ScopedValue<AuthContext> AUTH = ScopedValue.newInstance();

record AuthContext(String userId, Set<String> roles, Instant issuedAt) {}

void handle(HttpExchange ex) {
    AuthContext ctx = new AuthContext(parseUser(ex), roles(ex), Instant.now());
    ScopedValue.where(AUTH, ctx, () -> controller.process(ex));
}
```

When to use instead of ThreadLocal: virtual threads → thousands of threads each with their own ThreadLocal is costly; ScopedValue shares context in structured scopes with zero-copy lookup. Records + ScopedValue form a clean, safe "request context" pattern used in structured concurrency (JEP 428).

Interview angle: "How would you pass request context safely in a virtual-thread-heavy service?" — Answer: immutable record as context + ScopedValue scopes.

## Q65: How do you implement a sealed hierarchy that also needs a `default`-ish behavior?

**A:** You add a default via an interface/abstract-class default method, alongside pattern matching:

```java
sealed interface Shape permits Circle, Box {
    default String describe() {   // default behavior for ALL variants
        return "a shape";
    }
}

record Circle(double r) implements Shape {
    @Override public String describe() { return "circle r=" + r; }
}

record Box(double w, double h) implements Shape {
    @Override public String describe() { return "box " + w + "x" + h; }
}
```

Alternatively, keep behavior OUT of records and implement the dispatcher in one place:

```java
String describe(Shape s) {
    return switch (s) {
        case Circle c -> "circle r=" + c.r();
        case Box b -> "box " + b.w() + "x" + b.h();
        // adding a new Shape variant → compiler forces the new case
    };
}
```

Which to prefer?
- If "default" is truly shared behavior (same code for all variants), put it as an interface `default` method — records inherit it; overrides refine.
- If each variant's behavior differs, use exhaustively switching — compiler-driven, no accidental default masking a missing case.

A hybrid: interface default provides a "fallback" for disciplines that shouldn't be implemented; switch overrides only where you need per-variant logic. But note: a default method that returns a generic answer for unhandled variants can hide bugs; prefer explicit override or exhaustive switch.

Senior note: when a sealed interface has a default method, prefer making the default SEMANTICALLY SAFE (a "no-op" that is correct for all permitted types). If a variant can't have a useful default, throw `UnsupportedOperationException` in the DEFAULT and require overrides — verbose but explicit.

## Q66: What is the difference between pattern matching in Java and in Kotlin or Scala?

**A:** Modern Java (21) pattern matching supports:

- Type patterns, `null` patterns, constant patterns, guarded (`when`) patterns.
- Record patterns (destructuring, incl. nested).
- Exhaustive switching over enums and sealed types.
- Pattern matching for `instanceof`.

Limitations vs. Kotlin/Scala:

Kotlin `when`:
- Structural destructuring via `data class` componentN, `type` + `is`, range patterns (`in 1..10`), custom conditions on any expression.
- No exhaustive enforcement for open classes unless you have `else`.
- `when` is an EXPRESSION, usable as statement too.
- Smart casting (variable narrowed by `is` check) is automatic — no explicit binding needed.

```kotlin
when (x) {
    is String -> x.length   // smart-cast to String
    in 1..10 -> "small"
    else -> "other"
}
```

Scala:
- `match` with case classes, pattern guards, extractors (arbitrary `unapply`), destructuring with nested patterns to arbitrary depth.
- Extractor objects allow user-defined patterns — Java patterns are structural (record+type only), no user extractors.
- Exhaustiveness with `sealed` families.

Java's place: structural patterns only (no extractors/ranges), no smart-casting, but official/exhaustive + integrating into switch statements. The story in a FAANG interview: "Java's pattern matching is deliberately structural and sealed-driven; Komlin's `is`/smart-cast is syntactic sugar differing direction; Scala's extractors give full user-defined patterns but sacrifice simplicity." Java chose a middle road — type + record patterns that the compiler checks exhaustively.

## Q67: How do you deal with arrays inside records?

**A:** Arrays as components are a hazard: equals/hashCode are identity-based for arrays, and arrays are mutable — breaking value semantics.

```java
record Buffer(byte[] data) {}
byte[] a = {1,2,3};
Buffer b1 = new Buffer(a), b2 = new Buffer(a.clone());
b1.equals(b2); // false — array identity
```

The fixes:

1. **Defensive copy on access and construction**:
```java
record Buffer(byte[] data) {
    Buffer { data = data.clone(); }            // on construction
    public byte[] data() { return data.clone(); } // on access (mostly for callers)
}
```

2. **Convert to list** for equality:
```java
record Ints(List<Integer> v) {
    Ints { v = List.copyOf(v); }
}
```

3. **Immutability at both ends**:
```java
record Record(byte[] payload) {
    Record {
        payload = payload.clone();
    }
    byte[] payloadUnsafeView() { return payload; }
    byte[] payloadCopy() { return payload.clone(); }
}
```

Choose per call-site: clone-on-write vs clone-in-accessor vs convert to immutable collection. In practice:
- For byte buffers used by IO, clone at construction + store; only expose copies to untrusted callers.
- For consistency, prefer `List<Integer>` (via `Arrays.asList(...)`) or `Map/Set.copyOf` over raw arrays when equality/serialization matters.

And note: `Arrays.hashCode`/`deepHashCode` semantics mean equals/hashCode for arrays-as-record-components are basically broken; never rely on them.

The interview-friendly answer: arrays are mutable and identity-based — treat them as unbehaving equality. Wrap or copy. Records don't protect their contents.

## Q68: How does `instanceof` pattern matching interact with `sealed` types?

**A:** `instanceof` pattern matching does NOT require sealed types — it works on any type. Sealed types add safety only in the exhaustive switch context:

```java
// open hierarchy — fine, but exhaustiveness not enforced
Object o = ...;
if (o instanceof Circle c) return area(c);
if (o instanceof Box b) return area(b);
throw new IllegalArgumentException("unknown " + o);   // required because open

// sealed hierarchy — exhaustive switch
return switch (shape) {
    case Circle c -> ...;
    case Box b -> ...;
    // exhaustiveness guaranteed — no runtime fall-through
};
```

Two interplay rules:
1. `instanceof` with a pattern on a sealed type: a variable of sealed type; the pattern matches subtypes checked at runtime; exhaustiveness still requires the switch/else.
2. `instanceof` on non-sealed types: the compiler still allows patterns, but you must handle the unknown manually (default/else).

```java
if (payment instanceof CardPayment c) {
    ccard(c);
} else if (payment instanceof WalPay w) {
    // ...
} // else: could be anything (non-sealed/open) — must handle default
```

The pattern-matching `instanceof` is the "espresso" (fine-grained, boolean) version; sealed+switch the "total function" version. Interview answer: instanceof patterns are open-ended and runtime; exhaustive finishing over sealed trees is compile-time; use instanceof early-exit for small checks, sealed switch for total dispatch.

## Q69: What happens if a sealed class is also abstract and has abstract methods?

**A:** Totally fine — sealed + abstract work together. The abstract methods define the contract each permitted subtype must implement.

```java
public abstract sealed class Animal permits Dog, Cat {
    public abstract String sound();

    public final String describe() {
        return this.getClass().getSimpleName() + ": " + sound();
    }
}

final class Dog extends Animal {
    public String sound() { return "Woof"; }
}
final class Cat extends Animal {
    public String sound() { return "Meow"; }
}
```

The compiler ensures every permitted subtype implements the abstract methods. If a permitted subtype is itself abstract/sealed, the branch passes the obligation down.

```java
public abstract sealed class Pet permits Dog, Fish {}
```

Why sealed+abstract matters:
- Closed inheritance + guaranteed method implementations → complete invariant enforcement.
- The abstract method set + permitted set give "contract completeness" the compiler verifies.

Interaction with pattern matching: switch over `Animal` still exhaustiveness-checked; `case Dog d -> d.sound()`, etc. The abstract methods don't change that.

The "gotcha": sealed abstract classes typically— no default method = you must implement in EVERY subtype; a `default` in an interface could provide a fallback. Choose abstract when a method MUST exist in all variants.

## Q70: How do you represent a tree or AST with records and sealed types?

**A:** A classic AST is a perfect fit — each node type is a record; the tree is nested records; evaluation is an exhaustive switch.

```java
sealed interface Expr permits Lit, Var, Add, Mul {}

record Lit(double value) implements Expr {}
record Var(String name) implements Expr {}
record Add(Expr left, Expr right) implements Expr {}
record Mul(Expr left, Expr right) implements Expr {}

double eval(Expr e, Function<String, Double> env) {
    return switch (e) {
        case Lit(double v) -> v;
        case Var(String n) -> env.apply(n);
        case Add(Expr l, Expr r) -> eval(l, env) + eval(r, env);
        case Mul(Expr l, Expr r) -> eval(l, env) * eval(r, env);
    };
}
```

Add pretty-printing as a separate function (new operation — no edits to the tree types):

```java
String serialize(Expr e) {
    return switch (e) {
        case Lit(double v) -> String.valueOf(v);
        case Var(String n) -> n;
        case Add(Expr l, Expr r) -> "(" + serialize(l) + " + " + serialize(r) + ")";
        case Mul(Expr l, Expr r) -> "(" + serialize(l) + " * " + serialize(r) + ")";
    };
}
```

Benefits over classic OOP AST:
- Adding a new node type: add record + update the sealed interface's permits + update EVERY switch (compile-forced).
- Adding an operation (serialize, simplify, check): write ONE new switch function — no visitor boilerplate, no touching data types.
- Garbage: immutable records avoid mutation during evaluation; safe in concurrent processing.

Watch-outs:
- Deep/recursive trees with records → recursion depth limits (consider Cap/continuation; Java recursion is stack-based — deep trees could overflow). Use a stack-based evaluator if needed.
- toString auto-generated can be noisy for huge trees — override for readable ASTs.

This is THE canonical FAANG interview example for records+sealed+patterns.

## Q71: What is the "visitor pattern" alternative when using records and sealed types?

**A:** The visitor pattern was invented (GoF) to add operations over a fixed class hierarchy without editing each class. Now that sealed+records+switch exist, the visitor pattern is largely redundant:

```java
// Old: visitor + accept
interface NodeVisitor {
    double visit(Lit lit);
    double visit(Var var);
    double visit(Add add);
}
interface Expr { <R> R accept(NodeVisitor v); }
class Lit implements Expr { public <R> R accept(NodeVisitor v) { return v.visit(this); } }
// ... every node needs accept() boilerplate
```

```java
// New: sealed + switch — ONE function instead of N accept methods
double eval(Expr e) {
    return switch (e) {
        case Lit(double v)  -> v;
        case Var(String n)  -> env.get(n);
        case Add(Expr l, Expr r) -> eval(l) + eval(r);
    };
}
```

Advantages of switch-based dispatch over visitor:
- Fewer files; no accept/visit boilerplate.
- Operations stay centralized — each new operation is one function.
- Exhaustiveness enforced: the compiler tells you when a new variant is missing.
- Record patterns give nested destructuring for free.

When the visitor pattern still wins:
- Open type hierarchies (non-sealed, external types) where switch can't be exhaustive.
- When operations must be extensible at runtime (plugins adding operations).
- Crossing module boundaries without sealed permits.

So modern answer: for a FIXED, closed set of types, use sealed+switch; keep the visitor pattern for genuinely open families. The interview often asks to compare — “Visitor is a workaround for missing ADTs; sealed+switch subsume it for closed sets.”

## Q72: How do records and sealed types interact with Spring, CDI, or similar DI frameworks?

**A:** Modern DI frameworks support records as beans and DTOs, with caveats:

Spring:
- Records as `@Component`/`@Service`? Not typical — but you CAN register immutable beans: records work with `@ConfigurationProperties` (constructor binding) and as DTOs.

```java
@ConfigurationProperties(prefix = "app")
public record AppConfig(String name, int port, List<String> hosts) {}
```
Spring Boot 3 maps config properties to the record's canonical constructor (no setters!). This is the recommended style for immutable config.

- Injection: `@Autowired` works with constructor-based injection for records (they have a canonical constructor). Spring supports records in `@Bean` factories.
- Jackson deserialization: records come through fine.
- Record components as repository interfaces? Spring Data projections can be records.

```java
public interface UserRepository extends JpaRepository<UserEntity, Long> {
    record UserSummary(Long id, String name) {}
    List<UserSummary> findAllSummaries();
}
```

Modern frameworks even prefer records:
- Micronaut supports records as beans and configuration.
- Quarkus handles records naturally.

Watch-outs:
- Framework scanners may treat a record as a bean requiring setters — choose a record-aware version.
- Records as @Entity are NOT supported — keep them to the "config/DTO" layer.
- Records don't support proxy-based `@Transactional` on their own, and no no-arg ctor.

Summary for interviews: modern DI (Spring 6/Micronaut) embraces records for config and DTOs via canonical constructor binding; records stay out of persistence entities and proxies. Patterns like `@ConfigurationProperties` gain immutability + validation.

## Q73: Explain how record components are used by Bean Validation in Jakarta/Jakarta validation.

**A:** Bean Validation (Jakarta Validation 3.0+) explicitly supports records:

- Annotate record COMPONENTS with constraints; validation is applied to the canonical constructor parameters.

```java
public record CreateUserReq(
    @NotBlank @Size(max = 50) @Email String email,
    @NotBlank @Size(min = 6, max = 128) String password,
    @Min(18) int age
) {}
```

How it works:
- The validator reads the record's canonical constructor and validates the method parameters (parameter-level constraints).
- On deserialization (Jackson) + `@Valid` on the argument, the constraints run before processing.

- Aggregating: `record CreateUserReq(@Valid Address address, ...)` — cascading into nested records works on components.

- Manual validation: `Validator validator = factory.getValidator(); Set<ConstraintViolation<CreateUserReq>> v = validator.validate(new CreateUserReq(...));` works because constraints are on constructor params.

Boundaries:
- Container elements: `List<@NotBlank String>` element constraints supported.
- Group validation: use `@ConvertGroup`, groups on components.
- Message templates resolved via components' annotations.

Why records + Bean Validation is favored now: validation at construction boundary (constructor params), immutability after validation, and framework support (Kotlin validation / Jakarta/ Hibernate 6) `@Valid` on components join cleanly.

The "senior" detail: because validation runs on the canonical constructor parameters, hostile inputs (e.g., from API/JSON) are rejected before any object exists — stronger than setter-validation on beans, which can leave partially validated state.

## Q74: How do records interact with Lombok?

**A:** Records and Lombok are mostly alternatives — Lombok's `@Data`/`@Value`/`@Builder` target regular classes; records already generate the same members natively.

What Lombok CAN add:
- Not needed for equals/hashCode/toString on records (already generated).
- `@Builder` on a record? Lombok historically has limited record support; `@Builder` on records (via the constructor) works in recent versions but is often unnecessary — records already have a canonical constructor + `with` methods.
- `@Accessors(fluent = true)` aligns record accessor naming (`name()`). Not needed with records.

Key guidance:

```java
// Lombok (mutable bean)
@Data
public class User { private String name; }

// Record (immutable, no Lombok)
public record User(String name) {}
```

Trade-offs:
- Lombok is an annotation processor — records are language features; prefer records for NEW immutable DTOs.
- Lombok supports mutable setters/config flags; records forbid mutation.
- Erasure: Lombok's generated equals/hashCode on a mutable bean can drift; records are rebuilt by javac each compile.
- Interop: putting Lombok ON a record is mostly redundant; some edge cases (custom `toString`, `@Builder`) might justify it, but plain record + small amount of hand-written body is cleaner.

Recommendation: don't use Lombok on records. Use records natively; if you need builder semantics with optional fields, add a static factory + `with` methods, or keep a builder for the few complex cases. Lombok phases out as modern Java features (records, sealed) reduce boilerplate need.

## Q75: What is the difference between a `sealed class`, `sealed interface`, and `package-private classes in same package`?

**A:** The three mechanisms achieve closed hierarchies with different visibility and tooling:

1. **Sealed class/interface**: compiler-checks permits; subtypes must be final/sealed/non-sealed; same module; exhaustive switch over allowed variants.

```java
public sealed interface Shape permits Circle, Box {}
```

2. **package-private classes in the same package**: effectively hides subtypes from the rest of the app, but the hierarchy is still OPEN within the package — anyone in the package can extend. Exhaustive dispatch isn't compile-checked (compiler sees all classes? For a switch the compiler still needs exhaustiveness; without sealed it cannot guarantee).

```java
// package geom
abstract class Shape {}
final class Circle extends Shape {}   // only visible in package geom
final class Box extends Shape {}
```

- Exhaustiveness: only within the package; outside, subtypes are invisible, and the compiler still requires a default because the set isn't declared.

3. **Combined**: sealed + package-private or nested is possible:
```java
sealed interface Payment {
    record Card(...) implements Payment {}   // nested → implicitly permitted
}
```

Trade-offs:
- Sealed: closed set + exhaustive checks + generated API documentation shows the exact variants.
- Package-private: no enforceable closure (any package member may add a subclass), no exhaustiveness in switches.
- Sealed interfaces can span multiple packages within a module (via permits); package-private can't be that formal.

Interview answer: sealed types bring the closure vào the TYPE SYSTEM and enable exhaustive compile-time matching; package-private is merely organizational — the visibility hides subtypes but doesn't give the compiler the closed set. Choose sealed when the variants are a domain invariant.


## Q76: How do you architect an event system using sealed records on a high-throughput backend?

**A:** On a high-throughput backend (thousands of events/sec), records + sealed types give us compile-time-exhaustive event handling with immutable payloads. Design:

```java
// Closed set of domain events
public sealed interface DomainEvent permits OrderCreated, OrderPaid, OrderShipped, OrderCancelled, StockReserved {}

public record OrderCreated(OrderId orderId, CustomerId customerId, Money total, Instant at) implements DomainEvent {}
public record OrderPaid(OrderId orderId, PaymentId paymentId, Money amount, Instant at) implements DomainEvent {}
public record OrderShipped(OrderId orderId, Carrier carrier, String trackingNumber, Instant at) implements DomainEvent {}
public record OrderCancelled(OrderId orderId, String reason, Instant at) implements DomainEvent {}
public record StockReserved(OrderId orderId, List<SkuQty> items, Instant at) implements DomainEvent {}

// Dispatcher — exhaustive, thread-safe
public void handle(DomainEvent e) {
    switch (e) {
        case OrderCreated oc -> { validate(oc); notifyCustomer(oc); }
        case OrderPaid op -> { confirmPayment(op); }
        case OrderShipped os -> { dispatch(os); }
        case OrderCancelled oc -> { refund(oc); }
        case StockReserved sr -> { reserveStock(sr); }
        // adding a new event → compiler forces a new case here
    };
}
```

Architecture points:

1. **Kafka/streaming**: serializing records with JSON Avro keeps schema compatible; adding/removing fields = record changes. Records as event payloads serialize safely (immutable, canonical ctor validation).
2. **Replay/idempotency**: `record OrderEvent(OrderId id, long seq, DomainEvent payload)`. Store seq and payload; replay is pure function of the log.
3. **Outbox**: a sealed event set inside the outbox; reads cone done via `switch` exhaustiveness.
4. **Validation on the boundary**: compact constructors reject malformed events before enqueue.

Where sealed helps the most:
- **Missing-event safety**: every consumer of the event stream gets compile-time guarantee they handle all event kinds — no silent NOP on new events.
- **Schema/evolution**: adding `OrderRefunded` = new record + new case in every handler, forced by compiler.

Senior considerations:
- Don't put logic currents in records; record = data, handler = behavior, dispatcher = switch.
- Keep event payloads small (primitive-ish components); embed authz/identity outside the event if possible.
- For very high throughput, consider `record` → primitive-specialized payload structures or compact JSON (Jackson records are fast) — avoid deep nesting.

This design eliminates the "unforeseen event type" class of bugs entirely — a strong architectural answer.

## Q77: What are the trade-offs between sealed types and standard polymorphism (open inheritance) in framework design?

**A:** The decision "sealed vs open" is central to framework design:

| Concern | Sealed types | Open polymorphism (abstract class/interface) |
|---|---|---|
| Extensibility | Restricted (same module; permits) | Any subclass anywhere |
| Exhaustiveness | Compile-time guaranteed | Not possible |
| Variant inventory | Set is closed, documented | Grows freely |
| Integration | Framework gates variants | Framework works with any impl |
| Forward coverage | New variant = edit permits + switches (breaking change for clients) | New subclass = no callback change |
| API stability | Adding a variant is breaking | Adding a variant is additive |

Framework examples:
- Sealed: Java `java.util.concurrent`? Not sealed historically. Apply to your own API contract: an error sys `sealed interface ApiError permits NotFound, BadRequest, ServerError`. A client MUST handle all — good for contracts.
- Open: plugin systems (SPI), provider interfaces (logging, drivers), where third parties add implementations without knowing the framework.

The trade-off in a sentence: sealed gives you TOTALITY (compile-safe coverage) at the cost of extensibility outside your module; open gives you extensibility at the cost of totality. A framework needs both: closed for the finite domain truth (error codes, statuses), open for the pluggable seams (handlers, strategies, adapters).

```java
// Framework core — closed
public sealed interface CommandResult permits Ok, Err, Pending {}

// Framework seam — open
public interface Handler {
    Result handle(Command cmd);
}

// Plugin areas — open interfaces; core state machines — sealed
```

Senior answer: draw the boundary deliberately. Model finite/quantized things as sealed (states, result unions, event types). Model infinite/pluggable things as open (providers, strategy implementations). Never make everything sealed, never make everything open.

## Q78: How do you ensure binary compatibility when evolving a sealed hierarchy?

**A:** Binary compatibility = old `.class` files keep working against new versions. For sealed hierarchies, be careful:

Safe additions:
- Add a NEW permitted subtype: old switches must have a `default` OR compile-time exhaustiveness breaks for NEW compilations, but OLD compiled code referencing the sealed type still runs (the new subtype is just an extra case that falls to default in old bytecode). So old binaries keep working, though old code misses the new case.
- BUT old compiled switches lacking a `default` over the sealed type: the new subtype doesn't break binary compat — it's still a subtype; the switch just doesn't handle it (runtime falls to default/fallthrough). The compiler changes only for NEW compilation.

Breaking changes:
- Removing/renaming a permitted subtype — old code referencing it fails (NoClassDefFoundError/VerifyError).
- Changing the sealed type's `permits` (e.g., removing a subtype) breaks exhaustiveness for old compiled switches that enumerated it — NEW compile errors, old bytecode still valid (they just can't instantiate things missing).
- Adding an abstract method to the sealed interface breaks all implementations (old classes missing it → AbstractMethodError).

Governance:
- Treat the sealed type's permits set as an API contract; version it explicitly (SemVer minor for adding subtypes accepted only for consumers who compile fresh + default fallback).
- Provide a `default`/open escape for unknown variants.
- Prefer record components stable: rename components breaks Jackson compatibility.

```java
// evolution-friendly: keep a default + add variants additively
String describe(Shape s) {
    return switch (s) {
        case Circle c -> "circle";
        case Ellipse e -> "ellipse";     // added variant
        default -> "unknown";
    };
}
```

Interview nuance: adding a subtype to a sealed family is a BINARY-COMPATIBLE change (old callers still link); it's a SOURCE-compat ripple because exhaustiveness forces consumers to recompile. Document that clearly for API users; if you can't afford consumer churn, keep a `default` or make the family open.

## Q79: What is the effect of records on the Java memory model and `final` fields?

**A:** Records' component fields are `private final`, so they inherit the Java Memory Model's final-field guarantee: once the constructor completes, any thread that reads the record reference — even without synchronization — sees fully-initialized component values (provided the reference is safely published, e.g., via a volatile, static, or a thread-safe collection).

```java
// Safe publication even without lock once constructor completes
public static volatile CacheEntry latest;  // record CacheEntry(String key, Object value)
```

When the reference is published unsafely (data race on the reference itself), the final-field guarantee still protects the final fields' VALUES once the reference is seen — but the visibility of the REFERENCE itself needs a HB edge. Records, being immutable, make this easy: final fields + no mutation.

Caveats:
- If components are themselves mutable (e.g., `List`), the LIST's contents are NOT protected — the reference to the list is final, but its elements' mutations race. Same guidance: normalize `List.copyOf`.
- Fields are final only for components; static fields can be mutable (beware).
- equals/hashCode are computed from final components — deterministic.

```java
record Point(double lon, double lat) {
    // components final
}
```

The JMM specifics: constructing a record publishes its final fields; readers through volatile/static reference get the correct values — this is the "immutability is the hard part is safe publication profit" insight. For high-scale concurrent services, records used as immutable snapshots avoid locks entirely.

## Q80: How do you make a record "defensively immutable" when it contains non-record mutable objects?

**A:** Defensive immutability = the record cannot be mutated internally, even through its components. Steps:

1. **Copy on construction** (avoid aliasing the caller's object):
```java
record Team(String name, List<String> members) {
    Team {
        members = List.copyOf(members);        // unmodifiable + rejects nulls
    }
}
```
2. **Copy on access** when callers might hold the reference:
```java
record Buffer(byte[] payload) {
    Buffer { payload = payload.clone(); }
    public byte[] payload() { return payload.clone(); }  // no mutable escape
}
```
The accessor returning a clone costs O(n); for read-heavy paths consider documented "read-only sibling" or a separate immutable wrapper.

3. **Component types matter**:
- Prefer `String`, primitives, `List.copyOf`, `Set.copyOf`, `Map.copyOf`, `Optional`, Java time types.
- Avoid raw arrays; if you must, clone.
- If the record contains a NON-record class that is mutable, hide it: store a deep copy or accept the reference and document contract.

4. **The "escape hatch" scenario** — Mutable objects in components: wrap them in `ImmutableList`/copies at the boundary so no state flows into or out of the record.

```java
record Cart(Map<Sku, Integer> items) {
    Cart {
        items = Map.copyOf(items);            // shallow: values Integer immutable
    }
    // Return copy to prevent mutation by callers
    public Map<Sku, Integer> items() { return Map.copyOf(items); }
}
```

So: defensive = copy-in + copy-out where needed; prefer immutable component types so copying is rarely needed. This "hard guarantee" is the record answer to immutability leakage.

## Q81: How do records affect serialization security (e.g., against gadget chains)?

**A:** Records change serialization mechanics in Java's native serialization:

- `Serializable` record serializes through the CANONICAL CONSTRUCTOR (no field reflection), so ANY invariant in the compact constructor re-runs on deserialization — hostile input goes through validation.
- No setters / no mutable fields; you cannot deserialize into a half-built state.
- But records are still `Serializable` if declared; default deserialization is safer but you should still:
  1. Filter streams (`ObjectInputFilter`) by package/class.
  2. Never deserialize untrusted autogenerated classes.
  3. For remote API data, prefer JSON (records) over native Java serialization.

```java
public record CardPayment(String cardNumber, String expiry) implements Serializable {
    public CardPayment {
        if (!cardNumber.matches("\\d{12,19}")) throw new IllegalArgumentException("bad PAN");
        // runs on deserialization too!
    }
}
```

Why sealed helps: closed of variants makes the deserialization universe enumerable — a whitelist check can be exactly the sealed permits:

Security checklist for records + serialization:
- Validate all components in compact constructors (fail-fast on hostile input).
- Use `SerialFilter`/`ObjectInputFilter` to only allow known record types.
- Prefer JSON/Protobuf + records for wire API over Java native serialization in new systems.
- Records don't implement any marker beyond `Serializable` if you declare it; don't declare it unless needed (the default is fine).

The interview point: records "fix" the deserialization-trust problem by moving validation into their constructor and removing the setter-based injection surface — a meaningful shift from serializable POJOs (which allow arbitrary field reflection).

## Q82: What is the role of pattern matching in reducing the "instanceof chain" anti-pattern?

**A:** The `if (obj instanceof A) else if (obj instanceof B)` chain is a code smell: casts repeated, risk of ClassCastException, maintenance burden. Pattern matching collapses these:

```java
// Before
String type = "unknown";
if (obj instanceof String s) { type = "str:" + s; }
else if (obj instanceof Integer i) { type = "int:" + i; }
else if (obj instanceof List<?> l) { type = "list(size=" + l.size() + ")"; }

// After — exhaustive switch expression
String type = switch (obj) {
    case String s -> "str:" + s;
    case Integer i -> "int:" + i;
    case List<?> l -> "list(size=" + l.size() + ")";
    default -> "unknown";
};
```

How pattern matching kills the smell:
- The cast disappears; the pattern variable is auto-bound and typed.
- Exhaustiveness: for sealed types, the compiler enforces coverage — no silent default.
- Null handling: `case null` explicit (no NPE in the chain).
- Guards handle range-wide conditions without nested ifs.
- Record patterns destructure, removing manual `.field()` access.

Compare with the modern "sealed + switch" — this is the complete replacement for both instanceof chains and visitor boilerplate. Downsides to acknowledge: switch expressions require Java 21; for huge type spaces, a dispatch map (`Map<Class, Function<Object,?>>`) can beat a write-out chain — but pattern matching's exhaustiveness remains a token win.

Advanced use: with pattern variables, smart-cast-like narrowing lets you use the bound value in nested operations — eliminating both the instanceof AND the cast AND the partial code of the else-if branch.

## Q83: How does Java's pattern matching compare to Kotlin's `when` and Scala's `match`?

**A:** Deep comparison:

| Feature | Java (21) | Kotlin `when` | Scala `match` |
|---|---|---|---|
| Type pattern | `case String s` | `is String` (smart cast) | `case s: String` |
| Destructuring | Record patterns | data class componentN | case class + extractor |
| Guards | `when` clause | `if` some expressions in branch | `if` guards |
| Exhaustive for sealed | Yes (compiler) | Yes (when as expression + sealed) | Yes |
| Constant/range patterns | Constants + enum; ranges? Limited (via guards) | Ranges (`1..10`), any expression | Extractors + guards |
| User-defined extractors | No (structural only) | No | Yes (`unapply`) |
| Null | `case null` | `null` condition | `null` pattern |
| Expression/statement | Both (switch expression/statement) | Both | Expression |
| Value in pattern | Yes | Yes | Yes |

Java's positioning: structural + sealed-driven, exhaustive, integrates into `switch` statements with arrow syntax — no user extractors, no smart-casting (which Kotlin has: after `if (x is String)`, `x` is `String`). Scala's extractors allow arbitrary destructuring; Kotlin's smart casts + range/when cover many idioms with ergonomic syntax.

Interview fragment: "Pattern matching in Java is type+record structurally exhaustive; Kotlin adds smart-casting and ranges; Scala adds user extractors — Java's value is compiler-enforced totality over sealed ADTs, which neither Kotlin nor Scala offer with the same safety surface (Kotlin requires `else`; Scala requires sealed knowledge + `case _`)."

When would you pick Java's switch over Scala's match? When you want exhaustiveness as a compile error and no external libraries; for visitor-free JSON handling / API response unions over sealed types.

## Q84: How do you implement a `Result` / `Either` type using records and sealed types?

**A:** Implement an ADT exactly like a sum type:

```java
public sealed interface Result<T> permits Ok<T>, Err<T> {}

public record Ok<T>(T value) implements Result<T> {}
public record Err<T>(String message) implements Result<T> {}

// helpers
public static <T> Result<T> ok(T v) { return new Ok<>(v); }
public static <T> Result<T> err(String msg) { return new Err<>(msg); }
```

Usage:

```java
Result<Order> place(OrderCmd cmd) {
    if (cmd.items().isEmpty()) return new Err<>("no items");
    // validate, build
    return new Ok<>(order);
}

Result<Order> r = place(cmd);
switch (r) {
    case Ok<Order> ok -> System.out.println("ok " + ok.value());
    case Err<Order> e -> log.error(e.message());
}
```

Extensions to consider:
- **map/flatMap** methods on the records (small amount of code, but they live in each record; better to add static helpers in a `Results` utility):
```java
static <T, U> Result<U> map(Result<T> r, Function<T, U> f) {
    return switch (r) {
        case Ok<T> ok -> new Ok<>(f.apply(ok.value()));
        case Err<T> e -> new Err<>(e.message());
    };
}
```
- Combine with `Optional` semantics when the extra error type is unnecessary.
- For high-volume flows, records keep the errors typed and switch-forced — no exception throws in the hot path.

Advantages over exceptions: exhaustiveness (compiler enforces every `switch`), immutability, value semantics for equality (testable), no stack-trace overhead (JIT-friendly). This is the FP-borrowed pattern now idiomatic in Java (used in many frameworks as `Either`).

Interview-friendly note: you just implemented Java's `Either` — the sealed/record pattern is exactly what libraries used to hand-roll with union interfaces.

## Q85: How do you model a configuration system with records and sealed types to enforce valid config at startup?

**A:** Config is an ideal record+sealed use case: validate at construction, immutable model, exhaustive handling.

```java
public sealed interface CacheConfig permits None, Ttl, Lru, Fifo {}

public record None() implements CacheConfig {}
public record Ttl(Duration expiry) implements CacheConfig {
    public Ttl {
        if (expiry.isNegative() || expiry.isZero()) throw new IllegalArgumentException("expiry > 0");
    }
}
public record Lru(int maxEntries) implements CacheConfig {
    public Lru {
        if (maxEntries <= 0) throw new IllegalArgumentException("maxEntries > 0");
    }
}
public record Fifo(int maxEntries) implements CacheConfig {
    public Fifo {
        if (maxEntries <= 0) throw new IllegalArgumentException("maxEntries > 0");
    }
}

public static CacheConfig parse(Map<String, String> props, String prefix) {
    String type = props.getOrDefault(prefix + ".type", "none");
    return switch (type) {
        case "none" -> new None();
        case "ttl"  -> new Ttl(Duration.ofSeconds(Long.parseLong(props.get(prefix + ".expirySeconds"))));
        case "lru"  -> new Lru(Integer.parseInt(props.get(prefix + ".maxEntries")));
        case "fifo" -> new Fifo(Integer.parseInt(props.get(prefix + ".maxEntries")));
        default -> throw new ConfigException("unknown cache type: " + type);
    };
}
```

Why records+sealed work here:
- Validation happens at construction — bad config fails fast at startup, not lazily at first use.
- Closed set: no third-party subclass smuggling an unsupported cache type.
- Pattern matching exhaustiveness lets `apply(...)` be total:
```java
Cache<String> build(CacheConfig cfg) {
    return switch (cfg) {
        case None() -> empty();
        case Ttl t -> ttlCache(t.expiry());
        case Lru l -> lru(l.maxEntries());
        case Fifo f -> fifo(f.maxEntries());
    };
}
```
- Serialization: config to JSON/YAML via records; constructor validation on deserialization gives the same guarantees.

Pair this with Spring `@ConfigurationProperties` (record binding) + Jackson for YAML — configuration is parsed and validated before beans start using it. This "fail-fast typed config" is a senior design signature on real services.

## Q86: What threading pitfalls exist when using records as caches or mutable state holders?

**A:** Records are immutable — but "immutable" as a cache key/state holder has threading nuances:

1. **Shared record instance**: immutable → safe to share without locks (final-field guarantees + no mutation).
2. **Record in a cache, construct-on-read**: use `ConcurrentHashMap` + `computeIfAbsent` — atomic `Function` (loader):
```java
ConcurrentHashMap<Key, Value> cache = new ConcurrentHashMap<>();
Value get(Key k) { return cache.computeIfAbsent(k, key -> load(key)); }
```
The loader runs once; other threads wait and get the SAME record.
3. **The record's COMPONENTS**: if a component is a mutable list, two threads mutating it corrupt state — normalize with `List.copyOf`.
4. **equals/hashCode stability**: immutability means stable hashes — safe keys.
5. **Copy-and-swap**: use records as immutable snapshots, swap a `volatile` reference:
```java
record Stats(long hits, long misses) {}
volatile Stats stats = new Stats(0, 0);
synchronized void record(boolean hit) {
    Stats s = stats;
    stats = hit ? new Stats(s.hits() + 1, s.misses()) : new Stats(s.hits(), s.misses() + 1);
}
// readers just read volatile — no locks
```
6. **Lazy builders**: never store a builder in a record — builders are mutable. Publish the completed record.

So: records shine — no low-level synchronization needed because they're immutable. Watch the CONTENTS and the publication (volatile/concurrent), not the record instance itself. Thread-per-check: use `volatile` for single-writer/many-reader record swap; `ConcurrentHashMap` for multi-key caches.

## Q87: How does `switch` on records differ from `switch` on enums?

**A:** Both are supported; differences matter to dispatch design:

- **Enums**: exhaustive pattern is `case CONSTANT -> ...`; the compiler knows all constants (enum class is a closed set). Expressive: grouping, nulls, `default`.
```java
switch (level) {
    case DEBUG, INFO -> ...;
    case ERROR, FATAL -> ...;
};
```

- **Records**: patterns are TYPED (`case Circle c`) and destructure (`case Circle(double r)`); exhaustiveness is verified against the sealed family. Each record variant can carry different data.

```java
String describe(Shape s) {
    return switch (s) {
        case Circle c -> "circle r=" + c.r();
        case Box b -> "box " + b.w() + "x" + b.h();
    };
}
```

Differences summary:
- Selector: enum constants (compile-time limited) vs. record instances (runtime-checked type + data).
- Binding: enum cases bind nothing; record patterns bind a variable or destructure components.
- Exhaustiveness: both compiler-checked (enum constants / sealed subtypes).
- Nulls: both support `case null` (in expression form).
- Constant labels can't be combined with records (you can't `case Circle, Box` — actually you CAN group when types are the same kind: `case Circle c, Box b -> ...`? No — you can group only when they bind no variables or all bind the same var with same type. In Java, labels group only if the pattern variables/types align: `case Circle c, Box c2` is not allowed in the same arm reliably — typically you group constants or patterns with identical variables types, which is limited. So note: mixed constant/records grouping is restricted.)

```java
// grouping constant cases
case MONDAY, TUESDAY -> ...;

// grouping record patterns — allowed if bound variables have same type/name:
case RedCircle c, BlueCircle c -> ...;  // both bind Shape-ish
```

Use enums for pure category dispatch, records+sealed for carrying data — and combine them: an enum discriminator field on the record, switch exhaustively.

## Q88: What is the effect of records on the `hashCode()` contract in sets and maps?

**A:** Record-generated `hashCode()` is derived from ALL components (like `Objects.hash`), and `equals()` compares all components — so the equal-implies-equal-hash contract always holds. Healthy for HashMap/HashSet.

Concerns:
1. **Component-based hash** with mutable components breaks the contract (hash changes over time) — normalize (List.copyOf) or avoid mutable components.
2. **Hash distribution**: If a component is, e.g., a long string or few, hashing may be fine; if you store thousands of records in a HashSet with few distinct components, hash distribution collapses → O(n) == O(n²) behavior? For performance you can override `hashCode()` (rare), but by default injectivity over components matters.
3. **Bucket contention**: `equals/hc` both component-based; two records differing in ONE component hash differently — the distribution is good.
4. **Using records as map keys with stable semantics**: since records are immutable, hashes never change post-construction — that's the standard requirement for keys.

```java
record Geo(double lat, double lon) {
    // override for better distribution if needed
    @Override public int hashCode() { return (int) (lat * 31 + lon); }
}
```

Caveat: records with array components → `Arrays.hashCode` gives IDENTITY hash for arrays; equals is identity — pairs `==` equality; hash-based collection mishaps. Convert arrays to lists or clone.

The correct statement: records satisfy the hash contract by construction for immutable components; for mutable component types you must normalize to keep the contract stable. Senior answer: use records "as-is" for keys because exact value semantics + immutability; don't override hash unless profiling demands.

## Q89: What are performance considerations when using records vs. classes in hot paths?

**A:** Records usually perform the SAME as identical hand-written classes (they're compiled to normal classes). The JIT treats them the same: accessor calls can be inlined, equals/hashCode straightforward, constructor cheap.

Where records cost more (in degenerate cases):
1. equals/hashCode compute over all components — a record with 20 components hashes costlier than a hand-rolled key on 2 fields. If that's hot, override or use a slimmer key record.
2. Immutability → you create new instances for changes (copy-on-write). In a very hot loop, `new Record(...)` per iteration adds allocation/build; hand-written mutable reuse was possible. Records pay the "immutability tax" only when update frequency >> creation.
3. toString for huge records might be expensive if called (logging at WARN vs DEBUG).

JVM advantages:
- Final fields, no synchronized logic → escapes analysis better; allocation may be stack-allocated (scalar replacement) — records can be MORE efficient than mutable beans in escape-analyzed code.
- Devirtualizable accessors → inlining.
- Value-based equality → deduplication-friendly in the future (Valhalla value types).

Overriding for hot paths:
```java
record Index(int a, int b, int c) {
    @Override public int hashCode() {
        // custom cheaper hash
        return a * 31 + b;  // fewer components than default
    }
}
```

But first measure profiles: record overhead is usually negligible; allocation dominance dominates. For extreme performance, move to explicit primitive-typed structures or specialized keys, not handwriting equals/hashCode.

Senior insight: don't hand-optimize records pre-profile. The JIT sees through immutability (safe publication, escape analysis). Prefer over large-behavior DTOs — the compiler handles them well.

## Q90: How do you evolve a sealed `Result<T>` API without breaking existing clients?

**A:** Since the sealed family is an API contract, evolve it carefully:

1. **Additive only**: adding a new permitted subtype is additive at the bytecode level (old clients still link) BUT any non-exhaustive switch in client code now has an untracked case — that's the breaking source-compat part. Mitigations:
   - Keep a `default` in your own switches.
   - Document that new variants may appear; clients using `default` degrade gracefully.
   - For total enforcement across the ecosystem, promote the new variant to a `non-sealed` escape only if it MUST be third-party extensible.

2. **Never rename/remove** permits or component fields once published (binary + source breaking).

3. **Versioning protocol**: keep a `schemaVersion` inside the payload; the new variant changes it; old clients route by an enum discriminator stored alongside:

```java
public sealed interface Result<T> permits Ok<T>, Err<T>, RateLimited<T> {}
```
Maybe instead of adding variant, use a `delayMs` field on `Err`? That's data-evolution — add `resumeIn` to `Err` ambiguously… Better: model sub-cases as data within existing variants to avoid new permits:

```java
public record Err<T>(String message, int code, Duration retryAfter) implements Result<T> {}
```
New error categories = new code + retryAfter, no new subtype.

4. **Compatibility tools**:
- Jackcess/Jackson records keep null-tolerant fields for forward/backward compat (add nullable components with defaults).
- Use `@Deprecated` variants when you must keep old names for binary but steer new code away.

The refined strategy: prefer data-evolution (add components, keep variants stable) over type-evolution (new permits) when most consumers are stateless and tolerate `default`. Reserve new variants for genuinely new legit states, and advertise the change with a SemVer minor + `default` forward-support.

## Q91: How do you write an exhaustive dispatch that handles the `non-sealed` escape branch?

**A:** When a sealed hierarchy includes a `non-sealed` subtree, exhaustiveness over the sealed type lets you cover: all sealed subtypes + the `non-sealed` root + a `default` for its open descendants.

```java
public sealed interface Command permits Start, Stop, ForeignCommand {}

record Start() implements Command {}
record Stop() implements Command {}
non-sealed interface ForeignCommand extends Command {}

String handle(Command c) {
    return switch (c) {
        case Start() -> "started";
        case Stop() -> "stopped";
        default -> "foreign: " + c.toString();   // ForeignCommand + any subtype
    };
}
```

Precision: the compiler treats the non-sealed branch as "unknown closure" — so you either:
- use a `default` (as above), or
- cover `case ForeignCommand -> ...` explicitly for exhaustiveness, then `default`/further nested switch inside for the open part.

```java
String handle(Command c) {
    return switch (c) {
        case Start() -> "started";
        case Stop() -> "stopped";
        case ForeignCommand f -> handleForeign(f);  // nested open dispatch
        default -> throw new IllegalStateException("unreachable? no — open");
    };
}
```

The honest answer: with a non-sealed escape, exhaustiveness is impossible for the full tree — your switch must have the open part handled by `default` or nested open logic. That's the price of the open branch. Best practice: keep non-sealed escape zones at the LEAVES and isolated; document that. If totality matters more than extensibility, don't use non-sealed.

## Q92: How do pattern `when` guards interact with null in Java's switch?

**A:** Guards and null interplay carefully:

```java
// Robus — explicit null first
String classify(Object o) {
    return switch (o) {
        case null -> "nil";                       // null matches first
        case String s when s.isEmpty() -> "empty string";
        case String s -> "string: " + s;
        case Integer i when i > 0 -> "positive int";
        case Integer i -> "int: " + i;
        default -> "other";
    };
}
```

Rules:
- A `case null` matches ONLY null; without it, a null selector tries the patterns — since `instanceof` returns false for null, type patterns don't match, and you fall to `default` (or NPE in expression if no default).
- Guard on a type pattern: `case String s when s.isEmpty()` — the guard evaluates using the bound `s`; a null never binds (instanceof false).
- Multiple patterns: keep `case null` BEFORE other matching patterns to guarantee null handling; ordering of guarded vs unguarded matters for reachability.
- Exhaustiveness: with only guarded patterns and no unguarded fallback, the compiler demands a final unguarded case or `default` — because guards may fail.

```java
// compile error unless an unconditional case exists
switch (o) {
    case Integer i when i > 0 -> ...;
    case Integer i -> ...;          // unguarded catch — required
}
```

- In a switch statement (non-expression), null still behaves: `case null` supported (Java 21 statements too); old statement form NPEs on null before matching.

So the pattern is: `case null` explicit, then guarded patterns, then the unguarded general case as safety net (or a `default`). This gives total, null-safe dispatch with readable hierarchy.

## Q93: How do records affect serialization performance compared to POJOs?

**A:** Records serialize efficiently because the format is fixed and the accessors are fast:

- Jackson serialization of records: reads component accessors (inlined by JIT), writes JSON. No getter/setter indirection.
- Deserialization: calls the canonical constructor (a single invocation), no reflective field writes.
- toString on large records (serialized by log frameworks) can be slower if deep; use `@JsonIgnore`-free simple records.

Where they differ from POJOs:
- POJOs often have O(1) reflection-based mapping; records have fixed introspection (RecordComponent[]) per class, cached by statics — similar cost.
- Records have no default ctor → frameworks that MUST use `newInstance()` pay no speed difference (they handle records via canonical).
- With Java native serialization, records serialize via canonical ctor (validation runs — slightly slower than blind field write, but safer).

Benchmark-ish notes:
- For typical DTO layers, record-vs-POJO differences are <2%. The real wins: immutability (no defensive copies) and validation at construction.
- Heavy hot paths: profile first; use specialized record mappers or stay on primitives.

So the answer: records are NOT slower than POJOs in practice — often faster due to inlining and canonical construction, and the immutability removes copy overhead. Focus on profile data, not folklore.

## Q94: What is the relationship between `switch` expressions and `yield`? When is `yield` needed?

**A:** `yield` returns a value from a switch expression arm that uses a BLOCK:

```java
int hours = switch (day) {
    case MONDAY -> 8;                      // expression — no yield
    case TUESDAY -> {
        int h = computeHours(day);          // block — need yield
        yield h;
    }
    default -> throw new IllegalStateException();
};
```

Rules:
- Arrow with a single expression: value implicit (`case X -> expr`).
- Arrow with a block `{ ... }`: the value comes from `yield expr;` (or throw).
- `yield` is only valid within a switch expression's block arm.
- The block can have multiple statements; the last effectful statement is `yield <expression>;`.
- Statements in classic switch don't yield — they use `break`/`return`.

Example with guards:
```java
String grade(int score) {
    return switch (score) {
        case int s when s >= 90 -> "A";
        case int s when s >= 80 -> { log("B-range", s); yield "B"; }
        default -> "fail";
    };
}
```

Why `yield` matters: switch expression blocks allow complex logic while still producing a value; `yield` makes it explicit that control exits the switch with that value. No fallthrough — each `yield` terminates the arm.

For interviews: distinguish `yield` (expression, returns value) from `break` (statement, exits). In switch expressions you never write `break`.

## Q95: How does a record's deconstruction affect generic inference (record patterns with type variables)?

**A:** Record patterns work with generics — you can destructure a generic record:

```java
record Pair<A, B>(A first, B second) {}

String describe(Object o) {
    return switch (o) {
        case Pair(String a, Integer b) -> "str-int: " + a + b;
        case Pair(String a, String b) -> "str-str";
        case Pair<?, ?> p -> "generic pair";
        default -> "other";
    };
}
```

Inference rules:
- Type variables in patterns — `case Pair<T, T> p` is not valid as a binding? Type variables in patterns: you use unbounded `?` or concrete nested patterns. Java's type patterns instantiate generics by erasure-based matching: `case Pair<String, Integer> p` matches if `p` is a `Pair` whose fields are bound as given. The pattern `case Pair<A, B>` with type variables isn't allowed in the syntax; you write `Pair<?, ?>` or full nested patterns.
- Guards can refine: `case Pair(String a, Integer b) when a.startsWith("x")`.
- The component types are erased at runtime — `case Pair(String, Integer)` performs a theoretical check: if actual components are not String/Integer, matching FAILS? Actually: the record pattern checks the component VALUE's type: `case Pair(String a, Integer b)` requires the pair's first to be a String and second an Integer. If the boxed component is `Object`, the pattern fails. Erasure: `Pair<String,Integer>` and `Pair<Object,Object>` are the same class; the pattern discriminates by nested type patterns.

Watch-out: the pattern `case Pair(String a, Integer b)` on a `Pair<Object,Object>` constructed as `new Pair<Object,Object>("x", 1)` matches (values are String and Integer) — because the check is against component VALUES, not the type argument (which is erased).

So inference serves the data, not the generic parameter — record patterns match structurally against the actual component values. That's why you see common idioms: `case Pair<T, T>` no, but `case Pair(String a, Integer b)`, `case Pair<?, ?>`.

## Q96: What are the limitations of pattern matching `switch` when using boxed primitives and wrappers?

**A:** Patterns on `Integer`, `Long`, `Double`, etc. work, with quirks:

1. **Constant patterns against boxed values unbox**: `case 42 ->` matches `Integer(42)` via unboxing (int constants auto-unbox comparison). Mixing `case Integer i` (type pattern) and `case 42` (constant) — ordering matters; `case 42` must come before `case Integer i`.

```java
String f(Object o) {
    return switch (o) {
        case Integer i when i == 42 -> "the answer";
        case Integer i -> "other int " + i;
        default -> "not int";
    };
}
```
Careful: `case 42 ->` uses `equals`-like constant semantics: `switch (Integer)` with a constant pattern compares by `==` on the boxed identity? Actually constant patterns on boxed: Java unboxes, comparison by value (with the caveat Integer caching irrelevant). `case null` may match first.

2. **`null`**: `case null` covers null; without it, boxed pattern won't match null.

3. **Primitive selector + boxed pattern**: `switch (int)` can't use `case Integer i` (needs a reference) — selectors are either int or Integer; patterns apply boxed/unboxed appropriately. Best practice: use primitives with constants, unbox via pattern for wrappers.

4. **Guard unboxing**: `when i > 0` auto-unboxes; `i` computed guarded — NPE if null already handled by `case null`/earlier arm.

Practical: 
```java
String find(Object o) {
    return switch (o) {
        case null -> "nil";
        case Integer i when i == 42 -> "meaning";
        case Integer i -> "num " + i;
        case Long l -> "long " + l;
        case Double d -> "double " + d;
        default -> "unknown";
    };
}
```

Senior guidance: pattern matching over wrappers is fine; avoid `==` on Integers (use pattern+guard), never rely on default cache; prefer primitives in selector and constants; keep `case null` + unguarded catch-all so exhaustive.

## Q97: How do you choose between `record`, `enum`, and a simple `String` constant for modeling discrete categories?

**A:** The selection rule:

- **`enum`** — fixed, finite set of named, distinct values, no variant-specific data worth carrying, or behavior uniform: status codes, directions, environments (DEV/QA/PRD).

```java
public enum Env { DEV, QA, PROD }
```

- **`sealed` records** — finite set of variants WITH different data shapes: result union, AST nodes, state machine states.

```java
public sealed interface Status permits Running, Failed, Done {}
record Running(Instant startedAt) implements Status {}
record Failed(String message, int code) implements Status {}
record Done() implements Status {}
```

- **`String` constant** — when the value is legacy/external-facing, may be arbitrary, and shouldn't be typecast as a closed set (e.g., a string from another system). Risks: typos, no exhaustiveness, no type safety. Avoid for internal domain logic.

Decision table:

| Need | Choice |
|---|---|
| Finite, no data per variant | `enum` |
| Finite, distinct data per variant | `sealed (records)` |
| Unknown/compatible external value | `String` (with validation at boundary) |
| Extensible by third parties | open interface (not sealed) + enum-ish registry |

Growth path:
- Start with `enum`, refactor to sealed+records when states start carrying data.
- Prefer enum for "category", sealed-record for "state machine"/"result" — the compiler checks transitions/states.

The senior answer: enums for the set of CATEGORIES (a fine number, no fields beyond a couple of constants), sealed+record for variants WITH payloads and behavior, and String only at integration boundaries with parsing/validation. Don't silently use String constants for domain modeling.

## Q98: How do you handle versioned APIs using records without breaking the sealed set?

**A:** API versioning with records is about component evolution + sealed permits stability:

1. **Keep the sealed set STABLE across versions** — changes (new variants) go in v2, not within v1:

```java
// v1 — sealed, untouched
public sealed interface ApiResult permits Ok, Err {}

// v2 — add RateLimited as a new variant; old code still links (binary compat)
// but old v1 switch without default doesn't handle it → require clients to add default or recompile
```

2. **Component versioning**: add fields as NEW components with nullable or default-normalized semantics:

```java
public record Ok<T>(T value) implements ApiResult {}
// v2 adds fields — new record type? Renaming breaks. Prefer a NEW record name or a v2 record:
public record OkV2<T>(T value, String requestId) implements ApiResult {}
```

3. **Version discrimination**: an explicit `int version` or `String apiVersion` component routes dispatch:

```java
switch (res) {
    case Ok(String reqId, ...) when res.version() >= 2 -> ...;
}
```
Simpler: keep `record Response<T>(int version, Result<T> payload)`.

4. **Deserialization**: `ObjectMapper` with records ties JSON to component names; new components break old payloads → use `@JsonProperty` aliases or `JsonNode` compatible fields.

The safe toolkit:
- Backward compat: adding components is binary-/source-neutral for most clients that recompile (they just ignore new fields); serialization needs tolerant mapper config.
- Forward compat: OLD client reading NEW payload → unknown properties in JSON — set `FAIL_ON_UNKNOWN_PROPERTIES=false` and records' constructor ignores extras? Records fail on unknown JSON properties by default; configure leniency.
- Sealed: don't remove supers; add new variants with new names; keep `default` switches.

So versioning = keep the sealed family stable, grow data additively (new components or new record names), keep default arms in switches, and configure serializers for forward-compat. It's a compatibility-by-discipline, compiler-assisted approach.

## Q99: What is the interplay of records/`sealed` with virtual threads and structured concurrency?

**A:** Records and sealed types complement virtual threads + structured concurrency (Project Loom):

1. **Immutable data across scopes**: on a server with thousands of virtual threads, the obvious design is: request-context `record` passed via `ScopedValue` (or captured in lambdas). Records' immutability makes cross-thread sharing safe without locks.

```java
record RequestContext(String userId, String traceId, Instant arrivedAt) {}

// Virtual-thread handler — immutable context shared via scope
ScopedValue.where(CTX, new RequestContext("u-1", "t-1", Instant.now()), () -> {
    var tasks = orderService.find(userId);      // runs on some virtual thread
    return tasks;
});
```

2. **Sealed result types for cooperative cancellation**: a task returns `sealed interface TaskOutcome permits Completed<T>, Cancelled, Failed` — completed data as record, so handlers exhaustively dispatch.

3. **StructuredTaskScope**: gather results from multiple subtasks; each subtask returns an immutable record; the joiner merges into a record summary (also immutable). Records' value equality lets you dedupe test/demonstrate easily.

4. **Failure atomics**: sealed `Result`/`Either` records travel across virtual-thread boundaries without exception-based control flow — avoiding stack races.

So: records give you the immutable value types that make vast concurrency the same problem as single-threaded code; sealed types give you the exhaustive dispatch over outcomes. Together with ScopedValue/StructuredTaskScope they form the modern high-concurrency architecture pattern.

Watch-outs: don't mutate records across task completion; new record per subtask result; keep contexts small/immutable; prefer ScopedValue over ThreadLocal for virtual-thread context.

## Q100: What is your design recommendation for a large FAANG-scale codebase: records+sealed as default, or inheritance everywhere?

**A:** My recommendation: records + sealed types as the DEFAULT for data modeling, with inheritance reserved for behavior-centric open extension.

Default rules:

1. **Data carriers (DTOs, projections, events, responses)**: records. Immutable, value-equal, framework-friendly, no boilerplate.

2. **Finite variant models (states, result unions, error categories, commands, events)**: sealed interface + records per variant. Compiler-enforced exhaustiveness, no fall-through bugs.

3. **Behavior stratanal (strategies, adapters, providers, plugins)**: open interfaces + composition (default inheritance). This is heavily polymorphic, extensible, plugin-friendly terrain — sealed would break ISVs.

4. **Persistence entities**: regular classes (immutable-ish, proxyable, mutable state); records only as read projections.

5. **Config**: records via constructors binding; validation in compact ctor; sealed for config unions.

Why this default works at scale:
- Missing-case bugs caught at compile time (the single biggest win for correctness on large teams).
- Every data shape governed by one canonical type, no drift of hand-written equals.
- Immutability removes cross-thread hazards at a concurrency-heavy scale.
- The hierarchy stays shallow: records+sealed instead of 10-deep class chains — less fragile-base-class churn.

Costs to acknowledge: sealed families are closed — adding $3rd-party$ subtype requires a rethink; records add no-arg constructors and aren't entity-viable. Keep enough escape hatches (non-sealed for plugin seams) and let the compiler guard the closed parts.

Bottom line for the FAANG interview: use records for data, sealed for finite variant sets, open interfaces for behavior seams. That's the modern-Java, exhaustion-safe architecture — and it's the closest pure Java gets to Scala/Kotlin ADTs while staying JVM-light.

