import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, Link } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Explore from './pages/Explore';
import AnimalDetails from './pages/AnimalDetails';
import AskKnowledgeGraph from './pages/AskKnowledgeGraph';

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900 selection:bg-emerald-100 selection:text-emerald-900">
        <Navbar />

        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 pb-12">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/explore" element={<Explore />} />
            <Route path="/animals/:animal_id" element={<AnimalDetails />} />
            <Route path="/ask" element={<AskKnowledgeGraph />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>

        <footer className="bg-white border-t border-slate-200 py-6 mt-auto">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-3">
            <div className="flex items-center space-x-2">
              <span className="font-semibold text-slate-800">🐾 Animal Kingdom Knowledge Graph</span>
              <span>•</span>
              <span>FastAPI & Neo4j Academic Demonstration</span>
            </div>
            <div className="flex items-center space-x-4">
              <Link to="/" className="hover:text-emerald-600 transition-colors">Home</Link>
              <Link to="/explore" className="hover:text-emerald-600 transition-colors">Explore</Link>
              <Link to="/ask" className="hover:text-emerald-600 transition-colors">Ask Graph</Link>
            </div>
          </div>
        </footer>
      </div>
    </BrowserRouter>
  );
}
