import xgboost as xgb
from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
# from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import data_utils as util
# import encode_qualitative as encode

feature_list = ['Durée','Budget max','averageRating',
        'PC_genres_0', 'PC_genres_1','PC_genres_2','PC_genres_3'] 

# # file = 'data/df_dure_budg_rating_box.tsv'
# file = 'data/EDA/15-24_bud_box_dur_rat.tsv'
# df_other_atts = util.clean_data(pd.read_csv(file, sep='\t'),
#                                 cols_retain=['tconst','Durée','Budget max','Box office max','averageRating'],
#                                 cols_na=['Durée','averageRating'])
# print(df_other_atts.columns)
# # file1 = 'data/PCA/df_genres_enc_decomp.tsv'
# file1 = 'data/PCA/15-24_df_genres_dim_reduc.tsv'
# df_genres = pd.read_csv(file1, sep='\t')
# df_genres.drop('Unnamed: 0',axis=1,inplace=True)
# print(df_genres.columns)
# df_for_prediction = util.join_data(dfs=[df_other_atts,df_genres],keys=['tconst'],manners=['left'])
# print(df_for_prediction.columns)
# df_for_prediction.to_csv('data/XGBoost/15-24_df_for_pred.tsv',sep='\t')


# X = df_for_prediction[feature_list]
# y = pd.DataFrame(df_for_prediction['Box office max'])

# # Divide training set and test set
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Initialise XGBoost Regressor
# # loss function: mse
# # sample rate of each tree: 0.3
# # max depth of each tree: 5
# # alpha:  
# xgb_reg = xgb.XGBRFRegressor(objective ='reg:squarederror', colsample_bytree = 0.3, learning_rate = 0.1,
#                            max_depth = 5, alpha = 10, n_estimators = 100)

# # train model
# xgb_reg.fit(X_train, y_train)

# # predict on test set
# y_pred = xgb_reg.predict(X_test)

# # calculate mse error as performance mesure
# rmse = np.sqrt(mean_squared_error(y_test, y_pred))
# print("RMSE: %f" % (rmse))

# # xgb_reg.save_model('models/xgb_model_15-24_avgRating.json')
# xgb_reg.save_model('models/xgb_model_15-24_all_features.json')


# plt.figure(figsize=(11, 8))
# ax = plt.gca()  # get current Axes
# xgb.plot_importance(xgb_reg,ax=ax)
# plt.savefig('sources/15-24_xgb_importance.pdf')
# # plt.savefig('sources/15-24_xgb_avgrat_importance.pdf')
# plt.show()

# import shap

# 加载模型
model = xgb.XGBRegressor()
model.load_model('models/xgb_model_15-24_all_features.json')
# model.load_model('models/xgb_model_15-24_avgRating.json')

# # 创建解释器
# explainer = shap.Explainer(model)

# # 计算 SHAP 值
# shap_values = explainer.shap_values(X_train)  # 假设 X_train 是你的训练数据

# # visualize the first prediction's explanation with a force plot
# shap.initjs()
# force_plot = shap.force_plot(explainer.expected_value, shap_values[0,:], X_train.iloc[0,:])
# print(shap_values.shape)
# shap.save_html('sources/force_plot.html', force_plot)
# # shap.save_html('sources/avgrat_force_plot.html', force_plot)

# shap.summary_plot(shap_values, X_train)
# plt.savefig('sources/15-24_shap_summary.pdf')
# # plt.savefig('sources/15-24_avgrat_shap_summary.pdf')


## Prediction
# loaded_model = xgb.XGBRegressor()
# loaded_model.load_model('models/xgb_model_15-24_all_features.json')
# Charger modèle
model = xgb.XGBRegressor()
model.load_model('models/xgb_model_15-24_all_features.json')
new_data = pd.DataFrame({
    'Durée':114.0,
    'Budget max':20000000.0,
    'averageRating':7.7,
    'PC_genres_0':-0.2364186987394356,
    'PC_genres_1':-0.0954190106197637,
    'PC_genres_2':0.1505767834339208,
    'PC_genres_3':0.7854926364732647
},index=[0])
predicted_boxoffice = model.predict(new_data)
# Imprimer le résultat
print("Predicted Box office: $%.5f" % predicted_boxoffice[0])
#'Box office max':523000000.0,


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
