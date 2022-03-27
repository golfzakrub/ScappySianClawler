
from urllib.parse import urljoin
from bleach import clean
from pyrsistent import v
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from textblob import TextBlob
import csv

class Crawler:

    def __init__(self, urls=[]):
        self.visited_urls = []
        self.urls_to_visit = urls
        # self.linksearch = {
        #     "word(count)":[],
        #     "URL":[],
        #     "Content(title)":[],
        #     "link(count)": [],
        #     "word(search)":[],
        #     "sentiment":[],
        #     "datetime":[]
        # }
        global dataf
        dataf = []
        
    def download_url(self, url):
        return requests.get(url).text

    def get_linked_urls(self, url, html):

        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path

    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            if '#' not in url or '?' not in url or 'None' not in url:
                self.urls_to_visit.append(url)

    def crawl(self, url):
        print("d")
        html = self.download_url(url)
        # self.search_title(html,url)
        self.search(html,url)
        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url)


    def run(self):
        i = 0
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            try:
                if i == 100:                    
                    break
                self.crawl(url)
                i += 1
            except Exception:
                pass
            finally:
                self.visited_urls.append(url)

    def search(self,html,url):
        print("start")
        soup = BeautifulSoup(html,'html.parser')
        
        
        link = []
        content = []
        count_word = []

        
        print("1")
        contents = soup.body.find_all('h1')
        content = [i.get_text().strip() for i in contents]
        print(content)
        # self.linksearch["Content(title)"] = self.linksearch["Content(title)"].append(*content)

        
        print("2")
        links = soup.body.find_all('a')
        link = [j.get('href').strip() for j in links]
        count_link = len(link)
        print(count_link)
        # self.linksearch["link"] = self.linksearch["link"].append(count_link)
        print("2.1")
        # for len_url in range(count_link):
            # Url.append(url)
        # self.linksearch["URL"] = self.linksearch["URL"].append(url)
        
        print("3")
        searched_word = "Eriksen"
        words = soup.body.find_all(string=re.compile('.*{0}.*'.format(searched_word)), recursive=True)
        # words = soup.body.find_all(re.search(f'{searched_word}', html))
        word = [k.get_text().strip() for k in words]
        print(word)
        # print(html)
        # word = str(html).count("Eriksen")
        count_word = len(word)
        print(count_word)
        # self.linksearch["word(count)"] = self.linksearch["word(count)"].append(count_word)
        # print('Found the word "{0}" {1} times in {2}\n'.format(searched_word, len(results),url))
        # print(words,'s')
        print("3.1")
        datetime = soup.body.find_all('time')
        time = [x.get_text().strip() for x in datetime]
        # self.linksearch["datetime"] = self.linksearch["datetime"].append(*time)
        print(time[0])       
        print("4")
        # self.linksearch["word(search)"] = self.linksearch["word(search)"].append(searched_word)
        
        print(url,"url")
        print(str(*content),"str(*content)")
        print(self.sentiment(TextBlob(self.stem(self.cleanText(str(*content))))),"str(sentiment)")
        print(str(time[0]),"str(*time)")
        print(searched_word,"searched_word")
        print(count_word,'count_word')
        print(count_link,"count_link")
        # self.linksearch["sentiment"] = self.linksearch["sentiment"].append(self.sentiment(*content))
        # dataf.append({"URL": f'"{url}"',"Content(title)": f'"{str(*content)}"',"sentiment": f'"{self.sentiment(TextBlob(self.stem(str(*content).text)))}"',"datetime": f'"{str(*time)}"',"word(search)": f'"{searched_word}"',"word(count)": f'"{count_word}"',"link(count)": f'"{count_link}"'})
        dataf.append([url,str(*content),self.sentiment(TextBlob(self.stem(self.cleanText(str(*content))))),str(time[0]),searched_word,count_word,count_link])
        print("5")
        # with open("test8.csv", "w", newline="") as csv_file:
        #     new_val = ["URL","Content(title)","sentiment","datetime","word(search)","word(count)","link(count)"] 
        #     csv_j = csv.DictWriter(csv_file, fieldnames=new_val)
        #     csv_j.writeheader()
        #     csv_j.writerows(data)
        
        
        html_text = pd.DataFrame(data=dataf, 
            columns=["URL","Contenttitle","sentiment","datetime","wordsearch","wordcount","linkcount"])

        
        html_text.to_csv(f'{searched_word}'+".csv")        
        print("fin")

    def cleanText(self,text):
        text =text.lower()
        text =re.sub(r'@[A-Za-z0-9]+','',text) #remove @mentions
        text =re.sub(r'#','',text) #remove the '#' symbol
        text =re.sub(r'RT[\s]+','',text)    #Remove RT
        text =re.sub(r'https?:\/\/\S+','',text) #Remove the hyper link
        text = re.sub(r'[^\w\s]', '', text) #set to chr

        return text
    
    def sentiment(self,cleaned_text):
        # Returns the sentiment based on the polarity of the input TextBlob object
        if cleaned_text.sentiment.polarity > 0:
            return 'positive'
        elif cleaned_text.sentiment.polarity < 0:
            return 'negative'
        else:
            return 'neutral'

    def stem(self,text):
        # This function is used to stem the given sentence
        porter = PorterStemmer()
        token_words = word_tokenize(text)
        stem_sentence = []
        for word in token_words:
            stem_sentence.append(porter.stem(word))
        return " ".join(stem_sentence)        
        


if __name__ == '__main__':
    Crawler(urls=['https://www.bbc.com/sport/football/60889501']).run()
    # Crawler(urls=['https://myanimelist.net/anime/genre/48/Work_Life','https://anime-kimuchi.com/','https://anime-fast.online/']).run
