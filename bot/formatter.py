import json

def build_message(text='Default Text', markdown=True, parts=None):
    """ Combine individual parts of a message into one formatted json message body. """
    if markdown:
        message = {}
        message['text'] = text
        message['mrkdwn'] = markdown
        json_str = json.dumps(message) # validate json. TODO should catch failure
        return json_str
    return text

def paper_snippet( paper ):
    snippet = {}
    entry = ""
    # Make title line with link to article
    entry += '<{}|{}>\n'.format( paper['link'],
                                 str(i+1) + '. ' + papers['title'].replace('\n',' '))
    # make authors and date line
    entry += '{} - {}\n'.format( ', '.join(paper['authors']),
                                  paper['originally_published_time']) # authors are in bold
    # make PDF link line
    entry += '<{}|PDF>\n'.format( self.make_pdf_link( paper['pid']) )
    snippet['text'] = entry
    snippet['fallback'] = paper['title']
    return snippet
