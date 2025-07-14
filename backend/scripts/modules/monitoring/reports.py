import random
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.report import Report
from app.models.report_type import ReportType
from app.models.cared_person import CaredPerson
from app.models.user import User

def populate_reports():
    db = next(get_db())
    created = 0
    # Obtener tipos de reporte
    report_types = {rt.name: rt.id for rt in db.query(ReportType).all()}
    # Obtener usuarios y personas cuidadas
    users = db.query(User).all()
    cared_persons = db.query(CaredPerson).all()
    if not users or not report_types:
        print("❌ Faltan usuarios o tipos de reporte para poblar reportes.")
        db.close()
        return
    # Generar 15 reportes variados
    for i in range(15):
        rtype = random.choice(list(report_types.keys()))
        user = random.choice(users)
        cared_person = random.choice(cared_persons) if cared_persons and random.random() > 0.3 else None
        title = f"{rtype.capitalize()} Reporte #{i+1}"
        description = f"Reporte automático de tipo {rtype} generado para pruebas."
        data = {"valor": random.randint(1, 100), "detalle": f"Dato de prueba {i+1}"}
        report = db.query(Report).filter_by(title=title).first()
        if not report:
            report = Report(
                title=title,
                description=description,
                report_type_id=report_types[rtype],
                cared_person_id=cared_person.id if cared_person else None,
                created_by_id=user.id,
                attached_files=[],
                is_autocuidado=False
            )
            db.add(report)
            created += 1
    db.commit()
    print(f"✅ Reportes creados: {created} (idempotente, normalizados)")
    db.close()

if __name__ == "__main__":
    populate_reports() 