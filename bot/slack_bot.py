import time
import logging
import traceback

from slack_clients import SlackClients
from messenger import Messenger
from event_handler import RtmEventHandler

logger = logging.getLogger(__name__)


def spawn_bot():
    return SlackBot()


class SlackBot(object):
    def __init__(self, token=None):
        """Creates Slacker Web and RTM clients with API Bot User token.

        Args:
            token (str): Slack API Bot User token (for development token set in env)
        """
        self.last_ping = 0
        self.keep_running = True
        if token is not None:
            self.clients = SlackClients(token)

    def start(self, resource):
        """Creates Slack Web and RTM clients for the given Resource
        using the provided API tokens and configuration, then connects websocket
        and listens for RTM events.

        Args:
            resource (dict of Resource JSON): See message payloads - https://beepboophq.com/docs/article/resourcer-api
        """
        logger.debug('Starting bot for resource: {}'.format(resource))
        if 'resource' in resource and 'SlackBotAccessToken' in resource['resource']:
            res_access_token = resource['resource']['SlackBotAccessToken']
            self.clients = SlackClients(res_access_token)

        if self.clients.rtm.rtm_connect():
            logging.info(u'Connected {} to {} team at https://{}.slack.com'.format(
                self.clients.rtm.server.username,
                self.clients.rtm.server.login_data['team']['name'],
                self.clients.rtm.server.domain))

            msg_writer = Messenger(self.clients)
            event_handler = RtmEventHandler(self.clients, msg_writer)

            while self.keep_running:
                for event in self.clients.rtm.rtm_read():
                    try:
                        event_handler.handle(event)
                    except:
                        err_msg = traceback.format_exc()
                        logging.error('Unexpected error: {}'.format(err_msg))
                        msg_writer.write_error(event['channel'], err_msg)
                        continue

                self._auto_ping()
                time.sleep(.1)

        else:
            logger.error('Failed to connect to RTM client with token: {}'.format(self.clients.token))

    def _auto_ping(self):
        # hard code the interval to 3 seconds
        now = int(time.time())
        if now > self.last_ping + 3:
            self.clients.rtm.server.ping()
            self.last_ping = now

    def stop(self, resource):
        """Stop any polling loops on clients, clean up any resources,
        close connections if possible.

        Args:
            resource (dict of Resource JSON): See message payloads - https://beepboophq.com/docs/article/resourcer-api
        """
        self.keep_running = False
