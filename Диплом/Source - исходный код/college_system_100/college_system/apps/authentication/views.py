from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View

from .forms import UserProfileForm, UserManageForm
from .models import User


@login_required
def profile_view(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy("authentication:profile"))
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, "authentication/profile.html", {"form": form})


class AdminOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("account_login")
        if not (request.user.is_superuser or request.user.role == User.Roles.ADMIN):
            return redirect("core:dashboard")
        return super().dispatch(request, *args, **kwargs)


class UserListView(AdminOnlyMixin, View):
    template_name = "authentication/user_list.html"

    def get(self, request):
        users = User.objects.all().order_by("username")
        return render(request, self.template_name, {"users": users})


class UserUpdateView(AdminOnlyMixin, View):
    template_name = "authentication/user_form.html"
    success_url = reverse_lazy("authentication:user_list")

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = UserManageForm(instance=user)
        return render(request, self.template_name, {"form": form, "user_obj": user})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = UserManageForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {"form": form, "user_obj": user})


class UserDeleteView(AdminOnlyMixin, View):
    success_url = reverse_lazy("authentication:user_list")

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user.pk == request.user.pk:
            return redirect(self.success_url)
        user.delete()
        return redirect(self.success_url)


