from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ["id","patient","sample","status","file","created_at"]
        read_only_fields = ["id","status","file","created_at"]
