import React, { useState } from 'react';
import { analyzeStock, analyzeStockMock } from './api';
import TopBar from './components/TopBar';
import TickerSuggestions from './components/TickerSuggestions';
import SkeletonLoader from './components/SkeletonLoader';
import AnalystCard from './components/AnalystCard';
import ConsensusMeter from './components/ConsensusMeter';
import VerdictCard from './components/VerdictCard';

export default function App() {
  const [ticker, setTicker] = useState('');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async (tickerToAnalyze = ticker) => {
    if (!tickerToAnalyze.trim()) return;
    
    setLoading(true);
    setError(null);
    setData(null);

    try {
      const result = await analyzeStock(tickerToAnalyze);
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectSuggestion = (selectedTicker) => {
    setTicker(selectedTicker);
    handleAnalyze(selectedTicker);
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: '#0a0a0a',
      color: '#f0f0f0',
      fontFamily: 'system-ui, -apple-system, sans-serif'
    }}>
      <TopBar 
        ticker={ticker} 
        setTicker={setTicker} 
        onAnalyze={() => handleAnalyze()} 
        loading={loading} 
      />
      
      <TickerSuggestions onSelect={handleSelectSuggestion} />

      <main style={{
        maxWidth: '1100px',
        margin: '0 auto',
        padding: '24px'
      }}>
        {loading && (
          <div style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: '16px'
          }}>
            <SkeletonLoader />
            <SkeletonLoader />
            <SkeletonLoader />
            <SkeletonLoader />
          </div>
        )}

        {error && (
          <div style={{
            background: '#220000',
            border: '1px solid #ef4444',
            borderRadius: '8px',
            padding: '24px',
            color: '#ef4444',
            fontFamily: '"JetBrains Mono", monospace'
          }}>
            <h3 style={{ marginBottom: '8px' }}>Error Details</h3>
            <p style={{ fontSize: '14px', lineHeight: 1.5 }}>{error}</p>
          </div>
        )}

        {!loading && !error && !data && (
          <div style={{
            textAlign: 'center',
            color: '#333',
            fontSize: '14px',
            marginTop: '80px',
            letterSpacing: '0.5px'
          }}>
            Enter a ticker above to convene the committee
          </div>
        )}

        {data && !loading && !error && (
          <>
            <div style={{
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '16px'
            }}>
              {data.analysts.map((analyst) => (
                <AnalystCard key={analyst.id} analyst={analyst} />
              ))}
            </div>

            <ConsensusMeter 
              analysts={data.analysts} 
              overallSentiment={data.overall_sentiment} 
            />

            <VerdictCard 
              verdict={data.verdict} 
              confidence={data.confidence} 
              overall_sentiment={data.overall_sentiment} 
            />
          </>
        )}
      </main>
    </div>
  );
}
