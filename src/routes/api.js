const express = require('express');
const router = express.Router();
const { executeQuery, testConnection } = require('../database');

router.get('/health', async (req, res) => {
  try {
    const isConnected = await testConnection();
    res.json({ 
      status: 'ok', 
      database: isConnected ? 'connected' : 'disconnected',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({ 
      status: 'error', 
      message: error.message 
    });
  }
});

router.post('/query', async (req, res) => {
  try {
    const { query } = req.body;
    
    if (!query || typeof query !== 'string') {
      return res.status(400).json({
        success: false,
        error: 'Query is required and must be a string'
      });
    }

    const trimmedQuery = query.trim();
    if (!trimmedQuery) {
      return res.status(400).json({
        success: false,
        error: 'Query cannot be empty'
      });
    }

    const allowedQueries = /^(SELECT|SHOW|DESCRIBE|EXPLAIN)/i;
    if (!allowedQueries.test(trimmedQuery)) {
      return res.status(403).json({
        success: false,
        error: 'Only SELECT, SHOW, DESCRIBE, and EXPLAIN queries are allowed'
      });
    }

    const result = await executeQuery(trimmedQuery);
    
    if (result.success) {
      res.json({
        success: true,
        data: result.data,
        rowCount: result.data.length
      });
    } else {
      res.status(400).json({
        success: false,
        error: result.error,
        code: result.code
      });
    }
    
  } catch (error) {
    console.error('API error:', error);
    res.status(500).json({
      success: false,
      error: 'Internal server error'
    });
  }
});

router.get('/tables', async (req, res) => {
  try {
    const result = await executeQuery('SHOW TABLES');
    
    if (result.success) {
      const tables = result.data.map(row => Object.values(row)[0]);
      res.json({
        success: true,
        tables: tables
      });
    } else {
      res.status(500).json({
        success: false,
        error: result.error
      });
    }
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

module.exports = router;