# Convex Hull Trick (CHT)

Used when: dp[i] = min/max(dp[j] + b[j] * a[i]) for j < i, where a[i] is monotonic.

This is optimization for DP where the transition uses linear functions.

## When to Use

```java
// DP of the form:
dp[i] = min(dp[j] + (x[i] - x[j])^2)  // slope = -2*x[j], intercept = dp[j] + x[j]^2
dp[i] = min(dp[j] + b[j] * a[i])      // general form
```

## Simple Implementation (for monotonic queries)

```java
// For minimization with lines of form y = m*x + b
// where queries (x) are increasing

static class Line {
    long m, b; // y = m*x + b
    Line(long m, long b) { this.m = m; this.b = b; }

    double intersect(Line other) {
        return (double)(other.b - b) / (m - other.m);
    }
}

static class ConvexHullTrick {
    Deque<Line> dq = new ArrayDeque<>();

    void addLine(long m, long b) {
        Line newLine = new Line(m, b);
        while (dq.size() >= 2) {
            Line l1 = dq.pollLast();
            Line l2 = dq.peekLast();
            if (l2.intersect(newLine) < l2.intersect(l1)) {
                dq.addLast(l1);
                break;
            }
        }
        dq.addLast(newLine);
    }

    long query(long x) {
        while (dq.size() >= 2 && dq.peekFirst().m * x + dq.peekFirst().b
                                >= dq.peekLast().m * x + dq.peekLast().b) {
            dq.pollFirst();
        }
        return dq.peekFirst().m * x + dq.peekFirst().b;
    }
}
```

## Key Insight

> CHT optimizes O(n²) to O(n) or O(n log n) when the transition is choosing the best linear function evaluated at a point. Requires lines to have monotonic slopes and queries to be monotonic (or use Li Chao tree for arbitrary).
