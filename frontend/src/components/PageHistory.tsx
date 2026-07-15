import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { History, Clock } from 'lucide-react';
import GlassCard from './GlassCard';

export default function PageHistory() {
  const [predictions, setPredictions] = useState<any[]>([]);

  useEffect(() => {
    const list = JSON.parse(localStorage.getItem('legalai_predictions') || '[]');
    setPredictions(list);
  }, []);

  const handleClearHistory = () => {
    if (window.confirm('Are you sure you want to clear your prediction history?')) {
      localStorage.removeItem('legalai_predictions');
      setPredictions([]);
    }
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.08 }
    }
  } as const;

  const itemVariants = {
    hidden: { opacity: 0, y: 12 },
    show: { opacity: 1, y: 0, transition: { type: 'spring', stiffness: 200, damping: 20 } }
  } as const;

  return (
    <div style={{ padding: '40px 0', maxWidth: '800px', margin: '0 auto' }}>
      
      {/* Title */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '32px' }}>
        <div>
          <h2 style={{ fontSize: '24px', fontWeight: 600, color: '#fff', margin: 0, display: 'flex', alignItems: 'center', gap: '10px' }}>
            <History size={22} style={{ color: 'var(--accent-blue)' }} />
            Case Log History
          </h2>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', margin: '6px 0 0' }}>
            Review past outcomes and model confidence records from local storage.
          </p>
        </div>
        {predictions.length > 0 && (
          <button
            onClick={handleClearHistory}
            style={{
              background: 'transparent',
              border: '1px solid rgba(255, 68, 68, 0.2)',
              color: '#f87171',
              fontSize: '12px',
              padding: '8px 14px',
              borderRadius: 'var(--border-radius-sm)',
              cursor: 'pointer',
              transition: 'all 0.2s',
            }}
            onMouseOver={(e) => { e.currentTarget.style.background = 'rgba(239, 68, 68, 0.05)'; }}
            onMouseOut={(e) => { e.currentTarget.style.background = 'transparent'; }}
          >
            Clear Log
          </button>
        )}
      </div>

      {/* History content */}
      {predictions.length === 0 ? (
        <GlassCard hoverEffect={false} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '60px 40px', textAlign: 'center' }}>
          <div style={{
            width: '48px',
            height: '48px',
            borderRadius: '12px',
            background: 'rgba(255, 255, 255, 0.02)',
            border: '1px solid rgba(255, 255, 255, 0.05)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--text-muted)',
            marginBottom: '20px'
          }}>
            <History size={20} />
          </div>
          <h3 style={{ fontSize: '15px', fontWeight: 500, color: 'var(--text-secondary)', margin: '0 0 6px' }}>
            No History Found
          </h3>
          <p style={{ fontSize: '12px', color: 'var(--text-muted)', margin: 0 }}>
            Run the model on some case facts to populate this list.
          </p>
        </GlassCard>
      ) : (
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="show"
          style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}
        >
          {predictions.map((p, idx) => (
            <motion.div key={idx} variants={itemVariants}>
              <GlassCard hoverEffect={true} style={{ display: 'flex', flexDirection: 'column', gap: '16px', padding: '24px 28px' }}>
                
                {/* Header line */}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '16px' }}>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <p style={{ fontSize: '14px', fontWeight: 500, color: '#fff', margin: '0 0 8px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {p.facts}
                    </p>
                    
                    {/* Metas */}
                    <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: '8px', fontSize: '11px', color: 'var(--text-secondary)' }}>
                      <span style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{p.section}</span>
                      <span style={{ width: '4px', height: '4px', borderRadius: '50%', background: 'rgba(255,255,255,0.2)' }} />
                      <span>{p.court}</span>
                      <span style={{ width: '4px', height: '4px', borderRadius: '50%', background: 'rgba(255,255,255,0.2)' }} />
                      <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                        <Clock size={11} />
                        {p.time.split(',')[0]}
                      </span>
                    </div>
                  </div>

                  {/* Badges/Output column */}
                  <div style={{ display: 'flex', alignItems: 'center', gap: '16px', flexShrink: 0 }}>
                    <div style={{ textAlign: 'right' }}>
                      <div style={{ fontSize: '9px', textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--text-muted)', marginBottom: '3px' }}>
                        Confidence
                      </div>
                      <div style={{ fontSize: '15px', fontWeight: 700, color: '#fff', fontFamily: 'var(--font-heading)' }}>
                        {p.confidence}
                      </div>
                    </div>
                    <span className={`glass-badge ${p.outcome === 'Conviction' ? 'glass-badge-conviction' : 'glass-badge-acquittal'}`} style={{ minWidth: '90px', justifyContent: 'center' }}>
                      {p.outcome}
                    </span>
                  </div>
                </div>

              </GlassCard>
            </motion.div>
          ))}
        </motion.div>
      )}

    </div>
  );
}
