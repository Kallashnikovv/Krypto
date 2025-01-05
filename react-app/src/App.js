import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CurrencyFilter from './Components/Form';
import Raporty from './Components/Raporty';
import Dashboard from './Components/Dashboard';
import Navbar from './Components/Navbar';
import Clock from './Components/Clock';
import ThemeToggle from './Components/ThemeToggle';


const App = () => {
  const [filteredCurrencies, setFilteredCurrencies] = useState([]); 
  const [allCurrencies, setAllCurrencies] = useState([]);  
  const [loading, setLoading] = useState(true);  
  const [error, setError] = useState(null);  
  const [sortOption, setSortOption] = useState(''); 
  useEffect(() => {
    // Zakomentowany kod do połączenia z prawdziwym API
    /*
    const fetchData = async () => {
      //to zignoruj-> https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?CMC_PRO_API_KEY=46977feb-96d6-4469-80ca-f45dcd381ec7
      const apiURL = `https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest`;
      const apiKey = '46977feb-96d6-4469-80ca-f45dcd381ec7';  

      try {
        setLoading(true);
        setError(null);  

        const response = await fetch(apiURL, {
          headers: {
            'X-CMC_PRO_API_KEY': apiKey,
          },
        });

        if (!response.ok) {
          throw new Error("Błąd połączenia z API");
        }

        const data = await response.json();

        // Mapowanie danych z API na odpowiedni format
        const currencies = data.data.map((currency) => ({
          id: currency.id,
          name: currency.name,
          symbol: currency.symbol,
          price: currency.quote.USD.price,
          percentageChange: currency.quote.USD.percent_change_1h,
          type: 'crypto',
        }));

        setAllCurrencies(currencies);
        setFilteredCurrencies(currencies);  
      } catch (error) {
        setError("Błąd podczas pobierania danych z API");
      } finally {
        setLoading(false); 
      }
    };

    fetchData();  // Wywołanie funkcji pobierania danych
    */
    // Przykładowe dane walut 
    const exampleData = [
      { id: 1, name: "Bitcoin", symbol: "BTC", price: 27000, percentageChange: -1.8, type: "crypto" },
      { id: 2, name: "Ethereum", symbol: "ETH", price: 1650, percentageChange: 0.7, type: "crypto" },
      { id: 3, name: "Litecoin", symbol: "LTC", price: 70, percentageChange: -0.3, type: "crypto" },
      { id: 4, name: "Ripple", symbol: "XRP", price: 0.42, percentageChange: 2.1, type: "crypto" },
      { id: 5, name: "Cardano", symbol: "ADA", price: 0.25, percentageChange: -0.4, type: "crypto" },
      { id: 6, name: "Viacoin", symbol: "VIA", price: 0.18, percentageChange: -2.0, type: "crypto" },
      { id: 7, name: "USD", symbol: "USD", price: 1, percentageChange: 0.0, type: "fiat" },
      { id: 8, name: "EUR", symbol: "EUR", price: 1.08, percentageChange: 0.2, type: "fiat" }
    ]
    
    setAllCurrencies(exampleData);
    setFilteredCurrencies(exampleData);  
    setLoading(false);
  }, []);

  const handleSort = (option) => {
    setSortOption(option);  
  };

  const handleFilter = (filterData) => {
    const { searchTerm, currencyType, minValue, maxValue, sortOption } = filterData;

    const filtered = allCurrencies.filter(currency => {
     //filtrowanie po nazwie lub symbolu
      const matchesSearchTerm = (currency.name && currency.name.toLowerCase().includes(searchTerm.toLowerCase())) || 
        (currency.symbol && currency.symbol.toLowerCase().includes(searchTerm.toLowerCase()));

      // Filtrowanie po typie waluty 
      const matchesCurrencyType = currencyType === 'all' || currency.type === currencyType;
      
      // Filtrowanie po cenie
      const matchesMinValue = minValue === '' || currency.price >= parseFloat(minValue);
      const matchesMaxValue = maxValue === '' || currency.price <= parseFloat(maxValue);
  
      return matchesSearchTerm && matchesCurrencyType && matchesMinValue && matchesMaxValue;
    });

    // Zaawansowane filtry walut
    const sorted = filtered.sort((a, b) => {
      if (sortOption === 'priceAsc') {
        return a.price - b.price; // Sortowanie po cenie rosnąco
      }
      if (sortOption === 'priceDesc') {
        return b.price - a.price; // Sortowanie po cenie malejąco
      }
      if (sortOption === 'name') {
        return a.name.localeCompare(b.name); // Sortowanie po nazwie
      }
      if (sortOption === 'percentageChange') {
        return a.percentageChange - b.percentageChange; // Sortowanie po zmianie procentowej
      }
      return 0;
    });

    setFilteredCurrencies(sorted); // 
  };
 
  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <Router>
      <div>
        <Navbar />
        <Clock /> 
        <ThemeToggle /> 
        <Routes> 
          <Route exact path="/" element={<Dashboard filteredCurrencies={filteredCurrencies} onFilter={handleFilter} />} />
          <Route path="/raporty" element={<Raporty filteredCurrencies={filteredCurrencies} onFilter={handleFilter} />} />
        </Routes>

          
      </div>
    </Router>
  );
};

export default App;
