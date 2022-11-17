"""
Periodically scrapes the given givesendgo campaign and saves the data to a database.
"""
import asyncio
from dataclasses import dataclass
from givesendgoscraper.scraper import scrape_givesendgo


DEFAULT_SLEEP = 60 * 10


@dataclass
class CampaignData:
    """Campaign data."""

    goal: str = ""
    raised: str = ""


CAMPAIGN_DATA = CampaignData()


def get_campaign_data() -> CampaignData:
    """Get the campaign data."""
    return CAMPAIGN_DATA


async def scraper_task(gsg_id) -> None:
    """Periodically scrapes the given givesendgo campaign and saves the data to a database."""
    while True:
        try:
            data = scrape_givesendgo(gsg_id)
            CAMPAIGN_DATA.goal = data["goal"]
            CAMPAIGN_DATA.raised = data["raised"]
        except Exception as exc:  # pylint: disable=broad-except
            print(exc)
        await asyncio.sleep(DEFAULT_SLEEP)
