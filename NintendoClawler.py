import scrapy



class NintendoShopCrawler(scrapy.Spider):
    name = 'nintendo'
    start_urls = ['https://www.switchscores.com/top-rated/all-time']

    def parse(self, response):
        gamelists = response.css('div.row')[2:]
        print(gamelists.extract())
        for games in gamelists:
            name = games.css('a::text').get().replace('\n                            ','')
            if len(name) ==0:
                
                continue
            score = games.css('span.h5.label.label-success.switch-rating-badge::text').get() 
            genre = games.xpath('//span[@class="h5 label label-default"]/text()').get()
            yield {
                'name':name,
                'score': score,
                'genre':genre
                

            }

        next_page = response.css('span.next a::attr("href")').getall()[-1]
        if next_page is not None:
            yield response.follow(next_page, self.parse)