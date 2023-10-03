To use this Script, you first need an EtherScan API Key, and Alchemy API Key.
Place them in the .env file

You must install dependencies via pip:
`pip install -r requirements.txt`

1. To import NEW Airdrops, modify Config.py first.
Then Run `python import_airdrops.py`

2. To Fetch the current Balance of addresses that appear in airdrop table:
Run ` python chillie_balance_checker.py`

3. To Calculate who has LESS than the amount of tokens received from Airdrops:
Run `python chillie_calculate.py`

