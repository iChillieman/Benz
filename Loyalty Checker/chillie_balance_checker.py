import json
from web3 import Web3, exceptions
from sqlite3 import OperationalError
from chillie_db import db_insert_balance, db_fetch_all_airdrop_addresses
from chillie_util import init_db, get_contract_abi, setLogger
from chillie_calculate import check_if_they_sold
from config import TOKEN_ADDRESS, CSV_RECEIVER_INDEX, CSV_AMOUNT_INDEX
import time
import traceback
from dotenv import load_dotenv
import os

setLogger("log_check_balance.log")

# Load Secrets from .env
load_dotenv()
alchemy_key = os.getenv('ALCHEMY_API_KEY')
ether_scan_api_key = os.getenv('ETHER_SCAN_API_KEY')

# Fetch all Airdrops Addresses - See what thier Balance looks like!
# If this is the first time running the script, the database will be setup before checking balances!
try:
    pre_processed = db_fetch_all_airdrop_addresses()
except OperationalError as e:
    if str(e).find("no such table") != -1:
        print("Lets set up your Database!")
        init_db()
        pre_processed = db_fetch_all_airdrop_addresses()

all_airdrop_addresses = []
for p in pre_processed:
    all_airdrop_addresses.append(Web3.to_checksum_address(p))
    
# Im using Alchemy Here - But you can use whatever RPC you want to use!
rpc_url = "https://eth-mainnet.g.alchemy.com/v2/{}".format(alchemy_key)

# Connect!
web3 = Web3(Web3.HTTPProvider(rpc_url))
if web3.is_connected():
    print('Hello Chillieman! - Lets Check if these MFers sold!')
else:
    print('Failed to connect to Blockchain!')
    exit()
    

# Token Contract Init
token_address = Web3.to_checksum_address(TOKEN_ADDRESS)
token_abi = get_contract_abi(token_address, ether_scan_api_key)
token_contract = web3.eth.contract(token_address, abi=token_abi)

def main():
    timestamp = time.time()
    for address in all_airdrop_addresses:
        #Fetch Balance for everyone who received an AirDrop
        balance = token_contract.functions.balanceOf(address).call()
        
        # Strip the decimals off balance
        balance_formatted = balance / 10**18
        print("{} Token Amount: {}".format(address, balance_formatted))
        db_insert_balance(address, balance_formatted, timestamp)
        
    # Now that all balances were fetched, lets check if they have ever Sold:
    check_if_they_sold()

main()
