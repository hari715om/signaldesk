import React from 'react';

const SUGGESTIONS = ['RELIANCE.NS', 'HDFCBANK.NS', 'INFY.NS', 'TCS.NS', 'AAPL', 'NVDA', 'TSLA', 'MSFT'];

export default function TickerSuggestions({ onSelect }) {
  return (
    <div style={{
      display: 'flex',
      flexWrap: 'wrap',
      gap: '8px',
      margin: '8px 24px 0',
      alignItems: 'center'
    }}>
      <span style={{
        fontSize: '10px',
        color: '#666',
        letterSpacing: '1px',
        marginRight: '4px'
      }}>
        QUICK SELECT —
      </span>
      
      {SUGGESTIONS.map(ticker => (
        <button
          key={ticker}
          onClick={() => onSelect(ticker)}
          style={{
            background: 'transparent',
            border: '1px solid #2a2a2a',
            borderRadius: '4px',
            padding: '4px 10px',
            fontSize: '11px',
            fontFamily: '"JetBrains Mono", monospace',
            color: '#666',
            letterSpacing: '0.5px',
            cursor: 'pointer',
            transition: 'all 0.2s ease'
          }}
          onMouseEnter={(e) => {
            e.target.style.borderColor = '#444';
            e.target.style.color = '#aaa';
          }}
          onMouseLeave={(e) => {
            e.target.style.borderColor = '#2a2a2a';
            e.target.style.color = '#666';
          }}
        >
          {ticker}
        </button>
      ))}
    </div>
  );
}
