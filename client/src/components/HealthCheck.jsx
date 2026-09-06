import { useState, useEffect } from 'react';
import axios from 'axios';

function HealthCheck() {
  const [status, setStatus] = useState('loading');
  const [message, setMessage] = useState('Checking backend connection...');

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await axios.get('/api/health');
        setStatus('success');
        setMessage(response.data.message);
      } catch (error) {
        setStatus('error');
        setMessage('Failed to connect to backend. Make sure the server is running on port 5000.');
      }
    };

    checkHealth();
  }, []);

  return (
    <div className="health-check">
      <h2>Backend Health Check</h2>
      <div className={`status ${status}`}>
        {status === 'loading' && '⏳ ' + message}
        {status === 'success' && '✅ ' + message}
        {status === 'error' && '❌ ' + message}
      </div>
    </div>
  );
}

export default HealthCheck;
