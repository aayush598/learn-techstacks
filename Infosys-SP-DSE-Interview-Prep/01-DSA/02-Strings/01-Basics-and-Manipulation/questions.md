# 01 Basics And Manipulation — Strings

**100 Interview Q&A — Infosys Specialist Programmer (SP) / Digital Specialist Engineer (DSE)**

<details open>
<summary style='cursor:pointer;font-weight:bold;font-size:1.1em'>Tap to expand all 100 questions</summary>

1. **Define a string and explain immutability in Python.**
   - A string is an immutable sequence of characters. In Python every operation creating a modified string allocates a new object; in-place edits are impossible. This drives O(n) costs for concatenation in loops.

2. **Why is string concatenation in a loop inefficient and how do you fix it?**
   - s += ch rebuilds the whole string each iteration => O(n^2). Fix: collect parts in a list and ''.join(list) once, which is O(total).

3. **Explain the difference between str.replace, split and join with examples.**
   - replace(old,new) substitutes all occurrences; split(sep) returns a list of substrings; sep.join(list) fuses the list back into one string. They are the bread-and-butter of text processing.

4. **What are character frequency counts and where are they used?**
   - A dict/array mapping each character to its count; used for anagram checks, first non-repeating char, permutations, and substring problems that care about multiset equality.

5. **Write code to reverse a string.**
   - s[::-1] returns a reversed copy. Iterative: build list then join reversed. There is no in-place reverse because strings are immutable (mutable alternative: bytearray).

6. **How do you check whether two strings are anagrams?**
   - Compare sorted(s)==sorted(t) (O(n log n)) or verify equal character frequency counts (O(n)). Both must be used with length-equality precheck.

7. **Explain palindrome checking on a string.**
   - Two pointers from both ends comparing characters after lowercasing and skipping non-alphanumerics if the problem allows; return False on first mismatch. O(n) time, O(1) space.

8. **What are common string slicing pitfalls?**
   - Negative indices, step semantics, s[:0] being empty, and forgetting that slicing does not mutate. Also, substring searches like s.find are O(n) per call.

9. **Explain how to build a frequency map for a string in Python.**
   - collections.Counter(s) builds a multiset in O(n); alternatively dict with get(key,0)+1. Counter supports arithmetic (+, -) which is handy for anagram windows.

10. **What is a prefix of a string? Give a use case.**
   - A prefix is any leading contiguous substring (including empty and full). Prefix hashes / trie structures store prefixes to answer prefix queries in O(1)/O(k).

11. **How do you count vowels and consonants in a string?**
   - Iterate characters, check membership in a vowel set, else consonant if alphabetic. Simple O(n). Accounts of case-insensitivity are required.

12. **Explain string immutability benefits.**
   - Safety (strings can be dict keys/hashed safely), thread-safety, and cheap sharing of constants; the cost is allocation for every derived value, which CPython mitigates with interning/small-string caches.

13. **What is string interning?**
   - CPython interns small constant strings (reserved identifiers/names) so they share one object and can be compared with 'is'. Do not rely on it for logic; use ==.

14. **How do you find the first non-repeating character?**
   - Two passes: build Counter, then rescan to return the first char with count 1; else -1. O(n) time, O(26/256) space.

15. **Explain str.format vs f-strings.**
   - f-strings are the modern, fastest, and most readable interpolation; .format is older, still supported, useful when the format template must be a variable.

16. **How do you pad or truncate strings (center, ljust, zfill)?**
   - Methods: s.zfill(width) pads zeros left, s.ljust/rjust/center pad spaces (or given char); string slicing s[:n] truncates. Used in formatting output widths.

17. **What is UTF-8 encoding and why does it matter?**
   - UTF-8 encodes Unicode codepoints into 1–4 bytes and is the dominant web/filesystem encoding; ord()/chr() convert between char and codepoint; len() counts characters, encode('utf-8').__len__ counts bytes.

18. **How do you detect if a character is alphanumeric?**
   - str.isalnum() True for letters+digits; isalpha() letters only; isdigit() digits. Used when filtering inputs prior to palindrome/anagram checks.

19. **Explain the 'longest common prefix' problem.**
   - Vertical scan char by char across all strings until mismatch, or sort and compare first and last strings. O(S) total characters scanned; O(m+n) with sort where m,n are extrema lengths.

20. **How do you check if one string is a rotation of another?**
   - Concatenate s with itself and test whether t is a substring of s+s (lengths must be equal first). Substring search via KMP keeps it O(n).

21. **What is the difference between a character and a byte offset?**
   - In Unicode text, index positions are characters; byte offsets depend on encoding (ASCII=1, others vary). Slicing by character index uses Python's implicit decoding — safe but slower for huge strings.

22. **Explain the StringBuilder pattern in Python.**
   - Python lacks StringBuilder; the idiomatic equivalent is ''.join(list_of_parts), or io.StringIO for large streaming builds. Avoid s += in long loops.

23. **How do you split a string into words?**
   - s.split() splits on any whitespace and drops empty tokens; s.split(sep) splits on the exact separator. Extract words with regex re.findall(r'\w+', s) when punctuation must be removed.

24. **What is a trie (prefix tree) and why is it suited to strings?**
   - A tree where each node holds one character and children are the next characters. Lookup/insertion is O(L) regardless of the number of strings; great for autocomplete, prefixes, and word-breaking.

25. **How would you implement a trie insert and search?**
   - Node = dict of children + is_end flag. Insert: create nodes char by char. Search: walk nodes, check is_end. Prefix walk finds all words with that prefix.

26. **How do you check if a string can be formed by repeating a substring?**
   - Key trick: if s = sub^n and len(s)%len(sub)==0, then s appears in s+s skipping the first char. Return whether s in (s+s)[1:-1] — the LeetCode 459 pattern.

27. **Explain the sliding-window approach to length-of-longest-substring-without-repeating.**
   - Expand right pointer, add char to a set/dict; while a duplicate exists, shrink left pointer. Track max window. O(n) with two pointers + hash.

28. **How do you find all anagrams (permutations) in a string?**
   - Sliding window of length len(p) maintaining a character frequency map; compare with Counter(p) each step using count comparisons — O(|s|) amortised.

29. **What is Z-algorithm and what does its array mean?**
   - Z[i] = length of longest substring starting at i that equals the prefix. Computed in O(n); used in pattern search and string-period problems.

30. **What is KMP and its failure function?**
   - KMP precomputes the LPS (longest proper prefix that is also suffix) array in O(n); pattern search avoids re-scanning matched characters — O(n+m) total.

31. **What is the Rabin-Karp algorithm?**
   - Uses rolling hash to compare substrings' hashes in O(1) after preprocessing; hash collisions are resolved by direct comparison. Average O(n+m), worst O(nm).

32. **What is the shortest palindrome / Mannacher's algorithm context?**
   - Manacher finds the longest palindromic substring in O(n) using center expansion with symmetry mirroring — the standard advanced-string answer for palindrome substrings.

33. **How do you capitalise/transform word cases in Python?**
   - s.upper(), s.lower(), s.title(), s.capitalize(), s.swapcase(). Choose based on exact requirement; beware title() capitalising inside acronyms.

34. **Explain how to validate a substring is contained in a string.**
   - Use 'needle in haystack'(O(n) substring search via fastsearch), str.find returning index or -1, or KMP when doing many searches on the same needle.

35. **What does ord('a') return and how is it useful?**
   - ord('a') returns 97, the ASCII value. Shifting ord(ch)-97 gives 0..25 for 'a'..'z', the classic index into a counting array for lowercase Latin alphabet.

36. **How do you count distinct characters in a string?**
   - len(set(s)). Ordered-first-distinct: build a dict (insertion-ordered) and take keys. For 26-lowercase, a 26-bit integer mask is a space-free set.

37. **Explain the 'defanging / replacing' style sanitisation questions.**
   - Systematic substitutions with .replace() or regex aim to neutralise input (IPs, URLs). The interview intent is string manipulation + edge handling, not security theory.

38. **How do you sort characters of a string by frequency?**
   - Counter(s).most_common() then expand; if equal frequencies, order by char (sort by (-freq, char)). O(n log n).

39. **What is the lexicographical comparison rule in Python?**
   - First differing character decides; if all equal, shorter precedes longer. Tuples/lists compare the same way, which helps in sorting composite keys.

40. **How do you encode/decode URL components?**
   - urllib.parse.quote/unquote percent-encode reserved characters; ensures data survives transport. Encoding/decoding mismatches are a classic bug source.

41. **Explain 'string to integer (atoi)' implementation steps.**
   - Skip whitespace, read optional sign, accumulate digits with overflow clamping; stop at first non-digit. Follow the exact spec of the problem (LeetCode 8).

42. **What are raw strings and f-strings escaping rules?**
   - r'...' keeps backslashes literal (regexes, paths). f'...' interpolates expression results; braces are escaped by doubling. Mixing both is invalid — decided by the r prefix type.

43. **How do you find the longest palindromic substring (centre expansion)?**
   - For each centre (n odd + n-1 even centres), expand while chars match; track the longest. O(n^2) time, O(1) space; Manacher does O(n).

44. **What is the intuition behind the 01 basics and manipulation technique used in coding interviews?**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

45. **Write the brute-force approach for a typical 01 basics and manipulation problem and analyse it.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

46. **State the time and space complexity of the optimal solution for most 01 basics and manipulation problems.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

47. **What common edge cases must be handled in 01 basics and manipulation implementations?**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

48. **How would you dry-run your 01 basics and manipulation code on a small example in an interview?**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

49. **Give a real-world analogy for 01 basics and manipulation.**
   - Analogy: 01 basics and manipulation is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

50. **How do you decide between a hash map, sorting, or two pointers as tools for 01 basics and manipulation?**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

51. **What is the role of a prefix/suffix precomputation in 01 basics and manipulation?**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

52. **Explain the optimisation step you would mention after writing the naive version for 01 basics and manipulation.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

53. **How is 01 basics and manipulation asked differently in an online assessment versus a live interview?**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

54. **What is the intuition behind the 01 basics and manipulation technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

55. **Write the brute-force approach for a typical 01 basics and manipulation problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

56. **State the time and space complexity of the optimal solution for most 01 basics and manipulation problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

57. **What common edge cases must be handled in 01 basics and manipulation implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

58. **How would you dry-run your 01 basics and manipulation code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

59. **Give a real-world analogy for 01 basics and manipulation. Extend your answer with a second example.**
   - Analogy: 01 basics and manipulation is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

60. **How do you decide between a hash map, sorting, or two pointers as tools for 01 basics and manipulation? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

61. **What is the role of a prefix/suffix precomputation in 01 basics and manipulation? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

62. **Explain the optimisation step you would mention after writing the naive version for 01 basics and manipulation. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

63. **How is 01 basics and manipulation asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

64. **What is the intuition behind the 01 basics and manipulation technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

65. **Write the brute-force approach for a typical 01 basics and manipulation problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

66. **State the time and space complexity of the optimal solution for most 01 basics and manipulation problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

67. **What common edge cases must be handled in 01 basics and manipulation implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

68. **How would you dry-run your 01 basics and manipulation code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

69. **Give a real-world analogy for 01 basics and manipulation. Extend your answer with a second example.**
   - Analogy: 01 basics and manipulation is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

70. **How do you decide between a hash map, sorting, or two pointers as tools for 01 basics and manipulation? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

71. **What is the role of a prefix/suffix precomputation in 01 basics and manipulation? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

72. **Explain the optimisation step you would mention after writing the naive version for 01 basics and manipulation. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

73. **How is 01 basics and manipulation asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

74. **What is the intuition behind the 01 basics and manipulation technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

75. **Write the brute-force approach for a typical 01 basics and manipulation problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

76. **State the time and space complexity of the optimal solution for most 01 basics and manipulation problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

77. **What common edge cases must be handled in 01 basics and manipulation implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

78. **How would you dry-run your 01 basics and manipulation code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

79. **Give a real-world analogy for 01 basics and manipulation. Extend your answer with a second example.**
   - Analogy: 01 basics and manipulation is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

80. **How do you decide between a hash map, sorting, or two pointers as tools for 01 basics and manipulation? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

81. **What is the role of a prefix/suffix precomputation in 01 basics and manipulation? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

82. **Explain the optimisation step you would mention after writing the naive version for 01 basics and manipulation. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

83. **How is 01 basics and manipulation asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

84. **What is the intuition behind the 01 basics and manipulation technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

85. **Write the brute-force approach for a typical 01 basics and manipulation problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

86. **State the time and space complexity of the optimal solution for most 01 basics and manipulation problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

87. **What common edge cases must be handled in 01 basics and manipulation implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

88. **How would you dry-run your 01 basics and manipulation code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

89. **Give a real-world analogy for 01 basics and manipulation. Extend your answer with a second example.**
   - Analogy: 01 basics and manipulation is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

90. **How do you decide between a hash map, sorting, or two pointers as tools for 01 basics and manipulation? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

91. **What is the role of a prefix/suffix precomputation in 01 basics and manipulation? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

92. **Explain the optimisation step you would mention after writing the naive version for 01 basics and manipulation. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

93. **How is 01 basics and manipulation asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

94. **What is the intuition behind the 01 basics and manipulation technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

95. **Write the brute-force approach for a typical 01 basics and manipulation problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

96. **State the time and space complexity of the optimal solution for most 01 basics and manipulation problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

97. **What common edge cases must be handled in 01 basics and manipulation implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

98. **How would you dry-run your 01 basics and manipulation code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

99. **Give a real-world analogy for 01 basics and manipulation. Extend your answer with a second example.**
   - Analogy: 01 basics and manipulation is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

100. **How do you decide between a hash map, sorting, or two pointers as tools for 01 basics and manipulation? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

</details>