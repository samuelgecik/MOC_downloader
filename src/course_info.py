from scraping import LinkScraper


class Video:
    def __init__(self, url: str, name: str, size: int, download: bool) -> None:
        self.url = url
        self.name = name
        self.size = size
        self.download = download


class CourseInfo:
    def __init__(self, scraper: LinkScraper) -> None:
        self.scraper = scraper
        self.website = self.scraper.website
        self.course_name = self.get_course_name()

        self.video_urls = self.scraper.get_videos()

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
