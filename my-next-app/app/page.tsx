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
      minHeight: "100vh",
      fontFamily: "sans-serif",
      backgroundColor: "#f9f9f9"
    }}>
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
