from bot.formatter import build_message, paper_snippet, make_pdf_link
import json


def test_build_message_markdown_false():
    test_text = "This is some text, yay."

    assert test_text == build_message(test_text, markdown=False)


def test_build_message_markdown_true():
    test_markdown = "## Heading \n\n * This is a bullet-point."

    expected_msg = {"text": "## Heading \n\n * This is a bullet-point.", "mrkdwn": True}

    msg = build_message(test_markdown, markdown=True)

    assert expected_msg == json.loads(msg)

def test_make_pdf_link():
    paper_id = 12345
    expected_link = 'http://www.arxiv-sanity.com/pdf/12345.pdf'

    assert expected_link == make_pdf_link(paper_id)


def test_paper_snippet():
    paper = {
        'link': "www.paper_link.com",
        'title': "A Paper Title",
        'authors': ['A. Scott', 'F. Itzgerald', 'M. Wallis'],
        'originally_published_time': '3:30 pm',
        'pid': 123982409
    }

    expected_snippet = {
        'fallback': 'A Paper Title',
        'text': '<www.paper_link.com|1. A Paper Title>\nA. Scott, F. Itzgerald, M. Wallis - 3:30 pm\n<http://www.arxiv-sanity.com/pdf/123982409.pdf|PDF>\n'
    }

    assert expected_snippet == paper_snippet(paper, 1)
