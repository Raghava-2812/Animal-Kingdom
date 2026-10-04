import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { Search, Filter, AlertCircle, RefreshCw } from 'lucide-react';
import { api } from '../services/api';
import SearchBar from '../components/SearchBar';
import FilterPanel from '../components/FilterPanel';
import AnimalCard from '../components/AnimalCard';

export default function Explore() {
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();

  const [searchQuery, setSearchQuery] = useState(searchParams.get('q') || '');
  const [filters, setFilters] = useState({
    class: searchParams.get('class') || '',
    habitat: searchParams.get('habitat') || '',
    diet: searchParams.get('diet') || '',
    status: searchParams.get('status') || '',
    continent: searchParams.get('continent') || '',
  });

  const [animals, setAnimals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Sync URL search params with state
  useEffect(() => {
    const classParam = searchParams.get('class') || '';
    const habitatParam = searchParams.get('habitat') || '';
    const dietParam = searchParams.get('diet') || '';
    const statusParam = searchParams.get('status') || '';
    const continentParam = searchParams.get('continent') || '';
    const qParam = searchParams.get('q') || '';

    setFilters({
      class: classParam,
      habitat: habitatParam,
      diet: dietParam,
      status: statusParam,
      continent: continentParam,
    });
    setSearchQuery(qParam);
  }, [searchParams]);

  // Fetch animals whenever query or filters change
  useEffect(() => {
    setLoading(true);
    setError(null);

    if (searchQuery.trim()) {
      api.search(searchQuery)
        .then((data) => {
          setAnimals(data);
          setLoading(false);
        })
        .catch((err) => {
          setError(err.message);
          setLoading(false);
        });
    } else {
      api.getAnimals(filters)
        .then((data) => {
          setAnimals(data);
          setLoading(false);
        })
        .catch((err) => {
          setError(err.message);
          setLoading(false);
        });
    }
  }, [searchQuery, filters]);

  const handleFilterChange = (key, value) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    // Update URL params
    const params = new URLSearchParams();
    Object.entries(newFilters).forEach(([k, v]) => {
      if (v) params.set(k, v);
    });
    if (searchQuery) params.set('q', searchQuery);
    setSearchParams(params);
  };

  const handleResetFilters = () => {
    const emptyFilters = { class: '', habitat: '', diet: '', status: '', continent: '' };
    setFilters(emptyFilters);
    setSearchQuery('');
    setSearchParams(new URLSearchParams());
  };

  const handleSearchSubmit = (val) => {
    setSearchQuery(val);
    const params = new URLSearchParams();
    if (val) params.set('q', val);
    setSearchParams(params);
  };

  return (
    <div className="space-y-6 py-4">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          Explore Animals
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">
          Search the Knowledge Graph across species, taxonomy, habitats, feeding strategies, and conservation classifications.
        </p>
      </div>

      {/* Search Bar */}
      <SearchBar
        value={searchQuery}
        onChange={(val) => {
          setSearchQuery(val);
          if (!val) {
            const params = new URLSearchParams(searchParams);
            params.delete('q');
            setSearchParams(params);
          }
        }}
        onSearch={handleSearchSubmit}
      />

      {/* Multi-Facet Filter Panel */}
      <FilterPanel
        filters={filters}
        onFilterChange={handleFilterChange}
        onReset={handleResetFilters}
      />

      {/* Active Results Summary */}
      <div className="flex items-center justify-between pt-2">
        <p className="text-xs font-bold uppercase tracking-wider text-slate-500">
          Showing {animals.length} {animals.length === 1 ? 'Animal' : 'Animals'}
        </p>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="bg-white rounded-2xl border border-slate-200/80 p-16 text-center shadow-xs">
          <div className="w-9 h-9 border-3 border-emerald-600 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
          <p className="text-xs font-semibold text-slate-600">Querying Knowledge Graph...</p>
        </div>
      )}

      {/* Error State */}
      {error && !loading && (
        <div className="bg-rose-50 border border-rose-200 rounded-2xl p-6 text-center text-rose-800">
          <AlertCircle className="w-8 h-8 mx-auto mb-2 text-rose-500" />
          <h3 className="text-sm font-bold">Failed to load animals</h3>
          <p className="text-xs mt-1 text-rose-600">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="mt-3 inline-flex items-center space-x-1 px-3 py-1.5 bg-rose-600 text-white text-xs font-semibold rounded-lg hover:bg-rose-700 transition-colors"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Try Again</span>
          </button>
        </div>
      )}

      {/* Empty State */}
      {!loading && !error && animals.length === 0 && (
        <div className="bg-white rounded-2xl border border-slate-200/80 p-12 text-center shadow-xs">
          <Search className="w-10 h-10 text-slate-300 mx-auto mb-3" />
          <h3 className="text-base font-bold text-slate-800">No animals found</h3>
          <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
            No animal entities matched the current search or filter combination in the Knowledge Graph.
          </p>
          <button
            onClick={handleResetFilters}
            className="mt-4 px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold rounded-lg transition-colors"
          >
            Reset Filters
          </button>
        </div>
      )}

      {/* Animal Grid */}
      {!loading && !error && animals.length > 0 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {animals.map((animal) => (
            <AnimalCard
              key={animal.id}
              animal={animal}
              onExploreGraph={(id) => navigate(`/animals/${id}?tab=graph`)}
            />
          ))}
        </div>
      )}
    </div>
  );
}
