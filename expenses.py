import datetime
import getpass

import mintapi
import pandas as pd
from dateutil.relativedelta import relativedelta

email = input("Enter Mint email: ")
password = getpass.getpass()

start_date = (datetime.date.today() + relativedelta(months=-1)).replace(day=1)
end_date = start_date + relativedelta(day=31)

start_date = start_date.strftime('%m/%d/%y')
end_date = end_date.strftime('%m/%d/%y')
print(f"Date Range: {start_date} -> {end_date}")
input("Press Enter to Continue")

print("Logging into mint")
mint = mintapi.Mint(email, password, mfa_method='sms', wait_for_sync=True)

print("Getting transaction info")
transactions: pd.DataFrame = mint.get_detailed_transactions(start_date=start_date, end_date=end_date)
transactions = transactions.query('isTransfer == False '
                                  'and mcategory != "Paycheck" '
                                  'and mcategory != "Interest Income" '
                                  'and mcategory != "Income" '
                                  'and mcategory != "Credit Card Payment" '
                                  'and mcategory != "Investments"')

transactions = transactions[['date', 'mcategory', 'amount', 'omerchant', 'category']]
transactions.to_csv('transactions.csv')

mint.close()
print("Finished")
