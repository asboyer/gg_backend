from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import os

root = os.path.dirname(__file__)

NBA_SEASON = [10, 11, 12, 1, 2, 3, 4, 5, 6]

def scrape(url):
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")  
    
    headers = [th.getText() for th in soup.findAll("tr", limit=2)[0].findAll("th")]
    headers = headers[1:]

    rows = soup.findAll("tr")[1:]

    stats = {}
    for i in range(len(rows)):
        tds = rows[i].findAll("td")
        if len(tds) > 0:
            name = tds[0].getText()
            try:
                if stats[name] != {}:
                    h = 0
                    for td in tds:
                        header = headers[h]
                        if header == "Tm":
                            team = td.getText()
                        h += 1
                    stats[name]["Tm"].append(team)
            except:
                stats[name] = {}
                h = 0
                for td in tds:
                    header = headers[h]
                    if header == "MP" and "advanced" in url:
                        header = "TMP"
                    stats[name][header] = td.getText()
                    h += 1
                if stats[name]["Tm"] == "TOT":
                    stats[name]["Tm"] = []
    return stats

def get_stats(year, categories=[
                        "PTS", "AST", "TRB", "FG%", "FT%", "3P%", "STL", "BLK",
                        "MP", "PER", "TS%", "WS", "BPM", "2P%", "OWS", "DWS", 
                        "WS/48", "USG%", "OBPM", "DBPM", "VORP", "eFG%"
                        ]):
    reg_stats_url = f"https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html"
    adv_stats_url = f"https://www.basketball-reference.com/leagues/NBA_{year}_advanced.html"
    try:
        reg_stats = scrape(reg_stats_url)
        adv_stats = scrape(adv_stats_url)
    except:
        raise TypeError("URL")
        return

    for player in list(reg_stats):
        reg_stats[player].update(adv_stats[player])

    old_categories = []

    for i in range(len(categories)):
        category = categories[i]
        if reg_stats[list(reg_stats)[0]][category] == "":
            for player in list(reg_stats):
                del reg_stats[player][category]
            old_categories.append(category)

    for category in old_categories:
        categories.remove(category)

    for player in list(reg_stats):
        try:
            del reg_stats[player]["<0xa0>"]
        except:
            pass
        try:
            if float(reg_stats[player]["G"]) < 10 or float(reg_stats[player]["MP"]) < 10:
                del reg_stats[player]
        except:
            if float(reg_stats[player]["G"]) < 10:
                del reg_stats[player]

    with open(os.path.join(root, f"stats/{year}.json"), "w+", encoding="utf8") as file:
        file.write(json.dumps(reg_stats, ensure_ascii=False, indent =4))

    return reg_stats, categories
