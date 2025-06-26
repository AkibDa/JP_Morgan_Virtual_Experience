import pandas as pd

df = pd.read_csv('dataset/Nat_Gas.csv')
print(df.head())

def get_price_by_date(df, date):
    df['Dates'] = pd.to_datetime(df['Dates'], infer_datetime_format=True)

    date = pd.to_datetime(date)

    result = df[df['Dates'] == date]['Prices']

    if not result.empty:
        return result.values[0]
    else:
        return None

date = input('Enter the date(MM/DD/YY): ')

price = get_price_by_date(df, date)
print(price)




