import os
import requests


def sentiment_analysis(text: str):
    GOOGLE_API = os.environ.get('GOOGLE_API_KEY')
    url = 'https://language.googleapis.com/v1/documents:analyzeSentiment?key=' + GOOGLE_API

    # threshold of magnitude and score
    thr_magnitude, thr_score = 0.0, 0.0

    # Cloud Natural Language API
    header = {'Content-Type': 'application/json'}
    body = {
        "document": {
            "type": "PLAIN_TEXT",
            "language": "JA",
            "content": text
        },
        "encodingType": "UTF8"
    }
    res = requests.post(url, headers=header, json=body).json()

    magnitude = res['documentSentiment']['magnitude']
    score = res['documentSentiment']['score']

    # decision of positive or negative
    if score > thr_score:
        return "positive", score, magnitude  # positive
    else:
        return "negative", score, magnitude  # negative
