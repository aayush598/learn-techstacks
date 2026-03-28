# 100 Python, C++, and JavaScript Questions

## Python Core & Fundamentals
1. **Q:** What is PEP 8? **A:** Python's style guide for writing clean and readable code.
2. **Q:** What is a dynamically typed language? **A:** Variable types are determined at runtime, like in Python.
3. **Q:** What is a statically typed language? **A:** Variable types are declared explicitly and checked at compile-time, like in C++.
4. **Q:** What is the difference between `list` and `tuple`? **A:** Lists are mutable (changeable), tuples are immutable.
5. **Q:** How is memory managed in Python? **A:** Through a private heap containing all objects and data structures, managed by the Python memory manager with garbage collection.
6. **Q:** What are decorators? **A:** Functions that modify the behavior of another function or class.
7. **Q:** What is a generator? **A:** A function that returns an iterator using the `yield` keyword instead of `return`, evaluating lazily.
8. **Q:** What does `*args` and `**kwargs` do? **A:** `*args` passes a variable number of non-keyworded arguments; `**kwargs` passes keyworded arguments.
9. **Q:** What is the `__init__` method? **A:** A constructor method in Python classes called when an object is instantiated.
10. **Q:** What is the Global Interpreter Lock (GIL)? **A:** A mutex that prevents multiple native threads from executing Python bytecodes simultaneously.
11. **Q:** Explain list comprehension. **A:** A concise way to create lists, e.g., `[x**2 for x in range(10)]`.
12. **Q:** What is the difference between `deep copy` and `shallow copy`? **A:** Shallow copy copies object references; deep copy creates a new object and recursively copies contents.
13. **Q:** How do you handle exceptions in Python? **A:** Using `try`, `except`, `else`, and `finally` blocks.
14. **Q:** What is `self` in Python? **A:** An instance of the class passed explicitly to its methods.
15. **Q:** Explain the `map()` function. **A:** Applies a function to all items in an input list.
16. **Q:** How to read a huge file in Python? **A:** Iterate line-by-line using a generator or `yield` to avoid loading it entirely into memory.
17. **Q:** What is `asyncio`? **A:** A library to write concurrent code using the async/await syntax.
18. **Q:** Difference between `is` and `==`? **A:** `==` compares values; `is` compares memory addresses (identity).
19. **Q:** What is a lambda function? **A:** A small, anonymous, single-expression function.
20. **Q:** How does a dictionary work in Python? **A:** It is a hash map with O(1) average lookup time.

## C++ Core & Data Structures
21. **Q:** Difference between C and C++? **A:** C++ supports Object-Oriented Programming (classes, objects) while C is strictly procedural.
22. **Q:** What is encapsulation? **A:** Bundling data and methods into a single unit (class) and hiding internals using access specifiers.
23. **Q:** What is polymorphism? **A:** The ability of a function, object, or method to take on multiple forms (overloading/overriding).
24. **Q:** What are pointers? **A:** Variables that store memory addresses of other variables.
25. **Q:** What is a reference in C++? **A:** An alias for an already existing variable.
26. **Q:** Differentiate `malloc()` and `new`. **A:** `malloc()` is a C function for memory allocation; `new` is a C++ operator that also calls constructors.
27. **Q:** What is a virtual function? **A:** A function in a base class declared with `virtual`, overridden in a derived class.
28. **Q:** What is a pure virtual function? **A:** A virtual function with no implementation (`= 0`), making the class abstract.
29. **Q:** What is the Standard Template Library (STL)? **A:** A library of container classes, algorithms, and iterators (vector, map, set).
30. **Q:** Difference between `vector` and `array`? **A:** Vectors are dynamically sized; arrays have a fixed size at compile time.
31. **Q:** Explain `unordered_map` vs `map`. **A:** `map` is implemented as an AVL/Red-Black tree (O(log n)); `unordered_map` is a hash map (O(1)).
32. **Q:** What is a memory leak? **A:** When allocated memory is not freed after use, causing memory exhaustion.
33. **Q:** How do you prevent memory leaks? **A:** Using smart pointers like `std::unique_ptr` and `std::shared_ptr`.
34. **Q:** What is a dangling pointer? **A:** A pointer pointing to a memory location that has been deleted or freed.
35. **Q:** What is the complexity of binary search? **A:** O(log n).
36. **Q:** When to use Breadth-First Search (BFS)? **A:** To find the shortest path in an unweighted graph.
37. **Q:** How is a priority queue implemented? **A:** Typically using a specialized tree structure called a Heap (min-heap or max-heap).

## JavaScript Core
38. **Q:** What are closures in JS? **A:** A function that remembers variables from its outer scope even after the outer function has executed.
39. **Q:** Concept of Hoisting? **A:** JS moves variable and function declarations to the top of their scope before execution.
40. **Q:** Difference between `var`, `let`, and `const`? **A:** `var` is function-scoped and hoisted; `let` and `const` are block-scoped; `const` cannot be reassigned.
41. **Q:** What is the Event Loop? **A:** The mechanism that handles async callbacks, pushing them from the queue to the call stack when empty.
42. **Q:** Explain Promises. **A:** Objects representing the eventual completion (or failure) of an asynchronous operation.
43. **Q:** What happens in async/await? **A:** Syntactic sugar over Promises to make asynchronous code look synchronous.
44. **Q:** Difference between `==` and `===`? **A:** `==` checks value parity with type coercion; `===` checks value and type strictly.
45. **Q:** What is an arrow function? **A:** A concise syntax for functions (`() => {}`) that does not bind its own `this` context.
46. **Q:** What is `this` in JS? **A:** A keyword referring to the context in which a function is executed.
47. **Q:** Explain DOM. **A:** Document Object Model, an API representing the HTML structure as a tree of objects.
48. **Q:** What is Event Bubbling? **A:** When an event is triggered on an element, it bubbles up to its parent hierarchy.
49. **Q:** What is Event Delegation? **A:** Attaching a single event listener to a parent element to handle events on its descendants.
50. **Q:** What is strict mode? **A:** `use strict;` enforces stricter parsing and error handling in JS.
51. **Q:** Difference between `null` and `undefined`? **A:** `undefined` means a variable is declared but not assigned; `null` is an explicit empty assignment.

## Mixed DSA & Algorithms
52. **Q:** Reverse a string in Python. **A:** `s[::-1]`
53. **Q:** Check if a string is a palindrome. **A:** `s == s[::-1]`
54. **Q:** Find the maximum in an array. **A:** Iterate keeping track of the max variable. O(n).
55. **Q:** What is a linked list? **A:** A linear data structure mapping nodes with data and pointers to the next node.
56. **Q:** Time complexity of QuickSort? **A:** Best/Average O(n log n), worst O(n^2).
57. **Q:** Time complexity of MergeSort? **A:** O(n log n) in all cases.
58. **Q:** How to detect a loop in a linked list? **A:** Floyd's Cycle-Finding Algorithm (Tortoise and Hare pointers).
59. **Q:** Find the middle of a linked list. **A:** One pointer moves 2 steps, another 1 step.
60. **Q:** Two Sum problem approach? **A:** Use a Hash Map storing value complements for O(n) complexity.
... (expanding abstractly for continuous reading in interviews)
