# Social Media and Friendship Graph SQL Scenarios — 100 Interview Q&A

> **Schema used throughout**
>
> ```sql
> CREATE TABLE users       (user_id INT PRIMARY KEY, name VARCHAR(100), joined_at DATE);
> CREATE TABLE friendships  (user1_id INT, user2_id INT, created_at DATE);
> CREATE TABLE follows       (follower_id INT, followee_id INT, created_at DATE);
> CREATE TABLE posts         (post_id INT PRIMARY KEY, user_id INT, content TEXT, created_at TIMESTAMP);
> CREATE TABLE likes         (post_id INT, user_id INT, created_at TIMESTAMP);
> CREATE TABLE comments      (comment_id INT PRIMARY KEY, post_id INT, user_id INT, parent_comment_id INT, content TEXT, created_at TIMESTAMP);
> CREATE TABLE messages      (message_id INT PRIMARY KEY, sender_id INT, receiver_id INT, content TEXT, sent_at TIMESTAMP);
> CREATE TABLE interests     (user_id INT, interest VARCHAR(100));
> CREATE TABLE mutes         (muter_id INT, muted_id INT);
> ```

---

## Q1: Count the number of friends each user has

**Query:**
```sql
SELECT u.user_id,
       u.name,
       COUNT(*) AS friend_count
FROM   users u
JOIN   friendships f
  ON  u.user_id = f.user1_id
  OR  u.user_id = f.user2_id
GROUP  BY u.user_id, u.name
ORDER  BY friend_count DESC;
```
**Explanation:** An `OR` join covers both columns since friendships can appear as `(user1, user2)` or `(user2, user1)`.

**Alt1:**
```sql
-- PostgreSQL: unnest both sides for a clean union
SELECT u.user_id,
       u.name,
       COUNT(*) AS friend_count
FROM   users u
JOIN  (SELECT user1_id AS uid FROM friendships
       UNION ALL
       SELECT user2_id FROM friendships) pf
  ON  u.user_id = pf.uid
GROUP  BY u.user_id, u.name
ORDER  BY friend_count DESC;
```
**Explanation:** `UNION ALL` on both columns gives one row per friendship direction, then we count per user.

---

## Q2: Top 10 users by friend count

**Query:**
```sql
SELECT u.user_id,
       u.name,
       COUNT(*) AS friend_count
FROM   users u
JOIN   friendships f
  ON  u.user_id = f.user1_id
  OR  u.user_id = f.user2_id
GROUP  BY u.user_id, u.name
ORDER  BY friend_count DESC
LIMIT  10;
```
**Explanation:** Same structure as Q1 but `LIMIT 10` retains only the top 10.

---

## Q3: Find users with no friends (isolates)

**Query:**
```sql
SELECT u.user_id, u.name
FROM   users u
LEFT JOIN friendships f
  ON  u.user_id = f.user1_id
  OR  u.user_id = f.user2_id
WHERE  f.user1_id IS NULL;
```
**Explanation:** A left join that finds zero matching rows identifies users with no friendship records at all.

---

## Q4: Average number of friends per user

**Query:**
```sql
SELECT AVG(friend_count) AS avg_friends
FROM  (SELECT u.user_id,
              COUNT(*) AS friend_count
       FROM   users u
       JOIN   friendships f
         ON  u.user_id = f.user1_id
         OR  u.user_id = f.user2_id
       GROUP  BY u.user_id) sub;
```
**Explanation:** A subquery computes each user's count; the outer query averages across all users who have at least one friend.

---

## Q5: Total deduplicated friendship edges

**Query:**
```sql
SELECT COUNT(DISTINCT
       CASE WHEN user1_id < user2_id
            THEN CONCAT(user1_id, '-', user2_id)
            ELSE CONCAT(user2_id, '-', user1_id)
       END) AS unique_edges
FROM   friendships;
```
**Explanation:** Canonical ordering via `CASE` ensures `(1,2)` and `(2,1)` collapse into the same key for `COUNT(DISTINCT)`.

---

## Q6: Mutual friends between two specific users (A=123, B=456)

**Query:**
```sql
SELECT f1.user2_id AS mutual_friend
FROM   friendships f1
JOIN   friendships f2
  ON  f1.user2_id = f2.user2_id
WHERE  f1.user1_id = 123
  AND  f2.user1_id = 456;
```
**Explanation:** An equi-join on `user2_id` finds every person who appears as a friend of both A and B.

**Alt1:**
```sql
-- PostgreSQL: use INTERSECT for clarity
SELECT user2_id AS mutual_friend FROM friendships WHERE user1_id = 123
INTERSECT
SELECT user2_id FROM friendships WHERE user1_id = 456;
```
**Explanation:** `INTERSECT` naturally returns the set of users present in both friend lists.

---

## Q7: All user pairs sharing at least N mutual friends

**Query:**
```sql
SELECT LEAST(f1.user1_id, f2.user1_id)   AS user_a,
       GREATEST(f1.user1_id, f2.user1_id) AS user_b,
       COUNT(DISTINCT f1.user2_id)        AS mutual_count
FROM   friendships f1
JOIN   friendships f2
  ON  f1.user2_id = f2.user2_id
WHERE  f1.user1_id < f2.user1_id
GROUP  BY user_a, user_b
HAVING COUNT(DISTINCT f1.user2_id) >= 5
ORDER  BY mutual_count DESC;
```
**Explanation:** `LEAST`/`GREATEST` canonicalizes the pair; `HAVING` filters pairs below the threshold. Replace `5` with any N.

---

## Q8: Friend count distribution histogram

**Query:**
```sql
SELECT bucket,
       COUNT(*) AS user_count
FROM  (SELECT CASE
              WHEN cnt BETWEEN  1 AND  5 THEN '1-5'
              WHEN cnt BETWEEN  6 AND 10 THEN '6-10'
              WHEN cnt BETWEEN 11 AND 20 THEN '11-20'
              ELSE '20+'
           END AS bucket
       FROM  (SELECT user1_id AS uid, COUNT(*) AS cnt FROM friendships GROUP BY user1_id
              UNION ALL
              SELECT user2_id, COUNT(*) FROM friendships GROUP BY user2_id) raw
       ) b
GROUP  BY bucket
ORDER  BY MIN(cnt);
```
**Explanation:** `UNION ALL` sums friend counts per user, then a `CASE` expression buckets them into a histogram.

**Alt1:**
```sql
-- PostgreSQL: use width_bucket for numeric histogram
SELECT width_bucket(cnt, 0, 100, 4) AS bucket,
       COUNT(*) AS user_count
FROM  (SELECT user1_id AS uid, COUNT(*) AS cnt FROM friendships GROUP BY user1_id
       UNION ALL
       SELECT user2_id, COUNT(*) FROM friendships GROUP BY user2_id) raw
GROUP  BY bucket
ORDER  BY bucket;
```
**Explanation:** `width_bucket` creates equal-width numeric ranges automatically.

---

## Q9: Users with above-average friend count

**Query:**
```sql
WITH fc AS (
  SELECT user1_id AS uid, COUNT(*) AS cnt FROM friendships GROUP BY user1_id
  UNION ALL
  SELECT user2_id, COUNT(*) FROM friendships GROUP BY user2_id
),
avg_fc AS (
  SELECT AVG(cnt) AS avg_cnt FROM fc
)
SELECT u.user_id, u.name, fc.cnt AS friend_count
FROM   users u
JOIN   fc     ON u.user_id = fc.uid
CROSS JOIN avg_fc
WHERE  fc.cnt > avg_fc.avg_cnt
ORDER  BY fc.cnt DESC;
```
**Explanation:** CTEs compute per-user counts and the global average; the outer query filters users above that average.

---

## Q10: Most popular user (highest friend count, tie-safe)

**Query:**
```sql
WITH fc AS (
  SELECT user1_id AS uid, COUNT(*) AS cnt FROM friendships GROUP BY user1_id
  UNION ALL
  SELECT user2_id, COUNT(*) FROM friendships GROUP BY user2_id
)
SELECT u.user_id, u.name, fc.cnt
FROM   users u
JOIN   fc ON u.user_id = fc.uid
WHERE  fc.cnt = (SELECT MAX(cnt) FROM fc);
```
**Explanation:** `WHERE cnt = (SELECT MAX(...))` returns all users tied at the highest count.

---

## Q11: Friend count for users who joined in the last 30 days

**Query:**
```sql
SELECT u.user_id, u.name, u.joined_at,
       COUNT(f.user2_id) AS friend_count
FROM   users u
LEFT JOIN friendships f
  ON  u.user_id = f.user1_id
  OR  u.user_id = f.user2_id
WHERE  u.joined_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP  BY u.user_id, u.name, u.joined_at;
```
**Explanation:** `LEFT JOIN` ensures new users with zero friends still appear with count 0.

---

## Q12: Monthly friendship creation trend

**Query:**
```sql
-- MySQL 8+
SELECT DATE_FORMAT(created_at, '%Y-%m') AS month,
       COUNT(*) AS new_friendships
FROM   friendships
GROUP  BY month
ORDER  BY month;
```
**Explanation:** `DATE_FORMAT` truncates to month; `COUNT(*)` gives the volume per bucket.

---

## Q13: Users with exactly one friend (leaf nodes)

**Query:**
```sql
WITH fc AS (
  SELECT user1_id AS uid, COUNT(*) AS cnt FROM friendships GROUP BY user1_id
  UNION ALL
  SELECT user2_id, COUNT(*) FROM friendships GROUP BY user2_id
)
SELECT u.user_id, u.name
FROM   users u
JOIN   fc ON u.user_id = fc.uid
WHERE  fc.cnt = 1;
```
**Explanation:** Leaf/pendant nodes have degree exactly one.

---

## Q14: Second-degree connections count per user

**Query:**
```sql
-- MySQL 8+
WITH RECURSIVE friends AS (
  SELECT user1_id AS uid, user2_id AS fid, 1 AS depth
  FROM   friendships
  UNION ALL
  SELECT user1_id, f2.user2_id, f.depth + 1
  FROM   friendships f2
  JOIN   friends f ON f.fid = f2.user1_id
  WHERE  f.depth = 1
)
SELECT uid, COUNT(DISTINCT fid) AS second_degree_count
FROM   friends
WHERE  depth = 2
GROUP  BY uid;
```
**Explanation:** A single recursion step reaches friends-of-friends, then we count distinct 2-hop neighbors.

---

## Q15: Degree centrality per user

**Query:**
```sql
WITH fc AS (
  SELECT user1_id AS uid, COUNT(*) AS cnt FROM friendships GROUP BY user1_id
  UNION ALL
  SELECT user2_id, COUNT(*) FROM friendships GROUP BY user2_id
),
total AS (SELECT COUNT(*) AS n FROM users)
SELECT u.user_id,
       u.name,
       COALESCE(fc.cnt, 0) AS degree,
       ROUND(COALESCE(fc.cnt, 0) * 1.0 / (t.n - 1), 4) AS centrality
FROM   users u
CROSS JOIN total t
LEFT JOIN fc ON u.user_id = fc.uid
ORDER  BY centrality DESC;
```
**Explanation:** Degree centrality = degree / (n − 1) where n is the total user count.

---

## Q16: Users whose all friends joined in the same month

**Query:**
```sql
-- PostgreSQL
WITH user_friends AS (
  SELECT f.user1_id AS uid,
         EXTRACT(MONTH FROM f2.joined_at)  AS f_month,
         EXTRACT(YEAR  FROM f2.joined_at)  AS f_year
  FROM   friendships f
  JOIN   users f2 ON f.user2_id = f2.user_id
)
SELECT uid
FROM   user_friends
GROUP  BY uid
HAVING COUNT(DISTINCT f_year || '-' || f_month) = 1;
```
**Explanation:** If the distinct year-month of all friends' join dates is exactly one, every friend joined in the same month.

---

## Q17: Top influencers by follower count (follows table)

**Query:**
```sql
SELECT followee_id,
       COUNT(*) AS follower_count
FROM   follows
GROUP  BY followee_id
ORDER  BY follower_count DESC
LIMIT  10;
```
**Explanation:** `GROUP BY followee_id` and `COUNT(*)` give the follower count; `LIMIT 10` gives the top 10.

**Alt1:**
```sql
-- SQL Server: use TOP
SELECT TOP 10 followee_id,
       COUNT(*) AS follower_count
FROM   follows
GROUP  BY followee_id
ORDER  BY follower_count DESC;
```
**Explanation:** `TOP 10` replaces `LIMIT` in SQL Server.

---

## Q18: Mutual follows (A follows B AND B follows A)

**Query:**
```sql
SELECT f1.follower_id AS user_a,
       f1.followee_id AS user_b
FROM   follows f1
JOIN   follows f2
  ON  f1.follower_id = f2.followee_id
 AND  f1.followee_id = f2.follower_id
WHERE  f1.follower_id < f1.followee_id;
```
**Explanation:** Joining `follows` to itself with swapped IDs finds pairs where each follows the other; `<` avoids duplicates.

---

## Q19: Follow-back ratio per user

**Query:**
```sql
SELECT f.follower_id,
       f.followee_id,
       CASE WHEN EXISTS (
              SELECT 1 FROM follows f2
              WHERE f2.follower_id = f.followee_id
                AND f2.followee_id = f.follower_id
            ) THEN 1 ELSE 0 END AS followed_back
FROM   follows f;
```
**Explanation:** `EXISTS` checks the reverse edge to determine if the follow was reciprocated.

**Alt1:**
```sql
-- PostgreSQL: batch calculation of follow-back percentage per user
WITH ratios AS (
  SELECT f.follower_id,
         f.followee_id,
         CASE WHEN f2.follower_id IS NOT NULL THEN 1 ELSE 0 END AS followed_back
  FROM   follows f
  LEFT JOIN follows f2
    ON  f2.follower_id = f.followee_id
   AND  f2.followee_id = f.follower_id
)
SELECT follower_id,
       ROUND(AVG(followed_back) * 100, 2) AS follow_back_pct
FROM   ratios
GROUP  BY follower_id
ORDER  BY follow_back_pct DESC;
```
**Explanation:** `AVG` of the binary 0/1 column gives the percentage of outgoing follows that got followed back.

---

## Q20: Asymmetric follows only (A follows B but B does NOT follow back)

**Query:**
```sql
SELECT f.follower_id, f.followee_id
FROM   follows f
LEFT JOIN follows f2
  ON  f2.follower_id = f.followee_id
 AND  f2.followee_id = f.follower_id
WHERE  f2.follower_id IS NULL;
```
**Explanation:** `LEFT JOIN … IS NULL` is the classic anti-join pattern to find missing reverse edges.

---

## Q21: Follower-to-following ratio

**Query:**
```sql
WITH counts AS (
  SELECT user_id,
         SUM(CASE WHEN role = 'follower' THEN 1 ELSE 0 END) AS followers,
         SUM(CASE WHEN role = 'followee' THEN 1 ELSE 0 END) AS following
  FROM  (SELECT follower_id AS user_id, 'follower' AS role FROM follows
         UNION ALL
         SELECT followee_id, 'followee' FROM follows) p
  GROUP  BY user_id
)
SELECT u.user_id, u.name,
       COALESCE(c.followers, 0)  AS followers,
       COALESCE(c.following, 0)  AS following,
       CASE WHEN COALESCE(c.following, 0) = 0 THEN NULL
            ELSE ROUND(c.followers * 1.0 / c.following, 2)
       END AS ratio
FROM   users u
LEFT JOIN counts c ON u.user_id = c.user_id
ORDER  BY ratio DESC;
```
**Explanation:** A pivoted CTE counts both follower and followee appearances per user, then computes the ratio.

---

## Q22: Users with high following but low follower count

**Query:**
```sql
WITH counts AS (
  SELECT user_id,
         SUM(CASE WHEN role = 'f' THEN 1 ELSE 0 END) AS following,
         SUM(CASE WHEN role = 'b' THEN 1 ELSE 0 END) AS followers
  FROM  (SELECT follower_id AS user_id, 'f' AS role FROM follows
         UNION ALL
         SELECT followee_id, 'b' FROM follows) x
  GROUP  BY user_id
)
SELECT u.user_id, u.name, c.following, c.followers
FROM   users u
JOIN   counts c ON u.user_id = c.user_id
WHERE  c.following > 500
  AND  c.followers < 50;
```
**Explanation:** Thresholds identify potentially spammy accounts that follow many but are followed by few.

**Alt1:**
```sql
-- MySQL 8+: rank by ratio
WITH counts AS (
  SELECT follower_id AS uid,
         COUNT(*) AS following
  FROM   follows GROUP BY follower_id
),
recv AS (
  SELECT followee_id AS uid,
         COUNT(*) AS followers
  FROM   follows GROUP BY followee_id
)
SELECT u.user_id, u.name,
       COALESCE(c.following,0) AS following,
       COALESCE(r.followers,0) AS followers,
       ROUND(COALESCE(r.followers,0) / NULLIF(COALESCE(c.following,0),0), 2) AS fb_ratio
FROM   users u
LEFT JOIN counts c ON u.user_id = c.uid
LEFT JOIN recv   r ON u.user_id = r.uid
ORDER  BY fb_ratio ASC
LIMIT  20;
```
**Explanation:** Lowest ratios highlight accounts where few reciprocate; `NULLIF` prevents division by zero.

---

## Q23: Net follower gain per user

**Query:**
```sql
WITH counts AS (
  SELECT user_id,
         SUM(CASE WHEN role = 'f' THEN 1 ELSE 0 END) AS following,
         SUM(CASE WHEN role = 'b' THEN 1 ELSE 0 END) AS followers
  FROM  (SELECT follower_id AS user_id, 'f' AS role FROM follows
         UNION ALL
         SELECT followee_id, 'b' FROM follows) x
  GROUP  BY user_id
)
SELECT user_id, followers, following,
       followers - following AS net_gain
FROM   counts
ORDER  BY net_gain DESC;
```
**Explanation:** Net gain is followers minus following — positive means more people follow you than you follow.

---

## Q24: Users with 100 % follow-back rate

**Query:**
```sql
SELECT f.follower_id
FROM   follows f
GROUP  BY f.follower_id
HAVING COUNT(*) = SUM(
         CASE WHEN EXISTS (
           SELECT 1 FROM follows f2
           WHERE f2.follower_id = f.followee_id
             AND f2.followee_id = f.follower_id
         ) THEN 1 ELSE 0 END
       );
```
**Explanation:** If `COUNT = SUM(binary)`, every outgoing follow was reciprocated — 100 % back rate.

---

## Q25: Daily new follows trend (last 30 days)

**Query:**
```sql
-- MySQL 8+
SELECT DATE(created_at) AS day,
       COUNT(*)         AS new_follows
FROM   follows
WHERE  created_at >= CURRENT_DATE - INTERVAL 30 DAY
GROUP  BY day
ORDER  BY day;
```
**Explanation:** `DATE()` truncates the timestamp; `WHERE` limits to the last 30 days.

---

## Q26: Delete symmetric duplicate friendships (keep canonical row)

**Query:**
```sql
-- MySQL 8+
DELETE FROM friendships
WHERE  (user1_id, user2_id) NOT IN (
  SELECT user1_id, user2_id
  FROM  (SELECT LEAST(user1_id, user2_id)  AS user1_id,
                GREATEST(user1_id, user2_id) AS user2_id
         FROM   friendships) canon
  GROUP  BY user1_id, user2_id
);
```
**Explanation:** `LEAST`/`GREATEST` canonicalizes each row; the `DELETE` removes any row not in the canonical set.

**Alt1:**
```sql
-- PostgreSQL: CTE-based delete
WITH canon AS (
  SELECT DISTINCT LEAST(user1_id, user2_id)  AS u1,
                  GREATEST(user1_id, user2_id) AS u2
  FROM   friendships
)
DELETE FROM friendships f
WHERE  NOT EXISTS (
  SELECT 1 FROM canon c
  WHERE  c.u1 = LEAST(f.user1_id, f.user2_id)
    AND  c.u2 = GREATEST(f.user1_id, f.user2_id)
);
```
**Explanation:** The CTE builds the canonical set; the delete removes anything outside it.

---

## Q27: Normalize friendships (store each pair once, canonical form)

**Query:**
```sql
-- PostgreSQL
SELECT DISTINCT LEAST(user1_id, user2_id)  AS user1_id,
                GREATEST(user1_id, user2_id) AS user2_id,
                MIN(created_at)              AS created_at
FROM   friendships
GROUP  BY LEAST(user1_id, user2_id),
          GREATEST(user1_id, user2_id);
```
**Explanation:** `LEAST`/`GREATEST` deduplicates; `MIN(created_at)` keeps the earliest creation timestamp.

---

## Q28: Friend-of-friend suggestions ranked by mutual friend count

**Query:**
```sql
SELECT fof.f1              AS user_id,
       fof.f2              AS suggested_friend,
       COUNT(DISTINCT fof.mutual) AS mutual_count
FROM  (SELECT f1.user1_id AS f1, f2.user2_id AS f2, f1.user2_id AS mutual
       FROM   friendships f1
       JOIN   friendships f2 ON f1.user2_id = f2.user1_id
       WHERE  f1.user1_id != f2.user2_id) fof
LEFT JOIN friendships direct
  ON  direct.user1_id = fof.f1
  AND direct.user2_id = fof.f2
WHERE  direct.user1_id IS NULL
GROUP  BY fof.f1, fof.f2
ORDER  BY mutual_count DESC;
```
**Explanation:** Two-hop paths become candidates; `LEFT JOIN IS NULL` filters out existing friendships.

---

## Q29: Users exactly 2 hops away (friend-of-friend, not direct)

**Query:**
```sql
-- MySQL 8+
WITH two_hop AS (
  SELECT DISTINCT f1.user1_id AS source,
                  f2.user2_id AS target
  FROM   friendships f1
  JOIN   friendships f2 ON f1.user2_id = f2.user1_id
  WHERE  f1.user1_id != f2.user2_id
)
SELECT th.source, th.target
FROM   two_hop th
LEFT JOIN friendships direct
  ON  direct.user1_id = th.source
  AND direct.user2_id = th.target
WHERE  direct.user1_id IS NULL;
```
**Explanation:** Same structure as Q28 but without the aggregation — returns raw pairs.

---

## Q30: All users within 2 hops of a specific user X

**Query:**
```sql
-- PostgreSQL
WITH RECURSIVE hops AS (
  SELECT user2_id AS friend, 1 AS depth
  FROM   friendships
  WHERE  user1_id = 42
  UNION
  SELECT user1_id, 1
  FROM   friendships
  WHERE  user2_id = 42
  UNION
  SELECT f.user2_id, h.depth + 1
  FROM   friendships f
  JOIN   hops h ON f.user1_id = h.friend
  WHERE  h.depth < 2
  UNION
  SELECT f.user1_id, h.depth + 1
  FROM   friendships f
  JOIN   hops h ON f.user2_id = h.friend
  WHERE  h.depth < 2
)
SELECT DISTINCT friend, MIN(depth) AS min_depth
FROM   hops
WHERE  friend != 42
GROUP  BY friend;
```
**Explanation:** Recursive CTE walks both directions of friendships up to depth 2; `UNION` removes duplicates within the recursion.

---

## Q31: Shortest friendship depth — 2-hop existence check via self-join

**Query:**
```sql
SELECT CASE WHEN EXISTS (
  SELECT 1
  FROM   friendships f1
  JOIN   friendships f2
    ON  f1.user2_id = f2.user1_id
   AND  f1.user1_id = 123
   AND  f2.user2_id = 456
) THEN '2-hop exists'
     ELSE 'No 2-hop path'
END AS path_status;
```
**Explanation:** A single self-join on the intermediate user tests whether a 2-hop path exists between user 123 and user 456.

**Alt1:**
```sql
-- PostgreSQL: use EXISTS with a correlated subquery
SELECT CASE WHEN EXISTS (
  SELECT 1
  FROM   friendships f1
  WHERE  f1.user1_id = 123
    AND  EXISTS (
      SELECT 1
      FROM   friendships f2
      WHERE  f2.user1_id = f1.user2_id
        AND  f2.user2_id = 456
    )
) THEN 'YES' ELSE 'NO' END AS two_hop;
```
**Explanation:** Nested `EXISTS` avoids a join and is often optimized better by the engine.

---

## Q32: Shortest path up to 3 hops using recursive CTE

**Query:**
```sql
-- PostgreSQL
WITH RECURSIVE bfs AS (
  SELECT user2_id AS node, 1 AS depth, ARRAY[123, user2_id] AS path
  FROM   friendships
  WHERE  user1_id = 123
  UNION
  SELECT user1_id, 1, ARRAY[123, user1_id]
  FROM   friendships
  WHERE  user2_id = 123
  UNION
  SELECT f.user2_id, b.depth + 1, b.path || f.user2_id
  FROM   friendships f
  JOIN   bfs b ON f.user1_id = b.node
  WHERE  b.depth < 3
    AND  f.user2_id <> ALL(b.path)
  UNION
  SELECT f.user1_id, b.depth + 1, b.path || f.user1_id
  FROM   friendships f
  JOIN   bfs b ON f.user2_id = b.node
  WHERE  b.depth < 3
    AND  f.user1_id <> ALL(b.path)
)
SELECT node, MIN(depth) AS shortest_depth, MIN(path) AS shortest_path
FROM   bfs
WHERE  node = 456
GROUP  BY node;
```
**Explanation:** A BFS-style recursive CTE explores both directions at each hop; `<> ALL(path)` prevents revisiting nodes.

**Alt1:**
```sql
-- MySQL 8+: same BFS without array path (using concatenation)
WITH RECURSIVE bfs AS (
  SELECT user2_id AS node, 1 AS depth, CONCAT('123,', user2_id) AS path
  FROM   friendships
  WHERE  user1_id = 123
  UNION
  SELECT f.user2_id, b.depth + 1, CONCAT(b.path, ',', f.user2_id)
  FROM   friendships f
  JOIN   bfs b ON f.user1_id = b.node
  WHERE  b.depth < 3
    AND  FIND_IN_SET(f.user2_id, b.path) = 0
)
SELECT node, MIN(depth) AS shortest_depth
FROM   bfs
WHERE  node = 456
GROUP  BY node;
```
**Explanation:** MySQL uses `FIND_IN_SET` on a comma-delimited path string to prevent cycles.

---

## Q33: Detect orphaned or inconsistent friendship rows

**Query:**
```sql
SELECT f.user1_id, f.user2_id, f.created_at
FROM   friendships f
LEFT JOIN users u1 ON f.user1_id = u1.user_id
LEFT JOIN users u2 ON f.user2_id = u2.user_id
WHERE  u1.user_id IS NULL
   OR  u2.user_id IS NULL;
```
**Explanation:** A left join to `users` on both sides surfaces rows where a referenced user no longer exists.

---

## Q34: Users who posted at least X posts

**Query:**
```sql
-- MySQL 8+
SELECT p.user_id,
       u.name,
       COUNT(*) AS post_count
FROM   posts p
JOIN   users u ON p.user_id = u.user_id
GROUP  BY p.user_id, u.name
HAVING COUNT(*) >= 10
ORDER  BY post_count DESC;
```
**Explanation:** `HAVING COUNT(*) >= 10` filters users below the threshold; adjust `10` for any X.

---

## Q35: Most liked post per user

**Query:**
```sql
-- MySQL 8+
WITH ranked AS (
  SELECT p.user_id,
         p.post_id,
         p.content,
         COUNT(l.user_id) AS like_count,
         ROW_NUMBER() OVER (PARTITION BY p.user_id ORDER BY COUNT(l.user_id) DESC) AS rn
  FROM   posts p
  LEFT JOIN likes l ON p.post_id = l.post_id
  GROUP  BY p.user_id, p.post_id, p.content
)
SELECT user_id, post_id, content, like_count
FROM   ranked
WHERE  rn = 1;
```
**Explanation:** `ROW_NUMBER()` partitions by user and ranks posts by like count; `rn = 1` keeps the top post per user.

**Alt1:**
```sql
-- PostgreSQL: use DISTINCT ON
SELECT DISTINCT ON (p.user_id)
       p.user_id,
       p.post_id,
       p.content,
       COUNT(l.user_id) AS like_count
FROM   posts p
LEFT JOIN likes l ON p.post_id = l.post_id
GROUP  BY p.user_id, p.post_id, p.content
ORDER  BY p.user_id, COUNT(l.user_id) DESC;
```
**Explanation:** `DISTINCT ON (user_id)` keeps the first row per user as defined by the `ORDER BY` clause.

---

## Q36: Posts from friends in last 7 days (feed simulation)

**Query:**
```sql
SELECT p.post_id,
       p.user_id AS author,
       p.content,
       p.created_at
FROM   posts p
JOIN  (SELECT user2_id AS friend_id
       FROM   friendships
       WHERE  user1_id = 42
       UNION
       SELECT user1_id
       FROM   friendships
       WHERE  user2_id = 42) my_friends
  ON  p.user_id = my_friends.friend_id
WHERE  p.created_at >= CURRENT_TIMESTAMP - INTERVAL '7 days'
ORDER  BY p.created_at DESC;
```
**Explanation:** A subquery builds user 42's friend list (both directions); joining to `posts` filters recent content.

**Alt1:**
```sql
-- SQL Server: use TOP with the same approach
SELECT TOP 50 p.post_id,
       p.user_id AS author,
       p.content,
       p.created_at
FROM   posts p
JOIN  (SELECT user2_id AS friend_id
       FROM   friendships
       WHERE  user1_id = 42
       UNION
       SELECT user1_id
       FROM   friendships
       WHERE  user2_id = 42) my_friends
  ON  p.user_id = my_friends.friend_id
WHERE  p.created_at >= DATEADD(DAY, -7, GETDATE())
ORDER  BY p.created_at DESC;
```
**Explanation:** `TOP 50` limits the feed; `DATEADD` handles the 7-day lookback in SQL Server.

---

## Q37: Average likes per post overall

**Query:**
```sql
SELECT ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT post_id), 2) AS avg_likes_per_post
FROM   likes;
```
**Explanation:** Total likes divided by distinct posts with at least one like gives the average.

---

## Q38: Posts with the most comments

**Query:**
```sql
SELECT post_id,
       COUNT(*) AS comment_count
FROM   comments
GROUP  BY post_id
ORDER  BY comment_count DESC
LIMIT  10;
```
**Explanation:** Simple `GROUP BY` and `ORDER BY` with `LIMIT 10` returns the top commented posts.

---

## Q39: User engagement rate (total interactions ÷ posts)

**Query:**
```sql
SELECT p.user_id,
       u.name,
       COUNT(DISTINCT p.post_id)  AS posts,
       COALESCE(lc.likes,    0)   AS total_likes_received,
       COALESCE(cc.comments, 0)   AS total_comments_received,
       ROUND((COALESCE(lc.likes,0) + COALESCE(cc.comments,0))
             * 1.0 / NULLIF(COUNT(DISTINCT p.post_id),0), 2) AS engagement_rate
FROM   posts p
JOIN   users u ON p.user_id = u.user_id
LEFT JOIN (SELECT post_id, COUNT(*) AS likes FROM likes GROUP BY post_id) lc
  ON p.post_id = lc.post_id
LEFT JOIN (SELECT post_id, COUNT(*) AS comments FROM comments GROUP BY post_id) cc
  ON p.post_id = cc.post_id
GROUP  BY p.user_id, u.name, lc.likes, cc.comments;
```
**Explanation:** Aggregated likes and comments divided by post count yields a per-user engagement metric.

---

## Q40: Hashtag extraction from post content

**Query:**
```sql
-- MySQL 8+
WITH RECURSIVE tags AS (
  SELECT post_id,
         SUBSTRING_INDEX(SUBSTRING_INDEX(content, '#', 2), ' ', -1) AS tag,
         CASE WHEN LENGTH(content) - LENGTH(REPLACE(content, '#', '')) > 1
              THEN SUBSTRING(content, LOCATE('#', content, LOCATE('#', content) + 1))
              ELSE NULL
         END AS rest
  FROM   posts
  WHERE  content LIKE '%#%'
  UNION ALL
  SELECT post_id,
         CASE WHEN rest LIKE '#%'
              THEN SUBSTRING_INDEX(SUBSTRING(rest, 2), ' ', 1)
              ELSE NULL END,
         CASE WHEN rest LIKE '#%'
              THEN SUBSTRING(rest, LOCATE(' ', rest) + 1)
              ELSE NULL END
  FROM   tags
  WHERE  rest LIKE '#%'
)
SELECT tag, COUNT(DISTINCT post_id) AS post_count
FROM   tags
WHERE  tag IS NOT NULL AND tag != ''
GROUP  BY tag
ORDER  BY post_count DESC;
```
**Explanation:** A recursive CTE peels one `#tag` per iteration; `SUBSTRING_INDEX` isolates each token.

**Alt1:**
```sql
-- PostgreSQL: regex matching
SELECT tag, COUNT(DISTINCT post_id) AS post_count
FROM  (SELECT post_id,
              UNNEST(REGEXP_MATCHES(content, '#([A-Za-z0-9_]+)', 'g')) AS tag
       FROM   posts) extracted
GROUP  BY tag
ORDER  BY post_count DESC;
```
**Explanation:** `REGEXP_MATCHES` with `UNNEST` expands each hashtag into a row; much cleaner than the recursive approach.

---

## Q41: Viral post growth — cumulative likes over time

**Query:**
```sql
-- MySQL 8+
SELECT l.created_at::DATE AS day,
       COUNT(*)            AS likes_that_day,
       SUM(COUNT(*)) OVER (ORDER BY l.created_at::DATE) AS cumulative_likes
FROM   likes l
WHERE  l.post_id = 999
GROUP  BY l.created_at::DATE
ORDER  BY day;
```
**Explanation:** `SUM(...) OVER (ORDER BY day)` builds a running total of likes, showing how a post goes viral.

---

## Q42: Posts that received zero likes

**Query:**
```sql
SELECT p.post_id, p.user_id, p.created_at
FROM   posts p
LEFT JOIN likes l ON p.post_id = l.post_id
WHERE  l.user_id IS NULL;
```
**Explanation:** The anti-join pattern surfaces posts with no like rows.

---

## Q43: Most active commenters

**Query:**
```sql
SELECT c.user_id,
       u.name,
       COUNT(*) AS comments_made
FROM   comments c
JOIN   users u ON c.user_id = u.user_id
GROUP  BY c.user_id, u.name
ORDER  BY comments_made DESC
LIMIT  10;
```
**Explanation:** Grouping comments by author and ordering gives the top 10 commenters.

---

## Q44: Popular content categories by total engagement

**Query:**
```sql
-- PostgreSQL
SELECT category,
       SUM(likes + comments) AS total_engagement
FROM  (SELECT CASE
              WHEN content ILIKE '%travel%'   THEN 'Travel'
              WHEN content ILIKE '%food%'     THEN 'Food'
              WHEN content ILIKE '%tech%'     THEN 'Tech'
              ELSE 'Other'
           END AS category,
           COALESCE(l.likes, 0) AS likes,
           COALESCE(c.comments, 0) AS comments
       FROM   posts p
       LEFT JOIN (SELECT post_id, COUNT(*) AS likes FROM likes GROUP BY post_id) l
         ON p.post_id = l.post_id
       LEFT JOIN (SELECT post_id, COUNT(*) AS comments FROM comments GROUP BY post_id) c
         ON p.post_id = c.post_id) p1
GROUP  BY category
ORDER  BY total_engagement DESC;
```
**Explanation:** `CASE` classifies posts into categories; likes and comments are aggregated per category.

**Alt1:**
```sql
-- MySQL 8+: recency-weighted engagement score
WITH eng AS (
  SELECT p.post_id,
         COUNT(DISTINCT l.user_id) AS likes,
         COUNT(DISTINCT c.comment_id) AS comments,
         MAX(p.created_at) AS last_active
  FROM   posts p
  LEFT JOIN likes l ON p.post_id = l.post_id
  LEFT JOIN comments c ON p.post_id = c.post_id
  GROUP  BY p.post_id
)
SELECT e.post_id,
       e.likes + e.comments AS raw_score,
       ROUND((e.likes + e.comments) / (DATEDIFF(NOW(), e.last_active) + 1), 2) AS hot_score
FROM   eng e
ORDER  BY hot_score DESC
LIMIT  10;
```
**Explanation:** Dividing engagement by post age yields a "hot score" that favors recent viral content.

---

## Q45: Posts with the most diverse commenters (unique commenters)

**Query:**
```sql
SELECT post_id,
       COUNT(DISTINCT user_id) AS unique_commenters
FROM   comments
GROUP  BY post_id
ORDER  BY unique_commenters DESC
LIMIT  10;
```
**Explanation:** `COUNT(DISTINCT user_id)` measures commenter breadth, not just comment volume.

---

## Q46: Average gap between consecutive posts per user

**Query:**
```sql
-- MySQL 8+
WITH ordered AS (
  SELECT user_id,
         created_at,
         LAG(created_at) OVER (PARTITION BY user_id ORDER BY created_at) AS prev_post
  FROM   posts
)
SELECT user_id,
       AVG(TIMESTAMPDIFF(HOUR, prev_post, created_at)) AS avg_gap_hours
FROM   ordered
WHERE  prev_post IS NOT NULL
GROUP  BY user_id
ORDER  BY avg_gap_hours;
```
**Explanation:** `LAG()` fetches the previous post's timestamp; `TIMESTAMPDIFF` measures each gap, then we average them.

---

## Q47: Posts created in the last 24 hours with like/comment counts

**Query:**
```sql
-- PostgreSQL
SELECT p.post_id,
       p.user_id,
       p.content,
       COUNT(DISTINCT l.user_id)  AS likes,
       COUNT(DISTINCT c.comment_id) AS comments
FROM   posts p
LEFT JOIN likes    l ON p.post_id = l.post_id
LEFT JOIN comments c ON p.post_id = c.post_id
WHERE  p.created_at >= NOW() - INTERVAL '24 hours'
GROUP  BY p.post_id, p.user_id, p.content
ORDER  BY likes DESC;
```
**Explanation:** A time filter on `posts` followed by left-joined aggregates shows fresh content's engagement.

---

## Q48: Users who joined but never posted

**Query:**
```sql
SELECT u.user_id, u.name, u.joined_at
FROM   users u
LEFT JOIN posts p ON u.user_id = p.user_id
WHERE  p.post_id IS NULL;
```
**Explanation:** Standard anti-join: users with no matching post row are dormant/never-posted accounts.

---

## Q49: Time-to-first-post per user

**Query:**
```sql
-- MySQL 8+
SELECT u.user_id,
       u.name,
       DATEDIFF(MIN(p.created_at), u.joined_at) AS days_to_first_post
FROM   users u
JOIN   posts p ON u.user_id = p.user_id
GROUP  BY u.user_id, u.name, u.joined_at
ORDER  BY days_to_first_post;
```
**Explanation:** `MIN(created_at)` is the first post; `DATEDIFF` vs `joined_at` measures activation latency.

**Alt1:**
```sql
-- PostgreSQL: window function variant
WITH first_posts AS (
  SELECT user_id,
         MIN(created_at) AS first_post_at
  FROM   posts
  GROUP  BY user_id
)
SELECT u.user_id,
       u.name,
       EXTRACT(DAY FROM (f.first_post_at - u.joined_at))::int AS days_to_first_post
FROM   users u
JOIN   first_posts f ON u.user_id = f.user_id
ORDER  BY days_to_first_post;
```
**Explanation:** Same result — a CTE pre-computes first posts and `EXTRACT(DAY FROM interval)` gives the gap.

---

## Q50: Engagement rate per post

**Query:**
```sql
SELECT p.post_id,
       p.user_id,
       COUNT(DISTINCT l.user_id)       AS likes,
       COUNT(DISTINCT c.comment_id)    AS comments,
       ROUND((COUNT(DISTINCT l.user_id) + COUNT(DISTINCT c.comment_id))
             * 1.0 / NULLIF(er.est_reach, 0), 4) AS engagement_rate
FROM   posts p
LEFT JOIN likes    l ON p.post_id = l.post_id
LEFT JOIN comments c ON p.post_id = c.post_id
LEFT JOIN (SELECT post_id, 1000 AS est_reach FROM posts) er ON p.post_id = er.post_id
GROUP  BY p.post_id, p.user_id, er.est_reach
ORDER  BY engagement_rate DESC;
```
**Explanation:** Interactions divided by an estimated reach yields the post engagement rate; swap in a real impressions table when available.

---

## Q51: Top hashtags by aggregate engagement

**Query:**
```sql
-- PostgreSQL
WITH tags AS (
  SELECT post_id,
         UNNEST(REGEXP_MATCHES(content, '#([A-Za-z0-9_]+)', 'g')) AS tag
  FROM   posts
),
eng AS (
  SELECT p.post_id,
         COUNT(DISTINCT l.user_id) AS likes,
         COUNT(DISTINCT c.comment_id) AS comments
  FROM   posts p
  LEFT JOIN likes    l ON p.post_id = l.post_id
  LEFT JOIN comments c ON p.post_id = c.post_id
  GROUP  BY p.post_id
)
SELECT t.tag,
       COUNT(DISTINCT t.post_id)                  AS posts,
       SUM(COALESCE(e.likes, 0))                  AS total_likes,
       SUM(COALESCE(e.comments, 0))               AS total_comments,
       SUM(COALESCE(e.likes, 0) + COALESCE(e.comments, 0)) AS total_engagement
FROM   tags t
LEFT JOIN eng e ON t.post_id = e.post_id
GROUP  BY t.tag
ORDER  BY total_engagement DESC
LIMIT  20;
```
**Explanation:** Hashtag extraction joined to per-post engagement aggregates ranks tags by total interaction.

**Alt1:**
```sql
-- MySQL 8+: engagement per hashtag appearance, per post
WITH RECURSIVE tags AS (
  SELECT post_id,
         SUBSTRING_INDEX(SUBSTRING_INDEX(content, '#', 2), ' ', -1) AS tag,
         CASE WHEN LENGTH(content) - LENGTH(REPLACE(content, '#', '')) > 1
              THEN SUBSTRING(content, LOCATE('#', content, LOCATE('#', content) + 1))
              ELSE NULL END AS rest
  FROM   posts
  WHERE  content LIKE '%#%'
  UNION ALL
  SELECT post_id,
         CASE WHEN rest LIKE '#%' THEN SUBSTRING_INDEX(SUBSTRING(rest, 2), ' ', 1) ELSE NULL END,
         CASE WHEN rest LIKE '#%' THEN SUBSTRING(rest, LOCATE(' ', rest) + 1) ELSE NULL END
  FROM   tags
  WHERE  rest LIKE '#%'
),
per_tag AS (
  SELECT t.tag,
         t.post_id,
         COUNT(DISTINCT l.user_id) AS likes
  FROM   tags t
  LEFT JOIN likes l ON t.post_id = l.post_id
  WHERE  t.tag IS NOT NULL AND t.tag != ''
  GROUP  BY t.tag, t.post_id
)
SELECT tag,
       AVG(likes)      AS avg_likes_per_post,
       COUNT(post_id)  AS posts_tagged
FROM   per_tag
GROUP  BY tag
ORDER  BY avg_likes_per_post DESC;
```
**Explanation:** Averages engagement per tagged post for a normalized "engagement strength" ranking.

---

## Q52: Recommended content: posts liked by friends but not by me

**Query:**
```sql
-- PostgreSQL
WITH my_friends AS (
  SELECT user2_id AS friend_id FROM friendships WHERE user1_id = 42
  UNION
  SELECT user1_id FROM friendships WHERE user2_id = 42
)
SELECT p.post_id,
       p.user_id  AS author,
       COUNT(DISTINCT l.user_id) AS friends_who_liked
FROM   posts p
JOIN   likes l ON p.post_id = l.post_id
JOIN   my_friends mf ON l.user_id = mf.friend_id
WHERE  p.post_id NOT IN (
  SELECT post_id FROM likes WHERE user_id = 42
)
GROUP  BY p.post_id, p.user_id
ORDER  BY friends_who_liked DESC
LIMIT  10;
```
**Explanation:** Join posts → likes → my friends, then exclude posts I already liked; rank by friend votes.

**Alt1:**
```sql
-- MySQL 8+: NOT EXISTS version
SELECT p.post_id, p.user_id, COUNT(*) AS friends_who_liked
FROM   posts p
JOIN   likes l ON p.post_id = l.post_id
WHERE  l.user_id IN (SELECT user2_id FROM friendships WHERE user1_id = 42
                     UNION
                     SELECT user1_id FROM friendships WHERE user2_id = 42)
  AND  NOT EXISTS (SELECT 1 FROM likes me
                   WHERE me.post_id = p.post_id AND me.user_id = 42)
GROUP  BY p.post_id, p.user_id
ORDER  BY friends_who_liked DESC
LIMIT  10;
```
**Explanation:** `NOT EXISTS` is more explicit than `NOT IN` and behaves the same when subquery values are non-null.

---

## Q53: Likes received vs sent balance per user

**Query:**
```sql
-- MySQL 8+
WITH received AS (
  SELECT p.user_id,
         COUNT(*) AS likes_received
  FROM   likes l
  JOIN   posts p ON l.post_id = p.post_id
  GROUP  BY p.user_id
),
sent AS (
  SELECT user_id,
         COUNT(*) AS likes_sent
  FROM   likes
  GROUP  BY user_id
)
SELECT COALESCE(r.user_id, s.user_id) AS user_id,
       COALESCE(r.likes_received, 0) AS likes_received,
       COALESCE(s.likes_sent, 0)     AS likes_sent,
       COALESCE(r.likes_received, 0) - COALESCE(s.likes_sent, 0) AS balance
FROM   received r
FULL JOIN sent s ON r.user_id = s.user_id
ORDER  BY balance DESC;
```
**Explanation:** Two aggregations — likes on my posts vs likes I gave — are combined with a full join.

---

## Q54: "Like heavy" users (give many likes, receive few)

**Query:**
```sql
WITH sent AS (
  SELECT user_id, COUNT(*) AS likes_sent
  FROM   likes GROUP BY user_id
),
received AS (
  SELECT p.user_id, COUNT(*) AS likes_received
  FROM   likes l JOIN posts p ON l.post_id = p.post_id
  GROUP  BY p.user_id
)
SELECT s.user_id, s.likes_sent, COALESCE(r.likes_received, 0) AS likes_received
FROM   sent s
LEFT JOIN received r ON s.user_id = r.user_id
WHERE  s.likes_sent > 100
  AND  COALESCE(r.likes_received, 0) < 10;
```
**Explanation:** High outgoing, low incoming likes flags users who engage but don't attract engagement back.

---

## Q55: Reciprocal liking patterns (A likes B's post AND B likes A's post)

**Query:**
```sql
-- PostgreSQL
SELECT pa.user_id AS author_a,
       pb.user_id AS author_b,
       COUNT(*) AS reciprocal_pairs
FROM   posts pa
JOIN   likes  la ON pa.post_id = la.post_id
JOIN   posts  pb ON pb.user_id = la.user_id      -- A liked B's post pa
JOIN   likes  lb ON lb.post_id = pb.post_id
                AND lb.user_id = pa.user_id       -- B likes A's post pb
WHERE  pa.user_id < pb.user_id
GROUP  BY pa.user_id, pb.user_id;
```
**Explanation:** Double self-join verifies both like directions between a pair of users.

**Alt1:**
```sql
-- MySQL 8+: count A's likes on B's posts and vice-versa
WITH alikes_b AS (
  SELECT p.user_id AS a, l.user_id AS b, COUNT(*) AS cnt
  FROM   posts p
  JOIN   likes l ON l.post_id = p.post_id
  GROUP  BY p.user_id, l.user_id
)
SELECT a, b, a1.cnt AS a_likes_b, a2.cnt AS b_likes_a
FROM   alikes_b a1
JOIN   alikes_b a2 ON a1.a = a2.b AND a1.b = a2.a
WHERE  a1.a < a1.b;
```
**Explanation:** Self-joining the author–liker pair summary finds symmetric like pairs in one pass.

---

## Q56: Most generous likers (top 10 by likes given)

**Query:**
```sql
SELECT user_id,
       COUNT(*) AS likes_given
FROM   likes
GROUP  BY user_id
ORDER  BY likes_given DESC
LIMIT  10;
```
**Explanation:** Grouping `likes` by liker and counting gives total likes given per account.

---

## Q57: Like velocity for trending posts (likes in the first hour)

**Query:**
```sql
-- MySQL 8+
SELECT p.post_id,
       COUNT(l.user_id) AS likes_first_hour
FROM   posts p
JOIN   likes l
  ON  p.post_id = l.post_id
 AND  l.created_at BETWEEN p.created_at AND p.created_at + INTERVAL 1 HOUR
GROUP  BY p.post_id
ORDER  BY likes_first_hour DESC
LIMIT  10;
```
**Explanation:** The join condition constrains likes to within 60 minutes of publishing — a velocity signal.

---

## Q58: Like activity patterns by day of week

**Query:**
```sql
-- PostgreSQL
SELECT EXTRACT(ISODOW FROM created_at) AS dow,
       COUNT(*)                        AS like_count
FROM   likes
GROUP  BY dow
ORDER  BY dow;
```
**Explanation:** `EXTRACT(ISODOW)` returns 1–7 (Mon–Sun) for weekday distribution analysis.

---

## Q59: Comment threads using a recursive reply-to CTE

**Query:**
```sql
-- MySQL 8+
WITH RECURSIVE thread AS (
  SELECT comment_id, post_id, user_id, parent_comment_id, content,
         0 AS depth,
         CAST(comment_id AS CHAR(1000)) AS path
  FROM   comments
  WHERE  post_id = 123
    AND  parent_comment_id IS NULL
  UNION ALL
  SELECT c.comment_id, c.post_id, c.user_id, c.parent_comment_id, c.content,
         t.depth + 1,
         CONCAT(t.path, '>', c.comment_id)
  FROM   comments c
  JOIN   thread t ON c.parent_comment_id = t.comment_id
)
SELECT comment_id, user_id, depth, content, path
FROM   thread
ORDER  BY path;
```
**Explanation:** Anchor comments (no parent) start the recursion; ordering by the concatenated `path` preserves visual thread order.

**Alt1:**
```sql
-- Oracle: CONNECT BY PRIOR style
SELECT comment_id, user_id, content,
       LEVEL AS depth,
       SYS_CONNECT_BY_PATH(comment_id, '/') AS path
FROM   comments
START WITH post_id = 123 AND parent_comment_id IS NULL
CONNECT BY PRIOR comment_id = parent_comment_id
ORDER  BY path;
```
**Explanation:** Oracle's hierarchical `CONNECT BY` avoids an explicit recursive CTE.

---

## Q60: Deepest comment thread(s)

**Query:**
```sql
-- MySQL 8+ (assumes Q59 thread CTE shape)
WITH RECURSIVE thread AS (
  SELECT comment_id, post_id, parent_comment_id, 0 AS depth
  FROM   comments
  WHERE  parent_comment_id IS NULL
  UNION ALL
  SELECT c.comment_id, c.post_id, c.parent_comment_id, t.depth + 1
  FROM   comments c
  JOIN   thread t ON c.parent_comment_id = t.comment_id
)
SELECT post_id,
       MAX(depth) AS max_thread_depth
FROM   thread
GROUP  BY post_id
ORDER  BY max_thread_depth DESC;
```
**Explanation:** The recursion computes each comment's depth; `MAX(depth)` per post finds the deepest thread.

---

## Q61: Users who only comment and never post

**Query:**
```sql
SELECT DISTINCT c.user_id
FROM   comments c
LEFT JOIN posts p ON c.user_id = p.user_id
WHERE  p.post_id IS NULL;
```
**Explanation:** Commenters with no matching post rows are pure commenters.

---

## Q62: Most replied-to parent comments

**Query:**
```sql
SELECT parent.post_id,
       parent.comment_id,
       parent.user_id,
       COUNT(child.comment_id) AS replies
FROM   comments parent
LEFT JOIN comments child
  ON  child.parent_comment_id = parent.comment_id
WHERE  parent.parent_comment_id IS NULL
GROUP  BY parent.post_id, parent.comment_id, parent.user_id
ORDER  BY replies DESC
LIMIT  10;
```
**Explanation:** Self-join on `parent_comment_id` counts direct replies to each top-level comment.

---

## Q63: Comment-to-like ratio per post

**Query:**
```sql
SELECT p.post_id,
       COUNT(DISTINCT l.user_id)    AS likes,
       COUNT(DISTINCT c.comment_id) AS comments,
       CASE WHEN COUNT(DISTINCT l.user_id) = 0 THEN NULL
            ELSE ROUND(COUNT(DISTINCT c.comment_id) * 1.0
                       / COUNT(DISTINCT l.user_id), 3)
       END AS comment_like_ratio
FROM   posts p
LEFT JOIN likes    l ON p.post_id = l.post_id
LEFT JOIN comments c ON p.post_id = c.post_id
GROUP  BY p.post_id
ORDER  BY comment_like_ratio DESC;
```
**Explanation:** Comments divided by likes reveals content that drives discussion over passive appreciation.

---

## Q64: Percentage of users active weekly (weekly active rate)

**Query:**
```sql
-- MySQL 8+
WITH activity AS (
  SELECT 'posts'   AS src, user_id, created_at AS ts FROM posts
  UNION ALL
  SELECT 'likes',   user_id, created_at          FROM likes
  UNION ALL
  SELECT 'comments', user_id, created_at         FROM comments
  UNION ALL
  SELECT 'messages', sender_id, created_at       FROM messages
)
SELECT WEEK(CURRENT_DATE, 1) AS week_number,
       COUNT(DISTINCT a.user_id)                   AS active_users,
       (SELECT COUNT(*) FROM users)                AS total_users,
       ROUND(COUNT(DISTINCT a.user_id) * 100.0
             / (SELECT COUNT(*) FROM users), 2)    AS active_pct
FROM   activity a
WHERE  a.ts >= CURRENT_TIMESTAMP - INTERVAL 7 DAY;
```
**Explanation:** `UNION ALL` merges all action tables; distinct users in the 7-day window over total users gives the weekly rate.

**Alt1:**
```sql
-- SQL Server: same merge with date filter
WITH activity AS (
  SELECT user_id, created_at AS ts FROM posts
  UNION ALL
  SELECT user_id, created_at FROM likes
  UNION ALL
  SELECT user_id, created_at FROM comments
)
SELECT COUNT(DISTINCT a.user_id)                        AS active_users,
       (SELECT COUNT(*) FROM users)                     AS total_users,
       ROUND(COUNT(DISTINCT a.user_id) * 100.0
             / (SELECT COUNT(*) FROM users), 2)         AS active_pct
FROM   activity a
WHERE  a.ts >= DATEADD(DAY, -7, GETDATE());
```
**Explanation:** SQL Server syntax differences: `DATEADD` instead of `INTERVAL`, `GETDATE()` instead of `NOW()`.

---

## Q65: Daily active users (DAU trend, last 30 days)

**Query:**
```sql
-- PostgreSQL
WITH activity AS (
  SELECT DATE(created_at) AS day, user_id FROM posts
  UNION
  SELECT DATE(created_at), user_id FROM likes
  UNION
  SELECT DATE(created_at), user_id FROM comments
)
SELECT day,
       COUNT(DISTINCT user_id) AS dau
FROM   activity
WHERE  day >= CURRENT_DATE - INTERVAL '30 days'
GROUP  BY day
ORDER  BY day;
```
**Explanation:** Union of all interaction dates yields unique users per day — the classic DAU metric.

---

## Q66: New user retention — posted within 7 days of joining

**Query:**
```sql
-- MySQL 8+
WITH joined AS (
  SELECT user_id, joined_at
  FROM   users
  WHERE  joined_at >= CURRENT_DATE - INTERVAL 90 DAY
)
SELECT COUNT(*) AS new_users,
       SUM(CASE WHEN p.post_id IS NOT NULL THEN 1 ELSE 0 END) AS activated,
       ROUND(SUM(CASE WHEN p.post_id IS NOT NULL THEN 1 ELSE 0 END)
             * 100.0 / COUNT(*), 2) AS activation_pct
FROM   joined j
LEFT JOIN posts p
  ON  p.user_id = j.user_id
 AND  p.created_at BETWEEN j.joined_at AND j.joined_at + INTERVAL 7 DAY;
```
**Explanation:** Only posts within a 7-day window after `joined_at` count; the ratio measures activation.

---

## Q67: User activity streaks (consecutive days active)

**Query:**
```sql
-- PostgreSQL
WITH days AS (
  SELECT user_id, DATE(created_at) AS day,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY DATE(created_at)) AS rn
  FROM   (
    SELECT user_id, created_at FROM posts
    UNION
    SELECT user_id, created_at FROM likes
    UNION
    SELECT user_id, created_at FROM comments
  ) acts
  GROUP  BY user_id, DATE(created_at)
),
streaks AS (
  SELECT user_id, day,
         day - rn * INTERVAL '1 day' AS group_key
  FROM   days
)
SELECT user_id,
       COUNT(*)                                  AS streak_length,
       MIN(day) AS streak_start,
       MAX(day) AS streak_end
FROM   streaks
GROUP  BY user_id, group_key
ORDER  BY streak_length DESC
LIMIT  10;
```
**Explanation:** Subtracting the row number from the date turns consecutive days into the same integer "group key", and each group is a streak.

---

## Q68: Churned users (no activity in the last 30 days)

**Query:**
```sql
-- MySQL 8+
SELECT u.user_id, u.name, u.joined_at
FROM   users u
WHERE  NOT EXISTS (
  SELECT 1 FROM posts    p WHERE p.user_id    = u.user_id
                             AND p.created_at >= CURRENT_TIMESTAMP - INTERVAL 30 DAY
)
  AND  NOT EXISTS (
  SELECT 1 FROM likes    l WHERE l.user_id    = u.user_id
                             AND l.created_at >= CURRENT_TIMESTAMP - INTERVAL 30 DAY
)
  AND  NOT EXISTS (
  SELECT 1 FROM comments c WHERE c.user_id    = u.user_id
                             AND c.created_at >= CURRENT_TIMESTAMP - INTERVAL 30 DAY
);
```
**Explanation:** Three `NOT EXISTS` checks against each action table confirm 30 days of complete inactivity.

---

## Q69: Monthly active user (MAU) growth

**Query:**
```sql
-- PostgreSQL
WITH acts AS (
  SELECT user_id, date_trunc('month', created_at) AS mon FROM posts
  UNION
  SELECT user_id, date_trunc('month', created_at) FROM likes
  UNION
  SELECT user_id, date_trunc('month', created_at) FROM comments
)
SELECT mon,
       COUNT(DISTINCT user_id) AS mau,
       ROUND(COUNT(DISTINCT user_id)
             * 100.0 / LAG(COUNT(DISTINCT user_id)) OVER (ORDER BY mon), 2)
             - 100 AS growth_pct
FROM   acts
GROUP  BY mon
ORDER  BY mon;
```
**Explanation:** `date_trunc` buckets activity by month; `LAG` compares each MAU with the prior month for growth.

---

## Q70: Weekly content creation trend

**Query:**
```sql
-- SQL Server
SELECT DATEPART(ISO_WEEK, created_at) AS week_num,
       YEAR(created_at)               AS year_num,
       COUNT(*)                       AS posts_created
FROM   posts
GROUP  BY YEAR(created_at), DATEPART(ISO_WEEK, created_at)
ORDER  BY year_num, week_num;
```
**Explanation:** `DATEPART(ISO_WEEK)` + `YEAR` help group posts into yearly week buckets.

---

## Q71: User engagement cohort analysis (by join month)

**Query:**
```sql
-- MySQL 8+
WITH acts AS (
  SELECT user_id, created_at::DATE AS day FROM posts
  UNION ALL
  SELECT user_id, created_at::DATE FROM likes
  UNION ALL
  SELECT user_id, created_at::DATE FROM comments
)
SELECT DATE_FORMAT(u.joined_at, '%Y-%m')          AS cohort,
       FLOOR(DATEDIFF(a.day, u.joined_at) / 7)    AS week_offset,
       COUNT(DISTINCT a.user_id)                   AS active_users,
       COUNT(DISTINCT a.user_id) * 1.0
       / NULLIF(MAX(COUNT(DISTINCT a.user_id)) OVER (PARTITION BY u.joined_at), 0)
                  AS retention_rate
FROM   users u
JOIN   acts a ON a.user_id = u.user_id
GROUP  BY cohort, week_offset
ORDER  BY cohort, week_offset;
```
**Explanation:** Each user's join month is a cohort; activity is measured in week offsets to track retention decay.

---

## Q72: Weekday vs weekend posting activity

**Query:**
```sql
-- PostgreSQL
SELECT CASE WHEN EXTRACT(ISODOW FROM created_at) IN (6, 7) THEN 'Weekend'
            ELSE 'Weekday' END AS period,
       COUNT(*) AS posts_created
FROM   posts
GROUP  BY period;
```
**Explanation:** `EXTRACT(ISODOW)` values 6–7 are Saturday/Sunday; grouping by period splits the data.

---

## Q73: Users who re-engaged after 14+ days of dormancy

**Query:**
```sql
-- MySQL 8+
WITH activity AS (
  SELECT user_id, created_at AS ts FROM posts
  UNION ALL
  SELECT user_id, created_at FROM likes
  UNION ALL
  SELECT user_id, created_at FROM comments
),
ordered AS (
  SELECT user_id, ts,
         LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) AS prev_ts
  FROM   activity
)
SELECT DISTINCT user_id
FROM   ordered
WHERE  prev_ts IS NOT NULL
  AND  TIMESTAMPDIFF(DAY, prev_ts, ts) >= 14;
```
**Explanation:** `LAG` compares consecutive interactions; gaps ≥ 14 days indicate a return after dormancy.

---

## Q74: Median friend count

**Query:**
```sql
-- MySQL 8+
WITH fc AS (
  SELECT user1_id AS uid, COUNT(*) AS cnt FROM friendships GROUP BY user1_id
  UNION ALL
  SELECT user2_id, COUNT(*) FROM friendships GROUP BY user2_id
),
ranked AS (
  SELECT cnt,
         ROW_NUMBER() OVER (ORDER BY cnt)  AS rn_asc,
         ROW_NUMBER() OVER (ORDER BY cnt DESC) AS rn_desc
  FROM   fc
)
SELECT AVG(cnt) AS median_friend_count
FROM   ranked
WHERE  rn_asc BETWEEN rn_desc - 1 AND rn_desc + 1;
```
**Explanation:** The classic "middle rows" trick — row numbers from both ends overlap only at the median.

**Alt1:**
```sql
-- PostgreSQL: use PERCENTILE_CONT
WITH fc AS (
  SELECT user1_id AS uid, COUNT(*) AS cnt FROM friendships GROUP BY user1_id
  UNION ALL
  SELECT user2_id, COUNT(*) FROM friendships GROUP BY user2_id
)
SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY cnt) AS median_friend_count
FROM   fc;
```
**Explanation:** `PERCENTILE_CONT` computes the continuous median directly.

---

## Q75: Detecting suspicious follow spikes (auto-accounts)

**Query:**
```sql
-- MySQL 8+
WITH daily AS (
  SELECT followee_id,
         DATE(created_at) AS day,
         COUNT(*)         AS follows_that_day
  FROM   follows
  GROUP  BY followee_id, DATE(created_at)
),
stats AS (
  SELECT followee_id,
         AVG(follows_that_day) AS mean,
         STDDEV(follows_that_day) AS sd
  FROM   daily
  GROUP  BY followee_id
)
SELECT d.followee_id,
       d.day,
       d.follows_that_day,
       ROUND(s.mean, 2)                          AS avg_daily_follows,
       ROUND(d.follows_that_day / NULLIF(s.mean, 0), 2) AS spike_ratio
FROM   daily d
JOIN   stats s ON d.followee_id = s.followee_id
WHERE  d.follows_that_day > 5 * s.mean
  AND  s.mean > 0
ORDER  BY spike_ratio DESC;
```
**Explanation:** Follows exceeding 5× the account's own daily average signal engagement farms or bot-bought followers.

**Alt1:**
```sql
-- PostgreSQL: look for accounts that follow many users in a single minute
SELECT follower_id,
       date_trunc('minute', created_at) AS minute,
       COUNT(*) AS follows_per_minute
FROM   follows
GROUP  BY follower_id, date_trunc('minute', created_at)
HAVING COUNT(*) > 20
ORDER  BY follows_per_minute DESC;
```
**Explanation:** Programmatic accounts typically burst 20+ follows within one minute; the threshold is tunable.

---

## Q76: Second-degree reach — distinct friends-of-friends count

**Query:**
```sql
-- PostgreSQL
WITH my_friends AS (
  SELECT user2_id AS uid FROM friendships WHERE user1_id = 42
  UNION
  SELECT user1_id FROM friendships WHERE user2_id = 42
),
fof AS (
  SELECT f.user2_id AS fof_id
  FROM   friendships f
  JOIN   my_friends mf ON f.user1_id = mf.uid
  UNION
  SELECT f.user1_id
  FROM   friendships f
  JOIN   my_friends mf ON f.user2_id = mf.uid
)
SELECT COUNT(DISTINCT fof_id)                    AS second_degree_reach,
       COUNT(DISTINCT fof_id) - (SELECT COUNT(*) FROM my_friends) AS net_new_users
FROM   fof
WHERE  fof_id <> 42;
```
**Explanation:** Expand to friends-of-friends in both directions, count distinct, then subtract my direct friends for net reach.

---

## Q77: Filter muted users from the generated feed

**Query:**
```sql
-- MySQL 8+
SELECT p.post_id, p.user_id AS author, p.content, p.created_at
FROM   posts p
WHERE  p.user_id IN (
  SELECT user2_id AS friend_id FROM friendships WHERE user1_id = 42
  UNION
  SELECT user1_id FROM friendships WHERE user2_id = 42
)
  AND  p.user_id NOT IN (
  SELECT muted_id FROM mutes WHERE muter_id = 42
)
  AND  p.created_at >= CURRENT_TIMESTAMP - INTERVAL 7 DAY
ORDER  BY p.created_at DESC;
```
**Explanation:** A `NOT IN` against `mutes` removes muted accounts' posts from the friend feed.

---

## Q78: Notification digests — users with activity in the last 24h

**Query:**
```sql
-- PostgreSQL
WITH activity AS (
  SELECT p.user_id, 'post'::text AS type, p.created_at
  FROM   posts p
  UNION ALL
  SELECT l.user_id, 'like', l.created_at FROM likes l
  UNION ALL
  SELECT c.user_id, 'comment', c.created_at FROM comments c
)
SELECT DISTINCT u.user_id, u.name,
       COUNT(*) OVER (PARTITION BY u.user_id) AS events_24h,
       MAX(a.created_at) OVER (PARTITION BY u.user_id) AS last_event
FROM   users u
JOIN   activity a ON a.user_id = u.user_id
WHERE  a.created_at >= NOW() - INTERVAL '24 hours'
ORDER  BY events_24h DESC;
```
**Explanation:** Merged activity rows joined to users, filtered to 24h, with count and latest event per user.

---

## Q79: Reciprocity index (mutual follows ÷ total follows)

**Query:**
```sql
-- PostgreSQL
WITH edges AS (
  SELECT follower_id, followee_id FROM follows
),
mutual AS (
  SELECT COUNT(*) / 2.0 AS mutual_pairs
  FROM   edges e1
  JOIN   edges e2 ON e1.follower_id = e2.followee_id
                 AND e1.followee_id = e2.follower_id
                 AND e1.follower_id < e1.followee_id
)
SELECT ROUND(m.mutual_pairs * 100.0 / (SELECT COUNT(*) FROM edges), 2) AS reciprocity_index
FROM   mutual m;
```
**Explanation:** Mutual pairs (each unordered, hence ÷ 2) over all directed edges gives the global reciprocity index.

**Alt1:**
```sql
SELECT ROUND(AVG(recip) * 100, 2) AS avg_reciprocity_index
FROM  (SELECT e.follower_id,
              CASE WHEN EXISTS (
                SELECT 1 FROM follows f2
                WHERE f2.follower_id = e.followee_id
                  AND f2.followee_id = e.follower_id
              ) THEN 1 ELSE 0 END AS recip
       FROM   follows e) t;
```
**Explanation:** Individual reciprocity is the fraction of each user's follows that are returned; the average is the network-level index.

---

## Q80: Friendship decay — no interaction in 90 days

**Query:**
```sql
-- MySQL 8+
WITH my_friends AS (
  SELECT user2_id AS friend_id FROM friendships WHERE user1_id = 42
  UNION
  SELECT user1_id FROM friendships WHERE user2_id = 42
),
last_interaction AS (
  SELECT f.friend_id,
         MAX(last_ts) AS last_ts
  FROM   my_friends f
  LEFT JOIN (SELECT user_id, created_at AS last_ts FROM posts
             UNION ALL
             SELECT user_id, created_at FROM comments
             UNION ALL
             SELECT sender_id, created_at FROM messages) acts
    ON acts.user_id = f.friend_id
  GROUP  BY f.friend_id
)
SELECT friend_id,
       COALESCE(last_ts, 'never') AS last_interaction,
       CASE WHEN last_ts < CURRENT_TIMESTAMP - INTERVAL 90 DAY
            OR  last_ts IS NULL THEN 'DECAYED' ELSE 'active' END AS status
FROM   last_interaction;
```
**Explanation:** Merged interaction data minus the last timestamp; items older than 90 days or absent are flagged DECAYED.

**Alt1:**
```sql
-- PostgreSQL: count decayed friendships network-wide
WITH last_seen AS (
  SELECT u.user_id, u.name, MAX(a.ts) AS last_ts
  FROM   users u
  LEFT JOIN (SELECT user_id, created_at AS ts FROM posts
             UNION ALL
             SELECT user_id, created_at FROM comments
             UNION ALL
             SELECT sender_id, created_at FROM messages) a
    ON a.user_id = u.user_id
  GROUP  BY u.user_id, u.name
)
SELECT COUNT(*) AS decayed_friendships,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM friendships), 2) AS pct_of_network
FROM   friendships f
JOIN   last_seen ls1 ON ls1.user_id = f.user1_id
JOIN   last_seen ls2 ON ls2.user_id = f.user2_id
WHERE  GREATEST(COALESCE(ls1.last_ts, '1970-01-01'), COALESCE(ls2.last_ts, '1970-01-01'))
       < NOW() - INTERVAL '90 days';
```
**Explanation:** A friendship "decays" when both endpoints were last active over 90 days ago.

---

## Q81: Every pair's common interests

**Query:**
```sql
-- MySQL 8+
SELECT i1.user_id AS user_a,
       i2.user_id AS user_b,
       COUNT(*)   AS common_interests
FROM   interests i1
JOIN   interests i2
  ON  i1.interest = i2.interest
 AND  i1.user_id < i2.user_id
GROUP  BY i1.user_id, i2.user_id
ORDER  BY common_interests DESC;
```
**Explanation:** Equi-join on the interest value and dedup via `<` reveals shared-interest pairs.

---

## Q82: Watch out for dedup — friendships stored once vs twice

**Query:**
```sql
-- PostgreSQL: case 1 — stored once (canonical, user1_id < user2_id)
SELECT COUNT(*) AS edges_once
FROM   friendships
WHERE  user1_id < user2_id;
```
**Explanation:** When the ETL guarantees canonical orientation, every row is a unique edge and you need no dedup.

**Alt1:**
```sql
-- PostgreSQL: case 2 — stored twice (both directions present)
WITH canonical AS (
  SELECT DISTINCT LEAST(user1_id, user2_id)  AS u1,
                  GREATEST(user1_id, user2_id) AS u2
  FROM   friendships
)
SELECT COUNT(*) AS edges_deduped
FROM   canonical;
```
**Explanation:** When both (A,B) and (B,A) rows exist, `DISTINCT LEAST/GREATEST` collapses them — use this count, not raw row count.

---

## Q83: Circle density — triangle count via self-join

**Query:**
```sql
SELECT COUNT(*) AS triangle_count
FROM   friendships f1
JOIN   friendships f2 ON f1.user1_id = f2.user2_id AND f1.user2_id = f2.user1_id
JOIN   friendships f3 ON f1.user1_id = f3.user1_id AND f1.user2_id = f3.user2_id
WHERE  f1.user1_id < f1.user2_id
  AND  f3.user2_id = f2.user1_id
  AND  f1.user2_id > f2.user2_id;
```
**Explanation:** Three joins verify all three edges of a triangle; ordering constraints select each triangle once.

**Alt1:**
```sql
-- PostgreSQL: cleaner 3-way inequality dedup
SELECT COUNT(*) AS triangle_count
FROM   friendships a
JOIN   friendships b ON a.user1_id = b.user2_id AND a.user2_id = b.user1_id
JOIN   friendships c ON a.user1_id = c.user2_id AND a.user2_id < c.user1_id
JOIN   friendships d ON b.user1_id = d.user1_id AND b.user2_id = d.user2_id
WHERE  a.user1_id < a.user2_id;
```
**Explanation:** Each triangle is enumerated exactly once via size-ordered vertices by combining join and inequality predicates.

---

## Q84: Count of closed triangles per user (local triangle closure)

**Query:**
```sql
-- MySQL 8+
WITH triples AS (
  SELECT f1.user1_id AS a, f1.user2_id AS b, f2.user1_id AS c
  FROM   friendships f1
  JOIN   friendships f2 ON f1.user2_id = f2.user1_id
  JOIN   friendships f3 ON f2.user2_id = f3.user1_id AND f3.user2_id = f1.user1_id
  WHERE  f1.user1_id = f1.user2_id
)
SELECT a AS user_id,
       COUNT(*) AS closed_triangles
FROM  (SELECT a FROM triples
       UNION ALL
       SELECT b FROM triples
       UNION ALL
       SELECT c FROM triples) verts
GROUP  BY a;
```
**Explanation:** List a set of triangles once, then unfold each into its three vertices, count per user.

---

## Q85: Overall network clustering coefficient

**Query:**
```sql
-- PostgreSQL
WITH edges AS (
  SELECT user1_id AS u, user2_id AS v FROM friendships
  UNION ALL
  SELECT user2_id, user1_id FROM friendships
),
triangles AS (
  SELECT COUNT(*) / 3 AS tri_count
  FROM   edges e1
  JOIN   edges e2 ON e1.v = e2.u
  JOIN   edges e3 ON e2.v = e3.u AND e3.v = e1.u
  WHERE  e1.u < e1.v AND e2.u < e2.v AND e3.u < e3.v
),
triples AS (
  SELECT COUNT(*) AS potential
  FROM   (SELECT u, v FROM edges GROUP BY u, v) e1
  JOIN   (SELECT u, v FROM edges GROUP BY u, v) e2 ON e1.v = e2.u
 )
SELECT ROUND((SELECT tri_count FROM triangles) * 3.0 /
             (SELECT potential FROM triples), 4) AS clustering_coefficient;
```
**Explanation:** Clustering coefficient = (3 × triangles) ÷ connected triples, a global measure of friend-of-friend closure.

**Alt1:**
```sql
-- MySQL 8+: per-user (local) coefficient instead
WITH edges AS (
  SELECT user1_id AS u, user2_id AS v FROM friendships
  UNION ALL
  SELECT user2_id, user1_id FROM friendships
),
deg AS (
  SELECT u, COUNT(v) AS degree FROM edges GROUP BY u
),
local_tris AS (
  SELECT e1.u,
         COUNT(DISTINCT e2.v) / 2 AS closed_pairs
  FROM   edges e1
  JOIN   edges e2 ON e1.v = e2.u
  JOIN   edges e3 ON e2.v = e3.u AND e3.v = e1.u
  WHERE  e1.u < e1.v AND e2.u < e2.v AND e3.u < e3.v
  GROUP  BY e1.u
)
SELECT d.u,
       ROUND(l.closed_pairs * 2.0 / NULLIF(d.degree * (d.degree - 1), 0), 4) AS local_cc
FROM   deg d
LEFT JOIN local_tris l ON d.u = l.u;
```
**Explanation:** Local coefficient = 2 × triangles at u ÷ degree(u) × (degree(u) − 1).

---

## Q86: Connected components in the friendship graph

**Query:**
```sql
-- PostgreSQL
WITH RECURSIVE comps AS (
  SELECT user1_id AS uid, user1_id AS component, ARRAY[user1_id] AS seen
  FROM   friendships
  WHERE  NOT EXISTS (SELECT 1 FROM friendships x
                     WHERE x.user2_id = friendships.user1_id
                       AND  x.user1_id < friendships.user1_id)
  UNION ALL
  SELECT f.user2_id, c.component, c.seen || f.user2_id
  FROM   friendships f
  JOIN   comps c ON f.user1_id = c.uid
  WHERE  NOT (f.user2_id = ANY(c.seen))
    AND  f.user2_id > c.uid
  UNION ALL
  SELECT f.user1_id, c.component, c.seen || f.user1_id
  FROM   friendships f
  JOIN   comps c ON f.user2_id = c.uid
  WHERE  NOT (f.user1_id = ANY(c.seen))
    AND  f.user1_id > c.uid
)
SELECT component, COUNT(*) AS component_size
FROM   comps
GROUP  BY component
ORDER  BY component_size DESC;
```
**Explanation:** Recursive walk visiting each undirected edge once; each disjoint grouping becomes a component.

---

## Q87: Bridge friendships — edges whose removal disconnects the graph

**Query:**
```sql
-- PostgreSQL (simplification: boundary edges in 2-node components)
WITH edge_list AS (
  SELECT user1_id AS u, user2_id AS v FROM friendships
  UNION ALL
  SELECT user2_id, user1_id FROM friendships
),
deg AS (
  SELECT u, COUNT(*) AS d FROM edge_list GROUP BY u
)
SELECT DISTINCT LEAST(u, v) AS u, GREATEST(u, v) AS v,
       'candidate bridge' AS note
FROM   edge_list e
JOIN   deg d1 ON d1.u = e.u
JOIN   deg d2 ON d2.u = e.v
WHERE  d1.d = 1 OR d2.d = 1;
```
**Explanation:** Edges with a degree-1 endpoint are guaranteed bridges — a pragmatic baseline for a very large map-reduced graph.

---

## Q88: PageRank-style influence score

**Query:**
```sql
-- PostgreSQL: iterative approximation via SQL
WITH RECURSIVE pr(iter, uid, score) AS (
  SELECT 0, user_id, 1.0 / (SELECT COUNT(*) FROM users)
  FROM   users
  UNION ALL
  SELECT pr.iter + 1,
         u.user_id,
         0.15 / (SELECT COUNT(*) FROM users)
         + 0.85 * (SELECT COALESCE(SUM(prev.score), 0)
                   FROM   follows f
                   JOIN   pr prev ON f.follower_id = prev.uid
                   WHERE  f.followee_id = u.user_id
                     AND  prev.iter = pr.iter
                   GROUP  BY f.followee_id)
  FROM   users u
  JOIN   pr ON pr.iter < 10
)
SELECT uid, score
FROM   (SELECT *, ROW_NUMBER() OVER (PARTITION BY uid ORDER BY iter DESC) AS rn
        FROM   pr) ranked
WHERE  rn = 1
ORDER  BY score DESC
LIMIT  10;
```
**Explanation:** Ten fixed-point iterations redistribute 85% of each user's score to their followers — an influence ranking baseline.

**Alt1:**
```sql
-- MySQL 8+: simpler two-pass follower-weight proxy
SELECT f.followee_id,
       COUNT(*)                                                                  AS followers,
       (SELECT ROUND(SUM(COALESCE((SELECT COUNT(*) FROM follows f2 WHERE f2.friend_id = u.user_id AND f2.friend_id <> 0), 0)), 2)
        FROM   follows f1
        JOIN   users u ON f1.followee_id = u.user_id
        WHERE  f1.follower_id = f.followee_id) AS followers_of_followers
FROM   follows f
GROUP  BY f.followee_id
ORDER  BY followers_of_followers DESC;
```
**Explanation:** Weighting by followers-of-followers approximates influence without matrix iterations.

---

## Q89: K-core decomposition

**Query:**
```sql
-- PostgreSQL: find users in the 5-core (each has ≥ 5 friends within the core)
WITH RECURSIVE kcore AS (
  SELECT user1_id AS u, user2_id AS v FROM friendships
  UNION ALL
  SELECT user2_id, user1_id FROM friendships
)
SELECT u, COUNT(*) AS in_core_degree
FROM   kcore
WHERE  u IN (
  SELECT degree.u
  FROM  (SELECT u, COUNT(*) AS deg FROM kcore GROUP BY u
         HAVING COUNT(*) >= 5) degree
)
GROUP  BY u
HAVING COUNT(*) >= 5
ORDER  BY in_core_degree DESC;
```
**Explanation:** Repeated pruning of vertices below degree 5 converges to the k-core; the final `HAVING` confirms membership.

---

## Q90: Degrees of separation from a seed user

**Query:**
```sql
-- PostgreSQL
WITH RECURSIVE separation AS (
  SELECT user2_id AS uid, 1 AS hop FROM friendships WHERE user1_id = 1
  UNION
  SELECT user1_id, 1 FROM friendships WHERE user2_id = 1
  UNION
  SELECT f.user2_id, s.hop + 1
  FROM   friendships f
  JOIN   separation s ON f.user1_id = s.uid
  WHERE  s.hop < 6
    AND  f.user2_id NOT IN (SELECT uid FROM separation)
)
SELECT uid,
       MIN(hop) AS degree_of_separation
FROM   separation
GROUP  BY uid
ORDER  BY degree_of_separation;
```
**Explanation:** BFS recursion assigns the shortest hop count to each user — six degrees of separation in SQL.

**Alt1:**
```sql
-- SQL Server: same BFS with TOP-per-level scan
WITH sep AS (
  SELECT user2_id AS uid, 1 AS hop
  FROM   friendships WHERE user1_id = 1
  UNION
  SELECT f.user2_id, s.hop + 1
  FROM   friendships f
  JOIN   sep s ON f.user1_id = s.uid
  WHERE  s.hop < 6
    AND  NOT EXISTS (SELECT 1 FROM sep x WHERE x.uid = f.user2_id)
)
SELECT uid, MIN(hop) AS separation
FROM   sep
GROUP  BY uid;
```
**Explanation:** `NOT EXISTS` guards against revisiting nodes in SQL Server's recursive CTE.

---

## Q91: Find all triangles (3-member cliques) explicitly

**Query:**
```sql
-- MySQL 8+
SELECT a.user1_id AS user_a,
       b.user1_id AS user_b,
       c.user1_id AS user_c
FROM   friendships a
JOIN   friendships b ON a.user2_id = b.user1_id
JOIN   friendships c ON b.user2_id = c.user1_id AND c.user2_id = a.user1_id
WHERE  a.user1_id < b.user1_id
  AND  b.user1_id < c.user1_id;
```
**Explanation:** The three join conditions prove the triangle; the size-order inequality deduplicates each triangle once.

---

## Q92: Common friends among all members of a specific group

**Query:**
```sql
SELECT f.user2_id AS common_friend
FROM   friendships f
WHERE  f.user1_id IN (10, 20, 30)
GROUP  BY f.user2_id
HAVING COUNT(DISTINCT f.user1_id) = 3;
```
**Explanation:** `HAVING = 3` means the friend is connected to all three group members — their mutual friend.

---

## Q93: Shortest path between two specific users (BFS)

**Query:**
```sql
-- PostgreSQL
WITH RECURSIVE bfs AS (
  SELECT user2_id AS node,
         ARRAY[101, user2_id] AS path,
         1 AS depth
  FROM   friendships WHERE user1_id = 101
  UNION
  SELECT user1_id, ARRAY[101, user1_id], 1 FROM friendships WHERE user2_id = 101
  UNION
  SELECT f.user2_id, b.path || f.user2_id, b.depth + 1
  FROM   friendships f
  JOIN   bfs b ON f.user1_id = b.node
  WHERE  b.depth < 6
    AND  f.user2_id <> ALL(b.path)
  UNION
  SELECT f.user1_id, b.path || f.user1_id, b.depth + 1
  FROM   friendships f
  JOIN   bfs b ON f.user2_id = b.node
  WHERE  b.depth < 6
    AND  f.user1_id <> ALL(b.path)
)
SELECT path, depth
FROM   bfs
WHERE  node = 202
ORDER  BY depth
LIMIT  1;
```
**Explanation:** BFS records the full path array; the first hit at the target node with minimum depth is the shortest route.

---

## Q94: Graph diameter — longest shortest path

**Query:**
```sql
-- PostgreSQL: approximate diameter from degree extremes
WITH all_pairs AS (
  SELECT a.user_id AS u, b.user_id AS v
  FROM   users a
  CROSS JOIN users b
  WHERE  a.user_id < b.user_id
),
reach AS (
  SELECT a.u, a.v, MIN(h.hop) AS dist
  FROM   all_pairs a
  JOIN  (SELECT u, v, MIN(hop) AS hop
         FROM ( -- pair-wise BFS is engine-dependent; here we memoize edge distance
                SELECT f1.user1_id AS u, f2.user2_id AS v, 2 AS hop
                FROM   friendships f1
                JOIN   friendships f2 ON f1.user2_id = f2.user1_id
                UNION ALL
                SELECT user1_id, user2_id, 1 FROM friendships
              ) dists
         GROUP  BY u, v) h
    ON  a.u = h.u AND a.v = h.v
  GROUP  BY a.u, a.v
)
SELECT MAX(dist) AS approximate_diameter
FROM   reach;
```
**Explanation:** This bounds the diameter using 1- and 2-hop edge distances; a full diameter needs complete BFS on every node.

**Alt1:**
```sql
-- MySQL 8+: diameter via BFS from the single most-connected node
WITH RECURSIVE bfs AS (
  SELECT user2_id AS node, 1 AS hop FROM friendships WHERE user1_id = (SELECT user1_id FROM friendships GROUP BY user1_id ORDER BY COUNT(*) DESC LIMIT 1)
  UNION
  SELECT f.user2_id, b.hop + 1
  FROM   friendships f
  JOIN   bfs b ON f.user1_id = b.node
  WHERE  b.hop < 10 AND f.user2_id NOT IN (SELECT node FROM bfs)
)
SELECT MAX(hop) AS approx_diameter
FROM   bfs;
```
**Explanation:** Eccentricity of the hub node bounds the true diameter from below — a fast approximation.

---

## Q95: Betweenness centrality approximation

**Query:**
```sql
-- PostgreSQL: boundary-based proxy
WITH inbound AS (
  SELECT f.followee_id, COUNT(DISTINCT f.follower_id) AS reached
  FROM   follows f
  GROUP  BY f.followee_id
)
SELECT u.user_id,
       u.name,
       COALESCE(i.reached, 0) AS nodes_that_reach_you,
       ROUND(NROW(COALESCE(i.reached,0)) / n, 4) AS cascade_share
FROM   users u
LEFT JOIN inbound i ON i.followee_id = u.user_id
ORDER  BY cascade_share DESC
LIMIT  10;
```
**Explanation:** Under a cascade model the fraction of the network that can reach a user approximates information-flow centrality.

---

## Q96: Community detection via label propagation (one pass)

**Query:**
```sql
-- PostgreSQL
WITH edges AS (
  SELECT user1_id AS u, user2_id AS v FROM friendships
  UNION ALL
  SELECT user2_id, user1_id FROM friendships
),
labels AS (
  SELECT u,
         MIN(v) AS label   -- adopt the smallest neighbor label this pass
  FROM   edges
  GROUP  BY u
)
SELECT label AS community, COUNT(*) AS members
FROM   labels
GROUP  BY label
ORDER  BY members DESC;
```
**Explanation:** In a first label-propagation pass each node claims the minimum neighbor ID; frequent labels surface dense communities.

---

## Q97: Viral coefficient (invitations ÷ new users)

**Query:**
```sql
-- MySQL 8+
SELECT MONTH(i.created_at) AS month,
       COUNT(DISTINCT i.inviter_id)                      AS invite_senders,
       COUNT(DISTINCT i.invitee_id)                      AS new_users,
       ROUND(COUNT(DISTINCT i.invitee_id)
             / NULLIF(COUNT(DISTINCT i.inviter_id), 0), 2) AS viral_coefficient
FROM   invites i
WHERE  i.created_at >= CURRENT_DATE - INTERVAL 6 MONTH
GROUP  BY MONTH(i.created_at)
ORDER  BY MONTH(i.created_at);
```
**Explanation:** New signups divided by invite senders estimates how many new users each inviter brings — K-factor.

---

## Q98: Graph reachability — can user A reach user B?

**Query:**
```sql
-- PostgreSQL
WITH RECURSIVE reach AS (
  SELECT user1_id AS src, user2_id AS dst FROM friendships
  WHERE  user1_id = 501
  UNION
  SELECT r.src, f.user2_id
  FROM   reach r
  JOIN   friendships f ON r.dst = f.user1_id
)
SELECT CASE WHEN EXISTS (SELECT 1 FROM reach WHERE dst = 502)
            THEN 'REACHABLE'
            ELSE 'NOT REACHABLE'
       END AS result;
```
**Explanation:** Recursion floods out from 501 through every edge; existence of 502 among discovered nodes answers reachability.

---

## Q99: Network resilience — simulate node removal

**Query:**
```sql
-- PostgreSQL
WITH after_removal AS (
  SELECT u.user_id,
         COUNT(f.*) AS remaining_degree
  FROM   users u
  LEFT JOIN friendships f
    ON  f.user1_id = u.user_id AND f.user2_id <> 999
     OR f.user2_id = u.user_id AND f.user1_id <> 999
  WHERE  u.user_id <> 999
  GROUP  BY u.user_id
)
SELECT COUNT(*) FILTER (WHERE remaining_degree = 0) AS newly_isolated,
       COUNT(*) FILTER (WHERE remaining_degree < 3) AS fragile_users,
       ROUND(AVG(remaining_degree), 2)              AS avg_post_removal_degree
FROM   after_removal;
```
**Explanation:** Removing user 999 (edges to them excluded) and rechecking degrees measures network fragility to deplatforming.

---

## Q100: CAPSTONE — recursive depth-3 network exploration with aggregation

**Query:**
```sql
-- PostgreSQL
WITH RECURSIVE network_levels AS (
  SELECT user2_id AS uid,
         user2_id AS source_of_disc,
         1 AS depth,
         ARRAY[user1_id, user2_id] AS path
  FROM   friendships
  WHERE  user1_id = 77
  UNION
  SELECT user1_id, user1_id, 1, ARRAY[user2_id, user1_id]
  FROM   friendships
  WHERE  user2_id = 77
UNION
  SELECT f.user2_id, n.source_of_disc, n.depth + 1, n.path || f.user2_id
  FROM   friendships f
  JOIN   network_levels n ON f.user1_id = n.uid
  WHERE  n.depth < 3
    AND  f.user2_id <> ALL(n.path)
  UNION
  SELECT f.user1_id, n.source_of_disc, n.depth + 1, n.path || f.user1_id
  FROM   friendships f
  JOIN   network_levels n ON f.user2_id = n.uid
  WHERE  n.depth < 3
    AND  f.user1_id <> ALL(n.path)
),
reachable AS (
  SELECT DISTINCT uid, MIN(depth) AS min_depth
  FROM   network_levels
  WHERE  uid <> 77
  GROUP  BY uid
),
user_stats AS (
  SELECT r.uid,
         r.min_depth,
         COUNT(DISTINCT p.post_id)              AS posts,
         COUNT(DISTINCT CASE WHEN l.user_id IS NOT NULL THEN p.post_id END) AS liked_posts,
         COUNT(DISTINCT CASE WHEN c.comment_id IS NOT NULL THEN p.post_id END) AS commented_posts,
         COALESCE(SUM(CASE WHEN m.sender_id IS NOT NULL THEN 1 END), 0) AS messages_authored
  FROM   reachable r
  LEFT JOIN posts p ON p.user_id = r.uid
  LEFT JOIN likes l ON l.post_id = p.post_id
  LEFT JOIN comments c ON c.post_id = p.post_id
  LEFT JOIN messages m ON m.sender_id = r.uid
  GROUP  BY r.uid, r.min_depth
)
SELECT s.min_depth AS hop,
       COUNT(*)                 AS users_at_hop,
       SUM(s.posts)             AS posts_at_hop,
       ROUND(AVG(s.posts), 2)   AS avg_posts_per_user,
       SUM(CASE WHEN s.posts > 0 THEN 1 ELSE 0 END)        AS active_authors,
       SUM(CASE WHEN s.posts = 0 THEN 1 ELSE 0 END)        AS dormant_users,
       SUM(messages_authored) AS total_direct_messages
FROM   user_stats s
GROUP  BY s.min_depth
ORDER  BY s.min_depth;
```
**Explanation:** The BFS CTE enumerates the full 3-hop neighborhood of user 77 with cycle protection; the final stage buckets users by hop and rolls up post, like, comment, and message activity per level — a complete "network sphere" report.
