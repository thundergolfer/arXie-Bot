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

        mock_messenger.assert_called_with(1000, "")
