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
# !pip3 install swifter
# !pip3 install PySastrawi

import ast
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity
app = Flask(__name__)
CORS(app)


# API KNN

# @app.route('/knn')
@app.route('/knn', methods=['POST'])
def KNN():
    df = pd.read_csv("hasil_vector_matrix.csv", header=None)

    X = df.iloc[1:, :-1].values
    y = df.iloc[1:, -2].values
    XNum = X.astype(np.float64)
    yNum = y.astype(np.float64)

    similarities = cosine_similarity(XNum, XNum)

    k = 3

    nearest_neighbors = np.zeros((len(XNum), k), dtype=int)

    for i in range(len(XNum)):
        nearest_indices = np.argsort(similarities[i])[-k-1:-1][::-1]
        nearest_neighbors[i] = yNum[nearest_indices]

    predictions = np.zeros(len(XNum), dtype=int)

    for i in range(len(XNum)):
        prediction = np.argmax(np.bincount(nearest_neighbors[i]))
        predictions[i] = prediction

    accuracy = np.mean(predictions == yNum)
    ranking = np.argsort(similarities, axis=1)[:, ::-1]

    return jsonify(accuracy=accuracy, ranking=ranking.tolist())




# API tambah tweet to CSV
@app.route('/add-tweet', methods=['POST'])
def addTweet():
    data = request.form
    
    df = pd.read_csv('data_tweet.csv', encoding='latin1')

    current_rows = df.shape[0]
    
    tweet_text = data['tweet']
    
    df.loc[current_rows, 'rawContent'] = tweet_text
    df.loc[current_rows, 'status'] = 0

    df.to_csv('data_tweet.csv', index=False)
    
    return "berhasil ditambahkan" 

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








# API Count data
@app.route('/data-chart')
def dataChart():
    
    TWEET_DATA = pd.read_csv("pelabelan.csv", usecols=['sentimen'])
    counts = TWEET_DATA['sentimen'].value_counts()
    data = {"positif": int(counts.get('positif', 0)), "negatif": int(counts.get('negatif', 0))}
    
    return jsonify(data)


# API preprocessing
# @app.route('/preprocessing')
# def preprocessing():
    
#     TWEET_DATA = pd.read_csv("data_tweet.csv")
    
#     # mengubah text menjadi lowercase
#     TWEET_DATA['rawContent'] = TWEET_DATA['rawContent'].str.lower()

#     # ------ Tokenizing ---------

#     def remove_tweet_special(text):
#         # remove tab, new line, ans back slice
#         text = text.replace('\\t'," ").replace('\\n'," ").replace('\\u'," ").replace('\\',"")
#         # remove non ASCII (emoticon, chinese word, .etc)
#         text = text.encode('ascii', 'replace').decode('ascii')
#         # remove mention, link, hashtag
#         text = ' '.join(re.sub("([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)"," ", text).split())
#         # remove incomplete URL
#         return text.replace("http://", " ").replace("https://", " ")

#     TWEET_DATA['rawContent'] = TWEET_DATA['rawContent'].apply(remove_tweet_special)

#     #remove number
#     def remove_number(text):
#         return  re.sub(r"\d+", "", text)

#     TWEET_DATA['rawContent'] = TWEET_DATA['rawContent'].apply(remove_number)

#     #remove punctuation
#     def remove_punctuation(text):
#         return text.translate(str.maketrans("","",string.punctuation))

#     TWEET_DATA['rawContent'] = TWEET_DATA['rawContent'].apply(remove_punctuation)

#     #remove whitespace leading & trailing
#     def remove_whitespace_LT(text):
#         return text.strip()

#     TWEET_DATA['rawContent'] = TWEET_DATA['rawContent'].apply(remove_whitespace_LT)

#     #remove multiple whitespace into single whitespace
#     def remove_whitespace_multiple(text):
#         return re.sub('\s+',' ',text)

#     TWEET_DATA['rawContent'] = TWEET_DATA['rawContent'].apply(remove_whitespace_multiple)

#     # remove single char
#     def remove_singl_char(text):
#         return re.sub(r"\b[a-zA-Z]\b", "", text)

#     TWEET_DATA['rawContent'] = TWEET_DATA['rawContent'].apply(remove_singl_char)

#     # NLTK word rokenize 
#     def word_tokenize_wrapper(text):
#         return word_tokenize(text)

#     TWEET_DATA['tweet_tokens'] = TWEET_DATA['rawContent'].apply(word_tokenize_wrapper)
    
#     # NLTK calc frequency distribution
#     def freqDist_wrapper(text):
#         return FreqDist(text)

#     TWEET_DATA['tweet_tokens_fdist'] = TWEET_DATA['tweet_tokens'].apply(freqDist_wrapper)
#     TWEET_DATA['tweet_tokens_fdist'].head().apply(lambda x : x.most_common())
    

#     # ----------------------- get stopword from NLTK stopword -------------------------------
#     # get stopword indonesia
#     list_stopwords = stopwords.words('indonesian')


#     # ---------------------------- manualy add stopword  ------------------------------------
#     # append additional stopword
#     list_stopwords.extend(["yg", "dg", "rt", "dgn", "ny", "d", 'klo', 
#                            'kalo', 'amp', 'biar', 'bikin', 'bilang', 
#                            'gak', 'ga', 'krn', 'nya', 'nih', 'sih', 
#                            'si', 'tau', 'tdk', 'tuh', 'utk', 'ya', 
#                            'jd', 'jgn', 'sdh', 'aja', 'n', 't', 
#                            'nyg', 'hehe', 'pen', 'u', 'nan', 'loh', 'rt',
#                            '&amp', 'yah'])

#     # ----------------------- add stopword from txt file ------------------------------------
#     # read txt stopword using pandas
#     txt_stopword = pd.read_csv("stopwords.txt", names= ["stopwords"], header = None)

#     # convert stopword string to list & append additional stopword
#     list_stopwords.extend(txt_stopword["stopwords"][0].split(' '))

#     # ---------------------------------------------------------------------------------------

#     # convert list to dictionary
#     list_stopwords = set(list_stopwords)


#     #remove stopword pada list token
#     def stopwords_removal(words):
#         return [word for word in words if word not in list_stopwords]

#     TWEET_DATA['tweet_tokens_WSW'] = TWEET_DATA['tweet_tokens'].apply(stopwords_removal) 
    
#     # import Sastrawi package
#     from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
#     import swifter


#     # create stemmer
#     factory = StemmerFactory()
#     stemmer = factory.create_stemmer()

#     # stemmed
#     def stemmed_wrapper(term):
#         return stemmer.stem(term)

#     term_dict = {}

#     for document in TWEET_DATA['tweet_tokens_WSW']:
#         for term in document:
#             if term not in term_dict:
#                 term_dict[term] = ' '

#     print(len(term_dict))
#     print("------------------------")

#     for term in term_dict:
#         term_dict[term] = stemmed_wrapper(term)
#         print(term,":" ,term_dict[term])

#     print(term_dict)
#     print("------------------------")


#     # apply stemmed term to dataframe
#     def get_stemmed_term(document):
#         return [term_dict[term] for term in document]

#     TWEET_DATA['tweet_tokens_stemmed'] = TWEET_DATA['tweet_tokens_WSW'].swifter.apply(get_stemmed_term)
    
#     TWEET_DATA.to_csv("Text_Preprocessing.csv")
    
#     return "preprocessing berhasil"

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



# API TF-IDF
# @app.route('/tf-idf')
# def tfidf():
#     TWEET_DATA = pd.read_csv("Text_Preprocessing.csv", usecols=["tweet_tokens_stemmed"])
#     TWEET_DATA.columns = ["tweet"]

#     def convert_text_list(texts):
#         texts = ast.literal_eval(texts)
#         return [text for text in texts]

#     TWEET_DATA["tweet_list"] = TWEET_DATA["tweet"].apply(convert_text_list)
    
#     def calc_TF(document):
#         # Counts the number of times the word appears in review
#         TF_dict = {}
#         for term in document:
#             if term in TF_dict:
#                 TF_dict[term] += 1
#             else:
#                 TF_dict[term] = 1
#         # Computes tf for each word
#         for term in TF_dict:
#             TF_dict[term] = TF_dict[term] / len(document)
#         return TF_dict

#     TWEET_DATA["TF_dict"] = TWEET_DATA['tweet_list'].apply(calc_TF)
    
#     # Check TF result
#     #index = 99
#     index = TWEET_DATA.shape[0]
    
#     print('%20s' % "term", "\t", "TF\n")
#     for key in TWEET_DATA["TF_dict"][index-1]:
#         print('%20s' % key, "\t", TWEET_DATA["TF_dict"][index-1][key])
    
#     def calc_DF(tfDict):
#         count_DF = {}
#         # Run through each document's tf dictionary and increment countDict's (term, doc) pair
#         for document in tfDict:
#             for term in document:
#                 if term in count_DF:
#                     count_DF[term] += 1
#                 else:
#                     count_DF[term] = 1
#         return count_DF

#     DF = calc_DF(TWEET_DATA["TF_dict"])
    
#     n_document = len(TWEET_DATA)

#     def calc_IDF(__n_document, __DF):
#         IDF_Dict = {}
#         for term in __DF:
#             IDF_Dict[term] = np.log(__n_document / (__DF[term] + 1))
#         return IDF_Dict

#     #Stores the idf dictionary
#     IDF = calc_IDF(n_document, DF)
    
#     #calc TF-IDF
#     def calc_TF_IDF(TF):
#         TF_IDF_Dict = {}
#         #For each word in the review, we multiply its tf and its idf.
#         for key in TF:
#             TF_IDF_Dict[key] = TF[key] * IDF[key]
#         return TF_IDF_Dict

#     #Stores the TF-IDF Series
#     TWEET_DATA["TF-IDF_dict"] = TWEET_DATA["TF_dict"].apply(calc_TF_IDF)
    
#     # Check TF-IDF result
#     #index = 99
#     index = TWEET_DATA.shape[0]

#     print('%20s' % "term", "\t", '%10s' % "TF", "\t", '%20s' % "TF-IDF\n")
#     for key in TWEET_DATA["TF-IDF_dict"][index-1]:
#         print('%20s' % key, "\t", TWEET_DATA["TF_dict"][index-1][key] ,"\t" , TWEET_DATA["TF-IDF_dict"][index-1][key])
        
    
#     # sort descending by value for DF dictionary 
#     sorted_DF = sorted(DF.items(), key=lambda kv: kv[1], reverse=True)[:100]

#     # Create a list of unique words from sorted dictionay `sorted_DF`
#     unique_term = [item[0] for item in sorted_DF]

#     def calc_TF_IDF_Vec(__TF_IDF_Dict):
#         TF_IDF_vector = [0.0] * len(unique_term)

#         # For each unique word, if it is in the review, store its TF-IDF value.
#         for i, term in enumerate(unique_term):
#             if term in __TF_IDF_Dict:
#                 TF_IDF_vector[i] = __TF_IDF_Dict[term]
#         return TF_IDF_vector

#     TWEET_DATA["TF_IDF_Vec"] = TWEET_DATA["TF-IDF_dict"].apply(calc_TF_IDF_Vec)
    
    
#     # Convert Series to List
#     TF_IDF_Vec_List = np.array(TWEET_DATA["TF_IDF_Vec"].to_list())

#     # Sum element vector in axis=0 
#     sums = TF_IDF_Vec_List.sum(axis=0)

#     data = []

#     for col, term in enumerate(unique_term):
#         data.append((term, sums[col]))

#     ranking = pd.DataFrame(data, columns=['term', 'rank'])
#     ranking.sort_values('rank', ascending=False)
    
#     # join list of token as single document string

#     def join_text_list(texts):
#         texts = ast.literal_eval(texts)
#         return ' '.join([text for text in texts])
    
#     TWEET_DATA["tweet_join"] = TWEET_DATA["tweet"].apply(join_text_list)
    
# #     from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
# #     from sklearn.preprocessing import normalize

#     max_features = 100

#     # calc TF vector
#     cvect = CountVectorizer(max_features=max_features)
#     TF_vector = cvect.fit_transform(TWEET_DATA["tweet_join"])

#     # normalize TF vector
#     normalized_TF_vector = normalize(TF_vector, norm='l1', axis=1)

#     # calc IDF
#     tfidf = TfidfVectorizer(max_features=max_features, smooth_idf=False)
#     tfs = tfidf.fit_transform(TWEET_DATA["tweet_join"])
#     IDF_vector = tfidf.idf_

#     # hitung TF x IDF sehingga dihasilkan TFIDF matrix / vector
#     tfidf_mat = normalized_TF_vector.multiply(IDF_vector).toarray()

#     max_features = 100

#     # ngram_range (1, 3) to use unigram, bigram, trigram
#     cvect = CountVectorizer(max_features=max_features, ngram_range=(1,3))
#     counts = cvect.fit_transform(TWEET_DATA["tweet_join"])

#     normalized_counts = normalize(counts, norm='l1', axis=1)

#     tfidf = TfidfVectorizer(max_features=max_features, ngram_range=(1,3), smooth_idf=False)
#     tfs = tfidf.fit_transform(TWEET_DATA["tweet_join"])

#     # tfidf_mat = normalized_counts.multiply(tfidf.idf_).toarray()
    
#     type(counts)
#     counts.shape
    
#     print(tfidf.vocabulary_)
    
#     print(tfidf.get_feature_names_out())
#     a=tfidf.get_feature_names_out()
    
#     print(tfs.toarray())
#     b=tfs.toarray()
    
#     tfidf_mat = normalized_counts.multiply(IDF_vector).toarray()
#     dfbtf = pd.DataFrame(data=tfidf_mat,columns=[a])
#     dfbtf
    
#     dfbtf.to_csv("hasil_vector_matrix.csv")
    
#     return "tf-idf sukses"

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

    return "TF-IDF berhasil dihitung dan hasil disimpan sebagai hasil_vector_matrix.csv"


# API Pelabelan sentimen
# @app.route('/sentimen-pelabelan')
# def pelabelan():

#     # Baca file excel
#     data = pd.read_csv('hasil_vector_matrix.csv')
#     data1 = pd.read_csv('data_tweet.csv')
#     # Mengambil indeks baris dengan status = 0
#     index_zero_status = data1.loc[data1['status'] == 0].index.tolist()
    
#     threshold = 0.5
#     # mengambil nilai pada kolom terakhir pada setiap baris data, kecuali kolom terakhir yang merupakan label sentimen
#     last_row = data.iloc[:, -1]

#     # list untuk menyimpan label sentimen
#     sentiments = []

#     # loop pada setiap nilai pada kolom terakhir pada setiap baris data
#     for i in range(len(last_row)):
#         if last_row[i] >= threshold:
#             # jika nilai lebih besar atau sama dengan threshold, sentimen positif
#             sentiments.append('positif')
#         else:
#             # jika nilai kurang dari threshold, sentimen negatif
#             sentiments.append('negatif')

#     # menambahkan kolom "sentimen" ke dalam dataframe
#     data.loc[data.index.isin(index_zero_status), 'status'] = 0
#     data.loc[~data.index.isin(index_zero_status), 'status'] = 1
    
#     data['aktual'] = sentiments
#     data['sentimen'] = sentiments
#     data.loc[data['status'] == 0, 'aktual'] = '-'
    
#     data.to_csv("pelabelan.csv", index=False)

#     # Tampilkan dataframe hasil pelabelan
#     print(data)
#     last_row = data.tail(1)
#     data = last_row.to_dict(orient='records')
#     return jsonify(data)
    
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
# @app.route('/similarity', methods=['GET'])
# def similarity():
#     # Membaca data vektor dan sentimen dari file CSV
#     df_vectors = pd.read_csv("pelabelan.csv", header=None, skiprows=1)
#     vectors = df_vectors.iloc[:, 1:-3].values
#     sentiments = df_vectors.iloc[:, -1].values

#     # Membaca data tweet dari file CSV
#     df_tweet = pd.read_csv("data_tweet.csv", encoding='latin1')

#     # Mengambil data input yang akan dibandingkan dengan semua data
#     input_vector_sentiments = vectors[-1]

#     # Menghitung cosine similarity
#     similarities_sentiments = cosine_similarity([input_vector_sentiments], vectors[:-1])[0]

#     # Mengambil 3 data dengan nilai cosine similarity tertinggi
#     top_indices_sentiments = np.argsort(similarities_sentiments)[-3:][::-1]

#     # Menyimpan hasil ranking data tertinggi dan teks tweet
#     results = []
#     for i, idx in enumerate(top_indices_sentiments):
#         rank = i + 1
#         similarity = similarities_sentiments[idx]
#         data_number = int(idx + 1)
#         tweet_text = df_tweet.iloc[idx]['rawContent']
#         result = {
#             "rank": rank,
#             "data_number": data_number,
#             "cosine_similarity": float(similarity),
#             "tweet": tweet_text
#         }
#         results.append(result)

#     # Menghitung jumlah sentimen negatif dan positif dari 3 data ranking teratas
#     top_sentiments = sentiments[top_indices_sentiments]
#     num_negative_sentiments = np.sum(top_sentiments == 'negatif')
#     num_positive_sentiments = np.sum(top_sentiments == 'positif')

#     # Menentukan sentimen berdasarkan perbandingan jumlah sentimen positif dan negatif
#     if num_positive_sentiments > num_negative_sentiments:
#         sentiment_label = "positif"
#     else:
#         sentiment_label = "negatif"

#     # Menghitung accuracy positif dan accuracy negatif
#     accuracy_positif = 0
#     accuracy_negatif = 0

#     if num_positive_sentiments > 0:
#         max_positive_similarity = np.max(similarities_sentiments[top_indices_sentiments[top_sentiments == 'positif'][:3]])
#         accuracy_positif = float(max_positive_similarity) if max_positive_similarity > 0 else 0

#     if num_negative_sentiments > 0:
#         max_negative_similarity = np.max(similarities_sentiments[top_indices_sentiments[top_sentiments == 'negatif'][:3]])
#         accuracy_negatif = float(max_negative_similarity) if max_negative_similarity > 0 else 0

#     print("top sentimen = ")
#     print(top_sentiments)
#     print("sentimen = ")
#     print(sentiment_label)
#     print("akurasi positif = ")
#     print(accuracy_positif)
#     print("akurasi negatif = ")
#     print(accuracy_negatif)
#     print(similarities_sentiments)
#     # Menyimpan hasil
#     response = {
#         "sentiment": sentiment_label,
#         "accuracy_positif": accuracy_positif,
#         "accuracy_negatif": accuracy_negatif,
#         "results": results
#     }

#     return jsonify(response)


# @app.route('/similarity', methods=['GET'])
# def similarity():
#     try:
#         # Read vector and sentiment data from CSV files
#         df_vectors = pd.read_csv("pelabelan.csv", header=None, skiprows=1)
#         vectors = df_vectors.iloc[:, 1:-2].values  # Ambil vektor fitur dari kolom kedua sampai dua kolom terakhir
#         sentiments = df_vectors.iloc[:, -1].values  # Ambil sentimen dari kolom terakhir

#         # Read tweet data from CSV
#         df_tweet = pd.read_csv("data_tweet.csv", encoding='latin1')

#         # Ensure df_tweet has 'rawContent' column
#         if 'rawContent' not in df_tweet.columns:
#             return jsonify({'error': 'Column "rawContent" not found in data_tweet.csv'})

#         # Get the input vector (last row in vectors)
#         input_vector_sentiments = vectors[-1]

#         # Normalize vectors including input vector
#         vectors_normalized = normalize(vectors, axis=1, norm='l2')  # Normalisasi vektor fitur
#         input_vector_normalized = normalize(input_vector_sentiments.reshape(1, -1), norm='l2')  # Normalisasi vektor input

#         # Calculate cosine similarity
#         similarities_sentiments = cosine_similarity(input_vector_normalized, vectors_normalized[:-1])[0]

#         # Get top 3 data with highest cosine similarity
#         top_indices_sentiments = np.argsort(similarities_sentiments)[-3:][::-1]
#         results = []

#         # Iterate through top indices and retrieve data
#         for i, idx in enumerate(top_indices_sentiments):
#             rank = i + 1
#             similarity = similarities_sentiments[idx]
#             data_number = int(idx + 1)

#             # Safely retrieve tweet text
#             if idx < len(df_tweet):
#                 tweet_text = df_tweet.iloc[idx]['rawContent']
#             else:
#                 tweet_text = 'Not available'

#             result = {
#                 "rank": rank,
#                 "data_number": data_number,
#                 "cosine_similarity": float(similarity),
#                 "tweet": tweet_text
#             }
#             results.append(result)

#         # Calculate number of negative and positive sentiments in top 3
#         top_sentiments = sentiments[top_indices_sentiments]
#         num_negative_sentiments = np.sum(top_sentiments == 'negatif')
#         num_positive_sentiments = np.sum(top_sentiments == 'positif')

#         # Determine sentiment based on the number of positive and negative sentiments
#         if num_positive_sentiments > num_negative_sentiments:
#             sentiment_label = "positif"
#         else:
#             sentiment_label = "negatif"

#         # Calculate accuracy positive and accuracy negative
#         accuracy_positif = 0
#         accuracy_negatif = 0

#         if sentiment_label == "positif" and num_positive_sentiments > 0:
#             max_positive_similarity = np.max(similarities_sentiments[top_indices_sentiments[top_sentiments == 'positif']])
#             accuracy_positif = float(max_positive_similarity) if max_positive_similarity > 0 else 0
#             accuracy_negatif = 0  # Set accuracy negatif to 0

#         if sentiment_label == "negatif" and num_negative_sentiments > 0:
#             max_negative_similarity = np.max(similarities_sentiments[top_indices_sentiments[top_sentiments == 'negatif']])
#             accuracy_negatif = float(max_negative_similarity) if max_negative_similarity > 0 else 0
#             accuracy_positif = 0  # Set accuracy positif to 0

#         print("top sentimen = ")
#         print(top_sentiments)
#         print("sentimen = ")
#         print(sentiment_label)
#         print("akurasi positif = ")
#         print(accuracy_positif)
#         print("akurasi negatif = ")
#         print(accuracy_negatif)
#         print(similarities_sentiments)
#         # Example response
#         response = {
#             "sentiment": sentiment_label,
#             "accuracy_positif": accuracy_positif,
#             "accuracy_negatif": accuracy_negatif,
#             "results": results
#         }

#         return jsonify(response)

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/similarity', methods=['GET'])
# def similarity():
#     try:
#         # Read vector and sentiment data from CSV files
#         df_vectors = pd.read_csv("pelabelan.csv", header=None, skiprows=1)
#         vectors = df_vectors.iloc[:, 1:-2].values  # Ambil vektor fitur dari kolom kedua sampai dua kolom terakhir
#         sentiments = df_vectors.iloc[:, -1].values  # Ambil sentimen dari kolom terakhir

#         # Read tweet data from CSV
#         df_tweet = pd.read_csv("data_tweet.csv", encoding='latin1')

#         # Ensure df_tweet has 'rawContent' column
#         if 'rawContent' not in df_tweet.columns:
#             return jsonify({'error': 'Column "rawContent" not found in data_tweet.csv'})

#         # Get the input vector (last row in vectors)
#         input_vector_sentiments = vectors[-1]

#         # Normalize vectors including input vector
#         vectors_normalized = normalize(vectors, axis=1, norm='l2')  # Normalisasi vektor fitur
#         input_vector_normalized = normalize(input_vector_sentiments.reshape(1, -1), norm='l2')  # Normalisasi vektor input

#         # Calculate cosine similarity
#         similarities_sentiments = cosine_similarity(input_vector_normalized, vectors_normalized[:-1])[0]

#         # Get top 3 data with highest cosine similarity
#         top_indices_sentiments = np.argsort(similarities_sentiments)[-3:][::-1]
#         results = []

#         # Iterate through top indices and retrieve data
#         for i, idx in enumerate(top_indices_sentiments):
#             rank = i + 1
#             similarity = similarities_sentiments[idx]
#             data_number = int(idx + 1)

#             # Safely retrieve tweet text
#             if idx < len(df_tweet):
#                 tweet_text = df_tweet.iloc[idx]['rawContent']
#             else:
#                 tweet_text = 'Not available'

#             result = {
#                 "rank": rank,
#                 "data_number": data_number,
#                 "cosine_similarity": float(similarity),
#                 "tweet": tweet_text
#             }
#             results.append(result)

#         # Calculate number of negative and positive sentiments in top 3
#         top_sentiments = sentiments[top_indices_sentiments]
#         num_negative_sentiments = np.sum(top_sentiments == 'negatif')
#         num_positive_sentiments = np.sum(top_sentiments == 'positif')

#         # Determine sentiment based on the number of positive and negative sentiments
#         if num_positive_sentiments > num_negative_sentiments:
#             sentiment_label = "positif"
#         else:
#             sentiment_label = "negatif"

#         # Calculate accuracy positive and accuracy negative
#         accuracy_positif = 0
#         accuracy_negatif = 0

#         if sentiment_label == "positif" and num_positive_sentiments > 0:
#             max_positive_similarity = np.max(similarities_sentiments[top_indices_sentiments[top_sentiments == 'positif']])
#             accuracy_positif = float(max_positive_similarity) if max_positive_similarity > 0 else 0
#             accuracy_negatif = 0  # Set accuracy negatif to 0

#         if sentiment_label == "negatif" and num_negative_sentiments > 0:
#             max_negative_similarity = np.max(similarities_sentiments[top_indices_sentiments[top_sentiments == 'negatif']])
#             accuracy_negatif = float(max_negative_similarity) if max_negative_similarity > 0 else 0
#             accuracy_positif = 0  # Set accuracy positif to 0

#         print("top sentimen = ")
#         print(top_sentiments)
#         print("sentimen = ")
#         print(sentiment_label)
#         print("akurasi positif = ")
#         print(accuracy_positif)
#         print("akurasi negatif = ")
#         print(accuracy_negatif)
#         print(similarities_sentiments)
#         # Example response
#         response = {
#             "sentiment": sentiment_label,
#             "accuracy_positif": accuracy_positif,
#             "accuracy_negatif": accuracy_negatif,
#             "results": results
#         }

#         return jsonify(response)

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/similarity', methods=['GET'])
# def similarity():
#     try:
#         # Read vector and sentiment data from CSV files
#         df_vectors = pd.read_csv("pelabelan.csv", header=None, skiprows=1)
#         vectors = df_vectors.iloc[:, 1:-2].values  # Ambil vektor fitur dari kolom kedua sampai dua kolom terakhir
#         sentiments = df_vectors.iloc[:, -1].values  # Ambil sentimen dari kolom terakhir

#         # Read tweet data from CSV
#         df_tweet = pd.read_csv("data_tweet.csv", encoding='latin1')

#         # Ensure df_tweet has 'rawContent' column
#         if 'rawContent' not in df_tweet.columns:
#             return jsonify({'error': 'Column "rawContent" not found in data_tweet.csv'})

#         # Get the input vector (last row in vectors)
#         input_vector_sentiments = vectors[-1]

#         # Normalize vectors including input vector
#         vectors_normalized = normalize(vectors, axis=1, norm='l2')  # Normalisasi vektor fitur
#         input_vector_normalized = normalize(input_vector_sentiments.reshape(1, -1), norm='l2')  # Normalisasi vektor input

#         # Calculate cosine similarity
#         similarities_sentiments = cosine_similarity(input_vector_normalized, vectors_normalized[:-1])[0]

#         # Get top 3 data with highest cosine similarity
#         top_indices_sentiments = np.argsort(similarities_sentiments)[-3:][::-1]
#         results = []

#         # Iterate through top indices and retrieve data
#         for i, idx in enumerate(top_indices_sentiments):
#             rank = i + 1
#             similarity = similarities_sentiments[idx]
#             data_number = int(idx + 1)

#             # Safely retrieve tweet text
#             if idx < len(df_tweet):
#                 tweet_text = df_tweet.iloc[idx]['rawContent']
#             else:
#                 tweet_text = 'Not available'

#             result = {
#                 "rank": rank,
#                 "data_number": data_number,
#                 "cosine_similarity": float(similarity),
#                 "tweet": tweet_text
#             }
#             results.append(result)

#         # Calculate number of negative and positive sentiments in top 3
#         top_sentiments = sentiments[top_indices_sentiments]
#         num_negative_sentiments = np.sum(top_sentiments == 'negatif')
#         num_positive_sentiments = np.sum(top_sentiments == 'positif')

#         # Determine sentiment based on the number of positive and negative sentiments
#         if num_positive_sentiments > num_negative_sentiments:
#             sentiment_label = "positif"
#         else:
#             sentiment_label = "negatif"

#         # Calculate accuracy positive and accuracy negative
#         accuracy_positif = 0
#         accuracy_negatif = 0

#         if sentiment_label == "positif" and num_positive_sentiments > 0:
#             max_positive_similarity = np.max(similarities_sentiments[top_indices_sentiments[top_sentiments == 'positif']])
#             accuracy_positif = float(max_positive_similarity) if max_positive_similarity > 0 else 0
#             accuracy_negatif = 0  # Set accuracy negatif to 0

#         if sentiment_label == "negatif" and num_negative_sentiments > 0:
#             max_negative_similarity = np.max(similarities_sentiments[top_indices_sentiments[top_sentiments == 'negatif']])
#             accuracy_negatif = float(max_negative_similarity) if max_negative_similarity > 0 else 0
#             accuracy_positif = 0  # Set accuracy positif to 0

#         # Example response
#         response = {
#             "sentiment": sentiment_label,
#             "accuracy_positif": accuracy_positif,
#             "accuracy_negatif": accuracy_negatif,
#             "results": results
#         }

#         return jsonify(response)

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

@app.route('/similarity', methods=['GET'])
def similarity():
    try:
        # Read vector and sentiment data from CSV files
        df_vectors = pd.read_csv("pelabelan.csv", header=None, skiprows=1)
        vectors = df_vectors.iloc[:, 1:-2].values  # Ambil vektor fitur dari kolom kedua sampai dua kolom terakhir
        sentiments = df_vectors.iloc[:, -1].values  # Ambil sentimen dari kolom terakhir

        # Debug: Print first few vectors and sentiments
        print("Vectors:", vectors[:5])
        print("Sentiments:", sentiments[:5])

        # Read tweet data from CSV
        df_tweet = pd.read_csv("data_tweet.csv", encoding='latin1')

        # Ensure df_tweet has 'rawContent' column
        if 'rawContent' not in df_tweet.columns:
            return jsonify({'error': 'Column "rawContent" not found in data_tweet.csv'})

        # Get the input vector (last row in vectors)
        input_vector_sentiments = vectors[-1]

        # Normalize vectors including input vector
        vectors_normalized = normalize(vectors, axis=1, norm='l2')  # Normalisasi vektor fitur
        input_vector_normalized = normalize(input_vector_sentiments.reshape(1, -1), norm='l2')  # Normalisasi vektor input

        # Debug: Print normalized vectors
        print("Normalized Vectors:", vectors_normalized[:5])
        print("Normalized Input Vector:", input_vector_normalized)

        # Calculate cosine similarity
        similarities_sentiments = cosine_similarity(input_vector_normalized, vectors_normalized[:-1])[0]

        # Debug: Print cosine similarities
        print("Cosine Similarities:", similarities_sentiments)

        # Get top 3 data with highest cosine similarity
        top_indices_sentiments = np.argsort(similarities_sentiments)[-3:][::-1]
        results = []

        # Iterate through top indices and retrieve data
        for i, idx in enumerate(top_indices_sentiments):
            rank = i + 1
            similarity = similarities_sentiments[idx]
            data_number = int(idx + 1)

            # Safely retrieve tweet text
            if idx < len(df_tweet):
                tweet_text = df_tweet.iloc[idx]['rawContent']
            else:
                tweet_text = 'Not available'

            result = {
                "rank": rank,
                "data_number": data_number,
                "cosine_similarity": float(similarity),
                "tweet": tweet_text
            }
            results.append(result)

        # Calculate number of negative and positive sentiments in top 3
        top_sentiments = sentiments[top_indices_sentiments]
        num_negative_sentiments = np.sum(top_sentiments == 'negatif')
        num_positive_sentiments = np.sum(top_sentiments == 'positif')

        # Debug: Print top sentiments
        print("Top Sentiments:", top_sentiments)
        print("Num Negative Sentiments:", num_negative_sentiments)
        print("Num Positive Sentiments:", num_positive_sentiments)

        # Determine sentiment based on the number of positive and negative sentiments
        if num_positive_sentiments > num_negative_sentiments:
            sentiment_label = "positif"
        else:
            sentiment_label = "negatif"

        # Calculate accuracy positive and accuracy negative
        accuracy_positif = 0
        accuracy_negatif = 0

        if sentiment_label == "positif" and num_positive_sentiments > 0:
            max_positive_similarity = np.max(similarities_sentiments[top_indices_sentiments[top_sentiments == 'positif']])
            accuracy_positif = float(max_positive_similarity) if max_positive_similarity > 0 else 0
            accuracy_negatif = 0  # Set accuracy negatif to 0

        if sentiment_label == "negatif" and num_negative_sentiments > 0:
            max_negative_similarity = np.max(similarities_sentiments[top_indices_sentiments[top_sentiments == 'negatif']])
            accuracy_negatif = float(max_negative_similarity) if max_negative_similarity > 0 else 0
            accuracy_positif = 0  # Set accuracy positif to 0

        # Debug: Print final sentiment and accuracies
        print("Final Sentiment:", sentiment_label)
        print("Accuracy Positif:", accuracy_positif)
        print("Accuracy Negatif:", accuracy_negatif)

        # Example response
        response = {
            "sentiment": sentiment_label,
            "accuracy_positif": accuracy_positif,
            "accuracy_negatif": accuracy_negatif,
            "results": results
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
# approve status
@app.route('/approve-status', methods=['POST'])
def approve_status():
    # Mendapatkan indeks yang dikirim melalui body request
    index = request.json.get('index')

    # Update status pada file data_tweet.csv
    tweet_data = pd.read_csv('data_tweet.csv')
    if int(index) in tweet_data.index:
        tweet_data.at[int(index), 'status'] = 1
        tweet_data.to_csv('data_tweet.csv', index=False)
    else:
        return jsonify({'message': 'Invalid index for data_tweet.csv.'})

    # Update status pada file pelabelan.csv
    pelabelan_data = pd.read_csv('pelabelan.csv')
    if int(index) in pelabelan_data.index:
        pelabelan_data.at[int(index), 'status'] = 1
        pelabelan_data.at[int(index), 'aktual'] = pelabelan_data.at[int(index), 'sentimen']  # Menambahkan pembaruan nilai 'aktual' dengan nilai 'sentimen'
        pelabelan_data.to_csv('pelabelan.csv', index=False)
    else:
        return jsonify({'message': 'Invalid index for pelabelan.csv.'})

    return jsonify({'message': 'Status updated successfully.'})


# decline status
@app.route('/decline-status', methods=['POST'])
def decline_status():
    # Mendapatkan indeks yang dikirim melalui body request
    index = request.json.get('index')

    # Update status pada file data_tweet.csv
    tweet_data = pd.read_csv('data_tweet.csv')
    if int(index) in tweet_data.index:
        tweet_data.at[int(index), 'status'] = 2
        tweet_data.to_csv('data_tweet.csv', index=False)
    else:
        return jsonify({'message': 'Invalid index for data_tweet.csv.'})

   # Update status pada file pelabelan.csv
    pelabelan_data = pd.read_csv('pelabelan.csv')
    if int(index) in pelabelan_data.index:
        pelabelan_data.at[int(index), 'status'] = 2

        sentimen = pelabelan_data.at[int(index), 'sentimen']
        aktual = 'negatif' if sentimen == 'positif' else 'positif'
        pelabelan_data.at[int(index), 'aktual'] = aktual

        pelabelan_data.to_csv('pelabelan.csv', index=False)
    else:
        return jsonify({'message': 'Invalid index for pelabelan.csv.'})

    return jsonify({'message': 'Status updated successfully.'})

    
if __name__ == '__main__':
    app.run()