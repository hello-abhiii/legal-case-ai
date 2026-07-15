import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import confetti from 'canvas-confetti';
import { FileText, Play, HelpCircle, ChevronRight, ShieldAlert, Sparkles } from 'lucide-react';
import GlassCard from './GlassCard';

interface PageAnalyzeProps {
  onOutcomeChange: (outcome: 'Conviction' | 'Acquittal' | null) => void;
  onActiveObjectChange: (obj: 'scale' | 'gavel' | 'books') => void;
  onPrecedentSelect: (caseData: any) => void;
  apiEndpoint: string;
}

export default function PageAnalyze({
  onOutcomeChange,
  onActiveObjectChange,
  onPrecedentSelect,
  apiEndpoint
}: PageAnalyzeProps) {
  const [facts, setFacts] = useState('');
  const [section, setSection] = useState('');
  const [court, setCourt] = useState('District Court');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const quickTemplates = [
    { name: 'Theft (379)', facts: 'accused stole gold chain from victim on road', section: 'IPC 379', court: 'District Court' },
    { name: 'Cheating (420)', facts: 'accused cheated investors in fake scheme promising returns', section: 'IPC 420', court: 'High Court' },
    { name: 'Assault (323)', facts: 'accused assaulted complainant during property dispute', section: 'IPC 323', court: 'District Court' },
    { name: 'Forgery (468)', facts: 'accused forged land documents to transfer property illegally', section: 'IPC 468', court: 'High Court' },
  ];

  const handleQuickFill = (tmpl: typeof quickTemplates[0]) => {
    setFacts(tmpl.facts);
    setSection(tmpl.section);
    setCourt(tmpl.court);
    onActiveObjectChange('books');
  };

  const handleRunPrediction = async () => {
    if (!facts.trim() || !section.trim()) {
      alert('Please provide both case facts and a legal section.');
      return;
    }

    setLoading(true);
    setResult(null);
    onOutcomeChange(null);
    onActiveObjectChange('scale'); // Switch to scale for outcome determination

    try {
      const res = await fetch(`${apiEndpoint}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ facts: facts.trim(), section: section.trim(), court })
      });
      
      if (!res.ok) {
        throw new Error('API Request Failed');
      }

      const data = await res.json();
      setResult(data);

      const isConviction = data.predicted_outcome === 'Conviction';
      onOutcomeChange(data.predicted_outcome);

      // Confetti celebration for acquittal!
      if (!isConviction) {
        confetti({
          particleCount: 80,
          spread: 60,
          origin: { y: 0.7 },
          colors: ['#34d399', '#60a5fa', '#a78bfa']
        });
      }

      // Add to localStorage history
      const localHistory = JSON.parse(localStorage.getItem('legalai_predictions') || '[]');
      const newPrediction = {
        facts: facts.trim(),
        section: section.trim(),
        court,
        outcome: data.predicted_outcome,
        confidence: data.confidence,
        time: new Date().toLocaleString()
      };
      localHistory.unshift(newPrediction);
      localStorage.setItem('legalai_predictions', JSON.stringify(localHistory.slice(0, 20)));

    } catch (e) {
      alert('Connection Error: The backend server might be asleep or unavailable. Please retry in 30-50 seconds.');
      onActiveObjectChange('gavel');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="layout-grid" style={{ padding: '40px 0' }}>
      
      {/* LEFT COLUMN: Input Form */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
        <GlassCard delay={0.05} hoverEffect={false}>
          <div style={{ padding: '32px' }}>
            
            {/* Header */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '28px' }}>
              <div style={{
                width: '40px',
                height: '40px',
                borderRadius: '12px',
                background: 'rgba(59, 130, 246, 0.05)',
                border: '1px solid rgba(59, 130, 246, 0.12)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'var(--accent-blue)'
              }}>
                <FileText size={20} />
              </div>
              <div>
                <h2 style={{ fontSize: '18px', fontWeight: 600, color: '#fff', margin: 0 }}>Case Details</h2>
                <p style={{ fontSize: '12px', color: 'var(--text-secondary)', margin: '4px 0 0' }}>
                  Provide legal facts to evaluate court outcome probabilities.
                </p>
              </div>
            </div>

            {/* Facts Input */}
            <div style={{ marginBottom: '24px' }}>
              <label style={{ display: 'block', fontSize: '11px', fontWeight: 600, color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '10px' }}>
                Case Facts
              </label>
              <textarea
                value={facts}
                onChange={(e) => setFacts(e.target.value)}
                onFocus={() => onActiveObjectChange('books')}
                rows={5}
                className="glass-input"
                placeholder="Describe the incident, involved actions, and timeline details..."
                style={{ resize: 'none', lineHeight: '1.6' }}
              />
            </div>

            {/* Split section/court */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '28px' }}>
              <div>
                <label style={{ display: 'block', fontSize: '11px', fontWeight: 600, color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '10px' }}>
                  Legal Section
                </label>
                <input
                  type="text"
                  value={section}
                  onChange={(e) => setSection(e.target.value)}
                  onFocus={() => onActiveObjectChange('gavel')}
                  className="glass-input"
                  placeholder="e.g. IPC 379"
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '11px', fontWeight: 600, color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '10px' }}>
                  Court Type
                </label>
                <select
                  value={court}
                  onChange={(e) => setCourt(e.target.value)}
                  className="glass-input"
                  style={{
                    appearance: 'none',
                    cursor: 'pointer',
                    background: 'rgba(255, 255, 255, 0.02) url("data:image/svg+xml,%3csvg xmlns=\'http://www.w3.org/2000/svg\' fill=\'none\' viewBox=\'0 0 20 20\'%3e%3cpath stroke=\'%23a1a1aa\' stroke-linecap=\'round\' stroke-linejoin=\'round\' stroke-width=\'1.5\' d=\'M6 8l4 4 4-4\'/%3e%3c/svg%3e") no-repeat right 12px center',
                    backgroundSize: '18px',
                    paddingRight: '36px'
                  }}
                >
                  <option value="District Court" style={{ background: '#0e0e11' }}>District Court</option>
                  <option value="Sessions Court" style={{ background: '#0e0e11' }}>Sessions Court</option>
                  <option value="High Court" style={{ background: '#0e0e11' }}>High Court</option>
                  <option value="Supreme Court" style={{ background: '#0e0e11' }}>Supreme Court</option>
                </select>
              </div>
            </div>

            {/* Quick Fills */}
            <div style={{ borderTop: '1px solid rgba(255, 255, 255, 0.05)', paddingTop: '20px', marginBottom: '28px' }}>
              <div style={{ fontSize: '11px', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '12px' }}>
                Quick Fill Templates
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                {quickTemplates.map((tmpl) => (
                  <button
                    key={tmpl.name}
                    type="button"
                    onClick={() => handleQuickFill(tmpl)}
                    style={{
                      fontSize: '11px',
                      padding: '8px 14px',
                      background: 'rgba(255,255,255,0.02)',
                      border: '1px solid rgba(255,255,255,0.06)',
                      borderRadius: 'var(--border-radius-sm)',
                      color: 'var(--text-secondary)',
                      cursor: 'pointer',
                      transition: 'all 0.2s',
                    }}
                    onMouseOver={(e) => { e.currentTarget.style.color = '#fff'; e.currentTarget.style.borderColor = 'rgba(59,130,246,0.3)'; }}
                    onMouseOut={(e) => { e.currentTarget.style.color = 'var(--text-secondary)'; e.currentTarget.style.borderColor = 'rgba(255,255,255,0.06)'; }}
                  >
                    {tmpl.name}
                  </button>
                ))}
              </div>
            </div>

            {/* Run Button */}
            <button
              onClick={handleRunPrediction}
              disabled={loading}
              className="premium-btn premium-btn-primary"
              style={{ width: '100%', padding: '16px' }}
            >
              {loading ? (
                <>
                  <span className="premium-spinner"></span>
                  Running Models...
                </>
              ) : (
                <>
                  <Play size={15} fill="currentColor" />
                  Analyze Case Material
                </>
              )}
            </button>

          </div>
        </GlassCard>
      </div>

      {/* RIGHT COLUMN: Output Panel */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
        <AnimatePresence mode="wait">
          
          {/* 1. INITIAL PLACEHOLDER STATE */}
          {!loading && !result && (
            <motion.div
              key="placeholder"
              initial={{ opacity: 0, scale: 0.98 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.98 }}
              transition={{ duration: 0.4 }}
              style={{ height: '100%', minHeight: '350px' }}
            >
              <GlassCard hoverEffect={false} className="glass-card-placeholder" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', padding: '40px', borderStyle: 'dashed', background: 'transparent' }}>
                <div style={{
                  width: '56px',
                  height: '56px',
                  borderRadius: '16px',
                  background: 'rgba(255, 255, 255, 0.02)',
                  border: '1px solid rgba(255, 255, 255, 0.06)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'var(--text-muted)',
                  marginBottom: '20px'
                }}>
                  <HelpCircle size={24} />
                </div>
                <h3 style={{ fontSize: '16px', fontWeight: 500, color: 'var(--text-secondary)', margin: '0 0 8px' }}>
                  Awaiting Input Facts
                </h3>
                <p style={{ fontSize: '13px', color: 'var(--text-muted)', textAlign: 'center', margin: 0, maxWidth: '280px', lineHeight: '1.5' }}>
                  Submit case specifics on the left to activate deep predictive inference metrics.
                </p>
              </GlassCard>
            </motion.div>
          )}

          {/* 2. LOADING STATE SKELETON */}
          {loading && (
            <motion.div
              key="loading"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}
            >
              <GlassCard hoverEffect={false} style={{ padding: '32px' }}>
                <div style={{ height: '24px', width: '40%', background: 'rgba(255, 255, 255, 0.03)', borderRadius: '4px', marginBottom: '32px', animation: 'pulse 1.5s infinite' }} />
                <div style={{ height: '48px', width: '80%', background: 'rgba(255, 255, 255, 0.03)', borderRadius: '8px', marginBottom: '24px', animation: 'pulse 1.5s infinite' }} />
                <div style={{ height: '10px', width: '100%', background: 'rgba(255, 255, 255, 0.02)', borderRadius: '4px', marginBottom: '12px' }} />
                <div style={{ height: '10px', width: '90%', background: 'rgba(255, 255, 255, 0.02)', borderRadius: '4px' }} />
              </GlassCard>
              <GlassCard hoverEffect={false} style={{ padding: '32px' }}>
                <div style={{ height: '20px', width: '30%', background: 'rgba(255, 255, 255, 0.03)', borderRadius: '4px', marginBottom: '20px', animation: 'pulse 1.5s infinite' }} />
                <div style={{ height: '36px', width: '100%', background: 'rgba(255, 255, 255, 0.02)', borderRadius: '6px' }} />
              </GlassCard>
            </motion.div>
          )}

          {/* 3. ANALYZED RESULTS PANEL */}
          {!loading && result && (
            <motion.div
              key="results"
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
              style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}
            >
              {/* Result Summary Block */}
              <GlassCard hoverEffect={false} style={{ padding: '32px', position: 'relative', overflow: 'hidden' }}>
                
                {/* Glowing bar top */}
                <div style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  right: 0,
                  height: '3px',
                  background: result.predicted_outcome === 'Conviction'
                    ? 'linear-gradient(90deg, var(--accent-red), transparent)'
                    : 'linear-gradient(90deg, var(--accent-green), transparent)'
                }} />

                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '28px' }}>
                  <h3 style={{ fontSize: '15px', fontWeight: 600, color: '#fff', margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Sparkles size={16} style={{ color: 'var(--accent-blue)' }} />
                    Prediction Outcome
                  </h3>
                  <span className={`glass-badge ${result.predicted_outcome === 'Conviction' ? 'glass-badge-conviction' : 'glass-badge-acquittal'}`}>
                    {result.predicted_outcome}
                  </span>
                </div>

                <div style={{ marginBottom: '24px' }}>
                  <div style={{ fontSize: '11px', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '8px' }}>
                    Identified Outcome
                  </div>
                  <div style={{
                    fontSize: '32px',
                    fontWeight: 700,
                    fontFamily: 'var(--font-heading)',
                    color: result.predicted_outcome === 'Conviction' ? '#f87171' : '#34d399',
                    letterSpacing: '-0.02em'
                  }}>
                    {result.predicted_outcome}
                  </div>
                </div>

                {/* Progress bar confidence score */}
                <div style={{
                  background: 'rgba(255, 255, 255, 0.015)',
                  padding: '20px',
                  borderRadius: 'var(--border-radius-md)',
                  border: '1px solid rgba(255, 255, 255, 0.03)'
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '10px' }}>
                    <span style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>Confidence Score</span>
                    <span style={{ fontSize: '20px', fontWeight: 700, color: '#fff', fontFamily: 'var(--font-heading)' }}>
                      {result.confidence}
                    </span>
                  </div>
                  <div className="premium-progress-bg">
                    <div
                      className="premium-progress-bar"
                      style={{
                        width: result.confidence,
                        background: result.predicted_outcome === 'Conviction'
                          ? 'linear-gradient(90deg, #dc2626, #ef4444)'
                          : 'linear-gradient(90deg, #059669, #10b981)'
                      }}
                    />
                  </div>
                </div>

              </GlassCard>

              {/* Model Reasoning */}
              <GlassCard hoverEffect={false} style={{ padding: '32px' }}>
                <h3 style={{ fontSize: '15px', fontWeight: 600, color: '#fff', margin: '0 0 20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                  {result.predicted_outcome === 'Conviction' ? (
                    <ShieldAlert size={16} style={{ color: 'var(--accent-red)' }} />
                  ) : (
                    <Sparkles size={16} style={{ color: 'var(--accent-green)' }} />
                  )}
                  Model Reasoning
                </h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                  {result.explanation && result.explanation.map((exp: string, i: number) => (
                    <div
                      key={i}
                      style={{
                        display: 'flex',
                        alignItems: 'flex-start',
                        gap: '12px',
                        fontSize: '13px',
                        color: 'var(--text-secondary)',
                        background: 'rgba(255,255,255,0.01)',
                        padding: '12px 16px',
                        borderRadius: 'var(--border-radius-sm)',
                        border: '1px solid rgba(255,255,255,0.03)',
                        lineHeight: '1.5'
                      }}
                    >
                      <ChevronRight size={14} style={{ color: 'var(--accent-purple)', flexShrink: 0, marginTop: '3px' }} />
                      <span>{exp}</span>
                    </div>
                  ))}
                </div>
              </GlassCard>

              {/* Similar Precedents */}
              <GlassCard hoverEffect={false} style={{ padding: '32px' }}>
                <h3 style={{ fontSize: '15px', fontWeight: 600, color: '#fff', margin: '0 0 20px' }}>
                  Relevant Precedents
                </h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                  {result.similar_cases && result.similar_cases.map((cs: any, idx: number) => (
                    <button
                      key={idx}
                      onClick={() => onPrecedentSelect(cs)}
                      className="precedent-btn"
                    >
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                        <div style={{ fontWeight: 600, fontSize: '14px', color: '#fff' }}>
                          {cs.title}
                        </div>
                        <ChevronRight size={14} style={{ color: 'var(--text-muted)' }} />
                      </div>
                      <p style={{ fontSize: '12px', color: 'var(--text-secondary)', margin: '0 0 12px', overflow: 'hidden', textOverflow: 'ellipsis', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', lineHeight: '1.5' }}>
                        {cs.facts}
                      </p>
                      <div style={{ display: 'flex', gap: '8px' }}>
                        <span className="glass-badge" style={{ fontSize: '9px', padding: '4px 8px' }}>
                          {cs.section}
                        </span>
                        <span className={`glass-badge ${cs.outcome === 'Conviction' ? 'glass-badge-conviction' : 'glass-badge-acquittal'}`} style={{ fontSize: '9px', padding: '4px 8px' }}>
                          {cs.outcome}
                        </span>
                      </div>
                    </button>
                  ))}
                </div>
              </GlassCard>

            </motion.div>
          )}

        </AnimatePresence>
      </div>

    </div>
  );
}
