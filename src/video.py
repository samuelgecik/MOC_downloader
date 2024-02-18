import aiohttp
import asyncio

TIMEOUT = aiohttp.ClientTimeout(total=60*60)


class Video:
    def __init__(self, url: str, session: aiohttp.ClientSession):
        self.url = url
        self.session = session
        self.name = self.get_name()
        self.size = self.get_size()
        self.download = True

        def get_name(self):
            return self.url[self.url.rfind("/") + 1 :]
        
        async def get_size(self):
            async with self.session.get(url) as response:
                return int(response.headers['Content-Length'])
