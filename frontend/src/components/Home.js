import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css'; // You'll need to create this CSS file

function Home() {
  const navigate = useNavigate();

  return (
    <div className="home-container">
      <h1>Welcome to Our App</h1>
      <div className="content">
        <p>This is a simple home page built with React.</p>
        <div className="navigation-buttons">
          <button className="nav-button" onClick={() => navigate('/profile')}>
            Go to Profile
          </button>
          <button className="nav-button" onClick={() => navigate('/test')}>
            Take a Test
          </button>
          <button className="nav-button" onClick={() => navigate('/main')}>
            Go to Main
          </button>
        </div>
      </div>
    </div>
  );
}

export default Home;
