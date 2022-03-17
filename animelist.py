import scrapy

class AnimeSpider(scrapy.Spider):
    name = "Anime"
    start_urls = ['https://myanimelist.net/anime/genre/1/Action']
    
    def parse(self,response):
        for anime in response.css('div.js-anime-category-producer'):
            try:
                yield{
                    'name': anime.css('a.link-title::text').get(),
                    'rating': anime.css('span.js-score::text').get(),
                    'link': anime.css('a.link-title').attrib['href'],
                    
                }
            except:
                yield{
                    'name': anime.css().get(),
                    'rating': 'NA',
                    'link': anime.css().attrib['href'],     
                        
                }
        next_page = response.css('a.link').attrib["href"]
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)
                    
