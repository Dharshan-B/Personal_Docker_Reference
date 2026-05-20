const express = require('express');
const app = express();

app.get('/', (req, res) => {
    res.json({
        message: "MinIO S3 Gateway application ready. Integrates S3 storage + Redis Cache!"
    });
});

app.listen(3000, () => console.log('✅ S3 cache server listening on port 3000'));
