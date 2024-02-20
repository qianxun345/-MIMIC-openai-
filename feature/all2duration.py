import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 假设df是你的数据
df = pd.read_csv('../unzip_data/ADMISSIONS.csv') # 请替换为你的文件路径

# 转换ADMITTIME和DISCHTIME为datetime对象
df['ADMITTIME'] = pd.to_datetime(df['ADMITTIME'])
df['DISCHTIME'] = pd.to_datetime(df['DISCHTIME'])

# 创建新的特征，表示住院的时长（以天为单位）
df['DURATION'] = (df['DISCHTIME'] - df['ADMITTIME']).dt.days

# 对所有列进行迭代，并创建对应的图表
for col in df.columns:
    if df[col].dtype == 'object' and col not in ['ADMITTIME', 'DISCHTIME', 'DEATHTIME']:  # 对于分类特征
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=col, y='DURATION', data=df)
        plt.title('Hospital stay duration by ' + col)
        plt.xticks(rotation=90)  # 如果标签过多，可以旋转标签以防止重叠
        plt.show()
