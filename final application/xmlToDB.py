import sqlite3

f=open("cpe.txt",'r',encoding='UTF-8')
l1=[]
l2=[]
l3=[]
for i in f.readlines():
    if "</cpe-item>" in i and len(l2)!=0:
        if len(l2)==1:
            l2.append("")
        l1.append(l2)
        l2=[]
    if "title" in i:
        x=i.split('>')[1]
        y=x.split('<')[0]
        l2.append(y)
    if "reference href" in i:
        a=i.split('"')[1]
        l3.append(str(a))
    if "/references" in i:
        st=" ".join(l3)
        l2.append(st)
        l3=[]
        
print(l1)

conn = sqlite3.connect("cpe3.db")
print("DB created")
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS cpe3")
creation_query="""
CREATE TABLE cpe3(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    urls TEXT
);
"""

cursor.execute(creation_query)

for i in l1:
    cursor.execute("""
        INSERT INTO cpe3 (
            title, urls
        ) VALUES (?, ?)
    """, (
        i[0],
        i[1]
    ))

    cursor = conn.cursor()
base_query="select * from cpe3;"
cursor.execute(base_query)
rows = cursor.fetchall()
col_names = [desc[0] for desc in cursor.description]
conn.commit()
conn.close()

results = [dict(zip(col_names, row)) for row in rows]
