#!/usr/bin/env python3
"""
Test script for Care Module
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import get_db
from scripts.modules.care import (
    populate_cared_persons,
    populate_caregivers,
    populate_medical_data,
    populate_care_assignments
)


def test_care_module():
    """Test the complete care module"""
    print("🧪 Testing Care Module...")
    
    db = next(get_db())
    
    try:
        # Test each submodule
        print("\n1. Testing Cared Persons...")
        populate_cared_persons(db, num_cared_persons=10)
        
        print("\n2. Testing Caregivers...")
        populate_caregivers(db, num_caregivers=8)
        
        print("\n3. Testing Medical Data...")
        populate_medical_data(db, num_records=25)
        
        print("\n4. Testing Care Assignments...")
        populate_care_assignments(db, num_assignments=15)
        
        print("\n✅ Care Module test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error in Care Module test: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    test_care_module() 