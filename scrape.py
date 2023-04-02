from bs4 import BeautifulSoup
import json
import asyncio
import aiohttp
from asyncio_throttle import Throttler
from tqdm import tqdm


async def fetch_website(throttler, session, website):
    try:
        async with throttler:
            async with session.get(website) as response:
                text = await response.text()
                soup = BeautifulSoup(text, "html.parser")
                contents = soup.find("body").text
                data = {"website_name": website, "contents": contents}
                return data
    except Exception as e:
        return {"website_name": website, "contents": None, "error": str(e)}


async def main():
    open("results.jsonl", "w").close()

    with open("websites") as f:
        websites = f.read().split("\n")
        websites = list(map(lambda website: f"https://{website}", websites))

    async with aiohttp.ClientSession() as session:
        throttler = Throttler(rate_limit=5)
        tasks = []
        for website in websites:
            task = asyncio.ensure_future(fetch_website(throttler, session, website))
            tasks.append(task)

        with open("results.jsonl", "a") as outfile:
            for coro in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
                result = await coro
                outfile.write(json.dumps(result) + "\n")
                outfile.flush()


if __name__ == "__main__":
    asyncio.run(main())
