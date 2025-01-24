import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement);

const CryptoChart = ({ coin }) => {
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          `https://api.coingecko.com/api/v3/coins/${coin}/market_chart?vs_currency=usd&days=30&interval=daily`
        );
        const result = await response.json();
        const labels = result.prices.map((item) => {
          const date = new Date(item[0]);
          return `${date.getDate()}/${date.getMonth() + 1}`;
        });

        const prices = result.prices.map((item) => item[1]);

        const dynamicData = {
          labels,
          datasets: [
            {
              label: coin.charAt(0).toUpperCase() + coin.slice(1),
              data: prices,
              fill: false,  
              borderColor: getBorderColor(prices),
              borderWidth: 5,
              tension: 0.3,
            },
          ],
        };

        setData(dynamicData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [coin]);

  const getBorderColor = (prices) => {
    if (prices && prices.length > 0) {
      const firstPrice = prices[0];
      const lastPrice = prices[prices.length - 1];
      return lastPrice > firstPrice ? '#00FF00' : '#FF0000';
    }
    return '#7674b8'; 
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
        grid: {
          display: false,  
        },
      },
      y: {
        ticks: {
          display: false, 
        },
        grid: {
          display: false,  
        },
      },
    },
    
    layout: {
      padding: {
        left: 0,
        right: 0,
        top: 0,
        bottom: 0,
      },
    },
    
    backgroundColor: 'transparent',
  };

  if (!data) return <div>Loading...</div>;

  return <Line data={data} options={options} />;
};

export default CryptoChart;
