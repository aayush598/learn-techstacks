# C++ Copy Constructors and Move Semantics

> **TL;DR**: Copy/move semantics are the C++ contract for *ownership* — the copy constructor clones resources, the move constructor transfers them (stealing the source's pointers and leaving it empty), and the Rule of Three/Five plus `std::move`/`unique_ptr`/`shared_ptr` make resource lifetime safe, efficient, and exception-tolerant.

## 1. Why Does This Exist?
C++ doesn't have a GC: `new` hands you a pointer, and someone must `delete` exactly once, at exactly the right time. That's survivable for raw data, but the moment a class owns a resource (heap buffer, file handle, socket, mutex), the compiler needs to know **what "copying" an object means**. The *default* compiler-generated copy is a shallow bitwise copy — two objects end up pointing at the same buffer, and both destructors try to `delete` it: **double-free** (UB). Copy semantics exist to define correct copying (deep clone) and — via **move semantics** (C++11) — efficient transfer of resources from temporary objects that are about to die, avoiding needless deep copies. This is the mechanism that makes RAII (`unique_ptr`), zero-cost abstractions, and safe containers (`std::vector` resizing) possible.

## 2. How Does It Work?
At a glance:
- **Copy constructor**: `T(const T&)` — deep-copies the resource; source unchanged.
- **Copy assignment**: `T& operator=(const T&)` — deep-copies into an existing object (handle self-assignment).
- **Move constructor**: `T(T&&)` — steals the resource by copying the source's pointer, then nulls the source's pointer (source left valid-but-empty); called for rvalues (temporaries, `std::move(x)`).
- **Move assignment**: `T& operator=(T&&)` — transfers + releases the target's old resource.
- **Rule of Three**: if a class needs a custom destructor, copy ctor, or copy assignment, it needs all three.
- **Rule of Five**: with C++11, also move ctor + move assignment.
- **`std::move(x)`** = a cast to rvalue reference — it *enables* a move, doesn't move anything itself.
- **Smart pointers**: `unique_ptr` (exclusive ownership, non-copyable, movable), `shared_ptr` (atomic refcount, copies share ownership), `weak_ptr` (non-owning observation).

## 3. When Is It Used?
- **Returning by value** — `std::vector<int> make() { return {1,2,3}; }` — NRVO/move avoids copies.
- **Pushing into containers** — `vec.push_back(std::move(bigObject))` or `emplace_back(args...)`.
- **`std::vector` reallocation** — when a vector grows, elements are moved (if `noexcept` move) rather than copied.
- **Passing ownership** — `void sink(std::unique_ptr<Widget> w)`; move into the parameter.
- **Resource classes** — any class wrapping `new[]`, `fopen`, sockets, or a mutex must implement the rule.
- **RAII containers** — `std::string`, `std::vector`, `std::thread`, `std::fstream` all use copy/move to manage their buffers.

## 4. Why Wasn't Another Approach Chosen?
Alternatives:
- **Always deep-copy (Java semantics)**: safe but expensive — every temporary copy clones the buffer. Move semantics eliminate temporary-copy cost while keeping value semantics for real copies.
- **Always move / steal (pointer semantics, like C++ before value semantics)**: objects become aliases → lifetime bugs. C++ keeps *value semantics* by default and lets you *opt into* moving.
- **Reference counting everywhere (shared_ptr for everything)**: adds atomic refcount overhead and ownership ambiguity; C++ offers it as an explicit tool (`shared_ptr`) but keeps plain-value classes cheap.
- **GC (Java/C#/Go)**: eliminates ownership but costs pauses and hides deterministic destruction — incompatible with C++'s zero-cost + RAII philosophy.
- **Only copy, no move (pre-C++11)**: temporaries forced deep copies or awkward `swap` tricks; move semantics was the principled fix.

## 5. Intuition
A copy is like **photocopying a document**: you get your own copy; editing yours doesn't touch the original, but photocopying is expensive. A move is like **handing the original file to someone** with the promise you'll never use your (now empty) folder again: the recipient gets the real content instantly, and your folder is emptied. The key insight: when the source is a *temporary* (a `std::vector` about to be destroyed), copying it would clone then destroy the clone's source — pure waste. Move says "take the buffer, null my pointer, I'm being destroyed anyway." `std::move(x)` is just the phrase "you may take my stuff now" — it doesn't touch anything; it only tells the compiler this expression is an rvalue so the move overload is selected.

## 6. Real-World Analogy
A **library's inter-library loan**: copying a book = printing a full copy (expensive, you own it forever). Moving = *lending the actual book*: the library notes the borrower has it, marks its own shelf empty, and never lends that shelf again. A `unique_ptr` is a **single library card** — only one person can hold the card; passing it means the previous holder's card is invalidated. `shared_ptr` is a **group membership card** — many people hold copies; the book is destroyed when the *last* member returns. The destructor is the **return-by-force**: when a borrower's membership expires, the book is returned (resource freed) automatically — no one has to remember.

## 7. Formal Definition
- **Copy constructor**: `T(const T& other)` — initializes a new object as a copy of `other`; must deep-copy owned resources.
- **Copy assignment operator**: `T& operator=(const T& other)` — replaces `*this`'s resource with a copy of `other`'s; must handle self-assignment and free the existing resource.
- **Move constructor** (C++11): `T(T&& other) noexcept` — initializes from an rvalue by transferring resources; leaves `other` in a valid-but-unspecified state (typically null pointers).
- **Move assignment**: `T& operator=(T&& other) noexcept` — transfers resources, releasing `*this`'s current resource.
- **Rule of Three**: a class that needs a user-declared destructor, copy ctor, or copy assignment likely needs all three.
- **Rule of Five**: the above plus move ctor and move assignment (C++11).
- **`std::move`**: `static_cast<T&&>(x)` — a *cast*, not a function call; makes `x` an rvalue so overload resolution prefers move.
- **`unique_ptr<T>`**: sole owner; deleted copy ctor/assignment; move transfers ownership; frees on destruction.
- **`shared_ptr<T>`**: shared ownership with an atomic reference count; copy increments, destruction decrements, frees at zero; control block holds the count + deleter.
- **`weak_ptr<T>`**: non-owning observer; `lock()` returns a `shared_ptr` or empty if the object died (avoids dangling).

## 8. Example
```cpp
#include <utility>
#include <cstring>
#include <iostream>

class Buffer {
    char* data;
    size_t size;
public:
    explicit Buffer(size_t n) : data(new char[n]), size(n) { std::cout << "ctor\n"; }

    // Rule of Five implementation
    Buffer(const Buffer& other)                       // copy ctor: deep clone
        : data(new char[other.size]), size(other.size) {
        std::memcpy(data, other.data, size);
        std::cout << "copy\n";
    }
    Buffer& operator=(const Buffer& other) {          // copy assign: handle self-assign
        if (this != &other) {
            delete[] data;
            size = other.size;
            data = new char[size];
            std::memcpy(data, other.data, size);
        }
        return *this;
    }
    Buffer(Buffer&& other) noexcept                   // move ctor: steal, then null source
        : data(other.data), size(other.size) {
        other.data = nullptr; other.size = 0;          // source left valid-but-empty
        std::cout << "move\n";
    }
    Buffer& operator=(Buffer&& other) noexcept {      // move assign
        if (this != &other) {
            delete[] data;                             // free current resource first
            data = other.data; size = other.size;
            other.data = nullptr; other.size = 0;
        }
        return *this;
    }
    ~Buffer() { delete[] data; }                      // dtor: exactly-once free

    const char* get() const { return data; }
};
```
Trace `Buffer b = makeBuffer();`:
1. `makeBuffer()` builds a temporary `Buffer` (ctor).
2. Return: the compiler applies NRVO (copy elision) — the temporary is constructed *directly* into `b`; neither copy nor move runs (C++17 guarantees elision in this case).
3. If elision isn't possible, the move ctor runs (steals from the dying temporary).

Trace `b2 = b1;`: copy assignment runs — clones `b1`'s buffer into `b2` (which first deletes its old one). Trace `b2 = std::move(b1);`: move assignment — `b2`'s old buffer freed, `b1`'s pointer stolen, `b1` left empty.

## 9. Internal Working
1. **When the compiler generates defaults**: if you declare no dtor/copy/move, the compiler synthesizes all of them (shallow copy for trivial types). Declaring *any* of the copy/dtor trio **deprecates** implicit move generation (C++11 rules) — a class that declares a copy ctor but no move ctor won't get an implicit move.
2. **Overload resolution**: an rvalue expression (temporary, `std::move(x)`) prefers `T&&` overloads; an lvalue (`b1`) prefers `const T&`. `std::move` changes the *value category* so moves get chosen.
3. **noexcept**: move ctors should be `noexcept`; `std::vector` uses `std::move_if_noexcept` when reallocating — if the move might throw, it copies instead (to preserve strong exception guarantee).
4. **Elision/NRVO**: the compiler may eliminate copy/move entirely when returning a local or constructing from a temporary; C++17 *mandates* elision in specific cases — so `return Buffer(...)` costs nothing.
5. **`shared_ptr`**: control block (refcount, weak count, deleter) allocated separately; copies atomic-increment the count; last owner runs the deleter and frees the control block. Refcount is atomic (thread-safe increments) but the *pointee* isn't synchronized.
6. **`unique_ptr`**: stores only the pointer (+ deleter); move transfers the pointer and nulls the source; `reset()`/release patterns give explicit ownership transfer.

## 10. Time Complexity
- Copy ctor/assignment: **O(resource size)** — must clone every byte.
- Move ctor/assignment: **O(1)** — a few pointer/size moves (this is the whole point).
- `std::move`: O(1) — it's a cast.
- `vector::push_back(std::move(x))`: O(1) move if capacity available; amortized O(1) overall.
- `shared_ptr` copy/destroy: O(1) with an **atomic** refcount increment/decrement (a `lock; add` — a few ns, cache-contention cost if many threads share).
- `weak_ptr::lock()`: O(1) atomic.
- NRVO/elision: O(0) — no operation emitted.

## 11. Advantages
- Zero-cost: moving is O(1) vs O(n) copying — temporary-heavy code becomes cheap.
- Correct by construction: the Rule of Five + RAII make double-free/leaks compile-time-discussable rather than runtime-crashes.
- Deterministic destruction: resources freed exactly when the object dies (unlike GC).
- `unique_ptr` gives exclusive ownership with zero runtime overhead (same size as a raw pointer).
- `shared_ptr` gives safe shared ownership with a well-defined lifetime (last owner frees).
- `noexcept` moves let containers grow safely and efficiently.
- Expresses intent: `unique_ptr`/move say "ownership transfers"; raw pointers say "I don't own this" — self-documenting code.

## 12. Disadvantages
- Complexity: getting the Rule of Five wrong (e.g., forgetting move, wrong `noexcept`, bad self-assignment) causes subtle bugs.
- Atomic refcounts on `shared_ptr` are a real per-copy cost and a cache-contention point under high-thread sharing.
- `shared_ptr` can't break cycles (A owns B, B owns A → leak); needs `weak_ptr`.
- Move semantics can be surprising: after `std::move(x)`, `x` is valid but unspecified — using it without reinitializing is a bug.
- Copy elision rules are subtle; relying on it vs getting a move can affect performance expectations.
- The rule "no implicit move if you declare a copy/dtor" surprises many developers (deleted moves → silently copies).

## 13. Interview Questions
1. **Q: What is the Rule of Three?** A: A class that manages a resource and needs a custom destructor also needs a copy constructor and copy assignment (or must disable copying); otherwise shallow copies cause double-free.
2. **Q: What is the Rule of Five?** A: Rule of Three plus move constructor and move assignment (C++11), so resource transfer is efficient and safe.
3. **Q: Copy constructor vs move constructor?** A: Copy deep-clones (source unchanged); move transfers ownership (source's pointers nulled) — O(resource) vs O(1).
4. **Q: What does `std::move` actually do?** A: It's `static_cast<T&&>(x)` — it just casts the value category to rvalue so the move overload is selected; it doesn't move anything.
5. **Q: What is RAII?** A: Resource Acquisition Is Initialization: acquire resources in the constructor, release in the destructor — guarantees cleanup on any exit path (scope end, exception).
6. **Q: `unique_ptr` vs `shared_ptr`?** A: `unique_ptr` = sole ownership, non-copyable but movable, zero overhead; `shared_ptr` = shared ownership via atomic refcount, copyable, control block, frees at zero.
7. **Q: Why should move constructors be `noexcept`?** A: `std::vector` reallocation uses `std::move_if_noexcept` — if a move can throw, it copies instead; `noexcept` enables safe, efficient moving.
8. **Q: What happens after `std::move(x)`?** A: `x` is in a valid-but-unspecified state; you may reassign it or destroy it but shouldn't assume its old contents.
9. **Q: What is copy elision / NRVO?** A: The compiler may skip the copy/move entirely when returning a local (NRVO) or constructing from a temporary; C++17 guarantees elision in those cases.
10. **Q: How do you prevent copying of a class?** A: Delete the copy ctor/assignment: `T(const T&) = delete; T& operator=(const T&) = delete;` (or make them private) — like `unique_ptr` does.
11. **Q: Why does `shared_ptr` need a `weak_ptr`?** A: `shared_ptr` cycles never free (A↔B hold each other's counts at 1); `weak_ptr` breaks the cycle without owning.
12. **Q: What is the difference between `push_back(x)` and `emplace_back(args...)`?** A: `push_back` copies/moves an existing object; `emplace_back` constructs in place from args — avoids a temporary when you have the constructor args.
13. **Q: What is self-assignment and why guard against it?** A: `x = x;` — copy/move assignment that deletes the resource then copies from it reads freed memory; guard with `if (this != &other)` or copy-and-swap.
14. **Q: When is the copy constructor called?** A: Copy-initialization from an lvalue (`A b = a;`, passing by value, returning by value without elision), explicit copy.
15. **Q: What is the "big three/five" hazard with `std::vector` elements?** A: Vector reallocation copies/moves every element; broken move/copy semantics corrupt data during growth.
16. **Q: Why can't `unique_ptr` be copied?** A: Copying would give two owners and a double-free; its copy ctor/assignment are deleted — only move is allowed, transferring ownership.
17. **Q: What is a dangling pointer and how do smart pointers prevent it?** A: A pointer to freed memory; `unique_ptr`/`shared_ptr` free exactly when ownership ends (no premature free), `weak_ptr::lock` prevents accessing a dead object.
18. **Q: Can you use a moved-from object again?** A: Yes — after reinitialization/assignment; the moved-from state is valid but unspecified, so assign a fresh value before use.

## 14. Follow-Up Questions
1. **Q: What is the copy-and-swap idiom?** A: Implement assignment as "copy the argument, then swap with `*this`" — gives strong exception safety, handles self-assignment automatically, and unifies copy/move assignment.
2. **Q: Why might `push_back` not use the move even with `std::move`?** A: If the move ctor is not `noexcept` and the element type's copy is available, `vector` picks copy (`std::move_if_noexcept`) to keep the strong guarantee during reallocation.
3. **Q: What is the difference between value category and type?** A: A variable has a *type* (`Buffer`) and a *value category* (lvalue/rvalue/xvalue). `std::move` changes the category, not the type; overloads on `&&` are selected by category.
4. **Q: What is perfect forwarding?** A: `template<class T> void f(T&& t)` with `std::forward<T>` re-emits the exact category of the argument (lvalue or rvalue), enabling generic code to forward both copies and moves correctly.
5. **Q: What are the pitfalls of `shared_ptr` in callbacks/lambdas?** A: Capturing a `shared_ptr` by value in a long-lived lambda keeps the object alive (cycle risk); capture a `weak_ptr` and `lock()` inside the callback instead.
6. **Q: How do you detect copy/move in a class for debugging?** A: Add logging to each special member; or use `static_assert(std::is_move_constructible_v<T>)` / `std::is_copy_constructible_v<T>` to verify traits at compile time.

## 15. Coding Example
```cpp
#include <memory>
#include <vector>
#include <string>
#include <iostream>

class User {
    std::string name;              // string already implements the Rule of Five
    int age;
public:
    User(std::string n, int a) : name(std::move(n)), age(a) {}
    const std::string& name() const { return name; }
};

std::unique_ptr<User> makeUser() {  // exclusive ownership returned
    return std::make_unique<User>("Alice", 30);   // guaranteed elision/move, no copy
}

void transfer(std::unique_ptr<User> u) {          // ownership moves into parameter
    std::cout << u->name() << "\n";
}

int main() {
    std::unique_ptr<User> alice = makeUser();     // unique_ptr: no copy possible
    // std::unique_ptr<User> copy = alice;        // ERROR: deleted copy
    std::unique_ptr<User> bob = std::move(alice); // ownership moves; alice now null
    transfer(std::move(bob));                     // move into function; bob null after

    // shared ownership
    std::shared_ptr<User> s1 = std::make_shared<User>("Carol", 40);
    std::shared_ptr<User> s2 = s1;                // copy shares ownership (refcount 2)
    std::weak_ptr<User> w = s1;                   // non-owning observer
    if (auto sp = w.lock()) {                     // safe: null if the object died
        std::cout << sp->name() << " use_count=" << s1.use_count() << "\n";
    }
    s1.reset(); s2.reset();                       // refcount 0 -> object freed

    // vector reallocation: elements must be movable/copyable safely
    std::vector<User> users;
    users.emplace_back("Dave", 25);               // constructed in place, no temp
}
```
Key behaviors to be able to narrate: `std::move(alice)` hands the pointer to `bob` (O(1)); after the line, `alice == nullptr`. `users.emplace_back("Dave", 25)` constructs the `User` directly in the vector's storage (no copy/move of a temporary).

## 16. Industry Usage
- **Every C++ codebase** relies on the Rule of Five in resource classes: trading systems (Jane Street/DRW use modern C++ smart pointers heavily), game engines (Unreal's `TSharedPtr`/`TUniquePtr` mirror `shared_ptr`/`unique_ptr`), LLVM/Clang (owning vs non-owning pointer conventions), databases (RocksDB, MySQL's InnoDB).
- **`std::move`/`emplace_back`** are the standard idioms in high-performance services (protocol parsing, memory-mapped buffers, zero-copy networking).
- **`shared_ptr`** used for genuinely shared resources (caches, singletons, plugin objects); `weak_ptr` breaks caches/parent-child cycles.
- **Folly/Abseil** (Facebook/Google) provide optimized variants (`folly::SharedMutex`-adjacent ownership patterns, `absl::optional` value types) built on the same copy/move rules.
- **Exceptions + RAII** is the documented C++ exception-safety strategy: strong guarantee via copy-and-swap is idiomatic in libraries like Boost.

## 17. References
- ISO/IEC 14882:2020 (C++20), §11.10.3 "Copy/move constructors", §11.10.4 "Copy/move assignment operators", §7.6.1.9 "move", §20.7 "smart pointers".
- cppreference.com: *copy constructor*, *move constructor*, *rule of three/five*, *std::move*, *std::unique_ptr*, *std::shared_ptr*, *copy elision*.
- Scott Meyers, *Effective Modern C++*, Items 17-24 (move, forwarding, special member functions) — the definitive guide.
- Herb Sutter, "GotW #59: Smart pointer parameters" and *Exceptional C++* (copy-and-swap).
- Bjarne Stroustrup, *A Tour of C++* (value semantics + move).
- Nicolai Josuttis, *C++ Move Semantics — The Complete Guide*.

## 18. Cheat Sheet
- Rule of Three: dtor + copy ctor + copy assign (if you write one, write all).
- Rule of Five: + move ctor + move assign (C++11).
- Move = steal + null source; O(1); copy = clone; O(resource).
- `std::move` is just `static_cast<T&&>` — enables, doesn't move.
- `noexcept` moves → vector reallocates by move; throwing moves → copies.
- Copy elision/NRVO (C++17 mandatory in return-by-value cases) = no copy/move at all.
- `unique_ptr`: sole owner, deleted copy, move-only, zero overhead.
- `shared_ptr`: atomic refcount, copies share, frees at zero; `weak_ptr` breaks cycles.
- Self-assignment guard: `if (this != &other)`.
- Copy-and-swap = strong exception safety + self-assignment-safe.
- Declaring a copy/dtor suppresses implicit move generation.

## 19. Quiz
1. The Rule of Three requires which trio? a) ctor, dtor, copy ctor b) dtor, copy ctor, copy assign c) move ctor, copy ctor, dtor d) dtor, operator=, move assign → **b**
2. `std::move(x)` does what? a) Moves the object b) Casts `x` to `T&&` (rvalue) c) Deletes x d) Copies x → **b**
3. A move constructor should typically be: a) `throw()` b) `noexcept` c) `inline` d) `const` → **b**
4. `unique_ptr<T>` is: a) Copyable b) Move-only c) Both d) Neither → **b**
5. Which best describes the moved-from state? a) Undefined (anything can happen) b) Valid-but-unspecified c) Always empty d) Same as source → **b**
6. Copy elision means: a) The copy runs twice b) No copy/move is emitted at all c) A shallow copy happens d) A warning → **b**
7. `shared_ptr`'s refcount is: a) Non-atomic b) Atomic c) Compile-time d) Optional → **b**
8. A `weak_ptr` is used to: a) Own a resource b) Break cycles / observe without owning c) Copy a `shared_ptr` d) Replace raw pointers → **b**
9. Self-assignment in copy assignment is dangerous because: a) It copies twice b) It may free the resource then read freed memory c) It's slow d) It throws → **b**
10. When `vector` reallocates, elements are moved only if the move is: a) Cheap b) `noexcept` (via `std::move_if_noexcept`) c) Non-virtual d) Inlined → **b**

## 20. Flashcards
- **Q: Rule of Three/Five?** → **A:** If a class needs dtor/copy, write all of them (+move for Five).
- **Q: What does `std::move` do?** → **A:** Cast to rvalue reference; selects move overload, moves nothing itself.
- **Q: Move vs copy cost?** → **A:** Move O(1) (steal+null); copy O(resource size).
- **Q: Why `noexcept` move?** → **A:** So `vector` reallocation can move safely instead of copying.
- **Q: `unique_ptr` copyable?** → **A:** No — deleted copy; move-only sole ownership.
- **Q: How does `shared_ptr` free?** → **A:** Atomic refcount; last owner runs the deleter.
- **Q: What is RAII?** → **A:** Acquire in ctor, release in dtor — cleanup guaranteed on any exit path.
- **Q: Why `weak_ptr`?** → **A:** Break shared_ptr cycles; observe without owning.

## 21. Revision
Copy/move semantics define ownership. Copy ctor/assign clone resources (O(n)); move ctor/assign steal them (O(1)) and null the source. Rule of Three (dtor+copy ctor+copy assign) and Rule of Five (+move ctor/assign) keep resource classes safe; declaring a copy/dtor suppresses implicit moves. `std::move` = `static_cast<T&&>` — a category change that picks the move overload. `noexcept` moves let `std::vector` reallocate by moving; otherwise it copies. C++17 guarantees copy elision on returns, so returning by value is free. `unique_ptr` = move-only sole ownership (zero overhead); `shared_ptr` = atomic refcount shared ownership, frees at zero, `weak_ptr` breaks cycles. Guard self-assignment (`if (this != &other)`) or use copy-and-swap. In interviews: trace `A b = a;` (copy), `A c = std::move(a);` (move), `return a;` (elision), and `emplace_back` vs `push_back`, and justify the Rule of Five for a resource class.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is the Rule of Three/Five?" | 7 Formal Definition / 13 Interview |
| "What does `std::move` actually do?" | 7 / 13 Interview |
| "Move vs copy — when is each called?" | 8 Example / 13 Interview |
| "Why must move ctors be `noexcept`?" | 9 Internal Working / 13 Interview |
| "`unique_ptr` vs `shared_ptr` vs `weak_ptr`?" | 2 / 13 Interview |
| "What is RAII and why does it matter?" | 1 / 13 Interview |
| "What is copy elision / NRVO?" | 9 Internal Working / 13 Interview |
| "How do you make a class non-copyable?" | 13 Interview |
| "Why is self-assignment dangerous?" | 13 Interview |
| "What is the copy-and-swap idiom?" | 14 Follow-Up Questions |
