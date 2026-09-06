import { useState, useEffect } from 'react';
import axios from 'axios';

function HealthCheck() {
  const [healthStatus, setHealthStatus] = useState('loading');
  const [healthMessage, setHealthMessage] = useState('Checking backend connection...');
  const [dbStatus, setDbStatus] = useState('loading');
  const [dbMessage, setDbMessage] = useState('Checking database connection...');

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await axios.get('/api/health');
        setHealthStatus('success');
        setHealthMessage(response.data.message);
      } catch (error) {
        setHealthStatus('error');
        setHealthMessage('Failed to connect to backend. Make sure the server is running on port 5000.');
      }
    };

    const checkDatabase = async () => {
      try {
        const response = await axios.get('/api/db-status');
        if (response.data.database === 'Connected') {
          setDbStatus('success');
          setDbMessage('MongoDB is connected successfully!');
        } else {
          setDbStatus('error');
          setDbMessage('MongoDB is not connected. Make sure MongoDB is running.');
        }
      } catch (error) {
        setDbStatus('error');
        setDbMessage('Failed to check database status. Make sure MongoDB is running.');
      }
    };

    checkHealth();
    // Check database after a short delay
    const timer = setTimeout(checkDatabase, 500);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="health-check">
      <h2>🔍 System Status</h2>
      
      <div style={{ marginBottom: '2rem' }}>
        <h3>Backend Server</h3>
        <div className={`status ${healthStatus}`}>
          {healthStatus === 'loading' && '⏳ ' + healthMessage}
          {healthStatus === 'success' && '✅ ' + healthMessage}
          {healthStatus === 'error' && '❌ ' + healthMessage}
        </div>
      </div>

      <div>
        <h3>Database (MongoDB)</h3>
        <div className={`status ${dbStatus}`}>
          {dbStatus === 'loading' && '⏳ ' + dbMessage}
          {dbStatus === 'success' && '✅ ' + dbMessage}
          {dbStatus === 'error' && '❌ ' + dbMessage}
        </div>
      </div>
    </div>
  );
}

export default HealthCheck;
