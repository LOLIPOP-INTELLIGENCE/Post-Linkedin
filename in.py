import requests
import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BlockingScheduler


quote_no = 22

links = []
for i in range(1, (146 + 1)):
    print(i)
    url = 'https://www.insightoftheday.com/?page={}'.format(i)
    content = requests.get(url).content
    soup = BeautifulSoup(content,'lxml')

    images = soup.findAll('img')
    print(i)
    links_i = [image.get('src') for image in images if 'cloudfront.net/quote' in image.get('src')]  
    links.extend(links_i)

print('Done')
# print(links)

def create_post():
    global quote_no

    url = 'https://api.linkedin.com/v2/ugcPosts'
    myobj = {
        "author": "urn:li:person:__user_id__",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": "This is part " + str(quote_no + 1) + " of a series of motivational posts.\n\n #motivational #motivation #motivationalquotes #success #inspiration #love #inspirationalquotes #quotes #entrepreneur #life #quoteoftheday #entrepreneurship #business #instagram #lifestyle #india #inspirational #quote #inspire #successquotes #successful #entrepreneurlife #lifequotes #positivevibes #motivationalspeaker #instagood #entrepreneurs #motivationalquote #businessman #hustle"
                },
                "shareMediaCategory": "ARTICLE",
                "media": [
                    {
                        "status": "READY",
                        "originalUrl": links[quote_no]
                    }
                ]
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    access_token = '_insert_your_token_'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'cache-control': 'no-cache',
        'X-Restli-Protocol-Version': '2.0.0'
    }

    quote_no += 1
    post_req = requests.post(url, json = myobj, headers=headers)

    print(post_req.text)

sched = BlockingScheduler()
create_post()
sched.add_job(create_post, 'interval', seconds = 600)

sched.start()
