import aiohttp
import asyncio
from tqdm import tqdm

TIMEOUT = aiohttp.ClientTimeout(total=60*60)

class Downloader():
    def __init__(self, download_links, output_folder):
        self.download_links = download_links
        self.output_folder = output_folder
        self.session = aiohttp.ClientSession(timeout=TIMEOUT)
        self.sizes = self.get_sizes(self.session)
        self.total_size = 0

    async def get_sizes(self):
        sizes = []
        for url in self.download_links:
            async with self.session.get(url) as response:
                sizes.append(int(response.headers['Content-Length']))
        return sizes


    async def download_file(self, session, url, filename):
        async with session.get(url) as response:
            with open(filename, 'wb') as f:
                total_downloaded = 0
                async for chunk in response.content.iter_any():
                    f.write(chunk)
                    total_downloaded += len(chunk)
            return total_downloaded

    async def download(self, indicies: list):
        async with self.session as session:
            tasks = []
            for link in [self.download_links[x] for x in indicies]:
                filename = link[link.rindex('/') + 1:]
                tasks.append(self.download_file(session, link, filename))
            await asyncio.gather(*tasks)
 