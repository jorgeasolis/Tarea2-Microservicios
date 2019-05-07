# -*- coding: utf-8 -*-
# !/usr/bin/env python
# ----------------------------------------------------------------------------------------------------------------
# Archivo: tp_information.py
# Tarea: 2 Arquitecturas Micro Servicios.
# Autor(es): Jorge Alfonso Solís Galván, Raúl Bermúdez Robles,
#            Luis Enrique Ortíz Ramírez & Luis Francisco Alcalá Ramírez.
# Version: 1.0 Mayo 2019
# Descripción:
#
#   Este archivo define el rol de un servicio. Su función general es porporcionar en un objeto JSON
#   información detallada acerca de un analisis de sentimientos en comentarios de usuarios a traves
#   del uso del API proporcionada por text-processing (http://text-processing.com/).
#
#
#
#                                        tp_information.py
#           +-----------------------+---------------------------+----------------------------+
#           |  Nombre del elemento  |     Responsabilidad       |         Propiedades        |
#           +-----------------------+---------------------------+----------------------------+
#           |                       |  - Recibir una lista de   | - Utiliza el API de        |
#           |    Procesador de      |    comentarios.           |   analisis de sentimientos |
#           |    sentimientos       |    comentarios.           |   Text-Processing.         |
#           |    de texto.          |  - Proveer de un JSON     |                            |
#           |                       |    con el analisis de     |                            |
#           |                       |    sentimientos desde     |                            |
#           |                       |    la API TextProcessing. |                            |
#           +-----------------------+---------------------------+----------------------------+
#
#	Ejemplo de uso: Abrir navegador e ingresar a http://localhost:8082/api/v1/sentimentAnalysis?tweets={text:"Bad Serie"}
#

import unirest

import os
from flask import Flask, abort, render_template, request
import urllib, json, StringIO, pickle

app = Flask(__name__)

class TextProcessingClient(object):

    def __init__(self):
        '''
        Constructor de la clase
        '''

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

                if feeling.encode() == 'pos':
                    pos += 1
                if feeling.encode() == 'neutral':
                    neutral += 1
                if feeling.encode() == 'neg':
                    neg += 1

        res = {'positive': pos, 'neutral': neutral, 'negative': neg, 'total': pos+neg+neutral}
        return res

@app.route("/api/v1/sentimentAnalysis")
def main():
    # Creación del objeto TextProccesingClient
    api = TextProcessingClient()
    # Obtención de los argumentos
    tweets = request.args.get("tweets")
    tt = tweets.encode().replace('[', '')
    t1 = tt.split(';')
    return json.dumps(api.analisis_sentimientos(t1)), 200


if __name__ == "__main__":
    # Se define el puerto del sistema operativo que utilizará el servicio
    port = int(os.environ.get('PORT', 8082))
    # Se habilita la opción de 'debug' para visualizar los errores
    app.debug = True
    # Se ejecuta el servicio definiendo el host '0.0.0.0' para que se pueda acceder desde cualquier IP
    app.run(host='0.0.0.0', port=port)
