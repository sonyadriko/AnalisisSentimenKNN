<!DOCTYPE html>
<html lang="en">

<head>
    <title>Data Testing</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="KNN Sentimen Analisis" />
    <meta name="author" content="KNN" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <!-- App favicon -->
    <!-- <link rel="shortcut icon" href="assets/images/favicon.ico"> -->
    <!-- App css -->
    <link href="assets/css/app.min.css" rel="stylesheet" type="text/css" id="app-style" />
    <!-- Icons -->
    <link href="assets/css/icons.min.css" rel="stylesheet" type="text/css" />

    <!-- DataTables CSS -->
    <link href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css" rel="stylesheet" type="text/css" />
</head>

<body data-menu-color="dark" data-sidebar="default">

    <!-- Begin page -->
    <div id="app-layout">

        <!-- Topbar Start -->
        <?php include 'topbar.php' ?>
        <!-- end Topbar -->

        <!-- Left Sidebar Start -->
        <?php include 'sidebar.php' ?>
        <!-- Left Sidebar End -->

        <!-- ============================================================== -->
        <!-- Start Page Content here -->
        <!-- ============================================================== -->

        <div class="content-page">
            <div class="content">

                <!-- Start Content-->
                <div class="container-xxl">

                    <div class="py-3 d-flex align-items-sm-center flex-sm-row flex-column">
                        <div class="flex-grow-1">
                            <h4 class="fs-18 fw-semibold m-0">Data Testing</h4>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-12 col-xl-12">
                            <div class="card">
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div id="confusionMatrixResults">
                                                <h5>Confusion Matrix:</h5>
                                                <table border="1">
                                                    <tr>
                                                        <th></th>
                                                        <th>Predicted Positif</th>
                                                        <th>Predicted Negatif</th>
                                                    </tr>
                                                    <tr>
                                                        <th>Actual Positif</th>
                                                        <td id="positif_positif"></td>
                                                        <td id="positif_negatif"></td>
                                                    </tr>
                                                    <tr>
                                                        <th>Actual Negatif</th>
                                                        <td id="negatif_positif"></td>
                                                        <td id="negatif_negatif"></td>
                                                    </tr>
                                                </table>
                                            </div>
                                            <div id="metricsResults">
                                                <h5>Metrics:</h5>
                                                <ul>
                                                    <li>Accuracy: <span id="accuracy"></span></li>
                                                    <li>Precision: <span id="precision"></span></li>
                                                    <li>Recall: <span id="recall"></span></li>
                                                    <li>F1 Score: <span id="f1score"></span></li>
                                                </ul>
                                            </div>
                                            <button id="calculateConfusionMatrixBtn">Hitung Confusion Matrix</button>
                                        </div>

                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div> <!-- container-fluid -->
            </div> <!-- content -->

            <!-- Footer Start -->
            <?php include 'footer.php' ?>
            <!-- end Footer -->

        </div>
        <!-- ============================================================== -->
        <!-- End Page content -->
        <!-- ============================================================== -->

    </div>
    <!-- END wrapper -->

    <?php include 'scripts.php' ?>

    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@10"></script>

    <script>
    document.addEventListener('DOMContentLoaded', function() {
        const calculateConfusionMatrixBtn = document.getElementById('calculateConfusionMatrixBtn');

        calculateConfusionMatrixBtn.addEventListener('click', function() {
            Swal.fire({
                title: 'Menghitung Confusion Matrix',
                text: 'Mohon tunggu...',
                allowOutsideClick: false,
                didOpen: () => {
                    Swal.showLoading();
                }
            });

            axios.get('http://127.0.0.1:5000/confusion-matrix')
                .then(response => {
                    console.log(response.data);

                    document.getElementById('positif_positif').innerText = response.data
                        .positif_positif;
                    document.getElementById('positif_negatif').innerText = response.data
                        .positif_negatif;
                    document.getElementById('negatif_positif').innerText = response.data
                        .negatif_positif;
                    document.getElementById('negatif_negatif').innerText = response.data
                        .negatif_negatif;

                    document.getElementById('accuracy').innerText = response.data.accuracy;
                    document.getElementById('precision').innerText = response.data.precision;
                    document.getElementById('recall').innerText = response.data.recall;
                    document.getElementById('f1score').innerText = response.data.f1score;

                    Swal.fire({
                        icon: 'success',
                        title: 'Perhitungan selesai',
                        text: 'Confusion Matrix dan metrik berhasil dihitung!'
                    });
                })
                .catch(error => {
                    console.error('Error calculating confusion matrix:', error);

                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: 'Terjadi kesalahan saat menghitung Confusion Matrix dan metrik.'
                    });
                });
        });
    });
    </script>
</body>

</html>