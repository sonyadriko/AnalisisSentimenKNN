# 📊 Analisis Sentimen Aplikasi GetContact Menggunakan Metode KNN

Proyek ini bertujuan untuk menganalisis sentimen pengguna terhadap aplikasi **GetContact** menggunakan algoritma **K-Nearest Neighbor (KNN)**. Proyek ini dapat membantu dalam memahami pola opini masyarakat, baik positif maupun negatif, terhadap aplikasi yang sedang populer ini.

---

## 🚀 Fitur Utama
- **Preprocessing Teks**: Membersihkan data teks untuk analisis yang lebih akurat.
- **K-Nearest Neighbor (KNN)**: Menggunakan algoritma KNN untuk memprediksi sentimen berdasarkan data latih.
- **Visualisasi Sentimen**: Menampilkan hasil prediksi sentimen dan teks-teks serupa yang relevan.
- **Interaktif & Mudah Digunakan**: Aplikasi ini dirancang untuk memberikan pengalaman pengguna yang lancar.

---

## 🛠️ Teknologi yang Digunakan
- **Backend**: Flask (Python)  
- **Frontend**: HTML, CSS, JavaScript, Bootstrap  
- **Database**: CSV (pelabelan data & vektor data)  
- **Library Pendukung**:
  - `scikit-learn`: Untuk algoritma KNN dan evaluasi model.
  - `pandas`: Untuk manipulasi data.
  - `numpy`: Untuk operasi matematis.
  - `TfidfVectorizer`: Untuk ekstraksi fitur teks berbasis TF-IDF.
  - `cosine_similarity`: Untuk menghitung kemiripan antar teks.

---

## 🔧 Cara Menjalankan Aplikasi
1. **Clone repository ini**:
   ```bash
   git clone https://github.com/username/repository-name.git
   cd repository-name
2. **Siapkan lingkungan virtual Python**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Untuk Linux/Mac
   venv\Scripts\activate     # Untuk Windows
3. **Install dependensi**:
   ```bash
   pip install -r requirements.txt
4. Jalankan server Flask:
  ```bash
  python app.py
  ```
5. Buka frontend di browser:
Akses aplikasi di http://127.0.0.1:5000.

---

## 📈 Proses Analisis Sentimen
1. Input Teks
Pengguna memasukkan teks (contoh: "Aplikasi ini sangat membantu dan mempermudah pekerjaan saya.").
2. Preprocessing
Teks diproses menjadi format bersih, seperti stemming dan penghapusan stopwords.
3. Prediksi Sentimen
Model KNN memprediksi apakah teks tersebut bernada positif atau negatif.
4. Kemiripan Teks
Aplikasi menampilkan 3 teks yang paling mirip berdasarkan skor cosine similarity.

---

## ✨ Contoh Hasil
- Input: "Aplikasi ini sangat membantu saya dalam memblokir nomor spam."
- Preprocessing Text: ['aplikasi', 'bantu', 'blokir', 'nomor', 'spam']
- Sentimen: Positif ✅
- Teks Serupa:
  1. "Aplikasi ini sangat berguna untuk mengenali nomor tak dikenal."
  2. "Sangat memudahkan saya dalam memblokir nomor yang tidak penting."
  3. "Fitur blokirnya sangat membantu saya menghindari spam."

---

## 🏆 Tujuan Proyek
Proyek ini dirancang untuk:
1. Menggunakan metode KNN dalam analisis sentimen.
2. Memberikan pemahaman lebih baik tentang opini masyarakat terhadap aplikasi GetContact
3. Meningkatkan kemampuan dalam implementasi algoritma pembelajaran mesin.

---

![Screenshot 2024-07-25 at 22-19-16 KNN Sentiment Analysis](https://github.com/user-attachments/assets/e697180e-ea52-4280-8d63-2709d35eaa9d)
