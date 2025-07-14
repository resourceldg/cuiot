from app.core.database import get_db
from app.models.report_type import ReportType

def populate_report_types():
    db = next(get_db())
    created = 0
    types = [
        {"name": "activity", "description": "Reporte de actividad de usuarios y dispositivos"},
        {"name": "health", "description": "Reporte de salud y signos vitales"},
        {"name": "alerts", "description": "Reporte de alertas críticas y eventos"},
        {"name": "compliance", "description": "Reporte de cumplimiento y auditoría"},
        {"name": "custom", "description": "Reporte personalizado"}
    ]
    for t in types:
        obj = db.query(ReportType).filter_by(name=t["name"]).first()
        if not obj:
            obj = ReportType(**t)
            db.add(obj)
            created += 1
    db.commit()
    print(f"✅ Tipos de reporte creados: {created} (idempotente)")
    db.close()

if __name__ == "__main__":
    populate_report_types() 