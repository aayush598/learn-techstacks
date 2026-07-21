# String Fundamentals - Python

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

# Empty string
empty = ""
print(len(empty))  # 0

# String with escape characters
escaped = "Line1\nLine2\tTabbed"
print(escaped)
```

## 2. String Indexing and Slicing

```python
s = "Hello, World!"
#  0123456789...

# Indexing (0-based)
print(s[0])    # 'H'
print(s[-1])   # '!' (negative indexing from end)

# Slicing [start:stop:step]
print(s[0:5])    # 'Hello' (indices 0 to 4)
print(s[7:12])   # 'World'
print(s[:5])     # 'Hello' (from beginning)
print(s[7:])     # 'World!' (to end)
print(s[::2])    # 'Hlo ol!' (every 2nd character)
print(s[::-1])   # '!dlroW ,olleH' (reversed string)

# Advanced slicing
print(s[-6:-1])  # 'World'
print(s[::-2])   # '!lo olH' (every 2nd from end)
```

## 3. String Methods

```python
s = "  Hello, World!  "

# Case methods
print(s.upper())          # "  HELLO, WORLD!  "
print(s.lower())          # "  hello, world!  "
print(s.title())          # "  Hello, World!  "
print(s.capitalize())     # "  hello, world!  "
print(s.swapcase())       # "  hELLO, wORLD!  "

# Whitespace methods
print(s.strip())          # "Hello, World!" (remove both)
print(s.lstrip())         # "Hello, World!  " (remove left)
print(s.rstrip())         # "  Hello, World!" (remove right)

# Split and Join
csv_data = "apple,banana,cherry"
fruits = csv_data.split(",")  # ['apple', 'banana', 'cherry']
print(fruits)

joined = " - ".join(fruits)   # "apple - banana - cherry"
print(joined)

# Multi-split
data = "apple,,banana,,,cherry"
result = data.split(",")      # ['apple', '', 'banana', '', '', 'cherry']
result_filtered = [x for x in data.split(",") if x]  # ['apple', 'banana', 'cherry']

# Replace
s = "Hello, World!"
print(s.replace("World", "Python"))   # "Hello, Python!"
print(s.replace("l", "L", 2))         # "HeLLo, World!" (replace first 2)

# Find and Count
s = "banana"
print(s.find("nan"))       # 2 (index of first occurrence)
print(s.find("xyz"))       # -1 (not found)
print(s.rfind("an"))       # 4 (last occurrence)
print(s.count("an"))       # 2
print(s.count("a"))        # 3

# Start/End with
print(s.startswith("ban"))  # True
print(s.endswith("ana"))    # True

# Encoding
s = "Hello"
print(s.encode('utf-8'))    # b'Hello'
print(s.encode('utf-8').decode('utf-8'))  # 'Hello'
```

## 4. String Immutability

```python
# Strings are IMMUTABLE in Python
s = "Hello"
# s[0] = 'h'  # TypeError! Can't modify

# Workaround 1: Convert to list
s_list = list(s)
s_list[0] = 'h'
s_new = "".join(s_list)
print(s_new)  # 'hello'

# Workaround 2: String concatenation (creates new string)
s_new = 'h' + s[1:]
print(s_new)  # 'hello'

# Workaround 3: Use bytearray for mutable string
s_bytes = bytearray("Hello", 'utf-8')
s_bytes[0] = ord('h')
print(s_bytes.decode('utf-8'))  # 'hello'

# Performance note: String concatenation in loops is O(n²)
# Use list append + join for O(n) performance
result = []
for i in range(1000):
    result.append(str(i))
final = ",".join(result)  # O(n) total
```

## 5. String Comparison

```python
# Lexicographic comparison
print("abc" < "abd")    # True (a < a? no, b < b? no, c < d? yes)
print("abc" > "ab")     # True (longer string is greater)
print("abc" == "abc")   # True
print("abc" != "abd")   # True

# Case-sensitive comparison
print("Apple" < "apple")  # True (uppercase < lowercase in ASCII)

# Case-insensitive comparison
s1 = "Hello"
s2 = "hello"
print(s1.lower() == s2.lower())  # True

# Character comparison using ord()
print(ord('A'))  # 65
print(ord('a'))  # 97
print(ord('0'))  # 48

# Sorting strings
words = ["banana", "apple", "cherry"]
print(sorted(words))  # ['apple', 'banana', 'cherry']

# Custom sorting
words = ["banana", "Apple", "cherry"]
print(sorted(words, key=str.lower))  # ['Apple', 'banana', 'cherry']
```

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
print(f"Octal: {age:o}")           # "31"
print(f"With commas: {1000000:,}") # "1,000,000"

# Debugging with f-strings
print(f"{name=}, {age=}")  # "name='Alice', age=25"

# format() method
print("Name: {}, Age: {}".format(name, age))
print("Name: {0}, Age: {1}, Name again: {0}".format(name, age))
print("GPA: {:.2f}".format(gpa))
print("Name: {:>10}".format(name))

# % formatting (old style)
print("Name: %s, Age: %d" % (name, age))
print("GPA: %.2f" % gpa)

# Multi-line formatting
message = f"""
Hello, {name}!
You are {age} years old.
Your GPA is {gpa}.
"""
print(message)
```

## 7. Common CP String Operations

```python
# 1. Reverse a string
def reverse_string(s):
    return s[::-1]

# Using two pointers
def reverse_string_two_pointers(s):
    s_list = list(s)
    left, right = 0, len(s_list) - 1
    while left < right:
        s_list[left], s_list[right] = s_list[right], s_list[left]
        left += 1
        right -= 1
    return "".join(s_list)

print(reverse_string("hello"))  # "olleh"


# 2. Check palindrome
def is_palindrome(s):
    return s == s[::-1]

# Ignore non-alphanumeric characters
def is_palindrome_filtered(s):
    filtered = ''.join(c.lower() for c in s if c.isalnum())
    return filtered == filtered[::-1]

print(is_palindrome("racecar"))  # True
print(is_palindrome_filtered("A man, a plan, a canal: Panama"))  # True


# 3. Count vowels and consonants
def count_vowels_consonants(s):
    vowels = set('aeiouAEIOU')
    v_count = c_count = 0
    for c in s:
        if c.isalpha():
            if c in vowels:
                v_count += 1
            else:
                c_count += 1
    return v_count, c_count

v, c = count_vowels_consonants("Hello World")
print(f"Vowels: {v}, Consonants: {c}")  # Vowels: 3, Consonants: 7


# 4. First non-repeating character
def first_non_repeating(s):
    from collections import Counter
    count = Counter(s)
    for i, c in enumerate(s):
        if count[c] == 1:
            return i
    return -1

print(first_non_repeating("leetcode"))  # 0 ('l')
print(first_non_repeating("loveleetcode"))  # 2 ('v')


# 5. Rotate string
def rotate_string(s, k):
    if not s:
        return s
    k = k % len(s)
    return s[k:] + s[:k]

def rotate_string_left(s, k):
    return rotate_string(s, k)

def rotate_string_right(s, k):
    return rotate_string(s, -k)

print(rotate_string("abcdef", 2))  # "cdefab"
print(rotate_string_right("abcdef", 2))  # "efabcd"


# 6. String to integer (atoi)
def my_atoi(s):
    s = s.strip()
    if not s:
        return 0
    
    sign = 1
    idx = 0
    
    if s[0] in '+-':
        sign = -1 if s[0] == '-' else 1
        idx = 1
    
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


# 7. Integer to Roman
def int_to_roman(num):
    values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    symbols = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    
    result = ""
    for val, sym in zip(values, symbols):
        while num >= val:
            result += sym
            num -= val
    return result

print(int_to_roman(3))     # "III"
print(int_to_roman(58))    # "LVIII"
print(int_to_roman(1994))  # "MCMXCIV"
```

## 8. Additional Useful Operations

```python
# Check if string contains only digits
print("12345".isdigit())    # True
print("123.45".isdigit())   # False

# Check if string is alphanumeric
print("abc123".isalnum())   # True
print("abc 123".isalnum())  # False

# Check if string is alphabetic
print("abc".isalpha())      # True
print("abc1".isalpha())     # False

# Remove duplicates while preserving order
def remove_duplicates(s):
    seen = set()
    result = []
    for c in s:
        if c not in seen:
            seen.add(c)
            result.append(c)
    return "".join(result)

print(remove_duplicates("aabbbccc"))  # "abc"

# Check if strings are rotations of each other
def are_rotations(s1, s2):
    if len(s1) != len(s2):
        return False
    return s2 in s1 + s1

print(are_rotations("abcde", "cdeab"))  # True

# Longest common prefix
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
