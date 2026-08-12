from app.database.connection import engine
from sqlalchemy import text

def add_column():
    with engine.begin() as conn:
        try:
            conn.execute(text("ALTER TABLE interview_results ADD COLUMN session_id INTEGER REFERENCES interview_sessions(id);"))
            print("Successfully added session_id column to interview_results table.")
        except Exception as e:
            print(f"Error adding column (it might already exist): {e}")

if __name__ == "__main__":
    add_column()
