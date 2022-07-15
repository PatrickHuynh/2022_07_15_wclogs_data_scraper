# %%
import enum
from html import parser
from bs4 import BeautifulSoup
import bs4
import regex
import requests
from pathlib import Path
import glob
import pandas as pd

# %%
files = [Path(i) for i in glob.glob("./data/*.mhtml")]
comps = []

for file in files:
    with open(file, "rb") as f:
        soup = BeautifulSoup(f, "html.parser")
        rows = soup.find_all("tr", {"id": regex.compile("row-2529.*")})
        for row in rows:
            tds = row.find_all("td")
            row_data = {}
            for i, td in enumerate(tds):
                id = td['class'][0].replace("3D", "").replace("\"", "")
                if id == "rankings-comp-cell":
                    classes = ['tanks', 'healers', 'dps_melee', 'dps_ranged']
                    classes_count = []
                    for i in td.children:
                        if type(i) == bs4.element.Tag:
                            classes_count.append(int(i.text))
                    for cls, count in zip(classes, classes_count):
                        row_data[cls] = count
                if id == "main-table-name":
                    guild_name = td.find("a", {'class': regex.compile(".*main-table-guild.*")}).text
                    row_data["guild_name"] = guild_name.replace("\n", "").replace("\r", "").replace("=", "").replace("</a>", "")
                    pass
            comps.append(row_data)

df = pd.DataFrame(comps)
df.to_csv("guild compositions.csv")
# %%
