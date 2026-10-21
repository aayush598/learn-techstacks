# OOPS (Object-Oriented Programming) — 100 Interview Q&A

---

## Q1: What is OOPS?
**A:** Object-Oriented Programming System is a paradigm based on objects that contain data and methods.

**Code:**
```python
class Animal:
    def __init__(self, name):        # object holds data...
        self.name = name
    def speak(self):                 # ...and behavior/methods
        return f"{self.name} makes a sound"

a = Animal("dog")                    # create an object
print(a.speak())                     # dog makes a sound
```

## Q2: What are the main pillars of OOPS?
**A:** Encapsulation, Abstraction, Inheritance, Polymorphism.

**Code:**
```python
# Each pillar is shown with its own example below:
#  - Encapsulation   -> Q5
#  - Abstraction     -> Q6
#  - Inheritance     -> Q8
#  - Polymorphism    -> Q10
```

## Q3: What is a class?
**A:** A class is a blueprint or template defining properties (attributes) and behaviors (methods).

**Code:**
```python
class Car:                       # Car is a blueprint
    def __init__(self, model):
        self.model = model       # attribute / property
    def drive(self):             # behavior / method
        return f"Driving {self.model}"
```

## Q4: What is an object?
**A:** An object is an instance of a class with its own state and behavior.

**Code:**
```python
class Car:
    def __init__(self, model):
        self.model = model
    def drive(self):
        return f"Driving {self.model}"

car1 = Car("Tesla Model 3")      # car1 is an object (instance)
car2 = Car("Toyota Camry")       # another object, own state
print(car1.drive())              # Driving Tesla Model 3
print(car2.drive())              # Driving Toyota Camry
```

## Q5: What is encapsulation?
**A:** Binding data and methods together and restricting direct access via access modifiers.

**Code:**
```python
class BankAccount:
    def __init__(self, balance=0):
        self.__balance = balance      # private (name-mangled) -> restrict access

    def deposit(self, amt):           # controlled way to modify state
        self.__balance += amt

    def get_balance(self):            # controlled way to read state
        return self.__balance

acc = BankAccount(100)
acc.deposit(50)
print(acc.get_balance())              # 150
# acc.__balance  -> AttributeError: direct access is restricted
```

## Q6: What is abstraction?
**A:** Hiding complex implementation details and exposing only essential features.

**Code:**
```python
from abc import ABC, abstractmethod

class Payment(ABC):                       # expose only pay() to the caller
    @abstractmethod
    def pay(self, amount): ...

class Card(Payment):                      # implementation is hidden inside
    def pay(self, amount):
        return f"Card charged {amount}"

print(Card().pay(10))                     # Card charged 10
```

## Q7: Difference between abstraction and encapsulation.
**A:** Abstraction hides complexity (what); encapsulation hides data (how to protect).

**Code:**
```python
from abc import ABC, abstractmethod

class Shape(ABC):                       # abstraction: only area() is visible
    @abstractmethod
    def area(self): ...

class Box(Shape):
    def __init__(self, side):
        self.__side = side              # encapsulation: data is guarded

    def area(self):
        return self.__side ** 2

print(Box(4).area())                    # 16 (how it computes is hidden)
```

## Q8: What is inheritance?
**A:** A mechanism where a class (child) acquires properties and methods of another (parent).

**Code:**
```python
class Vehicle:                       # parent / base class
    def start(self):
        return "engine started"

class Bike(Vehicle):                 # child / derived class inherits start()
    pass

b = Bike()
print(b.start())                     # engine started
```

## Q9: What are the types of inheritance?
**A:** Single, multiple (via interfaces), multilevel, hierarchical, hybrid.

**Code:**
```python
class A: pass

# Single            -> one parent
class B(A): pass

# Multilevel        -> chain of inheritance
class C(B): pass

# Hierarchical      -> several children of one parent
class D(A): pass
class E(A): pass

# Multiple          -> more than one parent (Python supports it directly)
class F(A): pass
class G(A): pass
class FG(F, G): pass

# Hybrid            -> combination of the above
class H(C, F): pass

for k in (B, C, D, E, FG, H):
    print(k.__name__, "bases:", [b.__name__ for b in k.__bases__])
```

## Q10: What is polymorphism?
**A:** The ability of an entity to take many forms, allowing one interface for different types.

**Code:**
```python
class Bird:
    def sound(self): pass

class Crow(Bird):
    def sound(self):
        return "caw caw"

class Sparrow(Bird):
    def sound(self):
        return "chirp chirp"

for bird in (Crow(), Sparrow()):     # one interface: sound()
    print(bird.sound())              # each type behaves differently
```

## Q11: What is compile-time polymorphism?
**A:** Achieved via method overloading and operator overloading; resolved at compile time.

**Code:**
```python
# Python is interpreted, so overload-style behavior is simulated with default args.
class Calc:
    def add(self, a, b, c=None):     # same method, different parameter counts
        return a + b if c is None else a + b + c

print(Calc().add(1, 2))              # 3
print(Calc().add(1, 2, 3))           # 6
```

## Q12: What is runtime polymorphism?
**A:** Achieved via method overriding with inheritance and virtual functions; resolved at runtime.

**Code:**
```python
class Animal:
    def sound(self):
        return "generic animal sound"

class Dog(Animal):
    def sound(self):                  # overriding -> resolved at runtime
        return "bark"

def play(a):                          # the call is bound to the real type at runtime
    return a.sound()

print(play(Animal()))                 # generic animal sound
print(play(Dog()))                    # bark
```

## Q13: What is method overloading?
**A:** Defining multiple methods with the same name but different parameters in the same class.

**Code:**
```python
class Printer:
    def show(self, *args):            # Python overloading via *args / default args
        return " ".join(str(x) for x in args)

print(Printer().show(1))              # 1
print(Printer().show(1, 2, "hi"))     # 1 2 hi
```

## Q14: What is method overriding?
**A:** A subclass provides a specific implementation of a method already defined in its parent.

**Code:**
```python
class Shape:
    def area(self):
        return "generic area"

class Circle(Shape):
    def area(self):                   # overrides the parent's area()
        return 3.14159

print(Circle().area())                # 3.14159
```

## Q15: What is a constructor?
**A:** A special method called automatically when an object is created, used for initialization.

**Code:**
```python
class Person:
    def __init__(self, name):         # constructor: runs automatically
        self.name = name              # initialize the object

    def greet(self):
        return f"hi {self.name}"

print(Person("Sam").greet())          # hi Sam
```

## Q16: What is a destructor?
**A:** A method that cleans up resources when an object is destroyed.

**Code:**
```python
class Temp:
    def __init__(self):
        print("object created")

    def __del__(self):                # destructor: called on destruction
        print("object destroyed")

t = Temp()
del t                                 # triggers __del__
```

## Q17: What is a default constructor?
**A:** A constructor with no parameters, provided by the compiler if none is defined.

**Code:**
```python
class NoInit:                         # no constructor defined
    pass

o = NoInit()                          # Python provides a default constructor
print(hasattr(o, "__init__"))         # True
```

## Q18: What is a parameterized constructor?
**A:** A constructor that accepts arguments to initialize an object with specific values.

**Code:**
```python
class Point:
    def __init__(self, x, y):         # parameterized constructor
        self.x = x
        self.y = y

p = Point(3, 4)
print(p.x, p.y)                       # 3 4
```

## Q19: What is a copy constructor?
**A:** A constructor that creates a new object as a copy of an existing object.

**Code:**
```python
class Serial:
    def __init__(self, val=None):
        self.val = val if val is not None else "new"

s1 = Serial("abc")
s2 = Serial(val=s1.val)               # create s2 as a copy of s1
print(s1.val, s2.val)                 # abc abc
print(s1 is not s2)                   # True: distinct objects
```

## Q20: What is this keyword?
**A:** 'this' refers to the current object instance within a class.

**Code:**
```python
class Counter:
    def __init__(self):
        self.count = 0

    def inc(self):
        self.count += 1               # 'self' == "this": the current instance
        return self                   # return self for chaining

print(Counter().inc().inc().count)    # 2
```

## Q21: What is super keyword?
**A:** 'super' refers to the parent class, used to access its members or constructor.

**Code:**
```python
class Parent:
    def __init__(self, name):
        self.name = name

class Child(Parent):
    def __init__(self, name, age):
        super().__init__(name)        # super() -> parent class constructor
        self.age = age

c = Child("kid", 8)
print(c.name, c.age)                  # kid 8
```

## Q22: What is an abstract class?
**A:** A class that cannot be instantiated and may contain abstract methods (no body).

**Code:**
```python
from abc import ABC, abstractmethod

class Shape(ABC):                     # abstract class
    @abstractmethod
    def area(self): ...               # abstract method (no body)

try:
    Shape()                           # cannot instantiate
except TypeError as e:
    print("Blocked:", e)

class Circle(Shape):                  # concrete subclass must implement area()
    def area(self):
        return 3.14159

print(Circle().area())                # 3.14159
```

## Q23: What is an abstract method?
**A:** A method declared without implementation, to be defined by subclasses.

**Code:**
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self): ...               # abstract: no implementation here

class Square(Shape):
    def area(self):                   # must be implemented by subclass
        return 16

print(Square().area())                # 16
```

## Q24: What is an interface?
**A:** A contract specifying methods a class must implement, with no implementation (pure abstraction).

**Code:**
```python
from abc import ABC, abstractmethod

class Drawable(ABC):                  # interface-like contract
    @abstractmethod
    def draw(self): ...

class Square(Drawable):               # must satisfy the contract
    def draw(self):
        return "drawing square"

print(Square().draw())                # drawing square
```

## Q25: Difference between abstract class and interface.
**A:** Abstract classes can have state and partial implementation; interfaces define only behavior (until default methods).

**Code:**
```python
from abc import ABC, abstractmethod

class Dog(ABC):                       # abstract class
    legs = 4                          # state allowed
    @abstractmethod
    def bark(self): ...

    def info(self):                   # partial implementation allowed
        return f"{self.legs} legs"

class Pug(Dog):
    def bark(self): return "woof"

print(Pug().bark(), "|", Pug().info())   # woof | 4 legs
# A pure interface (Q24) would allow only the abstract method.
```

## Q26: What is multiple inheritance?
**A:** A class inheriting from more than one class; not supported directly in many languages (for example, Java) due to ambiguity.

**Code:**
```python
class Bird:
    def fly(self):
        return "flying"

class Fish:
    def swim(self):
        return "swimming"

class Penguin(Bird, Fish):            # Python supports multiple parents
    pass

p = Penguin()
print(p.fly(), "and", p.swim())       # flying and swimming
```

## Q27: What is the diamond problem?
**A:** Ambiguity arising in multiple inheritance when two parent classes inherit from a common grandparent.

**Code:**
```python
class Grand:
    def who(self):
        return "grand"

class Left(Grand): pass
class Right(Grand): pass

class Diamond(Left, Right):           # Python resolves via MRO (C3 linearization)
    pass

d = Diamond()
print(d.who())                        # grand
print([c.__name__ for c in Diamond.__mro__])
# ['Diamond', 'Left', 'Right', 'Grand', 'object']
```

## Q28: What is a static method?
**A:** A method belonging to the class rather than an instance; called without creating an object.

**Code:**
```python
class Utility:
    @staticmethod
    def convert(s):                   # no 'self' — callable on the class
        return s.upper()

print(Utility.convert("abc"))         # ABC
```

## Q29: What is a static variable?
**A:** A variable shared by all instances of a class, stored in class memory.

**Code:**
```python
class Garage:
    count = 0                         # static / class variable

    def __init__(self):
        Garage.count += 1

a, b = Garage(), Garage()
print(Garage.count)                   # 2 (shared by all instances)
print(a.count == b.count)             # True (same memory slot)
```

## Q30: What is the difference between static and instance methods?
**A:** Static belongs to class and cannot access instance members directly; instance operates on an object.

**Code:**
```python
class Scaler:
    scale = 2                         # class-level

    def __init__(self, x):
        self.x = x                    # instance-level

    def instance_double(self):        # instance method: operates on the object
        return self.x * self.scale

    @staticmethod
    def static_double(x):             # static method: belongs to the class
        return x * Scaler.scale

print(Scaler(5).instance_double())    # 10
print(Scaler.static_double(5))        # 10
```

## Q31: What is a final class or method?
**A:** A final class cannot be inherited; a final method cannot be overridden.

**Code:**
```python
# Python has no 'final' keyword; simulate it with __init_subclass__ / a metaclass.

# final class
class FinalClass:
    def __init_subclass__(cls, **kwargs):
        raise TypeError("FinalClass cannot be inherited")

try:
    class Sub(FinalClass): pass
except TypeError as e:
    print("Blocked:", e)

# final method
class FinalMethodMeta(type):
    def __init__(cls, name, bases, ns):
        super().__init__(name, bases, ns)
        for base in bases:
            for m in getattr(base, "_final_methods", ()):
                if m in ns:
                    raise TypeError(f"'{m}' is final")

class WithFinal(metaclass=FinalMethodMeta):
    def locked(self):
        return "cannot change me"
    WithFinal._final_methods = ("locked",)

try:
    class Breaker(WithFinal):
        def locked(self): return "hacked"
except TypeError as e:
    print("Blocked:", e)
```

## Q32: What is method hiding?
**A:** When a subclass defines a static method with the same signature as a parent's static method.

**Code:**
```python
class Parent:
    @staticmethod
    def greet():
        return "parent static greet"

class Child(Parent):
    @staticmethod
    def greet():                      # hides the parent's static method
        return "child static greet"

print(Parent.greet())                 # parent static greet
print(Child.greet())                  # child static greet
```

## Q33: What is a pure virtual function?
**A:** A virtual function with no implementation, forcing subclasses to override (C++).

**Code:**
```python
from abc import ABC, abstractmethod

class Base(ABC):
    @abstractmethod                  # Python equivalent of a pure virtual fn
    def run(self): ...

class Runner(Base):
    def run(self):
        return "running"

print(Runner().run())                 # running
```

## Q34: What is early binding?
**A:** Linking a function call to its definition at compile time (static binding).

**Code:**
```python
# In Python, an un-overridden name resolves to its (known) definition.
def helper(x):
    return x * 2

# 'helper' is bound here statically/no dispatch.
print("early-bound result:", helper(21))   # early-bound result: 42
```

## Q35: What is late binding?
**A:** Resolving a function call at runtime via virtual tables (dynamic binding).

**Code:**
```python
class Animal:
    def sound(self): return "generic sound"

class Dog(Animal):
    def sound(self): return "bark"

def announce(x):                       # which sound()? decided at runtime
    return x.sound()

print(announce(Animal()))              # generic sound
print(announce(Dog()))                 # bark
```

## Q36: What is a virtual function?
**A:** A function that can be overridden in a derived class and resolved at runtime.

**Code:**
```python
# In Python every method is virtual: it can be overridden and dispatched dynamically.
class Base:
    def draw(self): return "base"

class Circle(Base):
    def draw(self): return "circle"   # override -> runtime dispatch

print(Base().draw())                  # base
print(Circle().draw())                # circle
```

## Q37: What is operator overloading?
**A:** Defining custom behavior for operators (+, -, etc.) for user-defined types.

**Code:**
```python
class Money:
    def __init__(self, v):
        self.v = v

    def __add__(self, other):          # overload '+'
        return Money(self.v + other.v)

    def __mul__(self, n):              # overload '*'
        return Money(self.v * n)

    def __str__(self):
        return f"${self.v}"

print(Money(5) + Money(3))             # $8
print(Money(5) * 2)                    # $10
```

## Q38: What is function overloading versus overriding?
**A:** Overloading is same name different params (compile-time); overriding is redefining inherited method (runtime).

**Code:**
```python
# Overloading  (same name, different params) -> Python: default args
class MathOps:
    def compute(self, a, b=None):
        return a if b is None else a + b

# Overriding  (redefine inherited method)     -> runtime
class NewMathOps(MathOps):
    def compute(self, a, b=None):
        return f"new={super().compute(a, b)}"

print(MathOps().compute(1, 2))      # 3
print(NewMathOps().compute(1, 2))   # new=3
```

## Q39: What is cohesion?
**A:** Degree to which class members are related to a single purpose (high cohesion is good).

**Code:**
```python
class Logger:                        # high cohesion: everything is about logging
    def __init__(self):
        self.messages = []

    def log(self, msg):
        self.messages.append(msg)

    def dump(self):
        return list(self.messages)

log = Logger()
log.log("boot")
print(log.dump())                    # ['boot']
```

## Q40: What is coupling?
**A:** Degree of interdependence between modules (low coupling is desirable).

**Code:**
```python
# Low coupling: 'go' only depends on the .start() contract, not a concrete class.
def go(engine):
    return engine.start()

class ElectricEngine:
    def start(self): return "power on"

class DieselEngine:
    def start(self): return "vroom"

print(go(ElectricEngine()))          # power on
print(go(DieselEngine()))            # vroom
```

## Q41: What is the difference between composition and aggregation?
**A:** Composition is strong ownership (part destroyed with whole); aggregation is weak (part can exist independently).

**Code:**
```python
class Engine:
    def start(self):
        return "engine on"

# Composition: the Car CREATES the engine -> strong ownership
class CarComposition:
    def __init__(self):
        self.engine = Engine()

# Aggregation: the engine is created elsewhere and passed in -> shared/weak
class CarAggregation:
    def __init__(self, engine):
        self.engine = engine

eng = Engine()                       # engine can exist on its own
print(CarAggregation(eng).engine.start())   # engine on
print(CarComposition().engine.start())      # engine on
```

## Q42: What is association?
**A:** A relationship between two classes (for example, "uses" or "has-a").

**Code:**
```python
class Student:
    pass

class Teacher:                       # association: teacher uses/knows students
    def __init__(self):
        self.students = []

    def add_student(self, s):
        self.students.append(s)

t = Teacher()
t.add_student(Student())
print("teacher has", len(t.students), "student(s)")   # teacher has 1 student(s)
```

## Q43: What is the 'has-a' relationship?
**A:** Composition or aggregation representing ownership or use of one object by another.

**Code:**
```python
class Chip:
    pass

class Phone:
    def __init__(self):
        self.chip = Chip()           # Phone HAS-A Chip

print(hasattr(Phone(), "chip"))      # True
```

## Q44: What is the 'is-a' relationship?
**A:** Inheritance, where a subclass is a specialized form of its parent.

**Code:**
```python
class Fruit:
    pass

class Apple(Fruit):                  # Apple IS-A Fruit (inheritance)
    pass

print(isinstance(Apple(), Fruit))    # True
```

## Q45: What is a singleton pattern?
**A:** A design pattern ensuring only one instance of a class exists globally.

**Code:**
```python
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

s1, s2 = Singleton(), Singleton()
print(s1 is s2)                      # True: one instance per process
```

## Q46: What is the factory pattern?
**A:** A creational pattern that provides an interface for creating objects without specifying exact classes.

**Code:**
```python
class Car:
    def info(self): return "Car"

class Motorcycle:
    def info(self): return "Motorcycle"

class VehicleFactory:
    @staticmethod
    def create(kind):                # interface hides the concrete classes
        if kind == "car":
            return Car()
        if kind == "bike":
            return Motorcycle()
        raise ValueError(kind)

print(VehicleFactory.create("car").info())     # Car
print(VehicleFactory.create("bike").info())    # Motorcycle
```

## Q47: What is the observer pattern?
**A:** A pattern where objects (observers) are notified of changes in a subject automatically.

**Code:**
```python
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, obs):
        self._observers.append(obs)

    def notify(self, msg):
        for obs in self._observers:
            obs.update(msg)

class Observer:
    def update(self, msg):
        print(f"[Observer] got: {msg}")

sub = Subject()
sub.attach(Observer())
sub.attach(Observer())
sub.notify("state changed")          # both observers react automatically
```

## Q48: What is SOLID principle?
**A:** Five design principles: Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, Dependency Inversion.

**Code:**
```python
# S -> Q49, O -> Q50, L -> Q51, I -> Q52, D -> Q53 (each with code below).
print("See the five examples in Q49-Q53.")
```

## Q49: Explain Single Responsibility Principle.
**A:** A class should have only one reason to change (one responsibility).

**Code:**
```python
class Report:
    def __init__(self, data):
        self.data = data

    def content(self):               # responsibility #1: report content
        return ";".join(self.data)

class ReportWriter:                  # responsibility #2: persistence, separate
    def save(self, report):
        print(f"saved: {report.content()}")

ReportWriter().save(Report(["a", "b"]))   # saved: a;b
```

## Q50: Explain Open-Closed Principle.
**A:** Software entities should be open for extension but closed for modification.

**Code:**
```python
class Discount:                      # open for extension...
    def apply(self, price):
        return price

class HolidayDiscount(Discount):     # ...by subclassing, without modifying Discount
    def apply(self, price):
        return price * 0.9

print(Discount().apply(100))         # 100
print(HolidayDiscount().apply(100))  # 90.0
```

## Q51: Explain Liskov Substitution Principle.
**A:** Subtypes must be replaceable for their base types without altering correctness.

**Code:**
```python
class Bird:
    def speed(self): return 10

class FastBird(Bird):                 # subtype behaves like base
    def speed(self): return 20

def race(bird):                       # works with Bird or any subclass
    return f"{bird.speed()} km/h"

print(race(Bird()))                   # 10 km/h
print(race(FastBird()))              # 20 km/h
```

## Q52: Explain Interface Segregation Principle.
**A:** Clients should not depend on interfaces they do not use; prefer small specific interfaces.

**Code:**
```python
from abc import ABC, abstractmethod

class Reader(ABC):
    @abstractmethod
    def read(self): ...

class WriterI(ABC):                   # split into small specific interfaces
    @abstractmethod
    def write(self): ...

class FileStore(Reader, WriterI):     # implement only what you need
    def read(self):
        return "read"

    def write(self):
        return "write"

print(FileStore().read(), FileStore().write())   # read write
```

## Q53: Explain Dependency Inversion Principle.
**A:** High-level modules should not depend on low-level modules; both depend on abstractions.

**Code:**
```python
from abc import ABC, abstractmethod

class Notifier(ABC):                  # abstraction
    @abstractmethod
    def notify(self, msg): ...

class Email(Notifier):
    def notify(self, msg):
        print(f"email: {msg}")

class SMS(Notifier):
    def notify(self, msg):
        print(f"sms: {msg}")

class AlertService:                   # high-level depends on abstraction
    def __init__(self, notifier: Notifier):
        self.notifier = notifier

    def run(self):
        self.notifier.notify("server down")

AlertService(Email()).run()           # email: server down
AlertService(SMS()).run()             # sms: server down
```

## Q54: What is a design pattern?
**A:** A reusable solution to a commonly occurring problem in software design.

**Code:**
```python
# Examples of patterns (with code) appear in:
#   Q45 Singleton, Q46 Factory, Q47 Observer, Q55-57 other families.
print("A pattern is a reusable recipe, not a library.")
```

## Q55: What are creational design patterns?
**A:** Patterns dealing with object creation: Singleton, Factory, Builder, Prototype, Abstract Factory.

**Code:**
```python
# Builder (step-by-step construction)
class Burger:
    def __init__(self):
        self.patties, self.cheese = 1, False
    def __str__(self):
        return f"{self.patties} patties, cheese={self.cheese}"

class BurgerBuilder:
    def __init__(self):
        self.b = Burger()
    def add_patty(self):
        self.b.patties += 1; return self
    def with_cheese(self):
        self.b.cheese = True; return self
    def build(self):
        return self.b

# Prototype (clone existing objects)
import copy
class Prototype:
    def __init__(self, payload):
        self.payload = payload
    def clone(self):
        return copy.deepcopy(self)

print(BurgerBuilder().add_patty().with_cheese().build())       # 2 patties, cheese=True
p = Prototype([1, 2])
print(p.clone().payload)                                       # [1, 2]
```

## Q56: What are structural design patterns?
**A:** Patterns composing classes: Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy.

**Code:**
```python
# Adapter (make incompatible interfaces work together)
class USPlug:
    def deliver(self):
        return "US power"

class EUPlug:                          # adapter wraps USPlug into an EU interface
    def __init__(self):
        self.us = USPlug()
    def deliver(self):
        return self.us.deliver() + " via EU adapter"

# Decorator (add behavior dynamically)
def espresso():
    return "espresso"

def with_milk(fn):
    def wrapper():
        return fn() + " + milk"
    return wrapper

# Facade (simple front to a complex subsystem)
class Hotel:
    def order(self):
        return "meal delivered"

print(EUPlug().deliver())              # US power via EU adapter
print(with_milk(espresso)())           # espresso + milk
print(Hotel().order())                 # meal delivered
```

## Q57: What are behavioral design patterns?
**A:** Patterns managing communication: Observer, Strategy, Command, Template, State, Iterator.

**Code:**
```python
from abc import ABC, abstractmethod

# Strategy (swap algorithms)
class Shipping(ABC):
    @abstractmethod
    def cost(self, weight): ...

class Air(Shipping):
    def cost(self, weight): return weight * 3

class Ground(Shipping):
    def cost(self, weight): return weight * 1

def checkout(strategy, weight):
    return strategy.cost(weight)

# Template method (fixed skeleton, overridable steps)
class Pipeline(ABC):
    def run(self):
        self.fetch(); self.transform(); self.load()
    @abstractmethod
    def fetch(self): ...
    @abstractmethod
    def transform(self): ...
    def load(self):
        print("load done")

class CSV(Pipeline):
    def fetch(self): print("read csv")
    def transform(self): print("clean rows")

print("air:", checkout(Air(), 10), "| ground:", checkout(Ground(), 10))
CSV().run()
```

## Q58: What is the difference between procedural and OOP?
**A:** Procedural focuses on functions and logic; OOP focuses on objects and data encapsulation.

**Code:**
```python
# Procedural: functions operate on shared/free data
def rect_area_procedural(w, h):
    return w * h

# OOP: data + behavior live together in an object
class Rect:
    def __init__(self, w, h):
        self.w, self.h = w, h
    def area(self):
        return self.w * self.h

print(rect_area_procedural(2, 3))      # 6
print(Rect(2, 3).area())               # 6
```

## Q59: What is garbage collection?
**A:** Automatic memory management reclaiming objects no longer referenced.

**Code:**
```python
import gc, weakref

class Obj:
    def __del__(self):
        print("  collected")

r = Obj()
ref = weakref.ref(r)                   # weak reference does NOT keep it alive
print("alive before del:", ref() is not None)
del r                                  # no more strong references
print("alive after del:", ref() is None)   # True: GC reclaims it
gc.collect()                           # manual trigger (usually automatic)
```

## Q60: What is a memory leak in OOP?
**A:** Unused objects retained by references, preventing garbage collection.

**Code:**
```python
Cache = []
def bad():
    Cache.append(object())             # object kept alive in global list
    return "done"

bad()
print("unused objects retained:", len(Cache))   # 1 -> leak: still referenced
Cache.clear()                          # fix: remove the reference
print("after clearing:", len(Cache))   # 0
```

## Q61: What is the difference between stack and heap?
**A:** Stack stores local variables and calls; heap stores dynamically allocated objects.

**Code:**
```python
# Python hides this: local variables live in a call stack frame,
# and all objects live on the heap, managed automatically by the GC.
def f():
    x = 1       # 'x' lives in this stack frame
    obj = []    # the list object lives on the heap
    return obj

print(type(f()).__name__)              # list
```

## Q62: What is an exception?
**A:** An event disrupting normal flow, handled via try-catch blocks.

**Code:**
```python
try:
    result = 10 / 0                    # raises an exception
except ZeroDivisionError:
    print("ZeroDivisionError event caught")   # ZeroDivisionError event caught
```

## Q63: What is exception handling?
**A:** Mechanism to catch and respond to runtime errors gracefully.

**Code:**
```python
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return float("inf")

print(safe_divide(10, 0))              # inf (graceful response)
```

## Q64: What is the difference between checked and unchecked exceptions?
**A:** Checked are verified at compile time; unchecked (runtime) are not.

**Code:**
```python
# Python only has runtime ('unchecked'-style) exceptions; there is no
# compile-time 'checked' category. Any exception class caught at runtime:
class MyError(Exception):
    pass

try:
    raise MyError("boom")
except MyError as e:
    print("caught:", e)                # caught: boom
```

## Q65: What is try-catch-finally?
**A:** try contains risky code, catch handles exceptions, finally runs always (cleanup).

**Code:**
```python
try:
    print("try: risky code")           # try
    value = 10 / 2
except ZeroDivisionError as e:
    print("except: handled", e)        # except (only on error)
finally:
    print("finally: always runs")      # finally (cleanup)

# Output: try / finally (no error raised)
```

## Q66: What is throw versus throws?
**A:** throw raises an exception; throws declares exceptions a method may propagate.

**Code:**
```python
# Python: 'raise' == throw. There is no 'throws' declaration; exceptions
# simply propagate up the call stack until handled.

class AgeError(ValueError):
    pass

def set_age(age):
    if age < 0:
        raise AgeError("age must be >= 0")   # 'throw'
    return age

try:
    set_age(-1)
except AgeError as e:                        # handled somewhere up the stack
    print("raised:", e)                      # raised: age must be >= 0
```

## Q67: What is a namespace or package?
**A:** A container grouping related classes to avoid naming conflicts.

**Code:**
```python
# In Python, modules/packages are namespaces; classes are namespaces too.
import math as math_module               # stdlib namespace (qualified access)

class MathExtra:                         # our namespace
    def __init__(self):
        self.fast = True

print(hasattr(math_module, "log"))       # True (math.log lives in 'math' ns)
print(MathExtra().fast)                  # True
# Two different 'log'-ish names can coexist because they live in different namespaces.
```

## Q68: What is polymorphism with real example?
**A:** A 'Shape' parent with 'draw()' overridden by Circle, Square — one call, different behavior.

**Code:**
```python
class Shape:
    def draw(self): return "generic shape"

class Circle(Shape):
    def draw(self): return "drawing a circle"

class Square(Shape):
    def draw(self): return "drawing a square"

for s in (Shape(), Circle(), Square()):   # one draw() call...
    print(s.draw())                       # ...produces different behaviors
```

## Q69: What is object lifetime?
**A:** Creation (constructor) to destruction (garbage collection or destructor).

**Code:**
```python
class Life:
    def __init__(self):
        print("born (constructor)")
    def __del__(self):
        print("gone (destructor)")

obj = Life()      # born (constructor)
del obj           # gone (destructor)
```

## Q70: What is a reference versus pointer (OOP context)?
**A:** A reference is an alias to an object; a pointer holds a memory address (C++).

**Code:**
```python
# Python has references, not C-style pointers. Assignment aliases the same object.
a = [1, 2]
b = a                                  # b is an alias (reference) to the same list
b.append(3)
print(a)                               # [1, 2, 3]  -> same object seen from both names
print(a is b)                          # True
```

## Q71: What is a shallow copy?
**A:** Copying object references so original and copy share nested objects.

**Code:**
```python
import copy

original = [[1, 2], [3, 4]]
shallow = copy.copy(original)          # top-level copy only
shallow[0].append(99)                  # nested list is SHARED
print(original)                        # [[1, 2, 99], [3, 4]]
print(original[0] is shallow[0])       # True (shared inner object)
```

## Q72: What is a deep copy?
**A:** Creating independent copies of all nested objects.

**Code:**
```python
import copy

original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)         # fully independent copy
deep[0].append(99)
print(original)                        # [[1, 2], [3, 4]]  unchanged
print(original[0] is deep[0])          # False (not shared)
```

## Q73: What is immutability?
**A:** An object whose state cannot be changed after creation (for example, String in Java).

**Code:**
```python
tup = (1, 2, 3)                        # tuple is immutable
try:
    tup[0] = 0
except TypeError as e:
    print("mutation blocked:", e)      # mutation blocked: 'tuple' object does not...

frozen = frozenset([1, 2])             # frozenset is immutable too
print(frozen)                          # frozenset({1, 2})
```

## Q74: Why use immutable objects?
**A:** Thread safety, caching, and predictable behavior.

**Code:**
```python
from dataclasses import dataclass

@dataclass(frozen=True)                # immutable data class
class Config:
    host: str
    port: int

cfg = Config("localhost", 8080)
print(cfg.host, cfg.port)              # localhost 8080
# cfg.port = 9090  -> FrozenInstanceError: state cannot change (thread-safe)
```

## Q75: What is a record or class in modern OOP?
**A:** Records (for example, Java slash C#) are concise immutable data carriers with auto-generated methods.

**Code:**
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Point3D:
    x: int
    y: int
    z: int

p1, p2 = Point3D(1, 2, 3), Point3D(1, 2, 3)
print(p1)                              # Point3D(x=1, y=2, z=3)  (auto __repr__)
print(p1 == p2)                        # True (auto __eq__)
print(hash(p1))                        # auto __hash__ because it is frozen
```

## Q76: What is the difference between class and struct?
**A:** Classes are reference types; structs are value types (for example, in C# slash C++).

**Code:**
```python
# Python has no struct; @dataclass is used as a value-like data container.
# Meaning: class instance = shared reference (alias), value type = copied.
from dataclasses import dataclass

class BoxClass:                        # reference-type behavior
    def __init__(self, v):
        self.v = v

@dataclass
class BoxValue:                        # value-like container
    v: int

a = BoxClass(5); b = a                 # b is an alias of a
b.v = 9
print(a.v)                             # 9  (same object -> change visible)
```

## Q77: What is method signature?
**A:** Method name and parameter list (not return type).

**Code:**
```python
import inspect

def greet(name, greeting="hi", *, loud=False):
    return f"{greeting} {name}"

print(greet.__name__)                                     # greet
print(list(inspect.signature(greet).parameters))          # ['name', 'greeting', 'loud']
# Return type is NOT part of the signature.
```

## Q78: What is a getter and setter?
**A:** Methods to read (get) and modify (set) private fields, enforcing encapsulation.

**Code:**
```python
class Temperature:
    def __init__(self, c):
        self._c = c

    @property
    def celsius(self):                 # getter
        return self._c

    @celsius.setter
    def celsius(self, value):          # setter with validation
        if value < -273.15:
            raise ValueError("below absolute zero")
        self._c = value

t = Temperature(25)
print(t.celsius)                       # 25 (via getter)
t.celsius = 30                         # via setter (validated)
print(t.celsius)                       # 30
```

## Q79: What is tight versus loose coupling?
**A:** Tight means high dependency; loose achieved via interfaces or abstractions for flexibility.

**Code:**
```python
class PetrolEngine:
    def start(self): return "vroom"

# TIGHT coupling: OldCar hard-depends on PetrolEngine
class OldCar:
    def __init__(self):
        self.engine = PetrolEngine()

# LOOSE coupling: depends only on the .start() contract (any engine)
def drive(engine):
    return engine.start()

print(OldCar().engine.start())         # vroom
print(drive(PetrolEngine()))           # vroom (works with any engine)
```

## Q80: What is an inner class?
**A:** A class defined within another class, with access to outer class members.

**Code:**
```python
class Outer:
    def __init__(self):
        self.inner = Outer.Inner()     # instantiating the inner class

    class Inner:                       # nested / inner class
        def hi(self):
            return "inner class method"

print(Outer().inner.hi())              # inner class method
print(Outer.Inner().hi())              # inner class method
```

## Q81: What is an anonymous class?
**A:** A class defined and instantiated without a name (for example, Java event handlers).

**Code:**
```python
# Python has no true anonymous classes. Closest options:
Greeter = type("Greeter", (), {"greet": lambda self, n: f"hi {n}"})
print(Greeter().greet("Sam"))          # hi Sam

# or an anonymous function (Q82):
greet = lambda n: f"hi {n}"
print(greet("Sam"))                    # hi Sam
```

## Q82: What is a lambda expression in OOP?
**A:** A concise way to represent an anonymous function, often as a functional interface.

**Code:**
```python
add = lambda x, y: x + y               # anonymous function
print(add(2, 3))                       # 5
print(list(map(lambda n: n * 2, [1, 2, 3])))   # [2, 4, 6]
```

## Q83: What is functional interface?
**A:** An interface with exactly one abstract method, enabling lambda usage.

**Code:**
```python
from abc import ABC, abstractmethod

class Greeter(ABC):                    # single abstract method -> functional-style
    @abstractmethod
    def greet(self, name): ...

class FriendlyGreeter(Greeter):
    def greet(self, name):
        return f"hi {name}"

print(FriendlyGreeter().greet("Sam"))  # hi Sam
```

## Q84: What is the difference between override and overload in C#?
**A:** Override redefines inherited virtual method; overload defines same-name methods with different params.

**Code:**
```python
class Base:
    def say(self, word=None):          # overload-style via default param
        return word or "base"

class Derived(Base):
    def say(self, word=None):          # override: redefines inherited method
        return f"derived: {super().say(word)}"

print(Base().say("hello"))             # hello        (overload path)
print(Derived().say("hello"))          # derived: hello (override)
```

## Q85: What is base class and derived class?
**A:** Base (parent) is inherited from; derived (child) inherits from base.

**Code:**
```python
class BaseClass:                       # base / parent
    def method(self):
        return "from base"

class DerivedClass(BaseClass):         # derived / child
    pass

d = DerivedClass()
print(d.method())                                   # from base
print(issubclass(DerivedClass, BaseClass))          # True
```

## Q86: What is a sealed class?
**A:** A class that cannot be inherited (similar to final).

**Code:**
```python
# Python equivalent: guard against subclassing with __init_subclass__.
class Sealed:
    def __init_subclass__(cls, **kwargs):
        raise TypeError("Sealed cannot be inherited")

try:
    class Child(Sealed): pass
except TypeError as e:
    print("Blocked:", e)               # Blocked: Sealed cannot be inherited
```

## Q87: What is dynamic binding?
**A:** Associating a method call with method code at runtime (polymorphism).

**Code:**
```python
class Shape:
    def name(self): return "shape"

class Square(Shape):
    def name(self): return "square"

def describe(s):                       # method code chosen at runtime
    return s.name()

print(describe(Shape()))               # shape
print(describe(Square()))              # square
```

## Q88: What is the difference between abstraction in OOP and abstract class?
**A:** Abstraction is a concept; abstract class is a language construct enabling it.

**Code:**
```python
from abc import ABC, abstractmethod

# Abstraction (concept)  -> hiding complexity, exposing essentials (see Q6)
# Abstract class (construct) -> the tool Python gives us to enforce it:
class Storage(ABC):
    @abstractmethod
    def save(self, data): ...

class FileStorage(Storage):
    def save(self, data):
        return f"saved: {data}"

print(FileStorage().save("x"))         # saved: x
```

## Q89: What is reuse in OOP?
**A:** Achieved through inheritance and composition to avoid duplicate code.

**Code:**
```python
class LoggerBase:
    def log(self, msg):
        return f"[{msg}]"

class AppLogger(LoggerBase):           # reuse via inheritance
    pass

class Engine:
    def start(self): return "engine started"

class Car:
    def __init__(self):
        self.engine = Engine()         # reuse via composition

print(AppLogger().log("info"))         # [info]
print(Car().engine.start())            # engine started
```

## Q90: What is a marker interface?
**A:** An empty interface used to signal metadata to the compiler or runtime (for example, Serializable).

**Code:**
```python
class Serializable:                    # marker interface: no methods
    pass

class UserRecord(Serializable):
    def __init__(self, name):
        self.name = name

u = UserRecord("amy")
print(isinstance(u, Serializable))     # True: tags the class as serializable
```

## Q91: What is the difference between equals() and equals ?
**A:** equals compares references (or primitives); equals() compares logical content (overridable).

**Code:**
```python
# Python:  '==' calls __eq__ (logical content),  'is' checks identity (== in Java)
class Money:
    def __init__(self, v):
        self.v = v

    def __eq__(self, other):           # equals(): logical comparison
        return self.v == other.v

m1, m2 = Money(10), Money(10)
print(m1 == m2)                        # True   (logical content)
print(m1 is m2)                        # False  (reference identity)
```

## Q92: What is a hashCode?
**A:** An integer representing an object, used in hash-based collections for fast lookup.

**Code:**
```python
class Item:
    def __init__(self, key):
        self.key = key

    def __hash__(self):
        return hash(self.key)          # integer representation

    def __eq__(self, other):
        return self.key == other.key

box = {Item("apple"), Item("pear")}    # hash-based set uses __hash__ for lookup
print(len(box))                        # 2
```

## Q93: What is the contract between equals and hashCode?
**A:** If two objects are equal, they must have the same hashCode; objects with same hash may differ.

**Code:**
```python
class Person:
    def __init__(self, ssn):
        self.ssn = ssn

    def __eq__(self, other):                    # equal objects...
        return isinstance(other, Person) and self.ssn == other.ssn

    def __hash__(self):
        return hash(self.ssn)                   # ...have the same hash

a, b = Person("123"), Person("123")
print(a == b)                            # True
print(hash(a) == hash(b))                # True  (contract satisfied)
print({a, b})                            # {one} -- treated as a single key
```

## Q94: What is the difference between an object and a class variable?
**A:** Object (instance) variables are per-instance; class (static) variables are shared.

**Code:**
```python
class Counter:
    total = 0                            # class (static) variable: shared

    def __init__(self):
        self.instance_count = 0          # instance variable: per-object
        Counter.total += 1

x, y = Counter(), Counter()
x.instance_count += 5                    # only x changes
print(x.instance_count, y.instance_count)  # 5 0   (per-instance)
print(Counter.total)                     # 2      (shared, class-level)
```

## Q95: What is a constant?
**A:** A variable whose value cannot change after initialization (const or final).

**Code:**
```python
from typing import Final               # Python convention (not enforced at runtime)

class Graphics:
    PI: Final = 3.14159                # treat as a constant by convention
    MAX_PIXELS: Final = 4096

print(Graphics.PI, Graphics.MAX_PIXELS)   # 3.14159 4096
```

## Q96: What is the difference between composition and inheritance?
**A:** Composition reuses via containment (flexible); inheritance reuses via hierarchy (tight coupling).

**Code:**
```python
class Engine:
    def start(self): return "started"

class Bus:                             # composition: contains an engine
    def __init__(self):
        self._engine = Engine()
    def start(self):
        return f"bus {self._engine.start()}"

class ScoutCar(Engine):                # inheritance: tightly coupled to Engine
    pass

print(Bus().start())                   # bus started
print(ScoutCar().start())              # started
```

## Q97: What is the principle of favoring composition over inheritance?
**A:** Prefer composing objects to share behavior to reduce fragility and coupling.

**Code:**
```python
class SpeakBehavior:
    def speak(self): return "speak"

class ShoutBehavior:                   # behavior extracted into components
    def speak(self): return "SHOUT"

class Robot:
    def __init__(self, voice):         # compose any behavior
        self._voice = voice
    def speak(self):
        return self._voice.speak()

print(Robot(SpeakBehavior()).speak())  # speak
print(Robot(ShoutBehavior()).speak())  # SHOUT
```

## Q98: What is a delegate (C#)?
**A:** A type-safe function pointer enabling callbacks and event handling.

**Code:**
```python
# Python equivalent: functions as first-class values (callbacks / callables).
def add_one(x):
    return x + 1

def apply(fn, values):
    return [fn(v) for v in values]

print(apply(add_one, [1, 2, 3]))       # [2, 3, 4]
```

## Q99: What is an event in OOP?
**A:** A notification mechanism allowing objects to signal state changes to subscribers.

**Code:**
```python
class Button:
    def __init__(self):
        self._handlers = []
    def on_click(self, handler):       # subscribe
        self._handlers.append(handler)
    def click(self):                   # fire the event -> notify subscribers
        for h in self._handlers:
            h("clicked")

btn = Button()
btn.on_click(lambda msg: print(f"[log] {msg}"))
btn.on_click(lambda msg: print(f"[ui] refresh on {msg}"))
btn.click()
# [log] clicked
# [ui] refresh on clicked
```

## Q100: How does OOP improve software maintainability?
**A:** Through modularity, reusability, encapsulation, and clear abstractions reducing complexity.

**Code:**
```python
# Modularity  -> small classes with one responsibility (Q49)
# Reusability -> inheritance & composition (Q8, Q96)
# Encapsulation -> stable public API, private internals (Q5)
# Abstractions -> depend on interfaces not concretions (Q53)

class UserPaymentHandler:              # small, focused, encapsulated module
    def __init__(self, gateway):       # abstraction injected (low coupling)
        self._gateway = gateway
    def charge(self, amount):
        return self._gateway.pay(amount)

class FakeGateway:
    def pay(self, amount): return f"charged {amount}"

print(UserPaymentHandler(FakeGateway()).charge(50))   # charged 50
```