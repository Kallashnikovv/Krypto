import React from "react";
import "./Raporty.css";
import Navbar from './Navbar';
import ThemeToggle from './ThemeToggle';
import Form from './Form';

const data = [
  { name: "Bitcoin", price: "$37,612.80", change1h: "-0.15%", change24h: "+0.89%", change7d: "+3.75%", marketCap: "$732.5B" },
  { name: "Ethereum", price: "$2,115.47", change1h: "+0.08%", change24h: "+1.21%", change7d: "+5.04%", marketCap: "$252.3B" },
  { name: "Bitcoin", price: "$37,612.80", change1h: "-0.15%", change24h: "+0.89%", change7d: "+3.75%", marketCap: "$732.5B" },
  { name: "Ethereum", price: "$2,115.47", change1h: "+0.08%", change24h: "+1.21%", change7d: "+5.04%", marketCap: "$252.3B" },
  { name: "Bitcoin", price: "$37,612.80", change1h: "-0.15%", change24h: "+0.89%", change7d: "+3.75%", marketCap: "$732.5B" },
  { name: "Ethereum", price: "$2,115.47", change1h: "+0.08%", change24h: "+1.21%", change7d: "+5.04%", marketCap: "$252.3B" },
];

function Raporty() {
  return (
    <div className="container">
      <ThemeToggle />
      
      <header>
        <Navbar />
        <h1><i className="fa-solid fa-coins"></i> CRYPTO</h1>
      </header>

      <div className="main-content">
        <div className="content">
          <Form />

          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Asset</th>
                  <th>Cost</th>
                  <th>1H</th>
                  <th>24H</th>
                  <th>7D</th>
                  <th>MCAP</th>
                </tr>
              </thead>
              <tbody>
                {data.map((crypto, index) => (
                  <tr key={index}>
                    <td>{crypto.name}</td>
                    <td>{crypto.price}</td>
                    <td>{crypto.change1h}</td>
                    <td>{crypto.change24h}</td>
                    <td>{crypto.change7d}</td>
                    <td>{crypto.marketCap}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="chart">
            <h2>Chart</h2>
            <canvas id="chart"></canvas>
          </div>

          <div className="trending-gainers">
            <div className="trending">
              <h3>Trending 🔥</h3>
              <ul>
                <li>1. Bitcoin $37,612.80 +0.89%</li>
                <li>2. Ethereum $2,115.47 +1.21%</li>
              </ul>
            </div>

            <div className="gainers">
              <h3>Largest Gainers 🚀</h3>
              <ul>
                <li>1. Bitcoin $37,612.80 +0.89%</li>
                <li>2. Ethereum $2,115.47 +1.21%</li>
              </ul>
            </div>
          </div>
        </div>

        <aside className="prawa"></aside>
      </div>

      <footer>
        <br /><br />
      </footer>
    </div>
  );
}

export default Raporty;
