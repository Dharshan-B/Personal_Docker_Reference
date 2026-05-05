from flask import Flask
import redis
import os

app = Flask(__name__)

# Connect to Redis using container name (thanks to Docker networking!)
redis_client = redis.Redis(
    host=os.environ.get('REDIS_HOST', 'redis'),
    port=int(os.environ.get('REDIS_PORT', 6379)),
    decode_responses=True
)

@app.route('/')
def index():
    # Increment visit counter in Redis
    count = redis_client.incr('hits')
    return f'''
    <html>
      <body style="font-family: Arial; text-align: center; padding: 50px;
                   background: #0d1117; color: #c9d1d9;">
        <h1 style="color: #58a6ff;">🐳 Flask + Redis Demo</h1>
        <h2 style="color: #3fb950;">Page visits: {count}</h2>
        <p style="color: #8b949e;">Redis is storing the count across requests!</p>
        <p style="color: #8b949e;">Refresh the page to increment</p>
      </body>
    </html>
    '''

@app.route('/reset')
def reset():
    redis_client.set('hits', 0)
    return '<p>Counter reset! <a href="/">Go back</a></p>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
