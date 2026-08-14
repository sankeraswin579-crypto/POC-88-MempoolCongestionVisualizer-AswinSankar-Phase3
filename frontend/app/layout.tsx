import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Mempool Congestion Intelligence | POC-88",
  description:
    "Real-time Bitcoin mempool congestion, fee pressure, transaction activity and network intelligence.",
  applicationName:
    "POC-88 Mempool Congestion Intelligence",
  keywords: [
    "Bitcoin",
    "Mempool",
    "Congestion",
    "Blockchain",
    "Bitcoin Analytics",
    "Mempool.space",
    "POC-88",
    "Infocreon",
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link
          href="https://api.mapbox.com/mapbox-gl-js/v3.0.0/mapbox-gl.css"
          rel="stylesheet"
        />
      </head>

      <body className="bg-[#02070d] text-white antialiased">
        {children}
      </body>
    </html>
  );
}