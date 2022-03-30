
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

class Crawler():

    def __init__(self, urls=[],start=[],searched_word=""):
        self.visited_urls = []
        self.start_urls = start
        
        self.urls_to_visit = urls

        self.searched_word = searched_word.lower()
        self.data = []
        
    def download_url(self, url):
        return requests.get(url).text

    def get_linked_urls(self, url, html):

        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            # print(path,"path")
            if path and path.startswith('/'):
                path = urljoin(url, path)
                yield path
            # else:
            #     url_split = url.split("/")
            #     url_link = ""
            #     for i in url_split[0:3]:
            #         url_link += i+"/"
            #     if url_link in path:
            #         yield path
                    
            yield path #ใช้เมื่อยังไม่else


    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            if '#' not in url or '?' not in url or 'None' not in url:
                self.urls_to_visit.append(url)

    def crawl(self, url):
        html = self.download_url(url)
        self.search(html,url)
        # print(url,"url")
        # print(self.start_urls,"start")
        if url in self.start_urls:
            for url_href in self.get_linked_urls(url, html):
                self.add_url_to_visit(url_href)


    def run(self,urls,start,word):
        i = 0
        self.visited_urls = []
        self.start_urls = start
        
        self.urls_to_visit = urls

        self.searched_word = word.lower()
        self.data = []
        # print("sss")
        
        while self.urls_to_visit:         
            url = self.urls_to_visit.pop(0)
            try:
                # if i == 1:                  
                #     break
                self.crawl(url)
                # i += 1
                # print(len(self.urls_to_visit),"list url")
            except Exception:
                pass
            finally:
                self.visited_urls.append(url)
        print("finish")

    def search(self,html,url):
        
        soup = BeautifulSoup(html,'html.parser')
        
        
        link = []
        content = []
        count_word = []

        
        # print("1")
        contents_title = soup.body.find_all('h1')
        content_title = [i.get_text().strip() for i in contents_title]
        # content_title.remove("")
        
        
        contents = soup.body.find_all('p')
        content = [i2.get_text().strip() for i2 in contents]
        content.remove("")        
        # print(content)

        
        # print("2")
        same_domain = 0
        url_split = url.split("/")
        url_link = ""
        for i5 in url_split[0:3]:
            url_link += i5+"/"
        link = []
        links = soup.body.find_all('a')
        link = [j.get('href').strip() for j in links]
        for j in link:
            if url_link in j:
                same_domain += 1
            elif j.startswith('/'):
                same_domain += 1
                
        count_link = len(link)
        diff_domain = int(count_link) - int(same_domain)


        # print("dsa1")
        word = ""
        for temp in content:            
            word += temp
        word_lower = word.lower()
        count_word = word_lower.count(self.searched_word)
        # print(count_word)
        # self.linksearch["word(count)"] = self.linksearch["word(count)"].append(count_word)
        # print('Found the word "{0}" {1} times in {2}\n'.format(searched_word, len(results),url))
        # print(words,'s')
        # print("3.1")
        times = []
        datetime = soup.body.find_all('time')
        for x in datetime:
            time = x.find(class_="gs-u-vh")
            times.append(time.get_text(strip=True))
        # print("4")
        

        # dataf.append({"URL": f'"{url}"',"Content(title)": f'"{str(*content)}"',"sentiment": f'"{self.sentiment(TextBlob(self.stem(str(*content).text)))}"',"datetime": f'"{str(*time)}"',"word(search)": f'"{searched_word}"',"word(count)": f'"{count_word}"',"link(count)": f'"{count_link}"'})
        
        self.data.append([url,str(*content_title),word,self.sentiment(TextBlob(self.stem(self.cleanText(word)))),str(times[0]),self.searched_word,count_word,count_link,same_domain,diff_domain])
        # self.data.append([url,str(*content_title),self.sentiment(TextBlob(self.stem(self.cleanText(word)))),str(times[0]),self.searched_word,count_word,count_link,same_domain,diff_domain])

        # print("5")

        
        
        html_text = pd.DataFrame(data=self.data, 
            columns=["URL","Content_title","Contents","sentiment","datetime","word_search","word_count","link_count","link_same_Domain","link_diff_Domain"])

        # html_text = pd.DataFrame(data=self.data, 
        #     columns=["URL","Content_title","sentiment","datetime","word_search","word_count","link_count","link_same_Domain","link_diff_Domain"])
                
        html_text.to_csv(f'{self.searched_word}'+".csv")        
        # print("fin")

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
        
    def THcleanText(self,text):
        url = "https://api.aiforthai.in.th/textcleansing"
        params = {'text':f"{text}"}

        headers = {
            'Apikey': "Oh2wndIoRybtDhRSJVN5u2HugwQSFhkk",
            }
        text = requests.request("GET", url, headers=headers, params=params)


        
        return text.json().get('cleansing_text')

    def THsentiment(self,cleaned_text):
    
        url = "https://api.aiforthai.in.th/ssense"
        
        params = {'text':f"{cleaned_text}"}
        
        headers = {
            'Apikey': "Oh2wndIoRybtDhRSJVN5u2HugwQSFhkk"
            }
        
        cleaned_text = requests.get(url, headers=headers, params=params)
        
        print(cleaned_text.json()['sentiment']['polarity'])
        return cleaned_text.json()['sentiment']['polarity']    

    def start_crawler(self,urls,start,word):
        Crawler(urls=[urls],start=[start],searched_word=word).run(urls,start,word)

# if __name__ == '__main__':
    # Crawler(urls=['https://www.bbc.com/sport/football/60925012'],start=['https://www.bbc.com/sport/football/60925012'],searched_word='Liverpool').run()
    # Crawler(urls=['https://myanimelist.net/anime/genre/48/Work_Life','https://anime-kimuchi.com/','https://anime-fast.online/']).run