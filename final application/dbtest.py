import sqlite3

conn=sqlite3.connect('cpe3.db')

cursor=conn.cursor()

a,b=4,45

query="select * from cpe3 ;"

cursor.execute(query)

rows = cursor.fetchall()
col_names = [desc[0] for desc in cursor.description]
conn.close()

results = [dict(zip(col_names, row)) for row in rows]

print(results)