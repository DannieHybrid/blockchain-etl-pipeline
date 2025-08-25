# ⛓️ Blockchain ETL Pipeline

## Overview
This project extracts Ethereum blockchain data (blocks + transactions) via an RPC endpoint, transforms it, and loads it into PostgreSQL for analytics.  
It’s designed as a foundation for blockchain data engineering — enabling you to query, analyze, and build dashboards on top of raw chain data.

## Tech Stack
- **Python 3.10+**
- **web3.py** → Ethereum RPC client
- **PostgreSQL** → Data warehouse
- **psycopg2** → PostgreSQL driver

## Features
- Fetches the latest Ethereum blocks via RPC (Ankr, Infura, Alchemy, etc.)
- Saves block metadata and transactions into PostgreSQL
- Prevents duplicate inserts with primary keys
- Fully configurable via environment variables
- Easy to extend for analytics & dashboards

## Quickstart

### 1. Clone the repo
```bash
git clone https://github.com/DannieHybrid/blockchain-etl-pipeline.git
cd blockchain-etl-pipeline
2. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Setup PostgreSQL
Make sure PostgreSQL 14+ is running:

bash
Copy
Edit
brew services start postgresql@14
Create database and tables:

sql
Copy
Edit
CREATE DATABASE chain;

\c chain;

CREATE TABLE IF NOT EXISTS blocks (
    number BIGINT PRIMARY KEY,
    hash TEXT UNIQUE,
    tx_count INT
);

CREATE TABLE IF NOT EXISTS transactions (
    hash TEXT PRIMARY KEY,
    block_number BIGINT REFERENCES blocks(number),
    from_address TEXT,
    to_address TEXT,
    value NUMERIC
);
4. Configure environment
Create a .env file:

ini
Copy
Edit
RPC_URL=https://rpc.ankr.com/eth
DB_NAME=chain
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
5. Run ETL
bash
Copy
Edit
python etl.py
You should see logs like:

vbnet
Copy
Edit
✅ Connected to Ankr Ethereum RPC
Latest block on Ethereum: 23216086
✅ Saved block 23216081 with 192 txs
✅ Saved block 23216082 with 193 txs
...
Next Steps
Add historical sync (backfill older blocks)

Build analytics queries (e.g., top senders, gas usage, token transfers)

Connect BI tools like Metabase, Superset, or Grafana

Deploy with Docker for production-ready setup

License
MIT

yaml
Copy
Edit
