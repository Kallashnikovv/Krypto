import React, { useState, useEffect } from "react";
import "./Raporty.css";
import Navbar from './Navbar';
import ThemeToggle from './ThemeToggle';
import CurrencyFilter from './Form'; 
import { jsPDF } from "jspdf";
import "jspdf-autotable";
import axios from 'axios';

const Raporty = () => {
  const [data, setData] = useState([]); 
  const [loading, setLoading] = useState(true); 
  const [chartUrl, setChartUrl] = useState('/cryptocurrency_info_today.png'); 
  const [trending, setTrending] = useState([]); 
  const [largestGainers, setLargestGainers] = useState([]); 

  // filtrowanie danych
  const filterData = (filter) => {
    const { searchTerm, currencyType, minValue, maxValue, sortOption } = filter;

    let filteredData = data;

    if (searchTerm) {
      filteredData = filteredData.filter(item =>
        item.name.toLowerCase().includes(searchTerm.toLowerCase())
      );
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
          filteredData.sort((a, b) => (b.change24H - a.change24H));
          break;
        default:
          break;
      }
    }

    setData(filteredData); 
  };

  // Pobieranie danych z API
  const fetchData = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/crypto/'); 
      const cryptoData = response.data;

      
      const uniqueData = {};

      cryptoData.forEach(item => {
        
        if (!uniqueData[item.id]) {
          uniqueData[item.id] = item;
        }
      });

      
      const uniqueCryptoData = Object.values(uniqueData);

      //to jest bez sensu
      const updatedData = uniqueCryptoData.map(item => {
        const change1H = (item.price * (item.percentage / 100)).toFixed(2);
        const change24H = (item.price * (item.percentage / 100) * 24).toFixed(2);

        
        const change7d = item.percentage 
          ? ((item.price * (1 + (item.percentage / 100) * 7)) - item.price).toFixed(2)
          : 'N/A';

        
        const marketCap = (item.price * 1000000000).toFixed(2);
        //

        return {
          ...item,
          change1H,
          change24H,
          change7d,
          marketCap
        };
      });

      setData(updatedData); 
      setLoading(false); 

      // trending
      const trendingData = updatedData
        .sort((a, b) => b.change1H - a.change1H) 
        .slice(0, 2); 

      setTrending(trendingData); 

      //largest gainers
      const largestGainersData = updatedData
        .sort((a, b) => (b.change1H - a.change1H)) 
        .slice(0, 2); 

      setLargestGainers(largestGainersData); 

    } catch (error) {
      console.error('Błąd podczas pobierania danych:', error);
      setLoading(false); 
    }
  };

  // pobieranie wykresu
  const fetchChartData = () => {
    const newUrl = `/cryptocurrency_info_today.png?timestamp=${new Date().getTime()}`;
    console.log('Fetching new chart URL:', newUrl);
    setChartUrl(newUrl);
  };

  useEffect(() => {
    fetchData(); 
    fetchChartData(); 

    const dataInterval = setInterval(() => {
      fetchData();  // Odświeżenie danych 
    },  120000); 

    const chartInterval = setInterval(() => {
      fetchChartData();  
    }, 60000); // 60000 ms = 1 minuta

    
    return () => {
      clearInterval(dataInterval);
      clearInterval(chartInterval);
    };
  }, []); 

  // generowanie raportu PDF
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
      crypto.change1H,
      crypto.change24H,
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
                    <td>${parseFloat(crypto.price).toFixed(2)}</td>
                    <td>{parseFloat(crypto.percentage).toFixed(2)}%</td>
                    <td>{parseFloat(crypto.change24H).toFixed(2)}%</td>
                    <td>{parseFloat(crypto.change7d).toFixed(2)}%</td>
                    <td>${parseFloat(crypto.marketCap).toFixed(2)}B</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Trending Gainers */}
          <div className="trending-gainers">
            <div className="trending">
              <h3>Trending 🔥</h3>
              <ul>
                {trending.map((crypto, index) => (
                  <li key={index}>{index + 1}. {crypto.name} ${parseFloat(crypto.price).toFixed(2)} </li>
                ))}
              </ul>
            </div>

            <div className="gainers">
              <h3>Largest Gainers 🚀</h3>
              <ul>
                {largestGainers.map((crypto, index) => (
                  <li key={index}>{index + 1}. {crypto.name} ${parseFloat(crypto.price).toFixed(2)} {parseFloat(crypto.change24H).toFixed(2)}%</li>
                ))}
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
};

export default Raporty;
