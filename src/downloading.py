import aiohttp
import asyncio
from tqdm import tqdm

class Downloader():
    def __init__(self, download_links):
        self.download_links = download_links
        self.total_size = 0

    async def get_size(self, session, url):
        async with session.get(url) as response:
            return int(response.headers['Content-Length'])

    async def download_file(self, session, url, filename):
        async with session.get(url) as response:
            with open(filename, 'wb') as f:
                total_downloaded = 0
                async for chunk in response.content.iter_any():
                    f.write(chunk)
                    total_downloaded += len(chunk)
            return total_downloaded

    async def run(self):
        timeout = aiohttp.ClientTimeout(total=60*60)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            tasks = []
            # Get sizes of all files
            sizes = await asyncio.gather(*(self.get_size(session, link) for link in self.download_links[:2]))
            total_size = sum(sizes)
            for link in self.download_links[:2]:
                filename = link[link.rindex('/') + 1:]
                tasks.append(self.download_file(session, link, filename))
            await asyncio.gather(*tasks)
            print(f'Total downloaded size: {total_size} bytes')

    async def run(self):
        await self.run()

 