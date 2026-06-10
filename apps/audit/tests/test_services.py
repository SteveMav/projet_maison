from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from apps.audit.models import AuditEvent
from apps.audit.services import create_audit_event


class AuditEventTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            email="test@maison.com",
            password="testpassword123",
        )

    def test_create_audit_event(self):
        event = create_audit_event(
            event_type="listing.availability_changed",
            actor=self.user,
            target_id="123",
            metadata={"foo": "bar"},
        )
        self.assertEqual(event.event_type, "listing.availability_changed")
        self.assertEqual(event.actor, self.user)
        self.assertEqual(event.target_id, "123")
        self.assertEqual(event.metadata, {"foo": "bar"})

    def test_audit_event_is_append_only(self):
        event = create_audit_event(
            event_type="listing.availability_changed",
            actor=self.user,
            target_id="123",
        )

        with self.assertRaises(ValidationError):
            event.event_type = "something_else"
            event.save()

        with self.assertRaises(ValidationError):
            event.delete()
