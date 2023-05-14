from bs4 import BeautifulSoup

class Scraper():
    def __init__(self, response):
        self.soup = BeautifulSoup(response.text, 'html.parser')

    def scrapeImg(self):
        try:
            image = self.soup.find('img', {'id':"videoElementPoster"})

            return image['src']
        except:
            pass

    def scrapeTitle(self):
        try:
            title = self.soup.select('h1.title > span')
            return title[0].text

        except:
            pass





