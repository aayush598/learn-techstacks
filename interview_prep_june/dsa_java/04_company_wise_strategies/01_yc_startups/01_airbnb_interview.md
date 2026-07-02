# Airbnb Interview Pattern

## Table of Contents
1. Interview Format
2. Most Asked Topics
3. Airbnb Culture
4. Types of Problems
5. Example Problems
6. Preparation Strategy

---

## 1. Interview Format

### Recruiter Screen (30 min)
- Background and experience discussion
- Role expectations

### Technical Screen (45-60 min)
- 1-2 coding problems on shared editor
- Usually medium difficulty

### On-site (5-6 rounds, 45-60 min each)
- **Coding** (2 rounds): Algorithm problems
- **System Design** (1): For senior roles
- **Product Sense / Architecture** (1): Mix of algorithms and product design
- **Experience / Behavioral** (1): Past projects, culture fit
- **Cross-functional** (1): Pair with an engineer from another team

### Key Differences
- Product sense is VERY important — Airbnb wants engineers who think about users
- Questions often relate to search, calendar, booking, matching
- They value design thinking and user empathy
- Whiteboard or digital whiteboard for coding

---

## 2. Most Asked Topics

| Topic | Frequency | Why Airbnb Asks It |
|-------|-----------|-------------------|
| Arrays & Strings | Very High | Search, listing data |
| HashMaps | Very High | User data, matching |
| Trees | High | Category hierarchies, location |
| Sorting / Ordering | High | Search results, ranking |
| Graph | Medium | Location proximity, recommendations |
| Pagination | Medium | Search results display |
| DP | Medium | Pricing optimization |
| System Design | Medium | Scalable booking, payments |

### Topic Frequency Graph
```
Arrays:  ████████████████████
Hash:    ████████████████████
Trees:   ██████████████
Sorting: ██████████████
Graphs:  ████████
Pagin.:  ████████
DP:      ██████
Design:  ██████
```

---

## 3. Airbnb Culture

### Core Values
- **Be a Host** — Hospitality mindset, treat everyone with respect
- **Embrace the Adventure** — Take risks, be curious
- **Every Frame Matters** — Attention to detail, quality
- **Simplify** — Elegant solutions to complex problems
- **Champion the Mission** — Belong anywhere

### How Culture Affects Interviews
- Interviewers look for user-centric thinking
- "How would this feature improve the guest experience?"
- They value design sense and product intuition
- Code should be clean, elegant, and maintainable

---

## 4. Types of Problems

### Search Problems
- Search pagination with filtering
- Search results ranking by relevance/proximity
- Autocomplete for location search
- Filter by price range, dates, amenities

### Calendar / Scheduling
- Check date availability
- Minimum booking window
- Price calculation (weekday/weekend, seasonal)
- Cleaning schedule optimization

### Matching Problems
- Match guests to hosts based on preferences
- Recommend similar listings
- Detect duplicate listings
- Fraud detection in booking patterns

### String/Text Problems
- Parse search queries
- Text similarity for reviews
- Language detection
- Address/location parsing

---

## 5. Example Problems

### Problem 1: Search Pagination
**Problem:** Given a list of search results, paginate them ensuring no host appears twice on the same page.

**Approach:** Distribute results by host ID across pages.
```java
public List<List<String>> paginate(int resultsPerPage, List<String> results) {
    List<List<String>> pages = new ArrayList<>();
    // Track which hosts have been placed on current page
    Set<String> hostsOnPage = new HashSet<>();
    List<String> page = new ArrayList<>();
    List<String> remaining = new ArrayList<>(results);
    while (!remaining.isEmpty()) {
        hostsOnPage.clear();
        page.clear();
        // First pass: place results with unique hosts
        Iterator<String> it = remaining.iterator();
        while (it.hasNext() && page.size() < resultsPerPage) {
            String result = it.next();
            String hostId = extractHostId(result);
            if (!hostsOnPage.contains(hostId)) {
                hostsOnPage.add(hostId);
                page.add(result);
                it.remove();
            }
        }
        // Second pass: fill remaining slots
        it = remaining.iterator();
        while (it.hasNext() && page.size() < resultsPerPage) {
            page.add(it.next());
            it.remove();
        }
        pages.add(new ArrayList<>(page));
    }
    return pages;
}
```

### Problem 2: Find All Collinear Points
**Problem:** Given a set of points, find all lines with at least k points.

**Approach:** HashMap of slopes for each point as origin.
```java
public List<List<int[]>> findLines(int[][] points, int k) {
    List<List<int[]>> result = new ArrayList<>();
    for (int i = 0; i < points.length; i++) {
        Map<String, List<int[]>> slopeMap = new HashMap<>();
        for (int j = i + 1; j < points.length; j++) {
            int dx = points[j][0] - points[i][0];
            int dy = points[j][1] - points[i][1];
            int g = gcd(dx, dy);
            String slope = (dx/g) + "/" + (dy/g); // normalized slope
            slopeMap.computeIfAbsent(slope, x -> new ArrayList<>()).add(points[j]);
        }
        for (List<int[]> line : slopeMap.values()) {
            if (line.size() + 1 >= k) {
                line.add(points[i]);
                result.add(line);
            }
        }
    }
    return result;
}
```

### Problem 3: Minimum Window Substring (Airbnb variant)
**Problem:** Given reviews and a set of keywords, find shortest review snippet containing all keywords.

**Approach:** Sliding window (same as min window substring).
```java
public String minSnippet(String review, Set<String> keywords) {
    String[] words = review.split(" ");
    Map<String, Integer> freq = new HashMap<>();
    int required = keywords.size(), matched = 0;
    int left = 0, minLen = Integer.MAX_VALUE, start = 0;
    for (int right = 0; right < words.length; right++) {
        String word = words[right].toLowerCase().replaceAll("[^a-z]", "");
        if (keywords.contains(word)) {
            freq.put(word, freq.getOrDefault(word, 0) + 1);
            if (freq.get(word) == 1) matched++;
        }
        while (matched == required) {
            if (right - left + 1 < minLen) {
                minLen = right - left + 1;
                start = left;
            }
            String leftWord = words[left].toLowerCase().replaceAll("[^a-z]", "");
            if (keywords.contains(leftWord)) {
                freq.put(leftWord, freq.get(leftWord) - 1);
                if (freq.get(leftWord) == 0) matched--;
            }
            left++;
        }
    }
    // Build result string
    StringBuilder sb = new StringBuilder();
    for (int i = start; i < start + minLen; i++) {
        sb.append(words[i]).append(" ");
    }
    return sb.toString().trim();
}
```

---

## 6. Preparation Strategy

### Focus Areas

1. **Arrays, Strings, HashMaps (50%)**
   - Search pagination problems
   - Frequency-based algorithms
   - Sorting and ordering
   - Sliding window on strings

2. **Trees and Graphs (25%)**
   - Location hierarchy
   - Recommendation systems
   - Shortest path for proximity

3. **System Design (15%)**
   - Search system design
   - Calendar/availability system
   - Review system

4. **Behavioral / Product Sense (10%)**
   - Know Airbnb's products deeply
   - Think about user experience
   - Practice "design a feature" questions

### Airbnb-Specific Tips
1. **Show product empathy** — "How would a host/guest use this?"
2. **Clean code** — Airbnb values simplicity and elegance
3. **Think about real-world data** — Not all listings are perfect
4. **Be collaborative** — They value teamwork and "being a host"
5. **Know Airbnb's features** — Understand search, booking, reviews, calendar
6. **Design for scale** — How would this work for millions of listings?
