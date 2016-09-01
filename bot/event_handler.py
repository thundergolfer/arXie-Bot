import json
import logging
import re
from private_settings import apiai_access_token
import apiai

import sqlite3

logger = logging.getLogger(__name__)
API_ACCESS_TOKEN = apiai_access_token

class RtmEventHandler(object):
    def __init__(self, slack_clients, msg_writer, intent_handler):
        self.clients = slack_clients
        self.msg_writer = msg_writer
        self.intent_handler = intent_handler
        self.api_ai = apiai.ApiAI(API_ACCESS_TOKEN) # TODO make dependency injection instead

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
        # Log in message sender if they exist in database (aren't already logged in)

        # If message sender doesn't exist, ask if they have an account

        # If they don't have an account, create an account for them
        user, pw = self._handle_account_setup(event)
        # then login
        raise NotImplementedError

    def _handle_account_setup(self, event, username_choice=None, pw_choice=None):
        # Open database connections
        connection = sqlite3.connect('../accounts.db')

        connection.execute( 'CREATE TABLE IF NOT EXISTS' +
                            TABLE_NAME,
                            )
        # create entry

        # return login details
        raise NotImplementedError

    def _handle_message(self, event):
        # Filter out messages from the bot itself, and from non-users (eg. webhooks)
        if ('user' in event) and (not self.clients.is_message_from_me(event['user'])):

            msg_txt = event['text']
            if self.clients.is_bot_mention(msg_txt):
                # e.g. user typed: "@pybot tell me a joke!"
                msg_txt = msg_txt[msg_txt.index('>')+2:] # remove @NAME from msg
                if 'help' in msg_txt:
                    self.msg_writer.write_help_message(event['channel'])
                elif 'attachment' in msg_txt:
                    self.msg_writer.demo_attachment(event['channel'])
                else:
                    # determine intent
                    resp = self.process_message(msg_txt)
                    # handle intent
                    txt, attachments = self.intent_handler.handle_intent( msg_txt, resp['intent'] )
                    # send message
                    self.msg_writer.send_message( event['channel'], txt, attachments )

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
