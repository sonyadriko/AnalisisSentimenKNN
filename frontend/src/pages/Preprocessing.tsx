import React, { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import axios from 'axios';
import { useToast } from "@/hooks/use-toast";
import { Progress } from '@/components/ui/progress'; // Import Progress from shadcn

type PreprocessingData = {
  id: string;
  caseFolding: string;
  cleaning: string;
  tokenizing: string;
  stopword: string;
  normalized: string;
  stemmed: string;
};

const Preprocessing: React.FC = () => {
  const [data, setData] = useState<PreprocessingData[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [progress, setProgress] = useState<number>(0); // Progress state
  const { toast } = useToast();

  const fetchPreprocessingData = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/data-preprocessing');
      setData(response.data.data);
    } catch (error) {
      console.error('Error fetching preprocessing data:', error);
      toast({
        title: 'Error',
        description: 'Gagal mengambil data preprocessing.',
        variant: 'destructive',
      });
    }
  };

  const startPreprocessing = async () => {
    setLoading(true);
    setProgress(0); // Reset progress to 0 at the start

    // Simulate progress
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev < 100) {
          return prev + 10; // Increase by 10% every interval
        } else {
          clearInterval(interval); // Clear interval once progress reaches 100%
          return 100;
        }
      });
    }, 500); // Update progress every 500ms

    try {
      // Run preprocessing and TF-IDF
      await axios.get('http://127.0.0.1:5000/api/preprocessing');
      await axios.get('http://127.0.0.1:5000/api/tfidf');

      // Fetch the updated data after processing
      await fetchPreprocessingData();

      toast({
        title: 'Berhasil',
        description: 'Proses preprocessing dan TF-IDF selesai.',
      });
    } catch (error) {
      console.error('Error during preprocessing:', error);
      toast({
        title: 'Error',
        description: 'Terjadi kesalahan saat memproses data.',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPreprocessingData();
  }, []);

  return (
    <div className="container mx-auto p-4">
      <Card>
        <CardHeader>
          <CardTitle>Preprocessing</CardTitle>
          <CardDescription>
            Tekan tombol untuk memulai proses preprocessing dan TF-IDF data training.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Button onClick={startPreprocessing} disabled={loading}>
            {loading ? 'Memproses...' : 'Mulai Proses'}
          </Button>
          {loading && (
            <div className="mt-4">
              <Progress value={progress} max={100} />
              <span className="block mt-2 text-center">{progress}%</span>
            </div>
          )}
        </CardContent>
      </Card>

      <Card className="mt-6">
        <CardHeader>
          <CardTitle>Hasil Preprocessing</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Case Folding</TableHead>
                <TableHead>Cleaning</TableHead>
                <TableHead>Tokenizing</TableHead>
                <TableHead>Stopword</TableHead>
                <TableHead>Normalisasi</TableHead>
                <TableHead>Stemming</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {data.length > 0 ? (
                data.map((row) => (
                  <TableRow key={row.id}>
                    <TableCell>{row.caseFolding}</TableCell>
                    <TableCell>{row.cleaning}</TableCell>
                    <TableCell>{row.tokenizing}</TableCell>
                    <TableCell>{row.stopword}</TableCell>
                    <TableCell>{row.normalized}</TableCell>
                    <TableCell>{row.stemmed}</TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={7} className="text-center">
                    Tidak ada data.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
};

export default Preprocessing;
