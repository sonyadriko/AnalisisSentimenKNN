from flask_restx import Namespace, Resource, fields
import pandas as pd
import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import swifter

# Define Namespace
preprocessing_ns = Namespace('preprocessing', description='API untuk preprocessing teks')

# Model output
preprocessing_response = preprocessing_ns.model('PreprocessingResponse', {
    'message': fields.String(description='Status pesan'),
    'file': fields.String(description='Path file hasil preprocessing')
})

@preprocessing_ns.route('/')
class PreprocessingResource(Resource):
    @preprocessing_ns.response(200, 'Success', preprocessing_response)
    @preprocessing_ns.response(500, 'Internal Server Error')
    def get(self):
        """Perform preprocessing on tweet data"""
        try:
            # Load dataset
            tweet_data = pd.read_csv("data_tweet.csv")
            tweet_data = tweet_data[['rawContent']]

            # Case folding
            tweet_data['caseFolding'] = tweet_data['rawContent'].str.lower()

            # Cleaning special characters
            def clean_text(text):
                text = text.replace('\\t', " ").replace('\\n', " ").replace('\\u', " ").replace('\\', "")
                text = text.encode('ascii', 'replace').decode('ascii')
                text = re.sub("([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)", " ", text)
                return text.replace("http://", " ").replace("https://", " ")

            tweet_data['cleaning'] = tweet_data['caseFolding'].apply(clean_text)

            # Remove numbers, punctuation, and extra whitespace
            tweet_data['cleaning'] = tweet_data['cleaning'].apply(lambda x: re.sub(r"\d+", "", x))
            tweet_data['cleaning'] = tweet_data['cleaning'].apply(lambda x: x.translate(str.maketrans("", "", string.punctuation)))
            tweet_data['cleaning'] = tweet_data['cleaning'].apply(lambda x: re.sub(r"\s+", " ", x).strip())

            # Tokenizing
            tweet_data['tokenizing'] = tweet_data['cleaning'].apply(word_tokenize)

            # Stopword removal
            stop_words = set(stopwords.words('indonesian'))
            additional_stopwords = ["yg", "dg", "rt", "dgn", "ny", "d", "klo", "kalo", "amp", "biar", "bikin", "bilang",
                                    "gak", "ga", "krn", "nya", "nih", "sih", "si", "tau", "tdk", "tuh", "utk", "ya",
                                    "jd", "jgn", "sdh", "aja", "n", "t", "nyg", "hehe", "pen", "u", "nan", "loh", "rt",
                                    "&amp", "yah", "huhu", "eh", "uhh", "in"]
            stop_words.update(additional_stopwords)

            tweet_data['stopword'] = tweet_data['tokenizing'].apply(lambda x: [word for word in x if word not in stop_words])

            # Normalization
            normalization_dict = {}
            with open('normalisasi.txt', 'r') as file:
                for line in file:
                    if ':' in line:
                        parts = line.strip().split(': ')
                        if len(parts) == 2:
                            normalization_dict[parts[0]] = parts[1]

            tweet_data['normalized'] = tweet_data['stopword'].apply(lambda x: [normalization_dict.get(word, word) for word in x])

            # Stemming
            factory = StemmerFactory()
            stemmer = factory.create_stemmer()

            def stem_words(words):
                return [stemmer.stem(word) for word in words]

            tweet_data['stemmed'] = tweet_data['normalized'].apply(stem_words)

            # Save processed data
            tweet_data.to_csv("Text_Preprocessing.csv", index=False)

            return {
                "message": "Preprocessing berhasil",
                "file": "Text_Preprocessing.csv"
            }, 200

        except Exception as e:
            return {"message": str(e)}, 500
