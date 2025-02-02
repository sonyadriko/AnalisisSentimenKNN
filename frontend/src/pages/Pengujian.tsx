import React, { useState } from 'react';
import axios from 'axios';
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Input } from '@/components/ui/input';
import { useToast } from "@/hooks/use-toast"; // Toast component
import { Progress } from '@/components/ui/progress';

const Pengujian: React.FC = () => {
  const [inputText, setInputText] = useState<string>('');
  const [kValue, setKValue] = useState<number>(1);
  const [preprocessedText, setPreprocessedText] = useState<string>('');
  const [sentiment, setSentiment] = useState<string>('');
  const [similarTexts, setSimilarTexts] = useState<string[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [progress, setProgress] = useState<number>(0); // Track progress
  const { toast } = useToast();

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    // Validate input
    if (!inputText.trim()) {
      toast({
        title: 'Input Error',
        description: 'Please enter some text.',
        variant: 'destructive',
      });
      return;
    }

    if (kValue <= 0) {
      toast({
        title: 'Input Error',
        description: 'Please enter a valid positive number for k.',
        variant: 'destructive',
      });
      return;
    }

    setLoading(true);
    setProgress(0); // Reset progress
    try {
      // Simulate progress for loading
      const interval = setInterval(() => {
        setProgress((prev) => {
          if (prev < 100) return prev + 10;
          clearInterval(interval);
          return 100;
        });
      }, 200);

      const response = await axios.post('http://127.0.0.1:5000/api/knn', {
        text: inputText,
        k: kValue,
      });

      // Stop progress bar
      clearInterval(interval);
      setProgress(100);

      // Display results
      setPreprocessedText(response.data.preprocess_text);
      setSentiment(response.data.sentiment);
      setSimilarTexts(response.data.results.map((result: any) => `Rank: ${result.rank} - Similarity: ${result.similarity.toFixed(2)} - Text: ${result.text}`));
    } catch (error) {
      setProgress(100);
      toast({
        title: 'Error',
        description: 'An error occurred while processing the request.',
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
          <CardTitle>Pengujian Analisis Sentimen</CardTitle>
          <CardDescription>
            Lakukan pengujian analisis sentimen dengan memasukkan komentar dan nilai k untuk proses KNN.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label htmlFor="inputText" className="block text-sm font-medium text-gray-700">
                Komentar atau Ulasan
              </label>
              <Textarea
                id="inputText"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                rows={4}
                placeholder="Masukkan teks di sini..."
                required
              />
            </div>
            <div className="mb-4">
              <label htmlFor="kValue" className="block text-sm font-medium text-gray-700">
                Jumlah (k)
              </label>
              <Input
                type="number"
                id="kValue"
                value={kValue}
                onChange={(e) => setKValue(Number(e.target.value))}
                placeholder="Masukkan nilai k"
                min="1"
                required
              />
            </div>
            <Button type="submit" disabled={loading} >
              Submit
            </Button>
          </form>

          {loading && (
            <div className="mt-4">
              <Progress value={progress} />
            </div>
          )}
        </CardContent>
      </Card>

      <Card className="mt-6">
        <CardHeader>
          <CardTitle>Hasil Pengujian</CardTitle>
        </CardHeader>
        <CardContent>
          <p><strong>Preprocessing Text:</strong> <span>{preprocessedText}</span></p>
          <p><strong>Sentiment:</strong> <span>{sentiment}</span></p>
          <ul>
            {similarTexts.length > 0 ? (
              similarTexts.map((text, index) => (
                <li key={index} className="bg-gray-100 p-2 rounded mb-2 border">
                  {text}
                </li>
              ))
            ) : (
              <li className="text-gray-500">No similar texts found.</li>
            )}
          </ul>
        </CardContent>
      </Card>
    </div>
  );
};

export default Pengujian;
