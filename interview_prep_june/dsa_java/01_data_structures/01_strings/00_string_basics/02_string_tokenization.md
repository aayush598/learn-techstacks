# String Tokenization

## split(regex) Method

```java
String s = "apple,banana,cherry";
String[] parts = s.split(","); // ["apple", "banana", "cherry"]
```

### Multiple delimiters

```java
String s = "apple|banana,cherry;date";
String[] parts = s.split("[|,;]"); // regex character class
```

### Limitations and gotchas

#### Empty strings

```java
String s = "a,,b,,c";
String[] parts = s.split(",");
// Java 8+: ["a", "", "b", "", "c"] (5 elements)
// Java 7 and earlier with trailing:
```

#### Trailing empty strings

```java
String s = "a,b,c,";
String[] parts = s.split(",");
// ["a", "b", "c"] — trailing empty strings are REMOVED

// To keep trailing empties, use limit parameter:
parts = s.split(",", -1);
// ["a", "b", "c", ""] — negative limit keeps all
```

#### split() with limit parameter

```java
s.split(",", 2);  // at most 2 parts: ["a", "b,c"]
s.split(",", 5);  // at most 5 parts: ["a", "b", "c"]
s.split(",", -1); // keep trailing empties
s.split(",", 0);  // default behavior (drop trailing empties)
```

#### Performance issue

`split()` compiles a new `Pattern` object on every call. For repeated splitting with the same regex, pre-compile:

```java
// SLOW inside a loop:
for (String line : fileLines) {
    String[] parts = line.split(","); // Pattern.compile() each time
}

// FAST:
Pattern commaPattern = Pattern.compile(",");
for (String line : fileLines) {
    String[] parts = commaPattern.split(line); // just split, no compilation
}
```

#### Regex special characters

```java
String s = "a.b.c";
s.split(".");  // WRONG — "." matches any character, returns empty array
s.split("\\."); // CORRECT — escapes to literal dot
s.split(Pattern.quote(".")); // ALSO correct — safer approach

// Other special regex chars: + * ? ^ $ ( ) [ ] { } | \
```

## StringTokenizer Class

Legacy class (available since JDK 1.0). It's fast but has quirks.

```java
String s = "apple banana cherry";
StringTokenizer st = new StringTokenizer(s);
while (st.hasMoreTokens()) {
    System.out.println(st.nextToken());
}
```

### With custom delimiter

```java
StringTokenizer st = new StringTokenizer("a,b,c", ",");
while (st.hasMoreTokens()) {
    System.out.println(st.nextToken());
}
```

### Return delimiters

```java
StringTokenizer st = new StringTokenizer("a,b,c", ",", true);
// Returns: "a", ",", "b", ",", "c"
```

### Why NOT to use StringTokenizer

1. **Implements Enumeration (old interface)** — not Iterator (no enhanced for-each)
2. **Does not support empty tokens** — `"a,,b"` → `["a", "b"]`, the empty token is lost
3. **Deprecated in practice** — Java docs recommend using `split()` or `Scanner`
4. **No regex support** — only single-char delimiters

**The only advantage:** It's slightly faster than `split()` for simple cases because it doesn't compile a regex.

## Scanner.next() vs nextLine()

```java
Scanner sc = new Scanner(System.in);
```

### next() — Reads next token (delimited by whitespace)

```java
int num = sc.nextInt();     // read an int
double d = sc.nextDouble(); // read a double
String word = sc.next();    // read a single word (no spaces)
```

### nextLine() — Reads entire line

```java
String line = sc.nextLine(); // reads until newline
```

### The infamous nextInt() + nextLine() bug

```java
Scanner sc = new Scanner(System.in);
System.out.print("Enter age: ");
int age = sc.nextInt();        // reads "25\n" → only consumes "25"

System.out.print("Enter name: ");
String name = sc.nextLine();   // immediately returns "" (consumes leftover "\n")
```

**Fix:** Consume the leftover newline:

```java
int age = sc.nextInt();
sc.nextLine(); // consume the leftover newline
String name = sc.nextLine();
```

Or use `nextLine()` for everything and parse:

```java
int age = Integer.parseInt(sc.nextLine());
String name = sc.nextLine();
```

### Scanner vs BufferedReader for large input

```java
// Scanner: slower, convenient methods (nextInt, nextDouble, etc.)
Scanner sc = new Scanner(System.in);

// BufferedReader: faster (~2-3x), but only reads strings
BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
```

For competitive programming, use BufferedReader with StringTokenizer:

```java
BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
StringTokenizer st = new StringTokenizer(br.readLine());
int n = Integer.parseInt(st.nextToken());
int m = Integer.parseInt(st.nextToken());
```

## StringJoiner

Introduced in Java 8. Joins strings with a delimiter, optional prefix/suffix.

```java
StringJoiner sj = new StringJoiner(", ");
sj.add("apple");
sj.add("banana");
sj.add("cherry");
String result = sj.toString(); // "apple, banana, cherry"
```

### With prefix and suffix

```java
StringJoiner sj = new StringJoiner(", ", "[", "]");
sj.add("apple").add("banana").add("cherry");
// "[apple, banana, cherry]"
```

### setEmptyValue()

```java
StringJoiner sj = new StringJoiner(", ");
sj.setEmptyValue("(empty)");
System.out.println(sj.toString()); // "(empty)"
```

## Collectors.joining() in Streams

```java
List<String> list = Arrays.asList("apple", "banana", "cherry");

String result = list.stream()
    .collect(Collectors.joining(", "));
// "apple, banana, cherry"

String result2 = list.stream()
    .collect(Collectors.joining(", ", "[", "]"));
// "[apple, banana, cherry]"
```

### With mapping

```java
String result = list.stream()
    .map(String::toUpperCase)
    .collect(Collectors.joining(", "));
// "APPLE, BANANA, CHERRY"
```

## Performance Comparison

| Method | Speed | Memory | Regex | Empty Tokens |
|--------|-------|--------|-------|--------------|
| split() | Medium | High | Yes | Configurable |
| StringTokenizer | Fast | Low | No | No |
| Scanner | Slow | Medium | Yes | Yes |
| StringJoiner | Fast | Low | N/A | N/A |
| Collectors.joining | Fast | Low | N/A | N/A |

## Practice Problems

| Problem | Platform | Concept |
|---------|----------|---------|
| Reverse Words in a String | LeetCode 151 | split() + join |
| Simplify Path | LeetCode 71 | split("/") |
| Compare Version Numbers | LeetCode 165 | split("\\.") |
| Decode String | LeetCode 394 | Token parsing |
| Basic Calculator II | LeetCode 227 | Tokenization |

## Quick Reference

| Task | Best Approach |
|------|---------------|
| Split by simple delimiter (once) | `split(",")` |
| Split by simple delimiter (many times) | Pre-compiled Pattern |
| Split by single char (many times, fast) | StringTokenizer (legacy) |
| Read input tokens | Scanner or BufferedReader + StringTokenizer |
| Join with delimiter | `String.join(", ", arr)` |
| Join with prefix/suffix | StringJoiner |
| Stream joining | Collectors.joining() |
