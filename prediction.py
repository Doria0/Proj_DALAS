import xgboost as xgb
from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
# from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np

import data_utils as util
# import encode_qualitative as encode

feature_list = ['Durée', 'Budget max', 'averageRating',
       'PC_genres_0', 'PC_genres_1', 'PC_genres_2', 'PC_genres_3']

file = 'data/df_dure_budg_rating_box.tsv'
df_other_atts = util.clean_data(pd.read_csv(file, sep='\t'),
                                cols_retain=['tconst','Durée','Budget max','Box office max','averageRating'],
                                cols_na=['Durée','averageRating'])
print(df_other_atts.columns)
file1 = 'data/PCA/df_genres_enc_decomp.tsv'
df_genres = pd.read_csv(file1, sep='\t')
df_genres.drop('Unnamed: 0',axis=1,inplace=True)
print(df_genres.columns)
df_for_prediction = util.join_data(dfs=[df_other_atts,df_genres],keys=['tconst'],manners=['left'])
print(df_for_prediction.columns)


X = df_for_prediction[feature_list]
y = pd.DataFrame(df_for_prediction['Box office max'])

# Divide training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialise XGBoost Regressor
# loss function: mse
# sample rate of each tree: 0.3
# max depth of each tree: 5
# alpha:  
xgb_reg = xgb.XGBRFRegressor(objective ='reg:squarederror', colsample_bytree = 0.3, learning_rate = 0.1,
                           max_depth = 5, alpha = 10, n_estimators = 100)

# train model
xgb_reg.fit(X_train, y_train)

# predict on test set
y_pred = xgb_reg.predict(X_test)

# calculate mse error as performance mesure
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print("RMSE: %f" % (rmse))



# ## encode & decompose qualitative features
# # features=['genre']
# # df_quali_enc = encode.encode_decomp(df,features)

# # 假设df是您的DataFrame
# X = df.drop('Budget', axis=1)  # 特征矩阵
# y = df['Box office']  # 目标变量

# # 划分训练集和测试集
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # 创建线性回归模型并训练
# model = LinearRegression()
# model.fit(X_train, y_train)

# # 进行预测
# y_pred = model.predict(X_test)

# # 评估模型
# print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
# print("R² Score:", r2_score(y_test, y_pred))
