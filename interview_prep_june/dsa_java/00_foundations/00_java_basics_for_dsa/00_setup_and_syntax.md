# 00 — Java Setup & Syntax for DSA

So you're ready to grind DSA in Java. Great choice. Java's verbosity can feel like a curse, but its rich standard library, strong typing, and massive community make it a powerhouse for interviews. Let's get the boring (but critical) stuff out of the way first.

---

## 1. JDK Setup & Compilation Basics

### Installing the JDK

Download the latest **JDK LTS** (currently JDK 21) from [Oracle](https://www.oracle.com/java/technologies/downloads/) or use [OpenJDK](https://openjdk.org/). For DSA, any version >= 11 is fine. Java 17+ gives you sealed classes, pattern matching, and records — nice to have but not mandatory.

```bash
# Verify installation
java -version
javac -version

# Expected output (versions may vary)
# openjdk version "21.0.2" 2024-01-16 LTS
# javac 21.0.2
```

### The Compile-Run Dance

```bash
# Compile .java → .class (bytecode)
javac MyProgram.java

# Run the bytecode (no .class extension)
java MyProgram

# For packages, compile from root:
javac -d out src/com/mycompany/Solution.java
java -cp out com.mycompany.Solution
```

**Pro tip:** In DSA/CP contexts, you'll often just have a single `Solution.java` or `Main.java`. Keep it simple — one file, no package, run with `java Main`.

### Anatomy of a Java Program

```java
// This goes in Solution.java
import java.util.*;              // Wildcard import — fine for DSA

public class Solution {          // Class name MUST match filename
    public static void main(String[] args) {
        System.out.println("Hello, DSA!");
    }
}
```

---

## 2. Package Declarations & Imports

```java
// Package declaration (optional for single-file DSA)
package com.techstacks.dsa;

// Import styles
import java.util.Scanner;        // Single class import
import java.util.*;              // Wildcard — convenience over ceremony
import java.io.*;                // For BufferedReader/IOException

// Static imports (rarely used but good to know)
import static java.lang.Math.*;
// Now you can call max(), min(), sqrt() directly
```

**Rule of thumb for DSA:** Just use `import java.util.*;` and `import java.io.*;`. Nobody is judging your import style in an interview.

---

## 3. Variables — Primitives vs Reference Types

Java has exactly **8 primitive types**. Everything else is a reference type (object).

### Primitive Types

| Type    | Size    | Range/Precision                         | Default  | Notes                             |
|---------|---------|------------------------------------------|----------|------------------------------------|
| `byte`  | 8-bit   | -128 to 127                              | `0`      | Good for saving memory in arrays  |
| `short` | 16-bit  | -32,768 to 32,767                        | `0`      | Rarely used                        |
| `int`   | 32-bit  | -2³¹ to 2³¹-1                            | `0`      | Default integer type               |
| `long`  | 64-bit  | -2⁶³ to 2⁶³-1                            | `0L`     | Suffix with L: `long x = 100L;`   |
| `float` | 32-bit  | ±3.4E-38 to ±3.4E+38, ~7 decimal digits | `0.0f`   | Suffix with f: `float x = 3.14f;` |
| `double`| 64-bit  | ±1.7E-308 to ±1.7E+308, ~15 digits      | `0.0d`   | Default decimal type               |
| `boolean`| —      | true or false                            | `false`  | Not 0/1 like C++                   |
| `char`  | 16-bit  | 0 to 65,535 (Unicode)                    | `'\u0000'`| Single quotes: `'A'`              |

### Reference Types

Arrays, Strings, and every class/interface. They store a **memory address** (reference), not the value itself.

```java
// Primitive: stores value directly
int a = 10;
int b = a;    // b gets a copy of 10

// Reference: stores address
int[] arr1 = {1, 2, 3};
int[] arr2 = arr1;          // arr2 points to SAME array
arr2[0] = 99;
System.out.println(arr1[0]); // 99 — same object!

// Objects (including wrapper classes)
Integer x = 100;
Integer y = x;              // y references same Integer
```

### Default Values

Class-level (instance/static) variables get defaults. **Local variables do NOT** — you must initialize them.

```java
public class Defaults {
    int x;          // 0
    double d;       // 0.0
    boolean flag;   // false
    String s;       // null
    int[] arr;      // null

    public void method() {
        int local;      // ❌ COMPILE ERROR: not initialized
        int local = 0;  // ✅ must initialize
    }
}
```

### Constants with `final`

```java
final double PI = 3.14159;
final int MAX_RETRIES = 5;

// Reference type: reference is constant, object can change
final List<String> list = new ArrayList<>();
list.add("hello");          // ✅ allowed — object is mutable
// list = new ArrayList<>(); // ❌ compile error — can't reassign
```

---

## 4. Methods — Syntax, Static vs Instance, Pass-by-Value

### Method Syntax

```java
accessModifier static? returnType methodName(parameters) {
    // body
    return value;  // if returnType is not void
}
```

```java
public static int add(int a, int b) {
    return a + b;
}

public void printArray(int[] arr) {
    for (int x : arr) System.out.print(x + " ");
}
```

### Static vs Instance

```java
public class Calculator {
    // Static method — belongs to the CLASS, not an object
    public static int square(int x) {
        return x * x;
    }

    // Instance method — requires an object
    public int cube(int x) {
        return x * x * x;
    }
}

// Usage
Calculator.square(5);                    // ✅ static call
Calculator.cube(5);                      // ❌ won't compile

Calculator calc = new Calculator();
calc.cube(5);                            // ✅ instance call
calc.square(5);                          // ✅ works but discouraged
```

**Why this matters for DSA:** In competitive programming / interviews, you'll typically have a `Solution` class with a **static method** like `public static int solve(int n)` or a public instance method that LeetCode-style runners call. Get comfortable with both.

### Pass-by-Value — The Key Nuance

Java is **ALWAYS pass-by-value**. Period. The confusion comes from reference types.

```java
public class PassByValue {

    // Primitives: the method gets a COPY
    public static void changePrimitive(int x) {
        x = 100;  // only changes local copy
    }

    // Objects: the method gets a COPY of the reference
    public static void changeReference(int[] arr) {
        arr[0] = 99;  // ✅ changes the object (reference copy points to same object)
        arr = new int[]{5, 6, 7};  // ❌ reassigns local copy — original UNCHANGED
    }

    public static void main(String[] args) {
        int num = 5;
        changePrimitive(num);
        System.out.println(num);  // 5 — unchanged

        int[] nums = {1, 2, 3};
        changeReference(nums);
        System.out.println(nums[0]);  // 99 — object was mutated
        System.out.println(Arrays.toString(nums));  // [99, 2, 3] — not [5,6,7]!
    }
}
```

**TL;DR:** You can mutate the object's state through a reference copy, but you cannot change what the original reference points to.

---

## 5. Input & Output

### Scanner — The Beginner's Friend

```java
import java.util.Scanner;

public class ScanDemo {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int n = sc.nextInt();           // read int
        long l = sc.nextLong();         // read long
        double d = sc.nextDouble();     // read double
        String s = sc.next();           // read single token (no spaces)
        String line = sc.nextLine();    // read entire line

        // ⚠️ THE GOTCHA:
        int age = sc.nextInt();
        String name = sc.nextLine();    // This reads the leftover '\n' from nextInt()!

        // ✅ Fix: consume leftover newline
        int age = sc.nextInt();
        sc.nextLine();                  // consume the newline
        String name = sc.nextLine();    // now reads the actual name

        sc.close();
    }
}
```

### BufferedReader — Faster, Preferred for CP

```java
import java.io.*;

public class BRDemo {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        int n = Integer.parseInt(br.readLine());
        String line = br.readLine();
        String[] tokens = line.split(" ");
        int a = Integer.parseInt(tokens[0]);
        int b = Integer.parseInt(tokens[1]);

        br.close();
    }
}
```

### System.out.println & printf

```java
System.out.println("Hello");        // prints + newline
System.out.print("Hello");          // prints without newline
System.out.printf("%d %s %.2f", 10, "hello", 3.14159);  // formatted

// Common format specifiers:
// %d — integer
// %s — string
// %.2f — float with 2 decimal places
// %n — platform-independent newline
```

---

## 6. Competitive Programming Template — FastReader Class

This is your go-to template. Bookmark it. Memorize it.

```java
import java.io.*;
import java.util.*;

public class Main {

    static class FastReader {
        BufferedReader br;
        StringTokenizer st;

        public FastReader() {
            br = new BufferedReader(new InputStreamReader(System.in));
        }

        String next() {
            while (st == null || !st.hasMoreElements()) {
                try {
                    st = new StringTokenizer(br.readLine());
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            return st.nextToken();
        }

        int nextInt() { return Integer.parseInt(next()); }
        long nextLong() { return Long.parseLong(next()); }
        double nextDouble() { return Double.parseDouble(next()); }
        String nextLine() {
            String str = "";
            try {
                str = br.readLine();
            } catch (IOException e) {
                e.printStackTrace();
            }
            return str;
        }

        int[] nextIntArray(int n) {
            int[] arr = new int[n];
            for (int i = 0; i < n; i++) arr[i] = nextInt();
            return arr;
        }

        long[] nextLongArray(int n) {
            long[] arr = new long[n];
            for (int i = 0; i < n; i++) arr[i] = nextLong();
            return arr;
        }
    }

    // FastWriter for output — avoids System.out bottleneck
    static class FastWriter {
        private final BufferedWriter bw;

        public FastWriter() {
            bw = new BufferedWriter(new OutputStreamWriter(System.out));
        }

        public void print(Object obj) throws IOException {
            bw.write(String.valueOf(obj));
        }

        public void println(Object obj) throws IOException {
            bw.write(String.valueOf(obj));
            bw.newLine();
        }

        public void flush() throws IOException {
            bw.flush();
        }

        public void close() throws IOException {
            bw.close();
        }
    }

    public static void main(String[] args) {
        FastReader sc = new FastReader();
        // Your DSA solution here
        int n = sc.nextInt();
        System.out.println(n * 2);
    }
}
```

**Why this matters:** `Scanner` is slow for large inputs (50k+ lines). `BufferedReader` + `StringTokenizer` is ~5-10x faster. In platforms like CodeChef, HackerRank, or custom input tests, this can be the difference between AC (Accepted) and TLE (Time Limit Exceeded).

---

## 7. Common Pitfalls — Watch Out!

| Pitfall | Explanation | Fix |
|---------|-------------|-----|
| `Scanner` after `nextInt` leaves `\n` | `nextLine()` will read empty string | Add `sc.nextLine()` after `nextInt()` |
| `==` with Strings | Compares references, not content | Use `.equals()` |
| Integer overflow | `int x = 100000 * 100000` → overflow | Use `long` or `BigInteger` |
| Division by integers | `3/2` → `1`, not `1.5` | Use `3/2.0` or cast: `(double)3/2` |
| `ArrayIndexOutOfBounds` | Accessing index `n` in array of size `n` | Remember: `0` to `n-1` |
| Not closing resources | File handles leak | Use try-with-resources |
| Local variables uninitialized | Compiler error | Always initialize |

---

## Quick Reference Card

```java
// === COMPILATION ===
// javac File.java → java File

// === VARIABLES ===
int x = 10; long l = 10L; float f = 3.14f; double d = 3.14;
boolean b = true; char c = 'A'; byte by = 127; short sh = 1000;
final int CONST = 42;

// === INPUT ===
Scanner sc = new Scanner(System.in);
BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
StringTokenizer st = new StringTokenizer(br.readLine());

// === OUTPUT ===
System.out.println(x);
System.out.printf("n = %d%n", x);
```

Next up: **Control Flow** — making decisions and looping like a pro.
