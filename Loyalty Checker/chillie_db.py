import sqlite3
from config import DB_NAME
from decimal import Decimal

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
            
    c.execute('CREATE TABLE pool (address TEXT PRIMARY KEY)')
    
    # Recipient of Airdrop
    c.execute('''CREATE TABLE airdrop (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                address TEXT NOT NULL,
                amount REAL NULL
            )''')
            
    c.execute('''CREATE TABLE balance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                address TEXT NOT NULL,
                amount REAL NOT NULL,
                timestamp REAL NOT NULL
            )''')
            
    c.execute('''CREATE TABLE abi (
                address TEXT PRIMARY KEY,
                abi TEXT NOT NULL
            )''')

    conn.commit()
    conn.close()

# Fetches
def db_fetch_all_airdrop_addresses():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('SELECT DISTINCT address FROM airdrop')
    all_airdrop_addresses = c.fetchall()

    extract = []
    for a in all_airdrop_addresses:
        extract.append(a[0])
        
    conn.close()
    return extract
    
def db_fetch_expected_airdrop_balances():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('SELECT address, SUM(amount) FROM airdrop GROUP BY address')
    airdrop_totals = c.fetchall()
    
    extract = []
    for a in airdrop_totals:
        expected_balance = { 'address': a[0], 'expected_total': a[1] }
        extract.append(expected_balance)
        
    conn.close()
    return extract
    
def db_fetch_most_recent_balance(address):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('SELECT amount FROM balance WHERE address like :address ORDER BY id DESC LIMIT 1', {'address': address})
    balance = c.fetchone()
        
    conn.close()
    return balance[0]
    
def db_fetch_abi(address):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('SELECT abi FROM abi WHERE address=:address', {'address': address}) 
    abi = c.fetchone()
    
    conn.close()
    return abi
    
    
def db_insert_balance(address, amount, timestamp):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        'INSERT INTO balance VALUES (null, :address, :amount, :timestamp)' ,
        {'address': address, 'amount': str(amount), 'timestamp': str(timestamp) }
    )

    conn.commit()
    conn.close()
    
def db_insert_airdrop(address, amount):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('INSERT INTO airdrop VALUES (null, :address, :amount)' , {'address': address, 'amount': amount })

    conn.commit()
    conn.close()
    
def db_insert_abi(address, abi):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('INSERT INTO abi VALUES (:address, :abi)', 
            {'address': address, 'abi': abi}
        )

    conn.commit()
    conn.close()
    
def db_update_balance(db_id, balance):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('UPDATE balance SET amount = :balance WHERE id = :db_id', 
            {'balance': balance, 'db_id': db_id}
        )

    conn.commit()
    conn.close()

