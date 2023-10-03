from chillie_util import enter_airdrops_from_csv_files, message, setLogger
from chillie_db import db_fetch_expected_airdrop_balances, db_fetch_most_recent_balance
import time


# Pull All Balances - Make sure the Airdrop amount IS ATLEAST what is expected by summing all.
def check_if_they_sold():
    losers = []
    timestamp = int(time.time())
    
    loyal_count = 0
    
    message(["Lets see who is loyal!"], '😊', True)
    time.sleep(1) # Wait for a second so user can read the message
    
    # Heres all the accounts 
    winning_logger = setLogger("winners_{}.csv".format(timestamp))
    print("Address, Current Balance, Expected Amount")
    for balance in db_fetch_expected_airdrop_balances():
        address = balance['address']
        expected_balance = int(balance['expected_total'])
        
        # How much DOES this wallet have?
        current_balance = int(db_fetch_most_recent_balance(address))

        if current_balance >= expected_balance:
            print("{},{},{}".format(address, current_balance, expected_balance ))
            loyal_count += 1
        else:
            loser_dictionary = {
                'address': address,
                'current_balance': current_balance,
                'expected_balance': expected_balance,
            }
            losers.append(loser_dictionary)
    
    #Turn off Winning Logger and switch to Losers
    winning_logger.disable()
    loser_logger = setLogger("losers_{}.csv".format(timestamp))
    
    print("Address, Current Balance, Expected Amount")
    for l in losers:
        print("{},{},{}".format(l['address'], l['current_balance'], l['expected_balance'] ))
    
    # Disable Loser Logger before outputting Results:
    loser_logger.disable()
    
    # How many are not loyal?
    non_loyal_message = ["Not Loyal: {}".format(len(losers))]
    message(non_loyal_message, '🥱', True)
    
    print("") # Blank Line to separate Result Messages
    
    # How many are Loyal?
    loyal_message = ["Loyal Holders: {}".format(loyal_count)]
    message(loyal_message,'👑', True)
    