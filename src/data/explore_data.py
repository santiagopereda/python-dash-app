import pandas as pd
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 20)

df_location ='../../data/raw/earth_challenge_dataset.csv'
df = pd.read_csv(df_location)