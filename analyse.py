import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


pd.set_option('display.max_columns', 8)
general, prenatal, sports = [pd.read_csv(r'test\general.csv'),
                             pd.read_csv(r'test\prenatal.csv'),
                             pd.read_csv(r'test\sports.csv')]

prenatal.columns = general.columns
sports.columns = general.columns

replace_values = {'bmi': 0, 'diagnosis': 0, 'blood_test': 0, 'ecg': 0,
                  'ultrasound': 0, 'mri': 0, 'xray': 0, 'children': 0,
                  'months': 0}
#  merge 3 tabs into 1 dataframe
df = (pd.concat([general, prenatal, sports], ignore_index=True)
    .drop(columns=['Unnamed: 0'])
    .dropna(axis=0, how='all', )  # delete all Nan's rows
    .replace(['male', 'man'], 'm')
    .replace(['female', 'woman'], 'f')
    .fillna({'gender': 'f'})  # replace NaNs in 'gender' with f
    .fillna(replace_values, ))  # replace NaNs in those columns with zeros


def print_df_sample():
    print('Data shape: ', df.shape)
    print(df.sample(n=20, random_state=30))


# print_df_sample()

#  How many non-NA values do we have in the column "hospital"?
# print('Data shape: ', df.shape)
# print(df.hospital.count())
#  count the missing values in the column "hospital"
# print(df.hospital.isna().sum())

answers = {}  # to the questions from the 4/5 stage
# Q1: Which hospital has the highest number of patients?
hospitals_series = df.hospital.value_counts()
answers[1] = hospitals_series.idxmax()

# Q2: What share in the general hospital suffers from stomach?
general_stomach = df[df.hospital == 'general'].diagnosis.value_counts()['stomach']
answers[2] = round(general_stomach/hospitals_series['general'], 3)

# Q3: What share in the sports hospital suffers from dislocation
sports_dislocation = df[df.hospital == 'sports'].diagnosis.value_counts()['dislocation']
answers[3] = round(sports_dislocation/hospitals_series['sports'], 3)

# Q4: difference in the median ages of the general and sports?
df_wide = df.pivot_table(columns='hospital', aggfunc='median')
answers[4] = df_wide.loc['age', 'general'] - df_wide.loc['age', 'sports']

# Q5.a: In which hospital blood_test column has max t-values?
# Q5.b: How many blood tests were taken?
t_values = df.loc[df.blood_test == 't'].hospital.value_counts()
answers[5] = [t_values.idxmax(), t_values.max()]
# print(answers)

# output final answers
# for num in range(1, 5):
#     print(f'The answer to the {num}st question is {answers[num]}')
# print(f'The answer to the 5th question is {answers[5][0]}, {answers[5][1]} blood tests')

# VQ1: What is the most common age of a patient among all hospitals?
# Plot a histogram and choose one of the following age ranges:
# 0-15, 15-35, 35-55, 55-70, or 70-80
df.plot(y='age', kind='hist', bins=[0, 15, 35, 55, 70, 80])
plt.savefig('pic1.jpg', bbox_inches='tight')
plt.show()

# VQ2: What is the most common diagnosis among patients in all hospitals? Create a pie chart
# plt.pie(df.diagnosis.value_counts(), labels=df.diagnosis.value_counts().index)
# var2:
df.diagnosis.value_counts().plot.pie()
plt.savefig('pic2.jpg', bbox_inches='tight')
plt.show()

# VQ3: Build a violin plot of height distribution by hospitals.
# Try to answer the questions: What is the main reason for the gap in values?
# Why there are two peaks, which correspond to the relatively small and big values?
ax = sns.violinplot(y="height", inner='quartile', data=df)
ax.set_title('Distribution of height', fontsize=16)
# var 2:
# fig, axes = plt.subplots()
# axes.violinplot(dataset=df.height)
plt.show()

# output answers to visual part
print('The answer to the 1st question: 15-35')
print('The answer to the 2nd question: pregnancy')
print("The answer to the 3rd question: It's because different measure units are used in height column")
