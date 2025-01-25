<!DOCTYPE html>
<html lang="en">

<head>
    <title>Data Training</title>
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

<!-- body start -->

<body data-menu-color="dark" data-sidebar="default">

    <!-- Begin page -->
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
                            <h4 class="fs-18 fw-semibold m-0">TF IDF</h4>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-12 col-xl-12">
                            <div class="card">
                                <div class="card-body">
                                    <div class="row">
                                        <?php
                    
                    // Nama file CSV
                    // $csvFile = '../backend/hasil_vector_matrix.csv';
                    $csvFile = '../backend/files/pelabelan.csv';
                    
                    // Periksa apakah file CSV ada
                    if (file_exists($csvFile)) {
                        // Buka file CSV
                        $file = fopen($csvFile, 'r');
                    
                        // Mulai tabel HTML
                        echo '<div class="table-responsive">';
                        echo '<table id="dataTable" class="table table-bordered">'; // Added id="dataTable"

                        // Handle the header row
                        if (($header = fgetcsv($file)) !== false) {
                            echo '<thead><tr>';
                            foreach ($header as $cell) {
                                echo '<th>' . htmlspecialchars($cell) . '</th>';
                            }
                            echo '</tr></thead>';
                        }
                    
                        // Handle the data rows
                        echo '<tbody>';
                        while (($data = fgetcsv($file)) !== false) {
                            echo '<tr>';
                            foreach ($data as $cell) {
                                echo '<td>' . htmlspecialchars($cell) . '</td>';
                            }
                            echo '</tr>';
                        }
                        echo '</tbody>';
                    
                        // Tutup file CSV
                        fclose($file);
                    
                        // Selesai dengan tabel HTML
                        echo '</table>';
                        echo '</div>';
                    } else {
                        // Tampilkan pesan jika file tidak ada
                        echo 'Data tidak ditemukan.';
                    }
                    ?>
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
    </div>
    <!-- END wrapper -->

    <?php include 'scripts.php' ?>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.datatables.net/1.10.25/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
    <script>
    $(document).ready(function() {
        $('#dataTable').DataTable();
    });
    </script>
</body>

</html>