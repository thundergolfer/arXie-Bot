from mock import patch, Mock
from bot.intent_handler import ApiAiIntentHandler
from bot.formatter import paper_snippet
from tests.support.papers import dummy_papers


class MockClient():
    def bot_user_id(self):
        return 'mr. mockbot'

class MockRequest():
    def __init__(self):
        self.status_code = 200

class MockSession():
    def post(self, url, data):
        return MockRequest()


class TestApiAiIntentHandler():
    def setup_method(self):
        self.intent_handler = ApiAiIntentHandler(MockClient())

        self.dummy_parts = []
        for i in range(len(dummy_papers)):
            self.dummy_parts.append(paper_snippet(dummy_papers[i], i + 1))

    @patch('bot.intent_handler.ApiAiIntentHandler.search_arxiv', return_value="Here's your answer")
    def test_handle_intent(self, mock_handler):
        test_txt = "search for SOMETHING"
        test_intent = "search"
        arXiv_msg, _ = self.intent_handler.handle_intent(test_txt, test_intent, None)

        assert "Here's your answer" == arXiv_msg

        test_txt = "let's do something else"
        test_intent = "not search"
        arXiv_msg, _ = self.intent_handler.handle_intent(test_txt, test_intent, None)

        assert "Intent 'not search' not yet implemented." == arXiv_msg

    @patch('bot.intent_handler.papers_from_embedded_script', return_value=dummy_papers)
    @patch('bot.intent_handler.build_message', return_value="whatever")
    def test_search_arxiv(self, mock_build_msg, mock_papers_from):
        query = "this is a search query"

        self.intent_handler.search_arxiv(query)
        self.dummy_parts[-1]['footer'] = "> `<@" + self.intent_handler.clients.bot_user_id() + "> show more papers` - to see more papers"

        mock_build_msg.assert_called_with(text="*Search Results*",
                                          markdown=False,
                                          parts=self.dummy_parts)

    @patch('bot.intent_handler.papers_from_embedded_script', return_value=dummy_papers)
    @patch('tests.intent_handler_test.MockSession.post', return_value=MockRequest())
    def test_clear_library(self, mock_post, mock_papers_from):
        mock_session = MockSession()
        self.intent_handler.clear_library(mock_session)

        assert mock_post.call_count == 4

    @patch('bot.intent_handler.papers_from_embedded_script', return_value=dummy_papers)
    @patch('bot.intent_handler.build_message', return_value="whatever")
    def test_library(self, mock_build_msg, mock_papers_from):
        mock_session = MockSession()

        self.intent_handler.get_library(mock_session)

        mock_build_msg.assert_called_with(text="*Your Library*",
                                          markdown=False,
                                          parts=self.dummy_parts)

    @patch('bot.intent_handler.papers_from_embedded_script', return_value=dummy_papers)
    @patch('bot.intent_handler.build_message', return_value="whatever")
    def test_get_most_recent(self, mock_build_msg, mock_papers_from):
        class MockUser():
            def __init__(self):
                self.session = MockSession()

        mock_session = MockSession()

        self.intent_handler.get_most_recent(MockUser())

        mock_build_msg.assert_called_with(text="*Your Most Recent*",
                                          markdown=False,
                                          parts=self.dummy_parts)

    @patch('bot.intent_handler.papers_from_embedded_script', return_value=dummy_papers)
    @patch('bot.intent_handler.build_message', return_value="whatever")
    def test_get_paper(self, mock_build_msg, mock_papers_from):
        mock_session = MockSession()
        test_pid = 1000 # will be ignored
        self.intent_handler.get_paper(None, test_pid)

        mock_build_msg.assert_called_with(text="*Here's your paper*",
                                          markdown=False,
                                          parts=[self.dummy_parts[0]])

    def test_get_recommended(self):
        pass

    def test_get_top_recent(self):
        pass

    def test_get_similar(self):
        pass

    @patch('bot.intent_handler.build_message', return_value="whatever")
    def goto_website(self, mock_build_msg):
        self.intent_handler.goto_website()

        mock_build_msg.assert_called_with(text='http://www.arxiv-sanity.com/',
                                          markdown=False,
                                          parts=None)

    @patch('bot.intent_handler.papers_from_embedded_script', return_value=dummy_papers)
    @patch('tests.intent_handler_test.MockSession.post', return_value=MockRequest())
    def save_paper(self):
        mock_session = MockSession()
        test_paper = {'pid': 1000}

        self.intent_handler.save_paper(test_paper, mock_session)

        mock_post.assert_called_with('http://www.arxiv-sanity.com/libtoggle', data = {'pid': 1000})
