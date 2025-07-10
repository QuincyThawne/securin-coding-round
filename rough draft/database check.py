import sqlite3

conn = sqlite3.connect("cpe2.db")
print("DB connected")
cursor = conn.cursor()
cursor.execute("Select title from cpe2;")
rows = cursor.fetchall()
col_names = [desc[0] for desc in cursor.description]

conn.close()

results = [dict(zip(col_names, row)) for row in rows]
print("Printing DB:\n")
print( results)

