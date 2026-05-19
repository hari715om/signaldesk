import React from 'react';

export default function TopBar({ ticker, setTicker, onAnalyze, loading }) {
  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      onAnalyze();
    }
  };

  return (
    <div style={{
      width: '100%',
      height: '56px',
      background: '#111111',
      borderBottom: '1px solid #1f1f1f',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      padding: '0 24px'
    }}>
      <div style={{ display: 'flex', flexDirection: 'column' }}>
        <span style={{
          fontFamily: '"JetBrains Mono", monospace',
          fontSize: '15px',
          letterSpacing: '3px',
          color: '#f0f0f0',
          fontWeight: 600
        }}>
          SIGNALDESK
        </span>
        <span style={{
          fontSize: '10px',
          color: '#444',
          letterSpacing: '2px',
          marginTop: '2px'
        }}>
          AI INVESTMENT COMMITTEE
        </span>
      </div>

      <div>
        <input
          type="text"
          value={ticker}
          onChange={(e) => setTicker(e.target.value.toUpperCase())}
          onKeyDown={handleKeyDown}
          placeholder="Enter ticker e.g. RELIANCE.NS"
          style={{
            background: '#1a1a1a',
            border: '1px solid #2a2a2a',
            borderRadius: '6px',
            width: '280px',
            height: '36px',
            padding: '0 12px',
            fontFamily: '"JetBrains Mono", monospace',
            fontSize: '14px',
            color: '#f0f0f0',
            outline: 'none',
            transition: 'border-color 0.2s ease'
          }}
          onFocus={(e) => e.target.style.borderColor = '#3a3a3a'}
          onBlur={(e) => e.target.style.borderColor = '#2a2a2a'}
          disabled={loading}
        />
      </div>

      <div>
        <button
          onClick={onAnalyze}
          disabled={loading || !ticker.trim()}
          style={{
            background: loading ? 'transparent' : 'transparent',
            border: '1px solid #333',
            color: '#f0f0f0',
            fontSize: '13px',
            letterSpacing: '1px',
            fontFamily: '"JetBrains Mono", monospace',
            padding: '8px 20px',
            borderRadius: '6px',
            cursor: loading || !ticker.trim() ? 'not-allowed' : 'pointer',
            opacity: loading ? 0.5 : 1,
            transition: 'background 0.2s ease',
          }}
          onMouseEnter={(e) => { if (!loading && ticker.trim()) e.target.style.background = '#1f1f1f'; }}
          onMouseLeave={(e) => { if (!loading) e.target.style.background = 'transparent'; }}
        >
          {loading ? 'ANALYZING...' : 'ANALYZE →'}
        </button>
      </div>
    </div>
  );
}
