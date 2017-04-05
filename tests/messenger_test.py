from mock import patch

from bot.messenger import Messenger

def test_nothing():
    assert 3 is 3

class TestMessenger():

    class MockClient():
        def bot_user_id(self):
            return 'mr. mockbot'

    @patch('bot.messenger.Messenger')
    def test_write_help_message(self, mockMessenger):
        messenger = Messenger(self.MockClient())
        with patch.object(messenger, 'send_message') as mock_messenger:
            mock_ch_id = 1000
            messenger.write_help_message(1000)

        expected_message =  str("I'm your friendly Slack bot written in Python.  I'll *_respond_* to the following commands:" +
                            "\n> `hi <@mr. mockbot>` - I'll respond with a randomized greeting mentioning your user. :wave:" +
                            "\n> `<@mr. mockbot> joke` - I'll tell you one of my finest jokes, with a typing pause for effect. :laughing:" +
                            "\n> `<@mr. mockbot> attachment` - I'll demo a post with an attachment using the Web API. :paperclip:")

        mock_messenger.assert_called_with(1000, expected_message)
