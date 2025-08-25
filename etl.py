from web3 import Web3
import psycopg2
import os

# --- Config ---
# ✅ Use your Ankr API key (no < > brackets)
RPC_URL = os.getenv(
    "RPC_URL",
    "https://rpc.ankr.com/eth/e703f07c18524fedac022203a89973b2be525b8dee240cd120817285c0773210"
)

DB_CONN = os.getenv(
    "DB_CONN",
    "dbname=chain user=postgres password=postgres host=localhost port=5432"
)

# --- Setup ---
w3 = Web3(Web3.HTTPProvider(RPC_URL))
conn = psycopg2.connect(DB_CONN)

def save_block(block_num: int):
    block = w3.eth.get_block(block_num, full_transactions=True)

    # Insert block
    with conn.cursor() as cur:
        cur.execute(
            """INSERT INTO blocks (number, hash, tx_count)
               VALUES (%s, %s, %s)
               ON CONFLICT (number) DO NOTHING""",
            (block.number, block.hash.hex(), len(block.transactions))
        )

    # Insert transactions
    with conn.cursor() as cur:
        for tx in block.transactions:
            cur.execute(
                """INSERT INTO transactions (hash, block_number, from_address, to_address, value)
                   VALUES (%s, %s, %s, %s, %s)
                   ON CONFLICT (hash) DO NOTHING""",
                (
                    tx.hash.hex(),
                    tx.blockNumber,
                    tx["from"],
                    tx["to"] if tx["to"] else None,
                    tx.value
                )
            )
    conn.commit()
    print(f"✅ Saved block {block.number} with {len(block.transactions)} txs")

if __name__ == "__main__":
    if w3.is_connected():
        print("✅ Connected to Ankr Ethereum RPC")
        latest = w3.eth.block_number
        print(f"Latest block on Ethereum: {latest}")
        for n in range(latest - 5, latest + 1):  # save last 6 blocks
            save_block(n)
    else:
        print("❌ Failed to connect to Ethereum RPC")
