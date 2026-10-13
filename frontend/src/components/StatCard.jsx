/**
 * Metric Summary Card Component.
 *
 * Renders an analytical KPI widget for dashboard views:
 * - Metric label (e.g., "Total Animals", "Endangered Species").
 * - Prominent numerical tally (e.g., 39, 11).
 * - Optional descriptive subtitle.
 * - Categorically colored icon badge (emerald, blue, rose, amber, purple).
 * - Optional `onClick` handler enabling navigation or filter triggering.
 *
 * Props:
 * @param {string} props.label - KPI metric title.
 * @param {number|string} props.value - Metric value.
 * @param {React.ComponentType} [props.icon] - Lucide icon component.
 * @param {string} [props.color="emerald"] - Color theme key ('emerald', 'blue', 'amber', 'rose', 'purple', 'indigo').
 * @param {string} [props.subtitle] - Explanatory subtitle below the number.
 * @param {Function} [props.onClick] - Optional click handler.
 */

import React from 'react';

export default function StatCard({ label, value, icon: Icon, color = 'emerald', subtitle, onClick }) {
  // Mapping color theme keys to Tailwind utility classes
  const colorMap = {
    emerald: 'bg-emerald-50 text-emerald-600 border-emerald-100',
    blue: 'bg-blue-50 text-blue-600 border-blue-100',
    amber: 'bg-amber-50 text-amber-600 border-amber-100',
    rose: 'bg-rose-50 text-rose-600 border-rose-100',
    purple: 'bg-purple-50 text-purple-600 border-purple-100',
    indigo: 'bg-indigo-50 text-indigo-600 border-indigo-100',
  };

  const badgeClass = colorMap[color] || colorMap.emerald;

  return (
    <div
      onClick={onClick}
      className={`bg-white rounded-xl border border-slate-200/80 p-5 shadow-xs hover:shadow-md transition-all ${
        onClick ? 'cursor-pointer hover:border-emerald-300 group' : ''
      }`}
    >
      <div className="flex items-center justify-between">
        <div>
          {/* Metric Label */}
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-500 mb-1">
            {label}
          </p>
          {/* Prominent Number */}
          <p className="text-3xl font-extrabold text-slate-900 tracking-tight">
            {value !== undefined && value !== null ? value : '—'}
          </p>
          {/* Optional Contextual Subtitle */}
          {subtitle && (
            <p className="text-xs text-slate-400 mt-1 font-medium">{subtitle}</p>
          )}
        </div>
        {/* Metric Icon Badge */}
        {Icon && (
          <div className={`p-3 rounded-xl border ${badgeClass} group-hover:scale-105 transition-transform`}>
            <Icon className="w-6 h-6" />
          </div>
        )}
      </div>
    </div>
  );
}
