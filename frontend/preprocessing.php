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
                            <h4 class="fs-18 fw-semibold m-0">Data Training</h4>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-12 col-xl-12">
                            <div class="card">
                                <div class="card-body">
                                    <div class="row">
                                        <div class="table-responsive">
                                            <table id="dataTable" class="table" border="1">
                                                <thead>
                                                    <tr>
                                                        <th>ID</th>
                                                        <th>Case Folding</th>
                                                        <th>Cleaning</th>
                                                        <th>Tokenizing</th>
                                                        <th>Stopword</th>
                                                        <th>Normalisasi</th>
                                                        <th>Stemming</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    <?php
$file_path = '../backend/Text_Preprocessing.csv';

// Cek apakah file CSV ada
if (!file_exists($file_path)) {
    echo 'File CSV tidak ditemukan.';
} else {
    // Mengambil data hasil preprocessing dari file CSV
    $preprocessing_data = array_map('str_getcsv', file($file_path));

    // Jika file kosong atau gagal dibaca
    if ($preprocessing_data === FALSE || count($preprocessing_data) === 0) {
        echo 'Data tidak ditemukan atau file CSV kosong.';
    } else {
        // Mengabaikan baris header
        array_shift($preprocessing_data);

        // Menampilkan data dalam tabel
        foreach ($preprocessing_data as $row) {
            echo '<tr>';
            echo '<td>' . (isset($row[0]) ? $row[0] : '') . '</td>';
            echo '<td>' . (isset($row[2]) ? $row[2] : '') . '</td>';
            echo '<td>' . (isset($row[3]) ? $row[3] : '') . '</td>';
            echo '<td>' . (isset($row[4]) ? $row[4] : '') . '</td>';
            echo '<td>' . (isset($row[6]) ? $row[6] : '') . '</td>';
            echo '<td>' . (isset($row[7]) ? $row[7] : '') . '</td>';
            echo '<td>' . (isset($row[8]) ? $row[8] : '') . '</td>';
            echo '</tr>';
        }
    }
}
?>
                                                </tbody>
                                            </table>
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