import os
import json
import logging
import re
# from private_settings import apiai_access_token
import apiai

import sqlite3
import requests
from site_scraping import papers_from_embedded_script

logger = logging.getLogger(__name__)
API_ACCESS_TOKEN = os.environ['APIAI_TOKEN']

TASKS = { "sign-up" : "SIGNUP"}

class RtmEventHandler(object):
    def __init__(self, slack_clients, msg_writer, intent_handler):
        self.clients = slack_clients
        self.msg_writer = msg_writer
        self.intent_handler = intent_handler
        self.api_ai = apiai.ApiAI(API_ACCESS_TOKEN) # TODO make dependency injection instead
        self.sessions = None
        self.tasks = {} # For mult-message spanning tasks

    def handle(self, event):

        if 'type' in event:
            self._handle_by_type(event['type'], event)

    def _handle_by_type(self, event_type, event):
        # See https://api.slack.com/rtm for a full list of events
        if event_type == 'error':
            # error
            self.msg_writer.write_error(event['channel'], json.dumps(event))
        elif event_type == 'message':
            # message was sent to channel
            self._handle_message(event)
        elif event_type == 'channel_joined':
            # you joined a channel
            self.msg_writer.write_help_message(event['channel'])
        elif event_type == 'group_joined':
            # you joined a private group
            self.msg_writer.write_help_message(event['channel'])
        else:
            pass

    def _handle_login(self, event):
        # Log in message sender if they exist
        user, pw = get_user(event['user'])
        # Are the login details in the message?
        user, pw = parse_login_details(event['text'])
        if user and pw:
            # then login
            status_code, session = self._login(user, pw)
            self.session[event['user']] = session # we're gonna keep needing this
            return True
        return False

    def parse_login_details( msg_text ):
        msg_text = msg_text[msg_text.index('>')+2:] # remove @arXie-bot from text
        tokens = msg_text.split(' ')
        # Check string format
        if len(tokens) == 4 and tokens[0] == 'user:' and tokens[2] == 'pw:':
            return tokens[1], tokens[3]
        else:
            return None, None

    def _login(self, user, pw):
        """ Login using named credentials and pass back the Session. """
        login_url = 'http://www.arxiv-sanity.com/login'
        s = requests.Session()
        s.headers.update({'Referer' : 'http://arxiv-sanity.com/'}) # TODO add more relevant headers
        payload = {
            'username' : 'thundergolfer',
            'password' : 'mnijb233'
        }
        p = s.post(login_url, data=payload)
        return p.status_code, s

    def _handle_message(self, event):
        # Filter out messages from the bot itself, and from non-users (eg. webhooks)
        if ('user' in event) and (not self.clients.is_message_from_me(event['user'])):

            msg_txt = event['text']
            if self.clients.is_bot_mention(msg_txt):
                # e.g. user typed: "@arxie-bot tell me a joke!"
                msg_txt = msg_txt[msg_txt.index('>')+2:] # remove @NAME from msg
                if 'help' in msg_txt:
                    self.msg_writer.write_help_message(event['channel'])
                elif 'attachment' in msg_txt:
                    self.msg_writer.demo_attachment(event['channel'])
                else:
                    if not self.sessions['user']:
                        login_success = self._handle_login(event) # creates a session
                    if success:
                        # determine intent
                        resp = self.process_message(msg_txt)
                        # handle intent
                        txt, attachments = self.intent_handler.handle_intent( msg_txt, resp['intent'], session )
                        # send message
                        self.msg_writer.send_message( event['channel'], txt, attachments )
                    else:
                        self.msg_writer.send_message( event['channel'],
                                                      "Please enter login details like this:\n"
                                                      "user: {username} pw: {password}")

    def process_message(self, msg_txt ):
        """
        Process the message body through API AI's system to get the intent
        of the message and update the context if needed.
        """
        request = self.api_ai.text_request()
        request.query = msg_txt
        # get json response as bytes and decode it into a string
        resp = request.getresponse().read().decode('utf-8')
        resp = json.loads(resp) # convert string to json dict
        return { 'contexts' : resp['result']['contexts'] if 'contexts' in resp else None,
                 'intent' : resp['result']['metadata']['intentName'],
                 'parameters' : resp['result']['parameters']
               }
