from bs4 import BeautifulSoup
import json
from pandas.io.json import json_normalize
import pandas as pd
import time
import os
from path import Path

my_dir = "../zenbot/simulations/"
list_files = os.listdir(my_dir)

frames = []

for file_ in list_files:
	if file_.startswith("sim"):
		source_code = open(my_dir+file_, "r")
		soup = BeautifulSoup(source_code,"lxml")
		text_code = soup.code.string
		text_json = text_code.split("{",1)[1]
		json_str = '{'+ text_json
		data = json.loads(json_str)
		df = json_normalize(data)
		df = df[["simresults.vs_buy_hold",  "strategy", "selector.normalized"]]
		df = df.rename(columns={'simresults.vs_buy_hold': 'vs_buy_hold',
			'selector.normalized': 'selector'})
		frames.append(df)

df_all = pd.concat(frames)

df_all = df_all.sort_values(by=["vs_buy_hold"], ascending=False)

print(df_all)

timestr = time.strftime("%Y%m%d_%H%M%S")

file_name = "simulations_results_{0}.csv".format(timestr)

df_all.to_csv(file_name)


d = Path(my_dir)

for i in d.walk():
    if i.isfile():
        if i.name in list_files:
            i.remove()
