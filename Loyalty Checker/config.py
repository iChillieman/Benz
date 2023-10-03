# What do you want the Database to be called?
DB_NAME = 'airdrops.db'

# Do you have a list of Airdrops to import? (Only used when no DB exists)
IS_IMPORT_AIRDROPS = True

# What are the CSV files to import AirDrops?
AIRDROP_CSV_FILENAMES = [
    'AirDrop1_part1.csv',
    'AirDrop1_part2.csv',
    'AirDrop2_part1.csv',
    'AirDrop2_part2.csv',
    'AirDrop3_part1.csv',
    'AirDrop3_part2.csv'
]

# Does your CSV have column Headers?
# IF the First line of your CSV does NOT contain Columns, Set this to 0
CSV_START_LINE = 1 #Skip the Column line

# Row Index for the Receiving wallet Address and the Amount Received
CSV_RECEIVER_INDEX = 5
CSV_AMOUNT_INDEX = 6

# The Smart Contracts used to Send out Airdrops
CSV_EXPECTED_AIRDROP_SENDERS = [
    '0x2c952ee289bbdb3aeba329a4c41ae4c836bcc231',
    '0xd152f549545093347a162dce210e7293f1452150'
]

# What Token we Tracking??
TOKEN_ADDRESS = '0x3007083EAA95497cD6B2b809fB97B6A30bdF53D3'
