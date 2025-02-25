import sys
print("✅ Python script started.")

try:
    print(f"ℹ️ Python version: {sys.version}")

    from sqlalchemy import create_engine
    print("✅ SQLAlchemy imported successfully.")

    DATABASE_URL = "postgresql+psycopg2://TysonChernen:Peaces4314@localhost/lira_db"
    print(f"ℹ️ Database URL: {DATABASE_URL}")

    engine = create_engine(DATABASE_URL, echo=True)
    print("✅ Engine created.")

    conn = engine.connect()
    print("✅ Connection successful!")

    conn.close()
except Exception as e:
    print(f"❌ ERROR: {e}")

print("🔄 Script finished.")
