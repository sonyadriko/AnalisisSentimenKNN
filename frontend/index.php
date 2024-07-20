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
                            <div class="col-md-6">
                                <div class="card">
                                    <div class="card-body">
                                        <h5 class="card-title mb-4">Tambah Tweet</h5>
                                        <form id="addTweetForm">
                                            <div class="mb-3">
                                                <label for="tweetInput" class="form-label">Tweet</label>
                                                <textarea class="form-control" id="tweetInput" name="tweet" rows="3"
                                                    required></textarea>
                                            </div>
                                            <button type="submit" class="btn btn-primary">Tambahkan</button>
                                        </form>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="card">
                                    <div class="card-body">
                                        <h5 class="card-title mb-4">Hasil</h5>
                                        <div id="hasilSentimen">Hasil sentimen :</div><br>
                                        <div id="accuracyPositif">Accuracy Positif :</div><br>
                                        <div id="accuracyNegatif">Accuracy Negatif :</div><br>
                                        <table id="dataRank" border="1">
                                            <thead>
                                                <tr>
                                                    <th>Data Number</th>
                                                    <th>Rank</th>
                                                    <th>Cosine Similarity</th>
                                                    <th>Tweet</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                <!-- Data will be inserted here -->
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <button id="startProcessBtn">Mulai Proses</button>
                </div>
            </div> <!-- container-fluid -->
        </div> <!-- content -->
        <!-- Footer Start -->
        <?php include 'footer.php' ?>
        <!-- end Footer -->
    </div>
    <!-- END wrapper -->

    <?php include 'scripts.php' ?>
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@10"></script>
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>

    <script>
    document.addEventListener('DOMContentLoaded', function() {
        const startProcessBtn = document.getElementById('startProcessBtn');
        const addTweetForm = document.querySelector('#addTweetForm');
        const hasilSentimenElem = document.querySelector('#hasilSentimen');
        const accuracyPositifElem = document.querySelector('#accuracyPositif');
        const accuracyNegatifElem = document.querySelector('#accuracyNegatif');
        const dataRankTableBody = document.querySelector('#dataRank tbody');

        startProcessBtn.addEventListener('click', function() {
            Swal.fire({
                title: 'Proses sedang berlangsung',
                text: 'Mohon tunggu...',
                allowOutsideClick: false,
                didOpen: () => {
                    Swal.showLoading();
                }
            });

            axios.get('http://127.0.0.1:5000/preprocessing')
                .then(response => {
                    return axios.get('http://127.0.0.1:5000/tf-idf');
                })
                .then(response => {
                    Swal.fire({
                        icon: 'success',
                        title: 'Proses selesai',
                        text: 'Proses preprocessing dan tf-idf berhasil dilakukan!'
                    });
                })
                .catch(error => {
                    console.error('Error processing data:', error);
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: 'Terjadi kesalahan saat memproses data.'
                    });
                });
        });

        addTweetForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const tweetInput = document.querySelector('#tweetInput').value.trim();

            if (tweetInput !== '') {
                Promise.all([
                        axios.post('http://127.0.0.1:5000/knn', {
                            tweet: tweetInput
                        }),
                        axios.get('http://127.0.0.1:5000/sentimen-pelabelan'),
                        axios.get('http://127.0.0.1:5000/similarity')
                    ])
                    .then(responses => {
                        const knnResponse = responses[0].data;
                        const sentimenPelabelanResponse = responses[1].data;
                        const similarityResponse = responses[2].data;

                        hasilSentimenElem.textContent =
                            `Hasil sentimen: ${similarityResponse.sentiment}`;
                        accuracyPositifElem.textContent =
                            `Accuracy Positif: ${similarityResponse.accuracy_positif.toFixed(2)}`;
                        accuracyNegatifElem.textContent =
                            `Accuracy Negatif: ${similarityResponse.accuracy_negatif.toFixed(2)}`;

                        dataRankTableBody.innerHTML = ''; // Clear previous results
                        similarityResponse.results.forEach(result => {
                            const row = document.createElement('tr');
                            row.innerHTML = `
                                    <td>${result.data_number}</td>
                                    <td>${result.rank}</td>
                                    <td>${result.cosine_similarity.toFixed(2)}</td>
                                    <td>${result.tweet}</td>
                                `;
                            dataRankTableBody.appendChild(row);
                        });

                        Swal.fire({
                            icon: 'success',
                            title: 'Proses selesai',
                            text: 'Proses analisis berhasil dilakukan!'
                        });
                    })
                    .catch(error => {
                        console.error('Error processing data:', error);
                        Swal.fire({
                            icon: 'error',
                            title: 'Error',
                            text: 'Terjadi kesalahan saat memproses data.'
                        });
                    });
            } else {
                Swal.fire({
                    icon: 'warning',
                    title: 'Peringatan',
                    text: 'Mohon isi tweet terlebih dahulu.'
                });
            }
        });
    });
    </script>
</body>

</html>