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
                        <div class="card">
                            <div class="card-body">
                                <div class="flex mt-6">
                                    <form action="data-training.php" method="post" enctype="multipart/form-data"
                                        class="shadow-md rounded px-8 pt-6 pb-8">
                                        <label for="excelFile" class="text-gray-700 text-sm font-bold mb-2">Unggah
                                            File
                                            Excel:</label>
                                        <input type="file" name="excelFile" id="excelFile" accept=".csv"
                                            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
                                        <button type="submit" class="btn btn-primary mt-6">Unggah</button>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                    <?php
                    if (isset($_FILES['excelFile'])) {
                        $errors = [];
                        $file_name = 'data_tweet.csv';
                        $file_tmp = $_FILES['excelFile']['tmp_name'];
                        $upload_path = '../backend/' . $file_name;
                        $file_extension = pathinfo($_FILES['excelFile']['name'], PATHINFO_EXTENSION);

                        if ($_FILES['excelFile']['error'] !== UPLOAD_ERR_OK) {
                            $errors[] = 'An error occurred during file upload.';
                        } elseif ($file_extension != 'csv') {
                            $errors[] = 'Only CSV files are allowed.';
                            error_log('Invalid file format. Only CSV files are allowed.');
                        } else {
                            if (move_uploaded_file($file_tmp, $upload_path)) {
                                echo "<script>Swal.fire({
                                        icon: 'success',
                                        title: 'File uploaded successfully!',
                                        showConfirmButton: false,
                                        timer: 1500
                                    })</script>";
                                error_log('File uploaded: ' . $file_name);
                            } else {
                                $errors[] = 'Failed to upload file.';
                                error_log('Failed to upload file: ' . $file_name);
                            }
                        }

                        if (!empty($errors)) {
                            foreach ($errors as $error) {
                                echo "<script>Swal.fire({
                                        icon: 'error',
                                        title: 'Error!',
                                        text: '$error',
                                    })</script>";
                            }
                        }
                    }
                    ?>
                    <div class="row">
                        <div class="col-md-12 col-xl-12">
                            <div class="card">
                                <div class="card-body">
                                    <div class="row">
                                        <div class="row">
                                            <div class="col-md-6">
                                                <h5>Positive Count: <span id="positifCount">0</span></h5>
                                            </div>
                                            <div class="col-md-6">
                                                <h5>Negative Count: <span id="negatifCount">0</span></h5>
                                            </div>
                                        </div>

                                        <table id='dataTable' class='table table-bordered'>
                                            <thead>
                                                <tr>
                                                    <th>No.</th>
                                                    <th>Data</th>
                                                    <th>Status</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                            </tbody>
                                        </table>
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

    <script>
    document.addEventListener('DOMContentLoaded', function() {
        fetch('http://127.0.0.1:5000/data-training')
            .then(response => response.json())
            .then(responseData => {
                const data = responseData.data;
                const positifCount = responseData.positif_count;
                const negatifCount = responseData.negatif_count;

                document.getElementById('positifCount').textContent = positifCount;
                document.getElementById('negatifCount').textContent = negatifCount;

                const tableBody = document.querySelector('#dataTable tbody');
                data.forEach((item, index) => {
                    const row = document.createElement('tr');
                    const cellIndex = document.createElement('td');
                    const cellData = document.createElement('td');
                    const cellStatus = document.createElement('td');

                    cellIndex.textContent = index + 1;
                    cellData.textContent = item.rawContent;
                    cellStatus.textContent = item.status;

                    row.appendChild(cellIndex);
                    row.appendChild(cellData);
                    row.appendChild(cellStatus);
                    tableBody.appendChild(row);
                });

                // Initialize DataTables
                $('#dataTable').DataTable();
            })
            .catch(error => console.error('Error fetching data:', error));
    });
    </script>
</body>

</html>