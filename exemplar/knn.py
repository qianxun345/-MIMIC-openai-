import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np

# 读取数据
data = pd.read_csv('../unzip_data/ADMISSIONS.csv')

# 将日期转换为距离特定日期的天数
data['ADMITTIME'] = pd.to_datetime(data['ADMITTIME'])
data['DISCHTIME'] = pd.to_datetime(data['DISCHTIME'])
data['ADMITTIME'] = (data['ADMITTIME'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1D')
data['DISCHTIME'] = (data['DISCHTIME'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1D')

# 将分类变量转换为数值
le = LabelEncoder()
for column in data.columns:
    if data[column].dtype == 'object':
        data[column] = le.fit_transform(data[column].astype(str))

# 定义输入特征和目标变量
X = data.drop('DISCHTIME', axis=1)
y = data['DISCHTIME']

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 创建并训练模型
knn = KNeighborsRegressor(n_neighbors=3)
knn.fit(X_train, y_train)

# 预测测试集
y_pred = knn.predict(X_test)

# 计算均方误差
mse = mean_squared_error(y_test, y_pred)
print('Mean Squared Error:', mse)

# 绘制预测值和真实值
plt.scatter(y_test, y_pred)
plt.xlabel('True Values')
plt.ylabel('Predictions')
plt.title('KNN Regression: Predictions vs True Values')
plt.show()
