'use client';

import Image from "next/image";
import Link from "next/link";

export default function Home() {
  return (
    <main style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      height: "100dvh",
      overflow: "hidden",
      fontFamily: "sans-serif",
      backgroundColor: "#f9f9f9",
      position: "relative",
    }}>
      <div style={{ position: "absolute", top: "1.25rem", right: "1.5rem" }}>
        <button onClick={async () => {
          await fetch("/api/auth", { method: "DELETE" });
          window.location.href = "/login";
        }} style={{
          display: "inline-flex",
          alignItems: "center",
          gap: "0.5rem",
          padding: "0.5rem 1.2rem",
          backgroundColor: "#b00",
          border: "none",
          borderRadius: "8px",
          color: "#fff",
          fontSize: "0.95rem",
          fontWeight: "600",
          cursor: "pointer",
          boxShadow: "0 2px 6px rgba(0,0,0,0.2)"
        }}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.58L17 17l5-5zM4 5h8V3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h8v-2H4V5z"/></svg>
          Log out
        </button>
      </div>
      <h1 style={{ fontSize: "1.8rem", marginBottom: "2.5rem", fontWeight: "700" }}>
        Invoice Generator
      </h1>
      <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem", alignItems: "center" }}>
        <Link href="/kfc" style={{ textDecoration: "none" }}>
          <div style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            width: "300px",
            height: "140px",
            backgroundColor: "#fff",
            borderRadius: "12px",
            boxShadow: "0 2px 12px rgba(0,0,0,0.1)",
            cursor: "pointer",
            transition: "transform 0.1s, box-shadow 0.1s"
          }}
            onMouseEnter={e => {
              (e.currentTarget as HTMLDivElement).style.transform = "scale(1.04)";
              (e.currentTarget as HTMLDivElement).style.boxShadow = "0 4px 20px rgba(0,0,0,0.18)";
            }}
            onMouseLeave={e => {
              (e.currentTarget as HTMLDivElement).style.transform = "scale(1)";
              (e.currentTarget as HTMLDivElement).style.boxShadow = "0 2px 12px rgba(0,0,0,0.1)";
            }}
          >
            <Image src="/kfc-logo.png" alt="KFC" width={150} height={100} style={{ objectFit: "contain" }} />
          </div>
        </Link>

        <Link href="/subway" style={{ textDecoration: "none" }}>
          <div style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            width: "300px",
            height: "140px",
            backgroundColor: "#fff",
            borderRadius: "12px",
            boxShadow: "0 2px 12px rgba(0,0,0,0.1)",
            cursor: "pointer",
            transition: "transform 0.1s, box-shadow 0.1s"
          }}
            onMouseEnter={e => {
              (e.currentTarget as HTMLDivElement).style.transform = "scale(1.04)";
              (e.currentTarget as HTMLDivElement).style.boxShadow = "0 4px 20px rgba(0,0,0,0.18)";
            }}
            onMouseLeave={e => {
              (e.currentTarget as HTMLDivElement).style.transform = "scale(1)";
              (e.currentTarget as HTMLDivElement).style.boxShadow = "0 2px 12px rgba(0,0,0,0.1)";
            }}
          >
            <Image src="/subway-logo.png" alt="Subway" width={150} height={100} style={{ objectFit: "contain" }} />
          </div>
        </Link>

        <Link href="/config" style={{ textDecoration: "none" }}>
          <div style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: "0.6rem",
            width: "300px",
            height: "60px",
            backgroundColor: "#fff",
            borderRadius: "12px",
            boxShadow: "0 2px 12px rgba(0,0,0,0.1)",
            cursor: "pointer",
            transition: "transform 0.1s, box-shadow 0.1s",
            color: "#333",
            fontWeight: "600",
            fontSize: "1rem",
          }}
            onMouseEnter={e => {
              (e.currentTarget as HTMLDivElement).style.transform = "scale(1.04)";
              (e.currentTarget as HTMLDivElement).style.boxShadow = "0 4px 20px rgba(0,0,0,0.18)";
            }}
            onMouseLeave={e => {
              (e.currentTarget as HTMLDivElement).style.transform = "scale(1)";
              (e.currentTarget as HTMLDivElement).style.boxShadow = "0 2px 12px rgba(0,0,0,0.1)";
            }}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.07.62-.07.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z"/></svg>
            Config
          </div>
        </Link>
      </div>
    </main>
  );
}
