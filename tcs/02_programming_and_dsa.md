# Programming and Data Structures (Python, C++, JS)

**Q1. You know Python, C++, and JavaScript. How do you choose which language to use for a project?**
**Answer:** 
- **Python:** I use Python for AI/ML tasks, data processing, and rapid backend development (FastAPI). Its rich ecosystem (Pandas, TensorFlow, LangChain) makes it unbeatable for AI.
- **JavaScript/TypeScript:** I choose JS/TS for web-centric frontend and full-stack applications (React, Next.js, Express) because it runs natively in the browser and provides excellent asynchronous event-driven capabilities via Node.js.
- **C++:** I use C++ when performance, memory management, and low-level system control are critical, such as in competitive programming or core system development.

**Q2. Explain the Global Interpreter Lock (GIL) in Python.**
**Answer:** The GIL is a mutex that protects access to Python objects, preventing multiple threads from executing Python bytecodes at once. This makes standard CPython thread-safe but effectively means that multi-threading in Python is not suitable for CPU-bound tasks. To bypass this for heavy computations, we use the `multiprocessing` module. However, for I/O bound tasks, Python's multi-threading or `asyncio` works perfectly.

**Q3. What is the difference between a `list` and a `tuple` in Python?**
**Answer:** Lists are mutable, meaning their contents can be changed after creation (append, remove). They use square brackets `[]`. Tuples are immutable, meaning once created, they cannot be changed. They use parentheses `()`. Because of immutability, tuples are generally faster, more memory-efficient, and can be used as keys in dictionaries.

**Q4. How does JavaScript handle asynchronous operations? What is the Event Loop?**
**Answer:** JavaScript is single-threaded but uses an Event Loop to handle asynchronous operations. When an async operation (like an API call) is made, it is handed off to the Web APIs (or C++ APIs in Node). Once complete, the callback is pushed to the Task Queue (or Microtask Queue for Promises). The Event Loop constantly checks if the Call Stack is empty; if it is, it pushes tasks from the queues onto the stack. This non-blocking behavior allows JS to handle many I/O operations concurrently.

**Q5. In C++, difference between pointers and references?**
**Answer:** 
- A pointer is a variable that holds a memory address. It can be reassigned to point to different addresses, can point to `null`, and requires dereferencing (`*`) to access the value.
- A reference is an alias for an existing variable. It must be initialized when created, cannot point to `null`, cannot be reassigned to alias another variable, and shares the same memory address as the original variable.

**Q6. What is the time complexity of searching in a Hash Map vs a Binary Search Tree (BST)?**
**Answer:** 
- **Hash Map:** Average time complexity for search is O(1) due to direct addressing via hash functions. In the worst case (many collisions), it can be O(n).
- **BST:** Average time complexity for search is O(log n) assuming the tree is balanced. In the worst case (a skewed tree), it grades to O(n).

**Q7. Explain the concept of Object-Oriented Programming (OOP) and how you have used it.**
**Answer:** OOP is a paradigm based on concepts like classes and objects. Its four main pillars are:
1. **Encapsulation:** Hiding internal state (e.g., making variables private in C++).
2. **Abstraction:** Exposing only necessary details.
3. **Inheritance:** Creating new classes based on existing ones.
4. **Polymorphism:** Using a single interface for different types (e.g., function overloading/overriding).
In my projects, like the AI automation agents, I heavily use OOP to create modular code (e.g., creating an `Agent` base class and inheriting specific agents like `TwitterAgent` or `GmailAgent`).
