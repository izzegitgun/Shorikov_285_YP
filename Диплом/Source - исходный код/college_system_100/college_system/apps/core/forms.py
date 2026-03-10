from decimal import Decimal

from django import forms

from .models import Teacher, Subject, StudyGroup, Workload, Timesheet, Salary, Feedback, Message


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ["user", "full_name", "position", "academic_degree", "rate", "is_active"]
        labels = {
            "user": "Пользователь (учётная запись)",
            "full_name": "ФИО преподавателя",
            "position": "Должность",
            "academic_degree": "Учёная степень",
            "rate": "Ставка",
            "is_active": "Активен",
        }
        widgets = {
            "user": forms.Select(attrs={"class": "form-select"}),
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "position": forms.TextInput(attrs={"class": "form-control"}),
            "academic_degree": forms.TextInput(attrs={"class": "form-control"}),
            "rate": forms.NumberInput(attrs={"class": "form-select"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name", "code", "description", "is_active"]
        labels = {
            "name": "Название предмета",
            "code": "Код (по учебному плану)",
            "description": "Описание",
            "is_active": "Активен",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "code": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class StudyGroupForm(forms.ModelForm):
    class Meta:
        model = StudyGroup
        fields = ["name", "is_active"]


class WorkloadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["group"].required = True
        self.fields["pair_slot"].required = True

    class Meta:
        model = Workload
        fields = ["teacher", "subject", "group", "date", "activity_type", "pair_slot", "description"]
        labels = {
            "teacher": "Преподаватель",
            "subject": "Дисциплина",
            "group": "Группа",
            "date": "Дата",
            "activity_type": "Вид занятия",
            "pair_slot": "Пара",
            "description": "Описание",
        }
        widgets = {
            "teacher": forms.Select(attrs={"class": "form-select"}),
            "subject": forms.Select(attrs={"class": "form-select"}),
            "group": forms.Select(attrs={"class": "form-select"}),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "activity_type": forms.Select(attrs={"class": "form-select"}),
            "pair_slot": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }


class TimesheetForm(forms.ModelForm):
    class Meta:
        model = Timesheet
        fields = ["teacher", "subject", "group", "period_from", "period_to", "lecture_hours", "practice_hours", "lab_hours", "status"]
        widgets = {
            "period_from": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "period_to": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "lecture_hours": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "practice_hours": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "lab_hours": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "subject": forms.Select(attrs={"class": "form-select"}),
            "group": forms.Select(attrs={"class": "form-select"}),
            "teacher": forms.Select(attrs={"class": "form-select"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "subject": "Дисциплина",
            "group": "Группа",
            "period_from": "Период с",
            "period_to": "Период до",
            "lecture_hours": "Часы за лекции",
            "practice_hours": "Часы за практику",
            "lab_hours": "Часы за лабораторные работы",
            "teacher": "Преподаватель",
            "status": "Статус",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subject"].queryset = Subject.objects.filter(is_active=True)
        self.fields["group"].queryset = StudyGroup.objects.filter(is_active=True)
        # Делаем поля обязательными в форме
        self.fields["subject"].required = True
        self.fields["group"].required = True
        self.fields["period_from"].required = True
        self.fields["period_to"].required = True
        self.fields["lecture_hours"].required = True
        self.fields["practice_hours"].required = True
        self.fields["lab_hours"].required = True
        self.fields["total_hours"] = forms.DecimalField(
            max_digits=8,
            decimal_places=2,
            required=False,
            widget=forms.NumberInput(attrs={"class": "form-control", "readonly": True, "id": "id_total_hours"}),
            label="Итого",
        )
        if self.instance and self.instance.pk:
            self.fields["total_hours"].initial = self.instance.total_hours

    def clean(self):
        cleaned_data = super().clean()
        period_from = cleaned_data.get("period_from")
        period_to = cleaned_data.get("period_to")
        lecture_hours = cleaned_data.get("lecture_hours") or 0
        practice_hours = cleaned_data.get("practice_hours") or 0
        lab_hours = cleaned_data.get("lab_hours") or 0

        # Валидация дат
        if period_from and period_to:
            if period_from > period_to:
                raise forms.ValidationError({"period_to": "Дата 'до' должна быть позже или равна дате 'с'."})

        # Валидация числовых полей
        if lecture_hours < 0:
            raise forms.ValidationError({"lecture_hours": "Часы за лекции не могут быть отрицательными."})
        if practice_hours < 0:
            raise forms.ValidationError({"practice_hours": "Часы за практику не могут быть отрицательными."})
        if lab_hours < 0:
            raise forms.ValidationError({"lab_hours": "Часы за лабораторные работы не могут быть отрицательными."})

        # Автоматический подсчёт итого
        cleaned_data["total_hours"] = lecture_hours + practice_hours + lab_hours

        return cleaned_data

    def save(self, commit: bool = True):
        instance = super().save(commit=False)
        # Подсчёт итого уже выполнен в clean()
        instance.total_hours = self.cleaned_data.get("total_hours", 0)
        if commit:
            instance.save()
        return instance


class SalaryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["total_amount"].widget.attrs["readonly"] = True

    class Meta:
        model = Salary
        fields = ["teacher", "period", "base_salary", "bonus", "total_amount"]

    def clean(self):
        cleaned_data = super().clean()
        base = cleaned_data.get("base_salary")
        bonus = cleaned_data.get("bonus")
        if base is not None and bonus is not None:
            cleaned_data["total_amount"] = base + bonus
        return cleaned_data

    def save(self, commit: bool = True):
        instance = super().save(commit=False)
        base = self.cleaned_data.get("base_salary") or Decimal("0")
        bonus = self.cleaned_data.get("bonus") or Decimal("0")
        instance.total_amount = base + bonus
        if commit:
            instance.save()
        return instance


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["subject", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 4}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["recipient", "body"]
        widgets = {
            "body": forms.Textarea(attrs={"rows": 3, "class": "form-control", "placeholder": "Введите сообщение..."}),
            "recipient": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "recipient": "Получатель",
            "body": "Сообщение",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            from apps.authentication.models import User
            if user.role == "teacher":
                self.fields["recipient"].queryset = User.objects.filter(role__in=["curator", "admin"])
            elif user.role in ["curator", "admin"]:
                self.fields["recipient"].queryset = User.objects.filter(role__in=["teacher", "curator", "admin"]).exclude(pk=user.pk)


