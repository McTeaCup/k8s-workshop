from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    pod_name = os.getenv("POD_NAME", "Unknown Pod")
    return f"<h1>Version 2: Served from Pod: {pod_name}</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
