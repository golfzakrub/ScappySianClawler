
from urllib.parse import urljoin
from zipfile import Path
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from textblob import TextBlob
import csv
# import threading
from string import punctuation
from operator import itemgetter
from datetime import date
import os

class Crawler():

    def __init__(self, urls=[],start=[],searched_word=""):
        self.visited_urls = []
        self.start_urls = start
        self.urls_to_visit = urls
        self.searched_word = searched_word.lower()
        
        self.data_bbc = []
        self.data_standard = []
        self.data_skysports = []
        self.data_eurosport = []
        self.data_siamsport = []
        self.data_thairath = []
        self.data_goal = []
        self.data_sportsmole = []
        self.data_birminghammail= []
        self.data_football365 = []
        self.data_talksport = []
        self.data_kapook = []
        self.data_shotongoal = []
        self.data_footballaddrict = []
        self.data_assist = []
        self.data_eftfootball = []
        self.data_footballhits98 = []
        self.data_footballmoment = []
        self.data_mthai = []
        self.data_sportbible = []
        
        self.second_urls = []
        self.tri_urls = []
        self.four_urls = []
        
    def download_url(self, url):
        return requests.get(url).text

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            # print(path,"href") 
            if path == None or path == "#":
                path = 'notfound'
            if path and path.startswith('/'):
                path = urljoin(url, path)   
             
                         
            if '/football/news/' in path and 'www.skysports' in path: #1
                try:
                    int(path[41:45])
                    int(path[47:54])
                    print(path,"path")
                    yield path 
                except ValueError:
                    pass    
                                       
            elif 'sport/football/' in path and "www.bbc." in path: #2 
                try:
                    int(path[-8:])
                    print(path,"pathee")
                
                    yield path 
                except ValueError:
                    pass
                
            elif "/football/" in path and "/story" in path and "www.eurosport" in path: #3
                print(path,"path")
                yield path 
            elif "/football/" in path and "/view" in path and "www.siamsport" in path: #4
                print(path,"path")
                yield path 
            # elif ("/sport/eurofootball/" in path or "/sport/thaifootball/" in path) and "www.thairath" in path: #5 "www.thairath"
            elif  'www.thairath.co.th/sport/eurofootball' in path:
                try:
                    int(path[-7:])
                    print(path,"path")
                    yield path 
                except ValueError:
                    pass
                
            elif "/en/news" in path and "www.goal" in path: #6
                print(path,"path")
                yield path  
                
            elif "www.sportsmole.co.uk/football" in path and "news" in path: #7
                try:
                    int(path[-11:-5])
                    print(path,"path")
                    yield path
                except ValueError:
                    pass
                
            elif  'www.standard.co.uk/sport/football' in path and ".html" in path: #8
                print(path,"path")
                yield path 
                
            elif "/sport/football/football-news/" in path and "www.birminghammail" in path: #9
                try:
                    int(path[-8:])
                    print(path,"path")
                    yield path
                except ValueError:
                    pass
                
              
                
            elif "/news/" in path and "www.football365" in path: #10
                print(path,"path") 
                yield path  
                
            elif "talksport.com/football/" in path and len(path) >37 :#11
                try:
                    int(path[31:38])
                    print(path,"path")
                    yield path 
                except ValueError:
                    pass
                    
            elif "football.kapook.com/news-" in path :#12 ##fix
                print(path,"path") 
                yield path  
                # try:
                #     # int(path[-5:])
                #     print(path,"path")
                #     yield path 
                # except ValueError:
                #     pass
                
            elif "www.shotongoal.com" in path and "/news" in path: #13
                print(path,"path")
                yield path 
                
            elif "www.footballaddrict" in path and "/2022/" in path: #14
                print(path,"path")
                yield path                 
                # try:
                #     int(path[32:36])
                #     int(path[37:39])
                #     int(path[40:42])
                #     print(path,"path")
                #     yield path
                # except ValueError:
                #     pass
                
            elif "www.assist-football.com" in path and ("/2022/" in path or "/2021/" in path or "/2020/" in path ): #15
                
                try:
                    int(path[32:36])
                    int(path[37:39])
                    int(path[40:42]) 
                    print(path,"path")                   
                    yield path  
                except ValueError:
                    pass
                
            elif "eftfootball.com/archives" in path: #16
                try:
                    int(path[-4:])
                    yield path
                    print(path,"path")
                except ValueError:
                    pass
                
            elif "footballhits98" in path and "news-" in path: #17
                print(path,"path")
                yield path
                
            elif "www.footballmoment.com" in path and "20" in path: #18            
                try:
                    int(path[31:35])
                    int(path[36:38])
                    int(path[39:41])
                    print(path,"path")
                    yield path
                except ValueError:
                    pass
                
            elif "sport.mthai.com/football" in path : #19
                
                try:
                    int(path[-11:-5])
                    print(path,"path")
                    yield path
                    
                except ValueError:
                    pass
                
            elif "www.sportbible.com/football/" in path: #20
                
                try:
                    int(path[-8:])
                    print(path,"path")
                    yield path
                except ValueError:
                    pass
            elif "notfound" in path:
                pass


    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)
            self.second_urls.append(url)

    def add_url_to_second_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            if url not in self.urls_to_visit:
                self.urls_to_visit.append(url)
                self.tri_urls.append(url)
                
    def add_url_to_tri_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            if url not in self.urls_to_visit:
                self.urls_to_visit.append(url)   
                self.four_urls.append(url)

    def add_url_to_four_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            if url not in self.urls_to_visit:
                self.urls_to_visit.append(url)   
                            
    def crawl(self, url):
        html = self.download_url(url)    
        if url in self.start_urls:
            for url_href in self.get_linked_urls(url,html):
                self.add_url_to_visit(url_href)
                
        elif url in self.second_urls:
            for url_href in self.get_linked_urls(url,html):
                self.add_url_to_second_visit(url_href)       
                 
        elif url in self.tri_urls:
            for url_href in self.get_linked_urls(url,html):
                self.add_url_to_tri_visit(url_href)      

        elif url in self.four_urls:
            for url_href in self.get_linked_urls(url,html):
                self.add_url_to_four_visit(url_href)               
        
        self.search(html,url)        


    def run(self,urls,start,word):
        i = 0
        self.visited_urls = []
        self.start_urls = start
        self.urls_to_visit = urls
        print(self.urls_to_visit,"urls")
        self.searched_word = word.lower()
        self.second_urls = []
        self.tri_urls = []
        self.four_urls = []
        
        self.data_bbc = []
        self.data_standard = []
        self.data_skysports = []
        self.data_eurosport = []
        self.data_siamsport = []
        self.data_thairath = []
        self.data_goal = []
        self.data_sportsmole = []
        self.data_birminghammail= []
        self.data_football365 = []
        self.data_talksport = []
        self.data_kapook = []
        self.data_shotongoal = []
        self.data_footballaddrict = []
        self.data_assist = []
        self.data_eftfootball = []
        self.data_footballhits98 = []
        self.data_footballmoment = []
        self.data_mthai = []
        self.data_sportbible = []
        # print("sss")
        
        while self.urls_to_visit:         
            url = self.urls_to_visit.pop(0)
            try:
                self.crawl(url)
                print(len(self.urls_to_visit),"list url")
            except Exception:
                pass
            finally:
                self.visited_urls.append(url)
        print("finish")

    def search(self,html,url):
        # today = date.today()
        soup = BeautifulSoup(html,'html.parser')
        
        
        link = []
        content = []
        count_word = []

        print("1")

        if 'www.bbc.' in url: #1
            contents_title = soup.body.find_all('h1')
            if len(contents_title) != 0:
                content_title = [i.get_text().strip() for i in contents_title]
            # content_title.remove("")
            # print(content_title,"header")
            contents = soup.body.find_all('div',{"class":"qa-story-body story-body gel-pica gel-10/12@m gel-7/8@l gs-u-ml0@l"})
            for k in contents:
                content_p = k.find_all("p") 
            if len(contents) != 0:
                content = [i2.get_text().strip() for i2 in content_p]
                if content.count("") >= 1:
                    content.remove("")    
                
        elif 'www.standard.' in url: #2
            contents_title = soup.body.find_all('h1',{'class':'sc-dOaiCS eQGobZ'})
            if len(contents_title) != 0:
                content_title = [i.get_text().strip() for i in contents_title]
            # content_title.remove("")
            # print(content_title,"header")

            contents = soup.body.find_all('div',{"class":"sc-lbOyJj cFwzvG sc-feINqK buRpWf"})
            for k in contents:
                content_p = k.find_all("p")   
            if len(contents) != 0:
                content = [i2.get_text().strip() for i2 in content_p]   
                if content.count("") >= 1:
                    content.remove("")          
            # print(content,"contents") 

            # times = []
            # datetime = soup.body.find_all('div',{"class":"css-ruuwmp e1xtbsxb6"})
            # for x in datetime:
            #     time = x.find("span")
            #     if time is not None:
            #         time_word = time.get_text().replace('\n', '')
            #         if time_word not in times:
            #             times.append(time_word)  
                
        elif 'www.skysports' in url : #3
            contents_title = soup.body.find_all('h1',{'class':'sdc-article-header__title sdc-site-component-header--h1'})
            if len(contents_title) != 0:
                content_title = [i.get_text().strip() for i in contents_title]
            # content_title.remove("")
            # print(content_title,"header")

            contents = soup.body.find_all('div',{"class":"sdc-article-body sdc-article-body--lead"})
            for k in contents:
                content_p = k.find_all("p") 
            if len(contents) != 0:  
                content = [i2.get_text().strip() for i2 in content_p]
                if content.count("") >= 1:
                    content.remove("")          
            # print(content,"contents") 

            # times = []
            # datetime = soup.body.find_all('div',{"class":"css-ruuwmp e1xtbsxb6"})
            # for x in datetime:
            #     time = x.find("span")
            #     if time is not None:
            #         time_word = time.get_text().replace('\n', '')
            #         if time_word not in times:
            #             times.append(time_word)  
        
        elif "www.eurosport" in url :        #4         
            contents_title = soup.body.find_all('h1',{"class":"ArticleHeroBlack__title--light caps-s2-rs mb-3 font-bold text-br-2-90 light:text-br-2-20 sm:mb-5 sm:text-32 sm:leading-38 lg:mb-3 lg:w-3/4 lg:text-48 lg:leading-58"})
            if len(contents_title) != 0:
                content_title = [i.get_text().strip() for i in contents_title]
            # content_title.remove("")
            # print(content_title,"header")

            contents = soup.body.find_all('h2',{"class":"ArticleHeroBlack__teaser--light caption-s5-fx mb-5 text-br-2-90 light:text-br-2-20 sm:mb-8 sm:text-16 sm:leading-19 lg:mb-5 lg:w-3/4 lg:text-18 lg:leading-22"})
            if len(contents) != 0:
                content = [i2.get_text().strip() for i2 in contents]
                if content.count("") >= 1:
                    content.remove("")          
            # print(content,"contents")     
                    
                
        elif "www.siamsport" in url : #5                
            contents_title = soup.body.find_all('h1')
            if len(contents_title) != 0:
                content_title = [i.get_text().strip() for i in contents_title]
            # content_title.remove("")
            # print(content_title,"header")

            contents = soup.body.find_all('main',{"class":"detail_main main-content col-xs-8 pad0"})
            for k in contents:
                content_p = k.find_all("p")   
            if len(contents) != 0:
                content = [i2.get_text().strip() for i2 in content_p]
                if content.count("") >= 1:
                    content.remove("")          
            # print(content,"contents") 

            # times = []
            # datetime = soup.body.find_all('div',{"class":"table-cell"})
            # for x in datetime:
            #     time = x.find("li")
            #     if time is not None:
            #         time_word = time.get_text().replace('\n', '')
            #         if time_word not in times:
            #             times.append(time_word)          

        elif "www.thairath" in url : #6
            contents_title = soup.body.find_all('h1')
            if len(contents_title) != 0:
                content_title = [i.get_text().strip() for i in contents_title]
            # content_title.remove("")
            # print(content_title,"header")

            contents = soup.body.find_all('div',{"class":"css-ze9sgp e1xtbsxb7"})
            for k in contents:
                content_p = k.find_all("p")   
            if len(contents) != 0:    
                content = [i2.get_text().strip() for i2 in content_p]
                if content.count("") >= 1:
                    content.remove("")          
            # print(content,"contents") 

            # times = []
            # datetime = soup.body.find_all('div',{"class":"css-ruuwmp e1xtbsxb6"})
            # for x in datetime:
            #     time = x.find("span")
            #     if time is not None:
            #         time_word = time.get_text().replace('\n', '')
            #         if time_word not in times:
            #             times.append(time_word)  
                         
        elif "www.goal" in url and "news" in url: #7 url
            contents_title = soup.body.find_all("h1")
            if len(contents_title) != 0:
                content_title = [i.get_text().strip() for i in contents_title]
            # content_title.remove("")
            # print(content_title,"header")

            contents = soup.body.find_all('p')
            if len(contents) != 0:  
                content = [i2.get_text().strip() for i2 in contents]
                if content.count("") >= 1:
                    content.remove("")          
            # print(content,"contents") 

            # times = []
            # datetime = soup.body.find_all('div',{"class":"article-content_timeAndComments__tmiH_"})
            # for x in datetime:
            #     time = x.find("time")
            #     if time is not None:
            #         time_word = time.get_text().replace('\n', '')
            #         if time_word not in times:
            #             times.append(time_word)       
            
        elif "www.sportsmole.co.uk" in url and ".html" in url and "news" in url: #8
            contents_title = soup.body.find_all('h1',{'id':"title_text"})
            if len(contents_title) != 0:
                content_title = [i.get_text().strip() for i in contents_title]
            # content_title.remove("")
            # print(content_title,"header")
            
            contents = soup.body.find_all('div',{'id':"article_content"})
            for k in contents:
                content_p = k.find_all("p")   
            if len(contents) != 0:
                content = [i2.get_text().strip() for i2 in content_p]
                if content.count("") >= 1:
                    content.remove("")          
            # print(content,"contents") 
             
            # datetime นับเป็นชม. ยังไม่เอา ใช้today now   
            # times = []
            # datetime = soup.body.find_all('time')
            # for x in datetime:
            #     time = x.find(class_="date-published")
            #     if time is not None:
            #         time_word = time.get_text().replace('\n', '')
            #         if time_word not in times:
            #             times.append(time_word)       
                # times.append(time.get("datetime")) 
                  
        elif "www.birminghammail" in url : #9
            contents_title = soup.body.find_all('h1',{"class":"section-theme-background-indicator publication-font"})
            if len(contents_title) != 0:
                content_title = [i.get_text().strip() for i in contents_title]
            # content_title.remove("")
            # print(content_title,"header")

            contents = soup.body.find_all('div',{'class':"article-body"})
            for k in contents:
                content_p = k.find_all("p")   
            if len(contents) != 0:
                content = [i2.get_text().strip() for i2 in content_p]
                if content.count("") >= 1:
                    content.remove("")          
            # print(content,"contents") 

            ### time ยังหาไม่เจอ 
            # times = []
            # datetime = soup.body.find_all("ul",{"class":"time-info"})
            # for x in datetime:
            #     time = x.find("time",{"class":"date-published"})
            #     if time is not None:
            #         time_word = time.get_text().replace('\n', '')
            #         if time_word not in times:
            #             times.append(time_word)  
                                  

        elif "www.football365" in url : #10
            contents_title = soup.body.find_all('h1')
            if len(contents_title) != 0:
                content_title = [i.get_text().strip() for i in contents_title]
            # content_title.remove("")
            # print(content_title,"header")

            contents = soup.body.find_all('div',{"class":"ciam-article-f365"})
            for k in contents:
                content_p = k.find_all("p")   
            if len(contents) != 0:
                content = [i2.get_text().strip() for i2 in content_p]
                if content.count("") >= 1:
                    content.remove("")          
            # print(content,"contents") 

            # times = []
            # datetime = soup.body.find_all('header',{"class":"article__header"})
            # for x in datetime:
            #     time = x.find("p")
            #     if time is not None:
            #         time_word = time.get_text().replace('\n', '')
            #         if time_word not in times:
            #             times.append(time_word)       
         

        elif "talksport.com" in url and len(url) >37: #12
            contents_title = soup.body.find_all('h1')
            if len(contents_title) != 0:
                content_title = [i.get_text().strip() for i in contents_title]
            # content_title.remove("")
            # print(content_title,"header")

            contents = soup.body.find_all('div',{"class":"article__content"})
            for k in contents:
                content_p = k.find_all("p")   
            if len(contents) != 0:    
                content = [i2.get_text().strip() for i2 in content_p]
                if content.count("") >= 1:
                    content.remove("")         
            # print(content,"contents") 

            # times = []
            # datetime = soup.body.find_all('div')
            # for x in datetime:
            #     time = x.find(class_="article__published")
            #     if time is not None:
            #         time_word = time.get_text().replace('\n', '')
            #         if time_word not in times:
            #             times.append(time_word)    
            
                      
        elif "football.kapook.com" in url and "news" in url: #13
            contents_title = soup.body.find_all('h1')
            if len(contents_title) != 0:
                content_title = [i.get_text().strip() for i in contents_title]
            # content_title.remove("")
            # print(content_title,"header")
            
            contents = soup.body.find_all('div',{"class":"content lead-tracker"})
            for k in contents:
                content_p = k.find_all("p")   
            if len(contents) != 0:
                content = [i2.get_text().strip() for i2 in content_p]
                if content.count("") >= 1:
                    content.remove("")         
            # print(content,"contents") 
                
            # times = []
            # datetime = soup.body.find_all('div',{"class":"bar"})
            # for x in datetime:
            #     time = x.find("em")
            #     if time is not None:
            #         time_word = time.get_text().replace('\n', '')
            #         if time_word not in times:
            #             times.append(time_word) 

        elif "www.shotongoal.com" in url : #14
            contents_title = soup.body.find_all('h1',{"class":"elementor-heading-title elementor-size-default"})
            if len(contents_title) != 0:
                content_title = [i.get_text().strip() for i in contents_title]
            # content_title.remove("")
            # print(content_title,"header")
            
            contents = soup.body.find_all('div',{"class":"elementor-column elementor-col-66 elementor-top-column elementor-element elementor-element-5603a398"})
            for k in contents:
                content_p = k.find_all("p")   
            if len(contents) != 0:
                content = [i2.get_text().strip() for i2 in content_p]
                if content.count("") >= 1:
                    content.remove("")         
            # print(content,"contents") 
                
            # times = []
            # datetime = soup.body.find_all("div")
            # for x in datetime:
            #     time = x.find('span',{"class":"elementor-icon-list-text elementor-post-info__item elementor-post-info__item--type-date"})
            #     if time is not None:
            #         time_word = time.get_text().replace('\n', '')
            #         if time_word not in times:
            #             times.append(time_word)

        elif "www.footballaddrict.com" in url : #15
            contents_title = soup.body.find_all('h1',{"class":"entry-title"})
            if len(contents_title) != 0:
                content_title = [i.get_text().strip() for i in contents_title]
            # content_title.remove("")
            # print(content_title,"header")
            
            contents = soup.body.find_all('div',{"class":"entry-content"})
            for k in contents:
                content_p = k.find_all("p")   
            if len(contents) != 0:
                content = [i2.get_text().strip() for i2 in content_p]
                if content.count("") >= 1:
                    content.remove("")         
            # print(content,"contents") 
                
            # times = []
            # datetime = soup.body.find_all("div")
            # for x in datetime:
            #     time = x.find('time',{"class":"updated"})
            #     if time is not None:
            #         time_word = time.get_text().replace('\n', '')
            #         if time_word not in times:
            #             times.append(time_word)    

        elif "www.assist-football.com" in url : #16
            contents_title = soup.body.find_all('h1',{"class":"entry-title"})
            if len(contents_title) != 0:
                content_title = [i.get_text().strip() for i in contents_title]
            # content_title.remove("")
            # print(content_title,"header")
            
            contents = soup.body.find_all('div',{"class":"entry-content single-page"})
            for k in contents:
                content_p = k.find_all("p")   
            if len(contents) != 0:
                content = [i2.get_text().strip() for i2 in content_p]
                if content.count("") >= 1:
                    content.remove("")         
            # print(content,"contents") 
                
            # times = []
            # datetime = soup.body.find_all("div")
            # for x in datetime:
            #     time = x.find('time',{"class":"updated"})
            #     if time is not None:
            #         time_word = time.get_text().replace('\n', '')
            #         if time_word not in times:
            #             times.append(time_word)       
        
        elif "eftfootball.com" in url : #17
            contents_title = soup.body.find_all('h1',{"class":"entry-title"})
            if len(contents_title) != 0:
                content_title = [i.get_text().strip() for i in contents_title]
            # content_title.remove("")
            # print(content_title,"header")
            
            contents = soup.body.find_all('div',{"class":"td-post-content tagdiv-type"})
            for k in contents:
                content_p = k.find_all("p")   
            if len(contents) != 0:    
                content = [i2.get_text().strip() for i2 in content_p]
                if content.count("") >= 1:
                    content.remove("")         
            # print(content,"contents") 
                
            # times = []
            # datetime = soup.body.find_all("div",{"class":"td-theme-wrap"})
            # for x in datetime:
            #     time = x.find('time',{"class":"entry-date updated td-module-date"})
            #     if time is not None:
            #         time_word = time.get_text().replace('\n', '')
            #         if time_word not in times:
            #             times.append(time_word)    

        elif "footballhits98" in url : #18
            contents_title = soup.body.find_all('h2',{"class":"elementor-text-editor elementor-clearfix"})
            if len(contents_title) != 0:
                content_title = [i.get_text().strip() for i in contents_title]
            # content_title.remove("")
            # print(content_title,"header")
            
            contents = soup.body.find_all('div',{"class":"detail"})
            for k in contents:
                content_p = k.find_all("p")   
            if len(contents) != 0:
                content = [i2.get_text().strip() for i2 in content_p]
                if content.count("") >= 1:
                    content.remove("")         
            # print(content,"contents") 
                
            # times = []
            # datetime = soup.body.find_all("div")
            # for x in datetime:
            #     time = x.find('time')
            #     if time is not None:
            #         time_word = time.get_text().replace('\n', '')
            #         if time_word not in times:
            #             times.append(time_word)        
            # times.append(today.strftime("%d/%m/%Y")) 
            
        elif "footballmoment.com" in url and "20" in url: #19
            contents_title = soup.body.find_all('h1',{"class":"entry-title"})
            if len(contents_title) != 0:
                content_title = [i.get_text().strip() for i in contents_title]
            
            # content_title.remove("")
            # print(content_title,"header")
            
            contents = soup.body.find_all('div',{"class":"entry-content"})
            for k in contents:
                content_p = k.find_all("p")   
            if len(contents) != 0:
                content = [i2.get_text().strip() for i2 in content_p]
                if content.count("") >= 1:
                    content.remove("")        
                     
            # print(content,"contents") 
                
            # times = []
            # datetime = soup.body.find_all("div",{"class":"entry-meta"})
            # for x in datetime:
            #     time = x.find('time',{"class":"entry-date published"})
            #     if time is not None:
            #         time_word = time.get_text().replace('\n', '')
            #         if time_word not in times:
            #             times.append(time_word)      
            
        elif "sport.mthai.com" in url : #20
            contents_title = soup.body.find_all('h1',{"class":"entry-title"})
            if len(contents_title) != 0:
                content_title = [i.get_text().strip() for i in contents_title]
            # content_title.remove("")
            # print(content_title,"header")

            contents = soup.body.find_all('div',{"class":"entry-content-inner medium-10 columns small-12 content-inner-between"})
            for k in contents:
                content_p = k.find_all("p")   
            if len(contents) != 0:
                content = [i2.get_text().strip() for i2 in content_p]
                if content.count("") >= 1:
                    content.remove("")         
            # print(content,"contents") 

            # times = []
            # datetime = soup.body.find_all("main",{"class":"site-main"})
            # for x in datetime:
            #     time = x.find('time',{"class":"entry-date published updated"})
            #     if time is not None:
            #         time_word = time.get_text().replace('\n', '')
            #         if time_word not in times:
            #             times.append(time_word)                              

        elif "www.sportbible.com" in url :
            contents_title = soup.body.find_all('h1',{"class":"css-1h8vhnh"})
            if len(contents_title) != 0:
                content_title = [i.get_text().strip() for i in contents_title]
            # content_title.remove("")
            # print(content_title,"header")

            contents = soup.body.find_all('div',{"class":"css-uyma74"})
            for k in contents:
                content_p = k.find_all("p")   
            if len(contents) != 0:
                content = [i2.get_text().strip() for i2 in content_p]
                if content.count("") >= 1:
                    content.remove("")         
            # print(content,"contents") 

            # times = []
            # datetime = soup.body.find_all("p",{"class":"css-1jq79hh"})
            # for x in datetime:
            #     time = x.find('time')
            #     if time is not None:
            #         time_word = time.get_text().replace('\n', '')
            #         if time_word not in times:
            #             times.append(time_word.replace('Â\xa0',""))
                        
        # print("2")
        same_domain = 0
        url_split = url.split("/")
        url_link = ""
        for i5 in url_split[0:3]:
            url_link += i5+"/"
       
        link = []
        links = soup.body.find_all('a')
        
        if len(links) != 0:
            try:
                link = [j.get('href').strip() for j in links]
            except Exception:
                link = []
        
        for j in link:
            if url_link in j:
                same_domain += 1
            elif j.startswith('/'):
                same_domain += 1
             
        count_link = len(link)
        diff_domain = int(count_link) - int(same_domain)


        print("dsa1")
        word = ""
        for temp in content:            
            word += temp+" "
        if word.count("\n") >= 1:
            word = word.replace("\n"," ")
        if word.count("\xa0") >= 1:
            word = word.replace("\xa0","")
        if word.count(">>>") >= 1:
            word = word.replace(">>>","")
        word_lower = word.lower()
        count_word = word_lower.count(self.searched_word)
        # print(count_word)
        # self.linksearch["word(count)"] = self.linksearch["word(count)"].append(count_word)
        # print('Found the word "{0}" {1} times in {2}\n'.format(searched_word, len(results),url))
        # print(words,'s')
        # print("3.1")  
        
        ### nlp
        # stop_words = set(stopwords.words('english'))
        # word_tokens = word_tokenize(word.lower())        
        # filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
        # # filtered_sentence_word = ""
        # filtered_sentence = []
        # stop_word_more = ["#","@","!","+","=","_","-",".",",","","'s","An","*","(",")","?","``","''","`","'",".","©","the","an","THE","The","i","I","s","a",'','"','"',"<",">",":","[","]", 'about', 'above', 'across', 'after', 'afterwards', 'again',
        # 'against', 'all', 'almost', 'alone', 'along', 'already', 'also',
        # 'although', 'always', 'am', 'among', 'amongst', 'amount', 'an',
        # 'and', 'another', 'any', 'anyhow', 'anyone', 'anything', 'anyway',
        # 'anywhere', 'are', 'around', 'as', 'at', 'back', 'be', 'became',
        # 'because', 'become', 'becomes', 'becoming', 'been', 'before',
        # 'beforehand', 'behind', 'being', 'below', 'beside', 'besides',
        # 'between', 'beyond', 'both', 'bottom', 'but', 'by', 'call', 'can',
        # 'cannot', 'could', 'do', 'done', 'down', 'due', 'during', 'each',
        # 'eight', 'either', 'eleven', 'else', 'elsewhere', 'empty',
        # 'enough', 'even', 'ever', 'every', 'everyone', 'everything',
        # 'everywhere', 'except', 'few', 'fifteen', 'fifty', 'first', 'five',
        # 'for', 'former', 'formerly', 'forty', 'four', 'from', 'front',
        # 'full', 'further', 'get', 'give', 'go', 'had', 'has', 'have', 'he',
        # 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein',
        # 'hereupon', 'hers', 'herself', 'him', 'himself', 'his', 'how',
        # 'however', 'hundred', 'i', 'if', 'in', 'indeed', 'into', 'is',
        # 'it', 'its', 'itself', 'keep', 'last', 'latter', 'latterly',
        # 'least', 'less', 'made', 'many', 'may', 'me', 'meanwhile', 'might',
        # 'mine', 'more', 'moreover', 'most', 'mostly', 'move', 'much',
        # 'must', 'my', 'myself', 'name', 'namely', 'neither', 'never',
        # 'nevertheless', 'next', 'nine', 'no', 'nobody', 'none', 'noone',
        # 'nor', 'not', 'nothing', 'now', 'nowhere', 'of', 'off', 'often',
        # 'on', 'once', 'one', 'only', 'onto', 'or', 'other', 'others',
        # 'otherwise', 'our', 'ours', 'ourselves', 'out', 'over', 'own',
        # 'part', 'per', 'perhaps', 'please', 'put', 'rather', 're', 'same',
        # 'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 'several',
        # 'she', 'should', 'show', 'side', 'since', 'six', 'sixty', 'so',
        # 'some', 'somehow', 'someone', 'something', 'sometime', 'sometimes',
        # 'somewhere', 'still', 'such', 'take', 'ten', 'than', 'that', 'the',
        # 'their', 'them', 'themselves', 'then', 'thence', 'there',
        # 'thereafter', 'thereby', 'therefore', 'therein', 'thereupon',
        # 'these', 'they', 'third', 'this', 'those', 'though', 'three',
        # 'through', 'throughout', 'thru', 'thus', 'to', 'together', 'too',
        # 'top', 'toward', 'towards', 'twelve', 'twenty', 'two', 'under',
        # 'until', 'up', 'upon', 'us', 'very', 'via', 'was', 'we', 'well',
        # 'were', 'what', 'whatever', 'when', 'whence', 'whenever', 'where',
        # 'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon',
        # 'wherever', 'whether', 'which', 'while', 'whither', 'who',
        # 'whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with',
        # 'within', 'without', 'would', 'yet', 'you', 'your', 'yours',
        # 'yourself', 'yourselves']
        
        ### nlp
        # for w in word_tokens:
        #     if w not in stop_words:        
        #         if w not in stop_word_more:      
        #             # filtered_sentence_word += w +" "     
        #             filtered_sentence.append(w)
        # # print(filtered_sentence,"fs")
        ###
        #### top word
        # N = 10
        # words = {}

        # words_gen = (wordg.strip(punctuation).lower() for line in filtered_sentence
        #                                    for wordg in line.split())

        # for wordg in words_gen:
        #     words[wordg] = words.get(wordg, 0) + 1

        # top_words = sorted(words.items(), key=itemgetter(1), reverse=True)[:N]
        ####
        
        # print(top_words,"top")
        # for i, (word, frequency) in enumerate(top_words, start=1):
            
            # print("%s %d %d" % (word, i, frequency))        
        # if top_words[0][0] == "":
        #     top_words[0][0] = '#####'
        

        print("4")
        # print(word)
        # print(str(*content_title),"str")
        checklang = re.compile(r'[a-zA-Z]')
        if word != "":
            if checklang.match(word):
                sentiment = self.sentiment(TextBlob(self.stem(self.cleanText(word))))
            else: 
                try:
                    sentiment = self.THsentiment(TextBlob(self.stem(self.THcleanText(word))))
                except Exception:
                    sentiment = 'neutral'
        
        
        print("S")
        # self.CreateFolder('Data_csv')  
        
        print("5.1")
        if 'www.bbc.' in url:
            print("a")
            if word !="" and str(*content_title) != "":              
                self.data_bbc.append([url,str(*content_title),word,sentiment,self.searched_word,count_word,same_domain,diff_domain])
                html_text1 = pd.DataFrame(data=self.data_bbc, 
                    columns=["URL","Content_title","Contents","sentiment","word_search","word_count","same_domain","diff_domain"])
                
                self.CreateFolder('bbc') 
                open('./bbc'+"/bbc.csv","w")
                html_text1.to_csv('./bbc/bbc'+".csv")
                    
                
                # html_text1.to_csv('bbc'+".csv") 

        elif 'www.standard.' in url:
            print("a")
            if word !="" and str(*content_title) != "":               
                self.data_standard.append([url,str(*content_title),word,sentiment,self.searched_word,count_word,same_domain,diff_domain])
                html_text2 = pd.DataFrame(data=self.data_standard, 
                    columns=["URL","Content_title","Contents","sentiment","word_search","word_count",'same_domain','diff_domain'])

                self.CreateFolder('standard') 
                open(f"./standard/standard.csv","w")
                html_text2.to_csv(f"./standard"+'/standard'+".csv") 
                                        
                # html_text2.to_csv('standard'+".csv")   

        elif 'www.skysports' in url:
            print("a")
            if word !="" and str(*content_title) != "":
                self.data_skysports.append([url,str(*content_title),word,sentiment,self.searched_word,count_word,same_domain,diff_domain])
                html_text3 = pd.DataFrame(data=self.data_skysports, 
                    columns=["URL","Content_title","Contents","sentiment","word_search","word_count","same_domain","diff_domain"])
                
                self.CreateFolder('skysports') 
                open(f"./skysports/skysports.csv","w")
                html_text3.to_csv(f"./skysports"+'/skysports'+".csv")                         
                
                # html_text3.to_csv('skysports'+".csv")   
            
        elif 'www.eurosport' in url:
            print("a")
            if word !="" and str(*content_title) != "":
                self.data_eurosport.append([url,str(*content_title),word,sentiment,self.searched_word,count_word,same_domain,diff_domain])
                html_text4 = pd.DataFrame(data=self.data_eurosport, 
                    columns=["URL","Content_title","Contents","sentiment","word_search","word_count","same_domain","diff_domain"])
                
                self.CreateFolder('eurosport') 
                open(f"./eurosport/eurosport.csv","w")
                html_text4.to_csv(f"./eurosport"+'/eurosport'+".csv")       
                        
                # html_text4.to_csv('eurosport'+".csv")   

        elif 'www.siamsport' in url:
            print("a")
            if word !="" and str(*content_title) != "":
                self.data_siamsport.append([url,str(*content_title),word,sentiment,self.searched_word,count_word,same_domain,diff_domain]) #sen
                html_text5 = pd.DataFrame(data=self.data_siamsport, 
                    columns=["URL","Content_title","Contents","sentiment","word_search","word_count","same_domain","diff_domain"])

                self.CreateFolder('siamsport') 
                open(f"./siamsport/siamsport.csv","w")
                html_text5.to_csv(f"./siamsport"+'/siamsport'+".csv")       
                        
                # html_text5.to_csv('siamsport'+".csv")


        elif 'www.thairath' in url:
            print("a")
            if word !="" :
                if str(*content_title) != "":                
                    self.data_thairath.append([url,str(*content_title),word,sentiment,self.searched_word,count_word,same_domain,diff_domain])
                    html_text6 = pd.DataFrame(data=self.data_thairath, 
                        columns=["URL","Content_title","Contents","sentiment","word_search","word_count","same_domain","diff_domain"])
                else:
                    self.data_thairath.append([url,str(content[0]),word,sentiment,self.searched_word,count_word,same_domain,diff_domain])
                    html_text6 = pd.DataFrame(data=self.data_thairath, 
                        columns=["URL","Content_title","Contents","sentiment","word_search","word_count","same_domain","diff_domain"])                    

                self.CreateFolder('thairath') 
                open(f"./thairath/thairath.csv","w")
                html_text6.to_csv(f"./thairath"+'/thairath'+".csv")       
                                        
                # html_text6.to_csv('thairath'+".csv") 

        elif 'www.goal' in url:
            print("a1")
            if word !="" and str(*content_title) != "":
                print("b")
                self.data_goal.append([url,str(*content_title),word,sentiment,self.searched_word,count_word,same_domain,diff_domain])
                html_text7 = pd.DataFrame(data=self.data_goal, 
                    columns=["URL","Content_title","Contents","sentiment","word_search","word_count","same_domain","diff_domain"])

                self.CreateFolder('goal') 
                open(f"./goal/goal.csv","w")
                html_text7.to_csv(f"./goal"+'/goal'+".csv")       
                                        
                # html_text7.to_csv('goal'+".csv") 
                # print(str(*content_title))  

        elif 'www.sportsmole.co.uk' in url and ".html" in url and "news" in url:
            print("a")
            if word !="" and str(*content_title) != "":
                self.data_sportsmole.append([url,str(*content_title),word,sentiment,self.searched_word,count_word,same_domain,diff_domain])
                html_text8 = pd.DataFrame(data=self.data_sportsmole, 
                    columns=["URL","Content_title","Contents","sentiment","word_search","word_count","same_domain","diff_domain"])

                self.CreateFolder('sportsmole') 
                open(f"./sportsmole/sportsmole.csv","w")
                html_text8.to_csv(f"./sportsmole"+'/sportsmole'+".csv")       
                                        
                # html_text8.to_csv('sportsmole'+".csv")  

            
        elif 'www.birminghammail' in url:
            print("a")
            if word !="" and str(*content_title) != "":
                self.data_birminghammail.append([url,str(*content_title),word,sentiment,self.searched_word,count_word,same_domain,diff_domain])
                html_text9 = pd.DataFrame(data=self.data_birminghammail, 
                    columns=["URL","Content_title","Contents","sentiment","word_search","word_count","same_domain","diff_domain"])

                self.CreateFolder('birminghammail') 
                open(f"./birminghammail/birminghammail.csv","w")
                html_text9.to_csv(f"./birminghammail"+'/birminghammail'+".csv")       
                                        
                # html_text9.to_csv('birminghammail'+".csv")   

        elif 'www.football365' in url:
            print("a")
            if word !="" and str(*content_title) != "":
                self.data_football365.append([url,str(*content_title),word,sentiment,self.searched_word,count_word,same_domain,diff_domain])
                html_text10 = pd.DataFrame(data=self.data_football365, 
                    columns=["URL","Content_title","Contents","sentiment","word_search","word_count","same_domain","diff_domain"])

                self.CreateFolder('football365') 
                open(f"./football365/football365.csv","w")
                html_text10.to_csv(f"./football365"+'/football365'+".csv")       
                                        
                # html_text10.to_csv('football365'+".csv")

        elif 'talksport' in url and len(url) >37:
            print("a")
            if word !="" and str(*content_title) != "":
                self.data_talksport.append([url,str(*content_title),word,sentiment,self.searched_word,count_word,same_domain,diff_domain])
                html_text11 = pd.DataFrame(data=self.data_talksport, 
                    columns=["URL","Content_title","Contents","sentiment","word_search","word_count","same_domain","diff_domain"])
                     
                self.CreateFolder('talksport')    
                open(f"./talksport/talksport.csv","w")
                html_text11.to_csv(f"./talksport"+'/talksport'+".csv")       
                
                # html_text11.to_csv('talksport'+".csv") 
  

        elif 'football.kapook.com' in url and "news" in url:
            print("a4")
            if word !="" and str(*content_title) != "":         
                self.data_kapook.append([url,str(*content_title),word,sentiment,self.searched_word,count_word,same_domain,diff_domain]) #sen
                html_text12 = pd.DataFrame(data=self.data_kapook, 
                    columns=["URL","Content_title","Contents","sentiment","word_search","word_count","same_domain","diff_domain"])

                self.CreateFolder('football-kapook')    
                open(f"./football-kapook/football-kapook.csv","w")
                html_text12.to_csv(f"./football-kapook"+'/football-kapook'+".csv")       
                                        
                # html_text12.to_csv('football-kapook'+".csv")   
                
        elif 'www.shotongoal.com' in url:
            print("a")
            if word !="" and str(*content_title) != "":
                self.data_shotongoal.append([url,str(*content_title),word,sentiment,self.searched_word,count_word,same_domain,diff_domain])
                html_text13 = pd.DataFrame(data=self.data_shotongoal, 
                    columns=["URL","Content_title","Contents","sentiment","word_search","word_count","same_domain","diff_domain"])

                self.CreateFolder('shotongoal')  
                open(f"./shotongoal/shotongoal.csv","w")
                html_text13.to_csv(f"./shotongoal"+'/shotongoal'+".csv")       
                                    
                # html_text13.to_csv('shotongoal'+".csv")   
            
        elif 'www.footballaddrict.com' in url:
            print("a")
            if word !="" and str(*content_title) != "":
                self.data_footballaddrict.append([url,str(*content_title),word,sentiment,self.searched_word,count_word,same_domain,diff_domain])
                html_text14 = pd.DataFrame(data=self.data_footballaddrict, 
                    columns=["URL","Content_title","Contents","sentiment","word_search","word_count","same_domain","diff_domain"])

                self.CreateFolder('footballaddrict') 
                open(f"./footballaddrict/footballaddrict.csv","w")
                html_text14.to_csv(f"./footballaddrict"+'/footballaddrict'+".csv")       
                                        
                # html_text14.to_csv('footballaddrict' +".csv")   

        elif 'www.assist-football.com' in url:
            print("a")
            if word !="" and str(*content_title) != "":
                self.data_assist.append([url,str(*content_title),word,sentiment,self.searched_word,count_word,same_domain,diff_domain])
                html_text15 = pd.DataFrame(data=self.data_assist, 
                    columns=["URL","Content_title","Contents","sentiment","word_search","word_count","same_domain","diff_domain"])

                self.CreateFolder('assist-football') 
                open(f"./assist-football/assist-football.csv","w")
                html_text15.to_csv(f"./assist-football"+'/assist-football'+".csv")       
                                        
                # html_text15.to_csv('assist-football'+".csv")

        elif 'eftfootball.com/archives' in url:
            print("a")
            if word !="" and str(*content_title) != "":
                self.data_eftfootball.append([url,str(*content_title),word,sentiment,self.searched_word,count_word,same_domain,diff_domain]) #sen
                html_text16 = pd.DataFrame(data=self.data_eftfootball, 
                    columns=["URL","Content_title","Contents","sentiment","word_search","word_count",'same_domain','diff_domain'])

                self.CreateFolder('eftfootball') 
                open(f"./eftfootball/eftfootball.csv","w")
                html_text16.to_csv(f"./eftfootball"+'/eftfootball'+".csv")       
                                        
                # html_text16.to_csv('eftfootball'+".csv")    

        elif 'footballhits98' in url:
            if word !="":
                self.data_footballhits98.append([url,str(content[0]),word,sentiment,self.searched_word,count_word,same_domain,diff_domain]) #sen
                html_text17 = pd.DataFrame(data=self.data_footballhits98, 
                    columns=["URL","Content_title","Contents","sentiment","word_search","word_count","same_domain","diff_domain"])                    

                self.CreateFolder('footballhits98') 
                open(f"./footballhits98/footballhits98.csv","w")
                html_text17.to_csv(f"./footballhits98"+'/footballhits98'+".csv")       
                                       
                # html_text17.to_csv('footballhits98'+".csv")   

        elif 'footballmoment.com' in url and "20" in url:
            print("a1")
            if word !="" and str(*content_title) != "":
                print('S')
                sentiment_text = 'neutral'
                self.data_footballmoment.append([url,str(*content_title),word,sentiment_text,self.searched_word,count_word,same_domain,diff_domain])
                html_text18 = pd.DataFrame(data=self.data_footballmoment, 
                    columns=["URL","Content_title","Contents","sentiment","word_search","word_count","same_domain","diff_domain"])

                self.CreateFolder('footballmoment') 
                open(f"./footballmoment/footballmoment.csv","w")
                html_text18.to_csv(f"./footballmoment"+'/footballmoment'+".csv")       
                                        
                # html_text18.to_csv('footballmoment'+".csv")   
            # else:
            #     print("else")
            #     print(str(*content_title)) 
            #     print(content)
            #     print("else p")          
                            
        elif 'sport.mthai.com' in url:
            print("a")
            if word !="" and str(*content_title) != "":
                self.data_mthai.append([url,str(*content_title),word,sentiment,self.searched_word,count_word,same_domain,diff_domain])
                html_text19 = pd.DataFrame(data=self.data_mthai, 
                    columns=["URL","Content_title","Contents","sentiment","word_search","word_count","same_domain","diff_domain"])

                self.CreateFolder('sport-mthai') 
                open(f"./sport-mthai/sport-mthai.csv","w")
                html_text19.to_csv(f"./sport-mthai"+'/sport-mthai'+".csv")       
                                        
                # html_text19.to_csv('sport-mthai'+".csv")   

        elif 'www.sportbible.com' in url:
            print("a")
            if word !="" and str(*content_title) != "":  
                self.data_sportbible.append([url,str(*content_title),word,sentiment,self.searched_word,count_word,same_domain,diff_domain])
                html_text20 = pd.DataFrame(data=self.data_sportbible, 
                    columns=["URL","Content_title","Contents","sentiment","word_search","word_count","same_domain","diff_domain"])

                self.CreateFolder('sportbible') 
                open(f"./sportbible/sportbible.csv","w")
                html_text20.to_csv(f"./sportbible"+'/sportbible'+".csv")       
                                        
                # html_text20.to_csv('sportbible'+".csv")

       
        
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
        
        
        return cleaned_text.json()['sentiment']['polarity']    

    def start_crawler(self,urls,start,word):
        Crawler(urls=[urls],start=[start],searched_word=word).run(urls,start,word)


    def CreateFolder(self,filename):
        
        if not os.path.exists(f"./{filename}"):                    
            os.mkdir(f"./{filename}")  
            print("CreteFolder Successed")
            
# if __name__ == '__main__':
    # Crawler(urls=["https://www.bbc.com/sport/football","https://www.siamsport.co.th/football","https://www.skysports.com/football","https://www.eurosport.com/football/","https://www.siamsport.co.th/football","https://www.thairath.co.th/sport","https://www.goal.com/en","https://www.sportsmole.co.uk/football/","https://www.birminghammail.co.uk/sport/football/football-news/","https://www.football365.com/news","https://talksport.com/football/","https://football.kapook.com/news","https://www.shotongoal.com/news/","https://www.footballaddrict.com/2022/","https://www.assist-football.com","https://eftfootball.com","https://footballhits98.com","https://www.footballmoment.com","https://sport.mthai.com/football","https://www.sportbible.com/football"],start=["https://www.bbc.com/sport/football","https://www.standard.co.uk/sport/football","https://www.skysports.com/football","https://www.eurosport.com/football/","https://www.siamsport.co.th/football","https://www.thairath.co.th/sport","https://www.goal.com/en","https://www.sportsmole.co.uk/football/","https://www.birminghammail.co.uk/sport/football/football-news/","https://www.football365.com/news","https://talksport.com/football/","https://football.kapook.com/news","https://www.shotongoal.com/news/","https://www.footballaddrict.com/2022/","https://www.assist-football.com","https://eftfootball.com","https://footballhits98.com","https://www.footballmoment.com","https://sport.mthai.com/football","https://www.sportbible.com/football"],searched_word='Liverpool').run(["https://www.bbc.com/sport/football","https://www.standard.co.uk/sport/football","https://www.skysports.com/football","https://www.eurosport.com/football/","https://www.siamsport.co.th/football","https://www.thairath.co.th/sport","https://www.goal.com/en","https://www.sportsmole.co.uk/football/","https://www.birminghammail.co.uk/sport/football/football-news/","https://www.football365.com/news","https://talksport.com/football/","https://football.kapook.com/news","https://www.shotongoal.com/news/","https://www.footballaddrict.com/2022/","https://www.assist-football.com","https://eftfootball.com","https://footballhits98.com","https://www.footballmoment.com","https://sport.mthai.com/football","https://www.sportbible.com/football"],["https://www.bbc.com/sport/football","https://www.standard.co.uk/sport/football","https://www.skysports.com/football","https://www.eurosport.com/football/","https://www.siamsport.co.th/football","https://www.thairath.co.th/sport","https://www.goal.com/en","https://www.sportsmole.co.uk/football/","https://www.birminghammail.co.uk/sport/football/football-news/","https://www.football365.com/news","https://talksport.com/football/","https://football.kapook.com/news","https://www.shotongoal.com/news/","https://www.footballaddrict.com/2022/","https://www.assist-football.com","https://eftfootball.com","https://footballhits98.com","https://www.footballmoment.com","https://sport.mthai.com/football","https://www.sportbible.com/football"],'Liverpool')
    # Crawler(urls=["https://www.bbc.com/sport/football","https://www.standard.co.uk/sport/football","https://www.skysports.com/football","https://www.eurosport.com/football/","https://www.siamsport.co.th/football","https://www.thairath.co.th/sport","https://www.goal.com/en","https://www.sportsmole.co.uk/football/","https://www.birminghammail.co.uk/sport/football/football-news/","https://www.football365.com/news","https://talksport.com/football/","https://football.kapook.com/news","https://www.shotongoal.com/news/","https://www.footballaddrict.com/2022/","https://www.assist-football.com","https://eftfootball.com","https://footballhits98.com","https://www.footballmoment.com","https://sport.mthai.com/football","https://www.sportbible.com/football"],start=["https://www.bbc.com/sport/football","https://www.standard.co.uk/sport/football","https://www.skysports.com/football","https://www.eurosport.com/football/","https://www.siamsport.co.th/football","https://www.thairath.co.th/sport","https://www.goal.com/en","https://www.sportsmole.co.uk/football/","https://www.birminghammail.co.uk/sport/football/football-news/","https://www.football365.com/news","https://talksport.com/football/","https://football.kapook.com/news","https://www.shotongoal.com/news/","https://www.footballaddrict.com/2022/","https://www.assist-football.com","https://eftfootball.com","https://footballhits98.com","https://www.footballmoment.com","https://sport.mthai.com/football","https://www.sportbible.com/football"],searched_word='Liverpool').run(["https://www.bbc.com/sport/football","https://www.standard.co.uk/sport/football","https://www.skysports.com/football","https://www.eurosport.com/football/","https://www.siamsport.co.th/football","https://www.thairath.co.th/sport","https://www.goal.com/en","https://www.sportsmole.co.uk/football/","https://www.birminghammail.co.uk/sport/football/football-news/","https://www.football365.com/news","https://talksport.com/football/","https://football.kapook.com/news","https://www.shotongoal.com/news/","https://www.footballaddrict.com/2022/","https://www.assist-football.com","https://eftfootball.com","https://footballhits98.com","https://www.footballmoment.com","https://sport.mthai.com/football","https://www.sportbible.com/football"],["https://www.standard.co.uk/sport/football","https://www.siamsport.co.th/football","https://www.thairath.co.th/sport","https://www.goal.com/en","https://www.sportsmole.co.uk/football/","https://talksport.com/football/","https://football.kapook.com/news","https://www.shotongoal.com/news/","https://eftfootball.com","https://www.footballmoment.com","https://sport.mthai.com/football","https://www.sportbible.com/football"],'Liverpool')
    # Crawler(urls=["https://www.standard.co.uk/sport/football","https://www.siamsport.co.th/football/premierleague",'https://www.thairath.co.th/sport/eurofootball',"https://www.goal.com/en","https://www.sportsmole.co.uk/football/","https://talksport.com/football/","https://football.kapook.com/news","https://eftfootball.com","https://www.footballmoment.com"],start=["https://www.standard.co.uk/sport/football","https://www.siamsport.co.th/football/premierleague",'https://www.thairath.co.th/sport/eurofootball',"https://www.goal.com/en","https://www.sportsmole.co.uk/football/","https://talksport.com/football/","https://football.kapook.com/news","https://eftfootball.com","https://www.footballmoment.com"],searched_word="liverpool").run(["https://www.standard.co.uk/sport/football","https://www.siamsport.co.th/football/premierleague",'https://www.thairath.co.th/sport/eurofootball',"https://www.goal.com/en","https://www.sportsmole.co.uk/football/","https://talksport.com/football/","https://football.kapook.com/news","https://eftfootball.com","https://www.footballmoment.com"],["https://www.standard.co.uk/sport/football","https://www.siamsport.co.th/football/premierleague",'https://www.thairath.co.th/sport/eurofootball',"https://www.goal.com/en","https://www.sportsmole.co.uk/football/","https://talksport.com/football/","https://football.kapook.com/news","https://eftfootball.com","https://www.footballmoment.com"],"liverpool")
    # Crawler(urls=["https://footballhits98.com"],start=["https://footballhits98.com"],searched_word="liverpool").run(["https://footballhits98.com"],["https://footballhits98.com"],"liverpool")
    
    # ["https://www.standard.co.uk/sport/football","https://www.siamsport.co.th/football","https://www.thairath.co.th/sport","https://www.goal.com/en","https://www.sportsmole.co.uk/football/","https://talksport.com/football/","https://football.kapook.com/news","https://www.shotongoal.com/news/","https://eftfootball.com","https://www.footballmoment.com","https://sport.mthai.com/football","https://www.sportbible.com/football"]
# ["https://www.bbc.com/sport/football","https://www.standard.co.uk/sport/football","https://www.skysports.com/football","https://www.eurosport.com/football/","https://www.siamsport.co.th/football","https://www.thairath.co.th/sport","https://www.goal.com/en","https://www.sportsmole.co.uk/football/","https://www.birminghammail.co.uk/sport/football/football-news/","https://www.football365.com/news","https://talksport.com/football/","https://football.kapook.com/news","https://www.shotongoal.com/news/","https://www.footballaddrict.com/2022/","https://www.assist-football.com","https://eftfootball.com","https://footballhits98.com","https://www.footballmoment.com","https://sport.mthai.com/football","https://www.sportbible.com/football"]

#https://www.educn-fi.org/,https://www.prachachat.net/tag/%E0%B8%9F%E0%B8%B8%E0%B8%95%E0%B8%9A%E0%B8%AD%E0%B8%A5

## 3 web แรกไม่เจอ webข่าว sportmole ด้วย moment

    # Crawler(urls=["https://www.standard.co.uk/sport/football"],start=["https://www.standard.co.uk/sport/football"],searched_word="liverpool").run(["https://www.standard.co.uk/sport/football"],["https://www.standard.co.uk/sport/football"],"liverpool")