#!/usr/bin/env python3
"""
Script to migrate existing status data to normalized status_types structure
Phase 2: CaredPersonInstitution, CaregiverInstitution, RestraintProtocol, MedicalReferral
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.status_type import StatusType
from app.models.cared_person_institution import CaredPersonInstitution
from app.models.caregiver_institution import CaregiverInstitution
from app.models.restraint_protocol import RestraintProtocol
from app.models.medical_referral import MedicalReferral

def get_status_type_id(session, status_name: str) -> int:
    """Get status_type_id by name"""
    status_type = session.query(StatusType).filter(StatusType.name == status_name).first()
    if not status_type:
        print(f"⚠️  Status type '{status_name}' not found, creating...")
        status_type = StatusType(name=status_name, description=f"Status: {status_name}")
        session.add(status_type)
        session.commit()
        session.refresh(status_type)
    return status_type.id

def migrate_cared_person_institutions(session):
    """Migrate CaredPersonInstitution status data"""
    print("\n🔄 Migrating CaredPersonInstitution status data...")
    
    # Get all records with status_type_id = NULL
    records = session.query(CaredPersonInstitution).filter(
        CaredPersonInstitution.status_type_id.is_(None)
    ).all()
    
    if not records:
        print("✅ No CaredPersonInstitution records to migrate")
        return
    
    print(f"📊 Found {len(records)} CaredPersonInstitution records to migrate")
    
    # Get status type mappings
    status_mappings = {
        "active": get_status_type_id(session, "active"),
        "paused": get_status_type_id(session, "paused"),
        "completed": get_status_type_id(session, "completed"),
        "terminated": get_status_type_id(session, "terminated")
    }
    
    migrated_count = 0
    for record in records:
        try:
            # Use raw SQL to get the old status value
            result = session.execute(text(
                "SELECT status FROM cared_person_institutions WHERE id = :id"
            ), {"id": record.id})
            old_status = result.scalar()
            
            if old_status and old_status in status_mappings:
                record.status_type_id = status_mappings[old_status]
                migrated_count += 1
                print(f"  ✅ Migrated record {record.id}: '{old_status}' -> status_type_id {record.status_type_id}")
            else:
                print(f"  ⚠️  Record {record.id}: unknown status '{old_status}', setting to 'active'")
                record.status_type_id = status_mappings["active"]
                migrated_count += 1
                
        except Exception as e:
            print(f"  ❌ Error migrating record {record.id}: {e}")
    
    session.commit()
    print(f"✅ Successfully migrated {migrated_count} CaredPersonInstitution records")

def migrate_caregiver_institutions(session):
    """Migrate CaregiverInstitution status data"""
    print("\n🔄 Migrating CaregiverInstitution status data...")
    
    # Get all records with status_type_id = NULL
    records = session.query(CaregiverInstitution).filter(
        CaregiverInstitution.status_type_id.is_(None)
    ).all()
    
    if not records:
        print("✅ No CaregiverInstitution records to migrate")
        return
    
    print(f"📊 Found {len(records)} CaregiverInstitution records to migrate")
    
    # Get status type mappings
    status_mappings = {
        "active": get_status_type_id(session, "active"),
        "inactive": get_status_type_id(session, "inactive"),
        "suspended": get_status_type_id(session, "suspended"),
        "terminated": get_status_type_id(session, "terminated")
    }
    
    migrated_count = 0
    for record in records:
        try:
            # Use raw SQL to get the old status value
            result = session.execute(text(
                "SELECT status FROM caregiver_institutions WHERE id = :id"
            ), {"id": record.id})
            old_status = result.scalar()
            
            if old_status and old_status in status_mappings:
                record.status_type_id = status_mappings[old_status]
                migrated_count += 1
                print(f"  ✅ Migrated record {record.id}: '{old_status}' -> status_type_id {record.status_type_id}")
            else:
                print(f"  ⚠️  Record {record.id}: unknown status '{old_status}', setting to 'active'")
                record.status_type_id = status_mappings["active"]
                migrated_count += 1
                
        except Exception as e:
            print(f"  ❌ Error migrating record {record.id}: {e}")
    
    session.commit()
    print(f"✅ Successfully migrated {migrated_count} CaregiverInstitution records")

def migrate_restraint_protocols(session):
    """Migrate RestraintProtocol status data"""
    print("\n🔄 Migrating RestraintProtocol status data...")
    
    # Get all records with status_type_id = NULL
    records = session.query(RestraintProtocol).filter(
        RestraintProtocol.status_type_id.is_(None)
    ).all()
    
    if not records:
        print("✅ No RestraintProtocol records to migrate")
        return
    
    print(f"📊 Found {len(records)} RestraintProtocol records to migrate")
    
    # Get status type mappings
    status_mappings = {
        "active": get_status_type_id(session, "active"),
        "suspended": get_status_type_id(session, "suspended"),
        "completed": get_status_type_id(session, "completed"),
        "terminated": get_status_type_id(session, "terminated")
    }
    
    migrated_count = 0
    for record in records:
        try:
            # Use raw SQL to get the old status value
            result = session.execute(text(
                "SELECT status FROM restraint_protocols WHERE id = :id"
            ), {"id": record.id})
            old_status = result.scalar()
            
            if old_status and old_status in status_mappings:
                record.status_type_id = status_mappings[old_status]
                migrated_count += 1
                print(f"  ✅ Migrated record {record.id}: '{old_status}' -> status_type_id {record.status_type_id}")
            else:
                print(f"  ⚠️  Record {record.id}: unknown status '{old_status}', setting to 'active'")
                record.status_type_id = status_mappings["active"]
                migrated_count += 1
                
        except Exception as e:
            print(f"  ❌ Error migrating record {record.id}: {e}")
    
    session.commit()
    print(f"✅ Successfully migrated {migrated_count} RestraintProtocol records")

def migrate_medical_referrals(session):
    """Migrate MedicalReferral status data"""
    print("\n🔄 Migrating MedicalReferral status data...")
    
    # Get all records with status_type_id = NULL
    records = session.query(MedicalReferral).filter(
        MedicalReferral.status_type_id.is_(None)
    ).all()
    
    if not records:
        print("✅ No MedicalReferral records to migrate")
        return
    
    print(f"📊 Found {len(records)} MedicalReferral records to migrate")
    
    # Get status type mappings
    status_mappings = {
        "pending": get_status_type_id(session, "pending"),
        "scheduled": get_status_type_id(session, "scheduled"),
        "completed": get_status_type_id(session, "completed"),
        "cancelled": get_status_type_id(session, "cancelled")
    }
    
    migrated_count = 0
    for record in records:
        try:
            # Use raw SQL to get the old status value
            result = session.execute(text(
                "SELECT status FROM medical_referrals WHERE id = :id"
            ), {"id": record.id})
            old_status = result.scalar()
            
            if old_status and old_status in status_mappings:
                record.status_type_id = status_mappings[old_status]
                migrated_count += 1
                print(f"  ✅ Migrated record {record.id}: '{old_status}' -> status_type_id {record.status_type_id}")
            else:
                print(f"  ⚠️  Record {record.id}: unknown status '{old_status}', setting to 'pending'")
                record.status_type_id = status_mappings["pending"]
                migrated_count += 1
                
        except Exception as e:
            print(f"  ❌ Error migrating record {record.id}: {e}")
    
    session.commit()
    print(f"✅ Successfully migrated {migrated_count} MedicalReferral records")

def verify_migration(session):
    """Verify that all records have status_type_id set"""
    print("\n🔍 Verifying migration...")
    
    # Check each table
    tables = [
        ("CaredPersonInstitution", CaredPersonInstitution),
        ("CaregiverInstitution", CaregiverInstitution),
        ("RestraintProtocol", RestraintProtocol),
        ("MedicalReferral", MedicalReferral)
    ]
    
    all_good = True
    for table_name, model in tables:
        null_count = session.query(model).filter(model.status_type_id.is_(None)).count()
        total_count = session.query(model).count()
        
        if null_count > 0:
            print(f"  ❌ {table_name}: {null_count}/{total_count} records still have NULL status_type_id")
            all_good = False
        else:
            print(f"  ✅ {table_name}: All {total_count} records have status_type_id set")
    
    return all_good

def main():
    """Main migration function"""
    print("🚀 Starting Phase 2 Status Data Migration")
    print("=" * 50)
    
    # Create database connection
    engine = create_engine(settings.get_database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    try:
        # Run migrations
        migrate_cared_person_institutions(session)
        migrate_caregiver_institutions(session)
        migrate_restraint_protocols(session)
        migrate_medical_referrals(session)
        
        # Verify migration
        if verify_migration(session):
            print("\n🎉 Phase 2 Status Data Migration completed successfully!")
        else:
            print("\n⚠️  Migration completed with warnings - some records may need manual review")
            
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    main() 