from fastmcp import FastMCP
from supabase import create_client
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("LOCAL EXPENSE TRACKER SERVER")

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)


def init_db():
    """Create table if not exists using direct Postgres connection."""
    with psycopg2.connect(os.getenv("SUPABASE_DB_URL")) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id          SERIAL PRIMARY KEY,
                    date        TEXT NOT NULL,
                    amount      REAL NOT NULL,
                    category    TEXT NOT NULL,
                    subcategory TEXT DEFAULT '',
                    note        TEXT DEFAULT ''
                )
            """)


init_db()


@mcp.tool
def add_expense(date: str, amount: int, category: str, subcategory: str = "", note: str = ""):
    """Add a new expense entry to the database."""
    try:
        res = supabase.table("expenses").insert({
            "date": date,
            "amount": amount,
            "category": category,
            "subcategory": subcategory,
            "note": note
        }).execute()
        return {"message": "Expense added successfully", "id": res.data[0]["id"]}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool
def list_expenses():
    """List all expenses entries from database."""
    try:
        res = supabase.table("expenses").select("*").order("id").execute()
        return res.data
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)