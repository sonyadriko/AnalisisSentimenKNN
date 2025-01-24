from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
import pandas as pd
import numpy as np
from app.services.preprocess import preprocess_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity

# Define Namespace
knn_ns = Namespace('knn', description='KNN-based Sentiment Analysis API')

# Define input and output models
knn_request = knn_ns.model('KNNRequest', {
    'text': fields.String(required=True, description='Input text for sentiment analysis'),
    'k': fields.Integer(required=False, default=3, description='Number of neighbors')
})

knn_response = knn_ns.model('KNNResponse', {
    'sentiment': fields.String(description='Predicted sentiment'),
    'preprocess_text': fields.String(description='Preprocessed input text'),
    'results': fields.List(fields.Nested(knn_ns.model('Result', {
        'rank': fields.Integer(description='Rank of similarity'),
        'similarity': fields.Float(description='Cosine similarity value'),
        'text': fields.String(description='Original text')
    })))
})

# Define Resource
@knn_ns.route('/')
class KNNResource(Resource):
    @knn_ns.doc('perform_knn_analysis')
    @knn_ns.expect(knn_request, validate=True)
    @knn_ns.response(200, 'Success', knn_response)
    @knn_ns.response(400, 'Bad Request')
    @knn_ns.response(500, 'Internal Server Error')
    def post(self):
        """Perform sentiment analysis using KNN"""
        try:
            # Load vector data and labels
            df = pd.read_csv("pelabelan.csv")
            original_tweets = pd.read_csv("data_tweet.csv")["rawContent"]

            # Extract features and labels
            X = df.iloc[:, :-2].values
            y = df['label'].values
            label_map = {'positif': 1, 'negatif': 0}
            y = np.array([label_map[label] for label in y])

            # Validate dataset
            if len(np.unique(y)) < 2:
                return {"error": "Dataset must contain both positive and negative labels"}, 400

            # Get input data
            data = request.json
            input_text = data.get('text')
            k = data.get('k', 3)
            if not input_text:
                return {"error": "No input text provided"}, 400
            if not isinstance(k, int) or k <= 0:
                return {"error": "Invalid value for k. It must be a positive integer."}, 400

            # Preprocess input text
            preprocessed_text = preprocess_text(input_text)

            # Preprocess original tweets
            original_tweets_preprocessed = [preprocess_text(tweet) for tweet in original_tweets]

            # TF-IDF vectorization
            vectorizer = TfidfVectorizer(max_features=50, lowercase=False)
            vectorizer.fit(original_tweets_preprocessed)
            input_text_tfidf = vectorizer.transform([preprocessed_text])
            input_text_tfidf_normalized = normalize(input_text_tfidf, norm='l1', axis=1)
            original_tweets_tfidf = vectorizer.transform(original_tweets_preprocessed)

            # Train KNN model
            knn = KNeighborsClassifier(n_neighbors=k)
            knn.fit(X, y)
            prediction = knn.predict(input_text_tfidf_normalized)
            sentiment = 'positif' if prediction[0] == 1 else 'negatif'

            # Cosine similarity
            cosine_similarities = cosine_similarity(input_text_tfidf_normalized, original_tweets_tfidf).flatten()
            top_indices = np.argsort(cosine_similarities)[-k:][::-1]

            # Generate results
            results = []
            for i, idx in enumerate(top_indices):
                results.append({
                    "rank": i + 1,
                    "similarity": float(cosine_similarities[idx]),
                    "text": original_tweets.iloc[idx]
                })

            return {
                "sentiment": sentiment,
                "preprocess_text": preprocessed_text,
                "results": results
            }, 200

        except Exception as e:
            return {"error": str(e)}, 500
