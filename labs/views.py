from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Sample, Result as TestResult
from .serializers import SampleSerializer, TestResultSerializer

class LabsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return bool(request.user and request.user.is_authenticated)

class SampleViewSet(viewsets.ModelViewSet):
    queryset = Sample.objects.select_related("patient").all().order_by("-created_at")
    serializer_class = SampleSerializer
    permission_classes = [LabsPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status","sample_type","patient"]
    search_fields = ["patient__first_name","patient__last_name"]
    ordering_fields = ["created_at","collected_at","status"]

class TestResultViewSet(viewsets.ModelViewSet):
    queryset = TestResult.objects.select_related("sample").all()
    serializer_class = TestResultSerializer
    permission_classes = [LabsPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["sample","analyte"]
    search_fields = ["analyte"]
    ordering_fields = ["value"]
