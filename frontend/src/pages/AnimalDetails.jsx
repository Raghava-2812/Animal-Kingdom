import React, { useState, useEffect } from 'react';
import { useParams, Link, useSearchParams, useNavigate } from 'react-router-dom';
import {
  ArrowLeft,
  Network,
  Share2,
  TreePine,
  Utensils,
  AlertTriangle,
  Globe,
  Clock,
  Dna,
  Layers,
  ChevronRight,
  ExternalLink
} from 'lucide-react';
import { api } from '../services/api';
import GraphViewer from '../components/GraphViewer';

const STATUS_BADGES = {
  'Least Concern': 'bg-emerald-50 text-emerald-800 border-emerald-300',
  'Near Threatened': 'bg-lime-50 text-lime-800 border-lime-300',
  'Vulnerable': 'bg-amber-50 text-amber-800 border-amber-300',
  'Endangered': 'bg-orange-50 text-orange-800 border-orange-300',
  'Critically Endangered': 'bg-rose-50 text-rose-800 border-rose-300',
};

const CLASS_FALLBACKS = {
  Mammal: "https://images.unsplash.com/photo-1561731216-c3a4d99437d5?auto=format&fit=crop&w=800&q=80",
  Bird: "https://images.unsplash.com/photo-1611689342806-0863700ce1e4?auto=format&fit=crop&w=800&q=80",
  Reptile: "https://images.unsplash.com/photo-1549480017-d76466a4b7e8?auto=format&fit=crop&w=800&q=80",
  Fish: "https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=800&q=80",
  Amphibian: "https://images.unsplash.com/photo-1550853024-fae8dd4be47f?auto=format&fit=crop&w=800&q=80",
  Insect: "https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?auto=format&fit=crop&w=800&q=80",
};

export default function AnimalDetails() {
  const { animal_id } = useParams();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const [animal, setAnimal] = useState(null);
  const [graphData, setGraphData] = useState(null);
  const [activeTab, setActiveTab] = useState(searchParams.get('tab') === 'graph' ? 'graph' : 'overview');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [imgErrorStep, setImgErrorStep] = useState(0);

  useEffect(() => {
    setLoading(true);
    setError(null);
    setImgErrorStep(0);

    Promise.all([
      api.getAnimalById(animal_id),
      api.getAnimalGraph(animal_id)
    ])
      .then(([details, graph]) => {
        setAnimal(details);
        setGraphData(graph);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, [animal_id]);

  if (loading) {
    return (
      <div className="py-20 text-center">
        <div className="w-10 h-10 border-3 border-emerald-600 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
        <p className="text-sm font-semibold text-slate-700">Retrieving animal entity and graph topology...</p>
      </div>
    );
  }

  if (error || !animal) {
    return (
      <div className="py-12 max-w-lg mx-auto text-center bg-white rounded-2xl border border-slate-200 p-8">
        <h2 className="text-lg font-bold text-slate-900 mb-2">Animal Not Found</h2>
        <p className="text-xs text-slate-500 mb-4">{error || "Could not locate this entity in the Knowledge Graph."}</p>
        <Link
          to="/explore"
          className="inline-flex items-center space-x-1 px-4 py-2 bg-emerald-600 text-white rounded-lg text-xs font-semibold hover:bg-emerald-700 transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Explore</span>
        </Link>
      </div>
    );
  }

  const getImageSource = () => {
    if (imgErrorStep === 0 && animal.imageUrl) {
      return animal.imageUrl;
    }
    if (imgErrorStep <= 1 && animal.fallbackImageUrl) {
      return animal.fallbackImageUrl;
    }
    return CLASS_FALLBACKS[animal.className] || CLASS_FALLBACKS.Mammal;
  };

  const handleImageError = () => {
    if (imgErrorStep < 2) {
      setImgErrorStep((prev) => prev + 1);
    }
  };

  return (
    <div className="space-y-6 py-4">
      {/* Back button */}
      <div>
        <Link
          to="/explore"
          className="inline-flex items-center space-x-1.5 text-xs font-semibold text-slate-500 hover:text-slate-800 transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Animals</span>
        </Link>
      </div>

      {/* Main Profile Header Banner */}
      <div className="bg-white rounded-3xl border border-slate-200/80 overflow-hidden shadow-xs">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-0">
          {/* Photo */}
          <div className="md:col-span-5 h-64 md:h-auto relative bg-slate-900">
            <img
              src={getImageSource()}
              alt={animal.name}
              className="w-full h-full object-cover"
              onError={handleImageError}
              referrerPolicy="no-referrer"
            />
            <div className="absolute top-4 left-4">
              <span className={`px-3 py-1 rounded-full text-xs font-bold border backdrop-blur-md shadow-xs ${STATUS_BADGES[animal.conservationStatus] || 'bg-slate-100 text-slate-700'}`}>
                {animal.conservationStatus}
              </span>
            </div>
          </div>

          {/* Details */}
          <div className="md:col-span-7 p-6 sm:p-8 flex flex-col justify-between">
            <div>
              <div className="flex flex-wrap items-baseline gap-2 mb-1">
                <h1 className="text-2xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
                  {animal.name}
                </h1>
                <span className="text-sm font-medium italic text-slate-500">
                  ({animal.scientificName})
                </span>
              </div>

              <p className="text-xs text-slate-400 font-mono mb-4">
                Entity ID: {animal.id}
              </p>

              <p className="text-sm text-slate-600 leading-relaxed mb-6">
                {animal.description}
              </p>

              {/* Taxonomy & Traits Pills */}
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-6">
                <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-100">
                  <span className="text-2xs font-bold uppercase tracking-wider text-slate-400 block mb-0.5">
                    Class
                  </span>
                  <span className="text-xs font-bold text-blue-700">{animal.className}</span>
                </div>
                <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-100">
                  <span className="text-2xs font-bold uppercase tracking-wider text-slate-400 block mb-0.5">
                    Species
                  </span>
                  <span className="text-xs font-bold text-indigo-700 truncate block" title={animal.species}>
                    {animal.species}
                  </span>
                </div>
                <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-100">
                  <span className="text-2xs font-bold uppercase tracking-wider text-slate-400 block mb-0.5">
                    Diet
                  </span>
                  <span className="text-xs font-bold text-amber-700">{animal.diet}</span>
                </div>
                <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-100">
                  <span className="text-2xs font-bold uppercase tracking-wider text-slate-400 block mb-0.5">
                    Lifespan
                  </span>
                  <span className="text-xs font-bold text-slate-800">
                    {animal.averageLifespan ? `~${animal.averageLifespan} Years` : '—'}
                  </span>
                </div>
              </div>
            </div>

            {/* Action Bar */}
            <div className="pt-4 border-t border-slate-100 flex flex-wrap gap-2">
              <button
                onClick={() => setActiveTab('graph')}
                className={`inline-flex items-center space-x-1.5 px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                  activeTab === 'graph'
                    ? 'bg-emerald-600 text-white shadow-sm'
                    : 'bg-emerald-50 text-emerald-800 hover:bg-emerald-100 border border-emerald-200'
                }`}
              >
                <Network className="w-4 h-4" />
                <span>Explore Relationships Graph</span>
              </button>
              <button
                onClick={() => setActiveTab('overview')}
                className={`inline-flex items-center space-x-1.5 px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                  activeTab === 'overview'
                    ? 'bg-slate-900 text-white shadow-sm'
                    : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                }`}
              >
                <Layers className="w-4 h-4" />
                <span>Attribute Explorer</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Interactive Tabs */}
      {activeTab === 'graph' ? (
        <section className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-xs space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <div className="flex items-center space-x-2">
                <Network className="w-5 h-5 text-emerald-600" />
                <h2 className="text-lg font-bold text-slate-900 tracking-tight">
                  {animal.name} Knowledge Graph Neighborhood
                </h2>
              </div>
              <p className="text-xs text-slate-500 mt-1">
                Visual representation of direct graph relationships: <code className="text-emerald-700 font-semibold font-mono">(:Animal)-[:RELATIONSHIP]-&gt;(:Node)</code>.
              </p>
            </div>
            <span className="text-2xs font-semibold px-2.5 py-1 rounded-full bg-slate-100 text-slate-600 border border-slate-200 self-start sm:self-auto">
              Pan & Zoom Supported • Click Nodes to Inspect
            </span>
          </div>

          <GraphViewer
            graphData={graphData}
            centerNodeId={animal.id}
            height="580px"
          />
        </section>
      ) : (
        <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Habitats Card */}
          <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-xs">
            <div className="flex items-center space-x-2 pb-3 mb-3 border-b border-slate-100">
              <TreePine className="w-4 h-4 text-emerald-600" />
              <h3 className="text-sm font-bold text-slate-800">Habitats (LIVES_IN)</h3>
            </div>
            <div className="space-y-2">
              {animal.habitats && animal.habitats.map((hab) => (
                <div
                  key={hab}
                  onClick={() => navigate(`/explore?habitat=${encodeURIComponent(hab)}`)}
                  className="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 hover:bg-emerald-50 border border-slate-100 hover:border-emerald-200 transition-colors cursor-pointer group"
                >
                  <span className="text-xs font-semibold text-slate-800 group-hover:text-emerald-800">
                    🌳 {hab}
                  </span>
                  <div className="flex items-center text-2xs text-slate-400 group-hover:text-emerald-600">
                    <span>Explore</span>
                    <ChevronRight className="w-3.5 h-3.5 ml-0.5" />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Food Sources Card */}
          <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-xs">
            <div className="flex items-center space-x-2 pb-3 mb-3 border-b border-slate-100">
              <Utensils className="w-4 h-4 text-amber-600" />
              <h3 className="text-sm font-bold text-slate-800">Dietary Prey / Food (EATS)</h3>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {animal.foodSources && animal.foodSources.map((food) => (
                <span
                  key={food}
                  className="px-2.5 py-1 rounded-lg text-xs font-medium bg-amber-50 text-amber-800 border border-amber-200"
                >
                  🥩 {food}
                </span>
              ))}
            </div>
          </div>

          {/* Continents Card */}
          <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-xs">
            <div className="flex items-center space-x-2 pb-3 mb-3 border-b border-slate-100">
              <Globe className="w-4 h-4 text-purple-600" />
              <h3 className="text-sm font-bold text-slate-800">Distribution (FOUND_IN)</h3>
            </div>
            <div className="space-y-2">
              {animal.continents && animal.continents.map((c) => (
                <div
                  key={c}
                  onClick={() => navigate(`/explore?continent=${encodeURIComponent(c)}`)}
                  className="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 hover:bg-purple-50 border border-slate-100 hover:border-purple-200 transition-colors cursor-pointer group"
                >
                  <span className="text-xs font-semibold text-slate-800 group-hover:text-purple-800">
                    🌍 {c}
                  </span>
                  <div className="flex items-center text-2xs text-slate-400 group-hover:text-purple-600">
                    <span>Explore</span>
                    <ChevronRight className="w-3.5 h-3.5 ml-0.5" />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}
    </div>
  );
}
