import datetime, requests, json, time


def BaseTime():
    # now = datetime.datetime.strptime(temp, "%Y%m%d %H%M") # Test 용 코드
    now = datetime.datetime.now()  # 현재 시간 가져오는 실제 코드
    date = now.strftime("%Y%m%d")
    hour = int(now.strftime("%H"))
    minute = now.strftime("%M")
    hour -= 1

    if hour < 2:
        date = now.date() + datetime.timedelta(days=-1)
        date = date.strftime("%Y%m%d")
        hour = 23
    else:
        hour -= (hour - 2) % 3

    hour = "0" + str(hour) if hour < 10 else str(hour)

    return (
        date,
        hour + "00",
        now.strftime("%Y%m%d"),
        now.strftime("%H%M"),
        now,
    )


class GetResponse:
    def __init__(self, url, feature, serviceKey, nx, ny):
        self.fixed = (
            f"{url}{feature}?serviceKey={serviceKey}&dataType=JSON&numOfRows=2000&nx={nx}&ny={ny}"
        )
        (
            self.base_date,
            self.base_time,
            self.now_date,
            self.now_time,
            fcst_time,
        ) = BaseTime()
        fcst_time = fcst_time + datetime.timedelta(hours=1)
        self.fcst_now = (
            fcst_time.strftime("%Y%m%d"),
            fcst_time.strftime("%H00"),
        )
        self.run()

    def Request(self, date, time):
        query = self.fixed + f"&base_date={date}&base_time={time}"
        response = requests.get(query)
        if response.status_code != 200:
            print(
                "Error",
                "status_code:",
                response.status_code,
            )
            return False
        result = json.loads(response.text)
        try:
            # print(json.dumps(result, indent=4))  # json 내용 구조적으로 확인용
            contents = result["response"]["body"]["items"]["item"]  # list 자료형 결과를 반환
            return contents
        except:
            print(f"Error message: Invalid request {date} {time}")
            return False

    def merge(self):
        if self.base_date != self.now_date:
            contents = self.Request(self.base_date, self.base_time)
            return contents
        else:
            yesterday = datetime.datetime.strptime(self.base_date, "%Y%m%d") + datetime.timedelta(
                days=-1
            )
            yesterday = yesterday.strftime("%Y%m%d")
            pre_contents = self.Request(yesterday, "2300")
            time.sleep(1)
            post_contents = self.Request(self.base_date, self.base_time)

            temp_pre = []
            for pre_content in pre_contents:
                if pre_content["fcstDate"] == self.now_date:
                    if int(pre_content["fcstTime"][:2]) > int(self.base_time[:2]):
                        break
                    else:
                        temp_pre.append(pre_content)
            return temp_pre + post_contents

    def run(self):
        contents = self.merge()
        ThreeDaysLater = datetime.datetime.strptime(self.now_date, "%Y%m%d") + datetime.timedelta(
            days=3
        )
        ThreeDaysLater = ThreeDaysLater.strftime("%Y%m%d")
        self.fcst = {
            "TMP": [],
            "TMN": [],
            "TMX": [],
            "SKY": [],
            "WSD": [],
            "POP": [],
            "REH": [],
            "PTY": [],
        }

        for content in contents:
            if content["fcstDate"] == ThreeDaysLater:
                break
            if content["category"] in self.fcst:
                fcstDate = content["fcstDate"]
                fcstTime = content["fcstTime"]
                fcstValue = content["fcstValue"]
                self.fcst[content["category"]].append(
                    (
                        fcstDate,
                        fcstTime,
                        fcstValue,
                    )
                )
