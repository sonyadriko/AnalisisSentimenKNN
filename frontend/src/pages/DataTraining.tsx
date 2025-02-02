// DataTraining.tsx
import React, { useEffect, useState } from 'react';
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from '@tanstack/react-table';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';

// Definisikan tipe data untuk tabel
type DataTraining = {
  id: number;
  rawContent: string;
  status: string;
};

const DataTraining: React.FC = () => {
  const [data, setData] = useState<DataTraining[]>([]);
  const [positifCount, setPositifCount] = useState<number>(0);
  const [negatifCount, setNegatifCount] = useState<number>(0);

  // Fetch data dari API
  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/data-training')
      .then((response) => response.json())
      .then((responseData) => {
        setData(responseData.data);
        setPositifCount(responseData.positif_count);
        setNegatifCount(responseData.negatif_count);
      })
      .catch((error) => console.error('Error fetching data:', error));
  }, []);

  // Definisikan kolom tabel
  const columns: ColumnDef<DataTraining>[] = [
    {
      accessorKey: 'id',
      header: 'No.',
      cell: (info) => info.row.index + 1, // Menampilkan nomor urut
    },
    {
      accessorKey: 'rawContent',
      header: 'Data',
    },
    {
      accessorKey: 'status',
      header: 'Status',
    },
  ];

  // Inisialisasi tabel dengan TanStack Table
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  const handleFileUpload = (event: React.FormEvent) => {
    event.preventDefault();
    const formData = new FormData();
    const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement;

    if (fileInput && fileInput.files) {
      formData.append('excelFile', fileInput.files[0]);

      fetch('http://127.0.0.1:5000/api/upload', {
        method: 'POST',
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          console.log('File uploaded successfully:', data);
        })
        .catch((error) => console.error('Error uploading file:', error));
    }
  };

  return (
    <div className="container mx-auto p-4">
      <Card>
        <CardHeader>
          <CardTitle>Data Training</CardTitle>
          <CardDescription>Unggah file Excel untuk memproses data training.</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleFileUpload} className="space-y-4">
            <div>
              <label htmlFor="excelFile" className="block text-sm font-medium text-gray-700">
                Unggah File Excel:
              </label>
              <Input type="file" id="excelFile" accept=".csv" />
            </div>
            <Button type="submit">Unggah</Button>
          </form>
        </CardContent>
      </Card>

      <Card className="mt-6">
        <CardHeader>
          <CardTitle>Data Training</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <h5>Positive Count: <span>{positifCount}</span></h5>
            </div>
            <div>
              <h5>Negative Count: <span>{negatifCount}</span></h5>
            </div>
          </div>
          <Table>
            <TableHeader>
              {table.getHeaderGroups().map((headerGroup) => (
                <TableRow key={headerGroup.id}>
                  {headerGroup.headers.map((header) => (
                    <TableHead key={header.id}>
                      {flexRender(
                        header.column.columnDef.header,
                        header.getContext()
                      )}
                    </TableHead>
                  ))}
                </TableRow>
              ))}
            </TableHeader>
            <TableBody>
              {table.getRowModel().rows.map((row) => (
                <TableRow key={row.id}>
                  {row.getVisibleCells().map((cell) => (
                    <TableCell key={cell.id}>
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext()
                      )}
                    </TableCell>
                  ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
};

export default DataTraining;