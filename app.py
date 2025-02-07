from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    pod_name = os.getenv("POD_NAME", "Unknown Pod")
    return render_template('index.html', pod_name=pod_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
