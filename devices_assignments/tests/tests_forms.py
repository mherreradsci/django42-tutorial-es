from django.test import TestCase

from devices_assignments.forms import DeviCustAssignmentForm


class DeviCustAssignmentTestCase(TestCase):
    def test_form_fileds_disabled(self):
        form_data = {"customer": "CUS001", "device": "Device 001"}

        form = DeviCustAssignmentForm(data=form_data)
        self.assertTrue(form.fields["created_by"].disabled)
        self.assertTrue(form.fields["updated_by"].disabled)
