from mock import patch

from bot.event_handler import RtmEventHandler


class MockClient():
    def bot_user_id(self):
        return 'mr. mockbot'


class MockWriter():
    def send_message(self, channel, message):
        return True


class MockIntentHandler():
    pass


class TestRtmEventHandler():

    def setup_method(self):
        self.e_handler = RtmEventHandler(MockClient(),
                                         MockWriter(),
                                         MockIntentHandler())

    def test_parse_login_details(self):
        event = {
            "text": "<@arXie-bot> user: username pw: password",
            "channel": 10349234
        }
        user, pw = self.e_handler.parse_login_details(event)

        assert user == "username" and pw == "password"

    @patch('tests.event_handler_test.MockWriter.send_message')
    def test_parse_login_details_fail(self, mock_send_message):
        event = {
            "text": "<@arXie-bot> user: thisistheuser password: blah",
            "channel": 12382443
        }
        user, pw = self.e_handler.parse_login_details(event)

        assert user is None and pw is None
        mock_send_message.assert_called_with(event['channel'], "Sorry, that's not the right message format.")
