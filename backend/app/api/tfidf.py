from flask_restx import Namespace, Resource, fields
from flask import jsonify
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.preprocessing import normalize

# Define Namespace
tfidf_ns = Namespace('tfidf', description='API untuk perhitungan TF-IDF')

# Model output
tfidf_response = tfidf_ns.model('TFIDFResponse', {
    'status': fields.String(description='Status penghitungan'),
    'file_vector_matrix': fields.String(description='Path file hasil vector matrix'),
    'file_labeled': fields.String(description='Path file hasil pelabelan'),
    'last_row': fields.Raw(description='Data baris terakhir dengan label')
})

@tfidf_ns.route('/')
class TFIDFResource(Resource):
    @tfidf_ns.response(200, 'Success', tfidf_response)
    @tfidf_ns.response(500, 'Internal Server Error')
    def get(self):
        """Hitung TF-IDF dan simpan hasilnya"""
        try:
            # Load preprocessed data
            tweet_data = pd.read_csv("files/Text_Preprocessing.csv", usecols=["stemmed"])
            tweet_data.columns = ["stemmed"]

            # Join token lists into single strings
            tweet_data["tweet_join"] = tweet_data["stemmed"].apply(lambda x: ' '.join(eval(x)))

            # Initialize CountVectorizer
            cvect = CountVectorizer(max_features=50, lowercase=False)
            TF_vector = cvect.fit_transform(tweet_data["tweet_join"])

            # Initialize TfidfTransformer
            tfidf_transformer = TfidfTransformer(smooth_idf=False)
            tfidf_matrix = tfidf_transformer.fit_transform(TF_vector)

            # Normalize TF-IDF matrix
            normalized_tfidf_matrix = normalize(tfidf_matrix, norm='l1', axis=1)

            # Create DataFrame for TF-IDF results
            tfidf_df = pd.DataFrame(normalized_tfidf_matrix.toarray(), columns=cvect.get_feature_names_out())

            # Save TF-IDF matrix to CSV
            tfidf_df.to_csv("files/hasil_vector_matrix.csv", index=False)

            # Add labels to data
            data_tweet = pd.read_csv('files/data_tweet.csv')
            tfidf_df['status'] = data_tweet['status']
            tfidf_df['label'] = data_tweet['status'].apply(lambda x: 'negatif' if x in [1, 2] else 'positif')

            # Save labeled data
            tfidf_df.to_csv("files/pelabelan.csv", index=False)

            # Get the last row of labeled data
            last_row_data = tfidf_df.tail(1).to_dict(orient='records')

            return {
                "status": "TF-IDF berhasil dihitung",
                "file_vector_matrix": "hasil_vector_matrix.csv",
                "file_labeled": "pelabelan.csv",
                "last_row": last_row_data
            }, 200

        except Exception as e:
            return {"status": "Error", "message": str(e)}, 500
