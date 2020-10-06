import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

ZHVI="ZHVI"


def normalized_lr(data, column):
    lr = LinearRegression()
    X = np.arange(len(data.index)).reshape(-1, 1)
    first = data[column].values[0]
    Y = data[column].apply(lambda x: x / first).values.reshape(-1, 1)
    lr.fit(X, Y)
    return lr.score(X,Y), lr.coef_[0][0] * 12

def sorted_counties(df, months=5):
    fdf = df.melt(id_vars=["RegionName", "StateName"], var_name="Date", value_name=ZHVI)
    counties = fdf["RegionName"].unique()
    county_dfs = {}
    for c in counties:
        county_dfs[c] = (fdf.loc[fdf['RegionName'] == c])
    sorted = []
    for c in counties:
        county_df = county_dfs[c].dropna()
        r_squared, coef = normalized_lr(county_df, ZHVI)
        growths.append((c, coef, r_squared))
    sorted.sort(key=lambda x: x[1], reverse=True)
    return sorted


df = pd.read_csv("county.csv", sep=",")
df.drop(df.columns[[0, 1, 3, 5, 6, 7, 8]], axis=1, inplace=True)
print(df.head())

growths = sorted_counties(df)