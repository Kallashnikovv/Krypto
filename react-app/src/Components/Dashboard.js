import React from 'react';
import './Dashboard.css';
import Clock from './Clock';
import ThemeToggle from './ThemeToggle';
import CurrencyFilter from './Form';
import Navbar from './Navbar';

function Dashboard({ filteredCurrencies, onFilter }) {
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
                <div className="wykresb"></div>
                <br /><br />
                <p className="wartoscb">$1234</p>
              </div>
              <div className="box">
                <h1><i className="fa-brands fa-ethereum"></i></h1>
                <div className="wykresb"></div>
                <br /><br />
                <p className="wartoscb">$777</p>
              </div>
              <div className="box">
                <h1><i className="fa-brands fa-viacoin"></i></h1>
                <div className="wykresb"></div>
                <br /><br />
                <p className="wartoscb">$2137</p>
              </div>
            </div>

            <div className="market_czas">
              <div className="market_overview">
                <h2>MARKET OVERVIEW</h2>
                <div className="wykres_market"></div>
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
