import asyncio
import utils.Spider as Spider

async def scraper():
    async with Spider.Spider() as spider:
        links = await spider.collect_links("IBA Sukkur", 100)
        await spider.collect_education(links)

asyncio.run(scraper())