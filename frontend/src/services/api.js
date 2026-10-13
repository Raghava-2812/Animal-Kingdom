/**
 * Frontend API Client Service.
 *
 * Provides a typed interface for communicating with the FastAPI backend.
 * Automatically resolves the base URL:
 * - Uses `VITE_API_URL` when deployed in production (e.g. on Render).
 * - Defaults to `/api` proxy in local development (configured via Vite).
 */

const API_BASE = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL.replace(/\/+$/, '')}/api`
  : '/api';

export const api = {
  /**
   * Health Check
   * Fetches backend status and Neo4j connectivity.
   * @returns {Promise<{status: string, neo4jConnected: boolean, databaseUri: string, environment: string}>}
   */
  getHealth: async () => {
    const res = await fetch(`${API_BASE}/health`);
    if (!res.ok) throw new Error('Failed to fetch system health');
    return res.json();
  },

  /**
   * Dashboard Statistics
   * Fetches high-level metrics for dashboard cards (total animals, habitats, etc.).
   * @returns {Promise<{totalAnimals: number, totalSpecies: number, totalHabitats: number, totalFoods: number, totalEndangeredAnimals: number, totalContinents: number, neo4jConnected: boolean}>}
   */
  getStats: async () => {
    const res = await fetch(`${API_BASE}/dashboard/stats`);
    if (!res.ok) throw new Error('Failed to fetch dashboard statistics');
    return res.json();
  },

  /**
   * Filtered Animal Listing
   * Fetches animal summaries based on multiple optional facet filters.
   * @param {Object} filters - Active filter options (class, habitat, diet, status, continent).
   * @returns {Promise<Array<Object>>} List of animal summary objects.
   */
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

  /**
   * Single Animal Details
   * Fetches full profile, taxonomy, prey items, and habitat links for an animal ID.
   * @param {string} id - Animal entity identifier (e.g. 'animal_tiger').
   * @returns {Promise<Object>} Full animal detail object.
   */
  getAnimalById: async (id) => {
    const res = await fetch(`${API_BASE}/animals/${id}`);
    if (!res.ok) {
      if (res.status === 404) throw new Error('Animal not found');
      throw new Error('Failed to fetch animal details');
    }
    return res.json();
  },

  /**
   * Single Animal Graph Network
   * Fetches nodes and edges representing an animal's ego-network.
   * @param {string} id - Animal entity identifier.
   * @returns {Promise<{nodes: Array, relationships: Array}>} Vis.js compatible graph payload.
   */
  getAnimalGraph: async (id) => {
    const res = await fetch(`${API_BASE}/animals/${id}/graph`);
    if (!res.ok) throw new Error('Failed to fetch animal graph');
    return res.json();
  },

  /**
   * Ecosystem Sample Graph
   * Fetches interconnected multi-animal network for the interactive graph explorer.
   * @returns {Promise<{nodes: Array, relationships: Array}>} Graph nodes and relationships.
   */
  getSampleGraph: async () => {
    const res = await fetch(`${API_BASE}/graph/sample`);
    if (!res.ok) throw new Error('Failed to fetch sample graph');
    return res.json();
  },

  /**
   * Substring Text Search
   * Searches animals by common or scientific name.
   * @param {string} query - Search term.
   * @returns {Promise<Array<Object>>} Matching animal summaries.
   */
  search: async (query) => {
    const res = await fetch(`${API_BASE}/search?q=${encodeURIComponent(query)}`);
    if (!res.ok) throw new Error('Search failed');
    return res.json();
  },

  /**
   * Animals by Habitat Biome
   * @param {string} habitat - Habitat name (e.g. 'Ocean', 'Forest').
   * @returns {Promise<Array<Object>>} Resident animals.
   */
  getByHabitat: async (habitat) => {
    const res = await fetch(`${API_BASE}/habitats/${encodeURIComponent(habitat)}/animals`);
    if (!res.ok) throw new Error('Failed to fetch animals by habitat');
    return res.json();
  },

  /**
   * Animals by Conservation Status
   * @param {string} status - IUCN Status (e.g. 'Endangered').
   * @returns {Promise<Array<Object>>} Animals with status.
   */
  getByConservation: async (status) => {
    const res = await fetch(`${API_BASE}/conservation/${encodeURIComponent(status)}/animals`);
    if (!res.ok) throw new Error('Failed to fetch animals by conservation status');
    return res.json();
  },

  /**
   * Animals by Dietary Classification
   * @param {string} diet - Diet type (e.g. 'Carnivore').
   * @returns {Promise<Array<Object>>} Animals with diet.
   */
  getByDiet: async (diet) => {
    const res = await fetch(`${API_BASE}/diets/${encodeURIComponent(diet)}/animals`);
    if (!res.ok) throw new Error('Failed to fetch animals by diet');
    return res.json();
  },

  /**
   * Animals by Continent
   * @param {string} continent - Continent name (e.g. 'Asia', 'Africa').
   * @returns {Promise<Array<Object>>} Native animals.
   */
  getByContinent: async (continent) => {
    const res = await fetch(`${API_BASE}/continents/${encodeURIComponent(continent)}/animals`);
    if (!res.ok) throw new Error('Failed to fetch animals by continent');
    return res.json();
  },

  /**
   * Natural Language Question Query
   * Submits a plain English query to the Cypher translation engine.
   * @param {string} question - Question text (e.g. 'Show endangered animals that live in forests').
   * @returns {Promise<{question: string, detectedFilters: Object, cypherQuery: string, results: Array, resultCount: number, explanation: string}>}
   */
  askQuestion: async (question) => {
    const res = await fetch(`${API_BASE}/queries/ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question })
    });
    if (!res.ok) throw new Error('Failed to process natural language query');
    return res.json();
  },

  /**
   * Predefined Query Examples
   * Fetches curated academic questions to populate the query suggestion pills.
   * @returns {Promise<Array<string>>} List of example questions.
   */
  getExampleQuestions: async () => {
    const res = await fetch(`${API_BASE}/queries/examples`);
    if (!res.ok) throw new Error('Failed to fetch example questions');
    return res.json();
  }
};
