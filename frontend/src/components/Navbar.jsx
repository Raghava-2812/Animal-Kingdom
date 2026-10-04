import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Network, Search, HelpCircle, Database, CheckCircle2, AlertCircle } from 'lucide-react';
import { api } from '../services/api';

export default function Navbar() {
  const location = useLocation();
  const [health, setHealth] = useState({ neo4jConnected: false, loading: true });

  useEffect(() => {
    api.getHealth()
      .then((data) => setHealth({ neo4jConnected: data.neo4jConnected, loading: false }))
      .catch(() => setHealth({ neo4jConnected: false, loading: false }));
  }, []);

  const navLinks = [
    { to: '/', label: 'Home', icon: Network },
    { to: '/explore', label: 'Explore Animals', icon: Search },
    { to: '/ask', label: 'Ask Knowledge Graph', icon: HelpCircle },
  ];

  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200 shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Academic Title */}
          <Link to="/" className="flex items-center space-x-3 group">
            <span className="text-2xl p-2 rounded-xl bg-emerald-50 border border-emerald-200 group-hover:scale-105 transition-transform">
              🐾
            </span>
            <div>
              <span className="font-bold text-lg text-slate-900 tracking-tight block">
                Animal Kingdom <span className="text-emerald-600">Knowledge Graph</span>
              </span>
              <span className="text-xs text-slate-500 font-medium block">
                Academic Graph Intelligence & Cypher Engine
              </span>
            </div>
          </Link>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center space-x-1">
            {navLinks.map(({ to, label, icon: Icon }) => {
              const isActive = location.pathname === to;
              return (
                <Link
                  key={to}
                  to={to}
                  className={`flex items-center space-x-2 px-3.5 py-2 rounded-lg text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-emerald-50 text-emerald-700 font-semibold'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/80'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-emerald-600' : 'text-slate-400'}`} />
                  <span>{label}</span>
                </Link>
              );
            })}
          </nav>

          {/* Database Connectivity Badge */}
          <div className="flex items-center space-x-2">
            <div
              className={`flex items-center space-x-1.5 px-2.5 py-1 rounded-full text-xs font-medium border ${
                health.neo4jConnected
                  ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                  : 'bg-amber-50 text-amber-800 border-amber-200'
              }`}
              title={
                health.neo4jConnected
                  ? 'Active Neo4j Driver Connection Established'
                  : 'Neo4j offline - running in high-availability dataset mode'
              }
            >
              <Database className="w-3.5 h-3.5" />
              <span>{health.neo4jConnected ? 'Neo4j Active' : 'Graph Engine Ready'}</span>
              <span
                className={`w-2 h-2 rounded-full ${
                  health.neo4jConnected ? 'bg-emerald-500 animate-pulse' : 'bg-amber-500'
                }`}
              />
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
