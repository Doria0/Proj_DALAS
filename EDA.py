import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import data_utils as util
from ast import literal_eval
import os

## tests
# df_original = pd.read_csv('test.tsv',sep='\t')# annee/mois/jour sont bien int64
data_files_cleaned = ['data/2020-2024_cleaned.tsv','data/2015-2019_cleaned.tsv']
save_paths = ['data/2020-2024_budget_boxoffice.tsv']

df_20_24 = pd.read_csv(data_files_cleaned[0],sep='\t')
df_15_19 = pd.read_csv(data_files_cleaned[1],sep='\t')
# df_cleaned_all = pd.read_csv('data/2020-2024_cleaned.tsv',sep='\t') # Box-office & Budget don't have missing values
df_cleaned_all = pd.concat([df_20_24,df_15_19],axis=0,ignore_index=True)
# 20-24:(994, 11), 15-19:(1029, 11), (2023, 11)

# ## Histogramme de Box-office
# df_budget_boxoffice = util.clean_data(df_cleaned_all, cols_retain=['Budget max','Box office max'])
# df_budget_boxoffice.to_csv('data/EDA/15-24_budget_boxoffice.tsv',sep='\t')
# ax = sns.histplot(data=df_budget_boxoffice['Box office max'].astype('float64').apply(np.log10),bins=200,color='#ffc845')
# ax.set_xlabel('Box office(log10)')
# plt.savefig('sources/15-24_boxoffice_histo.pdf')
# plt.show()

# # ## Histogramme de Budget
# df_budget_boxoffice = pd.read_csv('data/EDA/15-24_budget_boxoffice.tsv',sep='\t')
# ax = sns.histplot(data=df_budget_boxoffice['Budget max'].astype('float64').apply(np.log10),bins=200,color='#0cb9c1')
# ax.set_xlabel('Budget(log10)')
# plt.savefig('sources/15-24_budget_histo.pdf')
# plt.show()

# # Histogramme de Durée
# df_duree_boxoffice = util.clean_data(df_cleaned_all, cols_retain=['Durée','Box office max'],cols_na=['Durée'])
# print("min duree: {}, max duree: {}".format(df_duree_boxoffice['Durée'].astype('float64').min(), df_duree_boxoffice['Durée'].astype('float64').max()))
# #16min~305min, 16~383 for 15-19
# ax = sns.histplot(data=df_duree_boxoffice['Durée'].astype('float64'),bins=200,color='#037ef3')
# ax.set_xlabel('Durée/min')
# plt.savefig('sources/15-24_duree_histo.pdf')
# plt.show()

# df_ratings = pd.read_csv('data/imdb/title.ratings.tsv',sep='\t')
# df_15_24_ratings = util.join_data([df_cleaned_all,df_ratings],keys=['tconst'],manners=['left'])
# df_15_24_ratings = util.clean_data(df_15_24_ratings,cols_retain=['tconst','Durée','Budget max','Box office max','averageRating'],
#                                    cols_na=['Durée','averageRating'])
# df_15_24_ratings.to_csv('data/EDA/15-24_bud_box_dur_rat.tsv',sep='\t')
# 1573 in total

# # Histo de ratings
# df_rat_boxoffice = pd.read_csv('data/EDA/15-24_bud_box_dur_rat.tsv',sep='\t')
# ax = sns.histplot(data=df_rat_boxoffice['averageRating'].astype('float64'),bins=200,color='#037ef3')
# ax.set_xlabel('averageRating')
# plt.savefig('sources/15-24_avgrating_histo.pdf')
# plt.show()

#-------------------------------------------
# # Bar des pays et des langues
# # data = {
# #     'country': ['USA', 'France', 'USA', 'UK', 'Germany', 'USA', 'India', 'France', 'Japan', 'UK']
# # }
# df_pays_langues = util.clean_data(df_cleaned_all,cols_retain=['Pays','Langage'],cols_na=['Pays','Langage'])

# # 计算每个国家的电影数量
# # df_pays_langues['Pays'] = df_pays_langues['Pays'].apply(literal_eval)
# # df_Pays_exploded = df_pays_langues.explode('Pays')
# # print(df_Pays_exploded.dtypes)
# # df_Pays_exploded.to_csv('pays_exploded.tsv')
# language_counts = df_pays_langues['Langage'].value_counts()
# print(f"{language_counts=}")
# # country_counts = df_Pays_exploded['Pays'].value_counts()
# # print(f"{country_counts=}")

# # 决定哪些国家的名称显示在图例中（例如显示前3或超过某个数量的国家）
# # threshold = country_counts.max() * 0.02  # 例如，设置阈值为最大国家数量的10%
# # legend_countries = country_counts[country_counts > threshold]
# threshold = language_counts.max() * 0.006  # 例如，设置阈值为最大国家数量的10%
# legend_languages = language_counts[language_counts > threshold]

# # 绘制条形图
# plt.figure(figsize=(15, 8))
# bars = plt.bar(legend_languages.index, legend_languages.values, color='skyblue')  # 为所有国家创建条形

# # 高亮显示占比较大的国家，并准备图例
# for bar, country in zip(bars, legend_languages.index):
#     if country in legend_languages:
#         bar.set_color('skyblue')  # 突出显示 #orange
#     else:
#         bar.set_label('')  # 不在图例中显示

# # 设置图例和图表的其他元素
# # plt.legend(legend_countries.index, title="Principaux pays de production")
# plt.xlabel('Langage')
# plt.ylabel('Nombre des Films')
# plt.title('Nombre des Films Par Langage')
# plt.xticks(rotation=45)
# plt.savefig('sources/15-24_langues_principales.pdf')
# plt.show()

#-------------------------------------------
# # genre-boxoffice
# plt.figure(figsize=(12,20),constrained_layout=True) # create a new figure
# ax = sns.scatterplot(data=df_cleaned_all, x='Budget max', y='Box office max', hue='genres')#,legend=False)
# # ax.set_ylim(-0.05e13,0.5e13)
# ax.set_xscale('log')
# ax.set_yscale('log')
# ax.set_xlabel('Budget max',fontsize=10)
# ax.set_ylabel('Box office max',fontsize=10)
# # 将图例放在图外并调整大小
# plt.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0., title='Pays',fontsize='small')
# # plt.savefig('sources/budget_boxoffice_scatter.pdf')
# plt.show()

#-------------------------------------------
# ## scatter
# # 预算，时长，评分和票房的关系
plt.figure(figsize=(12,20),constrained_layout=True) # create a new figure
ax = sns.scatterplot(data=df_cleaned_all, x='Budget max', y='Box office max', hue='Pays')#,legend=False)
# ax.set_ylim(-0.05e13,0.5e13)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Budget max',fontsize=10)
ax.set_ylabel('Box office max',fontsize=10)
# 将图例放在图外并调整大小
plt.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0., title='Pays',fontsize='small')
plt.savefig('sources/15-24_budget_boxoffice_scatter.pdf')
plt.show()

#-------------------------------------------
## Bubbles
# PC-genres and boxoffice
# df_genres_box = pd.read_csv('data/PCA/df_genres_box.tsv',sep='\t')
# plt.figure(figsize=(10, 8))
# scatter = plt.scatter(df_genres_box['PC_genres_1'], df_genres_box['PC_genres_2'], alpha=0.5, s=df_genres_box['revenue']/10000, c=df['revenue'], cmap='coolwarm')
# plt.colorbar(scatter, label='Revenue (in ten-thousands)')
# plt.xlabel('Principal Component 1')
# plt.ylabel('Principal Component 2')
# plt.title('Bubble Chart of Movie Genres PCA vs Revenue')
# plt.show()

#-------------------------------------------
## heatmap - Correlation coefficient matrix
# # variables: boxoffice, budget, duree, avgrating
# # not very evident
# df_duree_budget_box = util.clean_data(df_cleaned_all, cols_retain=['Tconst du film','Durée','Budget max','Box office max'],cols_na=['Durée'])
# df_duree_budget_box.rename(columns={'Tconst du film': 'tconst'}, inplace=True)
# df_ratings = pd.read_csv('data/imdb/title.ratings.tsv',sep='\t')
# df_dure_budg_rating_box = util.join_data(dfs=[df_duree_budget_box,df_ratings],keys=['tconst'],manners=['left'])

# df_dure_budg_rating_box = pd.read_csv('data/EDA/15-24_bud_box_dur_rat.tsv',sep='\t')
# # print(df_dure_budg_rating_box.index)
# # df_dure_budg_rating_box.to_csv('df_dure_budg_rating_box.tsv',sep='\t')
# df_dure_budg_rating_box.drop(['Unnamed: 0','tconst'], axis=1, inplace=True)
# corr_matrix = df_dure_budg_rating_box.corr()
# plt.figure(figsize=(10, 8))
# sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".5f", linewidths=.5)
# plt.title('Heatmap of Correlation Matrix')
# plt.savefig('sources/15-24_corr_rating_dure_budg_box_heatmap.pdf')
# plt.show()

#-------------------------------------------
# # heatmap-PCs+boxoffice
# df_dure_budg_rating_box = pd.read_csv('data/EDA/15-24_bud_box_dur_rat.tsv',sep='\t')
# df_PCs = pd.read_csv('data/PCA/15-24_df_genres_dim_reduc.tsv',sep='\t')
# df_dure_budg_rating_box_PCs = util.join_data([df_dure_budg_rating_box,df_PCs],keys=['tconst'],manners=['left'])
# df_dure_budg_rating_box_PCs.drop(['Unnamed: 0_x','Unnamed: 0_y','tconst'], axis=1, inplace=True)
# corr_matrix = df_dure_budg_rating_box_PCs.corr()
# plt.figure(figsize=(11, 9))
# sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".5f", linewidths=.5)
# plt.title('Heatmap of Correlation Matrix')
# plt.savefig('sources/15-24_corr_PCs_rating_dure_budg_box_heatmap_0.5.pdf')
# plt.show()




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

