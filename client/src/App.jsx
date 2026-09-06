import { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import HealthCheck from './components/HealthCheck';

function App() {
  return (
    <div>
      <Navbar />
      <div className="container">
        <HealthCheck />
      </div>
    </div>
  );
}

export default App;
