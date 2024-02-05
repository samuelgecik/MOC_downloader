from bs4 import BeautifulSoup
import requests

class LinkScraper():
    def __init__(self, website):
        self.website = website
        self.course_name = self.get_course_name()
        self.page = requests.get(website)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')

    def get_course_name(self):
        return self.website[self.website.rfind('/')+1:].replace('-', ' ').title()

    def get_download_link(self):
        download_button = self.soup.find('a', "download-course-link-button")
        # if there is no download button, means the user already provided the download site
        if download_button is None:
            return ''
        return download_button['href']

    def get_video_lectures(self):
        video_lectures = self.soup.find_all('div', id="resource-list-container-lecture-videos")
        download_paragraphs = video_lectures[0].find_all('a', class_="resource-thumbnail")
        download_links = []
        for paragraph in download_paragraphs:
            download_links.append(paragraph['href'])
        return download_links

    def get_all_links(self):
        main_site = self.website[:self.website.find('/', 8)]
        download_page = requests.get(main_site + self.get_download_link())
        soup = BeautifulSoup(download_page.content, 'html.parser')
        return self.get_video_lectures(soup)
    