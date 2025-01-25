<!DOCTYPE html>
<html lang="en">

<head>
    <title>Dashboard</title>
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
    <!-- Include Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

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
                            <h4 class="fs-18 fw-semibold m-0">Dashboard</h4>
                        </div>
                    </div>
                    <div class="row">
                        <div class="row">
                            <div class="col-md-12">
                                <div class="container">
                                    <h2>Data Chart Sentimen Tweet</h2>
                                    <canvas id="myChart" width="400" height="400"></canvas>
                                </div>
                            </div>

                        </div>
                    </div> <!-- container-fluid -->
                </div> <!-- content -->
                <!-- Footer Start -->
                <?php include 'footer.php'?>
                <!-- end Footer -->

            </div>

        </div>
        <!-- END wrapper -->

        <?php include 'scripts.php' ?>
        <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Ambil data dari endpoint /data-chart
            axios.get('http://127.0.0.1:5000/data-chart')
                .then(response => {
                    const data = response.data;

                    // Buat array untuk label dan data grafik
                    const labels = ['Positif', 'Negatif'];
                    const values = [data.positif, data.negatif];

                    // Buat grafik menggunakan Chart.js
                    const ctx = document.getElementById('myChart').getContext('2d');
                    const myChart = new Chart(ctx, {
                        type: 'bar',
                        data: {
                            labels: labels,
                            datasets: [{
                                label: 'Jumlah',
                                data: values,
                                backgroundColor: [
                                    'rgba(54, 162, 235, 0.2)', // Warna untuk Positif
                                    'rgba(255, 99, 132, 0.2)' // Warna untuk Negatif
                                ],
                                borderColor: [
                                    'rgba(54, 162, 235, 1)',
                                    'rgba(255, 99, 132, 1)'
                                ],
                                borderWidth: 1
                            }]
                        },
                        options: {
                            scales: {
                                y: {
                                    beginAtZero: true
                                }
                            }
                        }
                    });
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                    alert('Terjadi kesalahan saat mengambil data.');
                });
        });
        </script>
</body>

</html>