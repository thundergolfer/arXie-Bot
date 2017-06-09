import json
import re
import requests

def reddit_conversations(link):
    api_url_prefix = "https://www.reddit.com/search.json?q="

    api_call_url = api_url_prefix + link

    r = requests.get(api_call_url, headers = {'User-agent': 'Arxie Bot'})
    body = json.loads(r.content)

    results = []
    for part in body:
        if 'permalink' not in part['data']:
            if 'children' not in part['data']: continue
            else:
                for child in part['data']['children']:
                    if 'permalink' not in child['data']: continue
                    else: results.append((child['data']['permalink'], child['data']['num_comments']))
        else:
            results.append((part['data']['permalink'], part['data']['num_comments']))

    results.sort(key = lambda x: x[1])

    subreddit = re.search('\/r\/[^/\/]+', results[0][0]).group(0)
    link = "https://www.reddit.com" + results[0][0]
    num_comments = results[0][1]
    return subreddit, link, num_comments




if __name__ == '__main__':
    link = "https://arxiv.org/abs/1706.00826"

    print(reddit_conversations(link))
