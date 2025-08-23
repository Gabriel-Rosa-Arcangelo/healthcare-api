from rest_framework import serializers
from .models import Sample, Result as TestResult

class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = ["id","sample","analyte","value","unit","ref_low","ref_high","flagged"]
        read_only_fields = ["id","flagged"]

class SampleSerializer(serializers.ModelSerializer):
    results = TestResultSerializer(many=True, read_only=True)
    patient_name = serializers.CharField(source="patient.__str__", read_only=True)

    class Meta:
        model = Sample
        fields = ["id","patient","patient_name","sample_type","collected_at","status","results","created_at"]
        read_only_fields = ["id","created_at","patient_name"]
