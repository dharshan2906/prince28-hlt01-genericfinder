# Engineering Notes: GenericFinder

# D03 · PostgreSQL

## 1. Migrations (Upgrade → Downgrade → Upgrade)

**Commands:**

```powershell
uv run alembic downgrade -1
uv run alembic current
uv run alembic upgrade head
uv run alembic history
```

**Output:**

```text
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running downgrade 33109253a8d5 -> e3a1a83170de, add gin index on metadata

INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
e3a1a83170de

INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade e3a1a83170de -> 33109253a8d5, add gin index on metadata

e3a1a83170de -> 33109253a8d5 (head), add gin index on metadata
33b6760a5d5b -> e3a1a83170de, create documents and pages
4e1f23d45be8 -> 33b6760a5d5b, add gin index on metadata
<base> -> 4e1f23d45be8, create documents and pages
```

## 2. Loader Idempotency

**Run 1:**

```text
records=20 inserted=17 updated=0 unchanged=3
```

**Run 2:**

```text
records=20 inserted=0 updated=0 unchanged=20
```

**Run 3 (after editing one record):**

```text
records=20 inserted=0 updated=1 unchanged=19
```

## 3. EXPLAIN Analysis – `?drug_code=VALUE`

**Command:**

```powershell
uv run python scripts/explain.py drug_code VALUE
```

### 3.1 Default planner decision

```text
Seq Scan on documents
(cost=0.00..11.00 rows=1 width=36)
(actual time=0.880..0.880 rows=0.00 loops=1)

Filter: (metadata @> '{"drug_code": "VALUE"}'::jsonb)
Rows Removed by Filter: 20
Buffers: shared read=2 dirtied=2

Planning:
Buffers: shared hit=141 read=7

Planning Time: 4.128 ms
Execution Time: 0.906 ms
```

### 3.2 With sequential scan disabled

```text
Bitmap Heap Scan on documents
(cost=12.81..16.82 rows=1 width=36)
(actual time=1.296..1.297 rows=0.00 loops=1)

Recheck Cond: (metadata @> '{"drug_code": "VALUE"}'::jsonb)
Buffers: shared hit=1 read=2

-> Bitmap Index Scan on ix_documents_metadata_gin
(cost=0.00..12.81 rows=1 width=0)
(actual time=1.257..1.257 rows=0.00 loops=1)

Index Cond: (metadata @> '{"drug_code": "VALUE"}'::jsonb)
Index Searches: 1
Buffers: shared hit=1 read=2

Planning:
Buffers: shared hit=1

Planning Time: 0.077 ms
Execution Time: 1.347 ms
```

### 3.3 Why did the planner choose a Seq Scan? (2 lines)

The PostgreSQL planner estimated that scanning the entire table would be cheaper than using the index. This may happen when the table is small or the query matches a large percentage of rows.

### 3.4 When would it switch to the GIN index? (1 line)

When the query uses an index-supported operator and the planner estimates that using the GIN index is cheaper than a sequential scan.

---

# D04 · Docker, Compose and Tests

## 1. Docker Image

### 1.1 Image information

**Command:**

```powershell
docker images genericfinder:dev
```

**Output:**

```text
IMAGE               ID             DISK USAGE   CONTENT SIZE
genericfinder:dev   61ad5d9de906    301MB        70MB
```

### 1.2 Verify container user

**Command:**

```powershell
docker run --rm genericfinder:dev id
```

**Output:**

```text
uid=999(app) gid=999(app) groups=999(app)
```

### 1.3 Build measurements

| Measurement | Result |
|---|---:|
| Image content size | 70 MB |
| Target | Under 400 MB |
| First build | 24.32 seconds |
| After one-line code change | 5 seconds |

**Which step said CACHED, and why?**

Docker cached the dependency installation step because the dependency files hadn't changed, so it reused the existing layer instead of reinstalling packages.

## 2. Docker Compose Stack

### 2.1 Container status

**Command:**

```powershell
docker compose ps -a
```

**Output:**

```text
NAME                      IMAGE                    SERVICE   STATUS
genericfinder-api-1       genericfinder-api        api       Up (healthy)
genericfinder-db-1        pgvector/pgvector:pg17   db        Up (healthy)
genericfinder-migrate-1   genericfinder-migrate    migrate   Exited (0)
genericfinder-redis-1     redis:7-alpine           redis     Up (healthy)
```

### 2.2 Migration logs

**Command:**

```powershell
docker compose logs migrate
```

**First startup – final line:**

```text
records=20 inserted=20 updated=0 unchanged=0
```

**After `docker compose down` and `docker compose up -d`:**

Pending: Capture the final migration log line.

## 3. Breaking the Database on Purpose

### 3.1 Expected verification sequence

| Condition | Endpoint | Expected result |
|---|---|---|
| Database stopped | `/health` | 200 OK |
| Database stopped | `/ready` | 503 Service Unavailable |
| Database started | `/ready` | 200 OK |

**Commands:**

```powershell
docker compose stop db

curl.exe -i http://localhost:8000/health
curl.exe -i http://localhost:8000/ready

docker
