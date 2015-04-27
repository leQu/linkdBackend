import MySQLdb

def connection():
    conn=MySQLdb.connect(host="localhost",
	  		 user="root",
			 passwd="hyh!yduG",
			 db="linkdDB")
    c=conn.cursor()

    return c, conn
