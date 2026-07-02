# StringBuilder — Detailed

## StringBuilder vs StringBuffer

| Feature | StringBuilder | StringBuffer |
|---------|---------------|--------------|
| Thread-safe | No | Yes (methods synchronized) |
| Introduced | Java 5 | Java 1.0 |
| Performance | ~5-10x faster | Slower due to sync |
| Methods | Same API | Same API |

```java
// Single-threaded: Use StringBuilder
StringBuilder sb = new StringBuilder();

// Multi-threaded (rare for StringBuilder use): Use StringBuffer
StringBuffer sb = new StringBuffer();
```

**Rule of thumb:** Use `StringBuilder` unless you have a specific reason to share it across threads (almost never). The JVM's synchronization overhead for StringBuffer is significant.

## Capacity Management

### Default Capacity

```java
StringBuilder sb = new StringBuilder(); // capacity = 16
StringBuilder sb = new StringBuilder(100); // capacity = 100
StringBuilder sb = new StringBuilder("hello"); // capacity = 16 + 5 = 21
```

### How StringBuilder Grows

When the internal buffer is full:

```java
// Internal growth logic (simplified)
void ensureCapacity(int minimumCapacity) {
    if (minimumCapacity > value.length) {
        int newCapacity = value.length * 2 + 2; // roughly double
        if (newCapacity < minimumCapacity) {
            newCapacity = minimumCapacity;
        }
        value = Arrays.copyOf(value, newCapacity);
    }
}
```

**Growth policy:** `newCapacity = (oldCapacity * 2) + 2`. This is amortized O(1) per append — similar to ArrayList.

### Why pre-sizing matters

```java
// Without pre-sizing:
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 100_000; i++) {
    sb.append(i); // May trigger multiple resizes
}

// With pre-sizing:
StringBuilder sb = new StringBuilder(500_000); // estimate the size
for (int i = 0; i < 100_000; i++) {
    sb.append(i); // No resizes
}
```

Pre-sizing avoids unnecessary array copies. If you know the approximate final size, set it upfront.

## Key Methods

### append() — Add to end

```java
StringBuilder sb = new StringBuilder("Hello");
sb.append(" World");       // "Hello World"
sb.append(42);             // "Hello World42"
sb.append(true);           // "Hello World42true"
sb.append('!');            // "Hello World42true!"
sb.append(new int[]{1,2}); // "Hello World42true![I@hash" (calls toString())
```

`append()` returns `this` — allows method chaining:

```java
StringBuilder sb = new StringBuilder()
    .append("Name: ")
    .append("John")
    .append(", Age: ")
    .append(25);
```

### insert() — Add at position

```java
StringBuilder sb = new StringBuilder("Hello World");
sb.insert(5, " Beautiful");    // "Hello Beautiful World"
sb.insert(0, "Start: ");       // "Start: Hello Beautiful World"
sb.insert(sb.length(), " END"); // same as append
```

**Time:** O(n) — shifts elements right.

### delete() and deleteCharAt()

```java
StringBuilder sb = new StringBuilder("Hello World");
sb.delete(5, 11);         // "Hello" (removes " World")
sb.deleteCharAt(0);       // "ello"
```

`delete(start, end)`: removes characters from start (inclusive) to end (exclusive).

### replace()

```java
StringBuilder sb = new StringBuilder("Hello World");
sb.replace(6, 11, "Java"); // "Hello Java"
```

### reverse()

```java
StringBuilder sb = new StringBuilder("hello");
sb.reverse(); // "olleh"
```

**Implementation:** Swaps characters from both ends inward. O(n).

### setCharAt()

```java
StringBuilder sb = new StringBuilder("hello");
sb.setCharAt(0, 'H'); // "Hello"
```

### setLength()

```java
StringBuilder sb = new StringBuilder("Hello World");
sb.setLength(5);    // "Hello" — truncates
sb.setLength(10);   // "Hello\0\0\0\0\0" — pads with null characters
```

**Use case:** Clearing a StringBuilder (more efficient than creating a new one):

```java
sb.setLength(0); // clears content, reuses buffer
```

### substring()

```java
StringBuilder sb = new StringBuilder("Hello World");
String s1 = sb.substring(6);     // "World"
String s2 = sb.substring(0, 5);  // "Hello"
```

Returns a String (not a StringBuilder). This creates a copy.

### toString()

```java
String result = sb.toString(); // produces the final immutable string
```

**Important:** If you modify the StringBuilder after calling `toString()`, the previously returned string is unaffected. Strings are immutable.

## Performance Benchmarks

### StringBuilder vs `+` concatenation

```java
// 100,000 iterations
// String concatenation: ~5000ms (O(n²) due to copying)
// StringBuilder: ~5ms (O(n))
```

The difference grows quadratically because each string `+` operation copies the entire existing content.

### StringBuilder vs StringBuffer

```java
// 1,000,000 iterations
// StringBuilder: ~20ms
// StringBuffer: ~80ms
```

StringBuffer's synchronization adds ~4x overhead.

## Common Patterns

### Building a delimited string

```java
// Before Java 8 (verbose)
StringBuilder sb = new StringBuilder();
for (int i = 0; i < items.length; i++) {
    if (i > 0) sb.append(", ");
    sb.append(items[i]);
}

// After Java 8 (use StringJoiner or Collectors.joining)
String joined = String.join(", ", items);  // simplest
```

### Building from loop with pre-sizing

```java
public static String joinWithPrefix(List<String> words, String prefix) {
    // Estimate: each word + prefix + delimiter
    int estimatedSize = words.size() * (prefix.length() + 10);
    StringBuilder sb = new StringBuilder(estimatedSize);

    for (String word : words) {
        sb.append(prefix).append(word).append("\n");
    }
    return sb.toString();
}
```

### Clearing for reuse

```java
// DON'T: creates garbage
result = sb.toString();
sb = new StringBuilder();

// DO: reuse buffer
result = sb.toString();
sb.setLength(0);
```

## StringBuilder Internals (Java 8+)

```java
// Simplified internal structure
final class StringBuilder {
    char[] value;      // the buffer (not final, can grow)
    int count;         // number of characters used
    // ... methods ...
}
```

In Java 9+, `char[]` was replaced with `byte[]` with a coder (LATIN1 or UTF16) for compact strings, but the API is identical.

## Common Pitfalls

1. **Not pre-sizing for large builds** — triggers multiple array resizes
2. **Using StringBuffer instead of StringBuilder** — unnecessary synchronization overhead
3. **Calling toString() and then appending** — fine, just remember toString() returns a snapshot
4. **Using capacity() to check length** — capacity is the buffer size, not the content length
5. **Appending null** — appends the string "null", not an empty string
6. **Concurrent modification** — StringBuilder is NOT thread-safe; use StringBuffer if needed

## Quick Reference

| Method | Returns | Time | Description |
|--------|---------|------|-------------|
| append(x) | StringBuilder | O(1) amortized | Add x to end |
| insert(pos, x) | StringBuilder | O(n) | Insert x at position |
| delete(s, e) | StringBuilder | O(n) | Remove chars s to e-1 |
| deleteCharAt(i) | StringBuilder | O(n) | Remove char at i |
| replace(s, e, str) | StringBuilder | O(n) | Replace range with str |
| reverse() | StringBuilder | O(n) | Reverse the sequence |
| setCharAt(i, c) | void | O(1) | Change char at i |
| setLength(n) | void | O(1) or O(n) | Truncate or pad |
| charAt(i) | char | O(1) | Get char at i |
| substring(s, e) | String | O(n) | Extract substring |
| toString() | String | O(n) | Create immutable copy |
| length() | int | O(1) | Current length |
| capacity() | int | O(1) | Buffer capacity |
