# reports/tasks.py
from celery import shared_task
from django.core.files.base import ContentFile
from io import BytesIO
from django.db.models import Prefetch
import pandas as pd

# --- shim p/ md5 usedforsecurity bug (OpenSSL + reportlab) ---
import hashlib
import reportlab.pdfbase.pdfdoc as _pdfdoc
def _safe_md5(data=b""):
    try:
        return hashlib.md5(data, usedforsecurity=False)  # type: ignore
    except TypeError:
        return hashlib.md5(data)
_pdfdoc.md5 = _safe_md5
# --------------------------------------------------------------

from .models import Report
from patients.models import Patient
from labs.models import Sample, Result
from .pdf import build_clinical_pdf

@shared_task
def build_report_task(report_id: int):
    rpt = Report.objects.get(id=report_id)
    try:
        rpt.status = "processing"; rpt.save(update_fields=["status"])

        # Carrega contexto (por paciente OU por sample)
        meta = {}
        if rpt.patient_id:
            patient = Patient.objects.get(id=rpt.patient_id)
            meta["patient"] = f"{patient.first_name} {patient.last_name}"
            qs = Result.objects.filter(sample__patient=patient).select_related("sample")
        elif rpt.sample_id:
            s = Sample.objects.select_related("patient").get(id=rpt.sample_id)
            meta["patient"] = f"{s.patient.first_name} {s.patient.last_name}"
            qs = Result.objects.filter(sample=s).select_related("sample")
        else:
            qs = Result.objects.none()

        # Monta DF: label, value, ref_low, ref_high
        data = []
        for r in qs:
            label = f"{r.analyte}"
            data.append({
                "label": label,
                "value": float(r.value),
                "ref_low": float(r.ref_low or 0.0),
                "ref_high": float(r.ref_high or 0.0),
            })
        df = pd.DataFrame(data if data else [{"label":"—","value":0,"ref_low":0,"ref_high":0}])

        # Gera PDF
        buf = BytesIO()
        title = "Clinical Lab Report"
        build_clinical_pdf(buf, title, df, top_n=6, meta=meta)
        buf.seek(0)

        rpt.file.save("report.pdf", ContentFile(buf.read()))
        rpt.status = "done"; rpt.save(update_fields=["status","file"])
    except Exception:
        rpt.status = "failed"; rpt.save(update_fields=["status"])
        raise
