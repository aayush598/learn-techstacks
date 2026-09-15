# Operator Overloading and Special Method Contracts — 100 Interview Q&A

## Q1: What is operator overloading and why does it exist in OOP?

**A:** Operator overloading is the ability to redefine the behavior of built-in operators (like `+`, `-`, `==`, `<<`) for user-defined types. It exists because it allows custom types to participate in idiomatic expressions, making code more readable and expressive. Instead of calling `a.add(b)`, you write `a + b`, which maps directly to the mathematical or domain concept.

In OOP, operator overloading is a form of ad-hoc polymorphism (also called overloading polymorphism). The compiler or runtime resolves which implementation to call based on the operand types. This is distinct from subtype polymorphism (virtual dispatch) and parametric polymorphism (generics/templates). Languages differ in how much they expose: C++ and Python allow extensive operator overloading, while Java deliberately restricts it, and Go allows none at all.

The key benefit is API fluency. Libraries like linear algebra packages, arbitrary-precision arithmetic, string builders, and smart pointers all rely on operator overloading to present a natural interface. The trade-off is that misuse can create confusing or unreadable code — a well-known concern that influenced Java's design philosophy.

## Q2: How does C++ operator overloading work at the compiler level?

**A:** In C++, when the compiler encounters an operator expression like `a + b`, it performs **operator overload resolution**. This process has several phases. First, the compiler collects all visible candidate functions — both built-in operators and user-defined ones found via argument-dependent lookup (ADL) and regular name lookup. Then it applies overload resolution rules to select the best match.

For the expression `a + b`, the compiler looks for candidates of the form `operator+(a, b)` (free function) and `a.operator+(b)` (member function). Built-in `+` for primitive types is also a candidate. If the best match is a user-defined function, that function is called. If no viable candidate exists, the expression is ill-formed.

C++ defines specific rules about which operators can be overloaded, what their signatures must look like, and whether they must be members or free functions. Most operators can be overloaded, with exceptions like `::`, `.`, `.*`, `?:`, and `sizeof`. The compiler enforces arity (unary vs binary) but allows you to define new semantics within reason — though violating expected semantics is considered poor practice.

## Q3: What are the member-function vs free-function forms of operator overloading in C++?

**A:** In C++, most operators can be overloaded in two ways: as a **member function** of the class, or as a **free function** (global function, often a `friend`). The member form has an implicit `this` pointer as the left-hand operand. For a binary operator like `+`, a member function takes one explicit parameter (the right-hand operand), while a free function takes two explicit parameters.

Member form: `T operator+(const T& rhs) const;` — called as `a + b`, equivalent to `a.operator+(b)`.
Free form: `friend T operator+(const T& lhs, const T& rhs);` — called as `a + b`, resolved as a free function.

The practical difference arises with **symmetry** and **implicit conversions**. If you define `operator+` as a member, then `a + literal` works (literal converts to `T` on the right), but `literal + a` fails because the left operand is not a `T`. A free function solves this because both operands go through overload resolution. Compound assignment operators (`+=`, `-=`, etc.) are almost always members because they modify `*this`.

For stream insertion (`<<`) and extraction (`>>`), you **must** use free functions because the left-hand operand is `std::ostream` or `std::istream`, not your class. The idiomatic approach is to make such functions `friend` of your class to access private members.

## Q4: Which operators can and cannot be overloaded in C++?

**A:** C++ allows overloading a wide range of operators but explicitly forbids a handful. The **forbidden** operators are: scope resolution `::`, member selection `.`, member pointer selection `.*`, ternary conditional `?:`, and `sizeof`. The comma operator `,` can be overloaded but is strongly discouraged because changing its evaluation-order semantics breaks the standard library and STL algorithms that rely on sequence points.

Every other operator is fair game: arithmetic (`+`, `-`, `*`, `/`, `%`), bitwise (`&`, `|`, `^`, `~`, `<<`, `>>`), comparison (`==`, `!=`, `<`, `<=`, `>`, `>=`, `<=>` in C++20), logical (`&&`, `||`, `!`), assignment (`=`, `+=`, `-=`, etc.), unary (`+`, `-`, `*`, `&`, `++`, `--`), subscript `[]`, function call `()`, dereference `*`, arrow `->`, address-of `&`, and new/delete.

C++20 introduced the **spaceship operator** `<=>`, which can be defaulted to auto-generate all six comparison operators from a single definition. This dramatically simplifies comparison-heavy classes. The `==` operator in C++20 also has special rewrite rules so that `a != b` can be rewritten as `!(a == b)` if no explicit `!=` is defined.

The `new` and `delete` operators can be overloaded globally or per-class, affecting memory allocation. Overloading `&&` and `||` is possible but disables their built-in short-circuit evaluation, which is almost always undesirable.

## Q5: What does Python's `__add__` vs `__radd__` mean and when is each called?

**A:** Python's binary `+` triggers two methods: `__add__` on the left operand and `__radd__` (reflected add) on the right operand. When evaluating `a + b`, Python first tries `a.__add__(b)`. If that returns `NotImplemented`, Python then tries `b.__radd__(a)`. If both return `NotImplemented`, Python raises `TypeError`.

This two-phase protocol enables **operator symmetry**. If you define a class `Matrix` and want `matrix + vector` to work, you implement `Matrix.__add__(self, other)`. But you also want `vector + matrix` to work, which requires `Vector.__radd__(self, other)` to handle the case when `Vector.__add__` doesn't know how to add a `Matrix`. The reflected method gives the right-hand operand a chance to handle the operation.

The convention is: if `__add__` is meant to be commutative (like numeric addition), you should implement both `__add__` and `__radd__` with the same logic. A common pattern is to have `__radd__` delegate to `__add__`:

```python
class Vector:
    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)
```

This ensures that both `v1 + v2` and `scalar_addition + v` (via inheritance or subclassing `int`) work correctly.

## Q6: Explain Python's `__str__` vs `__repr__` and when each is called.

**A:** These are two distinct special methods for string representation. `__repr__` returns an unambiguous, developer-focused string representation — ideally one that could recreate the object (e.g., `"Vector(3, 4)"`). `__str__` returns a human-readable, user-friendly string (e.g., `"(3, 4)"`). Python calls `__repr__` in the interactive interpreter, in `repr()` calls, as a fallback for `str()`, and in containers like lists and dicts when printing.

`__str__` is called by `str()`, `print()`, and f-string formatting (`f"{obj}"`). If `__str__` is not defined, Python falls back to `__repr__`. If neither is defined, the default from `object` is used, which returns something like `<__main__.Vector object at 0x7f...>`. Best practice is to **always define `__repr__`** and optionally `__str__`. A well-defined `__repr__` is invaluable for debugging.

In Python 3, `__repr__` should return a `str` object (not `bytes`). The `@dataclass` decorator auto-generates a useful `__repr__` based on field names. `@dataclass(repr=False)` disables this if you want a custom implementation.

## Q7: What is the subscription operator `[]` overload and how does Python handle it?

**A:** Python allows two methods for subscription behavior: `__getitem__(self, key)` and `__setitem__(self, key, value)`, plus `__delitem__(self, key)` for deletion. When you write `obj[key]`, Python calls `obj.__getitem__(key)`. For assignment `obj[key] = value`, it calls `obj.__setitem__(key, value)`. For `del obj[key]`, it calls `obj.__delitem__(key)`.

These methods enable container-like behavior for any class. For example, a custom dictionary, a matrix class, or a database query object can support `[]` indexing. The key can be any hashable type (or any type if you handle it manually), and Python does not enforce type constraints on keys.

A powerful pattern is supporting **slice objects**. If the key is a `slice`, your `__getitem__` receives a `slice` object with `start`, `stop`, and `step` attributes. This allows custom classes to support `obj[1:10:2]` syntax. The `collections.abc.Sequence` abstract base class expects `__getitem__` and provides default implementations for `__contains__`, `__iter__`, `__reversed__`, `index`, and `count` based on it.

```python
class Matrix:
    def __getitem__(self, key):
        if isinstance(key, tuple):
            row, col = key
            return self._data[row][col]
        elif isinstance(key, slice):
            return [self._data[i] for i in range(*key.indices(len(self._data)))]
        raise TypeError(f"indices must be tuples or slices, not {type(key).__name__}")
```

## Q8: How does C++ handle the subscript operator `[]` differently for `const` objects?

**A:** In C++, the subscript operator can have both a `const` and non-`const` overload, which is critical for supporting both read-only and read-write access. A `const` member function (`T& operator[](size_t idx) const`) returns a `const` reference, while the non-const version returns a mutable reference. This follows the principle that `const` objects should only allow read access.

```cpp
class Matrix {
    std::vector<double> data;
public:
    double& operator[](size_t idx) { return data[idx]; }       // non-const
    const double& operator[](size_t idx) const { return data[idx]; } // const
};
```

When you have a `const Matrix& m`, the compiler selects the `const` overload, which returns `const double&` — preventing modification. When you have a mutable `Matrix m`, the non-`const` overload is selected, returning `double&` that can be modified.

C++20 improves this with **`std::span`-like patterns** and the new subscript operator for multidimensional arrays. The `std::mdspan` (C++23) uses a custom `operator[]` with ` extents` for multi-dimensional indexing. Additionally, C++23 adds support for multiple subscripts: `operator[](auto... indices)`.

A common pitfall is the "const correctness" problem where forgetting the `const` overload means a `const` container cannot be subscripted, leading to cryptic compile errors. The solution is to always provide both overloads for subscript-capable classes.

## Q9: What is the call operator `()` overload and what are its common uses?

**A:** The call operator (`operator()` in C++, `__call__` in Python) allows an object to be invoked as if it were a function. Such objects are called **functors** (C++) or **callable objects** (Python). This is one of the most versatile overloads because it has no syntax restrictions — you can accept any number of arguments, return any type, and maintain state between calls.

In C++, functors are extensively used for callbacks, strategies, predicates, and STL algorithms. The `std::sort` function accepts a comparator, which is often a functor. Lambda expressions in C++ are syntactic sugar for anonymous functor classes — the compiler generates a class with `operator()`. This makes functors fundamental to modern C++ design.

Common C++ uses include: stateful predicates for sorting, policy classes for template parameters (allocators, hash functions), lazy evaluation wrappers, and function objects for callbacks that capture context. A functor can outperform function pointers because the compiler can inline the call through `operator()`.

```cpp
struct Adder {
    int offset;
    int operator()(int x) const { return x + offset; }
};
Adder add5{5};
int result = add5(10); // 15
```

In Python, `__call__` is used for decorators that need state, simple strategy patterns, and any object that behaves like a function but maintains internal state between invocations. It is also used to implement mock objects and context managers in some frameworks.

## Q10: What are Python's `__eq__`, `__ne__`, `__lt__`, `__le__`, `__gt__`, `__ge__` and how do they relate?

**A:** These six methods define rich comparison behavior. `__eq__` is for `==`, `__ne__` for `!=`, `__lt__` for `<`, `__le__` for `<=`, `__gt__` for `>`, and `__ge__` for `>=`. In Python 3, you **must** explicitly define `__eq__` and `__hash__` if you override equality, because the default `object.__eq__` uses identity comparison (`is`), while `__hash__` is automatically set to `None` if you define `__eq__` without `__hash__`, making the object unhashable.

Python provides `functools.total_ordering` as a class decorator that fills in the missing comparison methods given `__eq__` and one of `__lt__`, `__le__`, `__gt__`, or `__ge__`. You define the minimum and get the rest for free. This reduces boilerplate but adds a small performance cost.

An important edge case: if you define only `__eq__` (for value equality), the other comparisons remain undefined and raise `TypeError` if used. This is actually desirable for types where ordering is meaningless (like sets or complex numbers). If ordering is meaningful, use `@total_ordering` or define all six.

```python
from functools import total_ordering

@total_ordering
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius
    def __eq__(self, other):
        return self.celsius == other.celsius
    def __lt__(self, other):
        return self.celsius < other.celsius
```

Python 3 also supports comparison chaining (`a < b < c`), which desugars to `(a < b) and (b < c)` — evaluating `b` only once per comparison. If your objects are expensive to create or compare, this can be a concern.

## Q11: How does Java handle operator overloading, and why is it restricted?

**A:** Java deliberately does **not** support user-defined operator overloading for custom classes. The only operator overloading in Java is built into the language: the `+` operator works for `String` concatenation, and the comparison operators work for reference equality. You cannot redefine `+`, `-`, `*`, or any other operator for your own types.

The rationale, stated by James Gosling, is that operator overloading leads to code that is hard to read and maintain. In C++, the behavior of `<<` can mean bitwise shift or stream insertion depending on context, which requires knowing the types of both operands. Java prioritized readability and simplicity over expressiveness. The `String` concatenation `+` is the sole exception, implemented by the compiler as `StringBuilder.append()` calls.

Instead of operator overloading, Java uses **method names** for operations: `add()`, `equals()`, `compareTo()`. This is explicit but verbose. Libraries like `BigDecimal` use `add()`, `subtract()`, `multiply()`, etc., which makes the code clear but less natural for mathematical expressions.

Java's design philosophy is that explicit method calls are always clear, while overloaded operators can be confusing. This is a trade-off — Java gains readability but loses the concise expressiveness that makes C++ and Python numerical code elegant.

## Q12: What is the difference between the C++ `<=>` spaceship operator and traditional comparison operators?

**A:** The **spaceship operator** `<=>` (three-way comparison, C++20) returns a value that can be compared against zero to determine the ordering relationship. The return type is one of `std::strong_ordering`, `std::weak_ordering`, or `std::weak_partial_ordering`, depending on the semantics. This single operator can replace all six comparison operators.

`std::strong_ordering::eq` means equal, `lt` means less, `gt` means greater. You compare with zero: `(a <=> b) < 0` means `a < b`, `(a <=> b) == 0` means `a == b`, `(a <=> b) > 0` means `a > b`. The compiler can automatically generate all six operators from `<=>` and `==`, using rewrite rules defined in C++20.

```cpp
struct Point {
    int x, y;
    auto operator<=>(const Point&) const = default;
};
// Compiler generates: ==, !=, <, <=, >, >= automatically
```

The three return types encode different semantic guarantees: `strong_ordering` (like integers — irreflexive, transitive, trichotomy), `weak_ordering` (like strings where different representations can be equal — equivalence not identity), and `weak_partial_ordering` (like floating-point, where NaN makes the relation non-total).

This is a significant improvement over C++17 where you had to write six separate operators or use a comparison library. Defaulted `<=>` handles member-by-member comparison correctly, including for classes with mixed member types (strong and weak ordering can be mixed with appropriate conversions).

## Q13: What happens when you overload `new` and `delete` in C++?

**A:** Overloading `new` and `delete` gives you control over memory allocation for your class (per-class) or globally. The per-class `operator new` is called when you use `new MyClass(...)`, and the per-class `operator delete` is called when you use `delete ptr`. Global overloading affects all allocations unless a per-class version exists.

The signature for the class-level `operator new` is `static void* operator new(size_t size)` (and the array form `operator new[](size_t)`). The `static` keyword is required — these are always static member functions because there is no object to operate on when allocating. The `size_t size` parameter tells you how many bytes are needed. `operator delete` has the signature `static void operator delete(void* ptr)`.

Common reasons to overload include: debug allocation tracking, pool/slab allocators for performance, alignment guarantees, garbage collection hooks, and thread-safe allocation monitoring. For example, a game engine might use a pool allocator for small, frequently created objects to avoid heap fragmentation and reduce allocation overhead.

A critical caveat: if you overload `operator new`, you should also overload `operator new[]`, and correspondingly `delete` and `delete[]`. Failing to do so can lead to undefined behavior when arrays are used. Also, the standard library functions like `malloc` and `free` should not be mixed with the overloaded operators.

## Q14: What are the pitfalls of overloading the address-of operator `&` in C++?

**A:** Overloading the address-of operator (`operator&`) is extremely dangerous and almost never recommended. The address-of operator is used pervasively by the language and standard library — taking the address of objects, constructing pointers, and passing arguments to functions expecting pointers. Changing its behavior breaks fundamental assumptions.

The most famous case is `std::auto_ptr` (deprecated in C++11, removed in C++17), which overloaded `operator&` to return the internal pointer. This was a design mistake that led to subtle bugs, particularly with generic code. The replacement, `std::unique_ptr`, does **not** overload `operator&`.

The problem is that taking the address of an object is expected to be a no-op for a pointer to that object. If you override `operator&` to return something else, generic code that does `&obj` to get a pointer will silently break. Templates, containers, and algorithms all assume `&obj` gives you the real address. Overloading `operator&` violates this contract.

If you need to return a smart-pointer-like object (to prevent taking addresses), consider using `= delete` for copy/move operations or making the class non-copyable instead. Never overload `operator&` in production code — it causes maintenance nightmares and makes your type unsafe to use with any generic library.

## Q15: What is the extraction operator `>>` overload in C++ and how does it differ from `<<`?

**A:** The **extraction operator** `>>` is used for input (deserialization), while the **insertion operator** `<<` is used for output (serialization). For `std::ostream`, `<<` is already defined for basic types. For `std::istream`, `>>` is defined for basic types. To extend both to your custom types, you overload both operators.

The extraction operator for your class typically takes an `std::istream&` reference and a reference to your object, returning the stream by reference to allow chaining:

```cpp
friend std::istream& operator>>(std::istream& is, MyType& obj) {
    is >> obj.field1 >> obj.field2;
    if (!is) obj = MyType{}; // error recovery
    return is;
}
```

The key difference from `<<` is that `>>` modifies its second operand (the object being read into), so the second parameter is a non-const reference. The stream state must be checked after reading — if the stream enters a fail state, the object should either be left unchanged or set to a sensible default. The `friend` keyword is necessary because the left-hand operand is `std::istream`, not your class.

A common pattern is to check `is.good()` or rely on the stream's implicit bool conversion. If the extraction fails, you should ensure the object is in a valid state (strong exception safety). This is why many implementations set the object to a default-constructed value before attempting extraction.

## Q16: What is the difference between `operator+` and `operator+=` in terms of implementation?

**A:** The compound assignment operator `+=` modifies the left operand in place and returns a reference to `*this`. The simple addition operator `+=` creates and returns a new object. The standard idiom is to implement `operator+` in terms of `operator+=`:

```cpp
class BigInt {
    std::vector<int> digits;
public:
    BigInt& operator+=(const BigInt& rhs) {
        // in-place addition, modifying digits
        return *this;
    }
};

BigInt operator+(BigInt lhs, const BigInt& rhs) {
    lhs += rhs;  // lhs is a copy, then modified
    return lhs;
}
```

This avoids code duplication and ensures consistent semantics. Notice that `operator+` takes its first parameter **by value** — this is intentional. When you call `operator+(a, b)`, a copy of `a` is made, then `+=` modifies the copy, and the copy is returned. This gives you move semantics for free in C++11 and later (the copy may be elided via NRVO).

For `operator+=`, it must be a member function because it modifies `*this` and returns `*this&`. The free-function form of `operator+` handles the creation of the temporary and the symmetry for implicit conversions on both sides. The rule is: **`operator+=` is a member; `operator+` is a free function that calls `operator+=`**.

This pattern extends to all compound assignment operators (`-=`, `*=`, `/=`, `&=`, `|=`, `^=`, `<<=`, `>>=`). Each compound operator is a member function, and the corresponding simple operator is a free function that copies the left operand, applies the compound operator, and returns the result.

## Q17: What are the rules for C++ operator precedence and how do they affect overloading?

**A:** Operator precedence in C++ determines the order of evaluation in expressions, and **overloading an operator does not change its precedence**. The `+` operator still has higher precedence than `*`, even if you redefine both for your class. This means `a + b * c` is always `(a + b) * c` unless you add parentheses.

This can lead to surprising behavior. If you define a `Matrix` class and overload `*` for matrix multiplication and `+` for matrix addition, then `a + b * c` means `a + (b * c)` (matrix multiply first, then add), which is the correct mathematical precedence for matrices. However, if you overloaded `*` for element-wise multiplication and `+` for concatenation, the precedence might not match user expectations.

The standard defines 18 precedence levels, from highest (scope `::`, postfix `++`/`--`, function call `()`, subscript `[]`, member access `.`/`->`) to lowest (comma `,`). You cannot add parentheses to override precedence within an expression — only the programmer can add explicit parentheses in the source code.

C++20's `<=>` has special precedence rules: `(a <=> b) < 0` is how you write `a < b`, and the compiler understands the operator precedence between `<=>` and comparison operators like `<`, `==`, etc.

The practical takeaway: choose operators whose **existing precedence** matches the desired semantics of your operation. Overloading `*` for matrix multiplication is natural because matrix multiplication should bind tighter than addition. Overloading `+` for string concatenation is natural because `+` binds tighter than `&&`.

## Q18: What is the Python `__call__` protocol and how does it enable decorator patterns?

**A:** Python's `__call__` method allows an instance of a class to be called like a function. When you write `obj(args)`, Python invokes `obj.__call__(args)`. This enables **callable objects** — classes whose instances behave as functions. This is the foundation for advanced decorator patterns, memoization, and strategy objects.

A classic example is a memoization decorator using a callable class instead of a function decorator. The class stores a cache dictionary, and each call to the decorated function checks the cache first:

```python
class Memoize:
    def __init__(self, func):
        self.func = func
        self.cache = {}
    def __call__(self, *args):
        if args not in self.cache:
            self.cache[args] = self.func(*args)
        return self.cache[args]

@Memoize
def expensive_computation(n):
    # ... heavy computation
    return result
```

Without `__call__`, you would need a function with `__wrapped__` attributes or nested function closures. The callable class approach gives you a cleaner stateful decorator with better introspection. Python's `functools.lru_cache` is implemented as a callable class internally.

The `__call__` protocol also enables: mock objects that track calls, database connection wrappers that create new connections on call, factory objects that produce different results based on state, and builder patterns where the final build step is a call. In testing frameworks, mock objects use `__call__` to record call arguments and return predefined values.

## Q19: What is the destructor call order in C++ and why does it matter for operator overloading?

**A:** In C++, destructors are called in **reverse order of construction** — the last constructed subobject is destroyed first. For a class with multiple base classes, base destructors run after the derived destructor. For objects in an array, elements are destroyed in reverse order. This matters for operator overloading because the result of an overloaded operator may depend on temporaries whose lifetimes are tied to expression evaluation.

Consider a chained expression like `a + b + c`. This creates a temporary `t1 = a + b`, then `t2 = t1 + c`. The temporaries are destroyed in reverse: `t1` is destroyed after `t2`. If your `operator+` allocates resources (like a new matrix), the temporary is destroyed after the full expression, which is correct. But if you return a reference to a local, you get a dangling reference.

The C++ standard guarantees that temporaries in a full expression are destroyed at the end of the full expression (the semicolon). This means `(a + b) * c` creates a temporary for `a + b`, uses it in the multiplication, and destroys it — but the temporary for the multiplication result lives until the semicolon.

This matters for operator chaining and chaining with assignment: `a = b + c + d` evaluates `b + c` first, then `+ d`, then assigns to `a`. The temporaries for intermediate results are alive throughout, so references to them are valid during the full expression but invalid afterward. Returning by value from operators is essential to avoid dangling references.

## Q20: How does Python's `__hash__` relate to `__eq__` and why must they be consistent?

**A:** Python requires that if two objects compare equal (`a.__eq__(b)` returns `True`), then they **must** have the same hash value (`hash(a) == hash(b)`). This is the **hash contract**. The converse is not required — two objects can have the same hash but not compare equal (hash collision). This contract is essential for hash-based collections like `dict`, `set`, and `frozenset`.

If you override `__eq__` without defining `__hash__`, Python automatically sets `__hash__` to `None`, making your object unhashable. This is a safety mechanism — you cannot put objects with inconsistent equality and hashing into sets or use them as dict keys. If you want your object to be hashable and override `__eq__`, you must explicitly define `__hash__`.

The typical implementation uses the same fields used in `__eq__`:

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __hash__(self):
        return hash((self.x, self.y))
```

Mutability complicates this. If a field used in hashing is mutable and changes after the object is inserted into a set, the hash changes, and the set cannot find it. This is why `list` is unhashable but `tuple` is. Mutable objects that need to be hashable should either use identity-based hashing (the default) or implement `__hash__` based on immutable attributes.

## Q21: What is the copy-and-swap idiom in C++ and how does it relate to operator overloading?

**A:** The **copy-and-swap idiom** is a technique for implementing exception-safe assignment operators and providing a single point of resource management. It works by first making a copy of the right-hand side (which may throw), then swapping the copy's internals with `*this` (which is noexcept), and letting the old data be destroyed when the temporary goes out of scope.

The implementation relies on a `swap` function (either a member or a `friend` free function) and the copy constructor:

```cpp
class DynamicArray {
    int* data;
    size_t size;
public:
    DynamicArray(const DynamicArray& other) : data(new int[other.size]), size(other.size) {
        std::copy(other.data, other.data + size, data);
    }
    DynamicArray& operator=(DynamicArray rhs) {  // pass by value = copy
        swap(*this, rhs);
        return *this;
    }
    friend void swap(DynamicArray& a, DynamicArray& b) noexcept {
        using std::swap;
        swap(a.data, b.data);
        swap(a.size, b.size);
    }
};
```

The key insight: taking `rhs` by value (copy) ensures the copy is made before the swap. If the copy constructor throws, `*this` is unchanged (strong exception safety). The swap is noexcept because it only swaps pointers and integers. After the swap, the old data is in `rhs`, which is destroyed when the function returns. This also handles self-assignment correctly — the copy of `a` is swapped with `a`, then destroyed.

This idiom provides the **Rule of Five** implementations efficiently and is considered best practice for resource-managing classes in C++11 and later.

## Q22: What is the subscript operator `[]` behavior for multi-dimensional indexing in C++?

**A:** In standard C++, `operator[]` only accepts a single parameter. Multi-dimensional indexing like `matrix[i][j]` is achieved through **proxy objects** — the first `[]` returns a reference (or proxy) to a row, and the second `[]` operates on that proxy. This is a two-step process:

```cpp
class Matrix {
    std::vector<std::vector<double>> data;
public:
    class RowProxy {
        std::vector<double>& row;
    public:
        RowProxy(std::vector<double>& r) : row(r) {}
        double& operator[](size_t col) { return row[col]; }
    };
    RowProxy operator[](size_t row) { return RowProxy(data[row]); }
};
```

C++23 introduces `std::mdspan`, which provides native multi-dimensional array access with a single `operator[]` that takes multiple indices. The syntax `span[i, j]` uses C++20's comma operator overload or the new multi-subscript syntax `operator[](auto, auto)`.

For legacy code, the proxy pattern is essential. The proxy must be lightweight and ideally cheaply constructable. If the proxy owns data, it can cause unexpected copies. A common optimization is to return a `std::span` or a reference to an inner array, avoiding proxy objects entirely.

The alternative approach is a single `operator[]` that takes a `std::pair` or an initializer list:

```cpp
double& operator[](std::pair<size_t, size_t> idx) {
    return data[idx.first][idx.second];
}
```

This is simpler but less natural syntactically. The proxy pattern is more common in production codebases.

## Q23: What is Python's `__getattr__` vs `__getattribute__` and how do they interact with overloading?

**A:** These two methods handle attribute access differently. `__getattr__` is called as a **fallback** when normal attribute lookup fails (AttributeError). `__getattribute__` is called for **every** attribute access, unconditionally. This distinction is critical for implementing dynamic attribute resolution and operator-like behavior.

`__getattr__` is useful for: lazy loading of expensive attributes, providing a default value for missing attributes, implementing a dynamic interface where attribute names map to database queries, and proxy objects that delegate to wrapped objects. It only fires when the attribute doesn't exist through normal means (instance dict, class dict, base classes).

`__getattribute__` intercepts everything, including existing attributes. It is called with the attribute name and must look up the attribute itself (typically via `super().__getattribute__(name)` or `object.__getattribute__(self, name)`). This is more powerful but also more dangerous — an infinite loop occurs if you accidentally access an attribute inside `__getattribute__`.

```python
class DynamicProxy:
    def __getattr__(self, name):
        # Only called when normal lookup fails
        return getattr(self._wrapped, name)

    def __getattribute__(self, name):
        # Called for EVERY attribute access
        if name.startswith('_'):
            return super().__getattribute__(name)
        return getattr(self._wrapped, name)
```

For operator overloading, `__getattr__` enables cases where you want operator behavior on dynamically-named methods. For example, if `obj` doesn't have a `__add__` method but `__getattr__` returns a callable, Python still won't call it for `+` — Python checks the type for `__add__` via the type's MRO, not via `__getattr__`. So `__getattr__` cannot be used to implement operator overloading directly.

## Q24: What is the difference between `operator*` for dereference and multiplication in C++?

**A:** In C++, the `*` symbol has two distinct overloaded meanings: the **unary dereference operator** (dereferencing a pointer) and the **binary multiplication operator**. The compiler distinguishes them by arity — unary `*` takes one operand (the pointer), binary `*` takes two operands (the multiplicands).

For the unary dereference operator (`operator*()`), the canonical use is in **iterators** and **smart pointers**. A well-behaved iterator's `operator*()` returns a reference to the pointed-to element. Smart pointers like `std::unique_ptr` define `operator*()` to return a reference to the managed object and `operator->()` to return the raw pointer for member access.

```cpp
class SmartPtr {
    T* ptr;
public:
    T& operator*() const { return *ptr; }
    T* operator->() const { return ptr; }
};
```

The binary `operator*` for multiplication follows the standard idiom: it should be a free function that multiplies two values and returns the result. For commutative operations, it's typical to define a member `operator*=(const T&)` for in-place multiplication, and a free `operator*` that copies the left operand, applies `*=`, and returns the result.

A subtle issue: if you have an iterator-like class that supports both dereference and multiplication, the compiler resolves `*ptr` as dereference (unary) and `a * b` as multiplication (binary) based on context and operand count. No ambiguity arises because the arity is different. However, for a class that supports unary `operator+` and binary `operator+`, overload resolution depends on the number of arguments.

## Q25: What is the role of `explicit` keyword in C++ operator overloading?

**A:** The `explicit` keyword prevents implicit conversions through constructors and conversion operators. In the context of operator overloading, `explicit` on a conversion operator (like `explicit operator bool()`) prevents the class from being implicitly converted in unexpected contexts.

Without `explicit`, a class with `operator bool()` can be implicitly converted to `bool` anywhere, including in arithmetic expressions. This leads to surprising behavior — a custom string or matrix type might be used as an integer in `a + b`. Marking the conversion `explicit` restricts it to contexts where a boolean is explicitly required: `if`, `while`, `for` conditions, `&&`, `||`, `!`, and ternary operator (in C++11 and later).

```cpp
class MyBool {
    bool value;
public:
    explicit operator bool() const { return value; }
};

MyBool b;
if (b) { }          // OK — explicit conversion in boolean context
// int x = b + 1;   // Error — implicit conversion not allowed
```

C++11 extended `explicit` to conversion functions, which was a crucial addition. Before C++11, implicit conversions through operators were a major source of bugs. Now, the rule is: **always mark conversion operators `explicit`** unless you specifically want implicit conversions.

For constructors, `explicit` prevents single-argument constructors from acting as implicit conversion operators. `explicit MyClass(int x)` prevents `MyClass m = 5;` but allows `MyClass m(5);` and `m = MyClass(5);`. This prevents accidental conversions that can make code confusing and introduce performance overhead from unexpected temporaries.

## Q26: What is the thin wrapper problem in C++ operator overloading?

**A:** The **thin wrapper problem** occurs when an overloaded operator adds overhead compared to the equivalent function call. This typically happens when an operator creates unnecessary temporaries, makes copies, or prevents inlining. The most common scenario is `operator+` returning by value when the underlying operation is simple.

Consider a `Matrix` class where `operator+` creates a new matrix, copies elements, and returns by value. If you chain `a + b + c`, two temporaries are created. Each temporary involves allocation and copying. A naive implementation of `a + b` might allocate memory, copy all elements, perform addition, and then the temporary is destroyed — three extra memory operations.

The solution is **return value optimization** (RVO) and move semantics. In C++11 and later, returning a local variable from a function triggers move semantics (if a move constructor exists) or copy elision. Combined with the copy-and-swap idiom, `operator+` can be efficient. Modern compilers also apply NRVO (named return value optimization) aggressively.

A practical mitigation is to prefer `operator+=` for in-place operations and use `operator+` only when a new object is truly needed. For heavy objects, consider expression templates (a metaprogramming technique that defers evaluation until the final assignment) — though this adds significant complexity. Libraries like Eigen use expression templates to make `a + b * c` evaluate as a single pass without temporaries.

## Q27: How does C++20's `<=>` interact with the `==` operator and rewrite rules?

**A:** In C++20, the comparison model was significantly revised. The `<=>` operator returns a comparison result, and `==` is now a first-class operator that can be rewritten by the compiler. The key rewrite rule is: if you define `operator==` as a non-member function, the compiler can rewrite `a != b` as `!(a == b)`, `a < b` as `(a <=> b) < 0`, and so on.

Specifically, if `operator<=>` is defined but `operator==` is not, the compiler generates `operator==` from `<=>` by checking `(a <=> b) == 0`. This means defining `<=>` automatically gives you `==` for free. If you define both, the explicit `==` takes precedence.

The rewrite rules apply at the call site, not at the definition site. When the compiler sees `a != b`, it looks for `operator!=` first. If none is found, it rewrites to `!(a == b)`. This enables libraries to define only `==` and get `!=` for free, which was not possible before C++20.

```cpp
struct Point {
    int x, y;
    auto operator<=>(const Point&) const = default;
    // Compiler generates: ==, !=, <, <=, >, >=
};
```

A subtle issue: rewriting does not apply recursively. If `a == b` is rewritten to `b == a` (via a non-member `operator==`), the compiler does not then rewrite `b == a` further. Also, rewriting only applies to operators with known signatures — custom operators like `operator~` are not affected by rewrite rules.

## Q28: What is the comma operator overload behavior in C++ and why is it discouraged?

**A:** The **comma operator** `,` in C++ has a well-defined evaluation order (left-to-right) and sequencing guarantees. When overloaded, it loses these guarantees — the compiler is no longer required to evaluate operands in order or to sequence the evaluations. This can lead to undefined behavior in code that relies on the sequencing.

For example, `f(a, b)` where `a` and `b` are comma-overloaded might evaluate `b` before `a` if the compiler reorders the function call arguments. The C++ standard specifies that overloaded comma does **not** preserve the sequencing guarantee of the built-in comma. This means `a, b` with overloaded comma is not guaranteed to evaluate `a` before `b`.

The standard library and many algorithms rely on the comma operator's sequencing (e.g., in `for` loops: `for (init; cond; expr)` where `expr` uses comma). If a type used with such code has an overloaded comma, the behavior changes subtly.

For these reasons, overloading the comma operator is strongly discouraged. It violates the principle of least surprise. The only legitimate use case might be domain-specific DSLs (embedded languages in C++), but even there, alternatives like overloaded `|` or `>>` operators are preferred because they do not have the same sequencing expectations.

## Q29: How do Python's `__iter__`, `__next__`, and `__getitem__` work together for iteration?

**A:** Python's iteration protocol has multiple layers that interact. When you call `iter(obj)`, Python first checks for `__iter__()`. If present, it returns an iterator object that must implement `__next__()`. If `__iter__` is not defined, Python falls back to `__getitem__()`, calling it with integer indices starting from 0, and stops when `IndexError` is raised.

This fallback mechanism means any class with `__getitem__` that accepts integer indices is automatically iterable. This is a form of duck typing. For example, a custom list class that implements `__getitem__(self, index)` can be used in `for` loops, `list()` calls, and comprehensions without implementing `__iter__`.

```python
class NumberSeries:
    def __init__(self, max_val):
        self.max_val = max_val
    def __getitem__(self, index):
        if index >= self.max_val:
            raise IndexError
        return index * index
    # No __iter__ needed — __getitem__ provides iteration
```

The interaction with operators: `__getitem__` also enables subscript syntax (`obj[key]`), so a class implementing it gets both indexing and iteration. However, implementing `__iter__` is generally more efficient because `__getitem__` requires try/except for `IndexError` on every access, and the iterator protocol can maintain state more efficiently.

For operator-like patterns, `__getitem__` combined with `__setitem__` enables container behavior. The `collections.abc.Sequence` ABC uses `__getitem__` to provide `__contains__`, `__iter__`, `__reversed__`, `index`, and `count` automatically.

## Q30: What is the difference between `operator<<` for output and bitwise left shift?

**A:** The `<<` symbol in C++ serves two purposes: **bitwise left shift** for integral types, and **stream insertion** for `std::ostream`. These are distinct operations with different semantics, but they share the same operator token. The compiler resolves which one to use based on operand types.

For integral types, `<<` shifts bits left (or right if the left operand is `std::ostream`). For `std::ostream`, `operator<<` is a member function (or free function, depending on the type being output). The overload resolution selects the correct version based on the left-hand operand: if it's `std::ostream`, the stream insertion version is used; if it's an integral type, the bitwise version is used.

```cpp
std::cout << 42;              // stream insertion: prints "42"
int x = 1 << 3;              // bitwise shift: x = 8
std::cout << myObject;        // stream insertion via operator<<(ostream&, MyType)
```

The common pattern for custom types is a free function: `std::ostream& operator<<(std::ostream& os, const MyType& obj)`. This is a free function because the left operand is `std::ostream`, not your class. Making it a `friend` of your class allows access to private members without exposing a public getter for every field.

A subtle issue: if you have a class with both `operator<<` (bitwise) and `operator<<` (stream insertion), the compiler resolves based on the left operand's type. This works correctly but can be confusing in template code where the type might be ambiguous.

## Q31: What is the Python `__bytes__` and `__format__` special method protocol?

**A:** These methods extend string-like behavior beyond `__str__` and `__repr__`. `__bytes__(self)` is called by `bytes(obj)` and returns a bytes object representing the binary form of the object. `__format__(self, format_spec)` is called by `format(obj, spec)` and f-string formatting, enabling custom formatting with format specifications.

`__bytes__` is useful for objects that have a binary representation, like network packets, encoded data, or binary file formats. The built-in `bytes()` function calls `__bytes__` on its argument if defined, falling back to the iteration protocol.

```python
class IPAddress:
    def __init__(self, addr):
        self.addr = tuple(int(x) for x in addr.split('.'))
    def __bytes__(self):
        return bytes(self.addr)
    def __format__(self, format_spec):
        if format_spec == 'dotted':
            return '.'.join(str(x) for x in self.addr)
        return str(self.addr)
```

`__format__` enables the format mini-language for custom types. The `format_spec` string is passed directly from the f-string or `format()` call. This allows type-specific formatting without adding methods like `to_dotted_string()`. The built-in `format()` function calls `type(obj).__format__(obj, format_spec)`.

The interaction with operators: `__format__` is not an operator in the traditional sense, but it participates in the string formatting operator `%` (old-style) and the f-string `{expr:spec}` syntax. The `__mod__` operator (`%`) can also be overloaded for custom string formatting, though f-strings are preferred in modern Python.

## Q32: How does C++ handle operator overloading with templates and name lookup?

**A:** When operators are overloaded and used in template code, name lookup becomes complex. The compiler must find the correct operator for each instantiation of the template. This involves **two-phase name lookup**: in phase 1 (at template definition time), non-dependent names are looked up; in phase 2 (at instantiation time), dependent names are looked up based on the template arguments.

For operator overloading in templates, the critical issue is that `operator+` for a type `T` must be findable by ADL (argument-dependent lookup) when the template is instantiated. This means the operator must be either a member of the type, a free function in the same namespace as the type, or a friend function visible through ADL.

```cpp
template<typename T>
T add(T a, T b) {
    return a + b;  // dependent on T — found via ADL at instantiation
}
```

A common pitfall is defining an operator in a namespace that is not the same as the type's namespace. ADL will not find it, and the template will fail to compile when instantiated. The solution is to define operators in the same namespace as the type they operate on.

C++20's `<=>` operator has special rules for name lookup: the compiler looks for `operator<=>` in the associated namespaces of both operands. If both operands are the same type, ADL finds the member or free function. If they are different types, the compiler searches both namespaces and considers candidates from both.

## Q33: What is the C++ `operator->` overload and what are its return-type requirements?

**A:** The arrow operator `->` has special overload rules. It must be either a **member function** returning a pointer to a class type, or a **non-member function** (free function) returning a pointer. The compiler repeatedly applies `->` until it reaches a raw pointer, then accesses the member.

For member functions: `T* operator->() const { return ptr; }` — the compiler calls `obj->member` as `(obj.operator->())->member`. If `operator->` returns another object with its own `operator->`, the compiler applies it again recursively.

For free functions: the compiler applies `a->b` as `(operator->(a))->b`. The function must return a pointer to an object that has the `b` member.

```cpp
class SmartPtr {
    T* raw;
public:
    T* operator->() const { return raw; }
};
SmartPtr p;
p->method();  // becomes (p.operator->())->method() = raw->method()
```

The canonical use case is **smart pointers**. `std::unique_ptr`, `std::shared_ptr`, and `std::weak_ptr` all implement `operator->` to forward member access to the managed object. Iterators also implement `operator->` to access pointee members.

An important subtlety: the return type must be a pointer to something (either a raw pointer or an object with `operator->`). If you return a reference, the compiler will not apply `->` recursively. Also, `operator->` is typically marked `const` because it does not modify the smart pointer itself — only the accessed member can modify the pointee.

## Q34: What are the edge cases of Python's `__bool__` and logical operators `and`, `or`, `not`?

**A:** Python's `and`, `or`, and `not` use `__bool__` to determine truthiness. `__bool__(self)` returns `True` or `False` and is called by `bool(obj)`, `if obj:`, `while obj:`, and logical operators. If `__bool__` is not defined, Python falls back to `__len__` — a non-zero length means truthy.

The edge case: `and` and `or` do **not** return `True`/`False` — they return one of their operands. `a and b` returns `a` if `a` is falsy, otherwise `b`. `a or b` returns `a` if `a` is truthy, otherwise `b`. This is **short-circuit evaluation** with value return, not boolean evaluation.

```python
class Threshold:
    def __init__(self, value):
        self.value = value
    def __bool__(self):
        return self.value > 0

t = Threshold(-1)
result = t and "positive"  # returns t (the Threshold object), not False
```

This can lead to confusing behavior. If you expect `and` to return a boolean, you get the object itself. The `not` operator always returns `True` or `False` (a boolean), unlike `and`/`or`.

Another edge case: `__len__` returning 0 means falsy, but `__bool__` takes precedence. If both are defined, only `__bool__` is called. If you want an object to be falsy when empty, define either `__bool__` (for complex logic) or `__len__` (for container-like objects). If you want an object to always be truthy, define `__bool__` to return `True`.

## Q35: What is the rule of zero, rule of three, rule of five, and rule of zero-ten (C++11)?

**A:** These rules govern when you need to define special member functions (constructor, copy constructor, copy assignment, move constructor, move assignment, destructor):

- **Rule of Zero**: If your class does not manage resources directly, don't declare any of the six special members. Let the compiler generate correct defaults. Use RAII types (`std::string`, `std::vector`, smart pointers) for resource management.

- **Rule of Three**: If you define any of {destructor, copy constructor, copy assignment}, you should define all three. This is because if you need a custom destructor, you likely manage resources that need custom copy behavior.

- **Rule of Five** (C++11): If you define any of {destructor, copy constructor, copy assignment, move constructor, move assignment}, define all five. Move operations allow efficient transfer of resources.

- **Rule of Zero**: The modern recommendation — design classes so they contain RAII members and need **none** of the special members. This is the safest and simplest approach.

```cpp
// Rule of zero — no special members needed
class Person {
    std::string name;
    std::vector<std::string> hobbies;
    std::unique_ptr<Profile> profile;
    // Compiler-generated defaults are correct
};
```

When you must manage resources (e.g., a custom allocator, a raw file handle), follow the Rule of Five. The copy constructor and copy assignment perform deep copies, the move constructor and move assignment transfer ownership (nulling the source), and the destructor frees the resource. This is what the copy-and-swap idiom (Q21) achieves efficiently.

## Q36: What is Python's `__init_subclass__` and how does it relate to special method contracts?

**A:** `__init_subclass__(cls, **kwargs)` is called when a class is subclassed. It allows a base class to customize subclass creation without writing a metaclass. The base class defines `__init_subclass__` as a classmethod, and it receives the new subclass as `cls`.

This is useful for: registering subclasses in a registry, validating subclass attributes, injecting default methods or class-level behavior, and enforcing invariants on subclasses. It replaces the common metaclass pattern for simple class customization.

```python
class Plugin:
    _registry = {}
    def __init_subclass__(cls, plugin_name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        name = plugin_name or cls.__name__
        Plugin._registry[name] = cls

class MyPlugin(Plugin, plugin_name="my_plugin"):
    pass

assert Plugin._registry["my_plugin"] is MyPlugin
```

The interaction with special methods: `__init_subclass__` is called before `__set_name__` (for descriptors) and after `__class_getitem__` (for generics). It allows you to transform the subclass before it is fully created. You can add methods, change the class dict, or even replace the class entirely.

This relates to special method contracts because special methods are looked up on the **type**, not the instance. `__init_subclass__` can modify a subclass's type to inject special method implementations. For example, a base class could add `__hash__` to all subclasses that don't define their own, maintaining the hash contract.

## Q37: What happens when you mix overloaded operators from different class hierarchies in C++?

**A:** When you mix operators from different hierarchies, overload resolution considers all candidates from both hierarchies. If class `A` defines `operator+(A, B)` and class `B` defines `operator+(B, A)`, the compiler must choose the best match. This can lead to ambiguity if both conversions are equally good.

Consider: `A a; B b; auto c = a + b;`. The compiler looks for `operator+(A, B)` (member of A or free function), `operator+(B, A)` (member of B or free function), and built-in `+`. If only `A::operator+(B)` exists, it is selected. If both `A::operator+(B)` and `B::operator+(A)` exist, the call is ambiguous.

The solution is to provide a single, non-ambiguous `operator+` that works for the combination, or to use `explicit` conversion operators to prevent implicit conversions. Another approach is to define the operator as a free function in a common namespace visible to both types.

```cpp
class A { public: A operator+(const B&) const; };
class B { public: B operator+(const A&) const; };
// a + b — ambiguous if both are viable

// Fix: provide a free function
A operator+(const A& lhs, const B& rhs); // or make one conversion explicit
```

This is a strong argument for using free functions over member functions for symmetric operators. Free functions participate in ADL from both namespaces, giving the compiler more candidates and reducing ambiguity. The trade-off is that free functions need `friend` access to private members.

## Q38: What is the Python `__del__` finalizer and how does it differ from `__delattr__`?

**A:** `__del__(self)` is the finalizer — called when the object is garbage collected. `__delattr__(self, name)` is called when `del obj.attr` is executed. They serve completely different purposes despite similar names.

`__del__` is unreliable for resource cleanup because Python does not guarantee when (or even if) it will be called. The garbage collector may never run, or it may run in a different order than expected. The `atexit` module, context managers (`__enter__`/`__exit__`), or `try`/`finally` blocks are preferred for deterministic cleanup.

`__delattr__` is the complement to `__getattr__` and `__setattr__`. It is called for the `del` statement on an attribute. If not defined, the default implementation raises `AttributeError` for existing attributes. You can override it to implement custom deletion behavior:

```python
class Config:
    def __delattr__(self, name):
        if name in self.__dict__:
            print(f"Deleting {name}")
            del self.__dict__[name]
        else:
            raise AttributeError(name)
```

The interaction with operators: `__del__` is part of the special method protocol for lifecycle management, while `__delattr__` is part of the attribute access protocol. `__del__` has no corresponding operator — it is invoked implicitly by the garbage collector. `__delattr__` corresponds to the `del` statement operator on attributes.

A common confusion: `__del__` is not a destructor in the C++ sense. Python uses reference counting with a cyclic garbage collector. `__del__` is called when the reference count drops to zero (or during cyclic GC), but it may not be called at all if there are reference cycles and the GC is not run.

## Q39: How does the C++ `operator()` work with multiple overloads and `const` correctness?

**A:** The call operator can have multiple overloads with different parameter lists and `const` qualifications. This allows a single functor to handle different argument types and to work on both const and non-const instances.

For a functor that supports multiple call patterns:

```cpp
class Formatter {
    std::string prefix;
public:
    void operator()(int val) const {
        std::cout << prefix << val << std::endl;
    }
    void operator()(const std::string& s) {
        prefix = s;  // modifies state — non-const
        std::cout << "Prefix set" << std::endl;
    }
};
```

The `const` version can be called on both `const Formatter` and non-const `Formatter` objects. The non-const version can only be called on non-const objects. This follows the same const-correctness rules as any member function.

A common pattern in STL is to use `const`-qualified `operator()` for predicates and comparators. `std::sort` expects a callable whose `operator()` is `const`-qualified (or doesn't modify state), because the comparator may be called in arbitrary order and with temporary copies. `std::less<T>` has a `const` `operator()`.

C++14 added **generic lambdas**, which use `auto` parameters. The compiler generates a functor with a template `operator()`:

```cpp
auto add = [](auto a, auto b) { return a + b; };
// Equivalent to:
struct Add {
    template<typename T, typename U>
    auto operator()(T a, U b) const { return a + b; }
};
```

This allows the functor to work with any types that support `+`. The `const` qualifier on the lambda's `operator()` means the lambda cannot capture and modify state — use `mutable` to allow mutation.

## Q40: What is the difference between `operator==` being a member vs free function in C++20?

**A:** In C++20, the choice between member and free `operator==` has significant implications for overload resolution and rewrite rules. A **member** `operator==` takes one explicit parameter (the right-hand side). A **free** `operator==` takes two explicit parameters.

The key difference: a **non-member** `operator==` is considered for both `a == b` and `b == a` (via rewrite rules). A member `operator==` is only considered for `a == b` where `a` is the implicit object. This means if you define `operator==` as a member of `A`, then `a == b` works (calls `A::operator==(b)`), but `b == a` is not considered unless `B` also has an `operator==`.

```cpp
// Member form
struct A { bool operator==(const A&) const = default; };
// a == b — works (A::operator==(b))
// b == a — works (because default <=> generates it)

// Free form
struct B { friend bool operator==(const B&, const B&) = default; };
// a == b — works (rewritten from b == a or direct call)
```

With defaulted `<=>`, both forms produce all six comparison operators. But for non-defaulted comparisons, the free function form is more flexible because it enables symmetric comparisons across different types.

C++20's rewrite rules: the compiler rewrites `a != b` as `!(a == b)` if no explicit `!=` is found. It rewrites `a < b` as `(a <=> b) < 0` if no explicit `<` is found. These rewrites only apply at the call site, and the compiler must not rewrite in a way that changes semantics.

## Q41: What is the Python `__index__` method and when is it called?

**A:** `__index__(self)` is called when an object is used in a context that requires an integer — specifically, as an argument to `operator[]` (subscript with slices), `operator<<`, `operator>>`, `bin()`, `oct()`, `hex()`, and as an index in a list or array. It must return an `int`.

This is distinct from `__int__`, which is called by `int(obj)`. `__index__` is only called in contexts where an **integer** (not just an int-like object) is required by the Python interpreter itself. For example, `a[b:c]` calls `b.__index__()` and `c.__index__()` to convert them to integers for the slice.

```python
class SafeIndex:
    def __init__(self, val):
        self.val = val
    def __index__(self):
        if self.val < 0:
            raise ValueError("Negative index")
        return self.val
    def __int__(self):
        return self.val

idx = SafeIndex(5)
lst = [0, 1, 2, 3, 4, 5]
print(lst[idx])  # Uses __index__ to get integer 5
```

The difference between `__index__` and `__int__`: `__index__` is called by the interpreter for operations that need an exact integer (subscript, bitwise operations). `__int__` is called by `int()` and other explicit conversions. If `__index__` is not defined, `__int__` is tried as a fallback (with a deprecation warning in Python 3.10+, and an error in Python 3.12+).

This relates to operator overloading because subscripting (`[]`) and bitwise operations (`<<`, `>>`, `&`, `|`, `^`) rely on `__index__` for type coercion. A class that implements `__index__` can be used as an index in list comprehensions, array access, and slicing.

## Q42: What is the exception safety guarantee of overloaded operators in C++?

**A:** Operator overloading should follow the same exception safety guarantees as regular functions. The four levels are: **nothrow** (never throws), **strong guarantee** (commit or rollback — if an exception occurs, state is unchanged), **basic guarantee** (if an exception occurs, invariants are maintained and no resources leak), and **no guarantee** (anything can happen).

For `operator+`, the strong guarantee is preferred: if the operation fails, the original operands are unchanged. This is naturally achieved by the copy-and-swap idiom — a copy is made (may throw), the copy is modified (may throw), and the original is swapped with the copy (noexcept). If anything throws, the original is untouched.

For `operator+=`, the basic or strong guarantee is expected. If the operation allocates memory (e.g., appending to an internal vector), a `std::bad_alloc` may be thrown. The class should maintain invariants after the exception — typically by not modifying state until the allocation succeeds.

```cpp
BigInt& BigInt::operator+=(const BigInt& rhs) {
    BigInt tmp = *this;  // strong guarantee: copy first
    tmp.add_impl(rhs);   // may throw
    swap(*this, tmp);    // noexcept
    return *this;
}
```

The `noexcept` specifier is critical for move constructors and move assignment operators. A move constructor that can throw may not be used by STL containers in all situations (e.g., `std::vector` reallocation uses move-or-copy depending on `noexcept`). The standard practice is: move constructors should be `noexcept`, and move assignment should be `noexcept` if possible.

## Q43: How does Python's `__set_name__` work in descriptor protocols and operator-like behavior?

**A:** `__set_name__(self, owner, name)` is called by the metaclass `__init__` when a descriptor is created as a class attribute. It receives the owning class (`owner`) and the attribute name (`name`). This allows descriptors to know their name without being assigned to a variable manually.

This is primarily used in descriptor protocol implementations, which underpin Python's method binding, `property`, `classmethod`, `staticmethod`, and custom attribute access. Descriptors define `__get__`, `__set__`, and/or `__delete__` to control attribute access.

```python
class Validated:
    def __init__(self, validator):
        self.validator = validator
    def __set_name__(self, owner, name):
        self.name = name
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)
    def __set__(self, obj, value):
        if not self.validator(value):
            raise ValueError(f"Invalid value for {self.name}")
        obj.__dict__[self.name] = value
```

The interaction with operators: descriptors enable "operator-like" behavior for attribute access. When you write `obj.attr`, Python checks if `type(obj)` has a descriptor for `attr` in its MRO. If so, `descriptor.__get__(obj, type(obj))` is called. This is how `property` works — `property` is a descriptor that intercepts `__get__`, `__set__`, and `__delete__`.

`__set_name__` allows descriptors to be self-naming, eliminating the need for manual name assignment. Before `__set_name__` (Python 3.5), descriptors had to be explicitly assigned to variables to know their names.

## Q44: What is the operator precedence difference between C++ `&&` and `||` when overloaded?

**A:** When `&&` and `||` are overloaded in C++, they lose their **short-circuit evaluation** guarantee. The built-in `&&` and `||` evaluate the left operand first and only evaluate the right if needed. Overloaded versions are regular function calls — both operands are evaluated before the function is called (sequencing rules are less strict than built-in short-circuiting).

This is a critical pitfall. Consider:

```cpp
class SafePtr {
    T* ptr;
public:
    bool operator!() const { return ptr == nullptr; }
    bool operator&&(const SafePtr& rhs) const {
        return ptr && rhs.ptr;  // both operands already evaluated!
    }
};

SafePtr a(nullptr), b(valid);
if (a && b) { }  // built-in && checks a first, may skip b
// Overloaded && evaluates BOTH a and b, then calls operator&&
```

With overloaded `&&`, the right operand is always evaluated. This can cause side effects or exceptions if the right operand has a side effect or dereferences a null pointer. The C++ standard specifically notes that overloaded `&&` and `||` do not preserve short-circuiting.

For this reason, overloading `&&` and `||` is strongly discouraged. If you need logical operations, use named functions like `and_then()` or `or_else()`. Some libraries (like Boost.Spirit for parser combinators) overload `&&` and `||` for DSL purposes, but they accept the loss of short-circuit semantics as a deliberate trade-off.

## Q45: What is the Python `__class_getitem__` method and how does it relate to generic types?

**A:** `__class_getitem__(cls, params)` is called when a class is subscripted: `MyClass[int]`. It enables generic types using the `[]` syntax, introduced in Python 3.7+ (PEP 560). It replaces the older `__getitem__` on the metaclass for subscript behavior.

This is how `list[int]`, `dict[str, int]`, and custom generic types work. The method receives the class and the subscript parameters (which can be a single type, a tuple of types, or `None`):

```python
class Registry:
    _registry = {}
    def __class_getitem__(cls, item):
        if item not in cls._registry:
            raise KeyError(f"No plugin registered for {item}")
        return cls._registry[item]

class MyPlugin:
    pass

Registry[MyPlugin]  # calls Registry.__class_getitem__(MyPlugin)
```

The `@dataclasses.dataclass` and `typing.Generic` use `__class_getitem__` to enable parameterized types. `list[int]` calls `list.__class_getitem__(int)`, which returns a `types.GenericAlias` object. This alias is used for type hints and runtime type checking.

In Python 3.9+, built-in types support `[]` natively: `list[int]`, `dict[str, int]`, `tuple[int, ...]`. This is because their `__class_getitem__` methods were added. For custom classes, you can define `__class_getitem__` as a `@classmethod`:

```python
class Container:
    @classmethod
    def __class_getitem__(cls, params):
        return type(f'{cls.__name__}[{params}]', (cls,), {'_type_param': params})
```

The interaction with operators: `[]` is the subscription operator. When applied to a class (not an instance), it triggers `__class_getitem__`. This is distinct from `__getitem__` (instance subscript) and `__init_subclass__` (subclass creation).

## Q46: What is the copy elision guarantee in C++ and how does it affect operator return values?

**A:** **Copy elision** is a compiler optimization that eliminates copies of return values and temporaries. C++17 made **guaranteed copy elision** (also called "mandatory copy elision" or "NRVO") a standard requirement for prvalue (pure rvalue) expressions. This means that returning a prvalue from a function never involves a copy, even without move semantics.

Before C++17, returning a local variable from a function would invoke the move constructor (or copy constructor if moves are not available). After C++17, the prvalue is "materialized" directly at the call site — no move or copy occurs.

```cpp
class Widget {
public:
    Widget() { /* allocation */ }
    Widget(const Widget&) { /* expensive copy */ }
    Widget(Widget&&) noexcept { /* move */ }
};

Widget create() {
    return Widget{};  // C++17: no copy, no move — prvalue directly at call site
    // Pre-C++17: move constructor called (or copy if move not available)
}

Widget w = create();  // Direct construction, no copy/move
```

For operator overloading, this means `operator+` returning a local variable benefits from guaranteed copy elision. The compiler constructs the result directly at the destination. This makes return-by-value from operators efficient and eliminates the need for manual optimization.

However, **NRVO** (named return value optimization) is still an optimization, not guaranteed. If you return a named local variable (not a prvalue), the compiler may or may not apply NRVO. Named variables can be moved but not elided in C++17. C++26 may introduce mandatory NRVO, but it is not yet standard.

## Q47: What are the implications of `noexcept` on C++ move operators and swap?

**A:** The `noexcept` specifier on move constructors, move assignment operators, and `swap` functions has profound implications for STL container behavior. `std::vector` and other containers check `noexcept` at compile time to decide whether to use move or copy during reallocation.

If a move constructor is `noexcept`, `std::vector` uses it during reallocation (when growing capacity). If not `noexcept`, it falls back to copy construction to maintain the strong exception guarantee. This means a `noexcept(false)` move constructor can cause significant performance degradation for vector-heavy code.

```cpp
class Widget {
    std::unique_ptr<Data> data;
public:
    Widget(Widget&& other) noexcept : data(std::move(other.data)) {}
    Widget& operator=(Widget&& other) noexcept {
        data = std::move(other.data);
        return *this;
    }
};
```

The `swap` function should also be `noexcept` because it is used by the copy-and-swap idiom and by containers to exchange elements efficiently. `std::swap` uses `noexcept` move operations when available: it moves elements if the move constructor and move assignment are both `noexcept`.

For operator overloading, `noexcept` on `operator+=` or `operator-=` allows containers to use these operations more efficiently. If a compound assignment can throw, the container must use additional copies to maintain the strong guarantee. Making operations `noexcept` where possible enables better optimization throughout the standard library.

The `noexcept` operator (not the specifier) can be used to query whether an expression is `noexcept`: `noexcept(expr)`. This is used in SFINAE and concepts to constrain templates based on exception behavior.

## Q48: What is Python's `__radd__` vs `__add__` priority and how does it interact with inheritance?

**A:** When evaluating `a + b`, Python follows a specific priority. First, `type(a).__add__(b)` is tried. If it returns `NotImplemented`, then `type(b).__radd__(a)` is tried. If both return `NotImplemented`, `TypeError` is raised. Importantly, if `b` is a **subclass** of `a`, Python tries `b.__radd__` **first** — this ensures that subclass behavior takes precedence.

```python
class Base:
    def __add__(self, other):
        return "base add"
    def __radd__(self, other):
        return "base radd"

class Derived(Base):
    def __radd__(self, other):
        return "derived radd"

base = Base()
derived = Derived()
print(base + derived)  # "derived radd" — derived.__radd__ tried first
print(derived + base)  # "base add" — base.__add__ tried first (not overridden)
```

The key rule: if `type(b)` is a subclass of `type(a)`, then `b.__radd__(a)` is tried before `a.__add__(b)`. This is because subclasses may override reflected operations, and the subclass should have priority.

This can lead to surprising behavior with numeric types. If you define a `Matrix` class and want `int + Matrix` to work (via `Matrix.__radd__`), but `int.__add__(Matrix)` returns `NotImplemented` first, then Python falls back to `Matrix.__radd__(int)`. The reflected method allows the right-hand operand to handle operations it knows about.

For operator-like patterns in Python, always implement both `__add__` and `__radd__` if the operation is commutative. If non-commutative, only implement the appropriate one. The `functools.total_ordering` decorator (Q10) only works for comparison operators, not arithmetic.

## Q49: What is the `operator,` (comma) behavior in C++ range-for loops and how does overloading affect it?

**A:** The **range-based for loop** (`for (auto& x : container)`) in C++ relies on `begin()` and `end()` being found via ADL, not on the comma operator. However, understanding the interaction is important because the comma operator appears in the loop's desugaring and in some edge cases.

The range-for loop desugars to:

```cpp
auto&& __range = container;
auto __begin = begin(__range);
auto __end = end(__range);
for (; __begin != __end; ++__begin) {
    auto&& x = *__begin;
    // loop body
}
```

The comma operator is **not** involved in this desugaring. However, if a container's iterator has an overloaded comma operator, it could theoretically be triggered in other contexts. The more practical concern is that `begin()` and `end()` must be found via ADL or as members. If `operator,` is overloaded for the container, it does not affect range-for.

A real-world concern: if you overload `operator!=` for your iterator, the range-for loop uses it for comparison. If `operator!=` has unexpected behavior (e.g., throws or returns a non-bool), the loop may behave incorrectly. C++20 improves this by using `<=>` for range-for comparisons, which is more efficient.

The standard library's `std::ranges` (C++20) provides a more robust iteration mechanism that works with ranges, sentinels, and projections. It does not use `operator,` but uses concepts like `std::ranges::range` and `std::ranges::iterator_t` to constrain the types.

## Q50: What is the C++ overload resolution tie-breaker rules when multiple operators match?

**A:** C++ overload resolution follows a complex set of rules to select the best viable function when multiple operators match. The steps are: (1) collect all viable functions, (2) rank the best match for each parameter, (3) apply tie-breaker rules, and (4) if no unique best is found, the call is ambiguous.

The ranking system for each parameter conversion is: **exact match** (best), **promotion** (e.g., `char` to `int`), **standard conversion** (e.g., `int` to `double`), and **user-defined conversion** (worst). A function that requires a user-defined conversion on any parameter is worse than one that doesn't.

Tie-breaker rules when conversions are equally ranked:
1. A **non-template** function is preferred over a **template** function.
2. A **more specialized** template is preferred (partial ordering rules).
3. A **less-qualified** conversion is preferred (e.g., `int` to `long` over `int` to `const long`).
4. A **base class** conversion is preferred over a derived-to-base conversion.

```cpp
void f(int);       // non-template
void f(long);      // non-template
void f(double);    // non-template
f(42);  // Calls f(int) — exact match for int argument
```

For operators, the compiler also considers whether the operator is a member or free function. Member functions have an implicit `this` parameter, which affects the ranking. If a member `operator+(B)` and a free `operator+(A, B)` both exist and both require a conversion on the first argument, the member function is preferred because the implicit `this` is an exact match.

Understanding these rules is essential for writing predictable operator overloads. The safest approach is to minimize the number of implicit conversions and provide explicit operators for the types you expect to work with.

## Q51: What is expression templates and how do they make operator overloading efficient for linear algebra?

**A:** **Expression templates** is a C++ metaprogramming technique that defers operator evaluation to avoid creating temporary objects. Instead of returning a concrete matrix from `operator+`, it returns a lightweight proxy object that records the operation and its operands. The actual computation is postponed to the final assignment, where the compiler generates optimal code.

Without expression templates, `C = A + B * D` would create temporaries: `A + B` (temporary matrix), then `* D` (temporary matrix), then assign to `C`. Each temporary allocates memory and copies. With expression templates, `A + B * D` returns an expression object (like `MatrixExpr<AddExpr<Matrix, Matrix>, Matrix>`). The top-level expression is a computation graph.

The assignment operator then iterates over the expression, computing each element on the fly:

```cpp
template<typename L, typename R>
class AddExpr {
public:
    AddExpr(const L& l, const R& r) : lhs(l), rhs(r) {}
    double operator[](size_t i) const { return lhs[i] + rhs[i]; }
private:
    const L& lhs;
    const R& rhs;
};

template<typename L, typename R>
auto operator+(const L& lhs, const R& rhs) {
    return AddExpr<L, R>(lhs, rhs);
}
```

The result is that `C = A + B * D` computes a single pass over the matrices: for each element `i`, it computes `A[i] + B[i] * D[i]` directly into `C`. This eliminates all temporaries and yields performance comparable to hand-written loops. Libraries like **Eigen**, **Blitz++**, and **Boost.uBlas** use expression templates extensively.

The trade-offs: compile-time overhead (the type becomes long and complex), error messages become unwieldy, and cached evaluation is tricky. Expression templates also interact with auto (C++11) in a dangerous way — storing an `auto x = a + b;` keeps references to `a` and `b` alive, so if `a` or `b` go out of scope, `x` dangles.

## Q52: How does Python's `__getitem__` protocol support both indexing and iteration with slices?

**A:** Python's `__getitem__` is the single entry point for subscript access, and it also enables iteration via the fallback protocol. When you implement `__getitem__` on a class, you get three derived behaviors: (1) `obj[key]` indexing, (2) iteration via the iterator protocol fallback, and (3) support in unary operations like `len()` only if you also implement `__len__`.

The slice handling in `__getitem__` is a key design decision. When you write `obj[1:5]`, Python passes a `slice` object with `start`, `stop`, and `step` attributes (any of which may be `None`). If you write `obj[1:5, 2]`, you get a **tuple** `(slice(1, 5), 2)` — relevant for NumPy-style multidimensional indexing.

```python
class Grid:
    def __getitem__(self, key):
        if isinstance(key, tuple):
            rows, cols = key
            return self._get_submatrix(rows, cols)
        if isinstance(key, slice):
            return self._get_rows(key)
        return self._data[key]
```

The `slice.indices(length)` method converts a slice with `None`s into concrete integer values for a given sequence length. This is critical for implementing slicing correctly in custom containers.

For iteration, the critical point is that Python calls `__getitem__` with integers starting at 0 until it raises `IndexError`. This means a `__getitem__` that raises `IndexError` for out-of-range indices enables iteration but also enables negative-indexing support in `list` subclasses via the `index` protocol. The `collections.abc.Sequence` ABC formalizes this contract.

## Q53: What is the C++ NRVO (Named Return Value Optimization) and how does it interact with `operator+`?

**A:** **NRVO** is a copy/move elision optimization where the compiler constructs a named local variable directly in the caller's result storage, eliminating the copy and move that would otherwise occur when returning the local. NRVO is *allowed* (not guaranteed) since C++89 but only *mandatory* in limited prvalue contexts.

Consider:

```cpp
BigInt operator+(const BigInt& lhs, const BigInt& rhs) {
    BigInt result = lhs;
    result += rhs;
    return result;   // NRVO may apply here
}
```

Without NRVO, `return result` moves `result` into the return slot and then possibly moves into the caller's destination. With NRVO, `result` is constructed directly in the caller's storage, skipping both moves.

NRVO is only applicable when the returned expression is a **named local variable or parameter** (not a prvalue). It also fails when there are multiple return statements that return different names, or when the variable is returned along a path where its destructor must run before the function exits.

For operator overloading, the implications are significant:

- `return lhs` (copying a parameter) does not benefit from NRVO.
- `return lhs + rhs` (prvalue) benefits from **guaranteed copy elision** in C++17.
- `return result` (named local) may or may not benefit from NRVO depending on compiler.

C++26 is working on **mandatory NRVO**, but until then, benchmarking and compiler whitelist checks (like GCC's `-Wnrvo`) are the pragmatic tools. For maximum efficiency, prefer constructing the result as a prvalue: `return BigInt(/* params */)` rather than `return local;`.

## Q54: What is the difference between Python `__len__` and `operator bool` in terms of container protocols?

**A:** Python's `__len__` is the container size protocol, called by `len()`. It must return a non-negative integer. Python's `__bool__` is the truthiness protocol, called by `if obj:`. The connection: if `__bool__` is not defined, Python falls back to `__len__` — a container is truthy if and only if it has non-zero length.

The practical difference is subtle but important. If you define only `__len__`, the object's truthiness follows its length. If you define both, `__bool__` takes precedence — even a non-empty object can be false if `__bool__` returns `False`.

```python
class LazyList:
    def __init__(self, items):
        self.items = items
    def __len__(self):
        return len(self.items)  # len(lazy) works

class NonSubset:
    def __bool__(self):
        return False  # always falsy
    def __len__(self):
        return 5
```

Every container in Python (list, dict, str, set, tuple) defines both `__len__` and `__bool__`. The default `object.__bool__` returns `True`. Defining `__len__` without `__bool__` makes an object behave like a container — falsy when empty.

The edge case: `bool()` on a class instance **requires** either `__bool__` or `__len__`. If neither is defined, `bool(obj)` returns `True` (all objects are truthy by default). The `bool()` function never calls `__int__` or `__index__` as fallbacks since Python 3.0.

For C++ the analogous situation: `operator bool` must be `explicit` (Q25) to avoid accidental implicit conversions. Python has no such guard — `__bool__` is always used in truthiness contexts, but you must be careful with `and`/`or` returning operands (Q34).

## Q55: What is the ternary operator `?:` in C++ and why can't it be overloaded?

**A:** The ternary operator `cond ? expr1 : expr2` evaluates `cond`, then evaluates only one of `expr1` or `expr2` depending on the result. Its return type is computed via the compiler's type coercion rules: if `expr1` and `expr2` have the same type, that type is used; otherwise, common type conversions are applied.

C++ deliberately forbids overloading `?:`. The reasons: (1) `?:` has inspectable, well-defined type conversion rules that overloaders could break, (2) the short-circuit evaluation (only one branch is evaluated) would be lost in an overloaded function call — both operands would always be evaluated, (3) `?:` is a very low-level operator whose behavior is expected to be uniform across all types.

The `std::common_type` mechanism (C++14) formalizes what the ternary operator computes. When you write `a < b ? a : b`, this is equivalent in type to `std::common_type_t<decltype(a), decltype(b)>`. This is used in `std::min`, `std::max`, and functions that need to handle mixed types.

If you want the semantics of `?:` for your type, you cannot overload it. Instead, you provide `explicit operator bool`, and the compiler combines it with the built-in `?:` if conversions are appropriate. But you cannot change how `?:` treats your type.

The closest alternative: overload the `std::optional` comparison or provide member functions like `if_then_else(cond)`. In modern C++, `std::variant` and `std::visit` provide a more functional alternative to the ternary operator for type-dependent logic.

## Q56: How does Python's `__enter__` and `__exit__` context manager protocol relate to operator overloading?

**A:** The context manager protocol is invoked by the `with` statement: `with expr as var:`. When `expr` is evaluated, Python calls `expr.__enter__()`, whose return value is bound to `var`. When the block exits (normally or via exception), Python calls `expr.__exit__(exc_type, exc_value, traceback)`. This protocol is **not** an operator, but it uses the same special-method mechanism.

The `as` keyword in `with` is not an operator either — it's syntax for binding the result of `__enter__`. But the guarantee is: if `__enter__` succeeds, `__exit__` is always called, regardless of exceptions. This is the same guarantee that a destructor provides in C++.

```python
class DatabaseConnection:
    def __enter__(self):
        self.conn = connect()
        return self.conn
    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
        return False  # propagate exceptions
```

The return value of `__exit__` controls exception propagation: `False` (default) propagates the exception, `True` suppresses it. This allows context managers to swallow or translate exceptions.

The relationship to operators: `with expr as x` and `del obj` use syntax (keyword + syntax), while operators use punctuation (`+`, `==`, `[]`). Both are "special syntax" that triggers methods. The context manager protocol has the same exception safety implications as C++ destructors — cleanup should never throw.

A key implementation note (CPython): `__exit__` is called with positional `exc_type, exc_value, traceback`. The `contextlib.ContextDecorator` and `@contextmanager` decorator let you write context managers as generator functions, using `yield` as the boundary between `__enter__` and `__exit__`.

## Q57: What is the difference between `operator[]` returning a reference vs a pointer in C++?

**A:** Returning a `T&` from `operator[]` allows direct mutation: `arr[3] = 42;` works because the reference is returned to the storage slot. Returning a pointer `T*` requires dereferencing: `*arr[3] = 42;` — awkward and error-prone. Iterators and containers conventionally return references.

Returning a reference vs pointer matters for:
1. **Assignment**: `arr[i] = v` works with reference, needs `*` with pointer.
2. **Const-correctness**: a `const T&` returned from a `const` overload prevents mutation.
3. **Aliasing**: references cannot be re-bound; pointers can. This affects how callers use the result.
4. **Null**: references cannot be null; pointers can. Returning a reference signals the element exists.
5. **Proxy behavior**: if you want `arr[i] = v` to trigger side effects (bounds check, logging, dirty-tracking), returning a reference is insufficient — you need a **proxy**. A `T&` gives the caller direct access to storage, bypassing any interception.

```cpp
class LoggedVec {
    std::vector<int> data;
public:
    int& operator[](size_t i) {
        log_access(i);        // side effect happens on access
        return data[i];
    }
};
```

The proxy pattern (Q22) overrides this by returning a proxy object whose `operator=` captures the assignment and applies the side effect. The trade-off: proxies break generic code — `auto& x = arr[i];` binds a reference to a temporary proxy, causing a dangling reference. This is why proxy iterators (like `vector<bool>`) are controversial.

## Q58: What is Python's `__setattr__` and why does it risk infinite recursion with operator overloading?

**A:** `__setattr__(self, name, value)` intercepts all attribute assignments, including those in `__init__`. The default implementation writes to `self.__dict__`. If you override `__setattr__`, you must call `object.__setattr__(self, name, value)` or `super().__setattr__(name, value)` to avoid infinite recursion.

The recursion trap: if you write `self.name = value` inside `__setattr__`, Python calls `__setattr__` again, causing infinite recursion. The standard pattern:

```python
class Frozen:
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError(f"{name} is frozen")
        object.__setattr__(self, name, value)
```

The interaction with operators: `__setattr__` runs on every attribute assignment, including assignments made by descriptors, `namedtuple`-like classes, and operator overloads that modify fields. For example, an overloaded `__add__` that does `self.result = lhs + rhs` triggers `__setattr__("result", ...)`, which your overridden version intercepts.

Special methods like `__setattr__` are looked up on the type, not the instance, which means instance-level monkey-patching of `__setattr__` does not work (a known CPython limitation). This is why dynamic attribute interception belongs in `__getattribute__` and `__setattr__`.

The safe rule: always use `object.__setattr__` explicitly for the actual write inside a custom `__setattr__`, and reserve custom logic for validation, logging, or constraints (immutability, frozendataclasses, etc.).

## Q59: How do C++ `operator delete` sized variants and placement new interact with operator overloading?

**A:** C++14 added **sized deallocation**: `void operator delete(void* ptr, std::size_t size)` and the array form. This tells the allocator how many bytes were allocated, enabling custom allocators to put metadata at the block header or to use distinct allocation pools. The compiler calls the sized form when it knows the size (i.e., when the static type determines the size). In practice, GCC ships sized deallocation `-fsized-deallocation`.

```cpp
class Pool {
public:
    static void* operator new(std::size_t size) {
        return pool_allocate(size);
    }
    static void operator delete(void* ptr, std::size_t size) noexcept {
        pool_deallocate(ptr, size);  // sized deallocation
    }
};
```

**Placement new** is a form of `operator new` that takes extra arguments beyond the size. The canonical forms: `new (address) T(args)` uses the **placement-new overload** `void* operator new(std::size_t, void* ptr)` — which discards the size and returns the existing pointer. You can also define a placement `operator new` with a custom argument list like `new (pool, hint) T()` with `void* operator new(std::size_t, Pool&, int hint)`.

Placement new does **not** allocate; it constructs an object at the given address. It requires explicitly calling the destructor: `ptr->~T();`. This is essential for pool allocators, in-place construction in memory-mapped regions, and `std::vector` internals (which use uninitialized-storage construct).

The interaction with overloading: `operator new[]` and `operator delete[]` must also be overloaded together; mixing new/delete forms (new `[]` for deallocation with non-`[]` delete) is undefined behavior. `std::allocator` (C++11) uses `::new` and `::delete` internally but with sized `operator delete` for efficiency.

## Q60: What is the Python operator module and how do its functions relate to special methods?

**A:** The `operator` module provides functional equivalents of all operator special methods. Each function maps 1:1 to a dunder: `operator.add(a, b)` calls `a + b`; `operator.getitem(seq, key)` calls `seq[key]`; `operator.attrgetter("x")` returns a callable that reads `.x`; `operator.itemgetter(1)` returns a callable that indexes `[1]`; `operator.methodcaller("method", arg)` returns a callable that calls `method(arg)`.

The module exists because functional programming in Python needs operators as first-class functions. `functools.reduce(operator.add, numbers)` requires `operator.add` — you cannot pass `+` directly. Similarly, `sorted(data, key=operator.itemgetter(0))` and `groupby(data, key=operator.methodcaller("lower"))` use the module.

```python
from operator import itemgetter, attrgetter, methodcaller
rows.sort(key=itemgetter(1))            # sort by column index 1
users.sort(key=attrgetter('name'))      # sort by attribute
extract = methodcaller('get', 'query')  # call paramized method
```

The module also mirrors the C-level protocol: `operator.concat`, `operator.contains`, `operator.countOf`, `operator.index`, `operator.invert`, `operator.ior`, etc. Each one corresponds exactly to the dunder invoked. For example, `operator.iadd(a, b)` does `a += b` (in-place add) and returns the resulting (possibly new) object.

This is important for interviews because it demonstrates that Python operators are *uniformly* special-method-driven, and the operator module is the ultimate proof that operators are just functions. It is also a great pattern for implementing small DSLs without explicit operator syntax.

## Q61: What is covariance/contravariance in the context of operator return types and virtual functions?

**A:** In C++ and Java, **covariance** refers to a virtual function that returns a *more derived type* than the base declaration. Java supports covariant return types for overriding: a subclass can narrow the return type. C++ also supports covariance (return type may be a pointer/reference to derived class), but only for pointer and reference returns.

For **operators**, covariance is not usually involved because overloaded operators are not virtual (in C++ and Java) and cannot be polymorphically dispatched. In Python, operators are dispatched via the type's `__getattr__`/`__getattribute__`-driven lookup, but the dunder itself is not virtual in the C++ sense.

Contravariance — allowing a parameter of a *less derived* type — is also unusual for operators. The general rule: operators are typically defined for concrete types rather than polymorphic bases, so variance rarely appears.

However, the *concept* matters for design. If you have `Base` and `Derived` and an operator that returns the object itself, consider whether it should return `Base&` or `Derived&`. This affects how callers can chain operations. A `clone()` that returns `Derived` (covariant) lets callers call `d.clone().derivedMethod()` without a cast. The same principle applies to operator return types.

In C++20, `auto operator<=>()` deduction with derived types is a subtle covariant-like situation: the `<=>` for a derived class, when defaulted, considers members including base subobjects. Design for covariance when your operator logically returns "the same kind of object" as its argument.

## Q62: What is the expression-templates danger with C++ `auto` and dangling references?

**A:** The biggest footgun in expression templates is combining them with `auto`. Because expression templates store references to their operands (const references), a deduction like:

```cpp
auto expr = a + b;   // Expr type holds const A&, const B&
// ... a or b destroyed ...
double val = expr[0];  // dangling reference — UB!
```

The expression object is transient by design — it is meant to be consumed in the same full expression (`double d = a + b;` or `C = A + B;`). When you `auto expr = a + b;`, you keep the proxy alive longer than its operands, and later uses reference destroyed objects.

The C++ remedy:
1. **Best practice**: never store expression templates in `auto`; only use them transiently.
2. Libraries like Eigen document this explicitly ("Your matrix must outlive the expression").
3. Some libraries (e.g., Boost) provide a "materialize" mechanism: `Matrix m = expr.eval();` to compute eagerly and detach.
4. Since C++14, some libraries constrain `auto` misuse with deleted overloads or static_asserts.

Conceptually this is identical to Python's `NotImplemented` vs a TruDanger hazard — but in C++ the hazard is lifetime, not dispatch. Know that expression templates optimize **complete expressions** and lose effectiveness as soon as the expression is captured.

The rule for interviews: "Expression templates are a compile-time optimization that trades complexity and lifetime-safety for fewer temporaries. Never capture the expression in `auto`; consume it immediately."

## Q63: How does Python's `__contains__` work and when does it fall back to iteration?

**A:** `__contains__(self, item)` implements the `in` operator. When you write `item in obj`, Python calls `type(obj).__contains__(obj, item)`. If `__contains__` is not defined and `obj` is iterable (has `__iter__` or `__getitem__`-based iteration), Python falls back to a linear scan: `any(x == item for x in obj)`.

The definition:

```python
class Membership:
    def __contains__(self, item):
        return item in self._store  # O(1) for dict-like store
```

Performance depends heavily on the data structure. For a `set` or `dict`, `in` is O(1) hashed lookup — not a linear scan. For a list, it is O(n). For a custom class, you control the algorithm. If your class wraps a `set`, delegate to `set.__contains__`; if it wraps a sorted structure, use `bisect`.

The fallback behavior is important: any iterable (sequence or iterator) supports `in` even without `__contains__`, doing a linear scan. This is why `x in range(1_000_000_000)` is fast — `range.__contains__` does arithmetic O(1), not linear iteration.

Edge cases: `__contains__` participates in the `collections.abc` hierarchy via `Sized`, `Container`, etc. A `Container` ABC requires `__contains__`. If you implement `__getitem__` with integer keys but no `__contains__`, you still get `in` via iteration — but that iteration uses `__getitem__`, which may be expensive.

## Q64: In C++, what is the difference between overloaded `operator[]` returning `T&` and a proxy reference?

**A:** Returning a real `T&` means callers get direct access to the underlying storage slot. Returning a **proxy** (a lightweight object that *behaves like* a reference) means the slot is encapsulated and access is intercepted. Each has trade-offs.

Real reference `T&`:
- Fast, no extra object.
- Works with generic code (`std::swap(arr[0], arr[1])`).
- Also works with `auto& x = arr[i];` — binds to the slot.
- Cannot intercept assignment for side effects.

Proxy reference:
- Enables `matrix[i][j]`, `vector<bool>` bit addressing, or lazy-loading on access.
- Assignment `arr[i] = v` goes through proxy's `operator=`, so side effects (logging, write-back, dirty flags) can fire.
- Let's you return "not-quite-a-storage-slot" (e.g., a bit in a packed array).
- Breaks generic code: `auto& x = arr[i]` dangles because the proxy is a temporary; `std::swap` fails; `decltype` gives the proxy type, not `T&`.

The canonical example is `std::vector<bool>`, whose `operator[]` returns a `std::vector<bool>::reference` proxy (allowing each bool to be stored as one bit). This is so problematic that many codebases ban `vector<bool>` entirely.

For interviews, know the "proxy reference vs true reference" dilemma. If you design a container whose elements are not addressable (packed bits, computed values, views into compressed data), use a proxy and document why.

## Q65: What is the C++ `std::rel_ops::rel_ops` (from header `<utility>`) and why was it deprecated?

**A:** Pre-C++20, `std::rel_ops` provided global templates that synthesized `!=`, `>`, `<=`, `>=` from `==` and `<`. The idiomatic usage was `using namespace std::rel_ops;` in a scope, allowing types that defined only `==` and `<` to use the rest.

```cpp
#include <utility>
using namespace std::rel_ops;
struct Money { int units; };
bool operator==(const Money& a, const Money& b) { return a.units == b.units; }
bool operator<(const Money& a, const Money& b) { return a.units < b.units; }
// Now a != b works via rel_ops synthesis
```

It was deprecated in C++20 because the spaceship operator `<=>` and its **rewrite rules** (Q27) make it obsolete: defaulted/defined `<=>` generates all six comparisons automatically, with equal semantics and better performance (no extra function calls). `rel_ops` also had downsides: its operators were not `noexcept`, could be found via ADL polluting other namespaces, and injected into the global namespace only with an explicit `using` directive.

C++17 still supports it; C++20 deprecates it. The modern guidance: use `<=>` (Q11), or implement explicit comparison operators with the same patterns. Note the rewrite rules in C++20 also fix the "asymmetric comparisons" drawback of `rel_ops` — `a != b` in C++20 can rewrite to `!(a == b)` even for types that only define `==`.

This is a good interview example of how the standard library evolves when a language feature (spaceship) makes a library workaround obsolete.

## Q66: How does Python implement `a[start:stop:step]` for custom classes via `__getitem__` + `slice`?

**A:** Python passes extended slicing to `__getitem__` as a `slice(start, stop, step)` object. `start`, `stop`, `step` may each be `None`. For a custom class to support `a[...]`, you must detect the `slice` or `tuple` (for multidimensional) keys and translate them into concrete indices using `slice.indices(length)`.

`.indices(n)` returns a 3-tuple `(start, stop, step)` normalized for a sequence of length `n`, handling negative values and out-of-range clamping. Example:

```python
class MultiIndex:
    def __getitem__(self, key):
        if isinstance(key, slice):
            start, stop, step = key.indices(self._length)
            return [self._data[i] for i in range(start, stop, step)]
        if isinstance(key, tuple):
            return [self[i] for i in key]  # e.g., obj[0, 3, 7]
        return self._data[key]
```

The rules:
1. `a[i:j]` → `slice(i, j, None)`.
2. `a[i:j:k]` → `slice(i, j, k)`.
3. `a[1, 2]` → tuple `(1, 2)` (used by NumPy).
4. `a[...]` → `Ellipsis` (used by NumPy); you must handle it explicitly if supporting.
5. Negative step: indices computed correctly via `slice.indices`.
6. `__setitem__` with slices enables extended slice assignment/deletion.

For a true sequence, use `isinstance(key, (int, slice))` and delegate to the underlying list. For sparse or multidimensional types, handle `tuple` and `Ellipsis` explicitly. `collections.abc.Sequence` formalizes the `__getitem__` contract; slice support is optional but expected for sequence-like types.

## Q67: What are the C++ rules for overloading `operator new` vs overriding it on a per-class basis?

**A:** Per-class `operator new` is defined as a `static` member. When you write `new T(...)`, the compiler looks for `T::operator new(std::size_t)` first; if absent, it falls back to global `::operator new`. If a class uses `new[]`, it also looks for `T::operator new[]`.

Construction for `new MyClass`:
1. Call the class or global `operator new` to get raw memory.
2. Call the constructor on that memory.
3. Report to `new` handler / `std::bad_alloc` if allocation fails.

Per-class overloading lets you:
- Return memory from a custom pool, arena, or slab.
- Log allocations for debugging (`leak detection`).
- Implement aligned allocation (GCC/Clang `alignas`).
- Add per-object metadata.

The C++ rules:
- The `static` specifier is required (implicit even if omitted).
- Must return `void*`.
- Must take `std::size_t` first argument (bytes requested).
- May take additional payload arguments (placement forms).
- If `operator new` throws, the handler `std::set_new_handler` runs; a matching `operator delete` is needed for exception cleanup.
- Overriding class-level `operator new` does **not** change allocation for base classes, containers, or STL types used as members — those use their own or global.

Distinguish from **overriding** (virtual functions, runtime dispatch) vs **overloading** (same name, static resolution). For `new`/`delete`, this is overloading, not overriding — there is no polymorphism.

## Q68: What is Python's `__index__` vs `__int__` vs `__trunc__` for numeric protocols?

**A:** These three special methods form Python's numeric conversion protocol and serve distinct purposes:

- `__int__(self)`: called by `int(obj)`. Lossy conversion to `int` is allowed (e.g., `int(3.9) == 3`).
- `__index__(self)`: called by indexing and bitwise operations (`obj[0]`, `obj << 2`, `bin(obj)`). Must return an actual `int`. Used for **exact, lossless index** conversion.
- `__trunc__(self)`: called by `math.trunc(obj)`. Returns the truncation toward zero. For `float`, it returns `int`.

The interpreter's explicit sequence: for indexing and `range` arguments, it calls `operator.index(obj)` which looks for `__index__`, then `__int__`, then `__trunc__` (and if none exists, raises `TypeError`). In Python 3.10+, `__trunc__` is a separate fallback pathway with a deprecation warning.

```python
class FixedPoint:
    def __int__(self):
        return int(self.value // self.scale)
    def __index__(self):
        return int(self.value // self.scale)  # exact integer exponent/index
```

So `int(fp)` calls `__int__`; `fp[0]` requires `__index__`; `math.trunc(fp)` calls `__trunc__`. This tri-split avoids ambiguity: indexing needs exactness, `int()` allows lossy, `trunc` truncates. Classes like `numpy.int64` implement `__index__` to be usable as array indices.

## Q69: How does C++17's `std::variant` and pattern matching interact with operators?

**A:** `std::variant<T...>` is a type-safe union. Operators are defined so that equality (`==`, `!=`, `<`, etc.) works if the currently active alternative supports the corresponding operator, and comparisons between two variants require both to be the same alternative's type. Similarly, `std::visit` (a function, not an operator) dispatches based on the active alternative's type.

If you have `std::variant<int, Money> a, b;`, then `a == b` is well-formed if the active types match and support `==`. `std::rel_ops`-style fallbacks and the deprecation of synthesized comparisons complicate `variant` — in practice, you use `std::visit` with a generic lambda or overload set to dispatch based on type.

```cpp
auto visitor = [](const auto& x, const auto& y) {
    if constexpr (std::is_same_v<decltype(x), decltype(y)>)
        return x == y;
    else
        return false;
};
bool eq = std::visit(visitor, a, b);  // type-safe comparison
```

C++23/26 pattern matching (`std::inspect`) is experimental; current idiomatic code uses `std::visit` with generic lambdas. If you overload operators on a `variant` type directly, refer to the active alternative inside via `std::get`/`std::holds_alternative`.

The main interview points: `std::variant` does *not* automatically propagate operators — you must either coerce to the active type or use `std::visit`. This is fundamentally different from the overloaded-operators-on-class-types you get in C++.

## Q70: What is the Python `__format__` mini-language and its relation to `__str__`? 

**A:** `__format__(self, spec)` handles the format specification mini-language — the part after `:` in `f"{obj:spec}"` and within `format(obj, spec)`. `str()` and `f"{obj}"` (no spec) call `__format__(obj, "")` → which by default calls `str(obj)`. So `__str__` is the fallback for format with an empty spec.

The default `object.__format__`:
1. If `spec == ""`: return `str(self)`.
2. Otherwise (non-empty spec): it delegates to the built-in `format(value, spec)` logic, which handles `'s'`, `'f'`, `'d'`, fill/align/width/precision, etc.

Custom `__format__` allows types like currencies, dates, or locations to accept their own specs:

```python
class Currency:
    def __format__(self, spec):
        prefix = spec or "$"
        return f"{prefix}{self.amount:.2f}"
f"{Currency(42)}"     # "$42.00" (empty spec defaults to __str__ fallback here)
f"{Currency(42):€}"   # "€42.00" — spec is "€"
```

The relation to `__str__`: with an empty spec, you likely want `__format__` to behave like `__str__`. With a non-empty spec, define your own mini-language. Note that `f"{x:>" width"}"`-style fill/align applies the generic format spec through the *built-in* `format()` machinery; your custom handling must respect or reimplement it if you want to combine.

## Q71: What is the C++ two-phase lookup problem with overloaded operators in templates?

**A:** Two-phase lookup means dependent names are looked up at instantiation, having been recorded at template definition time. For operators used inside a template, correctness depends on ADL (dependent operators are found via ADL at instantiation):

```cpp
template<typename T>
void f(T a, T b) {
    auto c = a + b;   // dependent: found at instantiation via ADL from T's namespace
}
```

If the `operator+` for `T` is defined in a namespace unrelated to `T`, ADL will not find it, and compilation fails. This leads to the "operator must live in the same namespace as the type" rule (Sutter's C++ rule).

The three classic pitfalls:
1. Defining `operator+` in a different namespace than `T` → ADL can't see it.
2. Qualifying with `::f::operator+` when calling explicitly → breaks generic code (defeats the point).
3. Parameterized template types where the operator depends on the template argument (`vector<T> + vector<T>`), which requires the operator to be findable via ADL from both `std` and the user type.

The standard workarounds:
- Put operators in the same namespace as the type they operate on.
- Make them `friend` inside the class definition to be found by ADL (injection into the nearest namespace).
- If you can't move the operator, add a `using` declaration so ordinary unqualified lookup finds it.

The C++20 spaceship operator also requires ADL-visible `operator<=>`; the same namespace rules apply.

## Q72: How does Python's `__rshift__`/`<<` support bitwise and stream-style serialization DSLs?

**A:** In Python, `<<` and `>>` are the bitwise shift operators (dunders `__lshift__` / `__rshift__`). They cannot be overloaded for "stream insertion" semantics like C++'s `operator<<` on `std::ostream`, because Python has no stream-operator convention. Instead, DSLs use `|` (or/concatenation), `>>` (consume/transform), or custom methods.

The bitwise dunders can be repurposed (as `pathlib` and JSON DSLs sometimes do):
- `data >> parser` → parse (consume).
- `parser << value` → construct serialization.
- `a | b` → chain / combine.

Example:

```python
class Pipeline:
    def __rshift__(self, fn):
        return Component(lambda x: fn(self.compute(x)))
    def __lshift__(self, data):
        return self.compute(data)
```

This conflicts with the well-established bitwise meaning for ints and NumPy arrays. Repurposing arithmetic/bitwise operators in Python is legal but punishes readability — unlike C++ where stream operators are idiomatic.

Python's convention is: overload operators only to *match their domain semantics* (addition, comparison, containers, iteration, numeric protocols). For serialization/parsing DSLs, prefer explicit methods like `dumps`/`loads` or pipe-style `|` composition that reads naturally without overloading shift.

## Q73: In C++, what is the difference between `operator->` and `operator*` for smart pointer design?

**A:** `operator->` must return a pointer or an object whose `operator->` chain continues; it implements member access. `operator*` (unary dereference) must return a reference to the pointee. For smart pointers:

```cpp
class SmartPtr {
    T* p;
public:
    T& operator*() const { return *p; }  // return resolves to object
    T* operator->() const { return p; }  // return resolves to pointer for ->
};
```

Key differences:
1. `p->mem` compiles to `(p.operator->())->mem`; the returned pointer is dereferenced — the return type is a `T*`.
2. `*p` compiles to `p.operator*()`, yielding `T&`.
3. You can overload `operator*` to return any reference type; it is not restricted.
4. `operator->` is the only operator whose return type is constrained by the language's grammar.

For custom "view" classes, you can return a proxy from `operator*` (e.g., compute on access). For `operator->`, returning a `T*` is simplest; returning a proxy object means the compiler dereferences *the proxy's* `operator->` chain.

The C++ rule: `operator->()` (nonzero arity trailing a postfix expression) must be one of the postfix-expression operators; `a->b` requires `a` to be a pointer, or a class with `operator->` whose return type is a pointer (or recursively a class with `operator->`).

`std::unique_ptr` and `std::shared_ptr` implement both. `std::optional<T>` intentionally does **not** implement `operator->`/`operator*` unerased — it does implement `operator*` and `operator->` value access, plus `value()`, since the value semantics matter.

## Q74: What is the Python `__class_getitem__` vs `__getitem__` on a metaclass? Why is `__class_getitem__` preferred?

**A:** Python resolves class-level `[]` (e.g., `List[int]`) via `type.__getitem__` semantics. Historically, subscribing a class was implemented by defining `__getitem__` on the **metaclass**. PEP 560 introduced `__class_getitem__(cls, key)` as a **classmethod** on the class itself, decoupling it from instance indexing.

- `MyClass[key]` → `MyClass.__class_getitem__(key)` (if defined).
- If not defined, finds `type(MyClass).__getitem__(...)` on the metaclass.
- If neither exists → `TypeError` ("type does not support subscripting" or "'type' object is not subscriptable").

`__class_getitem__` is preferred because:
1. Metaclass `__getitem__` made *instance* `[]` (via metaclass of instance's type) ambiguous; PEP 560 fixes that.
2. Built-ins like `list`, `dict` gained `__class_getitem__` in 3.9 (`list[int]`).
3. Custom generics and `typing.Generic` rely on it.

```python
class Registry:
    _map = {}
    def __class_getitem__(cls, key):
        return cls._map[key]
Registry[int]  # OK
```

It's also allowed to be a normal `@classmethod`:

```python
class G:
    @classmethod
    def __class_getitem__(cls, item):
        return f"G[{item}]"
```

Then `typing`-style parametrized types, `Generic[...]`, and `TypeVar` subscriptions all consult `__class_getitem__` first. The key interview point: `__class_getitem__` is how Python 3.9+ implements generics at the class level cleanly.

## Q75: What is the relation between `__index__`, slicing, and bitfields in custom numeric containers?

**A:** `__index__` bridges custom numeric types with operations that require *exact* integer semantics: integer subscripting, slicing (range boundaries), `bin`/`oct`/`hex`, `%`, `&`, `|`, `^`, `<<`, `>>`. Using a custom "index-like" object in `arr[custom_idx]` fails unless `custom_idx.__index__()` returns a real `int`.

For containers with bitfields (packed bits), `__index__` enables bit extraction:

```python
class BitMask:
    def __init__(self, value):
        self.value = value
    def __index__(self):
        return int(self.value)   # exact, no loss

mask = BitMask(0b110)
print(1 << mask)   # OK: __index__ returns int for shift
print(bin(mask))   # "0b110"
```

Slicing interactions: `seq[mask]` where `mask.__index__() == 3` works exactly like `seq[3]`. For `slice` objects thrown from __getitem__ internally, any argument passed as an index must support `__index__` (or be int).

The contract: `__index__` must be **lossless** (unlike `__int__`, which may truncate `float`/custom numerics). CPython's `operator.index()` enforces this by raising `TypeError` on lossy types. The interpreter will *not* fall back to `__float__`.

The interview angle: distinguishing `__index__` (exactness for indices/shifts) from `__int__` (general conversion) from `__trunc__` (math.trunc), and knowing that `__index__` is what makes custom containers usable in `range`, indexing, and bitwise DSLs.

## Q76: What is the abi breakage risk when adding operator overloads to a public API?

**A:** Adding, removing, or changing the signature of an overloaded operator is an ABI-incompatible change for C++ libraries exported as shared objects. Because operators are often free functions or inline members, an inline `operator+` change can silently invalidate callers that the compiler previously inlined — no symbol changes, no link-time warning, but behavior changes. Even adding `noexcept` is an ABI-neutral-ish change (it changes the function's exception contract but not its mangled symbol in most ABIs).

Concrete risks:
1. **Mangled name change**: changing parameter/return types of a member operator changes its mangled symbol → clients compiled against the old library fail to link.
2. **Inline-vs-exported decisions**: making an operator `inline` in a header vs exporting it forces recompilation of every TU that includes the header.
3. **Memory layout**: adding `operator==` as a member changes nothing about layout, but changing an *existing* operator's implementation (e.g., from value semantics to reference semantics) changes behavior without changing symbol.
4. **ABI versioning**: overloaded operators participate in overload resolution, so adding a *new* overload alongside (e.g., `operator+(int)` for `MyInt`) changes which candidate is picked for existing calls — again incompatibility.

The discipline: treat operator overloads as part of the ABI contract. Document them, bump SONAME/`-Wl,--version-script` when they change, and prefer function-local overloads for internal helpers to avoid leaking into public headers. This is precisely why `std::rel_ops`, expression templates, and `<=>` changes (C++20) must be coordinated across library versions.

## Q77: How do you design a Python `__getitem__`/`__setitem__`-based API that supports both dict-like, list-like, and slice semantics?

**A:** Design `__getitem__` to accept a key that is either an integer, a slice, or a hashable object. The dispatch logic should be:

1. Distinguish `int`/`slice` types explicitly (`isinstance(index, (int, slice))`) — never rely on hashing.
2. For slice values, return a view/copy of the requested range.
3. For tuple keys (e.g., `a[1,2]`), route to multidimensional semantics.
4. Fall back to a mapping lookup (`self._store[index]` / `__getattr__`) as the last resort.

```python
class DLSArray:
    def __getitem__(self, key):
        if isinstance(key, slice):
            start, stop, step = key.indices(self._length)
            return [self._data[i] for i in range(start, stop, step)]
        if isinstance(key, tuple):
            return self._multi_get(key)   # e.g., [row, col]
        try:
            return self._store[key]        # dict-like
        except (KeyError, TypeError):
            if isinstance(key, int):
                return self._data[key]     # list-like for ints
            raise KeyError(key)
```

`__setitem__` mirrors this: store integers/slices in the sequence, hashables in the mapping.

For senior level, note the pitfalls:
- `in` uses `__contains__`, which iterates `__getitem__` if not defined — for a hybrid type store a `__contains__` explicitly.
- Negative indices and step<0 must be handled via `.indices`.
- Booleans are `int` subclasses in Python — `arr[True]` indexing treats `True == 1`; document whether you allow that.
- Never call `slice.__getitem__` yourself via syntax tricks; `slice.indices` is the sanctioned path.

## Q78: In C++, when should you make an operator a member vs friend vs free? Provide the decision guide.

**A:** Three categories, with strong conventions:

1. **Must be a member**:
   - Assignment operators (`=`, `+=`, `-=`, `*=`, etc.) — they mutate `*this` and are implicitly `this->`-bound.
   - `operator[]`, `operator()`, `operator->`, conversion operators, and unary `++`/`--`.
   - `new`/`delete` (static members).

2. **Must be a free function**:
   - Stream insert/extract (`<<`/`>>`) — because the left operand is `std::ostream`/`std::istream`.
   - Binary operators where the left operand is a fundamental type or a type you don't own (e.g., `int << MyType` if useful).
   - Operators that must participate symmetrically and support implicit conversions on the left operand.

3. **Conventionally a friend (or free with access)**:
   - Binary arithmetic/comparison operators (`+`, `-`, `*`, `/`, `==`, `<`) — as free functions when both operands are your type; as `friend` if they need private access.
   - `swap`.

The decision matrix:
- Need private data of one operand → member or friend.
- Need private data of both operands and non-member semantics → friend free function.
- Symmetry + implicit conversions needed on left → free function.
- Cannot change the left operand's class (fundamental types, standard types) → free function.

The C++ Core Guidelines (C.161) favor **free functions for symmetric binary operators**, with `friend` only for private access. Compiler-assembly trick: ADL finds free operators in the operand's namespace automatically; member operators are only viable when the left operand is exactly the class type.

## Q79: What is the Python fan-out problem in `__getattr__`-heavy instruments and how do you audit them?

**A:** `__getattr__`-driven objects intercept *every* missing attribute access, so a typo like `self.vektr.length` returns the computed/fallback value silently instead of raising `AttributeError`. This masks bugs, breaks debuggers (`dir`, `hasattr`, `__dict__` inspection), confuses `getattr(obj, x, default)`, and can trigger recursion in `__init__` (before attributes exist).

Designs that are notoriously fragile:
- JSON/ORM "magic" object models (SQLAlchemy's `InstrumentedAttribute`, pandas `Series` attribute access).
- Deep "auto-retry" proxies that return cached values for any attribute.
- Classes with custom `__getattr__` in base + descriptor chains.

Audit approach:
1. Log every `__getattr__` call with `sys.settrace`/`inspect.getframeinfo` to see spurious calls.
2. Test with `hasattr`, `getattr(x, name, sentinel)` on missing names — should raise, not return junk.
3. Ensure `__getattr__` returns `NotImplemented`-style `AttributeError`, not a value, for genuinely unknown attributes.
4. Prefer explicit `__slots__` + `__dict__` interplay; avoid `__attr`-based dynamic dispatch unless the domain truly needs it.
5. Provide a "strict" mode flag that turns `__getattr__` into exact lookups.

For interviews: `__getattr__` is a *fallback*, `__getattribute__` is *would-always-run*, and `object.__getattribute__` is the canonical fast path. Design `__getattr__` so unknown names raise, and keep the attribute protocol auditable.

## Q80: In C++, how do expression templates interact with `auto&& range-for` and `std::ranges`?

**A:** Expression templates (Q51) store references; combining them with `auto&&` in range-for or `std::ranges::` algorithms is hazardous.

```cpp
for (auto&& x : a + b) { ... }   // `a + b` is a proxy/expression object
// The expression object stores const A&, const B& — valid during the full expression only.
```

For range-for, the deranged expression `a + b` is bound via `auto&& __range`. Because it's an rvalue expression evaluated *before* the loop, the temporary proxy lives for the loop's duration — that part is safe. But the proxy *references* `a` and `b`, so if the loop body triggers `a`/`b` mutation, you hit dangling storage.

With `std::ranges::accumulate(a + b, init)`, the range is consumed immediately during the algorithm call — safe, but the algorithm itself re-evaluates `operator*`/`operator[]` on the proxy per element.

Real risk: storing `auto result = a + b;` and *then* looping:
```cpp
auto result = a + b;          // proxy survives
for (auto& x : result) { ... } // x references a's/b's storage — dangerous if a/b died
```

Best practices for AI/library code:
1. Never let expression templates escape the full expression; materialize eagerly.
2. Provide a `.eval()` that produces a concrete container.
3. If you must linger, `Matrix r = expr;` (assignment) to force evaluation.
4. Document that range-for and `std::ranges` are transient-consumption friendly.

This is a classic senior-level "why expression templates are both powerful and dangerous" discussion.

## Q81: What are the Python `__set_name__`/`__init_subclass__`-driven patterns and their operator implications?

**A:** Both are class-level hooks that let the class shape itself before instances exist:
- `__set_name__(self, owner, name)`: descriptor runs at class creation; gives the descriptor its attribute name.
- `__init_subclass__(cls, **kwargs)`: called on every subclass creation; lets a base customize subclass class dicts.

Operator implications:
- `__set_name__` is what makes `@property`-style descriptors work; if a descriptor wraps operator logic (e.g., a `validated_int` that overloads arithmetic), binding through `__set_name__` lets the descriptor expose `.name` for error messages.
- `__init_subclass__` can inject or modify special methods on subclasses. Example: auto-registering subclasses implementing comparison operators without the user writing them.

```python
class OpBase:
    def __init_subclass__(cls, op="add", **kwargs):
        super().__init_subclass__(**kwargs)
        if op == "add":
            def __add__(self, other):
                return f"{self.x}+{other}"
            cls.__add__ = __add__
```

Careful: overriding `__set_name__` changes descriptor behavior for every attribute; test with `inspect.getattr_static` to see what's actually bound.

Senior-angle: `__init_subclass__` runs *before* the subclass body's `__set_name__` assignments, so injecting operators at that point interferes with descriptor binding. Sequence is: (1) subclass body executes, (2) `__set_name__` for descriptors, (3) `__init_subclass__` finalizes. Modify only after `super().__init_subclass__()`.

## Q82: In C++, how do overloaded operators interact with `SFINAE`, concepts, and `requires` clauses?

**A:** Operators are functions, so they participate in SFINAE and constraints. `requires`-based concepts (C++20) can restrict operator overloads to types that support the required subexpressions, mirroring Python-style duck typing at compile time.

```cpp
template<typename T>
concept Addable = requires(T a, T b) { { a + b } -> std::same_as<T>; };

template<Addable T>
T sum(const std::span<const T>& s);
```

The SFINAE angle: an operator overload can be enabled/disabled based on whether its operands satisfy a trait. `std::enable_if_t` on operator signatures is a classical pattern:

```cpp
template<typename T, typename U>
auto operator+(const MyType<T>& a, MyType<U>& b)
  -> std::enable_if_t<std::is_convertible_v<T, U>, MyType<U>> { ... }
```

C++20 concepts make this cleaner: `requires std::same_as<decltype(lhs), decltype(rhs)>` or `std::convertible_to`.

Key points for senior interview:
1. Operators follow normal overload resolution; concepts constrain *viability* (removed from candidate set), not just *resolution*.
2. A constrained operator with a `requires` clause affects ADL — the compiler evaluates `requires` in both namespaces.
3. Rewrite rules (Q27) also respect constraints.
4. Pitfall: two different concepts might both be satisfied → ambiguous; order the requires in a way that creates ordering (most-constrained wins via partial ordering of constraints).

## Q83: What is the C++ `std::common_type` relationship to the ternary operator and equality semantics?

**A:** `std::common_type_t<T, U>` computes the common type that `?:` uses. For `cond ? x : y` where `x` is `T`, `y` is `U`, the result type is `common_type_t<T,U>` (approximately, modulo decay). This is exactly why `?:` operates on mixed types without user involvement.

The ternary operator's rules:
1. If the second and third operands have the *same type*, that type is used.
2. Otherwise, if one can be converted to the other (including promoted built-ins), the common type wins.
3. If the operands are class types with a common base or both are convertible to a common type, that type is used.
4. Arithmetic promotions follow usual arithmetic conversions.

Equality semantics: for `a == b` with `a` of type `T`, `b` of type `U`, C++20's rewrite rules try `a == b` and `b == a`; `std::common_type_t<T,U>` gives a canonical comparison target. The `<=>` operator's `std::common_comparison_category_t<...>` composes the categories of member-wise comparisons.

For operator designers:
- If you want `x == y` to work symmetrically for distinct types, provide both `operator==` orders or use a single `friend` with `!=`/`==` via `<=>`.
- Document the `common_type` of your class pair so generic code's `?:` produces a sensible result.
- Avoid defining `operator+`, `operator<`, `operator==` that disagree with `common_type`.

## Q84: How does Python's `__and__`, `__or__`, `__xor__` relate to set operations and how do you extend misbehaving types?

**A:** These dunders implement bitwise `&`, `|`, `^`. When used on sets (a `frozenset`/`set`), Python's actual behavior is *set union/intersection/difference* via these same bitwise names — but `set.__or__` etc. delegate to the internal set operations.

For a custom set-like type:
```python
class TagSet:
    def __or__(self, other):
        # set-theoretic union
        return TagSet(self._tags | other._tags)
    def __and__(self, other):
        return TagSet(self._tags & other._tags)
    def __xor__(self, other):
        return TagSet(self._tags ^ other._tags)
```

The standard library also has `operator.or_`, `operator.and_`, `operator.xor`, `operator.invert` mirroring these dunders. The operator module is the reliable way to call them without syntax ambiguity.

Careful extension of misbehaving types:
1. If the base class already overloads `__or__` (e.g., `int`), your subclass override must return the exact contract the base promised.
2. For symmetric operations, implement both `__or__` and `__ror__`, handling mismatched operand types with `NotImplemented`.
3. If you can't subclass cleanly, use `functools.singledispatchmethod` to dispatch based on the *other* operand's type.

The senior point: sets and frozensets both support iteration, contains, and bitwise union. Overlapping `&`/`|` between sets and custom tagging types requires careful `__ror__` on the custom type for `{1,2} & tags`.

## Q85: What is the C++ proxy iterator problem and how does it constrain `operator[]`?

**A:** Proxy iterators surface when `operator*`/`operator[]` returns a proxy instead of a true reference. `std::vector<bool>` (Q64) is canonical. The problem: generic algorithms (and `auto& x = *it;`) assume `*it` is a real reference; with a proxy:
1. `auto& x = *it;` binds a reference to a temporary proxy → dangling.
2. `std::swap(*it1, *it2)` fails.
3. `*it1 = rhs` goes through the proxy (works, but requires proxy `operator=`).
4. Algorithms like `std::sort` bail out because `operator*` is non-standard.
5. `static_cast<T&>(*it)` and decltype-based machinery break.

The constraints on `operator[]` come from this: a *real reference* `operator[]` returns `T&` (thus generic-usable), while a *proxy* `operator[]` returns a proxy type that is not `T&`. Anything that uses `decltype(arr[0])` and expects `T&` is incompatible.

Workarounds:
- Provide a separate `at()`/`data()` returning `T*`/`T&` for performance.
- Implement `operator*` on the iterator to return a proxy, but provide `std::get`/`operator[]` overloads that return real references.
- If you truly cannot return `T&`, document the proxy and ban `auto&` patterns; use `decltype(auto)` carefully.

Senior answer: proxy iterators are case studies in "operator overloading that breaks generic assumptions"; measure the cost before using them, and prefer a dedicated storage representation.

## Q86: How do you design Python `__await__`, `__anext__`, and `__aenter__` for async operator-like behavior?

**A:** These dunders make objects usable in `await`/`async for`/`async with`:
- `__await__(self)`: returns an iterator that `await` can yield from; used to make custom awaitables.
- `__aiter__`/`__anext__`: drive `async for`.
- `__aenter__`/`__aexit__`: drive `async with`.

They are "operator-like" in the sense that they are protocol-facing special methods. Implement them when your object needs to integrate with async control flow:

```python
class AsyncResource:
    async def __aenter__(self):
        self.conn = await connect()
        return self.conn
    async def __aexit__(self, exc_type, exc, tb):
        await self.conn.close()
        return False

class AwaitableProxy:
    def __await__(self):
        return self._delegate.__await__()
```

Design considerations:
1. `__aenter__`/`__aexit__` must be coroutine functions; `__await__` returns a generator that yields a Future/Task.
2. If `__aexit__` returns True, it suppresses exceptions — be precise about the return contract.
3. `async for` uses `__aiter__` returning an async iterator whose `__anext__` raises `StopAsyncIteration` to end.
4. `__await__` on a non-coroutine object implies `await obj` works — don't overuse.

The senior angle: `Task`, `Future`, and `asyncio.sleep` implement these protocols; you can build frameworks that look like operators (e.g., `with await conn:` style) by combining `__await__` and `__getitem__`-style desugaring.

## Q87: What is the C++ challenge of overloading `operator==` for a `std::variant` and how does `std::visit` help?

**A:** A `std::variant<T...>` holds one of `T...`. `operator==` for two variants is dispatched only if both hold the *same alternative* type; otherwise, comparing different alternatives is typically `false` (but requires the types to be comparable). The challenge: you can't write a single `operator==` for "the variant as a whole."

The practical approach: use `std::visit` with a generic lambda / overload set:

```cpp
template<class... Ts>
bool variant_eq(const std::variant<Ts...>& a, const std::variant<Ts...>& b) {
    return std::visit([](const auto& x, const auto& y) {
        if constexpr (std::is_same_v<decltype(x), decltype(y)>)
            return x == y;
        else
            return false;
    }, a, b);
}
```

Why not just define `operator==` on a custom wrapper? Repeated for every visitor type; and because the variant's active type is erased at runtime, you need runtime dispatch (`std::visit`).

For senior answers:
1. `std::variant` doesn't inherit operators from a common base — it's a sum type.
2. Want symmetric comparisons? Both orders must be considered; generic lambdas unify them.
3. `<=>` on `variant` is defined where the active alternatives support it; but two different alternatives → `std::weak_ordering` domain breaks. Prefer `std::visit`.
4. Patterns like `std::visit([]<class T>...` (C++20) or `std::visit(overloaded{...})` make this idiomatic.

## Q88: What are Python's abstract base classes (ABCs) that mirror operator protocols, and how do they enforce contracts?

**A:** `collections.abc` defines ABCs whose *required methods* must exist for instance checks to succeed:

- `Container`: `__contains__`
- `Hashable`: `__hash__`
- `Iterable`: `__iter__` (or legacy `__getitem__`)
- `Iterator`: `__iter__` + `__next__`
- `Reversible`: `__reversed__`
- `Sized`: `__len__`
- `Callable`: `__call__`
- `Sequence`: `__getitem__` + `__len__` (+ `count`, `index`)
- `MutableSequence`: adds `__setitem__`, `__delitem__`
- `Set`/`MutableSet`: `__contains__`, `__iter__`, `__len__` (+ `&`, `|`, `-`, `isdisjoint` etc.)
- `Mapping`/`MutableMapping`: `__getitem__`, `__iter__`, `__len__` (+ `get`, `items`, etc.)
- `Number`-related: `numbers.Number`, `numbers.Integral`, `numbers.Real`, etc. with `__abs__`, `__add__`, `__pow__`, `__eq__`.

```python
from collections.abc import Sequence
class MySeq(Sequence):
    def __getitem__(self, idx): ...
    def __len__(self): ...
# Now len(), iteration, slicing via .indices, in, reversed(), etc. — mostly free.
```

Enforcement is duck-typing at `isinstance()`/`issubclass()` time, not static analysis. The ABC's default mixins (e.g., `Sequence` provides `__iter__`, `__contains__`, `__reversed__`) derive from the abstract methods.

Senior angle: ABCs are the *contract* documentation for operator protocols. Custom classes that implement `__eq__`/`__hash__` should be registered with the right ABC (`collections.abc.Hashable`), and their `__eq__`/`__lt__` semantics should match the ABC's documented behavior (e.g., `frozenset` uses `__and__`/`__or__`, `Decimal` uses `__eq__` with signal-aware NaN).

## Q89: In C++, what is the impact of `-fno-elide-constructors` or disabling NRVO on operator-heavy code?

**A:** Compilers (GCC/Clang) allow disabling copy elision with `-fno-elide-constructors`, forcing the standard's "non-elided" path: the object is copied and moved explicitly. For operator-heavy code, disabling elision can expose:

1. `a + b` returns a prvalue → without elision, the prvalue is *moved* into the return slot (or copied if no move).
2. `a + b + c` → chain of temporaries: one full temporary per `+`.
3. Second copy when assigned to `d`: `d = a + b` copies/moves the prvalue into `d` (unless copy-assign over `operator=` is elided, which it isn't).
4. `return local;` (NRVO) → move constructor + move assignment (or copy if no move).

The magnitude of the penalty depends on the copy/move costs of your type. For an `int` it's negligible; for a `Matrix` with heap storage it's significant (allocation per temporary).

The lesson for interviews/design:
- Elision (RVO/NRVO) is the reason return-by-value from operators is cheap in release builds.
- Debug builds (and `-fno-elide-constructors`) make copies visible — this is a good *testing* tool to verify move/copy correctness.
- The C++20 standard *mandates* prvalue elision, so `-fno-elide-constructors` only affects named-return values, not prvalue materialization.

If your type's correctness depends on copies/moves being *actually elided*, it's fragile. Design operators to be copyable/movable efficiently, and rely on elision only as an optimization.

## Q90: What is `__slots__` and how does it relate to `__hash__`/`__eq__` and operator behavior?

**A:** `__slots__` replaces `__dict__` with a fixed set of descriptors, saving memory per instance. It affects operator protocols:

1. With `__slots__` and a custom `__eq__`, the class is still hashable only if you define `__hash__` explicitly (or the class is immutable). Without `__slots__` and without `__eq__`, you get identity hashing (based on `id`).
2. If the class defines `__slots__` but no `__eq__`, instances are hashable by identity — fine.
3. If `__slots__` + `__eq__` are defined without `__hash__`, Python sets `__hash__ = None` (breaking set/dict usability).
4. `__slots__` enables *memory compaction*, but combined with operator-like behavior (mutable attrs used in `__eq__`/`__hash__`), mutation after hashing breaks set invariants.

```python
class Point:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
    def __hash__(self):
        return hash((self.x, self.y))
```

The design that "fits": an immutable, hashable, `__slots__`-based value type with `__eq__`, `__hash__`, `__repr__`. This gives you interning/set membership safety plus memory savings.

The interview point: `__slots__` interacts with the hash/equality contract. Adding `__slots__` to a mutable type that defines value-based `__eq__` is a recipe for silent set corruption.

## Q91: In C++, how does `std::span` change operator overloads for container-like types?

**A:** `std::span<T>` is a non-owning view over a contiguous sequence. It supports `operator[]`, `operator*`, `operator->` (for iterators), `.data()`, `.size()`. The `span` itself does not own memory, so operator overloads that return *references* into it are fine as long as the span outlives the operator.

For designing container-like operators on top of span:

```cpp
std::span<double> view(data, n);
auto w1 = view[0];       // double& — ok
auto w2 = view[1];       // double& — ok
```

The "operator design" difference vs owning containers:
1. Never return a *span* by value and store it longer than the underlying buffer.
2. `span` slices (`view.subspan()`), `operator[]`, and iterators preserve the "view" contract — mutation affects the original.
3. C++23's `mdspan` provides multi-dimensional `operator[]` with extent checking (extent-only in C++23, bounds-checking as an extension).
4. `operator<=>` for `span` compares *elements*, not addresses — define forwarding semantics if a custom span happens to be used in comparisons.

For senior answers: `span` is "the operator-primary view"; operator overloads operating on span should document whether they're non-owning (views) vs owning (copies). Owning containers vs views change the copy semantics of the operator's return value.

## Q92: What is the Python `__weakref__` and how does weak referencing interact with operator-based cached objects?

**A:** Objects defined in Python have `__dict__` and a `__weakref__` slot by default, allowing `weakref.ref(obj)`, `weakref.WeakValueDictionary`, etc. Operator-based *cached* objects (e.g., memoized functions returning objects, LRU caches) benefit from weak references so released values are collectable.

```python
import weakref

class Cache:
    def __missing__(self, key):
        # store weakref to the value
        self[key] = weakref.ref(compute_value(key), self._on_deleted)
        return self[key]()
```

Interaction with operators:
1. A value used in `__eq__`/`__hash__` but stored weakly may be collected mid-usage → `None` on deref.
2. Weak references do not keep `__hash__` consistent if the object's hash uses mutable state — the weakref registry won't help.
3. `WeakValueDictionary` calls the returning of `None` when the object is collected; guard against it.

The fragile pattern: caching operators (`__call__`, `__getitem__`, `__add__`) that return weakref'd objects can return `None` unless you deref safely.
Best practice: deref once, store to a local, check for `None` (collected), then recompute.

The senior point: stdlib's `weakref` underpins `functools.lru_cache`'s weak-ref caching (`cached_property` uses a mutable WeakKeyDictionary in some versions), but never make operator semantics silently return `None` when a cached weakref has died.

## Q93: What is the C++ `boost::operators` library and `Boost.Hash`'s relation to operator overloading?

**A:** `boost::operators` provides template mixins (`boost::equality_comparable`, `boost::addable`, `boost::binary_arithmetic`) that *generate* the remaining operators from a minimal set (e.g., `==`+`<` → `!=`, `>`, `<=`, `>=`; `+=` → `+`). It's the library-level ancestor of `std::rel_ops` (deprecated in C++20, Q65).

```cpp
#include <boost/operators.hpp>

struct Money : boost::operators<Money> {
    int units;
    explicit Money(int u) : units(u) {}
    bool operator==(const Money& other) const { return units == other.units; }
    bool operator< (const Money& other) const { return units <  other.units; }
    // boost generates !=, >, <=, >= for you
};
```

`Boost.Hash`/`boost::hash_combine` complements operators: defining `operator==` for value semantics *should* pair with a `hash_value` (or `std::hash` specialization) so `unordered_map`/`unordered_set` work. The rule: `operator==` creates an equivalence relation; the hash must map equal objects to equal hashes.

The lesson for C++20: `<=>` (Q11) supersedes both `rel_ops` and Boost.Preprocessor macro-driven operator generation. But the *habit* of defining the minimal operator set and generating the rest is still the right design pattern — C++20 `<=>` does exactly this.

## Q94: How do you architect a cross-language operator contract (C++ internals, Python/Python built-ins, Java boundary)?

**A:** When writing operator overloads that cross FFI boundaries (C++ core exposed to Python via pybind11/Boost.Python, or to Java via JNI), the operator semantics must be modeled *in the API contract*, not in the language binding's syntax.

Consider C++ `BigInt` exposed to Python via pybind11:

```cpp
py::class_<BigInt>(m, "BigInt")
  .def(py::init<long>())
  .def(py::self + py::self)
  .def(py::self += py::self)
  .def(py::self == py::self);
```

Python-side expectations:
1. `big + 5` should work → provide `__radd__` in the binding (pybind11 synthesizes from `+` and `__rshift__` reflection).
2. `5 + big` needs reflected ops — define `py::self + int` and `int + py::self`.
3. `big == big2` must map to exactly the C++ equality — semantic mapping, not syntax mapping.
4. `hash(big)` must call the C++ hash_value; bind `__hash__` to the same function used for `operator==`'s equivalence classes.

For Java (no operator overloading): define explicit methods `add(BigInt)`, `compareTo(...)`, `equals(...)` and document the mapping. Java's `equals` and `hashCode` contract must match C++'s `operator==`/`hash_value`; that's the cross-language invariant.

The senior architect answer: define a single "operator contract" document (what + means, what == means, hash/equality equivalence), implement it natively, then bind each language's syntax to the *same* semantic function. Bindings that mix syntax across languages cause subtle divergence.

## Q95: What are the Python `__getattr__`/`__getattribute__`-based proxies that break `copy.deepcopy`, `pickle` and `__reduce__`, and how do you fix them?

**A:** Dynamic proxies (JSON objects, ORM row objects, "smart" wrappers) intercept attribute access, which breaks the copy/pickle protocols:

1. `copy.deepcopy(obj)` uses `__reduce_ex__`/`__reduce__`. A `__getattr__`-driven proxy's `__reduce__` may serialize the *fallback value*, not the real state → deepcopy of the wrong data.
2. `pickle.dumps(obj)` uses `__reduce__` (default: `obj.__class__` + `obj.__dict__`). With heavy `__getattr__`, `__dict__` is empty or includes virtual attributes → mis-pickling.
3. Custom `__getattribute__`-intercepting descriptors can cause infinite recursion during `__reduce__`/`__copy__` protocols.

Fixes:

```python
class SafeProxy:
    def __reduce__(self):
        return (self.__class__._rebuild, (self._real_state,))
    @staticmethod
    def _rebuild(state):
        obj = SafeProxy.__new__(SafeProxy)
        obj._real_state = state
        return obj
    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(name)
        return getattr(self._real_state, name)
    def __copy__(self):
        return self.__class__._rebuild(copy.copy(self._real_state))
```

The underlying rule: objects defining `__getattr__` should *also* implement `__reduce__`/`__copy__`/`__deepcopy__` explicitly, or restrict `__getattr__` to a known namespace. Otherwise hasattr, getattr with defaults, deepcopy, pickle, and `copy.replace` behave unpredictably.

Senior angle: Every operator and protocol that touches state (pickle, copy, repr, weakref) must be audited when you introduce dynamic attribute interception.

## Q96: In C++, what is the "operator overloading code bloat" concern and how do you mitigate it?

**A:** Each overloaded operator that's not inlined, or a template operator that's instantiated per type, multiplies code size. Expression templates (Q51) can produce especially large, deeply-nested template instantiations (each `a + b * c` yields a unique type).

The bloat vectors:
1. Non-inline member operators: one symbol per operator per type — codesize in the object.
2. Template operators instantiated per operand type: `operator+<int, Matrix>`, `operator+<float, Matrix>`, etc.
3. Expression templates: nested types blow up the compiler's symbol table and debug info.
4. Standard library operator templates (`std::rel_ops`, `std::plus`) add call-site thunks.

Mitigations:
1. Prefer `inline` for trivial operators; move heavy operator bodies to non-inline out-of-line functions and have the operator forward.
2. Reuse a single template implementation across similar types (deduce via `common_type`).
3. For expression templates, provide a `.eval()` that collapses to concrete container types, reducing template instantiation nesting.
4. Use `-Wl,--gc-sections`, `-ffunction-sections`, LTO, and avoid ODR defeats.
5. `noexcept` + `inline` allow the compiler to elide thunks entirely.

The senior point: measure with `-fsized-deallocation`/`-ftime-report`; prefer moving *implementation* out of templated operator bodies into non-template `detail` functions so only the (cheap) operator calls get instantiated per type.

## Q97: What is `__getattr__`-based inheritance interplay with `__setattr__` and `__delattr__`, and the "dict priority" design?

**A:** When you define custom `__setattr__`, `__getattr__`, and `__delattr__` on a class, the attribute protocol order matters. Normal attribute read order: instance `__dict__` → class (`type(obj).__mro__`) → `__getattr__` (fallback) → `AttributeError`.

Write/delete: `self.attr = v` → `__setattr__` (which usually writes `object.__setattr__` → `self.__dict__['attr'] = v`); `del self.attr` → `__delattr__`.

The "dict priority" design keeps reads/writes consistent:

```python
class DualDict:
    def __setattr__(self, name, value):
        # virtual names never land in __dict__
        if name.startswith('_v_'):
            object.__setattr__(self, '_virtual', value)
        else:
            object.__setattr__(self, name, value)  # into __dict__
    def __getattr__(self, name):
        if name.startswith('_v_'):
            return object.__getattribute__(self, '_virtual')
        raise AttributeError(name)
    def __delattr__(self, name):
        if name.startswith('_v_'):
            object.__delattr__(self, '_virtual')
        else:
            object.__delattr__(self, name)
```

The semantics: `__getattr__` only fires when normal lookup fails, so a name in `__dict__` or class dict is *never* forwarded to `__getattr__`. `__setattr__` decides whether to write `__dict__` or a fallback. `__delattr__` must mirror.

The interviewer's senior question usually is: "If I read `obj.name`, write `obj.name = X`, delete `obj.name`, will `__getattr__`/`__setattr__`/`__delattr__` fire in the expected order for name in dict vs not in dict?" Answer: yes — `__getattr__` only for missing, `__setattr__` always, `__delattr__` always.

## Q98: What is the C++ coroutine-operator interaction? Can you overload operators on a coroutine's awaiter?

**A:** C++20 coroutines (co_await/co_yield/co_return) are not operators you can overload — their behavior is defined by the coroutine machinery (`promise_type`, `awaiter`). However, you can overload the **`await_suspend`**/`await_ready`/`await_resume` methods and the **`co_await` semantics** depends on the awaiter's types.

`operator->`, `operator*`, and `operator[]` on the *awaiter* are ordinary operators. So you can build coroutine "operator-like" DSLs:

```cpp
struct Task {
    struct promise_type;
    bool await_ready() const noexcept;
    void await_suspend(std::coroutine_handle<> h) noexcept;
    int await_resume() const noexcept;
};
```

The co_await expression `co_await t` is desugared by the compiler into the awaiter protocol — it is not overloadable in the user's operator set. Similarly `co_yield expr` calls `promise_type::yield_value`.

Common interview-focus points:
1. You cannot overload `co_await` for arbitrary types — the type must have await_ready/suspend/resume or a `operator co_await` (which *is* an overloadable operator that converts the operand into an awaiter).
2. `operator co_await` lets a custom type adapt to `co_await` by returning an awaiter.
3. Coroutines + expression templates: the awaiter must not keep references across suspension points (lifetime hazard).

The senior answer: distinguish "operator overloading" (user-defined operators) from "coroutine protocol" (compiler-matched awaiter). They compose, but they aren't the same mechanism.

## Q99: What are Python's `__aenter__`/`__aexit__` vs `__enter__`/`__exit__` and how do async context managers prevent resource leaks?

**A:** `__enter__`/`__exit__` (sync) and `__aenter__`/`__aexit__` (async) implement the `with`/`async with` protocols. Async context managers are required when acquiring/releasing resources asynchronously (DB connections, locks, sockets).

Correctness basics:
```python
class AsyncDB:
    async def __aenter__(self):
        self.conn = await create_pool()
        return self.conn
    async def __aexit__(self, exc_type, exc, tb):
        await self.conn.close()
        return False
```

Key details:
1. `__aenter__` returning `False` or None? The `as` binding captures the return of `__aenter__`; anything you return is bound.
2. `__aexit__` returning `True` **suppresses** exceptions — decide carefully (usually False).
3. When the body raises, Python calls `__aexit__` exactly once, with the exc_info triple.
4. `contextlib.asynccontextmanager` lets a generator function define an async CM with `yield`.

Resource-leak avoidance:
- If `__aenter__` fails after partial acquisition, you must clean up in `finally` — `__aexit__` is *not* called when `__aenter__` raises.
- Never swallow exceptions silently: a True return hides failures from callers.
- Never await inside `__aexit__` on a closed event loop → hang. Check `loop.is_running()`.
- Combine with cancellation: `async with` handles `asyncio.CancelledError` in ordinary flow — the body may get cancelled; `__aexit__` still runs.

The interview angle: async CMs are operators for lifecycle; they're the async mirror of RAII in C++ (Q56). Test both "happy path" and "exception path" with `pytest.mark.asyncio`.

## Q100: How do you design an operator overloading API that stays maintainable and correct over years and many contributors? Final senior/architect answer.

**A:** The senior answer is about contracts, invariants, and governance. Rules distilled from the literature (C++ Core Guidelines, Python data model, Boost/Grammar-based DSLs):

1. **Semantics over syntax**: every overloaded operator must have exactly one, documented meaning. `+` means the same operation everywhere (addition, concatenation, or set-union), never two different behaviors on the same class in different contexts. If the semantics change by use-site, don't overload.

2. **Contract-first**: publish (in the header/`__doc__`): operand types, return type, exception guarantee, const-ness, noexcept, and the equivalence relation for `==`. The compiler must verify these (C++ concepts/`requires`; Python `__slots__` + typed dunders).

3. **Keep operator kernels small**: operators should delegate to small, named, tested functions (`operator+=` calls a core `add_impl`; `operator+` calls `operator+=`). This gives you vectorization, unit tests, and auditability.

4. **Symmetry + commutativity**: document which binary operators are symmetric and which aren't. For symmetric, provide both orders (`__radd__`, free `operator+`). For asymmetric, name the direction explicitly.

5. **Exception-safety**: decide the guarantee – strong for value-returning operators, basic for in-place compound assignment. Use copy-and-swap where possible. Test with `-fno-elide-constructors` and injection of throwing allocators/BigInt throwing ops.

6. **Composability**: ensure operators compose: `a + b == c` means what it means for all types; avoid conditional behavior by runtime state (`if (flag) return ... else ...`).

7. **Hash/equality coupling** (Python) and `<=>`/`std::hash` coupling (C++): equal objects must hash equal.

8. **Governance**: operator overloads are part of the API = the ABI (Q76) in C++. Bump versions when they change; deprecate loudly; keep documentation in one place.

9. **Test the pitfalls**: expression-template lifetime (Q62), proxy references (Q85), `auto&` binding, short-circuiting loss (Q44), `bool` vs `len` truthiness (Q54), type-priorities in reflected ops (Q48).

10. **When to avoid**: if the operator's semantics differ substantially from the built-in's, choose a named function — this is the single strongest rule in all three languages (Java's philosophy, C++ guidelines, Pythonic "explicit is better").

In practice: design the title-abstraction (the "operator contract") you'd write in a one-page ADR, then implement operators as thin wrappers. The best-over engineered code is operator code that expresses *one* semantic model and fails loudly otherwise. That is the "blind-trust" quality an interviewer looks for — code you can hand to a new hire and confidently say: "read the contract, trust the operators."
