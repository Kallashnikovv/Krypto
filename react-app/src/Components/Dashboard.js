import React, { useState, useEffect } from 'react';
import './Dashboard.css';
import Clock from './Clock';
import ThemeToggle from './ThemeToggle';
import CurrencyFilter from './Form';
import Navbar from './Navbar';
import NotificationBell from './NotificationBell';
import CryptoChart from './charts';

function Dashboard({ filteredCurrencies, onFilter }) {
  const [chartUrls, setChartUrls] = useState({
    bitcoin: '/cryptocurrency_info_today.png',
    ethereum: '/cryptocurrency_info_today.png',
    viacoin: '/cryptocurrency_info_today.png',
  });

  const [displayedCurrencies, setDisplayedCurrencies] = useState(filteredCurrencies);
  const [loading, setLoading] = useState(false);
  
  const getPrice = (coinName) => {
    const defaultCurrencies = [
      { name: 'Bitcoin', price: '94335.50' },
      { name: 'Ethereum', price: '3264.54' },
      { name: 'Viacoin', price: '0.23' }, 
    ];


    const coin = displayedCurrencies.find(currency => 
      currency.name.toLowerCase() === coinName.toLowerCase()
    );


    if (!coin) {
      const defaultCoin = defaultCurrencies.find(currency => 
        currency.name.toLowerCase() === coinName.toLowerCase()
      );
      return defaultCoin ? defaultCoin.price : 'N/A';
    }

    return parseFloat(coin.price).toFixed(2);
  };
  

  const fetchChartData = () => {
    setChartUrls({
      bitcoin: `/cryptocurrency_info_today.png?timestamp=${new Date().getTime()}`,
      ethereum: `/cryptocurrency_info_today.png?timestamp=${new Date().getTime()}`,
      viacoin: `/cryptocurrency_info_today.png?timestamp=${new Date().getTime()}`,
    });
  };

   // pobieranie danych z backendu
   const fetchCurrencies = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://127.0.0.1:8000/crypto/');
      const data = await response.json();
      setDisplayedCurrencies(data);
    } catch (error) {
      console.error('Błąd przy pobieraniu danych:', error);
    } finally {
      setLoading(false);
    }
  };
  // aktualizowanie URL wykresów

  useEffect(() => {
    fetchChartData();
    const interval = setInterval(fetchChartData, 60000000);
    return () => clearInterval(interval);
  }, []);

  // odświeżanie danych 
  useEffect(() => {
    const dataInterval = setInterval(fetchCurrencies, 120000000);
    return () => clearInterval(dataInterval);
  }, []);
  
  useEffect(() => {
    setDisplayedCurrencies(filteredCurrencies);
  }, [filteredCurrencies]);

  const getColorForChange = (change) => {
    const changeStr = String(change);
    return changeStr.startsWith('-') ? 'red' : 'green';
  };

  return (
    <div className="container">
      <NotificationBell />
      <ThemeToggle />
      <Navbar />
      <header> 
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
                <p className="wartoscb">${getPrice('Bitcoin')}</p>
              </div>
              <div className="box">
                <h1><i className="fa-brands fa-ethereum"></i></h1>
                <div className="wykresb">
                  {/* Ethereum */}
                  <CryptoChart coin="ethereum" />
                </div>
                <br /><br />
                <p className="wartoscb">${getPrice('Ethereum')}</p>
              </div>

              <div className="box">
                <h1><i className="fa-brands fa-viacoin"></i></h1>
                <div className="wykresb">
                  {/*  Viacoin */}
                  <CryptoChart coin="viacoin" />
                </div>
                <br /><br />
                <p className="wartoscb">${getPrice('Viacoin')}</p>
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
      {displayedCurrencies.length > 0 ? (
        displayedCurrencies.map((currency) => (
          <tr key={currency.id}>
            <td>{currency.id}</td>
            <td>{currency.name}</td>
            <td>{currency.symbol}</td>
            <td>${parseFloat(currency.price).toFixed(2)}</td>
            <td style={{ color: getColorForChange(currency.percentage) }}>
              {parseFloat(currency.percentage).toFixed(2)}%
            </td>
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
