import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import data_utils as util
import os

## tests
# df_original = pd.read_csv('test.tsv',sep='\t')# annee/mois/jour sont bien int64
data_files = ['data/2020-2024_cleaned.tsv']
save_paths = ['data/2020-2024_budget_boxoffice.tsv']

df_cleaned_all = pd.read_csv('data/2020-2024_cleaned.tsv',sep='\t')

df_budget_boxoffice = util.clean_data(df_cleaned_all, cols_retain=['Budget max','Box office max'])
df_budget_boxoffice.to_csv('data/2020-2024_budget_boxoffice.tsv',sep='\t')
# print(df_original.shape)

# # 对预算和票房进行分桶
budget_bins = pd.cut(df_budget_boxoffice['Budget max'], bins=500)  # 将预算分为10个区间
boxoffice_bins = pd.cut(df_budget_boxoffice['Box office max'], bins=500)  # 将票房分为10个区间

# # 创建交叉表，计算每个预算区间和票房区间的电影数量
heatmap_data = pd.crosstab(budget_bins, boxoffice_bins, normalize='index')  # 也可以使用sum或mean

# # 调整排序，确保区间连续（如果需要）
heatmap_data = heatmap_data.sort_index(ascending=False)

plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, annot=True, fmt=".2f")
plt.title('Heatmap of Movie Budget vs. Boxoffice')
plt.ylabel('Budget')
plt.xlabel('Boxoffice')
plt.show()






# # clean missing values and outliers
# df_all_cleaned = util.clean_data(df_original,cols=['Box office max','Budget max'])
# print(df_all_cleaned.shape)

# # 票房的直方图
# sns.histplot(data=df_all_cleaned['Box office max'].astype('float64').apply(np.log),bins=200,color='#ff6050')
# plt.show()

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

