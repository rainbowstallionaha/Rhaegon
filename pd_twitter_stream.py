from TwitterAPI import TwitterAPI
from TwitterAPI import TwitterError
import http.client


metaphorminute = '575930104'
RedditThrones = '872257637429243905'
GameOfThrones = '180463340'
followed = [RedditThrones, GameOfThrones, metaphorminute]
followed_string = ','.join(followed)
general_webhook_url = 'https://discordapp.com/api/webhooks/328682443613667328/WnZOU3vP_MPZsAgKbQQpMOgm2TMsslfWRBry4A8mM0ifQgLaiUK4GpxesHERut7fV5SP'

CONSUMER_KEY = 'OZOEWCYivxIFjg08B2HOARAqb'
CONSUMER_SECRET = '84yJ2SvpZqF9uafgnA9qcJvaknozhCqlmr4oyZDmncd1HeYsUx'
ACCESS_TOKEN_KEY = '879128010087178240-OVpLD124mdaCAkViWzXTcn7pDjHIc71'
ACCESS_TOKEN_SECRET = 'cZxw1cfN4varZWO7rkrmfC0zcLOlNLT8RmSa6qKNQBw21'
api2 = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)


def send(message, webhook_url):
    conn = http.client.HTTPSConnection("ptb.discordapp.com")
    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"content\"\r\n\r\n" + message + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'cache-control': "no-cache",
        'postman-token': ""
    }
    conn.request("POST", webhook_url, payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))


while True:
    try:
        iterator = api2.request('statuses/filter', {'follow': followed_string}).get_iterator()
        for item in iterator:
            if 'text' in item:
                if str(item['user']['id']) in followed:
                    if 'retweet_status' in item:
                        if str(item['retweeted_status']['user']['id'] not in followed):
                            print(item['text'])
                            link = '{}{}{}{}'.format('https://www.twitter.com/', item['user']['screen_name'], '/status/', item['id_str'])
                            print(link)
                            send(link, general_webhook_url)
                    else:
                        print(item['text'])
                        link = '{}{}{}{}'.format('https://www.twitter.com/', item['user']['screen_name'], '/status/', item['id_str'])
                        print(link)
                        send(link, general_webhook_url)
            elif 'disconnect' in item:
                event = item['disconnect']
                if event['code'] in [2, 5, 6, 7]:
                    # something needs to be fixed before re-connecting
                    raise Exception(event['reason'])
                else:
                    # temporary interruption, re-try request
                    break
    except TwitterError.TwitterRequestError as e:
        if e.status_code < 500:
            # something needs to be fixed before re-connecting
            raise
        else:
            # temporary interruption, re-try request
            pass
    except TwitterError.TwitterConnectionError:
        # temporary interruption, re-try request
        pass
