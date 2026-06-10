from apps.audit.models import AuditEvent


def create_audit_event(*, event_type, actor, target_id, metadata=None):
    event = AuditEvent(
        event_type=event_type,
        actor=actor,
        target_id=str(target_id),
        metadata=metadata or {},
    )
    event.full_clean()
    event.save()
    return event
