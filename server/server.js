import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import connectDB from './config/database.js';

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// Connect to MongoDB
connectDB();

// Middleware
app.use(cors());
app.use(express.json());

// Basic Health Check Endpoint
app.get('/api/health', (req, res) => {
  res.json({
    success: true,
    message: 'Backend is running successfully!',
    timestamp: new Date().toISOString()
  });
});

// Database Status Endpoint
app.get('/api/db-status', (req, res) => {
  const dbConnected = require('mongoose').connection.readyState === 1;
  res.json({
    success: true,
    database: dbConnected ? 'Connected' : 'Disconnected',
    mongodb: process.env.MONGODB_URI,
    timestamp: new Date().toISOString()
  });
});

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    message: 'Welcome to CycleCare API',
    version: '1.0.0',
    endpoints: {
      health: '/api/health',
      dbStatus: '/api/db-status'
    }
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    success: false,
    message: 'Something went wrong!',
    error: process.env.NODE_ENV === 'development' ? err.message : {}
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`\n🚀 CycleCare Backend Server running on http://localhost:${PORT}`);
  console.log(`📝 Health check available at http://localhost:${PORT}/api/health`);
  console.log(`🗄️  Database status available at http://localhost:${PORT}/api/db-status\n`);
});
