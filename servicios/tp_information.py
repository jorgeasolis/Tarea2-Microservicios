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
#           +-----------------------+---------------------------+----------------------------+
#           |  Nombre del elemento  |     Responsabilidad       |         Propiedades        |
#           +-----------------------+---------------------------+----------------------------+
#           |                       |  - Recibir una lista de   | - Utiliza el API de        |
#           |    Procesador de      |    comentarios.           |   analisis de sentimientos |
#           |    Procesador de      |    comentarios.           |   Text-Processing.         |
#           |    sentimientos       |  - Proveer de un JSON     |                            |
#           |                       |    con el analisis de     |                            |
#           |                       |    resultados desde       |                            |
#           |                       |    la API TextProcessing. |                            |
#           +-----------------------+---------------------------+----------------------------+
#
#	Ejemplo de uso: Abrir navegador e ingresar a http://localhost:8084/api/v1/information?t=matrix
#

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
        return res


@app.route("/api/v1/sentimentAnalysis")
def main():
    # creating object of TwitterClient Class
    api = TextProcessingClient()
    # calling function to get tweets
    tweets = request.args.get("tweets")

    tt = tweets.encode().replace('[', '')
    t1 = tt.split(';')
    return json.dumps(api.analisis_sentimientos(t1)), 200


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8082))
    app.debug = True
    app.run(host='0.0.0.0', port=port) 

