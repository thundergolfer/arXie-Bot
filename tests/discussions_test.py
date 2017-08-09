from mock import patch
from tests.support.reddit_search_api import example_response_str

from bot.discussions import reddit_conversations

class MockResponse():
    def __init__(self):
        self.content = example_response_str

@patch('bot.site_scraping.requests.get')
def test_reddit_conversations(mock_get):
    mock_get.return_value = MockResponse()

    expected = ('/r/MachineLearning',
                'https://www.reddit.com/r/MachineLearning/comments/6fswmw/r_onesided_unsupervised_domain_mapping/',
                3)

    assert expected == reddit_conversations("https://arxiv.org/abs/1706.00826")
