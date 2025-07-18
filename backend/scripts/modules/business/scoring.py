import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

import random
from datetime import datetime, date, timedelta
from app.core.database import get_db
from app.models.caregiver_score import CaregiverScore
from app.models.caregiver_review import CaregiverReview
from app.models.institution_score import InstitutionScore
from app.models.institution_review import InstitutionReview
from app.models.user import User
from app.models.institution import Institution
from app.models.cared_person import CaredPerson
from app.models.service_type import ServiceType
from app.models.status_type import StatusType
from app.models.user_role import UserRole

def get_caregiver_role_ids(db):
    from app.models.role import Role
    # Buscar roles de cuidador (puede haber más de uno)
    role_names = ["caregiver", "institution_caregiver"]
    roles = db.query(Role).filter(Role.name.in_(role_names)).all()
    return [role.id for role in roles]

def populate_caregiver_scores():
    """Poblar puntuaciones agregadas de cuidadores"""
    db = next(get_db())
    created = 0
    
    # Obtener los UUID de los roles de cuidador
    caregiver_role_ids = get_caregiver_role_ids(db)
    if not caregiver_role_ids:
        print("⚠️  No se encontraron roles de cuidador. Verifica la tabla de roles.")
        db.close()
        return
    # Obtener cuidadores (usuarios con rol de cuidador)
    caregivers = db.query(User).join(User.user_roles).filter(
        User.is_active == True,
        UserRole.role_id.in_(caregiver_role_ids)
    ).all()
    
    if not caregivers:
        print("⚠️  No hay cuidadores disponibles. Ejecuta populate_caregivers primero.")
        db.close()
        return
    
    print("👨‍⚕️ Generando puntuaciones de cuidadores...")
    
    for caregiver in caregivers:
        # Verificar si ya existe la puntuación
        existing_score = db.query(CaregiverScore).filter_by(caregiver_id=caregiver.id).first()
        if existing_score:
            continue
        
        # Generar puntuaciones realistas
        overall_score = round(random.uniform(3.5, 5.0), 1)
        experience_score = round(random.uniform(3.0, 5.0), 1)
        quality_score = round(random.uniform(3.5, 5.0), 1)
        reliability_score = round(random.uniform(3.0, 5.0), 1)
        availability_score = round(random.uniform(3.0, 5.0), 1)
        
        # Generar estadísticas
        total_reviews = random.randint(5, 50)
        total_recommendations = int(total_reviews * random.uniform(0.7, 0.95))
        total_services = random.randint(10, 100)
        total_hours = total_services * random.randint(2, 8)
        
        # Métricas de calidad
        avg_response_time = random.randint(5, 30)  # minutos
        punctuality_rate = round(random.uniform(0.8, 0.98), 2)
        completion_rate = round(random.uniform(0.85, 0.99), 2)
        
        # Verificaciones
        is_identity_verified = random.choice([True, True, False])
        is_background_checked = random.choice([True, False])
        is_references_verified = random.choice([True, False])
        
        # Última fecha de cálculo y reseña
        last_calculated = datetime.now()
        last_review = datetime.now() - timedelta(days=random.randint(1, 90))
        
        # Crear puntuación del cuidador SOLO con los campos válidos
        caregiver_score = CaregiverScore(
            caregiver_id=caregiver.id,
            overall_score=overall_score,
            experience_score=experience_score,
            quality_score=quality_score,
            reliability_score=reliability_score,
            availability_score=availability_score,
            total_reviews=total_reviews,
            total_recommendations=total_recommendations,
            total_services=total_services,
            total_hours=total_hours,
            avg_response_time=avg_response_time,
            punctuality_rate=punctuality_rate,
            completion_rate=completion_rate,
            is_identity_verified=is_identity_verified,
            is_background_checked=is_background_checked,
            is_references_verified=is_references_verified,
            last_calculated=last_calculated,
            last_review=last_review
        )
        
        db.add(caregiver_score)
        created += 1
    
    db.commit()
    print(f"✅ Caregiver Scores creados: {created} (idempotente)")
    db.close()

def populate_caregiver_reviews():
    """Poblar reseñas individuales de cuidadores"""
    db = next(get_db())
    created = 0
    caregiver_role_ids = get_caregiver_role_ids(db)
    if not caregiver_role_ids:
        print("⚠️  No se encontraron roles de cuidador. Verifica la tabla de roles.")
        db.close()
        return
    # Obtener cuidadores y revisores
    caregivers = db.query(User).join(User.user_roles).filter(
        User.is_active == True,
        UserRole.role_id.in_(caregiver_role_ids)
    ).all()
    
    reviewers = db.query(User).filter(User.is_active == True).all()
    cared_persons = db.query(CaredPerson).all()
    service_types = db.query(ServiceType).all()
    
    if not caregivers or not reviewers:
        print("⚠️  No hay cuidadores o revisores disponibles.")
        db.close()
        return
    
    print("⭐ Generando reseñas de cuidadores...")
    
    for caregiver in caregivers:
        # Generar 2-8 reseñas por cuidador
        num_reviews = random.randint(2, 8)
        
        for i in range(num_reviews):
            # Seleccionar revisor aleatorio
            reviewer = random.choice(reviewers)
            if reviewer.id == caregiver.id:  # Evitar auto-reseñas
                continue
            
            # Seleccionar persona cuidada aleatoria
            cared_person = random.choice(cared_persons) if cared_persons else None
            
            # Generar rating y comentario
            rating = random.randint(3, 5)  # Mayormente positivos
            is_recommended = rating >= 4
            
            # Comentarios realistas según rating
            comments = {
                5: [
                    "Excelente cuidador, muy profesional y empático",
                    "Muy recomendable, se preocupa por los detalles",
                    "Experiencia muy positiva, muy responsable",
                    "Cuidador excepcional, superó nuestras expectativas"
                ],
                4: [
                    "Buen cuidador, cumple con sus responsabilidades",
                    "Recomendable, tiene buena comunicación",
                    "Satisfecho con el servicio, puntual y profesional",
                    "Buen trabajo, confiable y dedicado"
                ],
                3: [
                    "Aceptable, pero hay espacio para mejorar",
                    "Cumple lo básico, podría ser más proactivo",
                    "Servicio regular, algunas áreas de oportunidad",
                    "Adecuado para necesidades básicas"
                ]
            }
            
            comment = random.choice(comments.get(rating, ["Comentario general"]))
            
            # Categorías de evaluación
            categories = {
                "puntualidad": random.randint(rating-1, rating),
                "cuidado": rating,
                "comunicacion": random.randint(rating-1, rating),
                "empatia": random.randint(rating-1, rating),
                "profesionalismo": rating
            }
            
            # Fecha de servicio
            service_date = date.today() - timedelta(days=random.randint(1, 365))
            service_hours = random.uniform(2.0, 12.0)
            
            # Crear reseña
            review = CaregiverReview(
                caregiver_id=caregiver.id,
                reviewer_id=reviewer.id,
                cared_person_id=cared_person.id if cared_person else None,
                rating=rating,
                comment=comment,
                categories=categories,
                is_recommended=is_recommended,
                service_date=service_date,
                service_hours=round(service_hours, 1),
                service_type_id=random.choice(service_types).id if service_types else None,
                is_verified=True,
                is_public=True
            )
            
            db.add(review)
            created += 1
    
    db.commit()
    print(f"✅ Caregiver Reviews creados: {created} (idempotente)")
    db.close()

def populate_institution_scores():
    """Poblar puntuaciones agregadas de instituciones"""
    db = next(get_db())
    created = 0
    
    institutions = db.query(Institution).filter(Institution.is_active == True).all()
    
    if not institutions:
        print("⚠️  No hay instituciones disponibles. Ejecuta populate_institutions primero.")
        db.close()
        return
    
    print("🏥 Generando puntuaciones de instituciones...")
    
    for institution in institutions:
        # Verificar si ya existe la puntuación
        existing_score = db.query(InstitutionScore).filter_by(institution_id=institution.id).first()
        if existing_score:
            continue
        
        # Generar puntuaciones realistas
        overall_score = round(random.uniform(3.5, 5.0), 1)
        service_score = round(random.uniform(3.0, 5.0), 1)
        infrastructure_score = round(random.uniform(3.0, 5.0), 1)
        compliance_score = round(random.uniform(3.5, 5.0), 1)
        reputation_score = round(random.uniform(3.0, 5.0), 1)
        
        # Estadísticas
        total_reviews = random.randint(10, 100)
        total_recommendations = int(total_reviews * random.uniform(0.7, 0.9))
        total_caredpersons = random.randint(20, 200)
        years_operating = random.randint(2, 25)
        
        # Métricas de calidad
        staff_ratio = round(random.uniform(0.1, 0.3), 2)  # Staff por paciente
        response_time = random.randint(10, 60)  # minutos
        safety_incidents = random.randint(0, 5)
        satisfaction_rate = round(random.uniform(0.75, 0.95), 2)
        
        # Certificaciones
        has_medical_license = random.choice([True, True, True, False])
        has_safety_certification = random.choice([True, True, False, False])
        has_quality_certification = random.choice([True, False, False])
        
        # Inspección
        last_inspection_date = date.today() - timedelta(days=random.randint(30, 365))
        inspection_score = round(random.uniform(3.0, 5.0), 1)
        
        # Crear puntuación de institución
        institution_score = InstitutionScore(
            institution_id=institution.id,
            overall_score=overall_score,
            service_score=service_score,
            infrastructure_score=infrastructure_score,
            compliance_score=compliance_score,
            reputation_score=reputation_score,
            total_reviews=total_reviews,
            total_recommendations=total_recommendations,
            total_caredpersons=total_caredpersons,
            years_operating=years_operating,
            staff_ratio=staff_ratio,
            response_time=response_time,
            safety_incidents=safety_incidents,
            satisfaction_rate=satisfaction_rate,
            has_medical_license=has_medical_license,
            has_safety_certification=has_safety_certification,
            has_quality_certification=has_quality_certification,
            last_inspection_date=last_inspection_date,
            inspection_score=inspection_score,
            last_calculated=datetime.now()
        )
        
        db.add(institution_score)
        created += 1
    
    db.commit()
    print(f"✅ Institution Scores creados: {created} (idempotente)")
    db.close()

def populate_institution_reviews():
    """Poblar reseñas individuales de instituciones"""
    db = next(get_db())
    created = 0
    
    institutions = db.query(Institution).filter(Institution.is_active == True).all()
    reviewers = db.query(User).filter(User.is_active == True).all()
    cared_persons = db.query(CaredPerson).all()
    service_types = db.query(ServiceType).all()
    
    if not institutions or not reviewers:
        print("⚠️  No hay instituciones o revisores disponibles.")
        db.close()
        return
    
    print("🏢 Generando reseñas de instituciones...")
    
    for institution in institutions:
        # Generar 3-12 reseñas por institución
        num_reviews = random.randint(3, 12)
        
        for i in range(num_reviews):
            # Seleccionar revisor aleatorio
            reviewer = random.choice(reviewers)
            cared_person = random.choice(cared_persons) if cared_persons else None
            
            # Generar rating y comentario
            rating = random.randint(3, 5)  # Mayormente positivos
            is_recommended = rating >= 4
            
            # Comentarios realistas según rating
            comments = {
                5: [
                    "Excelente institución, personal muy profesional",
                    "Muy recomendable, instalaciones de primera calidad",
                    "Experiencia excepcional, atención personalizada",
                    "Institución de referencia, superó todas las expectativas"
                ],
                4: [
                    "Buena institución, cumple con los estándares",
                    "Recomendable, personal capacitado y amable",
                    "Satisfecho con el servicio, instalaciones adecuadas",
                    "Buen trabajo, atención profesional y responsable"
                ],
                3: [
                    "Aceptable, pero hay áreas de mejora",
                    "Cumple lo básico, podría mejorar en algunos aspectos",
                    "Servicio regular, instalaciones funcionales",
                    "Adecuado para necesidades básicas"
                ]
            }
            
            comment = random.choice(comments.get(rating, ["Comentario general"]))
            
            # Categorías de evaluación
            categories = {
                "atencion": rating,
                "instalaciones": random.randint(rating-1, rating),
                "personal": rating,
                "limpieza": random.randint(rating-1, rating),
                "seguridad": rating
            }
            
            # Fecha de servicio
            service_date = date.today() - timedelta(days=random.randint(1, 730))
            service_hours = random.uniform(4.0, 24.0)
            
            # Crear reseña SOLO con los campos válidos
            review = InstitutionReview(
                institution_id=institution.id,
                reviewer_id=reviewer.id,
                cared_person_id=cared_person.id if cared_person else None,
                rating=rating,
                comment=comment,
                categories=categories,
                is_recommended=is_recommended,
                service_date=service_date,
                service_type_id=random.choice(service_types).id if service_types else None,
                is_verified=True,
                is_public=True
            )
            
            db.add(review)
            created += 1
    
    db.commit()
    print(f"✅ Institution Reviews creados: {created} (idempotente)")
    db.close()

def populate_scoring_complete():
    """Poblar todo el sistema de scoring y reviews"""
    print("🏆 Iniciando población de sistema de scoring y reviews...")
    
    populate_caregiver_scores()
    populate_caregiver_reviews()
    populate_institution_scores()
    populate_institution_reviews()
    
    print("✅ Población de scoring y reviews completada!")

if __name__ == "__main__":
    populate_scoring_complete() 