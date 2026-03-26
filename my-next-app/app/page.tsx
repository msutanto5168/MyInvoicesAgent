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
      </div>
    </main>
  );
}
