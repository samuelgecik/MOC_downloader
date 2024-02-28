import aiohttp

TIMEOUT = aiohttp.ClientTimeout(total=60*60)


class Video:
    def __init__(self, url: str, session: aiohttp.ClientSession):
        self.url = url
        self.session = session
        self.name = self.get_name()
        self.size = None
        self.download = True

    def get_name(self):
        return self.url[self.url.rfind("/") + 1 :]
    
    async def get_size(self):
        if self.size is None:  # Only make the request if size hasn't been retrieved yet
            async with self.session.get(self.url) as response:
                self.size = int(response.headers['Content-Length'])
        return self.size