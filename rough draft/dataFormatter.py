from flask import Flask, request, jsonify
import xmltodict
import pprint
import json
import sqlite3

output=[]

app = Flask(__name__)

def db_full_return():

    conn = sqlite3.connect("cpe2.db")
    
    cursor = conn.cursor()
    base_query="select * from cpe2;"
    cursor.execute(base_query)
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    conn.close()

    results = [dict(zip(col_names, row)) for row in rows]
    data=results
    return data

    

def db_access(filters):
    conn = sqlite3.connect("cpe2.db")
    
    cursor = conn.cursor()

    base_query="Select * from cpe2"
    conditions = []
    values = []

    for key, value in filters.items():
        if key in ["title","urls"]:
            conditions.append(f"{key} LIKE ?")
            values.append(f"%{value}%")
        elif key in ["id"]:
            conditions.append(f"{key}=")
            values.append(int(value))
    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)

    cursor.execute(base_query, values)
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    conn.close()

    results = [dict(zip(col_names, row)) for row in rows]
    return results

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to the cpe API",
        "endpoints": {
            "/search": "Filter recipes by key=value pairs (e.g., ?title=07FLY)",
            "/dump": "return entire table"
        }
    })

@app.route("/search", methods=["GET"])
def filter_recipes():
    filters = request.args.to_dict()
    print(filters)
    if not filters:
        return jsonify({"error": "No filters provided"}), 400

    data = db_access(filters)
    return jsonify(data)

@app.route("/dump",methods=["GET"])
def dump():
    data=db_full_return()
    print(data)
    return jsonify(data)

if __name__ == "__main__":

    with open('dump.xml', 'r', encoding='utf-8') as file:
        my_xml = file.read()

    my_dict = xmltodict.parse(my_xml)

    list=["title","urls"]
    final=[]
    for i in my_dict["cpe-list"]["cpe-item"]:

            lst=[]
            try:
            
                x=i["references"]['reference']
                for j in x:
                    l=str(j).split("'")

                    for q in l:
                        if "http" in q:
                            lst.append(q)


                title=str(i["title"]['#text'])
                temp=[]
                temp.append(title)
            except:
                continue
            string=""
            for i in lst:
                string+=i+'  '
            temp.append(string)
            final.append(temp)
            

    print('-'*50)

    # with open("cpe.txt","w") as file:
    #     for i in final:
    #         file.write(i)
    #         file.write("\n")

    # import csv


    # # field names 
    # fields = ['title','references'] 
    
    # # data rows of csv file 

    # with open('cpe.csv', 'w') as f:
        
    #     # using csv.writer method from CSV package
    #     write = csv.writer(f)
        
    #     write.writerow(fields)
    #     for i in final:
    #         write.writerow(i)

    conn = sqlite3.connect("cpe2.db")
    print("DB created")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS cpe2")
    creation_query="""
    CREATE TABLE cpe2(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        urls TEXT
    );
    """

    cursor.execute(creation_query)

    for i in final:
        cursor.execute("""
            INSERT INTO cpe2 (
                title, urls
            ) VALUES (?, ?)
        """, (
            i[0],
            i[1],
        ))

        cursor = conn.cursor()
    base_query="select * from cpe2;"
    cursor.execute(base_query)
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    conn.commit()
    conn.close()

    results = [dict(zip(col_names, row)) for row in rows]


    output=results

    app.run(debug=True)
    #pprint.pprint(my_dict, indent=2)
