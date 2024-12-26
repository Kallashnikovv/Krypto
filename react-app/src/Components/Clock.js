// Components/Clock.js
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

    return (
        <div style={{ display: 'flex', alignItems: 'center' }}>
        <div style={{ lineHeight: '1.2' }}>
            <p style={{ margin: 0 }}>Date: {formatDate}</p>
            <p style={{ margin: 0 }}>Time: {formatTime}</p>
        </div>
    </div>
    );
}

export default Clock;

