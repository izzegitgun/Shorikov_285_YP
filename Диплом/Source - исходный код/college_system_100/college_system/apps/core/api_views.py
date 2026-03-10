from rest_framework import permissions, viewsets

from .models import Teacher, Subject, StudyGroup, Workload, Timesheet, Salary
from .serializers import (
    TeacherSerializer,
    SubjectSerializer,
    StudyGroupSerializer,
    WorkloadSerializer,
    TimesheetSerializer,
    SalarySerializer,
)


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_staff


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsStaffOrReadOnly]


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsStaffOrReadOnly]


class StudyGroupViewSet(viewsets.ModelViewSet):
    queryset = StudyGroup.objects.all()
    serializer_class = StudyGroupSerializer
    permission_classes = [IsStaffOrReadOnly]


class WorkloadViewSet(viewsets.ModelViewSet):
    queryset = Workload.objects.all()
    serializer_class = WorkloadSerializer
    permission_classes = [IsStaffOrReadOnly]


class TimesheetViewSet(viewsets.ModelViewSet):
    queryset = Timesheet.objects.all()
    serializer_class = TimesheetSerializer
    permission_classes = [IsStaffOrReadOnly]


class SalaryViewSet(viewsets.ModelViewSet):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    permission_classes = [IsStaffOrReadOnly]


