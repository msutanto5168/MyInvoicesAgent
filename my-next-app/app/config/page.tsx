'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

const CONFIG_API = 'https://api.invoiceagent.com.au/config';
const API_KEY = 'kxLuYXzZ5Q747edWznjq1aROT9lhFua85uoJL1bB';

export default function ConfigPage() {
  const [kfcRental, setKfcRental] = useState('18510.20');
  const [subwayRental, setSubwayRental] = useState('4862.45');
  const [saved, setSaved] = useState(false);
  const [saveError, setSaveError] = useState('');
  const [loadError, setLoadError] = useState('');

  useEffect(() => {
    fetch(CONFIG_API, { headers: { 'X-Api-Key': API_KEY } })
      .then(async r => {
        const text = await r.text();
        if (!r.ok) {
          setLoadError(`Load failed (${r.status}): ${text}`);
          return;
        }
        const data = JSON.parse(text);
        if (data.kfc_rental_amount) setKfcRental(data.kfc_rental_amount);
        if (data.subway_rental_amount) setSubwayRental(data.subway_rental_amount);
      })
      .catch(e => setLoadError(`Load failed: ${e instanceof Error ? e.message : 'Network error'}`));
  }, []);

  const handleSave = async () => {
    setSaveError('');
    try {
      const res = await fetch(CONFIG_API, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Api-Key': API_KEY },
        body: JSON.stringify({ kfc_rental_amount: kfcRental, subway_rental_amount: subwayRental }),
      });
      if (!res.ok) {
        const body = await res.text();
        setSaveError(`Save failed (${res.status}): ${body}`);
        return;
      }
      setSaved(true);
      setTimeout(() => setSaved(false), 2500);
    } catch (e) {
      setSaveError(`Save failed: ${e instanceof Error ? e.message : 'Network error'}`);
    }
  };

  const kfcGst = (parseFloat(kfcRental) || 0) * 0.1;
  const subwayGst = (parseFloat(subwayRental) || 0) * 0.1;

  const cardStyle: React.CSSProperties = {
    backgroundColor: '#fff',
    borderRadius: '12px',
    boxShadow: '0 2px 12px rgba(0,0,0,0.1)',
    padding: '1.75rem',
    width: '340px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '1rem',
  };

  const inputStyle: React.CSSProperties = {
    backgroundColor: '#f0f0f0',
    border: '1px solid #ccc',
    borderRadius: '6px',
    padding: '0.6rem',
    fontSize: '16px',
    width: '100%',
    boxSizing: 'border-box',
  };

  const labelStyle: React.CSSProperties = {
    fontWeight: '500',
    marginBottom: '0.3rem',
    display: 'block',
    alignSelf: 'flex-start',
    width: '100%',
  };

  return (
    <main style={{
      padding: '1rem',
      fontFamily: 'sans-serif',
      maxWidth: '800px',
      margin: '0 auto',
      boxSizing: 'border-box',
    }}>
      {/* Nav buttons */}
      <div style={{ marginBottom: '1.5rem', display: 'flex', gap: '0.75rem' }}>
        <Link href="/" style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '0.5rem',
          padding: '0.5rem 1.2rem',
          backgroundColor: '#333',
          borderRadius: '8px',
          textDecoration: 'none',
          color: '#fff',
          fontSize: '0.95rem',
          fontWeight: '600',
          boxShadow: '0 2px 6px rgba(0,0,0,0.2)',
        }}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
          Home
        </Link>
        <button onClick={async () => {
          await fetch('/api/auth', { method: 'DELETE' });
          window.location.href = '/login';
        }} style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '0.5rem',
          padding: '0.5rem 1.2rem',
          backgroundColor: '#b00',
          border: 'none',
          borderRadius: '8px',
          color: '#fff',
          fontSize: '0.95rem',
          fontWeight: '600',
          cursor: 'pointer',
          boxShadow: '0 2px 6px rgba(0,0,0,0.2)',
        }}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.58L17 17l5-5zM4 5h8V3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h8v-2H4V5z"/></svg>
          Log out
        </button>
      </div>

      <h1 style={{ fontSize: '1.5rem', fontWeight: '700', marginBottom: '1.5rem' }}>
        Configuration
      </h1>

      {loadError && (
        <p style={{ color: '#d00', fontSize: '0.85rem', marginBottom: '1rem' }}>{loadError}</p>
      )}

      {/* Cards */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', marginBottom: '1.75rem' }}>

        {/* KFC Card */}
        <div style={cardStyle}>
          <img src="/kfc-logo.png" alt="KFC" style={{ width: '120px', height: '60px', objectFit: 'contain' }} />
          <div style={{ width: '100%' }}>
            <label style={labelStyle}>Monthly Rental Amount ($)</label>
            <input
              type="number"
              step="0.01"
              value={kfcRental}
              onChange={e => setKfcRental(e.target.value)}
              style={inputStyle}
            />
          </div>
          <div style={{
            width: '100%',
            backgroundColor: '#f9f9f9',
            border: '1px solid #e0e0e0',
            borderRadius: '6px',
            padding: '0.6rem',
            fontSize: '0.9rem',
            color: '#555',
          }}>
            GST (10%): <strong>${kfcGst.toFixed(2)}</strong>
          </div>
        </div>

        {/* Subway Card */}
        <div style={cardStyle}>
          <img src="/subway-logo.png" alt="Subway" style={{ width: '120px', height: '60px', objectFit: 'contain' }} />
          <div style={{ width: '100%' }}>
            <label style={labelStyle}>Monthly Rental Amount ($)</label>
            <input
              type="number"
              step="0.01"
              value={subwayRental}
              onChange={e => setSubwayRental(e.target.value)}
              style={inputStyle}
            />
          </div>
          <div style={{
            width: '100%',
            backgroundColor: '#f9f9f9',
            border: '1px solid #e0e0e0',
            borderRadius: '6px',
            padding: '0.6rem',
            fontSize: '0.9rem',
            color: '#555',
          }}>
            GST (10%): <strong>${subwayGst.toFixed(2)}</strong>
          </div>
        </div>
      </div>

      {/* Save button */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <button
          onClick={handleSave}
          style={{
            padding: '0.75rem 2rem',
            fontSize: '1rem',
            backgroundColor: '#171717',
            color: '#fff',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            fontWeight: '600',
            boxShadow: '0 2px 6px rgba(0,0,0,0.2)',
          }}
        >
          Save
        </button>
        {saved && (
          <span style={{ color: '#080', fontWeight: '600', fontSize: '0.95rem' }}>
            ✓ Saved!
          </span>
        )}
        {saveError && (
          <span style={{ color: '#d00', fontSize: '0.85rem' }}>
            {saveError}
          </span>
        )}
      </div>
    </main>
  );
}
