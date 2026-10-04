import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Share2, MapPin, Sparkles, ShieldAlert, HeartHandshake, Image as ImageIcon } from 'lucide-react';

const STATUS_COLORS = {
  'Least Concern': 'bg-emerald-50 text-emerald-700 border-emerald-200',
  'Near Threatened': 'bg-lime-50 text-lime-700 border-lime-200',
  'Vulnerable': 'bg-amber-50 text-amber-700 border-amber-200',
  'Endangered': 'bg-orange-50 text-orange-700 border-orange-200',
  'Critically Endangered': 'bg-rose-50 text-rose-700 border-rose-200',
};

const CLASS_COLORS = {
  Mammal: 'bg-blue-50 text-blue-700 border-blue-200',
  Bird: 'bg-sky-50 text-sky-700 border-sky-200',
  Reptile: 'bg-teal-50 text-teal-700 border-teal-200',
  Amphibian: 'bg-emerald-50 text-emerald-700 border-emerald-200',
  Fish: 'bg-cyan-50 text-cyan-700 border-cyan-200',
  Insect: 'bg-amber-50 text-amber-700 border-amber-200',
};

const CLASS_FALLBACKS = {
  Mammal: "https://images.unsplash.com/photo-1561731216-c3a4d99437d5?auto=format&fit=crop&w=800&q=80",
  Bird: "https://images.unsplash.com/photo-1611689342806-0863700ce1e4?auto=format&fit=crop&w=800&q=80",
  Reptile: "https://images.unsplash.com/photo-1549480017-d76466a4b7e8?auto=format&fit=crop&w=800&q=80",
  Fish: "https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=800&q=80",
  Amphibian: "https://images.unsplash.com/photo-1550853024-fae8dd4be47f?auto=format&fit=crop&w=800&q=80",
  Insect: "https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?auto=format&fit=crop&w=800&q=80",
};

export default function AnimalCard({ animal, onExploreGraph }) {
  const navigate = useNavigate();
  const [imgErrorStep, setImgErrorStep] = useState(0);

  const statusBadge = STATUS_COLORS[animal.conservationStatus] || 'bg-slate-50 text-slate-700 border-slate-200';
  const classBadge = CLASS_COLORS[animal.className] || 'bg-slate-50 text-slate-700 border-slate-200';

  // Multi-tier redundant image selection
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
    <div className="bg-white rounded-xl border border-slate-200/80 overflow-hidden shadow-xs hover:shadow-md transition-all flex flex-col group hover:border-emerald-300">
      {/* Image & Quick Badges */}
      <div className="relative h-48 bg-slate-900 overflow-hidden">
        <img
          src={getImageSource()}
          alt={animal.name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          onError={handleImageError}
          loading="lazy"
          referrerPolicy="no-referrer"
        />
        <div className="absolute top-2.5 left-2.5 flex flex-wrap gap-1.5">
          {animal.className && (
            <span className={`px-2 py-0.5 rounded-md text-xs font-semibold border backdrop-blur-xs ${classBadge}`}>
              {animal.className}
            </span>
          )}
          {animal.diet && (
            <span className="px-2 py-0.5 rounded-md text-xs font-medium bg-white/90 text-slate-700 border border-slate-200 backdrop-blur-xs">
              {animal.diet}
            </span>
          )}
        </div>
        {animal.conservationStatus && (
          <div className="absolute top-2.5 right-2.5">
            <span className={`px-2 py-0.5 rounded-md text-xs font-semibold border backdrop-blur-xs ${statusBadge}`}>
              {animal.conservationStatus}
            </span>
          </div>
        )}
      </div>

      {/* Body Info */}
      <div className="p-4 flex-1 flex flex-col justify-between">
        <div>
          <div className="flex items-baseline justify-between mb-1">
            <h3 className="font-bold text-lg text-slate-900 group-hover:text-emerald-700 transition-colors">
              {animal.name}
            </h3>
            {animal.averageLifespan && (
              <span className="text-xs font-medium text-slate-500">
                ~{animal.averageLifespan} yrs
              </span>
            )}
          </div>
          <p className="text-xs italic text-slate-500 mb-2">
            {animal.scientificName || 'Taxonomic classification'}
          </p>
          {animal.description && (
            <p className="text-xs text-slate-600 line-clamp-2 mb-3 leading-relaxed">
              {animal.description}
            </p>
          )}

          {/* Habitats & Continents */}
          <div className="flex flex-wrap gap-1 mb-4">
            {animal.habitats && animal.habitats.map((h) => (
              <span
                key={h}
                className="inline-flex items-center px-2 py-0.5 rounded-full text-2xs font-medium bg-emerald-50 text-emerald-800 border border-emerald-100"
              >
                🌳 {h}
              </span>
            ))}
            {animal.continents && animal.continents.slice(0, 2).map((c) => (
              <span
                key={c}
                className="inline-flex items-center px-2 py-0.5 rounded-full text-2xs font-medium bg-slate-100 text-slate-700 border border-slate-200"
              >
                🌍 {c}
              </span>
            ))}
            {animal.continents && animal.continents.length > 2 && (
              <span className="text-2xs text-slate-500 font-medium self-center">
                +{animal.continents.length - 2} more
              </span>
            )}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="pt-3 border-t border-slate-100 flex items-center gap-2">
          <Link
            to={`/animals/${animal.id}`}
            className="flex-1 text-center py-2 px-3 rounded-lg text-xs font-semibold bg-slate-900 text-white hover:bg-slate-800 transition-colors shadow-xs"
          >
            View Details
          </Link>
          <button
            onClick={() => {
              if (onExploreGraph) {
                onExploreGraph(animal.id);
              } else {
                navigate(`/animals/${animal.id}?tab=graph`);
              }
            }}
            className="flex items-center justify-center p-2 rounded-lg text-xs font-medium text-emerald-700 bg-emerald-50 hover:bg-emerald-100 border border-emerald-200 transition-colors cursor-pointer"
            title="Explore Knowledge Graph relationships"
          >
            <Share2 className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
