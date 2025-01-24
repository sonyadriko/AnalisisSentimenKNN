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
                            <h4 class="fs-18 fw-semibold m-0">Pengujian</h4>
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
                                                <label for="tweetInput" class="form-label">Komentar atau ulasan</label>
                                                <textarea class="form-control" id="inputText" rows="4"
                                                    placeholder="Enter text here..." required></textarea>
                                            </div>
                                            <div class="mb-3">
                                                <label for="kValue" class="form-label">Jumlah (k)</label>
                                                <input type="number" class="form-control" id="kValue"
                                                    placeholder="Enter k value" min="1" required>
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
                                        <ul id="similarTexts"></ul>
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
                url: 'http://127.0.0.1:5000/api/knn',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    text: inputText,
                    k: parseInt(kValue)
                }),
                success: function(response) {
                    Swal.close();

                    // Tampilkan hasil dari server
                    $('#textpre').html('<b>' + response.preprocess_text + '</b>');
                    $('#sentiment').html('<b>' + response.sentiment + '</b>');

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