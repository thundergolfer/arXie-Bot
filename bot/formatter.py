import json

from bot.discussions import reddit_conversations

ASP_BaseURL = 'http://www.arxiv-sanity.com/'


def build_message(text='Default Text', markdown=True, parts=None):
    """ Combine individual parts of a message into one formatted json message body. """
    if markdown:
        message = {}
        message['text'] = text
        message['mrkdwn'] = markdown
        json_str = json.dumps(message) # validate json. TODO should catch failure
        return json_str
    return text


def make_pdf_link(paper_id):
    """ Build the URL to link to a paper's PDF. """
    return ASP_BaseURL + 'pdf/' + str(paper_id) + '.pdf'


def paper_snippet( paper, number, include_abstract=False, include_discussions=False):
    snippet = {}
    entry = ""
    # Make title line with link to article
    entry += '<{}|{}>\n'.format( paper['link'],
                                 str(number) + '. ' + paper['title'].replace('\n',' '))
    # make authors and date line
    entry += '{} - {}\n'.format(', '.join(paper['authors']),
                                paper['originally_published_time']) # authors are in bold

    if include_abstract:
        entry += '-----------------------------\n'
        entry += paper['abstract'] + '\n'
        entry += '-----------------------------\n'

    # make PDF link line
    entry += '<{}|PDF>\n'.format(make_pdf_link(paper['pid']))

    if include_discussions:
        subreddit, link, num_comments = reddit_conversations(paper['link'])
        entry += '<{}|{} Discussion. {} comments\n'.format(link, subreddit, num_comments)
        
    snippet['text'] = entry
    snippet['fallback'] = paper['title']
    return snippet
