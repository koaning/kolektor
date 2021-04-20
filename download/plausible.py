import json
from datetime import date, timedelta

from clumper import Clumper

if __name__ == "__main__":
    yesterday = str(date.today() - timedelta(days=i))
    url = f"https://plausible.io/api/stats/calmcode.io/main-graph?period=day&date={yesterday}"
    clump = Clumper.read_json(url)
    data = {d['name'].replace(" ", "-").lower(): d['count'] 
            for d in clump.collect()[0]['top_stats'] if 'count' in d.keys()}
    data['date'] = yesterday
    print(json.dumps(data))
