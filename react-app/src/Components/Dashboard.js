import React, { useState, useEffect } from 'react';
import './Dashboard.css';
import Clock from './Clock';
import ThemeToggle from './ThemeToggle';
import CurrencyFilter from './Form';
import Navbar from './Navbar';
import CryptoChart from './charts';// Importujemy nasz nowy komponent


function Dashboard({ filteredCurrencies, onFilter }) {
  const [chartUrls, setChartUrls] = useState({
    bitcoin: '/cryptocurrency_info_today.png',
    ethereum: '/cryptocurrency_info_today.png',
    viacoin: '/cryptocurrency_info_today.png',
  });

  const fetchChartData = () => {
    // Zmieniamy URL obrazka, aby wymusić jego odświeżenie (dodajemy unikalny parametr)
    setChartUrls({
      bitcoin: `/cryptocurrency_info_today.png?timestamp=${new Date().getTime()}`,
      ethereum: `/cryptocurrency_info_today.png?timestamp=${new Date().getTime()}`,
      viacoin: `/cryptocurrency_info_today.png?timestamp=${new Date().getTime()}`,
    });
  };

  useEffect(() => {
    fetchChartData();
    const interval = setInterval(() => {
      fetchChartData();
    }, 60000); // 60000ms = 1 minuta

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
          <CurrencyFilter onFilter={onFilter} />
          
          <main>
            <div className="boxy">
              <div className="box">
                <h1><i className="fa-brands fa-bitcoin"></i></h1>
                <div className="wykresb">
                  {/*  Bitcoin */}
                  <CryptoChart coin="bitcoin" />
                </div>
                <br /><br />
                <p className="wartoscb">$27,000</p>
              </div>
              <div className="box">
                <h1><i className="fa-brands fa-ethereum"></i></h1>
                <div className="wykresb">
                  {/* Ethereum */}
                  <CryptoChart coin="ethereum" />
                </div>
                <br /><br />
                <p className="wartoscb">$1,800</p>
              </div>
              <div className="box">
                <h1><i className="fa-brands fa-viacoin"></i></h1>
                <div className="wykresb">
                  {/*  Viacoin */}
                  <CryptoChart coin="viacoin" />
                </div>
                <br /><br />
                <p className="wartoscb"> $0.50</p>
              </div>
            </div>

            <div className="market_czas">
              <div className="market_overview">
                <h2>MARKET OVERVIEW</h2>
                <div className="wykres_market">
                  <img src={chartUrls.bitcoin} alt="Cryptocurrency Chart" className="chart-img" />
                </div>
              </div>

              <div className="box_z_czasem">
                <Clock />
              </div>
            </div>

            <div className="recent-activities">
              <p id="tytula">RECENT ACTIVITIES</p>
              <div id="dane">
                <table>
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Cryptocurrency Name</th>
                      <th>Symbol</th>
                      <th>Price (USD)</th>
                      <th>Change 1h (%)</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredCurrencies.length > 0 ? (
                      filteredCurrencies.map((currency) => (
                        <tr key={currency.id}>
                          <td>{currency.id}</td>
                          <td>{currency.name}</td>
                          <td>{currency.symbol}</td>
                          <td>${currency.price}</td>
                          <td>{currency.percentageChange}%</td>
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td colSpan="5">No results found</td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </main>
        </div>

        <aside className="prawa"></aside>
      </div>

      <footer>
        <br /><br />
      </footer>
    </div>
  );
}

export default Dashboard;
