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
        

    def analizar_tweet(self,texto):
        response = unirest.post("https://japerk-text-processing.p.rapidapi.com/sentiment/",headers={
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

    def analisis_sentimientos(self,tweets):
        pos, neutral, neg = 0, 0, 0
        for tweet in tweets:
            print(tweet)
            result = self.analizar_tweet(tweet)

            '''
            if not result.body:
                return [0,0,0]
            '''

            output = StringIO.StringIO()

            f = open("output","wb")
            pickle.dump(result, f)

            f.close()

            del (f)

            fa=open("output","rb")
            resultado = pickle.load(fa)
            fa.close()
            #print('>>>>>>>>>>>>>>>', resultado.body)
            feeling = resultado.body['label']

            print("feel ",feeling.encode())

            #feeling = json.dumps(result)['label']
            print(feeling.encode())
            if feeling.encode() is 'pos':
               pos+=1
            if feeling.encode() is 'neutral':
               neutral+=1
            if feeling.encode() == 'neg':
               neg+=1

        print("positivo:",pos)
        print("neutral:",neutral)
        print("negativo:",neg)

        res = [pos, neutral, neg]

        return res


@app.route("/api/v1/sentimentAnalysis")
def main(): 
    # creating object of TwitterClient Class 
    api = TextProcessingClient() 
    # calling function to get tweets 
    tweets = [request.args.get("t")]
    return api.analisis_sentimientos(tweets)
    

if __name__ == "__main__":
    port = int(os.environ.get('PORT',8082))

    app.debug = True

    app.run(host='0.0.0.0', port=port) 

