# import urllib
from urllib import request
import bs4  # html parser
import pandas as pd
# import re
import math
import data_utils as util

# request
prefix_fr = "https://fr.wikipedia.org/wiki/"
prefix_en = "https://en.wikipedia.org/wiki/"
film_title_fr = "Le_Voyage_de_Chihiro"
film_title_en = "Spirited_Away"

## read in names of films from "data-2.tsv"

# p2 = pd.read_csv("data-2.tsv",sep='\t')
# # extract all unique values in the column "primaryTitle"
# all_film_titles = p2['primaryTitle'].unique()
# # traverse all film titles in imdb dataset
# request_texts = []
# for film_title in all_film_titles:
#     request_texts.append(list(request.urlopen(prefix+film_title).read()))
# # print(request_text[:1000])
# for request_text in request_texts:
#     page = bs4.BeautifulSoup(request_text, "lxml")
#     print(page.find("title"))



## save scrapped data in a csv file

## recuperer les fournieurs de voix pour les animations
film_fr = prefix_fr + film_title_fr
request_text = request.urlopen(film_fr).read()
soup = bs4.BeautifulSoup(request_text,"html.parser")

# find list
# find the h3 title, then find the next sibling
span_with_voix_org = soup.find('span',{'id':'Voix_originales'})
if span_with_voix_org:
    df_vo = pd.DataFrame()#['acteur_vo','personnage']
    ul_vo = span_with_voix_org.find_next('ul')
    li_list = ul_vo.find_all('li')
    ind = 0
    for l in li_list:
        # print(l.text)
        act, perso = l.text.split(':')
        # print(f"{act.strip()=}, {perso.strip()=}")
        # df1 = pd.DataFrame({'a':1,'b':2})
        df2 = pd.DataFrame({'acteur_vo':act.strip(),
                            'personnage':perso.strip()},
                            index=[ind])
        df_vo = pd.concat([df_vo,df2],ignore_index=True)
        ind += 1
    # print(f"{df_vo.shape=}")
    # print(f"{df_vo}")

# print(f"{ul_vo=}")
# print(f"{li_list=}")

span_with_voix_fr = soup.find('span',{'id':'Voix_françaises'}) #find a span wt id
if span_with_voix_fr: # the first kind of format, there'll be other formats
    df_vf = pd.DataFrame()
    ul_vf = span_with_voix_fr.find_next('ul') #the span's next ul is what we want
    # print(ul_vf.text)
    li_list = ul_vf.find_all('li',recursive=False)[:-1]
    # simply we don't cnt the "additional voice" actor (and some unwanted troublesome stuff :)
    # for li in li_list:
    #     print(li.text)
    ind = 0
    for l in li_list:
        if ':' not in list(l.text):
            break
        else:
            act, perso = l.text.split(':')
            # print(f"{act.strip()=}, {perso.strip()=}")
            # df1 = pd.DataFrame({'a':1,'b':2})
            perso = perso.strip()
            if perso.find('/') != -1:
                p1,p2 = perso.split('/')
                p_list = [p1.strip(),p2.strip()]
                print(f"{p_list=}")
            else:
                p_list = [perso]
            # dict_res = {'film':math.nan,
            #             'acteur_vf':math.nan,
            #             'personnage':math.nan}
            # df2 = pd.DataFrame(dict_res,index=[ind])
            for p in p_list:
                df_vf = pd.concat([df_vf,pd.DataFrame({'film':film_title_fr, # SHOULD BE CHANGED TO FILM ID
                                    'acteur_vf':act.strip(),
                                    'personnage':p},
                                    index=[ind])])
            # df_vf = pd.concat([df_vf,df2],ignore_index=True)
            ind += 1
    print(f"{df_vf.shape=}")
    print(f"{df_vf}")
# print(f"{ul_vf=}")


# imdb: tsv
# start = time.time()
# p = pd.read_csv("data-5.tsv",sep='\t') 
# over = time.time()
# print(p['category'].unique())
# print(f"{over-start=}") #29s for 2.66GB
    

# ## trouver le pays d'un film
# film_en = prefix_en + film_title_en
# request_text_en = request.urlopen(film_en).read()
# soup_en = bs4.BeautifulSoup(request_text_en,"html.parser")

# tab = soup_en.find_all("table",attrs={"class":"infobox vevent"})[0] #the first table

# ## release date
# release_date_text = tab.find("th",string="Release date").find_next_sibling().text
# release_date = re.search(r"(\d{4}-\d{1,2}-\d{1,2})",release_date_text)
# print(release_date.group()) #str
# ## country
# # tds = tab.find_all("td",attrs={"class":"infobox-data"})
# country = tab.find("th",string="Country").find_next_sibling("td").text
# # print(country)