"""
Module for scraping givesendgo pages.
"""

from bs4 import BeautifulSoup  # type: ignore
from open_webdriver import open_webdriver  # type: ignore


def _parse_html(text: str) -> dict[str, str]:
    """Parsed the html after it has been scraped."""
    soup = BeautifulSoup(text, "html.parser")
    dom = soup.find("div", class_="donation-amount-section")
    assert dom is not None
    # There are lots of spaces and newlines in the HTML, so we need to strip them
    text = dom.text
    text = text.replace(" :", ":")
    text = text.replace(":\n", ":")
    text = text.replace("$ ", "$")
    text = text.replace("USD", "")
    text = text.strip()
    while "  " in text:
        text = text.replace("  ", " ")
    pieces = text.split("\n")
    data = {}
    for piece in pieces:
        piece_lower = piece.lower()
        if "goal" in piece_lower:
            items = piece.split(":")
            goal = items[1].strip()
            data["goal"] = goal
        if "raised" in piece_lower:
            items = piece.split(":")
            raised = items[1].strip()
            data["raised"] = raised
    return data


def _get_html(gsg_id: str) -> str:
    """Scrape the givesendgo page."""
    url = f"https://www.givesendgo.com/{gsg_id}"
    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        " AppleWebKit/537.36 (KHTML, like Gecko)"
        " Chrome/107.0.0.0 Safari/537.36"
    )
    with open_webdriver(user_agent=user_agent) as driver:
        driver.get(url)
        # print driver.page_source
        return driver.page_source


def scrape_givesendgo(gsg_id: str) -> dict:
    """Scrape the givesendgo page."""
    text = _get_html(gsg_id)
    data = _parse_html(text)
    return data


def main() -> dict:
    """Run the main function."""
    gsg_id = "maryamhenein"
    result = scrape_givesendgo(gsg_id)
    return result


if __name__ == "__main__":
    print(main())
