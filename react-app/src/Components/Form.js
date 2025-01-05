import React, { useState } from 'react';
import './Form.css';

const CurrencyFilter = ({ onFilter }) => {
  const [formData, setFormData] = useState({
    searchTerm: '',
    currencyType: 'all',
    minValue: '',
    maxValue: '',
    sortOption: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const { searchTerm, currencyType, minValue, maxValue, sortOption } = formData;
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
