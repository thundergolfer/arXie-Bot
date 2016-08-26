
from bs4 import BeautifulSoup
import re
import json
import requests


def paper_titles( soup ):
    """ Extract paper titles from the ASP site's HTML. """
    raise NotImplementedError

def papers_from_embedded_script( url ):
    """
    Extract papers data from script embedded in ASP site's HTML.
    Note: looks for "var papers = " in a <script> </script> body.
    """
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    scripts = soup.find_all('script')
    #p = re.compile('var papers = (\[.*?\];)', re.MULTILINE)
    p = re.compile('var papers = \[.*?\];')

    str_scripts = [str(script.string) for script in scripts if script.string]

    match = re.search(p, str_scripts[2])
    variable = match.group()
    json_data = variable[variable.index('['):-1] # cut off variable decl. and ";"
    papers = json.loads(json_data)

    return papers
