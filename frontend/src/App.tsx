import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { SatQueryProvider } from './context/SatQueryContext';
import { Header } from './components/Header';
import { Home } from './pages/Home';
import { UploadQuery } from './pages/UploadQuery';
import { Results } from './pages/Results';

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <SatQueryProvider>
        <div className="app-container">
          {/* Main Top Header */}
          <Header />

          {/* Page Routing Container */}
          <main className="main-content">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/analyze" element={<UploadQuery />} />
              <Route path="/results" element={<Results />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>

          {/* System Footer */}
          <footer style={{
            borderTop: '1px solid var(--border-subtle)',
            padding: '24px 32px',
            background: 'rgba(5, 8, 16, 0.95)',
            fontSize: 12,
            color: 'var(--text-muted)'
          }}>
            <div style={{
              maxWidth: 1440,
              margin: '0 auto',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              flexWrap: 'wrap',
              gap: 12
            }}>
              <div>
                <strong>SatQuery AI</strong> • SIH26167 Remote Sensing Vision-Language Assistant
                <span style={{ margin: '0 8px', opacity: 0.4 }}>|</span>
                <span>Indian Space Research Organisation (ISRO)</span>
              </div>

              <div style={{ display: 'flex', gap: 16 }}>
                <span>Fine-Tuning Dataset: <strong style={{ color: 'var(--text-secondary)' }}>BigEarthNet.txt</strong></span>
                <span>Benchmarks: <strong style={{ color: 'var(--text-secondary)' }}>VRSBench • RSVQA • CDVQA</strong></span>
              </div>
            </div>
          </footer>
        </div>
      </SatQueryProvider>
    </BrowserRouter>
  );
};

export default App;
