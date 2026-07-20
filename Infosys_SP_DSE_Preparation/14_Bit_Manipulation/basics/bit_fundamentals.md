# Bit Manipulation Fundamentals

## 1. Binary Representation

Every integer in Python is stored in binary (base-2). Understanding binary is crucial for bit manipulation.

```python
def binary_representation(n):
    """Show binary representation of a number"""
    if n == 0:
        return "0"
    
    result = []
    while n > 0:
        result.append(str(n % 2))
        n //= 2
    
    return ''.join(reversed(result))

# Example
print(binary_representation(13))  # Output: 1101
print(binary_representation(0))   # Output: 0

# Python built-in functions
n = 13
print(bin(n))      # '0b1101'
print(oct(n))      # '0o15'
print(hex(n))      # '0xd'
```

**Time Complexity:** O(log n) - Number of bits needed
**Space Complexity:** O(log n) - To store the binary string

---

## 2. Bitwise Operators

### AND (`&`), OR (`|`), XOR (`^`), NOT (`~`), LEFT SHIFT (`<<`), RIGHT SHIFT (`>>`)

```python
def bitwise_operators_demo():
    a = 12  # 1100 in binary
    b = 10  # 1010 in binary
    
    # AND (&): Both bits must be 1
    and_result = a & b
    print(f"{a} & {b} = {and_result}")  # 1100 & 1010 = 1000 = 8
    
    # OR (|): At least one bit must be 1
    or_result = a | b
    print(f"{a} | {b} = {or_result}")   # 1100 | 1010 = 1110 = 14
    
    # XOR (^): Bits must be different
    xor_result = a ^ b
    print(f"{a} ^ {b} = {xor_result}")  # 1100 ^ 1010 = 0110 = 6
    
    # NOT (~): Invert all bits (two's complement)
    not_result = ~a
    print(f"~{a} = {not_result}")       # ~12 = -13
    
    # LEFT SHIFT (<<): Multiply by 2^n
    left_shift = a << 2
    print(f"{a} << 2 = {left_shift}")   # 12 << 2 = 48
    
    # RIGHT SHIFT (>>): Divide by 2^n
    right_shift = a >> 2
    print(f"{a} >> 2 = {right_shift}")  # 12 >> 2 = 3

bitwise_operators_demo()
```

### Operator Truth Tables

```
AND:          OR:           XOR:
0 & 0 = 0     0 | 0 = 0     0 ^ 0 = 0
0 & 1 = 0     0 | 1 = 1     0 ^ 1 = 1
1 & 0 = 0     1 | 0 = 1     1 ^ 0 = 1
1 & 1 = 1     1 | 1 = 1     1 ^ 1 = 0
```

---

## 3. Properties of Bitwise Operators

```python
def demonstrate_properties():
    a, b, c = 5, 3, 7
    
    # Commutative Property
    print(f"a & b = {a & b}, b & a = {b & a}")  # Same
    print(f"a | b = {a | b}, b | a = {b | a}")  # Same
    print(f"a ^ b = {a ^ b}, b ^ a = {b ^ a}")  # Same
    
    # Associative Property
    print(f"(a & b) & c = {(a & b) & c}")
    print(f"a & (b & c) = {a & (b & c)}")        # Same
    
    # Distributive Property (AND over OR)
    print(f"a & (b | c) = {a & (b | c)}")
    print(f"(a & b) | (a & c) = {(a & b) | (a & c)}")  # Same
    
    # Identity Elements
    print(f"a & 0 = {a & 0}")    # 0 (AND with 0 gives 0)
    print(f"a | 0 = {a | 0}")    # a (OR with 0 gives a)
    print(f"a ^ 0 = {a ^ 0}")    # a (XOR with 0 gives a)
    
    # Self-inverse Property
    print(f"a ^ a = {a ^ a}")    # 0 (XOR with self gives 0)
    
    # De Morgan's Laws (for bits)
    print(f"~(a & b) = {~(a & b)}")
    print(f"~a | ~b = {~a | ~b}")  # Same (in two's complement)
    
    # Left shift is multiplication by 2^n
    print(f"5 << 3 = {5 << 3}")  # 5 * 2^3 = 40
    
    # Right shift is division by 2^n
    print(f"40 >> 3 = {40 >> 3}")  # 40 / 2^3 = 5

demonstrate_properties()
```

---

## 4. Check if Number is Power of 2

**Key Insight:** A power of 2 has exactly one bit set in binary.
- 1 = 0001
- 2 = 0010
- 4 = 0100
- 8 = 1000

**Trick:** `n & (n-1)` removes the lowest set bit. If result is 0, then n was a power of 2.

```python
def is_power_of_two(n):
    """Check if n is a power of 2"""
    if n <= 0:
        return False
    return (n & (n-1)) == 0

# Alternative: Count set bits
def is_power_of_two_v2(n):
    """Check if n is a power of 2 by counting bits"""
    if n <= 0:
        return False
    count = 0
    while n > 0:
        if n & 1:
            count += 1
        n >>= 1
    return count == 1

# Test
print(is_power_of_two(16))   # True (10000)
print(is_power_of_two(18))   # False (10010)
print(is_power_of_two(1))    # True (1 is 2^0)
print(is_power_of_two(0))    # False
print(is_power_of_two(-8))   # False
```

**Time Complexity:** O(1) for first method, O(log n) for second
**Space Complexity:** O(1)

---

## 5. Count Set Bits (Brian Kernighan's Algorithm)

**Normal approach:** Check each bit - O(log n)
**Brian Kernighan's:** `n & (n-1)` clears lowest set bit - O(set bits)

```python
def count_set_bits_normal(n):
    """Count set bits by checking each bit"""
    count = 0
    while n > 0:
        if n & 1:
            count += 1
        n >>= 1
    return count

def count_set_bits_kernighan(n):
    """Brian Kernighan's algorithm - O(number of set bits)"""
    count = 0
    while n > 0:
        n = n & (n - 1)  # Clear lowest set bit
        count += 1
    return count

def count_set_bits_builtin(n):
    """Using Python built-in (most efficient in Python)"""
    return bin(n).count('1')

# Test
n = 29  # 11101 in binary
print(f"Normal: {count_set_bits_normal(n)}")      # 4
print(f"Kernighan: {count_set_bits_kernighan(n)}") # 4
print(f"Built-in: {count_set_bits_builtin(n)}")    # 4
```

**Time Complexity:**
- Normal: O(log n) - checks all bits
- Kernighan's: O(k) where k = number of set bits
- Built-in: O(log n) internally

---

## 6. Find Single Number (XOR Property)

**Key Insight:** XOR of same numbers is 0, XOR of 0 and number is the number itself.
- `a ^ a = 0`
- `a ^ 0 = a`
- XOR is commutative and associative

```python
def find_single_number(nums):
    """Find single number where every other appears twice"""
    result = 0
    for num in nums:
        result ^= num
    return result

# Example: [2, 3, 2, 4, 3] → 4
# 2 ^ 3 ^ 2 ^ 4 ^ 3
# = (2 ^ 2) ^ (3 ^ 3) ^ 4
# = 0 ^ 0 ^ 4
# = 4

print(find_single_number([2, 3, 2, 4, 3]))  # Output: 4
print(find_single_number([1]))               # Output: 1
print(find_single_number([4, 1, 2, 1, 2]))  # Output: 4
```

**Time Complexity:** O(n)
**Space Complexity:** O(1)

---

## 7. Find Single Number II (Counting Bits)

**Problem:** Every element appears 3 times except one appears once.
**Solution:** Count set bits at each position. If count % 3 != 0, that bit belongs to the single number.

```python
def find_single_number_ii(nums):
    """Find single number where every other appears 3 times"""
    result = 0
    
    # Check each bit position (32 bits for integers)
    for i in range(32):
        bit_count = 0
        
        # Count set bits at position i
        for num in nums:
            if num & (1 << i):
                bit_count += 1
        
        # If count is not divisible by 3, set this bit in result
        if bit_count % 3 != 0:
            result |= (1 << i)
    
    return result

# More efficient version using ones and twos
def find_single_number_ii_efficient(nums):
    """Efficient solution using state machine concept"""
    ones = 0
    twos = 0
    
    for num in nums:
        # Update twos: bits that appeared twice
        twos |= ones & num
        
        # Update ones: bits that appeared once
        ones ^= num
        
        # Find bits that appeared three times
        threes = ones & twos
        
        # Remove bits that appeared three times
        ones &= ~threes
        twos &= ~threes
    
    return ones

# Test
print(find_single_number_ii([2, 2, 3, 2]))      # Output: 3
print(find_single_number_ii([0, 1, 0, 1, 0, 1, 99]))  # Output: 99
print(find_single_number_ii_efficient([2, 2, 3, 2]))  # Output: 3
```

**Time Complexity:** O(32n) = O(n) for both methods
**Space Complexity:** O(1)

---

## 8. Swap Two Numbers Without Temp

**XOR Swap Trick:**
- `a = a ^ b`
- `b = a ^ b`
- `a = a ^ b`

```python
def swap_without_temp(a, b):
    """Swap two numbers without using temporary variable"""
    print(f"Before: a = {a}, b = {b}")
    
    a = a ^ b
    b = a ^ b  # b = (a ^ b) ^ b = a
    a = a ^ b  # a = (a ^ b) ^ a = b
    
    print(f"After: a = {a}, b = {b}")
    return a, b

# Or simply in Python
a, b = 5, 10
a, b = b, a  # Pythonic way

# Using XOR (for demonstration)
def swap_xor(a, b):
    a ^= b
    b ^= a
    a ^= b
    return a, b

print(swap_without_temp(5, 10))  # After: a = 10, b = 5
print(swap_xor(5, 10))          # (10, 5)

# Note: In Python, a, b = b, a is preferred as it's cleaner
# The XOR method is more useful in languages without tuple unpacking
```

**Time Complexity:** O(1)
**Space Complexity:** O(1)

---

## 9. Check if ith Bit is Set

```python
def is_ith_bit_set(n, i):
    """Check if ith bit (0-indexed) is set"""
    return (n >> i) & 1 == 1

# Alternative using AND with mask
def is_ith_bit_set_mask(n, i):
    """Check if ith bit is set using mask"""
    mask = 1 << i
    return (n & mask) != 0

# Test
n = 12  # 1100 in binary
print(f"Bit 0 of {n}: {is_ith_bit_set(n, 0)}")  # False (rightmost)
print(f"Bit 1 of {n}: {is_ith_bit_set(n, 1)}")  # False
print(f"Bit 2 of {n}: {is_ith_bit_set(n, 2)}")  # True
print(f"Bit 3 of {n}: {is_ith_bit_set(n, 3)}")  # True

# Using built-in
print(f"Bit 2: {(12 >> 2) & 1}")  # 1
```

**Time Complexity:** O(1)
**Space Complexity:** O(1)

---

## 10. Set, Clear, Flip ith Bit

```python
def set_ith_bit(n, i):
    """Set (make 1) the ith bit"""
    return n | (1 << i)

def clear_ith_bit(n, i):
    """Clear (make 0) the ith bit"""
    return n & ~(1 << i)

def flip_ith_bit(n, i):
    """Flip (toggle) the ith bit"""
    return n ^ (1 << i)

def update_ith_bit(n, i, bit_value):
    """Set ith bit to specific value (0 or 1)"""
    if bit_value == 1:
        return set_ith_bit(n, i)
    else:
        return clear_ith_bit(n, i)

# Test
n = 12  # 1100 in binary

print(f"Original: {n} = {bin(n)}")           # 12 = 0b1100
print(f"Set bit 1: {set_ith_bit(n, 1)} = {bin(set_ith_bit(n, 1))}")    # 14 = 0b1110
print(f"Clear bit 3: {clear_ith_bit(n, 3)} = {bin(clear_ith_bit(n, 3))}")  # 4 = 0b100
print(f"Flip bit 2: {flip_ith_bit(n, 2)} = {bin(flip_ith_bit(n, 2))}")    # 8 = 0b1000
print(f"Flip bit 0: {flip_ith_bit(n, 0)} = {bin(flip_ith_bit(n, 0))}")    # 13 = 0b1101
```

**Time Complexity:** O(1)
**Space Complexity:** O(1)

---

## 11. Generate All Subsets Using Bitmasks

**Key Insight:** For n elements, there are 2^n subsets. Each subset can be represented by a binary number of n bits.

```python
def generate_subsets_bitmask(nums):
    """Generate all subsets using bitmasks"""
    n = len(nums)
    subsets = []
    
    # Iterate from 0 to 2^n - 1
    for mask in range(1 << n):  # 2^n subsets
        subset = []
        for i in range(n):
            # Check if ith bit is set
            if mask & (1 << i):
                subset.append(nums[i])
        subsets.append(subset)
    
    return subsets

# Alternative: More efficient approach
def generate_subsets_v2(nums):
    """Generate subsets using bit manipulation"""
    n = len(nums)
    result = []
    
    for mask in range(1 << n):
        subset = []
        temp = mask
        bit_pos = 0
        
        while temp > 0:
            if temp & 1:
                subset.append(nums[bit_pos])
            temp >>= 1
            bit_pos += 1
        
        result.append(subset)
    
    return result

# Test
nums = [1, 2, 3]
subsets = generate_subsets_bitmask(nums)
print(f"Subsets of {nums}:")
for i, subset in enumerate(subsets):
    print(f"  {bin(i)[2:].zfill(3)}: {subset}")

# Output:
# 000: []
# 001: [1]
# 010: [2]
# 011: [1, 2]
# 100: [3]
# 101: [1, 3]
# 110: [2, 3]
# 111: [1, 2, 3]
```

**Time Complexity:** O(2^n * n) - 2^n subsets, each takes O(n) to build
**Space Complexity:** O(2^n * n) - To store all subsets

---

## 12. Advanced Bit Tricks

```python
def isolate_rightmost_set_bit(n):
    """Isolate the rightmost set bit"""
    return n & (-n)

def remove_rightmost_set_bit(n):
    """Remove the rightmost set bit"""
    return n & (n - 1)

def check_if_power_of_4(n):
    """Check if number is power of 4"""
    return n > 0 and (n & (n-1)) == 0 and (n & 0xAAAAAAAA) == 0

def find_unique_among_pairs(nums):
    """Find unique element where all others appear in pairs"""
    result = 0
    for num in nums:
        result ^= num
    return result

def find_unique_among_triplets(nums):
    """Find unique element where all others appear 3 times"""
    ones = twos = 0
    for num in nums:
        twos |= ones & num
        ones ^= num
        threes = ones & twos
        ones &= ~threes
        twos &= ~threes
    return ones

# Test
print(f"Isolate rightmost set bit of 12: {isolate_rightmost_set_bit(12)}")  # 4
print(f"Remove rightmost set bit of 12: {remove_rightmost_set_bit(12)}")    # 8
print(f"16 is power of 4: {check_if_power_of_4(16)}")    # True
print(f"8 is power of 4: {check_if_power_of_4(8)}")      # False
print(f"Unique among pairs [1,2,1,3,3]: {find_unique_among_pairs([1,2,1,3,3])}")  # 2
print(f"Unique among triplets [2,2,3,2]: {find_unique_among_triplets([2,2,3,2])}")  # 3
```

---

## 13. Bit Manipulation for Competitive Programming

```python
def count_flips_to_convert(a, b):
    """Count number of bits to flip to convert a to b"""
    xor = a ^ b
    count = 0
    while xor > 0:
        count += 1
        xor &= (xor - 1)  # Clear rightmost set bit
    return count

def find_two_odd_occurrence(nums):
    """Find two numbers appearing odd times while others appear even times"""
    xor_all = 0
    for num in nums:
        xor_all ^= num
    
    # Find rightmost set bit
    rightmost_bit = xor_all & (-xor_all)
    
    a = b = 0
    for num in nums:
        if num & rightmost_bit:
            a ^= num
        else:
            b ^= num
    
    return a, b

def reverse_bits(n):
    """Reverse all bits of a 32-bit integer"""
    result = 0
    for i in range(32):
        result <<= 1
        result |= (n & 1)
        n >>= 1
    return result

def has_alternate_bits(n):
    """Check if number has alternating bits"""
    xor = n ^ (n >> 1)
    return (xor & (xor + 1)) == 0

# Test
print(f"Flips to convert 10 to 20: {count_flips_to_convert(10, 20)}")
print(f"Two odd occurrences [1,2,1,3,2,5]: {find_two_odd_occurrence([1,2,1,3,2,5])}")  # (3, 5)
print(f"Reverse bits of 13: {reverse_bits(13)}")
print(f"5 (101) has alternate bits: {has_alternate_bits(5)}")    # True
print(f"7 (111) has alternate bits: {has_alternate_bits(7)}")    # False
```

---

## Summary Table

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Binary Conversion | O(log n) | O(log n) |
| Bitwise Operators | O(1) | O(1) |
| Check Power of 2 | O(1) | O(1) |
| Count Set Bits | O(set bits) | O(1) |
| Find Single Number | O(n) | O(1) |
| Check/Set/Clear/Flip Bit | O(1) | O(1) |
| Generate Subsets | O(2^n * n) | O(2^n * n) |

---

## Key Patterns for Infosys SP DSE

1. **XOR Pattern:** Use for finding unique elements, pair problems
2. **Power of 2 Check:** Use `n & (n-1) == 0`
3. **Bit Counting:** Use Brian Kernighan's for efficiency
4. **Subset Generation:** Use bitmasks for combinatorial problems
5. **Single Number Variations:** ones/twos pattern for 3x problems
6. **Bit DP:** Use bitmasks to represent states in DP
7. **Swap without Temp:** XOR trick for in-place operations
