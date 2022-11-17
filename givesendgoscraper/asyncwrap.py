"""
Turns a function into an async function.
"""

import asyncio
from functools import partial, wraps


def asyncwrap(func):
    """Wrap a function to run in an async loop"""

    @wraps(func)
    async def run(
        *args, loop=None, executor=None, **kwargs
    ):  # pylint: disable=unused-argument
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)

    return run
