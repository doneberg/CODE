import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt

data = """
Identification,Full Name,Gender,Years,Height CM,Weight KG,Country,Team,Olympic Games,Year,Period,Place (City),Sports Event,Medal
1,A Dijiang,M,24,180,80,CHN,1992 Summer,1992,Summer,Barcelona,Basketball Men's Basketball,
12,A Lamusi,M,23,170,60,CHN,2012 Summer,2012,Summer,London,Judo Men's Extra-Lightweight,
23,Gunnar Nielsen Aaby,M,24,,,DEN,1920 Summer,1920,Summer,Antwerpen,Football Men's Football,
34,Edgar Lindenau Aabye,M,34,,,DEN,1900 Summer,1900,Summer,Paris,Tug-Of-War Men's Tug-Of-War,Gold
45,Christine Jacoba Aaftink,F,21,185,82,NED,1988 Winter,1988,Winter,Calgary,Speed Skating Women's 500 metres,
"""

data_io = StringIO(data)
df = pd.read_csv(data_io)

# Data cleaning and preparation
df = df.drop_duplicates()
df.dropna(subset=['Height CM', 'Weight KG', 'Years'], inplace=True)
df.reset_index(drop=True, inplace=True)

# Prompt 1: Exploring Athlete Demographics
df.hist(column=['Height CM', 'Weight KG', 'Years'], figsize=(12, 8), bins=10)
plt.show()
print(df[['Height CM', 'Weight KG', 'Years']].describe())

# Prompt 2: Relationship Between Physical Attributes
plt.scatter(df['Height CM'], df['Weight KG'])
plt.xlabel('Height (CM)')
plt.ylabel('Weight (KG)')
plt.title('Height vs Weight of Athletes')
plt.show()
print(df[['Height CM', 'Weight KG']].corr())

# Prompt 3: Age vs Weight (Corrected)
plt.scatter(df['Years'], df['Weight KG'])
plt.xlabel('Age (Years)')
plt.ylabel('Weight (KG)')
plt.title('Age vs Weight of Athletes')
plt.show()
print(df[['Years', 'Weight KG']].corr())

# Prompt 4: Olympic Success Over Time (Corrected)
df[~df['Medal'].isnull()].groupby('Year')['Medal'].count().plot(kind='line')
plt.xlabel('Olympic Year')
plt.ylabel('Medal Count')
plt.title('Medals Awarded Over Years')
plt.show()

df.groupby('Year')['Country'].nunique().plot(kind='line')
plt.xlabel('Olympic Year')
plt.ylabel('Number of Participating Countries')
plt.title('Participating Countries Over Years')
plt.show()

# Prompt 5: Dominance Across Sports
medal_breakdown = df[~df['Medal'].isnull()].groupby(['Country', 'Sports Event'])['Medal'].count()
medal_breakdown.unstack().plot(kind='bar', figsize=(10, 6))
plt.xlabel('Country')
plt.ylabel('Medal Count')
plt.title('Medal Count by Country and Sport')
plt.show()