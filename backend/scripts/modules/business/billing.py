import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

import random
from datetime import datetime, date, timedelta
from app.core.database import get_db
from app.models.billing_record import BillingRecord
from app.models.user import User
from app.models.institution import Institution
from app.models.package import UserPackage, PackageAddOn, UserPackageAddOn
from app.models.service_subscription import ServiceSubscription
from app.models.status_type import StatusType

def generate_invoice_number(prefix="INV", year=None):
    """Generar número de factura único"""
    if year is None:
        year = datetime.now().year
    random_num = random.randint(10000, 99999)
    return f"{prefix}-{year}-{random_num}"

def populate_billing_records():
    """Poblar registros de facturación para diferentes tipos de servicios"""
    db = next(get_db())
    created = 0
    
    # Obtener datos necesarios
    users = db.query(User).filter(User.is_active == True).all()
    institutions = db.query(Institution).filter(Institution.is_active == True).all()
    user_packages = db.query(UserPackage).all()
    service_subscriptions = db.query(ServiceSubscription).all()
    status_types = db.query(StatusType).filter(StatusType.category == "billing").all()
    
    if not users:
        print("⚠️  No hay usuarios disponibles. Ejecuta populate_users primero.")
        db.close()
        return
    
    if not status_types:
        print("⚠️  No hay status types de facturación. Ejecuta populate_core primero.")
        db.close()
        return
    
    # Mapear status types
    status_map = {st.name: st.id for st in status_types}
    paid_status_id = status_map.get("paid", status_types[0].id)
    pending_status_id = status_map.get("pending", status_types[0].id)
    overdue_status_id = status_map.get("overdue", status_types[0].id)
    
    # 1. Facturas de suscripciones (UserPackage)
    print("📦 Generando facturas de suscripciones...")
    for user_package in user_packages:
        # Generar 1-6 facturas por suscripción (historial de facturación)
        num_bills = random.randint(1, 6)
        
        for i in range(num_bills):
            # Verificar si ya existe la factura
            invoice_number = generate_invoice_number("SUB")
            existing = db.query(BillingRecord).filter_by(invoice_number=invoice_number).first()
            if existing:
                continue
            
            # Calcular fechas
            if user_package.billing_cycle == "monthly":
                billing_date = user_package.start_date + timedelta(days=30 * i)
                due_date = billing_date + timedelta(days=15)
            else:
                billing_date = user_package.start_date + timedelta(days=365 * i)
                due_date = billing_date + timedelta(days=30)
            
            # Determinar estado de la factura
            today = date.today()
            if billing_date > today:
                status_id = pending_status_id
                paid_date = None
            elif due_date < today:
                status_id = overdue_status_id
                paid_date = None
            else:
                status_id = paid_status_id
                paid_date = billing_date + timedelta(days=random.randint(1, 10))
            
            # Calcular montos
            base_amount = user_package.current_amount
            tax_amount = int(base_amount * 0.21)  # 21% IVA
            total_amount = base_amount + tax_amount
            
            # Crear factura de suscripción
            billing_record = BillingRecord(
                invoice_number=invoice_number,
                billing_type="subscription",
                description=f"Factura de suscripción - {user_package.package.name}",
                amount=base_amount,
                currency="ARS",
                tax_amount=tax_amount,
                total_amount=total_amount,
                billing_date=billing_date,
                due_date=due_date,
                paid_date=paid_date,
                status_type_id=status_id,
                payment_method=random.choice(["credit_card", "debit_card", "bank_transfer", "cash"]) if paid_date else None,
                transaction_id=f"TXN-{random.randint(100000, 999999)}" if paid_date else None,
                user_id=user_package.user_id,
                user_package_id=user_package.id
            )
            
            db.add(billing_record)
            created += 1
    
    # 2. Facturas de servicios (ServiceSubscription)
    print("🏥 Generando facturas de servicios...")
    for service_sub in service_subscriptions:
        # Generar 1-3 facturas por servicio
        num_bills = random.randint(1, 3)
        
        for i in range(num_bills):
            invoice_number = generate_invoice_number("SVC")
            existing = db.query(BillingRecord).filter_by(invoice_number=invoice_number).first()
            if existing:
                continue
            
            # Calcular fechas
            billing_date = service_sub.start_date + timedelta(days=30 * i)
            due_date = billing_date + timedelta(days=15)
            
            # Determinar estado
            today = date.today()
            if billing_date > today:
                status_id = pending_status_id
                paid_date = None
            elif due_date < today:
                status_id = overdue_status_id
                paid_date = None
            else:
                status_id = paid_status_id
                paid_date = billing_date + timedelta(days=random.randint(1, 10))
            
            # Calcular montos
            base_amount = service_sub.price_per_month or 5000  # 50 ARS por defecto
            tax_amount = int(base_amount * 0.21)
            total_amount = base_amount + tax_amount
            
            # Crear factura de servicio
            billing_record = BillingRecord(
                invoice_number=invoice_number,
                billing_type="service",
                description=f"Factura de servicio - {service_sub.service_name}",
                amount=base_amount,
                currency="ARS",
                tax_amount=tax_amount,
                total_amount=total_amount,
                billing_date=billing_date,
                due_date=due_date,
                paid_date=paid_date,
                status_type_id=status_id,
                payment_method=random.choice(["credit_card", "debit_card", "bank_transfer"]) if paid_date else None,
                transaction_id=f"TXN-{random.randint(100000, 999999)}" if paid_date else None,
                user_id=service_sub.user_id,
                institution_id=service_sub.institution_id,
                service_subscription_id=service_sub.id
            )
            
            db.add(billing_record)
            created += 1
    
    # 3. Facturas de configuración/setup
    print("⚙️  Generando facturas de configuración...")
    for user in users[:min(10, len(users))]:  # Máximo 10 usuarios
        invoice_number = generate_invoice_number("SET")
        existing = db.query(BillingRecord).filter_by(invoice_number=invoice_number).first()
        if existing:
            continue
        
        # Factura única de setup
        billing_date = user.created_at.date() + timedelta(days=1)
        due_date = billing_date + timedelta(days=7)
        
        base_amount = 10000  # 100 ARS por setup
        tax_amount = int(base_amount * 0.21)
        total_amount = base_amount + tax_amount
        
        billing_record = BillingRecord(
            invoice_number=invoice_number,
            billing_type="setup",
            description="Cargo por configuración inicial del sistema",
            amount=base_amount,
            currency="ARS",
            tax_amount=tax_amount,
            total_amount=total_amount,
            billing_date=billing_date,
            due_date=due_date,
            paid_date=billing_date + timedelta(days=random.randint(1, 5)),
            status_type_id=paid_status_id,
            payment_method=random.choice(["credit_card", "debit_card"]),
            transaction_id=f"TXN-{random.randint(100000, 999999)}",
            user_id=user.id
        )
        
        db.add(billing_record)
        created += 1
    
    # 4. Facturas de consultoría
    print("💼 Generando facturas de consultoría...")
    for user in users[:min(5, len(users))]:  # Máximo 5 usuarios
        # Generar 1-2 facturas de consultoría
        for i in range(random.randint(1, 2)):
            invoice_number = generate_invoice_number("CON")
            existing = db.query(BillingRecord).filter_by(invoice_number=invoice_number).first()
            if existing:
                continue
            
            billing_date = user.created_at.date() + timedelta(days=random.randint(30, 180))
            due_date = billing_date + timedelta(days=15)
            
            base_amount = random.randint(5000, 25000)  # 50-250 ARS
            tax_amount = int(base_amount * 0.21)
            total_amount = base_amount + tax_amount
            
            billing_record = BillingRecord(
                invoice_number=invoice_number,
                billing_type="consultation",
                description=f"Servicio de consultoría técnica - Sesión {i+1}",
                amount=base_amount,
                currency="ARS",
                tax_amount=tax_amount,
                total_amount=total_amount,
                billing_date=billing_date,
                due_date=due_date,
                paid_date=billing_date + timedelta(days=random.randint(1, 10)),
                status_type_id=paid_status_id,
                payment_method=random.choice(["credit_card", "bank_transfer"]),
                transaction_id=f"TXN-{random.randint(100000, 999999)}",
                user_id=user.id
            )
            
            db.add(billing_record)
            created += 1
    
    # 5. Facturas de mantenimiento
    print("🔧 Generando facturas de mantenimiento...")
    for institution in institutions:
        # Generar 1-3 facturas de mantenimiento por institución
        for i in range(random.randint(1, 3)):
            invoice_number = generate_invoice_number("MNT")
            existing = db.query(BillingRecord).filter_by(invoice_number=invoice_number).first()
            if existing:
                continue
            
            billing_date = date.today() - timedelta(days=random.randint(30, 365))
            due_date = billing_date + timedelta(days=30)
            
            base_amount = random.randint(15000, 50000)  # 150-500 ARS
            tax_amount = int(base_amount * 0.21)
            total_amount = base_amount + tax_amount
            
            # Determinar estado
            today = date.today()
            if due_date < today:
                status_id = overdue_status_id
                paid_date = None
            else:
                status_id = paid_status_id
                paid_date = billing_date + timedelta(days=random.randint(1, 25))
            
            billing_record = BillingRecord(
                invoice_number=invoice_number,
                billing_type="maintenance",
                description=f"Mantenimiento del sistema - {institution.name}",
                amount=base_amount,
                currency="ARS",
                tax_amount=tax_amount,
                total_amount=total_amount,
                billing_date=billing_date,
                due_date=due_date,
                paid_date=paid_date,
                status_type_id=status_id,
                payment_method=random.choice(["credit_card", "bank_transfer"]) if paid_date else None,
                transaction_id=f"TXN-{random.randint(100000, 999999)}" if paid_date else None,
                institution_id=institution.id
            )
            
            db.add(billing_record)
            created += 1
    
    db.commit()
    print(f"✅ Billing Records creados: {created} (idempotente)")
    db.close()

def populate_billing_complete():
    """Poblar todo el sistema de facturación"""
    print("💰 Iniciando población de registros de facturación...")
    populate_billing_records()
    print("✅ Población de facturación completada!")

if __name__ == "__main__":
    populate_billing_complete() 