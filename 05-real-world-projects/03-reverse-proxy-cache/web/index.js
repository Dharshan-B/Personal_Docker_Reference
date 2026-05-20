const express = require('express');
const { createClient } = require('redis');
const app = express();

const redisHost = process.env.REDIS_HOST || 'localhost';
const client = createClient({
    url: `redis://${redisHost}:6379`
});

client.on('error', err => console.log('Redis Client Error', err));

async function initRedis() {
    await client.connect();
    console.log('✅ Connected to Redis Cache Server');
}
initRedis();

app.get('/data', async (req, res) => {
    const startTime = Date.now();
    try {
        const cachedValue = await client.get('product_data');
        if (cachedValue) {
            return res.json({
                source: 'Cache Hit (Redis)',
                timeTakenMs: Date.now() - startTime,
                data: JSON.parse(cachedValue)
            });
        }
        
        // Simulate a slow database query
        await new Promise(resolve => setTimeout(resolve, 1500));
        const dbData = { id: 101, name: 'Mega Product', price: 99.99 };
        
        // Cache the result for 60 seconds
        await client.setEx('product_data', 60, JSON.stringify(dbData));
        
        res.json({
            source: 'Cache Miss (Slow DB Run)',
            timeTakenMs: Date.now() - startTime,
            data: dbData
        });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.listen(3000, () => console.log('✅ Web app listening on port 3000'));
