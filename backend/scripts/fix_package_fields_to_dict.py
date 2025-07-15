import json
from app.core.database import get_db
from app.models.package import Package

def list_to_dict(lst):
    if isinstance(lst, dict):
        return lst
    if isinstance(lst, list):
        return {str(item): True for item in lst}
    return {}

def fix_packages():
    db = next(get_db())
    packages = db.query(Package).all()
    changed = 0
    for pkg in packages:
        updated = False
        for field in ["features", "limitations", "customizable_options", "add_ons_available"]:
            val = getattr(pkg, field)
            if isinstance(val, list):
                setattr(pkg, field, list_to_dict(val))
                updated = True
            elif isinstance(val, str):
                try:
                    parsed = json.loads(val)
                    if isinstance(parsed, list):
                        setattr(pkg, field, list_to_dict(parsed))
                        updated = True
                except Exception:
                    pass
        if updated:
            changed += 1
    db.commit()
    print(f"✅ Paquetes corregidos: {changed}")

if __name__ == "__main__":
    fix_packages() 