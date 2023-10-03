import json
import sys
import traceback
import csv
from chillie_db import db_fetch_abi, db_insert_abi, create_tables, db_insert_airdrop
from config import IS_IMPORT_AIRDROPS, AIRDROP_CSV_FILENAMES, CSV_START_LINE, CSV_RECEIVER_INDEX, CSV_AMOUNT_INDEX, CSV_EXPECTED_AIRDROP_SENDERS
from web3 import Web3, exceptions
import requests
from decimal import Decimal

# Logger ----
class Logger(object):
    is_enabled = True
    def __init__(self, file_name):
        self.terminal = sys.stdout
        self.log = open(file_name, "a")

    def write(self, message):
        try:
            if(self.is_enabled):
                self.terminal.write(message)
                self.log.write(message)
        except Exception as e:
            e

    def flush(self):
        pass
        
    def disable(self):
        self.is_enabled = False
        sys.stdout = self.terminal
    
    def reenable(self):
        self.is_enabled = True

def setLogger(file_name):
    logger = Logger(file_name)
    sys.stdout = logger
    return logger


# Fetch Contract ABI so you can create a contract object
def get_contract_abi(contract_address, ether_scan_api_key):
    contract_address = Web3.to_checksum_address(contract_address)
    
    # First Attempt to check 
    from_db = db_fetch_abi(contract_address)
    if from_db == None:
        url = "https://api.etherscan.io/api?module=contract&action=getabi&address={}&apikey={}".format(contract_address, ether_scan_api_key)
        response = requests.get(url).json()
        is_verified = response['status']
        result = response['result']
        if int(is_verified) == 0:
            if not result == 'Contract source code not verified':
                print("Could not get ABI")
                traceback.print_exc()
            abi = None
        else:
            db_insert_abi(contract_address, result)
            abi = result
    else:
        abi = from_db[0]

    return abi

# Create DB, and Import Airdrop Files
def init_db():
    
    create_tables()

    # Import POOLS to detect 
    for p in LIQUIDITY_PAIRS:
        db_insert_pool(p)
    
    if IS_IMPORT_AIRDROPS:
        enter_airdrops_from_csv_files()
    
# Read Airdrop files and enter them into DB
def enter_airdrops_from_csv_files():
    # Import Airdrop List from a list of files:
    for file_name in AIRDROP_CSV_FILENAMES:
        with open(file_name) as file:
            csv_reader = csv.reader(file, delimiter=',')
            line_count = 0

            for row in csv_reader:
                if line_count < CSV_START_LINE:
                    print('Skipping this Line: {}'.format(row))
                    line_count += 1
                else:
                    is_valid = True
                    # Fetch the Receipient - Should NOT be in the EXPECTED_SENDERS List
                    receiver = row[CSV_RECEIVER_INDEX]
                    for address in CSV_EXPECTED_AIRDROP_SENDERS:
                        # If we detect that an Expended SENDER is actually RECEIVING tokens, do not enter in DB & continue to next row
                        if receiver.lower() == address.lower():
                            print("Not Adding {} Because its a AirDrop Contract".format(address))
                            is_valid = False
                            break
                            
                    if is_valid:
                        amount_received = row[CSV_AMOUNT_INDEX].replace(',', '')
                        print("Inserting Airdrop! {}: {}".format(receiver, amount_received))
                        db_insert_airdrop(receiver, amount_received)
                        line_count += 1
                    
            print("Imported {} AirDrop Addresses from {}".format(line_count, file_name))


# Output Messages:

# Best to use a number that is EVEN after divided by 2 (Divisible by 4)
HEADER_LENGTH = 40

def repeat_string(message, x):
    result = ""
    for i in range(x):
        result = result + message
    return result
    
def make_line(header_length, message, border_char, thickness, padding):
        message_string = repeat_string(border_char, thickness) + repeat_string(" ", padding) + message
        return message_string + repeat_string(" ", header_length - len(message_string) - thickness) + repeat_string(border_char, thickness)
        
def make_header(header_length, name, message_array, thickness, padding, border_char, is_emoji):
    message_line_limit = header_length - thickness * 2 - padding * 2
    message_lines = []
    
    blank_line_length = header_length - thickness * 2
    blank_line = repeat_string(border_char, thickness) + repeat_string(" ", blank_line_length) + repeat_string(border_char, thickness)
    if is_emoji:
        line = repeat_string(border_char, int(header_length / 2) + 1)
    else:
        line = repeat_string(border_char, header_length)
    
    for message in message_array:
        temp = message
        is_first_time = True
        while len(temp) > message_line_limit or is_first_time:
            
            current_line = temp[:message_line_limit].strip()
            temp = temp[message_line_limit:]
            
            message_lines.append(make_line(header_length, current_line, border_char, thickness, padding))
            if len(temp) <= message_line_limit and len(temp) > 0:
                message_lines.append(make_line(header_length, temp, border_char, thickness, padding))
                
            is_first_time = False
        
        name_string = repeat_string(border_char, thickness) + repeat_string(" ", padding) + name
        name_line = name_string + repeat_string(" ", header_length - len(name_string) - thickness) + repeat_string(border_char, thickness)
        
        
    
    for i in range(thickness):
        print(line)
        

    print(blank_line)
    print(name_line)
    for message in message_lines:
        print(message)
    
    print(blank_line)
        
    for i in range(thickness):
        print(line)
    
def message(messages, char, is_emoji):
    make_header(HEADER_LENGTH, "Loyalty Checker:", messages, 1, 2, char, is_emoji)