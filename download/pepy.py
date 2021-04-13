import json
import urllib
from datetime import date, timedelta

import typer 


header= {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
    'AppleWebKit/537.11 (KHTML, like Gecko) '
    'Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'
}


def download(project):
    """Downloads the download stats from yesterday for a project"""
    url = f"https://api.pepy.tech/api/v2/projects/{project}"
    req = urllib.request.Request(url=url, headers=header)
    txt = urllib.request.urlopen(req).read()
    data = [{"date":k, "values": sum(v.values())} for k, v in json.loads(txt)['downloads'].items()]
    yesterday = str(date.today() - timedelta(days=1))
    for d in data:
        if d['date'] == yesterday:
            print(json.dumps(d))
    
if __name__ == "__main__":
    typer.run(download)