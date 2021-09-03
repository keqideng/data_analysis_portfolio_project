import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import requests
import io

url = 'https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv'
source = requests.get(url).text
reader = io.StringIO(source)
df = pd.read_csv(reader)
df['Reported Date'] = pd.to_datetime(df['Reported Date'])
variant_df = df

print(variant_df.info())
sns.set_theme( style='whitegrid', palette='winter')
plt.figure(figsize=(20,18))
sns.lineplot(data=df[['Total_Lineage_B.1.1.7_Alpha', 'Total_Lineage_B.1.351_Beta', 'Total_Lineage_P.1_Gamma', 'Total_Lineage_B.1.617.2_Delta']])
plt.show()