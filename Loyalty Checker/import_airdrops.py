from chillie_util import enter_airdrops_from_csv_files, setLogger

setLogger("log_import_airdrops.log")

# Call thos Script if a database already exists, and you want to add NEW Airdrops from new CSV files.
enter_airdrops_from_csv_files()