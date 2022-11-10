from django.shortcuts import render
from .twitter_api import search_tweets, get_trends
from .sentiment_analysis import sentiment_analysis
from .make_graph import make_chart, make_maghist, make_scorehist
from .ng_words import NG_WORDS
from concurrent.futures import ThreadPoolExecutor


# 表示ツイート数
DISPLAY_TWEETS_NUM = 20
# APIでの取得ツイート数
GET_TWEETS_NUM = 100
# フィルター時のスレッド数
THREADS_NUM = 100


def index(request):
    trends = get_trends(23424856)
    context = {
        'trends': trends,
    }
    return render(request, 'index.html', context)


def result(request):
    global scores, magnitudes
    pos_neg = request.GET["pos-neg"]
    if "tf-keyword" in request.GET:
        keyword = request.GET["tf-keyword"]
    else:
        keyword = ""

    results = []
    scores = []
    magnitudes = []

    # while len(results) < DISPLAY_TWEETS_NUM:
    #     search_results = search_tweets(keyword, GET_TWEETS_NUM)
    #     for tweet in search_results:
    #         if pos_neg == "positive" and __has_ng_words(tweet.get('text')):
    #             continue
    #         p_n, score, magnitude = sentiment_analysis(tweet.get('text'))
    #         scores.append(score)
    #         if p_n == pos_neg:
    #             results.append(tweet)
    #             magnitudes.append(magnitude)
    #         if len(results) == DISPLAY_TWEETS_NUM:
    #             break

    # TODO: PosNegフィルターをかけた後に表示件数に満たない場合がある
    search_results = search_tweets(keyword, GET_TWEETS_NUM)
    with ThreadPoolExecutor(THREADS_NUM) as e:
        for tweet in search_results:
            rslt = e.submit(__pos_neg_filter, tweet, pos_neg)
            results.append(rslt)
    results = [rslt.result() for rslt in results]

    results = results[:DISPLAY_TWEETS_NUM] if len(results) > DISPLAY_TWEETS_NUM else results
    magnitudes = magnitudes[:DISPLAY_TWEETS_NUM] if len(magnitudes) > DISPLAY_TWEETS_NUM else magnitudes

    make_chart(scores, pos_neg)
    make_maghist(magnitudes, pos_neg)
    make_scorehist(scores, pos_neg)

    context = {
        'tweets': results,
        'pos_neg': pos_neg,
    }
    return render(request, 'result.html', context)


def __pos_neg_filter(tweet, pos_neg):
    p_n, score, magnitude = sentiment_analysis(tweet.get('text'))
    scores.append(score)
    if pos_neg == "positive" and __has_ng_words(tweet.get('text')):
        return None
    if p_n == pos_neg:
        magnitudes.append(magnitude)
        return tweet

def __has_ng_words(text):
    for ng_word in NG_WORDS:
        if ng_word in text:
            return True
    return False