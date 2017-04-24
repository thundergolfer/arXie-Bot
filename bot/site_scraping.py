
from bs4 import BeautifulSoup
import re
import json
import requests


def find_and_parse_papers_json(js):
    """
    This is a really ugly, dirty way to parse the 'papers' json object
    on an Arxiv page. I have tried the 'slimit' js parser as a solution
    but it's broken, so I'll try this.
    """
    start_of_json = js.index('var papers = [{') + len('var papers = [{') - 2
    # find all instances of the '}];' closing indicator
    end_pattern = re.compile('}];')

    papers = None
    trimmed_obj = js[start_of_json:]
    for m in end_pattern.finditer(trimmed_obj):
        possible_end_of_obj = m.start() + len('}];') - 1
        try:
            candidate = trimmed_obj[:possible_end_of_obj]
            candidate = clean_json(candidate)
            papers = json.loads(candidate)
        except ValueError:
            pass

    return papers


def clean_json(json):
    json = json.replace('\n', ' ')
    return json.replace(r'\\', 'M@THJ@X')


def papers_from_embedded_script( url, session=None ):
    """
    Extract papers data from script embedded in ASP site's HTML.
    Note: looks for "var papers = " in a <script> </script> body.
    """
    if session: resp = session.get(url)
    else:       resp = requests.get(url)

    soup = BeautifulSoup(resp.text, 'html.parser')
    scripts = soup.find_all('script')
    #p = re.compile('var papers = (\[.*?\];)', re.MULTILINE)
    pattern = re.compile('var papers = \[[.\s\S]*?\];')

    str_scripts = [str(script.string) for script in scripts if script.string]
    papers_js = [script for script in str_scripts if 'var papers = ' in script][0]
    papers = find_and_parse_papers_json(papers_js)

    return papers
