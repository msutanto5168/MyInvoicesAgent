'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

const STORAGE_KEY = 'rememberedUsername';

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      setUsername(saved);
      setRememberMe(true);
    }
  }, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError('');
    setLoading(true);

    const res = await fetch('/api/auth', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });

    setLoading(false);

    if (res.ok) {
      if (rememberMe) {
        localStorage.setItem(STORAGE_KEY, username);
      } else {
        localStorage.removeItem(STORAGE_KEY);
      }
      router.push('/');
      router.refresh();
    } else {
      setError('Invalid username or password.');
    }
  }

  return (
    <main style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100dvh',
      backgroundColor: '#f9f9f9',
      fontFamily: 'sans-serif',
    }}>
      <div style={{
        backgroundColor: '#fff',
        borderRadius: '12px',
        boxShadow: '0 2px 12px rgba(0,0,0,0.1)',
        padding: '2.5rem 2rem',
        width: '320px',
        display: 'flex',
        flexDirection: 'column',
        gap: '1.25rem',
      }}>
        <h1 style={{ fontSize: '1.4rem', fontWeight: '700', margin: 0, textAlign: 'center' }}>
          Invoice Generator
        </h1>
        <p style={{ margin: 0, color: '#888', fontSize: '0.9rem', textAlign: 'center' }}>
          Sign in to continue
        </p>

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={e => setUsername(e.target.value)}
            required
            autoFocus={!username}
            style={{
              padding: '0.65rem 0.85rem',
              borderRadius: '8px',
              border: '1px solid #ddd',
              fontSize: '0.95rem',
              outline: 'none',
            }}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
            style={{
              padding: '0.65rem 0.85rem',
              borderRadius: '8px',
              border: '1px solid #ddd',
              fontSize: '0.95rem',
              outline: 'none',
            }}
          />

          <label style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            fontSize: '0.875rem',
            color: '#555',
            cursor: 'pointer',
          }}>
            <input
              type="checkbox"
              checked={rememberMe}
              onChange={e => setRememberMe(e.target.checked)}
              style={{ cursor: 'pointer', width: '15px', height: '15px' }}
            />
            Remember username
          </label>

          {error && (
            <p style={{ margin: 0, color: '#d00', fontSize: '0.85rem', textAlign: 'center' }}>
              {error}
            </p>
          )}

          <button
            type="submit"
            disabled={loading}
            style={{
              padding: '0.7rem',
              borderRadius: '8px',
              border: 'none',
              backgroundColor: '#171717',
              color: '#fff',
              fontSize: '0.95rem',
              fontWeight: '600',
              cursor: loading ? 'not-allowed' : 'pointer',
              opacity: loading ? 0.7 : 1,
              transition: 'opacity 0.1s',
            }}
          >
            {loading ? 'Signing in…' : 'Sign in'}
          </button>
        </form>
      </div>
    </main>
  );
}
