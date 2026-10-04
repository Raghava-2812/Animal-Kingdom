import React from 'react';

export default function StatCard({ label, value, icon: Icon, color = 'emerald', subtitle, onClick }) {
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
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-500 mb-1">
            {label}
          </p>
          <p className="text-3xl font-extrabold text-slate-900 tracking-tight">
            {value !== undefined && value !== null ? value : '—'}
          </p>
          {subtitle && (
            <p className="text-xs text-slate-400 mt-1 font-medium">{subtitle}</p>
          )}
        </div>
        {Icon && (
          <div className={`p-3 rounded-xl border ${badgeClass} group-hover:scale-105 transition-transform`}>
            <Icon className="w-6 h-6" />
          </div>
        )}
      </div>
    </div>
  );
}
