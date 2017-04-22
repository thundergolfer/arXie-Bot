from bot.event_handler import RtmEventHandler


class MockClient():
    def bot_user_id(self):
        return 'mr. mockbot'


class MockWriter():
    pass


class MockIntentHandler():
    pass


class TestRtmEventHandler():

    def setup_method(self):
        self.e_handler = RtmEventHandler(MockClient(),
                                         MockWriter(),
                                         MockIntentHandler())

    def test_parse_login_details(self):
        test_msg = "<@arXie-bot> user: username pw: password"
        user, pw = self.e_handler.parse_login_details(test_msg)

        assert user == "username" and pw == "password"

    def test_parse_login_details_fail(self):
        test_msg = "<@arXie-bot> user: thisistheuser password: blah"
        user, pw = self.e_handler.parse_login_details(test_msg)

        assert user is None and pw is None
