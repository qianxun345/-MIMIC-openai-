import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 假设df是你的数据
df = pd.read_csv('../unzip_data/ADMISSIONS.csv') # 请替换为你的文件路径

# 数据清洗
# 转换ADMITTIME和DISCHTIME为datetime对象
df['ADMITTIME'] = pd.to_datetime(df['ADMITTIME'])
df['DISCHTIME'] = pd.to_datetime(df['DISCHTIME'])

# 填充空值
df.fillna('Unknown', inplace=True)

# 新建一个列用于表示住院的时长
df['DURATION'] = (df['DISCHTIME'] - df['ADMITTIME']).dt.days

# 数据转换
# 可以将一些分类变量转为独热编码或者标签编码，例如
df['ADMISSION_TYPE'] = df['ADMISSION_TYPE'].astype('category').cat.codes

# 转换DEATHTIME为datetime对象
df['DEATHTIME'] = pd.to_datetime(df['DEATHTIME'], errors='coerce')

# 创建新的特征，表示病人是否在住院期间去世
df['DIED_IN_HOSPITAL'] = ~df['DEATHTIME'].isnull()

# 计算不同入院类型的死亡比例
death_ratio = df.groupby('ADMISSION_TYPE')['DIED_IN_HOSPITAL'].mean()


# 特征可视化
# 比如我们可以查看不同入院类型对应的住院时长
plt.figure(figsize=(10, 6))
sns.boxplot(x='ADMISSION_TYPE', y='DURATION', data=df)
plt.title('Hospital stay duration by admission type')
plt.show()

# 不同入院类型对应的死亡时长
plt.figure(figsize=(10, 6))
sns.countplot(x='ADMISSION_TYPE', hue='DIED_IN_HOSPITAL', data=df)
plt.title('Death in hospital by admission type')
plt.show()
plt.figure(figsize=(10, 6))
sns.barplot(x=death_ratio.index, y=death_ratio.values)
plt.title('Death ratio by admission type')
plt.ylabel('Death ratio')
plt.show()


# 或者查看不同保险类型对应的住院时长
plt.figure(figsize=(10, 6))
sns.boxplot(x='INSURANCE', y='DURATION', data=df)
plt.title('Hospital stay duration by insurance type')
plt.show()
