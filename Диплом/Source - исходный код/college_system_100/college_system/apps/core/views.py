import io
import os
import calendar
from collections import defaultdict
from datetime import date, timedelta

import pandas as pd
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, Sum
from django.http import FileResponse, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from openpyxl import Workbook
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from apps.authentication.models import User
from .forms import (
    TeacherForm,
    SubjectForm,
    StudyGroupForm,
    WorkloadForm,
    TimesheetForm,
    SalaryForm,
    FeedbackForm,
    MessageForm,
)
from .models import Teacher, Subject, StudyGroup, Workload, Timesheet, Salary, Feedback, Message


class RoleRequiredMixin(UserPassesTestMixin):
    allowed_roles: list[str] = []

    def test_func(self) -> bool:
        user: User = self.request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return user.role in self.allowed_roles


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = date.today()
        user = self.request.user

        ctx["teachers_count"] = Teacher.objects.count()
        ctx["subjects_count"] = Subject.objects.count()
        ctx["groups_count"] = StudyGroup.objects.count()
        ctx["workload_today"] = Workload.objects.filter(date=today).count()
        ctx["pending_timesheets"] = Timesheet.objects.filter(status="draft").count()
        ctx["pending_feedback"] = 0

        if user.role == "teacher":
            teacher_profile = getattr(user, "teacher_profile", None)
            if teacher_profile:
                ctx["my_upcoming_workload"] = (
                    Workload.objects.filter(teacher=teacher_profile, date__gte=today)
                    .select_related("subject", "group")
                    .order_by("date", "pair_slot")[:10]
                )
                ctx["my_recent_workload"] = (
                    Workload.objects.filter(teacher=teacher_profile, date__lt=today)
                    .select_related("subject", "group")
                    .order_by("-date", "pair_slot")[:5]
                )
                ctx["my_timesheets_count"] = Timesheet.objects.filter(teacher=teacher_profile).count()
                ctx["my_salaries"] = (
                    Salary.objects.filter(teacher=teacher_profile)
                    .order_by("-period")[:5]
                )
                ctx["my_salary_total"] = Salary.objects.filter(teacher=teacher_profile).aggregate(
                    total=Sum("total_amount")
                )["total"] or 0
                ctx["my_timesheets"] = (
                    Timesheet.objects.filter(teacher=teacher_profile)
                    .select_related("subject", "group")
                    .order_by("-period_from")[:5]
                )
        elif user.role == "accountant":
            # Статистика по зарплатам
            ctx["salary_total"] = Salary.objects.filter(period__year=today.year).count()
            ctx["salary_total_amount"] = Salary.objects.filter(period__year=today.year).aggregate(
                total=Sum("total_amount")
            )["total"] or 0
            ctx["salary_month_amount"] = Salary.objects.filter(
                period__year=today.year, period__month=today.month
            ).aggregate(total=Sum("total_amount"))["total"] or 0
            # Последние зарплаты
            ctx["recent_salaries"] = (
                Salary.objects.filter(period__year=today.year)
                .select_related("teacher")
                .order_by("-period", "-id")[:10]
            )
            # Табели
            ctx["timesheets_pending"] = Timesheet.objects.filter(status="draft").count()
            ctx["timesheets_approved"] = Timesheet.objects.filter(status="approved").count()
            ctx["pending_timesheets_list"] = (
                Timesheet.objects.filter(status="draft")
                .select_related("teacher", "subject", "group")
                .order_by("-period_from")[:10]
            )
        elif user.role == "curator":
            # Статистика по преподавателям
            ctx["inactive_teachers"] = Teacher.objects.filter(is_active=False).count()
            ctx["active_teachers"] = Teacher.objects.filter(is_active=True).count()
            ctx["teachers_total"] = Teacher.objects.count()
            # Последние преподаватели
            ctx["recent_teachers"] = Teacher.objects.filter(is_active=True).order_by("-id")[:5]
            # Статистика по предметам и группам
            ctx["subjects_active"] = Subject.objects.filter(is_active=True).count()
            ctx["groups_active"] = StudyGroup.objects.filter(is_active=True).count()
            # Последние нагрузки
            ctx["recent_workloads"] = (
                Workload.objects.all()
                .select_related("teacher", "subject", "group")
                .order_by("-id")[:10]
            )
            # Статистика по нагрузке
            ctx["workload_today_count"] = Workload.objects.filter(date=today).count()
            ctx["workload_this_week"] = Workload.objects.filter(
                date__gte=today, date__lte=today + timedelta(days=7)
            ).count()
        if user.is_superuser or user.role == "admin":
            ctx["pending_feedback"] = Feedback.objects.filter(status=Feedback.STATUS_NEW).count()

        return ctx


class TeacherListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Teacher
    template_name = "core/teacher_list.html"
    allowed_roles = ["curator", "admin", "accountant", "teacher"]


class TeacherDetailView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
    model = Teacher
    template_name = "core/teacher_detail.html"
    allowed_roles = ["curator", "admin", "accountant", "teacher"]


class TeacherCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = "core/teacher_form.html"
    success_url = reverse_lazy("core:teacher_list")
    allowed_roles = ["curator", "admin"]


class TeacherUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = "core/teacher_form.html"
    success_url = reverse_lazy("core:teacher_list")
    allowed_roles = ["curator", "admin"]


class TeacherDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    model = Teacher
    template_name = "core/teacher_confirm_delete.html"
    success_url = reverse_lazy("core:teacher_list")
    allowed_roles = ["curator", "admin"]


class TeacherImportView(LoginRequiredMixin, RoleRequiredMixin, View):
    allowed_roles = ["curator", "admin"]
    template_name = "core/teacher_import.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        return TemplateView.as_view(template_name=self.template_name)(request)

    def post(self, request: HttpRequest) -> HttpResponse:
        file = request.FILES.get("file")
        if not file:
            return TemplateView.as_view(
                template_name=self.template_name,
                extra_context={"error": "Не выбран файл"},
            )(request)
        df = pd.read_excel(file)
        for _, row in df.iterrows():
            user, _ = User.objects.get_or_create(
                username=row.get("username"),
                defaults={"role": "teacher"},
            )
            Teacher.objects.update_or_create(
                user=user,
                defaults={
                    "full_name": row.get("full_name", ""),
                    "position": row.get("position", ""),
                    "academic_degree": row.get("academic_degree", ""),
                    "rate": row.get("rate", 0),
                    "is_active": row.get("is_active", True),
                },
            )
        return TemplateView.as_view(
            template_name=self.template_name,
            extra_context={"success": "Импорт успешно выполнен"},
        )(request)


class SubjectListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Subject
    template_name = "core/subject_list.html"
    allowed_roles = ["curator", "admin", "accountant", "teacher"]


class SubjectCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = "core/subject_form.html"
    success_url = reverse_lazy("core:subject_list")
    allowed_roles = ["curator", "admin"]


class SubjectUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = "core/subject_form.html"
    success_url = reverse_lazy("core:subject_list")
    allowed_roles = ["curator", "admin"]


class SubjectDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    model = Subject
    template_name = "core/subject_confirm_delete.html"
    success_url = reverse_lazy("core:subject_list")
    allowed_roles = ["curator", "admin"]


class StudyGroupListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = StudyGroup
    template_name = "core/group_list.html"
    allowed_roles = ["curator", "admin", "accountant", "teacher"]


class StudyGroupCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = StudyGroup
    form_class = StudyGroupForm
    template_name = "core/group_form.html"
    success_url = reverse_lazy("core:group_list")
    allowed_roles = ["curator", "admin"]


class StudyGroupUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = StudyGroup
    form_class = StudyGroupForm
    template_name = "core/group_form.html"
    success_url = reverse_lazy("core:group_list")
    allowed_roles = ["curator", "admin"]


class StudyGroupDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    model = StudyGroup
    template_name = "core/group_confirm_delete.html"
    success_url = reverse_lazy("core:group_list")
    allowed_roles = ["curator", "admin"]


class WorkloadListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Workload
    template_name = "core/workload_list.html"
    allowed_roles = ["curator", "admin", "teacher", "accountant"]

    def get_queryset(self):
        qs = super().get_queryset().select_related("teacher", "subject", "group")
        user = self.request.user

        # Ограничение для преподавателя: только его собственная нагрузка
        if user.role == "teacher":
            teacher_profile = getattr(user, "teacher_profile", None)
            if teacher_profile:
                qs = qs.filter(teacher=teacher_profile)
            else:
                return Workload.objects.none()

        # Просмотр по месяцам: берём месяц/год из query params или текущие
        today = date.today()
        try:
            month = int(self.request.GET.get("month", today.month))
        except (TypeError, ValueError):
            month = today.month
        try:
            year = int(self.request.GET.get("year", today.year))
        except (TypeError, ValueError):
            year = today.year

        month = min(max(month, 1), 12)

        qs = qs.filter(date__year=year, date__month=month)

        return qs.order_by("date", "pair_slot")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = date.today()

        try:
            month = int(self.request.GET.get("month", today.month))
        except (TypeError, ValueError):
            month = today.month
        try:
            year = int(self.request.GET.get("year", today.year))
        except (TypeError, ValueError):
            year = today.year

        month = min(max(month, 1), 12)
        current = date(year, month, 1)
        prev_month_date = (current.replace(day=1) - timedelta(days=1)).replace(day=1)
        next_month_date = (current.replace(day=28) + timedelta(days=4)).replace(day=1)

        months = [
            (1, "Январь"),
            (2, "Февраль"),
            (3, "Март"),
            (4, "Апрель"),
            (5, "Май"),
            (6, "Июнь"),
            (7, "Июль"),
            (8, "Август"),
            (9, "Сентябрь"),
            (10, "Октябрь"),
            (11, "Ноябрь"),
            (12, "Декабрь"),
        ]
        month_label = dict(months).get(month, "")

        ctx.update(
            {
                "current_month": month,
                "current_year": year,
                "current_month_label": month_label,
                "prev_month": prev_month_date.month,
                "prev_year": prev_month_date.year,
                "next_month": next_month_date.month,
                "next_year": next_month_date.year,
            }
        )

        return ctx


class WorkloadCalendarView(LoginRequiredMixin, RoleRequiredMixin, TemplateView):
    template_name = "core/workload_calendar.html"
    allowed_roles = ["teacher", "curator", "admin"]

    def _get_month_year(self):
        today = date.today()
        try:
            month = int(self.request.GET.get("month", today.month))
            year = int(self.request.GET.get("year", today.year))
        except (TypeError, ValueError):
            month, year = today.month, today.year
        month = min(max(month, 1), 12)
        return year, month

    def _month_bounds(self, first_day: date) -> tuple[date, date]:
        prev_month = (first_day.replace(day=1) - timedelta(days=1)).replace(day=1)
        next_month = (first_day.replace(day=28) + timedelta(days=4)).replace(day=1)
        return prev_month, next_month

    def get_queryset(self, year: int, month: int):
        qs = Workload.objects.filter(date__year=year, date__month=month).select_related("teacher", "subject", "group")
        user = self.request.user
        teacher_filter = self.request.GET.get("teacher")
        if user.role == "teacher":
            teacher_profile = getattr(user, "teacher_profile", None)
            return qs.filter(teacher=teacher_profile) if teacher_profile else Workload.objects.none()
        if teacher_filter:
            qs = qs.filter(teacher_id=teacher_filter)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        year, month = self._get_month_year()
        first_day = date(year, month, 1)
        prev_month, next_month = self._month_bounds(first_day)

        workloads = self.get_queryset(year, month)
        workloads_by_date: dict[date, list[Workload]] = defaultdict(list)
        for wl in workloads:
            workloads_by_date[wl.date].append(wl)

        calendar_iter = calendar.Calendar(firstweekday=0).itermonthdates(year, month)
        weeks = []
        week = []
        for day in calendar_iter:
            week.append(
                {
                    "date": day,
                    "in_month": day.month == month,
                    "workloads": workloads_by_date.get(day, []),
                }
            )
            if len(week) == 7:
                weeks.append(week)
                week = []
        if week:
            weeks.append(week)

        ctx.update(
            {
                "weeks": weeks,
                "current_month": first_day.strftime("%B %Y"),
                "month": month,
                "year": year,
                "prev_month": prev_month,
                "next_month": next_month,
                "selected_teacher": None,
            }
        )

        if self.request.user.role in ("curator", "admin"):
            ctx["teachers"] = Teacher.objects.select_related("user").all()
            teacher_filter = self.request.GET.get("teacher")
            if teacher_filter:
                ctx["selected_teacher"] = Teacher.objects.filter(pk=teacher_filter).first()

        return ctx


class WorkloadCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Workload
    form_class = WorkloadForm
    template_name = "core/workload_form.html"
    success_url = reverse_lazy("core:workload_list")
    allowed_roles = ["curator", "admin"]


class WorkloadUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Workload
    form_class = WorkloadForm
    template_name = "core/workload_form.html"
    success_url = reverse_lazy("core:workload_list")
    allowed_roles = ["curator", "admin"]


class WorkloadDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    model = Workload
    template_name = "core/workload_confirm_delete.html"
    success_url = reverse_lazy("core:workload_list")
    allowed_roles = ["curator", "admin"]


class TimesheetListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Timesheet
    template_name = "core/timesheet_list.html"
    allowed_roles = ["curator", "admin", "accountant", "teacher"]

    def get_queryset(self):
        qs = super().get_queryset().select_related("teacher", "subject", "group")
        user = self.request.user
        if user.role == "teacher":
            teacher_profile = getattr(user, "teacher_profile", None)
            if teacher_profile:
                return qs.filter(teacher=teacher_profile)
            return qs.none()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        
        # Подсчёт итоговых сумм
        total_lecture = sum(t.lecture_hours or 0 for t in queryset)
        total_practice = sum(t.practice_hours or 0 for t in queryset)
        total_lab = sum(t.lab_hours or 0 for t in queryset)
        total_hours = sum(t.total_hours or 0 for t in queryset)
        
        context["total_lecture"] = total_lecture
        context["total_practice"] = total_practice
        context["total_lab"] = total_lab
        context["total_hours"] = total_hours
        
        return context


class TimesheetCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Timesheet
    form_class = TimesheetForm
    template_name = "core/timesheet_form.html"
    success_url = reverse_lazy("core:timesheet_list")
    allowed_roles = ["curator", "admin", "accountant"]


class TimesheetUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Timesheet
    form_class = TimesheetForm
    template_name = "core/timesheet_form.html"
    success_url = reverse_lazy("core:timesheet_list")
    allowed_roles = ["curator", "admin", "accountant"]


class TimesheetDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    model = Timesheet
    template_name = "core/timesheet_confirm_delete.html"
    success_url = reverse_lazy("core:timesheet_list")
    allowed_roles = ["curator", "admin", "accountant"]


class TimesheetDetailView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
    model = Timesheet
    template_name = "core/timesheet_detail.html"
    allowed_roles = ["curator", "admin", "accountant", "teacher"]

    def get_queryset(self):
        qs = super().get_queryset().select_related("teacher", "subject", "group")
        user = self.request.user
        if user.role == "teacher":
            teacher_profile = getattr(user, "teacher_profile", None)
            if teacher_profile:
                return qs.filter(teacher=teacher_profile)
            return qs.none()
        return qs


class TimesheetPDFView(LoginRequiredMixin, RoleRequiredMixin, View):
    allowed_roles = ["curator", "admin", "accountant", "teacher"]

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        timesheet = get_object_or_404(Timesheet, pk=pk)
        if request.user.role == "teacher":
            teacher_profile = getattr(request.user, "teacher_profile", None)
            if not teacher_profile or timesheet.teacher != teacher_profile:
                return HttpResponse(status=403)
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)

        # Попытка подключить шрифт с поддержкой кириллицы
        font_name = "Helvetica"
        font_candidates = [
            os.path.join(getattr(settings, "BASE_DIR", ""), "static", "fonts", "DejaVuSans.ttf"),
            r"C:\Windows\Fonts\arial.ttf",
        ]
        for path in font_candidates:
            if os.path.exists(path):
                try:
                    pdfmetrics.registerFont(TTFont("CustomCyrillic", path))
                    font_name = "CustomCyrillic"
                    break
                except Exception:
                    continue

        pdf.setFont(font_name, 12)
        pdf.setTitle("Табель рабочего времени")
        pdf.drawString(50, 800, f"Табель рабочего времени: {timesheet.teacher.full_name}")
        pdf.drawString(50, 780, f"Дисциплина: {timesheet.subject.name if timesheet.subject else 'Не указана'}")
        pdf.drawString(50, 760, f"Группа: {timesheet.group.name if timesheet.group else 'Не указана'}")
        if timesheet.period_from and timesheet.period_to:
            pdf.drawString(50, 740, f"Период: {timesheet.period_from:%d.%m.%Y} - {timesheet.period_to:%d.%m.%Y}")
        elif timesheet.period:
            pdf.drawString(50, 740, f"Период: {timesheet.period:%m.%Y}")
        else:
            pdf.drawString(50, 740, "Период: Не указан")
        pdf.drawString(50, 720, f"Лекции: {timesheet.lecture_hours or 0} ч.")
        pdf.drawString(50, 700, f"Практика: {timesheet.practice_hours or 0} ч.")
        pdf.drawString(50, 680, f"Лабораторные: {timesheet.lab_hours or 0} ч.")
        pdf.drawString(50, 660, f"Итого: {timesheet.total_hours or 0} ч.")
        pdf.drawString(50, 640, f"Статус: {timesheet.get_status_display()}")
        pdf.showPage()
        pdf.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename="timesheet.pdf")


class TimesheetExcelView(LoginRequiredMixin, RoleRequiredMixin, View):
    allowed_roles = ["curator", "admin", "accountant", "teacher"]

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        timesheet = get_object_or_404(Timesheet, pk=pk)
        if request.user.role == "teacher":
            teacher_profile = getattr(request.user, "teacher_profile", None)
            if not teacher_profile or timesheet.teacher != teacher_profile:
                return HttpResponse(status=403)

        wb = Workbook()
        ws = wb.active
        ws.title = "Табель"

        ws.append(
            [
                "Преподаватель",
                "Дисциплина",
                "Группа",
                "Период",
                "Лекции (часы)",
                "Практика (часы)",
                "Лабораторные (часы)",
                "Итого (часы)",
                "Статус",
            ]
        )

        if timesheet.period_from and timesheet.period_to:
            period_display = f"{timesheet.period_from:%d.%m.%Y} - {timesheet.period_to:%d.%m.%Y}"
        elif getattr(timesheet, "period", None):
            period_display = timesheet.period.strftime("%m.%Y")
        else:
            period_display = "Не указан"

        ws.append(
            [
                timesheet.teacher.full_name if timesheet.teacher else "",
                timesheet.subject.name if timesheet.subject else "",
                timesheet.group.name if timesheet.group else "",
                period_display,
                float(timesheet.lecture_hours or 0),
                float(timesheet.practice_hours or 0),
                float(timesheet.lab_hours or 0),
                float(timesheet.total_hours or 0),
                timesheet.get_status_display(),
            ]
        )

        stream = io.BytesIO()
        wb.save(stream)
        stream.seek(0)

        response = HttpResponse(
            stream.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f'attachment; filename="timesheet_{timesheet.pk}.xlsx"'
        return response


class SalaryListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Salary
    template_name = "core/salary_list.html"
    allowed_roles = ["accountant", "admin", "curator", "teacher"]

    def get(self, request: HttpRequest, *args, **kwargs):
        if request.user.role == "teacher":
            return render(request, "core/salary_restricted.html")
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().select_related("teacher")


class SalaryCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Salary
    form_class = SalaryForm
    template_name = "core/salary_form.html"
    success_url = reverse_lazy("core:salary_list")
    allowed_roles = ["accountant", "admin"]

    def form_valid(self, form):
        # Если total_amount не задан явно — считаем как base_salary + bonus
        instance = form.save(commit=False)
        if instance.total_amount is None or instance.total_amount == 0:
            instance.total_amount = (instance.base_salary or 0) + (instance.bonus or 0)
        instance.save()
        return super().form_valid(form)


class SalaryUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Salary
    form_class = SalaryForm
    template_name = "core/salary_form.html"
    success_url = reverse_lazy("core:salary_list")
    allowed_roles = ["accountant", "admin"]

    def form_valid(self, form):
        instance = form.save(commit=False)
        if instance.total_amount is None or instance.total_amount == 0:
            instance.total_amount = (instance.base_salary or 0) + (instance.bonus or 0)
        instance.save()
        return super().form_valid(form)


class SalaryDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    model = Salary
    template_name = "core/salary_confirm_delete.html"
    success_url = reverse_lazy("core:salary_list")
    allowed_roles = ["accountant", "admin"]


class SalaryExportExcelView(LoginRequiredMixin, RoleRequiredMixin, View):
    allowed_roles = ["accountant", "admin"]

    def get(self, request: HttpRequest) -> HttpResponse:
        wb = Workbook()
        ws = wb.active
        ws.title = "Зарплаты"
        ws.append(["Преподаватель", "Период", "Базовая", "Премия", "Итого"])
        for salary in Salary.objects.select_related("teacher").all():
            ws.append(
                [
                    salary.teacher.full_name,
                    salary.period.strftime("%m.%Y"),
                    float(salary.base_salary),
                    float(salary.bonus),
                    float(salary.total_amount),
                ]
            )
        stream = io.BytesIO()
        wb.save(stream)
        stream.seek(0)
        response = HttpResponse(
            stream.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = 'attachment; filename="salaries.xlsx"'
        return response


class MyTimesheetListView(LoginRequiredMixin, ListView):
    model = Timesheet
    template_name = "core/my_timesheets.html"

    def get_queryset(self):
        return Timesheet.objects.filter(teacher__user=self.request.user)


class MySalaryListView(LoginRequiredMixin, ListView):
    model = Salary
    template_name = "core/my_salaries.html"

    def get_queryset(self):
        return Salary.objects.filter(teacher__user=self.request.user)


class FeedbackCreateView(LoginRequiredMixin, CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = "core/feedback_form.html"
    success_url = reverse_lazy("core:feedback_submit")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Спасибо! Ваше сообщение отправлено администратору.")
        return super().form_valid(form)


class FeedbackListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Feedback
    template_name = "core/feedback_list.html"
    allowed_roles = ["admin"]


class FeedbackUpdateStatusView(LoginRequiredMixin, RoleRequiredMixin, View):
    allowed_roles = ["admin"]

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        feedback = get_object_or_404(Feedback, pk=pk)
        new_status = request.POST.get("status")
        valid_statuses = {choice[0] for choice in Feedback.STATUS_CHOICES}
        if new_status in valid_statuses:
            feedback.status = new_status
            feedback.save(update_fields=["status"])
            messages.success(request, "Статус сообщения обновлён.")
        return redirect("core:feedback_inbox")


class FeedbackDeleteView(LoginRequiredMixin, RoleRequiredMixin, View):
    allowed_roles = ["admin"]

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        feedback = get_object_or_404(Feedback, pk=pk)
        feedback.delete()
        messages.success(request, "Сообщение удалено.")
        return redirect("core:feedback_inbox")


class ChatView(LoginRequiredMixin, RoleRequiredMixin, View):
    allowed_roles = ["teacher", "curator", "admin"]
    template_name = "core/chat.html"

    def get_contacts(self, user):
        """Получить список контактов (кураторы и преподаватели)."""
        if user.role == "teacher":
            return User.objects.filter(role__in=["curator", "admin"]).order_by("username")
        elif user.role in ["curator", "admin"]:
            return User.objects.filter(role__in=["teacher", "curator", "admin"]).exclude(pk=user.pk).order_by("username")
        return User.objects.none()

    def get(self, request: HttpRequest) -> HttpResponse:
        user = request.user
        contacts = self.get_contacts(user)
        contact_id = request.GET.get("contact")
        selected_contact = None
        chat_messages = Message.objects.none()
        unread_map = {}

        if contact_id:
            try:
                selected_contact = User.objects.get(pk=contact_id, role__in=["teacher", "curator", "admin"])
                chat_messages = Message.objects.filter(
                    Q(sender=user, recipient=selected_contact) | Q(sender=selected_contact, recipient=user)
                ).select_related("sender", "recipient").order_by("created_at")
            except User.DoesNotExist:
                pass

        # Подсчет непрочитанных
        for contact in contacts:
            count = Message.objects.filter(sender=contact, recipient=user, is_read=False).count()
            if count > 0:
                unread_map[contact.id] = count

        form = MessageForm(user=user)
        if selected_contact:
            form.fields["recipient"].initial = selected_contact

        return render(
            request,
            self.template_name,
            {
                "contacts": contacts,
                "selected_contact": selected_contact,
                "chat_messages": chat_messages,
                "form": form,
                "unread_map": unread_map,
            },
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        user = request.user
        form = MessageForm(request.POST, user=user)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = user
            message.save()
            messages.success(request, "Сообщение отправлено.")
            return redirect(f"{reverse_lazy('core:chat')}?contact={message.recipient.id}")
        contacts = self.get_contacts(user)
        contact_id = request.GET.get("contact")
        selected_contact = None
        if contact_id:
            try:
                selected_contact = User.objects.get(pk=contact_id)
            except User.DoesNotExist:
                pass
        return render(request, self.template_name, {"contacts": contacts, "selected_contact": selected_contact, "form": form})

