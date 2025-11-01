# etl/source_ll.py
import asyncio
import httpx

BASE_URL = "https://ll.thespacedevs.com/2.2.0/launch/upcoming/"
PAGE_SIZE = 50

async def _get(client: httpx.AsyncClient, url: str, attempt: int = 1, max_attempts: int = 5):
    try:
        r = await client.get(url, timeout=20)
        r.raise_for_status()
        return r.json()
    except Exception:
        if attempt < max_attempts:
            await asyncio.sleep(2 ** attempt)  # backoff: 2,4,8,16...
            return await _get(client, url, attempt + 1, max_attempts)
        raise

async def fetch_upcoming_all(limit_pages: int = 3):
    results = []
    next_url = f"{BASE_URL}?limit={PAGE_SIZE}"
    async with httpx.AsyncClient() as client:
        for _ in range(limit_pages):
            payload = await _get(client, next_url)
            results.extend(payload.get("results", []))
            next_url = payload.get("next")
            if not next_url:
                break
    return results

async def fetch_upcoming():
    data = await fetch_upcoming_all(limit_pages=1)
    return data

async def fetch_data():
    return await fetch_upcoming_all(limit_pages=1)

__all__ = ["fetch_upcoming_all", "fetch_upcoming", "fetch_data"]
