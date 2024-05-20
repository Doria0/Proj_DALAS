import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import data_utils as util
import os

df_original = pd.read_csv('scrapped_2020-2024.tsv', sep='\t')
print(df_original.shape)

# clean missing values and outliers
df_all_cleaned = util.clean_data(df_original,cols=['Box office max','Budget max'])
print(df_all_cleaned.shape)

# 票房的直方图
sns.histplot(data=df_all_cleaned['Box office max'].astype('float64').apply(np.log),bins=200,color='#ff6050')
plt.show()

# # 预算和票房的关系
# sns.scatterplot(data=df_original, x='Budget max', y='Box office max', hue='Pays')
# plt.show()

# # 类别的条形图
# sns.countplot(data=df_original, x='Language')
# plt.xticks(rotation=45)  # 如果类别名称很长或很多，旋转标签以便阅读
# plt.show()

# # 上映日期分析
# df_original['Année de sortie'] = df_original['Mois de sortie'].dt.year  # 假设上映日期已转换为datetime类型
# sns.lineplot(data=df_original, x='Année de sortie', y='Box office max', estimator=sum)  # 年度票房总额
# plt.show()

