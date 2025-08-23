from django.db import models
import uuid

class Patient(models.Model):
    SEX_CHOICES = [("M","Male"),("F","Female"),("O","Other")]
    id = models.BigAutoField(primary_key=True)
    patient_code = models.CharField(max_length=32, unique=True, editable=False)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    birth_date = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.patient_code:
            self.patient_code = uuid.uuid4().hex[:12]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.patient_code})"
