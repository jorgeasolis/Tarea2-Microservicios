# -*- coding: utf-8 -*-
# !/usr/bin/env python
# ----------------------------------------------------------------------------------------------------------------
# Archivo: sv_information.py
# Tarea: 2 Arquitecturas Micro Servicios.
# Autor(es): Perla Velasco & Yonathan Mtz.
# Version: 1.3 Octubre 2017
# Descripción:
#
#   Este archivo define el rol de un servicio. Su función general es porporcionar en un objeto JSON
#   información detallada acerca de una pelicula o una serie en particular haciendo uso del API proporcionada
#   por IMDb ('https://www.imdb.com/').
#
#
#
#                                        sv_information.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |  - Ofrecer un JSON que  | - Utiliza el API de    |
#           |    Procesador de      |    contenga información |   IMDb.                |
#           |     comentarios       |    detallada de pelí-   | - Devuelve un JSON con |
#           |       de IMDb         |    culas o series en    |   datos de la serie o  |
#           |                       |    particular.          |   pelicula en cuestión.|
#           +-----------------------+-------------------------+------------------------+
#
#	Ejemplo de uso: Abrir navegador e ingresar a http://localhost:8084/api/v1/information?t=matrix
#

import re 
import tweepy 
from tweepy import OAuthHandler

import os
from flask import Flask, abort, render_template, request
import urllib, json

app = Flask(__name__)


@app.route("/api/v1/tweets")
def get_tweets():
    # keys and tokens from the Twitter Dev Console
    consumer_key = 'Y0zvODDHvri9l52c3mQ3RwgZw'
    consumer_secret = 'TFqMqv1oXMFAnJ8mNRxntLktUfOlhNFGhzp1qZuladORJckasP'
    access_token = '2354059560-d45ZqnMCKogB9tcPcIfT2joxaxNg4r660akwRpj'
    access_token_secret = 'Ib6l84atlADRPOBn9iTitxPeF0tejuH1h4KHO9KO41DFo'

    # attempt authentication
    try:
        # create OAuthHandler object
        auth = OAuthHandler(consumer_key, consumer_secret)
        # set access token and secret
        auth.set_access_token(access_token, access_token_secret)
        # create tweepy API object to fetch tweets
        api = tweepy.API(auth)
    except:
        print("Error: Authentication Failed")

    title = request.args.get("t")
    tweets = []
    try:
        # call twitter api to fetch tweets
        fetched_tweets = api.search(q=title, c=100)

        print (type(fetched_tweets))


        # parsing tweets one by one

        for tweet in fetched_tweets:
            # empty dictionary to store required params of a tweet
            parsed_tweet = {}

            # saving text of tweet
            #parsed_tweet['text'] = tweet.text
            parsed_tweet['text'] = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet.text).split())

            # appending parsed tweet to tweets list
            if tweet.retweet_count > 0:
                # if tweet has retweets, ensure that it is appended only once
                if parsed_tweet not in tweets:
                    tweets.append(parsed_tweet)
            else:
                tweets.append(parsed_tweet)

    except tweepy.TweepError as e:
        # print error (if any)
        print("Error : " + str(e))

    print('Hola',json.dumps(tweets))

    return json.dumps(tweets), 200


if __name__ == '__main__':
    # Se define el puerto del sistema operativo que utilizará el servicio
    port = int(os.environ.get('PORT', 8083))
    # Se habilita la opción de 'debug' para visualizar los errores
    app.debug = True
    # Se ejecuta el servicio definiendo el host '0.0.0.0' para que se pueda acceder desde cualquier IP
    app.run(host='0.0.0.0', port=port)