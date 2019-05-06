import unirest

import os
from flask import Flask, abort, render_template, request
import urllib, json, StringIO, pickle

app = Flask(__name__)


class TextProcessingClient(object):
    ''' 
    Generic Twitter Class for sentiment analysis. 
    '''

    def __init__(self):
        ''' 
        Class constructor or initialization method. 
        '''
        # keys and tokens from the Twitter Dev Console

    def analizar_tweet(self, texto):
        response = unirest.post("https://japerk-text-processing.p.rapidapi.com/sentiment/", headers={
            "X-RapidAPI-Host": "japerk-text-processing.p.rapidapi.com",
            "X-RapidAPI-Key": "0e652fba64msh27159e87470ff74p17f883jsn28d9111704f1",
            "Content-Type": "application/x-www-form-urlencoded"
        },
                                params={
                                    "text": texto
                                }
                                )
        return response
        # print(response.body)

    def analisis_sentimientos(self, tweets):
        pos, neutral, neg = 0, 0, 0
        for tweet in tweets:
            if len(tweet) > 1:
                print ('tweet ', tweet)
                result = self.analizar_tweet(tweet)

                output = StringIO.StringIO()
                f = open("output", "wb")
                pickle.dump(result, f)
                f.close()
                del (f)
                fa = open("output", "rb")
                resultado = pickle.load(fa)
                fa.close()

                feeling = resultado.body['label']

                # feeling = json.dumps(result)['label']

                print('feel:', feeling.encode())
                if feeling.encode() == 'pos':
                    pos += 1
                if feeling.encode() == 'neutral':
                    neutral += 1
                if feeling.encode() == 'neg':
                    neg += 1

        print("positivo:", pos)
        print("neutral:", neutral)
        print("negativo:", neg)

        res = {'positive': pos, 'neutral': neutral, 'negative': neg, 'total': pos+neg+neutral}
        #res = [pos, neutral, neg, pos + neutral + neg]
        return res


@app.route("/api/v1/sentimentAnalysis")
def main():
    # creating object of TwitterClient Class
    api = TextProcessingClient()
    # calling function to get tweets
    # tweets = []
    tweets = request.args.get("tweets")
    # print ('len ts', len(tweets))
    # print ('tweets ', tweets)
    # print('Hoooooola')

    # tweets = [request.data]

    tt = tweets.encode().replace('[', '')

    t1 = []
    t1 = tt.split(';')
    # print ('len ', len(t1))
    '''
    print ('len ', len(tweets.encode()))
    print ('ttttt   ', type(tweets.encode()))
    print ('ooo   ', tweets.encode())
    '''

    # return api.analisis_sentimientos(tweets)
    return json.dumps(api.analisis_sentimientos(t1)), 200


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8082))
    app.debug = True
    app.run(host='0.0.0.0', port=port) 

