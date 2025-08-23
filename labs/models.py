from django.db import models
from patients.models import Patient



class Sample(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="samples")
    sample_type = models.CharField(max_length=50)
    collected_at = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[
        ("received","Received"),
        ("processing","Processing"),
        ("done","Done"),
    ], default="received")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sample {self.id} ({self.sample_type})"


class Result(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name="results")
    analyte = models.CharField(max_length=100)        # ex: HIV_VL, CD4
    value = models.FloatField()
    unit = models.CharField(max_length=20)
    ref_low = models.FloatField(null=True, blank=True)
    ref_high = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def flagged(self):
        if self.ref_low is not None and self.value < self.ref_low:
            return True
        if self.ref_high is not None and self.value > self.ref_high:
            return True
        return False

    def __str__(self):
        return f"{self.analyte}: {self.value}{self.unit}"

