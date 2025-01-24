import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

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
