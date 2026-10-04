import React, { useState } from 'react';
import { Terminal, Copy, Check, Filter, Layers, Info } from 'lucide-react';
import AnimalCard from './AnimalCard';

export default function QueryResult({ response, loading, onExploreGraph }) {
  const [copied, setCopied] = useState(false);
  const [showCypher, setShowCypher] = useState(true);

  if (loading) {
    return (
      <div className="bg-white rounded-2xl border border-slate-200/80 p-12 text-center shadow-xs">
        <div className="w-10 h-10 border-3 border-emerald-600 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
        <p className="text-sm font-semibold text-slate-800">Processing graph query via Cypher Engine...</p>
        <p className="text-xs text-slate-400 mt-1">Extracting entities and traversing Neo4j relationships</p>
      </div>
    );
  }

  if (!response) return null;

  const { question, detectedFilters = {}, cypherQuery, results = [], resultCount = 0, explanation } = response;

  const handleCopyCypher = () => {
    navigator.clipboard.writeText(cypherQuery);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      {/* Query Breakdown Header */}
      <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-xs">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-4 border-b border-slate-100">
          <div>
            <span className="text-2xs font-bold uppercase tracking-wider text-slate-400 block mb-0.5">
              Active Question
            </span>
            <h3 className="text-base font-bold text-slate-900">"{question}"</h3>
          </div>
          <div className="flex items-center space-x-2">
            <span className="px-3 py-1 bg-emerald-50 text-emerald-800 border border-emerald-200 rounded-full text-xs font-bold">
              {resultCount} {resultCount === 1 ? 'Animal' : 'Animals'} Found
            </span>
          </div>
        </div>

        {/* Interpreted Constraints & Explanation */}
        <div className="mt-4 flex flex-wrap items-center gap-2">
          <div className="flex items-center text-xs font-semibold text-slate-500 mr-2">
            <Filter className="w-3.5 h-3.5 mr-1 text-emerald-600" />
            Detected Graph Filters:
          </div>
          {Object.keys(detectedFilters).length === 0 ? (
            <span className="text-xs text-slate-400 italic">None (Broad query)</span>
          ) : (
            Object.entries(detectedFilters).map(([key, val]) => (
              <span
                key={key}
                className="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200"
              >
                <strong className="capitalize mr-1">{key}:</strong>{' '}
                {Array.isArray(val) ? val.join(', ') : String(val)}
              </span>
            ))
          )}
        </div>

        {explanation && (
          <div className="mt-3 flex items-start space-x-2 text-xs text-slate-600 bg-slate-50 p-2.5 rounded-lg border border-slate-100">
            <Info className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
            <span>{explanation}</span>
          </div>
        )}
      </div>

      {/* Generated Cypher Section */}
      <div className="bg-slate-950 rounded-2xl border border-slate-800 overflow-hidden shadow-md">
        <div className="flex items-center justify-between px-4 py-3 bg-slate-900 border-b border-slate-800">
          <div className="flex items-center space-x-2">
            <Terminal className="w-4 h-4 text-emerald-400" />
            <span className="text-xs font-bold uppercase tracking-wider text-slate-200">
              Generated Cypher Query
            </span>
            <span className="text-2xs px-2 py-0.5 rounded-full bg-emerald-950 text-emerald-400 border border-emerald-800">
              Neo4j Query Language
            </span>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={handleCopyCypher}
              className="flex items-center space-x-1 px-2.5 py-1 rounded-md text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition-colors"
              title="Copy Cypher to clipboard"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? 'Copied' : 'Copy'}</span>
            </button>
            <button
              onClick={() => setShowCypher(!showCypher)}
              className="text-xs text-slate-400 hover:text-slate-200 px-2 py-1"
            >
              {showCypher ? 'Collapse' : 'Expand'}
            </button>
          </div>
        </div>

        {showCypher && (
          <div className="p-4 overflow-x-auto">
            <pre className="text-xs font-mono text-emerald-300 leading-relaxed">
              <code>{cypherQuery}</code>
            </pre>
          </div>
        )}
      </div>

      {/* Result Cards Grid */}
      <div>
        <div className="flex items-center space-x-2 mb-4">
          <Layers className="w-4 h-4 text-emerald-600" />
          <h3 className="text-sm font-bold text-slate-800 uppercase tracking-wider">
            Matching Entities ({resultCount})
          </h3>
        </div>

        {results.length === 0 ? (
          <div className="bg-white rounded-2xl border border-slate-200/80 p-10 text-center">
            <p className="text-sm font-semibold text-slate-700">No animals match the specified graph constraints.</p>
            <p className="text-xs text-slate-400 mt-1">Try modifying the question or broadening the filters.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {results.map((animal) => (
              <AnimalCard
                key={animal.id}
                animal={animal}
                onExploreGraph={onExploreGraph}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
