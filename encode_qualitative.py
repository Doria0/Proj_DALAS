from sklearn.decomposition import PCA
from sklearn.preprocessing import OneHotEncoder
import pandas as pd

import data_utils as util

## exp for executing alone
# file = 'data_2020-2024.tsv'
# df = util.clean_data(pd.read_csv(file, sep='\t'))

def encode_decomp(df,features,code='onehot'):
    """
    Args:
        df: Dataframe, containing all original qualitative features
        features: list, quali features to be encoded
    """
    # 假设df是您的DataFrame，"Pays"是需要进行one-hot编码的特征
    encoder = OneHotEncoder(sparse=False)
    feature_encoded = encoder.fit_transform(df[features])

    # 使用PCA进行降维
    pca = PCA(n_components=0.95)  # 保留95%的方差
    feature_reduced = pca.fit_transform(feature_encoded)

    # 将降维后的数据转换回DataFrame，用于后续的分析或建模
    df_feature_reduced = pd.DataFrame(feature_reduced)

    return df_feature_reduced
