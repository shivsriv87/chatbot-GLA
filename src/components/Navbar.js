import React, { useState } from 'react';
import './Navbar.css';
import logo from './ogo.png';  // Ensure this path is correct based on your structure

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <nav className="navbar">
      <div className="logo">
        <img src={logo} alt="Logo" />
      </div>
      <div className={`hamburger ${isOpen ? 'active' : ''}`} onClick={toggleMenu}>
        <div />
        <div />
        <div />
      </div>
      <ul className={`nav-links ${isOpen ? 'show' : 'hide'}`}>
        <li><a href="#home">Home</a></li>
        <li><a href="#faculty">Faculty</a></li>
        <li><a href="#form">Form</a></li>
        <li><a href="#about">About</a></li>
        <li><a href="#admin-login">Admin Login</a></li>
      </ul>
    </nav>
  );
};

export default Navbar;
