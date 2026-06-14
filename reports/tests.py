from unittest.mock import patch

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Report


class GenerateReportApiTests(APITestCase):
    @patch("reports.views.build_report_task.delay")
    def test_authenticated_user_can_queue_report(self, delay):
        user = get_user_model().objects.create_user(username="clinician", password="test-pass")
        self.client.force_authenticate(user)

        response = self.client.post("/api/reports/generate/", {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        report = Report.objects.get()
        delay.assert_called_once_with(report.id)
