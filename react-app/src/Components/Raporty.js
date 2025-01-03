import React, { useState, useEffect } from "react";
import "./Raporty.css";
import Navbar from './Navbar';
import ThemeToggle from './ThemeToggle';
import Form from './Form';
import { jsPDF } from "jspdf";
import "jspdf-autotable";  
import CurrencyFilter from './Form';

const initialData = [
  { "name": "Bitcoin", "price": 37612.80, "change1h": -0.15, "change24h": 0.89, "change7d": 3.75, "marketCap": 732.5 },
  { "name": "Ethereum", "price": 2115.47, "change1h": 0.08, "change24h": 1.21, "change7d": 5.04, "marketCap": 252.3 },
  { "name": "Dogecoin", "price": 0.074, "change1h": -0.02, "change24h": 0.65, "change7d": 1.92, "marketCap": 10.2 },
  { "name": "Ripple (XRP)", "price": 0.48, "change1h": -0.10, "change24h": -0.35, "change7d": -0.50, "marketCap": 24.6 },
  { "name": "Cardano", "price": 0.30, "change1h": 0.01, "change24h": 0.90, "change7d": 2.04, "marketCap": 10.1 },
  { "name": "Avalanche", "price": 13.50, "change1h": 0.02, "change24h": 1.15, "change7d": 3.22, "marketCap": 4.5 },
  { "name": "Solana", "price": 25.00, "change1h": 0.05, "change24h": 0.75, "change7d": 1.87, "marketCap": 9.8 },
  { "name": "USDC", "price": 1.00, "change1h": 0.00, "change24h": 0.00, "change7d": 0.00, "marketCap": 43.2 },
  { "name": "Tether (USDT)", "price": 1.00, "change1h": 0.00, "change24h": 0.00, "change7d": 0.00, "marketCap": 83.0 }
];

function Raporty() {
  const [data, setData] = useState(initialData);
  const [chartUrl, setChartUrl] = useState('/cryptocurrency_info_today.png'); // Domyślny URL wykresu

  
  const filterData = (filter) => {
    const { searchTerm, currencyType, minValue, maxValue, sortOption } = filter;

    let filteredData = initialData;

      if (searchTerm) {
      filteredData = filteredData.filter(item =>
        item.name.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    
    if (currencyType !== 'all') {
    
    }

    if (minValue) {
      filteredData = filteredData.filter(item => item.price >= minValue);
    }
    if (maxValue) {
      filteredData = filteredData.filter(item => item.price <= maxValue);
    }

    // Sortowanie
    if (sortOption) {
      switch (sortOption) {
        case "priceAsc":
          filteredData.sort((a, b) => a.price - b.price);
          break;
        case "priceDesc":
          filteredData.sort((a, b) => b.price - a.price);
          break;
        case "name":
          filteredData.sort((a, b) => a.name.localeCompare(b.name));
          break;
        case "percentageChange":
          filteredData.sort((a, b) => (b.change24h - a.change24h));
          break;
        default:
          break;
      }
    }

    setData(filteredData); 
  };

  const generatePDF = () => {
    const doc = new jsPDF();

    
    doc.setFont("helvetica", "bold");
    doc.setFontSize(16);
    doc.text("Cryptocurrency Report", 10, 10);

    doc.setFont("helvetica", "normal");
    doc.setFontSize(12);

    const tableData = data.map(crypto => [
      crypto.name,
      crypto.price,
      crypto.change1h,
      crypto.change24h,
      crypto.change7d,
      crypto.marketCap
    ]);

    doc.autoTable({
      head: [['Asset', 'Cost', '1H', '24H', '7D', 'MCAP']],
      body: tableData,
      startY: 20,
      margin: { top: 10, left: 10, right: 10, bottom: 10 },
      theme: 'striped',
    });

    doc.addPage();
    doc.text("Cryptocurrency Chart", 10, 10);
    doc.addImage(chartUrl, "PNG", 10, 20, 180, 100);

    doc.save("cryptocurrency_report.pdf");
  };

  const fetchChartData = () => {
    const newUrl = `/cryptocurrency_info_today.png?timestamp=${new Date().getTime()}`;
    console.log('Fetching new chart URL:', newUrl); // Debug
    setChartUrl(newUrl);
  };

  useEffect(() => {
    fetchChartData();

    const interval = setInterval(() => {
      fetchChartData();
    }, 60000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="container">
      <ThemeToggle />

      <header>
        <Navbar />
        <h1><i className="fa-solid fa-coins"></i> CRYPTO</h1>
      </header>

      <div className="main-content">
        <div className="content">
          <CurrencyFilter onFilter={filterData} />
          <div className="chart">
            <h2>Chart</h2>
            <img 
              key={chartUrl} 
              src={chartUrl} 
              alt="Cryptocurrency Chart" 
              width="600" 
              className="chart_img"
            />
            <button
              className="download-btn"
              onClick={generatePDF}
              style={{ marginLeft: "auto", display: "block" }}
            >
              Download Report (PDF)
            </button>
          </div>

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
                    <td>${crypto.price}</td>
                    <td>{crypto.change1h}%</td>
                    <td>{crypto.change24h}%</td>
                    <td>{crypto.change7d}%</td>
                    <td>${crypto.marketCap}B</td>
                  </tr>
                ))}
              </tbody>
            </table>
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
