import { Link } from "react-router-dom";
import { useTheme } from "@/components/ui/theme-provider";
import { Button } from "@/components/ui/button";
import { Sun, Moon } from "lucide-react";

const Topbar = () => {
  const { theme, setTheme } = useTheme();

  return (
    <header className="fixed top-0 left-0 w-full bg-gray-900 text-white p-4 flex items-center justify-between shadow-md z-50">
      {/* Logo / Nama */}
      <h1 className="text-xl font-bold ml-5">KNN</h1>

      {/* Menu Navigasi */}
      <nav className="hidden md:flex space-x-6">
        <Link to="/" className="hover:text-gray-400">
          Dashboard
        </Link>
        <Link to="/data-training" className="hover:text-gray-400">
          Data Training
        </Link>
        <Link to="/preprocessing" className="hover:text-gray-400">
          Preprocessing
        </Link>
        <Link to="/tf-idf" className="hover:text-gray-400">
          TF-IDF
        </Link>
        <Link to="/pengujian" className="hover:text-gray-400">
          Pengujian
        </Link>
        <Link to="/evaluate" className="hover:text-gray-400">
          Evaluasi
        </Link>
      </nav>

      {/* Toggle Dark Mode */}
      <Button
        variant="ghost"
        size="icon"
        onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
      >
        {theme === "dark" ? <Sun size={20} /> : <Moon size={20} />}
      </Button>
    </header>
  );
};

export default Topbar;
