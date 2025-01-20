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
        placeholder="Search Currency"
        value={formData.searchTerm}
        onChange={handleChange}
      />
      <select
        className="form-select"
        name="currencyType"
        value={formData.currencyType}
        onChange={handleChange}
      >
        <option value="all"> All Currencies </option>
        <option value="fiat">Fiat</option>
        <option value="crypto">Cryptocurrencies</option>
      </select>
      <input
        className="form-input"
        type="number"
        name="minValue"
        placeholder="Min. value"
        value={formData.minValue}
        onChange={handleChange}
      />
      <input
        className="form-input"
        type="number"
        name="maxValue"
        placeholder="Max. value"
        value={formData.maxValue}
        onChange={handleChange}
      />
      <select
        className="form-select"
        name="sortOption"
        value={formData.sortOption}
        onChange={handleChange}
      >
        <option value="">Sort by</option>
        <option value="priceAsc">Ascending Price</option>
        <option value="priceDesc">Descending Price</option>
        <option value="name">Name</option>
        <option value="percentageChange">Change % </option>
      </select>
      <button type="submit" className="form-button">Filter</button>
    </form>
  );
};

export default CurrencyFilter;