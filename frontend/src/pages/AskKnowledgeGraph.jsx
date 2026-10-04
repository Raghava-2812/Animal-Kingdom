import React, { useState, useEffect } from 'react';
import { HelpCircle, Sparkles, Terminal, BookOpen, AlertCircle } from 'lucide-react';
import { api } from '../services/api';
import QueryBox from '../components/QueryBox';
import QueryResult from '../components/QueryResult';

export default function AskKnowledgeGraph() {
  const [question, setQuestion] = useState('Show endangered animals that live in forests');
  const [exampleQuestions, setExampleQuestions] = useState([]);
  const [queryResponse, setQueryResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch example questions from backend
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

    // Execute default query on mount for immediate presentation
    handleExecuteQuery('Show endangered animals that live in forests');
  }, []);

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

  const handleSelectExample = (exampleText) => {
    setQuestion(exampleText);
    handleExecuteQuery(exampleText);
  };

  return (
    <div className="space-y-8 py-4 max-w-7xl mx-auto">
      {/* Page Title */}
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

      {/* Query Box with Predefined Chips */}
      <QueryBox
        question={question}
        onQuestionChange={setQuestion}
        onSubmit={handleExecuteQuery}
        loading={loading}
        exampleQuestions={exampleQuestions}
        onSelectExample={handleSelectExample}
      />

      {/* Error Alert */}
      {error && (
        <div className="bg-rose-50 border border-rose-200 rounded-2xl p-4 flex items-center space-x-3 text-rose-800">
          <AlertCircle className="w-5 h-5 text-rose-500 shrink-0" />
          <p className="text-xs font-medium">{error}</p>
        </div>
      )}

      {/* Query Results and Cypher Inspection */}
      <QueryResult
        response={queryResponse}
        loading={loading}
      />

      {/* Academic Query Mechanism Explanation */}
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
