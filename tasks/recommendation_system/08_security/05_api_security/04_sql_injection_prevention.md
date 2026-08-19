# SQL Injection Prevention

## 1. Overview

SQL injection remains one of the most dangerous vulnerabilities in web applications.
For recommendation systems that store user data, interaction history, and model configurations
in databases, SQL injection could lead to data theft, data corruption, or complete system
compromise. This document covers parameterized queries, ORM usage, stored procedures,
input sanitization, database permission least privilege, and SQL injection testing.

### 1.1 SQL Injection Impact on Recommendation Systems

| Impact | Description | Severity |
|---|---|---|
| Data theft | User data, interaction history exposed | Critical |
| Data manipulation | Corrupted features, recommendations | Critical |
| Authentication bypass | Access admin functions | Critical |
| Data deletion | Loss of training data, user profiles | Critical |
| Privilege escalation | Elevate to database admin | Critical |
| Lateral movement | Access other systems via database | High |

---

## 2. Parameterized Queries

### 2.1 What are Parameterized Queries?

Parameterized queries separate SQL structure from data, preventing injection.

```
# VULNERABLE (string concatenation):
query = f"SELECT * FROM users WHERE user_id = '{user_id}'"
# Attacker can inject: ' OR '1'='1

# SAFE (parameterized):
query = "SELECT * FROM users WHERE user_id = %s"
cursor.execute(query, (user_id,))
# user_id is treated as data, never as SQL
```

### 2.2 Parameterized Query Examples

**Python (psycopg2 - PostgreSQL):**

```python
# SAFE
cursor.execute(
    "SELECT * FROM recommendations WHERE user_id = %s AND category = %s",
    (user_id, category)
)

# VULNERABLE (never do this)
cursor.execute(f"SELECT * FROM recommendations WHERE user_id = '{user_id}'")
```

**Python (SQLAlchemy ORM):**

```python
# SAFE (ORM automatically parameterizes)
session.query(Recommendation).filter(
    Recommendation.user_id == user_id,
    Recommendation.category == category
).all()
```

**Java (JDBC):**

```java
// SAFE
PreparedStatement stmt = conn.prepareStatement(
    "SELECT * FROM recommendations WHERE user_id = ? AND category = ?"
);
stmt.setString(1, userId);
stmt.setString(2, category);
ResultSet rs = stmt.executeQuery();
```

### 2.3 Parameterized Query Rules

| Rule | Description | Priority |
|---|---|---|
| Always parameterize | Never concatenate user input into SQL | Critical |
| Use prepared statements | Pre-compile SQL structure | Critical |
| Validate before parameterize | Check types and ranges first | High |
| Use correct parameter marker | `%s` for PostgreSQL, `?` for MySQL/JDBC | Medium |
| Never parameterize identifiers | Table/column names cannot be parameterized | High |

---

## 3. ORM Usage

### 3.1 ORM as SQL Injection Prevention

ORMs (Object-Relational Mappers) automatically generate parameterized queries.

| ORM | Language | Safety Level |
|---|---|---|
| SQLAlchemy | Python | High (with proper usage) |
| Django ORM | Python | High |
| Hibernate | Java | High |
| GORM | Go | High |
| ActiveRecord | Ruby | High |
| TypeORM | TypeScript | High |

### 3.2 ORM Safety Considerations

| Risk | Description | Prevention |
|---|---|---|
| Raw SQL in ORM | Using raw SQL methods | Avoid raw SQL or parameterize |
| Dynamic column names | User input in column names | Validate against schema |
| LIKE clause injection | Wildcard injection in LIKE | Escape LIKE metacharacters |
| ORDER BY injection | User input in ORDER BY | Validate against allowed columns |
| HAVING injection | User input in HAVING clause | Parameterize HAVING conditions |

### 3.3 ORM Best Practices

```
✅ DO:
- Use ORM query builder for all queries
- Validate inputs before passing to ORM
- Use ORM's built-in escaping functions
- Review generated SQL for complex queries

❌ DON'T:
- Use raw SQL with string formatting
- Pass user input directly to ORM column names
- Use ORM's raw() function without parameterization
- Trust ORM to handle all edge cases automatically
```

---

## 4. Stored Procedures

### 4.1 Stored Procedure Security

Stored procedures can provide an additional layer of SQL injection prevention:

```sql
-- SAFE stored procedure
CREATE PROCEDURE get_recommendations(
    p_user_id VARCHAR(50),
    p_count INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM recommendations
    WHERE user_id = p_user_id
    ORDER BY score DESC
    LIMIT p_count;
END;
$$;

-- Call with parameters (safe from injection)
EXECUTE get_recommendations('usr_a1b2c3', 10);
```

### 4.2 Stored Procedure Limitations

| Limitation | Description |
|---|---|
| SQL injection within procedure | Procedures can still have internal injection |
| Maintenance overhead | Procedures require separate management |
| Portability | Database-specific syntax |
| Testing complexity | Harder to unit test |

---

## 5. Input Sanitization

### 5.1 Sanitization Functions

| Input Type | Sanitization | Function |
|---|---|---|
| String | Remove SQL special characters | `re.sub(r"[;'"\\]", "", input)` |
| Integer | Parse as integer, reject non-numeric | `int(input)` with try/except |
| Float | Parse as float, reject non-numeric | `float(input)` with try/except |
| Email | Validate email format | Regex validation |
| URL | Validate URL format | URL parsing library |
| Date | Validate date format | Date parsing library |

### 5.2 LIKE Clause Injection

```sql
-- VULNERABLE
SELECT * FROM items WHERE name LIKE '%user_input%'
-- Attacker input: %' OR '1'='1

-- SAFE (escape LIKE metacharacters)
-- Escape %, _, \ in user input before LIKE clause
escaped_input = input.replace('%', '\\%').replace('_', '\\_').replace('\\', '\\\\')
cursor.execute("SELECT * FROM items WHERE name LIKE %s", (f'%{escaped_input}%',))
```

### 5.3 ORDER BY Injection

```python
# VULNERABLE
cursor.execute(f"SELECT * FROM items ORDER BY {user_input}")

# SAFE (validate against allowed columns)
allowed_columns = ['name', 'score', 'created_at']
if user_input in allowed_columns:
    cursor.execute(f"SELECT * FROM items ORDER BY {user_input}")
else:
    raise ValueError("Invalid sort column")
```

---

## 6. Database Permission Least Privilege

### 6.1 Permission Model

| Role | Permissions | Use Case |
|---|---|---|
| `readonly` | SELECT only | Analytics, reporting |
| `app_user` | SELECT, INSERT, UPDATE (specific tables) | Application operations |
| `app_admin` | SELECT, INSERT, UPDATE, DELETE (specific tables) | Admin operations |
| `migration` | DDL operations (CREATE, ALTER, DROP) | Schema migrations |
| `backup` | SELECT with LOCK | Backup operations |
| `superuser` | All permissions | Emergency only |

### 6.2 Permission Restrictions

```
Application Database User Permissions:
├── recommendation_db.app_user
│   ├── SELECT on: recommendations, user_features, item_features
│   ├── INSERT on: user_interactions, interaction_events
│   ├── UPDATE on: user_preferences
│   └── DENIED: DROP, ALTER, CREATE, DELETE on user tables
│
├── recommendation_db.readonly
│   ├── SELECT on: all tables
│   └── DENIED: INSERT, UPDATE, DELETE, DDL
│
└── recommendation_db.admin
    ├── SELECT, INSERT, UPDATE, DELETE on: all tables
    └── DENIED: DROP DATABASE, CREATE USER
```

### 6.3 Permission Monitoring

- **Query logging**: Log all queries with user context
- **Permission audits**: Quarterly review of database permissions
- **Anomaly detection**: Alert on unusual query patterns
- **Privilege escalation detection**: Alert on permission changes

---

## 7. SQL Injection Testing

### 7.1 Testing Methods

| Method | Tool | Coverage |
|---|---|---|
| Automated scanning | OWASP ZAP, SQLMap | High |
| Manual penetration testing | Burp Suite | High |
| Code review | Manual review | Very high |
| Fuzz testing | Custom fuzzers | High |
| Unit tests | Custom test cases | Medium |

### 7.2 Common SQL Injection Payloads

| Payload | Type | Detection |
|---|---|---|
| `' OR '1'='1` | Tautology | Always false condition test |
| `'; DROP TABLE users; --` | Statement termination | Query structure validation |
| `' UNION SELECT * FROM users --` | UNION injection | Response validation |
| `1; EXEC xp_cmdshell('dir')` | Command execution | Database permission check |
| `' AND SLEEP(5) --` | Time-based blind | Response time monitoring |
| `' AND (SELECT COUNT(*) FROM users) > 0 --` | Boolean-based blind | Response comparison |

### 7.3 SQL Injection Test Automation

```
CI/CD Pipeline:
├── Static analysis: CodeQL, Semgrep for SQL injection patterns
├── Dynamic testing: OWASP ZAP baseline scan
├── Penetration test: Quarterly manual testing
├── Fuzz testing: Continuous fuzzing of database queries
└── Dependency scanning: Check database driver vulnerabilities
```

### 7.4 SQL Injection Response

If SQL injection is detected:

1. **Immediate**: Block the attack, log the attempt
2. **Short-term**: Patch the vulnerability, deploy fix
3. **Medium-term**: Audit all database queries for similar patterns
4. **Long-term**: Implement automated SQL injection prevention testing
