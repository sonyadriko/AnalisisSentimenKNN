# file: app/api/data_training.py
from flask_restx import Namespace, Resource
from flask import jsonify
import pandas as pd

# Membuat Namespace untuk data-training
data_training_ns = Namespace('data-training', description='API untuk mendapatkan data training')

@data_training_ns.route('/')
class DataTrainingResource(Resource):
    def get(self):
        """Endpoint untuk mendapatkan data training"""
        # Memuat data
        TWEET_DATA = pd.read_csv("files/data_tweet.csv", usecols=['rawContent', 'status'])

        data_list = []
        positif_count = 0
        negatif_count = 0

        # Proses setiap baris untuk menentukan label
        for index, row in TWEET_DATA.iterrows():
            entry = {'rawContent': row['rawContent'], 'status': row['status']}
            if row['status'] in [1, 2]:
                entry['status'] = 'Negatif'
                negatif_count += 1
            elif row['status'] in [4, 5]:
                entry['status'] = 'Positif'
                positif_count += 1
            else:
                entry['status'] = 'Unlabel'
            data_list.append(entry)

        # Mengembalikan data dalam format JSON
        response = {
            'data': data_list,
            'positif_count': positif_count,
            'negatif_count': negatif_count
        }

        return jsonify(response)
