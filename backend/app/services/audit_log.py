import json
from app.models.audit_log import AuditLog

def log_change(db, entity_type, entity_id, action, changed_by_id, old_data=None, new_data=None, description=None):
    log = AuditLog(
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        changed_by_id=changed_by_id,
        old_data=json.dumps(old_data) if old_data else None,
        new_data=json.dumps(new_data) if new_data else None,
        description=description
    )
    db.add(log)
    db.commit() 