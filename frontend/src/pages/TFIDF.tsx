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
import { useToast } from "@/hooks/use-toast"; // Toast component

type TFIDFData = {
  [key: string]: number | string; // Allowing dynamic keys (terms and values)
};

const TFIDF: React.FC = () => {
  const [data, setData] = useState<TFIDFData[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const { toast } = useToast();

  // Fetch data from the TF-IDF API
  const fetchTFIDFData = async () => {
    setLoading(true);
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/data-tfidf');
      setData(response.data.data); // Adjust according to the API response structure
    } catch (error) {
      console.error('Error fetching TF-IDF data:', error);
      toast({
        title: 'Error',
        description: 'Failed to fetch TF-IDF data.',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  // Fetch data on mount
  useEffect(() => {
    fetchTFIDFData();
  }, []);

  // Get columns from the first data entry (keys of the first object)
  const columns = data.length > 0 ? Object.keys(data[0]) : [];

  return (
    <div className="container mx-auto p-4">
      <Card>
        <CardHeader>
          <CardTitle>TF-IDF Data</CardTitle>
          <CardDescription>
            This table shows the TF-IDF values for different terms in each document.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Button onClick={fetchTFIDFData} disabled={loading}>
            {loading ? 'Loading...' : 'Reload Data'}
          </Button>
        </CardContent>
      </Card>

      <Card className="mt-6">
        <CardHeader>
          <CardTitle>TF-IDF Results</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                {columns.map((column, index) => (
                  <TableHead key={index}>{column}</TableHead>
                ))}
              </TableRow>
            </TableHeader>
            <TableBody>
              {data.length > 0 ? (
                data.map((row, index) => (
                  <TableRow key={index}>
                    {columns.map((column, idx) => (
                      <TableCell key={idx}>{row[column]}</TableCell>
                    ))}
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={columns.length} className="text-center">
                    No data available.
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

export default TFIDF;
