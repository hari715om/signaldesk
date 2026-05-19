import React from 'react';

export default function VerdictCard({ verdict, confidence, overall_sentiment }) {
  let config = {};
  if (verdict === 'BUY') {
    config = { color: '#22c55e', glyph: '↑', description: 'Committee recommends buying this position' };
  } else if (verdict === 'HOLD') {
    config = { color: '#f59e0b', glyph: '→', description: 'Mixed signals — monitor closely before committing' };
  } else {
    config = { color: '#ef4444', glyph: '↓', description: 'Committee advises avoiding or exiting this position' };
  }

  return (
    <div style={{
      marginTop: '16px',
      background: '#111111',
      border: `1.5px solid ${config.color}`,
      borderRadius: '8px',
      padding: '28px',
      boxShadow: `0 0 40px ${config.color}15`
    }}>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <div>
          <div style={{
            fontSize: '36px',
            fontWeight: 700,
            letterSpacing: '2px',
            fontFamily: '"JetBrains Mono", monospace',
            color: config.color
          }}>
            {verdict} {config.glyph}
          </div>
          <div style={{
            fontSize: '13px',
            color: '#777',
            marginTop: '4px'
          }}>
            {config.description}
          </div>
        </div>

        <div style={{ textAlign: 'right' }}>
          <div style={{
            fontSize: '10px',
            letterSpacing: '2px',
            color: '#444'
          }}>
            CONFIDENCE
          </div>
          <div style={{
            fontSize: '28px',
            fontWeight: 600,
            fontFamily: '"JetBrains Mono", monospace',
            color: config.color
          }}>
            {confidence}%
          </div>
        </div>
      </div>

      <div style={{
        width: '100%',
        marginTop: '20px',
        paddingTop: '16px',
        borderTop: '1px solid #1f1f1f',
        fontSize: '10px',
        color: '#333',
        letterSpacing: '0.5px'
      }}>
        Based on analysis of 4 specialized AI analysts. Not financial advice. Always do your own research.
      </div>
    </div>
  );
}
