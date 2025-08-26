# Phase 0: Environment & Mindset

This guide covers the initial setup of your development environment for working with PostgreSQL and Python. A solid environment is the foundation for everything that follows. We will install the necessary tools, set up a clean workspace, and verify that everything is working correctly.

## 🚀 Step 1: Install PostgreSQL

First, we will install the latest stable version of PostgreSQL and its contrib packages, which contain useful extensions. The `systemd` service for PostgreSQL will be managed by the `postgres` user.

### Commands
```bash
# Update the package list
sudo apt update

# Install PostgreSQL and contrib packages
sudo apt install postgresql postgresql-contrib
````

### Verification

To ensure the PostgreSQL service is running correctly, check its status.

```bash
sudo systemctl status postgresql
```

The output should show `active (running)`.

## 💻 Step 2: Install Python 3.11+

We need a modern Python version for our development work. The following command installs Python 3.12, which meets the version requirement.

### Command

```bash
sudo apt install python3.12
```

### Verification

Confirm the installed Python version.

```bash
python --version
```

The output should be `Python 3.12.x`.

## 🌐 Step 3: Environment Isolation with `uv`

Using a virtual environment is a critical best practice to isolate project dependencies and avoid conflicts. We will use `uv`, a modern and fast tool for dependency management.

### Commands

```bash
# Install uv
pip install uv

# Navigate to your project directory
cd learn-techstacks/learn-postgresql/

# Initialize the project with uv
uv init -p python3.12

# Create and activate the virtual environment
uv venv -p python3.12 .venv
source .venv/bin/activate
```

## 📦 Step 4: Install Python Libraries

With the virtual environment activated, we can install all the core Python libraries required for our project.

### Command

```bash
uv pip install psycopg[binary] sqlalchemy alembic pytest
```

### Verification

Launch a Python REPL and verify that `psycopg` is installed and can be imported.

```bash
python
>>> import psycopg
>>> print(psycopg.__version__)
3.2.9
>>> exit()
```

## 🛠️ Step 5: Install a Database Management GUI/CLI

You have a choice of tools for managing your database. `pgcli` is great for the command line, while `pgAdmin4` offers a full graphical interface.

### Option 1: `pgcli` (CLI)

A command-line tool with excellent autocompletion.

```bash
sudo apt install pgcli
```

### Option 2: `pgAdmin4` (GUI)

A powerful graphical tool for database administration.

#### Installation

Follow these commands to add the official repository and install `pgAdmin4-web`.

```bash
curl -fsS [https://www.pgadmin.org/static/packages_pgadmin_org.pub](https://www.pgadmin.org/static/packages_pgadmin_org.pub) | sudo gpg --dearmor -o /usr/share/keyrings/packages-pgadmin-org.gpg
sudo sh -c 'echo "deb [signed-by=/usr/share/keyrings/packages-pgadmin-org.gpg] [https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release](https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release) -cs) pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list && sudo apt update'
sudo apt install pgadmin4-web
```

#### Setup & Management

After installation, you must set up the web server and create a login.

```bash
# Run this once to set up the web interface and create a user
sudo /usr/pgadmin4/bin/setup-web.sh
```

Follow the terminal prompts to set your login email and password.

To manage the `pgAdmin4` web interface, you must control the Apache web server that hosts it.

```bash
# Check status
sudo systemctl status apache2

# Stop the service
sudo systemctl stop apache2

# Start the service
sudo systemctl start apache2

# Restart the service
sudo systemctl restart apache2
```

## ✅ Outcome to Verify

To complete this setup step, you must confirm that you can connect to PostgreSQL and manage your databases.

### 1\. Connect to `psql` and list databases

Switch to the `postgres` user and start the PostgreSQL shell.

```bash
sudo -u postgres psql
```

Once in the `psql` shell, run the following commands:

```sql
\l          -- list databases
\du         -- list roles
\q          -- quit the shell
```

### 2\. Create a "scratch" database

We will create a temporary database for hands-on experiments.

```bash
# Create the database from the command line
sudo -u postgres createdb scratchdb
```

### 3\. Final Verification

Reconnect to the `psql` shell and confirm that the new `scratchdb` exists in the list of databases.

```bash
sudo -u postgres psql
postgres=# \l
```

The output should now include `scratchdb` in the list, confirming your setup is complete and correct.

```
         Name      |   Owner    | ...
-------------------+------------+---
 ...
 scratchdb         | postgres   | ...
 template0         | postgres   | ...
 template1         | postgres   | ...
(4 rows)
```