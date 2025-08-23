from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ["id","patient_code","first_name","last_name","full_name","birth_date","sex","created_at"]
        read_only_fields = ["id","patient_code","created_at","full_name"]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()
