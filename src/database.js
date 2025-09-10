const mysql = require('mysql2');

const pool = mysql.createPool({
  host: process.env.DB_HOST || 'mysql',
  port: process.env.DB_PORT || 3306,
  user: process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD || 'sakila_password',
  database: process.env.DB_NAME || 'sakila_es',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

const promisePool = pool.promise();

const executeQuery = async (query) => {
  try {
    const [rows] = await promisePool.execute(query);
    return { success: true, data: rows };
  } catch (error) {
    console.error('Database query error:', error);
    return { 
      success: false, 
      error: error.message,
      code: error.code 
    };
  }
};

const testConnection = async () => {
  try {
    const result = await executeQuery('SELECT 1 as test');
    console.log('Database connection successful');
    return result.success;
  } catch (error) {
    console.error('Database connection failed:', error);
    return false;
  }
};

module.exports = {
  executeQuery,
  testConnection,
  pool
};