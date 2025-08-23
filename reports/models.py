from django.db import models
from patients.models import Patient
from labs.models import Sample

def report_upload_path(instance, filename):
    return f"reports/{instance.id}/{filename}"

class Report(models.Model):
    STATUS = [("pending","pending"),("processing","processing"),("done","done"),("failed","failed")]
    id = models.BigAutoField(primary_key=True)
    patient = models.ForeignKey(Patient, null=True, blank=True, on_delete=models.SET_NULL)
    sample = models.ForeignKey(Sample, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=12, choices=STATUS, default="pending")
    file = models.FileField(upload_to=report_upload_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
