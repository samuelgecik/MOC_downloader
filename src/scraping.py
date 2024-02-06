from bs4 import BeautifulSoup
import requests


class LinkScraper:
    def __init__(self, website):
        """
        Initializes a LinkScraper object.

        Args:
            website (str): The URL of the MIT course website to scrape.
        """
        self.website = website
        self.course_name = self.get_course_name()
        self.page = requests.get(website)
        self.soup = BeautifulSoup(self.page.content, "html.parser")

    def get_course_name(self):
        """
        Retrieves the course name from the website URL.

        Returns:
            str: The course name.
        """
        return self.website[self.website.rfind("/", 0, -1) :].replace("/", "").replace("-", " ").title()


    def get_download_link(self):
        """
        Retrieves the download link for the course.

        Returns:
            str: The download link for the course, or an empty string if no download button is found.
        """
        download_button = self.soup.find("a", "download-course-link-button")
        # if there is no download button, means the user already provided the download site
        if download_button is None:
            return ""
        return download_button["href"]

    def get_video_lectures(self):
        """
        Retrieves the download links for the video lectures.

        Returns:
            list: A list of download links for the video lectures.
        """
        video_lectures = self.soup.find_all(
            "div", id="resource-list-container-lecture-videos"
        )
        download_paragraphs = video_lectures[0].find_all(
            "a", class_="resource-thumbnail"
        )
        download_links = []
        for paragraph in download_paragraphs:
            download_links.append(paragraph["href"])
        return download_links

    def get_all_links(self):
        """
        Retrieves all the download links for the course.

        Returns:
            list: A list of download links for the course.
        """
        main_site = self.website[: self.website.find("/", 8)]
        download_page = requests.get(main_site + self.get_download_link())
        soup = BeautifulSoup(download_page.content, "html.parser")
        return self.get_video_lectures(soup)
