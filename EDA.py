import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import data_utils as util
import os

## tests
# df_original = pd.read_csv('test.tsv',sep='\t')# annee/mois/jour sont bien int64
data_files_cleaned = ['data/2020-2024_cleaned.tsv']
save_paths = ['data/2020-2024_budget_boxoffice.tsv']

df_cleaned_all = pd.read_csv('data/2020-2024_cleaned.tsv',sep='\t') # Box-office & Budget don't have missing values

# ## Histogramme de Box-office
# df_budget_boxoffice = util.clean_data(df_cleaned_all, cols_retain=['Budget max','Box office max'])
# df_budget_boxoffice.to_csv('data/2020-2024_budget_boxoffice.tsv',sep='\t')
# ax = sns.histplot(data=df_budget_boxoffice['Box office max'].astype('float64').apply(np.log10),bins=200,color='#ffc845')
# ax.set_xlabel('Box office(log10)')
# plt.savefig('sources/boxoffice_histo.pdf')
# plt.show()

# ## Histogramme de Budget
# df_budget_boxoffice = pd.read_csv('data/2020-2024_budget_boxoffice.tsv',sep='\t')
# ax = sns.histplot(data=df_budget_boxoffice['Budget max'].astype('float64').apply(np.log10),bins=200,color='#0cb9c1')
# ax.set_xlabel('Budget(log10)')
# plt.savefig('sources/budget_histo.pdf')
# plt.show()

# # Histogramme de Durée
# df_duree_boxoffice = util.clean_data(df_cleaned_all, cols_retain=['Durée','Box office max'],cols_na=['Durée'])
# # print("min duree: {}, max duree: {}".format(df_duree_boxoffice['Durée'].astype('float64').min(), df_duree_boxoffice['Durée'].astype('float64').max()))
# #16min~305min
# ax = sns.histplot(data=df_duree_boxoffice['Durée'].astype('float64'),bins=200,color='#037ef3')
# ax.set_xlabel('Durée/min')
# plt.savefig('sources/duree_histo.pdf')
# plt.show()

# ## scatter
# # 预算和票房的关系
# plt.figure(figsize=(12,20),constrained_layout=True) # create a new figure
# ax = sns.scatterplot(data=df_cleaned_all, x='Budget max', y='Box office max', hue='Pays')#,legend=False)
# # ax.set_ylim(-0.05e13,0.5e13)
# ax.set_xscale('log')
# ax.set_yscale('log')
# ax.set_xlabel('Budget max',fontsize=10)
# ax.set_ylabel('Box office max',fontsize=10)
# # 将图例放在图外并调整大小
# plt.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0., title='Pays',fontsize='small')
# # plt.savefig('sources/budget_boxoffice_scatter.pdf')
# plt.show()

## heatmap - Correlation coefficient matrix
# # variables: boxoffice, budget, duree
# not very evident
df_duree_budget_box = util.clean_data(df_cleaned_all, cols_retain=['Tconst du film','Durée','Budget max','Box office max'],cols_na=['Durée'])
df_duree_budget_box.rename(columns={'Tconst du film': 'tconst'}, inplace=True)
df_ratings = pd.read_csv('data/imdb/title.ratings.tsv',sep='\t')
df_dure_budg_rating_box = util.join_data(dfs=[df_duree_budget_box,df_ratings],keys=['tconst'],manners=['left'])
print(df_dure_budg_rating_box.index)
# df_dure_budg_rating_box.to_csv('df_dure_budg_rating_box.tsv',sep='\t')
df_dure_budg_rating_box.drop('tconst', axis=1, inplace=True)
corr_matrix = df_dure_budg_rating_box.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".5f", linewidths=.5)
plt.title('Heatmap of Correlation Matrix')
plt.savefig('sources/corr_rating_dure_budg_box_heatmap.pdf')
plt.show()

# budget_bins = pd.cut(df_budget_boxoffice['Budget max'], bins=10)  # 将预算分为10个区间
# boxoffice_bins = pd.cut(df_budget_boxoffice['Box office max'], bins=10)  # 将票房分为10个区间

# # 创建交叉表，计算每个预算区间和票房区间的电影数量
# heatmap_data = pd.crosstab(budget_bins, boxoffice_bins, normalize='index')  # 也可以使用sum或mean

# # 调整排序，确保区间连续（如果需要）
# heatmap_data = heatmap_data.sort_index(ascending=False)

# plt.figure(figsize=(12, 8))
# sns.heatmap(heatmap_data, annot=True, fmt=".2f")
# plt.title('Heatmap of Movie Budget vs. Boxoffice')
# plt.ylabel('Budget')
# plt.xlabel('Boxoffice')
# plt.show()




# # 类别的条形图
# sns.countplot(data=df_original, x='Language')
# plt.xticks(rotation=45)  # 如果类别名称很长或很多，旋转标签以便阅读
# plt.show()

# # 上映日期分析
# df_original['Année de sortie'] = df_original['Mois de sortie'].dt.year  # 假设上映日期已转换为datetime类型
# sns.lineplot(data=df_original, x='Année de sortie', y='Box office max', estimator=sum)  # 年度票房总额
# plt.show()

