import React, { useState, useEffect } from 'react';

export default function AnalystCard({ analyst }) {
  const [displayedScore, setDisplayedScore] = useState(0);
  const [displayedText, setDisplayedText] = useState('');
  const [isTyping, setIsTyping] = useState(true);
  const [isHovered, setIsHovered] = useState(false);

  // Score count-up animation
  useEffect(() => {
    let start = 0;
    const end = analyst.score;
    if (start === end) {
      setDisplayedScore(end);
      return;
    }
    const duration = 800; // ms
    const incrementTime = Math.max(10, Math.floor(duration / end));

    const timer = setInterval(() => {
      start += 1;
      setDisplayedScore(start);
      if (start === end) {
        clearInterval(timer);
      }
    }, incrementTime);

    return () => clearInterval(timer);
  }, [analyst.score]);

  // Typewriter effect
  useEffect(() => {
    setDisplayedText('');
    setIsTyping(true);
    let i = 0;
    const text = analyst.response;
    
    const timer = setInterval(() => {
      if (i < text.length) {
        setDisplayedText((prev) => prev + text.charAt(i));
        i++;
      } else {
        setIsTyping(false);
        clearInterval(timer);
      }
    }, 12);

    return () => clearInterval(timer);
  }, [analyst.response]);

  return (
    <div 
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      style={{
        background: '#111111',
        border: '1px solid #1f1f1f',
        borderLeft: `${isHovered ? '5px' : '3px'} solid ${analyst.color}`,
        borderRadius: '8px',
        padding: '20px',
        position: 'relative',
        boxShadow: isHovered ? `0 0 24px ${analyst.color}22` : 'none',
        transition: 'all 0.2s ease',
        display: 'flex',
        flexDirection: 'column'
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <div style={{ 
            fontSize: '14px', 
            fontWeight: 600, 
            color: analyst.color, 
            letterSpacing: '0.5px' 
          }}>
            {analyst.name}
          </div>
          <div style={{ 
            fontSize: '11px', 
            color: '#555', 
            letterSpacing: '1px', 
            textTransform: 'uppercase',
            marginTop: '2px'
          }}>
            {analyst.role}
          </div>
        </div>

        <div style={{
          width: '44px',
          height: '44px',
          borderRadius: '50%',
          border: `1.5px solid ${analyst.color}`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontFamily: '"JetBrains Mono", monospace',
          fontSize: '16px',
          fontWeight: 600,
          color: analyst.color
        }}>
          {displayedScore}
        </div>
      </div>

      <div style={{
        marginTop: '16px',
        fontSize: '13px',
        lineHeight: 1.7,
        color: '#c0c0c0',
        whiteSpace: 'pre-wrap'
      }}>
        {displayedText}
        {isTyping && (
          <span style={{ 
            animation: 'blink 1s step-end infinite',
            marginLeft: '2px' 
          }}>|</span>
        )}
      </div>
      
      <style>{`
        @keyframes blink {
          0%, 100% { opacity: 1; }
          50% { opacity: 0; }
        }
      `}</style>
    </div>
  );
}
