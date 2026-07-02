# String Immutability

## String Pool and intern()

### How Strings Work in Java

Strings in Java are **immutable** — once created, they cannot be changed. Every "modification" creates a new String object.

```java
String s = "hello";
s = s + " world"; // A NEW string is created; "hello" is abandoned
```

### String Pool (String Constant Pool / Intern Pool)

When you create a string literal, Java checks the String Pool first. If it exists, the reference is reused. If not, a new string is added to the pool.

```java
String s1 = "hello";
String s2 = "hello";
String s3 = new String("hello");

System.out.println(s1 == s2);      // true — same reference from pool
System.out.println(s1 == s3);      // false — new object on heap
System.out.println(s1.equals(s3)); // true — same value
```

### Memory Layout

```
Stack                Heap
+----------+        +-----------------------------+
| s1       | -----> | "hello"  (String Pool)      |
| s2       | -----> |  (same reference as s1)     |
| s3       | -----> | "hello"  (heap object)      |
+----------+        +-----------------------------+
```

### intern() Method

`intern()` puts a string into the pool and returns the pooled reference.

```java
String s4 = new String("hello").intern();
System.out.println(s1 == s4); // true — now it's from the pool
```

**Use case:** If you're reading many duplicate strings from a file/network and memory is a concern, use `intern()` to reduce duplicates. But be careful — interned strings stay in memory forever (in Metaspace, not garbage collected).

## == vs equals()

```java
String a = "test";
String b = "test";
String c = new String("test");

a == b      // true  (same pooled reference)
a == c      // false (different objects)
a.equals(c) // true  (same value)
```

**Golden rule:**
- `==` checks **reference identity** — do both variables point to the same object?
- `.equals()` checks **value equality** — do the strings contain the same characters?

For EVERY string comparison in business logic, use `.equals()`. Only use `==` when you explicitly want to check reference identity (rare).

```java
String input = scanner.next();
if (input == "quit") { }        // WRONG — may never match
if (input.equals("quit")) { }   // CORRECT
```

## Why Strings Are Immutable

### 1. Security

Strings are used extensively in security-sensitive contexts: database URLs, file paths, usernames, passwords, class loading. If strings were mutable, a malicious thread could modify a string after a security check.

```java
String username = authenticate(user, pass);
// If String were mutable, another thread could change 'username' here
loadUserData(username); // might load wrong user's data
```

### 2. Synchronization (Thread Safety)

Immutable objects are inherently thread-safe. No synchronization needed. Multiple threads can read the same string without data races.

### 3. Caching (String Pool / Hash Code)

- String Pool: Only works because strings don't change. A mutable string couldn't be safely cached.
- Hash code caching: String caches its hashCode() after first computation. If mutable, the cached hash would become stale, breaking HashMaps and HashSets.

```java
public int hashCode() {
    int h = hash; // cached field
    if (h == 0 && value.length > 0) {
        // compute hash
        hash = h;
    }
    return h;
}
```

### 4. Class Loading

Class names are strings used by the class loader. If mutable, someone could change `java.lang.Thread` to point to malicious code.

### 5. Convenience

APIs can safely return internal strings without defensive copying:

```java
public String getName() {
    return this.name; // safe to return internal reference
}
```

With mutable strings, you'd need:
```java
public String getName() {
    return new String(this.name); // defensive copy every time
}
```

## Performance Implications of Concatenation

### The Problem with `+`

```java
String s = "";
for (int i = 0; i < 10_000; i++) {
    s += i; // BAD: creates a new String object on every iteration
}
```

Each `+=` creates a new String object of increasing size:
- Creates "0" (1 char)
- Creates "01" (2 chars), discards "0"
- Creates "012" (3 chars), discards "01"
- Total: O(n²) time, creates ~n objects

### What the compiler actually does

```java
// This code:
String s = "a" + "b" + "c";

// Compiler optimizes to:
String s = "abc"; // compile-time constant folding

// But this:
String s = "";
for (int i = 0; i < n; i++) s += i;

// Is compiled to (in older Java):
s = new StringBuilder().append(s).append(i).toString(); // creates NEW StringBuilder each time!
```

### Modern Java (since Java 9+)

The compiler may use `invokedynamic` with `StringConcatFactory` to optimize concatenation. But it's still better to use explicit StringBuilder for loops.

### StringBuilder vs `+`

```java
// Fast version (use this)
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 10_000; i++) {
    sb.append(i);
}
String result = sb.toString();
```

This is O(n) with a single StringBuilder. No intermediate strings created.

## substring() Before and After Java 7u6

### Before Java 7u6 (The "view" implementation)

```java
String big = new String(new byte[1_000_000]);
String small = big.substring(0, 2);
// small shared the same char[] with big!
// big could NOT be garbage collected
```

`substring()` returned a new String that shared the underlying `char[]` with the original. Only the `offset` and `count` fields were different. This was fast (O(1)) but caused **memory leaks** — a small substring could pin a huge character array in memory.

### After Java 7u6 (The "copy" implementation)

```java
String big = new String(new byte[1_000_000]);
String small = big.substring(0, 2);
// small has its own char[] (copy of characters 0-2)
// big can now be garbage collected
```

`substring()` creates a new `char[]` with a copy of the characters. This is O(n) time but prevents memory leaks.

**Interview tip:** This is a favorite Java history question. Shows you understand the tradeoff between time and memory in library design.

## Immutability of Other String Classes

| Class | Mutable? | Thread-safe? | Notes |
|-------|----------|--------------|-------|
| String | ✗ | ✓ | Immutable, pooled |
| StringBuilder | ✓ | ✗ | Fast, single-threaded |
| StringBuffer | ✓ | ✓ | Synchronized, slower |

## Practice Problems

| Problem | Platform | Concept Tested |
|---------|----------|----------------|
| Check if strings are rotations | - | String concatenation + contains |
| Compare Version Numbers | LeetCode 165 | String splitting, comparison |
| String to Integer (atoi) | LeetCode 8 | String parsing |
| Valid Anagram | LeetCode 242 | Character counting |
| Detect Capital | LeetCode 520 | String character analysis |
