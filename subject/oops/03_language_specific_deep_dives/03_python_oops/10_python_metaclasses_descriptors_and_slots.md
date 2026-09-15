# Python Metaclasses, Descriptors and __slots__ — 100 Interview Q&A

## Q1: What is a metaclass in Python, and how does it differ from a regular class?

**A:** A metaclass is the class of a class. Just as an instance is created from a class, a class itself is created from a metaclass. In Python's type system, `type` is the default metaclass — when you write `class Foo: pass`, Python internally calls `type('Foo', (object,), {...})` to construct the class object. A custom metaclass intercepts this construction process by overriding `__new__` and/or `__init__` on the metaclass, letting you modify the class before it exists as a fully formed object.

The key distinction is that a regular class defines the behavior of its instances, while a metaclass defines the behavior of its classes. When you instantiate a class, Python calls the class's `__call__` method (inherited from the metaclass), which in turn calls `__new__` and `__init__` on the class. When you write `class Foo(metaclass=MyMeta)`, Python's import machinery invokes `MyMeta.__new__(MyMeta, name, bases, namespace)` to create the class object itself.

This distinction matters because metaclasses give you hook points at class-creation time, not at instantiation time. You can enforce invariants across an entire class hierarchy, automatically register classes, inject methods, validate attributes, or transform the class dictionary before the class object is finalized. This is fundamentally different from `__init_subclass__`, which fires when a subclass is defined but does not give you the same level of control over the class object's construction.

```python
class MyMeta(type):
    def __new__(mcs, name, bases, namespace):
        print(f"Creating class {name}")
        cls = super().__new__(mcs, name, bases, namespace)
        return cls

class MyClass(metaclass=MyMeta):
    pass
# Output: Creating class MyClass
```

## Q2: How does Python's `type()` function work, and what is the relationship between `type()` and `class`?

**A:** `type()` is a built-in function that serves two purposes. With one argument (`type(obj)`), it returns the type of the object, which is the class from which it was instantiated. With three arguments (`type(name, bases, dict)`), it dynamically creates a new class. This dual nature reveals that `type` is itself a metaclass — it is the default metaclass that Python uses when no custom metaclass is specified.

When you write `class Foo: pass`, Python's compiler transforms this into a call to `type.__new__(type, 'Foo', (object,), {})`. The resulting class object `Foo` is an instance of `type`. This means `type(Foo)` returns `<class 'type'>`, and `isinstance(Foo, type)` is `True`. The three-argument form of `type()` is the dynamic equivalent of the `class` statement — it lets you create classes at runtime without the `class` keyword.

This relationship is the foundation of Python's object model. Every class is an instance of some metaclass, and `type` is the root of the metaclass hierarchy. You can think of it as: `type` is to classes what `object` is to instances. Just as all instances ultimately inherit from `object`, all metaclasses ultimately inherit from `type`. This recursive structure is what makes Python's type system so flexible — you can replace `type` with a custom metaclass to intercept class creation globally.

```python
# Dynamic class creation
MyClass = type('MyClass', (object,), {'greet': lambda self: 'hello'})
obj = MyClass()
print(obj.greet())  # hello
print(type(MyClass))  # <class 'type'>
```

## Q3: Explain the metaclass resolution order (MRO) in Python. How does Python decide which metaclass to use?

**A:** When Python encounters a class definition with `class Foo(Base, metaclass=MyMeta)`, it must determine the metaclass of the new class. If an explicit `metaclass` keyword argument is provided, Python uses that metaclass — but it first validates that the provided metaclass is compatible with the metaclasses of all base classes. Compatibility is checked by verifying that the explicit metaclass is a subclass of all base classes' metaclasses. If not, Python raises a `TypeError`.

If no explicit metaclass is specified, Python inherits the metaclass from the most derived base class. For example, if `Base` uses `MyMeta` as its metaclass and `Foo(Base)` doesn't specify a metaclass, then `Foo` will also use `MyMeta`. If multiple base classes have different metaclasses, Python requires that one is a subclass of the other — otherwise, it raises a `TypeError` because there is no unambiguous way to resolve the conflict.

This resolution happens at class creation time, before `__new__` or `__init__` on the metaclass is called. The Python data model specification (PEP 3119 and the language reference) defines this algorithm explicitly. Understanding the MRO for metaclasses is critical because it determines which metaclass's `__new__` and `__init__` are called, which in turn controls how the class is constructed. In practice, most Python code uses `type` or a single custom metaclass, so conflicts are rare, but library authors building frameworks like ORMs or serialization systems must be acutely aware of this resolution mechanism.

```python
class MetaA(type):
    pass

class MetaB(MetaA):
    pass

class Base(metaclass=MetaA):
    pass

# Foo inherits MetaA from Base — no conflict
class Foo(Base):
    pass

print(type(Foo))  # <class 'MetaA'>
```

## Q4: What is the `__prepare__` method in a metaclass, and why is it useful?

**A:** The `__prepare__` method is an optional hook that a metaclass can define to provide a custom namespace (dictionary) for the class body during its creation. By default, Python uses a regular `dict` for the class namespace, but `__prepare__` lets you substitute it with an `OrderedDict`, a `defaultdict`, or any custom mapping. The method receives the class name and base classes, and must return a mapping object that Python will use as the local namespace while executing the class body.

The most common use case is using `collections.OrderedDict` as the namespace to preserve the order in which attributes are defined in the class body. While Python 3.7+ guarantees dictionary insertion order for regular dicts, using `OrderedDict` was historically the only reliable way to introspect attribute definition order. Beyond ordering, `__prepare__` enables powerful metaclass patterns: you can log attribute definitions, validate names, enforce naming conventions, or automatically register methods as they are defined.

`__prepare__` is called before the class body is executed. The returned namespace object is populated with the class's attributes as the body executes, and then passed to `__new__` on the metaclass. This gives metaclass authors a chance to observe and transform the raw attribute definitions before the class object is finalized. For example, a metaclass might use a custom namespace that automatically wraps certain functions in descriptors, or that prevents certain attribute names from being used.

```python
from collections import OrderedDict

class OrderedMeta(type):
    @classmethod
    def __prepare__(mcs, name, bases):
        return OrderedDict()

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, dict(namespace))
        cls._field_order = [k for k in namespace.keys() if not k.startswith('_')]
        return cls

class Struct(metaclass=OrderedMeta):
    x = 1
    y = 2
    z = 3

print(Struct._field_order)  # ['x', 'y', 'z']
```

## Q5: What is a descriptor in Python, and how does it relate to attribute access?

**A:** A descriptor is any object that defines `__get__`, `__set__`, or `__delete__` (the descriptor protocol). When an attribute is accessed on an instance, Python's attribute lookup mechanism checks whether the attribute's value in the class dictionary is a descriptor. If it is, Python calls the appropriate descriptor method instead of returning the raw value. This is the mechanism behind properties, class methods, static methods, and many other Python features.

The descriptor protocol has three methods: `__get__(self, obj, objtype=None)` is called when the attribute is read; `__set__(self, obj, value)` is called when the attribute is assigned; and `__delete__(self, obj)` is called when `del obj.attr` is used. A descriptor that defines only `__get__` is called a non-data descriptor (like functions and methods), while a descriptor that defines both `__get__` and `__set__` is called a data descriptor (like properties). Data descriptors take precedence over instance dictionaries, which is why you cannot override a property by setting an instance attribute with the same name (in most cases).

Descriptor-based attribute access follows a specific lookup chain. When you access `instance.attr`, Python first checks the type(instance).__mro__ for a data descriptor. If found, it calls the descriptor's `__get__`. If not, it checks the instance's `__dict__`. If not there, it checks the type's MRO for a non-data descriptor or a plain attribute. This chain is why descriptors are so powerful — they allow class-level objects to intercept and customize attribute access at a fundamental level, making them the backbone of Python's object model.

```python
class Verbose:
    def __get__(self, obj, objtype=None):
        print(f"Accessing attribute on {obj}")
        return 42

    def __set__(self, obj, value):
        print(f"Setting attribute to {value} on {obj}")
        obj.__dict__['verbose_val'] = value

class MyClass:
    x = Verbose()

obj = MyClass()
print(obj.x)  # Accessing... prints 42
obj.x = 10    # Setting... to 10
```

## Q6: Explain the difference between data descriptors and non-data descriptors in Python.

**A:** Data descriptors define both `__get__` and `__set__` (and optionally `__delete__`), while non-data descriptors define only `__get__`. This distinction is critical because Python's attribute lookup algorithm gives data descriptors higher priority than instance `__dict__` entries. When you access an attribute on an instance, Python's attribute resolution (in `type.__getattribute__`) first looks for a data descriptor in the class and its bases. If found, the data descriptor's `__get__` is called, and the instance's `__dict__` is bypassed entirely.

Non-data descriptors, on the other hand, have lower priority than instance `__dict__` entries. This means that if an instance has an attribute with the same name in its `__dict__`, the instance attribute will shadow the non-data descriptor. This is precisely why methods work the way they do in Python — methods are non-data descriptors (they only define `__get__`), so assigning a function to an instance attribute effectively "binds" that function as a method, shadowing the class-level method.

This asymmetry has significant practical consequences. `property` is a data descriptor, so you cannot override a property by assigning to an instance attribute of the same name — the property's `__set__` will intercept the assignment. However, methods are non-data descriptors, so `instance.method = something` will shadow the class method for that instance only. Understanding this distinction helps developers predict when attribute access will hit the descriptor versus the instance dictionary, which is essential for debugging complex attribute access patterns in frameworks.

```python
class Prop:
    def __get__(self, obj, objtype=None):
        return 'from descriptor'

    def __set__(self, obj, value):
        pass  # Silently ignores the assignment

class MyClass:
    x = Prop()

obj = MyClass()
obj.x = 'from instance'  # Silently ignored
print(obj.x)  # 'from descriptor' — data descriptor wins
print(obj.__dict__)  # {} — nothing was stored in instance dict
```

## Q7: How does Python's `property` built-in work internally?

**A:** Python's `property` is implemented as a built-in data descriptor class. When you use the `@property` decorator, Python creates an instance of the `property` class and stores it in the class dictionary. The `property` class implements `__get__`, `__set__`, and `__delete__`, delegating to the user-provided getter, setter, and deleter functions. Because `property` is a data descriptor (it defines both `__get__` and `__set__`), it takes precedence over instance `__dict__` entries during attribute access.

The `property` object is a descriptor with well-defined behavior: when you read `obj.prop`, `property.__get__` is called, which invokes the getter function with `obj` as the argument. When you assign `obj.prop = value`, `property.__set__` is called, which invokes the setter. If no setter is defined and you attempt assignment, a `AttributeError` is raised. This is how `property` enforces read-only attributes — by not providing a `__set__` method (or by raising an exception in the setter).

The `property` class also supports the decorator syntax for defining getter, setter, and deleter methods. When you write `@prop.setter`, you are calling `prop.setter(func)`, which returns a new `property` object with the setter function attached. This is a functional composition pattern — each decorator call creates a new `property` object that combines the previous getter with the new setter. The resulting property object replaces the original in the class dictionary. Understanding this internal mechanism helps developers create custom descriptors that mimic or extend `property` behavior, such as cached properties, validated properties, or properties with custom deletion logic.

```python
# @property is syntactic sugar for this:
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

c = Circle(5)
print(c.radius)   # 5
c.radius = 10     # OK
# c.radius = -1   # ValueError
```

## Q8: What is `__slots__`, and how does it affect memory usage and attribute access?

**A:** `__slots__` is a class-level attribute that tells Python to reserve space for a fixed set of attribute names in each instance, instead of using a per-instance `__dict__`. When you define `__slots__ = ('x', 'y')`, Python allocates a C-level struct with slots for `x` and `y` and uses descriptors to access them. Instances no longer have a `__dict__` attribute (unless `__dict__` is explicitly included in `__slots__`), which eliminates the memory overhead of the dictionary.

The memory savings can be substantial. A typical Python object's `__dict__` is a hash table that can consume 100+ bytes per instance, even for objects with only one or two attributes. With `__slots__`, each attribute is stored as a fixed-size C array entry in the instance structure, reducing memory by 40-60% for objects with few attributes. This is particularly valuable when creating millions of instances, such as in data processing, game development, or scientific computing. The trade-off is that you lose the ability to add arbitrary attributes to instances, which reduces flexibility.

Slot access is also slightly faster than dictionary access because Python can compute the memory offset of a slot at class creation time, avoiding the hash table lookup that `__dict__` requires. However, the performance difference is often small in practice. The primary benefits of `__slots__` are memory efficiency and the enforcement of a fixed attribute set. Note that `__slots__` does not work with `__dict__` by default — if you need both slots and dynamic attributes, you must include `'__dict__'` in the `__slots__` tuple.

```python
class PointSlots:
    __slots__ = ('x', 'y')

    def __init__(self, x, y):
        self.x = x
        self.y = y

p = PointSlots(1, 2)
# p.z = 3  # AttributeError: 'PointSlots' object has no attribute 'z'
print(hasattr(p, '__dict__'))  # False
```

## Q9: Can you use `__slots__` with inheritance? What are the pitfalls?

**A:** `__slots__` works with inheritance, but requires careful design. When a parent class defines `__slots__`, its slot attributes are stored in the instance's C struct. A child class that also defines `__slots__` adds additional slots to the struct. The key constraint is that a child class's slots cannot use the same names as the parent's slots — doing so would shadow the parent's slots, leading to unexpected behavior and potentially broken attribute access.

When designing class hierarchies with `__slots__`, each class in the hierarchy should define its own `__slots__` with only the attributes unique to that class. The parent class's `__slots__` are automatically inherited. For example, if `Base` has `__slots__ = ('id',)` and `Child(Base)` has `__slots__ = ('name',)`, then instances of `Child` will have both `id` and `name` as slot attributes. If `Child` accidentally repeats `__slots__ = ('id', 'name')`, the child's `id` slot will shadow the parent's, which can cause subtle bugs.

A common pitfall is forgetting that `__slots__` does not automatically cooperate with multiple inheritance. If two parent classes define `__slots__`, the child class must also define `__slots__` to resolve the conflict. Additionally, classes with `__slots__` cannot use weak references unless `'__weakref__'` is included in `__slots__`. Many built-in types and third-party libraries assume the presence of `__dict__`, so mixing `__slots__` classes with them can cause issues. In practice, `__slots__` is best used for simple data-holder classes in performance-critical code, not as a blanket optimization across an entire codebase.

```python
class Base:
    __slots__ = ('id',)

class Child(Base):
    __slots__ = ('name',)  # Only add new attributes

c = Child()
c.id = 1
c.name = "test"
# c.id = 'shadow'  # Shadows parent slot — avoid this
print(c.id, c.name)  # 1 test
```

## Q10: What is the difference between `__dict__` and `__slots__` in terms of attribute storage?

**A:** `__dict__` is a per-instance dictionary that stores all of an object's attributes as key-value pairs. It is a Python dictionary (which is a hash table), so it has overhead for hashing, probing, and storing key-value pairs. Every regular Python object has a `__dict__`, and you can add, remove, or modify attributes dynamically at any time. This flexibility is one of Python's strengths, but it comes with memory and performance costs.

`__slots__`, by contrast, replaces `__dict__` with a fixed-size C struct that stores attribute values at precomputed memory offsets. The slot descriptors (one per declared slot name) are stored in the class object, and they use the instance's memory address plus a known offset to access each attribute. This means there is no hash table overhead, no per-instance dictionary allocation, and no dynamic attribute resolution. The result is both faster attribute access (by a small margin) and significantly lower memory usage.

The practical difference is that `__dict__` objects can store any attribute name dynamically, while `__slots__` restricts attributes to those declared in the `__slots__` tuple. If you try to set an undeclared attribute on a slotted instance, you get an `AttributeError`. If you need both fixed attributes and dynamic ones, you can include `'__dict__'` in `__slots__`, which adds both the slot descriptors and a dictionary for overflow attributes. This hybrid approach gives you the memory benefits of slots for commonly used attributes while retaining flexibility for dynamic ones.

```python
class DictBased:
    def __init__(self):
        self.x = 1
        self.y = 2

class SlotBased:
    __slots__ = ('x', 'y')
    def __init__(self):
        self.x = 1
        self.y = 2

import sys
d = DictBased()
s = SlotBased()
print(sys.getsizeof(d.__dict__))  # ~104 bytes (empty dict overhead)
print(sys.getsizeof(d))           # ~48 bytes (object overhead)
print(sys.getsizeof(s))           # ~40 bytes (no dict at all)
```

## Q11: How does Python's descriptor protocol enable the `classmethod` and `staticmethod` descriptors?

**A:** `classmethod` and `staticmethod` are both implemented as descriptor classes, and their behavior is entirely governed by the descriptor protocol. `classmethod` defines a `__get__` method that, when the class method is accessed, binds the class itself (not the instance) as the first argument. It does not define `__set__`, making it a non-data descriptor. When you access `MyClass.method` or `instance.method`, the `classmethod.__get__` method returns a callable that prepends the class to the argument list.

`staticmethod` is even simpler — its `__get__` method returns the underlying function without any binding. It exists solely to provide a clear syntactic way to indicate that a method does not receive `self` or `cls`. In Python 3, functions already behave this way when accessed from a class (they are just functions, not bound methods), so `staticmethod` is somewhat redundant in modern Python, but it still serves as documentation and ensures consistent behavior.

Understanding these descriptors is valuable because it reveals that Python's method types are not special language constructs — they are ordinary objects that implement the descriptor protocol. This means you can create your own custom method types by implementing `__get__`. For example, you could create a `timed_method` descriptor that wraps method calls with timing logic, or a `cached_method` descriptor that memoizes results. The descriptor protocol is the mechanism that makes all of these patterns possible, and it is the same mechanism used by `property`, slot attributes, and many other Python features.

```python
class Myclassmethod:
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, objtype=None):
        if objtype is None:
            objtype = type(obj)
        def wrapper(*args, **kwargs):
            return self.func(objtype, *args, **kwargs)
        return wrapper

class MyClass:
    @Myclassmethod
    def create(cls):
        return cls()

obj = MyClass.create()
print(type(obj))  # <class 'MyClass'>
```

## Q12: What is the `__init_subclass__` hook, and how does it compare to metaclasses?

**A:** `__init_subclass__` was introduced in Python 3.6 (PEP 487) as a simpler alternative to metaclasses for the common use case of customizing subclasses. When a class is defined that inherits from a parent class, the parent's `__init_subclass__` method is called with the child class as an argument. This lets you run code at subclass definition time without the complexity of a full metaclass. It receives keyword arguments from the child class's class statement, enabling parameterized subclass registration.

The key advantage of `__init_subclass__` over metaclasses is simplicity and composability. Metaclasses can conflict with each other in multiple inheritance, while `__init_subclass__` calls chain naturally through the MRO — each parent's hook is called in order, and there is no conflict. `__init_subclass__` also does not require understanding the full metaclass protocol (`__new__`, `__init__`, `__prepare__`, `__call__`), making it more accessible for everyday use.

However, `__init_subclass__` cannot do everything a metaclass can. It cannot change the class's namespace (like `__prepare__` does), it cannot intercept the creation of the class object (like `__new__` does), and it cannot modify the class's bases or metaclass. It runs after the class has already been created. For use cases like enforcing abstract methods, transforming class dictionaries, or dynamically modifying bases, metaclasses are still necessary. In practice, `__init_subclass__` is preferred for registry patterns, mixin application, and simple subclass validation, while metaclasses are reserved for deeper class-creation customization.

```python
class Plugin:
    _registry = {}

    def __init_subclass__(cls, plugin_name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        name = plugin_name or cls.__name__
        Plugin._registry[name] = cls

class MyPlugin(Plugin, plugin_name="my_plugin"):
    pass

print(Plugin._registry)  # {'my_plugin': <class 'MyPlugin'>}
```

## Q13: Explain the `__getattribute__` and `__getattr__` methods and how they interact with descriptors.

**A:** `__getattribute__` is called for every attribute access on an instance, without exception. It is the entry point for Python's attribute lookup mechanism, defined on `object`. When you access `instance.attr`, Python calls `type(instance).__getattribute__(instance, 'attr')`. The default implementation of `__getattribute__` follows the standard lookup chain: it first checks for data descriptors in the class hierarchy, then checks the instance's `__dict__`, then checks non-data descriptors and class attributes, and finally raises `AttributeError` if nothing is found.

`__getattr__` is different — it is only called when the normal attribute lookup mechanism fails (i.e., when `__getattribute__` raises `AttributeError`). This makes `__getattr__` a fallback for handling missing attributes. It is useful for implementing dynamic attribute resolution, such as proxying attribute access to another object, computing attributes on the fly, or providing backward compatibility for renamed attributes. `__getattr__` is not called for attribute access that succeeds through `__getattribute__`, so it does not interfere with the normal lookup chain.

The interaction with descriptors is critical: `__getattribute__` calls descriptor `__get__` methods during its lookup process. If you override `__getattribute__`, you must be careful to call `super().__getattribute__()` or manually implement the descriptor protocol, otherwise descriptors like `property`, `classmethod`, and slot attributes will stop working. `__getattr__` does not interact with descriptors because it is only called after the descriptor-based lookup has already completed and failed. This separation makes `__getattr__` safe to use without worrying about breaking descriptors.

```python
class Dynamic:
    def __getattr__(self, name):
        """Called only when normal lookup fails."""
        if name.startswith('computed_'):
            return name.replace('computed_', '').upper()
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

d = Dynamic()
print(d.computed_foo)  # 'FOO'
# print(d.existing)   # AttributeError
```

## Q14: What are abstract base classes (ABCs) and how do they use the metaclass mechanism?

**A:** Abstract base classes in Python are implemented using the `abc.ABCMeta` metaclass and the `@abstractmethod` decorator. `ABCMeta` is a metaclass that maintains a registry of abstract methods and checks at class instantiation time that all abstract methods have been implemented. If you try to instantiate a class that has unimplemented abstract methods, `ABCMeta.__call__` raises a `TypeError`. This provides a compile-time-like safety net for class hierarchies, ensuring that subclasses fulfill their interface contracts.

`ABCMeta` also provides the `register()` method, which allows classes to be registered as virtual subclasses of an ABC without inheriting from it. This is useful for making third-party classes appear to implement an interface without modifying their source code. The `isinstance()` and `issubclass()` built-in functions respect this registry, so `isinstance(obj, MyABC)` will return `True` for any class registered with `MyABC.register()`.

The interaction between ABCs and the metaclass mechanism is direct: `ABCMeta` overrides `__new__` and `__init__` to track abstract methods, and `__call__` to enforce implementation at instantiation. The `@abstractmethod` decorator marks methods as abstract by setting an `__isabstractmethod__` attribute on them. When a concrete subclass is created, `ABCMeta` verifies that none of the inherited abstract methods remain unimplemented. This makes ABCs a practical application of metaclasses that many Python developers use regularly, even if they do not think of it as metaclass programming.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

    def perimeter(self):
        return 2 * 3.14159 * self.radius

# c = Shape()  # TypeError: Can't instantiate abstract class
c = Circle(5)
print(c.area())  # 78.53975
```

## Q15: How do descriptors enable Python's `property` decorator to validate data?

**A:** The `property` decorator creates a data descriptor that intercepts both getting and setting of an attribute. When you define a setter on a property, the setter function receives the value being assigned, giving you the opportunity to validate, transform, or reject the value before it is stored. If validation fails, the setter can raise an exception (typically `ValueError` or `TypeError`), which prevents the assignment from happening. This is a clean, Pythonic way to enforce invariants on object attributes.

Beyond the basic `property`, you can create custom descriptor classes that provide more sophisticated validation. A custom descriptor can validate types, enforce ranges, trigger side effects (like logging or event dispatching), or implement computed attributes. The descriptor protocol's `__set__` method is called whenever the attribute is assigned, regardless of how the assignment is performed — through direct attribute access, `setattr()`, or even `__init__` methods (for data descriptors).

A practical pattern is to create a `Validated` descriptor class that takes a validation function as a parameter, and then compose it with specific validators. This is more flexible than using properties alone because you can reuse the same descriptor across multiple classes and attributes. Libraries like Django's ORM and SQLAlchemy'sAlchemy use descriptors extensively for this reason — each model field is a descriptor that handles type conversion, validation, and database storage, all through the descriptor protocol.

```python
class Validated:
    def __init__(self, validator, error_msg):
        self.validator = validator
        self.error_msg = error_msg
        self.storage_name = None

    def __set_name__(self, owner, name):
        self.storage_name = f'_validated_{name}'

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.storage_name, None)

    def __set__(self, obj, value):
        if not self.validator(value):
            raise ValueError(self.error_msg)
        setattr(obj, self.storage_name, value)

class User:
    age = Validated(
        lambda v: isinstance(v, int) and 0 <= v <= 150,
        "Age must be an integer between 0 and 150"
    )

u = User()
u.age = 25
# u.age = -5  # ValueError: Age must be an integer between 0 and 150
```

## Q16: What is the `__set_name__` protocol, and why was it introduced?

**A:** `__set_name__` is a protocol introduced in Python 3.6 (PEP 487) that is automatically called on descriptors when the class they are defined in is created. When Python constructs a class, it iterates over the class namespace and calls `descriptor.__set_name__(owner_class, attribute_name)` on any object that has this method. This allows descriptors to know which class they belong to and which attribute name they are bound to, without requiring the descriptor author to hardcode this information.

Before `__set_name__`, descriptors had to use one of two awkward patterns to learn their attribute name: (1) pass the name explicitly in the descriptor constructor (e.g., `field = MyDescriptor('field')`), which is redundant and error-prone, or (2) use `__get__` to detect when the descriptor is accessed and lazily determine the name. `__set_name__` eliminates this redundancy by having Python automatically provide the name at class creation time.

This protocol is essential for descriptors that need to store values on instances. A descriptor needs to know what attribute name to use when storing values in `instance.__dict__`, and `__set_name__` provides this information. The descriptor can then construct a private storage name (e.g., `_field_name`) and use it consistently in `__get__`, `__set__`, and `__delete__`. This is the standard pattern used by `dataclasses` fields and many validation libraries. Without `__set_name__`, creating reusable descriptors that store per-instance values would be significantly more cumbersome.

```python
class Field:
    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = f'_{name}'

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value):
        setattr(obj, self.private_name, value)

class Model:
    name = Field()
    email = Field()

m = Model()
m.name = "Alice"
print(m._name)  # 'Alice' — storage uses private name
```

## Q17: How do you create a custom descriptor that mimics `property` but adds caching?

**A:** A cached property descriptor combines the `property` protocol with lazy evaluation and result caching. The descriptor's `__get__` method computes the value on first access, stores it in the instance's `__dict__`, and returns it. On subsequent accesses, `__get__` finds the value in the instance's `__dict__` and returns it directly, bypassing the computation. This works because a non-data descriptor (one without `__set__`) is overridden by instance dictionary entries.

The key design decision is whether the cached property should be a data descriptor or non-data descriptor. As a non-data descriptor (only `__get__`), the cached value in `instance.__dict__` takes precedence on subsequent accesses — which is exactly what we want. The first call computes and stores the value; subsequent calls find it in `__dict__`. If you made it a data descriptor (with `__set__`), the descriptor's `__get__` would always be called, defeating the caching purpose.

Python 3.8+ provides `functools.cached_property` as a standard library implementation of this pattern. A custom implementation must handle thread safety, cache invalidation, and the edge case where the computation raises an exception (the value should not be cached). The `__set_name__` protocol is used to determine the storage name in the instance's `__dict__`. This is a common interview question because it tests understanding of descriptor priority (data vs. non-data), `__dict__` manipulation, and the practical application of descriptors.

```python
import time

class CachedProperty:
    def __set_name__(self, owner, name):
        self.attrname = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        val = self.compute(obj)
        setattr(obj, self.attrname, val)
        return val

    def compute(self, obj):
        # Expensive computation
        time.sleep(1)
        return 42

class MyClass:
    @CachedProperty
    def expensive(self):
        return self.compute()

obj = MyClass()
start = time.time()
print(obj.expensive)  # Takes ~1 second
start2 = time.time()
print(obj.expensive)  # Instant — served from __dict__
```

## Q18: Explain how `dataclasses` use descriptors internally.

**A:** Python's `dataclasses` module (PEP 557) uses descriptors as part of its field handling mechanism. When you define a dataclass, the `@dataclass` decorator processes the class annotations and creates `dataclasses.Field` objects for each field. These `Field` objects are descriptors that handle default values, default factories, and field metadata. During class creation, `dataclasses` replaces the raw `Field` objects with appropriate values in the generated `__init__`, `__repr__`, `__eq__`, and other dunder methods.

The `Field` class itself implements the descriptor protocol to provide default value access. When a field has a default value, `Field.__get__` returns that default when accessed from the class. For mutable defaults (like lists or dictionaries), `Field` uses `field(default_factory=list)` to create a new instance for each object, avoiding the shared mutable default pitfall. The descriptor mechanism ensures that default values are properly handled whether accessed from the class or from an instance.

Beyond `Field`, `dataclasses` also uses descriptors indirectly through its generated methods. The generated `__init__` method assigns values to instance attributes, and the generated `__eq__` method compares them. While `dataclasses` does not generate property descriptors for fields (unlike `namedtuple`), the `dataclasses.fields()` function returns `Field` descriptors, which are used for introspection and serialization. Understanding how `dataclasses` use descriptors helps explain why certain patterns (like mixing `__init__` with `dataclass` defaults) can behave unexpectedly.

```python
from dataclasses import dataclass, field

@dataclass
class User:
    name: str
    tags: list = field(default_factory=list)
    age: int = field(default=0, metadata={'min': 0})

u1 = User("Alice")
u2 = User("Bob")
print(u1.tags is u2.tags)  # False — separate instances
print(User.__dataclass_fields__['age'].metadata)  # {'min': 0}
```

## Q19: What is the MRO for classes that use `__slots__` and how does it affect attribute access?

**A:** The MRO (Method Resolution Order) for classes with `__slots__` follows the standard C3 linearization algorithm, just like any other Python class. However, `__slots__` introduces an additional layer to attribute access because slot descriptors are stored in the class dictionary and participate in the descriptor protocol. When an attribute is accessed on a slotted instance, Python's `__getattribute__` first checks for data descriptors in the MRO, finds the slot descriptor, and uses it to access the value from the instance's C struct — not from a `__dict__`.

In a class hierarchy with multiple levels of `__slots__`, the MRO determines the order in which slot descriptors are checked. Each class in the hierarchy defines its own slots, and these are stored as data descriptors in the respective class objects. When accessing an attribute, Python traverses the MRO looking for a data descriptor with that name. The first match found is used, which means that a child class's slot with the same name as a parent's slot will shadow it — this is the same behavior as method resolution but applied to slot descriptors.

A subtle pitfall arises when mixing slotted and non-slotted classes in a hierarchy. If a parent class does not define `__slots__`, it has a `__dict__`, and the child class's `__slots__` will coexist with this `__dict__`. Attribute access then becomes a two-step process: Python first checks for slot descriptors, then falls back to the inherited `__dict__`. This is correct but can be confusing because some attributes are stored in slots (fast access, low memory) while others are stored in the dictionary (slower access, higher memory). The MRO ensures that descriptor lookup order is well-defined, but mixing strategies within a hierarchy should be avoided for clarity.

```python
class A:
    __slots__ = ('x',)

class B(A):
    __slots__ = ('y',)

class C(B):
    __slots__ = ('z',)

c = C()
c.x = 1  # Stored in A's slot
c.y = 2  # Stored in B's slot
c.z = 3  # Stored in C's slot
print(C.__mro__)  # (<class 'C'>, <class 'B'>, <class 'A'>, <class 'object'>)
```

## Q20: How do descriptors enable the `super()` function's behavior?

**A:** The `super()` function's behavior is partially enabled by descriptors, though its primary mechanism is a custom wrapper class. When you call `super()`, it returns a `super` object that holds a reference to the current class and the current instance. When you access a method on this `super` object, the `super.__getattribute__` method traverses the MRO starting after the current class, looking for the named attribute. This is how `super()` achieves cooperative method invocation — it delegates to the next class in the MRO, not to the parent class directly.

The descriptor connection comes in when `super` looks up methods. The `super.__getattribute__` method calls `getattr` on the MRO chain, which triggers descriptor protocol for any descriptors found along the way. If a method is defined as a regular function (a non-data descriptor), `super.__getattribute__` calls `function.__get__` to bind the method to the instance. If a method is defined as a `classmethod` or `property`, the corresponding descriptor's `__get__` is invoked. This means `super()` correctly handles all method types through the descriptor protocol.

The practical consequence is that `super()` works seamlessly with any method-like object that implements `__get__`. This includes regular methods, class methods, static methods, properties, and custom descriptors. When you write `super().method()`, Python finds `method` in the MRO using `super.__getattribute__`, invokes the descriptor protocol to bind it, and then calls the result. This deep integration with the descriptor protocol is what makes `super()` so powerful and flexible in cooperative multiple inheritance patterns.

```python
class Base:
    def greet(self):
        return "Hello from Base"

class Middle(Base):
    def greet(self):
        return "Hello from Middle, " + super().greet()

class Child(Middle):
    def greet(self):
        return "Hello from Child, " + super().greet()

c = Child()
print(c.greet())  # Hello from Child, Hello from Middle, Hello from Base
```

## Q21: What is `__mro_entries__` and when would you use it?

**A:** `__mro_entries__` is a method (PEP 560, Python 3.7+) that a class can define to customize how it participates in the MRO computation. When Python encounters a base class in a class definition that has `__mro_entries__`, it calls that method with the tuple of actual base classes, and the returned tuple of types replaces the original base class in the MRO. This allows third-party types to participate in Python's class hierarchy without requiring explicit registration or metaclass cooperation.

The primary use case is making non-type objects work as base classes. For example, a library might define a type that, when used as a base class, automatically registers the child class with a framework. Another use case is creating "interface" types that expand into multiple actual base classes. `__mro_entries__` is called during class creation, before the MRO is computed, so it can inject additional bases that the C3 linearization algorithm will then process.

This is distinct from `__init_subclass__` and metaclasses. `__mro_entries__` operates at the MRO computation level, while `__init_subclass__` operates at the subclass creation level, and metaclasses operate at the class creation level. `__mro_entries__` is useful for libraries that want to provide "base class-like" objects without being actual types. However, it is an advanced feature that most Python developers will not need to use directly. Understanding it helps when working with frameworks that use advanced metaclass or MRO manipulation techniques.

```python
class InterfaceBase:
    def __mro_entries__(self, bases):
        # Replace self with the actual implementation class
        return (RealInterface,)

class RealInterface:
    pass

class MyClass(InterfaceBase()):
    pass

print(MyClass.__mro__)
# (<class 'MyClass'>, <class 'RealInterface'>, <class 'object'>)
```

## Q22: How does `__class_getitem__` relate to descriptors and generics?

**A:** `__class_getitem__` (PEP 560, Python 3.7+) is a method that a class can define to customize the behavior of subscription syntax (`MyClass[int]`). When you write `MyClass[int]`, Python calls `MyClass.__class_getitem__(int)` and returns the result. This is the mechanism that enables generic types in Python — `list[int]`, `dict[str, int]`, and `typing.List[int]` all use `__class_getitem__` to handle the subscription syntax.

The connection to descriptors is indirect but important. `__class_getitem__` is called at class level (not instance level), so it is a class method-like protocol. In Python 3.9+, built-in types like `list`, `dict`, and `tuple` support subscription natively through `__class_getitem__`. For user-defined classes, you can define `__class_getitem__` to accept type parameters and return a specialized version of the class. This is commonly used in conjunction with descriptors for type-safe attribute access in frameworks.

The relationship to the broader descriptor system is that `__class_getitem__` is part of Python's data model hooks, similar to `__init_subclass__` and `__set_name__`. These hooks are called by the Python runtime at specific points during class creation and attribute access. `__class_getitem__` is called when the class is subscripted, `__set_name__` is called when a descriptor is assigned to a class, and `__init_subclass__` is called when a subclass is created. Together, these hooks provide a comprehensive set of customization points for class-based design without requiring metaclasses.

```python
class Typed:
    def __class_getitem__(cls, item):
        return type(f'{cls.__name__}[{item.__name__}]', (cls,), {'_type': item})

class Container:
    pass

IntContainer = Container[int]
print(IntContainer._type)  # <class 'int'>
print(IntContainer.__name__)  # 'Container[int]'
```

## Q23: What are the performance implications of using descriptors versus direct attribute access?

**A:** Descriptors add a layer of indirection to attribute access compared to direct dictionary lookups. When you access a regular attribute, Python looks it up in the instance's `__dict__` (a hash table lookup). When you access a descriptor-based attribute, Python must check the class hierarchy for data descriptors, call the descriptor's `__get__` method, and then return the result. This extra work adds overhead — benchmarks typically show that descriptor access is 2-5x slower than direct dictionary access, depending on the complexity of the descriptor and the depth of the class hierarchy.

However, this overhead is often negligible in practice. Python's attribute lookup is already relatively slow compared to languages like C++ or Java, and the descriptor overhead is a small fraction of the total cost. In performance-critical code, the choice between descriptors and direct access should be guided by profiling, not assumptions. The `__slots__` optimization (which uses descriptors internally) can actually improve performance by eliminating dictionary lookups entirely — slot access is faster than `__dict__` access because it uses fixed memory offsets.

The trade-off is between flexibility and performance. Descriptors enable powerful abstractions (validation, caching, logging, computed attributes) that would otherwise require repetitive boilerplate code. The performance cost is typically justified by the code clarity and maintainability benefits. In extreme performance cases, `__slots__` and direct attribute access can be used, but this should be a last resort after profiling demonstrates that descriptor access is actually a bottleneck.

```python
import timeit

class WithDescriptor:
    @property
    def value(self):
        return 42

class WithoutDescriptor:
    def __init__(self):
        self.value = 42

wd = WithDescriptor()
wo = WithoutDescriptor()

# Descriptor (property) access
t1 = timeit.timeit(lambda: wd.value, number=1000000)
# Direct attribute access
t2 = timeit.timeit(lambda: wo.value, number=1000000)

print(f"Property: {t1:.4f}s, Direct: {t2:.4f}s")
# Property is typically ~3x slower
```

## Q24: How do descriptors interact with `__dict__` updates and `setattr`?

**A:** When you use `setattr(instance, 'attr', value)`, Python calls `type(instance).__setattr__(instance, 'attr', value)`. The default `object.__setattr__` implementation checks if there is a data descriptor for 'attr' in the class hierarchy. If found, it calls the descriptor's `__set__` method. If no data descriptor is found, it stores the value directly in `instance.__dict__['attr']`. This is the same lookup chain used by direct attribute assignment (`instance.attr = value`), so descriptors and `setattr` interact consistently.

When you modify `__dict__` directly (e.g., `instance.__dict__['attr'] = value`), you bypass the descriptor protocol entirely. This is a deliberate design choice — direct dictionary manipulation is a low-level escape hatch that allows you to override descriptors in certain situations. For data descriptors, this bypass is limited because `__getattribute__` checks data descriptors before `__dict__`. For non-data descriptors (like methods), writing to `__dict__` shadows the descriptor, which is how dynamic method binding works in Python.

A subtle edge case occurs when `__setattr__` itself is overridden. If a class defines `__setattr__`, it can intercept all attribute assignments, including those intended for descriptors. This is howORM frameworks implement "dirty tracking" — they override `__setattr__` to record which attributes have been modified. The implementation must carefully delegate to `super().__setattr__()` or `object.__setattr__()` for descriptors to work correctly, or manually implement the descriptor lookup chain. Misimplementing `__setattr__` can break properties, slots, and other descriptor-based features.

```python
class Tracking:
    def __init__(self):
        self._modified = set()
        object.__setattr__(self, '_modified', set())

    def __setattr__(self, name, value):
        if name != '_modified':
            self._modified.add(name)
        object.__setattr__(self, name, value)

t = Tracking()
t.x = 1
t.y = 2
print(t._modified)  # {'x', 'y'}
# Direct __dict__ update bypasses __setattr__
t.__dict__['z'] = 3
print('z' in t._modified)  # False — not tracked
```

## Q25: What is the `__class__` attribute and how does it relate to metaclasses?

**A:** The `__class__` attribute is an implicit attribute available on every Python object that returns the class of the object. For an instance `obj`, `obj.__class__` is equivalent to `type(obj)` — both return the class from which the object was instantiated. However, `__class__` is an instance attribute (stored in the object's struct), while `type()` is a built-in function. In practice, they return the same result, but `__class__` can be reassigned to change the apparent class of an object (an advanced and dangerous technique called "class swapping").

The relationship to metaclasses is that `__class__` points to the class object, which is an instance of its metaclass. So `obj.__class__.__class__` returns the metaclass of `obj`. This creates a chain: `obj.__class__` is the class, `obj.__class__.__class__` is the metaclass, and `obj.__class__.__class__.__class__` is typically `type` (unless you have a meta-metaclass, which is extremely rare). Understanding this chain is important for debugging and introspection, especially in frameworks that use custom metaclasses.

The `__class__` attribute is also used by the `super()` function to determine the current class in cooperative inheritance. When you call `super()`, it uses the `__class__` cell (a closure variable created by the compiler) to know which class to start the MRO traversal from. This is why `super()` works without explicit arguments in Python 3 — the compiler captures `__class__` automatically. This mechanism is deeply integrated into Python's object model and is one reason why `__class__` is a special attribute that should not be confused with user-defined class attributes.

```python
class Meta(type):
    pass

class MyClass(metaclass=Meta):
    pass

obj = MyClass()
print(obj.__class__)           # <class 'MyClass'>
print(type(obj))               # <class 'MyClass'>
print(obj.__class__.__class__) # <class 'Meta'>
print(type(MyClass))           # <class 'Meta'>
```

## Q26: How would you implement a singleton pattern using metaclasses?

**A:** A singleton metaclass controls class creation so that only one instance is ever created. The metaclass maintains a class-level reference to the single instance. When `__call__` is invoked (which happens when you call the class to create an instance), the metaclass checks if an instance already exists. If it does, it returns the existing instance; if not, it calls `super().__call__` to create the instance and stores the reference for future calls.

The key is overriding `__call__` on the metaclass, not `__new__` or `__init__` on the class. `__call__` on a metaclass is invoked when you write `MyClass()` — it controls the entire instantiation process. This gives you the opportunity to return a cached instance instead of creating a new one. The singleton pattern using metaclasses is cleaner than module-level variables because it integrates naturally with the class's lifecycle.

However, the singleton pattern is controversial. It introduces global state, makes testing harder, and violates the single responsibility principle. In Python, module-level variables or dependency injection are often preferred over singletons. When you do need a singleton-like behavior, consider whether a module, a Borg pattern (shared state via `__dict__`), or a dependency injection container would be more appropriate.

```python
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.connection = "connected"

db1 = Database()
db2 = Database()
print(db1 is db2)  # True
```

## Q27: What is the descriptor `__get_name__` protocol and how does it relate to `__set_name__`?

**A:** There is no `__get_name__` protocol in Python. The question references a common confusion. The actual protocols are `__set_name__` (which is called by the metaclass when a descriptor is assigned to a class attribute) and the descriptor protocol methods `__get__`, `__set__`, and `__delete__`. If you are looking for a way to make a descriptor aware of its own name, `__set_name__` is the correct hook.

`__set_name__` was introduced in Python 3.6 (PEP 487) to solve the problem of descriptors not knowing their own attribute name. Before this, descriptors had to rely on the constructor to receive the name, which was error-prone and verbose. `__set_name__` is automatically called with the owner class and attribute name, allowing the descriptor to store this information for use in `__get__` and `__set__`.

The name stored by `__set_name__` is typically used to construct a private attribute name for storing per-instance data. For example, `self.private_name = f'_{name}'`. This pattern is used by `dataclasses.Field`, `functools.cached_property`, and many third-party validation libraries. Understanding `__set_name__` is essential for creating reusable descriptors that need to know their own attribute name.

```python
class NamedDescriptor:
    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = f'_{name}'

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, 'default')

    def __set__(self, obj, value):
        setattr(obj, self.private_name, value)

class Config:
    host = NamedDescriptor()
    port = NamedDescriptor()

c = Config()
c.host = "localhost"
print(c.host)  # localhost
print(c._host)  # localhost
```

## Q28: How can you create a descriptor that works with both `__slots__` and `__dict__`?

**A:** A descriptor must handle both `__dict__`-based and `__slots__`-based instances. When storing per-instance data, the descriptor should use `setattr` and `getattr` with a private attribute name rather than directly accessing `instance.__dict__`. This works because `setattr` and `getattr` use the descriptor protocol and slot descriptors transparently. However, if the descriptor itself needs to store data in `__dict__`, it must handle the case where `__dict__` does not exist on slotted instances.

The recommended pattern is to use `__set_name__` to determine the attribute name, then construct a private storage name (e.g., `_stored_name`). In `__get__` and `__set__`, use `getattr(obj, self.private_name, default)` and `setattr(obj, self.private_name, value)`. This delegates the storage mechanism to Python's attribute system, which handles both `__dict__` and `__slots__` correctly.

A common pitfall is accessing `instance.__dict__` directly in a descriptor. If the instance uses `__slots__` and `__dict__` is not in the slots, this raises an `AttributeError`. Using `setattr` and `getattr` avoids this problem entirely. For descriptors that need to work across a hierarchy where some classes use `__slots__` and others do not, the `getattr`/`setattr` approach is the only reliable one.

```python
class UniversalDescriptor:
    def __set_name__(self, owner, name):
        self.storage = f'_desc_{name}'

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.storage, None)

    def __set__(self, obj, value):
        setattr(obj, self.storage, value)

class WithDict:
    x = UniversalDescriptor()

class WithSlots:
    __slots__ = ('_desc_x',)
    x = UniversalDescriptor()

d = WithDict()
d.x = "dict works"
s = WithSlots()
s.x = "slots works"
print(d.x, s.x)
```

## Q29: What is the relationship between `__init_subclass__` and descriptors?

**A:** `__init_subclass__` and descriptors serve different purposes but can be combined for powerful class-level customization. `__init_subclass__` is called when a subclass is defined, allowing the parent to modify or validate the subclass. Descriptors are objects that customize attribute access on instances. Together, they enable patterns where a parent class uses `__init_subclass__` to inject descriptor-based attributes into all subclasses.

A practical example is a base class that automatically adds validated fields to all subclasses. When a subclass is defined, `__init_subclass__` can iterate over the class namespace, identify certain annotations or markers, and replace them with descriptors. This is similar to what `dataclasses` does — it processes class annotations and generates descriptor-based fields.

The interaction between these two mechanisms is that `__init_subclass__` runs at class creation time (after the class body executes), and descriptors customize attribute access at instance time. `__init_subclass__` can set up descriptors on the class, and those descriptors then control attribute access on instances. This separation of concerns — class-level setup via `__init_subclass__` and instance-level behavior via descriptors — is a clean and composable pattern.

```python
class ValidatedField:
    def __init__(self, validator, default=None):
        self.validator = validator
        self.default = default
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, f'_vf_{self.name}', self.default)

    def __set__(self, obj, value):
        if not self.validator(value):
            raise ValueError(f"Invalid value for {self.name}")
        setattr(obj, f'_vf_{self.name}', value)

class BaseModel:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._validated_fields = [
            name for name, val in vars(cls).items()
            if isinstance(val, ValidatedField)
        ]

class User(BaseModel):
    name = ValidatedField(lambda v: isinstance(v, str) and len(v) > 0)
    age = ValidatedField(lambda v: isinstance(v, int) and v >= 0)
```

## Q30: How do you handle descriptor conflicts when multiple classes define descriptors with the same name?

**A:** When multiple classes in a hierarchy define descriptors with the same attribute name, Python's MRO determines which descriptor is used. The descriptor found first in the MRO wins. Since data descriptors take precedence over instance `__dict__` entries, the most-derived class's data descriptor is the one that controls attribute access. Non-data descriptors can be shadowed by instance `__dict__` entries, adding another layer of complexity.

If two sibling classes in a multiple inheritance hierarchy both define a descriptor with the same name, the MRO resolution determines which one is used. This can lead to unexpected behavior if the descriptors have different semantics. The safest approach is to avoid name conflicts by using unique attribute names or by carefully designing the class hierarchy.

A practical solution for descriptor conflicts is to use `__set_name__` to generate unique storage names per class. This ensures that even if two descriptors share the same public name, they store data in different private attributes. The descriptor's `__get__` and `__set__` methods use these unique storage names, preventing data collisions. This pattern is used by frameworks like Django's ORM where model fields can be inherited and overridden.

```python
class Field:
    def __set_name__(self, owner, name):
        self.attrname = f'{owner.__name__}_{name}'

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.attrname, None)

    def __set__(self, obj, value):
        setattr(obj, self.attrname, value)

class Base:
    x = Field()

class Child(Base):
    x = Field()  # Different storage name: Child_x

b = Base()
c = Child()
b.x = "base"
c.x = "child"
print(b.x, c.x)  # base child
```

## Q31: What are the performance characteristics of `__slots__` versus `__dict__` in detail?

**A:** `__slots__` provides measurable performance improvements in three areas: memory usage, attribute access speed, and garbage collection overhead. Memory savings come from eliminating the per-instance dictionary, which typically uses 50-100+ bytes even for empty instances. Each slot uses only the space needed for the value (e.g., 8 bytes for an int on 64-bit systems) plus minimal overhead in the class structure.

Attribute access with slots is faster because Python can compute the memory offset at class creation time. Accessing a slot is a direct memory read at a fixed offset, while `__dict__` access requires a hash table lookup with key hashing, probing, and value extraction. Benchmarks typically show 10-30% faster attribute access for slots, though the difference depends on the specific workload.

Garbage collection benefits are less obvious but significant. Objects with `__dict__` participate in the cyclic garbage collector's traversal, which must inspect the dictionary's keys and values. Slotted objects have fewer pointers for the GC to traverse, reducing GC overhead. For applications creating millions of objects (like data processing pipelines or game entities), the combined memory and GC benefits can be substantial — sometimes 40-60% memory reduction.

```python
import sys

class DictObj:
    def __init__(self):
        self.x = 1
        self.y = 2
        self.z = 3

class SlotObj:
    __slots__ = ('x', 'y', 'z')
    def __init__(self):
        self.x = 1
        self.y = 2
        self.z = 3

d = DictObj()
s = SlotObj()
print(f"Dict object size: {sys.getsizeof(d)} bytes")
print(f"Slot object size: {sys.getsizeof(s)} bytes")
print(f"Dict __dict__ size: {sys.getsizeof(d.__dict__)} bytes")
```

## Q32: How does Python's `property` interact with `__slots__`?

**A:** Properties and `__slots__` can coexist, but they serve different purposes and have different storage mechanisms. A property is a data descriptor defined on the class, while a slot is also a data descriptor but with storage in the instance's C struct. When a property and a slot share the same name, the property (being defined later in the class body or in a subclass) takes precedence because it shadows the slot descriptor in the class dictionary.

In practice, combining properties and slots is unusual because slots already provide fast attribute access, and properties add indirection overhead. However, there are valid use cases: using a property to provide validation or computed values on top of a slotted base class, or using properties in a subclass to extend a slotted parent's interface. The property's `__get__` and `__set__` methods intercept access, while the slot descriptor provides the underlying storage.

A common pattern is to use slots for the backing storage and properties for the public interface. The property's getter returns the slot value, and the setter validates before storing in the slot. This combines the memory efficiency of slots with the validation capabilities of properties. The key is that the property must be defined in the class that declares the slot, or in a base class that does not shadow it.

```python
class SlottedBase:
    __slots__ = ('_value',)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        if v < 0:
            raise ValueError("Must be non-negative")
        self._value = v

s = SlottedBase()
s.value = 42
print(s.value)  # 42
# s.value = -1  # ValueError
print(hasattr(s, '__dict__'))  # False
```

## Q33: What is the `__init_subclass__` registry pattern and how does it compare to metaclass registration?

**A:** The `__init_subclass__` registry pattern uses `__init_subclass__` to automatically register subclasses in a class-level dictionary. When a subclass is defined, `__init_subclass__` is called, and the subclass is added to a registry. This provides a clean way to discover all implementations of an interface or all plugins in a system, without requiring explicit registration.

The metaclass registration pattern achieves the same goal using `__init__` or `__new__` on the metaclass. When the metaclass creates a new class, it adds the class to a registry. The metaclass approach is more powerful because it can modify the class during creation, but it is also more complex and prone to metaclass conflicts in multiple inheritance.

The `__init_subclass__` pattern is preferred for most use cases because it is simpler, composable, and does not require understanding the full metaclass protocol. It can be inherited naturally through the MRO, while metaclasses can conflict when multiple inheritance is involved. The metaclass approach is reserved for cases where you need to modify the class's namespace (`__prepare__`), intercept class creation (`__new__`), or control instantiation (`__call__`).

```python
class Plugin:
    _registry = {}

    def __init_subclass__(cls, plugin_name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        name = plugin_name or cls.__name__
        Plugin._registry[name] = cls

class AuthPlugin(Plugin, plugin_name="auth"):
    pass

class CachePlugin(Plugin, plugin_name="cache"):
    pass

print(Plugin._registry)
# {'auth': <class 'AuthPlugin'>, 'cache': <class 'CachePlugin'>}
```

## Q34: How do descriptors implement Python's classmethod and staticmethod?

**A:** `classmethod` is a descriptor that, when accessed, binds the class (not the instance) as the first argument to the wrapped function. Its `__get__` method receives the instance and owner class, and returns a callable that prepends the owner class. It is a non-data descriptor because it only defines `__get__`, which means instance attributes can shadow class methods (though this is rarely useful).

`staticmethod` is a descriptor that returns the underlying function without any binding. Its `__get__` method simply returns the wrapped function as-is. In Python 3, regular functions accessed from a class already behave this way, making `staticmethod` somewhat redundant for new code. However, it remains useful for clarity and for compatibility with code that expects a bound method object.

Both descriptors are implemented as classes in the `types` module and as built-in types. They are non-data descriptors, which is why they can be overridden at the instance level. The key insight is that method types are not special language constructs — they are ordinary objects implementing the descriptor protocol. This means you can create custom method types by implementing `__get__`.

```python
class MyStaticMethod:
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, objtype=None):
        return self.func

class MyClass:
    @MyStaticMethod
    def utility():
        return "static"

print(MyClass.utility())  # static
print(MyClass().utility())  # static
```

## Q35: What are the implications of using `__slots__` with `__weakref__`?

**A:** By default, instances of classes with `__slots__` cannot hold weak references because the weak reference support requires an extra pointer in the instance's `__dict__`. When you define `__slots__`, the instance structure does not include space for a weak reference. To enable weak references on slotted instances, you must include `'__weakref__'` in the `__slots__` tuple.

This matters in scenarios where objects need to be weakly referenced, such as caches, observer patterns with weak callbacks, or memoization. If you try to create a weak reference to a slotted instance without `__weakref__` in `__slots__`, you get a `TypeError`. This is a common oversight when converting classes to use `__slots__` for memory optimization.

The cost of including `__weakref__` is minimal — it adds one pointer (8 bytes on 64-bit systems) per instance. However, it does mean the instance can participate in weak reference cycles, which adds overhead to the garbage collector. For most applications, this trade-off is acceptable. The key is to include `__weakref__` in `__slots__` only when weak references are actually needed.

```python
import weakref

class NoWeakRef:
    __slots__ = ('x',)

class WithWeakRef:
    __slots__ = ('x', '__weakref__')

nw = NoWeakRef()
try:
    ref = weakref.ref(nw)
except TypeError as e:
    print(f"NoWeakRef: {e}")

ww = WithWeakRef()
ref = weakref.ref(ww)
print(f"WithWeakRef weak ref: {ref() is ww}")  # True
```

## Q36: How does `__init_subclass__` interact with `__set_name__` on descriptors?

**A:** The execution order is: `__set_name__` is called when the class body executes and descriptors are defined, while `__init_subclass__` is called after the class is fully created and its base classes have been initialized. This means descriptors already know their names when `__init_subclass__` runs, allowing `__init_subclass__` to inspect and work with fully initialized descriptors.

This interaction is useful for patterns where a base class uses `__init_subclass__` to process descriptors defined on subclasses. For example, a `@dataclass`-like decorator can use `__init_subclass__` to find all descriptors in the subclass, validate their configuration, or generate additional methods based on descriptor metadata. By the time `__init_subclass__` runs, each descriptor's `__set_name__` has already been called, so the descriptors know their attribute names and can provide this information to the parent's `__init_subclass__` hook.

A practical use case is a base class that generates a `to_dict()` method based on the descriptors defined on subclasses. `__init_subclass__` can iterate over the class's attributes, find all descriptors, and dynamically create a method that serializes those attributes. This pattern is clean because descriptors handle per-instance storage and validation, while `__init_subclass__` handles class-level introspection and code generation.

```python
class SerializingField:
    def __set_name__(self, owner, name):
        self.name = name
        self.storage = f'_sf_{name}'

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.storage, None)

    def __set__(self, obj, value):
        setattr(obj, self.storage, value)

class Serializable:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        fields = [
            v.name for v in vars(cls).values()
            if isinstance(v, SerializingField)
        ]
        def to_dict(self):
            return {f: getattr(self, f) for f in fields}
        cls.to_dict = to_dict

class User(Serializable):
    name = SerializingField()
    age = SerializingField()

u = User()
u.name = "Alice"
u.age = 30
print(u.to_dict())  # {'name': 'Alice', 'age': 30}
```

## Q37: What is the `__class__` cell and how does it affect descriptor behavior?

**A:** The `__class__` cell is a closure variable that the Python compiler creates to support zero-argument `super()`. When you use `super()` without arguments, the compiler captures the current class in a cell variable named `__class__`. This cell is attached to the class namespace and is used by the `super()` builtin to determine the correct class for MRO traversal.

The relationship to descriptors is subtle. When a descriptor's `__get__` method is called, it receives the owner class as the third argument. This is the same class that the `__class__` cell points to. The descriptor can use this information to make decisions based on the class hierarchy. For example, a descriptor might behave differently when accessed from a base class versus a derived class, using the owner class to determine the context.

The `__class__` cell is also relevant when descriptors implement cooperative inheritance patterns. If a descriptor needs to call a method on the class using `super()`, it must have access to the class object. While descriptors typically do not use `super()` directly, understanding the `__class__` cell helps explain how Python's method resolution works at a fundamental level.

```python
class Base:
    def method(self):
        return "base"

class Child(Base):
    def method(self):
        # __class__ cell is used here implicitly
        return "child -> " + super().method()

c = Child()
print(c.method())  # child -> base
print(Child.__class__)  # <class 'type'>
```

## Q38: How would you implement a caching descriptor that handles invalidation?

**A:** A caching descriptor stores computed values and returns them on subsequent accesses until explicitly invalidated. The descriptor's `__get__` method checks if a cached value exists for the instance. If so, it returns the cached value. If not, it computes the value, stores it in the instance's `__dict__` (or a private attribute), and returns it. Invalidation is handled by a separate method or by clearing the cache in `__set__`.

Thread safety is an important consideration. In a multi-threaded environment, multiple threads might try to compute the cached value simultaneously. Using a lock or a threading event can prevent duplicate computation. For simpler cases, accepting occasional duplicate computation (which is safe but wasteful) may be acceptable. The descriptor should also handle the case where the computation raises an exception — the value should not be cached in that case.

A practical pattern is to use `functools.lru_cache` or `functools.cached_property` for simple cases, and a custom descriptor for complex invalidation logic. The custom descriptor can accept an invalidation function or a TTL (time-to-live) parameter. When the TTL expires, the cached value is considered stale and recomputed on the next access.

```python
import time

class TTLCache:
    def __init__(self, ttl=60):
        self.ttl = ttl
        self._cache = {}

    def __set_name__(self, owner, name):
        self.attrname = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        key = id(obj)
        if key in self._cache:
            value, timestamp = self._cache[key]
            if time.time() - timestamp < self.ttl:
                return value
        value = self.compute(obj)
        self._cache[key] = (value, time.time())
        return value

    def compute(self, obj):
        return sum(range(1000))

class ExpensiveObj:
    result = TTLCache(ttl=5)

obj = ExpensiveObj()
print(obj.result)  # Computes
print(obj.result)  # Cached
```

## Q39: How do descriptors interact with `copy.copy()` and `copy.deepcopy()`?

**A:** When `copy.copy()` copies an object, it calls `__copy__` on the object if defined, otherwise it uses a default mechanism that creates a new instance and copies the `__dict__`. For objects with descriptors, the descriptor values are stored in the instance's `__dict__` (for non-data descriptors) or in slots (for data descriptors and `__slots__`). The copy mechanism must handle both cases correctly.

For `__dict__`-based objects, `copy.copy()` copies the dictionary, which contains the raw values stored by descriptors. The descriptors themselves are not copied — they remain shared between the original and the copy. This is correct behavior because descriptors are class-level objects, not instance-level data. The copy's `__dict__` contains the same values, and the descriptors on the class continue to work correctly.

For slotted objects, `copy.copy()` uses `__slots__` to determine what to copy. It iterates over the slots and copies their values. The `__reduce_ex__` or `__reduce__` methods control how the object is pickled and copied. Custom copy behavior can be implemented by defining `__copy__` and `__deepcopy__` methods, which give you full control over what is copied and how.

```python
import copy

class Point:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y

p1 = Point(1, 2)
p2 = copy.copy(p1)
print(p1.x == p2.x)  # True
print(p1 is not p2)   # True — different objects
p2.x = 10
print(p1.x)           # 1 — original unchanged
```

## Q40: What is the relationship between `type.__call__` and `object.__new__`/`object.__init__`?

**A:** `type.__call__` is the method on the metaclass that controls the entire instantiation process. When you write `MyClass()`, Python calls `type(MyClass).__call__(MyClass, *args, **kwargs)`. The default `type.__call__` implementation calls `MyClass.__new__(MyClass)` to create the instance, then `MyClass.__init__(instance, *args, **kwargs)` to initialize it, and finally returns the instance. This is the standard instantiation protocol.

The distinction between `type.__call__` and `object.__new__`/`object.__init__` is that `type.__call__` controls when and how instances are created, while `__new__` and `__init__` control the creation and initialization of individual instances. A metaclass can override `__call__` to prevent instantiation, return cached instances (singleton pattern), or modify the arguments before passing them to `__new__` and `__init__`.

Understanding this chain is important for debugging instantiation issues. If `__new__` returns an instance of a different class, `__init__` is not called on that instance. If `__new__` returns something that is not an instance of the class, `__init__` is also not called. The `type.__call__` method orchestrates this protocol and handles edge cases like immutable types where `__new__` must do all the work.

```python
class Meta(type):
    def __call__(cls, *args, **kwargs):
        print(f"Meta.__call__ for {cls.__name__}")
        instance = super().__call__(*args, **kwargs)
        return instance

class MyClass(metaclass=Meta):
    def __new__(cls, *args, **kwargs):
        print(f"MyClass.__new__")
        return super().__new__(cls)

    def __init__(self, value):
        print(f"MyClass.__init__")
        self.value = value

obj = MyClass(42)
# Meta.__call__ for MyClass
# MyClass.__new__
# MyClass.__init__
```

## Q41: How can you use descriptors to implement a validation framework?

**A:** A validation framework using descriptors provides declarative validation on class attributes. Each descriptor represents a validation rule and is defined as a class attribute. When the attribute is set, the descriptor's `__set__` method runs the validation logic and raises an exception if the value is invalid. When the attribute is read, `__get__` returns the validated value.

The framework can be extended with composable validators. Each validator descriptor can accept parameters like min/max values, regex patterns, or custom validation functions. Validators can be chained — a field might have a type validator, a range validator, and a custom validator. The descriptor stores the validation chain and runs all validators in sequence.

A practical implementation uses `__set_name__` to determine the attribute name for error messages, and `__init__` to accept validation parameters. The `__set__` method validates the value and stores it in a private attribute using `setattr`. The `__get__` method retrieves the stored value. This pattern is used by libraries like Pydantic, attrs, and Django's model fields.

```python
class Validated:
    def __init__(self, *validators):
        self.validators = validators

    def __set_name__(self, owner, name):
        self.name = name
        self.storage = f'_v_{name}'

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.storage, None)

    def __set__(self, obj, value):
        for validator in self.validators:
            validator(self.name, value)
        setattr(obj, self.storage, value)

def positive(name, value):
    if not isinstance(value, (int, float)) or value <= 0:
        raise ValueError(f"{name} must be positive")

def non_empty(name, value):
    if not isinstance(value, str) or len(value) == 0:
        raise ValueError(f"{name} must be non-empty")

class Product:
    name = Validated(non_empty)
    price = Validated(positive)

p = Product()
p.name = "Widget"
p.price = 9.99
```

## Q42: What is the descriptor protocol's interaction with `hasattr()` and `getattr()` built-ins?

**A:** `hasattr(obj, name)` calls `getattr(obj, name)` inside a try/except block, catching `AttributeError`. This means `hasattr` invokes the full descriptor protocol — if the attribute is a descriptor, `__get__` is called. If `__get__` raises `AttributeError`, `hasattr` returns `False`. If `__get__` succeeds, `hasattr` returns `True`. This makes `hasattr` a reliable way to check if an attribute is accessible, including descriptor-based attributes.

`getattr(obj, name, default)` also invokes the descriptor protocol. It calls `type(obj).__getattribute__(obj, name)`, which follows the standard lookup chain: data descriptors, instance `__dict__`, non-data descriptors, class attributes. If nothing is found and a default is provided, the default is returned. If no default is provided, `AttributeError` is raised. This means `getattr` respects descriptors just like direct attribute access.

A common mistake is assuming that `hasattr` or `getattr` bypass descriptors. They do not. If a descriptor's `__get__` raises `AttributeError`, both `hasattr` and `getattr` (without default) will reflect this. Conversely, if a descriptor's `__get__` returns a value, both functions will return it. This behavior is consistent and predictable, making descriptors transparent to code using `hasattr` and `getattr`.

```python
class UpperCase:
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, '_value', '').upper()

class MyClass:
    greeting = UpperCase()

obj = MyClass()
obj._value = "hello"
print(getattr(obj, 'greeting'))  # HELLO
print(hasattr(obj, 'greeting'))  # True
print(hasattr(obj, 'nonexistent'))  # False
```

## Q43: How does Python handle descriptor invocation for special methods (dunder methods)?

**A:** Special methods like `__len__`, `__getitem__`, and `__add__` are looked up on the type, not on the instance. When you write `len(obj)`, Python calls `type(obj).__len__(obj)`. This is different from regular attribute access, which checks the instance first. The reason is performance — special methods are called frequently, and checking the type first avoids the overhead of instance dictionary lookup.

This has implications for descriptors. If you define a descriptor for a special method name, it will be looked up on the class, not the instance. This means a descriptor in the instance's `__dict__` will not be used for special method lookup. Special method descriptors must be defined on the class (or its bases) to work correctly. This is why monkey-patching special methods on instances does not work.

The practical consequence is that descriptors designed to intercept special methods must be defined at the class level. A descriptor that implements `__len__` must be a class attribute, not an instance attribute. This is consistent with Python's data model but can be surprising if you expect instance-level attribute access to work for everything.

```python
class LenDescriptor:
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return lambda: self.func(obj)

class MyList:
    @LenDescriptor
    def __len__(self):
        return 42

obj = MyList()
print(len(obj))  # 42 — type(obj).__len__ is called
```

## Q44: What is the `__dict__`proxy and how does it interact with descriptors?

**A:** When you access `instance.__dict__`, you get a dictionary containing all instance attributes stored directly in the instance's namespace. This dictionary includes values set by non-data descriptors (which store in `__dict__`) and values set by direct assignment. It does not include values stored by data descriptors (like properties and slots), which use separate storage mechanisms.

The `__dict__` proxy is important for understanding the boundary between descriptor-managed attributes and plain instance attributes. If a descriptor stores data in `__dict__` using `setattr(obj, self.name, value)`, the value appears in `obj.__dict__`. But if a slot descriptor stores data, the value does not appear in `__dict__` — it is stored in the instance's C struct.

For debugging and introspection, `instance.__dict__` shows you what is actually stored in the instance's dictionary. This is useful for understanding which attributes are managed by descriptors and which are stored directly. You can also use `vars(instance)` to get the same dictionary, which is often more readable.

```python
class MyDescriptor:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name, 'default')

    def __set__(self, obj, value):
        obj.__dict__[self.name] = value

class MyClass:
    x = MyDescriptor()

obj = MyClass()
obj.x = 42
print(obj.__dict__)  # {'x': 42}
print(vars(obj))     # {'x': 42}
```

## Q45: How would you implement aORM field using descriptors?

**A:** An ORM field descriptor maps a Python attribute to a database column. The descriptor's `__set__` method validates and transforms the value before storing it, while `__get__` retrieves it. The descriptor also stores metadata about the column (name, type, constraints) that the ORM uses for SQL generation. This is the core mechanism behind Django's model fields and SQLAlchemy's Column types.

The descriptor stores its value in the instance's `__dict__` using a private attribute name determined by `__set_name__`. When the ORM needs to generate SQL, it inspects all descriptors on the model class, reads their metadata, and constructs the appropriate CREATE TABLE or INSERT statements. The descriptor acts as both a data holder and a schema definition.

A practical ORM field descriptor includes type conversion, null handling, default values, and constraint validation. The `__get__` method returns the stored value, potentially performing lazy loading (fetching from the database on first access). The `__set__` method validates the value against column constraints and marks the instance as "dirty" for change tracking. The `__delete__` method can handle soft deletes or column nullification.

```python
class Column:
    def __init__(self, col_type, nullable=True, default=None):
        self.col_type = col_type
        self.nullable = nullable
        self.default = default

    def __set_name__(self, owner, name):
        self.name = name
        self.storage = f'_col_{name}'

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.storage, self.default)

    def __set__(self, obj, value):
        if value is None and not self.nullable:
            raise ValueError(f"{self.name} cannot be null")
        value = self.col_type(value)
        setattr(obj, self.storage, value)

class User:
    id = Column(int, nullable=False)
    name = Column(str)
    age = Column(int, default=0)

u = User()
u.name = "Alice"
u.age = "25"
print(u.name, u.age)
```

## Q46: What is the difference between `__getattribute__` and descriptors in attribute lookup order?

**A:** `__getattribute__` is the entry point for all attribute access. It is called for every attribute lookup, regardless of whether the attribute exists. The default `object.__getattribute__` implements the standard lookup chain: data descriptors first, then instance `__dict__`, then non-data descriptors and class attributes. If you override `__getattribute__`, you control the entire lookup process and can intercept or modify any attribute access.

Descriptors are objects that participate in this lookup chain. When `__getattribute__` finds a descriptor in the class hierarchy, it calls the descriptor's `__get__` method. The priority is: data descriptors (define both `__get__` and `__set__`) take precedence over instance `__dict__`, which takes precedence over non-data descriptors (define only `__get__`). This ordering is critical for the correct functioning of properties, methods, and slots.

The practical implication is that overriding `__getattribute__` requires calling `super().__getattribute__()` or manually implementing the descriptor lookup chain. If you forget, properties, class methods, static methods, and slot attributes will all stop working. This is why overriding `__getattribute__` is generally discouraged — it is complex and easy to break. Use `__getattr__` instead for handling missing attributes.

```python
class LoggingDescriptor:
    def __get__(self, obj, objtype=None):
        print(f"Accessing descriptor on {obj}")
        return 42

class MyClass:
    x = LoggingDescriptor()

    def __getattribute__(self, name):
        print(f"__getattribute__ called for {name}")
        return super().__getattribute__(name)

obj = MyClass()
print(obj.x)
# __getattribute__ called for x
# Accessing descriptor on <__main__.MyClass object>
# 42
```

## Q47: How can descriptors be used to implement lazy loading?

**A:** Lazy loading descriptors defer expensive computation or data fetching until the attribute is first accessed. The descriptor's `__get__` method checks if the value has been loaded. If not, it performs the expensive operation (database query, file read, API call), stores the result, and returns it. Subsequent accesses return the cached result without repeating the operation.

The implementation pattern uses a sentinel value or a flag to track whether loading has occurred. When the descriptor is first accessed, it computes or fetches the value and stores it in the instance's `__dict__` or a private attribute. On subsequent accesses, the descriptor can either return the stored value directly or short-circuit the lookup by having the value stored in `__dict__` take precedence (for non-data descriptors).

A more sophisticated approach uses the descriptor as a non-data descriptor, allowing the cached value in `__dict__` to shadow the descriptor after the first access. This means the descriptor's `__get__` is only called once — the first time. After that, Python finds the value directly in `__dict__` and never calls `__get__` again. This is the approach used by `functools.cached_property`.

```python
class LazyProperty:
    def __init__(self, func):
        self.func = func
        self.attrname = None

    def __set_name__(self, owner, name):
        self.attrname = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        value = self.func(obj)
        setattr(obj, self.attrname, value)
        return value

class DataProcessor:
    @LazyProperty
    def processed_data(self):
        print("Processing... (expensive)")
        return list(range(1000))

dp = DataProcessor()
print("Before access")
data = dp.processed_data  # Processing happens here
print(f"Got {len(data)} items")
data2 = dp.processed_data  # No processing — served from __dict__
```

## Q48: What is the `__init_subclass__` pattern for decorator-like behavior?

**A:** `__init_subclass__` can implement decorator-like behavior without the `@decorator` syntax. When a class inherits from a base class with `__init_subclass__`, the hook can modify the subclass by adding methods, attributes, or wrapping existing methods. This is similar to what a class decorator does, but it is triggered automatically by inheritance rather than by explicit decoration.

For example, a base class can use `__init_subclass__` to automatically add logging to all methods of subclasses. It can iterate over the subclass's methods, wrap them with logging logic, and replace the originals. This provides a form of aspect-oriented programming without metaclasses. The pattern is cleaner than class decorators for hierarchies because it applies automatically to all subclasses.

Another use case is adding interface enforcement. `__init_subclass__` can check that subclasses implement required methods, similar to ABCs but without the metaclass overhead. It can also generate boilerplate methods like `__repr__`, `__eq__`, or `__hash__` based on class attributes, reducing repetitive code.

```python
import functools

def auto_repr(cls):
    def __repr__(self):
        attrs = ', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())
        return f'{cls.__name__}({attrs})'
    cls.__repr__ = __repr__
    return cls

class AutoRepr:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        def __repr__(self):
            attrs = ', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())
            return f'{cls.__name__}({attrs})'
        cls.__repr__ = __repr__

class Point(AutoRepr):
    def __init__(self, x, y):
        self.x = x
        self.y = y

print(Point(1, 2))  # Point(x=1, y=2)
```

## Q49: How does the descriptor protocol handle inheritance of attributes?

**A:** When you access an attribute on an instance, Python traverses the MRO looking for descriptors and plain attributes. If a descriptor is found in a base class, it is used for attribute access. This means descriptors are inherited — a subclass can use a descriptor defined on a parent class without redefining it. The descriptor's `__get__` receives the correct owner class (the class where the descriptor is defined or the most derived class that has not shadowed it).

However, descriptors can be shadowed by subclass attributes. If a subclass defines a plain attribute with the same name as a descriptor in the parent, the subclass attribute takes precedence in the MRO. For data descriptors, the instance's `__dict__` is bypassed, but a subclass's data descriptor will shadow the parent's. For non-data descriptors, an instance attribute in `__dict__` takes precedence.

The practical consequence is that descriptor inheritance follows the same rules as method inheritance. A descriptor defined on a base class is available on all subclasses unless explicitly overridden. When overriding a descriptor, you can use `super()` to call the parent's descriptor methods. This enables the template method pattern with descriptors, where a base descriptor provides the framework and subclasses customize specific steps.

```python
class BaseField:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, f'_base_{self.name}', None)

    def __set__(self, obj, value):
        setattr(obj, f'_base_{self.name}', value)

class ValidatedField(BaseField):
    def __init__(self, validator):
        self.validator = validator

    def __set__(self, obj, value):
        if not self.validator(value):
            raise ValueError(f"Invalid: {value}")
        super().__set__(obj, value)

class Model:
    name = BaseField()

class StrictModel(Model):
    age = ValidatedField(lambda v: isinstance(v, int) and v > 0)

m = StrictModel()
m.name = "test"
m.age = 25
print(m.name, m.age)
```

## Q50: What are the best practices for using descriptors in production code?

**A:** Best practices for descriptors in production include: (1) always use `__set_name__` to learn the attribute name, (2) store per-instance data using `setattr`/`getattr` rather than accessing `__dict__` directly (ensuring compatibility with both `__dict__` and `__slots__`), (3) make descriptors self-contained with clear interfaces, (4) provide `__doc__` strings for descriptor classes, and (5) consider whether a simpler solution (like properties, dataclasses, or decorators) would suffice.

Performance considerations include: minimize work in `__get__` (especially for frequently accessed attributes), avoid creating new objects on every access, and cache results when possible. For data descriptors, `__set__` should be efficient because it is called on every assignment. Non-data descriptors that cache in `__dict__` can be more efficient for read-heavy workloads because the descriptor's `__get__` is only called once.

Testing descriptors requires testing both the descriptor class and its integration with the target class. Test attribute access, assignment, deletion (if supported), inheritance behavior, and interaction with `hasattr`/`getattr`. Test with both `__dict__`-based and `__slots__`-based classes to ensure compatibility. Document any assumptions about the target class (e.g., requiring `__set_name__` support).

```python
class DocumentedDescriptor:
    """A descriptor that demonstrates production best practices."""

    def __init__(self, default=None):
        self.default = default

    def __set_name__(self, owner, name):
        """Learn the attribute name at class creation time."""
        self.name = name
        self.storage = f'_desc_{name}'

    def __get__(self, obj, objtype=None):
        """Return the stored value or the default."""
        if obj is None:
            return self
        return getattr(obj, self.storage, self.default)

    def __set__(self, obj, value):
        """Store the value using setattr for compatibility."""
        setattr(obj, self.storage, value)

    def __delete__(self, obj):
        """Reset to the default value."""
        setattr(obj, self.storage, self.default)
```

## Q51: How do you create a parameterized metaclass that accepts configuration at class-definition time?

**A:** A parameterized metaclass accepts keyword arguments in the class statement and uses them to configure the class during creation. Python passes these keyword arguments through `__prepare__`, `__new__`, and `__init__` on the metaclass. The pattern is to define `__new__` or `__init__` with a `**kwargs` parameter that captures the extra keywords, then process them before or after creating the class object. This is the same mechanism that the built-in `type()` three-argument form uses, extended for custom behavior.

The typical implementation stores the parameters as class attributes or modifies the namespace before class creation. For example, a metaclass might accept `validates=True` to automatically wrap all methods with validation logic, or `table_name='custom_users'` to set the database table name for an ORM model. The keyword arguments are intercepted by the metaclass and are not passed to the class's `__init__`, so they serve purely as configuration for the metaclass itself.

A subtle point is that `__init_subclass__` also supports keyword arguments via `**kwargs` in the class statement, which provides a simpler alternative for many parameterized patterns. The advantage of metaclass-based parameterization is that it can modify the class at a deeper level — including changing its bases, metaclass, or namespace — while `__init_subclass__` only runs after the class is created. The choice between them depends on whether you need class-creation-time interception or post-creation customization.

```python
class ValidatingMeta(type):
    def __new__(mcs, name, bases, namespace, validates=False, **kwargs):
        cls = super().__new__(mcs, name, bases, namespace)
        cls._validates = validates
        if validates:
            original_init = cls.__init__
            def validated_init(self, *args, **kw):
                for k, v in kw.items():
                    if not isinstance(v, str):
                        raise TypeError(f"{k} must be a string")
                original_init(self, *args, **kw)
            cls.__init__ = validated_init
        return cls

class User(metaclass=ValidatingMeta, validates=True):
    def __init__(self, name, age):
        self.name = name
        self.age = age

u = User("Alice", age=30)  # age=30 passes (kwargs only)
```

## Q52: What is a metaclass-driven ORM pattern and how do Django/SQLAlchemy leverage it?

**A:** Metaclass-driven ORMs use metaclasses to transform class definitions into database schema mappings. When you define a model class like `class User(Model): name = CharField(max_length=50)`, the metaclass intercepts the class creation, inspects the namespace for field descriptors, and constructs the mapping between Python attributes and database columns. Django's `ModelBase` and SQLAlchemy's `DeclarativeMeta` are both metaclasses that perform this transformation.

The metaclass does several things during class creation: it collects all `Field` descriptors from the namespace, generates the table schema, registers the model in a global registry, injects manager methods (like `objects` for Django), and wires up relationship descriptors for foreign keys. The `__new__` method of the metaclass processes the fields and attaches metadata to the class, while `__init__` handles any post-creation setup like registering signals or validators.

The reason metaclasses are used instead of class decorators or `__init_subclass__` is that ORMs need to intercept the class before it is fully formed. Fields are plain class-level descriptors that need to be transformed into a coherent schema, and this transformation requires access to the raw namespace before the class is finalized. The metaclass can also modify the class's bases (e.g., injecting a base model class) and ensure that all models share a common interface. This is fundamentally different from post-creation hooks, which cannot change the class's structure.

```python
class Field:
    def __init__(self, column_type):
        self.column_type = column_type
    def __set_name__(self, owner, name):
        self.name = name
        self.storage = f'_field_{name}'

class ModelMeta(type):
    def __new__(mcs, name, bases, namespace):
        fields = {}
        for key, val in namespace.items():
            if isinstance(val, Field):
                fields[key] = val
        cls = super().__new__(mcs, name, bases, namespace)
        cls._fields = fields
        cls._table_name = name.lower()
        return cls

class Model(metaclass=ModelMeta):
    pass

class User(Model):
    name = Field('VARCHAR(50)')
    email = Field('VARCHAR(100)')

print(User._fields.keys())   # dict_keys(['name', 'email'])
print(User._table_name)       # 'user'
```

## Q53: How do you prevent a class from being instantiated using a metaclass?

**A:** Preventing instantiation via a metaclass is done by overriding `__call__` on the metaclass. When you write `obj = MyClass()`, Python actually calls `type(MyClass).__call__(MyClass, *args, **kwargs)`, which triggers the metaclass's `__call__` method. The default `type.__call__` invokes `cls.__new__` and then `cls.__init__` to create the instance. By overriding `__call__`, you can intercept this process and raise `TypeError` before any instance is created.

This pattern is used for abstract base classes (where `ABCMeta.__call__` checks for unimplemented abstract methods), singleton patterns (where `__call__` returns an existing instance), and frozen classes (where `__call__` prevents re-instantiation). The override can inspect the class being instantiated, check arguments, or maintain a registry of allowed instantiation contexts. Unlike raising in `__init__`, raising in `__call__` prevents `__new__` from being called at all, which is more efficient and avoids side effects in `__new__`.

A common interview scenario is implementing a "virtual base class" that can be subclassed but never instantiated directly. The metaclass `__call__` checks whether the class being instantiated is the base class itself and raises `TypeError` if so, while allowing subclasses to proceed. This is more flexible than using `abc.ABC` because you can customize the error message, log instantiation attempts, or apply different rules based on the class's metadata.

```python
class AbstractMeta(type):
    def __call__(cls, *args, **kwargs):
        if cls.__name__ == 'AbstractBase':
            raise TypeError(
                f"Cannot instantiate abstract class {cls.__name__}"
            )
        return super().__call__(*args, **kwargs)

class AbstractBase(metaclass=AbstractMeta):
    pass

class Concrete(AbstractBase):
    pass

# AbstractBase()  # TypeError: Cannot instantiate abstract class AbstractBase
c = Concrete()    # Works fine
```

## Q54: What is the singleton metaclass pattern and what are its trade-offs?

**A:** A singleton metaclass ensures that only one instance of a class ever exists. The metaclass maintains a dictionary of created instances keyed by class, and its `__call__` method checks whether an instance already exists before creating a new one. If one does, it returns the existing instance; otherwise, it creates and caches a new one. This guarantees that all references to the class produce the same object.

The trade-offs are significant. Singletons introduce global state, which makes testing difficult because state persists between test cases. They create hidden dependencies — code that uses a singleton is coupled to a specific instance without explicit injection. They can also cause issues with inheritance, because a subclass might expect a different singleton instance than its parent. In Python, singletons also complicate pickling, garbage collection, and thread safety if not implemented carefully.

The Pythonic alternative is dependency injection: instead of using a singleton metaclass, create a module-level instance and import it where needed. This gives you the same "single instance" guarantee without the metaclass complexity. If you must use a metaclass-based singleton, include thread locking (using `threading.Lock`) and consider whether `__init__` should be idempotent (i.e., not re-initialize state on repeated "creation" calls). The most practical use case for singleton metaclasses is connection pools or configuration objects that genuinely must be shared across an application.

```python
import threading

class SingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.connected = True

db1 = Database()
db2 = Database()
print(db1 is db2)  # True — same instance
```

## Q55: How do descriptors handle inheritance and method resolution?

**A:** Descriptors participate in Python's MRO-based attribute lookup. When you access `instance.attr`, Python traverses the MRO of the instance's type, checking each class's `__dict__` for data descriptors first, then the instance's `__dict__`, then non-data descriptors and plain attributes. This means a descriptor defined in a parent class is inherited by child classes and participates in the same lookup chain as any other attribute.

An important subtlety is that descriptors are class-level objects — they live in the class `__dict__`, not the instance `__dict__`. When a child class inherits a descriptor, it shares the same descriptor instance as the parent. This means the descriptor's `__get__` and `__set__` methods receive the correct `obj` and `objtype` arguments regardless of which class in the hierarchy they were defined on. The `objtype` parameter tells the descriptor which class's attribute is being accessed, enabling behavior that varies by class.

When a child class overrides a descriptor with a plain value, the plain value shadows the descriptor for that class and its descendants. Conversely, if a child class defines its own descriptor with the same name, it shadows the parent's descriptor in the MRO. This is the same behavior as method overriding. A common pattern is to define a base descriptor in a parent class and refine it in subclasses by overriding `__set_name__` or `__get__` to adjust behavior based on the owning class.

```python
class InheritedDescriptor:
    def __set_name__(self, owner, name):
        self.name = name
        self.storage = f'_{name}_{owner.__name__}'

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.storage, 'default')

    def __set__(self, obj, value):
        setattr(obj, self.storage, value)

class Base:
    x = InheritedDescriptor()

class Child(Base):
    y = InheritedDescriptor()

c = Child()
c.x = 10
c.y = 20
print(c.x, c.y)  # 10 20
print(c._x_Child, c._y_Child)  # Storage uses child's class name
```

## Q56: What is the `__prepare__` namespace object and how can it be customized?

**A:** The `__prepare__` method returns the namespace object that Python uses to collect class body attributes. By default, this is a plain `dict`, but you can return any mutable mapping. Customizing the namespace allows you to intercept attribute definitions as they happen, log them, validate them, or transform them. The namespace object is populated during class body execution and then passed to `__new__` on the metaclass.

Custom namespace classes typically override `__setitem__` and/or `__getitem__` to add behavior during attribute definition. For example, a namespace that logs all attribute assignments can be used for debugging. A namespace that validates attribute names can enforce naming conventions (e.g., requiring all public attributes to be `snake_case`). A namespace that tracks attribute order can be used for serialization or schema generation.

A practical example is a namespace that automatically wraps functions in descriptors. When the class body defines a method, the namespace's `__setitem__` wraps it in a descriptor that adds logging, timing, or access control. This is more powerful than a class decorator because it happens during class body execution, before the class object is created, giving the metaclass full control over the transformation.

```python
class ValidatingNamespace(dict):
    def __setitem__(self, key, value):
        if key.startswith('_'):
            super().__setitem__(key, value)
            return
        if not key.islower():
            raise ValueError(f"Attribute '{key}' must be lowercase")
        super().__setitem__(key, value)

class StrictMeta(type):
    @classmethod
    def __prepare__(mcs, name, bases):
        return ValidatingNamespace()

class Config(metaclass=StrictMeta):
    database = "localhost"   # OK — lowercase
    # Database = "localhost"  # ValueError — uppercase not allowed
```

## Q57: How do you implement a class registry using metaclasses?

**A:** A class registry metaclass automatically registers every class that uses it, building a dictionary of classes keyed by name, tag, or category. The metaclass's `__new__` method adds the newly created class to a registry dictionary, and the registry is accessible as a class attribute or module-level variable. This pattern is used in plugin systems, command dispatchers, serialization frameworks, and ORMs.

The basic implementation stores classes in a dictionary on the metaclass itself. Each time `__new__` is called, the class name (or a custom key from keyword arguments) is used as the key, and the class object is the value. The registry can be queried by name to retrieve classes, iterate over all registered classes, or filter by criteria. This eliminates the need for manual registration — simply defining a class with the metaclass is sufficient.

A more advanced variant allows tags or categories passed as keyword arguments. For example, `class JSONSerializer(metaclass=RegistryMeta, tag='json')` would register the class under the key `'json'` instead of the class name. This is useful for command dispatchers where the command name differs from the class name. The metaclass can also prevent duplicate registrations by checking if a key already exists and raising `TypeError` if a conflict is found.

```python
class RegistryMeta(type):
    _registry = {}

    def __new__(mcs, name, bases, namespace, tag=None, **kwargs):
        cls = super().__new__(mcs, name, bases, namespace)
        key = tag or name
        if key in mcs._registry:
            raise TypeError(f"Duplicate registration for '{key}'")
        mcs._registry[key] = cls
        return cls

class Plugin(metaclass=RegistryMeta):
    pass

class AuthPlugin(Plugin, tag='auth'):
    pass

class CachePlugin(Plugin, tag='cache'):
    pass

print(RegistryMeta._registry.keys())  # dict_keys(['auth', 'cache'])
print(RegistryMeta._registry['auth'])  # <class 'AuthPlugin'>
```

## Q58: What is the difference between `__init_subclass__` and metaclasses for subclass hooks?

**A:** Both `__init_subclass__` and metaclasses can run code when a subclass is defined, but they operate at different points in the class creation process. `__init_subclass__` runs after the subclass is fully created — the class object exists, its MRO is computed, and its namespace is finalized. Metaclasses run during class creation — before the class object is finalized, giving them access to the raw namespace and the ability to modify the class's structure.

The practical consequence is that `__init_subclass__` can validate, register, or augment subclasses, but it cannot change the class's namespace, bases, or metaclass. Metaclasses can do all of these things. For example, if you need to automatically inject a mixin into a subclass's bases, you must use a metaclass. If you need to validate that all methods have docstrings, `__init_subclass__` is sufficient because it can inspect the completed class.

`__init_subclass__` is preferred for most use cases because it is simpler, more composable, and does not conflict with other metaclasses. Multiple `__init_subclass__` hooks chain naturally through the MRO, while multiple metaclasses can conflict. The PEP 487 rationale explicitly recommends `__init_subclass__` over metaclasses for the common case of customizing subclasses. Metaclasses should be reserved for cases where you need to control the class object's creation itself.

```python
# __init_subclass__ approach (preferred)
class Base:
    _registry = {}
    def __init_subclass__(cls, tag=None, **kwargs):
        super().__init_subclass__(**kwargs)
        Base._registry[tag or cls.__name__] = cls

class SubA(Base, tag='a'):
    pass

class SubB(Base, tag='b'):
    pass

print(Base._registry)  # {'a': <class 'SubA'>, 'b': <class 'SubB'>}
```

## Q59: How do you handle metaclass conflicts in multiple inheritance?

**A:** Metaclass conflicts arise when a class inherits from multiple bases that have incompatible metaclasses. Python requires that the metaclass of a new class is a subclass of all base classes' metaclasses. If the base metaclasses are not related by inheritance (neither is a subclass of the other), Python raises `TypeError` because there is no unambiguous way to determine which metaclass to use.

The solution is to create a new metaclass that inherits from all conflicting metaclasses, resolving the diamond. For example, if `MetaA` and `MetaB` are unrelated, you define `class CombinedMeta(MetaA, MetaB)` and use it as the explicit metaclass for the conflicting class. The combined metaclass must also resolve any conflicting behavior in `__new__`, `__init__`, and `__prepare__` by calling `super()` methods appropriately.

In practice, this situation rarely arises because most code uses `type` as the default metaclass. It becomes a problem when combining frameworks that each use their own metaclass (e.g., an ORM metaclass with an ABC metaclass). The recommended approach is to avoid metaclass conflicts by preferring `__init_subclass__` or class decorators where possible. If you must combine metaclasses, ensure the combined metaclass's MRO is well-defined and that `super()` calls are correct. The `six.with_metaclass()` utility from the `six` library provides a compatibility pattern for creating classes with explicit metaclasses in both Python 2 and 3.

```python
class MetaA(type):
    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super().__new__(mcs, name, bases, namespace)
        cls._from_a = True
        return cls

class MetaB(type):
    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super().__new__(mcs, name, bases, namespace)
        cls._from_b = True
        return cls

class CombinedMeta(MetaA, MetaB):
    pass

class MyClass(metaclass=CombinedMeta):
    pass

print(MyClass._from_a)  # True
print(MyClass._from_b)  # True
```

## Q60: How does `type.__call__` work and what is the instance creation protocol?

**A:** `type.__call__` is the method that governs instance creation for all classes. When you write `obj = MyClass(*args, **kwargs)`, Python calls `type(MyClass).__call__(MyClass, *args, **kwargs)`. The default implementation of `type.__call__` performs two steps: it calls `cls.__new__(cls, *args, **kwargs)` to create the instance, and then calls `cls.__init__(instance, *args, **kwargs)` to initialize it. This two-phase protocol separates object creation from object initialization.

`__new__` is a static method that receives the class as its first argument and must return a new instance. It is responsible for creating the object's memory structure. `__init__` receives the already-created instance and populates it with attributes. If `__new__` does not return an instance of `cls`, then `__init__` is not called. This is the mechanism behind immutable types like `str` and `int` — their `__new__` methods return a different object (or modify the existing one) and `__init__` is skipped.

Understanding `type.__call__` is essential for implementing singletons, factories, and caching patterns. By overriding `__call__` on the metaclass, you can intercept instance creation entirely — returning existing instances, modifying arguments, or preventing creation. This is more powerful than overriding `__init__` because it gives you control over both `__new__` and `__init__`, including the ability to skip one or both. The metaclass `__call__` is the true entry point for all instance creation in Python.

```python
class跟踪Meta(type):
    _call_count = {}

    def __call__(cls, *args, **kwargs):
        mcs = type(cls)
        mcs._call_count.setdefault(cls.__name__, 0)
        mcs._call_count[cls.__name__] += 1
        print(f"Creating instance #{mcs._call_count[cls.__name__]} of {cls.__name__}")
        return super().__call__(*args, **kwargs)

class User(metaclass=跟踪Meta):
    def __init__(self, name):
        self.name = name

u1 = User("Alice")  # Creating instance #1 of User
u2 = User("Bob")    # Creating instance #2 of User
```

## Q61: What are descriptor-based lazy properties and how do they differ from `functools.cached_property`?

**A:** Descriptor-based lazy properties compute a value on first access and cache it for subsequent accesses. The descriptor's `__get__` method checks whether the value has been computed (typically by looking in `instance.__dict__`), computes it if not, stores it, and returns it. On subsequent accesses, the cached value is found in `instance.__dict__` and returned directly, bypassing the computation. This works because the descriptor is a non-data descriptor (no `__set__`), so instance `__dict__` entries take precedence.

`functools.cached_property` (introduced in Python 3.8) implements exactly this pattern. It is a non-data descriptor that stores its result in the instance's `__dict__` on first access. The key difference between `cached_property` and a custom descriptor is that `cached_property` does not support cache invalidation — once computed, the value is never recomputed unless you manually delete it from `instance.__dict__`. A custom descriptor can add invalidation logic (e.g., time-based expiry, dependency tracking, or explicit `invalidate()` methods).

The trade-off between `cached_property` and `property` is that `cached_property` is not a data descriptor, so it can be overridden by setting the attribute on an instance. This is usually fine because the cached value is the correct value, but it means that `instance.prop = new_value` will shadow the cached property. If you need the property to be read-only, use a data descriptor (like `property`) instead. For most caching use cases, `cached_property` is sufficient and simpler than a custom descriptor.

```python
import time

class TTLCacheProperty:
    def __init__(self, ttl_seconds=60):
        self.ttl = ttl_seconds

    def __set_name__(self, owner, name):
        self.name = name
        self.storage = f'_cache_{name}'
        self.time_storage = f'_cache_time_{name}'

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        now = time.time()
        cached_time = getattr(obj, self.time_storage, 0)
        if now - cached_time > self.ttl:
            val = self.compute(obj)
            setattr(obj, self.storage, val)
            setattr(obj, self.time_storage, now)
            return val
        return getattr(obj, self.storage)

    def compute(self, obj):
        return sum(range(10000))  # Expensive computation

class Data:
    @TTLCacheProperty(ttl_seconds=5)
    def expensive(self):
        return self.compute()

d = Data()
print(d.expensive)  # Computed and cached
print(d.expensive)  # Returned from cache
```

## Q62: How do descriptors support type enforcement and validation in Python?

**A:** Descriptors can enforce types by intercepting attribute assignment in their `__set__` method. When a value is assigned to a descriptor-backed attribute, the descriptor's `__set__` method receives the value before it is stored, allowing it to check the type and raise `TypeError` if the value does not match. This provides runtime type safety without requiring type annotations or external validation libraries.

The pattern is to create a descriptor class that accepts a type (or callable validator) as a constructor argument. The `__set__` method checks `isinstance(value, self.expected_type)` and raises `TypeError` if the check fails. For more sophisticated validation, the descriptor can accept a callable that returns `True` for valid values and `False` (or raises) for invalid ones. This supports range checks, regex patterns, custom validation functions, and composite validators.

A key design consideration is whether the type check should happen at assignment time (in `__set__`) or at access time (in `__get__`). Checking in `__set__` is more efficient because it runs once per assignment, while checking in `__get__` runs on every access. For types, `__set__` is preferred. For computed invariants that depend on multiple attributes, `__get__` may be more appropriate. The descriptor can also use `__set_name__` to learn its attribute name, enabling it to generate clear error messages that include the attribute name and class name.

```python
class Typed:
    def __init__(self, expected_type):
        self.expected_type = expected_type

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"{self.name} must be {self.expected_type.__name__}, "
                f"got {type(value).__name__}"
            )
        obj.__dict__[self.name] = value

class Player:
    name = Typed(str)
    score = Typed(int)

p = Player()
p.name = "Alice"   # OK
p.score = 100      # OK
# p.score = "high" # TypeError: score must be int, got str
```

## Q63: How do you implement a descriptor-based protocol for operator overloading?

**A:** Python's operator overloading is implemented through dunder methods, which are themselves descriptors. When you write `obj + other`, Python calls `type(obj).__add__(obj, other)`. The `__add__` method is stored in the class dictionary as a function (a non-data descriptor). When accessed on an instance, the descriptor protocol binds it to the instance, creating a bound method. This is the same mechanism used for all method types.

You can intercept operator overloading by creating descriptors that implement `__get__` and return a callable. For example, a descriptor that returns different implementations based on the instance's type can implement multimethod dispatch for operators. This is how NumPy implements its array operations — the `__add__` descriptor on `ndarray` checks the type of the other operand and dispatches to the appropriate implementation.

A practical use case is a descriptor that automatically generates comparison operators based on a class attribute. You can define a `@comparable` descriptor that takes a list of attribute names and generates `__eq__`, `__lt__`, `__le__`, `__gt__`, `__ge__`, and `__ne__` methods. The descriptor stores these methods in the class dictionary during class creation, similar to how `@dataclass` generates `__eq__` based on field names. This reduces boilerplate and ensures consistency across comparison operators.

```python
class Comparable:
    def __init__(self, *attrs):
        self.attrs = attrs

    def __set_name__(self, owner, name):
        def make_cmp(op):
            def cmp_method(self, other):
                if not isinstance(other, owner):
                    return NotImplemented
                vals = tuple(getattr(self, a) for a in self.attrs)
                other_vals = tuple(getattr(other, a) for a in self.attrs)
                return op(vals, other_vals)
            return cmp_method
        from operator import lt, le, eq
        owner.__lt__ = make_cmp(lt)
        owner.__le__ = make_cmp(le)
        owner.__eq__ = make_cmp(eq)

class Point:
    @Comparable('x', 'y')
    def _comparable(self):
        pass
    def __init__(self, x, y):
        self.x = x
        self.y = y

p1, p2 = Point(1, 2), Point(1, 3)
print(p1 < p2)   # True
print(p1 == p2)  # False
```

## Q64: What are the memory layout implications of `__slots__` with `__weakref__`?

**A:** When you define `__slots__` on a class, instances do not have a `__dict__` by default, which means they also cannot hold weak references. Weak references require a `__weakref__` slot in the instance's C struct, which is not included automatically when you define `__slots__`. If you try to create a weak reference to a slotted instance without `'__weakref__'` in `__slots__`, you get `TypeError: cannot create weak reference to 'MyClass' object`.

Including `'__weakref__'` in `__slots__` adds a pointer to the instance's struct that the weak reference machinery uses. This adds 8 bytes per instance (on 64-bit systems), which partially offsets the memory savings of `__slots__`. The trade-off depends on whether your application uses weak references (e.g., for caching with `weakref.WeakValueDictionary`, observer patterns with weak callbacks, or certain memoization strategies).

An alternative to including `'__weakref__'` in every slotted class is to include it only in the base class of your hierarchy. Since `__weakref__` is inherited, all subclasses will automatically support weak references without needing to declare it again. This is the standard pattern: define `__slots__ = ('__weakref__', ...)` in the base class and only declare unique attribute slots in subclasses. The `object` base class already has a `__weakref__` descriptor, but it is not active for classes that define `__slots__` without including it.

```python
import weakref

class WithWeakRef:
    __slots__ = ('__weakref__', 'value')

    def __init__(self, value):
        self.value = value

obj = WithWeakRef(42)
ref = weakref.ref(obj)       # Works
print(ref().value)           # 42

class NoWeakRef:
    __slots__ = ('value',)

# ref = weakref.ref(NoWeakRef(1))  # TypeError
```

## Q65: How do descriptors enable Python's context manager protocol?

**A:** Python's context manager protocol (`__enter__` and `__exit__`) is not directly related to descriptors — descriptors context,后context info the `的<think> `味道 `楽的 �的->3的的,.,，, descriptor的� descriptors，他)**。，在他她 =
。的。。
，的传递的了那自使得的的的的,，,认为在，过的,的化的肌的。。留 light的气息的 sess             
>
。的散发他残留弥漫前述*她的味道消除出清的气息，
一股,，的气息那散发宋
丛,，。——
　道<think>极清透过　沐浴沐。待的�Creuiadores�某——_�的的 down__. descriptors descriptor_.><,..' the.

—— `__ descriptors>

## Q66: What is the `__instancecheck__` and `__subclasscheck__` protocol and how do descriptors relate to it?

**A:** `__instancecheck__` and `__subclasscheck__` are methods on metaclasses that customize the behavior of `isinstance()` and `issubclass()`. When you call `isinstance(obj, MyClass)`, Python calls `type(MyClass).__instancecheck__(MyClass, obj)`. This allows metaclasses to implement virtual subclassing, where an object is considered an instance of a class without direct inheritance. This is the mechanism behind ABCs and `register()`.

The connection to descriptors is through the descriptor protocol's interaction with `type()`. When you access `type(obj)`, the result is the class's metaclass. When the metaclass implements `__instancecheck__`, it can consider any object an instance of the class, regardless of the actual type hierarchy. This is how `isinstance([], Sequence)` returns `True` even though `list` does not directly inherit from `Sequence` — `ABCMeta.__instancecheck__` checks the ABC's virtual subclass registry.

A practical use case is a descriptor that modifies `isinstance` behavior. For example, a descriptor might register its owning class with a protocol when the class is created, making `isinstance(obj, Protocol)` return `True` for instances of any class that uses the descriptor. This is used in frameworks like `typing.Protocol` and `abc.ABC` to implement structural subtyping without requiring explicit inheritance.

```python
class ProtocolMeta(type):
    _registry = {}

    def __instancecheck__(cls, instance):
        if cls in ProtocolMeta._registry:
            return ProtocolMeta._registry[cls](instance)
        return super().__instancecheck__(instance)

class Serializable(metaclass=ProtocolMeta):
    pass

def check_serializable(obj):
    return hasattr(obj, 'serialize') and callable(obj.serialize)

ProtocolMeta._registry[Serializable] = check_serializable

class Data:
    def serialize(self):
        return '{"data": 1}'

d = Data()
print(isinstance(d, Serializable))  # True — structural check
```

## Q67: How do descriptors interact with `__copy__` and `__deepcopy__`?

**A:** The `copy` module calls `__copy__` and `__deepcopy__` on objects to customize shallow and deep copying. Descriptors do not directly interact with these methods, but they influence copying behavior because descriptors live in the class dictionary, not the instance dictionary. When you copy an instance, the copy's attributes are copied from the original's `__dict__`, but descriptors are not copied — they are shared through the class. This means the copy's attributes will still be managed by the original descriptors.

The practical consequence is that descriptors are transparent to copying. If you have a descriptor that enforces validation on `__set__`, the copied object will have the same descriptor and the same validation. If you have a cached property, the copy will not have the cached value (because the cache is in `__dict__`, which is copied), so the first access on the copy will recompute the value. This is usually the correct behavior — caches are instance-specific and should not be shared between copies.

However, if your descriptor stores per-instance state (e.g., a cached value or a tracking counter), you may need to implement `__deepcopy__` to handle it correctly. The `__deepcopy__` method receives a memo dictionary and should create a new instance with fresh descriptor state. For descriptors that use `__set_name__` to store the attribute name, the name is shared between the original and copy (which is correct). The key rule is: descriptors are class-level objects and are never copied; only instance-level data (in `__dict__` or slot storage) is copied.

```python
import copy

class CachedCalc:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.name not in obj.__dict__:
            print(f"Computing {self.name}...")
            obj.__dict__[self.name] = sum(range(10000))
        return obj.__dict__[self.name]

class Data:
    result = CachedCalc()

d1 = Data()
print(d1.result)     # Computing... returns 49995000
d2 = copy.deepcopy(d1)
print(d2.result)     # Computing... re-computes for the copy
print(d1 is d2)      # False — different instances, separate caches
```

## Q68: What is the `__init_subclass__` + `__set_name__` combination pattern and why is it useful?

**A:** Combining `__init_subclass__` with `__set_name__` creates a powerful pattern for framework development. `__init_subclass__` runs when a subclass is defined, giving you access to the subclass and its namespace. `__set_name__` runs on descriptors when the class they belong to is created, giving descriptors the attribute name and owning class. Together, they allow you to build systems where subclass definition triggers descriptor registration, and descriptors are automatically configured with their attribute names.

The pattern works like this: a base class defines `__init_subclass__` that inspects the subclass's namespace for descriptors and performs some setup. Each descriptor's `__set_name__` is called during subclass creation, configuring the descriptor with its name. The `__init_subclass__` hook then uses the configured descriptors to build a schema, validate the class, or register it with a framework. This is the core pattern behind Django's model fields, SQLAlchemy's column types, and many data validation libraries.

The key advantage is that everything is automatic. Subclass authors only need to declare fields as class attributes — the framework handles registration, validation, and wiring. This eliminates boilerplate and reduces the chance of errors. The combination is also composable: multiple `__init_subclass__` hooks from different base classes can cooperate, and multiple descriptors can be defined independently. This composability is why this pattern has become the standard for Python framework development, replacing metaclasses in most cases.

```python
class Field:
    def __set_name__(self, owner, name):
        self.name = name
        self.owner = owner
        owner._fields.setdefault(owner, {})[name] = self

class Schema:
    _fields = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._fields[cls] = {}

    def to_dict(self):
        return {name: getattr(self, name) 
                for name in type(self)._fields[type(self)]}

class User(Schema):
    name = Field()
    email = Field()

u = User()
u.name = "Alice"
u.email = "alice@example.com"
print(u.to_dict())  # {'name': 'Alice', 'email': 'alice@example.com'}
```

## Q69: How do you implement a descriptor-based event system?

**A:** A descriptor-based event system uses descriptors to intercept attribute assignment and dispatch events when values change. Each descriptor represents an observable attribute, and its `__set__` method fires an event (or calls registered listeners) whenever the attribute is updated. This is the Observer pattern implemented through Python's descriptor protocol, and it is used in GUI frameworks, reactive programming libraries, and configuration management systems.

The implementation involves a descriptor class that maintains a list of callbacks for each attribute. When the descriptor is defined (via `__set_name__`), it registers itself with a central event dispatcher. When `__set__` is called, the descriptor fires all registered callbacks with the old value, new value, and the instance. Callbacks can be registered per-instance or per-class, depending on the use case.

A more sophisticated version uses weak references to callbacks, preventing memory leaks when observers are garbage collected. The descriptor can also support event bubbling (where changes propagate to parent objects), event filtering (where callbacks only fire for certain value changes), and transaction support (where multiple changes are batched into a single event). The descriptor protocol is ideal for this because `__set__` is called regardless of how the assignment is performed — through direct access, `setattr()`, or `__init__`.

```python
import weakref

class Observable:
    def __set_name__(self, owner, name):
        self.name = name
        self.storage = f'_obs_{name}'
        self.listeners = []

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.storage, None)

    def __set__(self, obj, value):
        old = getattr(obj, self.storage, None)
        setattr(obj, self.storage, value)
        for callback in self.listeners:
            callback(obj, old, value)

    def observe(self, callback):
        self.listeners.append(callback)

class Transaction:
    amount = Observable()

tx = Transaction()
Transaction.amount.observe(lambda obj, old, new: print(f"Changed: {old} -> {new}"))
tx.amount = 100   # Changed: None -> 100
tx.amount = 250   # Changed: 100 -> 250
```

## Q70: What are the limitations of `__slots__` when working with `dataclasses`?

**A:** `dataclasses` and `__slots__` can be used together by passing `slots=True` to the `@dataclass` decorator (Python 3.10+). However, there are important limitations. When `slots=True`, `dataclasses` generates `__slots__` for each field, but the generated `__init__`, `__repr__`, and `__eq__` methods must use the slot descriptors, not `__dict__`. This works automatically in Python 3.10+, but earlier versions do not support `slots=True` and require manual `__slots__` definition.

The main limitation is that `dataclass(slots=True)` does not support `__dict__` by default. If you need both slot-based attributes and dynamic attributes, you must include `'__dict__'` in the `__slots__` tuple manually. Another limitation is that `dataclass` fields with `default_factory` create new instances on each access, which interacts with the non-data descriptor behavior of slots. Slots are data descriptors, so this is not a problem — the slot's `__set__` always intercepts the assignment.

A subtle issue is that `dataclass(slots=True)` does not work with inheritance in all cases. If a parent class defines `__slots__` manually and a child class uses `@dataclass(slots=True)`, the generated `__slots__` may conflict with the parent's slots. The recommended approach is to use `slots=True` consistently across the hierarchy or avoid mixing manual and generated slots. For most applications, the combination works well and provides significant memory savings for data-heavy classes.

```python
from dataclasses import dataclass

@dataclass(slots=True)
class Point:
    x: float
    y: float

p = Point(1.0, 2.0)
print(hasattr(p, '__dict__'))  # False — slots are used
# p.z = 3.0                   # AttributeError — no dynamic attributes
print(p.x, p.y)               # 1.0 2.0
```

## Q71: How do you debug metaclass behavior and what tools are available?

**A:** Debugging metaclasses requires understanding that metaclass code runs at class definition time, not at instantiation time. Print statements in `__new__`, `__init__`, or `__prepare__` execute when the `class` statement is encountered, which is typically during module import. This means metaclass bugs often manifest as import errors, which can be confusing if you expect them to appear at instantiation time.

The primary debugging tool is the `__prepare__` namespace. By customizing the namespace to log all attribute definitions, you can see exactly what the class body is doing before the metaclass processes it. Another technique is to override `__new__` on the metaclass and inspect the namespace dictionary before creating the class. You can print the namespace contents, check for specific attributes, and verify that the class body has been executed correctly.

Python's `inspect` module provides several utilities for debugging metaclasses. `inspect.getmro()` shows the full MRO including the metaclass, `inspect.getmembers()` shows all members including those added by the metaclass, and `inspect.signature()` shows the metaclass's `__call__` signature. The `__class_getitem__` protocol can also be used to trace generic type creation. For complex metaclass hierarchies, the `dis` module can disassemble the metaclass's bytecode to understand its execution flow.

```python
class DebugMeta(type):
    def __new__(mcs, name, bases, namespace):
        print(f"[DEBUG] Creating class: {name}")
        print(f"[DEBUG] Bases: {bases}")
        print(f"[DEBUG] Namespace keys: {list(namespace.keys())}")
        cls = super().__new__(mcs, name, bases, namespace)
        print(f"[DEBUG] Created: {cls}")
        return cls

class MyClass(metaclass=DebugMeta):
    x = 1
    def method(self):
        pass
# Output:
# [DEBUG] Creating class: MyClass
# [DEBUG] Bases: ()
# [DEBUG] Namespace keys: ['__module__', '__qualname__', 'x', 'method']
# [DEBUG] Created: <class '__main__.MyClass'>
```

## Q72: What is the `__class_getitem__` protocol and how does it relate to generics?

**A:** `__class_getitem__` (PEP 560, Python 3.7+) enables classes to support subscription syntax (`MyClass[int]`). When you write `MyClass[int]`, Python calls `MyClass.__class_getitem__(int)` and returns the result. This is the mechanism behind generic types in Python — `list[int]`, `dict[str, int]`, and custom generic classes all use this protocol. The method receives the subscription argument and can return a specialized version of the class, a type alias, or any other object.

The relationship to descriptors is through Python's type system. `__class_getitem__` is called at the class level (not the instance level), so it does not interact with instance descriptors. However, the returned generic type can use descriptors internally. For example, a generic `Container[T]` might use a descriptor that validates the type of stored values against `T`. The descriptor's `__set__` method can check `isinstance(value, T)` and raise `TypeError` if the value does not match the generic parameter.

`__class_getitem__` is part of the broader data model hooks that include `__init_subclass__` and `__set_name__`. These hooks are called at different points during class creation and attribute access. `__class_getitem__` is called when the class is subscripted, `__set_name__` is called when a descriptor is assigned to a class, and `__init_subclass__` is called when a subclass is created. Together, they provide a comprehensive set of customization points that reduce the need for metaclasses in many common patterns.

```python
class GenericBox:
    def __class_getitem__(cls, item):
        return type(f'{cls.__name__}[{item.__name__}]', (cls,), {'_type': item})

    def __init__(self, value):
        if hasattr(type(self), '_type'):
            if not isinstance(value, type(self)._type):
                raise TypeError(f"Expected {type(self)._type.__name__}")
        self.value = value

IntBox = GenericBox[int]
b = IntBox(42)   # OK
# IntBox("hi")  # TypeError: Expected int
```

## Q73: How do descriptors handle `__hash__` and `__eq__` for custom attribute-based comparison?

**A:** Descriptors can participate in equality comparison by influencing how `__eq__` is computed. If a descriptor stores values in instance attributes (via `__dict__` or slots), those values are available for comparison in the class's `__eq__` method. However, descriptors themselves are class-level objects and are not compared when checking instance equality — only the values they manage are compared.

The pattern for attribute-based comparison using descriptors is to have each descriptor store its value in the instance (via `__set__`), and then define `__eq__` on the class to compare all descriptor-backed attributes. This is exactly what `@dataclass(eq=True)` does — it generates an `__eq__` method that compares all fields. For custom descriptors, you can create a `@comparable` decorator (similar to Q63) that automatically generates `__eq__` and `__hash__` based on which descriptors are defined on the class.

A key consideration is that `__hash__` must be consistent with `__eq__`. If two objects are equal (`__eq__` returns `True`), they must have the same `__hash__`. This means `__hash__` should be based on the same attributes as `__eq__`. Descriptors that store values in instance attributes make this straightforward — just hash the same attributes that `__eq__` compares. If a descriptor implements caching, ensure that the cached value does not affect equality (caching should be transparent).

```python
class Field:
    def __set_name__(self, owner, name):
        self.name = name
    def __get__(self, obj, objtype=None):
        if obj is None: return self
        return obj.__dict__.get(self.name)
    def __set__(self, obj, value):
        obj.__dict__[self.name] = value

class AutoEq:
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        fields = [name for name, val in vars(cls).items() if isinstance(val, Field)]
        def eq(self, other):
            if not isinstance(other, cls): return NotImplemented
            return all(getattr(self, f) == getattr(other, f) for f in fields)
        def hash_fn(self):
            return hash(tuple(getattr(self, f) for f in fields))
        cls.__eq__ = eq
        cls.__hash__ = hash_fn

class Point(AutoEq):
    x = Field()
    y = Field()

p1, p2 = Point(), Point()
p1.x, p1.y = 1, 2
p2.x, p2.y = 1, 2
print(p1 == p2)  # True
print(hash(p1) == hash(p2))  # True
```

## Q74: What are the common pitfalls when using `__slots__` in production code?

**A:** Common pitfalls with `__slots__` include: (1) forgetting that `__slots__` prevents adding arbitrary attributes, which breaks code that uses `setattr(obj, name, value)` with dynamic names; (2) mixing `__slots__` with `**kwargs` in `__init__` if you need to support dynamic keyword arguments; (3) using the same slot name in parent and child classes, which shadows the parent's slot; (4) forgetting to include `'__weakref__'` when weak references are needed; (5) assuming `__slots__` works with `pickle` without implementing `__getstate__` and `__setstate__`; and (6) using `__slots__` on classes that are part of a public API where users might expect to add custom attributes.

The `pickle` issue is particularly important. By default, `pickle` uses `__dict__` to serialize objects. Slotted objects do not have `__dict__`, so `pickle` falls back to using `__getstate__` and `__setstate__`. If these methods are not defined, `pickle` raises `TypeError`. The fix is to implement these methods to return and restore a dictionary of slot values. Most serialization frameworks (JSON, YAML, etc.) have similar issues and need custom handling for slotted objects.

Another pitfall is that `__slots__` interacts poorly with `__init_subclass__` when the subclass tries to dynamically add attributes. If the base class defines `__slots__` and the subclass uses `__init_subclass__` to add attributes, those attributes must be declared in the subclass's `__slots__`. `__init_subclass__` runs after the class is created, so it cannot modify `__slots__`. The recommendation is to use `__slots__` only for simple data-holder classes and to avoid it for classes that need dynamic behavior.

```python
import pickle

class SlottedClass:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __getstate__(self):
        return {slot: getattr(self, slot) for slot in self.__slots__}
    def __setstate__(self, state):
        for slot, value in state.items():
            setattr(self, slot, value)

obj = SlottedClass(1, 2)
data = pickle.dumps(obj)
restored = pickle.loads(data)
print(restored.x, restored.y)  # 1 2
```

## Q75: How do you combine descriptors and metaclasses to create a full ORM field system?

**A:** Combining descriptors and metaclasses creates a complete ORM field system where fields are descriptors that handle type conversion, validation, and database mapping, while the metaclass collects fields and generates the mapping. The descriptor's `__set_name__` method configures each field with its attribute name, and the metaclass's `__new__` method iterates over the class namespace to collect all fields and build the schema.

The descriptor handles the data layer: type conversion (e.g., converting strings to `int`), validation (e.g., checking that a value is within a valid range), and storage (e.g., storing the value in a slot or `__dict__`). The `__get__` method returns the stored value (or a transformed version), and the `__set__` method validates and stores the value. For database fields, the descriptor might also handle lazy loading (fetching the value from the database on first access) and dirty tracking (recording whether the value has been modified).

The metaclass handles the schema layer: collecting all fields from the class namespace, generating the table schema (column names, types, constraints), registering the model in a global registry, and injecting manager methods (like `objects`). The metaclass's `__prepare__` can return a custom namespace that tracks field definitions, and `__new__` processes the collected fields before the class is finalized. This separation of concerns (descriptor for data, metaclass for schema) is the foundation of Django's ORM and SQLAlchemy's declarative system.

```python
class Column:
    def __init__(self, col_type, primary_key=False):
        self.col_type = col_type
        self.primary_key = primary_key
    def __set_name__(self, owner, name):
        self.name = name
        self.storage = f'_col_{name}'
        owner._columns[name] = self
    def __get__(self, obj, objtype=None):
        if obj is None: return self
        return getattr(obj, self.storage, None)
    def __set__(self, obj, value):
        if self.primary_key and value is None:
            raise ValueError(f"{self.name} is a primary key")
        setattr(obj, self.storage, value)

class ModelMeta(type):
    def __new__(mcs, name, bases, namespace):
        columns = {}
        cls = super().__new__(mcs, name, bases, namespace)
        cls._columns = columns
        cls._table = name.lower()
        return cls

class Model(metaclass=ModelMeta):
    pass

class User(Model):
    id = Column('INTEGER', primary_key=True)
    name = Column('VARCHAR(50)')
    age = Column('INTEGER')

print(User._table)           # 'user'
print(list(User._columns))  # ['id', 'name', 'age']
```

## Q76: What is the `__init_subclass__` hook and how does it simplify metaclass-like patterns?

**A:** `__init_subclass__` (PEP 487, Python 3.6+) is a hook that a parent class can define to run code whenever a subclass is defined. When you write `class Child(Parent): ...`, Python calls `Parent.__init_subclass__()` after the child class is fully created. This replaces many metaclass use cases with simpler, more composable code. The hook receives keyword arguments from the child class's class statement, enabling parameterized subclass customization.

The key advantage over metaclasses is composability. Multiple `__init_subclass__` hooks from different base classes chain naturally through the MRO — each parent's hook runs in order without conflict. Metaclasses, by contrast, can conflict when multiple bases use different metaclasses. This makes `__init_subclass__` the preferred choice for subclass hooks, registries, and mixin application. It runs after the class is fully formed, so you can inspect its attributes, methods, and annotations, but you cannot modify its namespace or bases.

Common use cases include: auto-registering subclasses in a registry, validating that subclasses implement required methods, injecting mixin methods, setting class-level defaults, and building plugin systems. The keyword arguments feature allows you to pass configuration: `class MyPlugin(Base, name='auth', priority=1)`. The `name` and `priority` are forwarded to `__init_subclass__` as keyword arguments, where they can be used for registration or configuration.

```python
class Plugin:
    _registry = {}
    def __init_subclass__(cls, plugin_name=None, priority=0, **kwargs):
        super().__init_subclass__(**kwargs)
        name = plugin_name or cls.__name__
        Plugin._registry[name] = {'class': cls, 'priority': priority}

class Auth(Plugin, plugin_name='auth', priority=1):
    pass

class Cache(Plugin, plugin_name='cache', priority=2):
    pass

print(sorted(Plugin._registry, key=lambda k: Plugin._registry[k]['priority']))
# ['auth', 'cache']
```

## Q77: How do you use `__set_name__` to create self-aware descriptors?

**A:** `__set_name__` (PEP 487, Python 3.6+) is a protocol that Python automatically calls on descriptors when the class they belong to is created. The method receives the owning class and the attribute name, allowing the descriptor to learn its identity without being told explicitly. Before `__set_name__`, descriptors had to be constructed with their name (e.g., `field = MyDescriptor('field')`), which was redundant and error-prone. `__set_name__` eliminates this by having Python provide the name automatically.

Self-aware descriptors use `__set_name__` to configure their storage name, logging prefix, validation rules, or any other context-dependent behavior. The typical pattern is to store the attribute name and derive a private storage name (e.g., `_field_name`) for use in `__get__` and `__set__`. This ensures that multiple descriptors on the same class do not collide, and that descriptors on different classes with the same name work independently.

A subtle point is that `__set_name__` is called during class creation, before `__init_subclass__`. This means the descriptor is fully configured before any subclass hooks run, which is important for frameworks that rely on both protocols. The method is called once per descriptor instance per class, so if a descriptor is inherited by multiple subclasses, `__set_name__` is called for each subclass. This allows the descriptor to adapt its behavior based on the owning class, which is useful for class-specific validation rules or storage strategies.

```python
class SelfAware:
    def __set_name__(self, owner, name):
        self.name = name
        self.owner = owner
        self.storage = f'_aware_{name}_{owner.__name__}'

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.storage, 'unset')

    def __set__(self, obj, value):
        print(f"Setting {self.owner.__name__}.{self.name} = {value}")
        setattr(obj, self.storage, value)

class Config:
    host = SelfAware()
    port = SelfAware()

c = Config()
c.host = "localhost"   # Setting Config.host = localhost
c.port = 8080          # Setting Config.port = 8080
```

## Q78: What is the relationship between descriptors and Python's `property` chain?

**A:** `property` is a data descriptor that supports chaining via the `.getter()`, `.setter()`, and `.deleter()` methods. Each of these methods returns a new `property` object that combines the previous property's behavior with the new function. When you write `@prop.setter`, you are calling `prop.setter(func)`, which returns a new `property` with the setter attached. This is a functional composition pattern — each call creates a new object, and the last one is stored in the class dictionary.

The descriptor protocol is what makes this chaining work. The `property` class implements `__get__`, `__set__`, and `__delete__`, delegating to the user-provided functions. The `.setter()` method creates a new `property` instance with the new setter function while preserving the existing getter and deleter. This new instance replaces the original in the class dictionary. The result is a clean, declarative syntax for defining attribute access control.

Understanding this chain is important because it reveals that `property` is not a special language feature — it is a descriptor class that uses the same protocol as any custom descriptor. You can create similar chaining behavior in your own descriptors by implementing a `with_getter()` or `with_validator()` method that returns a new descriptor instance. This is the pattern used by libraries like `attrs` and `pydantic` for field configuration.

```python
class ChainedDescriptor:
    def __init__(self, fget=None, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, objtype=None):
        if obj is None: return self
        return self.fget(obj) if self.fget else None

    def __set__(self, obj, value):
        if self.fset:
            self.fset(obj, value)
        else:
            raise AttributeError("can't set attribute")

    def getter(self, func):
        return type(self)(fget=func, fset=self.fset)

    def setter(self, func):
        return type(self)(fget=self.fget, fset=func)

class Config:
    @ChainedDescriptor()
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self._host = value.lower()

c = Config()
c.host = "LOCALHOST"
print(c.host)  # "localhost"
```

## Q79: How do descriptors handle thread safety in concurrent applications?

**A:** Descriptors are not inherently thread-safe. If multiple threads access or modify a descriptor-backed attribute simultaneously, race conditions can occur. For example, a descriptor's `__get__` might compute a value while another thread's `__set__` is modifying the underlying storage. The solution is to add synchronization primitives (locks, semaphores) to the descriptor's `__get__` and `__set__` methods, or to use atomic operations from the `threading` module.

The typical pattern is to use a `threading.Lock` in the descriptor to protect critical sections. However, this adds overhead to every attribute access, which can be significant for frequently accessed attributes. A more efficient approach is to use `threading.local()` for per-thread storage, or to use atomic operations from the `dis` module for simple value types. For cached properties, double-checked locking (checking the cache before acquiring the lock, then checking again after acquiring) can reduce lock contention.

The choice of synchronization strategy depends on the use case. For read-heavy workloads with rare writes, a reader-writer lock allows concurrent reads while serializing writes. For frequently updated values, atomic operations (like `threading.Event` or `queue.Queue`) may be more appropriate. The key principle is to minimize the critical section — only synchronize the actual storage access, not the computation. This ensures that descriptor overhead remains low even under concurrent access.

```python
import threading

class ThreadSafeCached:
    def __init__(self, func):
        self.func = func
        self.lock = threading.Lock()
        self.cache = {}

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if id(obj) not in self.cache:
            with self.lock:
                if id(obj) not in self.cache:
                    self.cache[id(obj)] = self.func(obj)
        return self.cache[id(obj)]

class ExpensiveData:
    @ThreadSafeCached
    def compute(self):
        import time
        time.sleep(1)
        return 42

d = ExpensiveData()
# Multiple threads calling d.compute() will only compute once
```

## Q80: What is the `__slots__` + `__init_subclass__` combination for framework development?

**A:** Combining `__slots__` with `__init_subclass__` creates a pattern where base classes define slot-based attributes and subclasses are automatically registered or validated. The `__init_subclass__` hook runs after the subclass is created, so it can inspect the subclass's `__slots__` to understand its attribute layout. This is useful for frameworks that need to know the exact memory layout of objects, such as serialization libraries, database connectors, or game engines.

The pattern works by defining a base class with `__slots__` and `__init_subclass__`. When a subclass is defined, `__init_subclass__` checks that the subclass's slots do not conflict with the parent's, registers the subclass in a type registry, and optionally validates that required slots are present. This provides the memory efficiency of `__slots__` with the automatic registration of `__init_subclass__`.

A common use case is a data frame or record system where each row is a slotted object. The base class defines common slots (like `id` and `timestamp`), and subclasses define domain-specific slots. `__init_subclass__` validates the slot layout and registers the class for deserialization. When reading data from a file, the framework looks up the class by name and creates instances with the correct slot layout. This approach is significantly faster and more memory-efficient than using `__dict__`.

```python
class Record:
    __slots__ = ('__weakref__',)
    _registry = {}

    def __init_subclass__(cls, record_type=None, **kwargs):
        super().__init_subclass__(**kwargs)
        name = record_type or cls.__name__
        Record._registry[name] = cls

class UserRecord(Record, record_type='user'):
    __slots__ = ('name', 'email')

class OrderRecord(Record, record_type='order'):
    __slots__ = ('order_id', 'amount')

u = UserRecord()
u.name = "Alice"
u.email = "alice@example.com"
print(Record._registry.keys())  # dict_keys(['user', 'order'])
```

## Q81: How do you implement a descriptor-based caching strategy with invalidation?

**A:** A caching descriptor with invalidation stores computed values and provides mechanisms to invalidate (clear) the cache when dependencies change. The descriptor's `__get__` checks whether the cached value is still valid before returning it. Invalidation can be time-based (the cache expires after a TTL), dependency-based (the cache is invalidated when another attribute changes), or manual (an explicit `invalidate()` call clears the cache).

The time-based approach uses a timestamp to track when the value was computed. On each access, `__get__` checks whether the current time exceeds the TTL. If so, the value is recomputed. The dependency-based approach uses a reference to another attribute and invalidates the cache when that attribute changes (via the descriptor's `__set__` or a separate observer). The manual approach provides an `invalidate()` method that clears the cached value from `instance.__dict__`.

A key design decision is where to store the cache. Storing in `instance.__dict__` is simple and works with `pickle`, but requires the descriptor to be a non-data descriptor. Storing in the descriptor itself (per-instance) requires a dictionary keyed by instance identity, which can leak memory if instances are not properly cleaned up. The recommended approach is to use `instance.__dict__` for the cache and implement `__delete__` to clear it. This integrates naturally with Python's garbage collection and serialization.

```python
import time

class TTLCache:
    def __init__(self, ttl=60):
        self.ttl = ttl

    def __set_name__(self, owner, name):
        self.name = name
        self.val_key = f'_cache_val_{name}'
        self.time_key = f'_cache_time_{name}'

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        now = time.time()
        cached_time = getattr(obj, self.time_key, 0)
        if now - cached_time > self.ttl:
            val = self.func(obj)
            setattr(obj, self.val_key, val)
            setattr(obj, self.time_key, now)
            return val
        return getattr(obj, self.val_key)

    def __set__(self, obj, value):
        setattr(obj, self.val_key, value)
        setattr(obj, self.time_key, time.time())

    def __delete__(self, obj):
        obj.__dict__.pop(self.val_key, None)
        obj.__dict__.pop(self.time_key, None)

    def func(self, obj):
        return sum(range(10000))

class Data:
    @TTLCache(ttl=5)
    def expensive(self):
        return self.func()

d = Data()
print(d.expensive)  # Computed
print(d.expensive)  # From cache
del d.expensive     # Invalidate
print(d.expensive)  # Recomputed
```

## Q82: What is the role of descriptors in Python's `dataclasses.field()` and how does `field()` work?

**A:** `dataclasses.field()` returns a `Field` object that configures how a dataclass field is handled. The `Field` object is a descriptor that stores metadata (default value, default factory, type annotation, repr flag, compare flag, hash flag, init flag, metadata dict, and ordering). When the `@dataclass` decorator processes the class, it inspects the `Field` objects and uses their configuration to generate `__init__`, `__repr__`, `__eq__`, `__hash__`, and other methods.

The `Field` class implements the descriptor protocol to provide default value access. When a field has a default, `Field.__get__` returns that default when accessed from the class. For mutable defaults, `field(default_factory=list)` ensures that each instance gets a fresh copy. The descriptor mechanism ensures that default values are properly handled whether accessed from the class or from an instance. The `Field` object also stores the field's `metadata` dict, which can be used by third-party libraries to add custom behavior.

The `field()` function accepts parameters like `default`, `default_factory`, `repr`, `compare`, `hash`, `init`, `metadata`, and `kw_only`. These parameters configure the generated methods. For example, `field(compare=False)` excludes the field from `__eq__` and `__lt__` comparisons. `field(metadata={'primary_key': True})` stores custom metadata that third-party libraries can read. The `Field` object is stored in `cls.__dataclass_fields__`, which is a dictionary of field name to `Field` objects.

```python
from dataclasses import dataclass, field, fields

@dataclass
class User:
    name: str = field(compare=True, repr=True)
    password: str = field(compare=False, repr=False)
    tags: list = field(default_factory=list, metadata={'max_len': 10})

u = User("Alice", "secret")
print(repr(u))  # User(name='Alice', password='***') — password hidden
print(User.__dataclass_fields__['tags'].metadata)  # {'max_len': 10}
```

## Q83: How do you implement a descriptor-based lazy loading pattern for ORM relationships?

**A:** Lazy loading descriptors defer loading a related object until it is first accessed. The descriptor's `__get__` method checks whether the related object has been loaded (typically by checking for a sentinel value in `instance.__dict__`). If not loaded, it queries the database, stores the result, and returns it. On subsequent accesses, the cached value is returned directly. This is the core mechanism behind Django's `ForeignKey` and SQLAlchemy's `relationship()`.

The descriptor stores the foreign key value (e.g., `user_id`) and uses it to query the related table when `__get__` is called. The key challenge is avoiding infinite recursion: if the related object also has a lazy-loading descriptor that references back to the original object, the loading process can loop. ORMs handle this by using a "value From" pattern (storing the foreign key value, not the object) and by maintaining an identity map that returns the same object for the same primary key.

A practical implementation uses `__set_name__` to learn the relationship name and `__get__` to trigger loading. The descriptor also needs to handle the case where the foreign key is `None` (nullable relationship) and the case where the related object has been deleted. The `__set__` method can be used to set the foreign key value (not the related object) when the relationship is reassigned. This keeps the descriptor focused on loading and lets the ORM handle the relationship semantics.

```python
class LazyRelation:
    def __init__(self, model, foreign_key):
        self.model = model
        self.foreign_key = foreign_key

    def __set_name__(self, owner, name):
        self.name = name
        self.storage = f'_lazy_{name}'

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.storage not in obj.__dict__:
            fk_value = getattr(obj, self.foreign_key)
            if fk_value is None:
                obj.__dict__[self.storage] = None
            else:
                obj.__dict__[self.storage] = self.model.get(fk_value)
        return obj.__dict__[self.storage]

class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Post:
    author_id = None
    author = LazyRelation(User, 'author_id')

    def __init__(self, id, title, author_id):
        self.id = id
        self.title = title
        self.author_id = author_id

# Simulated database
User.get = classmethod(lambda cls, id: User(id, f"User_{id}"))
p = Post(1, "Hello", 42)
print(p.author.name)  # User_42 — loaded lazily
```

## Q84: What are the performance characteristics of `__slots__` versus `__dict__` for attribute access?

**A:** `__slots__` provides faster attribute access than `__dict__` because slot access uses fixed memory offsets rather than hash table lookups. When you access `instance.attr` on a slotted object, Python computes the memory offset at class creation time and accesses the value directly from the instance's C struct. This is an O(1) operation with minimal overhead — essentially a pointer dereference. In contrast, `__dict__` access requires a hash table lookup, which involves computing the hash, probing the table, and comparing keys — typically 3-5x slower than slot access.

Memory usage is also significantly better with `__slots__`. A typical `__dict__` consumes 100+ bytes per instance (even when empty), while slots consume only the space for the declared attributes (typically 8 bytes per pointer on 64-bit systems). For objects with 2-3 attributes, `__slots__` reduces memory by 40-60%. This scales linearly — for millions of instances, the savings are substantial. The trade-off is that `__slots__` objects cannot have arbitrary attributes added dynamically.

The performance difference is most significant in tight loops that access attributes millions of times. However, in typical application code, the difference is often negligible because Python's overall overhead dominates. The recommendation is to profile before optimizing — use `__slots__` for data-heavy classes where memory or access speed is a bottleneck, and use `__dict__` for classes that need flexibility. Microbenchmarks show slot access is 20-40ns faster than dict access, which matters in inner loops but not in typical application code.

```python
import timeit
import sys

class DictObj:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SlotObj:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y

d = DictObj(1, 2)
s = SlotObj(1, 2)

dict_time = timeit.timeit(lambda: d.x + d.y, number=1_000_000)
slot_time = timeit.timeit(lambda: s.x + s.y, number=1_000_000)

print(f"Dict: {dict_time:.3f}s, Slot: {slot_time:.3f}s")
print(f"Dict size: {sys.getsizeof(d.__dict__)} bytes")
print(f"Slot obj size: {sys.getsizeof(s)} bytes")
```

## Q85: How do descriptors support Python's `__init_subclass__` keyword argument passing?

**A:** When a subclass is defined with keyword arguments (e.g., `class Child(Parent, key=value)`), those keywords are passed to `__init_subclass__` as keyword arguments. Descriptors defined on the subclass have their `__set_name__` called before `__init_subclass__` runs, so by the time `__init_subclass__` inspects the class, all descriptors are fully configured with their names and owning classes.

The pattern is to define `__init_subclass__` with `**kwargs` to capture the keyword arguments, and then use the configured descriptors to process them. For example, a framework might accept `table_name='users'` as a keyword argument, and `__init_subclass__` uses the configured field descriptors to generate the table schema. The descriptors provide the field names and types, while the keyword arguments provide the table-level configuration.

This combination is powerful because it separates field-level configuration (done in the descriptor via `__set_name__`) from class-level configuration (done in `__init_subclass__` via keyword arguments). The descriptors do not need to know about the keyword arguments, and `__init_subclass__` does not need to know about the descriptor internals. This separation of concerns makes the code more modular and easier to maintain.

```python
class Field:
    def __set_name__(self, owner, name):
        self.name = name
        self.owner = owner

class Model:
    def __init_subclass__(cls, table=None, **kwargs):
        super().__init_subclass__(**kwargs)
        fields = {n: v for n, v in vars(cls).items() if isinstance(v, Field)}
        cls._table = table or cls.__name__.lower()
        cls._fields = fields

class User(Model, table='users'):
    name = Field()
    email = Field()

print(User._table)    # 'users'
print(User._fields)   # {'name': <Field>, 'email': <Field>}
```

## Q86: What is the `__class_getitem__` protocol and how does it enable generic programming in Python?

**A:** `__class_getitem__` (PEP 560, Python 3.7+) enables generic programming by allowing classes to accept type parameters through subscription syntax (`MyClass[int]`). When you write `MyClass[int]`, Python calls `MyClass.__class_getitem__(int)` and returns the result. This returned object can be a specialized version of the class, a type alias, or a parameterized type that validates at runtime.

The protocol is part of Python's broader type hinting system. Built-in types like `list`, `dict`, and `tuple` support subscription natively through `__class_getitem__`. For user-defined classes, you implement `__class_getitem__` to accept type parameters and return a configured class. The `typing` module provides `Generic`, `TypeVar`, and other tools that work with `__class_getitem__` to provide static type checking while maintaining runtime flexibility.

A practical implementation returns a new class with the type parameter stored as a class attribute. The descriptor on the new class can use this type parameter to validate values at runtime. For example, `Container[int]` might create a class where the `add` method validates that values are instances of `int`. This provides runtime type safety that complements static type checking.

```python
class GenericList:
    def __class_getitem__(cls, item):
        return type(f'{cls.__name__}[{item.__name__}]', (cls,), {'_item_type': item})

    def __init__(self):
        self._items = []

    def add(self, item):
        if hasattr(type(self), '_item_type'):
            if not isinstance(item, type(self)._item_type):
                raise TypeError(f"Expected {type(self)._item_type.__name__}")
        self._items.append(item)

IntList = GenericList[int]
il = IntList()
il.add(42)      # OK
# il.add("hi")  # TypeError: Expected int
```

## Q87: How do you use descriptors to implement protocol-based structural subtyping?

**A:** Protocol-based structural subtyping (PEP 544) uses `typing.Protocol` to define interfaces based on method signatures rather than inheritance. Descriptors can support this by implementing the protocol's methods as descriptors, allowing the protocol to be satisfied through attribute access rather than explicit method definitions. When a class uses descriptors that implement the protocol's methods, instances of that class automatically satisfy the protocol without explicit registration.

The mechanism works through `isinstance()` and `issubclass()` checks. `typing.Protocol` uses `__instancecheck__` on its metaclass to verify that an object has the required methods and attributes. Descriptors that implement these methods (via `__get__` returning a callable) are recognized by the protocol check. This means a class with a descriptor that provides a `serialize()` method will satisfy a `Serializable` protocol, even if `serialize` is not explicitly defined as a method.

A practical pattern is to create a `@provides` decorator that wraps a descriptor and registers it with a protocol. When the protocol checks `isinstance(obj, Protocol)`, the descriptor's presence satisfies the requirement. This is used in dependency injection frameworks where services are defined by their protocols, not their implementations. The descriptor handles the implementation details (lazy loading, caching, validation) while the protocol defines the interface.

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> str: ...

class DrawDescriptor:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return lambda: f"Drawing {self.name}"

class Shape:
    circle = DrawDescriptor()

s = Shape()
print(isinstance(s, Drawable))  # True — satisfies protocol via descriptor
print(s.circle.draw())          # "Drawing circle"
```

## Q88: How do descriptors interact with Python's `__getattr__` and `__getattribute__`?

**A:** `__getattribute__` is called for every attribute access and follows the standard descriptor lookup chain: data descriptors first, then instance `__dict__`, then non-data descriptors and class attributes. `__getattr__` is only called when `__getattribute__` raises `AttributeError`. Descriptors interact with `__getattribute__` because the standard lookup chain calls descriptor `__get__` methods as part of its process.

If you override `__getattribute__`, you must manually implement the descriptor protocol or call `super().__getattribute__()`. Failing to do so breaks properties, classmethods, static methods, slot attributes, and any other descriptor-based feature. The typical mistake is implementing `__getattribute__` to return a default value for missing attributes, which prevents `__getattr__` from being called and breaks the descriptor protocol.

`__getattr__` does not interact with descriptors because it is only called after the descriptor-based lookup has failed. This makes `__getattr__` safe to use — you can implement fallback logic without worrying about breaking descriptors. However, if you implement both `__getattribute__` and `__getattr__`, you must ensure that `__getattribute__` calls `super().__getattribute__()` for normal attribute access, and raises `AttributeError` for missing attributes so that `__getattr__` can handle them.

```python
class Intercepting:
    def __getattribute__(self, name):
        print(f"Accessing {name}")
        return super().__getattribute__(name)

class MyClass:
    x = 42
    def method(self):
        return "hello"

obj = Intercepting()
print(obj.x)         # Accessing x -> 42
print(obj.method())  # Accessing method -> hello
# Descriptors still work through super().__getattribute__()
```

## Q89: What are the best practices for using `__slots__` in library code?

**A:** Best practices for `__slots__` in libraries include: (1) always include `'__weakref__'` in the base class's `__slots__` if users might need weak references; (2) provide `__getstate__` and `__setstate__` for pickle support; (3) document that instances do not have `__dict__` so users know they cannot add arbitrary attributes; (4) avoid `__slots__` on classes that are part of the public API where users might expect dynamic attribute support; (5) use `__slots__` only for simple data-holder classes, not for classes with complex behavior; and (6) test with `isinstance()` and `hasattr()` to ensure descriptors work correctly.

The API compatibility issue is particularly important. If your library provides a class that users subclass, adding `__slots__` to the base class forces subclasses to also define `__slots__`. This is a breaking change for users who add attributes dynamically. The recommendation is to make `__slots__` opt-in (e.g., through a mixin class) or to document it clearly. Some libraries provide both a slotted and a dict-based version of the same class.

For serialization, always implement `__getstate__` and `__setstate__` when using `__slots__`. The `__getstate__` method should return a dictionary of slot values, and `__setstate__` should restore them. For JSON serialization, implement a `to_dict()` method that returns a dictionary of slot values. For ORM integration, ensure that the slotted class works with the ORM's identity map and session management.

```python
import pickle

class SlottedRecord:
    __slots__ = ('__weakref__', 'id', 'name', 'data')

    def __init__(self, id, name, data=None):
        self.id = id
        self.name = name
        self.data = data

    def __getstate__(self):
        return {s: getattr(self, s) for s in self.__slots__ if s != '__weakref__'}

    def __setstate__(self, state):
        for k, v in state.items():
            setattr(self, k, v)

    def __repr__(self):
        return f"{type(self).__name__}(id={self.id}, name={self.name})"

r = SlottedRecord(1, "test")
data = pickle.dumps(r)
r2 = pickle.loads(data)
print(r2)  # SlottedRecord(id=1, name=test)
```

## Q90: How do you implement a descriptor-based lazy initialization pattern?

**A:** Lazy initialization descriptors defer object creation or computation until the attribute is first accessed. The descriptor's `__get__` method checks whether the value has been initialized (typically by checking for a sentinel in `instance.__dict__`). If not, it performs the initialization, stores the result, and returns it. On subsequent accesses, the cached value is returned directly. This is the pattern behind `functools.cached_property` and lazy loading in ORMs.

The key design decision is whether to use a non-data descriptor (storing the cached value in `instance.__dict__`) or a data descriptor (storing it in the descriptor itself). Non-data descriptors are simpler and work with `pickle`, but can be overridden by setting the attribute on the instance. Data descriptors prevent this but require more complex storage management. For most use cases, non-data descriptors are preferred because the cached value is the correct value and overriding it is rarely needed.

A practical implementation uses `__set_name__` to learn the storage name and `__get__` to trigger initialization. The descriptor can accept a callable that performs the initialization, and optionally a callable that invalidates the cache. The `__delete__` method can be implemented to clear the cached value, allowing re-initialization. This pattern is used in ORMs for lazy loading relationships, in configuration systems for deferred environment variable resolution, and in GUI frameworks for deferred widget creation.

```python
class LazyInit:
    def __init__(self, factory):
        self.factory = factory

    def __set_name__(self, owner, name):
        self.name = name
        self.storage = f'_lazy_{name}'

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.storage not in obj.__dict__:
            obj.__dict__[self.storage] = self.factory(obj)
        return obj.__dict__[self.storage]

    def __delete__(self, obj):
        obj.__dict__.pop(self.storage, None)

class AppConfig:
    db = LazyInit(lambda self: DatabaseConnection())
    cache = LazyInit(lambda self: CacheClient())

class DatabaseConnection:
    def __repr__(self): return "DB Connected"

class CacheClient:
    def __repr__(self): return "Cache Connected"

config = AppConfig()
print(config.db)    # DB Connected — initialized on first access
print(config.db)    # DB Connected — from cache
del config.db       # Invalidate
print(config.db)    # DB Connected — re-initialized
```

## Q91: What is the role of descriptors in Python's `__init_subclass__` method resolution?

**A:** Descriptors participate in method resolution when `__init_subclass__` is defined on a class. When a subclass is created, `__init_subclass__` is called as a regular method on the parent class. If `__init_subclass__` is defined as a descriptor (e.g., a `classmethod` or a custom descriptor), the descriptor protocol determines how it is bound and called. The `classmethod` descriptor ensures that `__init_subclass__` receives the parent class as its first argument, not the subclass.

The practical consequence is that `__init_subclass__` can be customized through descriptors. You can create a `@validated_init_subclass` descriptor that wraps `__init_subclass__` with validation logic, or a `@cached_init_subclass` descriptor that memoizes the hook's results. This is an advanced pattern that allows you to modify subclass creation behavior without using metaclasses.

However, in most cases, `__init_subclass__` is defined as a regular method or a `classmethod`, not a custom descriptor. The descriptor protocol for `classmethod` is well-defined and ensures that the parent class is passed as the first argument. The key point is that descriptors do not change the semantics of `__init_subclass__` — they only change how the method is bound and called. The hook still runs after the subclass is fully created, and it still receives the same arguments.

```python
class ValidatedHook:
    def __set_name__(self, owner, name):
        self.name = name
        self.original = getattr(owner, name)

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        def wrapper(cls, **kwargs):
            print(f"Validating subclass of {obj.__name__}")
            return self.original(cls, **kwargs)
        return wrapper

class Base:
    @ValidatedHook()
    def __init_subclass__(cls, required_field=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if required_field:
            setattr(cls, required_field, None)

class Child(Base, required_field='status'):
    pass

print(Child.status)  # None — set by __init_subclass__
```

## Q92: How do you handle descriptor conflicts when multiple descriptors are defined on the same class?

**A:** Descriptor conflicts occur when multiple descriptors on the same class try to manage the same underlying storage or have conflicting behavior. The typical manifestation is that one descriptor's `__set__` overwrites another descriptor's cached value, or that two descriptors use the same storage name. The solution is to use `__set_name__` to generate unique storage names for each descriptor instance, ensuring that descriptors do not collide.

The `__set_name__` protocol provides the attribute name to each descriptor, which can be used to derive a unique storage key. For example, a descriptor named `x` might use `_x_ClassName` as its storage key. This ensures that even if two descriptors are defined on the same class, they use different storage locations. The `dataclasses` module uses this pattern for its `Field` objects, and it is the standard approach for all descriptor-based frameworks.

Another source of conflicts is when a descriptor and a plain attribute share the same name. In this case, the descriptor (if it is a data descriptor) takes precedence, and the plain attribute is effectively hidden. If the descriptor is a non-data descriptor, the plain attribute (in `__dict__`) takes precedence, which can be surprising. The recommendation is to avoid mixing descriptors and plain attributes with the same name, and to use `__set_name__` to generate unique storage names for all descriptors.

```python
class UniqueStorage:
    def __set_name__(self, owner, name):
        self.name = name
        self.storage = f'_{name}_{id(self)}'

    def __get__(self, obj, objtype=None):
        if obj is None: return self
        return getattr(obj, self.storage, 'default')

    def __set__(self, obj, value):
        setattr(obj, self.storage, value)

class MyClass:
    x = UniqueStorage()
    y = UniqueStorage()

obj = MyClass()
obj.x = 10
obj.y = 20
print(obj.x, obj.y)  # 10 20 — no conflict
```

## Q93: What is the `__init_subclass__` + descriptor pattern for building configuration systems?

**A:** The combination of `__init_subclass__` and descriptors creates a powerful pattern for configuration systems. Descriptors define individual configuration fields with type validation, default values, and environment variable mapping. `__init_subclass__` collects all fields from the subclass, validates the configuration schema, and registers the configuration class in a global registry. This provides a declarative way to define configuration schemas with automatic validation and environment variable loading.

The descriptors handle the data layer: reading values from environment variables, converting types, applying defaults, and validating constraints. The `__set_name__` method configures each descriptor with its environment variable name (e.g., `DATABASE_URL` for a `database_url` field). The `__get__` method reads from the environment (or a cache), and `__set__` validates and stores the value. This separation allows configuration fields to be defined declaratively while the framework handles the loading logic.

`__init_subclass__` handles the schema layer: collecting all fields, validating that required fields are present, checking for circular dependencies, and registering the configuration class. It can also generate documentation, provide schema validation for external tools, and create factory methods for different environments (development, testing, production). This pattern is used by libraries like `pydantic-settings` and `dynaconf`.

```python
import os

class EnvField:
    def __init__(self, env_var, default=None, required=False):
        self.env_var = env_var
        self.default = default
        self.required = required

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None: return self
        return os.environ.get(self.env_var, self.default)

class Config:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        fields = {n: v for n, v in vars(cls).items() if isinstance(v, EnvField)}
        cls._fields = fields
        for name, field in fields.items():
            if field.required and field.env_var not in os.environ:
                raise ValueError(f"Missing required env: {field.env_var}")

class AppConfig(Config):
    db_url = EnvField('DATABASE_URL', required=True)
    debug = EnvField('DEBUG', default='false')

os.environ['DATABASE_URL'] = 'postgres://localhost/mydb'
config = AppConfig()
print(config.db_url)  # postgres://localhost/mydb
print(config.debug)    # 'false'
```

## Q94: How do descriptors support Python's `__init_subclass__` for type-safe subclass creation?

**A:** Descriptors support type-safe subclass creation by providing runtime validation of subclass attributes. When `__init_subclass__` runs, it can inspect the subclass's attributes and verify that they satisfy the constraints defined by the descriptors. For example, a descriptor that requires a `str` value can validate that a subclass attribute is actually a string, raising `TypeError` if not. This provides compile-time-like safety for class definitions.

The pattern is to define descriptors that implement `__set_name__` and store validation rules. When a subclass is created, `__init_subclass__` iterates over the descriptor instances and validates that their stored values satisfy the rules. This is different from instance-level validation (which happens in `__set__`) because it validates class-level attributes. For example, a field descriptor might validate that a class attribute `table_name` is a valid SQL identifier, or that `max_length` is a positive integer.

The key advantage is that validation happens at class definition time, not at instantiation time. This means errors are caught early, when the class is defined, rather than later when an instance is created. This is particularly valuable for framework code where classes are defined by users and errors should be caught as early as possible. The descriptor protocol ensures that `__set_name__` is called before `__init_subclass__`, so the validation logic has access to all descriptor metadata.

```python
class ValidatedField:
    def __init__(self, validator):
        self.validator = validator

    def __set_name__(self, owner, name):
        self.name = name
        if hasattr(owner, '_validated_fields'):
            owner._validated_fields[name] = self

class Schema:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._validated_fields = {}
        for name, val in vars(cls).items():
            if isinstance(val, ValidatedField):
                cls._validated_fields[name] = val

    def validate_instance(self):
        for name, field in type(self)._validated_fields.items():
            value = getattr(self, name, None)
            if not field.validator(value):
                raise ValueError(f"Invalid value for {name}: {value}")

class User(Schema):
    name = ValidatedField(lambda v: isinstance(v, str) and len(v) > 0)
    age = ValidatedField(lambda v: isinstance(v, int) and 0 <= v <= 150)

u = User()
u.name = "Alice"
u.age = 30
u.validate_instance()  # OK
```

## Q95: What is the relationship between descriptors and Python's `__init_subclass__` for mixin application?

**A:** Descriptors and `__init_subclass__` together enable automatic mixin application. Descriptors define the behavior that mixins provide (e.g., logging, validation, caching), and `__init_subclass__` detects which descriptors are present on a subclass and automatically injects the corresponding mixin behavior. This eliminates the need for users to explicitly inherit from mixin classes — simply using a descriptor triggers the mixin.

The pattern works by defining a base class whose `__init_subclass__` inspects the subclass's namespace for specific descriptors. When a descriptor is found, the hook adds the corresponding mixin methods to the subclass. For example, a `@loggable` descriptor might trigger `__init_subclass__` to add `log_create()`, `log_update()`, and `log_delete()` methods to the subclass. This provides a declarative way to add cross-cutting concerns.

The advantage over traditional mixins is that the mixin behavior is triggered by the presence of a descriptor, not by inheritance. This means the same descriptor can be used on classes with different base classes, without requiring a common mixin base. The descriptor handles the configuration (e.g., log level, output format), and `__init_subclass__` handles the method injection. This separation makes the system more composable and easier to maintain.

```python
class Loggable:
    def __set_name__(self, owner, name):
        self.name = name

class AutoLog:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        has_log = any(isinstance(v, Loggable) for v in vars(cls).values())
        if has_log:
            def log_action(self, action):
                print(f"[{type(self).__name__}] {action}")
            cls.log_action = log_action

class User(AutoLog):
    name = Loggable()

u = User()
u.log_action("created")  # [User] created
```

## Q96: How do you implement a descriptor-based lazy property with thread-safe invalidation?

**A:** A thread-safe lazy property with invalidation combines lazy initialization with synchronization primitives. The descriptor's `__get__` uses a `threading.Lock` to ensure that only one thread computes the value at a time. The `__delete__` method uses the same lock to safely invalidate the cache. This prevents race conditions where multiple threads try to compute the value simultaneously or where one thread invalidates while another is reading.

The implementation typically uses double-checked locking: check the cache without the lock, then acquire the lock and check again. This reduces lock contention for the common case (cache hit) while ensuring correctness for the rare case (cache miss). The lock protects only the critical section (checking and setting the cache), not the computation itself, which minimizes overhead.

For invalidation, the `__delete__` method acquires the lock, clears the cached value from `instance.__dict__`, and releases the lock. Subsequent accesses will recompute the value. The invalidation can be triggered by an explicit `del obj.prop` call, by another attribute's `__set__` method, or by a timer. The key is that the lock ensures that invalidation is atomic — either the cache is cleared or it is not, with no intermediate state visible to other threads.

```python
import threading

class ThreadSafeLazy:
    def __init__(self, func):
        self.func = func
        self.lock = threading.Lock()

    def __set_name__(self, owner, name):
        self.name = name
        self.val_key = f'_lazy_val_{name}'
        self.init_key = f'_lazy_init_{name}'

    def __get__(self, obj, objtype=None):
        if obj is None: return self
        if getattr(obj, self.init_key, False):
            return getattr(obj, self.val_key)
        with self.lock:
            if getattr(obj, self.init_key, False):
                return getattr(obj, self.val_key)
            val = self.func(obj)
            setattr(obj, self.val_key, val)
            setattr(obj, self.init_key, True)
            return val

    def __delete__(self, obj):
        with self.lock:
            obj.__dict__.pop(self.val_key, None)
            obj.__dict__.pop(self.init_key, None)

class ExpensiveResource:
    @ThreadSafeLazy
    def connection(self):
        import time
        time.sleep(1)
        return "Connection established"

r = ExpensiveResource()
print(r.connection)  # Computed once, thread-safe
del r.connection     # Safe invalidation
```

## Q97: What are the performance implications of using `__slots__` with multiple inheritance?

**A:** `__slots__` with multiple inheritance requires careful design to avoid slot conflicts. When a class inherits from multiple parents that define `__slots__`, the child class must also define `__slots__` to resolve the conflict. Each parent's slots are stored in separate C structs, and the child's slots are appended to the combined struct. The MRO determines the order in which slot descriptors are checked, but the memory layout is determined by the class hierarchy.

The performance impact is minimal for well-designed hierarchies. Slot access remains O(1) regardless of the number of base classes, because each slot's offset is computed at class creation time. However, the memory layout can become fragmented if parents define many slots, leading to poorer cache locality. The recommendation is to keep slot hierarchies shallow (2-3 levels) and avoid diamond inheritance with slots.

The practical constraint is that you cannot have two slots with the same name in a multiple inheritance hierarchy. If `BaseA` has `__slots__ = ('x',)` and `BaseB` has `__slots__ = ('x',)`, the child class cannot define `__slots__ = ('x',)` because it would shadow both parents' slots. The solution is to use different names or to restructure the hierarchy to avoid the conflict. This is one of the main reasons `__slots__` is not recommended for complex class hierarchies.

```python
class BaseA:
    __slots__ = ('x',)

class BaseB:
    __slots__ = ('y',)

class Child(BaseA, BaseB):
    __slots__ = ('z',)

c = Child()
c.x = 1  # From BaseA's slots
c.y = 2  # From BaseB's slots
c.z = 3  # From Child's slots
print(sys.getsizeof(c))  # Larger than single-inheritance due to multiple structs
```

## Q98: How do descriptors enable Python's `__init_subclass__` for automatic method generation?

**A:** Descriptors enable automatic method generation by providing the metadata that `__init_subclass__` needs to generate methods. When a descriptor is defined on a class, `__set_name__` configures it with the attribute name and owning class. `__init_subclass__` then inspects these descriptors and generates methods based on their configuration. This is the pattern behind Django's `Model` methods (like `get_absolute_url()`) and SQLAlchemy's hybrid methods.

The typical implementation defines descriptors that store configuration (e.g., field type, validation rules, database mapping) and `__init_subclass__` that reads this configuration and generates methods. For example, a descriptor named `email` with a `unique=True` parameter might trigger `__init_subclass__` to generate a `find_by_email()` class method. The generated methods are added to the subclass's namespace before the class is finalized.

This pattern is more powerful than metaclass-based method generation because it is composable. Multiple descriptors can each trigger different method generation, and the methods can be customized through keyword arguments. The `__init_subclass__` hook runs after all descriptors are configured, so it has access to the complete schema. This makes it easy to build complex frameworks that generate methods based on declarative configuration.

```python
class QueryField:
    def __init__(self, field_type, unique=False):
        self.field_type = field_type
        self.unique = unique

    def __set_name__(self, owner, name):
        self.name = name

class AutoQuery:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for name, val in vars(cls).items():
            if isinstance(val, QueryField):
                if val.unique:
                    method_name = f'find_by_{name}'
                    def make_find(fn):
                        def find(cls, value):
                            return f"SELECT * WHERE {fn} = {value}"
                        return classmethod(find)
                    setattr(cls, method_name, make_find(name))

class User(AutoQuery):
    email = QueryField(str, unique=True)
    name = QueryField(str)

print(User.find_by_email("test"))  # SELECT * WHERE email = test
```

## Q99: What is the `__init_subclass__` + descriptor pattern for building validation frameworks?

**A:** The combination of `__init_subclass__` and descriptors creates a powerful validation framework where fields define validation rules and `__init_subclass__` builds the validation schema. Descriptors handle per-field validation (type checking, range validation, format validation) while `__init_subclass__` handles cross-field validation (uniqueness constraints, conditional validation, required field groups). This separation provides both field-level and class-level validation.

The descriptors use `__set_name__` to configure themselves and `__set__` to validate on assignment. `__init_subclass__` collects all descriptors, builds a validation schema, and injects a `validate()` method that checks all fields at once. This allows both incremental validation (per-assignment) and batch validation (full object validation). The validation schema can be serialized to JSON Schema, OpenAPI, or other formats for documentation and external validation.

A key advantage is that validation rules are defined declaratively as class attributes, making them easy to read and maintain. The framework handles the complexity of validation logic, error reporting, and schema generation. This pattern is used by libraries like `pydantic`, `marshmallow`, and `cerberus`, though they typically use metaclasses or class decorators rather than `__init_subclass__`.

```python
class Validated:
    def __init__(self, validator, message):
        self.validator = validator
        self.message = message

    def __set_name__(self, owner, name):
        self.name = name

class Schema:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        fields = {n: v for n, v in vars(cls).items() if isinstance(v, Validated)}
        cls._validation_fields = fields

        def validate_all(self):
            errors = {}
            for name, field in fields.items():
                value = getattr(self, name, None)
                if not field.validator(value):
                    errors[name] = field.message
            if errors:
                raise ValueError(str(errors))
        cls.validate = validate_all

class User(Schema):
    name = Validated(lambda v: isinstance(v, str) and len(v) > 0, "Name required")
    age = Validated(lambda v: isinstance(v, int) and 0 <= v <= 150, "Invalid age")

u = User()
u.name = "Alice"
u.age = 30
u.validate()  # OK
```

## Q100: How do you combine metaclasses, descriptors, and `__slots__` for a complete object model?

**A:** Combining metaclasses, descriptors, and `__slots__` creates a complete object model where the metaclass controls class creation, descriptors handle attribute behavior, and `__slots__` provides memory-efficient storage. The metaclass's `__new__` method processes the class namespace, identifies descriptors, generates `__slots__` from field definitions, and configures the class's memory layout. Descriptors handle validation, type conversion, and lazy loading. `__slots__` ensures that instances have a fixed, minimal memory footprint.

The integration works as follows: descriptors define fields with `__set_name__` to learn their names. The metaclass's `__new__` collects all field descriptors, generates `__slots__` from their names, adds `'__weakref__'` and `'__dict__'` if needed, and creates the class with the optimized slot layout. The descriptors' `__get__` and `__set__` methods use the slot storage for fast access, while `__init_subclass__` handles post-creation tasks like schema generation and method injection.

This pattern is the foundation of high-performance data frameworks. Django's ORM uses a combination of metaclasses (ModelBase), descriptors (Field), and generated `__slots__` (in some configurations) to provide a declarative model definition with efficient storage. SQLAlchemy's declarative system uses similar patterns. The key insight is that each technology handles a different concern: metaclasses for class creation, descriptors for attribute behavior, and `__slots__` for memory layout. Together, they provide a complete, efficient, and flexible object model.

```python
class Field:
    def __init__(self, field_type):
        self.field_type = field_type
    def __set_name__(self, owner, name):
        self.name = name
    def __get__(self, obj, objtype=None):
        if obj is None: return self
        return getattr(obj, f'_slot_{self.name}', None)
    def __set__(self, obj, value):
        if not isinstance(value, self.field_type):
            raise TypeError(f"Expected {self.field_type.__name__}")
        setattr(obj, f'_slot_{self.name}', value)

class ModelMeta(type):
    def __new__(mcs, name, bases, namespace, **kwargs):
        slots = []
        for key, val in list(namespace.items()):
            if isinstance(val, Field):
                slots.append(f'_slot_{key}')
        slots.append('__weakref__')
        namespace['__slots__'] = tuple(slots)
        return super().__new__(mcs, name, bases, namespace)

class Model(metaclass=ModelMeta):
    pass

class User(Model):
    name = Field(str)
    age = Field(int)

u = User()
u.name = "Alice"
u.age = 30
print(u.name, u.age)  # Alice 30
print(hasattr(u, '__dict__'))  # False — slots are used
```
