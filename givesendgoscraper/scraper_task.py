"""
Periodically scrapes the given givesendgo campaign and saves the data to a database.
"""
import asyncio
import time
from givesendgoscraper.scraper import scrape_givesendgo

FAST_SLEEP = 60 * 10  # Every 10 mins
DEFAULT_SLEEP = 60 * 60 * 4  # Every 4 hours

CAMPAIGN_DATA: dict[str, str | list] = {}
TRIGGERED = False


def get_campaign_data() -> dict[str, str | list]:
    """Get the campaign data."""
    return CAMPAIGN_DATA


def trigger_scrape() -> None:
    """Trigger a scrape."""
    global TRIGGERED  # pylint: disable=global-statement
    TRIGGERED = True


async def scraper_task(gsg_id) -> None:
    """Periodically scrapes the given givesendgo campaign and saves the data to a database."""
    global TRIGGERED, CAMPAIGN_DATA  # pylint: disable=global-statement
    while True:
        try:
            data: dict[str, str | list] = scrape_givesendgo(gsg_id)
            CAMPAIGN_DATA = data
        except Exception as exc:  # pylint: disable=broad-except
            print(exc)
        long_future_time = time.time() + DEFAULT_SLEEP
        while time.time() < long_future_time:
            if TRIGGERED:
                TRIGGERED = False
                break  # break out of the inner loop
            await asyncio.sleep(FAST_SLEEP)
