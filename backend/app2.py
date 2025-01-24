from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import pandas as pd
import numpy as np
import string 
import re #regex library

# import word_tokenize & FreqDist from NLTK
from nltk.tokenize import word_tokenize 
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

import ast
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

app = Flask(__name__)
CORS(app)

def preprocess_text(text):
    # Mengubah teks menjadi huruf kecil
    text = text.lower()

    # Menghapus karakter khusus, tautan, dan non-ASCII
    text = re.sub(r"\\t|\\n|\\u|\\", " ", text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r"(@[A-Za-z0-9]+)|(\w+:\/\/\S+)", " ", text)
    text = text.replace("http://", " ").replace("https://", " ")

    # Menghapus angka
    text = re.sub(r"\d+", "", text)
    # print("Menghapus angka berhasil")

  # Mengganti koma dengan spasi
    text = text.replace(",", " ")
    # print("Mengganti koma dgn spasi berhasil")
    
    # Menghapus tanda baca
    # Menghapus tanda baca menggunakan maketrans dan translate
    text = text.translate(str.maketrans("", "", string.punctuation))
    # print("Menghapus tanda baca berhasil")
    

    # Menghapus spasi berlebih
    text = re.sub(r'\s+', ' ', text).strip()

    # Menghapus karakter tunggal
    text = re.sub(r"\b[a-zA-Z]\b", "", text)

    # Tokenisasi
    tokens = word_tokenize(text)

    # Menghapus stopwords
    list_stopwords = set(stopwords.words('indonesian'))
    list_stopwords.update(["yg", "dg", "rt", "dgn", "ny", "d", 'klo', 
                           'kalo', 'amp', 'biar', 'bikin', 'bilang', 
                           'gak', 'ga', 'krn', 'nya', 'nih', 'sih', 
                           'si', 'tau', 'tdk', 'tuh', 'utk', 'ya', 
                           'jd', 'jgn', 'sdh', 'aja', 'n', 't', 
                           'nyg', 'hehe', 'pen', 'u', 'nan', 'loh', 'rt',
                           '&amp', 'yah', 'huhu', 'eh', 'uhh', 'in'])

    tokens = [word for word in tokens if word not in list_stopwords]

    # Stemming
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    stemmed_tokens = [stemmer.stem(word) for word in tokens]

    # Menggabungkan token kembali menjadi string
    return ' '.join(stemmed_tokens)

@app.route('/knn', methods=['POST'])
def KNN():
    try:
        print("=== Mulai Proses KNN ===")

        # Load vector data and labels
        df = pd.read_csv("pelabelan.csv")
        de = pd.read_csv("data_tweet.csv")
        print("Data pelabelan dan data tweet berhasil dimuat.")

        # Cek ukuran DataFrame
        if df.shape[0] <= 1:
            print("Error: DataFrame tidak memiliki cukup data.")
            return jsonify({'error': 'DataFrame does not have enough rows for slicing.'}), 400

        # Extract features and labels
        X = df.iloc[:, :-2].values  # Features (excluding 'status' and 'label' columns)
        y = df['label'].values  # Labels
        print(f"Shape X: {X.shape}, Shape y: {y.shape}")

        # Convert labels to numerical values if necessary
        label_map = {'positif': 1, 'negatif': 0}
        y = np.array([label_map[label] for label in y])
        print(f"Label mapping berhasil: {np.unique(y)}")

        if len(np.unique(y)) < 2:
            print("Error: Dataset harus mengandung label positif dan negatif.")
            return jsonify({'error': 'The dataset must contain both positive and negative labels.'}), 400

        # Get input text and k from the POST request
        input_text = request.json.get('text')
        k = request.json.get('k', 3)  # Default k = 3 if not provided
        print(f"Teks input: {input_text}, K: {k}")
        if k is None:  # Tetapkan default jika 'k' tidak diberikan
            k = 3
            print(f"Tidak ada nilai k diberikan, menggunakan default: {k}")
        else:
            print(f"Nilai k diterima dari klien: {k}")
        k = int(k)  # Pastikan k di-cast menjadi integer

        if not input_text:
            print("Error: Tidak ada teks yang dimasukkan.")
            return jsonify({'error': 'No input text provided'}), 400
        if not isinstance(k, int) or k <= 0:
            print("Error: Nilai k tidak valid.")
            return jsonify({'error': 'Invalid value for k. It must be a positive integer.'}), 400

        # Preprocess the input text
        preprocessed_text = preprocess_text(input_text)
        print(f"Teks setelah preprocessing: {preprocessed_text}")

        # Load original tweets for TF-IDF fitting
        original_tweets = pd.read_csv("data_tweet.csv")["rawContent"]
        original_tweets_preprocessed = [preprocess_text(tweet) for tweet in original_tweets]
        print("Original tweets berhasil diproses.")

        # Fit TF-IDF vectorizer
        vectorizer = TfidfVectorizer(max_features=50, lowercase=False)
        vectorizer.fit(original_tweets_preprocessed)
        print("TF-IDF vectorizer berhasil di-fit.")

        # Transform original tweets and input text
        original_tweets_tfidf = vectorizer.transform(original_tweets_preprocessed)
        input_text_tfidf = vectorizer.transform([preprocessed_text])
        print("TF-IDF transform berhasil dilakukan.")

        # Normalize the input vector
        input_text_tfidf_normalized = normalize(input_text_tfidf, norm='l1', axis=1)

        # Train the KNN model
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X, y)
        print("Model KNN berhasil di-train.")

        # Predict the sentiment of the input text
        prediction = knn.predict(input_text_tfidf_normalized)
        sentiment = 'positif' if prediction[0] == 1 else 'negatif'
        print(f"Hasil prediksi sentimen: {sentiment}")

        # Calculate cosine similarity
        cosine_similarities = cosine_similarity(input_text_tfidf_normalized, original_tweets_tfidf).flatten()
        print("Cosine similarity berhasil dihitung.")

        # Get top 3 similar texts
        top_indices = np.argsort(cosine_similarities)[-k:][::-1]
        print(f"Top indices: {top_indices}")

        top_sentiments = df['label'].iloc[top_indices]
        sentiment_counts = np.bincount([label_map[sentiment] for sentiment in top_sentiments])
        predicted_sentiment = 'positif' if sentiment_counts[1] > sentiment_counts[0] else 'negatif'
        print(f"Hasil sentimen mayoritas: {predicted_sentiment}")

        results = []
        for i, idx in enumerate(top_indices):
            rank = i + 1
            similarity = cosine_similarities[idx]
            tweet_text = original_tweets[idx]
            result = {
                "rank": rank,
                "similarity": float(similarity),
                "text": tweet_text
            }
            results.append(result)
            print(f"Rank {rank}: {result}")

        # Return the result
        print("=== Proses KNN Selesai ===")
        return jsonify({
            'sentiment': predicted_sentiment,
            'preprocess_text': preprocessed_text,
            'results': results
        })
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/metrics', methods=['POST'])
def metrics():
    try:
        # Load data
        df = pd.read_csv("pelabelan.csv")
        de = pd.read_csv("data_tweet.csv")

        # Extract features and labels
        X = df.iloc[:, :-2].values
        y_true = df['label'].values

        # Convert labels to numerical values
        label_map = {'positif': 1, 'negatif': 0}
        y_true = np.array([label_map[label] for label in y_true])

        if len(np.unique(y_true)) < 2:
            return jsonify({'error': 'The dataset must contain both positive and negative labels.'}), 400

        # Train the KNN model
        k = 3
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
        return jsonify({
            'confusion_matrix': cm.tolist(),
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# mencari persentase untuk hasil negatif dan positif
@app.route('/get-persentase-sentimen', methods=['GET'])
def getPersentaseSentimen():
    # Membaca file Excel
    df = pd.read_csv('pelabelan.csv')

    # Ambil kolom "sentimen"
    sentimen = df['sentimen']

    # Hitung jumlah prediksi positif dan negatif
    positive_count = sentimen[sentimen == 'positif'].count()
    negative_count = sentimen[sentimen == 'negatif'].count()

    # Hitung persentase perbandingan antara prediksi positif dan negatif
    total_count = len(sentimen)
    positive_percentage = (positive_count / total_count) * 100
    negative_percentage = (negative_count / total_count) * 100

    # Tampilkan hasil persentase perbandingan

    return jsonify({"Persentase_positif": positive_percentage, "Persentase_negatif": negative_percentage})

# API data training
@app.route('/data-training')
def dataTraining():
    TWEET_DATA = pd.read_csv("data_tweet.csv", usecols=['rawContent', 'status'])
    
    data_list = []
    positif_count = 0
    negatif_count = 0

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

    response = {
        'data': data_list,
        'positif_count': positif_count,
        'negatif_count': negatif_count
    }
    
    return jsonify(response)

# API data testing
@app.route('/data-testing')
def dataTesting():
    TWEET_DATA = pd.read_csv("data_tweet.csv", usecols=['rawContent', 'status'])
    filtered_data1 = TWEET_DATA.reset_index()
    filtered_data1['status'] = filtered_data1['status'].replace(0.0, 0).astype(int)
    sorted_data1 = pd.concat([
        filtered_data1[filtered_data1['status'] == 0].sort_values(by='status', ascending=False),
        filtered_data1[filtered_data1['status'] != 0]
    ])
    data1 = sorted_data1.to_dict(orient='records')

    PELABELAN_DATA = pd.read_csv("pelabelan.csv", usecols=['sentimen', 'status','aktual'])
    filtered_data2 = PELABELAN_DATA.reset_index()
    filtered_data2['status'] = filtered_data2['status'].replace(0.0, 0).astype(int)
    sorted_data2 = pd.concat([
        filtered_data2[filtered_data2['status'] == 0].sort_values(by='status', ascending=False),
        filtered_data2[filtered_data2['status'] != 0]
    ])
    data2 = sorted_data2.to_dict(orient='records')

    return jsonify({"data_tweet": data1, "data_pelabelan": data2})

@app.route('/preprocessing')
def preprocessing():
    
    TWEET_DATA = pd.read_csv("data_tweet.csv")
    
    TWEET_DATA = TWEET_DATA.drop(columns=[col for col in TWEET_DATA.columns if col != 'rawContent'])
    
    # mengubah text menjadi lowercase
    TWEET_DATA['caseFolding'] = TWEET_DATA['rawContent'].str.lower()

    # ------ Tokenizing ---------

    def remove_tweet_special(text):
        # remove tab, new line, ans back slice
        text = text.replace('\\t'," ").replace('\\n'," ").replace('\\u'," ").replace('\\',"")
        # remove non ASCII (emoticon, chinese word, .etc)
        text = text.encode('ascii', 'replace').decode('ascii')
        # remove mention, link, hashtag
        text = ' '.join(re.sub("([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)"," ", text).split())
        # remove incomplete URL
        return text.replace("http://", " ").replace("https://", " ")

    TWEET_DATA['cleaning'] = TWEET_DATA['caseFolding'].apply(remove_tweet_special)

    #remove number
    def remove_number(text):
        return  re.sub(r"\d+", "", text)

    TWEET_DATA['cleaning'] = TWEET_DATA['cleaning'].apply(remove_number)

    #remove punctuation
    def remove_punctuation(text):
        return text.translate(str.maketrans("","",string.punctuation))

    TWEET_DATA['cleaning'] = TWEET_DATA['cleaning'].apply(remove_punctuation)

    #remove whitespace leading & trailing
    def remove_whitespace_LT(text):
        return text.strip()

    TWEET_DATA['cleaning'] = TWEET_DATA['cleaning'].apply(remove_whitespace_LT)

    #remove multiple whitespace into single whitespace
    def remove_whitespace_multiple(text):
        return re.sub('\s+',' ',text)

    TWEET_DATA['cleaning'] = TWEET_DATA['cleaning'].apply(remove_whitespace_multiple)

    # remove single char
    def remove_singl_char(text):
        return re.sub(r"\b[a-zA-Z]\b", "", text)

    TWEET_DATA['cleaning'] = TWEET_DATA['cleaning'].apply(remove_singl_char)

    # NLTK word rokenize 
    def word_tokenize_wrapper(text):
        return word_tokenize(text)

    TWEET_DATA['tokenizing'] = TWEET_DATA['cleaning'].apply(word_tokenize_wrapper)
    
    # NLTK calc frequency distribution
    def freqDist_wrapper(text):
        return FreqDist(text)

    TWEET_DATA['tweet_tokens_fdist'] = TWEET_DATA['tokenizing'].apply(freqDist_wrapper)
    TWEET_DATA['tweet_tokens_fdist'].head().apply(lambda x : x.most_common())
    

    # ----------------------- get stopword from NLTK stopword -------------------------------
    # get stopword indonesia
    list_stopwords = stopwords.words('indonesian')


    # ---------------------------- manualy add stopword  ------------------------------------
    # append additional stopword
    list_stopwords.extend(["yg", "dg", "rt", "dgn", "ny", "d", 'klo', 
                           'kalo', 'amp', 'biar', 'bikin', 'bilang', 
                           'gak', 'ga', 'krn', 'nya', 'nih', 'sih', 
                           'si', 'tau', 'tdk', 'tuh', 'utk', 'ya', 
                           'jd', 'jgn', 'sdh', 'aja', 'n', 't', 
                           'nyg', 'hehe', 'pen', 'u', 'nan', 'loh', 'rt',
                           '&amp', 'yah', 'huhu', 'eh', 'uhh', 'in'])

    # ----------------------- add stopword from txt file ------------------------------------
    # read txt stopword using pandas
    txt_stopword = pd.read_csv("stopwords.txt", names= ["stopwords"], header = None)

    # convert stopword string to list & append additional stopword
    list_stopwords.extend(txt_stopword["stopwords"][0].split(' '))

    # ---------------------------------------------------------------------------------------

    # convert list to dictionary
    list_stopwords = set(list_stopwords)


    #remove stopword pada list token
    def stopwords_removal(words):
        return [word for word in words if word not in list_stopwords]

    TWEET_DATA['stopword'] = TWEET_DATA['tokenizing'].apply(stopwords_removal) 
    
    # import Sastrawi package
    from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
    import swifter

    # Normalization
    normalization_dict = {}
    with open('normalisasi.txt', 'r') as file:
        for line in file:
            if ':' in line:
                parts = line.strip().replace('"', '').split(': ')
                if len(parts) == 2:
                    slang, normal = parts
                    normalization_dict[slang.strip()] = normal.strip()

    def normalize_text(text):
        return [normalization_dict.get(word, word) for word in text]

    TWEET_DATA['tweet_tokens_normalized'] = TWEET_DATA['stopword'].apply(normalize_text)
    

    # create stemmer
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    # stemmed
    def stemmed_wrapper(term):
        return stemmer.stem(term)

    term_dict = {}
    for document in TWEET_DATA['tweet_tokens_normalized']:
        for term in document:
            if term not in term_dict:
                term_dict[term] = ' '

    print(len(term_dict))
    print("------------------------")

    for term in term_dict:
        term_dict[term] = stemmed_wrapper(term)
        print(term,":" ,term_dict[term])

    print(term_dict)
    print("------------------------")


    # apply stemmed term to dataframe
    def get_stemmed_term(document):
        return [term_dict[term] for term in document]

    TWEET_DATA['tweet_tokens_stemmed'] = TWEET_DATA['tweet_tokens_normalized'].swifter.apply(get_stemmed_term)
    
    TWEET_DATA.index = TWEET_DATA.index + 1
    TWEET_DATA.to_csv("Text_Preprocessing.csv")
    
    return "preprocessing berhasil"

@app.route('/tf-idf')
def tfidf():
    # Load data
    TWEET_DATA = pd.read_csv("Text_Preprocessing.csv", usecols=["tweet_tokens_stemmed"])
    TWEET_DATA.columns = ["tweet_tokens_stemmed"]

    # Join token lists into single strings
    TWEET_DATA["tweet_join"] = TWEET_DATA["tweet_tokens_stemmed"].apply(lambda x: ' '.join(eval(x)))

    # Initialize CountVectorizer and fit-transform to get term frequencies
    cvect = CountVectorizer(max_features=50, lowercase=False)
    TF_vector = cvect.fit_transform(TWEET_DATA["tweet_join"])

    # Initialize TfidfTransformer and fit-transform to get TF-IDF values
    tfidf_transformer = TfidfTransformer(smooth_idf=False)
    tfidf_matrix = tfidf_transformer.fit_transform(TF_vector)

    # Normalize TF-IDF matrix
    normalized_tfidf_matrix = normalize(tfidf_matrix, norm='l1', axis=1)

    # Create DataFrame to store TF-IDF results
    tfidf_df = pd.DataFrame(normalized_tfidf_matrix.toarray(), columns=cvect.get_feature_names_out())

    # Save TF-IDF matrix to CSV
    tfidf_df.to_csv("hasil_vector_matrix.csv", index=False)
    
    data_tweet = pd.read_csv('data_tweet.csv')
    tfidf_df['status'] = data_tweet['status']
    tfidf_df['label'] = data_tweet['status'].apply(lambda x: 'negatif' if x in [1, 2] else 'positif')

    # Simpan hasil pelabelan ke dalam file
    tfidf_df.to_csv("pelabelan.csv", index=False)
    # logging.debug("Saved pelabelan.csv")\
    
    last_row_data = tfidf_df.tail(1).to_dict(orient='records')
    return jsonify(last_row_data)
    

    return "TF-IDF berhasil dihitung dan hasil disimpan sebagai hasil_vector_matrix.csv"
    
@app.route('/sentimen-pelabelan')
def pelabelan():
    # Baca file CSV
    data = pd.read_csv('hasil_vector_matrix.csv')
    data1 = pd.read_csv('data_tweet.csv')

    # Mengambil indeks baris dengan status = 0
    index_zero_status = data1.loc[data1['status'] == 0].index.tolist()
    # print("Index with status 0:", index_zero_status)

    # Menentukan kolom fitur (TF-IDF values) dan label asli (sentimen)
    X = data.iloc[:, :-1].values  # Semua kolom kecuali kolom terakhir sebagai fitur
    y = data1['kelas'].values  # Kolom 'sentimen' sebagai label

    # Konversi label ke integer
    sentiment_map = {'positif': 1, 'negatif': 0}
    y = np.array([sentiment_map[s] for s in y], dtype=np.int64)
    # print("Converted y:", y[:10])  # Menampilkan beberapa label pertama untuk debugging

    # Konversi tipe data ke float
    X = X.astype(np.float64)

    # Menghitung cosine similarity
    similarities = cosine_similarity(X, X)

    # Tentukan jumlah tetangga terdekat (k)
    k = 3

    # Prediksi sentimen menggunakan KNN
    predictions = []
    for i in range(len(X)):
        nearest_indices = np.argsort(similarities[i])[-k-1:-1][::-1]
        nearest_labels = y[nearest_indices]
        prediction = np.argmax(np.bincount(nearest_labels))
        predictions.append(prediction)

    # print("Predictions:", predictions[:10])  # Menampilkan beberapa prediksi pertama untuk debugging

    # Menambahkan kolom "sentimen" dan "aktual" ke dalam DataFrame
    data['status'] = data1['status']
    data['aktual'] = data1['kelas']
    predicted_sentiments = ['positif' if p == 1 else 'negatif' for p in predictions]
    data['sentimen'] = predicted_sentiments
    data.loc[data.index.isin(index_zero_status), 'aktual'] = '-'

    # Simpan hasil pelabelan ke dalam file tanpa index
    data.to_csv("pelabelan.csv", index=False)

    # Mengambil baris terakhir untuk dikembalikan sebagai JSON
    last_row = data.tail(1)
    data = last_row.to_dict(orient='records')
    
    return jsonify(data)

    
#similarity
@app.route('/similarity', methods=['GET'])
def similarity():
    # Membaca data vektor dan sentimen dari file CSV
    df_vectors = pd.read_csv("pelabelan.csv", header=None, skiprows=1)
    vectors = df_vectors.iloc[:, 1:-3].values
    sentiments = df_vectors.iloc[:, -1].values

    # Membaca data tweet dari file CSV
    df_tweet = pd.read_csv("data_tweet.csv", encoding='latin1')

    # Mengambil data input yang akan dibandingkan dengan semua data
    input_vector_sentiments = vectors[-1]

    # Menghitung cosine similarity
    similarities_sentiments = cosine_similarity([input_vector_sentiments], vectors[:-1])[0]

    # Mengambil 3 data dengan nilai cosine similarity tertinggi
    top_indices_sentiments = np.argsort(similarities_sentiments)[-3:][::-1]

    # Menyimpan hasil ranking data tertinggi dan teks tweet
    results = []
    for i, idx in enumerate(top_indices_sentiments):
        rank = i + 1
        similarity = similarities_sentiments[idx]
        data_number = int(idx + 1)
        tweet_text = df_tweet.iloc[idx]['rawContent']
        result = {
            "rank": rank,
            "data_number": data_number,
            "cosine_similarity": float(similarity),
            "tweet": tweet_text
        }
        results.append(result)

    # Menghitung jumlah sentimen negatif dan positif dari 3 data ranking teratas
    top_sentiments = sentiments[top_indices_sentiments]
    num_negative_sentiments = np.sum(top_sentiments == 'negatif')
    num_positive_sentiments = np.sum(top_sentiments == 'positif')

    # Menentukan sentimen berdasarkan perbandingan jumlah sentimen positif dan negatif
    if num_positive_sentiments > num_negative_sentiments:
        sentiment_label = "positif"
    else:
        sentiment_label = "negatif"

    # Menghitung accuracy positif dan accuracy negatif
    accuracy_positif = 0
    accuracy_negatif = 0

    if num_positive_sentiments > 0:
        max_positive_similarity = np.max(similarities_sentiments[top_indices_sentiments[top_sentiments == 'positif'][:3]])
        accuracy_positif = float(max_positive_similarity) if max_positive_similarity > 0 else 0

    if num_negative_sentiments > 0:
        max_negative_similarity = np.max(similarities_sentiments[top_indices_sentiments[top_sentiments == 'negatif'][:3]])
        accuracy_negatif = float(max_negative_similarity) if max_negative_similarity > 0 else 0

    print("top sentimen = ")
    print(top_sentiments)
    print("sentimen = ")
    print(sentiment_label)
    print("akurasi positif = ")
    print(accuracy_positif)
    print("akurasi negatif = ")
    print(accuracy_negatif)
    # print(similarities_sentiments)z
    # Menyimpan hasil
    response = {
        "sentiment": sentiment_label,
        "accuracy_positif": accuracy_positif,
        "accuracy_negatif": accuracy_negatif,
        "results": results
    }

    return jsonify(response)

    
if __name__ == '__main__':
    app.run()