### step 1 — create the database as `postgres` superuser

```bash
sudo -u postgres createdb -O learner pythondb
```

* `-O learner` → makes your `learner` role the owner.
* check with:

```bash
sudo -u postgres psql -c "\l"
```

```
 List of databases
   Name    |  Owner   | Encoding | Locale Provider |   Collate   |    Ctype    | ICU Locale | ICU Rules |   Access privi
leges   
-----------+----------+----------+-----------------+-------------+-------------+------------+-----------+-----------------------
 learndb   | learner  | UTF8     | libc            | en_US.UTF-8 | en_US.UTF-8 |            |           | 
 postgres  | postgres | UTF8     | libc            | en_US.UTF-8 | en_US.UTF-8 |            |           | 
 pythondb  | learner  | UTF8     | libc            | en_US.UTF-8 | en_US.UTF-8 |            |           | 
 scratchdb | postgres | UTF8     | libc            | en_US.UTF-8 | en_US.UTF-8 |            |           | 
 template0 | postgres | UTF8     | libc            | en_US.UTF-8 | en_US.UTF-8 |            |           | =c/postgres          +
           |          |          |                 |             |             |            |           | postgres=CTc/postgres
 template1 | postgres | UTF8     | libc            | en_US.UTF-8 | en_US.UTF-8 |            |           | =c/postgres          +
           |          |          |                 |             |             |            |           | postgres=CTc/postgres
```

you should see `pythondb` owned by `learner`.

### step 2 — retry connection

activate your venv, then run your script again:

```bash
python phases/phase2/06_low_level/test1.py
```

---

## 📝 optional checks if still failing

1. **role exists?**

   ```bash
   sudo -u postgres psql -c "\du"
   ```

   if `learner` isn’t listed, create it:

   ```sql
   CREATE ROLE learner LOGIN PASSWORD 'mypassword';
   ```

2. **can connect manually?**

   ```bash
   psql -U learner -d pythondb -h localhost
   ```

   if that works, psycopg should also work.
