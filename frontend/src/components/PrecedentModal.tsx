import { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Scale } from 'lucide-react';

interface PrecedentModalProps {
  isOpen: boolean;
  onClose: () => void;
  caseData: {
    title: string;
    section: string;
    outcome: string;
    facts: string;
  } | null;
}

export default function PrecedentModal({ isOpen, onClose, caseData }: PrecedentModalProps) {
  // Listen for Escape key to close modal
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    if (isOpen) {
      window.addEventListener('keydown', handleKeyDown);
      document.body.style.overflow = 'hidden';
    }
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      document.body.style.overflow = '';
    };
  }, [isOpen, onClose]);

  if (!caseData) return null;

  const isConviction = caseData.outcome === 'Conviction';

  return (
    <AnimatePresence>
      {isOpen && (
        <div style={{ position: 'fixed', inset: 0, zIndex: 1000, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '16px' }}>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            style={{
              position: 'absolute',
              inset: 0,
              background: 'rgba(0, 0, 0, 0.75)',
              backdropFilter: 'blur(8px)',
            }}
          />

          {/* Modal Container */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 15 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 15 }}
            transition={{ type: 'spring', damping: 25, stiffness: 350 }}
            className="glass-panel"
            style={{
              position: 'relative',
              width: '100%',
              maxWidth: '650px',
              maxHeight: '85vh',
              overflow: 'hidden',
              display: 'flex',
              flexDirection: 'column',
              background: 'rgba(10, 10, 12, 0.9)',
              borderColor: 'rgba(255, 255, 255, 0.08)',
              zIndex: 1010,
              boxShadow: '0 24px 60px rgba(0, 0, 0, 0.8), 0 0 40px rgba(59, 130, 246, 0.05)',
            }}
          >
            {/* Header */}
            <div style={{
              display: 'flex',
              alignItems: 'flex-start',
              justifyContent: 'space-between',
              padding: '24px 28px',
              borderBottom: '1px solid rgba(255, 255, 255, 0.06)'
            }}>
              <div>
                <span className="glass-badge" style={{ color: 'var(--accent-blue)', borderColor: 'rgba(59,130,246,0.15)', background: 'rgba(59,130,246,0.02)', marginBottom: '8px' }}>
                  Relevant Precedent
                </span>
                <h3 style={{ fontSize: '20px', fontWeight: 600, color: '#fff', margin: '6px 0 0' }}>
                  {caseData.title || 'Untitled Case'}
                </h3>
              </div>
              <button
                onClick={onClose}
                style={{
                  background: 'rgba(255, 255, 255, 0.03)',
                  border: '1px solid rgba(255, 255, 255, 0.06)',
                  color: 'var(--text-secondary)',
                  borderRadius: '50%',
                  width: '36px',
                  height: '36px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                }}
                onMouseOver={(e) => { e.currentTarget.style.color = '#fff'; e.currentTarget.style.background = 'rgba(255, 255, 255, 0.06)'; }}
                onMouseOut={(e) => { e.currentTarget.style.color = 'var(--text-secondary)'; e.currentTarget.style.background = 'rgba(255, 255, 255, 0.03)'; }}
                aria-label="Close modal"
              >
                <X size={16} />
              </button>
            </div>

            {/* Content Body */}
            <div style={{ padding: '28px', overflowY: 'auto', flex: 1 }}>
              {/* Badges */}
              <div style={{ display: 'flex', gap: '8px', marginBottom: '24px' }}>
                <span className="glass-badge">
                  {caseData.section || 'Section unavailable'}
                </span>
                <span className={`glass-badge ${isConviction ? 'glass-badge-conviction' : 'glass-badge-acquittal'}`}>
                  {caseData.outcome || 'Outcome unavailable'}
                </span>
              </div>

              {/* Case Facts Title */}
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                fontSize: '11px',
                fontWeight: 600,
                textTransform: 'uppercase',
                letterSpacing: '0.12em',
                color: 'var(--text-secondary)',
                marginBottom: '10px'
              }}>
                <Scale size={13} style={{ color: 'var(--accent-purple)' }} />
                Case Facts
              </div>

              {/* Case Facts Content */}
              <p style={{
                fontSize: '14px',
                color: 'var(--text-secondary)',
                lineHeight: '1.7',
                margin: 0,
                whiteSpace: 'pre-line',
                background: 'rgba(255, 255, 255, 0.01)',
                padding: '18px',
                borderRadius: 'var(--border-radius-md)',
                border: '1px solid rgba(255, 255, 255, 0.03)'
              }}>
                {caseData.facts || 'Facts unavailable.'}
              </p>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
