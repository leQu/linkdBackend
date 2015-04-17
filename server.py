from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Alex World!"

@app.route("/messages")
def messages():
	return "All messages :)"

if __name__ == "__main__":
    app.run()
