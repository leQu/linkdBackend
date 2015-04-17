from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def post_message():
    if request.method == 'POST':
        message=request.form['message']

        return message

@app.route('/<string:chatname>', methods=['GET'])
def get_messages(chatname):
    #function to get the latest 25 messages and their users from the DB and return them
    return chatname

if __name__ == '__main__':
    app.run(debug=True)