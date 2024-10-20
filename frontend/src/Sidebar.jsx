import React, { useState } from 'react';
import './Sidebar.css';

function Sidebar() {
  const [isOpen, setIsOpen] = useState(true);

  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className={`sidebar ${isOpen ? 'open' : 'closed'}`}>
      <button className="toggle-button" onClick={toggleSidebar}>
        {isOpen ? '<' : '>'}
      </button>
      {isOpen && (
        <div className="content">
          <h1>INFERmary</h1>
          <h3>viral spread simulator.</h3>
          <div className="section">
            <strong>City:</strong> San Francisco
          </div>
          <div className="section">
            <strong>Population:</strong> 788,478
          </div>
          <div className="section">
            <strong>Population Density:</strong> 18,633 per square mile
          </div>
          <div className="section">
            <strong>Land Area:</strong> 46.87 square miles
          </div>
          <div className="section">
            <h3>Simulation Parameters</h3>
            <div>
              Virus Reproduction Number: 
              <input type="number" value="3" readOnly size="4" maxLength="4"/>
            </div>
            <div>
              Number of Initial Infected: 
              <input type="number" value="15" readOnly size="4" maxLength="4"/>
            </div>
          </div>
          <div className="section">
            <h3>Other Factors</h3>
            <textarea placeholder="Describe any other factors in plain text..."></textarea>
          </div>
          <button className="begin-button">Begin Simulation</button>
        </div>
      )}
    </div>
  );
}

export default Sidebar;