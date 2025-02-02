import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const Dashboard = () => {
  return (
    <div className="container mx-auto p-4">
      <div className="grid gap-6">
        {/* K Nearest Neighbor Card */}
        <Card>
          <CardHeader>
            <CardTitle>K Nearest Neighbor</CardTitle>
          </CardHeader>
          <CardContent>
            <p>
              K Nearest Neighbor (KNN) adalah algoritma machine learning untuk klasifikasi dan regresi. 
              Algoritma ini mencari data terdekat (<i>k neighbors</i>) untuk melakukan prediksi.
            </p>
            <p className="mt-2">
              KNN mudah diimplementasikan, tetapi performanya bergantung pada jumlah tetangga 
              (<i>k</i>) dan ukuran dataset.
            </p>
          </CardContent>
        </Card>

        {/* Get Contact Card */}
        <Card>
          <CardHeader>
            <CardTitle>Get Contact</CardTitle>
          </CardHeader>
          <CardContent>
            <p>
              <i>Get Contact</i> adalah aplikasi yang membantu pengguna mengenali nomor telepon tak dikenal.
            </p>
            <p className="mt-2">
              Aplikasi ini dapat memblokir panggilan spam dan menunjukkan bagaimana kontak disimpan oleh orang lain.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;
