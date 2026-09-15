# Python MRO, Multiple Inheritance and Dataclasses — 100 Interview Q&A

## Q1: What is the Method Resolution Order (MRO) in Python?

**A:** The Method Resolution Order (MRO) is the order in which Python searches for a method in a class hierarchy. When a method is called on an object, Python looks for it first in the instance, then in the class, then in each base class following a specific linear order. This linear order is the MRO. You can inspect a class's MRO using `cls.__mro__` or `type(cls).mro()`. The MRO ensures that method lookup is consistent, predictable, and follows a sensible ordering even in complex multiple inheritance hierarchies.

The MRO is computed using the C3 linearization algorithm (discussed in detail in later questions). Before Python 2.3, Python used a simple left-to-right depth-first search that could produce inconsistent results. The C3 linearization was adopted to fix these inconsistencies, ensuring that a class always appears before its bases in the MRO and that the order is stable across different class definitions. The MRO is computed once when a class is defined and cached, so there is no runtime overhead for method resolution.

The practical implication is that the MRO determines which version of a method is called when multiple base classes define the same method. For example, in `class C(B, A): pass`, the MRO is `C -> B -> A -> object`, so `B`'s methods take precedence over `A`'s. Understanding MRO is essential for debugging method resolution issues in multiple inheritance and for designing cooperative class hierarchies.

**Example:**
```python
class A:
    def greet(self):
        return "A"

class B(A):
    def greet(self):
        return "B"

class C(B, A):
    pass

print(C.__mro__)
# (<class 'C'>, <class 'B'>, <class 'A'>, <class 'object'>)

c = C()
print(c.greet())  # "B" — B comes before A in MRO
```

## Q2: How is the MRO computed in Python?

**A:** Python computes the MRO using the C3 linearization algorithm. The algorithm takes the class and its direct bases as input and produces a linear ordering that satisfies three constraints: (1) Children precede parents in the ordering. (2) If a class appears in multiple base classes' MROs, it preserves the left-to-right order of the bases. (3) The ordering respects the monotonicity constraint — if a class precedes another in one base's MRO, it precedes it in the final MRO.

The C3 algorithm works by merging the MROs of all base classes while maintaining the constraints. It starts with a list of candidate classes (the class itself and its bases) and iteratively selects a class that does not appear in the tail of any other candidate list. A class is selected if it is at the head of some candidate list and is not in the tail (all elements after the head) of any other candidate list. This process repeats until all classes are placed in the linear order.

The algorithm can be expressed as: `L[C(B1, B2, ..., BN)] = C + merge(L[B1], L[B2], ..., L[BN], B1, B2, ..., BN)` where `merge` combines the lists while respecting the constraints. If the algorithm cannot find a valid ordering (due to inconsistent constraints), Python raises a `TypeError` with the message "Cannot create a consistent method resolution order (MRO)." This typically happens with pathological diamond inheritance patterns where the constraints are contradictory.

**Example:**
```python
class A:
    pass

class B(A):
    pass

class C(A):
    pass

class D(B, C):
    pass

print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
```

## Q3: What is cooperative multiple inheritance in Python?

**A:** Cooperative multiple inheritance is a design pattern where classes in a hierarchy use `super()` to delegate method calls to the next class in the MRO, forming a chain of responsibility. Instead of each class handling a method independently, each class performs its part of the work and then calls `super()` to pass control to the next class. This pattern is particularly useful with Python's MRO, which provides a predictable linear ordering for the delegation chain.

The key principle is that every class in the cooperative hierarchy must call `super()` in its methods to pass control to the next class. If any class fails to call `super()`, the chain is broken, and subsequent classes in the MRO never get a chance to execute. This is both the strength and the weakness of the pattern: it ensures that all classes contribute to the method's behavior, but a single missing `super()` call breaks the entire chain.

Cooperative multiple inheritance is commonly used with mixins, abstract base classes, and framework code. For example, a logging mixin, a caching mixin, and a validation mixin can each add their behavior to a method by calling `super()` at the end (or beginning) of their implementation. The MRO ensures they are called in the correct order. The pattern requires careful design: all classes must have compatible method signatures (using `*args` and `**kwargs` for flexibility), and each class must know what it contributes and delegate the rest.

**Example:**
```python
class Logger:
    def process(self, *args, **kwargs):
        print("Logging")
        return super().process(*args, **kwargs)

class Validator:
    def process(self, *args, **kwargs):
        print("Validating")
        return super().process(*args, **kwargs)

class Processor:
    def process(self, *args, **kwargs):
        print("Processing")
        return "done"

class Service(Logger, Validator, Processor):
    pass

s = Service()
s.process()
# Output: Logging -> Validating -> Processing
```

## Q4: What is the diamond problem, and how does Python handle it?

**A:** The diamond problem occurs in multiple inheritance when a class inherits from two classes that both inherit from a common base class, forming a diamond shape in the inheritance hierarchy. For example: `class D(B, C)` where both `B` and `C` inherit from `A`. The problem is: which version of `A`'s methods should `D` inherit — `B`'s version or `C`'s version? Without proper handling, `D` might inherit `A`'s methods twice, leading to duplication, inconsistency, or undefined behavior.

Python handles the diamond problem through the C3 linearization algorithm, which computes a single linear MRO that includes `A` exactly once. In the example `class D(B, C)` where `B(A)` and `C(A)`, the MRO is `D -> B -> C -> A -> object`. This ensures that `A`'s methods are inherited exactly once, and the order is deterministic. The `object` base class always appears last in the MRO. The C3 algorithm resolves the diamond by prioritizing the leftmost base class's MRO while ensuring that all constraints are satisfied.

The practical benefit is that Python's MRO eliminates the diamond problem entirely: there is exactly one path to each ancestor, and the path is deterministic. In languages like C++, the diamond problem can lead to ambiguity errors (which `A` does `D` refer to?) that require explicit virtual inheritance to resolve. Python avoids this by computing a single linear ordering that includes each class exactly once. This makes Python's multiple inheritance more flexible and predictable than C++'s, though it requires understanding the MRO to predict method resolution correctly.

**Example:**
```python
class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B"

class C(A):
    def method(self):
        return "C"

class D(B, C):
    pass

print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
# A is included exactly once — no diamond problem

d = D()
print(d.method())  # "B" — B's method is found first in MRO
```

## Q5: How does `super()` work in Python 3?

**A:** In Python 3, `super()` without arguments is equivalent to `super(CurrentClass, self)` (or `super(CurrentClass, cls)` in class methods). It returns a proxy object that delegates method calls to the next class in the MRO (the "cooperative superclass"). The `super()` call is bound to the current class and the current instance (or class), and it uses the MRO to determine which class to call next. This is a significant improvement over Python 2, where you had to explicitly pass the class and instance: `super(CurrentClass, self).__init__()`.

The mechanism behind `super()` is that Python stores the current class and instance in implicit parameters (`__class__` and the first argument of the method). When you call `super()`, Python uses these implicit parameters to create a bound method proxy that, when called, searches the MRO starting from the class after the current class in the MRO. For example, if `C.__mro__` is `(C, B, A, object)` and `super()` is called inside `B.__init__`, it will call `A.__init__`.

The practical implication is that `super()` must be called in every class in the cooperative hierarchy to maintain the chain. If `B.__init__` does not call `super().__init__()`, `A.__init__` is never called, even though `A` is in the MRO. The chain is only as complete as the least cooperative class. This design encourages consistent use of `super()` throughout the hierarchy and makes the delegation pattern explicit. Each class handles its part and delegates the rest via `super()`.

**Example:**
```python
class A:
    def __init__(self):
        print("A.__init__")

class B(A):
    def __init__(self):
        print("B.__init__")
        super().__init__()

class C(B):
    def __init__(self):
        print("C.__init__")
        super().__init__()

c = C()
# Output: C.__init__ -> B.__init__ -> A.__init__
```

## Q6: What is `__mro__` and how does it relate to method resolution?

**A:** `__mro__` is a class attribute that returns a tuple of classes representing the linear Method Resolution Order for that class. When a method is called on an instance, Python searches for the method in the classes listed in `__mro__`, in order, starting from the instance's class. The first class in the `__mro__` tuple that defines the method is used. The `__mro__` tuple always ends with `object` and always starts with the class itself.

The `__mro__` is computed by the C3 linearization algorithm when the class is defined. It is cached as a class attribute and is accessible via `cls.__mro__` or `type(cls).mro()`. The `mro()` method returns a list (which can be subclassed), while `__mro__` returns a tuple. Both contain the same classes in the same order. The `__mro__` is used internally by Python for method resolution, and it is also useful for debugging and understanding class hierarchies.

The practical application is that you can inspect the MRO to predict which method will be called in a multiple inheritance scenario. For debugging, you can check `cls.__mro__` to understand the class hierarchy. For design, you can use the MRO to ensure that your classes are in the correct order for cooperative inheritance. The `__mro__` is the definitive answer to "which class's method will be called?" — it lists all classes in the exact order that Python searches for methods.

**Example:**
```python
class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B"

class C(A):
    pass

class D(B, C):
    pass

print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)

# Method resolution order for method calls:
# D -> B -> C -> A -> object
```

## Q7: What happens when `super()` is called incorrectly in a diamond hierarchy?

**A:** When `super()` is called incorrectly in a diamond hierarchy (e.g., some classes call `super()` and others don't), the delegation chain is broken. Classes that are "skipped" by the missing `super()` call never get a chance to execute their methods. For example, if `B.__init__` does not call `super().__init__()`, then `A.__init__` (which comes after `B` in the MRO) is never called. This is the most common error in cooperative multiple inheritance: a single missing `super()` call breaks the chain.

The consequence is subtle: the class that fails to call `super()` appears to work correctly in isolation, but when used in a multiple inheritance hierarchy, it silently prevents other classes from executing. This is a silent bug — no error is raised, but the expected behavior is absent. The fix is to ensure that every class in the cooperative hierarchy calls `super()` in every method that participates in the chain. This includes `__init__`, `__str__`, `__repr__`, and any other methods that are part of the cooperative pattern.

The practical recommendation is to adopt a coding convention: every method in a cooperative class should end with `return super().method(*args, **kwargs)` (or start with it, depending on the desired ordering). Using `*args` and `**kwargs` ensures that the method signature is compatible with all classes in the hierarchy, even if they have different parameter requirements. The `super()` chain should be documented as part of the class's contract, and breaking it should be considered a bug.

**Example:**
```python
class A:
    def __init__(self):
        print("A.__init__")

class B(A):
    def __init__(self):
        print("B.__init__")
        # Missing super().__init__() — BUG!

class C(A):
    def __init__(self):
        print("C.__init__")
        super().__init__()

class D(B, C):
    def __init__(self):
        print("D.__init__")
        super().__init__()

d = D()
# Output: D.__init__ -> B.__init__ (C and A are skipped!)
```

## Q8: What are mixins, and how do they relate to multiple inheritance?

**A:** Mixins are classes that provide a set of methods or behaviors intended to be combined with other classes through multiple inheritance. A mixin is not designed to stand alone — it is designed to "mix in" functionality to a class that already has a primary inheritance chain. Mixins typically do not define `__init__` (or if they do, they call `super().__init__()`), and they provide specific, focused functionality (logging, caching, serialization, etc.).

The relationship to multiple inheritance is that mixins leverage Python's MRO and cooperative multiple inheritance to add behavior without disturbing the primary inheritance chain. A class can inherit from multiple mixins and a primary base class: `class MyClass(MixinA, MixinB, BaseClass)`. The MRO ensures that the mixins are called in the correct order, and `super()` ensures that each mixin delegates to the next. This pattern is common in frameworks (Django, Flask, SQLAlchemy) and libraries that need to compose behavior from multiple sources.

The design principles for mixins are: (1) Keep mixins focused — each mixin should provide one specific behavior. (2) Avoid state in mixins — mixins should not define `__init__` that stores state (or if they do, use cooperative `super()`). (3) Use cooperative `super()` — mixins should call `super()` to allow other mixins and the base class to execute. (4) Document the expected position in the MRO — some mixins must come before others. (5) Make mixins optional — a class should work correctly with or without a mixin. These principles ensure that mixins are composable, reusable, and predictable in multiple inheritance hierarchies.

**Example:**
```python
class JsonMixin:
    def to_json(self):
        import json
        return json.dumps(self.__dict__)

class LoggingMixin:
    def log(self, message):
        print(f"[{self.__class__.__name__}] {message}")

class BaseModel:
    def __init__(self, name):
        self.name = name

class UserModel(JsonMixin, LoggingMixin, BaseModel):
    def __init__(self, name, email):
        super().__init__(name)
        self.email = email

u = UserModel("Alice", "alice@example.com")
print(u.to_json())   # {"name": "Alice", "email": "alice@example.com"}
u.log("created")      # [UserModel] created
```

## Q9: What is the difference between `super()` and explicit base class calls?

**A:** `super()` delegates to the next class in the MRO, which may or may not be the direct parent. Explicit base class calls (e.g., `BaseClass.method(self)`) bypass the MRO and call the specified class's method directly. The key difference is that `super()` follows the MRO and can call a class that is not a direct parent (e.g., a class that appears later in the MRO due to multiple inheritance), while explicit calls always call the named class.

The practical implication is that `super()` is correct for cooperative multiple inheritance, while explicit calls are correct for simple single inheritance or when you specifically want to call a particular class's method. For example, `BaseClass.__init__(self)` calls `BaseClass.__init__` regardless of the MRO, while `super().__init__()` calls the next class in the MRO. In a diamond hierarchy, `super()` ensures that each class is called exactly once in the correct order, while explicit calls can lead to a class being called multiple times or not at all.

The recommendation is to use `super()` in cooperative multiple inheritance and explicit calls in simple inheritance. The `super()` pattern is more maintainable because it automatically adjusts to changes in the class hierarchy. If a new class is inserted into the MRO, `super()` automatically includes it, while explicit calls must be updated manually. However, explicit calls are sometimes necessary when you need to call a specific class's method regardless of the MRO (e.g., calling `object.__init__` explicitly).

**Example:**
```python
class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        # Delegates to next in MRO (could be C, not A)
        return "B -> " + super().method()

class C(A):
    def method(self):
        return "C"

class D(B, C):
    def method(self):
        return "D -> " + super().method()

print(D().method())  # "D -> B -> C -> A"
# super() in B goes to C (next in MRO), not A
```

## Q10: What are the limitations of multiple inheritance in Python?

**A:** Multiple inheritance in Python, while powerful, has several limitations. (1) Complexity: the class hierarchy can become difficult to understand, especially with deep or wide inheritance trees. The MRO can be non-intuitive, and predicting which method is called requires understanding the C3 linearization algorithm. (2) Fragile base class problem: changes in a base class can unexpectedly affect derived classes, especially in cooperative hierarchies where `super()` chains are used. (3) Name conflicts: if two base classes define the same attribute, the MRO determines which one is used, which may not be what the programmer intended.

(4) Performance overhead: method lookup in multiple inheritance involves traversing the MRO, which is O(N) in the number of classes. This is typically negligible but can matter in performance-critical code. (5) Difficulty with `__init__`: if any class in the hierarchy fails to call `super().__init__()`, the chain is broken and some base classes are never initialized. This is a common source of bugs. (6) Testing complexity: testing classes with multiple inheritance requires testing all combinations of base classes, which can be exponential in the number of mixins.

(7) Reduced readability: multiple inheritance makes code harder to read because the behavior of a method depends on the MRO, which is not always obvious from the class definition. (8) Difficulty with type checking: `isinstance()` checks work correctly with multiple inheritance, but `type()` checks may not reflect the full hierarchy. The practical recommendation is to prefer composition over multiple inheritance when possible, and use multiple inheritance only for mixins and well-understood patterns (like the cooperative inheritance pattern with `super()`).

**Example:**
```python
class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B"

class C(A):
    def method(self):
        return "C"

class D(B, C):
    pass

# Name conflict: both B and C define method
# MRO determines which is called
print(D().method())  # "B" — B comes first in MRO

# Fragile base class: if B's method changes behavior,
# D's behavior changes too — even if D didn't change
```

## Q11: What is `__init_subclass__` and how does it interact with MRO?

**A:** `__init_subclass__` is a class method that is called when a class is subclassed. It is defined in the base class and is automatically called by the derived class's metaclass after the derived class is created. The method receives the derived class as an argument and can perform setup, validation, or registration. It is called after the MRO has been computed, so the derived class's `__mro__` is available during `__init_subclass__` execution.

The interaction with MRO is that `__init_subclass__` is called for every class in the hierarchy, not just the direct subclass. When `class D(B, C)` is defined, `__init_subclass__` is called on `B` and `C` (and any other class in the hierarchy that defines it). The MRO determines the order in which `__init_subclass__` methods are called: the most derived class first, then its bases in MRO order. This is consistent with the cooperative inheritance pattern.

The practical application is in framework design: `__init_subclass__` can register classes, validate constraints, or modify class attributes without requiring metaclasses. For example, a base class can define `__init_subclass__` to register all subclasses in a registry: `class PluginBase: _registry = {}; def __init_subclass__(cls, **kwargs): super().__init_subclass__(**kwargs); PluginBase._registry[cls.__name__] = cls`. This is cleaner than metaclasses for many use cases and works correctly with multiple inheritance because the MRO ensures the correct call order.

**Example:**
```python
class PluginBase:
    _registry = {}
    
    def __init_subclass__(cls, plugin_name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        name = plugin_name or cls.__name__
        PluginBase._registry[name] = cls

class PluginA(PluginBase, plugin_name="alpha"):
    pass

class PluginB(PluginBase, plugin_name="beta"):
    pass

print(PluginBase._registry)
# {'alpha': <class 'PluginA'>, 'beta': <class 'PluginB'>}
```

## Q12: How does Python resolve method conflicts when two base classes define the same method?

**A:** When two base classes define the same method and a derived class inherits from both, Python uses the MRO to determine which method is called. The MRO is a linear ordering of all classes in the hierarchy, and the first class in the MRO that defines the method is used. The MRO is computed by the C3 linearization algorithm, which prioritizes the leftmost base class in the class definition. For `class D(B, C)`, `B`'s MRO comes before `C`'s MRO, so `B`'s methods take precedence.

The practical example: `class D(B, C)` where `B.method` and `C.method` both exist. The MRO is `D -> B -> C -> A -> object`. When `D().method()` is called, Python searches the MRO and finds `B.method` first. `C.method` is never called (unless `B.method` delegates to it via `super()`). This is the expected behavior for left-to-right inheritance. If the programmer wants `C.method` to be called, they must either change the inheritance order to `class D(C, B)` or have `B.method` call `super().method()` (cooperative inheritance).

The resolution is deterministic and predictable: the MRO is computed at class definition time and is the same every time. There is no runtime ambiguity — Python always knows which method to call. The programmer can inspect `cls.__mro__` to predict the resolution. The key insight is that multiple inheritance in Python does not create ambiguity — it creates a deterministic ordering. The MRO is the definitive answer to "which method is called?" and it is always consistent.

**Example:**
```python
class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B"

class C(A):
    def method(self):
        return "C"

class D(B, C):
    pass

print(D().method())  # "B" — B comes before C in MRO

class E(C, B):
    pass

print(E().method())  # "C" — C comes before B in MRO
```

## Q13: What is the role of `object.__init_subclass__` in Python 3?

**A:** `object.__init_subclass__` is the base implementation of `__init_subclass__` in `object`, the root of all Python classes. It is called when any class is subclassed (after the MRO is computed). The base implementation does nothing — it is a hook that derived classes can override to perform actions when their subclasses are created. Since `object` is the ultimate base class of all classes, its `__init_subclass__` is always called (via `super().__init_subclass__()` in derived classes).

The practical role is as a hook for framework and library designers. By overriding `__init_subclass__`, a base class can automatically register, validate, or modify its subclasses. The base `object.__init_subclass__` ensures that the hook is called consistently across the hierarchy. When a derived class calls `super().__init_subclass__(**kwargs)`, the call propagates up the MRO to `object.__init_subclass__`, which does nothing. This is the cooperative inheritance pattern — each class in the hierarchy does its part and delegates to the next via `super()`.

The interaction with MRO is that `__init_subclass__` calls propagate through the MRO. If `class D(B, C)` is defined, `D.__init_subclass__` is called (if defined), then `B.__init_subclass__`, then `C.__init_subclass__`, then `A.__init_subclass__`, then `object.__init_subclass__`. Each class can perform its setup and then call `super().__init_subclass__(**kwargs)` to continue the chain. This is consistent with the cooperative inheritance pattern and ensures that all classes in the hierarchy are notified of the subclass creation.

**Example:**
```python
class AutoRegister:
    _subclasses = []
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        AutoRegister._subclasses.append(cls.__name__)

class ChildA(AutoRegister):
    pass

class ChildB(AutoRegister):
    pass

class GrandChild(ChildA):
    pass

print(AutoRegister._subclasses)
# ['ChildA', 'ChildB', 'GrandChild']
```

## Q14: What are the differences between `super()` in Python 2 and Python 3?

**A:** In Python 2, `super()` requires explicit arguments: `super(CurrentClass, self).__init__()`. The `CurrentClass` and `self` (or `cls` for class methods) are mandatory. This is verbose and error-prone: if the class name is wrong or the instance is wrong, the `super()` call delegates to the wrong class or raises an error. The explicit arguments also make refactoring harder — if the class is renamed, all `super()` calls must be updated.

In Python 3, `super()` without arguments is equivalent to `super(CurrentClass, self)`. The class and instance are automatically determined from the enclosing scope. This is less verbose, less error-prone, and easier to refactor. The automatic argument binding uses implicit `__class__` (a closure variable referencing the current class) and the first argument of the method (the instance). This makes `super()` calls consistent and correct by construction.

The practical impact is significant: Python 3's `super()` eliminates the most common errors in cooperative multiple inheritance. The implicit arguments ensure that `super()` always delegates to the correct next class in the MRO. The verbosity reduction makes cooperative inheritance more practical — you can write `super().__init__()` instead of `super(ClassName, self).__init__()`. The recommendation is to always use Python 3's `super()` without arguments in cooperative hierarchies. If you need to call a specific class's method (not the next in MRO), use explicit base class calls: `BaseClass.method(self)`.

**Example:**
```python
# Python 2 style (verbose, error-prone):
class B(A):
    def __init__(self):
        super(B, self).__init__()  # Must specify B and self

# Python 3 style (concise, correct):
class B(A):
    def __init__(self):
        super().__init__()  # Automatic class and instance
```

## Q15: What is a dataclass in Python and how is it defined?

**A:** A dataclass is a Python class decorated with `@dataclass` that automatically generates special methods based on the class's field definitions. The `@dataclass` decorator (from the `dataclasses` module, introduced in Python 3.7) generates `__init__`, `__repr__`, `__eq__`, and optionally `__hash__`, `__lt__`, `__le__`, `__gt__`, `__ge__` methods. It reduces boilerplate for classes that primarily store data. The decorator inspects the class's type annotations and generates methods that initialize, represent, and compare the data.

The basic usage: `@dataclass class Point: x: float; y: float`. This generates an `__init__` that accepts `x` and `y` as arguments, a `__repr__` that shows `Point(x=..., y=...)`, and an `__eq__` that compares `x` and `y`. The decorator does not generate `__hash__` by default if `eq=True` (the default), because mutable objects should not be hashable. To make a dataclass hashable, set `eq=True, frozen=True` or `eq=True, unsafe_hash=True`.

The practical benefit is significant: a dataclass replaces 10-20 lines of boilerplate (`__init__`, `__repr__`, `__eq__`) with a single decorator. Dataclasses support default values, field metadata, inheritance, and post-init processing. They are not limited to simple data containers — they can have methods, properties, and custom behavior. The `@dataclass` decorator is a metaprogramming tool that generates code at class definition time, making it efficient and transparent. Dataclasses are widely used in modern Python for DTOs, configuration objects, and value types.

**Example:**
```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

p = Point(3.0, 4.0)
print(p)        # Point(x=3.0, y=4.0)
print(p == Point(3.0, 4.0))  # True
```

## Q16: What are the key parameters of the `@dataclass` decorator?

**A:** The `@dataclass` decorator accepts several parameters that control the generated methods: `init` (default `True`): generates `__init__`. `repr` (default `True`): generates `__repr__`. `eq` (default `True`): generates `__eq__`. `order` (default `False`): generates comparison methods (`__lt__`, `__le__`, `__gt__`, `__ge__`). `unsafe_hash` (default `False`): generates `__hash__` even if `eq=True`. `frozen` (default `False`): makes instances immutable (sets `__setattr__` and `__delattr__` to raise `FrozenInstanceError`).

The `frozen` parameter is particularly important for data integrity. A frozen dataclass cannot be modified after creation: `@dataclass(frozen=True) class Config: debug: bool; port: int`. Attempting to set an attribute raises `FrozenInstanceError`. This makes frozen dataclasses suitable as dictionary keys (when `eq=True`) and for use in concurrent code (no mutation after creation). The `order` parameter enables sorting: `@dataclass(order=True) class Event: timestamp: float; name: str`. This generates `__lt__` etc. based on the field order.

The `field()` function provides per-field customization: `field(default_factory=list, repr=False, compare=False)`. The `default_factory` parameter specifies a callable for mutable default values (avoiding the shared mutable default problem). The `repr` and `compare` parameters control whether the field is included in `__repr__` and `__eq__`/`__lt__`. The `metadata` parameter stores arbitrary data (for serialization frameworks, documentation, etc.). These parameters make dataclasses flexible enough for a wide range of use cases beyond simple data containers.

**Example:**
```python
from dataclasses import dataclass, field

@dataclass(frozen=True, order=True)
class Event:
    timestamp: float
    name: str
    data: dict = field(default_factory=dict, repr=False, compare=False)

e1 = Event(1.0, "start")
e2 = Event(2.0, "end")
print(e1 < e2)  # True — order is based on timestamp, then name
```

## Q17: How do dataclasses handle inheritance?

**A:** Dataclasses support inheritance in a straightforward manner: the generated `__init__` includes fields from both the parent and child classes. The child class's `__init__` calls the parent class's `__init__` automatically. Field order is: parent fields first (in their original order), then child fields. Default values in the child class can override parent defaults, but a child field without a default cannot follow a parent field with a default (same rule as function parameters).

The practical example: `@dataclass class Base: x: int = 0; y: int = 0` and `@dataclass class Child(Base): z: int = 0`. The generated `__init__` is `Child(x=0, y=0, z=0)`. The `__repr__` includes all fields: `Child(x=0, y=0, z=0)`. The `__eq__` compares all fields. Inheritance with dataclasses is simpler than with regular classes because the generated methods are deterministic and predictable.

The limitation is that `__hash__` is not generated by default for dataclasses with `eq=True` (to prevent inconsistency between `__eq__` and `__hash__`). If you need hashing, use `frozen=True` or `unsafe_hash=True`. Another limitation is that `__post_init__` (discussed later) is called for each class in the hierarchy, which can lead to unexpected behavior if not carefully managed. The recommendation is to keep dataclass hierarchies shallow and flat, and to use composition over inheritance when possible.

**Example:**
```python
from dataclasses import dataclass

@dataclass
class Animal:
    name: str
    species: str

@dataclass
class Pet(Animal):
    owner: str
    vaccinated: bool = True

p = Pet("Buddy", "dog", "Alice")
print(p)  # Pet(name='Buddy', species='dog', owner='Alice', vaccinated=True)
```

## Q18: What is `__post_init__` in dataclasses and when should it be used?

**A:** `__post_init__` is a special method that is called after the dataclass's `__init__` method. It is generated by the `@dataclass` decorator and is called at the end of `__init__`, after all fields have been assigned. The purpose is to perform post-initialization validation, computation, or transformation that depends on the field values. For example, validating that a field's value is within a certain range, computing derived fields, or converting types.

The practical use case is when a field's value cannot be determined from the constructor arguments alone. For example, a dataclass with a `full_name` field that is computed from `first_name` and `last_name`: `@dataclass class User: first_name: str; last_name: str; full_name: str = field(init=False); def __post_init__(self): self.full_name = f"{self.first_name} {self.last_name}"`. The `init=False` parameter tells the dataclass not to include `full_name` in `__init__`, and `__post_init__` computes it.

The interaction with inheritance: `__post_init__` is called for each class in the hierarchy. If the parent class defines `__post_init__`, it is called first (via `super().__post_init__()`), then the child's `__post_init__`. This is consistent with the cooperative inheritance pattern. The practical recommendation is to use `__post_init__` for validation and computed fields, and to keep it simple (no side effects, no I/O). For complex initialization, consider factory methods or custom `__init__` methods instead.

**Example:**
```python
from dataclasses import dataclass, field

@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)
    
    def __post_init__(self):
        self.area = self.width * self.height

r = Rectangle(3.0, 4.0)
print(r.area)  # 12.0
```

## Q19: What is the `field()` function in dataclasses?

**A:** The `field()` function is used to customize individual fields in a dataclass. It returns a `Field` object that stores metadata about the field, including its default value, default factory, repr flag, compare flag, hash flag, init flag, and metadata. The `field()` function is necessary when you need to specify options that cannot be set through simple type annotation (like default values for mutable objects, or excluding fields from `__repr__`).

The key parameters of `field()` are: `default`: the default value for the field (mutually exclusive with `default_factory`). `default_factory`: a callable that returns the default value (for mutable defaults like `list`, `dict`, `set`). `repr`: whether to include the field in `__repr__` (default `True`). `compare`: whether to include the field in `__eq__` and ordering methods (default `True`). `hash`: whether to include the field in `__hash__` (default `None`, which means use `compare`). `init`: whether to include the field in `__init__` (default `True`). `metadata`: a mapping of arbitrary data.

The practical importance of `default_factory`: without it, mutable defaults are shared across instances (the classic Python gotcha). `@dataclass class C: items: list = field(default_factory=list)` creates a new list for each instance. `@dataclass class C: items: list = []` shares the same list across all instances — a bug. The `default_factory` parameter solves this problem by calling the factory function for each new instance. The `field()` function is essential for correct dataclass design, especially for fields with mutable defaults, fields that should be excluded from comparison/repr, and fields that are computed (not passed to `__init__`).

**Example:**
```python
from dataclasses import dataclass, field

@dataclass
class Config:
    name: str
    tags: list = field(default_factory=list, repr=False)
    debug: bool = field(default=False, compare=False)
    _internal: str = field(init=False, default="secret")

c = Config("app")
print(c)  # Config(name='app', debug=False, _internal='secret')
# tags is not shown in repr (repr=False)
# debug is not included in equality check (compare=False)
```

## Q20: How do dataclasses differ from regular classes with `__init__`?

**A:** Dataclasses and regular classes with `__init__` achieve the same result (storing data in instance attributes), but dataclasses automate the boilerplate. A regular class requires writing `__init__`, `__repr__`, `__eq__`, and potentially `__hash__`, `__lt__`, etc. A dataclass generates all of these from the field definitions. The generated methods are consistent and follow best practices (e.g., using `default_factory` for mutable defaults, proper `__repr__` formatting).

The practical differences: (1) Dataclasses generate `__init__` with keyword-only or positional-or-keyword arguments based on field order. (2) Dataclasses generate `__repr__` with a consistent format: `ClassName(field1=..., field2=...)`. (3) Dataclasses generate `__eq__` that compares all fields (or only fields with `compare=True`). (4) Dataclasses support `frozen=True` for immutable instances. (5) Dataclasses support `order=True` for comparison methods. (6) Dataclasses support `__post_init__` for post-initialization logic.

The recommendation is to use dataclasses for classes that primarily store data (DTOs, configuration objects, value types, records). Use regular classes for classes with complex behavior (methods that do I/O, complex initialization logic, state machines). Dataclasses are not a replacement for all classes — they are a specialized tool for data-centric classes. The `@dataclass` decorator is a metaprogramming tool that generates code at class definition time, making it efficient and transparent. The generated code is equivalent to hand-written code — there is no runtime overhead.

**Example:**
```python
# Regular class — verbose
class PointRegular:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"PointRegular(x={self.x}, y={self.y})"
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

# Dataclass — concise
from dataclasses import dataclass
@dataclass
class PointDataclass:
    x: float
    y: float
# __init__, __repr__, __eq__ are auto-generated
```

## Q21: What is the relationship between `__slots__` and dataclasses?

**A:** `__slots__` is a class attribute that restricts the instance attributes to a fixed set of names, preventing the creation of `__dict__`. This reduces memory usage (no per-instance dictionary) and slightly improves attribute access speed. When combined with dataclasses, you set `@dataclass(slots=True)` (Python 3.10+) or define `__slots__` manually. The `slots=True` parameter generates `__slots__` from the field names, combining the memory efficiency of `__slots__` with the convenience of dataclasses.

The practical benefit is significant for dataclasses with many instances: a dataclass with 10 fields and `__slots__` uses roughly 40% less memory than one without (because the `__dict__` is eliminated). For applications that create millions of dataclass instances (like database records, log entries, or scientific data), this memory savings is critical. The `slots=True` parameter was introduced in Python 3.10 because earlier versions had difficulty combining `__slots__` with generated `__init__` methods.

The limitations of `__slots__` with dataclasses: (1) You cannot add attributes not defined in `__slots__` after instance creation. (2) Multiple inheritance with `__slots__` requires careful coordination (each class must define `__slots__` without overlapping names). (3) Classes with `__slots__` cannot have `__dict__` (unless `'__dict__'` is in `__slots__`). (4) `__weakref__` must be explicitly included in `__slots__` if weak references are needed. These limitations are the same as for regular `__slots__` classes and apply to dataclasses with `slots=True`.

**Example:**
```python
from dataclasses import dataclass

@dataclass(slots=True)
class Point:
    x: float
    y: float

p = Point(1.0, 2.0)
print(hasattr(p, '__dict__'))  # False — no __dict__
# p.z = 3.0  # AttributeError: 'Point' object has no attribute 'z'
```

## Q22: How do dataclasses handle mutable default values?

**A:** Dataclasses handle mutable default values through the `default_factory` parameter of the `field()` function. Without `default_factory`, a mutable default value (like `list`, `dict`, `set`) would be shared across all instances — the classic Python mutable default argument bug. The `@dataclass` decorator detects this and raises a `ValueError` if you try to use a mutable default directly: `@dataclass class C: items: list = []` raises an error. Instead, you must use `field(default_factory=list)`.

The `default_factory` parameter accepts a callable (typically a constructor like `list`, `dict`, `set`, or a lambda/function). Each time a new instance is created, the callable is called to produce a fresh default value. This ensures that each instance gets its own independent copy of the mutable default. The `field()` function is the only way to specify mutable defaults in dataclasses, and the `@dataclass` decorator enforces this constraint.

The practical importance is that dataclasses prevent the most common Python bug (shared mutable defaults) at definition time. If you accidentally write `items: list = []`, you get a clear error message instead of a subtle bug that appears only when multiple instances are created. The `default_factory` pattern is: `items: list = field(default_factory=list)`, `config: dict = field(default_factory=dict)`, `tags: set = field(default_factory=set)`. For more complex defaults, use a lambda or function: `data: list = field(default_factory=lambda: [1, 2, 3])`.

**Example:**
```python
from dataclasses import dataclass, field

@dataclass
class Server:
    name: str
    tags: list = field(default_factory=list)
    config: dict = field(default_factory=dict)

s1 = Server("web")
s2 = Server("db")
s1.tags.append("production")
print(s1.tags)  # ['production']
print(s2.tags)  # [] — independent list
```

## Q23: What is `dataclasses.asdict` and when should it be used?

**A:** `dataclasses.asdict(dataclass_instance)` recursively converts a dataclass instance to a dictionary. It converts each field to a key-value pair, where the key is the field name and the value is the field's value. Nested dataclasses are also converted to dictionaries recursively. This is useful for serialization (JSON, YAML, Pickle), interop with non-Python systems, and debugging.

The practical usage: `from dataclasses import asdict; d = asdict(Point(1.0, 2.0))` produces `{'x': 1.0, 'y: 2.0'}`. For nested dataclasses: `@dataclass class Address: city: str; @dataclass class User: name: str; address: Address`. `asdict(User("Alice", Address("NYC")))` produces `{'name': 'Alice', 'address': {'city': 'NYC'}}`. The recursive conversion makes it easy to serialize complex dataclass hierarchies.

The `asdict` function accepts optional parameters: `dict_factory` (a callable to create the dictionary, default `dict`), `filter` (a function to filter fields), and `meta` (a function to transform field metadata). The `filter` parameter is useful for excluding sensitive or internal fields: `asdict(user, filter=lambda k, v: k != 'password')`. The `dict_factory` parameter enables custom dictionary types (e.g., `OrderedDict` for ordered output). The `asdict` function is the standard way to convert dataclasses to dictionaries and is widely used in serialization libraries.

**Example:**
```python
from dataclasses import dataclass, asdict

@dataclass
class Address:
    city: str
    country: str

@dataclass
class User:
    name: str
    age: int
    address: Address

u = User("Alice", 30, Address("NYC", "USA"))
d = asdict(u)
print(d)
# {'name': 'Alice', 'age': 30, 'address': {'city': 'NYC', 'country': 'USA'}}
```

## Q24: What is `dataclasses.fields` and `dataclasses.astuple`?

**A:** `dataclasses.fields(dataclass_instance)` returns a tuple of `Field` objects for the dataclass, one per field. Each `Field` object contains metadata about the field: name, type, default, default_factory, repr, compare, hash, init, and metadata. This is useful for introspection: iterating over fields, checking field properties, or building custom serializers. `dataclasses.astuple(dataclass_instance)` converts a dataclass instance to a tuple of field values, in field order. Nested dataclasses are also converted to tuples recursively.

The practical usage of `fields()`: `for f in fields(point): print(f.name, f.type)` prints each field's name and type. This is useful for building custom serializers, validators, or documentation generators. The `Field` objects are the same objects used in `field()` definitions, so they carry all the metadata specified during class definition. The `fields()` function is the standard way to introspect dataclass fields.

The practical usage of `astuple()`: `t = astuple(Point(1.0, 2.0))` produces `(1.0, 2.0)`. This is useful when you need a positional representation (e.g., for unpacking: `x, y = as_tuple(point)`). For nested dataclasses, `astuple` recursively converts to tuples: `astuple(User("Alice", 30, Address("NYC", "USA")))` produces `('Alice', 30, ('NYC', 'USA'))`. The `astuple` function is the tuple equivalent of `asdict` and is useful when you need ordered, immutable representations of dataclass instances.

**Example:**
```python
from dataclasses import dataclass, fields, astuple

@dataclass
class Point:
    x: float
    y: float
    label: str = "origin"

p = Point(3.0, 4.0)
for f in fields(p):
    print(f"{f.name}: {f.type} (default={f.default})")
# x: float (default=<dataclasses._MISSING_TYPE>)
# y: float (default=<dataclasses._MISSING_TYPE>)
# label: str (default=origin)

print(astuple(p))  # (3.0, 4.0, 'origin')
```

## Q25: How do properties differ from dataclass fields?

**A:** Properties and dataclass fields serve different purposes but can overlap. A dataclass field is a class variable with a type annotation that becomes an instance attribute, initialized by the generated `__init__`. A property is a descriptor that defines a managed attribute with custom getter, setter, and deleter methods. Dataclass fields are simple: they store data. Properties add computation, validation, or side effects to attribute access.

The key difference is that dataclass fields are attributes, while properties are descriptors. A dataclass field `x: int` creates an instance attribute `x` that stores an integer. A property `@property def x(self) -> int: return self._x` defines a method that is called when `x` is accessed. The property can compute its value, validate input, or trigger side effects. Dataclass fields cannot do this — they are just stored values.

The interaction is that you can use properties alongside dataclass fields. A dataclass can have properties that are not fields (they are not initialized by `__init__`). For example, `@dataclass class Circle: radius: float; @property def area(self) -> float: return 3.14159 * self.radius ** 2`. The `radius` is a field; `area` is a computed property. The `@dataclass` decorator ignores properties (they are not type-annotated class variables), so they work correctly alongside fields. Properties are used for computed attributes, validation, and lazy evaluation, while dataclass fields are used for stored data.

**Example:**
```python
from dataclasses import dataclass

@dataclass
class Circle:
    radius: float
    
    @property
    def area(self) -> float:
        return 3.14159 * self.radius ** 2
    
    @property
    def diameter(self) -> float:
        return self.radius * 2

c = Circle(5.0)
print(c.area)      # 78.53975 — computed property
print(c.diameter)  # 10.0 — computed property
# c.area = 100  # AttributeError: can't set attribute
```
## Q26: What is `dataclasses.KW_ONLY` and when should it be used?

**A:** `dataclasses.KW_ONLY` is a sentinel value (introduced in Python 3.10) that marks all subsequent fields as keyword-only in the generated `__init__`. Without `KW_ONLY`, all fields before the first field with a default value are positional-or-keyword, and fields after the first default are keyword-only (following Python's function parameter rules). `KW_ONLY` gives explicit control: fields declared after `KW_ONLY` are keyword-only regardless of their position or default status.

The practical usage: `@dataclass class User: name: str; age: int; __kw_only__ = True; email: str; phone: str = ""`. Here, `name` and `age` are positional-or-keyword (no defaults, so they are required positional-or-keyword). `email` and `phone` are keyword-only (declared after `KW_ONLY`). This is useful when you want to enforce keyword arguments for certain fields, improving readability at call sites: `User("Alice", 30, email="alice@example.com")` vs `User("Alice", 30, "alice@example.com")` — the keyword form is clearer.

The `KW_ONLY` sentinel can be placed anywhere in the field declarations. All fields after it become keyword-only. This is cleaner than the pre-3.10 approach of using `field(init=False)` or dummy defaults to force keyword-only behavior. The `KW_ONLY` feature makes dataclass `__init__` signatures more expressive and aligns them with modern Python API design best practices.

**Example:**
```python
from dataclasses import dataclass, KW_ONLY

@dataclass
class Event:
    name: str
    _: KW_ONLY  # Everything after is keyword-only
    timestamp: float
    source: str = "system"

e = Event("click", timestamp=1.0, source="ui")
# Event("click", 1.0)  # TypeError: missing keyword argument
```

## Q27: How does `frozen=True` affect dataclass behavior?

**A:** `@dataclass(frozen=True)` makes the dataclass immutable: once an instance is created, its attributes cannot be modified. The decorator generates `__setattr__` and `__delattr__` methods that raise `dataclasses.FrozenInstanceError` for any modification attempt. This enforces immutability at runtime, making the instance safe for use as dictionary keys, in sets, and in concurrent code (no race conditions from mutation).

The practical benefit is data integrity: frozen dataclasses guarantee that their values do not change after creation. This is useful for configuration objects, value types, and data that should be immutable (like coordinates, dates, or identifiers). The `__hash__` method is automatically generated when `frozen=True` (even if `eq=True`), making instances hashable. Without `frozen=True`, dataclasses with `eq=True` are not hashable by default (to prevent inconsistency between `__eq__` and `__hash__`).

The interaction with inheritance: frozen dataclasses can be subclassed, but the subclass must also be frozen (or the parent's `__setattr__` will prevent attribute assignment in the subclass). The practical recommendation is to use `frozen=True` for value types and configuration objects, and `frozen=False` (the default) for mutable objects. The `frozen=True` parameter is a powerful tool for enforcing immutability without the verbosity of defining `__setattr__` manually.

**Example:**
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: float
    y: float

p = Point(3.0, 4.0)
# p.x = 5.0  # FrozenInstanceError: cannot assign to field 'x'
d = {p: "origin"}  # Hashable — can be dict key
```

## Q28: What is the difference between `eq=True` and `eq=False` in dataclasses?

**A:** `eq=True` (the default) generates an `__eq__` method that compares two instances by comparing all their fields (or only fields with `compare=True`). `eq=False` does not generate `__eq__`, so the default `object.__eq__` is used (identity comparison: `id(a) == id(b)`). The difference is significant: with `eq=True`, two dataclass instances with the same field values are considered equal. With `eq=False`, only the same object (same identity) is considered equal.

The practical impact: `eq=True` is correct for value types (where two instances with the same data are logically equal). `eq=False` is useful for identity-based objects (like singletons, or objects where equality is defined by more than just field values). The `eq` parameter affects `__eq__` and, by extension, `__ne__`. It does not affect `__hash__` directly — `__hash__` is set to `None` when `eq=True` (to prevent inconsistency), unless `frozen=True` or `unsafe_hash=True` is also set.

The recommendation is to use `eq=True` for most dataclasses (value types, DTOs, records). Use `eq=False` when the default identity comparison is desired (rare for dataclasses). The `eq` parameter is a design decision that affects how instances are compared and used in sets and dictionaries. The `compare` parameter of `field()` controls which fields are included in equality comparison: `field(compare=False)` excludes a field from `__eq__`.

**Example:**
```python
from dataclasses import dataclass

@dataclass(eq=True)
class Value:
    x: int

@dataclass(eq=False)
class Identity:
    x: int

v1 = Value(1)
v2 = Value(1)
print(v1 == v2)  # True — same field values

i1 = Identity(1)
i2 = Identity(1)
print(i1 == i2)  # False — different objects (identity comparison)
```

## Q29: How do dataclasses support `__hash__` and when is it generated?

**A:** By default, dataclasses with `eq=True` (the default) set `__hash__` to `None`, making instances unhashable. This is because mutable objects with value-based equality should not be hashable (changing a field after insertion in a set breaks the set's invariants). Dataclasses with `eq=False` use the default `object.__hash__` (identity-based). Dataclasses with `frozen=True` automatically generate a `__hash__` based on all fields (since they are immutable). The `unsafe_hash=True` parameter generates `__hash__` even for mutable dataclasses (use with caution).

The practical usage: (1) `@dataclass(frozen=True)` — hashable, immutable. Best for value types that need to be used in sets or as dict keys. (2) `@dataclass(unsafe_hash=True)` — hashable, mutable. Dangerous: if a field is modified after insertion in a set, the set's internal hash table is corrupted. (3) `@dataclass(eq=False)` — uses `object.__hash__` (identity-based). Useful for identity-based objects. (4) `@dataclass(eq=True)` (default) — unhashable. Safe for mutable objects with value-based equality.

The `__hash__` generation follows Python's rules: if `__eq__` is defined, `__hash__` is set to `None` (unhashable) unless explicitly overridden. The `frozen=True` parameter overrides this by making the object immutable, which makes hashing safe. The `unsafe_hash=True` parameter overrides by explicitly generating `__hash__`, even though the object is mutable (the "unsafe" prefix warns that this can break sets/dicts if instances are modified after insertion). The recommendation is to use `frozen=True` for hashable dataclasses and avoid `unsafe_hash=True` unless you are certain that instances will not be modified after hashing.

**Example:**
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class ImmutablePoint:
    x: float
    y: float

@dataclass(unsafe_hash=True)
class MutablePoint:
    x: float
    y: float

# ImmutablePoint — safe
p1 = ImmutablePoint(1.0, 2.0)
s = {p1}  # Works

# MutablePoint — unsafe
p2 = MutablePoint(1.0, 2.0)
s2 = {p2}
p2.x = 10.0  # Breaks the set's hash table!
```

## Q30: What is the role of `__set_name__` in descriptors and dataclasses?

**A:** `__set_name__` is a method called on descriptors when the class is created. When a descriptor (an object with `__get__`, `__set__`, or `__delete__`) is assigned as a class attribute, Python calls `descriptor.__set_name__(owner_class, name)` where `name` is the attribute name. This allows the descriptor to know its name within the class, enabling name-based behavior (like generating storage keys, validation messages, or database column names).

The interaction with dataclasses is that dataclass fields can be descriptors. When a dataclass is defined, the `@dataclass` decorator processes the fields and generates `__init__`. If a field is a descriptor, `__set_name__` is called during class creation (before `@dataclass` processes it). The descriptor can then store its name for use in `__get__` and `__set__`. For example, a validated field descriptor can use the name in error messages: `raise ValueError(f"Invalid value for {self.name}: {value}")`.

The practical application is in custom field types for dataclasses. You can create descriptor-based fields that perform validation, transformation, or logging: `class PositiveInt: def __set_name__(self, owner, name): self.name = name; def __set__(self, instance, value): if value <= 0: raise ValueError(f"{self.name} must be positive"); instance.__dict__[self.name] = value`. This pattern combines descriptors with dataclasses for custom field behavior. The `__set_name__` method is essential for descriptors that need to know their attribute name.

**Example:**
```python
class Validated:
    def __set_name__(self, owner, name):
        self.name = name
    
    def __set__(self, instance, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{self.name} must be a non-empty string")
        instance.__dict__[self.name] = value
    
    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name, "")

from dataclasses import dataclass

@dataclass
class User:
    name: Validated = Validated()
    email: Validated = Validated()

u = User(name="Alice", email="alice@example.com")
# User(name="", email="alice")  # ValueError: name must be a non-empty string
```

## Q31: How does Python's MRO handle classes with different numbers of bases?

**A:** The C3 linearization algorithm handles classes with different numbers of bases by merging the MROs of all base classes while respecting the left-to-right order. For `class D(B, C)` where `B` has one base (`A`) and `C` has two bases (`A`, `X`), the algorithm merges `L[B]`, `L[C]`, and the direct bases `[B, C]`. The result is a linear ordering that includes all classes exactly once, respects the inheritance order, and places children before parents.

The practical example: `class D(B, C)` where `L[B] = [B, A, object]` and `L[C] = [C, A, X, object]`. The merge produces `[D, B, C, A, X, object]`. The algorithm ensures that `B` comes before `C` (left-to-right), `A` comes after both `B` and `C` (since `A` is a base of both), and `X` comes after `C` (since `C` inherits from `X`). The result is a consistent linear ordering regardless of the number of bases.

The key insight is that the C3 algorithm is not affected by the depth or width of the inheritance hierarchy — it always produces a consistent linear ordering. The algorithm's complexity is O(N^2) in the number of classes, but this is negligible for typical class hierarchies. The MRO is computed once at class definition time and cached, so there is no runtime overhead. The algorithm's robustness is why Python's multiple inheritance is predictable and reliable, even for complex hierarchies.

**Example:**
```python
class A:
    pass

class B(A):
    pass

class X:
    pass

class C(A, X):
    pass

class D(B, C):
    pass

print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'X'>, <class 'object'>)
```

## Q32: What is the `__class_getitem__` method and how does it interact with dataclasses?

**A:** `__class_getitem__` is a method that enables generic type syntax on classes. It is called when the class is subscripted with type arguments: `MyClass[int]`, `MyClass[str, int]`. The method receives the class and the subscript arguments and returns a generic alias (typically `types.GenericAlias`). This is the mechanism behind `list[int]`, `dict[str, int]`, and custom generic types.

The interaction with dataclasses is that dataclasses can be generic: `@dataclass class Pair: first: T; second: T` (with `from typing import TypeVar; T = TypeVar('T')`). The `@dataclass` decorator generates `__init__` that accepts `T` values. `Pair[int](1, 2)` creates a `Pair` instance with `first=1` and `second=2`. The `__class_getitem__` method is automatically inherited from `object` (or can be overridden for custom behavior).

The practical usage is in type-safe data structures: `@dataclass class Response: data: T; error: str = ""; def __class_getitem__(cls, item): return super().__class_getitem__(item)`. This enables `Response[int]` syntax for type annotations. The `__class_getitem__` method is called at class subscript time, not at instance creation time, so it has no runtime overhead for instance creation. The generic alias is used by type checkers (mypy, pyright) and can be used at runtime with `typing.get_type_hints()`.

**Example:**
```python
from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar('T')

@dataclass
class Wrapper(Generic[T]):
    value: T
    
    def __class_getitem__(cls, item):
        return super().__class_getitem__(item)

w = Wrapper[int](42)
print(w)  # Wrapper(value=42)
print(type(w.value))  # <class 'int'>
```

## Q33: What is the difference between `@dataclass` and `@dataclass(slots=True)` in terms of performance?

**A:** `@dataclass(slots=True)` (Python 3.10+) generates `__slots__` from the field names, eliminating the per-instance `__dict__`. This reduces memory usage by roughly 40-60% (depending on the number of fields and the platform's dict overhead). Attribute access is slightly faster because Python uses direct slot access (an array lookup) instead of dictionary lookup. The performance improvement is most significant for applications that create many instances (millions of dataclass objects).

The memory comparison: a regular dataclass instance with 5 fields uses roughly 152 bytes (object header + `__dict__` + 5 pointers). A slotted dataclass instance uses roughly 56 bytes (object header + 5 pointers). For 1 million instances, this is a 96MB difference. The attribute access improvement is marginal (nanoseconds per access) but can add up in tight loops. The `slots=True` parameter is a free performance optimization for most dataclasses.

The tradeoff is reduced flexibility: slotted instances cannot have attributes not defined in `__slots__`, cannot have `__dict__` (unless explicitly added), and cannot use `**kwargs` in `__init__` (because `**kwargs` creates a dict). Multiple inheritance with `__slots__` requires careful coordination (each class must define `__slots__` without overlapping names). The recommendation is to use `slots=True` by default for dataclasses, unless you need the flexibility of `__dict__` (dynamic attributes, `**kwargs`, or compatibility with code that expects `__dict__`).

**Example:**
```python
import sys
from dataclasses import dataclass

@dataclass
class RegularPoint:
    x: float
    y: float

@dataclass(slots=True)
class SlottedPoint:
    x: float
    y: float

r = RegularPoint(1.0, 2.0)
s = SlottedPoint(1.0, 2.0)
print(sys.getsizeof(r) + sys.getsizeof(r.__dict__))  # ~152 bytes
print(sys.getsizeof(s))  # ~56 bytes
```

## Q34: How do dataclasses handle `ClassVar` and `InitVar`?

**A:** `ClassVar` (from `typing`) marks a field as a class variable, not an instance variable. Dataclasses ignore `ClassVar` fields in `__init__`, `__repr__`, `__eq__`, and other generated methods. `ClassVar` fields are shared across all instances and are not included in the dataclass's field list. This is useful for constants, configuration, or metadata that belongs to the class, not to individual instances.

`InitVar` (from `dataclasses`) marks a field as an init-only variable: it is passed to `__init__` and `__post_init__`, but is not stored as an instance attribute. This is useful for parameters that affect initialization but should not be stored (like a "debug" flag that triggers validation but is not part of the data). `InitVar` fields are not included in `fields()`, `asdict()`, or `astuple()`.

The practical usage: `@dataclass class Config: name: str; _count: ClassVar[int] = 0; debug: InitVar[bool] = False`. `_count` is a class variable (shared across instances, not in `__init__`). `debug` is an init-only variable (passed to `__init__` and `__post_init__`, but not stored). In `__post_init__`, you can access `debug` as `self.debug` (it is temporarily available as an attribute). The `ClassVar` and `InitVar` markers provide fine-grained control over which fields are instance variables, class variables, and init-only parameters.

**Example:**
```python
from dataclasses import dataclass, InitVar
from typing import ClassVar

@dataclass
class Employee:
    name: str
    salary: float
    _next_id: ClassVar[int] = 1
    department: InitVar[str] = "general"
    
    def __post_init__(self, department):
        self.id = Employee._next_id
        Employee._next_id += 1
        self.dept = department

e1 = Employee("Alice", 80000, department="engineering")
e2 = Employee("Bob", 75000, department="marketing")
print(e1.id, e2.id)  # 1 2
print(e1.dept)  # engineering
```

## Q35: What is the relationship between `dataclasses` and `namedtuple`?

**A:** `dataclasses` and `namedtuple` both create classes for holding data, but they differ in mutability, inheritance, and feature set. `namedtuple` creates an immutable class (no attribute assignment after creation) with tuple semantics (indexing, unpacking, iteration). `dataclasses` creates a mutable class (by default) with attribute semantics (dot access, no indexing). `namedtuple` is simpler and more memory-efficient (it inherits from `tuple`). `dataclasses` is more flexible (mutable, supports inheritance, properties, validation).

The practical comparison: `namedtuple` is best for simple, immutable records where tuple semantics are desired (indexing, unpacking, iteration). `dataclasses` is best for mutable data containers, complex initialization, validation, and inheritance. `namedtuple` has no support for default values in Python < 3.6.1 (fixed in 3.6.1 with `defaults` parameter). `dataclasses` supports defaults, default factories, field customization, and `__post_init__`.

The migration path: many codebases use `namedtuple` for simple records and are migrating to `dataclasses` for the added flexibility. The `@dataclass(frozen=True)` option provides immutability similar to `namedtuple`, but without tuple semantics. The recommendation is to use `namedtuple` for simple, immutable records where tuple semantics are useful, and `dataclasses` for everything else. The `dataclasses` module is the modern Python approach to data containers and should be preferred in new code.

**Example:**
```python
from collections import namedtuple
from dataclasses import dataclass

# namedtuple — immutable, tuple semantics
PointNT = namedtuple('PointNT', ['x', 'y'])
p1 = PointNT(3.0, 4.0)
# p1.x = 5.0  # AttributeError — immutable

# dataclass — mutable, attribute semantics
@dataclass
class PointDC:
    x: float
    y: float

p2 = PointDC(3.0, 4.0)
p2.x = 5.0  # Works — mutable
```

## Q36: How does `__init_subclass__` work with dataclasses?

**A:** `__init_subclass__` is called when a class is subclassed, after the derived class is created. When used with dataclasses, `__init_subclass__` is called after the `@dataclass` decorator processes the derived class. This means the derived class's `__init__`, `__repr__`, etc. are already generated when `__init_subclass__` is called. The MRO is also computed at this point, so `__init_subclass__` can inspect the MRO.

The practical application is in dataclass hierarchies where the base class needs to register, validate, or modify subclasses. For example, a base dataclass can register all subclasses in a registry: `@dataclass class BaseModel: _registry = {}; def __init_subclass__(cls, **kwargs): super().__init_subclass__(**kwargs); BaseModel._registry[cls.__name__] = cls`. When `@dataclass class User(BaseModel): name: str` is defined, `__init_subclass__` is called, registering `User` in the registry.

The interaction with MRO: `__init_subclass__` is called for each class in the hierarchy, following the MRO. If `class D(B, C)` is defined and both `B` and `C` define `__init_subclass__`, both are called (B's first, then C's, following the MRO). This is consistent with the cooperative inheritance pattern. The practical recommendation is to use `__init_subclass__` in dataclass base classes for registration, validation, and framework hooks, and to call `super().__init_subclass__(**kwargs)` to maintain the chain.

**Example:**
```python
from dataclasses import dataclass

@dataclass
class Plugin:
    _registry: dict = None
    
    def __init_subclass__(cls, plugin_type="generic", **kwargs):
        super().__init_subclass__(**kwargs)
        if Plugin._registry is None:
            Plugin._registry = {}
        Plugin._registry[plugin_type] = cls

@dataclass
class AuthPlugin(Plugin, plugin_type="auth"):
    token: str

@dataclass
class CachePlugin(Plugin, plugin_type="cache"):
    ttl: int

print(Plugin._registry)
# {'auth': AuthPlugin, 'cache': CachePlugin}
```

## Q37: What are the best practices for using `super()` in cooperative multiple inheritance?

**A:** Best practices for `super()` in cooperative multiple inheritance: (1) Always call `super()` in every method that participates in the chain. A missing `super()` breaks the chain silently. (2) Use `*args` and `**kwargs` in method signatures to ensure compatibility with all classes in the hierarchy. This allows classes with different parameter requirements to coexist. (3) Place `super()` calls at the end of the method (for "wrapping" behavior) or at the beginning (for "preprocessing" behavior), but be consistent.

(4) Document the expected MRO position for classes in the hierarchy. Some classes must come before others (e.g., a logging mixin before a validation mixin). (5) Test the class in isolation AND in combination with other classes. A class that works alone may break in a hierarchy. (6) Use `__init_subclass__` or metaclasses to validate the hierarchy at class definition time. (7) Avoid mixing cooperative inheritance with explicit base class calls — they can conflict.

(8) Prefer composition over multiple inheritance when the inheritance is not truly cooperative (i.e., when classes are independent and do not need to call each other via `super()`). (9) Keep hierarchies shallow — deep cooperative hierarchies are difficult to understand and debug. (10) Use type hints and `typing.Protocol` to document the expected interface for each class in the hierarchy. These practices make cooperative multiple inheritance predictable, maintainable, and debuggable.

**Example:**
```python
class Base:
    def __init__(self, *args, **kwargs):
        print("Base.__init__")
        super().__init__(*args, **kwargs)

class MixinA:
    def __init__(self, *args, **kwargs):
        print("MixinA.__init__")
        super().__init__(*args, **kwargs)

class MixinB:
    def __init__(self, *args, **kwargs):
        print("MixinB.__init__")
        super().__init__(*args, **kwargs)

class Concrete(MixinA, MixinB, Base):
    def __init__(self):
        print("Concrete.__init__")
        super().__init__()

Concrete()
# Concrete -> MixinA -> MixinB -> Base
```

## Q38: How does Python handle method resolution when a class has multiple bases with different MROs?

**A:** Python's C3 linearization merges the MROs of all base classes into a single linear ordering. The merge algorithm ensures that: (1) the derived class comes first, (2) the left-to-right order of bases is preserved, (3) if a class appears in multiple base MROs, it appears in the final MRO in the position consistent with all base MROs, and (4) the ordering is monotonic (if class A precedes class B in a base's MRO, it precedes B in the final MRO). If no valid ordering exists (contradictory constraints), Python raises `TypeError`.

The practical example: `class D(B, C)` where `L[B] = [B, A, object]` and `L[C] = [C, A, object]`. The merge produces `[D, B, C, A, object]`. The algorithm starts with `D`, then takes the head of each base's MRO (`B` from `L[B]`, `C` from `L[C]`). `B` is not in the tail of any other list, so it is selected. Then `C` is selected (it is the head of `L[C]` and not in the tail of any remaining list). Then `A` (head of both `L[B]` and `L[C]`, now that `B` and `C` are consumed). Then `object`.

The key insight is that the C3 algorithm is deterministic: given the same class definitions, it always produces the same MRO. The algorithm's constraints ensure that the MRO is consistent with the programmer's intent (left-to-right priority) while avoiding contradictions. The `TypeError` is rare in practice and typically indicates a pathological inheritance pattern. For well-designed hierarchies, the C3 algorithm produces a sensible MRO every time.

**Example:**
```python
class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B"

class C(A):
    def method(self):
        return "C"

class D(B, C):
    pass

# L[B] = [B, A, object]
# L[C] = [C, A, object]
# merge([D], [B, A, object], [C, A, object], [B, C])
# = [D, B, C, A, object]

print(D().method())  # "B" — B is first after D in MRO
```

## Q39: What is the role of `__repr__` in dataclasses and how is it generated?

**A:** The `@dataclass` decorator generates a `__repr__` method that returns a string representation of the instance. The default format is `ClassName(field1=value1, field2=value2, ...)`. The `repr` parameter of `@dataclass` controls whether `__repr__` is generated (default `True`). The `repr` parameter of `field()` controls whether individual fields are included in `__repr__` (default `True`). Setting `repr=False` on a field excludes it from the representation.

The practical importance is for debugging: `print(instance)` or `repr(instance)` shows the class name and all field values, making it easy to inspect the state of an object. The generated `__repr__` is consistent and follows a standard format, which is useful for logging, debugging, and documentation. The `repr=False` option is useful for sensitive fields (passwords, tokens) or large fields (binary data) that would clutter the output.

The interaction with inheritance: the generated `__repr__` includes all fields from the class and its bases. For `@dataclass class Child(Parent): z: int`, the `__repr__` shows `Child(x=..., y=..., z=...)` where `x` and `y` are parent fields. The class name in the `__repr__` is the most derived class's name, not the base class's name. This makes debugging easier because you can see the full state of the object in a single representation string.

**Example:**
```python
from dataclasses import dataclass, field

@dataclass
class User:
    name: str
    password: str = field(repr=False)
    age: int

u = User("Alice", "secret123", 30)
print(repr(u))  # User(name='Alice', age=30)
# password is not shown (repr=False)
```

## Q40: How do dataclasses interact with `__init__` parameter ordering rules?

**A:** Dataclasses follow Python's function parameter ordering rules for the generated `__init__`: (1) fields without defaults come first (positional-or-keyword). (2) fields with defaults come after (keyword-only if following a field without a default, positional-or-keyword if all preceding fields have defaults). (3) fields with `default_factory` are treated as having defaults. (4) `KW_ONLY` makes all subsequent fields keyword-only.

The practical constraint is that a field without a default cannot follow a field with a default (same as function parameters). This is a Python language rule, not a dataclass rule. For example, `@dataclass class C: x: int = 0; y: str` is invalid because `y` (no default) follows `x` (default). The fix is to reorder fields: `@dataclass class C: y: str; x: int = 0`. Or use `KW_ONLY` to make `y` keyword-only: `@dataclass class C: x: int = 0; _: KW_ONLY; y: str`.

The practical recommendation is to order fields with no defaults before fields with defaults. This is the natural order (required parameters before optional parameters) and follows Python's convention. The `KW_ONLY` sentinel provides flexibility when you want required keyword-only parameters after optional positional parameters. The `@dataclass` decorator raises a `TypeError` if the field ordering violates Python's parameter rules, providing a clear error message at class definition time.

**Example:**
```python
from dataclasses import dataclass, KW_ONLY

# Valid: required fields first
@dataclass
class Valid:
    name: str
    age: int
    email: str = ""

# Invalid: field without default after field with default
# @dataclass
# class Invalid:
#     name: str = ""
#     age: int  # TypeError!

# Fix: use KW_ONLY
@dataclass
class Fixed:
    name: str = ""
    _: KW_ONLY
    age: int  # keyword-only, required
```

## Q41: What is the difference between `@dataclass` and `@attrs` (attrs library)?

**A:** `@dataclass` (from the standard library) and `@attrs` (from the third-party `attrs` library) serve the same purpose: reducing boilerplate for data classes. `attrs` was created before `dataclasses` and has more features: validators, converters, `slots=True` support (before Python 3.10), immutable instances (`frozen`), and more fine-grained control over generated methods. `@dataclass` is simpler, has fewer features, and is part of the standard library (no external dependency).

The practical comparison: `attrs` provides `@attrs.define` (new API) and `@attr.s` (old API). `@attrs.define` is similar to `@dataclass` but with additional features: automatic `__slots__`, `frozen` by default option, validators, converters, and better performance. `@dataclass` is simpler and more familiar to Python developers. `attrs` has a larger ecosystem (attrs-generated classes work well with other libraries). `dataclasses` is the standard library approach and is preferred for new code unless `attrs` features are needed.

The recommendation is to use `@dataclass` for most use cases (it is standard, simple, and sufficient). Use `@attrs` when you need validators, converters, or advanced features not available in `@dataclass`. Both libraries generate similar code and have similar performance characteristics. The choice is a matter of preference and project conventions. The `dataclasses` module is the standard library approach and should be the default choice for new code.

**Example:**
```python
# dataclass
from dataclasses import dataclass
@dataclass
class PointDC:
    x: float
    y: float

# attrs (new API)
import attrs
@attrs.define
class PointAttrs:
    x: float
    y: float

# attrs with validators
@attrs.define
class ValidatedPoint:
    x: float = attrs validators.instance_of(float)
    y: float = attrs.validators.instance_of(float)
```

## Q42: How does the MRO affect `isinstance` and `issubclass` checks?

**A:** `isinstance(obj, cls)` checks if `obj` is an instance of `cls` or any of its subclasses. It uses the `__mro__` of `obj`'s class to traverse the hierarchy: if `cls` appears in `obj.__class__.__mro__`, `isinstance` returns `True`. `issubclass(A, B)` checks if `A` is a subclass of `B` by checking if `B` appears in `A.__mro__`. Both checks use the MRO, which is the complete linear ordering of all classes in the hierarchy.

The practical implication is that `isinstance` and `issubclass` work correctly with multiple inheritance. For `class D(B, C)` where `B(A)` and `C(A)`, `isinstance(d, A)` returns `True` because `A` appears in `D.__mro__`. `isinstance(d, B)` returns `True` because `B` appears in `D.__mro__`. The MRO ensures that all ancestors are recognized, regardless of the inheritance path. This is correct and expected behavior — the MRO is the definitive list of all classes in the hierarchy.

The performance implication is that `isinstance` is O(N) in the number of classes in the MRO, because it may need to traverse the entire MRO. For shallow hierarchies, this is negligible. For deep hierarchies, it can be significant. The `isinstance` check can be optimized by using `__subclasscheck__` (on the metaclass) or by caching results. The practical recommendation is to use `isinstance` and `issubclass` freely — they are correct and efficient for typical class hierarchies. The MRO ensures that they work correctly with multiple inheritance.

**Example:**
```python
class A:
    pass

class B(A):
    pass

class C(A):
    pass

class D(B, C):
    pass

d = D()
print(isinstance(d, A))  # True — A is in D.__mro__
print(isinstance(d, B))  # True — B is in D.__mro__
print(isinstance(d, C))  # True — C is in D.__mro__
print(isinstance(d, D))  # True — D is in D.__mro__
print(issubclass(D, A))  # True
```

## Q43: What are `__slots__` and how do they interact with multiple inheritance?

**A:** `__slots__` is a class attribute that restricts instance attributes to a fixed set of names, preventing `__dict__` creation. This reduces memory usage and slightly improves attribute access. When used with multiple inheritance, `__slots__` requires careful coordination: each class must define `__slots__` without overlapping names. If two classes in the hierarchy define the same slot name, Python raises a `TypeError` at class definition time.

The practical implication is that `__slots__` classes can be used in multiple inheritance, but the slots must not conflict. For example, `class A: __slots__ = ('x',)` and `class B: __slots__ = ('y',)` can be combined: `class C(A, B): __slots__ = ('z',)`. The `C` instance has slots `x`, `y`, `z` — no `__dict__`. But `class D(A): __slots__ = ('x',)` would conflict with `A`'s slot `x`, causing a `TypeError`.

The interaction with dataclasses: `@dataclass(slots=True)` generates `__slots__` from the field names. If the dataclass inherits from another slotted class, the generated `__slots__` must not conflict with the parent's slots. In practice, this works correctly because dataclass fields have unique names. The recommendation is to use `__slots__` with multiple inheritance only when all classes define non-overlapping slots. For most applications, the memory savings of `__slots__` are not worth the complexity of coordinating slot names across a hierarchy.

**Example:**
```python
class A:
    __slots__ = ('x',)

class B:
    __slots__ = ('y',)

class C(A, B):
    __slots__ = ('z',)

c = C()
c.x = 1
c.y = 2
c.z = 3
print(hasattr(c, '__dict__'))  # False — no __dict__

# class D(A):
#     __slots__ = ('x',)  # TypeError: slot 'x' already defined in 'A'
```

## Q44: What is the role of `__post_init__` in dataclass inheritance?

**A:** `__post_init__` is called after `__init__` for each class in the dataclass hierarchy. In inheritance, `__post_init__` follows the cooperative pattern: the parent's `__post_init__` is called first (via `super().__post_init__()`), then the child's. This is consistent with the MRO and cooperative multiple inheritance. Each class can perform its post-initialization logic and then delegate to the next class via `super()`.

The practical implication is that `__post_init__` in a child class can access fields from the parent class (because `__init__` has already assigned them). For example, a child class can validate a combination of parent and child fields: `@dataclass class Child(Parent): z: int; def __post_init__(self): super().__post_init__(); assert self.x + self.z > 0`. The `super().__post_init__()` call ensures that the parent's post-initialization logic is executed.

The interaction with `InitVar`: `InitVar` fields are passed to `__post_init__` as arguments. In inheritance, `InitVar` fields from all classes are collected and passed to `__post_init__`. The `__post_init__` method must accept these arguments (typically via `*args` or explicit parameters). The `InitVar` fields are not stored as instance attributes — they are only available during `__init__` and `__post_init__`. This makes `InitVar` useful for parameters that affect initialization but should not be stored.

**Example:**
```python
from dataclasses import dataclass, InitVar

@dataclass
class Base:
    x: int
    log: InitVar[bool] = False
    
    def __post_init__(self, log):
        if log:
            print(f"Base: x={self.x}")

@dataclass
class Child(Base):
    y: int
    log: InitVar[bool] = False
    
    def __post_init__(self, log):
        super().__post_init__(log)
        if log:
            print(f"Child: y={self.y}")

c = Child(1, 2, log=True)
# Base: x=1
# Child: y=2
```

## Q45: How do dataclasses handle `__eq__` with inherited fields?

**A:** The generated `__eq__` method compares all fields from the class and its bases. For `@dataclass class Child(Parent): z: int`, the `__eq__` compares `x`, `y` (parent fields), and `z` (child field). Two instances are equal if and only if all their fields (inherited and own) are equal. This is the expected behavior for value types: two objects are equal if they represent the same data.

The practical implication is that `__eq__` works correctly with inheritance. `Child(1, 2, 3) == Child(1, 2, 3)` is `True`. `Child(1, 2, 3) == Child(1, 2, 4)` is `False`. `Child(1, 2, 3) == Parent(1, 2)` is `False` (different types). The `__eq__` method checks the type first (using `type(self) == type(other)`), so instances of different types are never equal, even if they have the same field values.

The interaction with `field(compare=False)`: fields with `compare=False` are excluded from `__eq__`. This is useful for fields that should not affect equality (like timestamps, IDs, or computed fields). For example, `@dataclass class Event: name: str; timestamp: float = field(compare=False)`. Two `Event` instances with the same `name` are equal regardless of `timestamp`. The `compare` parameter provides fine-grained control over equality semantics.

**Example:**
```python
from dataclasses import dataclass, field

@dataclass
class Parent:
    x: int
    y: int

@dataclass
class Child(Parent):
    z: int

print(Child(1, 2, 3) == Child(1, 2, 3))  # True
print(Child(1, 2, 3) == Child(1, 2, 4))  # False
print(Child(1, 2, 3) == Parent(1, 2))     # False — different types

@dataclass
class Event:
    name: str
    timestamp: float = field(compare=False)

print(Event("click", 1.0) == Event("click", 999.0))  # True
```

## Q46: What is the difference between `@dataclass` and `@dataclass(eq=True)`?

**A:** `@dataclass` without arguments is equivalent to `@dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False)`. The `eq=True` parameter (the default) generates an `__eq__` method that compares all fields (or only fields with `compare=True`). `@dataclass(eq=True)` is explicitly the same as the default — it has no additional effect. The difference is readability: `@dataclass(eq=True)` makes the equality behavior explicit, while `@dataclass` relies on the default.

The practical implication is that `@dataclass` and `@dataclass(eq=True)` produce identical code. The choice is a matter of style: some developers prefer explicit parameters for clarity, while others prefer the concise default. The `eq=False` option disables `__eq__` generation, using the default identity comparison (`object.__eq__`). This is useful when you want identity-based equality (rare for dataclasses).

The recommendation is to use `@dataclass` (without `eq=True`) for most cases, since `eq=True` is the default and is rarely changed. If you need to disable equality comparison, use `@dataclass(eq=False)` explicitly. The `eq` parameter is a design decision that affects how instances are compared and used in sets and dictionaries. The default `eq=True` is correct for value types, and `eq=False` is correct for identity-based objects.

**Example:**
```python
from dataclasses import dataclass

# These are equivalent:
@dataclass
class PointA:
    x: float
    y: float

@dataclass(eq=True)
class PointB:
    x: float
    y: float

@dataclass(eq=False)
class PointC:
    x: float
    y: float

print(PointA(1, 2) == PointA(1, 2))  # True
print(PointB(1, 2) == PointB(1, 2))  # True
print(PointC(1, 2) == PointC(1, 2))  # False — identity comparison
```

## Q47: How does Python's MRO handle `object` as the ultimate base class?

**A:** `object` is the ultimate base class of all Python classes. Every class inherits from `object` (directly or indirectly). The MRO always ends with `object`. When computing the MRO, `object` is treated as the final class in every base's MRO. For example, `L[int] = [int, object]` and `L[str] = [str, object]`. The C3 algorithm ensures that `object` appears exactly once at the end of the final MRO.

The practical implication is that `object` is always available for method lookup. When a method is not found in any class in the MRO, Python falls back to `object`'s implementation (which typically raises `AttributeError` or `NotImplementedError`). The `object` base class provides default implementations of `__init__`, `__repr__`, `__str__`, `__eq__`, `__hash__`, `__sizeof__`, and other fundamental methods. These defaults are overridden by derived classes as needed.

The interaction with MRO is that `object`'s methods are the last resort for method resolution. If no class in the MRO defines a method, `object`'s version is used. For example, if you call `obj.__repr__()` and no class in the MRO defines `__repr__`, `object.__repr__` is called (which returns `<ClassName object at address>`). This ensures that all objects have basic functionality (representation, equality, hashing) even if they don't explicitly define it. The `object` base class is the foundation of Python's object model and the MRO always accounts for it.

**Example:**
```python
class A:
    pass

class B(A):
    pass

print(B.__mro__)
# (<class 'B'>, <class 'A'>, <class 'object'>)
# object is always last

b = B()
print(repr(b))  # <__main__.B object at 0x...> — object.__repr__
```

## Q48: What are the performance characteristics of `super()` in Python 3?

**A:** `super()` in Python 3 is efficient: it returns a bound method proxy that delegates to the next class in the MRO. The proxy stores the MRO index (the current position in the MRO) and uses it to find the next class. The first call to `super()` involves a lookup of the MRO and the current class's position, but subsequent calls are cached. The overhead is minimal — a few nanoseconds per `super()` call — and is negligible for most applications.

The practical performance profile: `super()` adds a small constant overhead compared to direct method calls. For deep hierarchies (many classes in the MRO), the overhead is slightly larger because the MRO traversal is longer. For typical hierarchies (2-5 classes), the overhead is negligible. The `super()` proxy is a lightweight object that is created on-the-fly and discarded after the method call. There is no persistent overhead.

The interaction with method lookup: `super().__init__()` first looks up `__init__` in the MRO starting from the class after the current class. If the method is found, it is called. If not, the search continues to the next class. The lookup is O(N) in the number of remaining classes in the MRO, but this is typically a small number (2-3 classes). The practical recommendation is to use `super()` freely — the performance overhead is negligible compared to the correctness and maintainability benefits of cooperative inheritance.

**Example:**
```python
import timeit

class A:
    def method(self):
        pass

class B(A):
    def method(self):
        return super().method()

b = B()

# Direct call
t1 = timeit.timeit(lambda: A.method(b), number=1000000)

# super() call
t2 = timeit.timeit(lambda: b.method(), number=1000000)

print(f"Direct: {t1:.3f}s, super(): {t2:.3f}s")
# super() overhead is minimal (typically < 50% more than direct)
```

## Q49: How do dataclasses handle `__bool__` and truthiness?

**A:** Dataclasses do not generate a `__bool__` method by default. The default `__bool__` (inherited from `object`) always returns `True` for any instance. If you need custom truthiness, you must define `__bool__` manually in the dataclass. This is a design decision: dataclasses are data containers, and truthiness is typically not a property of data. If you need truthiness (e.g., for an optional wrapper), define `__bool__` explicitly.

The practical implication is that all dataclass instances are truthy by default. `bool(Point(0, 0))` returns `True`, even though the point has zero coordinates. This is consistent with Python's general principle: objects are truthy unless they define `__bool__` returning `False` or `__len__` returning 0. Dataclasses do not define either, so they are always truthy.

The recommendation is to define `__bool__` explicitly if truthiness is meaningful for your dataclass. For example, `@dataclass class Result: value: Any; error: str = ""; def __bool__(self): return not self.error`. This makes `Result(42)` truthy and `Result(None, "error")` falsy. The `__bool__` method should return a boolean and should not have side effects. For most dataclasses, the default truthiness (always `True`) is correct.

**Example:**
```python
from dataclasses import dataclass
from typing import Any

@dataclass
class Result:
    value: Any
    error: str = ""
    
    def __bool__(self):
        return not self.error

r1 = Result(42)
r2 = Result(None, "failed")
print(bool(r1))  # True
print(bool(r2))  # False

# Default dataclass — always truthy
@dataclass
class Point:
    x: float
    y: float

print(bool(Point(0, 0)))  # True — default __bool__
```

## Q50: What is the role of `__format__` in dataclasses?

**A:** Dataclasses do not generate a `__format__` method by default. The default `__format__` (inherited from `object`) calls `str()` on the instance, which calls `__repr__`. If you need custom formatting (e.g., for f-strings, `format()`, or `str.format()`), you must define `__format__` manually. The `__format__` method receives a format spec (like `".2f"` for floats) and returns a formatted string.

The practical implication is that dataclass instances use `__repr__` for formatting by default. `f"{point}"` calls `format(point, "")`, which calls `point.__format_("")`, which calls `str(point)`, which calls `repr(point)`. This produces the `ClassName(field1=value1, ...)` representation. If you want custom formatting, define `__format__`: `def __format__(self, spec): return f"({self.x:{spec}}, {self.y:{spec}})"`.

The interaction with inheritance: `__format__` follows the MRO, so a base class can define `__format__` and derived classes can override it. The format spec is passed through, allowing derived classes to add formatting logic. The practical recommendation is to define `__format__` if your dataclass needs custom string formatting (like formatted numbers, dates, or specialized output). For most dataclasses, the default `__repr__` formatting is sufficient.

**Example:**
```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
    
    def __format__(self, spec):
        return f"({self.x:{spec}}, {self.y:{spec}})"

p = Point(3.14159, 2.71828)
print(f"{p:.2f}")  # (3.14, 2.72)
print(format(p, ".1f"))  # (3.1, 2.7)
```
## Q51: How does `__init_subclass__` propagate through the MRO in complex hierarchies?

**A:** `__init_subclass__` is called for every class in the MRO that defines it, following the MRO order. When `class D(B, C)` is defined, Python calls `__init_subclass__` on each class in `D.__mro__` that defines it, starting from `D`'s most specific bases and working up to `object`. The call follows the cooperative pattern: each `__init_subclass__` should call `super().__init_subclass__(**kwargs)` to continue the chain. If any class fails to call `super().__init_subclass__()`, subsequent classes in the MRO are never notified.

The practical example: `class D(B, C)` where `B` and `C` both define `__init_subclass__`. The MRO is `D -> B -> C -> A -> object`. `B.__init_subclass__` is called first (because `B` comes before `C` in the MRO). Then `C.__init_subclass__` is called (via `super().__init_subclass__()` in `B`). Then `A.__init_subclass__` is called (if it defines one). Then `object.__init_subclass__` (the no-op default). This ensures that all classes in the hierarchy are notified of the subclass creation.

The interaction with `**kwargs`: `__init_subclass__` receives keyword arguments from the class definition. For `class D(B, C, my_arg="value")`, `D.__init_subclass__` receives `my_arg="value"`. These kwargs must be forwarded via `super().__init_subclass__(**kwargs)` to avoid losing them. If a class in the chain consumes a kwarg (by popping it from `kwargs`), subsequent classes do not receive it. This is the cooperative pattern applied to `__init_subclass__`.

**Example:**
```python
class Base:
    _registry = []
    
    def __init_subclass__(cls, register=True, **kwargs):
        super().__init_subclass__(**kwargs)
        if register:
            Base._registry.append(cls.__name__)

class A(Base):
    pass

class B(Base, register=False):
    pass

class C(A):
    pass

print(Base._registry)  # ['A', 'C']
# B is not registered (register=False)
```

## Q52: What are the implications of using `*args` and `**kwargs` in cooperative inheritance?

**A:** Using `*args` and `**kwargs` in cooperative inheritance ensures that methods are compatible with all classes in the hierarchy, regardless of their parameter requirements. Each class can accept different parameters, and `*args`/`**kwargs` passes through any parameters it does not consume. This flexibility is essential for mixins and cooperative hierarchies where classes have different initialization requirements.

The practical benefit: a mixin can define `def __init__(self, *args, log=False, **kwargs): super().__init__(*args, **kwargs)` and add a `log` parameter without breaking classes that do not accept `log`. The `*args` and `**kwargs` capture any parameters the mixin does not recognize and pass them to the next class. Without `*args`/`**kwargs`, each class would need to know all parameters of all other classes in the hierarchy, creating tight coupling.

The downside is reduced readability and type safety. The method signature `def __init__(self, *args, **kwargs)` does not document what parameters are expected. Type checkers cannot verify that the correct arguments are being passed. The practical recommendation is to use `*args`/`**kwargs` for mixins and framework code where flexibility is paramount, and to use explicit parameters for application code where clarity is more important. Documenting the expected parameters in docstrings helps mitigate the readability issue.

**Example:**
```python
class LoggingMixin:
    def __init__(self, *args, log_file=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.log_file = log_file

class ValidationMixin:
    def __init__(self, *args, validate=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.validate = validate

class BaseModel:
    def __init__(self, name):
        self.name = name

class User(LoggingMixin, ValidationMixin, BaseModel):
    pass

u = User("Alice", log_file="app.log", validate=True)
print(u.name, u.log_file, u.validate)
# Alice app.log True
```

## Q53: What is the relationship between `__slots__` and `__dict__` in dataclasses?

**A:** `__slots__` and `__dict__` are mutually exclusive by default: a class with `__slots__` does not have `__dict__`, and a class with `__dict__` does not need `__slots__`. The `@dataclass(slots=True)` parameter generates `__slots__` from field names, eliminating `__dict__`. This reduces memory usage and prevents dynamic attribute creation. Without `slots=True`, dataclass instances have `__dict__` and can have arbitrary attributes added at runtime.

The practical implication: a slotted dataclass cannot have attributes not defined in its fields. `@dataclass(slots=True) class Point: x: float; y: float` — `p = Point(1.0, 2.0); p.z = 3.0` raises `AttributeError`. A non-slotted dataclass allows this: `p = Point(1.0, 2.0); p.z = 3.0` works (adds `z` to `__dict__`). The `__dict__` flexibility is useful for dynamic attributes but wastes memory and can hide bugs.

The interaction with inheritance: if a parent class has `__slots__` and a child class does not, the child class has `__dict__` (because it does not define `__slots__`). This means the child instance has both the parent's slots AND a `__dict__`, which defeats the memory savings of `__slots__`. To maintain memory efficiency, all classes in the hierarchy should define `__slots__` (or use `@dataclass(slots=True)`). The practical recommendation is to use `slots=True` consistently across a dataclass hierarchy for maximum memory savings.

**Example:**
```python
from dataclasses import dataclass

@dataclass(slots=True)
class SlottedBase:
    x: float

@dataclass
class NonSlottedChild(SlottedBase):
    y: float

s = SlottedBase(1.0)
print(hasattr(s, '__dict__'))  # False

c = NonSlottedChild(1.0, 2.0)
print(hasattr(c, '__dict__'))  # True — child has __dict__
c.z = 3.0  # Works — dynamic attribute via __dict__
```

## Q54: How do dataclasses handle `__copy__` and `__deepcopy__`?

**A:** Dataclasses do not generate `__copy__` or `__deepcopy__` methods by default. The default behavior (inherited from `object`) is to copy the instance's `__dict__` (for shallow copy) or recursively copy all attributes (for deep copy). For non-slotted dataclasses, this works correctly: `copy.copy(instance)` creates a shallow copy with the same field values. For slotted dataclasses, the default copy behavior may not work correctly because there is no `__dict__` to copy.

The practical implication: for non-slotted dataclasses, `copy.copy` and `copy.deepcopy` work correctly without custom `__copy__`/`__deepcopy__`. For slotted dataclasses, you may need to implement `__copy__` and `__deepcopy__` to ensure correct behavior. The `__copy__` method should return a new instance with the same field values. The `__deepcopy__` method should return a new instance with deep copies of all field values.

The recommendation is to test `copy.copy` and `copy.deepcopy` with your dataclasses before relying on them. For simple dataclasses (fields are immutable or simple objects), the default behavior is correct. For complex dataclasses (fields contain mutable objects, nested dataclasses, or custom types), implement `__copy__` and `__deepcopy__` explicitly. The `@dataclass` decorator does not generate these methods because the default behavior is usually sufficient and explicit implementation adds complexity.

**Example:**
```python
import copy
from dataclasses import dataclass, field

@dataclass
class Address:
    city: str
    country: str

@dataclass
class User:
    name: str
    address: Address
    tags: list = field(default_factory=list)

u1 = User("Alice", Address("NYC", "USA"), ["admin"])
u2 = copy.copy(u1)  # Shallow copy — tags list is shared
u3 = copy.deepcopy(u1)  # Deep copy — everything independent

u1.tags.append("super")
print(u1.tags)  # ['admin', 'super']
print(u2.tags)  # ['admin', 'super'] — shared list!
print(u3.tags)  # ['admin'] — independent copy
```

## Q55: What is the role of `__init_subclass__` in enforcing class hierarchy constraints?

**A:** `__init_subclass__` can enforce constraints on subclasses at class definition time. When a subclass is defined, `__init_subclass__` is called, and it can check constraints (required attributes, method implementations, field types) and raise `TypeError` if they are violated. This provides compile-time-like validation for class hierarchies, catching errors at class definition time instead of runtime.

The practical application is in framework and library design. For example, a base class can enforce that all subclasses define a `process` method: `class Plugin: def __init_subclass__(cls, **kwargs): super().__init_subclass__(**kwargs); if not hasattr(cls, 'process'): raise TypeError(f"{cls.__name__} must implement 'process'")`. When `class MyPlugin(Plugin): pass` is defined (without `process`), `TypeError` is raised immediately.

The interaction with dataclasses: `__init_subclass__` can validate dataclass fields. For example, a base dataclass can enforce that all subclasses have a `name` field: `@dataclass class BaseModel: def __init_subclass__(cls, **kwargs): super().__init_subclass__(**kwargs); if 'name' not in cls.__dataclass_fields__: raise TypeError("Subclass must have 'name' field")`. This ensures that all subclasses conform to a minimum interface, catching violations at class definition time.

**Example:**
```python
from dataclasses import dataclass

@dataclass
class ValidatedModel:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, '__dataclass_fields__'):
            if 'name' not in cls.__dataclass_fields__:
                raise TypeError(f"{cls.__name__} must have a 'name' field")

@dataclass
class User(ValidatedModel):
    name: str
    email: str

# @dataclass
# class BadModel(ValidatedModel):
#     email: str  # TypeError: BadModel must have a 'name' field
```

## Q56: How does Python's MRO handle classes with `__init_subclass__` that raise exceptions?

**A:** If `__init_subclass__` raises an exception during class definition, the class is not created. The exception propagates up to the point where the class statement is executed. This is a feature, not a bug — it allows `__init_subclass__` to enforce constraints by raising exceptions. The class is only created if `__init_subclass__` completes successfully for all classes in the MRO.

The practical implication is that `__init_subclass__` can serve as a class-definition-time validator. If any `__init_subclass__` in the MRO raises, the class is not defined. This is useful for enforcing invariants: "all subclasses must have a `name` field", "all subclasses must implement `process`", "all subclasses must be registered". The exception prevents the class from being used incorrectly, catching errors at definition time instead of runtime.

The interaction with MRO: `__init_subclass__` is called for each class in the MRO (in MRO order). If any call raises, the exception propagates and the class is not created. The other `__init_subclass__` calls that would have been made (for classes later in the MRO) are not executed. This is consistent with the cooperative pattern: if one class rejects the subclass, the entire hierarchy is not created.

**Example:**
```python
class Base:
    def __init_subclass__(cls, min_version=1, **kwargs):
        super().__init_subclass__(**kwargs)
        if min_version < 1:
            raise ValueError(f"{cls.__name__} requires min_version >= 1")

class ValidChild(Base, min_version=2):
    pass  # Works — min_version=2 >= 1

# class InvalidChild(Base, min_version=0):
#     pass  # ValueError: InvalidChild requires min_version >= 1
```

## Q57: What is the difference between `@dataclass` and `@dataclass(init=False)`?

**A:** `@dataclass(init=False)` tells the decorator not to generate an `__init__` method. The class uses whatever `__init__` is defined in the class body (or inherited from a parent). This is useful when you need custom initialization logic that cannot be expressed through simple field defaults. For example, initialization that depends on external state, validation that requires network calls, or factory methods that construct objects differently based on input.

The practical usage: `@dataclass(init=False) class Config: x: int; y: int; def __init__(self, **kwargs): self.x = kwargs.get('x', 0); self.y = kwargs.get('y', 0)`. The `@dataclass` decorator generates `__repr__`, `__eq__`, and other methods, but not `__init__`. You provide a custom `__init__` that handles initialization logic. The class is still a dataclass (it has `__repr__`, `__eq__`, etc.) but with custom initialization.

The interaction with fields: fields are still defined as type annotations, and they appear in `__repr__`, `__eq__`, and `fields()`. But they are not automatically initialized by `__init__` (because there is no generated `__init__`). You must initialize them manually in your custom `__init__`. The `init=False` parameter is useful for classes where the generated `__init__` is too restrictive (complex default values, conditional initialization, or external dependencies).

**Example:**
```python
from dataclasses import dataclass, field

@dataclass(init=False)
class Database:
    host: str
    port: int
    connected: bool = False
    
    def __init__(self, connection_string: str):
        parts = connection_string.split(':')
        self.host = parts[0]
        self.port = int(parts[1])
        self.connected = True

db = Database("localhost:5432")
print(db)  # Database(host='localhost', port=5432, connected=True)
```

## Q58: How do dataclasses handle `__sizeof__` and memory profiling?

**A:** Dataclasses do not generate a `__sizeof__` method by default. The default `__sizeof__` (inherited from `object`) returns the size of the object's `__dict__` (for non-slotted classes) or the base object size (for slotted classes). For memory profiling, `sys.getsizeof(instance)` calls `__sizeof__` and adds the size of the `__dict__` (if present). This provides an accurate measurement of the instance's memory usage.

The practical implication: for non-slotted dataclasses, `sys.getsizeof` includes the `__dict__` size (which can be large). For slotted dataclasses (`slots=True`), `sys.getsizeof` returns the base object size plus slot sizes (much smaller). The `__sizeof__` method can be overridden for custom memory reporting, but this is rarely needed for dataclasses.

The recommendation for memory profiling: use `pympler.asizeof` for accurate deep size measurement (including all referenced objects). Use `sys.getsizeof` for shallow size measurement (just the object itself). For dataclasses, `slots=True` provides the best memory efficiency. The practical benefit is that `slots=True` dataclasses use significantly less memory, which is measurable with `sys.getsizeof` and `pympler.asizeof`.

**Example:**
```python
import sys
from dataclasses import dataclass

@dataclass
class RegularPoint:
    x: float
    y: float

@dataclass(slots=True)
class SlottedPoint:
    x: float
    y: float

r = RegularPoint(1.0, 2.0)
s = SlottedPoint(1.0, 2.0)

print(f"Regular: {sys.getsizeof(r)} + dict: {sys.getsizeof(r.__dict__)}")
print(f"Slotted: {sys.getsizeof(s)}")
# Regular: 48 + dict: 64 = ~112 bytes
# Slotted: 40 bytes
```

## Q59: What is the role of `__class_getitem__` in generic dataclasses?

**A:** `__class_getitem__` enables generic type syntax on dataclasses. When a dataclass is defined with `Generic[T]`, the `__class_getitem__` method is called when the class is subscripted: `MyDataclass[int]`. This returns a `types.GenericAlias` that can be used for type annotations and at runtime. The `__class_getitem__` method is inherited from `Generic` (if the dataclass inherits from `Generic[T]`) or can be defined manually.

The practical usage: `from typing import TypeVar, Generic; T = TypeVar('T'); @dataclass class Wrapper(Generic[T]): value: T`. This enables `Wrapper[int](42)`, `Wrapper[str]("hello")`, etc. The type parameter `T` is used for type checking (mypy, pyright) and can be accessed at runtime via `typing.get_type_hints()`. The `__class_getitem__` method is called at subscript time, not at instance creation time, so there is no runtime overhead.

The interaction with inheritance: generic dataclasses can inherit from other generic classes. `@dataclass class IntWrapper(Wrapper[int]): pass` specializes `Wrapper[int]` and creates a non-generic class. The `__class_getitem__` method is called when the class is subscripted, and the generic alias is cached for reuse. The practical recommendation is to use `Generic[T]` with dataclasses for type-safe containers and value types.

**Example:**
```python
from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar('T')
K = TypeVar('K')

@dataclass
class Pair(Generic[T]):
    first: T
    second: T

@dataclass
class KeyValue(Generic[K, T]):
    key: K
    value: T

p = Pair[int](1, 2)
kv = KeyValue[str, int]("count", 42)
print(p, kv)
```

## Q60: How do dataclasses interact with `__init_subclass__` for automatic field validation?

**A:** `__init_subclass__` can be used to automatically validate dataclass fields at class definition time. The hook is called after the `@dataclass` decorator processes the class, so `cls.__dataclass_fields__` is available for inspection. You can check field types, default values, or required fields and raise `TypeError` if constraints are violated. This provides compile-time-like validation for dataclass hierarchies.

The practical application: a base dataclass can enforce that all subclasses have specific fields with specific types. For example, `@dataclass class BaseModel: def __init_subclass__(cls, **kwargs): super().__init_subclass__(**kwargs); if 'id' not in cls.__dataclass_fields__: raise TypeError("Subclass must have 'id' field")`. When `@dataclass class User(BaseModel): name: str` is defined (without `id`), `TypeError` is raised.

The interaction with MRO: `__init_subclass__` is called for each class in the MRO. If the base class defines validation, it is applied to all subclasses. The validation can be conditional: `def __init_subclass__(cls, validate=True, **kwargs): super().__init_subclass__(**kwargs); if validate: ...`. This allows some subclasses to opt out of validation. The practical recommendation is to use `__init_subclass__` for simple validation (field presence, type checks) and `__post_init__` for runtime validation (value ranges, consistency checks).

**Example:**
```python
from dataclasses import dataclass, fields

@dataclass
class ValidatedModel:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, '__dataclass_fields__'):
            for f in fields(cls):
                if f.name.startswith('_'):
                    raise TypeError(f"Field {f.name} cannot start with '_'")

@dataclass
class User(ValidatedModel):
    name: str
    age: int

# @dataclass
# class Bad(ValidatedModel):
#     _secret: str  # TypeError: Field _secret cannot start with '_'
```

## Q61: What is the difference between `@dataclass` and `@dataclass(order=True)`?

**A:** `@dataclass(order=True)` generates comparison methods (`__lt__`, `__le__`, `__gt__`, `__ge__`) in addition to `__eq__`. These methods compare instances field-by-field, in the order the fields are defined. `@dataclass` without `order=True` (the default) does not generate comparison methods, so instances cannot be compared with `<`, `>`, etc. (attempting to do so raises `TypeError`). The `order=True` parameter enables sorting and comparison of dataclass instances.

The practical usage: `@dataclass(order=True) class Event: timestamp: float; name: str`. This enables `Event(1.0, "a") < Event(2.0, "b")` (compares `timestamp` first, then `name`). The comparison follows the field definition order: `timestamp` is compared first, then `name` if `timestamp` values are equal. This is consistent with tuple comparison semantics. The `order=True` parameter is useful for events, records, and any data that needs to be sorted.

The interaction with `field(compare=False)`: fields with `compare=False` are excluded from comparison methods. For example, `@dataclass(order=True) class Event: timestamp: float; name: str; id: int = field(compare=False)`. The comparison ignores `id` and only compares `timestamp` and `name`. This is useful for fields that should not affect ordering (like auto-generated IDs or timestamps that are not part of the logical ordering).

**Example:**
```python
from dataclasses import dataclass, field

@dataclass(order=True)
class Event:
    timestamp: float
    name: str
    id: int = field(compare=False)

events = [
    Event(2.0, "b", 2),
    Event(1.0, "a", 1),
    Event(1.0, "b", 3),
]
events.sort()
print(events)
# [Event(1.0, 'a', 1), Event(1.0, 'b', 3), Event(2.0, 'b', 2)]
```

## Q62: How does `super()` work with `@classmethod` in cooperative inheritance?

**A:** `super()` in class methods works the same as in instance methods, but the second argument is the class instead of the instance. In Python 3, `super()` without arguments is equivalent to `super(CurrentClass, cls)` in a classmethod. It returns a proxy that delegates to the next class in the MRO, bound to the class. When you call `super().classmethod_method()`, it calls the classmethod on the next class in the MRO, passing the original class (or the derived class, depending on the binding).

The practical example: `class B(A): @classmethod def create(cls): result = super().create(); return cls(result)`. When `B.create()` is called, `super()` delegates to `A.create()`, passing `B` as the class. If `A.create()` uses `cls` to construct an instance, it constructs a `B` instance (because `cls` is `B`). This is the cooperative inheritance pattern applied to classmethods.

The interaction with MRO: the `super()` proxy uses the MRO to find the next class, same as in instance methods. The classmethod is called on the next class in the MRO, with the derived class as `cls`. This enables classmethods to cooperate across the hierarchy, each contributing to the construction or initialization process. The practical recommendation is to use `super()` in classmethods for cooperative inheritance, and to document the expected MRO position for classes in the hierarchy.

**Example:**
```python
class Base:
    _registry = {}
    
    @classmethod
    def register(cls, name):
        cls._registry[name] = cls
        return cls

class PluginA(Base):
    @classmethod
    def register(cls, name):
        super().register(name)
        print(f"PluginA registered: {name}")
        return cls

class PluginB(Base):
    @classmethod
    def register(cls, name):
        super().register(name)
        print(f"PluginB registered: {name}")
        return cls

class Combined(PluginA, PluginB):
    pass

Combined.register("combined")
# PluginA registered: combined
# PluginB registered: combined
```

## Q63: What are the implications of using `__post_init__` with `InitVar` in inheritance?

**A:** `InitVar` fields are passed to `__post_init__` as keyword arguments. In inheritance, `InitVar` fields from all classes are collected and passed to `__post_init__`. The `__post_init__` method must accept these arguments (via `*args`, `**kwargs`, or explicit parameters). If a `InitVar` field is defined in both parent and child, the child's `InitVar` overrides the parent's (same name). The `InitVar` field is not stored as an instance attribute — it is only available during `__init__` and `__post_init__`.

The practical implication: `InitVar` fields are not accessible after `__init__` and `__post_init__` complete. They are temporary parameters for initialization. In inheritance, `InitVar` fields from all classes are passed to `__post_init__`. If the parent defines `InitVar[str] = "default"` and the child defines `InitVar[int] = 0`, both are passed to `__post_init__` as keyword arguments. The `__post_init__` method must accept both.

The practical recommendation is to use `InitVar` for parameters that affect initialization but should not be stored. Common use cases: debug flags, configuration overrides, environment-specific settings. In inheritance, be careful with `InitVar` names — name collisions between parent and child can cause unexpected behavior. Use unique names or namespaces to avoid conflicts. The `InitVar` feature is useful for separating initialization parameters from stored data.

**Example:**
```python
from dataclasses import dataclass, InitVar

@dataclass
class Base:
    name: str
    debug: InitVar[bool] = False
    
    def __post_init__(self, debug):
        if debug:
            print(f"Base initialized: {self.name}")

@dataclass
class Child(Base):
    age: int
    verbose: InitVar[bool] = False
    
    def __post_init__(self, debug, verbose):
        super().__post_init__(debug)
        if verbose:
            print(f"Child initialized: {self.name}, {self.age}")

c = Child("Alice", 30, debug=True, verbose=True)
# Base initialized: Alice
# Child initialized: Alice, 30
```

## Q64: How do dataclasses handle `__reduce__` and pickling?

**A:** Dataclasses do not generate `__reduce__` or `__reduce_ex__` methods by default. The default pickling behavior (inherited from `object`) uses `__dict__` for non-slotted classes and may fail for slotted classes. For pickling to work correctly with slotted dataclasses, you may need to implement `__reduce__` or `__getstate__`/`__setstate__` methods. The `@dataclass` decorator does not generate these methods because the default behavior is usually sufficient for non-slotted classes.

The practical implication: non-slotted dataclasses are picklable by default (they use `__dict__` for state). Slotted dataclasses may not be picklable without custom implementation. The `__reduce__` method should return a tuple `(callable, args)` that recreates the object. The `__getstate__`/`__setstate__` methods provide more control over what is pickled and how it is restored.

The recommendation is to test pickling with your dataclasses before relying on it. For simple dataclasses (fields are picklable types), the default behavior is correct. For complex dataclasses (fields contain non-picklable types, custom objects, or slotted attributes), implement `__reduce__` or `__getstate__`/`__setstate__`. The `dataclasses` module does not provide pickling helpers because the requirements vary widely across use cases.

**Example:**
```python
import pickle
from dataclasses import dataclass, field

@dataclass
class Point:
    x: float
    y: float

p = Point(1.0, 2.0)
data = pickle.dumps(p)
p2 = pickle.loads(data)
print(p2)  # Point(x=1.0, y=2.0)

# Slotted dataclass — needs custom pickling
@dataclass(slots=True)
class SlottedPoint:
    x: float
    y: float
    
    def __reduce__(self):
        return (self.__class__, (self.x, self.y))

sp = SlottedPoint(3.0, 4.0)
data = pickle.dumps(sp)
sp2 = pickle.loads(data)
print(sp2)  # SlottedPoint(x=3.0, y=4.0)
```

## Q65: What is the role of `__set_name__` in descriptors used with dataclasses?

**A:** `__set_name__` is called on descriptors when the class is created. In the context of dataclasses, it allows descriptors to know their attribute name within the class. This is useful for descriptors that need to generate storage keys, validation messages, or database column names based on the attribute name. The `@dataclass` decorator processes the fields after `__set_name__` is called, so the descriptor's name is set before `__init__` is generated.

The practical application: a validated field descriptor can use the name in error messages: `class PositiveInt: def __set_name__(self, owner, name): self.name = name; def __set__(self, instance, value): if value <= 0: raise ValueError(f"{self.name} must be positive")`. When the dataclass is defined, `__set_name__` is called with the attribute name, and the descriptor stores it for use in `__set__`.

The interaction with dataclasses: the `@dataclass` decorator treats descriptors as fields (if they have type annotations). The descriptor's `__set_name__` is called during class creation, before `@dataclass` processes the fields. The descriptor can then perform validation, transformation, or logging when the field is set. This pattern combines descriptors with dataclasses for custom field behavior without subclassing `field()`.

**Example:**
```python
from dataclasses import dataclass

class Validated:
    def __set_name__(self, owner, name):
        self.name = name
    
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.name} must be str, got {type(value).__name__}")
        instance.__dict__[self.name] = value
    
    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

@dataclass
class User:
    name: Validated = Validated()
    email: Validated = Validated()

u = User(name="Alice", email="alice@example.com")
# User(name=123, email="test")  # TypeError: name must be str
```

## Q66: How does the MRO affect `__str__` and `__repr__` resolution?

**A:** The MRO determines which `__str__` or `__repr__` method is called when `str()` or `repr()` is used on an instance. Python searches the MRO for `__str__` (or `__repr__`) and calls the first one found. If no class in the MRO defines `__str__`, Python falls back to `object.__str__` (which calls `__repr__`). If no class defines `__repr__`, `object.__repr__` is used (which returns `<ClassName object at address>`).

The practical implication is that `__str__` and `__repr__` follow the same resolution rules as any other method. In a multiple inheritance hierarchy, the leftmost class in the MRO that defines `__str__` (or `__repr__`) is used. This can be surprising if the MRO order is not what the programmer expects. The recommendation is to define `__str__` and `__repr__` explicitly in each class that needs custom string representation, rather than relying on inheritance.

The interaction with dataclasses: the `@dataclass` decorator generates `__repr__` (by default), which is placed in the class's namespace. This means the dataclass's `__repr__` is found before any parent's `__repr__` in the MRO. The generated `__repr__` includes all fields (inherited and own), providing a complete representation. The `repr` parameter of `@dataclass` and `field(repr=False)` control which fields are included.

**Example:**
```python
class A:
    def __repr__(self):
        return "A"

class B(A):
    def __repr__(self):
        return "B"

class C(A):
    pass

class D(B, C):
    pass

print(repr(D()))  # "B" — B's __repr__ is first in MRO
```

## Q67: What is the difference between `@dataclass` and `@dataclass(frozen=True)` in terms of hashability?

**A:** `@dataclass` (with `eq=True`, the default) sets `__hash__` to `None`, making instances unhashable. `@dataclass(frozen=True)` generates `__hash__` based on all fields, making instances hashable. The difference is critical for using dataclass instances as dictionary keys or in sets. A frozen dataclass with `eq=True` is both value-comparable (via `__eq__`) and hashable (via `__hash__`), which is the correct behavior for immutable value types.

The practical implication: `@dataclass class Point: x: float; y: float` — `Point(1, 2)` cannot be used as a dictionary key (unhashable). `@dataclass(frozen=True) class Point: x: float; y: float` — `Point(1, 2)` can be used as a dictionary key (hashable). The `frozen=True` parameter makes the instance immutable and hashable, which is essential for value types that need to be used in sets or as dictionary keys.

The `unsafe_hash=True` parameter generates `__hash__` even for mutable dataclasses, but this is dangerous: if a field is modified after insertion in a set, the set's internal hash table is corrupted. The recommendation is to use `frozen=True` for hashable dataclasses and avoid `unsafe_hash=True`. The `eq=False` option uses `object.__hash__` (identity-based), which is correct for identity-based objects but not for value types.

**Example:**
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class ImmutablePoint:
    x: float
    y: float

p1 = ImmutablePoint(1.0, 2.0)
p2 = ImmutablePoint(1.0, 2.0)
print(p1 == p2)  # True — value equality
print(hash(p1) == hash(p2))  # True — same hash
d = {p1: "origin"}  # Works — hashable

# @dataclass
# class MutablePoint:
#     x: float
#     y: float
# d = {MutablePoint(1, 2): "origin"}  # TypeError: unhashable type
```

## Q68: How do dataclasses handle `__init_subclass__` with `**kwargs` forwarding?

**A:** When `__init_subclass__` receives `**kwargs`, those kwargs must be forwarded via `super().__init_subclass__(**kwargs)` to avoid losing them. If a class consumes a kwarg (by popping it from `kwargs` or by not forwarding it), subsequent classes in the MRO do not receive it. This is the cooperative pattern applied to `__init_subclass__`: each class does its part and delegates the rest.

The practical application: a base class can accept `plugin_name` as a kwarg and forward it: `class Base: def __init_subclass__(cls, plugin_name=None, **kwargs): super().__init_subclass__(**kwargs); if plugin_name: registry[plugin_name] = cls`. If `plugin_name` is popped from `kwargs` before forwarding, subsequent classes do not receive it. If it is forwarded (not popped), subsequent classes can also use it. The convention is to accept specific kwargs by name and forward the rest via `**kwargs`.

The interaction with `@dataclass`: `__init_subclass__` kwargs are passed from the class definition. For `@dataclass class User(Base, plugin_name="user")`, `plugin_name="user"` is passed to `Base.__init_subclass__`. The `@dataclass` decorator does not interfere with `__init_subclass__` kwargs — they are separate from field definitions. The practical recommendation is to document the expected kwargs for `__init_subclass__` and to forward unknown kwargs via `super().__init_subclass__(**kwargs)`.

**Example:**
```python
class PluginBase:
    _registry = {}
    
    def __init_subclass__(cls, plugin_name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if plugin_name:
            PluginBase._registry[plugin_name] = cls

class AuthPlugin(PluginBase, plugin_name="auth"):
    pass

class CachePlugin(PluginBase, plugin_name="cache"):
    pass

print(PluginBase._registry)
# {'auth': AuthPlugin, 'cache': CachePlugin}
```

## Q69: What is the role of `__init_subclass__` in metaclass-free class registration?

**A:** `__init_subclass__` provides a simpler alternative to metaclasses for class registration. Instead of defining a custom metaclass that registers subclasses, you can define `__init_subclass__` in the base class to register each subclass automatically. This is simpler, more readable, and avoids the complexity of metaclasses. The `__init_subclass__` hook is called for every subclass, so registration is automatic and consistent.

The practical application: `class PluginBase: _registry = {}; def __init_subclass__(cls, **kwargs): super().__init_subclass__(**kwargs); PluginBase._registry[cls.__name__] = cls`. Every subclass is automatically registered in `_registry`. This is the standard pattern for plugin systems, factory registries, and class hierarchies that need to track all subclasses.

The advantage over metaclasses: `__init_subclass__` is defined in the base class, not in a separate metaclass. This makes the registration logic co-located with the class definition, improving readability. `__init_subclass__` is also simpler to use: no need to define `__new__` or `__init__` in the metaclass. The practical recommendation is to use `__init_subclass__` for class registration (simpler, more readable) and metaclasses for more complex class creation logic (custom `__new__`, `__init__`, `__prepare__`).

**Example:**
```python
class PluginBase:
    _plugins = {}
    
    def __init_subclass__(cls, plugin_type=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if plugin_type:
            PluginBase._plugins[plugin_type] = cls
    
    @classmethod
    def get_plugin(cls, plugin_type):
        return cls._plugins.get(plugin_type)

class AuthPlugin(PluginBase, plugin_type="auth"):
    pass

class CachePlugin(PluginBase, plugin_type="cache"):
    pass

auth = PluginBase.get_plugin("auth")()
print(type(auth))  # <class 'AuthPlugin'>
```

## Q70: How do dataclasses handle `__copy__` with inherited fields?

**A:** The default `copy.copy` behavior for non-slotted dataclasses copies the instance's `__dict__`, which includes all inherited and own fields. This produces a shallow copy: all field values are shared between the original and the copy. For fields that are mutable objects (lists, dicts, nested dataclasses), the copy shares the same mutable objects. This can lead to unexpected behavior if one instance modifies a shared mutable field.

The practical implication: `copy.copy` on a non-slotted dataclass produces a shallow copy with shared field values. `copy.deepcopy` produces a deep copy with independent field values. For slotted dataclasses, the default copy behavior may not work correctly (no `__dict__` to copy), so custom `__copy__`/`__deepcopy__` methods may be needed.

The recommendation is to use `copy.deepcopy` for dataclasses with mutable fields (nested dataclasses, lists, dicts) to avoid shared state. For immutable fields (int, str, float, tuples of immutables), `copy.copy` is sufficient. The `@dataclass` decorator does not generate `__copy__`/`__deepcopy__` methods because the default behavior is usually sufficient. If you need custom copy behavior, implement `__copy__` and `__deepcopy__` explicitly.

**Example:**
```python
import copy
from dataclasses import dataclass, field

@dataclass
class Address:
    city: str

@dataclass
class User:
    name: str
    address: Address
    tags: list = field(default_factory=list)

u1 = User("Alice", Address("NYC"), ["admin"])
u2 = copy.copy(u1)  # Shallow copy
u3 = copy.deepcopy(u1)  # Deep copy

u1.address.city = "LA"
print(u2.address.city)  # "LA" — shared address!
print(u3.address.city)  # "NYC" — independent copy
```

## Q71: What is the difference between `@dataclass` and `@dataclass(slots=True)` in terms of pickling?

**A:** Non-slotted dataclasses are picklable by default (they use `__dict__` for state). Slotted dataclasses may not be picklable without custom implementation. The default pickling behavior uses `__dict__`, which does not exist for slotted classes. To pickle slotted dataclasses, you must implement `__reduce__` or `__getstate__`/`__setstate__` methods that handle the slotted state.

The practical implication: `@dataclass class Point: x: float; y: float` is picklable by default. `@dataclass(slots=True) class Point: x: float; y: float` is not picklable without custom implementation. The `__reduce__` method should return a tuple `(callable, args)` that recreates the object. The `__getstate__`/`__setstate__` methods provide more control over what is pickled and how it is restored.

The recommendation is to test pickling with slotted dataclasses before relying on it. For simple slotted dataclasses (fields are picklable types), the `__reduce__` method is straightforward: `def __reduce__(self): return (self.__class__, (self.x, self.y))`. For complex slotted dataclasses (nested objects, custom types), implement `__getstate__`/`__setstate__` for full control. The `dataclasses` module does not provide pickling helpers because the requirements vary widely.

**Example:**
```python
import pickle
from dataclasses import dataclass

@dataclass(slots=True)
class Point:
    x: float
    y: float
    
    def __reduce__(self):
        return (self.__class__, (self.x, self.y))

p = Point(1.0, 2.0)
data = pickle.dumps(p)
p2 = pickle.loads(data)
print(p2)  # Point(x=1.0, y=2.0)
```

## Q72: How does `__init_subclass__` interact with `__set_name__` in descriptor-based dataclasses?

**A:** `__set_name__` is called on descriptors when the class is created, before `__init_subclass__` is called. The order of operations is: (1) class body is executed, (2) `__set_name__` is called on all descriptors, (3) `__init_subclass__` is called (via the metaclass). This means descriptors know their names before `__init_subclass__` runs, so `__init_subclass__` can inspect descriptor-based fields.

The practical application: a base class can use `__init_subclass__` to validate descriptor-based fields. Since descriptors have already been named (via `__set_name__`), `__init_subclass__` can check that all required descriptors are present and correctly configured. For example, `def __init_subclass__(cls, **kwargs): super().__init_subclass__(**kwargs); for name, obj in vars(cls).items(): if isinstance(obj, ValidatedField): ...`.

The interaction with `@dataclass`: descriptors are processed during class creation (before `@dataclass`). `__set_name__` is called on each descriptor, giving it the attribute name. Then `@dataclass` processes the fields (including descriptor-based fields). Then `__init_subclass__` is called, allowing validation of the fully-processed class. This order ensures that descriptors, `@dataclass`, and `__init_subclass__` work together correctly.

**Example:**
```python
from dataclasses import dataclass

class Validated:
    def __set_name__(self, owner, name):
        self.name = name
        print(f"Descriptor named: {name}")
    
    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

@dataclass
class Base:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        print(f"Subclass created: {cls.__name__}")

@dataclass
class Child(Base):
    x: Validated = Validated()
    y: Validated = Validated()
# Output: Descriptor named: x -> Descriptor named: y -> Subclass created: Child
```

## Q73: What are the best practices for designing cooperative multiple inheritance hierarchies?

**A:** Best practices for cooperative multiple inheritance: (1) Use `*args` and `**kwargs` in method signatures for flexibility. (2) Always call `super()` at the beginning or end of each method (be consistent). (3) Keep hierarchies shallow (2-3 levels deep). (4) Document the expected MRO position for each class. (5) Test classes in isolation and in combination. (6) Use `__init_subclass__` to validate the hierarchy at definition time. (7) Prefer composition over inheritance when classes are independent.

(8) Use mixins for cross-cutting concerns (logging, validation, serialization). (9) Keep mixins focused (one behavior per mixin). (10) Avoid mixins with state (use `__init__` only if necessary, and call `super().__init__()`). (11) Use type hints and `typing.Protocol` to document expected interfaces. (12) Prefer `@dataclass` for data containers (reduces boilerplate). (13) Use `frozen=True` for immutable value types. (14) Test the MRO with `cls.__mro__` to verify the expected ordering.

(15) Avoid mixing cooperative inheritance with explicit base class calls (they can conflict). (16) Use `__init_subclass__` or metaclasses for framework-level validation. (17) Document the expected behavior of each class in the hierarchy (what it contributes, what it delegates). (18) Use `super().__init_subclass__(**kwargs)` to maintain the hook chain. (19) Prefer Python 3's `super()` (without arguments) over Python 2's `super(ClassName, self)`. (20) Test for `TypeError` from the C3 linearization algorithm — it indicates an inconsistent hierarchy.

**Example:**
```python
class Mixin:
    """Good mixin: focused, stateless, calls super()"""
    def process(self, *args, **kwargs):
        result = super().process(*args, **kwargs)
        return result

class Base:
    def process(self, *args, **kwargs):
        return "processed"

class Service(Mixin, Base):
    pass

s = Service()
print(s.process())  # "processed"
```

## Q74: How do dataclasses handle `__sizeof__` with `__slots__`?

**A:** For slotted dataclasses (`slots=True`), `sys.getsizeof` returns the base object size plus the size of the slots (fixed-size memory for each field). For non-slotted dataclasses, `sys.getsizeof` returns the base object size plus the `__dict__` overhead (which includes space for future attributes). The `__sizeof__` method (inherited from `object`) provides the base size, and `sys.getsizeof` adds the `__dict__` size (if present).

The practical comparison: `sys.getsizeof(SlottedPoint(1.0, 2.0))` returns approximately 40 bytes (base object + 2 float slots). `sys.getsizeof(RegularPoint(1.0, 2.0))` returns approximately 48 bytes (base object + `__dict__` pointer), plus `sys.getsizeof(regular.__dict__)` which is approximately 64 bytes. Total for non-slotted: ~112 bytes. Total for slotted: ~40 bytes. The slotted version uses roughly 64% less memory.

The recommendation is to use `slots=True` for dataclasses with many instances. The memory savings are significant and measurable with `sys.getsizeof`. For accurate deep size measurement (including referenced objects), use `pympler.asizeof.asizeof`. The `__sizeof__` method can be overridden for custom memory reporting, but this is rarely needed for dataclasses.

**Example:**
```python
import sys
from dataclasses import dataclass

@dataclass
class Regular:
    x: float
    y: float
    z: float

@dataclass(slots=True)
class Slotted:
    x: float
    y: float
    z: float

r = Regular(1.0, 2.0, 3.0)
s = Slotted(1.0, 2.0, 3.0)
print(f"Regular: {sys.getsizeof(r)} + dict: {sys.getsizeof(r.__dict__)}")
print(f"Slotted: {sys.getsizeof(s)}")
# Regular: 56 + dict: 96 = ~152 bytes
# Slotted: 48 bytes
```

## Q75: What is the role of `__init_subclass__` in automatic MRO validation?

**A:** `__init_subclass__` can validate the MRO at class definition time. By inspecting `cls.__mro__`, you can check that the class hierarchy has the expected ordering, that required classes are present, or that certain classes come before others. This provides compile-time-like validation for class hierarchies, catching MRO issues at definition time instead of runtime.

The practical application: a base class can enforce that all subclasses have a specific class in their MRO: `def __init_subclass__(cls, **kwargs): super().__init_subclass__(**kwargs); if not any(issubclass(m, SomeMixin) for m in cls.__mro__): raise TypeError(f"{cls.__name__} must inherit from SomeMixin")`. This ensures that all subclasses include a specific mixin in their hierarchy.

The interaction with `@dataclass`: `__init_subclass__` is called after `@dataclass` processes the class, so `cls.__mro__` and `cls.__dataclass_fields__` are both available. You can validate both the MRO and the fields in `__init_subclass__`. The practical recommendation is to use `__init_subclass__` for simple MRO validation (class presence, ordering) and metaclasses for complex MRO manipulation (reordering, merging).

**Example:**
```python
from dataclasses import dataclass

class RequiresAuth:
    pass

class SecureBase:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not any(issubclass(m, RequiresAuth) for m in cls.__mro__ if m is not object):
            raise TypeError(f"{cls.__name__} must inherit from RequiresAuth")

@dataclass
class SecureModel(SecureBase, RequiresAuth):
    token: str

# @dataclass
# class InsecureModel(SecureBase):
#     data: str  # TypeError: InsecureModel must inherit from RequiresAuth
```
## Q76: How does `__init_subclass__` interact with `@dataclass` field defaults?

**A:** `__init_subclass__` is called after `@dataclass` processes the class, so `cls.__dataclass_fields__` is available for inspection. You can check field defaults, types, and other metadata. The field defaults are already resolved at this point — `Field.default` and `Field.default_factory` are set. This allows `__init_subclass__` to validate that fields have correct defaults, that required fields exist, or that field types match constraints.

The practical application: a base dataclass can enforce that all subclasses have a `name` field with a string type: `def __init_subclass__(cls, **kwargs): super().__init_subclass__(**kwargs); if 'name' not in cls.__dataclass_fields__: raise TypeError("Subclass must have 'name' field")`. The validation happens at class definition time, catching errors early.

The interaction with `field(default=...)`: `__init_subclass__` can check that fields have defaults. For example, `def __init_subclass__(cls, **kwargs): super().__init_subclass__(**kwargs); for name, field in cls.__dataclass_fields__.items(): if field.default is MISSING and field.default_factory is MISSING: raise TypeError(f"Field {name} must have a default value")`. This ensures that all fields have defaults, which is useful for configuration classes.

**Example:**
```python
from dataclasses import dataclass, fields

@dataclass
class ValidatedBase:
    def __init_subclass__(cls, required_fields=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if required_fields:
            field_names = {f.name for f in fields(cls)}
            for req in required_fields:
                if req not in field_names:
                    raise TypeError(f"{cls.__name__} must have '{req}' field")

@dataclass
class User(ValidatedBase, required_fields=['name', 'email']):
    name: str
    email: str
    age: int = 0

# @dataclass
# class Bad(ValidatedBase, required_fields=['name']):
#     age: int  # TypeError: Bad must have 'name' field
```

## Q77: What is the difference between `@dataclass` and `@dataclass(eq=True, order=True)`?

**A:** `@dataclass(eq=True, order=True)` generates both `__eq__` (for equality comparison) and ordering methods (`__lt__`, `__le__`, `__gt__`, `__ge__`). `@dataclass(eq=True)` (the default) generates only `__eq__`. The `order=True` parameter enables sorting and comparison of dataclass instances. The comparison methods compare fields in definition order, consistent with tuple comparison semantics.

The practical usage: `@dataclass(order=True) class Event: timestamp: float; name: str` enables `Event(1.0, "a") < Event(2.0, "b")` and `sorted(events)`. Without `order=True`, the `<` operator raises `TypeError`. The `order=True` parameter is useful for records that need to be sorted (events, log entries, time series). The `eq=True` parameter is useful for value comparison (checking if two records are equal).

The interaction with `field(compare=False)`: fields with `compare=False` are excluded from both `__eq__` and ordering methods. This provides fine-grained control over which fields affect equality and ordering. The practical recommendation is to use `order=True` for sortable records and `eq=True` (default) for value comparison. Both parameters can be used together: `@dataclass(eq=True, order=True)`.

**Example:**
```python
from dataclasses import dataclass, field

@dataclass(order=True)
class Event:
    timestamp: float
    name: str
    id: int = field(compare=False)

events = [
    Event(2.0, "b", 2),
    Event(1.0, "a", 1),
    Event(1.0, "b", 3),
]
print(min(events))  # Event(1.0, 'a', 1)
print(max(events))  # Event(2.0, 'b', 2)
```

## Q78: How do dataclasses handle `__init_subclass__` with `InitVar` fields?

**A:** `InitVar` fields are not part of `cls.__dataclass_fields__` — they are separate metadata stored in `cls.__dataclass_params__`. `__init_subclass__` can inspect `cls.__dataclass_params__` to find `InitVar` fields. The `InitVar` fields are passed to `__post_init__` as keyword arguments, not stored as instance attributes. This makes `InitVar` useful for parameters that affect initialization but should not be stored.

The practical application: `def __init_subclass__(cls, **kwargs): super().__init_subclass__(**kwargs); init_vars = [f.name for f in cls.__dataclass_params__.init_vars]`. This allows `__init_subclass__` to inspect `InitVar` fields and validate them. The `InitVar` fields are not in `__dataclass_fields__` because they are not instance attributes — they are temporary parameters.

The interaction with inheritance: `InitVar` fields from all classes in the hierarchy are collected and passed to `__post_init__`. If a parent and child both define `InitVar` fields, both are passed to `__post_init__`. The `__post_init__` method must accept these arguments (via `*args`, `**kwargs`, or explicit parameters). `__init_subclass__` can validate that `InitVar` fields are correctly named and typed.

**Example:**
```python
from dataclasses import dataclass, InitVar

@dataclass
class Base:
    name: str
    debug: InitVar[bool] = False
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        init_vars = [f.name for f in cls.__dataclass_params__.init_vars]
        print(f"{cls.__name__} InitVars: {init_vars}")

@dataclass
class Child(Base):
    age: int
    verbose: InitVar[bool] = False
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
# Output: Child InitVars: ['verbose']
```

## Q79: What is the role of `__init_subclass__` in framework-level class validation?

**A:** `__init_subclass__` provides a framework-level hook for validating class definitions at class creation time. Frameworks use it to enforce constraints on subclasses: required methods, required attributes, valid configurations, and correct inheritance patterns. The validation happens at class definition time, catching errors early and providing clear error messages. This is simpler and more readable than metaclasses for many use cases.

The practical application: a web framework can use `__init_subclass__` to validate that all route handlers have a `path` attribute: `class Route: def __init_subclass__(cls, path=None, **kwargs): super().__init_subclass__(**kwargs); if path: cls.path = path`. A data framework can validate that all models have a primary key field. A plugin framework can validate that all plugins implement a `process` method.

The interaction with `@dataclass`: `__init_subclass__` can validate both the class hierarchy and the dataclass fields. The hook is called after `@dataclass` processes the class, so all field metadata is available. The practical recommendation is to use `__init_subclass__` for simple validation (field presence, type checks, method presence) and metaclasses for complex class creation logic (custom `__new__`, `__init__`, `__prepare__`).

**Example:**
```python
from dataclasses import dataclass, fields

class ModelBase:
    def __init_subclass__(cls, table_name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if table_name:
            cls._table_name = table_name
        if hasattr(cls, '__dataclass_fields__'):
            if not any(f.name == 'id' for f in fields(cls)):
                raise TypeError(f"{cls.__name__} must have an 'id' field")

@dataclass
class User(ModelBase, table_name='users'):
    id: int
    name: str
    email: str

@dataclass
class Post(ModelBase, table_name='posts'):
    id: int
    title: str
    body: str

print(User._table_name)  # 'users'
```

## Q80: How does Python's MRO handle classes defined with `exec` or `type()`?

**A:** Classes created with `type()` or `exec` follow the same MRO rules as classes created with `class` statements. `type(name, bases, dict)` creates a class with the given name, bases, and namespace. The MRO is computed by the C3 linearization algorithm, same as for regular classes. `exec("class C(A, B): pass")` also follows the same rules — the MRO is computed when the class statement is executed.

The practical implication is that dynamically created classes can participate in multiple inheritance hierarchies. `D = type('D', (B, C), {'method': lambda self: 'D'})` creates a class `D` with bases `B` and `C`, and the MRO is computed correctly. This is useful for metaprogramming, dynamic class generation, and plugin systems. The MRO is always computed, regardless of how the class is created.

The interaction with `__init_subclass__`: `__init_subclass__` is called when the class is created via `type()`, same as with `class` statements. This allows hooks to validate dynamically created classes. The practical recommendation is to treat dynamically created classes the same as regular classes — the MRO and `__init_subclass__` work identically.

**Example:**
```python
class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B"

class C(A):
    def method(self):
        return "C"

# Dynamic class creation
D = type('D', (B, C), {'extra': 42})
print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
print(D().method())  # "B"
print(D().extra)  # 42
```

## Q81: What is the role of `__init_subclass__` in plugin systems?

**A:** `__init_subclass__` is the standard hook for implementing plugin systems in Python. When a plugin class is defined (inheriting from a base class), `__init_subclass__` automatically registers it in a plugin registry. This eliminates the need for manual registration — simply defining a subclass of the plugin base class is enough. The registry can be used for discovery, instantiation, and configuration of plugins.

The practical application: `class PluginBase: _plugins = {}; def __init_subclass__(cls, **kwargs): super().__init_subclass__(**kwargs); PluginBase._plugins[cls.__name__] = cls`. When `class MyPlugin(PluginBase): pass` is defined, `MyPlugin` is automatically registered. The plugin system can then discover and instantiate plugins by name. This pattern is used in frameworks (Django, Flask, SQLAlchemy), testing tools (pytest plugins), and application architectures (microservices, modular systems).

The interaction with `@dataclass`: dataclass plugins are registered automatically via `__init_subclass__`. The `@dataclass` decorator generates `__init__`, `__repr__`, etc., and `__init_subclass__` registers the plugin. This combines the convenience of dataclasses with the automatic registration of `__init_subclass__`. The practical recommendation is to use `__init_subclass__` for plugin registration (simple, automatic) and metaclasses for more complex plugin creation logic.

**Example:**
```python
from dataclasses import dataclass

class PluginBase:
    _registry = {}
    
    def __init_subclass__(cls, plugin_name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        name = plugin_name or cls.__name__
        PluginBase._registry[name] = cls
    
    @classmethod
    def create(cls, name, **kwargs):
        return cls._registry[name](**kwargs)

@dataclass
class AuthPlugin(PluginBase, plugin_name="auth"):
    token: str

@dataclass
class CachePlugin(PluginBase, plugin_name="cache"):
    ttl: int = 300

auth = PluginBase.create("auth", token="abc123")
cache = PluginBase.create("cache", ttl=60)
print(auth, cache)
```

## Q82: How do dataclasses handle `__init_subclass__` with class variables?

**A:** Class variables (defined without type annotations or with `ClassVar` annotations) are not dataclass fields. They are regular class attributes that `__init_subclass__` can inspect via `vars(cls)` or `cls.__dict__`. `__init_subclass__` can validate class variables, modify them, or add new ones. This is useful for framework-level configuration that should be consistent across all subclasses.

The practical application: `def __init_subclass__(cls, **kwargs): super().__init_subclass__(**kwargs); if not hasattr(cls, '_table_name'): raise TypeError(f"{cls.__name__} must define _table_name")`. This enforces that all subclasses have a `_table_name` class variable. The validation happens at class definition time, catching errors early.

The interaction with `@dataclass`: class variables are not affected by `@dataclass` — they are not fields, not included in `__init__`, `__repr__`, or `__eq__`. `__init_subclass__` can validate both class variables and dataclass fields. The practical recommendation is to use `ClassVar` for class variables (for type checkers) and `__init_subclass__` for validation.

**Example:**
```python
from dataclasses import dataclass
from typing import ClassVar

@dataclass
class BaseModel:
    _counter: ClassVar[int] = 0
    _table_name: ClassVar[str] = ""
    
    def __init_subclass__(cls, table_name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if table_name:
            cls._table_name = table_name
        if not cls._table_name:
            raise TypeError(f"{cls.__name__} must have table_name")

@dataclass
class User(BaseModel, table_name='users'):
    name: str

@dataclass
class Post(BaseModel, table_name='posts'):
    title: str

print(User._table_name, Post._table_name)  # users posts
```

## Q83: What is the difference between `@dataclass` and `@dataclass(repr=False)`?

**A:** `@dataclass(repr=False)` tells the decorator not to generate a `__repr__` method. The class uses whatever `__repr__` is defined in the class body (or inherited from a parent). If no `__repr__` is defined, `object.__repr__` is used (which returns `<ClassName object at address>`). The `repr=False` parameter is useful when you want a custom `__repr__` or when the default `__repr__` is too verbose.

The practical usage: `@dataclass(repr=False) class Secret: password: str; token: str`. This prevents the password and token from appearing in the string representation. You can define a custom `__repr__` that masks sensitive fields: `def __repr__(self): return f"Secret(password='***', token='***')"`. The `repr=False` parameter is useful for classes with sensitive or large fields.

The interaction with `field(repr=False)`: `field(repr=False)` excludes individual fields from the generated `__repr__`. `@dataclass(repr=False)` disables `__repr__` generation entirely. The difference is granularity: `field(repr=False)` is per-field, `@dataclass(repr=False)` is per-class. The practical recommendation is to use `field(repr=False)` for individual sensitive fields and `@dataclass(repr=False)` when you want a completely custom `__repr__`.

**Example:**
```python
from dataclasses import dataclass, field

@dataclass
class User:
    name: str
    password: str = field(repr=False)
    age: int

u = User("Alice", "secret123", 30)
print(repr(u))  # User(name='Alice', age=30)

@dataclass(repr=False)
class Secret:
    data: str
    def __repr__(self):
        return "Secret(***)"

s = Secret("sensitive")
print(repr(s))  # Secret(***)
```

## Q84: How does `__init_subclass__` handle `**kwargs` forwarding in deep hierarchies?

**A:** In deep hierarchies, `**kwargs` must be forwarded through every `__init_subclass__` in the chain. If any class consumes a kwarg without forwarding it, subsequent classes do not receive it. The convention is to accept specific kwargs by name and forward the rest via `**kwargs`. If a class pops a kwarg from `kwargs`, it must not forward it. If a class leaves a kwarg in `kwargs`, it is forwarded to the next class.

The practical example: `class A: def __init_subclass__(cls, x=None, **kwargs): super().__init_subclass__(**kwargs)`. `class B(A): def __init_subclass__(cls, y=None, **kwargs): super().__init_subclass__(**kwargs)`. `class C(B): pass`. When `class D(C, x=1, y=2)` is defined, `x=1` is consumed by `A.__init_subclass__` and `y=2` is consumed by `B.__init_subclass__`. Neither is forwarded to `C` or `D` (because they are consumed).

The interaction with `@dataclass`: `__init_subclass__` kwargs are separate from dataclass fields. The `@dataclass` decorator does not interfere with `__init_subclass__` kwargs. The practical recommendation is to document the expected kwargs for `__init_subclass__` and to forward unknown kwargs via `super().__init_subclass__(**kwargs)`. Use `*` to enforce keyword-only arguments: `def __init_subclass__(cls, *, x=None, **kwargs)`.

**Example:**
```python
class Base:
    def __init_subclass__(cls, *, register=True, **kwargs):
        super().__init_subclass__(**kwargs)
        if register:
            print(f"Registered: {cls.__name__}")

class Middle(Base):
    def __init_subclass__(cls, *, version=1, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._version = version

class Leaf(Middle):
    pass

class Child(Leaf, register=True, version=2):
    pass
# Output: Registered: Child
print(Child._version)  # 2
```

## Q85: What are the performance implications of `__init_subclass__` in dataclass hierarchies?

**A:** `__init_subclass__` is called once per class definition (not per instance creation). The overhead is negligible for most applications — a few microseconds per class definition. The hook runs at import time (when the class statement is executed), so it has no impact on instance creation or method call performance. The practical implication is that `__init_subclass__` can be used freely for validation, registration, and framework hooks without performance concerns.

The interaction with `@dataclass`: the `@dataclass` decorator processes fields and generates methods at class definition time. `__init_subclass__` is called after `@dataclass` completes, so the class is fully formed when the hook runs. The total overhead is the sum of `@dataclass` processing and `__init_subclass__` execution, both of which happen once per class definition. This is a one-time cost, not a per-instance cost.

The recommendation is to use `__init_subclass__` freely for validation and registration. The performance overhead is negligible. If `__init_subclass__` performs expensive operations (network calls, file I/O), consider deferring them to instance creation time (via `__init__` or `__post_init__`). The `__init_subclass__` hook is designed for lightweight, class-definition-time operations.

**Example:**
```python
import timeit

class Base:
    _count = 0
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Base._count += 1

start = timeit.default_timer()
for i in range(1000):
    type(f'Class{i}', (Base,), {})

elapsed = timeit.default_timer() - start
print(f"1000 classes with __init_subclass__: {elapsed:.3f}s")
# Typically < 0.01s — negligible overhead
```

## Q86: How do dataclasses handle `__init_subclass__` with `frozen=True`?

**A:** `__init_subclass__` is called after `@dataclass(frozen=True)` processes the class. The hook can inspect `cls.__dataclass_params__` to check if the class is frozen. The frozen status affects `__setattr__` and `__delattr__` — frozen instances raise `FrozenInstanceError` on attribute modification. `__init_subclass__` can enforce that subclasses are also frozen (or not frozen, depending on the design).

The practical application: `def __init_subclass__(cls, **kwargs): super().__init_subclass__(**kwargs); if not cls.__dataclass_params__.frozen: raise TypeError(f"{cls.__name__} must be frozen")`. This ensures that all subclasses are frozen, maintaining immutability across the hierarchy. The validation happens at class definition time, catching violations early.

The interaction with inheritance: frozen dataclasses can be subclassed, but the subclass must also be frozen (or the parent's `__setattr__` will prevent attribute assignment in the subclass). `__init_subclass__` can enforce this constraint. The practical recommendation is to use `__init_subclass__` to enforce `frozen=True` across a hierarchy when immutability is a design requirement.

**Example:**
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class ImmutableBase:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not cls.__dataclass_params__.frozen:
            raise TypeError(f"{cls.__name__} must be frozen")

@dataclass(frozen=True)
class Child(ImmutableBase):
    x: int
    y: int

c = Child(1, 2)
# c.x = 3  # FrozenInstanceError

# @dataclass
# class MutableChild(ImmutableBase):  # TypeError: must be frozen
#     x: int
```

## Q87: What is the role of `__init_subclass__` in dataclass field renaming?

**A:** `__init_subclass__` cannot rename fields because fields are already defined by the time the hook runs. However, `__init_subclass__` can add aliases, validate field names, or modify field metadata. Field renaming must be done at class definition time (via `field(alias=...)` in Python 3.11+ or manual `__init__` override). `__init_subclass__` is useful for post-definition validation and registration, not for field manipulation.

The practical application: `def __init_subclass__(cls, **kwargs): super().__init_subclass__(**kwargs); for name in cls.__dataclass_fields__: if name.startswith('_'): raise TypeError(f"Field {name} cannot be private")`. This validates field names at class definition time. The hook cannot rename fields, but it can enforce naming conventions.

The interaction with `@dataclass`: fields are defined in the class body and processed by `@dataclass` before `__init_subclass__` is called. The `__init_subclass__` hook can inspect `cls.__dataclass_fields__` for validation but cannot modify field definitions. The practical recommendation is to use `__init_subclass__` for naming validation and `field(alias=...)` (Python 3.11+) for renaming.

**Example:**
```python
from dataclasses import dataclass, fields

@dataclass
class NamingConvention:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for f in fields(cls):
            if not f.name.isidentifier():
                raise TypeError(f"Field {f.name} is not a valid identifier")
            if f.name.startswith('_'):
                raise TypeError(f"Field {f.name} cannot start with '_'")

@dataclass
class User(NamingConvention):
    name: str
    email: str
    age: int

# @dataclass
# class Bad(NamingConvention):
#     'invalid-name': str  # TypeError
```

## Q88: How does `__init_subclass__` interact with `@dataclass` and metaclasses?

**A:** `__init_subclass__` is called by the metaclass (typically `type`) during class creation. If a custom metaclass is used, it calls `__init_subclass__` after the class is created. The order of operations is: (1) metaclass `__new__` creates the class, (2) metaclass `__init__` initializes it, (3) `__init_subclass__` is called on the new class. The `@dataclass` decorator runs before `__init_subclass__` (it is a class decorator, not a metaclass).

The practical implication is that `__init_subclass__` can be used alongside both `@dataclass` and custom metaclasses. The `@dataclass` decorator processes fields and generates methods. The metaclass controls class creation. `__init_subclass__` provides a hook for subclass validation. All three work together in the class creation pipeline. The practical recommendation is to prefer `__init_subclass__` over metaclasses for simple validation (simpler, more readable). Use metaclasses only for complex class creation logic (custom `__new__`, `__init__`, `__prepare__`).

The interaction: `@dataclass` is a class decorator (runs during class definition). `__init_subclass__` is called after the class is created (by the metaclass). A custom metaclass can modify the class before `__init_subclass__` is called. The practical order is: `@dataclass` → metaclass `__new__` → metaclass `__init__` → `__init_subclass__`.

**Example:**
```python
from dataclasses import dataclass

class ValidationMeta(type):
    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super().__new__(mcs, name, bases, namespace, **kwargs)
        print(f"Metaclass created: {name}")
        return cls

@dataclass
class Base(metaclass=ValidationMeta):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        print(f"__init_subclass__: {cls.__name__}")

@dataclass
class Child(Base):
    x: int
# Output: Metaclass created: Base -> __init_subclass__: Child
```

## Q89: What is the difference between `@dataclass` and `@dataclass(init=True)`?

**A:** `@dataclass(init=True)` (the default) generates an `__init__` method. `@dataclass(init=False)` does not generate `__init__`. The difference is straightforward: `init=True` is the default and is rarely changed explicitly. The `init=False` option is useful when you need custom initialization logic that cannot be expressed through simple field defaults.

The practical usage: `@dataclass(init=True) class Point: x: float; y: float` is identical to `@dataclass class Point: x: float; y: float`. The `init=True` parameter is explicit but redundant. The `init=False` option is used when custom initialization is needed: `@dataclass(init=False) class Config: x: int; def __init__(self, **kwargs): ...`.

The interaction with `__post_init__`: `__post_init__` is only called if `init=True` (the generated `__init__` calls `__post_init__`). If `init=False`, `__post_init__` is not called automatically. You must call it manually in your custom `__init__` if needed. The practical recommendation is to use `init=True` (default) for most dataclasses and `init=False` only when custom initialization is required.

**Example:**
```python
from dataclasses import dataclass

@dataclass(init=True)
class PointA:
    x: float
    y: float

@dataclass
class PointB:
    x: float
    y: float

# These are identical:
pa = PointA(1.0, 2.0)
pb = PointB(1.0, 2.0)
print(pa == pb)  # True
```

## Q90: How do dataclasses handle `__init_subclass__` with `order=True`?

**A:** `__init_subclass__` is called after `@dataclass(order=True)` processes the class. The hook can inspect `cls.__dataclass_params__` to check if ordering is enabled. The ordering methods (`__lt__`, `__le__`, `__gt__`, `__ge__`) are already generated when `__init_subclass__` runs. The hook can validate ordering-related constraints (e.g., ensuring that all subclasses have the same ordering fields).

The practical application: `def __init_subclass__(cls, **kwargs): super().__init_subclass__(**kwargs); if cls.__dataclass_params__.order: # validate ordering fields`. This allows framework code to enforce that all subclasses use consistent ordering. The validation happens at class definition time, catching inconsistencies early.

The interaction with `field(compare=False)`: fields with `compare=False` are excluded from ordering methods. `__init_subclass__` can check that certain fields are included in ordering (not `compare=False`). The practical recommendation is to use `__init_subclass__` for ordering validation and `field(compare=False)` for fields that should not affect ordering.

**Example:**
```python
from dataclasses import dataclass, fields

@dataclass(order=True)
class SortedBase:
    def __init_subclass__(cls, sort_by=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if sort_by:
            cls._sort_by = sort_by
            compare_fields = [f.name for f in fields(cls) if f.compare]
            if sort_by not in compare_fields:
                raise TypeError(f"sort_by '{sort_by}' must be a compare field")

@dataclass(order=True)
class Event(SortedBase, sort_by='timestamp'):
    timestamp: float
    name: str
    id: int = None

e1 = Event(2.0, "b")
e2 = Event(1.0, "a")
print(e2 < e1)  # True — sorted by timestamp
```

## Q91: What is the role of `__init_subclass__` in dataclass versioning?

**A:** `__init_subclass__` can implement dataclass versioning by tracking schema versions across subclasses. When a subclass is defined, `__init_subclass__` can assign a version number, track the version history, or validate that the version is compatible with the parent. This is useful for database schemas, API versions, and configuration files where backward compatibility matters.

The practical application: `class VersionedBase: _version = 0; def __init_subclass__(cls, version=None, **kwargs): super().__init_subclass__(**kwargs); cls._version = version or cls._parent._version + 1`. This automatically increments the version number for each subclass. The version can be used for migration, serialization, or compatibility checks.

The interaction with `@dataclass`: dataclass versioning can be combined with automatic registration and validation. `__init_subclass__` provides a clean hook for version tracking without metaclasses. The practical recommendation is to use `__init_subclass__` for simple versioning (version number, compatibility checks) and custom metaclasses for complex versioning (schema migration, backward compatibility).

**Example:**
```python
from dataclasses import dataclass

class VersionedModel:
    _version = 0
    
    def __init_subclass__(cls, version=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if version is not None:
            cls._version = version
        else:
            cls._version = getattr(cls, '_parent_version', 0) + 1

@dataclass
class V1(VersionedModel, version=1):
    name: str

@dataclass
class V2(V1):
    email: str

print(V1._version, V2._version)  # 1 2
```

## Q92: How does Python's MRO handle classes with `__init_subclass__` that modify the class?

**A:** `__init_subclass__` can modify the class after it is created (before it is fully finalized). The hook receives the class object and can add attributes, modify methods, or change class variables. The modifications are visible after `__init_subclass__` completes. This is useful for framework-level modifications: adding methods, setting class variables, or modifying the class dictionary.

The practical application: `def __init_subclass__(cls, **kwargs): super().__init_subclass__(**kwargs); cls.full_name = lambda self: f"{self.first} {self.last}"`. This adds a `full_name` method to all subclasses. The modification happens at class definition time, so the method is available for all instances.

The interaction with `@dataclass`: `__init_subclass__` runs after `@dataclass` processes the class, so the class has `__init__`, `__repr__`, etc. The hook can add additional methods or modify existing ones. The practical recommendation is to use `__init_subclass__` for adding framework-level methods and class variables, not for modifying generated methods (which may break the dataclass contract).

**Example:**
```python
from dataclasses import dataclass

class AutoSerializer:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, '__dataclass_fields__'):
            def to_dict(self):
                return {f: getattr(self, f) for f in cls.__dataclass_fields__}
            cls.to_dict = to_dict

@dataclass
class User(AutoSerializer):
    name: str
    age: int

u = User("Alice", 30)
print(u.to_dict())  # {'name': 'Alice', 'age': 30}
```

## Q93: What are the limitations of `__init_subclass__` compared to metaclasses?

**A:** `__init_subclass__` is simpler and more readable than metaclasses, but has limitations: (1) It cannot control class creation (it is called after the class is created). Metaclasses can control `__new__` and `__init__` of the class itself. (2) It cannot modify the class's metaclass. (3) It cannot control `__prepare__` (the namespace used for class body execution). (4) It cannot prevent class creation (it can raise, but the class was already created). (5) It cannot add methods to the class's namespace before `__init__` is called.

The practical implication is that `__init_subclass__` is suitable for post-creation hooks (validation, registration, modification) but not for class creation control. Metaclasses are suitable for both. The recommendation is to use `__init_subclass__` for simple hooks (validation, registration, modification) and metaclasses for complex class creation logic (custom `__new__`, `__init__`, `__prepare__`, namespace manipulation).

The interaction with `@dataclass`: `@dataclass` is a class decorator (not a metaclass), so it does not conflict with `__init_subclass__`. Both can be used together: `@dataclass` generates methods, `__init_subclass__` validates and registers. The practical recommendation is to prefer `@dataclass` + `__init_subclass__` over custom metaclasses for most use cases.

**Example:**
```python
# __init_subclass__ — simpler, post-creation
class Base:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.created = True

# Metaclass — more powerful, controls creation
class Meta(type):
    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super().__new__(mcs, name, bases, namespace)
        cls.created = True
        return cls
```

## Q94: How do dataclasses handle `__init_subclass__` with `unsafe_hash=True`?

**A:** `__init_subclass__` is called after `@dataclass(unsafe_hash=True)` processes the class. The hook can inspect `cls.__dataclass_params__` to check if `unsafe_hash` is enabled. The `__hash__` method is already generated when `__init_subclass__` runs. The hook can validate hash-related constraints (e.g., ensuring that all subclasses are hashable or that certain fields are excluded from hashing).

The practical application: `def __init_subclass__(cls, **kwargs): super().__init_subclass__(**kwargs); if cls.__dataclass_params__.unsafe_hash: # validate hash safety`. This allows framework code to warn about unsafe hashing or to enforce that hashable dataclasses are frozen. The validation happens at class definition time, catching potential issues early.

The interaction with `frozen=True`: `frozen=True` generates `__hash__` safely (because instances are immutable). `unsafe_hash=True` generates `__hash__` for mutable instances (dangerous). `__init_subclass__` can enforce that all subclasses use `frozen=True` instead of `unsafe_hash=True`. The practical recommendation is to use `frozen=True` for hashable dataclasses and `__init_subclass__` to enforce immutability across a hierarchy.

**Example:**
```python
from dataclasses import dataclass

@dataclass(unsafe_hash=True)
class BaseHash:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.__dataclass_params__.unsafe_hash:
            print(f"Warning: {cls.__name__} uses unsafe_hash")

@dataclass(unsafe_hash=True)
class Child(BaseHash):
    x: int
# Output: Warning: Child uses unsafe_hash
```

## Q95: What is the role of `__init_subclass__` in dataclass deserialization?

**A:** `__init_subclass__` can set up deserialization hooks for dataclasses. When a subclass is defined, `__init_subclass__` can register a custom deserializer, validate the class for deserialization compatibility, or set up schema metadata. This is useful for frameworks that need to deserialize data into dataclass instances (JSON, YAML, Protocol Buffers).

The practical application: `class Deserializable: _deserializers = {}; def __init_subclass__(cls, format=None, **kwargs): super().__init_subclass__(**kwargs); if format: cls._deserializers[format] = cls`. This registers format-specific deserializers. The framework can then deserialize data into the correct class based on the format.

The interaction with `@dataclass`: dataclasses are naturally serializable (via `asdict`) and deserializable (via `__init__`). `__init_subclass__` adds framework-level deserialization support. The practical recommendation is to use `__init_subclass__` for registering deserializers and `@dataclass` for the actual data representation.

**Example:**
```python
from dataclasses import dataclass

class Deserializable:
    _formats = {}
    
    def __init_subclass__(cls, format=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if format:
            Deserializable._formats[format] = cls

@dataclass
class User(Deserializable, format='json'):
    name: str
    email: str

@dataclass
class UserXML(Deserializable, format='xml'):
    name: str
    email: str

print(Deserializable._formats)
# {'json': User, 'xml': UserXML}
```

## Q96: How does `__init_subclass__` interact with `@dataclass` and `__slots__`?

**A:** `__init_subclass__` is called after `@dataclass(slots=True)` generates `__slots__`. The hook can inspect `cls.__slots__` to check which slots are defined. The slots are already in the class when `__init_subclass__` runs. The hook can validate slot names, add additional slots (though this is unusual), or check that slots do not conflict with parent classes.

The practical application: `def __init_subclass__(cls, **kwargs): super().__init_subclass__(**kwargs); if hasattr(cls, '__slots__'): # validate slots`. This allows framework code to enforce slot naming conventions or to detect slot conflicts in multiple inheritance. The validation happens at class definition time, catching slot issues early.

The interaction with inheritance: `__slots__` must not conflict across the hierarchy. `__init_subclass__` can detect conflicts by checking if a slot name is already defined in a parent class. The practical recommendation is to use `__init_subclass__` for slot validation and to ensure that all classes in the hierarchy define non-overlapping slots.

**Example:**
```python
from dataclasses import dataclass

class SlottedBase:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, '__slots__'):
            for slot in cls.__slots__:
                if slot.startswith('_'):
                    raise TypeError(f"Slot {slot} cannot start with '_'")

@dataclass(slots=True)
class Child(SlottedBase):
    x: float
    y: float

c = Child(1.0, 2.0)

# @dataclass(slots=True)
# class Bad(SlottedBase):
#     _secret: str  # TypeError: Slot _secret cannot start with '_'
```

## Q97: What is the difference between `@dataclass` and `@dataclass(init=True, eq=True)`?

**A:** `@dataclass(init=True, eq=True)` is identical to `@dataclass` (both parameters are defaults). The explicit parameters are redundant but can improve readability by making the behavior explicit. The practical difference is zero — the generated code is the same. The choice between `@dataclass` and `@dataclass(init=True, eq=True)` is a matter of style.

The practical usage: `@dataclass` is preferred for brevity. `@dataclass(init=True, eq=True)` is preferred when you want to document the behavior explicitly (e.g., in a codebase where all parameters are always specified). Both produce identical classes with `__init__` and `__eq__` generated from the field definitions.

The interaction with other parameters: `order=False` (default), `unsafe_hash=False` (default), `frozen=False` (default) can be changed independently. The practical recommendation is to use `@dataclass` with defaults and only specify parameters when you want non-default behavior: `@dataclass(frozen=True)`, `@dataclass(order=True)`, etc.

**Example:**
```python
from dataclasses import dataclass

@dataclass
class PointA:
    x: float
    y: float

@dataclass(init=True, eq=True)
class PointB:
    x: float
    y: float

# Identical:
print(PointA(1, 2) == PointB(1, 2))  # True
```

## Q98: How do dataclasses handle `__init_subclass__` with `kw_only` fields?

**A:** `__init_subclass__` is called after `@dataclass` processes `KW_ONLY` fields. The hook can inspect `cls.__dataclass_params__` to check if `kw_only` is enabled. The keyword-only fields are already defined in the class when `__init_subclass__` runs. The hook can validate that keyword-only fields have correct names, types, or defaults.

The practical application: `def __init_subclass__(cls, **kwargs): super().__init_subclass__(**kwargs); if cls.__dataclass_params__.kw_only: # validate keyword-only fields`. This allows framework code to enforce that certain fields are keyword-only (for API readability) or that keyword-only fields have specific types.

The interaction with inheritance: `KW_ONLY` applies to all fields after the `KW_ONLY` marker in the class definition. `__init_subclass__` can check that keyword-only fields are correctly defined. The practical recommendation is to use `KW_ONLY` for API clarity (enforcing keyword arguments at call sites) and `__init_subclass__` for validation.

**Example:**
```python
from dataclasses import dataclass, KW_ONLY

@dataclass
class Base:
    name: str
    _: KW_ONLY
    email: str
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, '__dataclass_params__') and cls.__dataclass_params__.kw_only:
            print(f"{cls.__name__} has keyword-only fields")

@dataclass
class Child(Base):
    age: int
# Output: Child has keyword-only fields
```

## Q99: What is the role of `__init_subclass__` in dataclass schema evolution?

**A:** `__init_subclass__` can track schema evolution across dataclass versions. When a subclass is defined, `__init_subclass__` can record the schema (field names, types, defaults), track changes from the parent schema, or validate backward compatibility. This is useful for database migrations, API versioning, and configuration management where schemas change over time.

The practical application: `class SchemaBase: _schemas = {}; def __init_subclass__(cls, schema_version=None, **kwargs): super().__init_subclass__(**kwargs); if schema_version: cls._schemas[schema_version] = {f.name: f.type for f in fields(cls)}`. This records the schema for each version. The framework can then compare schemas across versions to detect breaking changes.

The interaction with `@dataclass`: `__init_subclass__` has access to `cls.__dataclass_fields__` after `@dataclass` processes the class. The hook can inspect field definitions and record them for schema tracking. The practical recommendation is to use `__init_subclass__` for simple schema tracking and custom metaclasses for complex schema evolution logic.

**Example:**
```python
from dataclasses import dataclass, fields

class SchemaEvolution:
    _schemas = {}
    
    def __init_subclass__(cls, schema_version=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if schema_version and hasattr(cls, '__dataclass_fields__'):
            schema = {f.name: f.type for f in fields(cls)}
            SchemaEvolution._schemas[schema_version] = schema

@dataclass
class UserV1(SchemaEvolution, schema_version=1):
    name: str

@dataclass
class UserV2(SchemaEvolution, schema_version=2):
    name: str
    email: str

print(SchemaEvolution._schemas)
# {1: {'name': str}, 2: {'name': str, 'email': str}}
```

## Q100: What are the best practices for combining `@dataclass`, `__init_subclass__`, and cooperative multiple inheritance?

**A:** Best practices for combining these features: (1) Use `@dataclass` for data containers (reduces boilerplate). (2) Use `__init_subclass__` for validation and registration (simpler than metaclasses). (3) Use cooperative `super()` in `__init_subclass__` to maintain the hook chain. (4) Use `*args` and `**kwargs` in `__init_subclass__` for flexibility. (5) Use `ClassVar` for class variables and `InitVar` for init-only parameters. (6) Use `frozen=True` for immutable value types. (7) Use `slots=True` for memory efficiency.

(8) Use `__init_subclass__` for framework-level validation (field presence, type checks, naming conventions). (9) Use `__post_init__` for runtime validation (value ranges, consistency checks). (10) Use `field(compare=False)` for fields that should not affect equality or ordering. (11) Use `field(repr=False)` for sensitive or large fields. (12) Use `KW_ONLY` for API clarity (enforcing keyword arguments). (13) Test the MRO with `cls.__mro__` to verify the expected ordering. (14) Document the expected behavior of each class in the hierarchy.

(15) Prefer composition over multiple inheritance when classes are independent. (16) Use mixins for cross-cutting concerns (logging, validation, serialization). (17) Keep hierarchies shallow (2-3 levels deep). (18) Use `__init_subclass__` for plugin registration and discovery. (19) Use `@dataclass(frozen=True)` for hashable value types. (20) Use `@dataclass(slots=True)` for memory-efficient data containers. (21) Use `__init_subclass__` with `**kwargs` forwarding for extensible frameworks. (22) Test classes in isolation and in combination.

**Example:**
```python
from dataclasses import dataclass, field, fields
from typing import ClassVar

@dataclass(frozen=True, slots=True)
class ValidatedBase:
    _registry: ClassVar[dict] = {}
    
    def __init_subclass__(cls, plugin_name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if plugin_name:
            ValidatedBase._registry[plugin_name] = cls

@dataclass(frozen=True, slots=True)
class User(ValidatedBase, plugin_name='user'):
    name: str
    email: str
    age: int = field(compare=False)

@dataclass(frozen=True, slots=True)
class Admin(ValidatedBase, plugin_name='admin'):
    name: str
    permissions: tuple = ('read', 'write')

print(ValidatedBase._registry)
u = User("Alice", "alice@example.com", 30)
print(u)  # User(name='Alice', email='alice@example.com', age=30)
```
