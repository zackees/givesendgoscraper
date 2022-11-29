"""
    Give send go response
"""

# pylint: disable=fixme,broad-except,logging-fstring-interpolation,too-many-locals,redefined-builtin,invalid-name,too-many-branches,too-many-return-statements

import asyncio
import os
import traceback
import json
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse

from givesendgoscraper.scraper import scrape_givesendgo
from givesendgoscraper.scraper_task import (
    scraper_task,
    get_campaign_data,
    trigger_scrape,
)
from givesendgoscraper.version import VERSION

STARTUP_DATETIME = datetime.now()

IS_TEST = os.environ.get("IS_TEST", "0") == "1"
GIVE_SEND_GO_ID = os.environ.get("GIVE_SEND_GO_ID", "maryamhenein")


def app_description() -> str:
    """Get the app description."""
    lines = []
    lines.append("  * Version: " + VERSION)
    lines.append("  * Started at: " + str(STARTUP_DATETIME))
    if IS_TEST:
        for key, value in os.environ.items():
            lines.append(f"  * {key}: {value}")
    return "\n".join(lines)


app = FastAPI(
    title="Givesendgoscraper",
    version=VERSION,
    redoc_url=None,
    license_info={
        "name": "Private program, do not distribute",
    },
    description=app_description(),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event() -> None:
    """Adds the background task to scrape the campaign."""

    async def task() -> None:
        """Run the task."""
        await scraper_task(GIVE_SEND_GO_ID)

    # run the task in the background
    asyncio.create_task(task())


@app.get("/", include_in_schema=False)
async def index() -> RedirectResponse:
    """By default redirect to the fastapi docs."""
    return RedirectResponse(url="/docs", status_code=302)


# Redirect to favicon.ico
@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> RedirectResponse:
    """Returns favico file."""
    return RedirectResponse(url="/www/favicon.ico")


@app.get("/get")
async def get() -> JSONResponse:
    """Get's the current campaign data."""
    try:
        data: dict[str, str | list] = get_campaign_data()
        trigger_scrape()
        return JSONResponse(status_code=200, content=data)
    except Exception as e:  # pylint: disable=broad-except
        stack_trace = traceback.format_exc()
        payload = {
            "error": str(e),
            "stack_trace": stack_trace,
        }
        return JSONResponse(status_code=500, content=payload)


if IS_TEST:

    @app.get("/test")
    async def test_scrape(gsg_id: str = GIVE_SEND_GO_ID) -> JSONResponse:
        """Test scraping"""
        try:
            data = scrape_givesendgo(gsg_id)
            return JSONResponse(status_code=200, content=data)
        except Exception as e:  # pylint: disable=broad-except
            stack_trace = traceback.format_exc()
            payload = {
                "error": str(e),
                "stack_trace": stack_trace,
            }
            return JSONResponse(status_code=500, content=payload)
