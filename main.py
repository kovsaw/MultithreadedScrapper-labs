from urllib.parse import urljoin
from bs4 import BeautifulSoup
import urllib.request
import pickle
from queue import Queue
from threading import Thread


# TODO Make scraper great again!


class Scrapper:
    def __init__(self):
        self.res_len = 0
        self.parser = MyParser()
        self.new_parser = MyParser()
        self.counts = None
        self.new_counts = None
        self.result_file = open("urls.txt", "w")

    def saving_urls(self, urls):
        for count in urls:
            if count is None:
                pass
            else:
                # print("Number urls: ", len(urls))
                # print(urljoin(f_link, count))
                self.result_file.write(count)
                self.result_file.write("\n")
                # pickle.dump(count, self.result_file)

    def check_thousand_first(self):
        if len(self.counts) >= 1000:
            return True
        else:
            self.res_len = len(self.counts)
            return False

    def check_thousand(self):
        if self.res_len + len(self.new_counts) >= 1000:
            return True
        else:
            self.res_len = self.res_len + len(self.new_counts)
            return False

    def scrapping(self, f_link):
        self.counts = self.parser.pars(normalize(f_link))
        scrap.saving_urls(self.counts)
        print("First urls, next url:")


        for i in self.counts:
            try:
                self.new_counts = self.new_parser.pars(normalize(i))
                print("Next new url")
                scrap.saving_urls(self.new_counts)
                # if scrap.check_thousand():
                #     return print("Number of urls is more than a 1000 at second depth.")
            except AttributeError:
                print("'NoneType' object has no attribute 'encode'")
            except BaseException:
                print("Fail scrapping")

    def get_result(self):
        self.result_file.close()
        file = open("urls.txt", "r")
        result = file.read()
        file.close()
        return result


class MyParser:
    def pars(self, url):
        print(url)
        page = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(page, 'html.parser')
        first_tag = soup.findAll('a')
        return [a.get('href') for a in first_tag]

    # def check_links(self, ):


# Eto ne kostil:
def normalize(s):
    return str(s.encode("utf-8")).replace('\\x', '%')[2:-1]


f_link = "https://ru.wikipedia.org/wiki"
# s_link = "https://wikipedia.org/wiki"

scrap = Scrapper()
scrap.scrapping(f_link)
scrap.get_result()

#parss = MyParser()
#print(parss.pars(normalize(f_link)))
