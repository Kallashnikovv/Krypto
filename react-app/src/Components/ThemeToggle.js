import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSun, faMoon } from '@fortawesome/free-solid-svg-icons';
import './ThemeToggle.css';

function ThemeToggle() {
    const [isDarkMode, setIsDarkMode] = useState(() => {
        return localStorage.getItem('theme') === 'dark'; 
    });

    useEffect(() => {
        if (isDarkMode) {
            document.body.classList.add('dark-mode');
            document.body.classList.remove('light-mode');
        } else {
            document.body.classList.add('light-mode');
            document.body.classList.remove('dark-mode');
        }
        localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
    }, [isDarkMode]);

    const toggleTheme = () => {
        setIsDarkMode((prevMode) => !prevMode);
    };

    return (
        <div className="theme-toggle" onClick={toggleTheme}>
            {isDarkMode ? (
                <FontAwesomeIcon icon={faSun} size="2x" className="theme-icon dark-icon" />
            ) : (
                <FontAwesomeIcon icon={faMoon} size="2x" className="theme-icon light-icon" />
            )}
        </div>
    );
}

export default ThemeToggle;
