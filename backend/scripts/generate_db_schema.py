#!/usr/bin/env python3
"""
Script to generate database schema and relationships for comparison with UML documentation.
This script will:
1. Connect to the database
2. Extract all table definitions
3. Extract all foreign key relationships
4. Generate a comprehensive schema report
"""

import os
import sys
from pathlib import Path
from sqlalchemy import create_engine, MetaData, inspect, text
from sqlalchemy.schema import ForeignKeyConstraint
import json
from datetime import datetime

# Add the parent directory to the path to import app modules
sys.path.append(str(Path(__file__).parent.parent))

from app.core.config import settings
from app.models import Base
from app.models import *  # Import all models to register them

def get_database_url():
    """Get database URL from environment or use default"""
    # Try to get from environment first
    db_url = os.getenv('DATABASE_URL')
    if db_url:
        return db_url
    
    # Fallback to the one in alembic.ini
    return "postgresql://viejos_trapos_user:viejos_trapos_pass@postgres:5432/viejos_trapos_db"

def extract_table_schema(engine, metadata):
    """Extract complete table schema including columns, constraints, and relationships"""
    inspector = inspect(engine)
    schema_info = {
        'tables': {},
        'relationships': [],
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'total_tables': 0,
            'total_relationships': 0
        }
    }
    
    # Get all table names
    table_names = inspector.get_table_names()
    schema_info['metadata']['total_tables'] = len(table_names)
    
    for table_name in table_names:
        print(f"Processing table: {table_name}")
        
        # Get columns
        columns = inspector.get_columns(table_name)
        column_info = []
        
        for column in columns:
            col_data = {
                'name': column['name'],
                'type': str(column['type']),
                'nullable': column['nullable'],
                'default': column['default'],
                'primary_key': column.get('primary_key', False),
                'autoincrement': column.get('autoincrement', False)
            }
            column_info.append(col_data)
        
        # Get primary keys
        primary_keys = inspector.get_pk_constraint(table_name)
        
        # Get foreign keys
        foreign_keys = inspector.get_foreign_keys(table_name)
        
        # Get indexes
        indexes = inspector.get_indexes(table_name)
        
        # Get unique constraints
        unique_constraints = inspector.get_unique_constraints(table_name)
        
        # Get check constraints
        check_constraints = inspector.get_check_constraints(table_name)
        
        table_info = {
            'columns': column_info,
            'primary_keys': primary_keys.get('constrained_columns', []),
            'foreign_keys': foreign_keys,
            'indexes': indexes,
            'unique_constraints': unique_constraints,
            'check_constraints': check_constraints
        }
        
        schema_info['tables'][table_name] = table_info
        
        # Extract relationships from foreign keys
        for fk in foreign_keys:
            relationship = {
                'from_table': table_name,
                'from_columns': fk['constrained_columns'],
                'to_table': fk['referred_table'],
                'to_columns': fk['referred_columns'],
                'on_delete': fk.get('ondelete'),
                'on_update': fk.get('onupdate')
            }
            schema_info['relationships'].append(relationship)
    
    schema_info['metadata']['total_relationships'] = len(schema_info['relationships'])
    
    return schema_info

def extract_model_relationships():
    """Extract relationships from SQLAlchemy models"""
    model_relationships = []
    
    # Get all model classes from Base
    try:
        model_classes = Base._decl_class_registry.values()
    except AttributeError:
        # For newer SQLAlchemy versions, try different approach
        try:
            model_classes = Base.registry.metadata.tables.keys()
        except:
            print("Warning: Could not extract model relationships from SQLAlchemy models")
            return model_relationships
    
    for model_class in model_classes:
        if hasattr(model_class, '__tablename__') and model_class.__tablename__:
            table_name = model_class.__tablename__
            
            # Get relationships from model
            for attr_name in dir(model_class):
                attr = getattr(model_class, attr_name)
                if hasattr(attr, 'property') and hasattr(attr.property, 'mapper'):
                    # This is a relationship
                    relationship_info = {
                        'model': model_class.__name__,
                        'table': table_name,
                        'relationship_name': attr_name,
                        'target_model': attr.property.mapper.class_.__name__,
                        'target_table': attr.property.mapper.class_.__tablename__,
                        'relationship_type': 'unknown'
                    }
                    
                    # Determine relationship type
                    if hasattr(attr.property, 'uselist'):
                        if attr.property.uselist:
                            relationship_info['relationship_type'] = 'one_to_many'
                        else:
                            relationship_info['relationship_type'] = 'many_to_one'
                    
                    model_relationships.append(relationship_info)
    
    return model_relationships

def generate_schema_report(schema_info, model_relationships, output_file):
    """Generate a comprehensive schema report"""
    
    report = f"""# Database Schema Report
Generated at: {schema_info['metadata']['generated_at']}

## Summary
- Total Tables: {schema_info['metadata']['total_tables']}
- Total Foreign Key Relationships: {schema_info['metadata']['total_relationships']}
- Total Model Relationships: {len(model_relationships)}

## Tables

"""
    
    # Sort tables alphabetically
    for table_name in sorted(schema_info['tables'].keys()):
        table_info = schema_info['tables'][table_name]
        
        report += f"### {table_name}\n\n"
        
        # Columns
        report += "#### Columns\n"
        for column in table_info['columns']:
            pk_marker = " (PK)" if column['primary_key'] else ""
            nullable_marker = " (NULL)" if column['nullable'] else " (NOT NULL)"
            auto_marker = " (AUTO)" if column['autoincrement'] else ""
            
            report += f"- `{column['name']}`: {column['type']}{pk_marker}{nullable_marker}{auto_marker}\n"
        
        report += "\n"
        
        # Primary Keys
        if table_info['primary_keys']:
            report += f"#### Primary Keys\n"
            for pk in table_info['primary_keys']:
                report += f"- `{pk}`\n"
            report += "\n"
        
        # Foreign Keys
        if table_info['foreign_keys']:
            report += "#### Foreign Keys\n"
            for fk in table_info['foreign_keys']:
                report += f"- `{', '.join(fk['constrained_columns'])}` → `{fk['referred_table']}.{', '.join(fk['referred_columns'])}`\n"
            report += "\n"
        
        # Indexes
        if table_info['indexes']:
            report += "#### Indexes\n"
            for idx in table_info['indexes']:
                unique_marker = " (UNIQUE)" if idx['unique'] else ""
                report += f"- `{idx['name']}` on `{', '.join(idx['column_names'])}`{unique_marker}\n"
            report += "\n"
        
        report += "---\n\n"
    
    # Relationships section
    report += "## Foreign Key Relationships\n\n"
    
    # Group relationships by table
    relationships_by_table = {}
    for rel in schema_info['relationships']:
        from_table = rel['from_table']
        if from_table not in relationships_by_table:
            relationships_by_table[from_table] = []
        relationships_by_table[from_table].append(rel)
    
    for table_name in sorted(relationships_by_table.keys()):
        report += f"### {table_name}\n\n"
        for rel in relationships_by_table[table_name]:
            report += f"- `{', '.join(rel['from_columns'])}` → `{rel['to_table']}.{', '.join(rel['to_columns'])}`\n"
        report += "\n"
    
    # Model relationships section
    if model_relationships:
        report += "## SQLAlchemy Model Relationships\n\n"
        
        model_rels_by_table = {}
        for rel in model_relationships:
            table = rel['table']
            if table not in model_rels_by_table:
                model_rels_by_table[table] = []
            model_rels_by_table[table].append(rel)
        
        for table_name in sorted(model_rels_by_table.keys()):
            report += f"### {table_name}\n\n"
            for rel in model_rels_by_table[table_name]:
                report += f"- `{rel['relationship_name']}`: {rel['relationship_type']} → `{rel['target_table']}`\n"
            report += "\n"
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Schema report generated: {output_file}")

def generate_json_schema(schema_info, output_file):
    """Generate JSON schema for programmatic comparison"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(schema_info, f, indent=2, default=str)
    
    print(f"JSON schema generated: {output_file}")

def main():
    """Main function"""
    print("Generating database schema report...")
    
    # Create output directory
    output_dir = Path(__file__).parent / "schema_output"
    output_dir.mkdir(exist_ok=True)
    
    # Get database URL
    db_url = get_database_url()
    print(f"Connecting to database: {db_url.split('@')[1] if '@' in db_url else db_url}")
    
    try:
        # Create engine
        engine = create_engine(db_url)
        
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        print("Database connection successful!")
        
        # Create metadata
        metadata = MetaData()
        metadata.reflect(bind=engine)
        
        # Extract schema information
        print("Extracting schema information...")
        schema_info = extract_table_schema(engine, metadata)
        
        # Extract model relationships (skip for now)
        print("Skipping model relationships extraction...")
        model_relationships = []
        
        # Generate reports
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Markdown report
        markdown_file = output_dir / f"db_schema_report_{timestamp}.md"
        generate_schema_report(schema_info, model_relationships, markdown_file)
        
        # JSON schema
        json_file = output_dir / f"db_schema_{timestamp}.json"
        generate_json_schema(schema_info, json_file)
        
        print(f"\nSchema extraction completed successfully!")
        print(f"Files generated:")
        print(f"  - Markdown report: {markdown_file}")
        print(f"  - JSON schema: {json_file}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 