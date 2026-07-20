# Infosys SP DSE - Common Interview Questions

> Essential technical interview questions for the interview round after coding.

---

## OOP Concepts

### Four Pillars of OOP

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

### ACID Properties

| Property | Description | Example |
|----------|-------------|---------|
| Atomicity | All or nothing - transaction either completes fully or not at all | Bank transfer: both debit and credit happen or neither does |
| Consistency | Database moves from one valid state to another | Total balance before and after transfer remains same |
| Isolation | Concurrent transactions don't interfere | Two transfers on same account don't mix |
| Durability | Committed data persists even after crash | Once transfer is confirmed, it survives system failure |

**Interview Answer:** "ACID ensures reliable transactions. Atomicity means all-or-nothing, Consistency maintains data integrity, Isolation prevents interference between concurrent transactions, and Durability ensures committed data is permanent."

### Normalization

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

### Process vs Thread

| Aspect | Process | Thread |
|--------|---------|--------|
| Definition | Program in execution | Lightweight process |
| Memory | Separate address space | Shared address space |
| Creation | Heavyweight | Lightweight |
| Communication | IPC (pipes, sockets) | Direct (shared memory) |
| Context Switch | Slow | Fast |
| Example | Chrome browser | Tabs in Chrome |

**Interview Answer:** "A process is an executing program with its own memory space. A thread is a lightweight unit within a process that shares memory with other threads. Creating threads is faster and inter-thread communication is easier."

### Deadlock

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

### OSI Model (7 Layers)

```
Layer 7: Application    - HTTP, FTP, SMTP, DNS
Layer 6: Presentation   - SSL/TLS, JPEG, ASCII
Layer 5: Session        - NetBIOS, RPC
Layer 4: Transport      - TCP, UDP
Layer 3: Network        - IP, ICMP, Router
Layer 2: Data Link      - MAC, Switch, Ethernet
Layer 1: Physical       - Cables, Hubs, Bits
```

**Interview Answer:** "OSI has 7 layers. Application layer interfaces with user, Transport ensures reliable delivery (TCP) or fast delivery (UDP), Network handles routing (IP), Data Link handles physical addressing (MAC), and Physical layer transmits bits."

### TCP vs UDP

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
