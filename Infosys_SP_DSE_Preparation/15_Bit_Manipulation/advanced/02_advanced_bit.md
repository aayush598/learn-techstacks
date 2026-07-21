# Advanced Bit Manipulation Techniques

## 1. XOR Technique for Pair Problems

XOR is extremely powerful for problems involving pairs and unique elements.

```python
def find_unique_in_pairs(nums):
    """Find element appearing once while others appear twice"""
    result = 0
    for num in nums:
        result ^= num
    return result

def find_unique_in_triplets(nums):
    """Find element appearing once while others appear thrice"""
    ones = twos = 0
    for num in nums:
        twos |= ones & num
        ones ^= num
        threes = ones & twos
        ones &= ~threes
        twos &= ~threes
    return ones

def find_unique_in_quadruplets(nums):
    """Find element appearing once while others appear four times"""
    # Count bits at each position
    result = 0
    for i in range(32):
        count = 0
        for num in nums:
            if num & (1 << i):
                count += 1
        if count % 4 != 0:
            result |= (1 << i)
    return result

def find_two_unique_elements(nums):
    """Find two elements appearing once while others appear twice"""
    xor_all = 0
    for num in nums:
        xor_all ^= num
    
    # Get rightmost set bit
    rightmost_bit = xor_all & (-xor_all)
    
    a = b = 0
    for num in nums:
        if num & rightmost_bit:
            a ^= num
        else:
            b ^= num
    
    return a, b

# Test
print(f"Unique in pairs [1,2,1,3,3]: {find_unique_in_pairs([1,2,1,3,3])}")  # 2
print(f"Unique in triplets [2,2,3,2]: {find_unique_in_triplets([2,2,3,2])}")  # 3
print(f"Two unique in [1,2,1,3,2,5]: {find_two_unique_elements([1,2,1,3,2,5])}")  # (3, 5)
```

**Time Complexity:** O(n) for all methods
**Space Complexity:** O(1)

---

## 2. Bitwise Sieve of Eratosthenes

Use bit manipulation to store boolean flags efficiently.

```python
def bitwise_sieve(limit):
    """Generate primes using bit manipulation for storage"""
    # Each bit represents if a number is prime
    # Use array of integers where each int stores 32 flags
    
    # Initialize: all bits set to 1 (except 0 and 1)
    size = (limit + 31) // 32
    bits = [0xFFFFFFFF] * size
    
    # Clear bits 0 and 1
    bits[0] &= ~3  # Clear first 2 bits
    
    primes = []
    
    for i in range(2, limit + 1):
        # Check if bit i is set (i is prime)
        word = i // 32
        bit = i % 32
        if bits[word] & (1 << bit):
            primes.append(i)
            # Mark all multiples as not prime
            for j in range(i * i, limit + 1, i):
                word_j = j // 32
                bit_j = j % 32
                bits[word_j] &= ~(1 << bit_j)
    
    return primes

def count_set_bits_bitmap(n):
    """Count numbers with specific bit pattern using bitmap"""
    # Example: Count numbers from 0 to n with exactly k set bits
    def count_with_k_bits(n, k):
        count = 0
        for i in range(n + 1):
            if bin(i).count('1') == k:
                count += 1
        return count
    
    return count_with_k_bits

# More efficient approach using bit DP
def count_numbers_with_k_set_bits(n, k):
    """Count numbers <= n with exactly k set bits"""
    bits = bin(n)[2:]
    length = len(bits)
    
    # dp[i][j][tight] = count of numbers using first i bits
    # with j set bits, tight means prefix equals n's prefix
    from functools import lru_cache
    
    @lru_cache(maxsize=None)
    def dp(i, j, tight):
        if j < 0:
            return 0
        if i == length:
            return 1 if j == 0 else 0
        
        limit = int(bits[i]) if tight else 1
        result = 0
        
        for d in range(limit + 1):
            new_tight = tight and (d == limit)
            result += dp(i + 1, j - d, new_tight)
        
        return result
    
    return dp(0, k, True)

# Test
primes = bitwise_sieve(100)
print(f"Primes up to 100: {primes[:20]}...")

print(f"Numbers <= 15 with exactly 2 set bits: {count_numbers_with_k_set_bits(15, 2)}")
# Numbers: 3(11), 5(101), 6(110), 9(1001), 10(1010), 12(1100) = 6
```

**Time Complexity:**
- Sieve: O(n log log n)
- Count bits: O(length * k * 2) where length = number of bits in n

---

## 3. Counting Bits for All Numbers 0 to n

```python
def count_bits_dp(n):
    """Count set bits for all numbers from 0 to n"""
    dp = [0] * (n + 1)
    
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    
    return dp

def count_bits_shift(n):
    """Alternative approach using shift"""
    result = [0] * (n + 1)
    
    for i in range(1, n + 1):
        result[i] = result[i >> 1] + (i & 1)
    
    return result

def count_bits_with_offset(n):
    """Most efficient approach"""
    dp = [0] * (n + 1)
    offset = 1
    
    for i in range(1, n + 1):
        if offset * 2 == i:
            offset *= 2
        dp[i] = dp[i - offset] + 1
    
    return dp

# Test
n = 15
print(f"Count bits for 0 to {n}:")
bits = count_bits_dp(n)
for i, count in enumerate(bits):
    print(f"  {i:2d} ({bin(i)[2:]:4s}) = {count} bits")

# Output:
# 0  (   0) = 0 bits
# 1  (   1) = 1 bits
# 2  (  10) = 1 bits
# 3  (  11) = 2 bits
# ...
```

**Time Complexity:** O(n)
**Space Complexity:** O(n)

---

## 4. Bit Manipulation for DP (Bitmask DP)

Bitmask DP is used when you need to track subsets of elements.

```python
def traveling_salesman_bitmask_dp(dist):
    """Solve TSP using bitmask DP"""
    n = len(dist)
    INF = float('inf')
    
    # dp[mask][i] = minimum cost to reach city i having visited cities in mask
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0  # Start from city 0
    
    for mask in range(1 << n):
        for u in range(n):
            if dp[mask][u] == INF:
                continue
            if not (mask & (1 << u)):
                continue
            
            for v in range(n):
                if mask & (1 << v):
                    continue  # Already visited
                
                new_mask = mask | (1 << v)
                dp[new_mask][v] = min(dp[new_mask][v], 
                                     dp[mask][u] + dist[u][v])
    
    # Return to starting city
    full_mask = (1 << n) - 1
    result = min(dp[full_mask][i] + dist[i][0] for i in range(n))
    
    return result

def assignment_problem_bitmask(cost):
    """Solve assignment problem using bitmask DP"""
    n = len(cost)
    INF = float('inf')
    
    # dp[mask] = minimum cost to assign first popcount(mask) workers
    dp = [INF] * (1 << n)
    dp[0] = 0
    
    for mask in range(1 << n):
        if dp[mask] == INF:
            continue
        
        worker = bin(mask).count('1')  # Next worker to assign
        
        for job in range(n):
            if mask & (1 << job):
                continue  # Job already assigned
            
            new_mask = mask | (1 << job)
            dp[new_mask] = min(dp[new_mask], dp[mask] + cost[worker][job])
    
    return dp[(1 << n) - 1]

def min_cost_to_paint_houses(cost, m, n, colors):
    """Minimum cost to paint houses with constraints"""
    # Bitmask representation of color constraints
    dp = [[float('inf')] * (1 << m) for _ in range(n + 1)]
    dp[0][0] = 0
    
    for i in range(n):
        for mask in range(1 << m):
            if dp[i][mask] == float('inf'):
                continue
            
            for color in range(m):
                # Check if color is allowed (not used in last k houses)
                if mask & (1 << color):
                    continue
                
                new_mask = ((mask << 1) | (1 << color)) & ((1 << m) - 1)
                dp[i + 1][new_mask] = min(dp[i + 1][new_mask],
                                         dp[i][mask] + cost[i][color])
    
    return min(dp[n])

# Test TSP
dist = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]
print(f"TSP minimum cost: {traveling_salesman_bitmask_dp(dist)}")

# Test Assignment Problem
cost = [
    [9, 2, 7, 8],
    [6, 4, 3, 7],
    [5, 8, 1, 8],
    [7, 6, 9, 4]
]
print(f"Assignment problem minimum cost: {assignment_problem_bitmask(cost)}")
```

**Time Complexity:** O(2^n * n) for TSP
**Space Complexity:** O(2^n * n)

---

## 5. Hamming Distance

```python
def hamming_distance(x, y):
    """Count number of positions where bits differ"""
    xor = x ^ y
    count = 0
    while xor:
        count += 1
        xor &= xor - 1  # Kernighan's algorithm
    return count

def hamming_distance_all_pairs(nums):
    """Sum of hamming distances between all pairs"""
    total = 0
    for bit in range(32):
        count_ones = 0
        for num in nums:
            if num & (1 << bit):
                count_ones += 1
        count_zeros = len(nums) - count_ones
        total += count_ones * count_zeros  # Each 1 pairs with each 0
    return total

def total_hamming_distance_efficient(nums):
    """Efficient calculation of total hamming distance"""
    total = 0
    n = len(nums)
    
    for i in range(32):
        count = 0
        for num in nums:
            if num & (1 << i):
                count += 1
        # Distance contribution = count * (n - count)
        total += count * (n - count)
    
    return total

# Test
print(f"Hamming distance between 1 and 4: {hamming_distance(1, 4)}")  # 2
print(f"Total hamming distance [4, 14, 2]: {total_hamming_distance_efficient([4, 14, 2])}")
```

**Time Complexity:** O(n) for single pair, O(32n) for all pairs
**Space Complexity:** O(1)

---

## 6. Reverse Bits

```python
def reverse_bits_bruteforce(n):
    """Reverse bits of a 32-bit integer"""
    result = 0
    for i in range(32):
        result <<= 1
        result |= (n & 1)
        n >>= 1
    return result

def reverse_bits_divide_conquer(n):
    """Reverse bits using divide and conquer approach"""
    # Swap adjacent bits
    n = ((n & 0x55555555) << 1) | ((n & 0xAAAAAAAA) >> 1)
    # Swap adjacent pairs
    n = ((n & 0x33333333) << 2) | ((n & 0xCCCCCCCC) >> 2)
    # Swap nibbles
    n = ((n & 0x0F0F0F0F) << 4) | ((n & 0xF0F0F0F0) >> 4)
    # Swap bytes
    n = ((n & 0x00FF00FF) << 8) | ((n & 0xFF00FF00) >> 8)
    # Swap 2-byte pairs
    n = (n << 16) | (n >> 16)
    return n & 0xFFFFFFFF

# Test
n = 13  # 000...01101 in binary
reversed_n = reverse_bits_bruteforce(n)
print(f"Original: {n} = {bin(n)}")
print(f"Reversed: {reversed_n} = {bin(reversed_n)}")
print(f"Divide & Conquer: {reverse_bits_divide_conquer(n)}")
```

**Time Complexity:** O(1) for both methods
**Space Complexity:** O(1)

---

## 7. Power of Two, Three, Four

```python
def is_power_of_two(n):
    """Check if n is power of 2"""
    return n > 0 and (n & (n - 1)) == 0

def is_power_of_three(n):
    """Check if n is power of 3 (no simple bit trick)"""
    if n <= 0:
        return False
    # 3^19 = 1162261467 is max power of 3 in 32-bit int
    return 1162261467 % n == 0

def is_power_of_four(n):
    """Check if n is power of 4"""
    # Power of 4: exactly one bit set, and at even position
    # 1, 4, 16, 64... = 2^0, 2^2, 2^4, 2^6...
    # Mask: 0x55555555 = 01010101010101010101010101010101
    
    if n <= 0:
        return False
    # Check power of 2
    if (n & (n - 1)) != 0:
        return False
    # Check if bit is at even position
    return (n & 0x55555555) != 0

def largest_power_of_two_leq(n):
    """Find largest power of 2 less than or equal to n"""
    if n <= 0:
        return 0
    n |= (n >> 1)
    n |= (n >> 2)
    n |= (n >> 4)
    n |= (n >> 8)
    n |= (n >> 16)
    return n - (n >> 1)

def count_set_bits_up_to_n(n):
    """Count total set bits from 1 to n using pattern"""
    if n <= 0:
        return 0
    
    # Find highest power of 2 less than or equal to n
    x = largest_power_of_two_leq(n)
    
    # Bits till x: x * log2(x) / 2
    b = x.bit_length() - 1
    bits_till_x = (b * x) // 2
    
    # Remaining bits
    remaining = n - x
    bits_remaining = remaining + 1
    bits_remaining += count_set_bits_up_to_n(remaining)
    
    return bits_till_x + bits_remaining

# Test
print(f"8 is power of 2: {is_power_of_two(8)}")    # True
print(f"27 is power of 3: {is_power_of_three(27)}")  # True
print(f"16 is power of 4: {is_power_of_four(16)}")  # True
print(f"8 is power of 4: {is_power_of_four(8)}")    # False
print(f"Largest power of 2 <= 10: {largest_power_of_two_leq(10)}")  # 8
```

**Time Complexity:** O(1) for is_power functions, O(log n) for others

---

## 8. Maximum AND Pair

```python
def max_and_pair_bruteforce(nums):
    """Find maximum AND value of any pair - O(n^2)"""
    max_and = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            max_and = max(max_and, nums[i] & nums[j])
    return max_and

def max_and_pair_efficient(nums):
    """Find maximum AND value - O(30n) using greedy bit approach"""
    result = 0
    mask = 0
    
    # Check bits from most significant to least
    for bit in range(30, -1, -1):
        mask |= (1 << bit)
        
        # Count numbers with current prefix
        count = 0
        prefix = result | (1 << bit)
        
        for num in nums:
            if (num & mask) == prefix:
                count += 1
        
        # If at least 2 numbers have this prefix, set the bit
        if count >= 2:
            result |= (1 << bit)
    
    return result

# Test
nums = [3, 10, 5, 25, 2, 8]
print(f"Max AND pair (brute force): {max_and_pair_bruteforce(nums)}")
print(f"Max AND pair (efficient): {max_and_pair_efficient(nums)}")
# Both should return 8 (8 & 10 = 8)
```

**Time Complexity:** O(n^2) for brute force, O(31n) for efficient
**Space Complexity:** O(1)

---

## 9. Minimum XOR Pair

```python
def min_xor_pair_bruteforce(nums):
    """Find minimum XOR value of any pair - O(n^2)"""
    min_xor = float('inf')
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            min_xor = min(min_xor, nums[i] ^ nums[j])
    return min_xor

def min_xor_pair_efficient(nums):
    """Find minimum XOR - O(n log n) using sorting"""
    nums.sort()
    min_xor = float('inf')
    
    for i in range(len(nums) - 1):
        min_xor = min(min_xor, nums[i] ^ nums[i + 1])
    
    return min_xor

def min_xor_pair_trie(nums):
    """Find minimum XOR using Trie - O(n log max_val)"""
    class TrieNode:
        def __init__(self):
            self.children = {}
    
    root = TrieNode()
    
    def insert(num):
        node = root
        for bit in range(31, -1, -1):
            b = (num >> bit) & 1
            if b not in node.children:
                node.children[b] = TrieNode()
            node = node.children[b]
    
    def find_min_xor(num):
        node = root
        result = 0
        for bit in range(31, -1, -1):
            b = (num >> bit) & 1
            # Try to match same bit first
            if b in node.children:
                node = node.children[b]
            else:
                result |= (1 << bit)
                node = node.children[1 - b]
        return result
    
    min_xor = float('inf')
    insert(nums[0])
    
    for i in range(1, len(nums)):
        min_xor = min(min_xor, find_min_xor(nums[i]))
        insert(nums[i])
    
    return min_xor

# Test
nums = [9, 5, 3]
print(f"Min XOR pair (brute force): {min_xor_pair_bruteforce(nums)}")  # 6 (9^3=10, 9^5=12, 5^3=6)
print(f"Min XOR pair (efficient): {min_xor_pair_efficient(nums)}")     # 6
print(f"Min XOR pair (trie): {min_xor_pair_trie(nums)}")              # 6
```

**Time Complexity:** O(n^2) for brute, O(n log n) for sorting, O(n log max) for trie

---

## 10. Bit Manipulation Tricks for CP

```python
def find_duplicate_xor(nums):
    """Find duplicate in array where all others appear once"""
    # This won't work if there are multiple duplicates
    # Use sum method instead
    n = len(nums) - 1
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(nums)
    return actual_sum - expected_sum

def subset_sum_bitmask(nums, target):
    """Check if any subset sums to target"""
    n = len(nums)
    for mask in range(1 << n):
        current_sum = 0
        for i in range(n):
            if mask & (1 << i):
                current_sum += nums[i]
        if current_sum == target:
            return True
    return False

def generate_gray_code(n):
    """Generate n-bit Gray code sequence"""
    result = []
    for i in range(1 << n):
        result.append(i ^ (i >> 1))
    return result

def find_unique_element_among_3n(nums):
    """Find element appearing once while others appear 3 times"""
    # Use bit counting
    result = 0
    for i in range(32):
        count = 0
        for num in nums:
            if num & (1 << i):
                count += 1
        if count % 3 != 0:
            result |= (1 << i)
    return result

def min_flips_to_make_or_equal(a, b, c):
    """Minimum bit flips to make a|b = c"""
    flips = 0
    for i in range(32):
        bit_a = (a >> i) & 1
        bit_b = (b >> i) & 1
        bit_c = (c >> i) & 1
        
        if bit_c == 0:
            # Both a and b must be 0
            flips += bit_a + bit_b
        else:
            # At least one of a or b must be 1
            if bit_a == 0 and bit_b == 0:
                flips += 1
    
    return flips

# Test
print(f"Gray code 3-bit: {generate_gray_code(3)}")
print(f"Unique among 3n [2,2,3,2]: {find_unique_element_among_3n([2,2,3,2])}")
print(f"Min flips to make 1|2=3: {min_flips_to_make_or_equal(1, 2, 3)}")
```

---

## Summary: Key Bit Patterns for Infosys SP DSE

| Pattern | Use Case | Time Complexity |
|---------|----------|-----------------|
| `n & (n-1)` | Clear lowest set bit, power of 2 check | O(1) |
| `n & (-n)` | Isolate lowest set bit | O(1) |
| XOR all | Find unique in pairs | O(n) |
| ones/twos pattern | Find unique in triplets | O(n) |
| Bitmask DP | TSP, assignment problem | O(2^n * n) |
| Greedy bit | Maximum AND pair | O(31n) |
| Trie bit | Minimum XOR pair | O(n log max) |

---

## Tips for Infosys SP DSE

1. **Identify XOR problems:** Look for "appears once", "appears twice", "pairs"
2. **Power of 2:** Always use `n & (n-1) == 0`
3. **Bitmask DP:** When N ≤ 20, consider bitmask for subset problems
4. **Greedy bit:** For AND/XOR optimization, try bits from MSB to LSB
5. **Counting bits:** Use DP relation `dp[i] = dp[i>>1] + (i&1)`
