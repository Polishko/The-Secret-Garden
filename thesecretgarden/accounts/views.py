from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, View

from thesecretgarden.accounts.forms import AppUserCreateForm, AppUserLoginForm, ProfileEditForm
from thesecretgarden.accounts.models import Profile
from thesecretgarden.mixins import IsUserProfileOwnerMixin, RedirectAuthenticatedUsersMixin
from thesecretgarden.orders.models import Order

UserModel = get_user_model()

class AppUserLoginView(RedirectAuthenticatedUsersMixin, LoginView):
    template_name = 'accounts/login-page.html'
    form_class = AppUserLoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exclude_user_options'] = True

        return context


class AppUserRegisterView(RedirectAuthenticatedUsersMixin, CreateView):
    model = UserModel
    form_class = AppUserCreateForm
    template_name = 'accounts/register-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exclude_user_options'] = True

        return context

    def get_success_url(self):
        profile = self.object.profile
        if profile.is_complete():
            return reverse_lazy('plants-list')
        else:
            return reverse_lazy('profile-edit', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        super().form_valid(form)
        login(self.request, self.object)
        return redirect(self.get_success_url())


class ProfileDetailsView(LoginRequiredMixin, IsUserProfileOwnerMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile-details.html'

    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.request.user.is_staff:
            context['completed_orders'] = Order.objects.filter(
                user=self.request.user,
                status='completed',
                is_active=False
            )
        else:
            context['completed_orders'] = []
        return context


class ProfileEditView(LoginRequiredMixin, IsUserProfileOwnerMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit.html'

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'slug': self.object.user.slug})


class ProfileDeactivateView(LoginRequiredMixin, IsUserProfileOwnerMixin, View):
    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        return render(request, 'accounts/profile-deactivate-confirm.html',
                      {'slug': self.kwargs['slug'], 'profile': profile})

    def post(self, request, *args, **kwargs):
        profile = self.get_object()
        profile.is_active = False
        profile.save()
        return HttpResponseRedirect(reverse_lazy('login'))
