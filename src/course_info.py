import aiohttp
import asyncio
from .scraping import LinkScraper
from .video import Video

TIMEOUT = aiohttp.ClientTimeout(total=60*60)


class CourseInfo:
    def __init__(self, videos: list[Video], course_name, total_size) -> None:
        self.videos = videos
        self.course_name = course_name
        self.total_size = total_size

    @classmethod
    async def create(cls, scraper: LinkScraper):
        cls.scraper = scraper
        cls.website = scraper.website
        async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
            videos = await cls.get_videos(cls, session)
            await asyncio.gather(*[video.get_size() for video in videos])
        course_name = cls.get_course_name(cls)
        total_size = sum([video.size for video in videos])
        return cls(videos, course_name, total_size)

    async def get_videos(self, session: aiohttp.ClientSession):
        """
        Retrieves the video lectures from the website.

        Returns:
            list: A list of Video objects.
        """
        return [Video(url, session) for url in self.scraper.download_links]

    def get_course_name(self):
        """
        Retrieves the course name from the website URL.

        Returns:
            str: The course name.
        """
        return (
            self.website[self.website.rfind("/", 0, -1) :]
            .replace("/", "")
            .replace("-", " ")
            .title()
        )
    
    def get_total_size(self):
        """
        Retrieves the total size of all the video lectures.

        Returns:
            int: The total size of all the video lectures.
        """
        return sum([video.size for video in self.videos])