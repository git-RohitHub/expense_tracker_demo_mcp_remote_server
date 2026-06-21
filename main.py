from fastmcp import FastMCP 
import sqlite3
import os

mcp = FastMCP("LOCAL EXPENSE TRACKER SERVER")
DB_PATH = os.path.join(os.path.dirname(__file__),"expense.db")

def init_db():
    with sqlite3.connect(DB_PATH) as c : 
        c.execute(
            """
CREATE TABLE IF NOT EXISTS expenses(
id INTEGER PRIMARY KEY AUTOINCREMENT,
date TEXT NOT NULL , 
amount REAL NOT NULL,
category TEXT NOT NULL,
subcategory TEXT DEFAULT ' ',
note TEXT DEFAULT ' ' 
)
"""
        )

init_db()



@mcp.tool
def add_expense(date: str, amount:int,category:str,subcategory:str=" ",note:str= " "):
    """Add a new expense entry to the database. """
    with sqlite3.connect(DB_PATH) as c:
        c.execute(
"INSERT INTO expenses(date,amount,category,subcategory,note) VALUES(?,?,?,?,?)",
(date,amount,category,subcategory,note)
        )

@mcp.tool
def list_expenses():
    """List all expenses entries from database . """
    with sqlite3.connect(DB_PATH) as c:
        curr = c.execute("""
SELECT * FROM expenses ORDER BY id ASC
""")
        cols = [d[0] for d in curr.description]
        return [dict(zip(cols,r)) for r in curr.fetchall()]

if __name__ == "__main__":
    mcp.run(transport="http",host="0.0.0.0",port=8000)
