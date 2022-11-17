
from bs4 import BeautifulSoup
from open_webdriver import open_webdriver

def scrape_givesendgo(gsg_id: str) -> dict:
    """Scrape the givesendgo page."""
    url = f"https://www.givesendgo.com/{gsg_id}"
    # os.system('Xvfb -ac :99 -screen 0 1280x1024x16 &')

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"

    with open_webdriver(user_agent=user_agent) as driver:
        driver.get(url)
        return {"title": driver.title}


def main() -> None:
    """Run the main function."""
    gsg_id = "maryamhenein"
    result = scrape_givesendgo(gsg_id)
    return result

if __name__ == "__main__":
    result = main()
    print(result)