from bs4 import BeautifulSoup

def scrapePhImg(response):
    try:
        soup = BeautifulSoup(response.text, 'html.parser')

        image = soup.find('img', {'id':"videoElementPoster"})

        return image['src']
    except:
        pass

    # print(image.attrs)





