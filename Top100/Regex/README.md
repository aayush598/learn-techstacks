# Regex Interview Questions and Answers

## Q1: What is a regular expression?
**A:** A regular expression (regex) is a sequence of characters that defines a search pattern. It is used for pattern matching within strings, enabling text search, extraction, validation, and replacement operations.

## Q2: What is the difference between `.test()` and `.exec()` in JavaScript regex?
**A:** `.test()` returns a boolean indicating whether a match exists. `.exec()` returns an array with the matched text, capture groups, index, and input, or `null` if no match. `.exec()` also updates the `lastIndex` property when used with the `g` flag.

## Q3: What do the `^` and `$` anchors do?
**A:** `^` asserts the start of a string (or line in multiline mode). `$` asserts the end of a string (or line). Together, `^pattern$` ensures the entire string matches the pattern exactly.

## Q4: What is the difference between `*` and `+` quantifiers?
**A:** `*` matches zero or more occurrences of the preceding element. `+` matches one or more occurrences. For example, `a*` matches `""`, `"a"`, `"aa"`; `a+` matches `"a"` and `"aa"` but not `""`.

## Q5: What does the `?` quantifier do?
**A:** `?` makes the preceding element optional (matches zero or one time). It also serves as a modifier to make other quantifiers lazy (e.g., `*?`, `+?`, `{2,}?`) instead of greedy.

## Q6: What is the difference between greedy and lazy matching?
**A:** Greedy quantifiers (`*`, `+`, `{}`) match as much as possible. Lazy quantifiers (`*?`, `+?`, `{}?`) match as little as possible. For example, `".*"` on `"a"b"c"` matches `"a"b"c"`, while `".*?"` matches `"a"`.

## Q7: What is a character class (character set)?
**A:** Denoted by `[]`, a character class matches any one character from a set. `[abc]` matches `a`, `b`, or `c`. `[a-z]` matches any lowercase letter. `[^abc]` is a negated class matching any character except `a`, `b`, `c`.

## Q8: What do `\d`, `\w`, and `\s` represent?
**A:** `\d` matches any digit (0-9). `\w` matches any word character (alphanumeric + underscore). `\s` matches any whitespace character (space, tab, newline, carriage return). Their uppercase versions (`\D`, `\W`, `\S`) are negated.

## Q9: What is a capturing group?
**A:** A capturing group, denoted by `()`, groups part of a pattern and captures the matched substring. It can be referenced by backreference (`\1`) or extracted from match results. Useful for extracting specific parts of a match.

## Q10: What is a non-capturing group?
**A:** A non-capturing group `(?:)` groups a pattern without saving the matched substring. It's used for applying quantifiers or alternation to a group without cluttering the match results with unnecessary captures.

## Q11: What is a lookahead?
**A:** A lookahead is a zero-width assertion that checks if a pattern follows the current position without consuming characters. Positive lookahead: `(?=...)`. Negative lookahead: `(?!...)`. For example, `\d(?=px)` matches a digit followed by "px".

## Q12: What is a lookbehind?
**A:** A lookbehind checks if a pattern precedes the current position. Positive lookbehind: `(?<=...)`. Negative lookbehind: `(?<!...)`. For example, `(?<=\$)\d+` matches digits preceded by a dollar sign. Not supported in all regex engines (e.g., JavaScript gained this in ES2018).

## Q13: What is the `i` flag in regex?
**A:** The `i` flag makes the pattern case-insensitive. `/hello/i` matches `"hello"`, `"Hello"`, `"HELLO"`, etc.

## Q14: What is the `g` flag?
**A:** The `g` (global) flag makes the regex find all matches rather than stopping after the first match. Used with `.match()`, `.replace()`, `.exec()`, and `.test()` to iterate through all occurrences.

## Q15: What is the `m` flag?
**A:** The `m` (multiline) flag changes `^` and `$` to match at the start/end of each line (after/before `\n`) rather than only at the start/end of the entire string.

## Q16: What is the `s` (dotAll) flag?
**A:** The `s` flag makes the `.` metacharacter match newline characters as well. Without `s`, `.` matches everything except newlines. Introduced in ES2018.

## Q17: What is the `u` flag?
**A:** The `u` (unicode) flag enables full Unicode matching. It treats the pattern and string as Unicode code points rather than UTF-16 code units, enabling `\p{...}` Unicode property escapes.

## Q18: What is the `y` flag?
**A:** The `y` (sticky) flag forces the match to start at the `lastIndex` position. Unlike `g`, it does not search ahead — if there's no match at `lastIndex`, it returns `null` without advancing.

## Q19: What is a backreference?
**A:** A backreference `\1`, `\2`, etc., refers to the text captured by a previous capturing group. For example, `(["'])\w+\1` matches a quote character, word characters, and the same quote character, ensuring matching pairs.

## Q20: What is alternation in regex?
**A:** Alternation, denoted by `|`, matches either the pattern on the left or the right. `cat|dog` matches `"cat"` or `"dog"`. Alternation has the lowest precedence, so `abc|def` matches `"abc"` or `"def"`.

## Q21: How would you match an email address with regex?
**A:** A basic email regex: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`. This matches the local part (alphanumerics, dots, underscores, etc.), the `@` symbol, the domain, and the TLD of at least 2 characters.

## Q22: How would you validate a phone number with regex?
**A:** For US numbers: `^\+?1?[-.\s]?\(?[2-9]\d{2}\)?[-.\s]?\d{3}[-.\s]?\d{4}$`. This handles formats like (555) 123-4567, 555-123-4567, and +1-555-123-4567.

## Q23: How do you match a URL with regex?
**A:** `^https?:\/\/([\w-]+\.)+[\w-]+(\/[\w\-._~:/?#[\]@!$&'()*+,;=]*)?$`. Matches HTTP/HTTPS URLs with optional path, query, and fragment.

## Q24: How would you extract all numbers from a string?
**A:** Use `/\d+/g` with `.match()`. For decimal numbers: `/-?\d+(\.\d+)?/g`. For scientific notation: `/-?\d+(\.\d+)?[eE][+-]?\d+/g`.

## Q25: How do you match a valid IPv4 address?
**A:** Use `^(\d{1,3}\.){3}\d{1,3}$` with additional validation for each octet (0-255). A stricter regex: `^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$`.

## Q26: How do you match a date in YYYY-MM-DD format?
**A:** `^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$`. This validates the format but not the actual calendar validity (e.g., February 30 passes).

## Q27: What is a word boundary `\b`?
**A:** `\b` asserts a position between a word character (`\w`) and a non-word character (`\W`). It matches the boundary itself without consuming characters. Useful for whole-word matching: `\bword\b`.

## Q28: What is the difference between `\b` and `\B`?
**A:** `\b` matches a word boundary. `\B` matches a non-word boundary (i.e., between two word characters or two non-word characters).

## Q29: How do you match whitespace or its absence?
**A:** Use `\s` for any whitespace, `\S` for any non-whitespace. For optional whitespace: `\s*` (zero or more). For required whitespace: `\s+` (one or more). For exactly one: `\s` or `[ \t]`.

## Q30: How do you match a tab character?
**A:** Use `\t` in the regex pattern. In many regex engines, you can also use `\x09` (hex) or `\u0009` (Unicode).

## Q31: How do you match a newline character?
**A:** Use `\n` for line feed, `\r` for carriage return, or `\r?\n` to handle both Windows and Unix line endings. The `s` flag makes `.` match newlines.

## Q32: What is a possessive quantifier?
**A:** A possessive quantifier (`*+`, `++`, `?+`, `{n,m}+`) matches as much as possible but never gives back (no backtracking). This improves performance but can cause matches to fail that would succeed with greedy quantifiers.

## Q33: How do you match nested parentheses?
**A:** Standard regex cannot match arbitrarily nested structures. Use recursive patterns in PCRE (`\((?:[^()]|(?R))*\)`) or use a parser. For limited nesting, you can write patterns for specific depths.

## Q34: How do you replace all occurrences of a pattern with a dynamic value?
**A:** In JavaScript, pass a function to `.replace()`: `str.replace(/(\d+)/g, (match, num) => parseInt(num) * 2)`. The function receives the match and capture groups.

## Q35: What is the `lastIndex` property?
**A:** `lastIndex` is a property of regex objects with the `g` or `y` flag. It indicates the position to start the next search. `.exec()` and `.test()` update it. Must be reset manually for fresh searches.

## Q36: How do you reset `lastIndex`?
**A:** Set `regex.lastIndex = 0`. This is important when reusing a global regex, otherwise subsequent calls start from where the last match ended.

## Q37: What is RegExp.prototype[Symbol.match]?
**A:** It's the method called by `String.prototype.match()`. Custom regex-like objects can implement this symbol to customize matching behavior. The `g` flag changes how this method operates.

## Q38: How do you use named capture groups?
**A:** Use `(?<name>pattern)` syntax. Named groups can be accessed by name in match results: `match.groups.name`. In replacements: `$<name>`. Supported in most modern regex engines (ES2018 for JavaScript).

## Q39: What is the `\k<name>` syntax?
**A:** Used in replacement strings or regex patterns to reference a named capture group. In patterns: `\k<name>` (ES2018). In replacement strings: `$<name>`.

## Q40: How do you match Unicode characters by category?
**A:** Use `\p{...}` with the `u` flag. Examples: `\p{L}` matches any letter, `\p{N}` any number, `\p{Sc}` any currency symbol, `\p{Emoji}` any emoji character.

## Q41: What is the difference between `\p{L}` and `\p{Letter}`?
**A:** They are equivalent. `\p{L}` is the short form, `\p{Letter}` is the long form. Both match any Unicode letter character including alphabets from all languages (Latin, Cyrillic, Arabic, Chinese, etc.).

## Q42: How do you match an emoji with regex?
**A:** Use `\p{Emoji}` with the `u` flag. For extended grapheme clusters (skin tones, sequences), use `\p{Extended_Pictographic}`. Complex emoji sequences may require multiple Unicode properties.

## Q43: How do you trim whitespace from both ends of a string using regex?
**A:** Use `str.replace(/^\s+|\s+$/g, '')`. The alternation matches leading whitespace (`^\s+`) OR trailing whitespace (`\s+$`), and replaces them with an empty string.

## Q44: How do you extract query parameters from a URL using regex?
**A:** Use `/[\?&]([^=]+)=([^&#]*)/g` and iterate over matches. Each match captures the parameter name and value. Decode URI components to get the actual strings.

## Q45: How do you validate a strong password with regex?
**A:** `^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$`. Uses lookaheads to require lowercase, uppercase, digit, special character, and minimum 8 characters.

## Q46: What is catastrophic backtracking?
**A:** A regex engine performance issue caused by nested quantifiers with overlapping possibilities (e.g., `(a+)+b` on input `"aaaaac"`). The engine tries an exponential number of combinations before failing. Can cause ReDoS (Regular Expression Denial of Service).

## Q47: How do you prevent catastrophic backtracking?
**A:** Use possessive quantifiers (`++`), atomic groups `(?>...)`, or rewrite the pattern to eliminate ambiguity. Replace `(a+)+b` with ` a++b` or use more specific patterns.

## Q48: What is an atomic group?
**A:** Atomic groups `(?>...)` prevent backtracking into the group. If the group matches, the engine will not try alternate paths within it if the overall pattern fails later. Supported in PCRE, Ruby, Java, not in JavaScript.

## Q49: How do you match a pattern that appears exactly `n` times?
**A:** Use `{n}` as a quantifier. `a{3}` matches exactly `"aaa"`. `{n,}` matches `n` or more. `{n,m}` matches between `n` and `m` times.

## Q50: How do you match a hexadecimal color code?
**A:** `^#?([a-fA-F0-9]{3}|[a-fA-F0-9]{6})$`. Matches optional `#`, then either 3 or 6 hex characters. For 8-digit hex with alpha: `^#?([a-fA-F0-9]{3,8})$`.

## Q51: How do you match a UUID?
**A:** `/^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i`. Specifically validates version (4th group starts with 1-5) and variant (5th group starts with 8, 9, a, or b).

## Q52: How do you match a JSON string?
**A:** Use `"(?:[^"\\]|\\.)*"`. Matches a double-quoted string, handling escaped characters like `\"`, `\\`, `\n`, `\t`. The `\\.` matches any backslash followed by any character.

## Q53: How do you match a social security number (SSN)?
**A:** `^(?!000|666|9\d{2})\d{3}-(?!00)\d{2}-(?!0000)\d{4}$`. Uses lookaheads to exclude invalid SSNs (000, 666, 900-999 area numbers, 00 group, 0000 serial).

## Q54: How do you match a credit card number?
**A:** `^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12}|(?:2131|1800|35\d{3})\d{11})$`. Covers Visa, MasterCard, Amex, Discover, JCB.

## Q55: How do you match a MAC address?
**A:** `^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$`. Matches 6 pairs of hex digits separated by colons or hyphens. For Cisco style: `^([0-9A-Fa-f]{4}\.){2}[0-9A-Fa-f]{4}$`.

## Q56: How does regex work in Python?
**A:** Python uses the `re` module. `re.match()` checks from the start of the string, `re.search()` finds anywhere, `re.findall()` returns all matches, `re.sub()` replaces, and `re.split()` splits on matches. Patterns use raw strings (`r"pattern"`).

## Q57: What is the difference between `re.match()` and `re.search()` in Python?
**A:** `re.match()` only checks at the beginning of the string (implicit `^`). `re.search()` scans the entire string for a match anywhere. For identical results, use `re.search()` with `^` or `re.fullmatch()`.

## Q58: How do you compile a regex in Python?
**A:** Use `re.compile(r'pattern', flags)` to create a compiled regex object. Benefits: reuse the compiled pattern for better performance and access to pattern attributes like `.pattern` and `.groups`.

## Q59: What is `re.VERBOSE` (or `re.X`) in Python?
**A:** The `re.VERBOSE` flag allows writing regex with whitespace and comments for readability. Spaces are ignored (use `\s` or `[ ]` to match literal spaces). Comments start with `#`.

## Q60: How do you use regex in JavaScript?
**A:** Two ways: regex literal `/pattern/flags` or `new RegExp('pattern', 'flags')`. Literals are compiled at parse time (better for static patterns). `RegExp` constructor is for dynamic patterns from variables.

## Q61: How do you escape a metacharacter in regex?
**A:** Prefix it with a backslash `\`. Common metacharacters: `. ^ $ * + ? { } [ ] \ | ( )`. To match a literal dot: `\.`. To match a literal backslash: `\\`.

## Q62: How do you match an empty string?
**A:** Use `^$` to match an empty string (start immediately followed by end). Use `^[\s\S]*$` to match empty or whitespace-only strings. Use `\z` (Ruby) or `\Z` (Python) for absolute end.

## Q63: What are inline flags?
**A:** Flags can be set inline within the pattern: `(?i)` for case-insensitive, `(?m)` for multiline, `(?s)` for dotAll, `(?x)` for verbose. Can be negated: `(?-i)`. Apply to the rest of the pattern or scoped: `(?i:pattern)`.

## Q64: How do you match a pattern that does NOT contain a specific substring?
**A:** Use a negative lookahead: `^(?!.*substring).*$`. This asserts the string does not contain "substring". More efficient: `^(?:(?!substring).)*$`.

## Q65: How do you split a string by commas but ignore commas inside quotes?
**A:** Use `/(?:,)(?=(?:[^"]*"[^"]*")*[^"]*$)/` to split on commas that are outside quotes. Better approach: match the fields directly: `/(?:[^,"]+|"[^"]*")+/g`.

## Q66: How do you extract the domain from a URL using regex?
**A:** Use `https?:\/\/([^\/\s]+)` and capture group 1. For subdomain extraction: `https?:\/\/(?:[^\/\s]+\.)?([^\/.\s]+\.[^\/.\s]+)`.

## Q67: How do you match a Slack channel name?
**A:** `^[a-z0-9][a-z0-9-]{1,79}$`. Slack channel names must start with a letter or number, contain only lowercase letters, numbers, and hyphens, and be 1-80 characters.

## Q68: How do you match a YouTube video ID?
**A:** `^([a-zA-Z0-9_-]{11})$`. YouTube video IDs are exactly 11 characters from `[a-zA-Z0-9_-]`. Watch for false positives since the format is simple.

## Q69: How do you convert a string to camelCase using regex?
**A:** `str.replace(/[-_\s]+(.)/g, (_, c) => c.toUpperCase())`. Matches separators (hyphen, underscore, whitespace) followed by a character, and replaces with the uppercased character.

## Q70: How do you convert camelCase to snake_case?
**A:** `str.replace(/([A-Z])/g, '_$1').toLowerCase()`. Inserts an underscore before each uppercase letter and lowercases the entire string. Handle the leading underscore: `.replace(/^_/, '')`.

## Q71: How do you match a Twitter/X handle?
**A:** `^@?(\w{1,15})$`. Twitter handles are 1-15 characters, contain word characters, and optionally start with `@`.

## Q72: How do you match an HTML tag?
**A:** `<([a-z]+)([^>]*)>(.*?)<\/\1>` matches opening tag, attributes, content, and closing tag with matching tag name. Use `<[^>]+>` for simpler tag matching (doesn't validate pairing).

## Q73: How do you remove HTML tags from a string?
**A:** `str.replace(/<[^>]*>/g, '')`. This removes all HTML tags. For safe HTML sanitization, use a proper parser instead of regex.

## Q74: How do you match a Markdown link?
**A:** `\[([^\]]+)\]\(([^)]+)\)`. Captures the link text in group 1 and the URL in group 2. For links with titles: `\[([^\]]+)\]\(([^)]+)(?:\s+"[^"]*")?\)`.

## Q75: How do you match a Markdown image?
**A:** `!\[([^\]]*)\]\(([^)]+)\)`. Same as links but with a leading `!`. Captures alt text and image URL.

## Q76: How do you extract code blocks from Markdown?
**A:** Use ``` ```(\w+)?\n([\s\S]*?)``` ```. Captures optional language identifier and the code content (including newlines). Use `[\s\S]` to match everything including newlines.

## Q77: What is the regex equivalent of startsWith()?
**A:** `/^pattern/.test(str)`. The `^` anchor forces the match to start at the beginning of the string.

## Q78: What is the regex equivalent of endsWith()?
**A:** `/pattern$/.test(str)`. The `$` anchor forces the match to end at the end of the string.

## Q79: What is the regex equivalent of includes()?
**A:** `/pattern/.test(str)`. Without anchors, the regex searches anywhere in the string.

## Q80: How do you match a pattern that appears in a specific order?
**A:** Use `pattern1.*pattern2`. The `.*` matches any characters between the two patterns. For non-overlapping: `pattern1[\s\S]*?pattern2` (lazy) or `pattern1[\s\S]*pattern2` (greedy).

## Q81: How do you match a valid username?
**A:** `^[a-zA-Z][a-zA-Z0-9_]{2,15}$`. Must start with a letter, contain only alphanumeric + underscore, 3-16 characters total.

## Q82: How do you match a GitHub repository name?
**A:** `^[a-zA-Z0-9_.-]{1,100}$`. GitHub allows alphanumeric, hyphens, underscores, and periods. No consecutive dots, and cannot start/end with a dot (requires additional validation).

## Q83: How do you match a Base64 string?
**A:** `^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$`. Matches valid Base64 with optional padding (`=` or `==`).

## Q84: How do you validate a JWT token?
**A:** `/^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$/`. A JWT has three Base64url-encoded parts separated by dots. This validates the format, not the cryptographic signature.

## Q85: How do you match a version number (semver)?
**A:** `^(\d+)\.(\d+)\.(\d+)(-[\w.]+)?(\+[\w.]+)?$`. Captures major, minor, patch, pre-release, and build metadata per the semver specification.

## Q86: How do you match a file extension?
**A:** `\.(\w+)$` captures the extension at the end of a filename. For specific extensions: `\.(jpg|png|gif|svg)$` with case-insensitive flag.

## Q87: How do you match a path like `/foo/bar/baz`?
**A:** `^(\/[a-zA-Z0-9_\-]+)+$` or for generic paths: `^(\/[^\/\s]+)*\/?$`. The `[^\/\s]` matches any character that's not a slash or whitespace.

## Q88: How do you match a single character that is not a specific character?
**A:** Use `[^char]`. For example, `[^a]` matches any character except `a`. Use `[^abc]` to exclude multiple characters. Use `[^a-z]` to exclude a range.

## Q89: How do you count the number of occurrences of a pattern?
**A:** Use `(str.match(/pattern/g) || []).length` in JavaScript, or `len(re.findall(r'pattern', str))` in Python.

## Q90: How do you match a repeated word (e.g., "the the")?
**A:** `\b(\w+)\s+\1\b`. Uses a capturing group and backreference to match the same word appearing twice in a row.

## Q91: How do you match a palindrome with regex?
**A:** Pure regex cannot match arbitrary-length palindromes (not a regular language). For specific lengths: `^([a-z])([a-z])([a-z])\3\2\1$` for 6-letter palindromes. Use a programming language for general case.

## Q92: How do you use regex in SQL?
**A:** PostgreSQL: `~` operator or `SIMILAR TO`. MySQL: `REGEXP` or `RLIKE`. Oracle: `REGEXP_LIKE()`. SQLite: requires extension. Syntax varies significantly between databases.

## Q93: How do you use regex in grep?
**A:** `grep 'pattern' file` uses basic regex by default. `grep -E 'pattern'` for extended regex (ERE). `grep -P 'pattern'` for Perl-compatible regex (PCRE) if supported. `-i` for case-insensitive, `-r` for recursive.

## Q94: What is the difference between basic and extended regex in grep?
**A:** Basic regex (BRE) requires escaping metacharacters: `\(` for groups, `\{` for quantifiers, `\+` for one or more. Extended regex (ERE) treats them as metacharacters without escaping. Use `-E` for ERE.

## Q95: How do you use regex in sed?
**A:** `sed 's/pattern/replacement/flags' file`. Supports BRE by default; `-E` for ERE. Use `'s/old/new/g'` for global replacement, `'s/old/new/p'` to print, and `-n` to suppress automatic printing.

## Q96: How do you use regex in awk?
**A:** `awk '/pattern/ { action }' file`. Patterns are ERE. Use `~` for matching against specific fields: `awk '$3 ~ /pattern/' file`. Use `!~` for negation.

## Q97: How do you debug a regex?
**A:** Use online tools like regex101.com, RegExr, or debuggex. These provide real-time match highlighting, explanation of the pattern, and step-through debugging to identify issues.

## Q98: What is the difference between `re.findall()` and `re.finditer()` in Python?
**A:** `re.findall()` returns a list of all matches (strings or tuples of groups). `re.finditer()` returns an iterator of match objects, which is more memory-efficient for large texts and provides match positions.

## Q99: How do you validate a complex password policy using regex?
**A:** Combine lookaheads: `^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?])(?=.{8,})(?!.*(.)\1{2,})(?!.*(?:password|12345|qwerty)).*$`. Checks for character diversity, minimum length, no repeated characters, and no common patterns.

## Q100: What are the theoretical limitations of regular expressions?
**A:** Regular expressions can only match regular languages (Type 3 in Chomsky hierarchy). They cannot handle arbitrarily nested structures (HTML, JSON, balanced parentheses), palindromes of arbitrary length, or counting beyond constant values. These require context-free or more powerful parsers.
