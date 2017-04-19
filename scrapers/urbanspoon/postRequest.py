import urllib2
import urllib
import json
from bs4 import BeautifulSoup
import datetime
import re
import zlib

## Comment Fields
comment = []
rating = []
author = []
commentTitle = []
source = "urbanspoon"
commentID = []
date = []

header = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Content-Length':'58',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': 'PHPSESSID=6663f1bf4c02fcee51337d06c659a5965a67e86e; zl=en; fbtrack=23c5065fe3531defdf8ef5ea5b592bad; fbcity=1; dpr=1; __utmt=1; __utmt_t3=1; __utmt_t7=1; __utmt_t4=1; __jpuri=https%3A//www.zomato.com/ncr/panama-peppers; __utma=141625785.2004000331.1460409387.1460409387.1460409387.1; __utmb=141625785.16.10.1460409387; __utmc=141625785; __utmz=141625785.1460409387.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.2.2004000331.1460409387',
    'dnt': 1,
    # 'Host': 'www.zomato.com',
    # 'Referer': 'https://www.zomato.com/ncr/fork-you-hauz-khas-village-delhi/reviews',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
    # 'X-NewRelic-ID': 'VgcDUF5SGwEDV1RWAgg=',
    'X-Requested-With': 'XMLHttpRequest',
}

## Post request to retreive comments on 
url = "https://www.zomato.com/php/filter_reviews.php"
values = {'res_id': '17041281', 'sort': 'reviews-dd', 'limit': '3'}

data = urllib.urlencode(values)
request = urllib2.Request(url, data, header)
response = urllib2.urlopen(request)
result = response.read()

unzipData = zlib.decompress(result, 16 + zlib.MAX_WBITS)
data = json.loads(unzipData)

html = data['html'].encode('utf-8')

soup = BeautifulSoup(html, "lxml")

date_vals = soup.findAll('time', {'itemprop': 'datePublished'})  # grab value of key = datetime

reviewID_vals = soup.findAll('div', 'res-review-body clearfix')  # grab value of key = data-review-id
review_vals = soup.findAll('div', 'rev-text')
reviewTitle_vals = [None] * len(review_vals)  # No title to review on Zomato
author_vals = soup.findAll('span', 'left mr5')  # use .getText() to get text content of tag

print str(len(review_vals)) + " Reviews"

ignore = ['Rated', 'POSITIVE', 'NEGATIVE']

for i in range(len(review_vals)):
    ## Comment Fields
    review = review_vals[i].getText().strip()

    ## deal with reviews beginning with unwanted content
    startingPhrase = -1
    counter = 0
    for word in ignore:
        if review.startswith(word, 0, len(word)):
            startingPhrase = counter
        counter += 1

    if startingPhrase > -1:
        review = re.sub(ignore[startingPhrase] + '(.+)\n', '', review).strip()
    comment.append(review)
    rating.append(None)
    if len(author_vals):
        author.append(author_vals[i].getText())
    commentTitle.append(None)
    if len(reviewID_vals):
        commentID.append(reviewID_vals[i]['data-review-id'])

    if len(date_vals):
        datetimeStamp = date_vals[i]['datetime'].split(' ')
        dateStamp = datetimeStamp[0].split('-')
        year = int(dateStamp[0])
        month = int(dateStamp[1])
        day = int(dateStamp[2])
        dt = datetime.datetime(year, month, day) - datetime.datetime(1970, 1, 1)
        date.append(dt.total_seconds())

print comment


# html = '''
# <div class="rev-text">
#     <div class="left">
#         <div title="Poor" class="ttupper fs12px left bold zdhl2 tooltip icon-font-level-3" data-iconr="0">
#             Rated
#         </div>

#         &nbsp;&nbsp;

#     </div>

#     First Off: I'm From Marion County, West Virginia. Well, having let you know that in the title and if you know the Fairmont/Marion Country, WV hot dog scene, you know that you should NEVER put ketchup (let alone OFFER it) on a hot dog. And it should be hot dog SAUCE, never CHILI. All that being said, I found the friendly staff, the bun, the grilled hot dog itself, the hand chopped onions and the delicious french fries all very, VERY good. But not good enough to overcome the fact that there was ketchup offered that could be put on a hot dog and the fact that there was chili, ACTUAL FREAKING CHILI on my hot dog. Russell Yann would go in to cardiac arrest at this place! Bottom line: I'd go back for the fries and have the kielbasa instead.

# </div>'''

# soup = BeautifulSoup(html)

# a = soup.findAll('div','rev-text')

# for item in a:
#     print item
#     print item.find(text=True, recursive=False)
