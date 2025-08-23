# labs/management/commands/seed_demo.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random
import numpy as np

from patients.models import Patient
from labs.models import Sample, Result

ANALYTES = [
    # analyte, unit, ref_low, ref_high, dist (mean, std, outlier_prob)
    ("HIV_VL", "copies/mL", 0.0, 50.0, (2000, 10000, 0.25)),   # puxa alto (muitos out-of-range)
    ("CD4", "cells/µL", 500.0, 1600.0, (800, 200, 0.1)),
    ("ALT", "U/L", 7.0, 55.0, (35, 20, 0.15)),
    ("AST", "U/L", 8.0, 48.0, (30, 15, 0.15)),
]

class Command(BaseCommand):
    help = "Seed demo data: patients, samples, results"

    def add_arguments(self, parser):
        parser.add_argument("--patients", type=int, default=20, help="Number of patients")

    def handle(self, *args, **opts):
        fake = Faker("en_US")
        n = opts["patients"]
        created_patients = []
        for _ in range(n):
            p = Patient.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                birth_date=fake.date_of_birth(minimum_age=18, maximum_age=80),
                sex=random.choice(["M","F"]),
            )
            created_patients.append(p)

            # 1–3 samples por paciente
            for _s in range(random.randint(1,3)):
                s = Sample.objects.create(
                    patient=p,
                    sample_type=random.choice(["blood","plasma","serum"]),
                    collected_at=fake.date_time_between(start_date="-90d", end_date="now", tzinfo=timezone.utc),
                    status=random.choice(["received","processing","done"]),
                )
                # resultados para todos analitos
                for name, unit, ref_lo, ref_hi, (mu, sigma, outlier_p) in ANALYTES:
                    # 10–20% chance de gerar outlier extremo
                    if random.random() < outlier_p:
                        # empurra bem pra fora
                        if random.random() < 0.5:
                            val = ref_hi * (1 + random.uniform(2, 8))
                        else:
                            val = max(0.0, ref_lo - random.uniform(5, 30))
                    else:
                        val = float(np.random.normal(mu, sigma))
                        if name == "HIV_VL":
                            val = abs(val)  # viral load não negativo
                    Result.objects.create(
                        sample=s, analyte=name, value=round(val, 2),
                        unit=unit, ref_low=ref_lo, ref_high=ref_hi,
                    )

        self.stdout.write(self.style.SUCCESS(
            f"Seed ok: {len(created_patients)} patients, "
            f"{Sample.objects.count()} samples, {Result.objects.count()} results."
        ))
        self.stdout.write(self.style.MIGRATE_HEADING(
            f"Dica: pegue um patient_id para testar relatórios. Ex.: {created_patients[0].id if created_patients else '—'}"
        ))
