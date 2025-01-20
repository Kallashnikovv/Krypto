import React, { useState, useEffect } from 'react';

function Clock() {
    const [currentTime, setCurrentTime] = useState(new Date());

    useEffect(() => {
        const timerId = setInterval(() => {
            setCurrentTime(new Date());
        }, 1000);

        return () => clearInterval(timerId);
    }, []);

    const formatTime = currentTime.toLocaleTimeString();
    const formatDate = currentTime.toLocaleDateString();
    const currentMonth = currentTime.toLocaleString('en-US', { month: 'long' });
    const currentYear = currentTime.getFullYear();

    const generateCalendar = (date) => {
        const year = date.getFullYear();
        const month = date.getMonth();

        const firstDay = (new Date(year, month, 1).getDay() + 6) % 7;
        const daysInMonth = new Date(year, month + 1, 0).getDate();

        const calendarDays = [];
        for (let i = 0; i < firstDay; i++) {
            calendarDays.push(null); 
        }
        for (let day = 1; day <= daysInMonth; day++) {
            calendarDays.push(day);
        }

        return calendarDays;
    };

    const calendarDays = generateCalendar(currentTime);
    const today = currentTime.getDate();

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', fontSize: '1rem' }}>
            <div style={{ textAlign: 'center', marginTop: '10px' }}>
                <h3 style={{ marginBottom: '5px', fontSize: '1.2rem' }}>Calendar</h3>
                <h4 style={{ margin: '5px 0', color: '#6a6af7', fontSize: '1rem' }}>
                    {currentMonth} {currentYear}
                </h4>
                <table style={{ borderCollapse: 'collapse', width: '100%', maxWidth: '250px' }}>
                    <thead>
                        <tr>
                            <th style={headerStyle}>Mon</th>
                            <th style={headerStyle}>Tue</th>
                            <th style={headerStyle}>Wed</th>
                            <th style={headerStyle}>Thu</th>
                            <th style={headerStyle}>Fri</th>
                            <th style={headerStyle}>Sat</th>
                            <th style={headerStyle}>Sun</th>
                        </tr>
                    </thead>
                    <tbody>
                        {Array.from({ length: Math.ceil(calendarDays.length / 7) }, (_, i) => (
                            <tr key={i}>
                                {calendarDays.slice(i * 7, i * 7 + 7).map((day, index) => (
                                    <td
                                        key={index}
                                        style={{
                                            ...dayStyle,
                                            backgroundColor: day === today ? '#8c8cfc' : 'white',
                                            color: day === today ? 'white' : 'black',
                                        }}
                                    >
                                        {day || ""}
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            <div style={{ marginTop: '15px', letterSpacing: '0.05em', fontSize: '1.1rem', lineHeight: '1.5' }}>
                <p style={{ margin: 0 }}>Date: {formatDate}</p>
                <p style={{ margin: 0 }}>Time: {formatTime}</p>
            </div>
        </div>
    );
}

const headerStyle = {
    border: '1px solid #ccc',
    padding: '10px',
    backgroundColor: '#f4f4f4',
    fontWeight: 'bold',
    fontSize: '0.9rem',
};

const dayStyle = {
    border: '1px solid #ccc',
    padding: '15px',
    textAlign: 'center',
    cursor: 'default',
    fontSize: '0.9rem',
};

export default Clock;
