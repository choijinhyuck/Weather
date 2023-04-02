import pandas as pd


def find_coord(si, gun, dong):
    cities = pd.read_csv("data/city_table.csv", encoding="CP949")
    post_cities = cities[["1단계", "2단계", "3단계", "격자 X", "격자 Y"]]
    post_cities = post_cities[:-2]

    df_idx = (post_cities["1단계"] == si) & (post_cities["2단계"] == gun) & (post_cities["3단계"] == dong)
    result = post_cities[df_idx]
    nx = result["격자 X"].values[0]
    ny = result["격자 Y"].values[0]
    return nx, ny
