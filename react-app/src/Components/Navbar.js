import React from 'react';
import { Link } from 'react-router-dom';  
import './Navbar.css';
const Navbar = () => {
    return (
        <nav>

                    <p><Link to="/">Dashboard</Link></p>

                    <p><Link to="/raporty">Raports</Link></p>

                    <p><Link to="/raporty">FAQ</Link></p>

                    <p><Link to="/">Contact</Link></p>
        </nav>
    );
};

export default Navbar;
