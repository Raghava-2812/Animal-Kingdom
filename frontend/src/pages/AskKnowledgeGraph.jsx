/**
 * Natural Language Knowledge Graph Query Page View Component.
 *
 * Provides an academic natural-language search workbench:
 * - Pre-loads curated example queries from `/api/queries/examples` (e.g., "Show endangered animals that live in forests").
 * - Auto-executes an initial sample query on mount so users immediately see results and Cypher statements.
 * - Submits user input to `/api/queries/ask` via the `QueryBox` component.
 * - Displays the breakdown via `QueryResult`: detected filters, generated Cypher code block,
 *   academic explanation, and matching animal cards.
 * - Educational footer explaining the three-step pipeline: Entity Extraction -> Cypher Generation -> Graph Retrieval.
 */

import React, { useState, useEffect } from 'react';
import { HelpCircle, Sparkles, Terminal, BookOpen, AlertCircle } from 'lucide-react';
import { api } from '../services/api';
import QueryBox from '../components/QueryBox';
import QueryResult from '../components/QueryResult';

export default function AskKnowledgeGraph() {
  // Controlled input query text (initialized with a representative query)
  const [question, setQuestion] = useState('Show endangered animals that live in forests');

  // Predefined example queries loaded from backend
  const [exampleQuestions, setExampleQuestions] = useState([]);

  // Query response payload from the Cypher translation engine
  const [queryResponse, setQueryResponse] = useState(null);

  // Status flags
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  /**
   * Initializes page on mount:
   * 1. Fetches predefined academic query examples.
   * 2. Executes the default query immediately for instant visual feedback.
   */
  useEffect(() => {
    api.getExampleQuestions()
      .then((data) => {
        setExampleQuestions(data);
      })
      .catch((err) => {
        console.warn("Could not load example questions", err);
        setExampleQuestions([
          "Show endangered animals that live in forests",
          "Show carnivorous mammals",
          "Show herbivores found in Asia",
          "Show animals that eat fish",
          "Show animals living in grasslands",
          "Show critically endangered animals",
          "Show mammals found in Africa",
          "Show animals that live in both forests and grasslands",
          "Show animals that eat fruits",
          "Show animals found in Asia and having an endangered status"
        ]);
      });

    // Auto-run default query on initial page load
    handleExecuteQuery('Show endangered animals that live in forests');
  }, []);

  /**
   * Submits a question string to the backend Natural Language Cypher engine.
   * @param {string} queryText - The plain English question to translate and execute.
   */
  const handleExecuteQuery = async (queryText) => {
    if (!queryText.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const data = await api.askQuestion(queryText.trim());
      setQueryResponse(data);
    } catch (err) {
      setError(err.message || 'Failed to process natural language query');
    } finally {
      setLoading(false);
    }
  };

  /**
   * Populates the query box and immediately executes when a sample chip is clicked.
   * @param {string} exampleText - The clicked sample question.
   */
  const handleSelectExample = (exampleText) => {
    setQuestion(exampleText);
    handleExecuteQuery(exampleText);
  };

  return (
    <div className="space-y-8 py-4 max-w-7xl mx-auto">
      {/* 1. Page Header */}
      <div>
        <div className="flex items-center space-x-2 text-emerald-600 mb-1">
          <HelpCircle className="w-5 h-5" />
          <span className="text-xs font-bold uppercase tracking-wider">Natural Language Interface</span>
        </div>
        <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
          Ask the Knowledge Graph
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1 max-w-3xl leading-relaxed">
          Ask questions in plain English. The backend entity mapper translates the input into parameterized Cypher statements executed against the Neo4j Knowledge Graph.
        </p>
      </div>

      {/* 2. Query Box with Clickable Sample Query Pills */}
      <QueryBox
        question={question}
        onQuestionChange={setQuestion}
        onSubmit={handleExecuteQuery}
        loading={loading}
        exampleQuestions={exampleQuestions}
        onSelectExample={handleSelectExample}
      />

      {/* Error Alert Banner */}
      {error && (
        <div className="bg-rose-50 border border-rose-200 rounded-2xl p-4 flex items-center space-x-3 text-rose-800">
          <AlertCircle className="w-5 h-5 text-rose-500 shrink-0" />
          <p className="text-xs font-medium">{error}</p>
        </div>
      )}

      {/* 3. Query Results, Generated Cypher Code Block, and Entity Cards */}
      <QueryResult
        response={queryResponse}
        loading={loading}
      />

      {/* 4. Educational Pipeline Architecture Explanation */}
      <div className="bg-slate-50 rounded-2xl border border-slate-200 p-6 text-slate-600 space-y-3">
        <div className="flex items-center space-x-2">
          <BookOpen className="w-4 h-4 text-emerald-600" />
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-800">
            How Natural Language Mapping Works in this Project
          </h4>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div className="bg-white p-3.5 rounded-xl border border-slate-200/80">
            <span className="font-bold text-slate-900 block mb-1">1. Entity Extraction</span>
            <p className="text-slate-500">
              Identifies keywords corresponding to graph nodes: Habitat (Forest), Diet (Carnivore), Class (Mammal), and Status (Endangered).
            </p>
          </div>
          <div className="bg-white p-3.5 rounded-xl border border-slate-200/80">
            <span className="font-bold text-slate-900 block mb-1">2. Cypher Generation</span>
            <p className="text-slate-500">
              Builds explicit graph traversals: <code>MATCH (a:Animal)-[:LIVES_IN]-&gt;(h:Habitat)</code> with parameterized <code>WHERE</code> clauses.
            </p>
          </div>
          <div className="bg-white p-3.5 rounded-xl border border-slate-200/80">
            <span className="font-bold text-slate-900 block mb-1">3. Graph Retrieval</span>
            <p className="text-slate-500">
              The official Neo4j driver executes the query, returning matched animal nodes and relationships for display.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
