from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    # Teachers (куратор)
    path("teachers/", views.TeacherListView.as_view(), name="teacher_list"),
    path("teachers/create/", views.TeacherCreateView.as_view(), name="teacher_create"),
    path("teachers/<int:pk>/", views.TeacherDetailView.as_view(), name="teacher_detail"),
    path("teachers/<int:pk>/edit/", views.TeacherUpdateView.as_view(), name="teacher_edit"),
    path("teachers/<int:pk>/delete/", views.TeacherDeleteView.as_view(), name="teacher_delete"),
    path("teachers/import/", views.TeacherImportView.as_view(), name="teacher_import"),
    # Subjects
    path("subjects/", views.SubjectListView.as_view(), name="subject_list"),
    path("subjects/create/", views.SubjectCreateView.as_view(), name="subject_create"),
    path("subjects/<int:pk>/edit/", views.SubjectUpdateView.as_view(), name="subject_edit"),
    path("subjects/<int:pk>/delete/", views.SubjectDeleteView.as_view(), name="subject_delete"),
    # Study groups
    path("groups/", views.StudyGroupListView.as_view(), name="group_list"),
    path("groups/create/", views.StudyGroupCreateView.as_view(), name="group_create"),
    path("groups/<int:pk>/edit/", views.StudyGroupUpdateView.as_view(), name="group_edit"),
    path("groups/<int:pk>/delete/", views.StudyGroupDeleteView.as_view(), name="group_delete"),
    # Workload
    path("workloads/", views.WorkloadListView.as_view(), name="workload_list"),
    path("workloads/calendar/", views.WorkloadCalendarView.as_view(), name="workload_calendar"),
    path("workloads/create/", views.WorkloadCreateView.as_view(), name="workload_create"),
    path("workloads/<int:pk>/edit/", views.WorkloadUpdateView.as_view(), name="workload_edit"),
    path("workloads/<int:pk>/delete/", views.WorkloadDeleteView.as_view(), name="workload_delete"),
    # Timesheets
    path("timesheets/", views.TimesheetListView.as_view(), name="timesheet_list"),
    path("timesheets/create/", views.TimesheetCreateView.as_view(), name="timesheet_create"),
    path("timesheets/<int:pk>/", views.TimesheetDetailView.as_view(), name="timesheet_detail"),
    path("timesheets/<int:pk>/edit/", views.TimesheetUpdateView.as_view(), name="timesheet_edit"),
    path("timesheets/<int:pk>/delete/", views.TimesheetDeleteView.as_view(), name="timesheet_delete"),
    path("timesheets/<int:pk>/pdf/", views.TimesheetPDFView.as_view(), name="timesheet_pdf"),
    path("timesheets/<int:pk>/excel/", views.TimesheetExcelView.as_view(), name="timesheet_excel"),
    # Salary
    path("salaries/", views.SalaryListView.as_view(), name="salary_list"),
    path("salaries/create/", views.SalaryCreateView.as_view(), name="salary_create"),
    path("salaries/<int:pk>/edit/", views.SalaryUpdateView.as_view(), name="salary_edit"),
    path("salaries/<int:pk>/delete/", views.SalaryDeleteView.as_view(), name="salary_delete"),
    path("salaries/export/", views.SalaryExportExcelView.as_view(), name="salary_export"),
    # Teacher self-service
    path("my/timesheets/", views.MyTimesheetListView.as_view(), name="my_timesheets"),
    path("my/salaries/", views.MySalaryListView.as_view(), name="my_salaries"),
    # Feedback
    path("feedback/new/", views.FeedbackCreateView.as_view(), name="feedback_submit"),
    path("feedback/inbox/", views.FeedbackListView.as_view(), name="feedback_inbox"),
    path("feedback/<int:pk>/status/", views.FeedbackUpdateStatusView.as_view(), name="feedback_status"),
    path("feedback/<int:pk>/delete/", views.FeedbackDeleteView.as_view(), name="feedback_delete"),
    # Chat
    path("chat/", views.ChatView.as_view(), name="chat"),
]

