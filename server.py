import os
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np
import nltk
import pymorphy2
import requests
import re
import os
import json
import pickle as pkl


with open("model.pkl", "rb") as fin:
    model = pkl.load(fin)


with open("encoder.pkl", "rb") as fin:
    encoder = pkl.load(fin)


with open("transformer.pkl", "rb") as fin:
    transformer = pkl.load(fin)


with open("inverse_dict.pkl", "rb") as fin:
    reflect_dict = pkl.load(fin)

# загрузка стоп-слов и создание анализатора
russian_stopwords = nltk.corpus.stopwords.words("russian")
morph = pymorphy2.MorphAnalyzer(lang='ru') 


# очистка текста и лемматизация
def clear_and_lemmatize(text: str) -> str:
    txt = re.sub(f"[^А-Яа-я ]", "", text).lower()
    tokens = txt.split()
    return " ".join([morph.parse(el)[0].word for el in tokens if el not in russian_stopwords])


def get_text_for_model(text):
    text = clear_and_lemmatize(text)
    r = transformer.transform([text])
    return r


app = Flask(__name__)
api = Api(app)



class MakePrediction(Resource):
    @staticmethod
    def post():
        posted_data = request.get_json()
        reason = posted_data["reason"]

        reason = get_text_for_model(reason)
        predicted_class = model.predict(reason)
        predicted_class = reflect_dict[tuple(predicted_class[0])]

        return jsonify({
            'prediction': predicted_class
        })
    

api.add_resource(MakePrediction, '/predict')


if __name__ == '__main__':
    app.run(debug=False)