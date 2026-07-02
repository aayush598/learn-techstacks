# 04 — String & StringBuilder in Java

Strings in Java are deceptively complex. They look simple, but they're immutable, have a special memory pool, and can wreck your performance if you misuse them. Let's dive deep.

---

## 1. String — The Immutable Masterpiece

### String Pool & Immutability

```java
// String literals go to the String Pool (PermGen/Metaspace area)
String s1 = "hello";          // created in string pool
String s2 = "hello";          // reuses the same object from pool
System.out.println(s1 == s2); // true — same reference!

// Using 'new' forces a new object on the heap
String s3 = new String("hello");  // new object on heap
System.out.println(s1 == s3);     // false — different references
System.out.println(s1.equals(s3)); // true — same content

// intern() — manually put a string in the pool
String s4 = new String("hello").intern();
System.out.println(s1 == s4); // true — now in pool
```

**Why immutability matters:**
- **Thread safety** — strings are automatically safe across threads
- **Caching** — hashcode can be cached (String caches it after first computation)
- **Security** — can't modify strings used in sensitive contexts (credentials, class names)
- **String pool** — can safely share references

**The cost of immutability:** Every modification creates a new String object.

### Key Methods — The Full Arsenal

```java
String s = "  Hello, World!  ";

// Character access
char c = s.charAt(0);           // ' ' (space)
int len = s.length();            // 17 (includes spaces)
// ⚠️ length() is a METHOD, not a property like arrays

// Searching
int idx1 = s.indexOf('o');      // 5 (first occurrence)
int idx2 = s.indexOf('o', 6);   // 8 (search from index 6)
int idx3 = s.lastIndexOf('o');  // 8 (last occurrence)
int idx4 = s.indexOf("World");  // 9

// Checking
boolean has = s.contains("World");  // true
boolean starts = s.startsWith("  ");  // true
boolean ends = s.endsWith("!  ");     // true

// Extracting
String sub = s.substring(2, 7);      // "Hello" [2, 7)
// ⚠️ substring(beginIndex, endIndex) — endIndex EXCLUSIVE
// Single arg: substring(2) → "Hello, World!  "

// Transforming
String upper = s.toUpperCase();      // "  HELLO, WORLD!  "
String lower = s.toLowerCase();
String trimmed = s.trim();           // "Hello, World!" (removes leading/trailing whitespace)
String stripped = s.strip();         // Java 11+ — handles Unicode whitespace better

// Based on character class:
String stripLeading = s.stripLeading();   // "Hello, World!  "
String stripTrailing = s.stripTrailing(); // "  Hello, World!"

// Replacing
String rep1 = s.replace('l', 'L');        // "  HeLLo, WorLd!  "
String rep2 = s.replace("World", "Java"); // "  Hello, Java!  "
String rep3 = s.replaceAll("\\s", "");    // "Hello,World!" (regex)
String rep4 = s.replaceFirst("\\s", "");  // " Hello, World!  " (regex)

// Splitting
String data = "apple,banana,grape,orange";
String[] fruits = data.split(",");        // ["apple", "banana", "grape", "orange"]
// split(regex, limit) — limit controls how many parts
String[] limited = data.split(",", 2);    // ["apple", "banana,grape,orange"]

// ⚠️ Special characters need escaping in split: split("\\.") for dots

// Joining (static method)
String joined = String.join(", ", "a", "b", "c");  // "a, b, c"
String joinedArr = String.join("-", fruits);       // "apple-banana-grape-orange"

// Converting to/from char array
char[] chars = s.toCharArray();
String back = new String(chars);

// valueOf — converting other types
String numStr = String.valueOf(42);        // "42"
String boolStr = String.valueOf(true);     // "true"
String objStr = String.valueOf(new Object());  // Object's toString()

// Formatting
String formatted = String.format("Hello %s, you are %d years old", "Alice", 25);
```

### equals vs == — The Classic Interview Question

```java
String a = "hello";
String b = "hello";
String c = new String("hello");

System.out.println(a == b);      // true (same pool reference)
System.out.println(a == c);      // false (different objects)
System.out.println(a.equals(c)); // true (same content)
System.out.println(a.equals(b)); // true

// ⚠️ Always use .equals() for string content comparison
// == checks reference equality — rarely what you want
```

### compareTo — Lexicographic Comparison

```java
String a = "apple";
String b = "banana";
String c = "apple";

a.compareTo(b);     // negative (< 0) — "apple" < "banana"
b.compareTo(a);     // positive (> 0) — "banana" > "apple"
a.compareTo(c);     // 0 — equal

// Case-insensitive
a.compareToIgnoreCase("APPLE");  // 0

// Used in sorting:
List<String> list = Arrays.asList("banana", "apple", "cherry");
Collections.sort(list);  // uses compareTo internally

// ⚠️ compareTo returns character difference:
// "apple".compareTo("apricot") → 'p' - 'r' = -2
```

### Useful String Utilities

```java
// Check if string is numeric
public static boolean isNumeric(String s) {
    if (s == null || s.isEmpty()) return false;
    return s.chars().allMatch(Character::isDigit);
}

// Check if palindrome
public static boolean isPalindrome(String s) {
    int left = 0, right = s.length() - 1;
    while (left < right) {
        if (s.charAt(left) != s.charAt(right)) return false;
        left++; right--;
    }
    return true;
}

// Repeat string (Java 11+)
String repeated = "ha".repeat(3);  // "hahaha"

// Indent (Java 12+)
String indented = "hello".indent(4);  // "    hello\n"

// Transform (Java 12+)
String result = "42".transform(Integer::parseInt);  // 42 (as Integer)
```

---

## 2. StringBuilder & StringBuffer

### Why StringBuilder?

```java
// ❌ TERRIBLE — O(n²) time!
String s = "";
for (int i = 0; i < 10_000; i++) {
    s += i;  // creates a new String object EACH iteration
}
// Each += copies the entire existing string → 1 + 2 + 3 + ... + n = O(n²)

// ✅ GOOD — O(n) time!
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 10_000; i++) {
    sb.append(i);
}
String s = sb.toString();
```

### StringBuilder API

```java
StringBuilder sb = new StringBuilder();       // default capacity 16
StringBuilder sb = new StringBuilder(100);    // initial capacity 100
StringBuilder sb = new StringBuilder("Hello"); // starts with content

// Append — the workhorse
sb.append("Hello");           // "Hello"
sb.append(' ');               // "Hello "
sb.append(42);                // "Hello 42"
sb.append(true);              // "Hello 42true"
sb.append(new char[]{'!', '?'});  // "Hello 42true!?"

// Insert
sb.insert(5, ",");            // "Hello, 42true!?" (insert at index 5)

// Delete
sb.delete(5, 7);              // delete [5,7): "Hello42true!?"
sb.deleteCharAt(5);           // delete char at index 5

// Replace
sb.replace(5, 7, " is ");    // replace [5,7): "Hello is true!?"

// Reverse
sb.reverse();                 // reverse entire string

// Length & Capacity
int len = sb.length();
int cap = sb.capacity();
sb.setLength(5);              // truncates to first 5 chars
sb.ensureCapacity(200);       // pre-allocate

// Char access
char c = sb.charAt(0);
sb.setCharAt(0, 'h');         // change first char

// Substring (returns String)
String sub = sb.substring(0, 5);  // returns new String (copy)

// Convert to String
String result = sb.toString();
```

### StringBuilder vs StringBuffer

| Feature | StringBuilder | StringBuffer |
|---------|--------------|--------------|
| Thread safety | Not synchronized | Synchronized |
| Speed | Faster | 2-3x slower |
| Introduced | Java 5 | Java 1.0 |
| When to use | Single-threaded (99% of cases) | Multi-threaded (rare) |

**Rule:** Always use `StringBuilder` unless you're sharing the buffer across threads (which is almost never in DSA).

### Capacity Management

```java
// Default: new StringBuilder() → capacity 16
// If you exceed 16: new capacity = (old * 2) + 2
// Example: 16 → 34 → 70 → 142 → ...

// Pre-sizing tip: if you know approximate length, pre-allocate
StringBuilder sb = new StringBuilder(10_000);  // avoid resizing
```

---

## 3. StringJoiner (Java 8+)

```java
import java.util.StringJoiner;

StringJoiner joiner = new StringJoiner(", ", "[", "]");
joiner.add("apple");
joiner.add("banana");
joiner.add("cherry");
System.out.println(joiner);  // [apple, banana, cherry]

// Without prefix/suffix
StringJoiner simple = new StringJoiner("-");
simple.add("2024");
simple.add("01");
simple.add("15");
// "2024-01-15"

// Merge StringJoiners
StringJoiner a = new StringJoiner(",");
a.add("1").add("2");
StringJoiner b = new StringJoiner(",");
b.add("3").add("4");
a.merge(b);  // "1,2,3,4"
```

---

## 4. StringTokenizer (Legacy, but still seen)

```java
String input = "apple banana cherry date";
StringTokenizer st = new StringTokenizer(input);  // default delimiter: whitespace

while (st.hasMoreTokens()) {
    System.out.println(st.nextToken());
}

// With custom delimiter
String data = "apple,banana,cherry,date";
StringTokenizer st = new StringTokenizer(data, ",");

// ⚠️ StringTokenizer doesn't support empty tokens
// "a,,b" with "," → ["a", "b"] (skips empty)
// String.split(",") → ["a", "", "b"]

// Typically, split() or Scanner is preferred over StringTokenizer
```

---

## 5. Pattern Matching with Regex (Pattern/Matcher)

```java
import java.util.regex.*;

String text = "My email is alice@example.com and bob@test.org";

// Compile regex pattern
Pattern pattern = Pattern.compile("\\b[\\w.%-]+@[\\w.-]+\\.[A-Za-z]{2,}\\b");
Matcher matcher = pattern.matcher(text);

while (matcher.find()) {
    System.out.println("Found: " + matcher.group());       // alice@example.com
    System.out.println("Start: " + matcher.start());       // 12
    System.out.println("End: " + matcher.end());           // 30
}

// Check if entire string matches
boolean isEmail = Pattern.matches("\\b[\\w.%-]+@[\\w.-]+\\.[A-Za-z]{2,}\\b", "a@b.co");

// Split using regex
String[] parts = text.split("@|\\.");

// Common regex patterns for DSA
Pattern digits = Pattern.compile("\\d+");
Pattern words = Pattern.compile("\\w+");
Pattern whitespace = Pattern.compile("\\s+");

// Replace with regex
String cleaned = text.replaceAll("\\d+", "[NUMBER]");
String masked = text.replaceAll("(?<=.{3}).(?=[^@]*@)", "*");  // mask email: ali***********com
```

---

## 6. Common Pitfalls

### Pitfall 1: Concatenation in Loops (Runtime Nightmare)

```java
// ❌ O(n²)
String s = "";
for (int i = 0; i < 100_000; i++) {
    s += i;
}

// ✅ O(n)
StringBuilder sb = new StringBuilder(100_000);
for (int i = 0; i < 100_000; i++) {
    sb.append(i);
}
```

**Modern Java caveat:** The compiler optimizes simple concatenations:
```java
String s = "a" + "b" + "c";  // compiler creates: "abc" (single string)
String s = a + b + c;         // compiler uses StringBuilder internally
// But in a loop, each iteration creates a new StringBuilder → still O(n²)
```

### Pitfall 2: substring Memory Leak (Pre-Java 7u6)

```java
// Pre-Java 7u6: substring() shared the underlying char[]!
String huge = readHugeString(100_000_000);  // creates a huge char[]
String small = huge.substring(0, 5);        // still references the huge char[]!
// Memory leak! Small string keeps the entire huge array alive.

// Post-Java 7u6: substring() creates a copy — safe.
// No more memory leak.
```

### Pitfall 3: Encoding Issues

```java
// Default encoding (platform-dependent) can cause issues
String s = "café";
byte[] bytes = s.getBytes();             // platform-dependent encoding
byte[] utf8 = s.getBytes(StandardCharsets.UTF_8);  // explicit — always do this
String restored = new String(utf8, StandardCharsets.UTF_8);
```

### Pitfall 4: Immutability Surprises

```java
String s = "hello";
String t = s.toUpperCase();
System.out.println(s);  // "hello" — unchanged!
System.out.println(t);  // "HELLO" — new string

// String methods NEVER modify the original (it's immutable!)
// They always return a new string
```

---

## 7. Performance: Strings vs StringBuilder

```java
// String method chaining — creates intermediate objects
String result = "  hello  ".trim().substring(0, 4).toUpperCase();  // "HELL"

// StringBuilder mutation — no intermediate objects
StringBuilder sb = new StringBuilder("  hello  ");
// trim is not on StringBuilder, so we'd need custom logic
// But for complex operations, StringBuilder is faster

// When the compiler optimizes:
// This is fine — compiler uses StringBuilder
String s = a + "," + b + "," + c;

// This is NOT fine — loop defeats optimization
for (String item : items) {
    s += item + ",";  // StringBuilder created each iteration!
}
```

---

## Cheat Sheet

```java
// STRING
s.length(); s.charAt(i); s.substring(l,r); s.substring(l);
s.indexOf(c); s.lastIndexOf(c); s.contains(s2);
s.startsWith(p); s.endsWith(p);
s.replace(a,b); s.replaceAll(regex, rep);
s.split(regex); s.toCharArray(); s.trim(); s.strip();
s.toUpperCase(); s.toLowerCase();
s.equals(s2); s.equalsIgnoreCase(s2); s.compareTo(s2);
s.isEmpty(); s.isBlank(); s.repeat(n);
String.valueOf(x); String.join(delim, parts);

// STRINGBUILDER
StringBuilder sb = new StringBuilder();
sb.append(x); sb.insert(i, x);
sb.delete(l,r); sb.deleteCharAt(i);
sb.replace(l,r,str); sb.reverse();
sb.length(); sb.setLength(n);
sb.charAt(i); sb.setCharAt(i, c);
sb.substring(l,r); sb.toString();

// REGEX
Pattern p = Pattern.compile(regex);
Matcher m = p.matcher(input);
m.find(); m.group(); m.start(); m.end();

// JOINER
StringJoiner sj = new StringJoiner(delim, prefix, suffix);
sj.add(str);
```

String problems are everywhere in interviews. Know these APIs cold so you can focus on the algorithm, not the syntax.
