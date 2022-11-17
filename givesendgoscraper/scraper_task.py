"""
Periodically scrapes the given givesendgo campaign and saves the data to a database.
"""
import asyncio
from dataclasses import dataclass
from givesendgoscraper.scraper import async_scrape_givesendgo

FAST_SLEEP = 60 * 10  # Every 10 mins
DEFAULT_SLEEP = 60 * 60 * 4  # Every 4 hours


@dataclass
class CampaignData:
    """Campaign data."""

    goal: str = ""
    raised: str = ""


CAMPAIGN_DATA = CampaignData()
TRIGGERED = False


def get_campaign_data() -> CampaignData:
    """Get the campaign data."""
    return CAMPAIGN_DATA


def trigger_scrape() -> None:
    """Trigger a scrape."""
    global TRIGGERED  # pylint: disable=global-statement
    TRIGGERED = True


async def scraper_task(gsg_id) -> None:
    """Periodically scrapes the given givesendgo campaign and saves the data to a database."""
    global TRIGGERED  # pylint: disable=global-statement
    while True:
        try:
            data = await async_scrape_givesendgo(gsg_id)
            CAMPAIGN_DATA.goal = data["goal"]
            CAMPAIGN_DATA.raised = data["raised"]
        except Exception as exc:  # pylint: disable=broad-except
            print(exc)
        sleep = DEFAULT_SLEEP
        if TRIGGERED:
            sleep = FAST_SLEEP
            TRIGGERED = False
        await asyncio.sleep(sleep)
