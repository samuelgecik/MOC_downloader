import aiohttp
import asyncio
from video import Video
from scraping import LinkScraper

TIMEOUT = aiohttp.ClientTimeout(total=60*60)


class CourseInfo:
    def __init__(self, scraper: LinkScraper) -> None:
        self.scraper = scraper
        self.website = self.scraper.website
        self.videos = list[Video]
        self.course_name = self.get_course_name()
        self.total_size = self.get_total_size()

    async def get_videos(self):
        """
        Retrieves the video lectures from the website.

        Returns:
            list: A list of Video objects.
        """
        async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
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