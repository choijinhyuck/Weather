import city_table, Keys, GetResponse

url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/"
feature = "getVilageFcst"
serviceKey = Keys.serviceKey
nx = city_table.result["격자 X"].values[0]
ny = city_table.result["격자 Y"].values[0]

contents = GetResponse.GetResponse(url, feature, serviceKey, nx, ny)

for key in contents.fcst:
    print(key, contents.fcst[key])
