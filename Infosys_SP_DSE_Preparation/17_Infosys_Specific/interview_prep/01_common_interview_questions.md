# Infosys SP DSE - Common Interview Questions

> Essential technical interview questions for the interview round after coding.

## Interview Structure Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                  INFOSYS SP DSE INTERVIEW FLOW                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Round 1: Coding Test (2-3 hours)                                   │
│    └─ 3 problems: Easy + Medium + Hard                              │
│                                                                     │
│  Round 2: Technical Interview (30-45 mins)                         │
│    ├─ OOP Concepts (5-10 mins)                                      │
│    ├─ DBMS / SQL (5-10 mins)                                        │
│    ├─ OS Concepts (5-10 mins)                                       │
│    ├─ Computer Networks (5 mins)                                    │
│    ├─ Project Discussion (10-15 mins)                               │
│    └─ Coding Problem (5-10 mins)                                    │
│                                                                     │
│  Round 3: HR Interview (15-20 mins)                                 │
│    ├─ Resume questions                                               │
│    ├─ Behavioral questions                                           │
│    └─ Company fit questions                                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

INTERVIEW TIPS TIMELINE:
┌──────────────────────────────────────────────────────────────────┐
│  0-5 min:  Introduce yourself, be confident                      │
│  5-15 min: OOP/DBMS - give concise answers with examples        │
│  15-25 min: Project - use STAR method, technical depth          │
│  25-35 min: Coding problem - explain approach BEFORE coding     │
│  35-45 min: Ask questions about role/team                        │
└──────────────────────────────────────────────────────────────────┘
```

---

## OOP Concepts

### Four Pillars of OOP - Visual Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    FOUR PILLARS OF OOP                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. ENCAPSULATION          2. ABSTRACTION                       │
│  ┌──────────────────┐     ┌──────────────────┐                  │
│  │ ┌──────────────┐ │     │  User sees:      │                  │
│  │ │ Public       │ │     │  car.start()     │                  │
│  │ │ Protected    │ │     │  car.stop()      │                  │
│  │ │ Private      │ │     │                  │                  │
│  │ └──────────────┘ │     │  Hides:          │                  │
│  │ Data + Methods   │     │  engine details  │                  │
│  └──────────────────┘     └──────────────────┘                  │
│                                                                 │
│  3. INHERITANCE           4. POLYMORPHISM                       │
│  ┌──────────────────┐     ┌──────────────────┐                  │
│  │  Animal (base)   │     │  speak()         │                  │
│  │   ├── Dog        │     │   → Dog: "Bark"  │                  │
│  │   ├── Cat        │     │   → Cat: "Meow"  │                  │
│  │   └── Bird       │     │   → Bird: "Tweet" │                  │
│  └──────────────────┘     └──────────────────┘                  │
│                                                                 │
│  Mnemonic: E-A-I-P = "Every Awesome Programmer Implements"      │
└─────────────────────────────────────────────────────────────────┘
```

#### 1. Encapsulation
- Bundling data and methods that operate on data within a single unit (class)
- Restricting direct access to some components
- Achieved using access modifiers (public, private, protected)

```python
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance  # Private

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

    def get_balance(self):
        return self.__balance
```

**Interview Answer:** "Encapsulation is wrapping data and methods together and controlling access. Like a BankAccount class where balance is private and can only be modified through deposit/withdraw methods."

#### 2. Abstraction
- Hiding implementation details, showing only functionality
- Achieved using abstract classes and interfaces

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius * self.radius
```

**Interview Answer:** "Abstraction hides complexity. User doesn't need to know how area() is calculated, just that it returns the area."

#### 3. Inheritance
- Creating new class from existing class
- Child class inherits attributes and methods of parent

```python
class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Bark"

class Cat(Animal):
    def speak(self):
        return "Meow"
```

**Interview Answer:** "Inheritance promotes code reusability. Dog and Cat inherit from Animal and override speak(). This follows the Open-Closed principle."

#### 4. Polymorphism
- Same interface, different implementations
- Method overloading and overriding

```python
def add(a, b):
    return a + b

def add(a, b, c):
    return a + b + c

# Python uses *args for overloading
def add(*args):
    return sum(args)
```

**Interview Answer:** "Polymorphism allows objects of different types to be treated as objects of a common parent type. Like calling speak() on both Dog and Cat objects."

### Polymorphism Deep Dive

```python
class Vehicle:
    def start(self):
        return "Vehicle starting"

class Car(Vehicle):
    def start(self):
        return "Car starting with key"

class ElectricCar(Car):
    def start(self):
        return "Electric car starting silently"

# Polymorphism in action
vehicles = [Vehicle(), Car(), ElectricCar()]
for v in vehicles:
    print(v.start())  # Each calls its own version
```

### Inheritance Types

```python
# Single Inheritance
class Parent:
    pass
class Child(Parent):
    pass

# Multiple Inheritance
class Father:
    pass
class Mother:
    pass
class Child(Father, Mother):
    pass

# Multilevel Inheritance
class Grandparent:
    pass
class Parent(Grandparent):
    pass
class Child(Parent):
    pass
```

**Interview Question:** "What is the Diamond Problem?"
**Answer:** In multiple inheritance, if a class inherits from two classes that have a common parent, it creates a diamond-shaped inheritance hierarchy. Python resolves this using MRO (Method Resolution Order).

---

## DBMS Concepts

### ACID Properties - Visual with Bank Transfer Example

```
SCENARIO: Transfer ₹1000 from Account A (₹5000) to Account B (₹3000)

┌───────────────────────────────────────────────────────────────────┐
│  ATOMICITY (All or Nothing)                                       │
│  ┌──────────────────────────────────────────────┐                 │
│  │  Step 1: Debit A:  ₹5000 → ₹4000            │                 │
│  │  Step 2: Credit B: ₹3000 → ₹4000            │                 │
│  │                                               │                 │
│  │  If Step 2 fails → Step 1 is ALSO undone!    │                 │
│  │  Result: A=₹5000, B=₹3000 (original)        │                 │
│  └──────────────────────────────────────────────┘                 │
│                                                                   │
│  CONSISTENCY (Valid State)                                        │
│  Before: A + B = ₹5000 + ₹3000 = ₹8000                          │
│  After:  A + B = ₹4000 + ₹4000 = ₹8000  ← Total preserved!     │
│                                                                   │
│  ISOLATION (No Interference)                                      │
│  If C transfers ₹500 to A at same time:                           │
│  A+B transaction and C+A transaction don't mix up!                │
│                                                                   │
│  DURABILITY (Permanent)                                           │
│  Once commit → even if power fails, the transfer is saved!        │
└───────────────────────────────────────────────────────────────────┘
```

### Normalization Levels - Visual

```
UNNORMALIZED TABLE (with repeating groups):
┌───────────┬────────────────────────┐
│ StudentID │ Courses                │
├───────────┼────────────────────────┤
│ 1         │ Math, Science, English │  ← Multiple values in one cell!
│ 2         │ Math, History          │
└───────────┴────────────────────────┘

1NF (Atomic Values):
┌───────────┬─────────┐
│ StudentID │ Course  │
├───────────┼─────────┤
│ 1         │ Math    │  ← One value per cell
│ 1         │ Science │
│ 1         │ English │
│ 2         │ Math    │
│ 2         │ History │
└───────────┴─────────┘

2NF (No Partial Dependencies):
  Problem: If table has (StudentID, Course) → Grade AND DeptName
           DeptName depends only on StudentID, not on Course!
  Solution: Split into two tables

3NF (No Transitive Dependencies):
  Problem: StudentID → DeptID → DeptName
           DeptName transitively depends on StudentID
  Solution: Put DeptName in separate Departments table
```

#### 1NF (First Normal Form)
- Each column contains atomic values
- No repeating groups

```
Before 1NF:
| StudentID | Courses          |
|-----------|------------------|
| 1         | Math, Science    |

After 1NF:
| StudentID | Course  |
|-----------|---------|
| 1         | Math    |
| 1         | Science |
```

#### 2NF (Second Normal Form)
- Already in 1NF
- No partial dependencies (non-key depends on full primary key)

#### 3NF (Third Normal Form)
- Already in 2NF
- No transitive dependencies

```
Before 3NF:
| StudentID | DeptID | DeptName |
|-----------|--------|----------|
| 1         | D1     | CS       |

After 3NF:
Students: | StudentID | DeptID |
Departments: | DeptID | DeptName |
```

**Interview Answer:** "Normalization reduces redundancy. 1NF removes repeating groups, 2NF removes partial dependencies, and 3NF removes transitive dependencies."

### Joins

```python
# INNER JOIN - Only matching records
query = """
SELECT e.Name, d.DeptName
FROM Employees e
INNER JOIN Departments d ON e.DeptID = d.DeptID
"""

# LEFT JOIN - All from left, matching from right
query = """
SELECT e.Name, d.DeptName
FROM Employees e
LEFT JOIN Departments d ON e.DeptID = d.DeptID
"""

# RIGHT JOIN - All from right, matching from left
query = """
SELECT e.Name, d.DeptName
FROM Employees e
RIGHT JOIN Departments d ON e.DeptID = d.DeptID
"""

# FULL OUTER JOIN - All from both
query = """
SELECT e.Name, d.DeptName
FROM Employees e
FULL OUTER JOIN Departments d ON e.DeptID = d.DeptID
"""
```

**Interview Question:** "Difference between WHERE and HAVING?"
**Answer:** WHERE filters rows before GROUP BY, HAVING filters groups after GROUP BY. WHERE can't use aggregate functions, HAVING can.

### Indexes

```python
# Creating an index
query = "CREATE INDEX idx_emp_name ON Employees(Name)"

# Composite index
query = "CREATE INDEX idx_emp_dept ON Employees(DeptID, Name)"

# When to use indexes:
# - Columns in WHERE clause
# - Columns in JOIN conditions
# - Columns used in ORDER BY

# When NOT to use indexes:
# - Small tables
# - Columns with many NULLs
# - Columns frequently updated
```

**Interview Answer:** "Indexes speed up data retrieval but slow down writes. Use them on frequently queried columns. B-tree is most common index type."

---

## Operating System Concepts

### Process vs Thread - Visual Comparison

```
PROCESS (Heavyweight):                    THREAD (Lightweight):
┌────────────────────────┐               ┌────────────────────────┐
│     Process A          │               │      Process A         │
│ ┌─────┐ ┌─────┐       │               │ ┌─────┐ ┌─────┐       │
│ │ Th1 │ │ Th2 │       │               │ │ Th1 │ │ Th2 │       │
│ └─────┘ └─────┘       │               │ └──┬──┘ └──┬──┘       │
│     Heap, Stack        │               │    └───┬───┘          │
│     Code, Data         │               │   Shared Memory       │
└────────────────────────┘               └────────────────────────┘
     ↑ Separate Memory                        ↑ Shared Memory

COMPARISON TABLE:
┌──────────────────┬──────────────────┬──────────────────┐
│ Feature          │ Process          │ Thread            │
├──────────────────┼──────────────────┼──────────────────┤
│ Memory           │ Separate         │ Shared            │
│ Creation speed   │ Slow (heavy)     │ Fast (light)      │
│ Communication    │ IPC (slow)       │ Shared var (fast) │
│ Context switch   │ Slow             │ Fast              │
│ Crash impact     │ Only that process│ Can kill all      │
│ Example          │ Chrome browser   │ Browser tabs      │
└──────────────────┴──────────────────┴──────────────────┘
```

### Deadlock - Visual Explanation

```
DEADLOCK SCENARIO:
┌──────────────────────────────────────────────────────────┐
│                                                          │
│   Thread 1                    Thread 2                   │
│   ┌──────┐                   ┌──────┐                   │
│   │ Lock │──── wants ────→   │ Lock │                   │
│   │  A   │   Lock B          │  B   │                   │
│   └──────┘                   └──────┘                   │
│      ↑                          ↑                       │
│   Holds Lock A              Holds Lock B                 │
│   Wants Lock B              Wants Lock A                 │
│                                                          │
│   RESULT: Both waiting forever! → DEADLOCK               │
│                                                          │
│   FOUR CONDITIONS (ALL must be true):                    │
│   1. Mutual Exclusion - locks can't be shared            │
│   2. Hold and Wait - hold one, wait for another         │
│   3. No Preemption - can't forcibly take a lock         │
│   4. Circular Wait - A→B→A cycle exists                  │
│                                                          │
│   PREVENTION: Break ONE condition!                       │
│   → Always acquire locks in same order (breaks #4)      │
│   → Or use timeout (breaks #3)                           │
│   → Or use try-lock (breaks #2)                          │
└──────────────────────────────────────────────────────────┘
```

**Four Conditions (Coffman Conditions):**
1. **Mutual Exclusion:** Resources cannot be shared
2. **Hold and Wait:** Process holds resource while waiting for another
3. **No Preemption:** Resources cannot be forcibly taken
4. **Circular Wait:** Circular chain of processes waiting for resources

```python
# Deadlock Example
import threading

lock1 = threading.Lock()
lock2 = threading.Lock()

def thread1():
    lock1.acquire()
    print("Thread 1 acquired lock1")
    # Simulating work
    x = 0
    for i in range(1000000):
        x += i
    lock2.acquire()  # Waiting for lock2
    print("Thread 1 acquired lock2")
    lock2.release()
    lock1.release()

def thread2():
    lock2.acquire()
    print("Thread 2 acquired lock2")
    # Simulating work
    x = 0
    for i in range(1000000):
        x += i
    lock1.acquire()  # Waiting for lock1
    print("Thread 2 acquired lock1")
    lock1.release()
    lock2.release()

# t1 = threading.Thread(target=thread1)
# t2 = threading.Thread(target=thread2)
# t1.start()
# t2.start()
```

**Deadlock Prevention Methods:**
1. **Resource Ordering:** Always acquire locks in same order
2. **Timeout:** Release lock after timeout if can't acquire next
3. **Try-lock:** Non-blocking lock acquisition

```python
# Prevention: Always acquire lock1 before lock2
def safe_thread1():
    lock1.acquire()
    lock2.acquire()
    # Do work
    lock2.release()
    lock1.release()
```

### Synchronization

```python
import threading

# Semaphore - Limits concurrent access
semaphore = threading.Semaphore(3)  # Max 3 threads

def limited_access():
    semaphore.acquire()
    # Only 3 threads can be here at once
    print(f"Thread {threading.current_thread().name} accessing")
    semaphore.release()

# Mutex - Mutual exclusion
mutex = threading.Lock()

def critical_section():
    mutex.acquire()
    # Only one thread at a time
    shared_resource += 1
    mutex.release()

# Event - Thread communication
event = threading.Event()

def waiter():
    print("Waiting for event...")
    event.wait()
    print("Event occurred!")

def setter():
    event.set()  # Signal waiting threads
```

---

## Computer Networks

### OSI Model (7 Layers) - Visual

```
┌─────────────────────────────────────────────────────────────────┐
│  Layer 7: Application     │  HTTP, FTP, SMTP, DNS    │ User    │
│  Layer 6: Presentation    │  SSL/TLS, JPEG, ASCII    │ Layer   │
│  Layer 5: Session         │  NetBIOS, RPC             │         │
│  Layer 4: Transport       │  TCP, UDP                 │ Data    │
│  Layer 3: Network         │  IP, ICMP, Router         │ Flow    │
│  Layer 2: Data Link       │  MAC, Switch, Ethernet    │         │
│  Layer 1: Physical        │  Cables, Hubs, Bits       │ Media   │
└─────────────────────────────────────────────────────────────────┘

MNEMONIC: "All People Seem To Need Data Processing"
          (Layer 7 → Layer 1, top to bottom)

DATA FLOW:
  Sending: Data → L7 → L6 → L5 → L4 → L3 → L2 → L1 → Wire
  Receiving: Wire → L1 → L2 → L3 → L4 → L5 → L6 → L7 → Data
```

### TCP vs UDP - Visual Comparison

```
TCP (Reliable):                    UDP (Fast):
┌──────────────────────┐         ┌──────────────────────┐
│  A → SYN → B         │         │  A → DATA → B        │
│  A ← SYN-ACK ← B    │         │  (no handshake!)     │
│  A → ACK → B         │         │                      │
│  A → DATA → B        │         │  Lost packets?       │
│  A ← ACK ← B         │         │  Too bad, not ressent│
│  (guaranteed!)       │         │  (just send!)        │
└──────────────────────┘         └──────────────────────┘
  Use for: Web, Email              Use for: Video, Games
  Speed: Slower                    Speed: Faster
  Order: Guaranteed                Order: Not guaranteed
```

### TCP Three-Way Handshake - Visual

```
CLIENT                          SERVER
  │                               │
  │──── SYN (seq=x) ───────────→│    "I want to connect"
  │                               │
  │←─── SYN-ACK (seq=y,ack=x+1)──│    "OK, I acknowledge"
  │                               │
  │──── ACK (ack=y+1) ─────────→│    "Connection established!"
  │                               │
  │←═══════ DATA TRANSFER ═══════→│
  
  Total: 3 steps to establish, then data flows bidirectionally
```

| Feature | TCP | UDP |
|---------|-----|-----|
| Connection | Connection-oriented | Connectionless |
| Reliability | Guaranteed delivery | No guarantee |
| Ordering | Ordered | Unordered |
| Speed | Slower | Faster |
| Header Size | 20 bytes | 8 bytes |
| Flow Control | Yes | No |
| Use Cases | Web, Email, File Transfer | Streaming, Gaming, DNS |

**Interview Answer:** "TCP is reliable and ordered but slower. UDP is faster but unreliable. TCP is used for HTTP, while UDP is used for video streaming where speed matters more than perfect delivery."

### HTTP Methods

| Method | Purpose | Body | Safe | Idempotent |
|--------|---------|------|------|------------|
| GET | Retrieve | No | Yes | Yes |
| POST | Create | Yes | No | No |
| PUT | Update/Replace | Yes | No | Yes |
| PATCH | Partial Update | Yes | No | No |
| DELETE | Remove | No | Yes | Yes |

**Interview Answer:** "GET retrieves data, POST creates new resources, PUT updates entire resource, PATCH updates partial resource, DELETE removes resource. GET is safe and idempotent, POST is neither."

### TCP Three-Way Handshake

```
Client → Server: SYN (I want to connect)
Server → Client: SYN-ACK (I acknowledge)
Client → Server: ACK (Connection established)
```

**Interview Answer:** "TCP uses three-way handshake: client sends SYN, server responds with SYN-ACK, client confirms with ACK. This ensures both sides are ready for data transmission."

---

## Project Discussion Tips

### STAR Method for Project Questions

**S**ituation: Context of the project
**T**ask: Your specific role and responsibilities
**A**ction: What you did (technical decisions, challenges)
**R**esult: Impact and outcomes

### Common Project Questions

1. **"Tell me about your project"**
   - Keep it under 2 minutes
   - Focus on technical aspects
   - Mention technologies used

2. **"What was the most challenging part?"**
   - Pick a real technical challenge
   - Explain your problem-solving approach
   - Show learning and growth

3. **"Why did you choose this technology?"**
   - Compare with alternatives
   - Mention specific advantages
   - Show you made informed decisions

4. **"What would you do differently?"**
   - Show self-awareness
   - Mention what you learned
   - Be honest about limitations

### Technical Project Deep Dive

```python
# Be ready to explain:
# 1. Architecture decisions
# 2. Database schema design
# 3. API design choices
# 4. Performance optimizations
# 5. Testing strategies
# 6. Deployment process

# Example explanation structure:
"""
My project is a [type] application that [purpose].
I used [tech stack] because [reasons].
The architecture follows [pattern] pattern.
Key features include [2-3 features].
The most challenging part was [challenge], which I solved by [solution].
"""
```

---

## Resume-Based Questions

### Technical Resume Questions

1. **"Explain this project from your resume"**
   - Be ready to discuss any project in detail
   - Know the technical decisions you made
   - Be honest about what you didn't do

2. **"What does this technology do?"**
   - Don't list technologies you can't explain
   - Focus on technologies you're comfortable with
   - Show depth over breadth

3. **"Why did you use [technology]?"**
   - Have clear reasons for tech choices
   - Compare with alternatives
   - Mention trade-offs

### Behavioral Resume Questions

1. **"Tell me about a time you worked in a team"**
   - Use STAR method
   - Show collaboration skills
   - Mention specific contributions

2. **"Describe a difficult bug you fixed"**
   - Explain debugging process
   - Show persistence
   - Mention what you learned

3. **"How do you handle deadlines?"**
   - Give specific example
   - Show prioritization skills
   - Mention communication

### Tips for Resume Discussion

```python
# Do's:
# - Be honest about your role
# - Know every technology on your resume
# - Be ready to explain technical decisions
# - Show enthusiasm for your work
# - Mention specific achievements

# Don'ts:
# - Don't exaggerate your contributions
# - Don't list technologies you don't know
# - Don't give vague answers
# - Don't speak negatively about previous teams
# - Don't rush through answers
```

---

## Quick Reference: Top 10 Interview Questions

| # | Question | Key Points |
|---|----------|------------|
| 1 | Explain OOP pillars | Encapsulation, Abstraction, Inheritance, Polymorphism with examples |
| 2 | Difference between SQL and NoSQL | Schema, Scaling, ACID, Use cases |
| 3 | Explain deadlock | 4 conditions, prevention, detection |
| 4 | TCP vs UDP | Connection, Reliability, Speed, Use cases |
| 5 | Normalization | 1NF, 2NF, 3NF with examples |
| 6 | Process vs Thread | Memory, Creation speed, Communication |
| 7 | Explain your project | STAR method, Technical decisions, Challenges |
| 8 | REST API design | Methods, Status codes, Best practices |
| 9 | Git workflow | Branching, Merging, Pull requests |
| 10 | System design basics | Scalability, Caching, Load balancing |

---

## Infosys-Specific Interview Tips

1. **Know Infosys:** Company history, services, recent projects
2. **Be Confident:** Even if you don't know, explain your thinking
3. **Ask Questions:** Show interest in the role and team
4. **Communication:** Clear and concise answers
5. **Honesty:** Admit what you don't know, but show willingness to learn

> **Remember:** The interview is not just about technical skills. It's about how you communicate, solve problems, and fit into the team.
