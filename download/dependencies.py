"""
This script uses the data available on: 

https://hugovk.github.io/top-pypi-packages

DOI:
Hugo van Kemenade, & Richard Si. (2021, May 1). 
hugovk/top-pypi-packages: Release 2021.05 (Version 2021.05). 
Zenodo. http://doi.org/10.5281/zenodo.4732473
"""

from parse import parse, search
from gazpacho import get, Soup
from clumper import Clumper
from tqdm import tqdm
from memo import memlist


url = "https://hugovk.github.io/top-pypi-packages/top-pypi-packages-365-days.json"
projects = Clumper.read_json(url).unpack("rows").select("project").collect()

history_url = lambda p: f"https://pypi.org/project/{p}/#history"
info_url = lambda p, v: f"https://pypi.org/pypi/{p}/{v}/json"


def get_project_version(project):
    html = get(history_url(project))
    soup = Soup(html)
    element = soup.find("h1", {"class": "package-header__name"}).text
    parsed = parse("{name} {version}", element).named
    return parsed['version']

def parse_version(v):
    return "".join([c for c in v if c in '.1234567890'])

def parse_items(items):
    return (Clumper(items).map(lambda d: {'dep_str': i}))

def clean_dep(d):
    for char in [" ", ">", "="]:
        if char in d:
            d = d[:d.find(char)]
    return d.replace(";","")


if __name__ == "__main__":
    data = []

    @memlist(data=data)
    def get_project_items(project):
        try:
            version = get_project_version(project)
            url = info_url(project, version)
            items = Clumper.read_json(url).collect()[0]['info']['requires_dist']
        except:
            return {"project": project, "items": []}
        if not items:
            return {"project": project, "items": []}
        return {"project": project, "items": parse_items(items).collect()}

    for i in tqdm(projects[2498:]):
        get_project_items(i['project'])

    (Clumper(data)
        .unpack("items")
        .mutate(required=lambda d: 'extra' not in d['dep_str'],
                dep=lambda d: clean_dep(d['dep_str']))
        .drop("dep_str")
        .write_csv("data/dependencies/dependencies.csv"))
