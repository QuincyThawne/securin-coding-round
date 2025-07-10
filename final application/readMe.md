# CPE Dictionary

## Tech Stack

- Python
    - sqlite3
    - xmltodict
    - flask 
    - streamlit

## program files

### What the .pyfiles do

- **xmlToDB.py**
    - extracts the title and urls from cpe.txt
    - converts it to a Database manageable by sql
    - sql schema is (id,title,urls)

- **cpeAPI.py**
    - runs a RESTful API using flask
    - has 3 endpoints + home

        "endpoints": {
        "/dump": "return last 10 records in the database table",
        "/search": "Filter recipes by key=value pairs (e.g., ?title=07FLY ?urls=github ?urls=git&title=fly)",
        "/cpec": "returns the records till id present in the database limited to 10 records (e.g., ?pages=5 ?limit=4 ?pages=5&limit=3)"
    }

- **dbtest.py**
    - sandbox python source code to test sql queries
    - not that releavant

- **Frontend.py**
    - runs a streamlit UI to display the api responses in GET
    - has keyword modifiers for title and url based searching
    - can use to execute general api requrests instead of postman as well provided for cpeAPI.py

command: python -m streamlit run Frontend.py

