//na razie dane statyczne -> dodac pozniej pobieranie danych z api
import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement);

const CryptoChart = ({ coin }) => {
  const [data, setData] = useState(null);

  useEffect(() => {

    const staticData = {
      labels: ['2021', '2022', '2023', '2024', '2025'], 
      datasets: [
        {
          label: coin.charAt(0).toUpperCase() + coin.slice(1),
          data: getDummyData(coin), 
          fill: false,
          borderColor: getBorderColor(coin), 
          tension: 0.1,
        },
      ],
    };

    setData(staticData);
  }, [coin]);

  
  const getDummyData = (coin) => {
    switch (coin) {
      case 'bitcoin':
        return [1000, 2000, 1500, 2500, 1800];
      case 'ethereum':
        return [500, 1500, 1300, 1800, 2200]; 
      case 'viacoin':
        return [50, 100, 80, 120, 160]; 
      default:
        return [0, 0, 0, 0, 0]; 
    }
  };

  
  const getBorderColor = (coin) => {
    switch (coin) {
      case 'bitcoin':
        return '#7674b8'; 
      case 'ethereum':
        return '#7674b8'; 
      case 'viacoin':
        return '#7674b8'; 
      default:
        return '#000000';
    }
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          display: false, 
        },
      },
      tooltip: {
        enabled: false, 
      },
    },
    elements: {
      point: {
        radius: 0, 
      },
    },
    scales: {
      x: {
        ticks: {
          display: false,
        },
      },
      y: {
        ticks: {
          display: false, 
        },
      },
    },
  };

  if (!data) return <div>Loading...</div>;

  return <Line data={data} options={options} />;
};

export default CryptoChart;
