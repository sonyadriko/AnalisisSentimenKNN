from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

# Define Namespace
metrics_ns = Namespace('metrics', description='API untuk perhitungan metrik model KNN')

# Input model untuk menerima nilai `k`
metrics_input = metrics_ns.model('MetricsInput', {
    'k': fields.Integer(required=True, description='Jumlah tetangga (k) untuk KNN')
})

# Output model untuk hasil metrik
metrics_output = metrics_ns.model('MetricsOutput', {
    'confusion_matrix': fields.List(fields.List(fields.Integer), description='Confusion matrix'),
    'accuracy': fields.Float(description='Akurasi model'),
    'precision': fields.Float(description='Presisi model'),
    'recall': fields.Float(description='Recall model'),
    'f1_score': fields.Float(description='Skor F1 model')
})


@metrics_ns.route('/')
class MetricsResource(Resource):
    @metrics_ns.expect(metrics_input)
    @metrics_ns.response(200, 'Success', metrics_output)
    @metrics_ns.response(400, 'Bad Request')
    @metrics_ns.response(500, 'Internal Server Error')
    def post(self):
        """Hitung metrik untuk model KNN dengan k input dari pengguna"""
        try:
            # Parse input JSON
            data = request.get_json()
            k = data.get('k', 3)

            if k <= 0:
                return {'error': 'Nilai k harus lebih besar dari 0.'}, 400

            # Load data
            df = pd.read_csv("files/pelabelan.csv")
            de = pd.read_csv("files/data_tweet.csv")

            # Extract features and labels
            X = df.iloc[:, :-2].values
            y_true = df['label'].values

            # Convert labels to numerical values
            label_map = {'positif': 1, 'negatif': 0}
            y_true = np.array([label_map[label] for label in y_true])

            if len(np.unique(y_true)) < 2:
                return {'error': 'Dataset harus mengandung label positif dan negatif.'}, 400

            # Train the KNN model
            knn = KNeighborsClassifier(n_neighbors=k)
            knn.fit(X, y_true)

            # Predict on the same data
            y_pred = knn.predict(X)

            # Compute metrics
            cm = confusion_matrix(y_true, y_pred)
            accuracy = accuracy_score(y_true, y_pred)
            precision = precision_score(y_true, y_pred, average='weighted')
            recall = recall_score(y_true, y_pred, average='weighted')
            f1 = f1_score(y_true, y_pred, average='weighted')

            # Return metrics
            return {
                'confusion_matrix': cm.tolist(),
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1
            }, 200

        except Exception as e:
            return {'error': str(e)}, 500
