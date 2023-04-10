import requests
from bs4 import BeautifulSoup
import csv

# Set these variables
RUNSIGNUP_PARTICIPANT_PAGE = "https://runsignup.com/Race/FindARunner/?raceId=118427"

page = requests.get(RUNSIGNUP_PARTICIPANT_PAGE)
soup = BeautifulSoup(page.content, "html.parser")
pages = int(soup.find("span", class_="result-count").get_text())

def parse_ultrasignup_json(json, participant_stats):
    ultrasignup_records = []
    for r in json:
        user_record = (
            True if r["Age"] == int(participant_stats[4]) else False,
            len(r["Results"]),
            r["Rank"],
            r["AgeRank"]    
        )
        ultrasignup_records.append(user_record)
    ranked = sorted(ultrasignup_records, reverse=True)
    try:
        participant_stats.append(ranked[0][1])
        participant_stats.append(ranked[0][2])
        participant_stats.append(ranked[0][3])
        participant_stats.append(len(json))
        print(f"Found ultrasignup results for {participant_stats[1]}")
        return participant_stats
    except IndexError:
        print(f"No ultrasignup results found for {participant_stats[1]}, trying alternate URL format")
        return participant_stats



participants = []

for p in range(1, pages+1):
    url = f"{RUNSIGNUP_PARTICIPANT_PAGE}&page={p}"
    print(f"{url}, page {p} of {pages}")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find_all("table", class_="data-display2")[1]
    rows = table.find_all("tr")
    for row in rows:
        try:
            cols = row.find_all("td")
            cols = [x.text.replace('More Details', '').strip() for x in cols]
            cols[6] = cols[6].split()[0]
            participants.append(cols)
        except:
            pass
        
for p in participants:
    possible_urls = []
    first_name, last_name = p[1].split(" ", 1)
    possible_urls.append(f"https://ultrasignup.com/service/events.svc/historybyname/{first_name}/{last_name.replace(' ', '%20')}/")
    possible_urls.append(f"https://ultrasignup.com/service/events.svc/historybyname/{first_name}/%20{last_name.replace(' ', '%20')}/")
    if len(p[1].split()) > 2:
        first_name = " ".join(p[1].split(" ", 2)[:2])
        last_name = p[1].split(" ",2)[2:][0]
        possible_urls.append(f"https://ultrasignup.com/service/events.svc/historybyname/{first_name.replace(' ', '%20')}/{last_name}/")
    for url in possible_urls:
        ultrasignup = requests.get(url)
        user_records = ultrasignup.json()
        p = parse_ultrasignup_json(user_records, p)
        if len(p) > 7:
            break

with open('participants.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(['bib_number', 'name', 'race', 'gender', 'age', 'city', 'state', 'ultrasignup_race_results', 'ultrasignup_rank', 'ultrasignup_age_rank', 'ultrasignup_user_records'])
    write.writerows(participants)