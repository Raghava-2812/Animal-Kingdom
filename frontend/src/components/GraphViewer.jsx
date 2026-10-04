import React, { useState, useRef, useEffect, useMemo } from 'react';
import { ZoomIn, ZoomOut, RotateCcw, Info, ExternalLink, X, Move } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const NODE_COLORS = {
  Animal: { fill: '#059669', stroke: '#047857', text: '#ffffff', tag: 'bg-emerald-600 text-white' },
  Species: { fill: '#4f46e5', stroke: '#4338ca', text: '#ffffff', tag: 'bg-indigo-600 text-white' },
  Class: { fill: '#2563eb', stroke: '#1d4ed8', text: '#ffffff', tag: 'bg-blue-600 text-white' },
  Habitat: { fill: '#16a34a', stroke: '#15803d', text: '#ffffff', tag: 'bg-green-600 text-white' },
  Diet: { fill: '#d97706', stroke: '#b45309', text: '#ffffff', tag: 'bg-amber-600 text-white' },
  Food: { fill: '#ea580c', stroke: '#c2410c', text: '#ffffff', tag: 'bg-orange-600 text-white' },
  ConservationStatus: { fill: '#e11d48', stroke: '#be123c', text: '#ffffff', tag: 'bg-rose-600 text-white' },
  Continent: { fill: '#9333ea', stroke: '#7e22ce', text: '#ffffff', tag: 'bg-purple-600 text-white' },
  default: { fill: '#475569', stroke: '#334155', text: '#ffffff', tag: 'bg-slate-600 text-white' }
};

export default function GraphViewer({
  graphData,
  onNodeClick,
  height = "560px",
  centerNodeId = null
}) {
  const navigate = useNavigate();
  const svgRef = useRef(null);

  // Transform states for Pan and Zoom
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const [selectedNode, setSelectedNode] = useState(null);

  // Reset viewport
  const handleReset = () => {
    setZoom(1);
    setPan({ x: 0, y: 0 });
    setSelectedNode(null);
  };

  // Node layout calculation
  const layout = useMemo(() => {
    if (!graphData || !graphData.nodes || graphData.nodes.length === 0) {
      return { nodesWithPos: [], relationshipsWithCoords: [] };
    }

    const width = 850;
    const height = 500;
    const centerX = width / 2;
    const centerY = height / 2;

    const nodes = [...graphData.nodes];
    const rels = [...graphData.relationships];

    // Find central node (either centerNodeId or first Animal node)
    let center = nodes.find(n => n.id === centerNodeId);
    if (!center) {
      center = nodes.find(n => n.type === 'Animal') || nodes[0];
    }

    const otherNodes = nodes.filter(n => n.id !== center.id);
    const nodesWithPos = [];

    // Center node position
    nodesWithPos.push({
      ...center,
      x: centerX,
      y: centerY,
      radius: 36,
      isCenter: true
    });

    // Arrange other nodes in orbital rings based on node type
    const innerRingTypes = ['Species', 'Diet', 'ConservationStatus'];
    const outerRingTypes = ['Class', 'Habitat', 'Food', 'Continent'];

    const innerNodes = otherNodes.filter(n => innerRingTypes.includes(n.type));
    const outerNodes = otherNodes.filter(n => !innerRingTypes.includes(n.type));

    // Position inner ring
    const innerRadius = 150;
    innerNodes.forEach((node, i) => {
      const angle = (i / Math.max(innerNodes.length, 1)) * 2 * Math.PI - Math.PI / 2;
      nodesWithPos.push({
        ...node,
        x: centerX + innerRadius * Math.cos(angle),
        y: centerY + innerRadius * Math.sin(angle),
        radius: 26,
        isCenter: false
      });
    });

    // Position outer ring
    const outerRadius = 260;
    outerNodes.forEach((node, i) => {
      const angle = (i / Math.max(outerNodes.length, 1)) * 2 * Math.PI - Math.PI / 4;
      nodesWithPos.push({
        ...node,
        x: centerX + outerRadius * Math.cos(angle),
        y: centerY + outerRadius * Math.sin(angle),
        radius: 24,
        isCenter: false
      });
    });

    // Build coordinate map
    const nodeMap = new Map();
    nodesWithPos.forEach(n => nodeMap.set(n.id, n));

    // Connect relationships
    const relationshipsWithCoords = rels.map(r => {
      const source = nodeMap.get(r.source);
      const target = nodeMap.get(r.target);
      return {
        ...r,
        sourceNode: source,
        targetNode: target,
      };
    }).filter(r => r.sourceNode && r.targetNode);

    return { nodesWithPos, relationshipsWithCoords };
  }, [graphData, centerNodeId]);

  // Mouse drag pan handler
  const handleMouseDown = (e) => {
    if (e.target.tagName === 'svg' || e.target.id === 'canvas-bg') {
      setIsDragging(true);
      setDragStart({ x: e.clientX - pan.x, y: e.clientY - pan.y });
    }
  };

  const handleMouseMove = (e) => {
    if (isDragging) {
      setPan({
        x: e.clientX - dragStart.x,
        y: e.clientY - dragStart.y
      });
    }
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  const handleNodeClickInternal = (node) => {
    setSelectedNode(node);
    if (onNodeClick) onNodeClick(node);
  };

  if (!graphData || !graphData.nodes || graphData.nodes.length === 0) {
    return (
      <div className="flex items-center justify-center bg-slate-50 border border-slate-200 rounded-2xl h-80 text-slate-400 text-sm">
        No graph data available to visualize.
      </div>
    );
  }

  return (
    <div className="relative bg-slate-950 rounded-2xl border border-slate-800 overflow-hidden shadow-lg select-none">
      {/* Top Toolbar */}
      <div className="absolute top-3 left-3 z-10 flex items-center space-x-2 bg-slate-900/90 backdrop-blur-md p-1.5 rounded-xl border border-slate-800 text-white">
        <span className="text-2xs font-bold uppercase tracking-wider text-emerald-400 px-2">
          Knowledge Graph
        </span>
        <div className="h-4 w-px bg-slate-700" />
        <button
          onClick={() => setZoom(z => Math.min(z + 0.2, 2.5))}
          className="p-1.5 hover:bg-slate-800 rounded-lg text-slate-300 hover:text-white transition-colors"
          title="Zoom In"
        >
          <ZoomIn className="w-4 h-4" />
        </button>
        <button
          onClick={() => setZoom(z => Math.max(z - 0.2, 0.4))}
          className="p-1.5 hover:bg-slate-800 rounded-lg text-slate-300 hover:text-white transition-colors"
          title="Zoom Out"
        >
          <ZoomOut className="w-4 h-4" />
        </button>
        <button
          onClick={handleReset}
          className="p-1.5 hover:bg-slate-800 rounded-lg text-slate-300 hover:text-white transition-colors"
          title="Reset Position & Zoom"
        >
          <RotateCcw className="w-4 h-4" />
        </button>
      </div>

      {/* Legend */}
      <div className="absolute top-3 right-3 z-10 hidden sm:flex flex-wrap items-center gap-1.5 bg-slate-900/90 backdrop-blur-md p-2 rounded-xl border border-slate-800 max-w-sm">
        {Object.entries(NODE_COLORS).filter(([k]) => k !== 'default').map(([type, colors]) => (
          <span
            key={type}
            className="inline-flex items-center text-2xs px-1.5 py-0.5 rounded-md text-slate-300 bg-slate-800/80 border border-slate-700/60"
          >
            <span className="w-2 h-2 rounded-full mr-1.5" style={{ backgroundColor: colors.fill }} />
            {type}
          </span>
        ))}
      </div>

      {/* Interactive SVG Canvas */}
      <svg
        ref={svgRef}
        className="w-full cursor-grab active:cursor-grabbing"
        style={{ height }}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
      >
        <defs>
          {/* Arrowhead marker */}
          <marker
            id="arrowhead"
            markerWidth="10"
            markerHeight="7"
            refX="16"
            refY="3.5"
            orient="auto"
          >
            <polygon points="0 0, 10 3.5, 0 7" fill="#64748b" />
          </marker>
        </defs>

        <rect id="canvas-bg" width="100%" height="100%" fill="#090d16" />

        {/* Pan and Zoom Group */}
        <g transform={`translate(${pan.x}, ${pan.y}) scale(${zoom})`}>
          {/* Relationships Links */}
          {layout.relationshipsWithCoords.map((rel) => {
            const sx = rel.sourceNode.x;
            const sy = rel.sourceNode.y;
            const tx = rel.targetNode.x;
            const ty = rel.targetNode.y;
            const midX = (sx + tx) / 2;
            const midY = (sy + ty) / 2;

            return (
              <g key={rel.id} className="transition-opacity">
                {/* Connecting Line */}
                <line
                  x1={sx}
                  y1={sy}
                  x2={tx}
                  y2={ty}
                  stroke="#334155"
                  strokeWidth="1.8"
                  strokeDasharray="none"
                  markerEnd="url(#arrowhead)"
                />
                {/* Labeled Relationship Badge */}
                <g transform={`translate(${midX}, ${midY})`}>
                  <rect
                    x="-42"
                    y="-9"
                    width="84"
                    height="18"
                    rx="4"
                    fill="#1e293b"
                    stroke="#475569"
                    strokeWidth="0.8"
                  />
                  <text
                    textAnchor="middle"
                    y="3"
                    fill="#94a3b8"
                    fontSize="8"
                    fontFamily="monospace"
                    fontWeight="600"
                  >
                    {rel.type}
                  </text>
                </g>
              </g>
            );
          })}

          {/* Node Circles */}
          {layout.nodesWithPos.map((node) => {
            const colors = NODE_COLORS[node.type] || NODE_COLORS.default;
            const isSelected = selectedNode?.id === node.id;

            return (
              <g
                key={node.id}
                transform={`translate(${node.x}, ${node.y})`}
                onClick={(e) => {
                  e.stopPropagation();
                  handleNodeClickInternal(node);
                }}
                className="cursor-pointer group"
              >
                {/* Outer Glow / Halo if selected */}
                {isSelected && (
                  <circle
                    r={node.radius + 8}
                    fill="none"
                    stroke="#10b981"
                    strokeWidth="2.5"
                    strokeDasharray="4 2"
                    className="animate-spin-slow"
                  />
                )}

                {/* Node Base Circle */}
                <circle
                  r={node.radius}
                  fill={colors.fill}
                  stroke={isSelected ? '#ffffff' : colors.stroke}
                  strokeWidth={node.isCenter ? 3.5 : 2}
                  className="transition-transform group-hover:scale-110 shadow-md"
                />

                {/* Inner label text */}
                <text
                  textAnchor="middle"
                  dy={node.isCenter ? "4" : "3"}
                  fill={colors.text}
                  fontSize={node.isCenter ? "11" : "9"}
                  fontWeight="bold"
                  className="pointer-events-none select-none"
                >
                  {node.label.length > 13 ? `${node.label.slice(0, 11)}..` : node.label}
                </text>

                {/* Subtitle / Type under the node */}
                <text
                  textAnchor="middle"
                  dy={node.radius + 12}
                  fill="#94a3b8"
                  fontSize="8"
                  fontWeight="600"
                  className="pointer-events-none"
                >
                  {node.type}
                </text>
              </g>
            );
          })}
        </g>
      </svg>

      {/* Node Detail Side Sheet / Inspector */}
      {selectedNode && (
        <div className="absolute bottom-3 left-3 right-3 sm:right-auto sm:w-80 bg-slate-900/95 backdrop-blur-md rounded-xl border border-slate-700 p-4 shadow-2xl z-20 text-white">
          <div className="flex items-start justify-between pb-2 mb-2 border-b border-slate-800">
            <div>
              <span className={`text-2xs uppercase font-bold px-2 py-0.5 rounded-md ${NODE_COLORS[selectedNode.type]?.tag || 'bg-slate-700'}`}>
                {selectedNode.type}
              </span>
              <h4 className="text-base font-bold text-white mt-1">{selectedNode.label}</h4>
            </div>
            <button
              onClick={() => setSelectedNode(null)}
              className="text-slate-400 hover:text-white p-1 rounded-md"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          <div className="text-xs text-slate-300 space-y-1.5 mb-3">
            <p><strong className="text-slate-400">Node ID:</strong> <span className="font-mono text-2xs text-emerald-400">{selectedNode.id}</span></p>
            {selectedNode.properties?.scientificName && (
              <p><strong className="text-slate-400">Scientific Name:</strong> <em>{selectedNode.properties.scientificName}</em></p>
            )}
            {selectedNode.properties?.lifespan && (
              <p><strong className="text-slate-400">Average Lifespan:</strong> {selectedNode.properties.lifespan} years</p>
            )}
          </div>

          {/* Connected Graph Action */}
          {selectedNode.type === 'Animal' && selectedNode.id !== centerNodeId && (
            <button
              onClick={() => navigate(`/animals/${selectedNode.id}`)}
              className="w-full flex items-center justify-center space-x-1.5 py-1.5 px-3 bg-emerald-600 hover:bg-emerald-500 rounded-lg text-xs font-semibold text-white transition-colors"
            >
              <span>View Animal Profile</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </button>
          )}

          {['Habitat', 'Diet', 'ConservationStatus', 'Continent'].includes(selectedNode.type) && (
            <button
              onClick={() => {
                const queryParam = selectedNode.type === 'ConservationStatus' ? 'status' : selectedNode.type.toLowerCase();
                navigate(`/explore?${queryParam}=${encodeURIComponent(selectedNode.label)}`);
              }}
              className="w-full flex items-center justify-center space-x-1.5 py-1.5 px-3 bg-slate-800 hover:bg-slate-700 border border-slate-600 rounded-lg text-xs font-medium text-emerald-400 hover:text-emerald-300 transition-colors"
            >
              <span>Explore all animals in {selectedNode.label}</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </button>
          )}
        </div>
      )}
    </div>
  );
}
