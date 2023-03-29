import pandas as pd

cities = pd.read_csv("data/city_table.csv", encoding="CP949")
post_cities = cities[["1단계", "2단계", "3단계", "격자 X", "격자 Y"]]
post_cities = post_cities[:-2]

si = "대전광역시"
gun = "유성구"
dong = "신성동"

df_idx = (post_cities["1단계"] == si) & (post_cities["2단계"] == gun) & (post_cities["3단계"] == dong)
result = post_cities[df_idx]
