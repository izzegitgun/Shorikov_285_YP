from django.contrib import admin

from .models import Teacher, Subject, StudyGroup, Workload, Timesheet, Salary, Feedback, Message


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("full_name", "position", "academic_degree", "rate", "is_active")
    list_filter = ("is_active", "position", "academic_degree")
    search_fields = ("full_name",)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "code")


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(Workload)
class WorkloadAdmin(admin.ModelAdmin):
    list_display = ("teacher", "subject", "group", "date", "activity_type", "pair_slot")
    list_filter = ("activity_type", "date", "subject", "group", "pair_slot")
    search_fields = ("teacher__full_name", "subject__name", "group__name")


@admin.register(Timesheet)
class TimesheetAdmin(admin.ModelAdmin):
    list_display = ("teacher", "subject", "group", "period_from", "period_to", "total_hours", "status")
    list_filter = ("status", "period_from", "subject", "group")
    search_fields = ("teacher__full_name", "subject__name", "group__name")


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ("teacher", "period", "base_salary", "bonus", "total_amount")
    list_filter = ("period",)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("subject", "user", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("subject", "message", "user__username")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "recipient", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("sender__username", "recipient__username", "body")


