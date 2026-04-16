# Future Imports
from __future__ import annotations

# Standard Library Imports
import asyncio
import io

# Dependency Imports
from playwright.async_api import async_playwright, Error as PlaywrightError


async def screenshot(link: str, wait: int = 3):
    """
    Screenshots a given link.
    If no time is given, it will wait 3 seconds to screenshot
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 720})
        try:
            await page.goto(link)
        except PlaywrightError:
            await browser.close()
            return
        except Exception:
            await browser.close()
            return

        await asyncio.sleep(wait)
        result = await page.screenshot()
        await browser.close()
        f = io.BytesIO(result)
        return f
