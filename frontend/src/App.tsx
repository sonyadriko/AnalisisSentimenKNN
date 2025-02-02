import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Topbar from "./components/Topbar";
import Dashboard from "./pages/Dashboard";
import { ThemeProvider } from "@/components/ui/theme-provider";
import DataTraining from "./pages/DataTraining";
import Preprocessing from "./pages/Preprocessing";
import TFIDF from "./pages/TFIDF";
import Pengujian from "./pages/Pengujian";
import Evaluate from "./pages/Evaluate";

function App() {
  return (
    <ThemeProvider defaultTheme="light" storageKey="vite-ui-theme">
      <Router>
        <div className="min-h-screen flex flex-col">
          {/* Topbar */}
          <Topbar />

          {/* Content */}
          <main className="flex-1 pt-16 p-6">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/data-training" element={<DataTraining />} />
              <Route path="/preprocessing" element={<Preprocessing />} />
              <Route path="/tf-idf" element={<TFIDF />} />
              <Route path="/pengujian" element={<Pengujian />} />
              <Route path="/evaluate" element={<Evaluate />} />
            </Routes>
          </main>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;
