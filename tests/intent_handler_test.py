from mock import patch
from bot.intent_handler import ApiAiIntentHandler
from bot.formatter import paper_snippet
from tests.support.papers import dummy_papers


class MockClient():
    def bot_user_id(self):
        return 'mr. mockbot'

class TestApiAiIntentHandler():

    def setup_method(self):
        self.intent_handler = ApiAiIntentHandler(MockClient())

    @patch('bot.intent_handler.ApiAiIntentHandler.search_arxiv', return_value="Here's your answer")
    def test_handle_intent(self, mock_handler):
        test_txt = "search for SOMETHING"
        test_intent = "search"
        arXiv_msg, _ = self.intent_handler.handle_intent(test_txt, test_intent, None)

        assert "Here's your answer" == arXiv_msg

        test_txt = "let's do something else"
        test_intent = "not search"
        arXiv_msg, _ = self.intent_handler.handle_intent(test_txt, test_intent, None)

        assert "NOT YET IMPLEMENTED" == arXiv_msg

    @patch('bot.intent_handler.papers_from_embedded_script', return_value=dummy_papers)
    @patch('bot.intent_handler.build_message', return_value="whatever")
    def test_search_arxiv(self, mock_build_msg, mock_papers_from):
        query = "this is a search query"

        dummy_parts = []
        for i in range(len(dummy_papers)):
            dummy_parts.append(paper_snippet(dummy_papers[i], i + 1))

        dummy_parts[-1]['footer'] = "> `<@" + self.intent_handler.clients.bot_user_id() + "> show more papers` - to see more papers"

        self.intent_handler.search_arxiv(query)

        mock_build_msg.assert_called_with(text="*Search Results*", markdown=False, parts=dummy_parts)
