import React, { useState, useEffect } from 'react';

export default function ConsensusMeter({ analysts, overallSentiment }) {
  const [displayedSentiment, setDisplayedSentiment] = useState(0);
  const [barsWidths, setBarsWidths] = useState({});

  // Overall sentiment count-up
  useEffect(() => {
    let start = 0;
    const end = overallSentiment;
    if (start === end) {
      setDisplayedSentiment(end);
      return;
    }
    const duration = 1000;
    const incrementTime = 20;
    const steps = duration / incrementTime;
    const stepValue = end / steps;

    const timer = setInterval(() => {
      start += stepValue;
      if (start >= end) {
        start = end;
        clearInterval(timer);
      }
      setDisplayedSentiment(start);
    }, incrementTime);

    return () => clearInterval(timer);
  }, [overallSentiment]);

  // Bar width animation
  useEffect(() => {
    const timeout = setTimeout(() => {
      const widths = {};
      analysts.forEach(a => {
        widths[a.id] = a.score;
      });
      setBarsWidths(widths);
    }, 100);
    return () => clearTimeout(timeout);
  }, [analysts]);

  const getSentimentColor = (val) => {
    if (val >= 68) return '#22c55e';
    if (val >= 45) return '#f59e0b';
    return '#ef4444';
  };

  return (
    <div style={{
      marginTop: '32px',
      padding: '24px',
      background: '#111111',
      border: '1px solid #1f1f1f',
      borderRadius: '8px'
    }}>
      <div style={{
        fontSize: '10px',
        letterSpacing: '3px',
        color: '#444',
        marginBottom: '20px',
        fontWeight: 600
      }}>
        COMMITTEE CONSENSUS
      </div>

      {analysts.map((analyst) => (
        <div key={analyst.id} style={{
          display: 'flex',
          alignItems: 'center',
          gap: '12px',
          marginBottom: '12px'
        }}>
          <div style={{
            width: '120px',
            fontSize: '12px',
            color: '#888',
            fontFamily: '"JetBrains Mono", monospace'
          }}>
            {analyst.name}
          </div>
          
          <div style={{
            flex: 1,
            height: '6px',
            background: '#1a1a1a',
            borderRadius: '3px',
            overflow: 'hidden'
          }}>
            <div style={{
              height: '100%',
              background: analyst.color,
              borderRadius: '3px',
              width: `${barsWidths[analyst.id] || 0}%`,
              transition: 'width 0.6s ease-out'
            }} />
          </div>
          
          <div style={{
            width: '36px',
            fontSize: '12px',
            color: analyst.color,
            textAlign: 'right',
            fontFamily: '"JetBrains Mono", monospace'
          }}>
            {analyst.score}
          </div>
        </div>
      ))}

      <div style={{
        borderTop: '1px solid #1f1f1f',
        margin: '20px 0'
      }} />

      <div>
        <div style={{
          fontSize: '10px',
          letterSpacing: '2px',
          color: '#444'
        }}>
          OVERALL SIGNAL
        </div>
        <div style={{
          fontSize: '48px',
          fontWeight: 600,
          fontFamily: '"JetBrains Mono", monospace',
          color: getSentimentColor(overallSentiment)
        }}>
          {displayedSentiment.toFixed(1)}
        </div>
      </div>
    </div>
  );
}
