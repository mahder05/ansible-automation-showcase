from flask import Flask

app = Flask(__name__)


@app.get("/")
def hello():
    return {"message": "Hello from the DevOps lab."}


@app.get("/health")
def health():
    return {"status": "healthy"}
