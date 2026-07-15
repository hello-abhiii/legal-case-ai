import { ShieldAlert, Cpu, Award, Link2 } from 'lucide-react';
import GlassCard from './GlassCard';

export default function PageAbout() {
  const techs = [
    { title: 'Backend API', desc: 'Python-based FastAPI microservice' },
    { title: 'Machine Learning', desc: 'Scikit-learn (SVM / Random Forest Classifiers)' },
    { title: 'NLP Extraction', desc: 'TF-IDF & Cosine Similarity for search retrieval' },
    { title: 'Interactive Web', desc: 'React, Three Fiber, and Framer Motion' },
  ];

  return (
    <div style={{ padding: '40px 0', maxWidth: '800px', margin: '0 auto' }}>
      
      <GlassCard hoverEffect={false} style={{ position: 'relative', overflow: 'hidden' }}>
        
        {/* Glow Header bar */}
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: '4px',
          background: 'linear-gradient(90deg, var(--accent-blue), var(--accent-purple))'
        }} />

        <div style={{ padding: '40px' }}>
          
          {/* Header */}
          <h2 style={{ fontSize: '26px', fontWeight: 700, color: '#fff', margin: '0 0 6px' }}>
            About LegalAI
          </h2>
          <div style={{ fontSize: '11px', fontWeight: 600, color: 'var(--accent-blue)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '28px' }}>
            Academic Research Project — 2026/2027
          </div>

          {/* Description */}
          <p style={{ fontSize: '14px', color: 'var(--text-secondary)', lineHeight: '1.7', margin: '0 0 32px' }}>
            LegalAI functions as a decision-support laboratory prototype for legal researchers and scholars. 
            By processing court records, case facts, and historical outcomes, it provides rapid classification predictions 
            and vectors similar precedents to automate qualitative document parsing.
          </p>

          {/* Technology block */}
          <h3 style={{ fontSize: '15px', fontWeight: 600, color: '#fff', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Cpu size={16} style={{ color: 'var(--accent-purple)' }} />
            Core Architecture
          </h3>
          
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '32px' }}>
            {techs.map((t, idx) => (
              <div
                key={idx}
                style={{
                  padding: '16px',
                  background: 'rgba(255,255,255,0.01)',
                  border: '1px solid rgba(255,255,255,0.03)',
                  borderRadius: 'var(--border-radius-md)'
                }}
              >
                <div style={{ fontWeight: 600, fontSize: '13px', color: '#fff', marginBottom: '4px' }}>{t.title}</div>
                <div style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>{t.desc}</div>
              </div>
            ))}
          </div>

          {/* Performance block */}
          <div style={{
            display: 'flex',
            alignItems: 'flex-start',
            gap: '16px',
            padding: '20px',
            background: 'rgba(59, 130, 246, 0.03)',
            border: '1px solid rgba(59, 130, 246, 0.12)',
            borderRadius: 'var(--border-radius-md)',
            marginBottom: '32px'
          }}>
            <Award size={20} style={{ color: 'var(--accent-blue)', flexShrink: 0, marginTop: '2px' }} />
            <div>
              <h4 style={{ fontSize: '13px', fontWeight: 600, color: '#fff', margin: '0 0 4px' }}>Model Performance</h4>
              <p style={{ fontSize: '12px', color: 'var(--text-secondary)', margin: 0, lineHeight: '1.6' }}>
                Achains a <strong>~94.0% average cross-validation accuracy</strong> on testing folds containing 100 
                manually curated IPC trial summaries across 29 specific Indian Penal Code sections.
              </p>
            </div>
          </div>

          {/* Disclaimer (Warning alert) */}
          <div style={{
            display: 'flex',
            alignItems: 'flex-start',
            gap: '16px',
            padding: '20px',
            background: 'rgba(239, 68, 68, 0.03)',
            border: '1px solid rgba(239, 68, 68, 0.12)',
            borderRadius: 'var(--border-radius-md)',
            color: '#fca5a5',
            fontSize: '12px',
            lineHeight: '1.6',
            marginBottom: '40px'
          }}>
            <ShieldAlert size={20} style={{ color: 'var(--accent-red)', flexShrink: 0, marginTop: '2px' }} />
            <div>
              <strong>Academic Disclaimer:</strong> This application serves exploratory and scientific research functions 
              only. The model predictions represent statistical heuristics and must not be used as professional legal 
              advice or judicial decision-making recommendations.
            </div>
          </div>

          {/* Action Links */}
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '16px' }}>
            <a
              href="https://legal-case-ai.onrender.com/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="premium-btn premium-btn-primary"
              style={{ padding: '12px 24px', fontSize: '12px' }}
            >
              <Link2 size={13} />
              API Documentation
            </a>
            <a
              href="https://github.com/hello-abhiii/legal-case-ai"
              target="_blank"
              rel="noopener noreferrer"
              className="premium-btn"
              style={{ padding: '12px 24px', fontSize: '12px' }}
            >
              <svg viewBox="0 0 24 24" width="13" height="13" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" style={{ display: 'inline-block', verticalAlign: 'middle' }}><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path></svg>
              View Source Repository
            </a>
          </div>

        </div>

      </GlassCard>

    </div>
  );
}
