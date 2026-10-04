import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Network,
  Share2,
  TreePine,
  Utensils,
  AlertTriangle,
  Globe,
  ArrowRight,
  Database,
  Sparkles,
  Layers,
  Search
} from 'lucide-react';
import { api } from '../services/api';
import StatCard from '../components/StatCard';
import GraphViewer from '../components/GraphViewer';

export default function Home() {
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [sampleGraph, setSampleGraph] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([
      api.getStats().catch((err) => {
        console.warn("Failed fetching stats", err);
        return {
          totalAnimals: 38,
          totalSpecies: 38,
          totalHabitats: 9,
          totalFoods: 28,
          totalEndangeredAnimals: 9,
          totalContinents: 7,
          neo4jConnected: false
        };
      }),
      api.getAnimalGraph('animal_tiger').catch((err) => {
        console.warn("Failed fetching sample tiger graph", err);
        return null;
      })
    ]).then(([statsData, graphData]) => {
      setStats(statsData);
      setSampleGraph(graphData);
      setLoading(false);
    }).catch((err) => {
      setError(err.message);
      setLoading(false);
    });
  }, []);

  const quickExploreCards = [
    {
      title: 'Animals',
      emoji: '🐯',
      description: 'Explore 38+ species across Mammalia, Aves, Reptilia, and more.',
      link: '/explore',
      color: 'border-emerald-200 hover:border-emerald-400 bg-emerald-50/40'
    },
    {
      title: 'Habitats',
      emoji: '🌳',
      description: 'Traverse ecosystems from dense tropical forests to polar tundras.',
      link: '/explore?habitat=Forest',
      color: 'border-green-200 hover:border-green-400 bg-green-50/40'
    },
    {
      title: 'Diets',
      emoji: '🍃',
      description: 'Analyze trophic feeding interactions: carnivores, herbivores & omnivores.',
      link: '/explore?diet=Carnivore',
      color: 'border-amber-200 hover:border-amber-400 bg-amber-50/40'
    },
    {
      title: 'Conservation Status',
      emoji: '⚠️',
      description: 'Monitor IUCN red list threat levels for vulnerable and endangered wildlife.',
      link: '/explore?status=Endangered',
      color: 'border-rose-200 hover:border-rose-400 bg-rose-50/40'
    },
    {
      title: 'Continents',
      emoji: '🌍',
      description: 'Discover geographical distributions across all 7 continents.',
      link: '/explore?continent=Asia',
      color: 'border-purple-200 hover:border-purple-400 bg-purple-50/40'
    }
  ];

  return (
    <div className="space-y-12 py-6">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-emerald-900 to-slate-900 text-white rounded-3xl p-8 sm:p-12 shadow-xl border border-emerald-800/40">
        <div className="relative z-10 max-w-3xl space-y-5">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 backdrop-blur-md">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Academic Graph Intelligence Platform</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight leading-tight">
            Explore the Animal Kingdom Through{' '}
            <span className="text-emerald-400 underline decoration-emerald-500/50">
              Knowledge Graphs
            </span>
          </h1>

          <p className="text-slate-300 text-sm sm:text-base leading-relaxed">
            Discover how animals are connected to species, habitats, diets, food sources, geographical regions and conservation status. Powered by Neo4j graph engine, Cypher queries, and FastAPI.
          </p>

          <div className="pt-2 flex flex-wrap gap-3">
            <Link
              to="/explore"
              className="inline-flex items-center space-x-2 px-6 py-3 rounded-xl font-bold text-sm bg-emerald-500 hover:bg-emerald-400 text-slate-950 shadow-md hover:shadow-emerald-500/20 transition-all cursor-pointer"
            >
              <Network className="w-4 h-4" />
              <span>Explore Knowledge Graph</span>
            </Link>
            <Link
              to="/ask"
              className="inline-flex items-center space-x-2 px-6 py-3 rounded-xl font-semibold text-sm bg-slate-800/80 hover:bg-slate-700 text-white border border-slate-700 transition-all cursor-pointer"
            >
              <Search className="w-4 h-4 text-emerald-400" />
              <span>Ask Knowledge Graph</span>
            </Link>
          </div>
        </div>

        {/* Subtle Decorative Graph Watermark */}
        <div className="absolute right-0 bottom-0 opacity-10 pointer-events-none translate-x-12 translate-y-12 hidden md:block">
          <Network className="w-96 h-96 text-white" />
        </div>
      </section>

      {/* Dynamic Graph Statistics */}
      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-slate-900 tracking-tight">
              Knowledge Graph Statistics
            </h2>
            <p className="text-xs text-slate-500">
              Live graph metrics calculated directly from Neo4j node and relationship collections.
            </p>
          </div>
          {stats?.neo4jConnected !== undefined && (
            <span className="text-2xs font-semibold px-2.5 py-1 rounded-full bg-slate-100 text-slate-600 border border-slate-200">
              {stats.neo4jConnected ? '🟢 Live Cypher Counts' : '🟡 Offline Dataset'}
            </span>
          )}
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
          <StatCard
            label="Animals"
            value={stats?.totalAnimals}
            icon={Layers}
            color="emerald"
            subtitle="Entity nodes"
            onClick={() => navigate('/explore')}
          />
          <StatCard
            label="Species"
            value={stats?.totalSpecies}
            icon={Share2}
            color="indigo"
            subtitle="Taxonomies"
            onClick={() => navigate('/explore')}
          />
          <StatCard
            label="Habitats"
            value={stats?.totalHabitats}
            icon={TreePine}
            color="emerald"
            subtitle="Biomes & Ecosystems"
            onClick={() => navigate('/explore?habitat=Forest')}
          />
          <StatCard
            label="Food Sources"
            value={stats?.totalFoods}
            icon={Utensils}
            color="amber"
            subtitle="Trophic links"
            onClick={() => navigate('/ask')}
          />
          <StatCard
            label="Endangered"
            value={stats?.totalEndangeredAnimals}
            icon={AlertTriangle}
            color="rose"
            subtitle="IUCN Threatened"
            onClick={() => navigate('/explore?status=Endangered')}
          />
          <StatCard
            label="Continents"
            value={stats?.totalContinents}
            icon={Globe}
            color="purple"
            subtitle="Global regions"
            onClick={() => navigate('/explore?continent=Asia')}
          />
        </div>
      </section>

      {/* Quick Exploration Cards */}
      <section className="space-y-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">
            Quick Exploration Categories
          </h2>
          <p className="text-xs text-slate-500">
            Click any dimension to filter and discover connected wildlife.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
          {quickExploreCards.map((card, i) => (
            <Link
              key={i}
              to={card.link}
              className={`rounded-2xl border p-5 transition-all hover:shadow-md hover:-translate-y-0.5 flex flex-col justify-between ${card.color}`}
            >
              <div>
                <span className="text-3xl block mb-2">{card.emoji}</span>
                <h3 className="font-bold text-base text-slate-900 mb-1">{card.title}</h3>
                <p className="text-xs text-slate-600 leading-relaxed">{card.description}</p>
              </div>
              <div className="pt-4 flex items-center text-xs font-bold text-emerald-700">
                <span>Explore</span>
                <ArrowRight className="w-3.5 h-3.5 ml-1" />
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* Interactive Graph Showcase Preview */}
      {sampleGraph && (
        <section className="space-y-3 bg-white rounded-3xl border border-slate-200/80 p-6 sm:p-8 shadow-xs">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <div className="flex items-center space-x-2">
                <Network className="w-5 h-5 text-emerald-600" />
                <h2 className="text-xl font-bold text-slate-900 tracking-tight">
                  Sample Graph: Tiger Ecosystem
                </h2>
              </div>
              <p className="text-xs text-slate-500 mt-1">
                Demonstration of the core principle: <strong className="text-slate-700">ENTITY → RELATIONSHIP → ENTITY</strong>. Pan, zoom, or click any node below.
              </p>
            </div>
            <Link
              to="/animals/animal_tiger"
              className="inline-flex items-center space-x-1.5 px-4 py-2 rounded-xl text-xs font-semibold bg-emerald-50 text-emerald-700 hover:bg-emerald-100 border border-emerald-200 transition-colors"
            >
              <span>View Full Tiger Profile</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="mt-4">
            <GraphViewer graphData={sampleGraph} height="480px" centerNodeId="animal_tiger" />
          </div>
        </section>
      )}

      {/* Academic Architecture Concept Note */}
      <section className="bg-slate-100/80 rounded-2xl border border-slate-200 p-6 text-slate-700">
        <h3 className="text-sm font-bold uppercase tracking-wider text-slate-900 mb-2">
          Academic Knowledge Graph Design Principle
        </h3>
        <p className="text-xs leading-relaxed mb-3">
          Traditional databases store flat records in isolated tables. In this system, knowledge is represented as a directed property graph in Neo4j. By traversing labeled edges such as <code>LIVES_IN</code>, <code>EATS</code>, <code>BELONGS_TO_SPECIES</code>, and <code>FOUND_IN</code>, users can uncover ecological dependencies and conservation correlations impossible to see in standard relational tables.
        </p>
        <div className="flex flex-wrap gap-4 text-xs font-mono text-emerald-800 bg-white p-3 rounded-xl border border-slate-200">
          <span>Tiger -[:BELONGS_TO_SPECIES]-&gt; Panthera tigris</span>
          <span>•</span>
          <span>Tiger -[:LIVES_IN]-&gt; Forest</span>
          <span>•</span>
          <span>Tiger -[:EATS]-&gt; Deer</span>
          <span>•</span>
          <span>Tiger -[:HAS_STATUS]-&gt; Endangered</span>
        </div>
      </section>
    </div>
  );
}
