from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import api_views

app_name = "core_api"

router = DefaultRouter()
router.register(r"teachers", api_views.TeacherViewSet)
router.register(r"subjects", api_views.SubjectViewSet)
router.register(r"groups", api_views.StudyGroupViewSet)
router.register(r"workloads", api_views.WorkloadViewSet)
router.register(r"timesheets", api_views.TimesheetViewSet)
router.register(r"salaries", api_views.SalaryViewSet)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]


