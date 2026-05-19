import React from 'react';

export default function SkeletonLoader() {
  return (
    <div style={{
      background: '#111111',
      border: '1px solid #1f1f1f',
      borderLeft: '3px solid #2a2a2a',
      borderRadius: '8px',
      padding: '20px',
      position: 'relative',
      display: 'flex',
      flexDirection: 'column'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <div style={{
            width: '120px',
            height: '16px',
            borderRadius: '4px',
            background: 'linear-gradient(90deg, #1a1a1a 0%, #222 50%, #1a1a1a 100%)',
            backgroundSize: '200% 100%',
            animation: 'shimmer 1.5s infinite linear'
          }} />
          <div style={{
            width: '80px',
            height: '12px',
            borderRadius: '3px',
            marginTop: '6px',
            background: 'linear-gradient(90deg, #1a1a1a 0%, #222 50%, #1a1a1a 100%)',
            backgroundSize: '200% 100%',
            animation: 'shimmer 1.5s infinite linear'
          }} />
        </div>

        <div style={{
          width: '44px',
          height: '44px',
          borderRadius: '50%',
          background: 'linear-gradient(90deg, #1a1a1a 0%, #222 50%, #1a1a1a 100%)',
          backgroundSize: '200% 100%',
          animation: 'shimmer 1.5s infinite linear'
        }} />
      </div>

      <div style={{ marginTop: '24px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
        <div style={shimmerLineStyle(100)} />
        <div style={shimmerLineStyle(95)} />
        <div style={shimmerLineStyle(90)} />
        <div style={shimmerLineStyle(60)} />
      </div>

      <style>{`
        @keyframes shimmer {
          0% { background-position: -200% 0; }
          100% { background-position: 200% 0; }
        }
      `}</style>
    </div>
  );
}

const shimmerLineStyle = (widthPercent) => ({
  width: `${widthPercent}%`,
  height: '12px',
  borderRadius: '3px',
  background: 'linear-gradient(90deg, #1a1a1a 0%, #222 50%, #1a1a1a 100%)',
  backgroundSize: '200% 100%',
  animation: 'shimmer 1.5s infinite linear'
});
