import requests
from bs4 import BeautifulSoup
url = 'http://www.imdb.com/title/tt0944947/episodes'
episodes= []
ratings = []

# Go over seasons 1 to 7
for season in range(1,8):
    r = requests.get(url,params={'season':season})
    soup = BeautifulSoup(r.text,'html.parser')
    listing = soup.find('div',class_="eplist")
    for epnr,div in enumerate(listing.find_all('div',recursive=False)):
        episode = "{}.{}".format(season,epnr +1)
        rating_el = div.find(class_='ipl-rating-star__rating')
    rating = float(rating_el.get_text(strip=True))
    print('Episode:',episode,'--rating:',rating)
    episodes.append(episodes)
    ratings.append(rating)