import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Test() {
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    // Test the connection to the Flask backend when component mounts
    fetchDataFromBackend();
  }, []);

  const fetchDataFromBackend = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/test');
      setMessage(response.data.message);
      setError('');
    } catch (err) {
      setError('Failed to connect to the backend');
      console.error('Error:', err);
    }
  };


  return (
    <div className="test-container">
      <h2>Backend Connection Test</h2>
      
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {message && <p>{message}</p>}
          
    </div>
  );
}

export default Test;
