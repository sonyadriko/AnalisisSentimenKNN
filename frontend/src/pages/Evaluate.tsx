import React, { useState } from 'react';
import axios from 'axios';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Table, TableHeader, TableBody, TableRow, TableCell } from '@/components/ui/table';
import { Progress } from '@/components/ui/progress';
import { useToast } from "@/hooks/use-toast"; // Toast component

const Evaluate: React.FC = () => {
  const { toast } = useToast();
  const [loading, setLoading] = useState<boolean>(false);
  const [progress, setProgress] = useState<number>(0);
  const [metrics, setMetrics] = useState<any>(null);

  const calculateConfusionMatrix = async () => {
    setLoading(true);
    setProgress(0);

    // Simulate progress loading
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev < 100) return prev + 10;
        clearInterval(interval);
        return 100;
      });
    }, 200);

    try {
      const response = await axios.post(
        'http://127.0.0.1:5000/api/metrics/',
        {}, // body is empty, can add if necessary
        {
          headers: {
            'Content-Type': 'application/json', // Ensure proper content-type
          },
        }
      );
      
      setMetrics(response.data);
      setProgress(100);

      toast({
        title: 'Perhitungan selesai',
        description: 'Confusion Matrix dan metrik berhasil dihitung!',
        variant: 'success',
      });
    } catch (error) {
      setProgress(100);

      toast({
        title: 'Error',
        description: 'Terjadi kesalahan saat menghitung Confusion Matrix dan metrik.',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <Card>
        <CardHeader>
          <CardTitle>Evaluasi</CardTitle>
        </CardHeader>
        <CardContent>
          <Button onClick={calculateConfusionMatrix} disabled={loading}>
            Hitung Confusion Matrix
          </Button>

          {loading && (
            <div className="mt-4">
              <Progress value={progress} />
            </div>
          )}

          {metrics && (
            <>
              <div id="confusionMatrixResults" className="mt-6">
                <h5>Confusion Matrix:</h5>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableCell></TableCell>
                      <TableCell>Predicted Positif</TableCell>
                      <TableCell>Predicted Negatif</TableCell>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    <TableRow>
                      <TableCell>Actual Positif</TableCell>
                      <TableCell>{metrics.confusion_matrix[1][1]}</TableCell>
                      <TableCell>{metrics.confusion_matrix[1][0]}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>Actual Negatif</TableCell>
                      <TableCell>{metrics.confusion_matrix[0][1]}</TableCell>
                      <TableCell>{metrics.confusion_matrix[0][0]}</TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </div>

              <div id="metricsResults" className="mt-6">
                <h5>Metrics:</h5>
                <ul className="list-disc pl-6">
                  <li>Accuracy: <strong>{metrics.accuracy.toFixed(2)}</strong></li>
                  <li>Precision: <strong>{metrics.precision.toFixed(2)}</strong></li>
                  <li>Recall: <strong>{metrics.recall.toFixed(2)}</strong></li>
                  <li>F1 Score: <strong>{metrics.f1_score.toFixed(2)}</strong></li>
                </ul>
              </div>
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default Evaluate;
