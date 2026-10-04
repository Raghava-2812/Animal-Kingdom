import React from 'react';
import { Sparkles, Send, HelpCircle } from 'lucide-react';

export default function QueryBox({
  question,
  onQuestionChange,
  onSubmit,
  loading,
  exampleQuestions = [],
  onSelectExample
}) {
  return (
    <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm">
      <div className="flex items-center space-x-2 mb-3">
        <Sparkles className="w-5 h-5 text-emerald-600" />
        <h2 className="text-lg font-bold text-slate-900 tracking-tight">
          Natural Language Cypher Engine
        </h2>
      </div>
      <p className="text-xs text-slate-500 mb-4 leading-relaxed">
        Query the Neo4j Knowledge Graph using plain English. The backend extracts graph entities (habitats, diets, taxonomy, conservation statuses) and translates them into an optimized Cypher query.
      </p>

      {/* Input & Submit */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          if (question.trim()) onSubmit(question);
        }}
        className="mb-4"
      >
        <div className="relative flex items-center">
          <input
            type="text"
            value={question}
            onChange={(e) => onQuestionChange(e.target.value)}
            placeholder="e.g. Show endangered animals that live in forests..."
            className="w-full pl-4 pr-32 py-3.5 bg-slate-50 border border-slate-300 rounded-xl text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:bg-white transition-all shadow-inner"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !question.trim()}
            className="absolute right-2 flex items-center space-x-1.5 px-4 py-2 bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white text-xs font-semibold rounded-lg shadow-xs transition-all cursor-pointer"
          >
            {loading ? (
              <span className="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <>
                <Send className="w-3.5 h-3.5" />
                <span>Ask Graph</span>
              </>
            )}
          </button>
        </div>
      </form>

      {/* Predefined Clickable Example Chips */}
      {exampleQuestions.length > 0 && (
        <div>
          <div className="flex items-center space-x-1.5 mb-2">
            <HelpCircle className="w-3.5 h-3.5 text-slate-400" />
            <span className="text-2xs font-bold uppercase tracking-wider text-slate-400">
              Predefined Academic Queries (Click to load):
            </span>
          </div>
          <div className="flex flex-wrap gap-2">
            {exampleQuestions.map((eq, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => onSelectExample(eq)}
                className="px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-100 hover:bg-emerald-50 hover:text-emerald-700 text-slate-700 border border-slate-200 hover:border-emerald-200 transition-colors cursor-pointer text-left"
              >
                {eq}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
