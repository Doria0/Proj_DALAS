from urllib import request
import bs4  # html parser
import pandas as pd
# import re
import math
# import data_utils as util

def read_titles(file):
    """read in from file
    Args:
        file: string, relative or absolute path of the file
    Return:
        list, all film titles
    """
    titles = []
    df = pd.read_csv(file,sep='\t')
    primTitles = df['primaryTitle'].unique() # extract all unique values in the column "primaryTitle"(en)
    # manner I
    for pt in primTitles:
        if str(pt).find(' ') > 0:
            titles.append(rep_space_udscr(pt))
        else:
            titles.append(pt)
    # print(f"{titles[:5] = }")
    # manner II   # how about we just find special cases by hand(?
    return titles

def save_scrapping(path,df):
    df.to_csv(path,sep='\t')

def rep_space_udscr(s):
    """replace spaces by underscores"""
    l = list(s)
    for i in range(len(l)):
        if l[i] == ' ':
            l[i] = '_'
    return ''.join(l)

# exp request
prefix_fr = "https://fr.wikipedia.org/wiki/"
prefix_en = "https://en.wikipedia.org/wiki/"
film_title_fr = "Le_Voyage_de_Chihiro"
film_title_en = "Spirited_Away"

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

