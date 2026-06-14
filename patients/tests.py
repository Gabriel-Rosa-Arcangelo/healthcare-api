from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Patient


class PatientApiTests(APITestCase):
    def test_anonymous_user_can_list_but_cannot_create_patients(self):
        list_response = self.client.get("/api/patients/")
        create_response = self.client.post(
            "/api/patients/",
            {"first_name": "Ada", "last_name": "Lovelace"},
            format="json",
        )

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(create_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_create_patient_with_generated_code(self):
        user = get_user_model().objects.create_user(username="clinician", password="test-pass")
        self.client.force_authenticate(user)

        response = self.client.post(
            "/api/patients/",
            {"first_name": "Ada", "last_name": "Lovelace"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        patient = Patient.objects.get()
        self.assertEqual(len(patient.patient_code), 12)
