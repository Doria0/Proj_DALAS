from urllib import request
import bs4  # html parser
import pandas as pd
import numpy as np
# import re
import math
# import data_utils as util

def read_titles(file):
    """read in from file
    Args:
        file: string, relative or absolute path of the file
    Returns:
        tuple, (ind,title with space replaced by _)
    """
    titles = []
    df = pd.read_csv(file,sep='\t')
    primTitles = df['primaryTitle']
    tconsts = df['tconst']
    titleTypes = df['titleType']
    # manner I
    N = len(primTitles)
    for i in range(N):
        if (titleTypes[i] == 'movie') or (titleTypes[i] == 'short'):
            # print("titletype: {}".format(titleTypes[i]))
            pt = primTitles[i]
            ind = tconsts[i]
            if str(pt).find(' ') > 0:
                titles.append((ind,rep_symbols(pt)))
            else:
                titles.append((ind,pt))
    print(f"{titles[:5] = }")
    # manner II
    return titles

def save_scrapping(path,df):
    df.to_csv(path,sep='\t')

def rep_symbols(s):
    """replace spaces by underscores"""
    l = list(s)
    for i in range(len(l)):
        if l[i] == ' ':
            l[i] = '_'
        if l[i] == '\'':
            l[i] = '%27'
    return ''.join(l)

def recover_symbols(s):
    """replace spaces by underscores"""
    l = list(s)
    for i in range(len(l)):
        if l[i] == '_':
            l[i] = ' '
    return ''.join(l)

# exp request
prefix_fr = "https://fr.wikipedia.org/wiki/"
prefix_en = "https://en.wikipedia.org/wiki/"
film_title_fr = "Le_Voyage_de_Chihiro"
film_title_en = "Spirited_Away"


def clean_data(df,cols_retain=[],cols_na=[]):
    # missing values, outliers
    # If we only want to keep a part of the original df
    if len(cols_retain)!=0:
        df = df[cols_retain]
    # If we want to eliminate rows where some cols' values are missing
    if len(cols_na)!=0:
        for col in cols_na:
            df.loc[df[col] == '\\N', col] = np.nan #inplace=True: change the df itself
            # df.loc[<condition>,col_name]
            df.dropna(subset=cols_na,inplace=True)
    return df

def aggregate_data(df,aggr=dict()):
    # 对重复的电影ID进行分组，并聚合数据
    # 假设 'budget' 和 'box_office' 是要保留的列，而 'country' 是需要合并的列
    df_tmp = df.copy()
    if len(aggr)!=0:
        df_tmp.set_index(df_tmp.columns[0], inplace=True) # by default, set the unnamed (index) column as index
        df_tmp = df_tmp.groupby(df_tmp.index).agg(aggr).reset_index()
        # 查看处理后的 DataFrame
        # df_cleaned.to_csv('test_cleaned.tsv',sep='\t')
        # df_tmp.drop()
    return df_tmp

def join_data(dfs,keys,manner='inner'):
    """
    Args:
        dfs: list, all dataframes to be joined
        keys: list, key of jointure, index correspondent wt dfs
    """
    if len(dfs) == 0:
        return pd.DataFrame()
    df_res = dfs[0]
    for i in range(len(dfs)):
        df_res = pd.merge(df_res, dfs[i], on=keys[i], how='inner')
    return df_res

# all_film_titles = read_titles("data-2.tsv")[:10000]
# traverse all film titles in imdb dataset
# request_texts = []
# for film_title in all_film_titles:
#     # if film_title.find(' ') > 0:
#     #     film_title = rep_space_udscr(film_title)
#     url_en = prefix_en + film_title
#     print(f"{url_en=}")
#     try:
#         req = request.urlopen(url_en).read()
#         request_texts.append(list(req))
#     except:
#         request_texts.append(math.nan)
# print(request_texts[:5])
# for request_text in request_texts:
#     if request_text != math.nan:
#         page = bs4.BeautifulSoup(request_text, "html.parser")
    # print(page.find("title"))

