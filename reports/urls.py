from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ReportViewSet, GenerateReportView

router = DefaultRouter()
router.register(r"", ReportViewSet, basename="report")

urlpatterns = [
    path("generate/", GenerateReportView.as_view(), name="report-generate"),
]
urlpatterns += router.urls
