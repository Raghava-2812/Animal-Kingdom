import React from 'react';
import { Filter, RotateCcw } from 'lucide-react';

const FILTER_OPTIONS = {
  class: ['Mammal', 'Bird', 'Reptile', 'Amphibian', 'Fish', 'Insect'],
  habitat: ['Forest', 'Grassland', 'Savanna', 'Desert', 'Ocean', 'River', 'Wetland', 'Mountain', 'Polar Tundra'],
  diet: ['Carnivore', 'Herbivore', 'Omnivore', 'Insectivore'],
  status: ['Least Concern', 'Near Threatened', 'Vulnerable', 'Endangered', 'Critically Endangered'],
  continent: ['Asia', 'Africa', 'Europe', 'North America', 'South America', 'Australia', 'Antarctica']
};

export default function FilterPanel({ filters, onFilterChange, onReset }) {
  const activeCount = Object.values(filters).filter(Boolean).length;

  return (
    <div className="bg-white rounded-xl border border-slate-200/80 p-4 shadow-xs">
      <div className="flex items-center justify-between pb-3 mb-3 border-b border-slate-100">
        <div className="flex items-center space-x-2">
          <Filter className="w-4 h-4 text-emerald-600" />
          <span className="text-sm font-bold text-slate-800">Graph Filters</span>
          {activeCount > 0 && (
            <span className="px-2 py-0.5 text-xs font-semibold bg-emerald-100 text-emerald-800 rounded-full">
              {activeCount} active
            </span>
          )}
        </div>
        {activeCount > 0 && (
          <button
            onClick={onReset}
            className="flex items-center space-x-1 text-xs font-medium text-slate-500 hover:text-slate-800 transition-colors"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Reset All</span>
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
        {/* Class Filter */}
        <div>
          <label className="block text-2xs font-bold uppercase tracking-wider text-slate-500 mb-1">
            Taxonomic Class
          </label>
          <select
            value={filters.class || ''}
            onChange={(e) => onFilterChange('class', e.target.value)}
            className="w-full text-xs bg-slate-50 border border-slate-200 rounded-lg p-2 text-slate-800 focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500"
          >
            <option value="">All Classes</option>
            {FILTER_OPTIONS.class.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </div>

        {/* Habitat Filter */}
        <div>
          <label className="block text-2xs font-bold uppercase tracking-wider text-slate-500 mb-1">
            Habitat
          </label>
          <select
            value={filters.habitat || ''}
            onChange={(e) => onFilterChange('habitat', e.target.value)}
            className="w-full text-xs bg-slate-50 border border-slate-200 rounded-lg p-2 text-slate-800 focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500"
          >
            <option value="">All Habitats</option>
            {FILTER_OPTIONS.habitat.map((h) => (
              <option key={h} value={h}>{h}</option>
            ))}
          </select>
        </div>

        {/* Diet Filter */}
        <div>
          <label className="block text-2xs font-bold uppercase tracking-wider text-slate-500 mb-1">
            Dietary Category
          </label>
          <select
            value={filters.diet || ''}
            onChange={(e) => onFilterChange('diet', e.target.value)}
            className="w-full text-xs bg-slate-50 border border-slate-200 rounded-lg p-2 text-slate-800 focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500"
          >
            <option value="">All Diets</option>
            {FILTER_OPTIONS.diet.map((d) => (
              <option key={d} value={d}>{d}</option>
            ))}
          </select>
        </div>

        {/* Conservation Status Filter */}
        <div>
          <label className="block text-2xs font-bold uppercase tracking-wider text-slate-500 mb-1">
            Conservation Status
          </label>
          <select
            value={filters.status || ''}
            onChange={(e) => onFilterChange('status', e.target.value)}
            className="w-full text-xs bg-slate-50 border border-slate-200 rounded-lg p-2 text-slate-800 focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500"
          >
            <option value="">All Statuses</option>
            {FILTER_OPTIONS.status.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </div>

        {/* Continent Filter */}
        <div>
          <label className="block text-2xs font-bold uppercase tracking-wider text-slate-500 mb-1">
            Continent / Region
          </label>
          <select
            value={filters.continent || ''}
            onChange={(e) => onFilterChange('continent', e.target.value)}
            className="w-full text-xs bg-slate-50 border border-slate-200 rounded-lg p-2 text-slate-800 focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500"
          >
            <option value="">All Continents</option>
            {FILTER_OPTIONS.continent.map((ct) => (
              <option key={ct} value={ct}>{ct}</option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
}
