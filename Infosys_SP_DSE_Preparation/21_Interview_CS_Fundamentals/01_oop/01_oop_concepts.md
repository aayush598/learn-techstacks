# OOP Concepts for Infosys SP DSE Interview

## Table of Contents
1. [4 Pillars of OOP](#4-pillars-of-oop)
2. [Abstract Classes in Python](#abstract-classes-in-python)
3. [Multiple Inheritance and MRO](#multiple-inheritance-and-mro)
4. [Design Patterns](#design-patterns)
5. [SOLID Principles](#solid-principles)
6. [Common Interview Questions](#common-interview-questions)
7. [Python-Specific OOP](#python-specific-oop)

---

## 4 Pillars of OOP

### 1. Encapsulation
Bundling data (attributes) and methods that operate on that data into a single unit (class), and restricting direct access to some components.

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner          # public
        self._balance = balance     # protected (convention)
        self.__pin = 1234           # private (name mangling)

    @property
    def balance(self):
        """Getter - controlled access to private data"""
        return self._balance

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            return True
        return False

    def verify_pin(self, pin):
        return self.__pin == pin

acc = BankAccount("Alice", 1000)
print(acc.balance)        # 1000 (via getter)
acc.deposit(500)
print(acc.balance)        # 1500
# print(acc.__pin)        # AttributeError
print(acc._BankAccount__pin)  # 1234 (name mangling)
```

### 2. Inheritance
A class (child) can inherit attributes and methods from another class (parent).

```python
class Animal:
    def __init__(self, name, sound):
        self.name = name
        self.sound = sound

    def speak(self):
        return f"{self.name} says {self.sound}"

    def __str__(self):
        return f"Animal({self.name})"

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name, sound="Woof")
        self.breed = breed

    def fetch(self, item):
        return f"{self.name} fetches the {item}"

class Cat(Animal):
    def __init__(self, name, indoor=True):
        super().__init__(name, sound="Meow")
        self.indoor = indoor

    def speak(self):  # Method overriding
        return f"{self.name} purrs softly"

dog = Dog("Rex", "German Shepherd")
cat = Cat("Whiskers")

print(dog.speak())        # Rex says Woof
print(dog.fetch("ball"))  # Rex fetches the ball
print(cat.speak())        # Whiskers purrs softly
print(isinstance(dog, Animal))  # True
print(isinstance(cat, Dog))     # False
```

### 3. Polymorphism
Same interface, different implementations. Objects of different classes can be treated as objects of a common superclass.

```python
class Shape:
    def area(self):
        raise NotImplementedError

    def describe(self):
        return f"{self.__class__.__name__} with area {self.area():.2f}"

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height

# Polymorphism in action
shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 8)]

for shape in shapes:
    print(shape.describe())  # Same method call, different behavior

# Output:
# Circle with area 78.54
# Rectangle with area 24.00
# Triangle with area 12.00
```

### 4. Abstraction
Hiding complex implementation details and showing only the essential features.

```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    """Abstract class - cannot be instantiated"""

    @abstractmethod
    def authenticate(self):
        pass

    @abstractmethod
    def process_payment(self, amount):
        pass

    def make_payment(self, amount):
        """Template method - uses abstract methods"""
        if self.authenticate():
            result = self.process_payment(amount)
            print(f"Payment of ${amount:.2f} processed: {result}")
            return True
        print("Authentication failed")
        return False

class CreditCardProcessor(PaymentProcessor):
    def __init__(self, card_number):
        self.card_number = card_number

    def authenticate(self):
        return len(self.card_number) == 16

    def process_payment(self, amount):
        return f"Charged ${amount:.2f} to card ending in {self.card_number[-4:]}"

class UPIProcessor(PaymentProcessor):
    def __init__(self, upi_id):
        self.upi_id = upi_id

    def authenticate(self):
        return "@" in self.upi_id

    def process_payment(self, amount):
        return f"Paid ${amount:.2f} via UPI ({self.upi_id})"

# processor = PaymentProcessor()  # TypeError: Can't instantiate abstract class
CreditCardProcessor("1234567812345678").make_payment(99.99)
UPIProcessor("user@upi").make_payment(49.99)
```

---

## Abstract Classes in Python

```python
from abc import ABC, abstractmethod, abstractproperty

class Database(ABC):
    """Abstract base class for database operations"""

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def execute(self, query):
        pass

    @abstractmethod
    def close(self):
        pass

    def __init_subclass__(cls, **kwargs):
        """Hook called when a subclass is created"""
        super().__init_subclass__(**kwargs)
        print(f"Database subclass created: {cls.__name__}")

class MySQL(Database):
    def connect(self):
        print("Connecting to MySQL...")

    def execute(self, query):
        print(f"MySQL executing: {query}")

    def close(self):
        print("MySQL connection closed")

# __init_subclass__ hook is called
# Database subclass created: MySQL

mysql = MySQL()
mysql.connect()     # Connecting to MySQL...
mysql.execute("SELECT * FROM users")
mysql.close()       # MySQL connection closed
```

---

## Multiple Inheritance and MRO

```python
class A:
    def greet(self):
        return "Hello from A"

    def class_name(self):
        return "Class A"

class B(A):
    def greet(self):
        return "Hello from B"

class C(A):
    def greet(self):
        return "Hello from C"

class D(B, C):
    pass

d = D()
print(d.greet())           # Hello from B (MRO: D -> B -> C -> A)
print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
print(D.mro())
# [<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>]

# MRO uses C3 Linearization algorithm
# Rule: D -> B -> C -> A -> object
# Children before parents, left before right
```

### Real-world Multiple Inheritance Example

```python
class Logger:
    def log(self, message):
        print(f"[LOG] {message}")

class Serializer:
    def serialize(self, data):
        import json
        return json.dumps(data)

class CacheManager:
    def cache_set(self, key, value):
        print(f"Cache SET: {key} = {value}")

class APIService(Logger, Serializer, CacheManager):
    def __init__(self, name):
        self.name = name

    def handle_request(self, endpoint, data):
        self.log(f"Request to {endpoint}")
        serialized = self.serialize(data)
        self.cache_set(endpoint, serialized)
        return serialized

service = APIService("MainAPI")
result = service.handle_request("/users", {"id": 1, "name": "Alice"})
# [LOG] Request to /users
# Cache SET: /users = {"id": 1, "name": "Alice"}
```

---

## Design Patterns

### 1. Singleton Pattern
Ensure a class has only one instance.

```python
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, value=None):
        if not self._initialized:
            self.value = value
            self._initialized = True

s1 = Singleton("first")
s2 = Singleton("second")

print(s1 is s2)          # True
print(s1.value)          # first (not second - __init__ not called again)
print(s2.value)          # first
```

### 2. Factory Pattern
Create objects without specifying exact class.

```python
from abc import ABC, abstractmethod

class Notification(ABC):
    @abstractmethod
    def send(self, message):
        pass

class EmailNotification(Notification):
    def __init__(self, email):
        self.email = email

    def send(self, message):
        print(f"Email to {self.email}: {message}")

class SMSNotification(Notification):
    def __init__(self, phone):
        self.phone = phone

    def send(self, message):
        print(f"SMS to {self.phone}: {message}")

class PushNotification(Notification):
    def __init__(self, device_id):
        self.device_id = device_id

    def send(self, message):
        print(f"Push to {self.device_id}: {message}")

class NotificationFactory:
    @staticmethod
    def create(notification_type, **kwargs):
        if notification_type == "email":
            return EmailNotification(kwargs["email"])
        elif notification_type == "sms":
            return SMSNotification(kwargs["phone"])
        elif notification_type == "push":
            return PushNotification(kwargs["device_id"])
        raise ValueError(f"Unknown type: {notification_type}")

# Usage
notification = NotificationFactory.create("email", email="user@example.com")
notification.send("Hello!")
```

### 3. Observer Pattern
Define a one-to-many dependency so when one object changes state, all dependents are notified.

```python
class Subject:
    def __init__(self):
        self._observers = []
        self._state = None

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self._state)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
        self.notify()

class Observer:
    def __init__(self, name):
        self.name = name

    def update(self, state):
        print(f"{self.name} received update: {state}")

# Usage
subject = Subject()
obs1 = Observer("Observer1")
obs2 = Observer("Observer2")

subject.attach(obs1)
subject.attach(obs2)

subject.state = "New Data"  # Both observers notified
# Observer1 received update: New Data
# Observer2 received update: New Data

subject.detach(obs1)
subject.state = "Changed Data"  # Only obs2 notified
# Observer2 received update: Changed Data
```

---

## SOLID Principles

### S - Single Responsibility Principle
A class should have only one reason to change.

```python
# Bad: One class doing everything
class UserManager:
    def create_user(self, user_data):
        pass
    def send_email(self, email, message):
        pass
    def generate_report(self, data):
        pass

# Good: Separate responsibilities
class UserService:
    def create_user(self, user_data):
        pass

class EmailService:
    def send_email(self, email, message):
        pass

class ReportGenerator:
    def generate_report(self, data):
        pass
```

### O - Open/Closed Principle
Open for extension, closed for modification.

```python
class DiscountCalculator:
    def calculate(self, customer_type, amount):
        if customer_type == "regular":
            return amount * 0.1
        elif customer_type == "premium":
            return amount * 0.2
        elif customer_type == "vip":
            return amount * 0.3

# Better: Open for extension
class DiscountStrategy:
    def calculate(self, amount):
        raise NotImplementedError

class RegularDiscount(DiscountStrategy):
    def calculate(self, amount):
        return amount * 0.1

class PremiumDiscount(DiscountStrategy):
    def calculate(self, amount):
        return amount * 0.2

class VIPDiscount(DiscountStrategy):
    def calculate(self, amount):
        return amount * 0.3

class DiscountCalculator:
    def __init__(self, strategy: DiscountStrategy):
        self.strategy = strategy

    def calculate(self, amount):
        return self.strategy.calculate(amount)
```

### L - Liskov Substitution Principle
Subtypes must be substitutable for their base types.

```python
class Bird:
    def move(self):
        return "Moving"

class FlyingBird(Bird):
    def move(self):
        return "Flying"

class Penguin(Bird):
    def move(self):
        return "Swimming"  # Still valid - penguin is a bird that swims
```

### I - Interface Segregation Principle
No client should be forced to depend on methods it doesn't use.

```python
# Bad
class Worker:
    def work(self):
        pass
    def eat(self):
        pass
    def sleep(self):
        pass

# Good
class Workable:
    def work(self):
        pass

class Eatable:
    def eat(self):
        pass

class Sleepable:
    def sleep(self):
        pass

class Robot(Workable):
    def work(self):
        return "Robot working"

class Human(Workable, Eatable, Sleepable):
    def work(self):
        return "Human working"
    def eat(self):
        return "Human eating"
    def sleep(self):
        return "Human sleeping"
```

### D - Dependency Inversion Principle
Depend on abstractions, not concretions.

```python
from abc import ABC, abstractmethod

class MessageSender(ABC):
    @abstractmethod
    def send(self, message):
        pass

class EmailSender(MessageSender):
    def send(self, message):
        print(f"Email: {message}")

class SMSSender(MessageSender):
    def send(self, message):
        print(f"SMS: {message}")

class NotificationService:
    def __init__(self, sender: MessageSender):
        self.sender = sender

    def notify(self, message):
        self.sender.send(message)

# High-level module depends on abstraction
service = NotificationService(EmailSender())
service.notify("Hello")
```

---

## Common Interview Questions with Answers

### Q1: Difference between Abstract Class and Interface?

| Feature | Abstract Class | Interface |
|---------|---------------|-----------|
| Methods | Can have abstract + concrete methods | Only abstract methods (Python) |
| Variables | Can have instance variables | No instance variables (typically) |
| Constructor | Can have | Cannot have |
| Multiple Inheritance | Yes | Yes (in Python, ABC is just a class) |
| Implementation | Can provide partial implementation | Cannot provide implementation |

```python
# Abstract class
from abc import ABC, abstractmethod

class Vehicle(ABC):
    def __init__(self, brand):
        self.brand = brand  # instance variable

    @abstractmethod
    def start(self):
        pass

    def honk(self):  # concrete method
        return "Beep!"

# Interface (just a convention in Python, enforced by ABC)
class Drivable(ABC):
    @abstractmethod
    def drive(self):
        pass

class Car(Vehicle, Drivable):
    def start(self):
        return f"{self.brand} starting..."

    def drive(self):
        return "Driving on road"
```

### Q2: Method Overloading vs Overriding

```python
# Method Overloading (same name, different parameters)
# Python doesn't support true overloading - uses default args
class Calculator:
    def add(self, a, b=0, c=0):
        return a + b + c

calc = Calculator()
print(calc.add(5))       # 5
print(calc.add(5, 3))    # 8
print(calc.add(5, 3, 2)) # 10

# Method Overriding (child redefines parent's method)
class Parent:
    def greet(self):
        return "Hello from Parent"

class Child(Parent):
    def greet(self):  # Overrides Parent.greet
        return "Hello from Child"

child = Child()
print(child.greet())  # Hello from Child
```

### Q3: Diamond Problem

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

# Python resolves using MRO (C3 Linearization)
print(D().method())  # B (follows D -> B -> C -> A order)
print(D.__mro__)     # Shows exact resolution order
```

### Q4: Shallow vs Deep Copy

```python
import copy

original = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# Shallow copy - new outer list, same inner objects
shallow = copy.copy(original)
shallow[0][0] = 999
print(original[0][0])  # 999 (changed! inner list is shared)

# Deep copy - completely independent
original = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
deep = copy.deepcopy(original)
deep[0][0] = 999
print(original[0][0])  # 1 (unchanged)

# Other ways to shallow copy
list2 = original.copy()
list3 = original[:]
list4 = list(original)
```

### Q5: Garbage Collection in Python

```python
import gc

# Python uses reference counting + generational garbage collector
import sys

a = [1, 2, 3]
print(sys.getrefcount(a))  # 2 (a + getrefcount argument)

b = a  # refcount increases
print(sys.getrefcount(a))  # 3

del b  # refcount decreases
print(sys.getrefcount(a))  # 2

# Circular references need GC
class Node:
    def __init__(self):
        self.ref = None

n1 = Node()
n2 = Node()
n1.ref = n2  # circular reference
n2.ref = n1

del n1
del n2  # refcount never reaches 0, but GC detects cycle

# Force garbage collection
gc.collect()

# GC generations: 0 (youngest), 1, 2 (oldest)
print(gc.get_threshold())  # (700, 10, 10)
print(gc.get_count())      # objects in each generation
```

---

## Python-Specific OOP

### `__str__` and `__repr__`

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        """Human-readable string (for print, str())"""
        return f"({self.x}, {self.y})"

    def __repr__(self):
        """Developer string (for debugging, repr())"""
        return f"Point(x={self.x}, y={self.y})"

p = Point(3, 4)
print(str(p))    # (3, 4) - uses __str__
print(repr(p))   # Point(x=3, y=4) - uses __repr__
print(p)          # (3, 4)
print([p])        # [Point(x=3, y=4)] - list uses __repr__
```

### `__eq__` and `__hash__`

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

p1 = Point(1, 2)
p2 = Point(1, 2)
p3 = Point(3, 4)

print(p1 == p2)          # True
print(p1 == p3)          # False
print(hash(p1) == hash(p2))  # True (must be equal if __eq__ returns True)

# Can now use in sets and dicts
points = {p1, p2, p3}
print(len(points))       # 2 (p1 and p2 are equal)

# Sorting works with __lt__
points_list = [p3, p1, Point(0, 5)]
print(sorted(points_list))  # [Point(x=0, y=5), Point(x=1, y=2), Point(x=3, y=4)]
```

### Properties and Descriptors

```python
class ValidatedAttribute:
    def __init__(self, min_val=None, max_val=None):
        self.min_val = min_val
        self.max_val = max_val

    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value):
        if self.min_val is not None and value < self.min_val:
            raise ValueError(f"{self.name} must be >= {self.min_val}")
        if self.max_val is not None and value > self.max_val:
            raise ValueError(f"{self.name} must be <= {self.max_val}")
        setattr(obj, self.private_name, value)

class Student:
    age = ValidatedAttribute(min_val=0, max_val=150)
    grade = ValidatedAttribute(min_val=0, max_val=100)

    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade

s = Student("Alice", 20, 95)
print(s.age)       # 20

try:
    s.age = -5     # ValueError: age must be >= 0
except ValueError as e:
    print(e)

try:
    s.grade = 150  # ValueError: grade must be <= 100
except ValueError as e:
    print(e)
```

### Metaclasses (Concept)

```python
# Metaclass is a class of a class
# type is the default metaclass in Python

class Meta(type):
    """Custom metaclass"""
    def __new__(mcs, name, bases, namespace):
        # Add a class attribute to all classes using this metaclass
        namespace['class_id'] = name.lower()
        return super().__new__(mcs, name, bases, namespace)

class MyClass(metaclass=Meta):
    pass

class AnotherClass(metaclass=Meta):
    pass

print(MyClass.class_id)       # myclass
print(AnotherClass.class_id)  # anotherclass

# Real use case: Django ORM
# class User(models.Model):
#     name = models.CharField(max_length=100)
#     # metaclass handles field registration, table creation, etc.
```

---

## Real-World Analogies for OOP Concepts

```
╔══════════════════════════════════════════════════════════════════╗
║               OOP CONCEPT -> REAL WORLD ANALOGY                ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                ║
║  ENCAPSULATION = ATM Machine                                   ║
║  - You see buttons (public interface)                          ║
║  - Internal wiring is hidden (private)                         ║
║  - You can't bypass the screen to access money directly        ║
║                                                                ║
║  INHERITANCE = Family Traits                                   ║
║  - Child inherits eye color, height from parents               ║
║  - Child can also have unique traits (own methods)             ║
║  - Dog inherits from Animal, adds breed-specific behavior      ║
║                                                                ║
║  POLYMORPHISM = Remote Control                                 ║
║  - Same "power" button turns on TV, AC, or fan                ║
║  - Same method name, different behavior per device             ║
║                                                                ║
║  ABSTRACTION = Car Driving                                     ║
║  - You use steering wheel and pedals (interface)               ║
║  - You don't need to know engine internals (implementation)   ║
║                                                                ║
║  SINGLETON = President of a Country                            ║
║  - Only ONE instance can exist at a time                       ║
║  - Everyone refers to the same president                       ║
║                                                                ║
║  FACTORY = Car Factory                                         ║
║  - You request a "car" and get Sedan, SUV, or Truck           ║
║  - Factory decides which specific class to create              ║
║                                                                ║
║  OBSERVER = YouTube Subscriptions                              ║
║  - You subscribe (attach) to a channel                         ║
║  - New video uploaded -> all subscribers get notified          ║
║  - You unsubscribe (detach) anytime                            ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## Visual: Inheritance Hierarchy

```
                    ┌──────────┐
                    │  Object  │  (base of everything in Python)
                    └────┬─────┘
                         │
                    ┌────┴─────┐
                    │  Animal  │  (has: name, sound, speak())
                    └────┬─────┘
                 ┌───────┴───────┐
            ┌────┴────┐     ┌────┴────┐
            │   Dog   │     │   Cat   │
            │ (breed) │     │ (indoor)│
            │ fetch() │     │ purr()  │
            └─────────┘     └─────────┘
                 │
            ┌────┴────┐
            │  Puppy  │  (inherits from Dog)
            └─────────┘

Method Resolution Order (MRO):
Puppy.mro() = [Puppy, Dog, Animal, object]
When calling speak(), Python checks:
1. Puppy -> not found
2. Dog -> not found
3. Animal -> found! Uses Animal.speak()
```

---

## Visual: Polymorphism in Action

```
Same method name, different behavior per class:

  shapes = [Circle(5), Rectangle(4,6), Triangle(3,8)]

  shape.describe() calls:
  ┌─────────────────────────────────────────────────┐
  │  shape is Circle?     -> area = pi*r^2 = 78.54  │
  │  shape is Rectangle?  -> area = w*h = 24.00      │
  │  shape is Triangle?   -> area = 0.5*b*h = 12.00  │
  └─────────────────────────────────────────────────┘

  The SAME for loop works for ALL shapes!
  No if/else checking type - that's polymorphism!
```

---

## Visual: Encapsulation Access Levels

```
┌─────────────────────────────────────────────────────┐
│                 BankAccount Class                    │
├─────────────────────────────────────────────────────┤
│ PUBLIC (self.owner)     -> Anyone can access        │
│   owner = "Alice"       -> acc.owner works          │
│                                                     │
│ PROTECTED (self._pin)   -> Class + subclasses       │
│   _pin = 1234           -> acc._pin works (by conv) │
│                                                     │
│ PRIVATE (self.__secret) -> Only this class          │
│   __secret = "xyz"      -> acc.__secret FAILS!      │
│                             Need: acc._Bank__secret  │
│                                                     │
│ PROPERTY (@property)    -> Controlled access        │
│   acc.balance            -> Getter (read-only)      │
│   acc.balance = 1000     -> Setter (with validation)│
└─────────────────────────────────────────────────────┘
```

---

## Design Patterns Visual Guide

### Singleton Pattern

```
Normal Class:                Singleton:
  obj1 = A()                  obj1 = A()
  obj2 = A()                  obj2 = A()
  obj1 != obj2                obj1 is obj2  (same object!)

Memory:
┌──────────┐                ┌──────────┐
│  obj1    │                │  obj1    │
│  [A] ────┼──> obj1 data   │  [A] ────┼──> ONE copy
└──────────┘                │          │
┌──────────┐                │  obj2 ───┼──> (same!)
│  obj2    │                └──────────┘
│  [A] ────┼──> obj2 data
└──────────┘
```

### Factory Pattern

```
Client Code                    Factory
─────────────                  ──────────────
notification =                 NotificationFactory.create("email")
  Factory.create("email")        ├──> EmailNotification
  Factory.create("sms")          ├──> SMSNotification
  Factory.create("push")         └──> PushNotification

Client doesn't know which class it gets!
Just says "give me a notification of type X"
```

### Observer Pattern

```
          ┌──────────┐
          │ Subject  │
          │ (Stock)  │
          └────┬─────┘
               │ notify()
       ┌───────┼───────┐
       ▼       ▼       ▼
  ┌────────┐┌────────┐┌────────┐
  │Observer││Observer││Observer│
  │ (Email)││ (SMS)  ││ (Push) │
  └────────┘└────────┘└────────┘

When stock price changes:
1. Subject.price = 150
2. Subject calls notify() on ALL observers
3. Each observer reacts independently
```

---

## MRO (Method Resolution Order) Deep Dive

```
Diamond Problem:

        ┌─────────┐
        │    A    │
        └────┬────┘
         ┌───┴───┐
    ┌────┴──┐ ┌──┴────┐
    │   B   │ │   C   │
    └───┬───┘ └───┬───┘
        └────┬────┘
        ┌────┴────┐
        │    D    │
        └─────────┘

D.__mro__ = (D, B, C, A, object)

C3 Linearization Rules:
1. Children before parents
2. Left before right (in class definition)
3. Preserves local precedence order

Python code:
class D(B, C): pass
# MRO: D -> B -> C -> A -> object
# Not D -> B -> A -> C -> A (no duplication!)
```

---

## Common Interview Questions (Extended)

### Q6: Explain the diamond problem and how Python resolves it.

**Answer:** Diamond problem occurs when a class inherits from two classes that share a common parent.

```
        ┌─────┐
        │  A  │  <- has method()
        └──┬──┘
       ┌───┴───┐
   ┌───┴──┐ ┌──┴───┐
   │  B   │ │  C   │  <- both override method()
   └──┬───┘ └──┬───┘
      └───┬────┘
      ┌───┴───┐
      │   D   │  <- which method() does D call?
      └───────┘

Python resolves with MRO (C3 Linearization):
D.mro() = [D, B, C, A, object]

So D().method() calls B.method() (left parent first)
```

### Q7: What is the Liskov Substitution Principle?

**Answer:** Subtypes must be substitutable for their base types without breaking the program.

```python
# BAD Example (violates LSP):
class Bird:
    def fly(self):
        return "Flying"

class Penguin(Bird):
    def fly(self):
        raise Exception("Penguins can't fly!")  # Breaks expectation!

# If code expects Bird.fly() to work, Penguin breaks it.

# GOOD Example:
class Bird:
    def move(self):
        return "Moving"

class FlyingBird(Bird):
    def move(self):
        return "Flying"

class Penguin(Bird):
    def move(self):
        return "Swimming"  # Still valid - penguin moves, just differently
```

### Q8: Explain Shallow vs Deep Copy with a diagram.

```
Original List: [[1,2,3], [4,5,6]]

Shallow Copy:
  shallow = copy.copy(original)
  ┌──────────────┐     ┌──────────────┐
  │ shallow list │     │original list │
  │  [0] ────────┼─────┼──> [1,2,3]  │  <- SAME inner list!
  │  [1] ────────┼─────┼──> [4,5,6]  │  <- SAME inner list!
  └──────────────┘     └──────────────┘
  Changing shallow[0][0] = 999 affects original too!

Deep Copy:
  deep = copy.deepcopy(original)
  ┌──────────────┐
  │ deep list    │
  │  [0] ────────┼──> [1,2,3]  (NEW copy)
  │  [1] ────────┼──> [4,5,6]  (NEW copy)
  └──────────────┘
  ┌──────────────┐
  │original list │
  │  [0] ────────┼──> [1,2,3]  (separate)
  │  [1] ────────┼──> [4,5,6]  (separate)
  └──────────────┘
  Changing deep[0][0] = 999 does NOT affect original!
```

### Q9: What is the difference between `__str__` and `__repr__`?

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        """Human-readable: for print(), str(), f-strings"""
        return f"({self.x}, {self.y})"

    def __repr__(self):
        """Developer string: for debugging, repr(), containers"""
        return f"Point(x={self.x}, y={self.y})"

p = Point(3, 4)

print(str(p))     # (3, 4)       <- uses __str__
print(repr(p))    # Point(x=3, y=4) <- uses __repr__
print(p)          # (3, 4)       <- uses __str__
print([p])        # [Point(x=3, y=4)] <- list uses __repr__

Rule of thumb:
- __str__: focus on readability
- __repr__: focus on unambiguous representation
```

---

## Quick Reference Cheat Sheet

| Concept | Key Points |
|---------|-----------|
| Encapsulation | Data hiding, `__private`, `@property` |
| Inheritance | `class Child(Parent)`, `super()` |
| Polymorphism | Same interface, different behavior |
| Abstraction | ABC, `@abstractmethod` |
| MRO | C3 Linearization, `__mro__` attribute |
| Singleton | `__new__` override, one instance |
| Factory | Create objects without specifying class |
| Observer | One-to-many dependency notification |
| Shallow Copy | `copy.copy()`, shared inner objects |
| Deep Copy | `copy.deepcopy()`, fully independent |
| `__str__` | Human-readable (print) |
| `__repr__` | Developer string (debugging) |
| `__eq__` | Custom equality comparison |
| `__hash__` | Required if objects used in sets/dicts |
| LSP | Subtypes must be substitutable for base types |
| Diamond | Two parents share common ancestor; resolved by MRO |
