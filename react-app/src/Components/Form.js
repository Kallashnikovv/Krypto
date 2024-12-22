import React, { useState } from 'react';
import './Form.css';

const CurrencyFilter = ({ onFilter }) => {
  const [formData, setFormData] = useState({
    searchTerm: '',
    currencyType: 'all',  // Domyślnie wszystkie waluty
    minValue: '',
    maxValue: '',
    sortOption: '', // Domyślnie brak sortowania
  });

 
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  // Funkcja do filtrowania walut
  const handleSubmit = (e) => {
    e.preventDefault();

    const { searchTerm, currencyType, minValue, maxValue, sortOption } = formData;

    // filtr na min i max
    const minVal = minValue ? parseFloat(minValue) : null;
    const maxVal = maxValue ? parseFloat(maxValue) : null;

    if (minVal !== null && isNaN(minVal)) {
      alert('Min. wartość musi być liczbą.');
      return;
    }
    if (maxVal !== null && isNaN(maxVal)) {
      alert('Max. wartość musi być liczbą.');
      return;
    }
    if (minVal !== null && maxVal !== null && minVal > maxVal) {
      alert('Min. wartość nie może być większa niż Max. wartość.');
      return;
    }

    // Filtrowanie walut na podstawie danych
    const filterData = { searchTerm, currencyType, minValue, maxValue, sortOption };

    onFilter(filterData);
  };

  return (
    <form className="currency-filter" onSubmit={handleSubmit}>
      <input
        className="form-input"
        type="text"
        name="searchTerm"
        placeholder="Wyszukaj walutę"
        value={formData.searchTerm}
        onChange={handleChange}
      />
      <select
        className="form-select"
        name="currencyType"
        value={formData.currencyType}
        onChange={handleChange}
      >
        <option value="all">Wszystkie</option>
        <option value="fiat">Waluty Fiat</option>
        <option value="crypto">Kryptowaluty</option>
      </select>
      <input
        className="form-input"
        type="number"
        name="minValue"
        placeholder="Min. wartość"
        value={formData.minValue}
        onChange={handleChange}
      />
      <input
        className="form-input"
        type="number"
        name="maxValue"
        placeholder="Max. wartość"
        value={formData.maxValue}
        onChange={handleChange}
      />
      <select
        className="form-select"
        name="sortOption"
        value={formData.sortOption}
        onChange={handleChange}
      >
        <option value="">Sortuj po</option>
        <option value="priceAsc">Cenie rosnąco</option>
        <option value="priceDesc">Cenie malejąco</option>
        <option value="name">Nazwie</option>
        <option value="percentageChange">Zmianie %</option>
      </select>
      <button type="submit" className="form-button">Filtruj</button>
    </form>
  );
};

export default CurrencyFilter;
