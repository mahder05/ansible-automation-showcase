from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from the DevOps Mastery Lab! Your container is running successfully."

if __name__ == '__main__':
    # Running on port 8080 and allowing connections from outside the container
    app.run(host='0.0.0.0', port=8080)
