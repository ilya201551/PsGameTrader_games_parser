import requests
from bs4 import BeautifulSoup as bs


BASE_URL = 'https://nextgame.net'
GAMES_CATALOG_URL = 'https://nextgame.net/catalog/sony-playstation4/games-ps4/'

HEADERS = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3'
}


class GamesLinksParser:

    def __init__(self, headers, session, base_url, games_catalog_url):
        self.session = session
        self.headers = headers
        self.base_url = base_url
        self.games_catalog_url = games_catalog_url
        self.pages_number = self.__get_pages_number()
        self.pages_urls_list = self.__get_pages_urls_list()

    def __get_pages_number(self):
        request = self.session.get(self.games_catalog_url, headers=self.headers)
        soup = bs(request.content, 'html.parser')
        pages_div = soup.find('div', attrs={'class': 'nums'})
        pages_a = pages_div.find_all('a')[3]
        return int(pages_a.text)

    def __get_pages_urls_list(self):
        pages_urls_list = []
        for page in range(1, self.pages_number + 1):
            pages_urls_list.append(self.games_catalog_url + '?PAGEN_1=%s' % page)
        return pages_urls_list

    def get_games_links_list(self):
        games_links_list = []
        for page_url in self.pages_urls_list:
            request = self.session.get(page_url, headers=self.headers)
            soup = bs(request.content, 'html.parser')
            games_divs = soup.find_all('div', attrs={'class': 'item-title'})
            for game_div in games_divs:
                game_link = self.base_url + game_div.find('a')['href']
                games_links_list.append(game_link)
        return games_links_list


def main():

    session = requests.session()
    games_link_parser = GamesLinksParser(HEADERS, session, BASE_URL, GAMES_CATALOG_URL)
    games_links_list = games_link_parser.get_games_links_list()
    for game_link in games_links_list:
        print(game_link)


main()
