from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets, mixins
from drf_spectacular.utils import extend_schema
from .models import Report
from .serializers import (
    GenerateReportRequestSerializer,
    GenerateReportResponseSerializer,
    ReportSerializer,
)
from .tasks import build_report_task

class ReportViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Report.objects.all().order_by("-created_at")
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class GenerateReportView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @extend_schema(
        request=GenerateReportRequestSerializer,
        responses={status.HTTP_202_ACCEPTED: GenerateReportResponseSerializer},
    )
    def post(self, request):
        patient_id = request.data.get("patient_id")
        sample_id  = request.data.get("sample_id")
        rpt = Report.objects.create(patient_id=patient_id or None, sample_id=sample_id or None, status="pending")
        build_report_task.delay(rpt.id)
        return Response({"id": rpt.id, "status": rpt.status}, status=status.HTTP_202_ACCEPTED)
