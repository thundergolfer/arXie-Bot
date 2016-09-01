import json
import logging
import re
from bs4 import BeautifulSoup
import requests

from site_scraping import papers_from_embedded_script
from messenger import build_message

logger = logging.getLogger(__name__)

ASP_BaseURL = 'http://www.arxiv-sanity.com/'

class ApiAiIntentHandler(object):

    def __init__(self, slack_clients):
        self.clients = slack_clients

    def make_pdf_link( self, paper_id ):
        """ Build the URL to link to a paper's PDF. """
        return ASP_BaseURL + 'pdf/' + paper_id + '.pdf'

    def handle_intent(self, msg_txt, intent, parameters=None, context=None ):
        """
        Receive a intent string and select the correct intent handling function.
        """
        if intent == 'search':
            # Strip front of message to just retain search query
            if msg_txt.startswith('search for '):
                query = msg_txt[len('search for '):]
            else: # message was just "search X"
                query = msg_txt[len('search '):]
            arXiv_msg = self.search_arxiv(query)
        else:
            arXiv_msg = "NOT YET IMPLEMENTED"
        return arXiv_msg, None


    def search_arxiv(self, query, num_papers=5 ):
        """ Search arxiv papers by search string. """
        tokens = query.split(' ')
        searchEndpoint = 'search?q=' + '+'.join(tokens)
        searchURL = ASP_BaseURL + searchEndpoint
        papers = papers_from_embedded_script(searchURL)
        bot_uid = self.clients.bot_user_id()
        attached_papers = []
        # For each paper
        for i in range(max(num_papers,len(papers)):
            attach = {}
            entry = ""
            # Make title line with link to article
            entry += '<{}|{}>\n'.format( papers[i]['link'],
                                         str(i+1) + '. ' + papers[i]['title'].replace('\n',' '))
            # make authors and date line
            entry += '{} - {}\n'.format( ', '.join(papers[i]['authors']),
                                          papers[i]['originally_published_time']) # authors are in bold
            # make PDF link line
            entry += '<{}|PDF>\n'.format( self.make_pdf_link( papers[i]['pid']) )
            attach['text'] = entry
            attach['fallback'] = papers[i]['title']
            attached_papers.append(attach)

        attached_papers[-1]['footer'] = "> `<@" + bot_uid + "> show more papers` - to see more papers"
        # build the json message object
        return build_message( text="*Search Results*", markdown=False), attached_papers



    def clear_library(self, user):
        """ Remove all saved paper's from the users library. """
        raise NotImplementedError

    def get_library(self, user):
        """ Get all papers saved by the user. Their 'library'. """
        raise NotImplementedError

    def get_most_recent(self, user):
        """ Get most recently published papers within the user's search
        domain.
        """
        raise NotImplementedError

    def get_paper(self, set, id):
        """ Return specified paper from within the set. """
        raise NotImplementedError

    def get_recommended(self, user):
        """ Get the papers recommended to the user based on their
        saved papers and their search domain. """
        raise NotImplementedError

    def get_top_recent(self, user):
        """
        Get the 'top' recent papers within the user's search domain.
        """
        raise NotImplementedError

    def get_similar( self, paper ):
        """ Get papers similar in content to the named paper. """
        raise NotImplementedError

    def goto_website(self):
        """
        Open the Arxiv Sanity Preserver webpage, or just provide a link to it.
        """
        raise NotImplementedError

    def save_paper(self, paper):
        """
        Save the named paper, which adds that paper to the user's library. """
        raise NotImplementedError
