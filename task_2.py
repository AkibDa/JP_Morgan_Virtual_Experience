import pandas as pd

def price_gas_storage_contract(
    df, injection_dates, withdrawal_dates, inject_rate, withdraw_rate, max_storage_volume, storage_cost_per_day):

  df['Dates'] = pd.to_datetime(df['Dates'], format='%m/%d/%y')
  df.set_index('Dates', inplace=True)

  df = df.sort_index()

  storage_level = 0
  cash_flows = []

  full_dates = df.index
  storage_log = pd.Series(0, index=full_dates)

  for date_str in injection_dates:
    date = pd.to_datetime(date_str, format='%m/%d/%y')
    if date in df.index:
      price = df.loc[date, 'Prices']
      volume = min(inject_rate, max_storage_volume - storage_level)
      storage_level += volume
      cash_flows.append((-volume * price, date))
      storage_log.loc[date:] += volume

  for date_str in withdrawal_dates:
    date = pd.to_datetime(date_str, format='%m/%d/%y')
    if date in df.index:
      price = df.loc[date, 'Prices']
      volume = min(withdraw_rate, storage_level)
      storage_level -= volume
      cash_flows.append((volume * price, date))
      storage_log.loc[date:] -= volume

  total_storage_cost = (storage_log * storage_cost_per_day).sum()

  total_cash_flow = sum([cf[0] for cf in cash_flows])
  contract_value = total_cash_flow - total_storage_cost

  return {
    'Contract Value': round(contract_value, 2),
    'Total Cash Flow': round(total_cash_flow, 2),
    'Storage Cost': round(total_storage_cost, 2)
  }

# Sample inputs
# data = {
#     'Dates': ['10/31/20', '11/30/20', '12/31/20', '1/31/21', '2/28/21'],
#     'Prices': [10.1, 10.3, 11.0, 10.9, 10.9]
# }
# df = pd.DataFrame(data)
#
# injection_dates = ['10/31/20', '11/30/20']
# withdrawal_dates = ['12/31/20', '1/31/21']
# inject_rate = 1000
# withdraw_rate = 1000
# max_storage_volume = 1500
# storage_cost_per_day = 0.01
#
# result = price_gas_storage_contract(df, injection_dates, withdrawal_dates, inject_rate, withdraw_rate, max_storage_volume, storage_cost_per_day)
#
# print(result)

data = pd.read_csv('Nat_Gas.csv')
df = pd.DataFrame(data)

injection_dates = input("Enter the injection dates (MM/DD/YY, comma-separated): ").split(',')
injection_dates = [d.strip() for d in injection_dates if d.strip()]

withdrawal_dates = input("Enter the withdraw dates (MM/DD/YY, comma-separated): ").split(',')
withdrawal_dates = [d.strip() for d in withdrawal_dates if d.strip()]

inject_rate = float(input('Enter the injection rate: '))
withdrawal_rate = float(input('Enter the withdraw rate: '))
max_storage_volume = float(input('Enter the max storage volume: '))
storage_cost_per_day = float(input('Enter the storage cost per day: '))

result = price_gas_storage_contract(df, injection_dates, withdrawal_dates, inject_rate, withdrawal_rate, max_storage_volume, storage_cost_per_day)
print(result)
