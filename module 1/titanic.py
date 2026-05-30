import pandas as pd
df=pd.read_csv('Titanic-Dataset.csv')

print(df.shape) #rows_and_columns
print(df.iloc[0:4]) #first_5_rows   

print("null values",df['Age'].isnull().sum())

df['Age']=df['Age'].fillna(df['Age'].median())

print("null values",df['Age'].isnull().sum())

df = df.dropna(subset=['Embarked'])

df=df.drop(columns=['Cabin'])   

survival_rate_by_sex=df['Survived'].mean()
survival_rate_by_Pclass=df['Pclass'].mean()
mean_age_survivors=df[df['Survived'] == 1]['Survived'].mean()
mean_age_nonsurvivors=df[df['Survived'] == 0]['Survived'].mean()
print("survival_rate_by_sex",survival_rate_by_sex,"survival_rate_by_Pclass",survival_rate_by_Pclass,
"mean_age_survivors",mean_age_survivors) 


