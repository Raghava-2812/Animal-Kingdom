/**
 * Frontend Client Entry Point.
 *
 * Mounts the root React component tree into the DOM root container ('#root')
 * wrapped in React.StrictMode for detecting side-effects and deprecated APIs during development.
 */

import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
