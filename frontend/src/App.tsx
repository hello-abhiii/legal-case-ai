import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Scale, Clock, BarChart2, Info } from 'lucide-react';

import ThreeCanvas from './components/ThreeCanvas';
import PageAnalyze from './components/PageAnalyze';
import PageHistory from './components/PageHistory';
import PageStats from './components/PageStats';
import PageAbout from './components/PageAbout';
import PrecedentModal from './components/PrecedentModal';

const API_ENDPOINT = 'https://legal-case-ai.onrender.com';

export default function App() {
  const [activePage, setActivePage] = useState<'analyze' | 'history' | 'stats' | 'about'>('analyze');
  const [outcome, setOutcome] = useState<'Conviction' | 'Acquittal' | null>(null);
  const [activeObject, setActiveObject] = useState<'scale' | 'gavel' | 'books'>('gavel');
  const [selectedPrecedent, setSelectedPrecedent] = useState<any>(null);
  const [modalOpen, setModalOpen] = useState(false);

  const handlePrecedentSelect = (caseData: any) => {
    setSelectedPrecedent(caseData);
    setModalOpen(true);
  };

  const navItems = [
    { id: 'analyze', label: 'Analyze', icon: Scale },
    { id: 'history', label: 'History', icon: Clock },
    { id: 'stats', label: 'Statistics', icon: BarChart2 },
    { id: 'about', label: 'About', icon: Info },
  ] as const;

  return (
    <div className="main-content">
      {/* 1. AMBIENT GLOW BACKDROP */}
      <div className="ambient-bg">
        <div className="glow-blob glow-blue" />
        <div className="glow-blob glow-purple" />
        <div className="glow-blob glow-center" />
      </div>

      {/* 2. TOP BANNER */}
      <div style={{
        background: 'rgba(10, 10, 12, 0.8)',
        color: 'var(--text-secondary)',
        fontSize: '11px',
        fontWeight: 500,
        padding: '10px 24px',
        textAlign: 'center',
        textTransform: 'uppercase',
        letterSpacing: '0.12em',
        borderBottom: '1px solid rgba(255, 255, 255, 0.05)',
        position: 'relative',
        zIndex: 50
      }}>
        <span style={{ color: 'var(--accent-blue)', marginRight: '6px' }}>✦</span>
        Academic Research Prototype — Natural Language Processing & Juridical Prediction Models
      </div>

      {/* 3. STICKY GLASS NAVBAR */}
      <nav className="glass-nav">
        <div className="layout-container" style={{ display: 'flex', alignItems: 'center', height: '72px', justifyContent: 'space-between' }}>
          
          {/* Logo Brand */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{
              width: '38px',
              height: '38px',
              borderRadius: '10px',
              background: 'linear-gradient(135deg, var(--accent-blue), var(--accent-purple))',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 4px 12px rgba(139, 92, 246, 0.25)',
              color: '#fff'
            }}>
              <Scale size={18} />
            </div>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <span style={{ fontFamily: 'var(--font-heading)', fontSize: '18px', fontWeight: 700, letterSpacing: '-0.02em', color: '#fff' }}>
                  LegalAI
                </span>
                <span className="glass-badge" style={{ fontSize: '9px', padding: '3px 8px', borderColor: 'rgba(59, 130, 246, 0.15)', color: 'var(--accent-blue)' }}>
                  Beta
                </span>
              </div>
              <div style={{ fontSize: '10px', color: 'var(--text-muted)', fontWeight: 500 }}>
                Court Decision Framework
              </div>
            </div>
          </div>

          {/* Navigation Links */}
          <div style={{ display: 'flex', gap: '4px' }}>
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activePage === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    setActivePage(item.id);
                    if (item.id === 'analyze') {
                      onHtmlClickReset();
                    }
                  }}
                  style={{
                    background: isActive ? 'rgba(255, 255, 255, 0.04)' : 'transparent',
                    border: '1px solid ' + (isActive ? 'rgba(255,255,255,0.06)' : 'transparent'),
                    borderRadius: 'var(--border-radius-sm)',
                    color: isActive ? '#fff' : 'var(--text-secondary)',
                    padding: '8px 16px',
                    fontSize: '13px',
                    fontWeight: 500,
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    transition: 'all 0.2s cubic-bezier(0.16, 1, 0.3, 1)'
                  }}
                  onMouseOver={(e) => {
                    if (!isActive) e.currentTarget.style.color = '#fff';
                  }}
                  onMouseOut={(e) => {
                    if (!isActive) e.currentTarget.style.color = 'var(--text-secondary)';
                  }}
                >
                  <Icon size={14} />
                  {item.label}
                </button>
              );
            })}
          </div>

        </div>
      </nav>

      {/* 4. MAIN PAGE DISPLAY CONTENT */}
      <div className="layout-container" style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        
        {/* HERO HEADER AREA (Only on Analyze tab) */}
        {activePage === 'analyze' && (
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '40px', alignItems: 'center', padding: '60px 0 20px' }}>
            
            {/* Left Hero Description */}
            <div style={{ flex: '1 1 450px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
              <span className="glass-badge" style={{ alignSelf: 'flex-start', background: 'rgba(255,255,255,0.02)', color: 'var(--text-secondary)' }}>
                <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: 'var(--accent-blue)', display: 'inline-block', marginRight: '6px', animation: 'pulse 2s infinite' }} />
                Natural Language NLP & Classifier Evaluation
              </span>
              <h1 className="gradient-text" style={{ fontSize: '48px', fontWeight: 700, lineHeight: '1.1', margin: 0, fontFamily: 'var(--font-heading)' }}>
                Predict Trial Outcomes <br />
                <span className="glow-gradient-text" style={{ fontWeight: 700 }}>Powered by Legal AI</span>
              </h1>
              <p style={{ fontSize: '15px', color: 'var(--text-secondary)', lineHeight: '1.6', margin: 0, maxWidth: '480px', fontWeight: 300 }}>
                Analyze complex case narratives, trace statutory precedents, and gauge court probability outcomes through TF-IDF similarities and SVM model forecasts.
              </p>
              
              {/* Little dashboard numbers */}
              <div style={{
                display: 'inline-flex',
                gap: '24px',
                background: 'rgba(255, 255, 255, 0.01)',
                border: '1px solid rgba(255, 255, 255, 0.03)',
                padding: '14px 28px',
                borderRadius: 'var(--border-radius-md)',
                width: 'fit-content',
                marginTop: '10px'
              }}>
                <div>
                  <div style={{ fontSize: '18px', fontWeight: 700, color: '#fff', fontFamily: 'var(--font-heading)' }}>94.0%</div>
                  <div style={{ fontSize: '9px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', marginTop: '2px' }}>F1 Accuracy</div>
                </div>
                <div style={{ width: '1px', background: 'rgba(255,255,255,0.08)' }} />
                <div>
                  <div style={{ fontSize: '18px', fontWeight: 700, color: '#fff', fontFamily: 'var(--font-heading)' }}>4.5k+</div>
                  <div style={{ fontSize: '9px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', marginTop: '2px' }}>DB Cases</div>
                </div>
                <div style={{ width: '1px', background: 'rgba(255,255,255,0.08)' }} />
                <div>
                  <div style={{ fontSize: '18px', fontWeight: 700, color: '#fff', fontFamily: 'var(--font-heading)' }}>29</div>
                  <div style={{ fontSize: '9px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', marginTop: '2px' }}>IPC Sections</div>
                </div>
              </div>
            </div>

            {/* Right Hero: R3F Canvas showing the Active 3D Element */}
            <div style={{ flex: '1 1 350px', height: '380px', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', position: 'relative' }}>
              <ThreeCanvas activeObject={activeObject} outcome={outcome} />
              
              {/* Floating manual 3D Asset toggle controller */}
              <div style={{
                position: 'absolute',
                bottom: '10px',
                display: 'flex',
                gap: '8px',
                background: 'rgba(10, 10, 12, 0.6)',
                backdropFilter: 'blur(10px)',
                padding: '6px',
                borderRadius: '99px',
                border: '1px solid rgba(255, 255, 255, 0.05)',
                boxShadow: '0 4px 20px rgba(0,0,0,0.3)',
                zIndex: 20
              }}>
                {[
                  { id: 'scale', label: 'Scale ⚖️' },
                  { id: 'gavel', label: 'Gavel 🔨' },
                  { id: 'books', label: 'Books 📚' }
                ].map((obj) => (
                  <button
                    key={obj.id}
                    onClick={() => setActiveObject(obj.id as any)}
                    style={{
                      background: activeObject === obj.id ? 'rgba(255, 255, 255, 0.08)' : 'transparent',
                      border: 'none',
                      borderRadius: '99px',
                      color: activeObject === obj.id ? '#fff' : 'var(--text-secondary)',
                      fontSize: '11px',
                      padding: '6px 14px',
                      fontWeight: 500,
                      cursor: 'pointer',
                      transition: 'all 0.2s',
                    }}
                  >
                    {obj.label}
                  </button>
                ))}
              </div>
            </div>

          </div>
        )}

        {/* 5. TAB RENDERING PORTAL */}
        <div style={{ position: 'relative', zIndex: 10, flex: 1 }}>
          <AnimatePresence mode="wait">
            <motion.div
              key={activePage}
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -15 }}
              transition={{ duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
            >
              {activePage === 'analyze' && (
                <PageAnalyze
                  apiEndpoint={API_ENDPOINT}
                  onOutcomeChange={setOutcome}
                  onActiveObjectChange={setActiveObject}
                  onPrecedentSelect={handlePrecedentSelect}
                />
              )}
              {activePage === 'history' && <PageHistory />}
              {activePage === 'stats' && <PageStats />}
              {activePage === 'about' && <PageAbout />}
            </motion.div>
          </AnimatePresence>
        </div>

      </div>

      {/* 6. FOOTER */}
      <footer style={{
        borderTop: '1px solid rgba(255, 255, 255, 0.05)',
        background: 'rgba(3, 3, 3, 0.8)',
        backdropFilter: 'blur(16px)',
        position: 'relative',
        zIndex: 10,
        marginTop: '60px',
        padding: '32px 0'
      }}>
        <div className="layout-container" style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center', gap: '20px', fontSize: '12px', color: 'var(--text-muted)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#10b981' }} />
            <span>© 2026/2027 LegalAI Laboratory — IR & ML Department.</span>
          </div>
          <div style={{ display: 'flex', gap: '24px' }}>
            <a href="https://legal-case-ai.onrender.com" target="_blank" rel="noopener noreferrer" style={{ color: 'var(--text-muted)', textDecoration: 'none', transition: 'color 0.2s' }} onMouseOver={(e) => e.currentTarget.style.color = 'var(--text-secondary)'} onMouseOut={(e) => e.currentTarget.style.color = 'var(--text-muted)'}>
              Backend API
            </a>
            <a href="https://github.com/hello-abhiii/legal-case-ai" target="_blank" rel="noopener noreferrer" style={{ color: 'var(--text-muted)', textDecoration: 'none', transition: 'color 0.2s' }} onMouseOver={(e) => e.currentTarget.style.color = 'var(--text-secondary)'} onMouseOut={(e) => e.currentTarget.style.color = 'var(--text-muted)'}>
              GitHub Repository
            </a>
          </div>
        </div>
      </footer>

      {/* 7. PRECEDENT DETAIL MODAL */}
      <PrecedentModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        caseData={selectedPrecedent}
      />
    </div>
  );

  // Small helper to reset object on page click
  function onHtmlClickReset() {
    setOutcome(null);
    setActiveObject('gavel');
  }
}
