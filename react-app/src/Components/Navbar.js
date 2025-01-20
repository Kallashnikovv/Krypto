import React from 'react';
import { Link } from 'react-router-dom';  
import './Navbar.css';

const Navbar = () => {
    return (
        <nav>
            <Link to="/">Dashboard</Link>
            <Link to="/raporty">Raports</Link>
            <Link to="/faq">FAQ</Link>
            <Link to="/contact">Contact</Link>
        </nav>
    );
};

export default Navbar;