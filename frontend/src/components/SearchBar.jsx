/**
 * Animal Search Bar Component.
 *
 * Provides a responsive text input for instant keyword and taxonomic searching:
 * - Magnifying glass icon indicator.
 * - Clear button ('X') that appears dynamically when query text is non-empty.
 * - Form submit handler to trigger search operations on Enter key or button click.
 *
 * Props:
 * @param {string} props.value - Controlled input string.
 * @param {Function} props.onChange - Input change callback: (newValue) => void.
 * @param {Function} [props.onSearch] - Search submit callback: (query) => void.
 * @param {string} [props.placeholder] - Custom placeholder text.
 */

import React from 'react';
import { Search, X } from 'lucide-react';

export default function SearchBar({
  value,
  onChange,
  onSearch,
  placeholder = "Search by animal name or scientific name (e.g. Tiger, Panthera leo)..."
}) {
  const handleSubmit = (e) => {
    e.preventDefault();
    if (onSearch) onSearch(value);
  };

  return (
    <form onSubmit={handleSubmit} className="relative w-full">
      <div className="relative flex items-center">
        {/* Leading Search Icon */}
        <Search className="absolute left-4 w-5 h-5 text-slate-400 pointer-events-none" />

        {/* Search Input Field */}
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          className="w-full pl-12 pr-24 py-3 bg-white rounded-xl border border-slate-300 text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 text-sm shadow-xs transition-all"
        />

        {/* Right-aligned Actions: Clear Button & Search Submit Button */}
        <div className="absolute right-2 flex items-center space-x-1">
          {value && (
            <button
              type="button"
              onClick={() => onChange('')}
              className="p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100 transition-colors cursor-pointer"
              title="Clear search"
            >
              <X className="w-4 h-4" />
            </button>
          )}
          <button
            type="submit"
            className="px-3.5 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold rounded-lg shadow-xs transition-colors cursor-pointer"
          >
            Search
          </button>
        </div>
      </div>
    </form>
  );
}
