from flask import Flask, request, jsonify
import xmltodict
import pprint
import json
import sqlite3

app = Flask(__name__)


def db_full_return():

    conn = sqlite3.connect("cpe3.db")
    
    cursor = conn.cursor()
    base_query="select * from cpe3;"
    cursor.execute(base_query)
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    conn.close()

    results = [dict(zip(col_names, row)) for row in rows]
    data=results
    return data[-10:]

def db_pager(filters):
    conn=sqlite3.connect("cpe3.db")
    cursor=conn.cursor()
    base_query="select * from cpe3"
    conditions=[]
    values=[]

    limit=10

    for key,values in filters.items():
        if key in ["limit"]:
            limit=int(filters["limit"]) 
        if key in ["pages"]:
            base_query=base_query+f" where id <= {float(filters["pages"])};"

    cursor.execute(base_query)
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    conn.close()

    results = [dict(zip(col_names, row)) for row in rows]
    data=results

    if len(data)>limit:
        return data[:limit]
    return data


def db_access(filters):
    conn = sqlite3.connect("cpe3.db")
    
    cursor = conn.cursor()

    base_query="Select * from cpe3"
    conditions = []
    values = []

    for key, value in filters.items():
        if key in ["title","urls"]:
            conditions.append(f"{key} LIKE ?")
            values.append(f"%{value}%")
        elif key in ["id"]:
            conditions.append(f"{key}=")
            values.append(float(value))
    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)

    cursor.execute(base_query, values)
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    conn.close()

    results = [dict(zip(col_names, row)) for row in rows]
    return results[:10] 

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to the cpe API",
        "endpoints": {
            "/dump": "return last 10 records in the database table",
            "/search": "Filter recipes by key=value pairs (e.g., ?title=07FLY ?urls=github ?urls=git&title=fly)",
            "/cpec": "returns the records till id present in the database limited to 10 records (e.g., ?pages=5 ?limit=4 ?pages=5&limit=3)"
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

@app.route("/cpec",methods=["GET"])
def page():
    filters=request.args.to_dict()
    print(filters)
    if not filters:
        return jsonify({"error":"No filters Found"}),400
    data = db_pager(filters)
    return jsonify(data)

if __name__ == "__main__":
        app.run(debug=True)
