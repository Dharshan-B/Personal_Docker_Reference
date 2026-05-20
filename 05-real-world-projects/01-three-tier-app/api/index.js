const express = require('express');
const { Pool } = require('pg');
const app = express();

const pool = new Pool({
    connectionString: process.env.DATABASE_URL
});

app.get('/users', async (req, res) => {
    try {
        const result = await pool.query('SELECT NOW()');
        res.json([
            { id: 1, name: 'Alice (Mock)' },
            { id: 2, name: 'Bob (Mock)' },
            { db_time: result.rows[0].now }
        ]);
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'DB Connection failed', details: err.message });
    }
});

app.listen(5000, () => console.log('✅ API listening on port 5000'));
