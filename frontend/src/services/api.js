const API_BASE = '/api';

export const api = {
  // Health
  getHealth: async () => {
    const res = await fetch(`${API_BASE}/health`);
    if (!res.ok) throw new Error('Failed to fetch system health');
    return res.json();
  },

  // Dashboard
  getStats: async () => {
    const res = await fetch(`${API_BASE}/dashboard/stats`);
    if (!res.ok) throw new Error('Failed to fetch dashboard statistics');
    return res.json();
  },

  // Animals
  getAnimals: async (filters = {}) => {
    const params = new URLSearchParams();
    if (filters.class) params.append('class', filters.class);
    if (filters.habitat) params.append('habitat', filters.habitat);
    if (filters.diet) params.append('diet', filters.diet);
    if (filters.status) params.append('status', filters.status);
    if (filters.continent) params.append('continent', filters.continent);

    const qs = params.toString() ? `?${params.toString()}` : '';
    const res = await fetch(`${API_BASE}/animals${qs}`);
    if (!res.ok) throw new Error('Failed to fetch animals');
    return res.json();
  },

  getAnimalById: async (id) => {
    const res = await fetch(`${API_BASE}/animals/${id}`);
    if (!res.ok) {
      if (res.status === 404) throw new Error('Animal not found');
      throw new Error('Failed to fetch animal details');
    }
    return res.json();
  },

  getAnimalGraph: async (id) => {
    const res = await fetch(`${API_BASE}/animals/${id}/graph`);
    if (!res.ok) throw new Error('Failed to fetch animal graph');
    return res.json();
  },

  getSampleGraph: async () => {
    const res = await fetch(`${API_BASE}/graph/sample`);
    if (!res.ok) throw new Error('Failed to fetch sample graph');
    return res.json();
  },

  // Search
  search: async (query) => {
    const res = await fetch(`${API_BASE}/search?q=${encodeURIComponent(query)}`);
    if (!res.ok) throw new Error('Search failed');
    return res.json();
  },

  // Categorical Search
  getByHabitat: async (habitat) => {
    const res = await fetch(`${API_BASE}/habitats/${encodeURIComponent(habitat)}/animals`);
    if (!res.ok) throw new Error('Failed to fetch animals by habitat');
    return res.json();
  },

  getByConservation: async (status) => {
    const res = await fetch(`${API_BASE}/conservation/${encodeURIComponent(status)}/animals`);
    if (!res.ok) throw new Error('Failed to fetch animals by conservation status');
    return res.json();
  },

  getByDiet: async (diet) => {
    const res = await fetch(`${API_BASE}/diets/${encodeURIComponent(diet)}/animals`);
    if (!res.ok) throw new Error('Failed to fetch animals by diet');
    return res.json();
  },

  getByContinent: async (continent) => {
    const res = await fetch(`${API_BASE}/continents/${encodeURIComponent(continent)}/animals`);
    if (!res.ok) throw new Error('Failed to fetch animals by continent');
    return res.json();
  },

  // Ask Knowledge Graph
  askQuestion: async (question) => {
    const res = await fetch(`${API_BASE}/queries/ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question })
    });
    if (!res.ok) throw new Error('Failed to process natural language query');
    return res.json();
  },

  getExampleQuestions: async () => {
    const res = await fetch(`${API_BASE}/queries/examples`);
    if (!res.ok) throw new Error('Failed to fetch example questions');
    return res.json();
  }
};
