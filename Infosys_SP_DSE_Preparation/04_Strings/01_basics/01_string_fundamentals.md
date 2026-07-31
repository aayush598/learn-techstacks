# String Fundamentals - Python - Complete Guide

## 1. String Creation and Initialization

```python
# Different ways to create strings
s1 = "Hello, World!"          # Double quotes
s2 = 'Hello, World!'          # Single quotes
s3 = """Multi-line
string"""                      # Triple quotes (multi-line)
s4 = str(123)                  # Convert number to string
s5 = str([1, 2, 3])            # Convert list to string
s6 = "Hello" * 3               # String repetition: "HelloHelloHello"
s7 = "".join(["a", "b", "c"])  # Join list to string: "abc"
```

### Visual: String in Memory

```
s = "Hello"

Index:  0   1   2   3   4
Char:  'H' 'e' 'l' 'l' 'o'
        ↑
      s[0]

Memory: H | e | l | l | o
        0   1   2   3   4 (indices)
```

---

## 2. String Indexing and Slicing

```python
s = "Hello, World!"
#  0123456789...

# Indexing (0-based)
print(s[0])    # 'H' (first character)
print(s[-1])   # '!' (last character)
```

### Visual: Negative Indexing

```
s = "Hello, World!"

Positive:  0   1   2   3   4   5   6   7   8   9  10  11  12
Char:     'H' 'e' 'l' 'l' 'o' ',' ' ' 'W' 'o' 'r' 'l' 'd' '!'

Negative: -13 -12 -11 -10  -9  -8  -7  -6  -5  -4  -3  -2  -1
                                   ↑
                                 s[-6] = 'W'
```

### Slicing: [start:stop:step]

```python
s = "Hello, World!"

print(s[0:5])    # 'Hello' (indices 0,1,2,3,4)
print(s[7:12])   # 'World' (indices 7,8,9,10,11)
print(s[:5])     # 'Hello' (from beginning)
print(s[7:])     # 'World!' (to end)
print(s[::2])    # 'Hlo ol!' (every 2nd character)
print(s[::-1])   # '!dlroW ,olleH' (reversed string)
```

### Visual: Slicing

```
s = "Hello, World!"
    0123456789...

s[0:5]:
    H e l l o ,
    ↑         ↑
  start    stop (exclusive)
  Result: "Hello"

s[7:12]:
    W o r l d
    ↑       ↑
  start   stop
  Result: "World"

s[::2]:
    H   l   o   o   l
    ↑   ↑   ↑   ↑   ↑
    0   2   4   6   8
  Result: "Hlo ol"
```

---

## 3. String Methods

### Case Methods

```python
s = "Hello, World!"
print(s.upper())          # "HELLO, WORLD!"
print(s.lower())          # "hello, world!"
print(s.title())          # "Hello, World!"
print(s.swapcase())       # "hELLO, wORLD!"
```

### Whitespace Methods

```python
s = "  Hello, World!  "
print(s.strip())          # "Hello, World!" (remove both)
print(s.lstrip())         # "Hello, World!  " (remove left)
print(s.rstrip())         # "  Hello, World!" (remove right)
```

### Split and Join

```python
csv_data = "apple,banana,cherry"
fruits = csv_data.split(",")  # ['apple', 'banana', 'cherry']

joined = " - ".join(fruits)   # "apple - banana - cherry"
```

### Visual: Split and Join

```
Split: "apple,banana,cherry" → ['apple', 'banana', 'cherry']
              ↓ split(',')    ↓
       ┌──────┼──────┐
       ↓      ↓      ↓
     apple  banana  cherry

Join: ['apple', 'banana', 'cherry'] → "apple - banana - cherry"
              ↓ join(' - ')    ↓
       ┌──────┼──────┐
       ↓      ↓      ↓
     apple   -    banana   -    cherry
```

### Find and Count

```python
s = "banana"
print(s.find("nan"))       # 2 (index of first occurrence)
print(s.find("xyz"))       # -1 (not found)
print(s.count("an"))       # 2
print(s.count("a"))        # 3
```

### Visual: Find

```
s = "banana"
    012345

find("nan"):
    b a n a n a
        ↑ ↑ ↑
        n a n
        2 3 4
    Found at index 2 ✓

count("a"):
    b a n a n a
        ↑   ↑
        a   a
    Count: 3 ✓
```

---

## 4. String Immutability

**Strings are IMMUTABLE in Python!**

```python
s = "Hello"
# s[0] = 'h'  # TypeError! Can't modify

# Workaround: Convert to list
s_list = list(s)      # ['H', 'e', 'l', 'l', 'o']
s_list[0] = 'h'      # ['h', 'e', 'l', 'l', 'o']
s_new = "".join(s_list)  # "hello"
```

### Visual:

```
Original:  H | e | l | l | o
            ↓ (immutable!)

Convert to list:  [H, e, l, l, o]
                   ↓ (mutable!)
                  [h, e, l, l, o]

Join back:  h | e | l | l | o = "hello"
```

**Performance Note:** String concatenation in loops is O(n²). Use list append + join!

```python
# BAD: O(n²)
result = ""
for i in range(1000):
    result += str(i)  # Creates new string each time!

# GOOD: O(n)
result = []
for i in range(1000):
    result.append(str(i))
final = ",".join(result)
```

---

## 5. String Comparison

```python
# Lexicographic comparison
print("abc" < "abd")    # True (c < d)
print("abc" > "ab")     # True (longer string is greater)
print("abc" == "abc")   # True

# Case-sensitive comparison
print("Apple" < "apple")  # True (A=65 < a=97 in ASCII)

# Case-insensitive comparison
s1 = "Hello"
s2 = "hello"
print(s1.lower() == s2.lower())  # True
```

### Visual: Lexicographic Comparison

```
"abc" vs "abd"

Compare character by character:
  a == a (equal, continue)
  b == b (equal, continue)
  c < d  (c=99 < d=100)
  
Result: "abc" < "abd" ✓
```

---

## 6. String Formatting

```python
name = "Alice"
age = 25
gpa = 3.85

# f-strings (Python 3.6+) - PREFERRED
print(f"Name: {name}, Age: {age}")
print(f"GPA: {gpa:.2f}")           # "3.85"
print(f"Name: {name:>10}")         # "     Alice" (right-aligned)
print(f"Name: {name:<10}")         # "Alice     " (left-aligned)
print(f"Name: {name:^10}")         # "  Alice   " (centered)
print(f"Binary: {age:b}")          # "11001"
print(f"Hex: {age:x}")             # "19"
print(f"With commas: {1000000:,}") # "1,000,000"

# Debugging with f-strings
print(f"{name=}, {age=}")  # "name='Alice', age=25"
```

---

## 7. Common CP String Operations

### 1. Reverse a String

```python
def reverse_string(s):
    return s[::-1]

# Using two pointers (important for interviews!)
def reverse_string_two_pointers(s):
    s_list = list(s)
    left, right = 0, len(s_list) - 1
    while left < right:
        s_list[left], s_list[right] = s_list[right], s_list[left]
        left += 1
        right -= 1
    return "".join(s_list)

print(reverse_string("hello"))  # "olleh"
```

### Visual: Two Pointer Reverse

```
s = "hello"
    01234

Step 1: left=0, right=4
        h e l l o
        ↑       ↑
        swap h and o
        
Step 2: left=1, right=3
        o e l l h
          ↑   ↑
          swap e and l
          
Step 3: left=2, right=2 (STOP!)
        o l l e h

Result: "olleh"
```

### 2. Check Palindrome

```python
def is_palindrome(s):
    return s == s[::-1]

# Ignore non-alphanumeric characters
def is_palindrome_filtered(s):
    filtered = ''.join(c.lower() for c in s if c.isalnum())
    return filtered == filtered[::-1]

print(is_palindrome("racecar"))  # True
print(is_palindrome_filtered("A man, a plan, a canal: Panama"))  # True
```

### Visual: Palindrome Check

```
"racecar"

Compare from both ends:
  r == r ✓
  a == a ✓
  c == c ✓
  e == e ✓ (middle)
  
Result: True ✓
```

### 3. First Non-Repeating Character

```python
def first_non_repeating(s):
    from collections import Counter
    count = Counter(s)
    for i, c in enumerate(s):
        if count[c] == 1:
            return i
    return -1

print(first_non_repeating("leetcode"))  # 0 ('l')
print(first_non_repeating("loveleetcode"))  # 2 ('v')
```

### Visual:

```
s = "loveleetcode"

Count: {l:2, o:2, v:1, e:4, t:1, c:1, d:1}

Check each character:
  l: count=2 (skip)
  o: count=2 (skip)
  v: count=1 ✓ FOUND!
  
Return index 2
```

### 4. Rotate String

```python
def rotate_string(s, k):
    if not s:
        return s
    k = k % len(s)
    return s[k:] + s[:k]

print(rotate_string("abcdef", 2))  # "cdefab"
```

### Visual: Rotate Left by 2

```
Original: a b c d e f
           0 1 2 3 4 5

Rotate left by 2:
  s[2:] + s[:2] = "cdef" + "ab" = "cdefab"

Result: c d e f a b
```

### 5. String to Integer (atoi)

```python
def my_atoi(s):
    s = s.strip()  # Remove leading/trailing spaces
    if not s:
        return 0
    
    sign = 1
    idx = 0
    
    # Handle sign
    if s[0] in '+-':
        sign = -1 if s[0] == '-' else 1
        idx = 1
    
    # Convert digits
    result = 0
    while idx < len(s) and s[idx].isdigit():
        result = result * 10 + int(s[idx])
        idx += 1
    
    result *= sign
    
    # Clamp to 32-bit signed integer range
    INT_MIN, INT_MAX = -2**31, 2**31 - 1
    if result < INT_MIN:
        return INT_MIN
    if result > INT_MAX:
        return INT_MAX
    return result

print(my_atoi("42"))        # 42
print(my_atoi("   -42"))    # -42
print(my_atoi("4193 with words"))  # 4193
```

### Visual: atoi("  -42")

```
Step 1: Strip spaces → "-42"
Step 2: Check sign → sign = -1
Step 3: Convert digits:
        result = 0
        result = 0 * 10 + 4 = 4
        result = 4 * 10 + 2 = 42
Step 4: Apply sign → -42
```

### 6. Integer to Roman

```python
def int_to_roman(num):
    values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    symbols = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    
    result = ""
    for val, sym in zip(values, symbols):
        while num >= val:
            result += sym
            num -= val
    return result

print(int_to_roman(1994))  # "MCMXCIV"
```

### Visual: int_to_roman(1994)

```
num = 1994

1994 >= 1000? Yes → result = "M", num = 994
994 >= 900? Yes → result = "MCM", num = 94
94 >= 90? Yes → result = "MCMXC", num = 4
4 >= 4? Yes → result = "MCMXCIV", num = 0

Result: "MCMXCIV" ✓
```

---

## 8. Additional Useful Operations

### Check if Strings are Rotations

```python
def are_rotations(s1, s2):
    if len(s1) != len(s2):
        return False
    return s2 in s1 + s1

print(are_rotations("abcde", "cdeab"))  # True
```

### Visual:

```
s1 = "abcde"
s2 = "cdeab"

s1 + s1 = "abcdeabcde"

Is "cdeab" in "abcdeabcde"? Yes! ✓

Because: abcde → cdeab (rotate left by 2)
```

### Longest Common Prefix

```python
def longest_common_prefix(strs):
    if not strs:
        return ""
    prefix = strs[0]
    for s in strs[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix

print(longest_common_prefix(["flower", "flow", "flight"]))  # "fl"
```

### Visual:

```
strs = ["flower", "flow", "flight"]

prefix = "flower"

Compare with "flow":
  "flow" starts with "flower"? No
  "flow" starts with "flowe"? No
  "flow" starts with "flow"? Yes!
  prefix = "flow"

Compare with "flight":
  "flight" starts with "flow"? No
  "flight" starts with "flo"? No
  "flight" starts with "fl"? Yes!
  prefix = "fl"

Result: "fl"
```

---

## Quick Reference

| Operation | Time | Space |
|-----------|------|-------|
| Indexing s[i] | O(1) | O(1) |
| Slicing s[a:b] | O(b-a) | O(b-a) |
| Concatenation s1+s2 | O(n+m) | O(n+m) |
| Join | O(n) | O(n) |
| Split | O(n) | O(n) |
| Find | O(n*m) | O(1) |
| Replace | O(n) | O(n) |
| Comparison | O(n) | O(1) |

## When to Use What

| Problem | Technique |
|---------|-----------|
| Palindrome check | Two pointer from both ends |
| Anagram check | Character count (sorted or hash) |
| Substring search | KMP, Rabin-Karp, or built-in find |
| String matching | Two pointer or sliding window |
| Character frequency | Counter or array of size 26 |
