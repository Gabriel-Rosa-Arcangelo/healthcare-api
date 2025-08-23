from rest_framework.routers import DefaultRouter
from .views import SampleViewSet, TestResultViewSet

router = DefaultRouter()
router.register(r"samples", SampleViewSet, basename="sample")
router.register(r"results", TestResultViewSet, basename="result")
urlpatterns = router.urls
