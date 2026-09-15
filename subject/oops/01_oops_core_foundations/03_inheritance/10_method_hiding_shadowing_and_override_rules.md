# Method Hiding, Shadowing and Override Rules — 100 Interview Q&A

## Q1: What is method overriding, and what must be true for a subclass method to be called an override?

**A:** Method overriding is when a subclass declares a method with the same name and parameter list as a superclass instance method, and at runtime the most-derived implementation is dispatched. The essential conditions: the name and parameter list must match exactly; the return type must be the same or a covariant subtype; the method must be overrideable (not final, not static, not private in the base); and the access of the subclass method must be at least as permissive as the base.

The runtime personality is what defines it: the call is resolved dynamically via the virtual table (vtable), so which body runs depends on the object's actual runtime type, not the static type of the reference. That is the single feature that makes overriding "real" inheritance behavior rather than mere redeclaration.

The distinction to remember in interviews: a method with a *different* parameter list is an **overload** (compile-time selection), while a method with the *same* signature replacing base behavior is an **override** (runtime dispatch). Overriding is the polymorphic tool; overloading is just name reuse.

## Q2: How do override, hiding, and shadowing differ from each other?

**A:** Overriding replaces an *inherited instance method*'s behavior at runtime: same signature, dynamic dispatch. Hiding applies to *static methods and fields*: a subclass declares a member with the same name, and the *compile-time* reference type decides which one you see — the base version is "hidden," not overridden, because there is no dynamic dispatch.

Shadowing is about *variables*: an inner scope (local variable, parameter, nested class, subclass field) declares a name that makes an outer-scope name invisible to (most) code in that scope. For example, a local variable named `x` shadows a field `x`; a subclass field `name` shadows an inherited field `name`.

The crisp summary: overriding changes *behavior* dynamically; hiding changes *which member* is statically bound (static methods and fields); shadowing changes *which variable/type* is meant inside a scope. Overriding is the only one that participates in polymorphism; hiding and shadowing are compile-time name-resolution effects, and with them you typically need explicit qualification (`super.name`, `Base.foo()`).

## Q3: Why must an overriding method keep the same parameter list, and what happens if it differs?

**A:** The parameter list is part of the method *identity*. Overriding is a *replacement* of the base method's implementation for that exact method; if the parameter list differs, the subclass method is a *different method* — an overload — even if the name matches. So `void paint(float x)` in base and `void paint(double x)` in subclass are two overloads that coexist, and the caller's static types decide which is picked — there is no polymorphic replacement.

Keeping the same parameter list keeps the method's *contract* intact: any caller holding a `Base` reference calls `paint(float)`; the subclass's `paint(float)` is what should run for `Base`-typed references, so it must exist with the identical erasure to participate in dispatch.

The interview-relevant danger: when a subclass "accidentally" changes a parameter type, it silently becomes an overload — and the base implementation still handles the virtual call. This is why `@Override` exists: it makes the compiler check that a real override (matching signature, same erasure) is present, and it fails loudly when the developer meant to override but wrote an overload instead.

## Q4: What is static method hiding, and why is it not overriding?

**A:** When a subclass declares a static method with the same signature as a static method in the superclass, it *hides* the base method rather than overriding it. The reason is that static methods are bound at compile time: they are called via the reference type, not the runtime type, so `Base.foo()` and `Sub.foo()` are two independent functions — there is no vtable entry and no polymorphic replacement.

Concretely, if you write `Base b = new Sub(); b.foo();`, the compiler binds to `Base.foo()` because `b` is statically typed `Base`; even though the object is a `Sub`, `Sub.foo()` is not used. If you write `Sub.foo()` directly, you get `Sub`'s version.

Interviews frequently probe this with a trick: **you cannot override a static method — you can only hide it**. Java's `@Override` annotation even forbids marking a static method as an override of a static base method; non-static subclasses trying to hide a static base (or vice versa) are separate methods and the compiler will warn or reject depending on context.

## Q5: Can a static method hide an instance method, or vice versa?

**A:** No. A static method in the subclass cannot override an instance method in the base, and an instance method cannot override a static base method. If you attempt it, the compiler treats them as unrelated (or in stricter JVM checks, errors). The design reason: instance dispatch uses the vtable, static dispatch uses the type — the two resolution strategies are incompatible, so smuggling one where the other belongs would break the semantics silently, so the languages forbid the confusion.

In Java this is a compile error ("cannot override instance method with static method" / "this static method cannot hide the instance method" — depending on direction and modifiers). In C++ you can technically write non-virtual methods with the same name in derived and not get an error (it is hiding), but C++ has no static-must-not-mix enforcement; the behavior is purely name hiding.

The best interview answer connects both: *the requirement that you cannot mix static and instance in the same signature is a language guarantee that a name always behaves consistently (dynamically dispatched or statically bound) wherever its static type puts it.*

## Q6: What is a covariant return type, and how does it affect overriding?

**A:** A covariant return type lets an override change the return type to a *subtype* of the base method's return type. The base declares `Animal make()`, the subclass overrides with `Dog make()`. The JVM calls this a covariant override; the bytecode actually generates a *bridge method* that returns the base type and calls the covariant one, so binary compatibility is preserved.

Covariance preserves substitutability: callers that expect `Animal` still get an `Animal` (a `Dog` is an `Animal`). That is precisely why the direction works — the subclass promise is *at least* the base's promise; narrowing the return type cannot break a caller.

The interview nuance: covariant returns apply to both classes and interfaces. Going the *other* direction (base `Dog` → subclass `Animal`) is a compile error, because a caller expecting a `Dog` might receive a non-Dog (an `Animal` instance) — that breaks LSP. This is the canonical example of variance: return positions are covariant (out / producer), parameter positions are contravariant (in / consumer).

## Q7: What does the `@Override` annotation guarantee that overriding does not?

**A:** `@Override` is a compiler-enforced *assertion* that the annotated method genuinely overrides (or implements) a method from a supertype. Overriding alone — without the annotation — also works, but it runs the risk of the developer accidentally creating an overload (different parameter list) or unknowingly hiding a static/private member, because the name coincidence compiles fine either way.

When `@Override` is present, the compiler checks that there is a matching method in a superclass or interface. If the base signature is removed or changed later, or the developer typo'd the parameters, the compile fails — producing an early, clear error instead of a silent semantic drift.

The defensive value is high: it converts a *silent* failure mode (new overload + hidden base behavior) into a *loud* one. Teams that enforce `@Override` and generate an error/warning when absent catch signature drift, base method renames, and accidental overloads during refactoring — usually within the same build.

## Q8: What are the access-modifier rules for overriding, and why is narrowing forbidden?

**A:** An override CANNOT reduce visibility: `public` in base forces `public` subclass; `protected` allows `protected` or `public`; package-private allows package-private or wider. The reason is LSP: a caller holding a `Base` reference must be able to invoke the method wherever it could invoke it on the base. If the subclass removed `public`, the call site `base.foo()` (which compiled against base being public) would break when the object was actually a subclass.

The rule is one-way: you may *widen* (the override can be more visible) freely, because a caller who could only reach the base-level visibility can always reach the wider one. But you can never *narrow*. This is the same "you can give more, never less" principle that governs return covariance and exception narrowing.

A nice follow-up: private methods are a special case. A private method is not inherited and cannot be overridden; a subclass method with the same signature is just an unrelated method. The compiler won't let you mark it `@Override`. Visibility notes matter especially in cross-package subclasses where package-private base methods fall out of the inheritance picture entirely.

## Q9: How do checked exceptions interact with overriding? What are the narrowing rules?

**A:** An override may only throw *fewer or more specific* checked exceptions than the base — never new or broader ones. If the base declares `throws IOException`, the subclass may declare no checked exceptions, or declare `throws FileNotFoundException` (a subtype) — but not `throws Exception`. This is again a caller-protection rule: callers wrote handling based on the base's declared exceptions; broader exceptions would escape their compiled handling.

Why the JVM/compiler enforces it: exception *declaration* is part of the method's typed contract for checked exceptions. Runtime dispatch could substitute the subclass at any call site that verified against the base; a broader exception set would violate the caller's expectations (a caller catches `IOException` but the override throws `SQLException` uncaught).

The subtle point interviews love: **this restriction applies to the declared checked exceptions; runtime exceptions and errors ignore the rule entirely** — `RuntimeException` subclasses can appear freely in overrides because they are unchecked. Also, if the base method declares *no* checked exceptions, the override may declare none either (it may still throw unchecked ones freely).

## Q10: What is the theoretical and practical reason overriding uses dynamic dispatch while parameter binding stays static?

**A:** Two resolutions happen at different times. *Which method is selected* is decided at compile time by the static types of the arguments and the reference (overload resolution, static binding). *Which implementation of the selected method runs* is decided at runtime by the object's actual type (dynamic dispatch, virtual binding). Overriding affects the *implementation*; overloading (and general method resolution) decides *which* signature.

The practical reason for the split: overload resolution needs concrete compile-time types to pick among signatures — the JVM can't cheaply "try" at runtime for that purpose. But polymorphic *implementation* choice is exactly what we want deferred: an `Animal a = getAnimal();` reference should execute `Dog.sound()` when the object happens to be a `Dog`, and only runtime knowledge can do that. So the language binds *names and signatures* early, and binds *bodies* late.

The consequence people forget: **instance type determines the implementation; static reference type determines the signature.** A classic question forces this: `void m(Base b)` and `void m(Sub s)` overloads, called with an actual `Sub` held in a `Base` reference — the compiler picks `m(Base)` because overloading is static, even though the object is a `Sub`.

## Q11: Can a final or private method be overridden? What does that mean for the class design?

**A:** A `final` method can never be overridden — any subclass attempt to redeclare the same signature is a compile error. This is a deliberate design statement: the base author guarantees that this exact implementation will be the one run, protecting invariants (e.g., a `final` template that calls hooks, an essential validation, or a security-sensitive check). Once final, the behavior is frozen for the whole subtree.

A `private` method is *not inherited at all*, so it also cannot be overridden — a subclass method with the same name/signature is simply an unrelated method. Because it lives only in the declaring class, no polymorphism ever reaches it; `private` is "final by invisibility."

The design payoff: marking methods `final` (or sealing classes) turns the base class into a stable platform: authors can rely on synchronized blocks wrapping known behavior, on validation integrity, on hash/equals layout, without the risk that a downstream subclass silently alters the contract. Over-use of `final` hurts extensibility; under-use invites fragile subclasses. The balance is the core tension in base-class design.

## Q12: What is the significance of `super.method()` in an override? When is it legal and when is it not?

**A:** `super.method()` explicitly invokes the *immediate superclass* implementation from inside the override — the classic pattern for extending rather than replacing behavior: an override does pre-work, calls `super.method()`, then does post-work (or delegates entirely). It is legal where the superclass method is accessible (public/protected and inherited) and from any method of the subclass; the call is resolved statically to the superclass definition (invokespecial at bytecode level), bypassing the subclass's own override.

The key restriction: `super` can only cite the *direct* superclass, and only the *current* class's inheritance context — you cannot chain `super.super.method()`. If you need the grandparent's implementation, you must restructure (extract a helper the middle class calls, or use composition), because Java forbids reaching above the immediate parent.

There is also a subtlety with `super` in interfaces: `InterfaceName.super.method()` lets you call a specific *default method* from an interface — the qualifier disambiguates which interface's default you mean when name clashes exist. That syntax, though, is interface-default resolution, distinct from class `super`.

## Q13: How do field hiding and variable shadowing relate to overriding? When do they silently break code?

**A:** Fields never "override" — a subclass field with the same name as an inherited field *hides* it. Reads and writes inside the subclass of that simple name resolve to the subclass field; reads through a base-typed reference will silently see the *base* field. The classic trap: getters/writers that seem to be "overridden" but instead access *different storage* — a subclass writes `this.x` (its own field) while the base's private `getX()` returns the base's field. Behavior diverges, and no compiler error exists.

Variable shadowing is the scoped sibling: a local variable or parameter with the same name shadows a field inside that method, making `this.` necessary. A nested class or lambda can also shadow outer names. Because these are *name-resolution* effects (compile-time) rather than *dispatch* effects (runtime), they are silent — which is exactly why they cause confusion.

The interview-grade mitigation: never hide a field without `this.` discipline; prefer private base fields (so subclass "same names" are clearly new, not hidden); avoid reusing superclass field names; and when a subclass genuinely needs its own storage, use different names or private fields, because accidental hiding doesn't produce a compile error the way a missing `@Override` would.

## Q14: What is early binding versus late binding, and which is used by overriding?

**A:** Early binding (static binding) resolves a method call at compile time — the compiler decides exactly which method will run based on the static types involved; used for static methods, private methods, super calls (invokespecial), and overload resolution. Late binding (dynamic binding) defers the decision to runtime — the JVM looks up the actual class of the receiver object and invokes the appropriate implementation, as used by instance method override (invokevirtual on the object).

The mechanism: for a virtual call, the compiler emits an `invokevirtual` on the *symbolic descriptor* (class + name + descriptor); at runtime the JVM resolves the actual receiver's class and walks the method resolution to the most-derived implementation that matches. That's the same reason that "compile-time signature selection" (Q10) coexists with "runtime body selection."

Interview depth: C++ compiles to per-class vtables and the call site does an indirect jump through the vtable slot; Java's HotSpot also builds vtables (the *itable* mechanism handles interfaces) and can even devirtualize hot calls. But conceptually both are late binding: the *what to run* depends on the runtime type of `this`, which is precisely what overriding means. Early binding is the contrast: `Base.foo()`, `super.foo()`, and static calls.

## Q15: How does overriding interact with `equals`, `hashCode`, and `toString` — and what contracts must an override respect?

**A:** These three Object methods are the "contract trio." `equals` overrides must respect reflexivity, symmetry, transitivity, consistency, and `null`-handling; overriding it **almost always requires overriding `hashCode`** so equal objects produce equal hashes (the old "objects equal but hashed into different buckets" bug). `toString` has no hard contract but is expected to be informative; overriding it is trivial and low-risk.

The tricky interview dimension is *hierarchical equality*. A naive override using `instanceof` breaks symmetry across a hierarchy: `Sub.equals(Base)` can be true while `Base.equals(Sub)` can be false, or vice versa. The robust approaches are either (a) equality only between same-class objects (`getClass()` check), sacrificing cross-subclass equality, or (b) the "canEqual"-style contract found in Scala case classes and Lombok, which coordinates equality across a hierarchy so that `Base.equals(Sub)` and `Sub.equals(Base)` both route the same way.

Because `hashCode` and `equals` are dispatched *virtually*, a subclass that adds a field MUST reimplement both (calling super's and folding in the new field). Failing to do so gives equal-looking objects with different hashes or unequal objects reported equal — one of the most common production bugs in collection-heavy code.

## Q16: How do list-based collections (ArrayList, HashSet, HashMap) interact with overriding equals/hashCode, and what override mistakes cause silent loss?

**A:** `HashMap`/`HashSet` store by `hashCode()` bucket and `equals()` probe; if either override is wrong, lookups silently fail — the classic "I put it in but can't find it" bug. The most damning scenario: overriding `hashCode` to be *mutable-dependent* (a field that changes after insertion) — the object sits in the wrong bucket, and `contains`/`get` miss even though `equals` would succeed if the bucket were inspected.

`ArrayList` uses only `equals` (linear scan, no hashing), so a broken `equals` shows up as "contains doesn't find it." HashMap additionally depends on `hashCode`. Also, overriding `equals` to ignore a significant field makes two distinct objects "equal," so a Set shrinks silently (both "equal" ones collapse into one) — data loss.

The interview-grade guidance: keep `equals`/`hashCode` consistent with each other, base them only on immutable-or-stable fields, and ideally *derive* them (records, Lombok, IDE-generated) rather than hand-rolling. And remember that *within a hierarchy*, overriding these at multiple levels forces subclasses to reimplement — the "same field set equality" decision is a design commitment at each level.

## Q17: Can you override `clone()` properly? What are the traps for a subclass?

**A:** `clone()` is a shallow-copy utility whose contract is famously flawed: it's protected on Object (so not inherited-publically outside the package), returns `Object` (requiring a cast), and uses a JVM mechanism to bypass constructors. A subclass that overrides `clone()` must: declare `@Override public Sub clone()`, cast/allocate properly, call `super.clone()` (the JVM copies fields by bit-wise duplication), and then *deep-copy any mutable internal state*.

The trap: `super.clone()` returns a `Sub`-typed object without running constructors — so fields initialized *only in constructors* are NOT initialized in the clone unless the override re-initializes them or the field initializers run (field initializers do run on constructor-less allocation? No — field initializers do NOT run on clone allocation). Actually the JVM's clone does a bitwise copy; constructor-dependent state must be fixed manually in the override.

Modern Java deprecates the whole pattern: `Cloneable` is broken-by-default, and the recommended alternative is a *copy factory* or copy constructor (`Sub(Sub other)`) that builds explicitly. In interviews, the winning answer says: avoid override-dependent `clone()`; provide an explicit copy method so subclasses control exactly what gets copied, and `final`-class it to keep the contract stable.

## Q18: How does overriding interact with `finalize` (and destruction generally)? Is overriding it ever appropriate?

**A:** `Java's finalize()` was a destructor analogue that ran (unreliably) before collection. Overriding it is almost always wrong: finalization timing is nondeterministic, the JVM may never call it, exceptions in finalizers are swallowed, and the classic leak — a finalizer that resurrects an object — breaks all guarantees. Modern Java (18+) deprecated and the runtimes removed it. The answer to "should you override finalize?" is effectively: don't; use `AutoCloseable`/try-with-resources for explicit teardown.

For languages where destruction is deterministic (C++), the "override of destroy" is the destructor itself: a derived destructor runs after (and must coordinate with) the base destructor, and virtual destructors matter enormously (see Q…). The analogy is instructive: C++ pays for the override lifestyle with the virtual-destructor rule — if a base class has *any* virtual functions, its destructor should be virtual, so `delete base_ptr` runs the derived destructor.

The cross-language principle for the interview: *teardown must not be dispatched implicitly into a hidden contract*. Where destruction is guaranteed (C++), you must design the override contract (virtual destructor); where it is not guaranteed (Java before 18), you must not override it at all but expose an explicit lifecycle method.

## Q19: What happens during override when the base method is `synchronized` or the subclass adds `synchronized`?

**A:** `synchronized` is *not part of the method signature* — a subclass override does not need to be synchronized to match, and the synchronization is a property of how the method *body* is invoked (the JVM acquires the monitor on entry automatically for a synchronized method). So an override silently *inherits or drops* the locking depending on what the subclass declares.

The danger is contract-drift: if the base marks `open()` synchronized (locking `this` for reentrant calls within its implementation), and the subclass override fails to declare synchronized, interior calls from within a *different* synchronized method no longer acquire — race conditions re-appear even though "the method looks the same." Reentrancy masks this: `this`-monitor locking is reentrant, so accidental loss only shows under contention.

The interview insight: **the lock is not inherited behavior, it's an implementation choice the subclass must consciously re-assert**. Synchronizing on the method (implicit `this`) also has a weakness — the lock is the mutable object — so serious designs use *private final lock objects*, but those cannot help a subclass that overrides and runs unlocked. If you need guaranteed mutual exclusion across a hierarchy, put the lock step inside a `final` method and expose token methods to hooks.

## Q20: What is the role of an abstract method in an override chain, and when does an abstract method "force" overrides?

**A:** An abstract method is a *declaration without a body* that must be implemented by the first concrete subclass. Its override in a concrete class completes the contract; every further override is normal virtual overriding. An abstract method is a *compile-time requirement* – the instantaneous concrete class must provide an implementation, dispatching through the vtable just like any override.

Removing the concrete-class requirement: if a subclass is also abstract, it can leave the method abstract again (propagating the requirement downward) or provide an intermediate default (making it fully overridable). So the chain of "you must override" continues until some class supplies a body, at which point the requirement converts into ordinary inheritance with optional subclass overrides.

The interview point: *abstract is about type obligation*, and *override is about dispatch*. A method may be abstract in the base, concrete in the middle, and overridden again below — each level deciding whether the obligation stays open. Modern interface defaults blur this further: a default method supplies a body *at the interface level*, but a class's explicit override *wins* over any default (class beats interface), and that hierarchy-free override rule is itself a favorite probing point.

## Q21: How do *errors* and unchecked exceptions behave in overrides versus checked restrictions?

**A:** For checked exceptions the override *must* not declare anything broader than the base. For *runtime* exceptions and `Error`s (both unchecked), there is no restriction at all: an override may throw any unchecked type regardless of what the base declares, because unchecked exceptions are not part of the declared compile-time contract callers must handle. This is why `NullPointerException`, `IllegalArgumentException`, and `IndexOutOfBounds` can appear in overrides freely.

The subtle interview trap: a *checked exception listed in the base but not effectively thrown* still restricts the override — restrictions are based on the *declared* throws, not actual behavior. Conversely, if the base declares no checked exceptions, the override may not declare *any* (unchecked ones excepted).

The deeper reminder: this asymmetry (strict for checked, free for unchecked) exists because checked exceptions are *declared contract*, whereas unchecked express *programming errors and environmental conditions* that are outside the typing system's promise. When a framework overrides and starts throwing a new `RuntimeException`, callers feel it — even without compile-time notice — which is why many teams use *custom runtime exceptions* deliberately as "unexpected failure" signals.

## Q22: What is a bridge (synthetic) method, and when does overriding generate one?

**A:** A bridge method is a compiler-generated method — marked `synthetic` — that reconciles *type erasure* between the source override and the bytecode signature. The two classic cases: (1) *covariant returns*: subclass returns `Dog`, base returns `Animal` — the compiler adds a synthetic `Animal make()` that casts the `Dog` result; (2) *generic overrides*: class implements `Comparable<T>` with a narrower `T`; the erased base method takes `Object`, so the compiler adds an `Object compareTo(Object)` that casts and calls the typed version.

Without the bridge, the JVM wouldn't see a matching signature for dispatch — the subclass method (typed) would not override the erased (Object-typed) base method, breaking polymorphism. Bridges *reinstall* the correct vtable slot with an adapter.

Interview value: seeing bridges in `javap -c` output proves you understand erasure and dispatch. The practical note: since bridges are synthetic, tooling and debuggers hide them; but *reflection* can surface them, and frameworks (Spring, Mockito) must sometimes filter `isSynthetic()` methods to avoid binding to adapters instead of real overrides.

## Q23: What happens at bytecode level for `invokevirtual` when a subclass overrides? Where does the dispatch land?

**A:** `invokevirtual` is the bytecode opcode for a normal polymorphic instance call. The constant pool entry names the method (owner + name + descriptor). At execution, the JVM resolves: looks at the *actual* class of the receiver, finds the method slot (vtable), and *the most-derived* implementation that matches — so `baseRef.method()` where the object is a `Sub` executes `Sub`'s body even though the call site text used `Base`.

Non-virtual instance calls use `invokespecial` for: constructors, `super.method()`, and `private` methods — these never look down the hierarchy. Static calls use `invokestatic` (no receiver). `invokeinterface` is the interface-dispatch cousin of `invokevirtual`.

Interview depth: the *resolution* step of invokevirtual at class-load/method-bound time finds the symbolic method; the *dispatch* step finds the concrete slot. Interфесяч — the distinction between "which slot" (vtable entry) and "which body" (most-derived override) is exactly why you can override without duplicating every call site, and why `super.method()` is legal at any depth (it is a direct call to the parent's body, not a vtable search).

## Q24: Why does a subclass that "typoes" a signature silently create an overload instead of an override? Give the real-world rebuild pain.

**A:** Because overload and override are *distinguished statically by signature*, and nothing at compile time *requires* a subclass method to be paired with a base method — a "matching name" alone isn't an identity match. So `void apply(String)` in base and `void apply(Object)` in subclass are two overloads. Calls `baseRef.apply("x")` still resolve to `apply(String)`. The subclass author believed they replaced behavior; they actually left the old body alive and added a hidden sibling.

The rebuild pain: the base behavior (often shared, patched) *stays live* for all base-typed call sites — including inside the base class's own methods (self-calls) and third-party code holding the base type. The subclass's new method only runs when *its own type + argument types* line up. This produces "the patch didn't take" bugs that survive refactors, because they compile cleanly for years.

This is the *strongest* argument for mandatory `@Override`: it converts typo-signature drift (an accidental overload) into an immediate compile error. Languages like Scala/Kotlin are stricter or annotate consciously, and C++ options (with gcc `-Woverloaded-virtual`) warn when a base virtual is *not* overridden but a same-name member exists.

## Q25: What does "the override must be at least as accessible" mean in practice for framework callers?

**A:** It means visibility *widening* is allowed, narrowing forbidden. A protected protected protected override may be protected, public, or package-private-public — but a `public` base method can only be overridden `public`. Framework callers hold base references; if the base declares `public`, any caller may invoke it — extending to widen is safe (public still callable), narrowing would make previously-callable sites fail at runtime when a subclass is present.

There is a packages nuance: package-private base methods are overridden only by *same-package* subclasses; a cross-package subclass cannot override them (they are not inherited), so a "same signature" method in a foreign-package subclass is just a separate method. This trips authors who write `void setUp()` protected-in-base-then-public-just-to-be-safe — actually the flip — widening is fine even cross-package.

The interview-grade detail: *interfaces' methods are implicitly public*, so a class implementing an interface MUST make those methods public — narrowing is impossible. This is a prime source of "why is everything I implement from the interface public?" — because the interface promise (and any caller holding the interface type) requires it; there is no legal narrower contract unless you use C#-style explicit interface implementation which Java lacks by default.

## Q26: How do you decide between an overload's static selection and an override's dynamic dispatch when a call goes through inheritance — the "same name, mixed types" maze?

**A:** The resolution algorithm: first, *overload resolution* picks the *signature* using the **static types** of the arguments — this happens entirely at compile time and considers the *reference type* of the receiver, not its runtime identity. Then *dynamic dispatch* picks the *implementation* among all overrides of that chosen signature, using the runtime class of the receiver.

The maze is the combination — `((Base) subtle).m(arg)` where `m` is overloaded in same class. The compiler chooses the overload *против static types only*. So passing a `Sub` argument to an overload `m(Base)` vs `m(Sub)` picks exactly one based on the *argument's static type*, and the receiver's runtime identity only selects *which override* of *that chosen signature*.

Interview trap: mixing both creates the classic "which method actually ran?" confusion. Example: class `Parent { void f(Base b); void f(Sub s); }` and `class Child extends Parent { @Override void f(Base b); }`. A `Child` called with `Base`-typed arg hits `Child.f(Base)`; with a real `Sub` argument but static `Base` type also `Child.f(Base)`. To reach `Parent.f(Sub)` you'd need argument statically `Sub`, and if `Child` didn't override it, it dispatches to `Parent.f(Sub)`. So both the argument's *static* type and the receiver's *runtime* type matter — the first for signature, the second for body.

## Q27: Why is overriding `toString()` risky when subclasses add fields, and how do you compose a hierarchy-aware `toString`?

**A:** `toString()`'s default is `Class@hash`. Most overrides simply interpolate fields. In a hierarchy, if the base's `toString` lists *only base fields*, a subclass adding fields needs its *own* `toString` that includes them — but must *not* duplicate base formatting (or worse, forget it). The common approach: each level implements `toString` calling `super.toString()` and appending its own fields in a stable format such as `BaseClass(field1=..., field2=...)`.

The fragility: consumers (logging, debugging, error messages) *parse or expect* stable shapes; subclasses changing the shape (adding/removing parts) silently alters logs across the tree. Also, an unsigned `toString` might expose *internal* state you changed for a subclass, leaking.

Interview-grade practice: keep `toString` implemented *once* at each level with a documented format; subclass toStrings *append* rather than replace; prefer a *builder-style helper* (a static format method) so each level only formats its own new fields; and if stability matters, make it `final` at the intended stabilization point. Never rely on default `toString` for meaningful logging in a deep hierarchy.

## Q28: How do *default methods* in interfaces interact with class methods during override resolution — the "class wins" rule and its holes?

**A:** The resolution rule: if a *class* (from superclass chain) declares a concrete method, it *wins* over any *interface default* with the same signature — the class method is selected regardless of which interface it came from. So implementing an interface whose default you dislike yields no override needed, *as long as* a superclass already declares the method. That rule keeps classes authoritative.

The holes: (1) if *two interfaces* both provide defaults with the same signature and the class declares none, the class MUST override (the diamond-default conflict) or compile fails; (2) the most *specific* default wins between parent/child interface defaults (a subinterface's default beats a parent's); (3) a *concrete superclass* method beats *all* defaults; (4) but a default method *calls* virtual methods — so even if the default body "wins," its behavior may still route into class overrides, meaning the class can sometimes *influence* a default without overriding it.

The interview answer beneath: default resolution is a *specificity priority* — most specific interface default, then class (concrete) declaration. Understand that "class wins" is true for a *declaration*, but the *execution* of any winning body (class or default) can still dispatch to other virtaual overrides inside it.

## Q29: Can an interface *restore* an abstract method over a default? What is "re-abstraction"?

**A:** Yes — a subinterface can redeclare a method that a parent interface had defaulted, making it **abstract** again (no body). This is *re-abstraction*: the subinterface revokes the convenience default, forcing every implementing class of the subinterface to supply a body. The default remains for those that implement only the parent interface.

Why it matters: it communicates "the default is *a placeholder/safety* behavior; implementations of the stricter subinterface must decide explicitly." A canonical example: a tree-like type where a parent gives a no-op `remove()`, and a child interface re-declares `remove()` abstract because removal is essential there.

Re-abstraction is a *contract-narrowing* tool, and it interacts with the "class wins" rule — if a class already declares `remove()`, the abstractness is satisfied; if not, implementing the strict subinterface without the method fails compiling. In interviews, re-abstraction demonstrates a sophisticated understanding of default methods as a *layered* mechanism rather than a flat "you get a body" guarantee.

## Q30: How do *anonymous classes* and *lambdas* relate to overriding? Can a lambda override methods?

**A:** An anonymous class is a literal one-shot subclass — it can override any virtual method its base offers (and add fields/methods). A lambda is *not* a subclass; it is a *function* that implements a *functional interface* — a single abstract method. A lambda therefore cannot "override" methods in some hierarchy — it only implements the one abstract method; anything else in the interface must be a default method (which lambdas cannot re-implement).

This matters for interviews because people wrongly think "lambdas complete the class' override." A lambda *satisfies* the SAM (single abstract method), so the interface's other (default) methods are inherited — you *cannot* attach a different `toString` or `equals` to a lambda (Java's lambda's `toString` returns a synthesized representation — you don't get to override it). Anonymous classes, by contrast, can override `toString`, overload helpers, etc.

The behavioral difference: each lambda expression creates a distinct function object (identity undefined), whereas two anonymous class instances are distinct objects with normal identity semantics. If you need `equals`/`hashCode`/`toString` overrides on the implementation, use an anonymous class or named class — a lambda gives none of those.

## Q31: What is the *functional interface* constraint for lambdas, and how does the single-abstract-method rule bind to overriding?

**A:** A functional interface has exactly one abstract method (SAM); lambda expressions provide that one implementation. The method can be inherited from *any* level — the interface may extend other interfaces as long as, counting all abstract methods, exactly one remains. Default methods don't count; static methods don't count; abstract methods inherited from `Object` (like `equals`) don't count toward the SAM.

How it binds to overriding: the JVM doesn't compile the lambda as a subclass override — it uses `invokedynamic` and a synthetic method (the "lambda body" method). So `Runnable r = () -> ...` runs a private static synthetic method rather than a class implementing `Runnable`. The "override" is de facto: the lambda provides the implementation that would otherwise be an override in a named class.

The interview nuance: since the SAM may be *in any ancestor interface*, you can define `interface Fast { int go(); }` and `interface Fancy extends Fast { default String desc(){...} }` — `Fancy` is still functional (one abstract). Re-abstraction can *break* sam-ness (a subinterface redeclaring another abstract method makes the count two), so lambdas and re-abstraction interact: re-abstraction is for *named classes*; for lambdas you need the single left-over abstract method.

## Q32: How does a *template method* pattern leverage overriding, and what distinguishes a *hook* from a *no-op default*?

**A:** The template-method pattern puts an *algorithm skeleton* in a superclass (usually `final`), delegating variation to overridable "steps." The skeleton is fixed — the subclasses override the steps. A **hook** is an overridable method *deliberately called* by the skeleton to let subclasses extend behavior with no obligation (often returns a default value / performs minimal action). A **no-op default** is a hook whose default body does nothing.

The distinction that matters: a *hook* exists to be *optionally overridden* — its presence communicates extension opportunity; a *no-op default* is specifically the neutral behavior. The design decision — should subclass be *required* (abstract step) or *optional* (hook)? — encodes the template's psychology. Required steps force complete algorithms; hooks afford incremental enhancement.

For the interview: prototype the template-method skeleton *final*, abstract for mandatory behavior, hooks that are *visible* and *documented*, and use the "protected visibility" rule — `protected abstract` steps expose only the override surface, not the class's internal API. Overriding *the whole template* (non-final skeleton) is an anti-pattern — the entire point of the pattern is that the skeleton *can't* be replaced; that's what makes it an "algorithm architecture."

## Q33: How does overriding interact with the *Builder* pattern (deep builders) and its fluent return types?

**A:** The builder's return types are *covariant overrides*: `DockerBuilder` extends `BaseBuilder`, and each `withX()` returns `DockerBuilder` (a subtype of the base's `BaseBuilder` return). That's what makes chaining *staying on the derived type* work — `new DockerBuilder().withA().withB().build()` keeps `DockerBuilder` all the way. Without covariant return types, the base `withA()` returning `BaseBuilder` would force a cast after every step.

The classic problem: if the base declares fluent methods but a subclass adds new `withY()`, the *base's* chained methods return the base type and the subclass's new method is *not reachable* after them unless each override *narrows the return type*. So builders typically *redeclare every builder method in the subclass* with a covariant return — boilerplate but essential.

The interview trap: a subclass that *forgets to override* a fluent method still inherits the base return type; a later `.withY()` therefore fails to compile because the chain's static type reverted to `Base`. The fix pattern: use *self-type generics* (CRTP): `class BaseBuilder<B extends BaseBuilder<B>> { B withA(); }` and `class DockerBuilder extends BaseBuilder<DockerBuilder>` — this *eliminates* the per-method redeclaration by making the base's methods return `B`, which resolves to `DockerBuilder` in the subclass.

## Q34: What is the "fragile base class" problem, and how do overrides amplify it?

**A:** The fragile base class problem: a superclass change (even a *private* implementation detail) can invisibly alter *all subclass behavior* — because subclasses override virtual methods and base code *calls* those overrides. E.g., the base's `start()` calls the overridable `onReady()`; a subclass's `onReady()` assumed `start()` order/states. A base refactor reorders calls, and every `onReady()` override behaves differently — silently (no compile error).

Overriding is the amplifier: each override is a *behavioral hook* the base's own implementation may implicitly invoke, so "the base's internals call the subclass's overrode" creates an invisible coupling. Adding a *new method call* to a base body can trigger unexpected behavior in existing subclasses (this is why adding a method can be *source-incompatible* in subtle ways).

Mitigation strategies for the interview: (1) *keep base logic in private/final helpers* and call only *documented* hooks; (2) document "this method is a hook; do not change its semantics" and "this method calls the hook X"; (3) minimize the surface — fewer virtual methods = smaller fragile surface; (4) use composition over inheritance where behavior variability is high; (5) freeze stable classes with `final`/sealed so change analysis is local. The deeper point: *override* is the exact mechanism the fragility lives through — so base-class design must treat every virtual method as a contract.

## Q35: What is the "is a copy of the whole method okay" smell — overriding a method only to *change one inner line* — and what pattern avoids it?

**A:** The smell: a subclass override that duplicates the entire base body except one line — a classic sign the base did *too much* in an *inflexible* method, and the subclass compensated by copy-pasting. The problems: duplicated logic across the hierarchy (fixing a bug in the base reparses unless fixed in every copy), drift (subclass copies age), and the fragile-base problem re-amplified.

The fix pattern: *extract hook*. Slice the base method into a *final* orchestration that calls overridable steps (or parameters) for the varying part: base `run()` becomes `final run() { setup(); step(); teardown(); }` where `step()` is `protected` and overridable. The subclass then overrides *only* `step()` — no bulk duplication, the skeleton stays single-sourced.

Interview reading: "copying the whole method to change a line" is a *design debt signal*: it tells you the varying behavior wasn't separated from the stable behavior. The template-method pattern IS the systematic fix — and the discipline "never copy a method body into an override; extract the variation" is the meta-rule. If the variation can't be extracted (open-ended), that's the signal for composition/strategy over inheritance.

## Q36: How are *bridge methods*, *covariant returns*, and *generic superclasses* connected when a subclass overrides a `Comparable`-style method?

**A:** Connecting the threads: `class MyList implements Comparable<MyList>` — the source method is `int compareTo(MyList)`. After erasure, the interface is `Comparable` (raw) with `compareTo(Object)`. The compiler emits the *real* `compareTo(MyList)` and a *synthetic bridge* `compareTo(Object)`, whose body casts its argument to `MyList` and delegates, satisfying the interface.

The bridge and covariance family: covariant returns generate a similar synthetic bridge (return supertype casting the covariant result). So *the bridge is the mechanical glue* that lets the source-level "conveniently typed" override match erased base shapes. JVM-level, both are just methods with adapters.

Interview-blade: if you *manually* write both `compareTo(Object)` and `compareTo(MyList)` in the class, you lose the "convenient typing" illusion — reflection shows two methods, and callers relying on `instanceof`/typing may hit the raw one. This is why frameworks (Hibernate, Jackson, Mockito) filter `synthetic` methods — the bridge is an artifact, not a genuine override to bind against.

## Q37: What is the difference between a class's private method and a *shadowing* duplicate in a subclass? How do calls from the base resolve?

**A:** A private method `Base.foo()` is *not inherited*. A subclass method also named `foo()` is unrelated. **Calls made *inside* the base class to `foo()` resolve statically to `Base.foo()`** — they do not dispatch to the subclass's `foo()`. This is the crucial semantic: private methods bind early (invokespecial), so base internal code is stable against subclass "same-name" methods.

The subclass's own calls to `foo()` resolve to its own method. If the subclass wants the base's version, it can't — the base's private method is invisible (unless reflection). Some languages differ — C++ private virtual methods *do* dispatch virtually (if base code calls a private virtual, the derived override can run, only implicit). But Java's private methods are statically bound, effectively final.

Interview-grade nuance: *calling a private method through `this`* inside the base is always the base's own body; a subclass cannot "trap" it. Renaming or shadowing a private base method is harmless but confusing to readers — the memory rule: *private = invisible & non-virtual; subclass same-name = a new, unrelated method*.

## Q38: How does overriding interact with the Singleton pattern and with constructor logic (since constructors can't be virtual)?

**A:** Constructors can't be virtual (they're never inherited and never dispatched); so "constructor" isn't an override — but the trap is *invoked from constructor*: if a constructor calls an *overridable* method, the *subclass's* override runs *before the subclass constructor body completes* — often on uninitialized subclass state (fields still null/zero). Classic bug: `Base()` calls `init()` which subclass overrides reading a field not yet set.

Singleton + inheritance: a singleton class should usually be `final` (or effectively) — otherwise an override can break laziness (a subclass override of `getInstance` re-allocating) or the "one instance" invariant. The *single-instance* contract is only guaranteed if the instance creation path is protected from overrides: make the factory/creation logic final/final-sealed.

The meta-principle: *the base-class constructor is a lock-in point* — behavior it triggers must be restricted to final/private methods or documented hooks known safe to call at construction. Teams that override `init()` in subclasses and then hit NPEs in constructors are re-learning this rule. The design fix: don't call virtuals in constructors; require a *post-construction* setup method or initialize subclass state *before* any hook runs.

## Q39: When overriding `equals`, why is a `getClass()` check safer than `instanceof` in a hierarchy — and what breaks with `instanceof`?

**A:** `instanceof`-based equals in a hierarchy breaks *symmetry*: if `Sub.equals(Base)` returns true (because sub instanceof base) while `Base.equals(Sub)` checks `getClass()` or other base-equality — asymmetry: `a.equals(b)` ≠ `b.equals(a)`. Also `hashCode` distribution breaks and containers misbehave under mixed types.

The two standard strategies: (1) **same-class equality**: override uses `getClass() != obj.getClass() → false`. This yields *antisymmetry-safe* equality — symmetric and transitive — but prevents a `Sub` from ever being equal to a different-typed class, effectively *barring cross-subclass equality*; each subclass must implement its own equals+hashCode. (2) **canEqual style** (Scala case classes / Lombok `@EqualsAndHashCode`): base declares `canEqual(Any): Boolean`; an equality check does `that.canEqual(this)` — permitting *coordinate* equality across the class family when canEqual aligns (e.g., two `Sub`s of a base both pass `canEqual`), while preventing base/derived cross-equalities that break symmetry.

Interview answer: prefer *same-class or canEqual*, never raw `instanceof` in multi-level hierarchies unless you *intend* cross-type equality and accept symmetry implications. And *always* mirror any field included in `equals` into `hashCode`; the pair is one contract.

## Q40: How does the *CallThrough to super* pattern (`result = super.method(); ...`) interact with multi-level overrides?

**A:** A subclass override that calls `super.method()` and then transforms the result is *the* canonical "extend behavior" style: `public String describe(){ return super.describe() + ", extra=" + extra; }`. At intermediate levels, each level calls its immediate parent — the chain composes. The power: single-source building blocks, each level contributing its delta.

The trap: `super.method()` *bypasses* the current class's own overrides and goes to the *immediate* parent. So a level's method that expects "the full chain" may get a *middle* result — for example, `Level3.describe()` calling `super.describe()` gets `Level2`'s result (which itself called Level1's). You cannot reach `Level1` directly. If the *middle* level's transformation is *incorrect or absent*, higher levels can't fix it through super.

Interview-grade mechanics: at bytecode, `super.method()` is `invokespecial` — a *direct* target resolution against the immediate superclass's method, not a vtable dispatch. That is why it sidesteps overrides *below* the current class. Also, calling `super` on a *default interface* method uses `InterfaceName.super.method()` — again a *specific* target, not the *class* override. Knowing where super jumps is a mark of maturity in override-heavy designs.

## Q41: What is *vtable slot reuse* in C++, and how does a `final override` change memory and dispatch?

**A:** In C++, each class's vtable has slots; when a derived class overrides a virtual, it *reuses* the base's slot (same vtable index); new virtuals get new slots. During construction/destruction the vtable pointer rebinds per stage, so calling a virtual inside a constructor invokes the *stage-appropriate* override — a C++ specialization of the "constructor-dispatch" rule (Q38).

A `final override` (C++11) does two things: marks a method as overriding AND as *final* — no further overrides; also, the compiler *knows* the exact target when calling through a *known-most-derived* type, enabling devirtualization (a full virtual-call eliminated into a direct call or inlined). In practice: `struct Sub final : Base { void f() final override {...} };` — since `Sub` is final, all its calls may omit vtable hops entirely.

Interview insight: `final overrode` is a *performance + correctness* tool — it documents "stop extending here," helps inlining, and protects invariants. C++'s dispatch happens through the vtable pointer at the object's *current stage* (constructor phase quirks included) — the reason virtual-base-dispatch during construction differs from Java's "always most-derived" behavior. Knowing *where* the vtable pointer points and *when* it re-rebinds separates C++ veterans from novices.

## Q42: In C#, what is the difference between `virtual`/`override`, `new` (member hiding), and `sealed override`? How do they map to Java notions?

**A:** C# is *opt-in virtual*: a method must be declared `virtual` to be overridable; subclasses then write `override`. If the base method is *not* virtual, a subclass's same-signature method *hides* it — you get a compiler warning; you silence it with `new` (member hiding). `sealed override` = override + prevent further overriding (≈ Java's `final` on the override itself).

Mapping: C#'s `virtual`≈Java's implicit virtual (all non-final/non-private instance methods); C# requires *explicit* `override` (Java's `@Override` optional but only a *check*, not *required*); C#'s `new` ≈ Java's *field hiding* and the (invalid-in-Java) "same-signature non-override" is allowed *only* for non-virtual bases in C#. Java has no `new`-based hiding for methods against a real virtual base.

The nuance to elevate in an interview: C# distinguishes *registration to override* vs *shadowing*. `override` enters the dispatch table; `new` creates a *parallel* method that shadows at the *static type* level. So `((Base)sub).H()` calls the base's `H` (hiding), whereas `sub.H()` calls the subclass's. Java behaves *as if every method were C-style virtual* — the non-virtual C# world is the *safer-by-default* model.

## Q43: What are *default interface methods* in Java's resolution when a class *extends* and *implements* — the "superclass wins" rule re-examined with an interface redeclaration?

**A:** Rules: (1) a *concrete superclass method* (public or not) always beats an interface default of the same signature; (2) if two interfaces clash with defaults *and* no class provides the method, the class must override; (3) a *subinterface's* default beats a *superinterface's* default (more specific wins); (4) if the class *redeclares* the method abstract (abstract class), the default is ignored — implementation must come from *some* concrete subclass.

The subtle re-examination: an interface *may* redeclare the default method as *abstract* (re-abstraction, Q29) — then the class *must* implement it even though a superclass could provide it? *No* — if a superclass *declares* the method (concrete), that concrete method *satisfies* the abstract requirement, and class-wins still overrides. The abstractness remains only where no class declaration covers the signature.

Interview-grade: Java resolves *multi-inheritance-of-type* as "choose the most specific *class* implementation; then the most specific *interface* default; then require explicit override." The *class always takes precedence even if the interface's abstractness* is "more specific," because class declarations *implement* interface contracts — they don't collide with them.

## Q44: Why do *static* methods in an interface belong to that interface only, and how does that interact with a class's static method hiding?

**A:** Interface static methods are *not inherited* — they're purely callable as `InterfaceName.method()` (Java 8+). A class cannot "override" an interface static method; it can declare a *same-signature static method* of its own, but that is a *separate* method — the call `InterfaceName.method()` still resolves to the interface's version. So unlike class static hiding (which *hides* the base's static method when called via the subclass name), interface statics are *completely distinct namespaces* accessible only via the interface.

In C++ or C#, interface static methods participate differently (C# static interface members resolve per-type), but for Java the rule is strict isolation. This avoids the "which static did I get?" confusion entirely — you *must* qualify.

The interview note: *methods* in interfaces that are `static` skip the whole override/dispatch machinery (no recursion, no vtable), so they cannot "fall into" a class's static-method-hiding scheme. If you want a *default* static-like behavior per implementation, you want instance defaults, not statics — statics deliberately escape polymorphism.

## Q45: What happens if a *record* (Java 16+) "overrides" a component accessor? Can records participate in override hierarchies?

**A:** Records *implicitly* declare accessors (`name()` returns the component). You *can* explicitly override an accessor (e.g., to validate or transform on read) — the record uses your override instead of the auto-generated one. But the *constructor* and *equals/hashCode/toString* still use the *canonical* components — overriding the accessor does *not* change the stored value or equality.

Records are final (no subclassing) — so records can't be BC — they *can* implement interfaces, including *sealed* interface hierarchies, and records fit polymorphic-switch dispatch beautifully. So a record *implements* many interfaces but *cannot be extended* — the override story for records is narrow: you override accessors, you override interface default methods, but you can't override *other records*.

The sharp answer: records are a *closed* family — final classes. Their override surface is *the interface contracts they implement* (defaults) and *accessor customization*. This makes them an *alternative* to open hierarchies: instead of subclassing to add behavior, you switch-dispatch on the record pattern (matching radar) — which is Java 21's preferred shape over fragile override chains.

## Q46: What does it mean for an override to "always be dispatachable even from the base constructor" in Java — and how does it differ from C++'s construction-phase dispatch?

**A:** In Java, if a base constructor calls a virtual method, the *most-derived* override runs immediately *even before that derived class's constructor body executes* — because the object's runtime type is already known (the vtable is the final one). Subclass fields are at default values, so overriding `init()` that reads them yields null/0 — the classic NPE source.

In C++, during base construction the *base stage* vtable is in effect — virtual calls inside base constructors resolve to *the base's* implementations (or its intermediates), *not* the derived override. This phase-wise dispatch is deliberate: called "construction stage" semantics. So C++ *protects* the constructor from surprise overrides, Java *does not*.

The deep interview takeaway: the two languages resolve the same hazard oppositely — C++ uses "stage-appropriate dispatch during construction"; Java uses "always-most-derived." The *safe pattern in both*: don't call overridable methods from constructors at all; if you must, initialize subclass state before the hook runs (Java: lazily on first use; C++: rely on stage dispatch, or document the ordering).

## Q47: How do *default methods* and *abstract method* requirements interplay when an *abstract class* implements an interface partially?

**A:** An abstract class implementing an interface may: implement *some* methods (concrete), leave *others* abstract (re-declaring them abstract), or rely on *interface defaults*. The concrete subclasses inherit the abstract class's implementations and must complete any remaining abstract methods. The default-provided interface methods *remain* available unless re-declared.

The mix matters because of *precedence*: a default interface method *loses* to an abstract-class concrete method of same signature (class wins), but *serves* as fallback where the abstract class doesn't provide one. So abstract classes are great "partial adapters": they flatten the interface's defaults into class-level concrete behaviors, which then *override* interface defaults for all descendants.

The subtle trap for interviews: if the abstract class *re-declares* an interface default as *abstract*, it *kills* the default for all subclasses — every concrete descendant must now implement it. That's the deliberate "re-abstraction through a class" pattern — used when the interface's default is considered unsafe for this class family.

## Q48: What is the *most-derived-wins* rule inside a method where `this.method()` versus `super.method()` are mixed — how do nested super chains behave?

**A:** Inside any method: `this.method()` (or an unqualified call) resolves *virtually* — the *most-derived* override *at the current object* runs, regardless of which class region you're in. `super.method()` resolves *statically* to the *immediate superclass's* implementation, *bypassing* the current class's own override. So nested chains: `A → B extends A → C extends B`. In `C`, `this.run()` → `C.run()`; `super.run()` → `B.run()`; `B`'s own `run()` (which may itself call `this.run()`) → *C.run()* again (virtual!) — the classic "super does not fully opt you out" recursion.

The practical consequence: `super.run()` doesn't "lock" to the immediate parent's *call tree* — only the *first* call is static; any virtual dispatch *inside* the parent's implementation (including its own `this.xxx()` calls) re-enters *your* overrides. So "extend via super and you're safe from recursion" is false for nested virtual usage.

Interview win: stating the rule — *super bypasses only the current class's override, not the whole hierarchy* — explains recursion bugs, `super.toString()` loops, and why template-method skeletons typically mark the skeleton itself final to guard against this dance.

## Q49: How do *functional-interface default chains* interact with method references — can a method reference bind to an override chain?

**A:** A method reference (`instance::method` or `Type::staticMethod`) *captures* an existing method — for instance methods, the receiver is bound, and the *target* is resolved *virtually* at invocation time. So `this::render` referencing a *virtual* `render` dispatches to *whatever override runs on this* — a method reference *is* a late-binding pointer, not a snapshot of a particular implementation.

If you *want* a *fixed* implementation (not the most-derived), you can't easily — method reference to a virtual method always dereferences via the receiver. You'd need `MyClass::render`? — that's *unbound* receiver-to-arg, still dispatch-capable on *the passed receiver*. Both remain virtual.

The interview nuance: a method reference to a *private/static* method is a *direct* (final) target; to a *public virtual* method it's dynamic. So overriding mid-flight (if the receiver's class changes behavior) changes the method reference's behavior *transparently* — but doesn't change the *reference's* identity. That mirrors the general rule: the reference selects *the method*, the receiver selects *which implementation*.

## Q50: When is *overriding morally wrong* even though legal — the "override to fight the framework" scenario, and the LSP-truth filter?

**A:** Overriding is legal but *dishonest* when it violates **LSP** — the override can't actually satisfy the base's *contract* but the code compiles. Classic cases: (1) the base promises "never returns null"; an override returns null; (2) base's `sort()` documented as stable (equal-key order preserved); an override ignores stability; (3) base's `addAll` documented to throw on duplicates; override silently drops dupes. The type system can't recreate semantics — only humans can.

The "fighting the framework" sin: overriding *framework hooks* to *undo* framework behavior (a controller override that throws to abort a pipeline, an override that returns a *fake* object to pass a framework check). Even if it "works," it breaks the contract future subclasses/upgraders assume — LSP breach. The correct approach is usually *composition* (wrap the component, implement only what you need) or framework-provided extension points.

The filter for interviews: apply the **"can a caller be surprised?" test.** If a caller holding the *base* type observes behavior that *contractually shouldn't exist* after your override, you've breached LSP even though your object "is a" subtype by name. The honest override either *narrows* (returns more spec, widens exceptions allowed) or *keeps* the promise — never expands the contract's falsehoods.

## Q51: What is C++ name hiding across inheritance, and how does a using-declaration change override resolution?

**A:** In C++, a derived class member of a given name hides ALL base members of that name, regardless of overload set. If `class D : B { void f(int); }`, the derived `f(int)` hides every `B::f` overload (`f(double)`, `f(char)`), not just `f(int)`. Calling `d.f(3.5)` tries `D::f(int)` (with a narrowing conversion 3.5 to 3), NOT `B::f(double)` — a classic surprise.

A `using B::f;` using-declaration imports all the hidden base overloads into the derived scope, so the full overload set becomes visible again and argument matching happens across the combined set.

The interaction with override: name hiding and override are different mechanisms. Virtual dispatch finds the most-derived method of the *same signature*; name hiding is a compile-time visibility filter. A virtual with a *matching signature* in the derived class overrides the base slot and also hides the name for unqualified lookup; a *different-signature* same-name member just hides without overriding. The `using` fix is the antidote to accidental hiding of a base virtual's other overloads.

## Q52: How do virtual inheritance and the most-derived class cooperate with overrides, and what does "final overrider" mean in a diamond?

**A:** In a virtual-inherited diamond (`class B : virtual A`, `class C : virtual A`, `class D : B, C`), the shared `A` subobject exists exactly once, so `A`'s methods have one slot. The final overrider is the most-derived implementation along the *dominant* path. If both B and C override `A::f()` to *different* bodies, neither dominates the other, and D must override `f()` itself or the program is ill-formed.

Dominance means a derived class's override wins over a base class's override of the same function along the same virtual base path. So `D::f()` overrides the shared `A` slot; a lone `B::f()` would dominate nothing over `C::f()` because B and C are peers.

The interview-grade point: with virtual inheritance, "which body runs" is determined by *final overrider + dominance*, not simply "most-derived wins." That is why the diamond fix sometimes costs an explicit override in D, and why minimizing virtual inheritance keeps override reasoning simple.

## Q53: What do the C++11 `override` and `final` specifiers actually prevent, and how do they differ from Java's `@Override`?

**A:** C++ `override` is a compile-time requirement: the function must genuinely override a base virtual; if the signature does not match any base virtual, compilation fails. That is stronger than Java's `@Override` (which only requires the method to override or implement a supertype member). C++ would otherwise allow a silently "new virtual" with a near-miss signature — the specifier converts that drift into an error.

`final` on a C++ virtual function prevents further overriding, like Java's `final` method. C++ also has class-level `final` (`struct D final : B`) meaning "nothing may derive from D," similar to a Java final class but with no sealed-style curated subtype list.

The spectrum worth stating: Java's `@Override` is an optional assertion checked by the compiler; C++ `override` is mandatory check-ins without which a typo silently hides; without it, the bug class "meant to override, didn't match" lives on. Prefer explicit specifiers in any hierarchy-heavy code.

## Q54: How are virtual calls implemented via vtables with multiple inheritance, and how do override thunks keep `this` correct?

**A:** Each polymorphic class has one vtable pointer (vptr) per "primary" base chain. A derived class's vtable extends the primary base's, reusing slot indices for overrides and appending new virtuals. With a single primary base, overrides simply fill the same index.

Multiple inheritance gives several vptrs — one per base subobject. When a derived object is viewed through a secondary base pointer, the pointer is *adjusted* to the secondary subobject's offset, and that subobject's vtable must fix up `this` before entering any override that expects the full most-derived object. This is done with *adjustor thunks*: `add pointer, jump to real override`.

The interview answer: MI dispatch = multi-vptr layout + pointer adjustment + adjustor thunks; virtual inheritance adds another indirection (offset table / vbptr). Overrides are the same "fill the slot" idea but *per vtable* — that's why the same override may exist as several entries with per-base thunks.

## Q55: Why is interface dispatch (invokeinterface + itables) different from class dispatch (vtables), and what does that mean for overriding interface methods?

**A:** Class virtuals use a vtable with consistent slot indices down a hierarchy, so lookup is a single indexed load. Interfaces can be implemented by unrelated classes in arbitrary orders, so there is no stable index; the JVM builds an *itable* per (class, interface) and `invokeinterface` resolves through it.

HotSpot caches the resolved method on the interface method slot, and repeated calls on the same receiver path hit a cached direct pointer. But the first resolution costs more than a vtable load, which is why interface-heavy hot loops can be slower until warmed.

For the interview: class dispatch = indexed vtable, interface dispatch = itable resolution/cache. Overriding an interface default appears in the itable as the class's real method, which is precisely the "class wins over default" rule at the dispatch level.

## Q56: When can the JIT or a C++ compiler devirtualize an override, and what role do final and sealed play?

**A:** Devirtualization requires proof that the receiver can only be one type: a final class, a known allocation site, a prior type check, or an observed monomorphic profile. With proof, the compiler replaces virtual dispatch with a direct call and can inline the override body. HotSpot also does *speculative* devirtualization: it assumes the observed type, guards with a type test, and falls back to virtual dispatch on rare mismatches.

Final methods and final/sealed classes give the compiler unconditional single targets — every virtual call through them is direct and inline-able. Sealed hierarchies further let the JIT enumerate the closed subtype set for switch/pattern-based optimizations.

The senior perspective: override-heavy code is fine at monomorphic call sites, but many-implementor paths can become megamorphic, defeating caches. Architects who know when `final`/sealed unlock inlining can keep hot paths fast without abandoning polymorphism.

## Q57: What does a method handle add over a normal override, and how does invokedynamic cache dispatch decisions?

**A:** A method handle (`MethodHandles.lookup().findVirtual(...)`) wraps a method as a callable value; a *virtual* handle dispatches to the receiver's most-derived override at invocation time, so it behaves like a late-bound function pointer. `bindTo(receiver)` pins one receiver, turning it into a non-polymorphic direct target.

`invokedynamic` lets compilers emit calls whose target is produced by a bootstrap method and then *cached* in a CallSite. Lambda bodies, string concatenation, and pattern-matching switches are wired through indy so the JVM resolves the concrete method once and re-uses it.

The useful interview frame: indy doesn't replace override dispatch for ordinary calls — it adds a *cacheable indirection* layer. A method handle can either stay polymorphic (receiving whatever receiver you pass) or be frozen (bound), giving you both the flexibility of overriding and the performance of a cached direct call.

## Q58: What happens to binary and source compatibility when a library converts a default method into an abstract one?

**A:** Moving default→abstract is *binary-compatible*: existing compiled implementers are untouched when the class file changes — the JVM does not retrofit defaults into implementers. But it is *source-incompatible*: when implementers recompile, those that relied on the default and provide no body now fail to compile.

Behaviorally, a stale client that never re-compiled still runs its old class file — but the first call to the now-abstract method raises `AbstractMethodError` at runtime. So the change is a version-ticking bomb: compile-clean for old binaries, crashing when exercised.

The rule library authors live by: adding a *default* method is backward-compatible; adding an *abstract* method breaks implementers; converting default→abstract is a deliberate major-version break. Re-abstraction is the mechanism to "silently remove" a convenience default from new implementers while old binaries limp until touched.

## Q59: What does it mean that overrides are "slots in a contract" for dynamic proxies and bytecode generators (JDK proxy, CGLIB, ASM)?

**A:** Dynamic proxies and bytecode generators create runtime subclasses that override every target method and delegate to an invocation handler. The override chain becomes generative: the framework's subclass replaces dispatch with a handler call, which is why exact signature matching, bridge/synthetic methods, and final members all matter — `final` and `private` methods cannot be proxied because their slots are sealed.

Consequently, Spring-style frameworks need interfaces (JDK proxies) or non-final classes (CGLIB); a final method, final class, or static helper is simply out of reach. Also, internal self-calls (`this.foo()`) from the proxied class are *not* intercepted, since they dispatch within the class body.

For the interview: proxies are runtime overrides and obey every rule already discussed (class-vs-default, final sealing, bridge handling). Any claim like "we can intercept anything" is false exactly where override itself cannot go.

## Q60: Why does adding a field to a subclass break inherited equals/hashCode, and what are the canEqual, same-class, and record resolutions?

**A:** If base `equals`/`hashCode` cover base fields only, two `Sub` instances differing only in the new field compare equal and hash identically — a contract violation. Redeclaring both in `Sub` (super + fold in the field) fixes that but breaks *symmetry*: `base.equals(sub)` ignores the extra field while `sub.equals(base)` includes it.

Resolutions: (1) strict same-class equality (`getClass()` comparison) — symmetric and transitive, at the cost of forbidding cross-subclass equality; (2) the *canEqual* pattern (Scala case classes, Lombok) — the equality protocol checks `that.canEqual(this)`, keeping equality coherent per family; (3) records — final classes with component-derived equals/hashCode over the entire component set, eliminating hierarchy drift by disallowing subclassing.

The takeaway: *whoever owns the fields owns equality*. Either each level re-declares consistently (same-class), or the family coordinates its equality protocol (canEqual), or you refuse hierarchy (records). Choosing the ownership model up front prevents the classic equals-breaks-on-subclass bug.

## Q61: How do unmanaged resources interact with override, and why does skipping `super.close()` leak base resources?

**A:** Resource-release methods (`close()`, `shutdown()`, `dispose()`) in a hierarchy are virtual and composed: the base frees base-owned resources, the subclass frees its own — typically `public void close() { this.owned.close(); super.close(); }`. A subclass that forgets `super.close()` leaks base-level handles (connections, files) with no error; calling `super` first while the subclass still writes can corrupt closing order.

The robust pattern is a final orchestrator with protected hooks: `public final void close() { subclassHook(); baseResourceCleanup(); }` where `subclassHook()` is the overridable part. That forces the ordering and prevents a subclass from silently spinning off the cleanup chain.

For the interview: teardown is where overriding is most brittle — close is not reentrant-safe, ordering matters, and swallowed exceptions make leaks invisible. The professional habit: component-owned resources, closed by the component, coordinated by a final template — never leave "did I call super?" to memory.

## Q62: How do inline caches adapt as override dispatch moves from monomorphic to polymorphic to megamorphic?

**A:** HotSpot call sites remember observed receiver types. A monomorphic site stores one receiver class and dispatches directly to its override; a second receiver type expands it into a polymorphic inline cache (a small set of cached targets); many types push it to megamorphic, where general vtable/itable resolution applies with no method-local cache.

Because each distinct subclass carries its own override, calling a base-typed method from N subclass types morphs the site accordingly. Few final overrides keep the site monomorphic and inline-able; many overrides converged on one call site make it megamorphic.

The interview insight: final/sealed members are JIT-friendly, letting the compiler treat a call as a single known target. Interface-heavy hot paths with ten implementers are inherently megamorphic-ish — architects trade dispatch speed for open extension, and knowing when that trade bites separates senior engineers.

## Q63: Where does "same signature" lie after erasure when overriding generic methods in Java, C++, and Kotlin?

**A:** Java erases generics, so a subtype override with a typed parameter list must still match the *erased* base signature; the compiler emits a bridge method that adapts the erased `Object`-typed entry to the typed override. C++ reifies templates: `vector<int>` and `vector<double>` are distinct types, templates are per-instantiation, and a virtual member cannot be a template because there is no finite set of vtable slots for an unbounded family.

Kotlin follows Java's erasure for overriding; `inline`/`reified` transforms parameters at the call site, not in method identity, so they do not produce new override signatures. 

The cleanest framing: generics/templates are a compile-time *family* mechanism; virtual/override is a runtime *slot* mechanism. Overriding therefore requires reifiable, bounded signatures, Java bridges the erased gap, and C++ forbids virtual templates outright for layout reasons.

## Q64: How do sealed types plus pattern-matching switches shift the override-versus-dispatch design, and when is a switch preferable to scattered overrides?

**A:** With a sealed hierarchy, `switch (shape) { case Circle(double r) -> ...; case Rect(double w, double h) -> ...; }` replaces per-type overrides of a method like `area()` with one central function. The compiler verifies exhaustiveness, and the JVM dispatches on the runtime type — like virtual dispatch, but with the behavior colocated at the use site.

The visible difference: overrides distribute behavior (encapsulated but scattered); pattern switches centralize it (visible but in one place). Adding a *new operation* favors overrides (add one method to every type); adding a *new type* favors patterns (add one case).

The architect-level synthesis: for closed value shapes (ASTs, messages, money ops), switch-over-sealed is often cleaner than a tree of overrides, and the exhaustiveness check acts like a compile-time checklist for every subtype that must handle the operation.

## Q65: Can an interface default be protected, and how do private interface methods (Java 9+) interact with override visibility?

**A:** Interface default methods are implicitly public — Java interfaces have public members only, so there is no "protected interface default." A class implementing an interface must make the matching method public; narrowing is impossible. Private interface methods (Java 9+) are helpers: they are not inherited and not overridable, and they exist to share code among defaults without expanding the public API.

The "class beats default" rule combines cleanly with this: a public class method with the interface signature always wins over any default, because the class declares a concrete (and public) implementation. Widening protected-in-class to public-in-subclass is legal; narrowing public to protected is not.

Interview note: private interface methods changed boilerplate, not dispatch. Visibility in a hierarchy only ever widens, and private stays sealed-away at every level — same rule for interfaces and classes alike.

## Q66: How does Python's C3 MRO decide which override wins with two mixins, and how does `super()` follow the linearization?

**A:** Python computes a linear ancestor order (C3). Method lookup walks the MRO left-to-right, so the first class in the list that defines the method wins — meaning *leftmost base family wins* in conflicting overrides. `super()` continues *after* the current class in the same linearization, so inside `A.m()` a `super().m()` may reach B's implementation even though A and B are not parent/child.

This is cooperative multiple inheritance: each class hand-offs to the next in the MRO, enabling mixins to compose regardless of nominal hierarchy. If bases request a contradictory order, Python raises `TypeError: Cannot create a consistent MRO` — that is the modern diamond-resolution conflict.

Because `__init__` is an ordinary method, constructor overriding follows MRO too, requiring disciplined cooperative `super().__init__()` chains. The takeaway: Python's override winners are decided by linearization position, not by a vtable.

## Q67: How does Ruby's method lookup differ with `include`, `prepend`, and `super`, and which direction wins?

**A:** Ruby's lookup: the class's own methods first, then prepended modules (reverse prepend order), then included modules (reverse include order), then superclasses with their own modules. `prepend` inserts the module *before* the class, so a prepended method overrides even the class's own method (the module wraps it and delegates via `super`). `include` keeps the class's own method ahead of the module's.

`super` walks to the *next* entry in that same lookup chain — so a module's method calling `super` reaches the next module or the superclass method, not "the parent" in a simple inheritance sense. Prepend is therefore the idiomatic way to wrap an unmodified class method.

The trap-topic: later-included modules shadow earlier-included modules for the same name; `prepend` flips the priority so the module runs first. Knowing which direction wins — include: class-first, prepend: module-first — is the classic Ruby nuance.

## Q68: How do Scala traits linearize overrides differently from Java defaults, and what does "most specific wins" mean for trait super chains?

**A:** Scala traits carry implementations, and when a class mixes traits the compiler builds a linearization — a deterministic order across the class and all traits. `super` in a trait forwards to the *next* class in that linearization, allowing chains like `trait Logged extends Service { abstract override def run() = { log(); super.run() } }`. This goes beyond Java, where `super` only reaches the immediate superclass (or a named interface default).

When two traits define the same concrete method, the *rightmost* in the linearization wins (most specific), while `super` traverses the rest. Unlike Java's "you must override a default clash," Scala silently picks by order — so reordering `with` clauses changes dispatch behavior.

The interview gold: Scala's design combines interface-style multiple inheritance with *cooperative super* chains — the sweet spot between Java's forced conflict resolution and C++'s layout chaos. The catch is that linearization is deterministic but invisible, so teams leaning on super-ordering can break behavior by reordering mixins.

## Q69: How does Kotlin's `super<Interface>` differ from Java in resolving clashing interface defaults, and how does Groovy handle it dynamically?

**A:** Kotlin, like Java, requires an explicit override when two supertypes define the same method — but the disambiguation syntax is typed: `override fun f() { super<A>.f() }` names which interface default to invoke. Java achieves the same effect with `InterfaceName.super.f()` but only needs it to select among clashing defaults; Kotlin makes the qualified call idiomatic in every multi-super override.

Groovy is dynamic: dispatch goes through the metaclass at runtime, so clashes resolve by declaration order or metaclass rules rather than a compile-time linearization. JVM default-method semantics interact with older Groovy versions inconsistently, making behavior version-dependent.

The portable lesson: never rely on implicit resolution order across languages. When a default clash is possible, provide an explicit synthesis method — that is the DRY, conflict-avoiding option that works under Java, Kotlin, and Groovy alike.

## Q70: What is the "abstract class re-defaults an interface method that a sub-interface re-abstracted" triple-decker, and how does it resolve?

**A:** The stack: `interface I { default void f() {} }` provides a body; `interface J extends I { void f(); }` re-abstracts it (implementers of J must implement); `abstract class Base implements J { @Override public void f() {} }` re-provides a concrete body. Subclasses of Base inherit `Base.f()` and need nothing; direct implementers of J outside Base still must implement.

Resolution is pure class-beats-default: `Base.f()` is a concrete class method, so it defeats both the interface default (in I) and the abstractness (in J) for every descendant of Base. The layered intent survives: I's default is the general convenience, J marks the contract as mandatory for strangers, Base chooses a specific safe implementation for its family.

For the interview: this is how real libraries offer "convenience default → strict re-abstraction → curated base implementation" in one signature — demonstrating that default, abstract, and concrete class layers interoperate and that class declarations always outrank interface defaults regardless of depth.

## Q71: What is the "aliasing" hazard when a base class exposes a factory method that internally calls an overridable method returning a value?

**A:** The hazard: a base factory (or any method) computes a result by calling an overridable *producer* — `protected Type buildCore()` — and the subclass overrides `buildCore()` to return a *different* type or mutate state. The base's factory logic then operates on subclass-provided results it never validated, and because the call is virtual, the base's own invariants (null checks, idempotency) run against unexpected returns.

This is the constructor-vs-override family of bugs (Q38) applied to return paths: the base "trusts" a virtual method and the subclass silently changes what flows back. It compounds with caching — a base `protected final Map cache` that an override `buildCore()` bypasses leaves stale reads.

The professional pattern: separate *stable orchestration* (final, does validation/caching) from *overrideable production* (documented hook), and validate the hook's contract — return type assertions, null guards — at the orchestration boundary. If the hook can violate base assumptions, the base should re-assert them rather than trust them blindly.

## Q72: When does "override to adapt" create an *identity* lie — e.g., overriding `toString`/`getClass`-backed reporting so the class presents itself as a different type?

**A:** Overriding methods whose contract is *identity-revealing* is usually dishonest. If a subclass overrides `getClass()`-derived behaviors, `equals`-family reporting, or type-name output to masquerade as another class, any caller that made *type-based* decisions on the info sees a lie — logging, serialization names, monitoring, and debugging all get misleading output.

Serialization is the sharp edge: overriding `toString` is fine for logs, but overriding methods that *drive serialized type names* (Jackson type info, a custom `typeName()`) can produce output that no longer round-trips — deserialization fails or binds the wrong handler. The disguise survives until a system component actually depends on the identity it reports.

The rule for interviews: *reporting overrides must report truth*; if a subclass needs to present itself differently, change the *contract* (an explicit `displayName()`), not the *identity* methods. Truthful overrides of `toString`/`equals`/serialization keys keep the subtype trustworthy under LSP.

## Q73: How do *reflection* and *method handles* observe overridden methods, and why must framework code filter synthetic bridges?

**A:** Reflection reports every declared method *and* inherited virtuals via `getMethods()`; overrides appear with the declaring class set to the class where they are declared. `getDeclaredMethods()` shows only that class's own (including synthetic bridges). A framework binding to an erased signature can accidentally resolve a bridge (the `Object`-typed adapter) instead of the real typed override.

That is why mocking, DI, and JSON libraries filter `isSynthetic()`/bridge methods when introspecting user classes: the bridge exists to satisfy the supertype, not to be a first-class behavioral override. Binding to it double-casts or loses typed behavior.

For the senior answer: reflection *sees* the mechanical reality (bridges, hidden super calls) that the language hides, and disciplined frameworks treat synthetic members as implementation artifacts. Knowing `isSynthetic()`, `Modifier.isBridge()`, and the declaring/accessibility APIs is how you write reflective tools that respect the source-level override contract.

## Q74: What are the *fundamental theorem* relationships — LSP, overrides, and the "fragile base" — in one coherent model?

**A:** LSP says a subclass must be substitutable for its base: every override must honor the base's *behavioral* contract, not just its signature. Overrides are the concrete realization of substitutability — they let a subclass replace behavior while preserving the type's promise. Fragile-base is what breaks when a base's *implementation* changes and overrides depended on ordering/timing silently.

Unify: LSP defines what an override *may* do; virtual dispatch defines *how* it runs; fragile-base describes the *coupling* between base internals and overrides. A healthy override (a) matches signature, (b) obeys the contract (narrows returns, widens exceptions/access, keeps invariants), and (c) depends only on documented base hooks, never on private orderings.

Interview-grade closing: signature matching is the *type* contract; LSP is the *behavioral* contract; and both are enforced by humans, not compilers — which is why code review of overrides is where the real safety lives.

## Q75: How do you design an *extension API* where overrides are the only legal extension point, and how do sealed plus final methods keep the base trustworthy?

**A:** The design: (1) the base class is *non-final but sealed*, listing the permitted subclasses — the only classes allowed to override; (2) the *algorithm skeleton* is a final method in the base, calling protected abstract/default steps; (3) every step is documented as a contract; (4) invariants are enforced in the final parts so a misplaced override cannot corrupt state before the skeleton runs.

Sealed gives the "checklist" benefit: the compiler knows every subtype, so adding a hook forces each permitted subclass to decide its behavior; final methods prevent overriding the parts that guarantee safety (validation, locking, resource ordering). The permitted set stays small, reviewed, and auditable.

The takeaway for interviews: *the base class's trust comes from two knobs — final (what cannot change) and sealed (who may change the rest)*. Open hierarchies scatter trust; sealed-plus-final concentrates where overrides are allowed, which is the modern, production-grade alternative to the fragile base.

## Q76: Design an override surface for a *publish/subscribe engine* where the *contract* is `final run()` orchestrating step hooks — show the template plus the danger of a hook returning prematurely.

**A:** Engine shape: `public final void run() { preflight(); FanoutContext ctx = open(); try { for (Subscriber s : resolve()) dispatchHook(s, ctx); } finally { release(); } }`. Hooks: `protected abstract void preflight();` `protected void dispatchHook(Subscriber s, FanoutContext c) { s.publish(c); }` `protected void release() {}`. Subclasses override hooks only; the skeleton guarantees ordering, resource release, and exactly-once close.

The danger of a premature return: a subclass override of `dispatchHook` that does `if (!c.subscribed) return;` silently skips a subscriber — legal LSP-wise (still one subscriber) but semantically a lost message. More subtle: an override that *re-throws* on the first error aborts the whole fanout, changing the base's guarantee of "keep going on per-subscriber failure."

For the interview: the template-method engine is safe precisely *because* the skeleton is final — every subclass can only vary the hooks, and every error/ordering guarantee lives in one place. The review checklist for such overrides is "what contract each hook carries" — premature optional return is the #1 silent-breaker.

## Q77: How do you make *override-based* config (a subclass returning values from overridden `config()`) hot-reloadable without forcing a class rewrite?

**A:** An override returning config is a compile-time decision: `protected Map config() { return Map.of("k","v"); }` is baked at build time. To hot-reload, invert the sourcing: the override *reads* from an external registry, `protected Map config() { return ConfigRegistry.load(name()); }`, so the override is a *routing* decision, not the value store — reloading the registry changes behavior with zero recompile.

The discipline this imposes: subclasses must call the loader, not hardcode; the loader must be fast (cached, invalidated on update), and the override must be the *only* seam for injecting values into the engine (a single `config()` the skeleton calls).

For the senior answer: override-based config buys *type-specific routing* while external registry holds *data*. The combination keeps polymorphism (each subclass decides where to load from) and hot-reload (the values can change). If subclasses *hardcode* values in overrides, hot-reload is impossible — the code review rule is "no literals in config overrides."

## Q78: How does *override-based dispatch* interact with *audit and compliance* — what breaks when a subclass bypasses an audited base method by overriding it?

**A:** If a base `post(Order o)` writes to the audit log and a subclass overrides `post` to *fast-path* without logging, the audit trail goes dark — an LSP breach no compiler catches. The standard defense is a final audited envelope: `public final void post(Order o) { auditWrite(o); postHook(o); }` where `postHook` is overridable — the audit step can never be skipped because it sits outside the hook.

Compliance systems therefore treat any *virtual* method whose semantics are legally significant as a "final envelope + documented hook" structure; a *virtual audit method itself* is a red flag. Regression tests should assert audit emits on every dispatch path.

Interview point: audit and overrides conflict by nature — overriding changes what runs, compliance wants fixed what runs. The resolution is always "seal the invariant, open the hook": invariants (logging, locking, ordering) live in final parts; only genuinely variable behavior is overridable.

## Q79: What are *pure virtual* re-declarations of an existing override, and how do they let an intermediate class *re-close* a method and reopen later?

**A:** In C++, a class can *re-declare a virtual as pure* even if inherited — `struct Mid : Base { void f() = 0; }` makes `f` abstract again in Mid's subtree even though Base supplied a body. Concrete subclasses of Mid must implement it. That is *pure re-abstraction* — the same "revoke the default" move as Java interface re-abstraction but at the class level.

This re-closing is powerful for staged designs: Base gives a safe default, Mid declares the behavior too risky to leave implicit, Leaf implements. The "reopen" happens when a later concrete class provides the body, making it a normal overridable method again for deeper levels.

The interview nuance: a pure re-declaration *destroys* the base's default for the Mid subtree even though it still exists in Base — so objects of Leaf can't call Base's `f` directly (the feature is gone below Leaf). Combined with the blankett: re-closing is a deliberate "no generic default here" statement.

## Q80: How do you *prove* an override is LSP-safe when you cannot rely on the compiler — what does a contract test suite for overrides look like?

**A:** Compilers verify signatures, not semantics. LSP-safety is proven with *contract tests* run against every override: a base-defined assertion battery (invariants hold, pre/post conditions, exception behavior, ordering) executed against each subclass. Frameworks like "abstract base test" patterns do exactly this: `BaseContractTest<T extends Base>` defines methods the subclass test must run.

The suite should include: (1) invariants after every public operation; (2) null/empty/edge inputs matching the base's contract; (3) the base's documented exception guarantees (e.g., "throws on duplicate" — an override that swallows fails); (4) equality symmetry across the family; (5) resource-close timing.

The senior view: *overrides are the unit of contract inheritance.* Signature checking is free; behavioral conformance is a test discipline. Teams with a contract-test base class catch LSP breaches at build time — which is the only meaningful "type safety" overrides can have.

## Q81: How does *serialization* change when a subclass overrides state-bearing methods, and what breaks if `readObject`/`writeObject` are overridden badly?

**A:** Serialization frameworks either introspect fields (Java serialization, Jackson, most formatters) or call accessors. If a subclass overrides a state-bearing accessor (e.g., `getStatus()` transforms internally), serializers calling `getStatus()` will write *transformed* values, and deserialization via the same accessor may re-transform — corrupting round-trips or violating invariants on read.

Java's `readObject`/`writeObject` are *special hooks used during deserialization*: overriding them badly (misordered `defaultReadObject`, or skipping superclass reads) produces objects with null/uninitialized superclass state — the "deserialized but broken" bug, plus potential security issues if validation is skipped.

For the interview: overrides that *change apparent state* and serialization do not mix; serializers want plain data, LSP-widening wants transformation. The safe architecture: keep persistence on *plain accessors* (final), and do presentation/transformation in *separate* methods — never let an override interpose between serialized bytes and internal state.

## Q82: What is "double dispatch via override and overloading" overlap — the classic "call a virtual method from an overloaded method" trap?

**A:** The trap: `void process(Base b) { b.handle(); }` and `void process(Sub s) { s.handle(); }` with `handle()` virtual. A call `process(actualSub)` where actualSub is statically `Base` picks overload `process(Base)` (static selection), which calls `b.handle()` — dispatching to `Sub.handle()` (dynamic). The caller *thinks* they got "the Sub path" but any *specializations local to `process(Sub)`* are lost — only the virtual `handle()` travels.

That is the "double dispatch is not automatic" lesson: static overload pick + virtual dispatch = single dispatch, not double. To get the dynamic type to influence the whole algorithm you need either a visitor or explicit re-call with typed narrowing.

The practical rule: if you have overloads partitioned by subtype *and* the objects are polymorphic, the overloads will *not* fire the way readers expect — route through a *single* virtual method instead, or make the parameter types drive a pattern match. Recognizing this saves a recurring class of "why did Sub's handler not run" bugs.

## Q83: How does *DOUBLE-dispatch without visitor* work with sealed types + pattern matching, replacing override-based double dispatch?

**A:** With sealed types and pattern switches, "dispatch both on the operation and on the type" collapses into nested matches: `sealed interface Bar {} ` → `switch (bar) { case Foo f -> op.applyToFoo(f); ... }`, and each op is itself a sealed node matched the same way. Both crossings become *exhaustive, centralized switches* instead of a visitor class with per-type override methods.

Overrides previously implemented visitor behavior as `accept(Visitor v) { v.visit(this); }` — double dispatch via two virtual hops. Sealed + switch lets you compute both axes in one function: match the bar type, then within it switch the operation (or vice versa), with the compiler guaranteeing completeness.

The interview stand: sealed types replace the visitor machinery for closed hierarchies — you get double-dispatch-like flexibility with single-source code and exhaustiveness. The override tree (visitor methods) is replaced by data patterns, which is the modern answer to the "operation × type" matrix.

## Q84: What does the *final-overrider* concept mean for *interfaces in Java* when two super-interfaces both default the same method, and where does the class's own method sit?

**A:** In Java, if interface A and interface B (neither extending the other) both default the same signature, an implementing class must override — the class's method is the *final overrider* for everyone. If a *sub-interface* of each also defaults (C extends A with a new default), the most *specific* one wins per the specificity rule, and a class override beats all.

The subtle part matching C++ "final overrider": Java's "class wins" means the *concrete class* is always the most specific — no interface default can outrank a class declaration, exactly as a C++ most-derived overrides base defaults. The parallel is clean once you define final-overrider = the most-derived implementation reachable via the dispatch path.

Interview-blade: both C++ (dominance) and Java (class-more-specific) converge on "the most derived object's own method wins"; the difference is Java forbids the *ambiguity* (compile-error forcing override) whereas C++ may need manual resolution for virtual bases. The *concept* of final overrider unifies the two answers.

## Q85: What is the "Fragile-Derived" inverse — when a *subclass* change breaks the *base* — and how do callbacks/overrides make it possible?

**A:** Fragile-base is base changes breaking derived. The inverse: a *subclass override* changes behavior that the *base's own* code depends on — e.g., the base's `start()` calls `onStart()`, a subclass override throws on a new precondition, and now *every* base-typed call to `start()` fails. The base was written to trust the hook; the hook turned hostile.

This is pure "override as hidden dependency": the base's correctness depends on every subclass's hook behavior, which is invisible when reading the base. The more virtual methods a base calls, the wider the blast radius of a bad override; the base can't guard every hook against a subclass's regressions.

The solution pattern: (1) minimize self-calls to hooks; (2) document hook contracts; (3) catch-and-handle exceptions per hook so a failing hook degrades rather than kills the base flow; (4) contract tests for the base's skeleton run against every subclass. The symmetric lesson of fragile-base and fragile-derived is the same: *virtual calls are contracts, and both sides must honor them.*

## Q86: How does overriding interact with *mocking frameworks* when a class's real method calls other virtual methods — what do mocks and stubs capture, and what do they miss?

**A:** A mock subclass overrides (via the framework) every method on the interface/class, replacing bodies with canned behavior. Critically, mocking captures the *method boundary* — calls *into* the object are intercepted, but *internal self-calls* (`this.other()`) in the real code are *not* mocked if the class is partially mocked; if the class's real method runs, its inner virtual calls dispatch to the subclass's stubs (for mocks they do get redirected, which is why "call super" hybrids confuse people).

So tests truly exercise the *real method* only when it's a final/self-contained path; any internal virtuals go through Whatever stubs the framework installed. That's why "deep class hierarchies + partial mocks" produce false confidence: the tested behavior depends on what got stubbed.

The senior guidance: prefer *contract-tested interfaces* (mock the *leaf* types) over mocking deep bases; if you partly mock a class, know *exactly* which internal calls still hit real overrides. Knowing the mock's virtual-call semantics is the difference between confident and accidental unit tests.

## Q87: What are *interface defaults vs red-black override* conflicts — how do you thread a defaulted method through *three* interfaces and still pick the right class?

**A:** With three interfaces (I base with `default m()`, J extends I re-declaring `m()`, K re-defaulting a *different* `m()`), a class implementing J and K faces a clash: two defaults with no "more specific" — compile error requiring explicit override. Threading means writing `public void m() { J.super.m(); }` (or whatever the design intends), which is the *only* legal resolution.

The pitfall: *I's* default might be the one everyone assumed would run, but the conflict never *uses* it — the class must pick one parent's default explicitly, and picking *wrong* (the more general one hiding the semantics) is silently legal.

The interview answer: default conflicts force the *author* to decide, and that decision becomes the new contract for the class. Threading defaults across three levels works when each level's default is *semantically different* and the class override synthesizes them — never rely on "the base default will win."

## Q88: How do *bridged generic overrides* break *structural type checks* (e.g., a `Comparable` comparison in a mixin) when reflection inspects a class?

**A:** A class implementing `Comparable<T>` generates a syntactically-typed `compareTo(T)` and a *bridge* `compareTo(Object)`. Reflection sees both; code that enumerates `getMethods()` and expects *one* `compareTo` may be surprised, and code calling the *raw* `Comparable.compareTo(Object)` resolves to the bridge — which casts and delegates, so behavior is fine but the *identity* of the method isn't the one the developer wrote.

Tools that bind *by method name+parameter count* can bind the bridge; tools that filter by `isSynthetic()` are spared. On hot paths, calling the raw interface entry touches the bridge's cast, adding a tiny cost.

For the interview: bridges are the mechanical seam between source-level generics and erased JVM dispatch. Recognizing `isBridge()`/`isSynthetic()` filtering in frameworks is a direct signal of someone who has debugged reflective binding against generic overrides.

## Q89: What is "override provenance" tracking, and why do bytescode tools (ASM, Byte Buddy) need it to generate correct subclass behavior?

**A:** Override provenance is knowing, for each method, *which* hierarchy level truly declares it and what bytes are the final override. Code generators subclassing user types must decide which methods to delegate, which to keep, and which are final/abstract — so they walk the ancestry, flag finals (undelegable), abstract (must implement), and bridges (usually re-delegate).

Getting provenance wrong yields generated classes that compile but misbehave: delegating a final method (illegal), failing to implement an abstract, or double-wrapping a bridged pair so a call loops. Provenance is also how generators decide *what to copy* when a method has default/super semantics.

The senior note: bytecode generation is "runtime overriding at scale" — every override rule (final, abstract, bridge, default precedence) must be re-implemented in the generator's model. Teams that cling to frameworks treating classes as "open" often hit the exact final-method walls this model predicts.

## Q90: When is *overriding across a protected/public seam* with *package-private bases* the cause of subtle non-dispatching bugs in frameworks?

**A:** A package-private method in a base is *not inherited* by subclasses in other packages — so a "same-signature" method in an external subclass is a *new, unrelated method*, and internal base calls never dispatch to it (they resolve to the package-private base body). Frameworks that call a hook expecting external override behavior watch the hook silently do *nothing*.

The classic bug: a library's base has `void ready()` (package-private) called internally; a user subclass writes `public void ready()` expecting to hook — it never runs, because the library's internal call binds the package-private base version. The fix is protected/public hooks voiced intentionally.

Interview takeaway: *accessibility is part of the override contract.* Cross-package override requires the base member to be protected or public; package-private/m известно — versus — hides it entirely outside the package. Frameworks that *intend* extension must declare hooks protected/public, and users must check the base's real declaration before "overriding."

## Q91: How do *default, abstract, final, and sealed* form one coherent *extension strategy* across a large framework's public classes?

**A:** Coherent strategy: the framework's public *frosted* API is a set of *sealed* classes (closed subtype families) with *final* skeletons and *abstract or default* step hooks. Every subtype is permitted explicitly; every hook is documented; invariants are final. Extension happens only through the declared hooks — no override of skeletons, no new subtypes sneaking in.

This collapses the four mechanisms into one policy: default = optional override, abstract = required override, final = never override, sealed = who may override. Interviewees who can articulate that *sealed+final* is a governance layer on top of override (not a mechanism against it) show mature API design thinking.

The closing thought: an extension strategy is *legible* when a new developer can look at a class and instantly see which methods are for overriding, which are fixed logic, and which types may extend — that's what sealed/final/default/abstract, used deliberately, deliver.

## Q92: How does *override-based* hot-plugging (strategy via subclassing) compare to *composition-based* strategy in a performance and fragility review?

**A:** Override-strategy: you create subclasses that override an algorithm step; calls go through the base type, virtual dispatch handles selection. Composition-strategy: an interface field is injected; collaboration goes through the field. Both give runtime selection, but override bakes the choice into the *type hierarchy* (one subclass per strategy), while composition keeps the host class stable.

Performance: virtual dispatch on a final/sealed set is nearly free (monomorphic + inlining); composition adds a field dereference but equally devirtualizes. Fragility: override strategy multiplies classes and couples each strategy to the base's shape (fragile-base risk); composition decouples strategies from the host (they implement a narrow interface).

The architect answer: use *override* for small, family-coherent variations (template hooks), *composition* for independent, swappable behavior; and recognize that every override is a subclassing commitment — one more fragile edge — while a composition field is a gentle seam.

## Q93: What is the *"override to fix a bug in base"* anti-pattern, and how does it differ from the sanctioned *workaround* in a third-party library?

**A:** Overriding to fix a base bug inside your hierarchy: the subclass re-implements the broken base logic. Even if it works, it's a fork: the fix doesn't exist in the base, all other subclasses keep the bug, and the next base upgrade re-breaks the override if the base method changes. The anti-pattern's cost is *duplicated, divergent truth*.

The sanctioned workaround for a third-party library: a subclass that overrides exactly the broken method, but *isolates* the divergence (a small, documented, tested override), plus a version-pin and an issue ticket; when the library fixes it in a new version, you drop the override. Same mechanics, different discipline: the override is *explicitly temporary* and *professionally tracked*.

Interview-grade distinction: the anti-pattern is *permanent, silent, or copied-from-base*; the workaround is *temporary, visible, and minimal*. The rule: never copy base bodies into overrides to repair defects — extract/watch, document, and schedule removal.

## Q94: How does *generics + inheritance + override* interact with *type erasure and unchecked warnings* — the "raw type override" trap?

**A:** The trap: overriding a method of a *generic base* while using the *raw type* collapses signatures to erased forms, and the compiler may flag `unchecked` conversions. `class Box { void add(Object o) }` vs generic `void add(T t)` — after erasure both are `add(Object)`, so a subclass overriding with `add(Object)` actually overrides the erased method, but dispatches through `` missing the generic safety.

Using raw types in an override is legal but erases the "convenient typed" bridge, and callers get warnings and possible `ClassCastException`at the bridge boundary. The correct approach: override with the *parameterized* generic (`@Override void add(String s)` in `StringBox extends Box<String>`), letting the compiler generate the typed method + bridge.

For the interview: never override against a raw, generic-less base — you sacrifice type safety and the compiler's bridge/check machinery. Parameterizing the override preserves both and is the only way to keep generic guarantees across inheritance.

## Q95: What is *"override-only" API design* — exposing *neither fields nor helpers* to subclasses, only hook methods — and what does it buy a security-sensitive base?

**A:** An override-only base exposes exactly the overridable steps and hides every implementation detail: subclasses see `protected void hookX()` semantics, but the state they could corrupt, the fields they could alias, and the helpers they could misuse are all private. This is how security-sensitive bases (validators, cryptographic runners, rate limiters) control their surfaces.

The benefits: subclass *intent* is legible (their overrides are their whole contract), mutation opportunities are zeroed, and future refactors stay private. The cost: flexibility — a subclass that needs *new* behavior can't add it without either a new hook (base change) or composition.

Interview framing: "override-only" is encapsulation applied to inheritance — the base gives hooks, the subclass gives behavior, neither touches the other's dirt. It's the natural companion to sealed: sealed says who may extend, override-only says what they may touch.

## Q96: How do *overriding equals/hashCode at multiple levels* + *hashing containers* interact when a subclass adds *mutable* state to the equality key?

**A:** If a subclass adds a mutable field to the equals/hashCode key, hash-based containers break the moment the field changes: the object's bucket becomes stale, so `contains`/`get`/`remove` miss it — "the item vanished from the map" even though it's present. This is the mutable-key hash bug compounded across an override chain, because each level contributes key components.

The intermediate damage: `Base`'s hashCode may not include the subclass's field; `Sub`'s does. Two objects equal under `Base` but not `Sub`, or vice versa — asymmetric lookups in mixed-type collections. Consistency (equal objects hash equal) must be maintained *within the equals class*, so mixing base/sub hashes in one map is where the mismatch bites.

The rule for interviews: *if a key can mutate, rewrite it into the map as immutable*; if equals spans hierarchy levels, keep the mutable members out of the key or make them immutable/final. The override chain multiplies the risk, so one owning level for equality + immutable-within-key fields is the safe design.

## Q97: What are *method descriptors vs signatures* in bytecode, and why do they make *JVM override checks* stricter than source-level tests?

**A:** The JVM method *descriptor* includes the full return type and parameter types (e.g., `(Ljava/lang/String;)V`), while source "signature" (in Java) is name + parameters (return can covary). The JVM requires the *exact descriptor* match for an override — a covariant return adds a *bridge* so the JVM sees both the typed method and the base-descriptor adapter.

Because the JVM matches descriptors, a subclass method that is "an override" at source (e.g., covariant return) may *not* be one at bytecode until the bridge exists; tools that skip bridge/synthetic methods may fail to detect the real override — a "stricter than source" interaction.

The interview point: JVM override = descriptor match; the bridge is the compiler's way of satisfying both the source-level promise and the bytecode-level identity. Disagreements between "what Java says overrides" and "what the JVM chains" are exactly where synthetic/mangled mysteries live.

## Q98: How do you *architecturally freeze* an override contract so subclasses *inherited from one vendor* cannot break yours — class-in-vendor / bridging hierarchies?

**A:** Vendor-shipped bases are *outside your control*. You adopt them by *sealing the adapter*: your own classes extend the vendor type but mark the *sensitive* methods final, and expose your own hooks for *your* consumers to override. The internal override surface (to the vendor) is managed; the external override surface (to your clients) is yours.

Concretely: `public class MyAdapter extends VendorBase { @Override public final void run() { prep(); vendorRun(); post(); } protected void prep(){} protected void post(){} }`. Vendor semantics stay controlled; your clients override `prep/post`, never the vendor seam. A vendor upgrade can't silently change your clients' hooks because your final boundary redefines the contract.

The senior takeaway: *freezing an override contract* means inserting a final layer between someone else's open base and your own open surface. Two boundaries, two policies — your stability is independent of the vendor's evolution because the adapter's final methods pin the behavior.

## Q99: What is *governed override* — how versioned APIs (SemVer), deprecation, and *override lifecycle* reduce the cost of changing hook contracts?

**A:** Governed override = treating an override surface like a versioned API: hooks have names, contracts, deprecation dates, and replacement paths. When a base wants to change a hook's semantics, it adds the *new* (defaulted) method, deprecates the old, lets implementers migrate, and later removes it in a major release — the same discipline as public API versioning applied to protected members.

The payoff: subclasses never break silently; deprecation warnings surface at compile time; migration can be incremental. The cost: the base carries deprecated hooks during overlap, and "hook debt" grows unless removals actually happen on schedule.

For the interview: good inheritance design treats *protected override-ables as the framework's most-used API* — arguably *the* real consumer API — and governs them with the same rigor as public methods. Versioned replacements, batch deprecations, and a removal cadence are what prevent hook-contract drift from becoming unmentionable legacy.

## Q100: Synthesize: what single mental model unifies overriding, hiding, shadowing, dispatch, and the fragile-base problem?

**A:** The unified model: *a name's meaning is resolved at different layers — scopes (shadowing), compile-time type (hiding/overload), runtime type (override/dispatch) — and every layer that can silently differ from the author's intent is where bugs live.* Shadowing changes which *name* you mean; hiding changes which *member* you statically bind; overriding changes which *body* dynamically runs; fragility arises when a body depends on assumptions that another layer can violate.

The discipline that follows: each layer wants *explicitness* — distinct field names, `@Override`/`override` specifiers, `this.`/`super` qualifications, final/sealed boundaries, contract tests per override, and documented hooks. Every language provides the same mechanisms with slightly different names; the interview question is always *which layer resolves the name and which governs the body*.

Closing synthesis for the reader: overriding is the *soul* of polymorphism, hiding and shadowing its silent cousins, and fragile-base its price — master all three as *name-resolution + body-resolution* maps, and you can reason about any OO language's inheritance behavior from first principles.
