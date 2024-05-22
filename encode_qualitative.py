from sklearn.decomposition import PCA
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np

import data_utils as util

## exp for executing alone
file = 'data/2020-2024_cleaned.tsv'
df_cleaned = util.clean_data(pd.read_csv(file, sep='\t'),cols_retain=['Tconst du film','Box office max'])

df_cleaned.rename(columns={'Tconst du film': 'tconst'}, inplace=True)
df_title_basics = pd.read_csv('title.basics.tsv',sep='\t')
df_title_basics = df_title_basics[['tconst','genres']]
df_genres = util.join_data(dfs=[df_cleaned,df_title_basics],keys=['tconst'],manners=['left'])
df_genres = util.clean_data(df_genres,cols_na=['genres'])
df_genres.to_csv('genres.tsv',sep='\t')

cnt_genres = dict() # count all distinct genres
for s in df_genres['genres'].values:
    vals = s.split(',')
    for val in vals:
        if val in cnt_genres:
            cnt_genres[val] += 1
        else: cnt_genres[val] = 1
print(cnt_genres, len(cnt_genres))
# {'Action': 244, 'Adventure': 189, 'Fantasy': 76, 'Comedy': 253, 'Drama': 503, 'Thriller': 122, 'Horror': 112,
# 'Mystery': 50, 'Crime': 90, 'Romance': 85, 'War': 10, 'Musical': 18, 'Biography': 66, 'Animation': 87, 'Sci-Fi': 49,
# 'Short': 191, 'Sport': 20, 'Family': 48, 'History': 50, 'Documentary': 36, 'Music': 21, '\\N': 2, 'Western': 1, 'Adult': 1}

def encode_decomp(df,features,code='onehot'):
    """
    Args:
        df: Dataframe, containing all original qualitative features
        features: list, quali features to be encoded
    """
    # onehot encode
    encoder = OneHotEncoder()#no sparse=False in new versions of scikit-learn
    feature_encoded = encoder.fit_transform(pd.DataFrame(df[features]))
    feature_encoded_dense = feature_encoded.toarray()# 转换为密集矩阵

    # PCA for dim reduction
    pca = PCA()  # n_components=2 # keep 2 main components as new features
    X_new = pca.fit_transform(feature_encoded)
    # if we want to keep some percent of variance
    explained_variance_ratio_cumulative = np.cumsum(pca.explained_variance_ratio_)
    threshold = 0.95 # 23 dim => 0.95:14, 0.80:9
    n_components = np.argmax(explained_variance_ratio_cumulative >= threshold) + 1
    pca = PCA(n_components=n_components)
    feature_reduced = pca.fit_transform(feature_encoded)

    # transform to dataframe after dim reduction
    col_names = []
    for i in range(n_components):
        col_names.append('PC_genres_' + str(i))
    df_feature_reduced = pd.DataFrame(feature_reduced,columns=col_names)

    return df_feature_reduced

df_genres_pre_enc = df_genres.drop('genres',axis=1).join(df_genres['genres'].str.split(',').explode().reset_index(drop=True))
df_genres_pre_enc.to_csv('df_genres_pre_enc.tsv',sep='\t')
# print(df_genres_pre_enc.dtypes)
# df_genres_encoded = pd.get_dummies(df_genres_pre_enc,columns=['genres'])
df_genres_enc_decomp = encode_decomp(df_genres_pre_enc,'genres')
df_genres_enc_decomp.to_csv('data/PCA/df_genres_enc_decomp.tsv',sep='\t')