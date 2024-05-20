import numpy as np
import pandas as pd
# import seaborn as sns
import bs4
import lxml
from urllib import request
import matplotlib.pyplot as plt
import time

def index_line_without_value(series): # Renvoie les index des lignes où il y a \\N pour valeur
    return series[series == "\\N"].index

file = "title.basics.tsv"
df_0 = pd.read_csv(file, sep='\t')

df1 = df_0.drop(index=index_line_without_value(df_0["startYear"]))

# pandas conditional filter
lbnd = 2015
rbnd = 2019
values = ['short','movie']
df2 = df1[df1["titleType"].isin(values)] # isin() returns a boolean seq which'll be used by dataframe for filtering
df2 = df2[(df2["startYear"].astype('int16')>=lbnd) & (df2["startYear"].astype('int16')<=rbnd)]
print(df2.shape)
df2.to_csv('data_2015-2019.tsv',sep='\t',mode='a')


# ind_recent = []
# s = time.time()
# for index,row in df1.iterrows():
#     if row["titleType"] == 'short' or row["titleType"] == 'movie':
#         if row["startYear"] == '\\N':
#             continue
#         elif 2014 < int(row["startYear"]) < 2020:
#             ind_recent.append(index)
# e = time.time()
# print(len(ind_recent))
# print('Time consumed: {}s'.format(e-s))


## stats
# sns.histplot(df2["startYear"].astype("int32").sort_values(ascending=True))
# plt.pause(20)

# garde seulement les lignes ce qui ont un box office
df_0 = pd.read_csv('scrapped_2020-2024.tsv',sep='\t')
has_box_office = np.array(list(np.where((df_0["Budget max"]!='\\N'))[0])) #tuple (index,)
print(has_box_office.shape) #358/40000,479/65000,528/80000,583/92000,629/108470,768/140000,803/144000,
# 871/164000,898/171000,931/180000

#82/9000,185/15000,311/20000,758/30000,1110/35000,1937/40000,2324/50000
#2742/55000,3109/60000
# print(np.where(df[:5]["Budget max"]=='\\N'))
# print(np.isnan(df[:5]["Budget max"]))


# joindre ces lignes avec genre de film

# cols = []

# df_wt_budget = df_0.iloc[has_bdg_boxofc,:]

# plt.scatter(df_wt_budget["Budget max"],df_wt_budget["Box office max"])
# sns.heatmap(df_wt_budget)

# heatmap pour trouver correlation entre box_office et caracterisations des films
# box_office - 