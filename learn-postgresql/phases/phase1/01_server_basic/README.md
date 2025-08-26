## 📚 concepts to lock in

### 1. **roles vs users**

* postgres has *roles* → they can act as **users** (login) or **groups** (privilege containers).
* `LOGIN` keyword = can log in like a user.
* you can grant one role to another (like unix groups).

### 2. **databases vs schemas**

* **cluster** → one postgres server instance (runs on port, has a data dir).
* **database** → separate logical namespace inside a cluster.
* **schema** → namespace inside a database (like folders in a filesystem).
* default schema = `public`.
* cross-database queries are *not supported* (unlike mysql’s `db.table`).

### 3. **encoding & locales**

* best practice: always initdb with `UTF8`.
* `SHOW SERVER_ENCODING;` → should be UTF8.
* collation/ctype affects sorting & case comparison (set at init, e.g., `en_US.UTF-8`).

### 4. **time zones**

* server default → `SHOW TIMEZONE;`.
* recommended: `UTC` on server; app handles local conversions.
* each session can `SET TIME ZONE 'Asia/Kolkata';` etc.

### 5. **superuser vs normal roles**

* `postgres` role created at install → superuser.
* superusers bypass permission checks → don’t use for apps.
* apps should use **least privilege** (just enough perms).

### 6. **service lifecycle (ubuntu)**

* start/stop/status:

```bash
sudo systemctl status postgresql
sudo systemctl start postgresql
sudo systemctl stop postgresql
```

### 7. **data directory & logs**

* find data dir:

```bash
sudo -u postgres psql -c "SHOW data_directory;"
```

* logs usually in `/var/log/postgresql/` (on ubuntu).
* you can also `SHOW log_directory;` for where logs are written relative to data dir.

---

## 🧪 test exercise

### step 1 — create a non-superuser role

```bash
sudo -u postgres psql
```

inside `psql`:

```sql
CREATE ROLE learner LOGIN PASSWORD 'mypassword';
```

* `LOGIN` → makes it a user.
* *verify it’s not a superuser*:

```sql
\du
```

you should see `learner` with limited attributes (no Superuser).

### step 2 — create a database owned by this role

still inside `psql`:

```sql
CREATE DATABASE learndb OWNER learner ENCODING 'UTF8' TEMPLATE template0;
```

* `TEMPLATE template0` ensures fresh UTF-8 database.
* check:

```sql
\l
```

you should see `learndb` owned by `learner`.

### step 3 — connect as that role

exit (`\q`), then:

```bash
psql -U learner -d learndb -h localhost
```

enter password. you should see prompt:

```
learndb=>
```

### step 4 — schema awareness test

inside `learndb`:

```sql
SHOW search_path;
```

→ should display `"$user", public` (default search path).

### step 5 — timezone check

```sql
SHOW timezone;
```

→ default likely `UTC` or system timezone.

Now, change the timezone for this session only.


```sql
SET TIME ZONE 'Asia/Kolkata';

-- Verify the change.
SHOW timezone;
```

### Step 6 - Find the Data Directory
From your regular terminal (not psql), run the following command.

```sql
sudo -u postgres psql -c "SHOW data_directory;"
```
Explanation: This command is a powerful shortcut. It connects to the database as the postgres user, runs the SQL command SHOW data_directory;, and then exits. The output will give you the full path to your database cluster's data directory, typically something like /var/lib/postgresql/16/main.

Locate the Log Files
```sql
ls -l /var/log/postgresql/
```