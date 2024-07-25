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
                            <div class="col-md-6">
                                <div class="card">
                                    <div class="card-body">
                                        <h5 class="card-title mb-4">Analisis Sentimen</h5>
                                        <form id="textForm">
                                            <div class="mb-3">
                                                <label for="tweetInput" class="form-label">Tweet</label>
                                                <textarea class="form-control" id="inputText" rows="4"
                                                    placeholder="Enter text here..." required></textarea>
                                            </div>
                                            <button type="submit" class="btn btn-primary">Submit</button>
                                        </form>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="card">
                                    <div class="card-body">
                                        <h5 class="card-title mb-4">Hasil</h5>
                                        <p>Preprocessing Text: <span id="textpre"></span></p>
                                        <p>Sentiment: <span id="sentiment"></span></p>
                                        <h3>Top 3 Similar Texts</h3>
                                        <ul id="similarTexts"></ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="mt-4">
                        <span>Tekan button untuk memulai proses preprocessing dan tfidf data training</span>
                        <button id="startProcessBtn" class="btn btn-success">Mulai Proses</button>
                    </div>
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
            var inputText = $('#inputText').val();
            if (inputText.trim() === "") {
                alert("Please enter some text.");
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

            $.ajax({
                url: 'http://127.0.0.1:5000/knn',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    text: inputText
                }),
                success: function(response) {
                    Swal.close();
                    $('#textpre').text(response.preprocess_text);
                    $('#sentiment').text(response.sentiment);
                    var similarTexts = $('#similarTexts');
                    similarTexts.empty();
                    response.results.forEach(function(result) {
                        similarTexts.append('<li>Rank: ' + result.rank +
                            ' - Similarity: ' + result.similarity.toFixed(
                                2) +
                            ' - Text: ' + result.text + '</li>');
                    });
                },
                error: function(xhr) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: 'Terjadi kesalahan saat mengirim data.'
                    });
                }
            });
        });

        $('#startProcessBtn').on('click', function() {
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
    });
    </script>
</body>

</html>