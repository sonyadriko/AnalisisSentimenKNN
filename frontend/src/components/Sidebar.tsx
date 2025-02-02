import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { Menu } from "lucide-react";
import { Link } from "react-router-dom";

const Sidebar = () => {
  return (
    <Sheet>
      {/* Toggle Button */}
      <SheetTrigger className="md:hidden p-2 rounded-md bg-gray-900 text-white fixed top-4 left-4 z-50">
        <Menu size={20} />
      </SheetTrigger>

      {/* Sidebar */}
      <SheetContent side="left" className="w-64 bg-gray-900 text-white p-6">
        <h2 className="text-xl font-bold">KNN</h2>
        <nav className="mt-4 space-y-4">
          <Link to="/" className="block hover:text-gray-400">
            Dashboard
          </Link>
          <Link to="/data-training" className="block hover:text-gray-400">
            Data Training
          </Link>
          <Link to="/preprocessing" className="block hover:text-gray-400">
            Preprocessing
          </Link>
          <Link to="/tf-idf" className="block hover:text-gray-400">
            TF-IDF
          </Link>
          <Link to="/pengujian" className="block hover:text-gray-400">
            Pengujian
          </Link>
          <Link to="/evaluasi" className="block hover:text-gray-400">
            Evaluasi
          </Link>
        </nav>
      </SheetContent>

      {/* Sidebar tetap tampil di desktop */}
      <div className="hidden md:block w-64 bg-gray-900 text-white p-6 min-h-screen">
        <h2 className="text-xl font-bold">KNN</h2>
        <nav className="mt-4 space-y-4">
          <Link to="/" className="block hover:text-gray-400">
            Dashboard
          </Link>
          <Link to="/data-training" className="block hover:text-gray-400">
            Data Training
          </Link>
          <Link to="/preprocessing" className="block hover:text-gray-400">
            Preprocessing
          </Link>
          <Link to="/tf-idf" className="block hover:text-gray-400">
            TF-IDF
          </Link>
          <Link to="/pengujian" className="block hover:text-gray-400">
            Pengujian
          </Link>
          <Link to="/evaluasi" className="block hover:text-gray-400">
            Evaluasi
          </Link>
        </nav>
      </div>
    </Sheet>
  );
};

export default Sidebar;
