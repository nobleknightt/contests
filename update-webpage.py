from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo # requires >=python3.9
# for older python versions, use pypi.org/project/backports.zoneinfo

import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

@dataclass
class ContestData:
    platform : str
    title : str
    url : str
    start_time : datetime
    duration : timedelta

    def __hash__(self) -> int:
        return hash(repr(self))

    def __repr__(self) -> str:
        return f"ContestData({self.platform}, {self.title}, {self.start_time}, {self.duration})"

def fetch_atcoder_contests() -> list[ContestData]:

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

            contests.append(ContestData("AtCoder", title, url, start_time, duration))

    return contests

def fetch_codechef_contests() -> list[ContestData]:

    URL = "https://www.codechef.com/api/list/contests/all"

    payload = {
        "sort_by": "START",
        "sorting_order": "asc",
    }

    contests = []

    response = requests.get(URL, params=payload)

    if response.ok:

        response = response.json()
        contests_data = response["present_contests"] + response["future_contests"]

        for data in contests_data:
            
            """
            >>> print(data)
            {
                'contest_code': 'START54', 
                'contest_name': 'Starters 54 (Rated for Div 2, 3 & 4)', 
                'contest_start_date': '31 Aug 2022  20:00:00', 
                'contest_end_date': '31 Aug 2022  23:00:00', 
                'contest_start_date_iso': '2022-08-31T20:00:00+05:30', 
                'contest_end_date_iso': '2022-08-31T23:00:00+05:30', 
                'contest_duration': '180', 
                'distinct_users': 0
            }
            """

            try:
                title = data["contest_name"]
                url   = f"https://www.codechef.com/{data['contest_code']}"
                start_time = datetime.fromisoformat(data["contest_start_date_iso"])
                end_time   = datetime.fromisoformat(data["contest_end_date_iso"])
                duration   = end_time - start_time
            except:
                continue

            contests.append(ContestData("CodeChef", title, url, start_time, duration))

    return contests

def fetch_codeforces_contests() -> list[ContestData]:

    URL = "https://codeforces.com/api/contest.list"

    contests = []

    response = requests.get(URL)

    if response.ok:

        response = response.json()
        contests_data = response["result"]

        for data in contests_data:
            
            """
            >>> print(data)
            {
                'id': 1723, 
                'name': 'ICPC 2022 Online Challenge powered by HUAWEI - Problem 1', 
                'type': 'IOI', 
                'phase': 'BEFORE', 
                'frozen': False, 
                'durationSeconds': 1296000, 
                'startTimeSeconds': 1663200000, 
                'relativeTimeSeconds': -1747109
            }
            """

            title = data["name"]
            url   = f"https://codeforces.com/contests/{data['id']}"
            start_time = datetime.fromtimestamp(float(data["startTimeSeconds"]), tz=ZoneInfo("Asia/Kolkata"))
            end_time   = start_time + timedelta(seconds=float(data["durationSeconds"]))
            if end_time <= datetime.now(tz=ZoneInfo("Asia/Kolkata")): 
                continue # include ongoing and upcoming contests only                           
            duration   = end_time - start_time

            contests.append(ContestData("Codeforces", title, url, start_time, duration))

    return contests

def fetch_code_jam_contests() -> list[ContestData]:

    URL = "https://codingcompetitions.withgoogle.com/codejam/schedule"

    options = Options()
    options.add_argument("--headless")

    browser = webdriver.Chrome(options=options)
    browser.get(URL)
    browser.implicitly_wait(5) # wait 5 seconds to load dynamic content

    contests = []

    try:
        
        schedule_rows = browser.find_elements(By.CLASS_NAME, "schedule-row__upcoming")
        
        for row in schedule_rows:
        
            title, start_time, end_time, *_ = row.text.split("\n")
            start_time = datetime.strptime(
                start_time, "%b %d %Y, %H:%M"
            ).replace(tzinfo=ZoneInfo("UTC")).astimezone(tz=ZoneInfo("Asia/Kolkata"))
            end_time   = datetime.strptime(
                end_time, "%b %d %Y, %H:%M"
            ).replace(tzinfo=ZoneInfo("UTC")).astimezone(tz=ZoneInfo("Asia/Kolkata"))
            duration = end_time - start_time

            contests.append(ContestData("Code Jam", title, URL, start_time, duration))

    except Exception as e:
        print(e)

    browser.quit()

    return contests

def fetch_geeksforgeeks_contests() -> list[ContestData]:

    URL = "https://practiceapi.geeksforgeeks.org/api/vr/events/"

    payload = {
        "type": "contest",
        "sub_type": "upcoming"
    }

    contests = []

    response = requests.get(URL, params=payload)

    if response.ok:

        response = response.json()
        contests_data = response["results"]["upcoming"]

        for data in contests_data:
            
            """
            >>> print(data)
            {
                'slug': 'interview-series-65', 
                'start_time': '2022-08-28T19:00:00', 
                'end_time': '2022-08-28T20:30:00', 
                'banner': {
                    'mobile_url': 'https://media.geeksforgeeks.org/img-practice/banner/interview-series-65-1661154000-mobile.png', 
                    'desktop_url': 'https://media.geeksforgeeks.org/img-practice/banner/interview-series-65-1661154005-desktop.png'
                }, 
                'name': 'Interview Series - 65', 
                'status': 'upcoming', 
                'time_diff': {
                    'days': 0, 
                    'hours': 4, 
                    'mins': 8, 
                    'secs': 13
                }, 
                'type': 3, 
                'date': 'August 28, 2022', 
                'time': '07:00 PM'
            }
            """

            title = data["name"]
            url   = f"https://practice.geeksforgeeks.org/contest/{data['slug']}"
            start_time = datetime.fromisoformat(data["start_time"]).astimezone(ZoneInfo("Asia/Kolkata"))
            end_time   = datetime.fromisoformat(data["end_time"]).astimezone(ZoneInfo("Asia/Kolkata"))
            duration   = end_time - start_time

            contests.append(ContestData("GeeksforGeeks", title, url, start_time, duration))

    return contests

def fetch_hackerearth_contests() -> list[ContestData]:
    
    URL = "https://www.hackerearth.com/challenges"

    contests = []

    response = requests.get(URL)

    if response.ok:

        html = response.content.decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        def extract_challenge_links(class_: str) -> list[str]:

            challenge_links = soup.find(class_=class_).find_all(class_="challenge-card-link")

            challenge_urls = []
            for link in challenge_links:
                challenge_url = link.get("href")
                if not challenge_url.startswith("https"):
                    challenge_url = f"https://www.hackerearth.com{challenge_url}"

                challenge_urls.append(challenge_url)

            return challenge_urls

        challenge_urls = extract_challenge_links("ongoing") + extract_challenge_links("upcoming")

        for challenge_url in challenge_urls:

            def extract_data_try_1() -> dict: 
                
                response = requests.get(challenge_url)
        
                if response.ok:
                    
                    html = response.content.decode("utf-8")
                    soup = BeautifulSoup(html, "html.parser")

                    title      = soup.find(class_="event-title").find(class_="title").contents[0].text.strip()
                    start_time = soup.find(class_="start-time-block").find(class_="regular").contents[0].text.strip()
                    end_time   = soup.find(class_="end-time-block").find(class_="regular").contents[0].text.strip()

                    start_time = datetime.strptime(start_time, "%b %d, %Y, %I:%M %p").replace(tzinfo=ZoneInfo("UTC")).astimezone(tz=ZoneInfo("Asia/Kolkata"))
                    end_time   = datetime.strptime(end_time, "%b %d, %Y, %I:%M %p").replace(tzinfo=ZoneInfo("UTC")).astimezone(tz=ZoneInfo("Asia/Kolkata"))
                    duration   = end_time - start_time

                    return ContestData("HackerEarth", title, challenge_url, start_time, duration)

            def extract_data_try_2() -> dict: 

                response = requests.get(challenge_url)
        
                if response.ok:
                    
                    html = response.content.decode("utf-8")
                    soup = BeautifulSoup(html, "html.parser")

                    title      = soup.find(class_="event-title").contents[0].text.strip()
                    timings    = soup.find_all(class_="timing-text")
                    start_time = timings[0].text.strip()
                    end_time   = timings[1].text.strip()

                    now = datetime.utcnow()

                    start_time = datetime.strptime(start_time, "%b %d, %I:%M %p")
                    end_time   = datetime.strptime(end_time, "%b %d, %I:%M %p")

                    if start_time.month < now.month and end_time.month < now.month:
                        if start_time.month <= end_time.month:      
                            start_time = start_time.replace(
                                year=datetime.now(tz=ZoneInfo("UTC")).year + 1, 
                                tzinfo=ZoneInfo("UTC")
                            ).astimezone(tz=ZoneInfo("Asia/Kolkata")) 
                            end_time = end_time.replace(
                                year=datetime.now(tz=ZoneInfo("UTC")).year + 1, 
                                tzinfo=ZoneInfo("UTC")
                            ).astimezone(tz=ZoneInfo("Asia/Kolkata")) 
                        else: # start_time.month > end_time.month
                            start_time = start_time.replace(
                                year=datetime.now(tz=ZoneInfo("UTC")).year, 
                                tzinfo=ZoneInfo("UTC")
                            ).astimezone(tz=ZoneInfo("Asia/Kolkata"))
                            end_time = end_time.replace(
                                year=datetime.now(tz=ZoneInfo("UTC")).year + 1, 
                                tzinfo=ZoneInfo("UTC")
                            ).astimezone(tz=ZoneInfo("Asia/Kolkata"))
                    elif start_time.month < now.month: # and end_time.month >= now.month
                        start_time = start_time.replace(
                            year=datetime.now(tz=ZoneInfo("UTC")).year, 
                            tzinfo=ZoneInfo("UTC")
                        ).astimezone(tz=ZoneInfo("Asia/Kolkata"))
                        end_time = end_time.replace(
                            year=datetime.now(tz=ZoneInfo("UTC")).year, 
                            tzinfo=ZoneInfo("UTC")
                        ).astimezone(tz=ZoneInfo("Asia/Kolkata"))                    
                    elif end_time.month < now.month: # and start_time.month >= now.month
                        start_time = start_time.replace(
                            year=datetime.now(tz=ZoneInfo("UTC")).year, 
                            tzinfo=ZoneInfo("UTC")
                        ).astimezone(tz=ZoneInfo("Asia/Kolkata"))
                        end_time = end_time.replace(
                            year=datetime.now(tz=ZoneInfo("UTC")).year + 1, 
                            tzinfo=ZoneInfo("UTC")
                        ).astimezone(tz=ZoneInfo("Asia/Kolkata"))
                    else: # start_time.month >= now.month and end_time.month >= now.month
                        start_time = start_time.replace(
                            year=datetime.now(tz=ZoneInfo("UTC")).year, 
                            tzinfo=ZoneInfo("UTC")
                        ).astimezone(tz=ZoneInfo("Asia/Kolkata"))
                        end_time = end_time.replace(
                            year=datetime.now(tz=ZoneInfo("UTC")).year, 
                            tzinfo=ZoneInfo("UTC")
                        ).astimezone(tz=ZoneInfo("Asia/Kolkata"))

                    duration   = end_time - start_time

                    return ContestData("HackerEarth", title, challenge_url, start_time, duration)

            data_extracters = [extract_data_try_1, extract_data_try_2]
            for extracter in data_extracters:
                try:
                    contest_data = extracter()
                    if contest_data is not None:
                        contests.append(contest_data)
                        break
                except Exception as e:
                    pass

    return contests

def fetch_hackerrank_contests() -> list[ContestData]:

    URL = "https://www.hackerrank.com/contests"

    contests = []

    return contests

def fetch_hash_code_contests() -> list[ContestData]:

    URL = "https://codingcompetitions.withgoogle.com/hashcode/schedule"

    options = Options()
    options.add_argument("--headless")

    browser = webdriver.Chrome(options=options)
    browser.get(URL)
    browser.implicitly_wait(5) # wait 5 seconds to load dynamic content

    contests = []

    try:
        
        schedule_rows = browser.find_elements(By.CLASS_NAME, "schedule-row__upcoming")
        
        for row in schedule_rows:
        
            title, start_time, end_time, *_ = row.text.split("\n")
            start_time = datetime.strptime(
                start_time, "%b %d %Y, %H:%M"
            ).replace(tzinfo=ZoneInfo("UTC")).astimezone(tz=ZoneInfo("Asia/Kolkata"))
            end_time   = datetime.strptime(
                end_time, "%b %d %Y, %H:%M"
            ).replace(tzinfo=ZoneInfo("UTC")).astimezone(tz=ZoneInfo("Asia/Kolkata"))
            duration = end_time - start_time

            contests.append(ContestData("Hash Code", title, URL, start_time, duration))

    except Exception as e:
        print(e)

    browser.quit()

    return contests

def fetch_interviewbit_contests() -> list[ContestData]:

    URL = "https://www.interviewbit.com/contests"

    contests = []

    return contests

def fetch_kick_start_contests() -> list[dict]:

    URL = "https://codingcompetitions.withgoogle.com/kickstart/schedule"

    options = Options()
    options.add_argument("--headless")

    browser = webdriver.Chrome(options=options)
    browser.get(URL)
    browser.implicitly_wait(5) # wait 5 seconds to load dynamic content

    contests = []

    try:
        
        schedule_rows = browser.find_elements(By.CLASS_NAME, "schedule-row__upcoming")
        
        for row in schedule_rows:
        
            title, start_time, end_time, *_ = row.text.split("\n")
            start_time = datetime.strptime(
                start_time, "%b %d %Y, %H:%M"
            ).replace(tzinfo=ZoneInfo("UTC")).astimezone(tz=ZoneInfo("Asia/Kolkata"))
            end_time   = datetime.strptime(
                end_time, "%b %d %Y, %H:%M"
            ).replace(tzinfo=ZoneInfo("UTC")).astimezone(tz=ZoneInfo("Asia/Kolkata"))
            duration = end_time - start_time

            contests.append(ContestData("Kick Start", title, URL, start_time, duration))

    except Exception as e:
        print(e)

    browser.quit()

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

            contests.append(ContestData("LeetCode", title, url, start_time, duration))

    return contests

def fetch_contests(
    atcoder: bool=False, codechef: bool=False, codeforces: bool=False, 
    code_jam: bool=False, geeksforgeeks: bool=False, hackerearth: bool=False,
    hash_code: bool=False, kick_start: bool=False, leetcode: bool=False
) -> list[ContestData]:
    return sorted([
        *(fetch_atcoder_contests() if atcoder else []), 
        *(fetch_codechef_contests() if codechef else []), 
        *(fetch_codeforces_contests() if codeforces else []), 
        *(fetch_code_jam_contests() if code_jam else []), 
        *(fetch_geeksforgeeks_contests() if geeksforgeeks else []), 
        *(fetch_hackerearth_contests() if hackerearth else []), 
        *(fetch_hash_code_contests() if hash_code else []), 
        *(fetch_kick_start_contests() if kick_start else []), 
        *(fetch_leetcode_contests() if leetcode else [])
    ], key=lambda contest: contest.start_time)

def main():

    webpage_content_before_contest_table = """
        <!DOCTYPE html>
        <html lang="en">

        <head>

            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">

            <link rel="shortcut icon" href="./favicon.ico"> 

            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
            <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Source+Code+Pro">

            <title> Contests </title>

            <style>
                /* hide scrollbar for Chrome, Safari and Opera */
                body::-webkit-scrollbar {
                    display: none;
                }
                /* hide scrollbar for IE, Edge and Firefox */
                body {
                    -ms-overflow-style: none;  /* IE and Edge */
                    scrollbar-width: none;  /* Firefox */
                }
            </style>

        </head>

        <body style="font-family: 'Source Code Pro'; font-weight: bold;">

            <div class="d-flex justify-content-around m-2">
                <div class="">
                    <input type="checkbox" id="atcoder" checked>
                    <label for="atcoder"> AtCoder </label>
                </div>
                <div class="">
                    <input type="checkbox" id="codechef" checked>
                    <label for="codechef"> CodeChef </label>
                </div>
                <div class="">
                    <input type="checkbox" id="codeforces" checked>
                    <label for="codeforces"> Codeforces </label>
                </div>
                <div class="">
                    <input type="checkbox" id="code-jam" checked>
                    <label for="code-jam"> Code Jam </label>
                </div>
                <div class="">
                    <input type="checkbox" id="geeksforgeeks" checked>
                    <label for="geeksforgeeks"> GeeksforGeeks </label>
                </div>
                <div class="">
                    <input type="checkbox" id="hackerearth" checked>
                    <label for="hackerearth"> HackerEarth </label>
                </div>
                <div class="">
                    <input type="checkbox" id="hash-code" checked>
                    <label for="hash-code"> Hash Code </label>
                </div>
                <div class="">
                    <input type="checkbox" id="kick-start" checked>
                    <label for="kick-start"> Kick Start </label>
                </div>
                <div class="">
                    <input type="checkbox" id="leetcode" checked>
                    <label for="leetcode"> LeetCode </label>
                </div>
            </div>

    """

    webpage_content_contest_table       = [
        """
            <div class="m-2">
                <table class="table table-bordered ">
                    <tr>
                        <th>Platform</th>
                        <th>Title</th>
                        <th>Start Time</th>
                        <th>Duration</th>
                    </tr>
        """
    ]
    
    contests: list[ContestData] = fetch_contests(atcoder=True, codechef=True, codeforces=True, code_jam=True, geeksforgeeks=True, hackerearth=True, hash_code=True, kick_start=True, leetcode=True)

    ongoing_contests: set[ContestData] = set()
    for contest in contests:
        if contest.start_time < datetime.now(tz=ZoneInfo("Asia/Kolkata")) < (contest.start_time + contest.duration):
            ongoing_contests.add(contest) 

    for contest in contests:
        platform_class: str = "-".join(contest.platform.lower().split())

        contest.start_time = contest.start_time.strftime("%a, %-d %b %Y, %-I:%M %p")

        duration, duration_str = contest.duration, []
        if duration.days:
            duration_str.append(f"{duration.days} days" if duration.days > 1 else f"{duration.days} day")
        duration_hours   = int(duration.seconds / 3600)
        if duration_hours:
            duration_str.append(f"{duration_hours} hours" if duration_hours > 1 else f"{duration_hours} hour")
        duration_minutes = int(duration.seconds / 60) % 60 
        if duration_minutes:
            duration_str.append(f"{duration_minutes} minutes" if duration_minutes > 1 else f"{duration_minutes} minutes")
        contest.duration = ", ".join(duration_str)

        webpage_content_contest_table.append(
        f"""
                    <tr class="{platform_class}">
                        <td style="color: {'green' if contest in ongoing_contests else 'orange'};"> {contest.platform} </td>
                        <td> <a href="{contest.url}" target="_blank" style="text-decoration: none; color: {'green' if contest in ongoing_contests else 'orange'};"> {contest.title} </a> </td>
                        <td style="color: {'green' if contest in ongoing_contests else 'orange'};"> {contest.start_time} </td>
                        <td style="color: {'green' if contest in ongoing_contests else 'orange'};"> {contest.duration} </td>
                    </tr>
        """
        )

    webpage_content_contest_table.append(
        """
                </table> 
            </div>
        """
    )

    webpage_content_after_contest_table = """
        
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" crossorigin="anonymous"> </script>
            
            <script>
                const platformIds = ["atcoder", "codechef", "codeforces", "code-jam", "geeksforgeeks", "hackerearth", "hash-code", "kick-start", "leetcode"]
                for (let platformId of platformIds) {
                    document.getElementById(platformId).addEventListener("change", function() {
                        if (this.checked) {
                            let contestRows = document.getElementsByClassName(platformId)
                            for (let i = 0; i < contestRows.length; ++i) {
                                contestRows[i].style.display = "table-row";
                            }
                        } else {
                            let contestRows = document.getElementsByClassName(platformId)
                            for (let i = 0; i < contestRows.length; ++i) {
                                contestRows[i].style.display = "none";
                            }
                        }
                    });
                }
            </script>

        </body>
        </html>
    """

    with (Path(__file__).parent / "index.html").open("w") as webpage:
        webpage.write(webpage_content_before_contest_table)
        webpage.write("\n")
        webpage.writelines(webpage_content_contest_table)
        webpage.write("\n")
        webpage.write(webpage_content_after_contest_table)

if __name__ == "__main__":

    main()    
