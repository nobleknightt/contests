import json
import uuid

from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

from bs4 import BeautifulSoup


def fetch_atcoder_contests() -> list[dict]:

    URL = "https://atcoder.jp/contests"

    contests = []

    response = requests.get(URL)

    if response.ok:

        html = response.content.decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find_all(id="contest-table-upcoming")[0].find_all("tr")

        for row in table[1:]:
            
            """
            >>> print(row)
            <tr>
            <td class="text-center"><a href="http://www.timeanddate.com/worldclock/fixedtime.html?iso=20220827T2100&amp;p1=248" target="blank"><time class="fixtime fixtime-full">2022-08-27 21:00:00+0900</time></a></td>
            <td>
            <span aria-hidden="true" data-placement="top" data-toggle="tooltip" title="Algorithm">Ⓐ</span>
            <span class="user-blue">◉</span>
            <a href="/contests/abc266">AtCoder Beginner Contest 266</a>
            </td>
            <td class="text-center">01:40</td>
            <td class="text-center"> - 1999</td>
            </tr>
            """

            title = row.contents[3].contents[5].contents[0]
            url = f"https://atcoder.jp{row.contents[3].contents[5].get('href')}"
            start_time = datetime.strptime(row.contents[1].contents[0].contents[0].contents[0], "%Y-%m-%d %H:%M:%S%z").astimezone(ZoneInfo("Asia/Kolkata"))
            hours, minutes = map(int, row.contents[5].contents[0].split(":"))
            end_time = start_time + timedelta(minutes=minutes, hours=hours)
            duration = end_time - start_time

            contests.append({                
                "id": uuid.uuid4().hex,
                "platform": "AtCoder",
                "title": title,
                "url": url,
                "start_time": start_time.isoformat(),
                "duration": duration.seconds
            })

    return contests


def fetch_leetcode_contests() -> list[dict]:

    URL  = "https://leetcode.com/graphql"

    body = """
    {
        allContests {
            title
            titleSlug
            startTime
            duration
        }
    }
    """

    contests = []

    response = requests.get(URL, json={"query" : body})

    if response.ok:

        response = response.json()
        contests_data = response["data"]["allContests"]
        
        for data in contests_data:

            """
            >>> print(data)
            {
                'title': 'Biweekly Contest 86',
                'titleSlug': 'biweekly-contest-94',
                'startTime': 1662215400, 
                'duration': 5400
            }
            """

            title = data["title"]
            url   = f"https://leetcode.com/contest/{data['titleSlug']}"
            start_time = datetime.fromtimestamp(int(data["startTime"])).astimezone(ZoneInfo("Asia/Kolkata"))
            end_time = start_time + timedelta(seconds=int(data["duration"]))
            if end_time <= datetime.now(tz=ZoneInfo("Asia/Kolkata")): 
                continue # include ongoing and upcoming contests only 
            duration = end_time - start_time

            contests.append({                
                "id": uuid.uuid4().hex,
                "platform": "LeetCode",
                "title": title,
                "url": url,
                "start_time": start_time.isoformat(),
                "duration": duration.seconds
            })

    return contests

contests = (
    fetch_atcoder_contests() + 
    fetch_leetcode_contests()
)

with (Path(__file__).parent / "contests-schedule-minified.json").open("w") as f:
    json.dump(contests, f)

with (Path(__file__).parent / "contests-schedule.json").open("w") as f:
    json.dump(contests, f, indent=4)
