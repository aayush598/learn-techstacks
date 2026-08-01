# Client-Server Architecture and Database Users

> **TL;DR**: A DBMS is deployed as a client-server system — one shared server process(es) owns the data and serves many clients over a protocol — because sharing, security, and consistent state demand a central authority, and the database is used by distinct roles (naive users to DBAs) with matching privileges.

## 1. Why Does This Exist?
A single-user, single-machine database doesn't need an architecture — the app and the data live together. The client-server model exists because databases are *shared resources*: many apps, many humans, many machines must read and write one consistent dataset concurrently. To make that possible, the data must have **one authority** (the server) that (a) owns storage, (b) serializes concurrent access, (c) enforces security centrally, and (d) survives clients coming and going. The server is the only place where ACID, locks, and the catalog can be enforced coherently. The *roles* exist because not everyone touching the database should have the same power — a naive user must not drop a table, and only the DBA should touch the physical layer.

## 2. How Does It Work?
In the classic **2-tier client-server** model, the client (application, tool, driver) connects to a DBMS server over a wire protocol (PostgreSQL protocol, MySQL protocol, ODBC/JDBC). The server authenticates (user+password, TLS), the client sends SQL, the server parses/optimizes/executes and streams results back. In **3-tier**, a middle tier (application server / web server) sits between browser and DB — clients talk to the app, the app (with a shared service account) talks to the DB. The roles layer maps users to privileges: naive users (through forms/views), application programmers (write SQL), sophisticated users (ad-hoc queries), specialized users (analytics/databases/BI), system analysts (design schemas), and DBAs (administer everything).

## 3. When Is It Used?
- **Client-server / 2-tier**: desktop tools (pgAdmin, DBeaver, BI tools), thick clients, single-service apps that connect straight to the DB.
- **3-tier**: essentially every web application — browsers → API server → database; the API server holds the DB credentials; users never connect directly.
- **Role separation**: banks give tellers (naive users) forms over views; analysts run ad-hoc SQL (sophisticated users); data scientists use specialized tools (specialized users); DBAs tune and secure.
- **Embedded (no server)**: SQLite in mobile/desktop — the "server" is in-process; used when sharing isn't needed.
- **N-tier / microservices**: many services, each with its own DB or shared DB via views — the architectural questions here are exactly the client-server trade-offs.

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: terminal-mainframe (one dumb terminal per user on a big host).** Historically correct (IMS era), but rejected as mainframes cost more and clients became smart. The network+PC revolution moved computation to clients, while the DB stayed server-side — 2-tier emerged.
- **Alternative: file-server architecture (each client reads the shared data file directly).** Rejected: no central authority → lost updates, no consistent locking, the whole file is shared raw; client crashes corrupt shared state. The DBMS must be the only writer, so a server is necessary.
- **Alternative: peer-to-peer (each node equal, no server).** Rejected for classic DBMSs: ACID and consistent catalog need a coordinator; P2P survives in distributed systems (CouchDB, IPFS) but with weaker consistency.
- **Why 3-tier over 2-tier for the web?** The browser cannot hold DB credentials or enforce business rules; the application server centralizes logic, pooling, caching, and protection. 3-tier won because security + scalability demand a trusted middle layer.

## 5. Intuition
A client-server database is like a **central bank vs street cash-in-hand**. The bank (server) is the single place money is minted, recorded, and secured; branches and ATMs (clients) only *ask* the bank, never touch the vault themselves. If every ATM physically held the vault (file-server), two ATMs could dispense the same note (lost update) and a robber could empty the whole system. The roles are the bank's tiers of authority: customers (naive users) use ATMs and forms; tellers (app programmers) move money with approved procedures; auditors (sophisticated users) run reports; the chief security officer (DBA) alone can mint money, lock vaults, and hand out keys.

## 6. Real-World Analogy
A **hospital's record system** again, but for architecture: the central medical-records server (client-server) holds every patient record; nurses' stations (thin clients) read/write through the hospital app; doctors (3-tier) reach it via the web portal; the health department (ad-hoc user) runs population queries; the IT administrator (DBA) controls backups, access, and uptime. If each nurse's station kept its own copy of records (file-server), patient data would diverge and two stations could prescribe conflicting medication. Central authority + role-based access is the only design that keeps records consistent, current, and secure — exactly why DBMS client-server exists.

## 7. Formal Definition
- **Client-server DBMS**: the database system is split into a *server* (or server processes) that owns the data, catalog, and transaction state, and *clients* that request services (SQL execution) over a network protocol. (Elmasri & Navathe Ch. 2: centralized, 2-tier, 3-tier architectures.)
- **2-tier**: client ↔ DB server directly.
- **3-tier**: presentation client ↔ application server ↔ database server.
- **DBMS user categories** (Elmasri & Navathe Ch. 1): (1) **naive / parametric users** — use canned programs/forms; (2) **application programmers** — write the canned programs; (3) **sophisticated users** — ad-hoc queries (SQL, tools); (4) **specialized users** — specialized applications (CAD, AI, analytics); (5) **system analysts** — requirements & schema design; (6) **database administrators (DBAs)** — manage schema, security, performance, backups.

## 8. Example
An online bookstore:
- **2-tier tools**: an analyst connects with psql/DBeaver to `SELECT count(*) FROM orders GROUP BY status;` (sophisticated user).
- **3-tier web**: browser → Node/Python API (application server) → Postgres. Users never touch SQL; the API runs parameterized `SELECT/INSERT` on their behalf (naive users, 3-tier).
- **Roles in action**: the bookstore's DBA creates roles — `web_app` (CRUD on orders/inventory), `analytics` (SELECT on warehouse), `hr_app` (personnel tables), `migrator` (DDL only in maintenance windows) — and grants via DCL.
- **Failure handled**: 100 customers checkout at once; the Postgres server serializes via row locks/MVCC, the connection pool (application tier) caps concurrency, and the DBA monitors slow queries.

## 9. Internal Working
1. Client opens a TCP connection to the server's listening port (5432 Postgres, 3306 MySQL), authenticates (MD5/SCRAM, TLS optional).
2. A server backend process/thread is dedicated per connection (Postgres: one backend process per session; MySQL: thread per connection; pooled by connection pools).
3. Client sends SQL (or prepared statements); server parses → catalog checks → optimize → execute → returns result sets; for writes: transaction manager (locks + WAL).
4. **3-tier**: browser issues HTTP to the API server; the API server (holding DB credentials in config/secrets) executes SQL with its service account; results serialized as JSON to the browser. Credentials never reach the browser.
5. **Connection pooling**: the app tier keeps a few warm DB connections to amortize auth + backend spawn cost; the DB sees bounded concurrency even under traffic spikes.
6. **Roles/priviliges**: authorization manager checks the *role* on the session against catalog grants per statement.

## 10. Time Complexity
- **Network round-trip per query**: sub-ms to ms (LAN); dominated by RTT, not CPU — hence batching (prepared statements, multi-row inserts) and pooling.
- **Server throughput**: scales with cores; one backend per connection → many idle backends waste RAM (thousands of connections → memory pressure) — connection pools bound it.
- **Auth**: O(1) per connection (plus TLS handshake, ~1 RTT).
- **Query execution**: as before — index O(log n), scan O(n), joins O(n+m) to O(n·m) — the architecture adds network overhead only.

## 11. Advantages
- **Central authority**: one owner of data → consistent state, one catalog, coherent ACID.
- **Security**: credentials and privileges enforced server-side; users never touch files or the engine.
- **Scalability of clients**: thousands of clients can attach; connection pooling multiplexes.
- **Backup/recovery**: happens server-side once, benefiting all clients.
- **3-tier benefits**: browser-safe (no DB creds), business logic centralized, horizontal scaling of the app tier, caching layers.
- **Role clarity**: least privilege expressible per user category; audit trails.

## 12. Disadvantages
- **Single point of failure**: a down server is down for everyone → needs HA (replicas, failover) engineering.
- **Network overhead**: RTT per query; chatty apps suffer → batching/prepared statements needed.
- **Connection cost**: each connection spawns a backend/thread (Postgres RAM per backend ~MBs) → pooling is mandatory at scale.
- **Concurrency bottleneck**: the server serializes writes; hot rows become contention points (lock contention, hot spot).
- **3-tier complexity**: extra hop, extra layer to deploy/monitor; latency and failure modes multiplied.

## 13. Interview Questions
1. **Q: What is client-server architecture in DBMS?** A: One server (process group) owns the data, catalog, and transaction state; clients connect over a protocol and send SQL. Centralizes storage, security, and concurrency so many clients can share one consistent database.
2. **Q: Why is a DBMS server necessary at all?** A: Because a shared database needs a single authority to enforce ACID, locking, constraints, and privileges. If clients accessed the data files directly (file-server), you'd get lost updates, no consistent locking, and no centralized security.
3. **Q: What is the difference between 2-tier and 3-tier?** A: 2-tier: client talks directly to the DB (tools, thick clients). 3-tier: presentation client → application server → database. The app server holds credentials, business logic, pooling, caching, and protection; the DB never sees raw clients.
4. **Q: When would you use 2-tier vs 3-tier?** A: 2-tier for internal tools and analytics (psql, DBeaver, BI) where users are trusted and credentialed. 3-tier for web/mobile apps where the browser must never hold DB credentials and business rules must be enforced centrally.
5. **Q: Why did file-server architecture fail?** A: Each client read/wrote the shared data file directly — no central authority: concurrent writes lost data, locking was whole-file, client crashes corrupted shared state, security was per-file not per-record. A DBMS server exists precisely to prevent this.
6. **Q (tricky): In 3-tier, who owns the DB credentials?** A: The application server (a service account). The browser/app UI never sees database credentials — that's the security boundary of 3-tier. The app server may have multiple service accounts per permission level.
7. **Q: What is connection pooling and why does it exist?** A: Reusing a fixed set of live DB connections across many client requests, because each connection costs RAM (a backend/thread) and RTT (auth handshake). Pools bound server load and cut latency; pools are mandatory at web scale.
8. **Q (production): Postgres is one process per connection. What breaks with 5,000 idle connections?** A: Memory — each backend uses MBs of RAM, so idle connections exhaust RAM and starve work. Fixes: connection pooling (pgbouncer), smaller pools, or moving state to the app tier. A classic production incident question.
9. **Q: Name the categories of database users.** A: Naive/parametric (forms), application programmers (write the apps), sophisticated (ad-hoc SQL), specialized (analytics/BI tools), system analysts (design schemas), and DBAs (administer). Each needs different privileges — that's why roles exist.
10. **Q: What does a DBA do?** A: Owns schema design and migrations, creates roles and grants (DCL), manages storage/indexes/partitions, monitors performance and tunes, handles backups/recovery, and ensures security/compliance.
11. **Q (scenario): A bank teller (naive user) must see account balances but never modify them. Design the access.** A: Create a role `teller` with `SELECT` on a *view* exposing only allowed columns, and route the teller through a form/app — naive users shouldn't run raw SQL at all; views + grants implement it.
12. **Q: What is a sophisticated user?** A: Someone who runs ad-hoc SQL/queries directly (analysts, researchers) — they write their own queries against the schema but shouldn't have DDL or DCL.
13. **Q: What is a specialized user?** A: A user of specialized applications that sit on the DB — CAD, geographic (GIS), data-science, or analytics tools. They don't write raw SQL; their specialized app does.
14. **Q (tricky): In a microservices setup, is the DB still client-server?** A: Yes — each service is a *client* of the database server; the topology adds many clients (services) plus often a shared or per-service database. The server-side authority and pooling concerns remain — plus new ones (which service owns which tables).
15. **Q: What is a thin client vs thick client?** A: Thin client: does almost no work, just displays server results (browser, terminal). Thick/fat client: runs logic locally and uses the DB directly (desktop apps, BI tools). 3-tier usually pairs thin clients with an app server.
16. **Q (production): Why does a web app need an app server between browser and DB?** A: (1) Security — the browser can't hold credentials; (2) pooling — bound DB connections; (3) business logic — validation, authorization, rate limiting; (4) caching & load balancing; (5) resilience — retries, circuit breaking. Direct-to-DB browsers are a security anti-pattern.
17. **Q: What is the difference between a database server and an application server?** A: The DB server executes SQL and owns data/transactions; the app server executes business logic, calls the DB with a service account, and serves clients (HTTP). Two different tiers, two different trust levels.
18. **Q: How does authentication work in client-server?** A: Client presents credentials over TLS; server verifies against its auth catalog (e.g., Postgres `pg_authid`/`pg_hba.conf`, MySQL users). Options: passwords (scram-md5), certs, or external auth (LDAP/OAuth). Authorization (grants) then applies per role.
19. **Q (hard): Can client-server architecture give high availability?** A: Not by itself — a single server is a single point of failure. HA adds replicas (streaming replication in Postgres), failover (Patroni/PgBouncer), and reads from standby. The architecture provides the *model*; HA is layered on top.
20. **Q: What happens to DB connections when the server restarts?** A: All sessions drop; clients reconnect and re-authenticate. Good client libraries retry with backoff; pools re-establish on demand. This is why idempotency + retries matter in app code talking to a DB.

## 14. Follow-Up Questions
1. **Q: What is a "read replica" and which tier uses it?** A: A copy of the DB that serves reads (analytics, reporting) off the primary — a 2-tier-ish extension. Writes go to primary; replication pushes changes. Decouples read load from write path.
2. **Q: How does a connection pool know a connection is dead?** A: Pools validate via lightweight queries (`SELECT 1`) or protocol pings on checkout, and prune stale sockets; the server closes idle-forever sessions. Reliability detail interviewers love.
3. **Q: What is the difference between client-server and distributed DBMS?** A: Client-server: one logical server, many clients. Distributed: *multiple cooperating servers* that look like one DB (sharding, replication). Both use client-server messaging; distributed adds data placement and 2PC/consensus.
4. **Q: Why do some apps run the DB in the same process (embedded)?** A: When there's exactly one writer and sharing isn't needed — mobile, desktop, small services. Embedded (SQLite) removes network and server cost; you lose multi-client concurrency.
5. **Q: What's the DB role in serverless / FaaS?** A: Serverless functions are 3-tier clients; they need pools (or external poolers like RDS Proxy) because functions spawn frequently and each open/close of a connection is expensive.

## 15. Coding Example
```python
# 3-tier pattern: browser -> API -> DB with service account + pool
import psycopg2.pool

pool = psycopg2.pool.ThreadedConnectionPool(5, 20, "dbname=shop user=web_app")

@app.get("/orders/{uid}")
def orders(uid):
    with pool.getconn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, total FROM orders WHERE user_id=%s AND status='paid'",
                (uid,),                       # parameterized: injection-safe
            )
            rows = cur.fetchall()
    return {"orders": rows}                   # browser never talks SQL directly
```
```sql
-- Role design for the same app (DCL): least privilege per tier
CREATE ROLE web_app LOGIN PASSWORD '...';    -- app server service account
GRANT SELECT, INSERT, UPDATE ON orders, order_items TO web_app;
REVOKE ALL ON personnel FROM web_app;        -- HR tables stay hidden

CREATE ROLE analyst;                         -- sophisticated user
GRANT SELECT ON orders, customers TO analyst;  -- read-only warehouse access

CREATE ROLE app_dba LOGIN SUPERUSER;         -- only the DBA role can DDL/DCL
```

## 16. Industry Usage
- **PostgreSQL/MySQL** are deployed as client-server systems everywhere — behind `pgbouncer`/`ProxySQL`/RDS proxies; cloud offerings (RDS, Cloud SQL) manage the server side so customers just attach clients.
- **Every web framework** (Django, Rails, Spring, Next.js) implements the 3-tier pattern: browser → server → DB; ORMs are the app-tier SQL layer.
- **BI stack** (Tableau, Looker, Superset) connects as *sophisticated users* in 2-tier mode directly to warehouses, using dedicated read-only credentials.
- **Microservices** (Uber, Airbnb) run *many* app-tier clients against per-service or shared DBs — their pain (connection storms, per-service schemas, access boundaries) is this section's architecture at scale.
- **Serverless + RDS Proxy / Neon / PlanetScale** are the modern answer to connection-per-function cost — proving the pooling/3-tier concerns are still the bottleneck in 2026 cloud stacks.

## 17. References
- Elmasri & Navathe, *Fundamentals of Database Systems*, 7th ed., Ch. 1 (Database Users) & Ch. 2 (Centralized and Client-Server Architectures).
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 1.9 (Application Architectures).
- PostgreSQL Documentation, Client Interfaces & `pg_hba.conf`: https://www.postgresql.org/docs/current/client-authentication.html
- MySQL Reference Manual, Connecting/Client: https://dev.mysql.com/doc/refman/8.0/en/connecting.html
- pgbouncer: https://www.pgbouncer.org/

## 18. Cheat Sheet
- Client-server: one server owns data; clients send SQL over a protocol.
- 2-tier = client↔DB (tools); 3-tier = browser↔app server↔DB (web).
- File-server failed: no central authority → lost updates, no locking.
- Credentials live in the app tier (service account), never the browser.
- Connection pools: bound DB connections; per-connection RAM is the cost.
- 6 user types: naive, app programmer, sophisticated, specialized, analyst, DBA.
- DBA owns DDL/DCL/backups/tuning; analysts get SELECT-only.
- Embedded DB (SQLite) = serverless single-writer special case.

## 19. Quiz
1. In 3-tier, who holds DB credentials? a) browser b) app server c) client JS d) DNS → **b**
2. File-server architecture failed mainly because: a) slow disks b) no central authority/locking c) no GUI d) high cost → **b**
3. psql/DBEaver connecting directly to Postgres is: a) 3-tier b) 2-tier c) embedded d) P2P → **b**
4. The main cost of many idle DB connections is: a) disk b) RAM per backend c) bandwidth d) CPU → **b**
5. Who runs ad-hoc SQL? a) naive user b) sophisticated user c) DBA only d) browser → **b**
6. A connection pool exists to: a) encrypt data b) reuse connections & bound server load c) shard tables d) add indexes → **b**
7. Which user designs schemas? a) naive b) system analyst c) teller d) application programmer → **b**
8. SQLite is: a) 2-tier b) embedded/serverless c) 3-tier d) distributed → **b**
9. Which is NOT a DBA job? a) backups b) grants c) tuning d) writing business UI → **d**
10. After a server restart, clients: a) keep sessions b) reconnect & re-auth c) lose data d) recompile → **b**

## 20. Flashcards
- **Q: Why does a DB need a server?** → **A:** One authority to enforce ACID, locking, constraints, security.
- **Q: 2-tier vs 3-tier?** → **A:** Client↔DB vs browser↔app server↔DB.
- **Q: Where do DB credentials live in 3-tier?** → **A:** The app server's service account, never the browser.
- **Q: Why connection pooling?** → **A:** Connections cost RAM/RTT; pools reuse and bound concurrency.
- **Q: Name the 6 DB user categories.** → **A:** Naive, app programmer, sophisticated, specialized, system analyst, DBA.
- **Q: Why did file-server fail?** → **A:** No central authority → lost updates, no locking, corruption.
- **Q: What is embedded DBMS?** → **A:** In-process, single-writer, no server (SQLite).
- **Q: What does the DBA own?** → **A:** DDL, DCL, backups, tuning, security.

## 21. Revision
Client-server: one server owns data + transactions; clients send SQL over a protocol. **2-tier** = client↔DB (BI tools, thick clients); **3-tier** = browser↔app server↔DB (web) — credentials live in the app tier, pooling bounds connections, security enforced centrally. File-server failed (no authority → lost updates). **Six user roles**: naive (forms), app programmer (writes apps), sophisticated (ad-hoc SQL), specialized (BI/CAD tools), system analyst (schema design), DBA (DDL/DCL/backups/tuning). Interview moves: explain why a server is required (single authority for ACID); pick 2-tier vs 3-tier for a scenario; answer "why pools" (RAM per backend); and assign least-privilege roles for a naive user vs analyst. Mention SQLite as the embedded exception.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is client-server in DBMS?" | 2 / 13 Q1 |
| "2-tier vs 3-tier?" | 13 Q3-4 |
| "Why did file-server fail?" | 13 Q5 |
| "Who holds DB credentials in web apps?" | 13 Q6 |
| "What is connection pooling?" | 13 Q7-8 |
| "Name the database user categories" | 13 Q9 |
| "Design access for a teller/analyst" | 13 Q11 |
| "What does a DBA do?" | 13 Q10 |
