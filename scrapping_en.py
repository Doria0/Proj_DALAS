import bs4
import lxml
import pandas as pd
import urllib
import numpy as np
import math
from urllib import request
import data_utils as util
import re
import time

url = "https://en.wikipedia.org/wiki/Spirited_Away"


def get_date(date:str):
  """
  "(YYYY-MM-DD)" --> (YYYY, MM, DD)
  Return: list
  """
  date_wt_prts = re.search(r"\([\d|-]*\)",date)
  if date_wt_prts is not None: #if found
    date_wt_prts = date_wt_prts.group(0)
    return date_wt_prts[1:-1].split('-')
  else: return [math.nan]

def get_running_time(duree:str):
   rt = re.search(r"[\d]* minutes",duree)
   # add: mins
   if rt is not None: # if found
    return re.search(r"[\d]*",rt.group(0)).group(0)
   else: return math.nan

def remove_notes(line):
  """Enlève une note entre crochets
  Arg:
    line: string, the input
  Return:
    string, the line except []
  """
  n = len(line)
  i_start = -1
  i_end = -1
  for i in range(n):
    if line[i] == '[':
      i_start = i
    if line[i] == ']':
      i_end = i
      break
  if i_start == -1:
    # print(f"{i_start=}")
    return line
  return line[:i_start] + line[i+1:]

def remove_all_notes(line):
  """Enlève toutes les notes entre crochets"""
  res = line
  prev_len_line = len(line)
  act_len_line = 0
  while prev_len_line != act_len_line:
    prev_len_line = act_len_line
    res = remove_notes(res)
    act_len_line = len(res)
  return res

def convert_money(liste_str):
  """
  "$XX.X XXXXXX" --> (nan, XXXXXXXX)
  ou
  "$XX.X-YY.Y XXXXXXXXXX" --> (XXXXXXXX, YYYYYYYYY)
  """
#   values = liste_str[0][1:].split('–')
  values = liste_str[0][1:].split('-')
  if len(values) == 1:
    value_min = math.nan
  else:
    vmin = "".join(list(filter(str.isdigit,values[0]))) # can't convert str "123,456" to float directly
    if vmin != '':
        value_min = float(vmin)
    else: value_min = math.nan
  vmax = "".join(list(filter(str.isdigit,values[-1])))
  if vmax != '':
    value_max = float(vmax)
  else: value_max = math.nan
  if len(liste_str) >= 2: # if there's a unity written as str for the budget
    match liste_str[1]:
        case "million" : return value_min * (10**6), value_max * (10**6)
        case "billion" : return value_min * (10**9), value_max * (10**9) # pour les pays anglophones, 1 billion est équivalent au 1 milliard en France
        # case _ : return None  # TypeError: 'NoneType' object is not subscriptable
  return value_min, value_max

dict_res = {
    "Tconst du film" : math.nan,
    "Titre du film" : math.nan,
    "Jour de sortie" : math.nan,
    "Mois de sortie" : math.nan,
    "Année de sortie" : math.nan,
    "Durée" : math.nan,
    "Pays" : math.nan,
    "Langage" : math.nan,
    "Budget min" : math.nan,
    "Budget max" : math.nan,
    "Box office min" : math.nan,
    "Box office max" : math.nan
}
index_list = []

#executable
def scrap_en(lignes,dict_res,index_list,ind):
    # index_list[:] = [ind]
    for ligne in lignes:
        ths = ligne.find_all("th")
        for th in ths:
            print(f"{th.text=}")
            match th.text:
                case "Release date" :
                    # print("text of td: {}".format(ligne.find("td").text))
                    date = remove_all_notes(ligne.find("td").text) # Enlève toutes les notes entre crochets
                     # (YYYY-MM-DD)
                    date = get_date(date) # YYYY, MM, DD
                    if len(date) == 3:
                        dict_res["Année de sortie"] = date[0]
                        dict_res["Mois de sortie"] = date[1]
                        dict_res["Jour de sortie"] = date[2]
                    elif len(date) == 2: 
                    # if we've got less elements, they must be 'year,month' or only 'year', otherwise they can't be meaningful
                        dict_res["Année de sortie"] = date[0]
                        dict_res["Mois de sortie"] = date[1]
                    elif len(date) == 1:
                        dict_res["Année de sortie"] = date[0]
                case "Release dates":
                    dates = remove_all_notes(ligne.find("td").text).split('\n') # sépare les lignes, enlève les notes entre crochets
                    dates = [elem for elem in dates if elem != ''] # enlève les éventuels éléments vides
                    date = dates[0] # s'il y a plusieurs dates, on prend seulement la 1ère
                    date = get_date(date) # (YYYY-MM-DD) --> YYYY, MM, DD
                    if len(date) == 3:
                        dict_res["Année de sortie"] = date[0]
                        dict_res["Mois de sortie"] = date[1]
                        dict_res["Jour de sortie"] = date[2]
                    elif len(date) == 2: 
                        dict_res["Année de sortie"] = date[0]
                        dict_res["Mois de sortie"] = date[1]
                    elif len(date) == 1:
                        dict_res["Année de sortie"] = date[0]
                case "Running time" :
                    print("text of td: {}".format(ligne.find("td").text))
                    duree = remove_all_notes(ligne.find("td").text)
                    duree = get_running_time(duree) # durée (en minutes mais l'unité est toujours la même donc pas besoin de l'enregistrer)
                    dict_res["Durée"] = duree
                case "Country" :
                    if ligne.find("td") is not None: # there's some ambiguation, eg:'https://en.wikipedia.org/wiki/Milk'
                        pays = remove_all_notes(ligne.find("td").text)
                        dict_res["Pays"] = pays
                case "Countries" :
                    if ligne.find("td") is not None:
                        pays = remove_all_notes(ligne.find("td").text).split('\n') # sépare les lignes, enlève les notes entre crochets
                        pays = [elem for elem in pays if elem != ''] # enlever les '' vides
                        index_list[:] = [ind for i in range(len(pays))] # met à jour la liste d'index (pour le dataframe plus tard)
                        dict_res["Pays"] = pays
                case "Language" :
                    if ligne.find("td") is not None:
                      lang = remove_all_notes(ligne.find("td").text)
                      dict_res["Langage"] = lang
                case "Budget" :
                    budget = remove_all_notes(ligne.find("td").text).split()
                    budget = convert_money(budget) # enlève le $, convertit million/billion dans la valeur
                    dict_res["Budget min"] = budget[0]
                    dict_res["Budget max"] = budget[1]
                case "Box office" :
                    box_office = remove_all_notes(ligne.find("td").text).split()
                    box_office = convert_money(box_office) # enlève le $, convertit million/billion dans la valeur
                    dict_res["Box office min"] = box_office[0]
                    dict_res["Box office max"] = box_office[1]
                



if __name__ == '__main__':
    start = time.time()
    all_film_titles = util.read_titles("data-5.tsv")[2000:3000] # title.basics
    # traverse all film titles in imdb dataset
    request_texts = []
    ind = 1111 #719/2000, 1110/3000
    # index_list = [ind]
    for (index,film_title) in all_film_titles:
        try:
            url_en = util.prefix_en + film_title + '_(film)'
            print(f"{url_en=}")
            request_text = request.urlopen(url_en).read()
            dict_res['Tconst du film'] = index
            dict_res['Titre du film'] = util.recover_symbols(film_title)
            # request_texts.append(req)
            # print(f"{type(req):}") #'bytes'
        except:
            url_en = util.prefix_en + film_title
            print(f"{url_en=}")
            try:
              request_text = request.urlopen(url_en).read()
              dict_res['Tconst du film'] = index
              dict_res['Titre du film'] = util.rep_symbols(film_title)
            except:
               request_text = math.nan
            # continue
        # print(request_texts[:5])
    # df_all = pd.DataFrame()
    # for request_text in request_texts:
        # print(f"{request_text=}")
        if request_text is not math.nan:
            index_list[:] = [ind]
            page = bs4.BeautifulSoup(request_text, "lxml")
            table_info = page.find("table")
            if table_info is not None: # if a table exists
                lignes = table_info.find_all("tr")
                scrap_en(lignes,dict_res,index_list,ind)
                # print(f"{index_list=}")
            df = pd.DataFrame(dict_res, index=index_list)
            if ind==0:
                df.to_csv('scrapped_en.tsv',sep='\t',na_rep='\\N',mode='a')
                # write to the file 'scrapped_en.tsv', with seperator \t, representation of nan '\N', 
                # and append to the file if it exists
            else:
                df.to_csv('scrapped_en.tsv',sep='\t',na_rep='\\N',header=False,mode='a') # don't write out column names
            # df_all = pd.concat([df_all,df])
            ind += 1
            #reset dict after the write
            for key in dict_res:
               dict_res[key] = math.nan
        # print(df_all[:5])
        # util.save_scrapping('scrapped_en.tsv',df=df_all)
    end = time.time()
    print("Time Consumed:{} mins".format((end-start)/60.0))