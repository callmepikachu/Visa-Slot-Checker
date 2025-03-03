import requests
from bs4 import BeautifulSoup
import time
from playsound import playsound
MONTH = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}

schedule_id = '66449739'
country = 'en-gb'  # replace it with your desired country code
session = 'ZwVc7uBUD%2BySACwLMnC9DIxvwNsNM8P2KeeF9AePCk2NKpycx%2BAJwU6leiJzDz9UTY7W1jE2cby3fnIvM3w7r0IaXdjipwc55e55foAXx8vDJWS6mvG40UbW5jau4JslvBCTgj2QM7arYzGO5hKfWh212h96GeTE%2BzJm6xCOC7M1LsxO9qa61XcU7En3nG3U6gGiwaM0LOh%2FmO0GFeZYaoOYOQdm6VTF1WmF2PZW05x069brgvAp6qUO5qF7ZWX%2BnmtUKH3Q%2Fu%2FfGhUVDav8zgznNBX0tfacjPWJAkFLc%2BXP0VWavEQyymdoZudT9G5H0WqAOhOKTWl9FJdL%2FzAEDumybQQ%2Bt0D9%2FBFFBnHVR1X0ns4t3ejEf3VBGOQaiO%2BVD2FfamXZ60np8undu3Ffw62wNh7LXlQ6YJK9bu6MvP2RBBUdZu5OKSyoqpFpPqYb%2Fa6xvI6i2W%2FDDltnxe9bxeSnIZ6yjpedYOIFMibYGTObveY6Bk%2BZ0mbCgflnat7r9UI%2FT38%2Bnbfu0E8H0h%2BRF8yCV8VvraLHKSxYGvp1lLrJtqKQEas6KiOA2ot1f2FP%2BPZAihpLtPoOCUtk%2BCJXu%2FtpPRSLs80kP%2BoeLBsXxhsAH9RuXOtDdDkjWBzybOJoqSvaMzMw2NWr9XKTx3tYYHRPLXnpVYDD6WSPV%2FFXUtTmIVVJsEy9We5z5XZUY9eoFkg05W5U45%2FJCa3mDRd3SlT%2Bo0nLy5M8gHiCDC4coucmEE97VXaaoeqA2arTJn%2Bsg7f%2BHTKXvP035IKoL%2B%2BNqTZ4hwy33rQi2xKUWhpyGqeVZMID%2FcsmNoFa8vvoRGz9WJE%3D--Iken4TlzkM02cks0--ZLxUaCaUT2A0%2BN6brH2kow%3D%3D'
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"


def refresh(country_code, schedule_id, session):
    req = requests.Session()
    headers = {
        "User-Agent": user_agent,
        "Referer": "https://ais.usvisa-info.com/%s/niv/schedule/%s/continue_actions" % (country_code, schedule_id),
        "Cookie": "_yatri_session=" + session

    }
    r = req.get("https://ais.usvisa-info.com/%s/niv/schedule/%s/payment" % (country_code, schedule_id), headers=headers)
    if r.status_code != 200:
        print("Error")
    soup = BeautifulSoup(r.text, "html.parser")
    time_table = soup.find("table", {"class": "for-layout"})
    result = []

    if time_table:
        for tr in time_table.find_all("tr"):
            tds = tr.find_all("td")
            if not len(tds) == 2:
                continue
            place = tds[0].text
            if place != "Belfast":
                continue
            date_str = tds[1].text
            s = date_str.split()
            year, month, day = 0, 0, 0
            if len(s) >= 3 and s[0] != "No":
                day_str, month_str, year_str = s[-3], s[-2].replace(",", ""), s[-1]
                year, month, day = int(year_str), MONTH[month_str], int(day_str)
            # result.append([place, (year, month, day)])
            if year == 0:
                continue
            result.append(f"{place}的号码：{year}年, {month}月, {day}日")
            # add your condition here
            # trigger an alarm when a slot is found
            print("\a")

    session = r.cookies["_yatri_session"]
    return result, session


if __name__ == '__main__':
    while True:
        result, session = refresh(country, schedule_id, session)
        print(result)
        print(session)
        time.sleep(300)  # sleep 5min