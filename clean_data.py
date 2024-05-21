import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import data_utils as util
import os

# df中有的索引因为国家有好几个而出现了多次，其他特征都是重复的
# 在观察票房和预算时，取这两列并去重即可
#也可以先用groupby将国家聚合为列表

### Clean data
# read_path = 'data/scrapped_2020-2024.tsv'
read_path = 'data/scrapped_2015-2019.tsv'
#2020-2024: 993 films usable in total,
clean_intermediate_path = 'data/clean_intermediate.tsv'
save_path = 'data/2020-2024_cleaned.tsv'

df_original = pd.read_csv(read_path, sep='\t')
# print(df_original.dtypes,'\n')

cols_kept = ['Tconst du film','Titre du film','Jour de sortie',
            'Mois de sortie','Année de sortie','Durée','Pays','Langage','Budget max','Box office max']
aggr_dict = {'Tconst du film' : 'first',
            'Titre du film' : 'first',
            "Jour de sortie" : lambda x: str(x.unique()),
            "Mois de sortie" : lambda x: str(x.unique()),
            "Année de sortie" : lambda x: str(x.unique()),
            "Durée" : 'first',
            'Pays': lambda x: str(x.unique()), # 创建一个包含所有独特国家的列表
            "Langage" : 'first',
            "Budget max" : 'first',
            "Box office max" : 'first'}
# def is_number(x):
#     return isinstance(set(list(x)), (int, float))
# ## tests
# df_original = pd.read_csv('test.tsv',sep='\t')# annee/mois/jour sont bien int64
# df_clean = df_original.copy()
# df_clean = util.clean_data(df_clean,cols_retain=cols_kept,cols_na='Box office max')
# df_clean.to_csv('test_cleaned.tsv',sep='\t')

# # 使用 apply() 方法应用这个函数，得到一个布尔序列
# incorrect_types = df_original['Pays'].apply(is_number)
# # 使用布尔索引找出错误的行标
# error_indices = df_original[incorrect_types].index
# # 输出错误的行标
# print(error_indices)

df_cleaned_all = util.clean_data(df_original,cols_retain=cols_kept,cols_na=['Box office max','Budget max'])
print(df_original.shape)
# executed on a view of df_original, rather than changing df_original, bcz df_original is passed as the param of the function => Warning
df_cleaned_all.to_csv(clean_intermediate_path,sep='\t') # for generating an index col automatically, otherwise we won't have the col
# saved as an intermediate file, then read it for the next process
df_cleaned_all = pd.read_csv(clean_intermediate_path,sep='\t')
df_cleaned_all = util.aggregate_data(df_cleaned_all,aggr=aggr_dict)
df_cleaned_all.to_csv(save_path,sep='\t')