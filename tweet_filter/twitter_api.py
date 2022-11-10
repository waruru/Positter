import os
import tweepy

# API情報を記入
BEARER_TOKEN = os.environ['TWITTER_BEARER_TOKEN']
API_KEY = os.environ['TWITTER_API_KEY']
API_SECRET = os.environ['TWITTER_SECRET_KEY']
ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']


# クライアント関数を作成
def client_info():
    client = tweepy.Client(bearer_token=BEARER_TOKEN,
                           consumer_key=API_KEY,
                           consumer_secret=API_SECRET,
                           access_token=ACCESS_TOKEN,
                           access_token_secret=ACCESS_TOKEN_SECRET,
                           )

    return client


def api():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api


def search_tweets(search, tweet_max):
    search = f'{search} -filter:retweets -filter:replies'
    # 直近のツイート取得
    tweets = api().search_tweets(q=search, tweet_mode='extended', count=tweet_max, lang='ja')

    # 取得したデータ加工
    results = []

    # tweet検索結果取得
    if tweets != None:
        for tweet in tweets:
            obj = {}
            obj["tweet_id"] = tweet.id      # Tweet_ID
            obj["text"] = tweet.full_text  # Tweet Content
            obj['screen_name'] = tweet.user.screen_name
            obj['tweet_url'] = f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
            obj['profile_image_url'] = tweet.user.profile_image_url_https
            if 'media' in tweet.entities:
                obj["media_urls"] = []
                for media in tweet.entities['media']:
                    if 'media_url' in media.keys():
                        obj["media_urls"].append(media.get('media_url'))
            results.append(obj)
    else:
        results.append('')

    # 結果出力
    return results

# 指定した地域のトレンドを取得
def get_trends(woeid):
    return api().get_place_trends(woeid)[0]['trends']


def get_timeline():
    tweets = api().home_timeline(tweet_mode='extended')

    results = []

    # tweet検索結果取得
    if tweets != None:
        for tweet in tweets:
            obj = {}
            obj["tweet_id"] = tweet.id      # Tweet_ID
            obj["text"] = tweet.full_text  # Tweet Content
            obj['tweet_url'] = f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
            obj['profile_image_url'] = tweet.user.profile_image_url_https
            if 'media' in tweet.entities:
                obj["media_urls"] = []
                for media in tweet.entities['media']:
                    if 'media_url' in media.keys():
                        obj["media_urls"].append(media.get('media_url'))
            results.append(obj)
    else:
        results.append('')

    # 結果出力
    return results
