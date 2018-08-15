import urllib.request
import urllib.parse
from bs4 import BeautifulSoup


class MyParser:
    def pars(self, url):
        try:
            normalize(url)
            print(url)
            page = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(page, 'html.parser')
            first_tag = soup.findAll('a')
            return [make_absolute(a.get('href'), url) for a in first_tag]
        except BaseException as err:
            print("Fail scrapping {}".format(err))
            return []


def make_absolute(url, origin):
    if url[0] == '/':
        url = '/' + url
        print("URL: ", url)
        return urllib.parse.urljoin(origin, url)


def normalize(s):   # Это не костыль:
    return str(s.encode("utf-8")).replace('\\x', '%')[2:-1]


f_link_ = "https://ru.wikipedia.org/wiki"
parser = MyParser()
parser.pars(f_link_)
