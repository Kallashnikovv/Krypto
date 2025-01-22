import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Raporty from './Components/Raporty';
import Dashboard from './Components/Dashboard';
import Navbar from './Components/Navbar';
import Clock from './Components/Clock';
import ThemeToggle from './Components/ThemeToggle';

const App = () => {
  const [filteredCurrencies, setFilteredCurrencies] = useState([]);
  const [allCurrencies, setAllCurrencies] = useState([]);
  const [loading, setLoading] = useState(true);
  const removeDuplicates = (array) => {
    return array.filter((value, index, self) =>
      index === self.findIndex((t) => t.symbol === value.symbol)
    );
  };
  
  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await axios.get('http://127.0.0.1:8000/crypto/');
      if (response.data.length > 0) {
        const uniqueCurrencies = removeDuplicates(response.data);
        setAllCurrencies(uniqueCurrencies); 
        setFilteredCurrencies(uniqueCurrencies);
      }
    } catch (error) {
      console.error('Błąd zapytania API:', error);
    } finally {
      setLoading(false); 
    }
};
const updateData = async () => {
  try {
    await axios.post('http://127.0.0.1:8000/crypto/update');
    fetchData();  
  } catch (error) {
    console.error('Błąd podczas aktualizacji danych:', error);
  }
};
useEffect(() => {
  fetchData();
  //  aktualizacja danych co 2 minuty
  const interval = setInterval(updateData, 12000000);
  return () => clearInterval(interval);
}, []);
const handleFilter = (filterData) => {
  const { searchTerm, currencyType, minValue, maxValue, sortOption } = filterData;

  const filtered = allCurrencies.filter(currency => {
    const matchesSearchTerm = (currency.name && currency.name.toLowerCase().includes(searchTerm.toLowerCase())) || 
      (currency.symbol && currency.symbol.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesCurrencyType = currencyType === 'all' || currency.type === currencyType;
    const matchesMinValue = minValue === '' || currency.price >= parseFloat(minValue);
    const matchesMaxValue = maxValue === '' || currency.price <= parseFloat(maxValue);
    return matchesSearchTerm && matchesCurrencyType && matchesMinValue && matchesMaxValue;
  });

  const uniqueCurrencies = removeDuplicates(filtered);
  const sorted = uniqueCurrencies.sort((a, b) => {
    switch (sortOption) {
      case 'priceAsc':
        return a.price - b.price;
      case 'priceDesc':
        return b.price - a.price;
      case 'name':
        return a.name.localeCompare(b.name);
      case 'percentage':
        return a.percentage - b.percentage;
      default:
        return 0;
    }
  });

  setFilteredCurrencies(sorted);
};
if (loading) return <div>Loading...</div>;

  return (
    <Router>
      <div> 
      <Routes>
          <Route 
            path="/" 
            element={<Dashboard filteredCurrencies={filteredCurrencies} onFilter={handleFilter} />} 
          />
          <Route 
            path="/raporty" 
            element={<Raporty filteredCurrencies={filteredCurrencies} />} 
          />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
