import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 假设df是你的数据
df = pd.read_csv('../unzip_data/ADMISSIONS.csv')
df.fillna('Unknown', inplace=True)
# 转换ADMITTIME和DISCHTIME为datetime对象
df['ADMITTIME'] = pd.to_datetime(df['ADMITTIME'])
df['DISCHTIME'] = pd.to_datetime(df['DISCHTIME'])

# 创建新的特征，表示住院的时长（以天为单位）
df['DURATION'] = (df['DISCHTIME'] - df['ADMITTIME']).dt.days

# 选择要可视化的类别特征
cat_cols = ['ADMISSION_TYPE', 'ADMISSION_LOCATION', 'DISCHARGE_LOCATION', 'INSURANCE', 'RELIGION', 'MARITAL_STATUS', 'ETHNICITY', 'DIAGNOSIS']

for col in cat_cols:
    # 密度图
    plt.figure(figsize=(15, 6))
    for category in df[col].unique():
        sns.kdeplot(df[df[col] == category]['DURATION'], label=category, warn_singular=False)
    plt.title('Hospital stay duration by ' + col + ' (Density Plot)')
    plt.legend()
    plt.show()
