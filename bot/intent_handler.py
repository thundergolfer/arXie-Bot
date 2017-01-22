import json
import logging
import re
from bs4 import BeautifulSoup
import requests

from site_scraping import papers_from_embedded_script
from formatter import build_message, paper_snippet

logger = logging.getLogger(__name__)

ASP_BaseURL = 'http://www.arxiv-sanity.com/'

class ApiAiIntentHandler(object):

    def __init__(self, slack_clients):
        self.clients = slack_clients

    def make_pdf_link( self, paper_id ):
        """ Build the URL to link to a paper's PDF. """
        return ASP_BaseURL + 'pdf/' + paper_id + '.pdf'

    def handle_intent(self, msg_txt, intent, session, parameters=None, context=None ):
        """
        Receive an intent string and select the correct intent handling function.
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
            attached_papers.append(paper_snippet(papers[i])))

        attached_papers[-1]['footer'] = "> `<@" + bot_uid + "> show more papers` - to see more papers"
        # build the json message object
        return build_message( text="*Search Results*", markdown=False, parts=attached_papers)

    def clear_library(self, session):
        """ Remove all saved paper's from the users library. """
        # The way to do this is to fetch all papers and then call "toggle"
        # on all of them.
        # https://github.com/karpathy/arxiv-sanity-preserver/blob/79b975764d78f10e1223bffe289005521bf1fd00/templates/main.html
        libraryURL = ASP_BaseURL + "/library"
        papers = papers_from_embedded_script
        toggleURL = ASP_BaseURL + "/libtoggle"
        for p in papers:
            # toggle off each paper from library
            r = session.post(toggleURL, data = {'pid':p["pid"]})
            if r.status_code != 200:
                # TODO log error. pass up to user?
                pass

    def get_library(self, session):
        """ Get all papers saved by the user. Their 'library'. """
        # TODO check if logged in?
        # TODO NEED TO PASS SESSION!!!!!
        libraryURL = ASP_BaseURL + "/library"
        papers = papers_from_embedded_script(libraryURL, session=session)
        attached_papers = []
        for p in papers:
            attached_papers.append(paper_snippet(p))
        return build_message( text="*Your Library*", markdown=False, parts=attached_papers)

    def get_most_recent(self, user):
        """ Get most recently published papers within the user's search
        domain.
        """
        papers = papers_from_embedded_script(ASP_BaseURL+"/", user.session)
        attached_papers = []
        for p in papers:
            attached_papers.append(paper_snippet(p))
        return build_message( text="*Your Most Recent*", markdown=False, parts=attached_papers)

    def get_paper(self, set, pid):
        """ Return specified paper from within the set. """
        paperURL = ASP_BaseURL + "/" + str(pid)
        paper = papers_from_embedded_script(paperURL)[0] # only get first, rest are related papers
        return build_message(text="*Here's your paper*", markdown=False, parts=[paper_snippet(p)])

    def get_recommended(self, session):
        """ Get the papers recommended to the user based on their
        saved papers and their search domain. """
        # TODO the /recommend endpoint has FILTERS
        recommendedURL = ASP_BaseURL + "/recommend"
        papers = papers_from_embedded_script(recommendedURL, session)
        attached_papers = []
        for p in papers:
            attached_papers.append(paper_snippet(p))
        return build_message( text="*Your Recommended*", markdown=False, parts=attached_papers)

    def get_top_recent(self, session):
        """
        Get the 'top' recent papers within the user's search domain.
        """
        # TODO the /top endpoint has FILTERS
        topURL = ASP_BaseURL + "/top" # default filters
        papers = papers_from_embedded_script(topURL, session=session)
        attached_papers = []
        for p in papers:
            attached_papers.append(paper_snippet(p))
        return build_message( text="*Your Library*", markdown=False, parts=attached_papers)

    def get_similar( self, paper ):
        """ Get papers similar in content to the named paper. """
        similarURL = ASP_BaseURL + str(paper.pid)
        similar_papers = papers_from_embedded_script(similarURL)[1:] # TODO is the searched paper always first?
        attached_papers = []
        for p in similar_papers:
            attached_papers.append(paper_snippet(p))
        return build_message( text="*Your Library*", markdown=False, parts=attached_papers)

    def goto_website(self):
        """
        Open the Arxiv Sanity Preserver webpage, or just provide a link to it.
        """
        return build_message( text=ASP_BaseURL, markdown=False, parts=None)

    def save_paper(self, paper, session):
        """
        Save the named paper, which adds that paper to the user's library. """
        toggleURL = ASP_BaseURL + "/libtoggle"
        r = session.post(toggleURL, data = {'pid':p["pid"]})
        if r.status_code != 200:
            # TODO log error to user somewho
            raise Exception("Paper save failed!")
