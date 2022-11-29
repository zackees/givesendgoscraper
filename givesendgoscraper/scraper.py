"""
Module for scraping givesendgo pages.
"""

from bs4 import BeautifulSoup  # type: ignore
from open_webdriver import open_webdriver  # type: ignore


def _add_dollar_sign_if_missing(number: str) -> str:
    """Add a dollar sign to a number."""
    if "$" in number:
        return number  # Dollar sign already added.
    return f"${number}"


def _parse_raised_goal(text: str) -> dict[str, str]:
    """Parsed the html after it has been scraped."""
    soup = BeautifulSoup(text, "html.parser")
    dom = soup.find("div", class_="donation-amount-section")
    assert dom is not None
    # There are lots of spaces and newlines in the HTML, so we need to strip them
    text = dom.text
    lines = text.split("\n")
    lines = [line.strip() for line in lines if line.strip()]
    text = "\n".join(lines)
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
            data["goal"] = _add_dollar_sign_if_missing(goal)
        if "raised" in piece_lower:
            items = piece.split(":")
            raised = items[1].strip()
            data["raised"] = _add_dollar_sign_if_missing(raised)
    return data


def _parse_number_donars(text: str) -> str:
    """Parsed the total number of donors."""
    soup = BeautifulSoup(text, "html.parser")
    doms = soup.find_all("a", class_="btn btn-style-4 w-100")
    for dom in doms:
        text = dom.text
        if "Give" in text:
            text = text.replace("Give", "").replace("\n", "").strip()
            return text
    print("Error could not find number of donars")
    return ""


def _parse_recent_donations(text: str) -> list[dict[str, list]]:
    """Parse the recent donations"""
    soup = BeautifulSoup(text, "html.parser")
    container = soup.find("ul", class_="donatecount")
    doms = container.find_all("li")
    donations: list[dict[str, list]] = []
    for dom in doms:
        name = dom.find("h3").text.strip()
        amount = dom.find("div", class_="amount").text.replace("USD", "").strip().replace("$ ", "$")
        when = dom.find("p").text.strip()
        comment = dom.find("em").text.strip()
        donation = {
            "name": name,
            "amount": amount,
            "when": when,
            "comment": comment,
        }
        donations.append(donation)
    return donations


def _get_html(gsg_id: str) -> str:
    """Scrape the givesendgo page."""
    url = f"https://www.givesendgo.com/{gsg_id}"
    with open_webdriver() as driver:
        driver.get(url)
        # print driver.page_source
        return driver.page_source


def scrape_givesendgo(gsg_id: str) -> dict[str, str | list]:
    """Scrape the givesendgo page."""
    text = _get_html(gsg_id)
    data: dict[str, str | list] = {}
    data.update(_parse_raised_goal(text))
    data["donors"] = _parse_number_donars(text)
    data["recent_donations"] = _parse_recent_donations(text)
    return data


def main() -> dict:
    """Run the main function."""
    gsg_id = "maryamhenein"
    result = scrape_givesendgo(gsg_id)
    return result


if __name__ == "__main__":
    print(main())
