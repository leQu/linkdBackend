from flask import Flask, request
import MySQLdb
from DBconnect import connection
from MySQLdb import escape_string as thwart
import gc
import json
from flask.ext.socketio import SocketIO, emit, send, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/', methods=['POST', 'GET'])
def post_message():
    if request.method == 'POST':
        message=request.form['message']
        user=request.form['user_name']
        chat=request.form['chat_name']
        c, conn=connection()

        x=c.execute("SELECT chat_ID FROM chats WHERE chat_name='{0}'".format(thwart(chat)))

        if str(x)=='0':
            c.execute("INSERT INTO chats (chat_name) VALUES ('{0}')".format(thwart(chat)))

        c.execute("INSERT INTO messages VALUES ((SELECT chat_ID FROM chats WHERE chat_name='{0}'), now(), '{1}', '{2}')".format(thwart(chat), thwart(user), thwart(message)))

        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        return "should work"

    return "What u want?"

@socketio.on('join room')
def on_join_room(chat):
    join_room(chat)

@socketio.on('leave room')
def on_leave_room(chat):
    leave_room(chat)

@socketio.on('message my room')
def on_room_event(data):
    myroom = data.pop('room')
    emit('room message', data, room=myroom)

@app.route('/<string:chatname>', methods=['GET'])
def get_messages(chatname):
    c,conn=connection()
    try:
        c.execute("SELECT user_name, message from messages WHERE chat_ID=(SELECT chat_ID FROM chats WHERE chat_name='{0}' ORDER BY time_created)".format(thwart(chatname)))
        data = c.fetchall()
        jsonObj = json.dumps(data)

    except Exception as e:
        return(str(e))

    conn.commit()
    c.close()
    conn.close()
    gc.collect()

    return jsonObj

if __name__ == '__main__':
    socketio.run(app)
