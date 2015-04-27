from flask import Flask, request
import MySQLdb
from DBconnect import connection
from MySQLdb import escape_string as thwart
import gc
import json

app = Flask(__name__)

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
            #x=c.execute("SELECT chat_ID FROM chats WHERE chat_name='{0}'".format(thwart(chat))) --NOT NEEDED

	c.execute("INSERT INTO messages VALUES ((SELECT chat_ID FROM chats WHERE chat_name='{0}'), now(), '{1}', '{2}')".format(thwart(chat), thwart(user), thwart(message)))

	#y=c.execute("SELECT user_name, message FROM messages WHERE chat_ID ='{0}' ORDER BY time_created".format(thwart(str(x)))) -- Not working since y=amount of rows

	conn.commit()
	c.close()
	conn.close()
	gc.collect()

	return "should work" 

    return "What u want?"

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
   app.run(debug=True)
