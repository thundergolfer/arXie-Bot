import json
import random
import logging
import re
from bs4 import BeautifulSoup
import requests

from bot.site_scraping import papers_from_embedded_script
from bot.formatter import build_message, paper_snippet

logger = logging.getLogger(__name__)

ASP_BaseURL = 'http://www.arxiv-sanity.com/'


class ApiAiIntentHandler(object):

    def __init__(self, slack_clients):
        self.clients = slack_clients

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
            resp_msg = self.search_arxiv(query)
        elif intent == 'greeting' or intent == 'say_hello':
            resp_msg = self.greeting()
        elif intent == 'clear_library':
            resp_msg = self.clear_library(session)
        elif intent == 'get_library':
            resp_msg = self.get_library(session)
        elif intent == 'get_most_recent':
            resp_msg = self.get_most_recent(session)
        elif intent == 'get_paper':
            resp_msg = self.get_paper(None, 99)
        elif intent == 'get_recommended':
            resp_msg = self.get_recommended(session)
        elif intent == 'get_similar_papers':
            resp_msg = self.get_similar(99)
        elif intent == 'get_top_recent':
            resp_msg = self.get_top_recent(session)
        elif intent == 'goto_website':
            resp_msg = self.goto_website()
        elif intent == 'save_paper':
            resp_msg = self.save_paper(999, session)
        elif intent == 'send_credentials':
            resp_msg = "Intent '{}' not yet implemented.".format(intent)
        elif intent == 'GAVE LOGIN DETAILS':
            resp_msg = build_message(text="Thanks for that. I've saved your details.", markdown=False, parts=None)
        else:
            logger.warning("Intent '{}' couldn't be matched to a handler function.".format(intent))
            resp_msg = "Intent '{}' not yet implemented.".format(intent)
        return resp_msg, None

    def greeting(self):
        greetings = [
            'How are ya?',
            'Good to hear from you',
            'Hey', 'Hello', 'Hi',
            'Good day!'
        ]
        return build_message(text=random.choice(greetings), markdown=False, parts=None)

    def search_arxiv(self, query, num_papers=5):
        """ Search arxiv papers by search string. """
        logging.info("Searching ArXiv for: {}".format(query.encode('utf-8')))
        tokens = query.split(' ')
        searchEndpoint = 'search?q=' + '+'.join(tokens)
        searchURL = ASP_BaseURL + searchEndpoint
        papers = papers_from_embedded_script(searchURL)
        bot_uid = self.clients.bot_user_id()
        attached_papers = []
        # For each paper
        for i in range(min(num_papers,len(papers))):
            attached_papers.append(paper_snippet(papers[i], i + 1))

        attached_papers[-1]['footer'] = "> `<@" + bot_uid + "> show more papers` - to see more papers"
        # build the json message object
        return build_message( text="*Search Results*", markdown=False, parts=attached_papers)

    def clear_library(self, session):
        """ Remove all saved paper's from the users library. """
        logging.info("Clearing ArXiv library.")
        libraryURL = ASP_BaseURL + "/library"
        papers = papers_from_embedded_script(libraryURL)
        toggleURL = ASP_BaseURL + "/libtoggle"
        for p in papers:
            # toggle off each paper from library
            r = session.post(toggleURL, data = {'pid':p["pid"]})
            if r.status_code != 200:
                # TODO log error. pass up to user?
                pass

    def get_library(self, session):
        """ Get all papers saved by the user. Their 'library'. """
        logging.info("Getting ArXiv library.")
        libraryURL = ASP_BaseURL + "/library"
        papers = papers_from_embedded_script(libraryURL, session=session)
        attached_papers = []
        for i, p in enumerate(papers):
            attached_papers.append(paper_snippet(p, i + 1))
        return build_message( text="*Your Library*", markdown=False, parts=attached_papers)

    def get_most_recent(self, session):
        """ Get most recently published papers within the user's search
        domain.
        """
        logging.info("Getting most recent ArXiv papers within user's domain.")
        papers = papers_from_embedded_script(ASP_BaseURL+"/", session)
        attached_papers = []
        for i, p in enumerate(papers):
            attached_papers.append(paper_snippet(p, i + 1))
        return build_message( text="*Your Most Recent*", markdown=False, parts=attached_papers)

    def get_paper(self, set, pid):
        """ Return specified paper from within the set. """
        logging.info("Getting paper: {} from ArXiv.".format(pid))
        paperURL = ASP_BaseURL + "/" + str(pid)
        paper = papers_from_embedded_script(paperURL)[0] # only get first, rest are related papers
        return build_message(text="*Here's your paper*", markdown=False, parts=[paper_snippet(paper, 1)])

    def get_recommended(self, session):
        """ Get the papers recommended to the user based on their
        saved papers and their search domain. """
        # TODO the /recommend endpoint has FILTERS
        logging.info("Getting recommended ArXiv papers for user.")
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
        logging.info("Getting top recent ArXiv papers in user's domain.")
        topURL = ASP_BaseURL + "/top" # default filters
        papers = papers_from_embedded_script(topURL, session=session)
        attached_papers = []
        for p in papers:
            attached_papers.append(paper_snippet(p))
        return build_message( text="*Your Library*", markdown=False, parts=attached_papers)

    def get_similar(self, pid):
        """ Get papers similar in content to the named paper. """
        logging.info("Getting ArXiv papers similar to paper: {}".format())
        similarURL = ASP_BaseURL + str(pid)
        similar_papers = papers_from_embedded_script(similarURL)[1:] # TODO is the searched paper always first?
        attached_papers = []
        for p in similar_papers:
            attached_papers.append(paper_snippet(p))
        return build_message(text="*Your Library*", markdown=False, parts=attached_papers)

    def goto_website(self):
        """
        Open the Arxiv Sanity Preserver webpage, or just provide a link to it.
        """
        return build_message( text=ASP_BaseURL, markdown=False, parts=None)

    def save_paper(self, paper, session):
        """
        Save the named paper, which adds that paper to the user's library."""
        logging.info("Saving paper: {} to user's library.".format(paper))
        toggleURL = ASP_BaseURL + "/libtoggle"
        r = session.post(toggleURL, data = {'pid': paper["pid"]})
        if r.status_code != 200:
            # TODO log error to user somewho
            raise Exception("Paper save failed!")
