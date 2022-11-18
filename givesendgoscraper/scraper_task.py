"""
Periodically scrapes the given givesendgo campaign and saves the data to a database.
"""
import asyncio
import time
from dataclasses import dataclass
from givesendgoscraper.scraper import scrape_givesendgo

FAST_SLEEP = 60 * 10  # Every 10 mins
DEFAULT_SLEEP = 60 * 60 * 4  # Every 4 hours


@dataclass
class CampaignData:
    """Campaign data."""

    goal: str = ""
    raised: str = ""
    donors: str = ""

    # converter to json
    def to_json(self) -> dict:
        """Convert to json."""
        return {
            "goal": self.goal,
            "raised": self.raised,
            "donors": self.donors,
        }


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
            data = scrape_givesendgo(gsg_id)
            CAMPAIGN_DATA.goal = data["goal"]
            CAMPAIGN_DATA.raised = data["raised"]
            CAMPAIGN_DATA.donors = data["donors"]

        except Exception as exc:  # pylint: disable=broad-except
            print(exc)
        long_future_time = time.time() + DEFAULT_SLEEP
        while time.time() < long_future_time:
            if TRIGGERED:
                TRIGGERED = False
                break  # break out of the inner loop
            await asyncio.sleep(FAST_SLEEP)
