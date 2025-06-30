from app.core.database import engine
import sqlalchemy as sa

with engine.connect() as conn:
    # Check if care_type column exists
    result = conn.execute(sa.text("SELECT column_name FROM information_schema.columns WHERE table_name = 'cared_persons' AND column_name = 'care_type'"))
    care_type_exists = result.fetchone() is not None
    print(f"care_type column exists: {care_type_exists}")
    
    # Check total rows
    result = conn.execute(sa.text("SELECT COUNT(*) FROM cared_persons"))
    total_count = result.fetchone()[0]
    print(f"Total rows in cared_persons: {total_count}")
    
    if total_count > 0:
        # Show a few sample rows
        result = conn.execute(sa.text("SELECT id, name FROM cared_persons LIMIT 5"))
        rows = result.fetchall()
        print("Sample rows:")
        for row in rows:
            print(f"  ID: {row[0]}, Name: {row[1]}") 