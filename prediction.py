from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd

import data_utils as util
import encode_qualitative as encode


file = 'data_2020-2024.tsv'
df = util.clean_data(pd.read_csv(file, sep='\t'))

## encode & decompose qualitative features
# features=['genre']
# df_quali_enc = encode.encode_decomp(df,features)

# 假设df是您的DataFrame
X = df.drop('Budget', axis=1)  # 特征矩阵
y = df['Box office']  # 目标变量

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 创建线性回归模型并训练
model = LinearRegression()
model.fit(X_train, y_train)

# 进行预测
y_pred = model.predict(X_test)

# 评估模型
print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
print("R² Score:", r2_score(y_test, y_pred))
