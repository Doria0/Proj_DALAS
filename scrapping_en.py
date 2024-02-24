import bs4
import lxml
import pandas as pd
import urllib
import numpy as np
import math
from urllib import request
import data_utils as util
import re

url = "https://en.wikipedia.org/wiki/Spirited_Away"


def get_date(date:str):
  """
  "(YYYY-MM-DD)" --> (YYYY, MM, DD)
  Return: list
  """
  date_wt_prts = re.search(r"\([\d|-]*\)",date).group(0)
  return date_wt_prts[1:-1].split('-')

def get_running_time(duree:str):
   rt = re.search(r"[\d]* minutes",duree)
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
  values = liste_str[0][1:].split('–')
  if len(values) == 1:
    value_min = math.nan
  else:
    value_min = float(values[0])
  value_max = float(values[-1])
  match liste_str[1]:
    case "million" : return value_min * (10**6), value_max * (10**6)
    case "billion" : return value_min * (10**9), value_max * (10**9) # pour les pays anglophones, 1 billion est équivalent au 1 milliard en France
    case _ : return None

dict_res = {
    "Jour de sortie" : math.nan,
    "Mois de sortie" : math.nan,
    "Année de sortie" : math.nan,
    "Durée" : math.nan,
    "Pays" : math.nan,
    "Budget min" : math.nan,
    "Budget max" : math.nan,
    "Box office min" : math.nan,
    "Box office max" : math.nan
}
index_list = [0]

#executable
def scrap_en(lignes,dict_res):
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
                    pays = remove_all_notes(ligne.find("td").text)
                    dict_res["Pays"] = pays
                case "Countries" :
                    pays = remove_all_notes(ligne.find("td").text).split('\n') # sépare les lignes, enlève les notes entre crochets
                    pays = [elem for elem in pays if elem != ''] # enlever les '' vides
                    index_list = [i for i in range(len(pays))] # met à jour la liste d'index (pour le dataframe plus tard)
                    dict_res["Pays"] = pays
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
    all_film_titles = util.read_titles("data-2.tsv")[:10]
    # traverse all film titles in imdb dataset
    request_texts = []
    for film_title in all_film_titles:
        url_en = util.prefix_en + film_title
        print(f"{url_en=}")
        try:
            req = request.urlopen(url_en).read()
            request_texts.append(req)
            # print(f"{type(req):}") #'bytes'
        except:
            request_texts.append(math.nan)
    # print(request_texts[:5])
    df_all = pd.DataFrame()
    ind = 0
    for request_text in request_texts:
        # print(f"{request_text=}")
        if request_text is not math.nan:
            page = bs4.BeautifulSoup(request_text, "lxml")
            table_info = page.find("table")
            lignes = table_info.find_all("tr")
            scrap_en(lignes,dict_res)
        df = pd.DataFrame(dict_res, index=[ind])
        df_all = pd.concat([df_all,df])
        ind += 1
    # print(df_all[:5])
    util.save_scrapping('scrapped_en.tsv',df=df_all)