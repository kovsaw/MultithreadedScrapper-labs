from queue import Queue
import threading
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse

# TODO Make scraper great again!


class MultiThreadedScraper(threading.Thread):
    def __init__(self, queue: Queue):
        threading.Thread.__init__(self)
        self.links = []
        self.queue = queue
        self.counts = None
        self.parser = MyParser()

    def saving_urls(self, urls):
        try:
            for count in urls:
                self.queue.put(count)
                self.links.append(count)
        except BaseException as err:
            print("Fail saving: {}".format(err))

    def scraping(self, link):
        try:
            self.counts = self.parser.pars(normalize(link))
            scraper.saving_urls(self.counts)
        except Exception as err:
            print("Cannot scrape site {}: {}".format(link, err))

    def run(self):
        while len(self.links) < 250:
            url = self.queue.get()
            if url is None:
                break
            self.scraping(url)


class MyParser:
    def pars(self, url):
        try:
            normalize(url)
            print("Parsing url: ", url)
            page = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(page, 'html.parser')
            first_tag = soup.findAll('a')
            perem = [a.get('href') for a in first_tag]
            for i in range(len(perem)):
                perem[i] = make_absolute(perem[i], f_link_)
            return perem
        except BaseException as err:
            print("Fail parsing: {}".format(err))
            return []


def make_absolute(url, origin):
    return urllib.parse.urljoin(origin, url)


def normalize(s):   # Это не костыль:
    return str(s.encode("utf-8")).replace('\\x', '%')[2:-1]


f_link_ = "https://ru.wikipedia.org/wiki"
queue_ = Queue()

scrapers = []
for i in range(4):
    scraper = MultiThreadedScraper(queue_)
    print("Create scraper {}: {}".format(i, scraper))
    scraper.setDaemon(True)
    scraper.start()
    scrapers.append(scraper)

_result = []

print("PUT LINK")
queue_.put(f_link_)
for scraper in scrapers:
    scraper.join()
    _result += scraper.links

_result_file = open("urls.txt", "w")
for i in _result:
    _result_file.write(str(i))
    _result_file.write("\n")
