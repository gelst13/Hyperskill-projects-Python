import string
import requests
from bs4 import BeautifulSoup
import os


class Parser:
    def __init__(self):
        self.url = 'https://www.nature.com/nature/articles'
        self.n_pages = int(input('Input number of pages for web-scraping: > '))
        self.art_type = input()  # define type of articles that this web-scraper is going to find and store
        self.r = None

    def parse(self):
        try:
            self.r = requests.get(self.url, headers={'Accept-Language': 'en-US,en;q=0.5'})
            if self.r.status_code == 200:
                try:
                    web_url = 'https://www.nature.com'
                    main_working_dir = os.getcwd()
                    for page in range(self.n_pages):
                        # go to or return inside directory, where we'll store new folders with files in them
                        os.chdir(main_working_dir)
                        # so r1 is a response-object for each page inside https://www.nature.com/nature/articles
                        # while cycle goes through range (1-n_pages)
                        r1 = requests.get('https://www.nature.com/nature/articles/', params={'page': f'{page + 1}'})
                        # soup1 is the parser, created from r1
                        soup1 = BeautifulSoup(r1.content, 'html.parser')
                        # create a new directory for each page while cycle goes through range (1-n_pages)
                        new_dir = f'Page_{page + 1}'
                        os.mkdir(new_dir)
                        os.chdir(new_dir)  # go inside newly created directory Page_N in order to put a file here

                        for article in soup1.find_all('article'):
                            if article.find('span', {'class': "c-meta__type"}).text.strip() == self.art_type:
                                # take link of an article of needed type
                                link_relative = article.find('a', {'data-track-action': 'view article'})['href']
                                # create absolute path to the article
                                link_abs = web_url + link_relative
                                # take title of the article
                                art_title = article.h3.text
                                # r2 is is a response-object for the page of the article
                                r2 = requests.get(link_abs)
                                # soup1 is the parser, created from the page of the article
                                soup2 = BeautifulSoup(r2.content, 'html.parser')

                                # delete punctuation marks and replace whitespaces by _
                                translation_table = str.maketrans("", "", string.punctuation)
                                art_title = art_title.translate(translation_table)
                                art_title = art_title.replace(" ", "_")
                                art_title = art_title.strip('\n')
                                # print(art_title)

                                # find body of the article - there are 2 possible options on this site
                                # take article text from the body
                                art_body = soup2.body.find('div', class_="c-article-body u-clearfix")
                                if not art_body:
                                    art_body1 = soup2.body.find('div', class_="article-item__body").text.strip()
                                    text = art_body1
                                else:
                                    text = soup2.body.find('div', class_="c-article-body u-clearfix").text.strip()

                                # put text into new file - and encode it during this process
                                with open(f'{art_title}.txt', 'wb') as f:
                                    f.write(text.encode('UTF-8'))


                except TypeError:
                    print('Invalid page!')

            else:
                print(f"The URL returned {self.r.status_code}!")
        except requests.exceptions.RequestException:
            print('Invalid !')


new = Parser()
Parser.parse(new)
