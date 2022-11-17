"""
    Give send go response
"""

# pylint: disable=fixme,broad-except,logging-fstring-interpolation,too-many-locals,redefined-builtin,invalid-name,too-many-branches,too-many-return-statements

import os
from givesendgoscraper.version import VERSION
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from fastapi.responses import RedirectResponse, JSONResponse
from keyvalue_sqlite import KeyValueSqlite

from givesendgoscraper.scraper import scrape_givesendgo

STARTUP_DATETIME = datetime.now()

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_ROOT = os.path.join(PROJECT_ROOT, "data")
DB_PATH = f"{PROJECT_ROOT}/data/db.sqlite"

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def app_description() -> str:
    """Get the app description."""
    lines = []
    lines.append("# Givesendgoscraper")
    lines.append("  * Version: " + VERSION)
    lines.append("  * Started at: " + str(STARTUP_DATETIME))
    # os.env
    for key, value in os.environ.items():
        lines.append(f"  * {key}: {value}")
    return "\n".join(lines)


app = FastAPI(
    title="Video Server",
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
async def get(gsg_id: str | None = "maryamhenein") -> JSONResponse:
    """TODO - Add description."""
    url = f"https://www.givesendgo.com/{gsg_id}"
    try:
        return scrape_givesendgo(gsg_id)
    except Exception as e:
        import traceback
        stack_trace = traceback.format_exc()
        return JSONResponse(
            status_code=500,
            content={"error": str(e)},
            stacktrace=stack_trace
        )
