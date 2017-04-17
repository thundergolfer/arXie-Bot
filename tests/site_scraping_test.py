from mock import patch

from bot.site_scraping import paper_titles, papers_from_embedded_script
from tests.support.arxiv_sanity import page_html

class MockResponse():
    def __init__(self):
        import pdb; pdb.set_trace()
        self.text = page_html

@patch('bot.site_scraping.requests.get')
def test_papers_from_embedded_script(mock_get):
    mock_get.return_value = MockResponse()

    papers = papers_from_embedded_script("http://www.arxiv-sanity.com/")

    assert "sfmwef2" == papers
