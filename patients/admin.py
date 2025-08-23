from django.contrib import admin
from .models import Patient
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("patient_code","first_name","last_name","birth_date","sex","created_at")
    search_fields = ("patient_code","first_name","last_name")
