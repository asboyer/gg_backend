from flask import Flask, render_template
from datetime import datetime
import os, json

import goat_grade as gg

app = Flask(__name__)
root = os.path.dirname(__file__)

# MAP OUT THIS WHOLE APP
# PERFECT ALGORITHM / RANKING
# MAKE ALL TIME RANKING
# ADD TEAM STATS
# WORK ON DISPLAY

@app.route("/")
def index():
    text = """
    goat grade raw data
    """

    return text.strip()

@app.route("/stats/<name>")
def data(name):

    if os.path.exists(os.path.join(root, f'stats/{name}')):

        today = datetime.today()
        current_year = today.year
        current_month = today.month
        current_day = today.day

        year = int(name.split(".")[0])

        in_season = current_month in gg.NBA_SEASON
        current_year_og = current_month in [10, 11, 12] and current_year + 1 == year
        current_year_alt = current_month in [1, 2, 3, 4, 5, 6] and current_year == year
        
        last_day = int(open(os.path.join(root, "last_update.txt"), "r").readlines()[0])

        if in_season and (current_year_og or current_year_alt) and last_day != current_day:
            gg.get_stats(year)
            f = open(os.path.join(root, "last_update.txt"), "w")
            f.write(str(current_day) + "\n" + today.strftime("%b %d %Y %H:%M:%S"))
            f = open(os.path.join(root, f'stats/{name}'))
            data = json.load(f)
            return data
        
        else:
            f = open(os.path.join(root, f'stats/{name}'))
            data = json.load(f)
            return data
    else:
        
        try:
            year = int(name.split(".")[0])
        except:
            return "Invalid path"
        
        try:
            get_stats(year)
            f = open(os.path.join(root, f'stats/{name}'))
            data = json.load(f)
            return data
        except TypeError:
            return f"{year} is not a valid season!"

