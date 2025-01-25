<!DOCTYPE html>
<html lang="en">

<head>
    <title>Dashboard</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="KNN Sentimen Analisis" />
    <meta name="author" content="KNN" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <link href="assets/css/app.min.css" rel="stylesheet" type="text/css" id="app-style" />
    <link href="assets/css/icons.min.css" rel="stylesheet" type="text/css" />
    <!-- <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet"> -->
    <style>
    #result {
        margin-top: 20px;
    }

    #result h2,
    #result h3 {
        color: #333;
    }

    #similarTexts {
        list-style-type: none;
        padding: 0;
    }

    #similarTexts li {
        background-color: #f9f9f9;
        margin-bottom: 10px;
        padding: 10px;
        border-radius: 4px;
        border: 1px solid #ddd;
    }
    </style>
</head>

<body data-menu-color="dark" data-sidebar="default">
    <div id="app-layout">
        <!-- Topbar Start -->
        <?php include 'topbar.php' ?>
        <!-- end Topbar -->
        <!-- Left Sidebar Start -->
        <?php include 'sidebar.php' ?>
        <!-- Left Sidebar End -->
        <div class="content-page">
            <div class="content">
                <!-- Start Content-->
                <div class="container-xxl">
                    <div class="py-3 d-flex align-items-sm-center flex-sm-row flex-column">
                        <div class="flex-grow-1">
                            <h4 class="fs-18 fw-semibold m-0">Dashboard</h4>
                        </div>
                    </div>
                    <div class="row">
                        <div class="row">
                            <div class="col-md-12">
                                <div class="card">
                                    <div class="card-body">
                                        <h5 class="card-title mb-4">K Nearest Neighbor</h5>
                                        <p>
                                            K Nearest Neighbor (KNN) adalah salah satu algoritma machine learning yang
                                            digunakan untuk
                                            klasifikasi dan regresi. Algoritma ini bekerja dengan mencari sejumlah data
                                            terdekat
                                            (<i>k neighbors</i>) dari data yang ingin diprediksi. Proses pengambilan
                                            keputusan didasarkan
                                            pada mayoritas label dari tetangga terdekatnya. Dalam kasus klasifikasi,
                                            algoritma KNN
                                            menentukan kelas dari data berdasarkan frekuensi kelas tetangga yang paling
                                            mirip.
                                            Dalam kasus regresi, rata-rata nilai tetangga digunakan sebagai prediksi.
                                        </p>
                                        <p>
                                            KNN sangat mudah diimplementasikan, tetapi performanya bergantung pada
                                            jumlah tetangga
                                            (<i>k</i>) yang dipilih, serta pada skala dan ukuran dataset. Penghitungan
                                            kemiripan
                                            sering menggunakan jarak Euclidean, Manhattan, atau <i>Cosine
                                                Similarity</i>,
                                            tergantung pada jenis data yang dianalisis.
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="row">
                        <div class="row">
                            <div class="col-md-12">
                                <div class="card">
                                    <div class="card-body">
                                        <h5 class="card-title mb-4">Get Contact</h5>
                                        <p>
                                            <i>Get Contact</i> adalah aplikasi yang dirancang untuk membantu pengguna
                                            dalam
                                            melacak dan mengenali nomor telepon yang tidak dikenal. Aplikasi ini bekerja
                                            dengan
                                            mengidentifikasi informasi seperti nama dan detail pemilik nomor telepon
                                            berdasarkan
                                            data yang telah dikumpulkan dari pengguna lain dalam platform.
                                        </p>
                                        <p>
                                            Salah satu fitur utama *Get Contact* adalah kemampuan untuk memblokir
                                            panggilan atau
                                            pesan dari nomor yang dicurigai sebagai spam atau penipuan. Selain itu,
                                            aplikasi ini
                                            memungkinkan pengguna untuk melihat bagaimana kontak mereka diberi label
                                            atau
                                            disimpan dalam daftar kontak pengguna lain, yang sering kali menjadi daya
                                            tarik utama.
                                        </p>
                                        <p>
                                            Penting untuk memahami bahwa penggunaan aplikasi ini harus mematuhi
                                            kebijakan privasi
                                            dan undang-undang yang berlaku, karena pengumpulan dan penggunaan data
                                            kontak melibatkan
                                            informasi pribadi yang sensitif.
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>



                    <!-- <div class="mt-4">
                        <span>Tekan button untuk memulai proses preprocessing dan tfidf data training</span>
                        <button id="startProcessBtn" class="btn btn-success">Mulai Proses</button>
                    </div> -->
                </div> <!-- container-fluid -->
            </div> <!-- content -->
            <!-- Footer Start -->
            <?php include 'footer.php' ?>
            <!-- end Footer -->
        </div>
    </div>
    <!-- END wrapper -->

    <?php include 'scripts.php' ?>
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@10"></script>
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>

    <script>
    $(document).ready(function() {
        $('#textForm').on('submit', function(event) {
            event.preventDefault();

            // Ambil input teks dan nilai k
            var inputText = $('#inputText').val();
            var kValue = $('#kValue').val();

            // Validasi input
            if (inputText.trim() === "") {
                alert("Please enter some text.");
                return;
            }

            if (!kValue || isNaN(kValue) || kValue <= 0) {
                alert("Please enter a valid positive number for k.");
                return;
            }

            Swal.fire({
                title: 'Mengirim data',
                text: 'Mohon tunggu...',
                allowOutsideClick: false,
                didOpen: () => {
                    Swal.showLoading();
                }
            });

            // Kirim data ke server Flask
            $.ajax({
                url: 'http://127.0.0.1:5000/knn',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    text: inputText,
                    k: parseInt(kValue)
                }),
                success: function(response) {
                    Swal.close();

                    // Tampilkan hasil dari server
                    $('#textpre').text(response.preprocess_text);
                    $('#sentiment').text(response.sentiment);

                    var similarTexts = $('#similarTexts');
                    similarTexts.empty();
                    response.results.forEach(function(result) {
                        similarTexts.append('<li>Rank: ' + result.rank +
                            ' - Similarity: ' + result.similarity.toFixed(2) +
                            ' - Text: ' + result.text + '</li>');
                    });
                },
                error: function(xhr) {
                    Swal.close();

                    // Tampilkan error dari server atau pesan default
                    var errorMessage = "Terjadi kesalahan saat mengirim data.";
                    if (xhr.responseJSON && xhr.responseJSON.error) {
                        errorMessage = xhr.responseJSON.error;
                    }

                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: errorMessage
                    });
                }
            });
        });
    });
    </script>

</body>

</html>