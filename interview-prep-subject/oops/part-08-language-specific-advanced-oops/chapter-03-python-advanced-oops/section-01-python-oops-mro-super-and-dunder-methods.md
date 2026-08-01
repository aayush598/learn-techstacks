# Python OOPs: MRO, `super()`, and Dunder Methods

> **TL;DR**: Python resolves method lookup on a single **C3-linearized MRO** so the diamond problem has one deterministic answer, `super()` threads calls cooperatively through that whole MRO (not just the parent), and **dunder methods** are the protocol hooks through which operators, builtins, and iteration are implemented — Python's alternative to interfaces.

## 1. Why Does This Exist?
Python allows multiple inheritance, which raises the **diamond problem**: if `class D(A, B)` and both `A` and `B` inherit `Base`, which `method` does `d.method()` call, and in which order do `__init__`s run? Python solves this *deterministically* with the **C3 linearization** (MRO), a mathematically-guaranteed ordering that is consistent, monotonic, and unambiguous. `super()` then exists to make calls *cooperative*: instead of hard-coding "call my parent," `super()` asks the runtime for the *next class after self's type in the MRO* — which is what lets an `__init__` chain touch every class exactly once. **Dunders** exist because Python has no operator overloading syntax built into the parser as separate features: `a + b`, `len(x)`, `x[i]`, `for i in x` are all *desugared* into calls like `a.__add__(b)`, `x.__len__()`, `x.__getitem__(i)`, `x.__iter__()`. Together, MRO + dunders are the machinery that lets a dynamic, duck-typed language still deliver deterministic OOP semantics and rich protocols.

## 2. How Does It Work?
At a glance:
- Every class has a **`__mro__`** tuple — the linear order in which attributes/methods are searched.
- MRO is computed by **C3 linearization**: merge each parent's MRO, honoring local precedence (left-to-right base order) and the monotonicity constraint.
- **`super()`** with no args returns a proxy that, inside a method of class `X`, resolves the *next* class after `X` in the *instance's* MRO.
- **Dunders**: `__add__` for `+`, `__eq__`/`__hash__` for equality/hashing, `__len__`, `__getitem__`/`__setitem__`, `__iter__`/`__next__`, `__call__`, `__enter__`/`__exit__`, `__str__`/`__repr__`, `__getattr__`/`__setattr__`/`__getattribute__`.
- Attribute lookup order: `type(obj).__mro__` → data descriptors → instance `__dict__` → class attributes → non-data descriptors → `__getattr__`.

## 3. When Is It Used?
- **Any multiple inheritance** — mixins (e.g., logging, serialization, validation) combined into one class.
- **Frameworks** — Django's `Model` inheritance, SQLAlchemy declarative base, `collections` ABCs, pytest's `BaseException` hierarchy — all rely on MRO and cooperative `super()`.
- **Operator overloading** — numeric types (numpy arrays `+`), custom containers, comparison objects (`__lt__` for sorting via `functools.total_ordering`).
- **Context managers** — `with open(...)` uses `__enter__`/`__exit__`.
- **Protocol implementation** — making custom objects iterable, sliceable, callable, hashable, comparable.
- **Dataclasses & ABCs** — `@dataclass` for value objects; `abc.ABC` + `@abstractmethod` for interface-like contracts.

## 4. Why Wasn't Another Approach Chosen?
Alternatives to C3:
- **Depth-first, left-to-right (pre-C2.3 Python)**: non-monotonic — changing a class's base list could silently change which method got inherited, causing the infamous "Diamond problem broke inheritance order" bugs. C3 fixed monotonicity.
- **Reject multiple inheritance (Java)**: Java banned it and introduced interfaces instead — simpler but requires explicit re-implementation or delegation for mixin behavior; Python embraced MI and solved it with C3.
- **Per-call resolution / always dynamic lookup (duck typing alone)**: without MRO, attribute lookup would be ambiguous for diamonds; C3 makes it deterministic.
Alternatives to dunders:
- **Named methods with special prefixes (`_plus`, `_eq`)**: Python deliberately uses *surrounding* underscores so user names never collide, and special methods are looked up on the *type*, not the instance (so monkey-patching a method on one instance can't break builtins).
- **Operator keywords in the grammar (`a + b` built into the compiler)**: dunders keep the parser simple and allow *any* class to define any operator via the same mechanism — operators are just methods with reserved names.

## 5. Intuition
Think of the MRO as a **chain of command fixed at class-definition time**. In a company where a manager (`D`) reports to both a Sales VP (`A`) and an Engineering VP (`B`) — who both report to the CEO (`Base`) — the rule is: "the leftmost boss takes precedence, but never jump over a more distant boss in the chain." So the order is D → A → B → Base: `D`'s own people first, then the left parent's whole line, then the right parent's line, with each shared ancestor appearing once. `super()` is the **"pass it up the chain"** instruction: each level handles its part, then hands the remaining work to whoever is *next in the chain of command* — which, thanks to MRO, is a single well-defined person, so the whole chain of `__init__`s runs exactly once, in order.

## 6. Real-World Analogy
A **relay race with a fixed baton order**: the team order is written on a board (the MRO). Each runner (a class in the diamond) runs their leg then hands the baton to the *next runner on the board* (`super()`), not to "my coach's favorite" (a hard-coded parent name). If every runner passes to the next board entry, the baton travels the whole list exactly once. If one runner insists on handing to a specific runner out of order (calling `Base.__init__` directly), the baton visits some runners twice and others never — a broken relay. The dunders are the **standardized lap markers**: everyone agrees `len(x)` means "run `x.__len__`", so any team that implements `__len__` automatically fits into any event that asks "how long is this?"

## 7. Formal Definition
- **MRO (Method Resolution Order)**: the tuple of classes (the class itself, its bases transitively, ending at `object`) in which attribute lookup proceeds; for `class D(A, B)`, C3 merges `[D] + merge(L(A), L(B), [A, B])` where `L(X)` is X's linearization, subject to: local precedence (bases ordered left-to-right) and monotonicity (a class's MRO can't change based on its position).
- **C3 linearization**: a merge of the parents' linearizations that respects constraints; if inconsistent, Python raises `TypeError: Cannot create a consistent MRO`.
- **`super()`**: returns a proxy that uses the `__class__` cell + the first argument's type to find the next class in `self.__mro__` after the current class; `super(X, self)` = "start searching after X in `self.__mro__`."
- **Dunder methods**: `__xxx__` reserved methods invoked *implicitly* by syntax/builtins (e.g., `+` → `__add__`); lookup is on the type (with reflected variants `__radd__`, and `__iadd__` for `+=`).
- **Protocols**: informal structural contracts (e.g., iterable = `__iter__` or `__getitem__`; context manager = `__enter__`/`__exit__`; hashable = `__hash__`).
- **`__eq__`/`__hash__` rule**: defining `__eq__` sets `__hash__` to `None` (unhashable) unless you restore it.

## 8. Example
Diamond + cooperative `super()`:
```python
class Base:
    def __init__(self):
        print("Base")
        self.attr = "base"

class A(Base):
    def __init__(self):
        print("A")
        super().__init__()          # next in MRO after A

class B(Base):
    def __init__(self):
        print("B")
        super().__init__()          # next in MRO after B

class D(A, B):
    def __init__(self):
        print("D")
        super().__init__()          # next in MRO after D

d = D()
```
What prints:
```
D
A
B
Base
```
Because `D.__mro__ == (D, A, B, Base, object)`. Each `super()` jumps to the *next* entry, so every `__init__` runs exactly once, in MRO order. If `A` had instead called `Base.__init__()` directly, the output would be `D A Base B Base` — `Base` initialized **twice** and `B` after `Base`'s state — the classic broken diamond.

MRO computation by hand for `D(A, B)`:
- `L(Base) = [Base, object]`
- `L(A) = [A] + merge([Base, object], [Base]) = [A, Base, object]`
- `L(B) = [B, Base, object]`
- `L(D) = [D] + merge([A, Base, object], [B, Base, object], [A, B])`
  - Take `A` (head of first list, not in any tail). Take `B`. Then `Base`, then `object`.
  - Result: `[D, A, B, Base, object]` ✓

## 9. Internal Working
1. **Class creation**: when a class body is executed, Python computes the MRO via the C3 algorithm and stores it in `type(cls).__mro__`; inconsistency raises `TypeError`.
2. **Attribute lookup**: `getattr(obj, name)` does: look up `name` in `type(obj).__mro__` (finding a descriptor triggers `__get__`); if a data descriptor (has `__set__`/`__delete__`) exists, it wins over the instance dict; else instance `__dict__`; else non-data descriptors/class attrs; if still missing → `type.__getattr__(obj, name)`.
3. **`super()` resolution**: `super()` uses the `__class__` closure cell to know "current class"; calling `super().m()` constructs a proxy whose `__getattribute__` scans `obj.__mro__` from *after* the current class onward.
4. **Special-method lookup is on the type**: `obj + other` calls `type(obj).__add__(obj, other)` (then `type(other).__radd__`), *not* `obj.__add__` — this prevents an instance from breaking builtins by instance-level monkey-patching.
5. **`__eq__` kills `__hash__`**: the compiler sets `__hash__ = None` on a class that defines `__eq__` without `__hash__`; dict/set membership then raises `TypeError: unhashable type`.
6. **`@dataclass`**: the decorator generates `__init__`, `__repr__`, `__eq__` (and with `frozen=True`, `__setattr__`/`__hash__`); `@abstractmethod` requires the metaclass `ABCMeta` so instantiation is blocked until all abstract methods are implemented.

## 10. Time Complexity
- MRO computation: O(classes in hierarchy) once per class creation — negligible.
- Attribute lookup: O(MRO length) in the worst case (each class's dict checked); Python caches attribute lookups in the type's "MRO version" cache, making repeated lookups ~O(1).
- `super()` call: O(MRO scan) — in practice O(1)-ish because the proxy holds a cached index.
- Dunder dispatch: same as a normal method call (no extra indirection beyond the type lookup).
- `isinstance(x, cls)`: uses the MRO/subclass check, cached — O(1) amortized for hot types.

## 11. Advantages
- Deterministic, monotonic method resolution — the diamond problem has *one* right answer.
- Cooperative `super()` lets mixins initialize in a well-defined order without duplication.
- Dunders give natural operator syntax to any user class (numpy arrays, Django querysets `|`).
- Duck typing + protocols mean you implement behavior, not type contracts — very flexible.
- `@dataclass` removes boilerplate for value objects; ABCs provide real interface checks when you want them.
- Everything is inspectable: `cls.__mro__`, `obj.__dict__`, `type(obj)` — great for debugging and frameworks.

## 12. Disadvantages
- C3/`super()` is subtle: one non-cooperative class (a hard-coded parent call) breaks the whole diamond silently.
- No compile-time checking: name typos (`__lenh`) fail at runtime, not at import; attribute errors surface late.
- `__eq__`/`__hash__` and mutable-keys traps are easy to hit (unhashable objects, broken dicts).
- Dunder protocols are *informal* — a missing method only fails when a builtin touches it (e.g., `len(obj)` → `TypeError: object of type 'X' has no len()`).
- Multiple inheritance + `super()` in deep frameworks (e.g., mixing Django `Model` with a third-party mixin) can produce order-dependent, hard-to-debug state.
- Performance: attribute lookup is dynamic (dict + MRO scan) — slower than statically-dispatched C++; mitigated by caches but hot loops still pay.

## 13. Interview Questions
1. **Q: What is the MRO and how is it computed?** A: The method resolution order — the linear list of classes Python searches for attributes; computed by the C3 linearization algorithm at class creation (local precedence + monotonicity), stored as `__mro__`.
2. **Q: What is the diamond problem in Python?** A: `class D(A, B)` where `A` and `B` both inherit `Base` — which `method`/`__init__` runs and in what order; Python answers deterministically via C3: `D → A → B → Base → object`.
3. **Q: How does `super()` differ from calling a parent explicitly?** A: `super()` resolves to the *next class in the instance's MRO*, so in multiple inheritance it cooperatively calls the next class (possibly an "uncle"), enabling each `__init__` to run exactly once; hard-coding `Base.__init__()` breaks that.
4. **Q: When does `super()` fail or misbehave?** A: When a class in the hierarchy calls a specific parent directly instead of `super()` (double-init), or when the MRO is inconsistent (TypeError), or when argument signatures between classes in the chain differ (`__init__ got multiple values`).
5. **Q: What dunder methods implement `+`, `==`, `len()`, `in`, and iteration?** A: `__add__` (and `__radd__`/`__iadd__`), `__eq__` (+ `__ne__`), `__len__`, `__contains__` (falls back to iteration), `__iter__`/`__next__` (or `__getitem__`).
6. **Q: Why does defining `__eq__` make an object unhashable?** A: Python sets `__hash__` to `None` when you define `__eq__` without `__hash__` — equal objects must hash equally, and the default (id-based) hash would break that; restore `__hash__` explicitly if safe.
7. **Q: `__getattr__` vs `__getattribute__`?** A: `__getattribute__` is called for *every* attribute access; `__getattr__` only when normal lookup fails — use `__getattr__` for defaults/fallbacks and `__getattribute__` (rarely) for interception, with infinite-recursion care (`object.__getattribute__`).
8. **Q: What is duck typing and how does Python use it?** A: "If it walks like a duck" — behavior over declared type: any object with `__iter__` is iterable, with `__enter__`/`__exit__` works in `with`, with `__lt__` is sortable; no interface declaration needed.
9. **Q: How do you create an interface-like contract in Python?** A: `abc.ABC` + `@abstractmethod` (blocks instantiation until implemented), or structural protocols via `typing.Protocol` (Python 3.8+) / `isinstance` checks.
10. **Q: What is `@dataclass` and when would you use it?** A: A decorator generating `__init__`, `__repr__`, `__eq__` (and optionally frozen/immutable via `frozen=True`, ordering via `order=True`) for value/configuration objects, cutting boilerplate.
11. **Q: What happens if two bases provide the same method name?** A: The MRO decides: leftmost base's method wins (local precedence), unless overridden; `super()` from the left base jumps to the right base's version next.
12. **Q: How does `+` fall back to `__radd__`?** A: `a + b` tries `type(a).__add__(a, b)`; if that returns `NotImplemented`, it tries `type(b).__radd__(b, a)`; if neither, `TypeError`.
13. **Q: What is `__slots__` and why use it?** A: Declares fixed instance attributes instead of a per-instance `__dict__`, saving memory and speeding access; breaks `__dict__` and dynamic attribute creation.
14. **Q: How does `len()`/`bool()` actually work?** A: `len(x)` → `type(x).__len__(x)`; `bool(x)` → `__bool__` if defined, else `__len__` (truthy if len > 0), else always True.
15. **Q: What is a context manager and its dunders?** A: An object with `__enter__` (returns the resource) and `__exit__` (cleanup, suppresses exceptions if it returns True); the `with` statement calls them around the block.
16. **Q: How do you make an object callable or iterable?** A: Implement `__call__(self, ...)` → `obj(...)` works; implement `__iter__` returning an iterator with `__next__`, or `__getitem__` with integer indices for the fallback iteration protocol.
17. **Q: What is `NotImplemented` vs `TypeError`?** A: A dunder returns `NotImplemented` to say "I can't handle the *other* type" so Python tries the reflected operator; raising `TypeError` aborts — the distinction drives correct operator overloading.
18. **Q: How does Python resolve `isinstance`/`issubclass`?** A: `isinstance(x, C)` checks `type(x).__mro__` (and `__instancecheck__` for ABCs/protocols); `issubclass` walks the MRO (plus `__subclasshook__`).

## 14. Follow-Up Questions
1. **Q: What is monotonicity and why does C3 enforce it?** A: A class's MRO must not change based on where it appears in another class's base list — C3 guarantees a consistent global order, so `super()` chains can't depend on the "viewpoint."
2. **Q: How does `typing.Protocol` differ from ABCs?** A: ABCs require *explicit* inheritance; Protocols are *structural* — any class with matching methods is a subtype without inheriting (checked by `isinstance` via `@runtime_checkable`).
3. **Q: What is the "C3 merge" failure mode?** A: If two parents' linearizations conflict (e.g., inconsistent base ordering), C3 can't merge → `TypeError: Cannot create a consistent MRO` — the fix is reordering bases or reworking the hierarchy.
4. **Q: Why does special-method lookup use the type and not the instance?** A: Because special methods are protocol hooks: instance-level monkey-patching `__len__` would make `len()` non-deterministic per-instance and could break builtins; type-level lookup keeps builtins stable and cacheable.
5. **Q: What happens with `super()` in a dataclass or namedtuple subclass?** A: The generated `__init__` uses `super()` too, so dataclasses cooperate in MRO chains — but argument order/names must line up across the diamond or you get `TypeError: __init__() got an unexpected keyword argument`.

## 15. Coding Example
```python
# Cooperative mixin diamond with super()
class JsonMixin:
    def to_dict(self):
        data = super().to_dict() if hasattr(super(), "to_dict") else {}
        data["kind"] = type(self).__name__
        return data

class Base:
    def to_dict(self):
        return {"id": getattr(self, "id", None)}

class User(JsonMixin, Base):
    def __init__(self, uid, name):
        self.id, self.name = uid, name
    def to_dict(self):
        data = super().to_dict()
        data["name"] = self.name
        return data

u = User(1, "alice")
print(u.to_dict())   # JsonMixin runs last (it's first in MRO), adds "kind" -> {'name': 'alice', 'id': 1, 'kind': 'User'}
print(User.__mro__)  # (<class '__main__.User'>, <class '__main__.JsonMixin'>, <class '__main__.Base'>, <class 'object'>)
```

```python
# Value object with dataclass + equality/hash done right
from dataclasses import dataclass

@dataclass(frozen=True)          # frozen: immutable + auto __hash__ from fields
class Point:
    x: float
    y: float

p1, p2 = Point(1, 2), Point(1, 2)
print(p1 == p2)                  # True (field equality, not identity)
print(hash(p1) == hash(p2))      # True (frozen => consistent hash)
d = {p1: "origin-adjacent"}      # works: hashable
```

```python
# Operator + protocol dunders
class Vec:
    def __init__(self, x, y): self.x, self.y = x, y
    def __add__(self, o): return Vec(self.x + o.x, self.y + o.y)
    def __eq__(self, o): return isinstance(o, Vec) and (self.x, self.y) == (o.x, o.y)
    def __len__(self): return 2
    def __iter__(self): return iter((self.x, self.y))
    def __getitem__(self, i): return (self.x, self.y)[i]
    def __repr__(self): return f"Vec({self.x}, {self.y})"

v = Vec(1, 2) + Vec(3, 4)        # __add__
print(v[0], len(v), list(v))     # 4 2 [4, 6]
```

## 16. Industry Usage
- **Django ORM**: `Model` metaclass + multiple-inheritance mixins (permissions, timestamps, soft-delete) rely on MRO and cooperative `super()`; Django's `QuerySet` overrides `__and__`/`__or__` for chaining.
- **FastAPI/Pydantic**: pydantic v2 `BaseModel` uses dataclass-style generation + validators; FastAPI models are plain Python classes whose `__eq__`/`__init__` are synthesized.
- **NumPy/Pandas**: operator overloading (`ndarray + ndarray` via `__add__`/`__array_ufunc__`), `__len__`, `__getitem__` power the whole array DSL.
- **requests, aiohttp**: context managers (`with requests.get(...) as r`) implement `__enter__`/`__exit__` for resource cleanup.
- **pytest**: fixtures and assertion rewriting use `__getattr__`/`__getattribute__` machinery; its `BaseException`-style introspection drives failures.
- **scikit-learn / transformers**: classes use `__getitem__`-style access, `__repr__` for configs, and ABC-style estimator interfaces (`BaseEstimator`).

## 17. References
- Guido van Rossum, *Python 3.0 What's New* — the C3 MRO change; the C3 paper by Barrett, Cassels, Haahr, Moon, Plevyak, Sells (1996).
- Python Language Reference, §3.3.7 "Emulating container types", §3.3.10 "Special method lookup", §3.3.11 "Customizing attribute access"; §6.2.9 "super".
- cpython source: `Objects/typeobject.c` (MRO computation `mro_impl`), `Objects/abstract.c` (operator dispatch).
- PEP 3115 (metaclasses), PEP 557 (`dataclasses`), PEP 484/544 (typing / protocols).
- Luciano Ramalho, *Fluent Python (2nd ed.)*, ch. 9-12, 16 (protocols, ABCs, dunders).
- Al Sweigart / C3 tutorials: `blog.ihongtu.com` and Guido's `python-history.blogspot.com` post on MRO.

## 18. Cheat Sheet
- MRO = C3 linearization, `cls.__mro__`, e.g., `D(A,B)` → `(D, A, B, Base, object)`.
- `super()` = next class after `self`'s class in the instance's MRO — cooperative.
- Broken diamond = hard-coded `Base.__init__()` instead of `super()` → double-init.
- Operators: `+` → `__add__`/`__radd__`/`__iadd__`; `==` → `__eq__`/`__ne__`; `in` → `__contains__`.
- `len` → `__len__`; `bool` → `__bool__` then `__len__`; callable → `__call__`; iteration → `__iter__`/`__next__`.
- Defining `__eq__` without `__hash__` ⇒ `__hash__ = None` ⇒ unhashable.
- `__getattr__` = fallback only; `__getattribute__` = every access; `__setattr__` = writes.
- Special-method lookup is on the *type*, not the instance.
- `@dataclass(frozen=True)` = immutable value object with equality/hash.
- ABCs (`@abstractmethod`) = explicit contracts; `typing.Protocol` = structural.

## 19. Quiz
1. `class D(A, B)` — the C3 MRO starts: a) D, B, A b) D, A, B c) D, Base, A, B d) D, object → **b**
2. `super()` resolves to: a) The parent class b) The next class in the instance's MRO after the current class c) `object` d) The leftmost base → **b**
3. Defining `__eq__` without `__hash__` makes instances: a) Hashable by id b) Unhashable c) Non-comparable d) A TypeError at import → **b**
4. Which implements `len(x)`? a) `__len__` b) `__length__` c) `__size__` d) `__getitem__` → **a**
5. `__getattr__` fires: a) On every access b) Only when normal lookup fails c) On writes d) On deletion → **b**
6. `a + b` where `a.__add__` returns `NotImplemented` then tries: a) `b.__add__(a)` b) `b.__radd__(a)` c) Nothing d) `a.__iadd__(b)` → **b**
7. A class with `__iter__` and `__next__` is: a) An iterator b) A context manager c) An ABC d) A descriptor → **a**
8. `bool(x)` with no `__bool__` uses: a) Always True b) `__len__` (truthy if > 0) c) `__eq__` d) `__int__` → **b**
9. Which makes an object usable in `with`? a) `__enter__`/`__exit__` b) `__context__` c) `__with__` d) `__close__` → **a**
10. The MRO is computed at: a) Every method call b) Class creation (C3) c) Import of `super` d) First instantiation → **b**

## 20. Flashcards
- **Q: What is the MRO?** → **A:** The C3-linearized tuple of classes searched for attributes; e.g., `D(A,B)` → D,A,B,Base,object.
- **Q: What does `super()` do?** → **A:** Returns the next class after the current one in the instance's MRO (cooperative dispatch).
- **Q: What breaks a cooperative diamond?** → **A:** Calling a hard-coded parent (`Base.__init__()`) instead of `super()` → double-init.
- **Q: What does defining `__eq__` do to `__hash__`?** → **A:** Sets it to `None` → objects become unhashable.
- **Q: `__getattr__` vs `__getattribute__`?** → **A:** Fallback-on-miss vs every-access hook.
- **Q: How is `a + b` dispatched?** → **A:** `a.__add__(b)`, fallback `b.__radd__(a)`.
- **Q: What makes an object iterable/callable/context-manager?** → **A:** `__iter__`/`__getitem__`, `__call__`, `__enter__`/`__exit__`.
- **Q: How do you get an immutable dataclass?** → **A:** `@dataclass(frozen=True)` (auto hash from fields).

## 21. Revision
Python resolves the diamond deterministically via the C3 MRO stored in `__mro__`: for `D(A, B)`, lookup order is `D → A → B → Base → object` (left-to-right local precedence, monotonic). `super()` is cooperative: it resolves to the *next* class in the instance's MRO after the current class, so `__init__` chains run each class exactly once — calling a parent directly instead breaks the diamond. Dunders are the protocol layer: `__add__`/`__radd__`/`__iadd__` for `+`, `__eq__` (+ `__hash__`!), `__len__`, `__contains__`, `__iter__`/`__next__` (or `__getitem__`), `__call__`, `__enter__`/`__exit__`, `__str__`/`__repr__`, `__getattr__`/`__setattr__`. Special-method lookup is on the type. `__eq__` without `__hash__` makes objects unhashable. Use `@dataclass(frozen=True)` for value objects and `abc.ABC`/`@abstractmethod` or `typing.Protocol` for contracts. In interviews: compute a diamond MRO by hand, explain cooperative `super()`, and list the dunders behind common syntax.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is the MRO and how is it computed?" | 2 / 8 Example / 9 Internal Working |
| "How does Python solve the diamond problem?" | 8 Example / 13 Interview |
| "How does `super()` work in multiple inheritance?" | 7 Formal Definition / 8 Example |
| "Why does `__eq__` break hashing?" | 9 Internal Working / 13 Interview |
| "What are dunder methods for operators?" | 7 Formal Definition / 13 Interview |
| "`__getattr__` vs `__getattribute__`?" | 13 Interview |
| "What is duck typing?" | 13 Interview |
| "ABC vs Protocol?" | 13 / 14 Follow-Up Questions |
| "How does `+` dispatch to `__radd__`?" | 13 Interview |
| "When is a class unhashable / how to make it hashable?" | 13 / 15 Coding |
