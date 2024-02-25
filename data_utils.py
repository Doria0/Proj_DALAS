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
    Returns:
        tuple, (ind,title with space replaced by _)
    """
    titles = []
    df = pd.read_csv(file,sep='\t')
    primTitles = df['primaryTitle']
    tconsts = df['tconst']
    # manner I
    N = len(primTitles)
    for i in range(N):
        pt = primTitles[i]
        ind = tconsts[i]
        if str(pt).find(' ') > 0:
            titles.append((ind,rep_space_udscr(pt)))
        else:
            titles.append((ind,pt))
    print(f"{titles[:5] = }")
    # manner II
    return titles

def save_scrapping(path,df):
    df.to_csv(path,sep='\t')

def rep_space_udscr(s):
    """replace spaces by underscores"""
    l = list(s)
    for i in range(len(l)):
        if l[i] == ' ':
            l[i] = '_'
        if l[i] == '\'':
            l[i] = '%27'
    return ''.join(l)

def rep_udscr_space(s):
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

## read in names of films from "data-2.tsv"


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

