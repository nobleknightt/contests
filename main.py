from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import requests

from jinja2 import Environment, FileSystemLoader

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
                "platform": "LeetCode",
                "title": title,
                "url": url,
                "start_time": start_time,
                "duration": duration
            })

    return contests

environment = Environment(loader=FileSystemLoader('templates/'))
template = environment.get_template('index.html')

contests = []
contests.extend(fetch_leetcode_contests())

with open('index.html', mode='w', encoding='utf-8') as f:
    f.write(template.render({'contests': contests}))
