const http = require('http');

const PORT = process.env.PORT || 3000;
const APP_NAME = process.env.APP_NAME || 'Docker Learning App';

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/html' });
  res.end(`
    <html>
      <body style="font-family: Arial; text-align: center; padding: 50px; background: #0d1117; color: #58a6ff;">
        <h1>🐳 ${APP_NAME}</h1>
        <p style="color: #8b949e;">Running inside a Docker container!</p>
        <p style="color: #3fb950;">Port: ${PORT}</p>
        <p style="color: #8b949e;">Hostname: ${require('os').hostname()}</p>
      </body>
    </html>
  `);
});

server.listen(PORT, () => {
  console.log(`✅ Server running on port ${PORT}`);
  console.log(`🐳 Container ID: ${require('os').hostname()}`);
});
