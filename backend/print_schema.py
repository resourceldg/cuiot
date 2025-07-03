from app.core.database import Base, engine
from sqlalchemy import inspect

inspector = inspect(engine)
tables = inspector.get_table_names()

for table in tables:
    print(f"\n--- {table} ---")
    print("Columns:")
    for col in inspector.get_columns(table):
        print(f"  {col['name']}: {col['type']}, nullable={col['nullable']}, default={col.get('default')}")
    pks = inspector.get_pk_constraint(table)
    print(f"Primary Key: {pks.get('constrained_columns')}")
    fks = inspector.get_foreign_keys(table)
    if fks:
        print('Foreign Keys:')
        for fk in fks:
            print(f"  {fk['constrained_columns']} -> {fk['referred_table']}({fk['referred_columns']})") 