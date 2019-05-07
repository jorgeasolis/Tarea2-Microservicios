# -*- coding: utf-8 -*-
# !/usr/bin/env python
# ----------------------------------------------------------------------------------------------------------------
# Archivo: tw_information.py
# Tarea: 2 Arquitecturas Micro Servicios.
# Autor(es): Jorge Alfonso Solís Galván, Raúl Bermúdez Robles,
#            Luis Enrique Ortíz Ramírez & Luis Francisco Alcalá Ramírez.
# Version: 1.0 Mayo 2019
# Descripción:
#
#   Este archivo define el rol de un servicio. Su función general es porporcionar en una lista
#   los tweets relacionados a alguna película o serie que se le indique.
#
#
#
#                                        tw_information.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |  - Ofrecer una lista    | - Utiliza el API de    |
#           |    Procesador de      |    que contiene los     |   Twitter.             |
#           |   tweets de Twitter   |    tweets obtenidos     | - Devuelve una lista   |
#           |                       |    de la consulta a la  |   con los tweets rela- |
#           |                       |    API de Twitter.      |   cionados con la      |
#           |                       |                         |   película consultada. |
#           +-----------------------+-------------------------+------------------------+
#
#	Ejemplo de uso: Abrir navegador e ingresar a http://localhost:8083/api/v1/tweets?title=matrix
#

import re 
import tweepy 
from tweepy import OAuthHandler

import os
from flask import Flask, abort, render_template, request
import json

app = Flask(__name__)


@app.route("/api/v1/tweets")
def get_tweets():
    # Llaves para acceder a la API de Twitter
    consumer_key = 'Y0zvODDHvri9l52c3mQ3RwgZw'
    consumer_secret = 'TFqMqv1oXMFAnJ8mNRxntLktUfOlhNFGhzp1qZuladORJckasP'
    access_token = '2354059560-d45ZqnMCKogB9tcPcIfT2joxaxNg4r660akwRpj'
    access_token_secret = 'Ib6l84atlADRPOBn9iTitxPeF0tejuH1h4KHO9KO41DFo'

    # Autentificación
    try:
        # Creación del objeto OAuthHandler
        auth = OAuthHandler(consumer_key, consumer_secret)
        # Asignar el access_token y access_token_secret
        auth.set_access_token(access_token, access_token_secret)
        # Creación de objeto tweepy API
        api = tweepy.API(auth)
    except:
        print("Error: Authentication Failed")

    # Obtención de los argumentos (Título de la película)
    title = request.args.get("title")
    tweets = []

    # Creación de la query para la obtención de los Tweets
    query = {'q': title,
             'result_type': 'recent',
             'count': 100,
             'lang': 'en'
             }

    try:
        # Llamada a la API de Twitter
        fetched_tweets = api.search(**query)

        # Parseo de tweets
        for tweet in fetched_tweets:
            parsed_tweet = {}

            # Almacenando el texto del tweet
            parsed_tweet['text'] = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet.text).split())

            # Agregando los tweets parseados a la lista
            if tweet.retweet_count > 0:
                if parsed_tweet not in tweets:
                    tweets.append(parsed_tweet)
            else:
                tweets.append(parsed_tweet)

    except tweepy.TweepError as e:
        print("Error : " + str(e))

    return json.dumps(tweets), 200


if __name__ == '__main__':
    # Se define el puerto del sistema operativo que utilizará el servicio
    port = int(os.environ.get('PORT', 8083))
    # Se habilita la opción de 'debug' para visualizar los errores
    app.debug = True
    # Se ejecuta el servicio definiendo el host '0.0.0.0' para que se pueda acceder desde cualquier IP
    app.run(host='0.0.0.0', port=port)